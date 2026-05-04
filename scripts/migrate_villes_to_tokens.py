#!/usr/bin/env python3
"""
migrate_villes_to_tokens.py — Sprint Y.6.

Patches the 228 chronicles/villes/*.html files. Conservative because each
city chronicle has its own intentional per-city accent palette (memory:
city-chronicles-format.md):
  - --g, --gd, --gp local CSS vars (per-city brand color)
  - theme-color = city signature (Bali #0d9488, Tokyo #dc2626, etc.)
  - Per-city fonts (Bali: Playfair Display + DM Serif + DM Sans;
    others differ)

What this script DOES (safe transformations)
--------------------------------------------
1. Inject <link rel="stylesheet" href="/assets/wm-tokens.css"> (provides
   --green charter as system-wide fallback; per-city --g/--gd/--gp
   continue to override locally because they're declared in inline :root).
2. Inject <script>window.__WM_DISABLE_WEBP_SWAP=true;</script> (Sprint Y.5
   parity — perf gain on LCP).
3. Wrap <img src="/assets/X.jpg"> in <picture> SSR with WebP source.

What this script DOES NOT touch
-------------------------------
- --g, --gd, --gp inline CSS vars (per-city palette)
- theme-color meta (per-city signature, see data-category-color
  convention from Sprint 1 a749c8e + Sprint Y.1 tokens.css)
- Per-city fonts (Playfair, DM Serif, DM Sans, etc.)
- Body content / images / structure
- canonical, hreflang, JSON-LD

USAGE
-----
  python3 scripts/migrate_villes_to_tokens.py --dry-run
  python3 scripts/migrate_villes_to_tokens.py --self-test
  python3 scripts/migrate_villes_to_tokens.py
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VILLES_DIR = REPO / "chronicles" / "villes"
TOKENS_LINK = '<link rel="stylesheet" href="/assets/wm-tokens.css">'
DISABLE_SWAP_SNIPPET = '<script>window.__WM_DISABLE_WEBP_SWAP=true;</script>'
DISABLE_SWAP_RE = re.compile(r'window\.__WM_DISABLE_WEBP_SWAP\s*=\s*true', re.IGNORECASE)
IMG_JPG_RE = re.compile(
    r'(<img\b[^>]*?\bsrc="(/assets[a-zA-Z]*?/[^"]+)\.jpg"[^>]*?>)',
    re.IGNORECASE,
)


def transform(src: str) -> str:
    """Apply transforms. Idempotent."""
    out = src

    # 1. Inject tokens.css (idempotent)
    if "wm-tokens.css" not in out:
        out = re.sub(
            r'(<meta\s+charset[^>]*/?>)',
            r'\1\n  ' + TOKENS_LINK,
            out, count=1,
        )

    # 2. Inject __WM_DISABLE_WEBP_SWAP opt-out (idempotent)
    if not DISABLE_SWAP_RE.search(out):
        if "</title>" in out:
            out = out.replace("</title>", "</title>\n  " + DISABLE_SWAP_SNIPPET, 1)
        else:
            out = re.sub(r'(<head[^>]*>)', r'\1\n  ' + DISABLE_SWAP_SNIPPET, out, count=1)

    # 3. Wrap <img src=*.jpg> in <picture> (skip already-wrapped)
    picture_spans = []
    for m in re.finditer(r'<picture\b[^>]*>.*?</picture>', out, re.DOTALL):
        picture_spans.append((m.start(), m.end()))

    def is_inside_picture(pos):
        return any(s <= pos < e for s, e in picture_spans)

    result = []
    last = 0
    for m in IMG_JPG_RE.finditer(out):
        if is_inside_picture(m.start()):
            continue
        full = m.group(1)
        base = m.group(2)
        webp = base + ".webp"
        result.append(out[last:m.start()])
        result.append(f'<picture><source srcset="{webp}" type="image/webp">{full}</picture>')
        last = m.end()
    result.append(out[last:])
    return "".join(result)


def main_run(dry_run: bool = False) -> int:
    files = sorted(VILLES_DIR.glob("*.html"))
    if not files:
        print(f"FATAL: no city chronicles in {VILLES_DIR}", file=sys.stderr)
        return 2

    written = 0
    unchanged = 0
    pic_added_total = 0
    for f in files:
        src = f.read_text(encoding="utf-8")
        new = transform(src)
        if new == src:
            unchanged += 1
            continue
        added = new.count("<picture>") - src.count("<picture>")
        pic_added_total += added
        if not dry_run:
            f.write_text(new, encoding="utf-8")
        written += 1

    print(f"\n{'[DRY] ' if dry_run else ''}Summary: {written} modified, {unchanged} unchanged, {len(files)} total. <picture> added: {pic_added_total}")
    return 0


def self_test() -> int:
    fixture = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Bali</title>
<link rel="canonical" href="https://wiggmap.com/chronicles/villes/chronicle-bali-indonesia-en.html"/>
<meta name="theme-color" content="#0d9488" />
<style>:root{--g:#0d9488;--gd:#0f766e;--gp:#f0fdfa;--serif:'Playfair Display',Georgia,serif}</style>
</head>
<body>
<img src="/assets/hero-indonesia.jpg" alt="Indonesia">
<img src="/assetscity/bali.jpg" alt="Bali">
</body>
</html>
'''
    out = transform(fixture)
    failures = []
    if "wm-tokens.css" not in out:
        failures.append("tokens link missing")
    if DISABLE_SWAP_SNIPPET not in out:
        failures.append("opt-out script missing")
    # Per-city palette MUST be preserved
    if "--g:#0d9488" not in out:
        failures.append("per-city --g preserved? FAIL")
    if "#0d9488" not in out:
        failures.append("city signature theme-color stripped")
    if "Playfair Display" not in out:
        failures.append("per-city font stripped")
    if 'srcset="/assets/hero-indonesia.webp"' not in out:
        failures.append("hero-indonesia not wrapped")
    if 'srcset="/assetscity/bali.webp"' not in out:
        failures.append("assetscity/bali not wrapped")
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
    print("ALL SELF-TESTS PASSED ✓ (9 assertions)")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        sys.exit(self_test())
    sys.exit(main_run(dry_run=args.dry_run))
