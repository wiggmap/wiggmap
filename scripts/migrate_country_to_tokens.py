#!/usr/bin/env python3
"""
migrate_country_to_tokens.py — Sprint Y.3.

Idempotent script to patch the 484 countries/*.html files:
1. Inject <link rel="stylesheet" href="/assets/wm-tokens.css"> in <head>
2. Replace theme-color #1d7f48 → #1a5430
3. Replace inline :root{} drift hex values:
   - --green:#1d7f48 → --green:#1a5430
4. Replace #15803d (art-tag color) → #1a5430
5. Replace any remaining #1d7f48 / #1c7c46 / #1a7a45 → #1a5430

Preserves:
- canonical, hreflang, JSON-LD
- All structural HTML
- Country-specific content / hero images
- CTA bright #22c55e + hover #16a34a (D4)

USAGE
-----
  python3 scripts/migrate_country_to_tokens.py --dry-run    # preview only
  python3 scripts/migrate_country_to_tokens.py --self-test  # internal tests
  python3 scripts/migrate_country_to_tokens.py              # actual write
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COUNTRIES_DIR = REPO / "countries"
TOKENS_LINK = '<link rel="stylesheet" href="/assets/wm-tokens.css">'

# Forest variants → charter
DRIFT_HEX = {
    "#1d7f48": "#1a5430",  # forest variant — theme-color + --green inline
    "#15803d": "#1a5430",  # Tailwind green-700 — art-tag color in body text
    "#1c7c46": "#1a5430",  # legacy variant
    "#1a7a45": "#1a5430",  # very legacy
}


def transform(src: str) -> str:
    """Apply all transforms. Idempotent."""
    out = src

    # 1. Inject <link rel=stylesheet> after <meta charset> (idempotent guard)
    if "wm-tokens.css" not in out:
        out = re.sub(
            r'(<meta\s+charset[^>]*/?>\s*\n)',
            r'\1' + TOKENS_LINK + '\n',
            out,
            count=1,
        )

    # 2-5. Replace drift hex values, line by line, skipping data-category-color lines
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
    return "\n".join(new_lines)


def main_run(dry_run: bool = False) -> int:
    files = sorted(COUNTRIES_DIR.glob("*.html"))
    if not files:
        print(f"FATAL: no HTML files in {COUNTRIES_DIR}", file=sys.stderr)
        return 2

    written = 0
    unchanged = 0
    sample_log = []
    for f in files:
        src = f.read_text(encoding="utf-8")
        new = transform(src)
        if new == src:
            unchanged += 1
            continue
        if dry_run:
            if len(sample_log) < 5:
                drift_count = sum(src.count(d) for d in DRIFT_HEX)
                sample_log.append(f"  [DRY] {f.name}: drift hex refs={drift_count}, would write {len(new)} bytes")
            written += 1
        else:
            f.write_text(new, encoding="utf-8")
            written += 1

    if dry_run and sample_log:
        for line in sample_log:
            print(line)
        print(f"  ... ({written} files would be modified, {unchanged} unchanged)")
    print(f"\n{'[DRY] ' if dry_run else ''}Summary: {written} modified, {unchanged} unchanged, {len(files)} total")
    return 0


def self_test() -> int:
    fixture = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Test</title>
<link rel="canonical" href="https://wiggmap.com/countries/test-en.html" />
<meta name="theme-color" content="#1d7f48" />
<style>:root{--green:#1d7f48;--green-dk:#155f36}</style>
</head>
<body>
<a class="wm-skip" href="#wm-main">Skip</a>
<a id="wm-main"></a>
<p><span style="color:#15803d">Hello</span></p>
<p>Bright CTA: <span style="background:#22c55e">go</span></p>
</body>
</html>
'''
    out = transform(fixture)
    failures = []
    if "wm-tokens.css" not in out:
        failures.append("tokens link not injected")
    if "#1d7f48" in out:
        failures.append("forest drift #1d7f48 still present")
    if "#15803d" in out:
        failures.append("forest drift #15803d still present")
    if "#1a5430" not in out:
        failures.append("charter forest #1a5430 not injected")
    if "#22c55e" not in out:
        failures.append("CTA bright #22c55e was wrongly stripped")
    if 'class="wm-skip"' not in out:
        failures.append("skip-link wm-skip lost")
    if "rel=\"canonical\"" not in out:
        failures.append("canonical lost")
    # Idempotence
    out2 = transform(out)
    if out != out2:
        failures.append("idempotence violated")

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
