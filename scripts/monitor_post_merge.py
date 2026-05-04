#!/usr/bin/env python3
"""
monitor_post_merge.py — Post-merge production monitoring for Sprint 2.

Designed to run at: T+0 (merge), T+1h, T+4h, T+24h.

Tests ~50 critical URLs on https://wiggmap.com:
  - 39 migrated lang-dir URLs (must return 200 with correct canonical/lang/hreflang)
  - 14 legacy URLs (must 301 to /en/* or /fr/*)
  - Query-string-preserving redirect on /compare.html?c=...
  - sitemap.xml + robots.txt + manifest.webmanifest (must be 200)
  - Service Worker version (must be wiggmap-v3)
  - Sprint 1 non-regression on /en/ (bc.webp preload, skip-link, theme-color)

Output: human-readable summary to stdout, machine-readable JSON to
monitor_post_merge_{timestamp}.json (writable to /tmp by default).

Behaviour
---------
  - Returns exit 0 if every check passes.
  - Returns exit 1 if ANY check fails (CI-friendly).
  - Detailed failure reasons printed inline.
  - Designed to be safe to re-run: read-only HTTP, no side effects.

USAGE
-----
  python3 scripts/monitor_post_merge.py
  python3 scripts/monitor_post_merge.py --base https://deploy-preview-1--phenomenal-zabaione-d26a6d.netlify.app  # test on preview first
  python3 scripts/monitor_post_merge.py --json /tmp/monitor.json   # custom output path
  python3 scripts/monitor_post_merge.py --quiet                    # only errors + summary
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG (must match MIGRATION_PLAN.md §1.1 D4/D5)
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_BASE = "https://wiggmap.com"
TIMEOUT = 12  # seconds per request
USER_AGENT = "wiggmap-monitor/1.0 (+post-merge audit)"

LANGS = ["en", "fr", "es"]

# Sprint 2 — 13 root pages migrated to /en/, /fr/, /es/ (per migrate_to_lang_dirs.py).
# Sprint D1 — wiggmatch added as EN-source (per build_wiggmatch_trilingual.py).
EN_SOURCE = [
    "index.html", "about.html", "compare.html", "globe.html",
    "indexchronicles.html", "terms.html", "privacy.html", "confirmation.html",
    "wiggmatch.html",  # Sprint D1
]
FR_SOURCE = [
    "chronicles-villes.html", "chronicles-dest.html", "chronicles-family.html",
    "chronicles-horizons.html", "chronicles-visas.html",
]
SOURCE_LANG = {**{p: "en" for p in EN_SOURCE}, **{p: "fr" for p in FR_SOURCE}}
ALL_PAGES = list(SOURCE_LANG.keys())

# Sprint D1 — wiggmatch is treated as EN-source per D4 (each lang variant is its
# own source — no untranslated banner, no noindex,follow). The check_migrated_pages
# helper uses SOURCE_LANG to decide; for wiggmatch we override that behaviour
# because all 3 langs are real translations (WM_I18N + WM_DYN dictionaries).
WIGGMATCH_ALL_LANGS_SOURCE = True

# Legacy URLs that should 301 to their migrated targets
LEGACY_REDIRECTS = [
    ("/", "/en/"),
    ("/index.html", "/en/"),
    ("/about.html", "/en/about.html"),
    ("/compare.html", "/en/compare.html"),
    ("/compare.html?c=thailand,indonesia,portugal", "/en/compare.html?c=thailand,indonesia,portugal"),
    ("/globe.html", "/en/globe.html"),
    ("/indexchronicles.html", "/en/indexchronicles.html"),
    ("/terms.html", "/en/terms.html"),
    ("/privacy.html", "/en/privacy.html"),
    ("/confirmation.html", "/en/confirmation.html"),
    ("/chronicles-villes.html", "/fr/chronicles-villes.html"),
    ("/chronicles-dest.html", "/fr/chronicles-dest.html"),
    ("/chronicles-family.html", "/fr/chronicles-family.html"),
    ("/chronicles-horizons.html", "/fr/chronicles-horizons.html"),
    ("/chronicles-visas.html", "/fr/chronicles-visas.html"),
    ("/wiggmatch.html", "/fr/wiggmatch.html"),
]

# Slug-lang URLs that must continue to work flat (sample — full coverage too noisy).
# Sprint X — LP + lead-magnet trilingual coverage extended:
# - 3 LP slugs × 3 langs = 9 URLs (lp/{slug}-{lang}.html)
# - 1 lead-magnet slug × 3 langs = 3 URLs (lead-magnet/visas-2026-{lang}.html)
# Lead-magnet noindex'd → status 200 still expected (Netlify serves the file,
# noindex only tells search engines to skip indexing; users + monitor still
# get a 200).
FLAT_TRILINGUAL_SAMPLE = [
    # countries (1 slug × 3 langs sample)
    "/countries/portugal-en.html",
    "/countries/portugal-fr.html",
    "/countries/portugal-es.html",
    # chronicles villes (1 slug × 3 langs sample)
    "/chronicles/villes/chronicle-bali-indonesia-en.html",
    "/chronicles/villes/chronicle-bali-indonesia-fr.html",
    "/chronicles/villes/chronicle-bali-indonesia-es.html",
    # chronicles thématiques (1 sample)
    "/chronicles/chronicle-digital-nomad-visas-2026-en.html",
    # compare/static (1 sample)
    "/compare/static/portugal-vs-spain/",
    # LP — Sprint X full trilingual coverage (3 slugs × 3 langs)
    "/lp/vivre-bali-budget-en.html",
    "/lp/vivre-bali-budget-fr.html",
    "/lp/vivre-bali-budget-es.html",
    "/lp/visa-mm2h-malaisie-en.html",
    "/lp/visa-mm2h-malaisie-fr.html",
    "/lp/visa-mm2h-malaisie-es.html",
    "/lp/erasmus-prague-budget-en.html",
    "/lp/erasmus-prague-budget-fr.html",
    "/lp/erasmus-prague-budget-es.html",
    # Lead-magnet — Sprint X full trilingual coverage
    "/lead-magnet/visas-2026-en.html",
    "/lead-magnet/visas-2026-fr.html",
    "/lead-magnet/visas-2026-es.html",
]

# Misc resources
MISC_200 = [
    "/sitemap.xml",
    "/robots.txt",
    "/manifest.webmanifest",
    "/sw.js",
    "/_headers",  # Netlify usually returns 404 here in prod (file isn't served), tolerated
]


# ─────────────────────────────────────────────────────────────────────────────
# HTTP helper
# ─────────────────────────────────────────────────────────────────────────────

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Forbid auto-following redirects so we can inspect them."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        return None


def fetch(base: str, path: str, follow: bool = False) -> tuple[int, dict, str]:
    """Return (status, headers_dict, body). Never raises."""
    url = base + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(_NoRedirect)
        resp = opener.open(req, timeout=TIMEOUT)
        body = resp.read().decode("utf-8", errors="replace")
        return resp.getcode(), dict(resp.headers), body
    except urllib.error.HTTPError as e:
        # Redirect responses come through as HTTPError when not following
        if e.code in (301, 302, 303, 307, 308):
            return e.code, dict(e.headers), ""
        return e.code, {}, ""
    except Exception as e:
        return 0, {"_error": str(e)}, ""


def normalize_location(loc: str) -> str:
    """Strip scheme+host so we compare paths."""
    return re.sub(r"^https?://[^/]+", "", loc or "")


# ─────────────────────────────────────────────────────────────────────────────
# CHECKS
# ─────────────────────────────────────────────────────────────────────────────

def check_migrated_pages(base: str) -> list[dict]:
    """Each /en/*, /fr/*, /es/* page must 200 with correct canonical / lang."""
    rows = []
    for page in ALL_PAGES:
        src = SOURCE_LANG[page]
        # Sprint D1 — wiggmatch is fully translated in all 3 langs (real
        # WM_I18N + WM_DYN translations, not the "untranslated banner"
        # fallback). Treat each lang variant as its own source.
        all_langs_source = (page == "wiggmatch.html" and WIGGMATCH_ALL_LANGS_SOURCE)
        for lg in LANGS:
            path = f"/{lg}/" if page == "index.html" else f"/{lg}/{page}"
            status, _, body = fetch(base, path)
            issues = []
            if status != 200:
                issues.append(f"status={status} (expected 200)")
            html_lang = (re.search(r'<html\s+lang="([^"]+)"', body) or [None, None])[1]
            if html_lang != lg:
                issues.append(f"html lang={html_lang} (expected {lg})")
            canon = (re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', body) or [None, None])[1]
            if all_langs_source:
                # Each lang is its own canonical
                expected_canon_lang = lg
            else:
                expected_canon_lang = lg if lg == src else src
            expected_canon = f"{DEFAULT_BASE}/{expected_canon_lang}/" if page == "index.html" else f"{DEFAULT_BASE}/{expected_canon_lang}/{page}"
            if canon != expected_canon:
                issues.append(f"canonical={canon} (expected {expected_canon})")
            is_translated = all_langs_source or (lg == src)
            has_noindex = bool(re.search(r'<meta\s+name="robots"\s+content="noindex,follow"', body))
            has_banner = "wm-untranslated-banner" in body
            if is_translated and (has_noindex or has_banner):
                issues.append("source-lang variant carries noindex/banner")
            if (not is_translated) and not (has_noindex and has_banner):
                issues.append("untranslated variant missing noindex+banner")
            rows.append({
                "check": "migrated",
                "path": path,
                "ok": len(issues) == 0,
                "status": status,
                "issues": issues,
            })
    return rows


def check_legacy_redirects(base: str) -> list[dict]:
    """Legacy /about.html etc. must 301 to their migrated targets,
    AND the redirect target must itself return 200.

    The "target → 200" check was missing in the initial Sprint 2 monitor;
    its absence allowed a regression to slip through (Sprint 2 _redirects
    pointed /wiggmatch.html → /fr/wiggmatch.html but the target file
    didn't exist → users got 404 chained from a 301). Hotfix a0d4149
    restored the file; this check prevents the class of bug from coming
    back unnoticed.
    """
    rows = []
    for src, expected_loc in LEGACY_REDIRECTS:
        status, hdrs, _ = fetch(base, src)
        loc = normalize_location(hdrs.get("Location") or hdrs.get("location") or "")
        issues = []
        if status != 301:
            issues.append(f"status={status} (expected 301)")
        if loc != expected_loc:
            issues.append(f"location={loc} (expected {expected_loc})")
        # NEW (post-Sprint D1 hotfix lesson): verify the redirect target itself
        # returns 200. If a 301 points to a 404, the user experience is just as
        # broken as a missing redirect — and the 301 alone wouldn't surface it.
        # We follow at most one hop so the check is cheap and unambiguous.
        if status == 301 and loc:
            # Strip query string from target for the existence probe — we just
            # want to know the resource exists. Query-preserving redirects are
            # tested separately in check_query_preservation.
            target_path = loc.split("?", 1)[0].split("#", 1)[0]
            target_status, _, _ = fetch(base, target_path, follow=False)
            if target_status not in (200, 301, 308):
                issues.append(f"redirect target {target_path} returned {target_status} (expected 200)")
        rows.append({
            "check": "legacy",
            "path": src,
            "ok": len(issues) == 0,
            "status": status,
            "issues": issues,
        })
    return rows


def check_flat_trilingual(base: str) -> list[dict]:
    """Slug-lang pages (countries, chronicles, lp, compare/static) must keep 200."""
    rows = []
    for path in FLAT_TRILINGUAL_SAMPLE:
        status, _, _ = fetch(base, path, follow=True)  # follow because compare/static may have trailing-slash redirects
        rows.append({
            "check": "flat",
            "path": path,
            "ok": status == 200,
            "status": status,
            "issues": [] if status == 200 else [f"status={status} (expected 200)"],
        })
    return rows


def check_misc_resources(base: str) -> list[dict]:
    """sitemap.xml, robots.txt, manifest, sw.js must 200. /_headers tolerated as 404."""
    rows = []
    for path in MISC_200:
        status, _, body = fetch(base, path, follow=True)
        ok = (status == 200) or (path == "/_headers" and status in (200, 404))
        issues = [] if ok else [f"status={status}"]
        # Spot-check sitemap content. /sitemap.xml became a sitemap-index in
        # commit ae3e5ea referencing 4 sub-sitemaps. If we see <sitemapindex>,
        # fetch each <loc> sub-sitemap and sum their URL counts. Otherwise
        # treat as a legacy single-sitemap and count <url> directly.
        if path == "/sitemap.xml" and status == 200:
            if "<sitemapindex" in body:
                sub_locs = re.findall(r"<loc>(https?://[^<]+/sitemap-[^<]+\.xml)</loc>", body)
                total = 0
                for sub in sub_locs:
                    sub_path = re.sub(r"^https?://[^/]+", "", sub)
                    _, _, sub_body = fetch(base, sub_path, follow=True)
                    total += sub_body.count("<url>")
                url_count = total
            else:
                url_count = body.count("<url>")
            if url_count < 900:
                ok = False
                issues.append(f"sitemap url count={url_count} (expected ~922)")
        # Spot-check sw.js
        if path == "/sw.js" and status == 200 and "wiggmap-v3" not in body:
            ok = False
            issues.append("CACHE_NAME != wiggmap-v3")
        rows.append({
            "check": "misc",
            "path": path,
            "ok": ok,
            "status": status,
            "issues": issues,
        })
    return rows


def check_sprint1_no_regression(base: str) -> list[dict]:
    """On /en/, confirm Sprint 1 wins (bc.webp preload, skip-link, theme-color)."""
    status, _, body = fetch(base, "/en/")
    issues = []
    if status != 200:
        issues.append(f"/en/ status={status}")
    if not re.search(r'<link\s+rel="preload"\s+as="image"\s+href="/assets/bc\.webp"', body):
        issues.append("bc.webp preload missing")
    if 'fetchpriority="high"' not in body:
        issues.append("fetchpriority=high missing on preload")
    if 'class="wm-skip"' not in body:
        issues.append("skip-link missing")
    if 'id="wm-main"' not in body:
        issues.append("wm-main anchor missing")
    tc = (re.search(r'<meta\s+name="theme-color"\s+content="([^"]+)"', body) or [None, None])[1]
    if tc != "#1a5430":
        issues.append(f"theme-color={tc} (expected #1a5430)")
    return [{
        "check": "sprint1",
        "path": "/en/",
        "ok": len(issues) == 0,
        "status": status,
        "issues": issues,
    }]


def check_query_preservation(base: str) -> list[dict]:
    """The /compare.html?c=... case is the trickiest — must 301 with query."""
    test_url = "/compare.html?c=thailand,indonesia,portugal"
    status, hdrs, _ = fetch(base, test_url)
    loc = normalize_location(hdrs.get("Location") or hdrs.get("location") or "")
    issues = []
    if status != 301:
        issues.append(f"status={status} (expected 301)")
    if "/en/compare.html" not in loc:
        issues.append(f"location={loc} (expected /en/compare.html?c=...)")
    if "c=thailand,indonesia,portugal" not in loc and "c=thailand%2Cindonesia%2Cportugal" not in loc:
        issues.append(f"query string lost: location={loc}")
    return [{
        "check": "query",
        "path": test_url,
        "ok": len(issues) == 0,
        "status": status,
        "issues": issues,
    }]


def check_sprint_y_perf(base: str) -> list[dict]:
    """Sprint Y.5 perf gate: country pages must serve <picture> SSR with
    a webp source, AND opt out of the runtime swap. Catches regressions
    where someone removes the <picture> wrapper or the opt-out flag.

    Spot-checks 1 country page per region (random sample would be ideal
    but deterministic = reproducible runs).
    """
    rows = []
    samples = [
        "/countries/portugal-en.html",
        "/countries/japan-en.html",
        "/countries/mexico-en.html",
    ]
    for path in samples:
        _, _, body = fetch(base, path)
        issues = []
        # 1. <picture> wrapper around hero
        if "<picture>" not in body:
            issues.append("<picture> SSR missing")
        # 2. webp source declared
        if 'type="image/webp"' not in body:
            issues.append("WebP <source> missing")
        # 3. opt-out flag set (otherwise footer.js runtime swap fires
        #    redundantly and adds ~33 fetches per page)
        if "__WM_DISABLE_WEBP_SWAP" not in body:
            issues.append("opt-out flag missing — runtime swap will fire")
        rows.append({
            "check": "perf-y5",
            "path": path,
            "ok": len(issues) == 0,
            "issues": issues,
        })
    return rows


def check_compare_paths(base: str) -> list[dict]:
    """Hotfix 9fdfb9b regression gate: compare.html files must use
    absolute paths for /data/countries.json + /data/header.js + /assets/
    (relative paths broke the page on /en/, /fr/, /es/ migrated copies)."""
    rows = []
    samples = [
        "/compare.html",  # 301 → /en/compare.html
        "/en/compare.html",
        "/fr/compare.html",
        "/es/compare.html",
    ]
    for path in samples:
        # follow redirect for /compare.html (301 → /en/compare.html)
        _, _, body = fetch(base, path, follow=True)
        issues = []
        # 1. absolute /data/countries.json fetch
        if 'fetch("/data/countries' not in body and "fetch('/data/countries" not in body:
            # may be templated as `_cf` constant — accept either
            if '"/data/countries' not in body and "'/data/countries" not in body:
                issues.append("countries.json fetch path not absolute")
        # 2. absolute /data/header.js script
        if 'src="/data/header.js"' not in body:
            issues.append("/data/header.js src not absolute (header will not render)")
        rows.append({
            "check": "compare-paths",
            "path": path,
            "ok": len(issues) == 0,
            "issues": issues,
        })
    return rows


# ─────────────────────────────────────────────────────────────────────────────
# DRIVER
# ─────────────────────────────────────────────────────────────────────────────

def run(base: str, quiet: bool) -> tuple[int, list[dict]]:
    """Run every check, return (exit_code, rows)."""
    started = time.time()
    if not quiet:
        print(f"\n=== wiggmap post-merge monitor — {datetime.now(timezone.utc).isoformat()}", flush=True)
        print(f"=== base: {base}", flush=True)

    rows: list[dict] = []
    sections = [
        ("Migrated lang-dir pages (39)", check_migrated_pages),
        ("Legacy redirects (16)", check_legacy_redirects),
        ("Flat trilingual sample (countries/chronicles/lp/compare-static)", check_flat_trilingual),
        ("Misc resources (sitemap/robots/manifest/sw)", check_misc_resources),
        ("Query-string preservation on /compare.html?c=...", check_query_preservation),
        ("Sprint 1 non-regression on /en/", check_sprint1_no_regression),
        ("Sprint Y.5 perf gate (<picture> SSR + opt-out flag)", check_sprint_y_perf),
        ("Compare.html absolute-paths gate (hotfix 9fdfb9b)", check_compare_paths),
    ]
    for label, fn in sections:
        if not quiet:
            print(f"\n--- {label}", flush=True)
        section_rows = fn(base)
        rows.extend(section_rows)
        for r in section_rows:
            if r["ok"]:
                if not quiet:
                    print(f"  ✓ {r['path']}", flush=True)
            else:
                # Always show failures, even in quiet mode
                print(f"  ✗ {r['path']} — {'; '.join(r['issues'])}", flush=True)

    failed = [r for r in rows if not r["ok"]]
    elapsed = time.time() - started
    print(f"\n=== Summary: {len(rows) - len(failed)}/{len(rows)} OK, {len(failed)} KO  ({elapsed:.1f}s)", flush=True)
    if failed:
        print("=== KO paths:", flush=True)
        for r in failed:
            print(f"  - {r['path']} [{r['check']}]: {'; '.join(r['issues'])}", flush=True)
    return (1 if failed else 0), rows


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    p.add_argument("--base", default=DEFAULT_BASE, help=f"Base URL (default: {DEFAULT_BASE})")
    p.add_argument("--json", default=None, help="Write detailed JSON report to this path")
    p.add_argument("--quiet", action="store_true", help="Only print failures + summary")
    args = p.parse_args()

    base = args.base.rstrip("/")
    code, rows = run(base, args.quiet)

    json_path = args.json or f"/tmp/monitor_post_merge_{int(time.time())}.json"
    Path(json_path).write_text(json.dumps({
        "base": base,
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "exit_code": code,
        "rows": rows,
    }, indent=2), encoding="utf-8")
    print(f"\nJSON report: {json_path}", flush=True)
    sys.exit(code)


if __name__ == "__main__":
    main()
