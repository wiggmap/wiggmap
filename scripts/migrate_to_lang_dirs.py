#!/usr/bin/env python3
"""
migrate_to_lang_dirs.py — Sprint 2 trilingual roots migration.

Generates /en/, /fr/, /es/ directories from existing root pages, applying:
- <html lang="..."> rewrite
- <link rel="canonical"> per page (self if matches source lang, else source)
- hreflang block (en, fr, es, x-default = source lang)
- <meta name="robots" content="noindex,follow"> on untranslated pages
- "Page not yet translated" UI banner on untranslated pages
- Internal absolute link rewrite: /about.html -> /{lang}/about.html etc.
  (only the 13 root pages; countries/, chronicles/, lp/, etc. left untouched)

Idempotent: re-running produces byte-identical output.

USAGE
-----
  python3 scripts/migrate_to_lang_dirs.py --dry-run    # preview only
  python3 scripts/migrate_to_lang_dirs.py --self-test  # internal tests
  python3 scripts/migrate_to_lang_dirs.py              # actual write
"""

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
LANGS = ["en", "fr", "es"]
LANG_LABEL = {"en": "English", "fr": "French", "es": "Spanish"}
SITE_URL = "https://wiggmap.com"

# Pages with EN as source-of-truth (other langs get untranslated banner).
# Note: 404.html is intentionally excluded — D3 (a) keeps it as a single
# multilingual file with JS lang swap (Netlify can't serve a per-lang 404
# natively without complex edge-handler config).
EN_SOURCE = [
    "index.html",
    "about.html",
    "compare.html",
    "globe.html",
    "indexchronicles.html",
    "terms.html",
    "privacy.html",
    "confirmation.html",
]

# Pages with FR as source-of-truth (other langs get untranslated banner)
FR_SOURCE = [
    "chronicles-villes.html",
    "chronicles-dest.html",
    "chronicles-family.html",
    "chronicles-horizons.html",
    "chronicles-visas.html",
]

# Mapping page -> source lang
SOURCE_LANG = {**{p: "en" for p in EN_SOURCE}, **{p: "fr" for p in FR_SOURCE}}

# All root pages this script handles (13 pages × 3 langs = 39 files)
ALL_PAGES = list(SOURCE_LANG.keys())

# Internal links to rewrite: any href="/page.html" pointing to a migrated page
# becomes href="/{lang}/page.html" (or /{lang}/ for index.html).
# Pages NOT listed here keep their absolute root URL (countries/, chronicles/,
# lp/, lead-magnet/, mon-compte, onboarding, ggg/, connect/, etc.)
MIGRATED_PAGE_NAMES = ALL_PAGES + [
    "wiggmatch.html",  # wiggmatch is migrated to /fr/wiggmatch.html only (D1)
]


# ─────────────────────────────────────────────────────────────────────────────
# CORE TRANSFORM
# ─────────────────────────────────────────────────────────────────────────────

def url_for(page, lang):
    """Return canonical URL for a given page in a given lang."""
    if page == "index.html":
        return f"{SITE_URL}/{lang}/"
    if page == "wiggmatch.html":
        # D1: only FR variant is created in this sprint
        return f"{SITE_URL}/fr/wiggmatch.html"
    return f"{SITE_URL}/{lang}/{page}"


def output_path(page, lang):
    """Return repo-relative output path for the migrated page."""
    if page == "index.html":
        return Path(lang) / "index.html"
    return Path(lang) / page


def hreflang_block(page, source_lang):
    """Build the 4-link hreflang block (en, fr, es, x-default)."""
    lines = []
    for lg in LANGS:
        url = url_for(page, lg)
        lines.append(f'<link rel="alternate" hreflang="{lg}" href="{url}">')
    lines.append(
        f'<link rel="alternate" hreflang="x-default" href="{url_for(page, source_lang)}">'
    )
    return "\n".join(lines)


