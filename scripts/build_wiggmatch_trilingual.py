#!/usr/bin/env python3
"""
build_wiggmatch_trilingual.py — Sprint D1 wiggmatch trilingual generator.

Reads /fr/wiggmatch.html (the master FR, prepared in D1.1 with URL-first
lang detection + URL-navigating wmSetLang) and emits two sister files:
  /en/wiggmatch.html
  /es/wiggmatch.html

Per-lang transforms applied
---------------------------
- <html lang="fr"> → <html lang="en|es">
- <title> → lang-specific title (full quality, not literal translation)
- <meta name="description"> → lang-specific desc
- <meta property="og:title|og:description|og:url> → lang-specific
- <link rel="canonical"> → /{lang}/wiggmatch.html (D4: EN-source → /en/)
- <link rel="alternate" hreflang> quartet (en, fr, es, x-default=/en/)
- JSON-LD inLanguage="{lang}" (string, not array)
- JSON-LD url + WebApplication.description + Quiz.name + BreadcrumbList
  items → lang-specific
- WebApplication.priceCurrency: EUR for FR, USD for EN, EUR for ES
- BreadcrumbList items[1].name "WiggMatch" stays, items[0].name localized

What is NOT translated
----------------------
- WM_I18N dictionary (already contains full FR/EN/ES translations)
- WM_DYN dictionary (idem)
- Scoring engine (lang-independent)
- City database (city names use FR keys mapped via WM_DYN.country_map)
- HTML structure, CSS, all behavioural JS

Idempotence: re-running produces byte-identical output.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MASTER = REPO / "fr" / "wiggmatch.html"
SITE = "https://wiggmap.com"

# ─────────────────────────────────────────────────────────────────────────────
# Per-lang content overrides (the meta+head+JSON-LD strings)
# ─────────────────────────────────────────────────────────────────────────────

LANG_META = {
    "en": {
        "html_lang": "en",
        "title": "WiggMatch — Find your perfect city in 8 questions · WiggMap",
        "description": "8 questions, 3 minutes. Discover which city in the world really matches your expat profile — backed by real data, not generic dreams.",
        "og_title": "WiggMatch — Find your perfect city in 8 questions · WiggMap",
        "og_description": "8 questions, 3 minutes. Discover which city in the world really matches your expat profile — backed by real data, not generic dreams.",
        "lang_comment": "<!-- lang=\"en\" matches the URL /en/wiggmatch.html. The runtime IIFE re-applies WM_I18N at load via data-i18n. Source-of-truth lang per Sprint D1 D4 = EN. -->",
        "ld_currency": "USD",
        "ld_app_desc": "Personalised quiz that finds the city made for you in 8 questions.",
        "ld_quiz_name": "WiggMatch — Find your ideal city abroad",
        "ld_quiz_about": "Expat city matching",
        "ld_quiz_subject": "Travel & Relocation",
        "bc_home_name": "Home",
        "bc_home_url": f"{SITE}/en/",
    },
    "fr": {
        "html_lang": "fr",
        "title": "WiggMatch — Trouve ta ville idéale à l'étranger · WiggMap",
        "description": "8 questions, 3 minutes. Découvre quelle ville dans le monde correspond vraiment à ton profil expat — basé sur des données réelles, pas des rêves génériques.",
        "og_title": "WiggMatch — Trouve ta ville idéale à l'étranger · WiggMap",
        "og_description": "8 questions, 3 minutes. Découvre quelle ville dans le monde correspond vraiment à ton profil expat — basé sur des données réelles, pas des rêves génériques.",
        "lang_comment": "<!-- lang=\"fr\" matches the URL /fr/wiggmatch.html. Master file, source of the trilingual generation pipeline (build_wiggmatch_trilingual.py). -->",
        "ld_currency": "EUR",
        "ld_app_desc": "Quiz personnalisé qui trouve la ville faite pour toi en 8 questions.",
        "ld_quiz_name": "WiggMatch — Trouve ta ville idéale à l'étranger",
        "ld_quiz_about": "Matching ville expatriation",
        "ld_quiz_subject": "Voyage & expatriation",
        "bc_home_name": "Accueil",
        "bc_home_url": f"{SITE}/fr/",
    },
    "es": {
        "html_lang": "es",
        "title": "WiggMatch — Encuentra tu ciudad ideal en 8 preguntas · WiggMap",
        "description": "8 preguntas, 3 minutos. Descubre qué ciudad del mundo realmente encaja con tu perfil expat — con datos reales, no sueños genéricos.",
        "og_title": "WiggMatch — Encuentra tu ciudad ideal en 8 preguntas · WiggMap",
        "og_description": "8 preguntas, 3 minutos. Descubre qué ciudad del mundo realmente encaja con tu perfil expat — con datos reales, no sueños genéricos.",
        "lang_comment": "<!-- lang=\"es\" matches the URL /es/wiggmatch.html. Generated from /fr/wiggmatch.html via scripts/build_wiggmatch_trilingual.py. -->",
        "ld_currency": "EUR",
        "ld_app_desc": "Quiz personalizado que encuentra la ciudad hecha para ti en 8 preguntas.",
        "ld_quiz_name": "WiggMatch — Encuentra tu ciudad ideal en el extranjero",
        "ld_quiz_about": "Matching ciudad expatriación",
        "ld_quiz_subject": "Viajes y expatriación",
        "bc_home_name": "Inicio",
        "bc_home_url": f"{SITE}/es/",
    },
}


def transform(src: str, lang: str) -> str:
    """Apply all per-lang transforms. Idempotent."""
    m = LANG_META[lang]
    self_url = f"{SITE}/{lang}/wiggmatch.html"
    out = src

    # 1. <html lang="..."> + the comment line right after it
    out = re.sub(
        r'<html lang="[a-z]{2}">\s*\n<!--[^>]*-->',
        f'<html lang="{m["html_lang"]}">\n{m["lang_comment"]}',
        out, count=1,
    )

    # 2. <title>
    out = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{m["title"]}</title>',
        out, count=1,
    )

    # 3. <meta name="description">
    out = re.sub(
        r'<meta name="description" content="[^"]*"\s*/>',
        f'<meta name="description" content="{m["description"]}"/>',
        out, count=1,
    )

    # 4. canonical
    out = re.sub(
        r'<link rel="canonical" href="[^"]*"\s*/>',
        f'<link rel="canonical" href="{self_url}"/>',
        out, count=1,
    )

    # 5. og:title
    out = re.sub(
        r'<meta property="og:title" content="[^"]*"\s*/>',
        f'<meta property="og:title" content="{m["og_title"]}"/>',
        out, count=1,
    )

    # 6. og:description
    out = re.sub(
        r'<meta property="og:description" content="[^"]*"\s*/>',
        f'<meta property="og:description" content="{m["og_description"]}"/>',
        out, count=1,
    )

    # 7. og:url
    out = re.sub(
        r'<meta property="og:url" content="[^"]*"\s*/>',
        f'<meta property="og:url" content="{self_url}"/>',
        out, count=1,
    )

    # 8. JSON-LD WebApplication block
    web_app_re = re.compile(
        r'<script type="application/ld\+json">\{"@context":"https://schema\.org","@type":"WebApplication"[^<]*?\}</script>',
    )
    new_web_app = (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"WebApplication",'
        '"name":"WiggMatch",'
        f'"url":"{self_url}",'
        '"applicationCategory":"TravelApplication","operatingSystem":"Any",'
        f'"description":"{m["ld_app_desc"]}",'
        f'"inLanguage":"{lang}",'
        '"isAccessibleForFree":true,'
        f'"offers":{{"@type":"Offer","price":"0","priceCurrency":"{m["ld_currency"]}"}},'
        '"publisher":{"@type":"Organization","name":"WiggMap","url":"https://wiggmap.com/","logo":"https://wiggmap.com/assets/logo.png"}}'
        '</script>'
    )
    out = web_app_re.sub(new_web_app, out, count=1)

    # 9. JSON-LD Quiz block
    quiz_re = re.compile(
        r'<script type="application/ld\+json">\{"@context":"https://schema\.org","@type":"Quiz"[^<]*?\}</script>',
    )
    new_quiz = (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"Quiz",'
        f'"name":"{m["ld_quiz_name"]}",'
        f'"about":{{"@type":"Thing","name":"{m["ld_quiz_about"]}"}},'
        '"educationalAlignment":{"@type":"AlignmentObject",'
        '"alignmentType":"educationalSubject",'
        f'"targetName":"{m["ld_quiz_subject"]}"}},'
        f'"inLanguage":"{lang}",'
        f'"url":"{self_url}"}}'
        '</script>'
    )
    out = quiz_re.sub(new_quiz, out, count=1)

    # 10. JSON-LD BreadcrumbList block
    bc_re = re.compile(
        r'<script type="application/ld\+json">\{"@context":"https://schema\.org","@type":"BreadcrumbList"[^<]*?\}</script>',
    )
    new_bc = (
        '<script type="application/ld+json">'
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,'
        f'"name":"{m["bc_home_name"]}",'
        f'"item":"{m["bc_home_url"]}"}},'
        '{"@type":"ListItem","position":2,'
        '"name":"WiggMatch",'
        f'"item":"{self_url}"}}'
        ']}'
        '</script>'
    )
    out = bc_re.sub(new_bc, out, count=1)

    return out


# ─────────────────────────────────────────────────────────────────────────────
# DRIVER
# ─────────────────────────────────────────────────────────────────────────────

def main_run(dry_run: bool = False) -> int:
    if not MASTER.exists():
        print(f"FATAL: master not found at {MASTER}", file=sys.stderr)
        return 2
    src = MASTER.read_text(encoding="utf-8")
    written = 0
    for lang in ("en", "fr", "es"):
        dst = REPO / lang / "wiggmatch.html"
        new_content = transform(src, lang)
        if dry_run:
            print(f"  [DRY] would write {dst.relative_to(REPO)}  ({len(new_content)} bytes)")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() and dst.read_text(encoding="utf-8") == new_content:
            print(f"  = unchanged {dst.relative_to(REPO)}  ({len(new_content)} bytes)")
        else:
            dst.write_text(new_content, encoding="utf-8")
            print(f"  ✓ wrote {dst.relative_to(REPO)}  ({len(new_content)} bytes)")
        written += 1
    return 0


def self_test() -> int:
    """Sanity-check the transform function on the live master."""
    if not MASTER.exists():
        print(f"FATAL: master not found at {MASTER}", file=sys.stderr)
        return 2
    src = MASTER.read_text(encoding="utf-8")

    failures = []

    for lang in ("en", "fr", "es"):
        out = transform(src, lang)
        # Required tokens
        if f'<html lang="{lang}">' not in out:
            failures.append(f"[{lang}] html lang attr missing")
        if f'href="{SITE}/{lang}/wiggmatch.html"' not in out:
            failures.append(f"[{lang}] canonical missing")
        if f'"inLanguage":"{lang}"' not in out:
            failures.append(f"[{lang}] JSON-LD inLanguage missing")
        # JSON-LD parses
        import json as _json
        for m in re.finditer(r'<script type="application/ld\+json">(.+?)</script>', out, re.DOTALL):
            try:
                _json.loads(m.group(1))
            except Exception as e:
                failures.append(f"[{lang}] JSON-LD parse error: {e} on: {m.group(1)[:80]}")

    # Idempotence (transform of transform = transform)
    once = transform(src, "en")
    twice = transform(once, "en")
    if once != twice:
        failures.append("idempotence violated for EN")

    # All 3 langs produce DIFFERENT output (sanity)
    en = transform(src, "en")
    fr = transform(src, "fr")
    es = transform(src, "es")
    if en == fr or en == es or fr == es:
        failures.append("two langs produced identical output (regex didn't match?)")

    if failures:
        print("SELF-TEST FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("ALL SELF-TESTS PASSED ✓")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        sys.exit(self_test())
    sys.exit(main_run(dry_run=args.dry_run))
