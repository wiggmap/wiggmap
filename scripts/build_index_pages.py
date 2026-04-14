#!/usr/bin/env python3
"""
Inject static HTML rendering of chronicles into the index pages so that
bots and SEO crawlers see real content (instead of an empty <div id="sectionsRoot">).

Updates:
  - indexchronicles.html  (injects ARTICLES grouped by SECTIONS into #sectionsRoot)
  - chronicles-villes.html (injects CITIES grouped by COUNTRIES into #sectionsRoot)

The JS still runs and replaces the static HTML at load time, so user behavior
is unchanged. The static HTML is for crawlers and pre-JS rendering.

Re-run this script after adding/removing chronicles or cities.
"""

import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ──────────────────────────────────────────────────────────────────────
# Parse JS object literal arrays into Python dicts
# ──────────────────────────────────────────────────────────────────────
def js_array_to_python(js_text):
    """Convert a JS array literal (with unquoted keys) into Python data."""
    text = js_text.strip()
    # Quote unquoted keys
    text = re.sub(r'([{,]\s*)([a-zA-Z_][\w]*)\s*:', r'\1"\2":', text)
    # Trailing commas before } or ]
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    return json.loads(text)


def extract_array(html_text, var_name):
    """Extract `var ARTICLES=[...];` from JS embedded in an HTML file."""
    pattern = re.compile(
        r'var\s+' + re.escape(var_name) + r'\s*=\s*(\[.*?\])\s*;',
        re.DOTALL
    )
    m = pattern.search(html_text)
    if not m:
        return None
    return js_array_to_python(m.group(1))


# ──────────────────────────────────────────────────────────────────────
# indexchronicles.html
# ──────────────────────────────────────────────────────────────────────
SECTION_LABELS = {
    'en': {
        'visas': 'Visas & Immigration', 'dest': 'Expat Destinations',
        'family': 'Family & Education',
        'horizons': 'Horizons', 'city': 'City Chronicles',
    },
    'fr': {
        'visas': 'Visas & Immigration', 'dest': 'Destinations Expat',
        'family': 'Famille & Éducation',
        'horizons': 'Horizons', 'city': 'Chroniques Villes',
    },
    'es': {
        'visas': 'Visas e Inmigración', 'dest': 'Destinos Expat',
        'family': 'Familia & Educación',
        'horizons': 'Horizontes', 'city': 'Crónicas Ciudad',
    },
}


def render_index_static(articles, sections, lang='en'):
    """Build static HTML mirroring what render() does in JS, for one language."""
    out = []
    labels = SECTION_LABELS[lang]
    see_all = {'en': 'See all →', 'fr': 'Voir tout →', 'es': 'Ver todo →'}[lang]
    tag_serie = {'en': 'Series', 'fr': 'Série', 'es': 'Serie'}[lang]
    tag_foresight = {'en': 'Foresight', 'fr': 'Prospective', 'es': 'Prospectiva'}[lang]
    for sec in sections:
        sid = sec['id']
        label = labels.get(sid, sid)
        page_url = sec.get('page', '')
        if isinstance(page_url, dict):
            page_url = page_url.get(lang) or page_url.get('en', '')
        out.append('<div class="category">')
        out.append('<div class="cat-header"><div class="cat-dot"></div>')
        out.append(f'<span class="cat-name">{label}</span>')
        if page_url:
            out.append(f'<a class="cat-voir" href="{page_url}">{see_all}</a>')
        out.append('</div>')
        out.append('<div class="carousel-wrap">')
        out.append('<div class="arrow arrow-left" onclick="scrollCarousel(this,-1)">‹</div>')
        out.append('<div class="scroll-row">')
        items = [a for a in articles if a.get('section') == sid]
        if sid != 'city':
            items.sort(key=lambda a: a.get('date', ''), reverse=True)
        for a in items[:20]:
            url = a.get('url', {})
            if isinstance(url, dict):
                url = url.get(lang) or url.get('en') or '#'
            title = a.get('title', {})
            if isinstance(title, dict):
                title = title.get(lang) or title.get('en') or ''
            reg = a.get('reg', {})
            if isinstance(reg, dict):
                reg = reg.get(lang) or reg.get('en') or ''
            flag = a.get('flag', '')
            time = a.get('time', '')
            bg = a.get('bg', 'smoke')
            wm = a.get('wm', '')
            wm_html = f'<div class="watermark">{wm}</div>' if wm else ''
            flag_html = f'<div class="card-flag">{flag}</div>' if flag else ''
            if sid == 'horizons' and wm == '1966':
                tag = f'{tag_serie} 1966 · {time}'
            elif sid == 'horizons' and wm == '2056':
                tag = f'{tag_foresight} · {time}'
            else:
                tag = f'{reg} · {time}'
            out.append(
                f'<a class="card bg-{bg}" href="{url}">{wm_html}{flag_html}'
                f'<div class="card-overlay">'
                f'<div class="card-tag">{tag}</div>'
                f'<div class="card-title">{title}</div>'
                f'</div></a>'
            )
        out.append('</div>')
        out.append('<div class="arrow arrow-right" onclick="scrollCarousel(this,1)">›</div>')
        out.append('</div></div>')
    return ''.join(out)