def banner_html(source_lang, page):
    """UI banner shown on untranslated pages."""
    src_url = url_for(page, source_lang)
    src_label = LANG_LABEL[source_lang]
    return (
        '<!-- TODO-i18n: remove this banner + the noindex meta when this page is '
        'translated. See MIGRATION_PLAN.md §10 D4/D5. -->\n'
        '<div class="wm-untranslated-banner" role="note" '
        'style="background:#fff7e6;border-bottom:2px solid #d97706;'
        'padding:10px 18px;font-family:Inter,system-ui,sans-serif;'
        'font-size:13px;color:#7a4f10;text-align:center;">'
        f'<p style="margin:0;">This page hasn’t been translated yet. '
        f'<a href="{src_url}" '
        'style="color:#1a5430;font-weight:700;text-decoration:underline;">'
        f'View original in {src_label} →</a></p>'
        '</div>\n'
    )


# Regex tools — compile once
RE_HTML_LANG = re.compile(r'<html\s+lang="[^"]*"', re.IGNORECASE)
RE_CANONICAL = re.compile(
    r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>', re.IGNORECASE
)
RE_HREFLANG_LINK = re.compile(
    r'<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>\s*\n?',
    re.IGNORECASE,
)
RE_ROBOTS_META = re.compile(
    r'<meta\s+name="robots"\s+content="[^"]*"\s*/?>\s*\n?', re.IGNORECASE
)
RE_BANNER = re.compile(
    r'<!--\s*TODO-i18n:[^\n]*\n<div class="wm-untranslated-banner".*?</div>\n',
    re.DOTALL,
)
RE_BANNER_DIV_ONLY = re.compile(
    r'<div class="wm-untranslated-banner".*?</div>\n?', re.DOTALL
)
RE_HEAD_OPEN = re.compile(r'<head[^>]*>', re.IGNORECASE)
RE_WMMAIN_ANCHOR = re.compile(r'(<a id="wm-main"[^>]*></a>\s*\n?)', re.IGNORECASE)
RE_BODY_OPEN = re.compile(r'(<body[^>]*>\s*\n?)', re.IGNORECASE)


def rewrite_html_lang(src, lang):
    return RE_HTML_LANG.sub(f'<html lang="{lang}"', src, count=1)


def rewrite_canonical(src, page, lang, source_lang):
    canonical_url = url_for(page, lang) if lang == source_lang else url_for(page, source_lang)
    new_tag = f'<link rel="canonical" href="{canonical_url}">'
    if RE_CANONICAL.search(src):
        return RE_CANONICAL.sub(new_tag, src, count=1)
    # No canonical exists — inject inside <head>
    return RE_HEAD_OPEN.sub(lambda m: m.group(0) + "\n" + new_tag, src, count=1)


def replace_hreflang_block(src, page, source_lang):
    """Remove all existing hreflang links, then inject the fresh block right
    after the canonical (or after <head> if no canonical)."""
    src = RE_HREFLANG_LINK.sub("", src)
    block = hreflang_block(page, source_lang) + "\n"
    if RE_CANONICAL.search(src):
        return RE_CANONICAL.sub(lambda m: m.group(0) + "\n" + block.rstrip("\n"),
                                 src, count=1)
    return RE_HEAD_OPEN.sub(lambda m: m.group(0) + "\n" + block.rstrip("\n"),
                             src, count=1)


def set_robots(src, value):
    """Set or replace the robots meta. value=None removes any existing."""
    src = RE_ROBOTS_META.sub("", src)
    if value is None:
        return src
    new_tag = f'<meta name="robots" content="{value}">\n'
    return RE_HEAD_OPEN.sub(lambda m: m.group(0) + "\n" + new_tag.rstrip("\n"),
                             src, count=1)


def remove_banner(src):
    """Strip any previously-injected untranslated banner."""
    src = RE_BANNER.sub("", src)
    src = RE_BANNER_DIV_ONLY.sub("", src)
    return src


def inject_banner(src, source_lang, page):
    """Inject the banner just after <a id='wm-main'>, fallback after <body>."""
    banner = banner_html(source_lang, page)
    if RE_WMMAIN_ANCHOR.search(src):
        return RE_WMMAIN_ANCHOR.sub(lambda m: m.group(1) + banner, src, count=1)
    if RE_BODY_OPEN.search(src):
        return RE_BODY_OPEN.sub(lambda m: m.group(1) + banner, src, count=1)
    return src  # no body? leave as is


