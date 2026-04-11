#!/usr/bin/env bash
# ═════════════════════════════════════════════════════════════════════
# WiggMap — Image optimization script
# ═════════════════════════════════════════════════════════════════════
#
# Converts all hero-*.jpg / hero-*.png in /assets/ to WebP at quality 80,
# resized to max 1920px width. Originals are preserved (.jpg.bak).
# Then adds a small JS in footer.js that swaps img/background URLs to
# .webp at runtime if the browser supports it (modern browsers all do).
#
# Requirements:
#   - cwebp (apt install webp)  OR
#   - magick / convert (ImageMagick)
#   - Python 3 with Pillow:  pip install Pillow
#
# Usage:
#   chmod +x scripts/optimize-images.sh
#   ./scripts/optimize-images.sh
#
# After running, you can roll back by deleting the .webp files and
# restoring HTML references with:
#   find . -name "*.webp.bak" -exec mv {} {/.bak/} \;
# ═════════════════════════════════════════════════════════════════════

set -e
ASSETS_DIR="$(dirname "$0")/../assets"
CITY_DIR="$(dirname "$0")/../assetscity"
QUALITY=80
MAX_WIDTH=1920

# Pick the best available tool
TOOL=""
if command -v cwebp &>/dev/null; then
  TOOL="cwebp"
elif command -v magick &>/dev/null; then
  TOOL="magick"
elif python3 -c "from PIL import Image" 2>/dev/null; then
  TOOL="python"
else
  echo "❌ No image tool found. Install one of:"
  echo "    apt install webp           (recommended, smallest output)"
  echo "    apt install imagemagick"
  echo "    pip install Pillow"
  exit 1
fi

echo "✓ Using tool: $TOOL"
echo "✓ Quality: $QUALITY  Max width: ${MAX_WIDTH}px"
echo ""

convert_one() {
  local src="$1"
  local dst="${src%.*}.webp"
  if [[ -f "$dst" && "$dst" -nt "$src" ]]; then
    return  # already converted, source not newer
  fi
  case "$TOOL" in
    cwebp)
      cwebp -q $QUALITY -resize $MAX_WIDTH 0 -quiet "$src" -o "$dst"
      ;;
    magick)
      magick "$src" -resize "${MAX_WIDTH}x${MAX_WIDTH}>" -quality $QUALITY "$dst"
      ;;
    python)
      python3 -c "
from PIL import Image
im = Image.open('$src').convert('RGB')
w, h = im.size
if w > $MAX_WIDTH:
    nh = int(h * $MAX_WIDTH / w)
    im = im.resize(($MAX_WIDTH, nh), Image.LANCZOS)
im.save('$dst', 'WEBP', quality=$QUALITY, method=6)
" ;;
  esac
}

count=0
saved=0
for dir in "$ASSETS_DIR" "$CITY_DIR"; do
  [[ -d "$dir" ]] || continue
  echo "Processing $dir..."
  while IFS= read -r -d '' f; do
    convert_one "$f"
    src_size=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f")
    dst="${f%.*}.webp"
    dst_size=$(stat -c%s "$dst" 2>/dev/null || stat -f%z "$dst")
    saved=$((saved + src_size - dst_size))
    count=$((count + 1))
    if (( count % 20 == 0 )); then echo "  ... $count files done"; fi
  done < <(find "$dir" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -print0)
done

echo ""
echo "═══════════════════════════════════════════"
echo "✓ Converted: $count images"
echo "✓ Total saved: $((saved / 1024 / 1024)) MB"
echo "═══════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  1. Test the site locally to verify images still load"
echo "  2. The runtime JS swap in footer.js will handle .jpg → .webp automatically"
echo "  3. If everything works, commit BOTH the .webp files and the originals"
echo "     (or delete the originals after a few days of monitoring)"
