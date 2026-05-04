#!/usr/bin/env python3
"""
migrate_hero_to_picture.py — Sprint Y.5.

Wraps the LCP hero image on each country page in a <picture> element with
WebP source + JPG fallback, AND adds a <script>window.__WM_DISABLE_WEBP_SWAP=true;</script>
to <head> so the runtime swap in footer.js (Sprint D1 8c6e690) is opted out.

Net effect per page: -1 round-trip per <img>, eliminates the 33+ "test"
fetches that runtime swap performs on country pages.

Targets only <img class="hero-img" ...> (the LCP hero, 1 per page).
Other <img> tags (rc-vimg related chronicles carousel) keep their .jpg
form for now — runtime swap is disabled, so they'll be served as JPG
which is suboptimal but acceptable until a future <picture> SSR pass.

Wait — disabling runtime swap on rc-vimg means they stay JPG. To avoid
that regression, this script ALSO wraps rc-vimg <img> tags in <picture>.

USAGE
-----
  python3 scripts/migrate_hero_to_picture.py --dry-run
  python3 scripts/migrate_hero_to_picture.py --self-test
  python3 scripts/migrate_hero_to_picture.py
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COUNTRIES_DIR = REPO / "countries"

# Pattern for <img> with src="/assets/...jpg" — we wrap in <picture>
# Must be careful with the regex: capture the full <img ...> tag and the
# src attribute value, then emit a <picture> wrapper.
IMG_JPG_RE = re.compile(
    r'(<img\b[^>]*?\bsrc="(/assets/[^"]+)\.jpg"[^>]*?>)',
    re.IGNORECASE,
)

DISABLE_SWAP_SNIPPET = '<script>window.__WM_DISABLE_WEBP_SWAP=true;</script>'

DISABLE_SWAP_RE = re.compile(r'window\.__WM_DISABLE_WEBP_SWAP\s*=\s*true', re.IGNORECASE)


def transform(src: str) -> str:
    """Apply transforms. Idempotent."""
    out = src

    # 1. Inject <script>window.__WM_DISABLE_WEBP_SWAP=true;</script> in <head>
    #    only if not already present.
    if not DISABLE_SWAP_RE.search(out):
        # Inject right after the <head> opening tag (or after first <script>
        # block if any). Prefer "right after </title>" for visibility.
        if "</title>" in out:
            out = out.replace("</title>", "</title>\n  " + DISABLE_SWAP_SNIPPET, 1)
        else:
            # Fallback: after <head>
            out = re.sub(r'(<head[^>]*>)', r'\1\n  ' + DISABLE_SWAP_SNIPPET, out, count=1)

    # 2. Wrap <img src="/assets/X.jpg"> in <picture><source webp><img></picture>
    #    Skip if already inside a <picture> (idempotence).
    def replace_img(m):
        full = m.group(1)
        base = m.group(2)  # "/assets/hero-portugal" (no .jpg)
        # Don't wrap if the immediate context already has a <picture>
        # (we run a per-replacement check via a post-pass later if needed).
        webp_url = base + ".webp"
        return f'<picture><source srcset="{webp_url}" type="image/webp">{full}</picture>'

    # Track which positions are already inside <picture>
    # Simple heuristic: find <picture> spans, skip <img> inside them
    picture_spans = []
    for m in re.finditer(r'<picture\b[^>]*>.*?</picture>', out, re.DOTALL):
        picture_spans.append((m.start(), m.end()))

    def is_inside_picture(pos):
        return any(s <= pos < e for s, e in picture_spans)

    # Apply replacement only outside existing <picture> wrappers
    result = []
    last = 0
    for m in IMG_JPG_RE.finditer(out):
        if is_inside_picture(m.start()):
            continue
        result.append(out[last:m.start()])
        result.append(replace_img(m))
        last = m.end()
    result.append(out[last:])
    return "".join(result)


def main_run(dry_run: bool = False) -> int:
    files = sorted(COUNTRIES_DIR.glob("*.html"))
    if not files:
        print(f"FATAL: no country pages in {COUNTRIES_DIR}", file=sys.stderr)
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

    print(f"\n{'[DRY] ' if dry_run else ''}Summary: {written} modified, {unchanged} unchanged, {len(files)} total. <picture> wrappers added: {pic_added_total}")
    return 0


def self_test() -> int:
    fixture = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Test</title>
<link rel="canonical" href="https://wiggmap.com/test.html"/>
</head>
<body>
<img class="hero-img" src="/assets/hero-portugal.jpg" alt="Portugal">
<picture><source srcset="/assets/already.webp" type="image/webp"><img src="/assets/already.jpg" alt="x"></picture>
<img class="rc-vimg" src="/assets/hero-uae.jpg" alt="UAE" loading="lazy">
</body>
</html>
'''
    out = transform(fixture)
    failures = []
    if DISABLE_SWAP_SNIPPET not in out:
        failures.append("opt-out script not injected")
    if out.count("<picture>") < 3:  # 1 already + 2 new (hero + rc-vimg)
        failures.append(f"expected 3 <picture> wrappers, got {out.count('<picture>')}")
    if 'srcset="/assets/hero-portugal.webp"' not in out:
        failures.append("hero-portugal webp source missing")
    if 'srcset="/assets/hero-uae.webp"' not in out:
        failures.append("hero-uae webp source missing")
    # Already-wrapped picture should NOT be re-wrapped
    if out.count('<picture>') > 3:
        failures.append("re-wrapped already-wrapped <img> (idempotence violated)")
    # Idempotence: 2nd run = no change
    out2 = transform(out)
    if out != out2:
        failures.append("2nd run produced different output (idempotence failed)")
    # Ensure ALL original tags preserved
    if 'rel="canonical"' not in out:
        failures.append("canonical lost")

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