def rewrite_internal_links(src, lang):
    """Rewrite href="/page.html" → href="/{lang}/page.html" (or /{lang}/ for
    index.html) for the migrated root pages only. Other absolute paths
    (countries/, chronicles/, lp/, lead-magnet/, mon-compte/, onboarding/,
    ggg/, connect/, /assets/, etc.) are left untouched.

    For wiggmatch.html, link always rewrites to /fr/wiggmatch.html (D1).
    """
    out = src
    for pname in MIGRATED_PAGE_NAMES:
        if pname == "wiggmatch.html":
            target = "/fr/wiggmatch.html"
        elif pname == "index.html":
            # /index.html → /{lang}/    (and bare / stays bare /, handled at root redirect)
            target = f"/{lang}/"
        else:
            target = f"/{lang}/{pname}"

        # href="/pname"  +  preserve query strings:  href="/pname?..."
        # Match as a whole href value bounded by " or ' to avoid accidental subpath match.
        # Allow trailing ? or # or "
        for quote in ['"', "'"]:
            # exact href="/pname"
            out = out.replace(f'href={quote}/{pname}{quote}', f'href={quote}{target}{quote}')
            # href="/pname?..." or href="/pname#..."
            out = re.sub(
                r'href=' + quote + r'/' + re.escape(pname) + r'([?#][^' + quote + r']*)' + quote,
                lambda m, t=target, q=quote: f'href={q}{t}{m.group(1)}{q}',
                out
            )
    return out


def transform(src, page, lang):
    """Apply the full transform pipeline. Idempotent."""
    source_lang = SOURCE_LANG[page]
    is_translated = (lang == source_lang)

    out = src
    out = rewrite_html_lang(out, lang)
    out = rewrite_canonical(out, page, lang, source_lang)
    out = replace_hreflang_block(out, page, source_lang)
    out = remove_banner(out)
    if is_translated:
        out = set_robots(out, None)  # remove any previously-injected noindex
    else:
        out = set_robots(out, "noindex,follow")
        out = inject_banner(out, source_lang, page)
    out = rewrite_internal_links(out, lang)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# DRIVER
# ─────────────────────────────────────────────────────────────────────────────

def main_run(dry_run=False):
    written = 0
    skipped = 0
    for page in ALL_PAGES:
        src_path = REPO_ROOT / page
        if not src_path.exists():
            print(f"  SKIP missing source: {page}", file=sys.stderr)
            skipped += 1
            continue
        src = src_path.read_text(encoding="utf-8")
        for lang in LANGS:
            out = transform(src, page, lang)
            dst = REPO_ROOT / output_path(page, lang)
            note = "self" if SOURCE_LANG[page] == lang else f"canonical={SOURCE_LANG[page]}"
            banner = "banner=true" if SOURCE_LANG[page] != lang else "banner=false"
            if dry_run:
                print(f"  [DRY] would write {dst.relative_to(REPO_ROOT)}  ({note}, {banner}, {len(out)} bytes)")
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                # Idempotence guard: only write if content changed
                if dst.exists() and dst.read_text(encoding="utf-8") == out:
                    print(f"  = unchanged {dst.relative_to(REPO_ROOT)}  ({note}, {banner})")
                else:
                    dst.write_text(out, encoding="utf-8")
                    print(f"  ✓ wrote {dst.relative_to(REPO_ROOT)}  ({note}, {banner}, {len(out)} bytes)")
            written += 1
    return written, skipped


def self_test():
    """Internal sanity tests on the transform pipeline."""
    fixture = '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Test</title>