def update_indexchronicles():
    path = os.path.join(ROOT, 'indexchronicles.html')
    html = open(path, encoding='utf-8').read()
    articles = extract_array(html, 'ARTICLES')
    sections = extract_array(html, 'SECTIONS')
    if not articles or not sections:
        print(f"  ! Could not parse arrays in {path}")
        return False

    # Build static HTML for English (default crawl language)
    static_html = render_index_static(articles, sections, lang='en')

    # Wrap in noscript-style fallback that JS will replace
    fallback = f'<div id="sectionsRoot">\n<!-- BEGIN STATIC PRERENDER (regenerated by scripts/build_index_pages.py) -->\n{static_html}\n<!-- END STATIC PRERENDER -->\n</div>'

    # Replace existing #sectionsRoot block (idempotent: matches anything between
    # the opening tag and </main>, regardless of nested </div> from prerender)
    new_html, n = re.subn(
        r'<div\s+id="sectionsRoot"[^>]*>.*?(?=\s*</main>)',
        fallback,
        html,
        count=1,
        flags=re.DOTALL,
    )
    if n == 0:
        # Fallback: empty self-closing
        new_html, n = re.subn(
            r'<div\s+id="sectionsRoot"[^>]*/?>',
            fallback,
            html,
            count=1,
        )
    if n == 0:
        print("  ! Could not find #sectionsRoot in indexchronicles.html")
        return False

    open(path, 'w', encoding='utf-8').write(new_html)
    print(f"✓ indexchronicles.html updated — {len(articles)} articles, {len(sections)} sections, {len(static_html)} chars of static HTML injected")
    return True


# ──────────────────────────────────────────────────────────────────────
# chronicles-villes.html
# ──────────────────────────────────────────────────────────────────────
def render_villes_static(cities, countries, lang='en'):
    out = []
    for co in countries:
        cid = co['id']
        label = co.get('label', {})
        if isinstance(label, dict):
            label = label.get(lang) or label.get('en') or cid
        out.append(f'<div class="theme-section"><div class="theme-head">')
        out.append(f'<span class="theme-dot"></span><span class="theme-label">{label}</span>')
        out.append('<div class="theme-rule"></div></div><div class="carousel">')
        items = [c for c in cities if c.get('country') == cid]
        for c in items:
            url = c.get('url', {})
            if isinstance(url, dict):
                url = url.get(lang) or url.get('en') or '#'
            title = c.get('t', {})
            if isinstance(title, dict):
                title = title.get(lang) or title.get('en') or ''
            flag = c.get('flag', '')
            out.append(
                f'<a class="vcard" href="{url}">'
                f'<div class="vcard-body">'
                f'<div class="vcard-meta">{flag} {title}</div>'
                f'<div class="vcard-title">{title} 2026</div>'
                f'</div></a>'
            )
        out.append('</div></div>')
    return ''.join(out)


def update_chronicles_villes():
    path = os.path.join(ROOT, 'chronicles-villes.html')
    html = open(path, encoding='utf-8').read()
    cities = extract_array(html, 'CITIES')
    countries = extract_array(html, 'COUNTRIES')
    if not cities or not countries:
        print("  ! Could not parse CITIES/COUNTRIES in chronicles-villes.html")
        return False

    static_html = render_villes_static(cities, countries, lang='en')
    fallback = f'<div id="sectionsRoot">\n<!-- BEGIN STATIC PRERENDER (regenerated by scripts/build_index_pages.py) -->\n{static_html}\n<!-- END STATIC PRERENDER -->\n</div>'

    new_html, n = re.subn(
        r'<div\s+id="sectionsRoot"[^>]*>.*?(?=\s*</main>)',
        fallback,
        html,
        count=1,
        flags=re.DOTALL,
    )
    if n == 0:
        new_html, n = re.subn(
            r'<div\s+id="sectionsRoot"[^>]*/?>',
            fallback,
            html,
            count=1,
        )
    if n == 0:
        print("  ! Could not find #sectionsRoot in chronicles-villes.html")
        return False

    open(path, 'w', encoding='utf-8').write(new_html)
    print(f"✓ chronicles-villes.html updated — {len(cities)} cities, {len(countries)} countries, {len(static_html)} chars of static HTML injected")
    return True


def main():
    update_indexchronicles()
    update_chronicles_villes()


if __name__ == '__main__':
    main()
