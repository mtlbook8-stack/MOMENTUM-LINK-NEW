"""Generate responsive WebP + JPEG variants from the source PNG artwork."""
import glob, json, os, sys
from PIL import Image

SRC = sys.argv[1]
OUT = sys.argv[2]
WIDTHS = (1536, 768)

os.makedirs(OUT, exist_ok=True)
files = sorted(glob.glob(os.path.join(SRC, "*.png")))
total_in = total_out = 0

# Real dimensions per image, so the pages can declare the right intrinsic size
# instead of assuming every source shares one aspect ratio.
manifest = {}

for path in files:
    stem = os.path.splitext(os.path.basename(path))[0]
    total_in += os.path.getsize(path)
    img = Image.open(path).convert("RGB")
    manifest[stem] = [WIDTHS[0], round(img.height * WIDTHS[0] / img.width)]
    for w in WIDTHS:
        h = round(img.height * w / img.width)
        resized = img if w == img.width else img.resize((w, h), Image.LANCZOS)
        suffix = "" if w == WIDTHS[0] else f"-{w}"
        for ext, opts in (("webp", dict(quality=78, method=6)),
                          ("jpg", dict(quality=82, optimize=True, progressive=True))):
            dest = os.path.join(OUT, f"{stem}{suffix}.{ext}")
            resized.save(dest, **opts)
            total_out += os.path.getsize(dest)
    print(stem, flush=True)

with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, indent=1, sort_keys=True)

print(f"DONE {len(files)} sources  {total_in/1e6:.1f}MB -> {total_out/1e6:.1f}MB")