<link rel="canonical" href="https://wiggmap.com/about.html">
<link rel="alternate" hreflang="en" href="https://wiggmap.com/about.html">
</head>
<body>
<a id="wm-main" tabindex="-1"></a>
<a href="/about.html">about</a>
<a href="/compare.html?c=fr,jp">compare</a>
<a href="/countries/portugal-en.html">portugal</a>
<a href="/wiggmatch.html">match</a>
</body>
</html>
'''
    # Test 1: EN canonical for about.html in EN lang -> self
    out = transform(fixture, "about.html", "en")
    assert '<html lang="en"' in out, "T1.1 lang attr"
    assert 'href="https://wiggmap.com/en/about.html"' in out, "T1.2 canonical self"
    assert 'hreflang="en" href="https://wiggmap.com/en/about.html"' in out, "T1.3 hreflang en"
    assert 'hreflang="fr" href="https://wiggmap.com/fr/about.html"' in out, "T1.4 hreflang fr"
    assert 'hreflang="es" href="https://wiggmap.com/es/about.html"' in out, "T1.5 hreflang es"
    assert 'hreflang="x-default" href="https://wiggmap.com/en/about.html"' in out, "T1.6 x-default"
    assert 'noindex' not in out, "T1.7 no noindex on translated"
    assert 'wm-untranslated-banner' not in out, "T1.8 no banner on translated"
    assert 'href="/en/about.html"' in out, "T1.9 internal /about → /en/about"
    assert 'href="/en/compare.html?c=fr,jp"' in out, "T1.10 internal compare with query"
    assert 'href="/countries/portugal-en.html"' in out, "T1.11 country link untouched"
    assert 'href="/fr/wiggmatch.html"' in out, "T1.12 wiggmatch always /fr/"

    # Test 2: about.html in FR lang -> untranslated banner + canonical to EN
    out2 = transform(fixture, "about.html", "fr")
    assert '<html lang="fr"' in out2, "T2.1 lang attr"
    assert 'href="https://wiggmap.com/en/about.html"' in out2, "T2.2 canonical to EN source"
    assert 'noindex,follow' in out2, "T2.3 noindex,follow on untranslated"
    assert 'wm-untranslated-banner' in out2, "T2.4 banner injected"
    assert 'View original in English' in out2, "T2.5 banner mentions source lang"
    assert 'href="/fr/about.html"' in out2, "T2.6 internal /about → /fr/about (lang of THIS page)"

    # Test 3: chronicles-villes.html FR-source in EN -> untranslated banner
    out3 = transform(fixture, "chronicles-villes.html", "en")
    assert '<html lang="en"' in out3, "T3.1 lang attr"
    assert 'href="https://wiggmap.com/fr/chronicles-villes.html"' in out3, "T3.2 canonical to FR source"
    assert 'noindex,follow' in out3, "T3.3 noindex"
    assert 'View original in French' in out3, "T3.4 banner French"

    # Test 4: chronicles-villes.html in FR (source) -> no banner
    out4 = transform(fixture, "chronicles-villes.html", "fr")
    assert 'href="https://wiggmap.com/fr/chronicles-villes.html"' in out4, "T4.1 canonical self"
    assert 'noindex' not in out4, "T4.2 no noindex on source-lang"
    assert 'wm-untranslated-banner' not in out4, "T4.3 no banner on source-lang"

    # Test 5: idempotence — running transform twice = same output
    out_a = transform(fixture, "about.html", "fr")
    out_b = transform(out_a, "about.html", "fr")
    assert out_a == out_b, "T5 idempotence violated"

    # Test 6: index.html link rewrite produces /{lang}/ not /{lang}/index.html
    fixture6 = '<a href="/index.html">home</a>'
    full6 = '<html lang="en"><head></head><body><a id="wm-main"></a>' + fixture6 + '</body></html>'
    out6 = transform(full6, "about.html", "en")
    assert 'href="/en/"' in out6, "T6 /index.html → /en/"

    print("ALL TESTS PASSED ✓ (6 test groups, 26 assertions)")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no write")
    parser.add_argument("--self-test", action="store_true", help="Run internal tests")
    args = parser.parse_args()

    if args.self_test:
        sys.exit(self_test())

    written, skipped = main_run(dry_run=args.dry_run)
    print(f"\n{'[DRY] ' if args.dry_run else ''}Summary: {written} files processed, {skipped} skipped")
