#!/usr/bin/env python3
"""
migrate_chronicles_to_tokens.py — Sprint Y.4.

Idempotent migration of the 75 thematic chronicle files (chronicles/*.html
excluding /villes/). Same pattern as migrate_country_to_tokens.py but with
two extra purges specific to chronicles thematic:

- Inject <link rel=stylesheet href=/assets/wm-tokens.css>
- Replace #22c55e/#16a34a/#15803d/#1d7f48/#1c7c46 → forest charter
  (on chronicles thematic, these were used as "--green" alias which is
  drift; chronicles do NOT have CTA buttons that need bright variants)
- Replace Poppins font → Inter (D3 Sprint Y arbitrage)
- Skip lines containing data-category-color (preserve category overrides)
- Preserve canonical, hreflang, JSON-LD (Article + FAQPage), skip-link
  (Sprint 1) where present, all body content / images / structure

USAGE
-----
  python3 scripts/migrate_chronicles_to_tokens.py --dry-run
  python3 scripts/migrate_chronicles_to_tokens.py --self-test
  python3 scripts/migrate_chronicles_to_tokens.py
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHRONICLES_DIR = REPO / "chronicles"
TOKENS_LINK = '<link rel="stylesheet" href="/assets/wm-tokens.css">'

# Forest drift on chronicles thematic — #22c55e and #16a34a were used as
# --green/--green-dark aliases (NOT as CTA bright). Replace with charter.
DRIFT_HEX = {
    "#22c55e": "#1a5430",   # was misused as --green (charter is forest)
    "#16a34a": "#155f36",   # was misused as --green-dark (charter is #155f36)
    "#15803d": "#1a5430",
    "#1d7f48": "#1a5430",
    "#1c7c46": "#1a5430",
    "#1a7a45": "#1a5430",
}

# Poppins → Inter (D3 sprint Y arbitrage)
POPPINS_PATTERN = re.compile(r'\bPoppins\b')
POPPINS_REPLACEMENT = "Inter"


def transform(src: str) -> str:
    """Apply transforms. Idempotent."""
    out = src

    # 1. Inject tokens.css link (idempotent).
    # Note: some chronicles have <meta charset>+<meta viewport> on the SAME line
    # (no newline between them). Match charset tag with optional trailing whitespace
    # including newline — without forcing a newline.
    if "wm-tokens.css" not in out:
        out = re.sub(
            r'(<meta\s+charset[^>]*/?>)',
            r'\1\n' + TOKENS_LINK,
            out, count=1,
        )

    # 2. Drift hex replacement, line-by-line, skip data-category-color
    lines = out.split("\n")
    new_lines = []
    for line in lines:
        if "data-category-color" in line:
            new_lines.append(line)
            continue
        new_line = line
        for drift, canonical in DRIFT_HEX.items():
            new_line = new_line.replace(drift, canonical)
        new_lines.append(new_line)
    out = "\n".join(new_lines)

    # 3. Poppins → Inter (D3)
    out = POPPINS_PATTERN.sub(POPPINS_REPLACEMENT, out)

    return out


def main_run(dry_run: bool = False) -> int:
    # Top-level chronicles only — skip /villes/ subdir (Sprint Y.6 separate)
    files = [f for f in sorted(CHRONICLES_DIR.glob("*.html")) if f.is_file()]
    if not files:
        print(f"FATAL: no thematic chronicles in {CHRONICLES_DIR}", file=sys.stderr)
        return 2

    written = 0
    unchanged = 0
    for f in files:
        src = f.read_text(encoding="utf-8")
        new = transform(src)
        if new == src:
            unchanged += 1
            continue
        if dry_run:
            written += 1
        else:
            f.write_text(new, encoding="utf-8")
            written += 1

    print(f"\n{'[DRY] ' if dry_run else ''}Summary: {written} modified, {unchanged} unchanged, {len(files)} total")
    return 0


def self_test() -> int:
    fixture = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Test</title>
<link rel="canonical" href="https://wiggmap.com/chronicles/test-en.html" />
<meta name="theme-color" content="#22c55e" />
<style>:root{--green:#22c55e;--green-dark:#16a34a;--sans:'Poppins',system-ui,sans-serif}</style>
</head>
<body>
<a class="wm-skip" href="#wm-main">Skip</a>
<a id="wm-main"></a>
<span class="tag-easy" style="color:#15803d">tag</span>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage"}</script>
</body>
</html>
'''
    out = transform(fixture)
    failures = []
    if "wm-tokens.css" not in out:
        failures.append("tokens link not injected")
    if "#22c55e" in out:
        failures.append("drift #22c55e still present")
    if "#16a34a" in out:
        failures.append("drift #16a34a still present")
    if "#15803d" in out:
        failures.append("drift #15803d still present")
    if "#1a5430" not in out:
        failures.append("charter forest #1a5430 not injected")
    if "#155f36" not in out:
        failures.append("charter forest-dark #155f36 not injected")
    if "Poppins" in out:
        failures.append("Poppins not purged")
    if "Inter" not in out:
        failures.append("Inter not substituted")
    if 'class="wm-skip"' not in out:
        failures.append("skip-link lost")
    if '"FAQPage"' not in out:
        failures.append("JSON-LD FAQPage lost")
    if 'rel="canonical"' not in out:
        failures.append("canonical lost")
    out2 = transform(out)
    if out != out2:
        failures.append("idempotence violated")

    if failures:
        print("SELF-TEST FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("ALL SELF-TESTS PASSED ✓ (12 assertions)")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        sys.exit(self_test())
    sys.exit(main_run(dry_run=args.dry_run))
