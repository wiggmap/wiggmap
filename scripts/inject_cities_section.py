#!/usr/bin/env python3
"""
inject_cities_section.py — Sprint AUDIT 5.2 + 1.8.

Inject a "Cities in {country}" section into country pages that have at least
one city chronicle. The section appears just before the closing </main>
(or before the footer if no <main>) and links to the city chronicle URLs.

Builds the country↔cities mapping from chronicle filenames at runtime and
applies a hand-maintained slug translation table to bridge FR-style slugs
in chronicle filenames (espagne, turquie, grece...) with EN slugs in
country pages (spain, turkey, greece...).

Idempotent: re-running produces byte-identical output (a marker comment
and the section's stable id make detection trivial).
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COUNTRIES_DIR = REPO / "countries"
VILLES_DIR = REPO / "chronicles" / "villes"

# Hand-maintained: chronicle ville country slug → WiggMap country page slug
# Built by listing the 19 distinct country slugs in chronicle filenames and
# mapping each to its WiggMap counterpart.
SLUG_FR_TO_WIGG = {
    "emirats": "united-arab-emirates",
    "turquie": "turkey",
    "grece": "greece",
    "usa": "united-states",
    "indonesia": "indonesia",
    "thailand": "thailand",
    "espagne": "spain",
    "argentine": "argentina",
    "allemagne": "germany",
    "colombie": "colombia",
    "japan": "japan",
    "australia": "australia",
    "canada": "canada",
    "portugal": "portugal",
    "malaisie": "malaysia",
    "mexico": "mexico",
    "france": "france",
    "italie": "italy",
    "philippines": "philippines",
}

# Per-lang headings + intro
I18N = {
    "en": {
        "heading": "Cities in {country}",
        "intro": "Detailed city chronicles published on WiggMap:",
    },
    "fr": {
        "heading": "Villes en {country}",
        "intro": "Chroniques détaillées sur WiggMap :",
    },
    "es": {
        "heading": "Ciudades en {country}",
        "intro": "Crónicas detalladas en WiggMap:",
    },
}

# Display country names (lang-specific)
COUNTRY_DISPLAY = {
    "united-arab-emirates": {"en": "the UAE", "fr": "Émirats", "es": "EAU"},
    "turkey": {"en": "Turkey", "fr": "Turquie", "es": "Turquía"},
    "greece": {"en": "Greece", "fr": "Grèce", "es": "Grecia"},
    "united-states": {"en": "the USA", "fr": "USA", "es": "EE.UU."},
    "indonesia": {"en": "Indonesia", "fr": "Indonésie", "es": "Indonesia"},
    "thailand": {"en": "Thailand", "fr": "Thaïlande", "es": "Tailandia"},
    "spain": {"en": "Spain", "fr": "Espagne", "es": "España"},
    "argentina": {"en": "Argentina", "fr": "Argentine", "es": "Argentina"},
    "germany": {"en": "Germany", "fr": "Allemagne", "es": "Alemania"},
    "colombia": {"en": "Colombia", "fr": "Colombie", "es": "Colombia"},
    "japan": {"en": "Japan", "fr": "Japon", "es": "Japón"},
    "australia": {"en": "Australia", "fr": "Australie", "es": "Australia"},
    "canada": {"en": "Canada", "fr": "Canada", "es": "Canadá"},
    "portugal": {"en": "Portugal", "fr": "Portugal", "es": "Portugal"},
    "malaysia": {"en": "Malaysia", "fr": "Malaisie", "es": "Malasia"},
    "mexico": {"en": "Mexico", "fr": "Mexique", "es": "México"},
    "france": {"en": "France", "fr": "France", "es": "Francia"},
    "italy": {"en": "Italy", "fr": "Italie", "es": "Italia"},
    "philippines": {"en": "the Philippines", "fr": "Philippines", "es": "Filipinas"},
}

MARKER_BEGIN = "<!-- WM-CITIES-SECTION-BEGIN -->"
MARKER_END = "<!-- WM-CITIES-SECTION-END -->"


def build_country_to_cities() -> dict[str, dict[str, list[str]]]:
    """Returns {wigg_country_slug: {lang: [city_slug, ...]}}."""
    mapping: dict[str, dict[str, list[str]]] = {}
    for f in sorted(VILLES_DIR.glob("chronicle-*.html")):
        m = re.match(r"^chronicle-([a-z0-9-]+)-(en|fr|es)\.html$", f.name)
        if not m:
            continue
        slug_full, lang = m.group(1), m.group(2)
        parts = slug_full.split("-")
        if len(parts) < 2:
            continue
        country_fr = parts[-1]
        city = "-".join(parts[:-1])
        wigg = SLUG_FR_TO_WIGG.get(country_fr)
        if not wigg:
            continue  # skip countries we don't have a mapping for
        mapping.setdefault(wigg, {}).setdefault(lang, []).append(city)
    # Sort each city list alphabetically
    for wigg in mapping:
        for lang in mapping[wigg]:
            mapping[wigg][lang] = sorted(set(mapping[wigg][lang]))
    return mapping


def render_section(wigg_country: str, lang: str, cities: list[str]) -> str:
    """Render the HTML section for a country in a given lang."""
    if not cities:
        return ""
    country_display = COUNTRY_DISPLAY.get(wigg_country, {}).get(lang, wigg_country.replace("-", " ").title())
    t = I18N[lang]
    heading = t["heading"].format(country=country_display)
    intro = t["intro"]

    # Find the original chronicle filename for each city to build the link.
    # Pattern: /chronicles/villes/chronicle-{city}-{country_fr}-{lang}.html
    # We need to know the FR-style country slug to reconstruct the link.
    # Reverse-lookup: find the FR slug whose mapping matches `wigg_country`.
    country_fr = next((fr for fr, wg in SLUG_FR_TO_WIGG.items() if wg == wigg_country), wigg_country)

    items = []
    for city in cities:
        href = f"/chronicles/villes/chronicle-{city}-{country_fr}-{lang}.html"
        title = city.replace("-", " ").title()
        items.append(f'      <li><a href="{href}">{title}</a></li>')

    items_html = "\n".join(items)
    section = f"""{MARKER_BEGIN}
