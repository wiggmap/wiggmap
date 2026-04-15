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

def prio_for(url_path: str) -> tuple[str, str]:
    if url_path in ("/", ""):
        return "1.0", "weekly"
    if url_path in ("/globe.html", "/compare.html", "/wiggmatch.html", "/about.html", "/indexchronicles.html"):
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
    if url_path in ("/privacy.html", "/terms.html"):
        return "0.3", "yearly"
    return "0.5", "monthly"

def collect() -> list[str]:
    urls: list[str] = []

    # Root page
    urls.append("/")

    # Root-level HTML
    for f in sorted(os.listdir(ROOT)):
        if not f.endswith(".html"):
            continue
        if f in EXCLUDE_ROOT or f == "index.html":
            continue
        if f.startswith("template_"):
            continue
        urls.append("/" + f)

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
    """Return list of (lang, url) alternates for url if it matches *-{lang}.html pattern."""
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
            default_en = next((a for l, a in alts if l == "en"), None)
            if default_en:
                lines.append(
                    f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{default_en}" />'
                )
        lines.append("  </url>")
    lines.append("</urlset>")
    out = "\n".join(lines) + "\n"
    (ROOT / "sitemap.xml").write_text(out, encoding="utf-8")
    print(f"Wrote sitemap.xml with {len(urls)} URLs")

if __name__ == "__main__":
    main()
