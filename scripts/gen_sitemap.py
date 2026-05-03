#!/usr/bin/env python3
"""Regenerate sitemap.xml including all countries, chronicles, villes, 1966, lp, lead-magnet, compare/static, connect and root pages."""
import os
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://wiggmap.com"
TODAY = date.today().isoformat()

EXCLUDE_ROOT = {
    "404.html", "mon-compte.html", "confirmation.html", "forms.html",
    "onboarding.html", "index.html.bak", "index.html.old",
    "template_chronicles.html",
}

# Sprint 2 — pages now served from /en/, /fr/, /es/ instead of root.
# These are excluded from root listing AND drive the per-lang directory listing.
# Source: MIGRATION_PLAN.md §1.1 (D4/D5 source-of-truth mapping).
MIGRATED_TO_LANG_DIRS = {
    "about.html", "compare.html", "globe.html", "indexchronicles.html",
    "terms.html", "privacy.html", "confirmation.html",
    "chronicles-villes.html", "chronicles-dest.html", "chronicles-family.html",
    "chronicles-horizons.html", "chronicles-visas.html",
    # Sprint D1 — wiggmatch trilingual: served from /en/, /fr/, /es/.
    # Legacy /wiggmatch.html stays in repo as 301 source (no rollback safety net
    # broken yet) but must NOT be sitemapped.
    "wiggmatch.html",
}

def prio_for(url_path: str) -> tuple[str, str]:
    if url_path in ("/", ""):
        return "1.0", "weekly"
    # Sprint 2 — lang-dir homes (/en/, /fr/, /es/) are top priority
    if url_path in ("/en/", "/fr/", "/es/"):
        return "1.0", "weekly"
    # Sprint 2 — high-value migrated root pages
    name = url_path.rsplit("/", 1)[-1]
    is_lang_dir = url_path.startswith("/en/") or url_path.startswith("/fr/") or url_path.startswith("/es/")
    if is_lang_dir and name in {
        "about.html", "compare.html", "globe.html", "indexchronicles.html",
    }:
        return "0.9", "weekly"
    if is_lang_dir and name.startswith("chronicles-"):
        return "0.7", "monthly"
    if is_lang_dir and name in {"terms.html", "privacy.html"}:
        return "0.3", "yearly"
    if is_lang_dir and name == "confirmation.html":
        return "0.2", "yearly"
    # Sprint D1 — wiggmatch trilingual: high-value lead-magnet quiz on all 3 langs
    if url_path in ("/en/wiggmatch.html", "/fr/wiggmatch.html", "/es/wiggmatch.html"):
        return "0.9", "weekly"
    if url_path.startswith("/countries/"):
        return "0.8", "monthly"
    if url_path.startswith("/chronicles/villes/"):
        return "0.7", "monthly"
    if url_path.startswith("/chronicles/1966/"):
        return "0.7", "monthly"
    if url_path.startswith("/chronicles/"):
        return "0.7", "monthly"
    if url_path.startswith("/compare/static/"):
        return "0.6", "monthly"
    if url_path.startswith("/lp/") or url_path.startswith("/lead-magnet/"):
        return "0.6", "monthly"
    if url_path.startswith("/connect/"):
        return "0.5", "monthly"
    return "0.5", "monthly"