<section class="wm-cities-in-country" style="margin:32px 0;padding:24px 28px;background:var(--paper, #fffdf8);border:1px solid var(--rule, #c8bfaa);border-radius:14px;">
  <h2 style="font-family:var(--font-display, 'Fraunces', Georgia, serif);font-size:22px;font-weight:700;color:var(--green, #1a5430);margin:0 0 8px;">{heading}</h2>
  <p style="font-size:13px;color:var(--ink-soft, #54554e);margin:0 0 14px;">{intro}</p>
  <ul style="list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px;">
{items_html}
  </ul>
  <style>.wm-cities-in-country ul a{{display:inline-block;padding:7px 14px;background:var(--green-tint, rgba(26,84,48,0.08));color:var(--green, #1a5430);border-radius:999px;font-size:13px;font-weight:600;text-decoration:none;transition:background .15s}}.wm-cities-in-country ul a:hover{{background:var(--green, #1a5430);color:#fff}}</style>
</section>
{MARKER_END}"""
    return section


def transform(src: str, wigg_country: str, lang: str, cities: list[str]) -> str:
    """Inject (or replace) the cities section. Idempotent."""
    if not cities:
        return src

    # Strip any existing section (for idempotence + updates)
    src = re.sub(
        re.escape(MARKER_BEGIN) + ".*?" + re.escape(MARKER_END) + "\n?",
        "",
        src,
        flags=re.DOTALL,
    )

    section = render_section(wigg_country, lang, cities) + "\n"

    # Inject before </main> if present, else before </body>
    if "</main>" in src:
        src = src.replace("</main>", section + "</main>", 1)
    elif "</body>" in src:
        src = src.replace("</body>", section + "</body>", 1)
    else:
        src = src + "\n" + section
    return src


def main_run(dry_run: bool = False) -> int:
    mapping = build_country_to_cities()
    print(f"Country↔cities map: {len(mapping)} countries with chronicle villes.")
    written = 0
    skipped = 0
    for wigg_country, by_lang in mapping.items():
        for lang in ("en", "fr", "es"):
            cities = by_lang.get(lang, [])
            if not cities:
                continue
            target = COUNTRIES_DIR / f"{wigg_country}-{lang}.html"
            if not target.exists():
                print(f"  SKIP {target.name}: country page does not exist")
                skipped += 1
                continue
            src = target.read_text(encoding="utf-8")
            new = transform(src, wigg_country, lang, cities)
            if new == src:
                continue
            if dry_run:
                written += 1
            else:
                target.write_text(new, encoding="utf-8")
                written += 1
    print(f"\n{'[DRY] ' if dry_run else ''}Summary: {written} country pages enriched, {skipped} skipped (missing target)")
    return 0


def self_test() -> int:
    fixture = '''<!DOCTYPE html>
<html lang="en"><head><title>Test</title></head>
<body>
<main>
<h1>Portugal</h1>
<p>some content</p>
</main>
</body></html>
'''
    out = transform(fixture, "portugal", "en", ["lisbonne", "porto"])
    failures = []
    if MARKER_BEGIN not in out: failures.append("marker BEGIN missing")
    if MARKER_END not in out: failures.append("marker END missing")
    if "Cities in Portugal" not in out: failures.append("heading missing")
    if "/chronicles/villes/chronicle-lisbonne-portugal-en.html" not in out:
        failures.append("link to Lisbon chronicle ville missing")
    if "/chronicles/villes/chronicle-porto-portugal-en.html" not in out:
        failures.append("link to Porto missing")
    # Idempotence
    out2 = transform(out, "portugal", "en", ["lisbonne", "porto"])
    if out != out2:
        failures.append("idempotence violated")
    # Updating with new cities replaces the old section
    out3 = transform(out, "portugal", "en", ["lisbonne", "porto", "faro"])
    if out3.count(MARKER_BEGIN) != 1:
        failures.append(f"multiple marker blocks after update: {out3.count(MARKER_BEGIN)}")
    if "/chronicles/villes/chronicle-faro-portugal-en.html" not in out3:
        failures.append("update did not insert new city")

    if failures:
        print("SELF-TEST FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("ALL SELF-TESTS PASSED ✓ (7 assertions)")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        sys.exit(self_test())
    sys.exit(main_run(dry_run=args.dry_run))
