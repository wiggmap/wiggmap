#!/usr/bin/env python3
"""Regenerate sitemap.xml + sub-sitemaps + image sitemap entries."""
import os
import re
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

def hero_image_for(url_path: str) -> tuple[str, str] | None:
    """For URLs with an obvious hero image, return (image_url, caption).
    Used to emit <image:image> per Google's image sitemap spec.
    """
    name = url_path.rsplit("/", 1)[-1]
    # Country pages: /countries/portugal-en.html → /assets/hero-portugal.webp
    if url_path.startswith("/countries/") and name.endswith(".html"):
        # strip trailing -{lang}.html (3 letters: -en, -fr, -es, OR longer like -es-AR — be safe)
        m = re.match(r"^([a-z0-9-]+)-(en|fr|es)\.html$", name)
        if m:
            slug = m.group(1)
            # Note: assume webp exists (Sprint Y.5 ensured 1:1 webp/jpg)
            return (f"{BASE}/assets/hero-{slug}.webp", f"Hero photo of {slug.replace('-', ' ').title()}")
    # City chronicles: /chronicles/villes/chronicle-bali-indonesia-en.html → /assetscity/bali.png
    if url_path.startswith("/chronicles/villes/") and name.startswith("chronicle-"):
        m = re.match(r"^chronicle-([a-z0-9-]+?)-(?:[a-z]+-)*?(en|fr|es)\.html$", name)
        if m:
            # Heuristic: take the FIRST token before the second-to-last dash as the city slug.
            # The chronicle slug pattern is "chronicle-{city}-{country}-{lang}.html"
            # so we need the first token after "chronicle-".
            inner = name[len("chronicle-"):]
            # Drop the trailing -{lang}.html
            inner = re.sub(r"-(en|fr|es)\.html$", "", inner)
            # Now split by '-' and pick the first segment as city slug
            parts = inner.split("-")
            if parts:
                # For "bali-indonesia" → city = "bali"
                # For "buenos-aires-argentine" → city = "buenos-aires" (2 tokens before country)
                # Heuristic: country is always the last token unless it's known multi-word
                # Conservative: take everything except the last token as the city
                if len(parts) >= 2:
                    city = "-".join(parts[:-1])
                else:
                    city = parts[0]
                return (f"{BASE}/assetscity/{city}.png", f"Hero photo of {city.replace('-', ' ').title()}")
    return None


def render_url_block(url: str, url_set: set[str]) -> list[str]:
    """Render the <url> block (loc + lastmod + changefreq + priority +
    hreflang + image:image when relevant). Returns a list of lines."""
    prio, freq = prio_for(url)
    alts = build_hreflang_group(url, url_set)
    lines = ["  <url>"]
    lines.append(f"    <loc>{BASE}{url}</loc>")
    lines.append(f"    <lastmod>{TODAY}</lastmod>")
    lines.append(f"    <changefreq>{freq}</changefreq>")
    lines.append(f"    <priority>{prio}</priority>")
    for lang, alt in alts:
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{BASE}{alt}" />'
        )
    if alts:
        name = url.rsplit("/", 1)[-1]
        fr_source_names = {
            "chronicles-villes.html", "chronicles-dest.html",
            "chronicles-family.html", "chronicles-horizons.html",
            "chronicles-visas.html",
        }
        preferred = "fr" if name in fr_source_names else "en"
        default_url = next((a for l, a in alts if l == preferred), None)
        if not default_url:
            default_url = next((a for l, a in alts if l == "en"), None)
        if default_url:
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{default_url}" />'
            )
    # Image sitemap: emit <image:image> for hero photos on country + city chronicles.
    img = hero_image_for(url)
    if img:
        img_url, img_caption = img
        lines.append("    <image:image>")
        lines.append(f"      <image:loc>{img_url}</image:loc>")
        lines.append(f"      <image:caption>{img_caption}</image:caption>")
        lines.append("    </image:image>")
    lines.append("  </url>")
    return lines


def write_sub_sitemap(name: str, urls: list[str], url_set: set[str]) -> int:
    """Write a single sitemap file. Returns URL count."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]
    for u in urls:
        lines.extend(render_url_block(u, url_set))
    lines.append('</urlset>')
    out = "\n".join(lines) + "\n"
    (ROOT / name).write_text(out, encoding="utf-8")
    return len(urls)


def write_index(sub_sitemaps: list[str]) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for name in sub_sitemaps:
        lines.append('  <sitemap>')
        lines.append(f'    <loc>{BASE}/{name}</loc>')
        lines.append(f'    <lastmod>{TODAY}</lastmod>')
        lines.append('  </sitemap>')
    lines.append('</sitemapindex>')
    out = "\n".join(lines) + "\n"
    (ROOT / "sitemap.xml").write_text(out, encoding="utf-8")


def split_urls(urls: list[str]) -> dict[str, list[str]]:
    """Bucket URLs into named sub-sitemaps for Search Console clarity."""
    buckets = {
        "sitemap-roots.xml": [],     # Lang-dir homes + root pages + connect/lp/lead-magnet
        "sitemap-countries.xml": [], # /countries/*
        "sitemap-chronicles.xml": [],# /chronicles/* (incl /villes/, /1966/)
        "sitemap-compare.xml": [],   # /compare/static/*
    }
    for u in urls:
        if u.startswith("/countries/"):
            buckets["sitemap-countries.xml"].append(u)
        elif u.startswith("/chronicles/"):
            buckets["sitemap-chronicles.xml"].append(u)
        elif u.startswith("/compare/static/"):
            buckets["sitemap-compare.xml"].append(u)
        else:
            buckets["sitemap-roots.xml"].append(u)
    return buckets


def main():
    urls = collect()
    url_set = set(urls)
    buckets = split_urls(urls)

    written = {}
    for name, bucket_urls in buckets.items():
        if not bucket_urls:
            continue
        count = write_sub_sitemap(name, bucket_urls, url_set)
        written[name] = count
        print(f"  Wrote {name} with {count} URLs")

    # sitemap.xml at root becomes the sitemap index
    write_index([n for n in written.keys()])
    total = sum(written.values())
    print(f"  Wrote sitemap.xml (index) referencing {len(written)} sub-sitemaps")
    print(f"\nTotal URLs across all sub-sitemaps: {total}")


if __name__ == "__main__":
    main()
