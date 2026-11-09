#!/usr/bin/env python3
"""Build the eight files a site photograph needs.

    python3 make_photo.py <source-image> <key>

writes <key>.jpeg, <key>.webp and -md / -sm / -xs in both formats into the
site root, at the widths the markup asks for: 1280, 768, 640, 320. Aspect
ratio is kept, so `photo()` can emit real intrinsic dimensions and nothing
reflows when a file lands.

Why not optimize_images.py: that script rewrites its inputs in place, which
re-compresses an already compressed file on a second run, and it only knows
about the ten gallery images and the instructor portrait. This one always
reads a source it never writes to, and takes any key.

The quality settings match what the existing files were built with - 82 for
the full JPEG, 80 for the full WebP, 80/78 for the derivatives.
"""
import os
import sys

from PIL import Image

ROOT = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

# (suffix, width, jpeg quality, webp quality). The full size keeps the .jpeg
# extension the rest of the site expects; the derivatives use .jpg, which is
# the convention already on disk.
TIERS = [("", 1280, 82, 80), ("-md", 768, 80, 78),
         ("-sm", 640, 80, 78), ("-xs", 320, 80, 78)]


def fit_width(im, w):
    if im.width <= w:
        return im
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src_path, key = sys.argv[1], sys.argv[2]
    src = Image.open(src_path).convert("RGB")
    out = []
    for suffix, width, jq, wq in TIERS:
        im = fit_width(src, width)
        jpg = f"{key}{suffix}.{'jpeg' if suffix == '' else 'jpg'}"
        for path, kw in ((jpg, dict(format="JPEG", quality=jq,
                                    optimize=True, progressive=True)),
                         (f"{key}{suffix}.webp",
                          dict(format="WEBP", quality=wq, method=6))):
            dest = os.path.join(ROOT, path)
            im.save(dest, **kw)
            out.append((path, im.size, os.path.getsize(dest) / 1024))

    total = 0.0
    for path, size, kb in out:
        total += kb
        print(f"{path:22s} {size[0]:>5}x{size[1]:<5} {kb:7.1f} KB")
    print(f"{'TOTAL':22s} {'':>11} {total:7.1f} KB")


if __name__ == "__main__":
    main()