def collect() -> list[str]:
    urls: list[str] = []

    # Sprint 2 — Root canonical (/) + lang-dir roots
    urls.append("/")
    for lg in ("en", "fr", "es"):
        if (ROOT / lg).is_dir() and (ROOT / lg / "index.html").is_file():
            urls.append(f"/{lg}/")

    # Root-level HTML — exclude pages that have moved to /en/, /fr/, /es/
    import re as _re_root
    google_verify_re = _re_root.compile(r'^google[a-f0-9]{16,}\.html$')
    for f in sorted(os.listdir(ROOT)):
        if not f.endswith(".html"):
            continue
        if f in EXCLUDE_ROOT or f == "index.html":
            continue
        if f in MIGRATED_TO_LANG_DIRS:
            # served from /en/{f}, /fr/{f}, /es/{f} — added below from those dirs
            continue
        if f.startswith("template_"):
            continue
        # Search Console / Bing webmaster verification files: never sitemapped
        if google_verify_re.match(f) or f.startswith("BingSiteAuth"):
            continue
        urls.append("/" + f)

    # Sprint 2 — /en/, /fr/, /es/ subdirs (root migrated pages)
    for lg in ("en", "fr", "es"):
        d = ROOT / lg
        if not d.is_dir():
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html") or f == "index.html":
                continue
            urls.append(f"/{lg}/{f}")

    # countries/
    d = ROOT / "countries"
    for f in sorted(os.listdir(d)):
        if f.endswith(".html"):
            urls.append(f"/countries/{f}")

    # chronicles/ (top-level .html)
    d = ROOT / "chronicles"
    for f in sorted(os.listdir(d)):
        p = d / f
        if p.is_file() and f.endswith(".html"):
            urls.append(f"/chronicles/{f}")

    # chronicles/villes/
    d = ROOT / "chronicles" / "villes"
    for f in sorted(os.listdir(d)):
        if f.endswith(".html"):
            urls.append(f"/chronicles/villes/{f}")

    # chronicles/1966/
    d = ROOT / "chronicles" / "1966"
    for f in sorted(os.listdir(d)):
        if f.endswith(".html"):
            urls.append(f"/chronicles/1966/{f}")

    # compare/static/*/index.html
    d = ROOT / "compare" / "static"
    if d.is_dir():
        for sub in sorted(os.listdir(d)):
            p = d / sub / "index.html"
            if p.is_file():
                urls.append(f"/compare/static/{sub}/")

    # lp/
    d = ROOT / "lp"
    if d.is_dir():
        for f in sorted(os.listdir(d)):
            if f.endswith(".html"):
                urls.append(f"/lp/{f}")

    # lead-magnet/
    d = ROOT / "lead-magnet"
    if d.is_dir():
        for f in sorted(os.listdir(d)):
            if f.endswith(".html"):
                urls.append(f"/lead-magnet/{f}")

    # connect/ (public feed pages)
    d = ROOT / "connect"
    if d.is_dir():
        for f in sorted(os.listdir(d)):
            if f.endswith(".html"):
                urls.append(f"/connect/{f}")

    # dedupe while preserving order
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out

def build_hreflang_group(url: str, all_set: set[str]) -> list[tuple[str, str]]:
    """Return list of (lang, url) alternates for url.

    Two URL patterns supported:
    1. slug-lang pattern: /any/path/slug-{lang}.html
       (countries, chronicles, lp, lead-magnet)
    2. Sprint 2 lang-dir pattern: /{lang}/page.html or /{lang}/
       (migrated root pages)
    """
    # Pattern 2 — lang-dir (/en/about.html etc.). Detect first since it's
    # more specific.
    import re as _re
    m = _re.match(r'^/(en|fr|es)(/.*)?$', url)
    if m:
        rest = m.group(2) or "/"
        alts = []
        for l in ("en", "fr", "es"):
            candidate = f"/{l}{rest}"
            if candidate in all_set:
                alts.append((l, candidate))
        return alts

    # Pattern 1 — slug-lang (legacy, for countries/chronicles/lp/lead-magnet)
    name = url.rsplit("/", 1)[-1]
    if not name.endswith(".html"):
        return []
    stem = name[:-5]
    for lang in ("en", "fr", "es"):
        suffix = f"-{lang}"
        if stem.endswith(suffix):
            base_stem = stem[: -len(suffix)]
            base_path = url.rsplit("/", 1)[0]
            alts = []
            for l in ("en", "fr", "es"):
                candidate = f"{base_path}/{base_stem}-{l}.html"
                if candidate in all_set:
                    alts.append((l, candidate))
            return alts
    return []

def main():
    urls = collect()
    url_set = set(urls)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for u in urls:
        prio, freq = prio_for(u)
        alts = build_hreflang_group(u, url_set)
        lines.append("  <url>")
        lines.append(f"    <loc>{BASE}{u}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        for lang, alt in alts:
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{BASE}{alt}" />'
            )
        if alts:
            # Sprint 2 — x-default points to source-of-truth lang per MIGRATION_PLAN.md D4/D5.
            # FR-source for chronicles-* index pages, EN-source for everything else.
            name = u.rsplit("/", 1)[-1]
            fr_source_names = {
                "chronicles-villes.html", "chronicles-dest.html",
                "chronicles-family.html", "chronicles-horizons.html",
                "chronicles-visas.html",
            }
            preferred = "fr" if name in fr_source_names else "en"
            default_url = next((a for l, a in alts if l == preferred), None)
            if not default_url:  # fallback to EN if preferred lang missing
                default_url = next((a for l, a in alts if l == "en"), None)
            if default_url:
                lines.append(
                    f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{default_url}" />'
                )
        lines.append("  </url>")
    lines.append("</urlset>")
    out = "\n".join(lines) + "\n"
    (ROOT / "sitemap.xml").write_text(out, encoding="utf-8")
    print(f"Wrote sitemap.xml with {len(urls)} URLs")

if __name__ == "__main__":
    main()
