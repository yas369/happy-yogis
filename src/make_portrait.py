#!/usr/bin/env python3
"""Build the three responsive derivatives a teacher portrait needs.

    python3 make_portrait.py <source-image> <stem>

writes <stem>.jpeg, <stem>.webp, <stem>-sm.webp and <stem>-xs.webp into the
site root, all cropped to 4:5 - the aspect the arch frame on the teacher
section renders at, so nothing is downloaded only to be cropped away by
object-fit.

The widths (300 / 560 / 720) and the 4:5 crop match
`instructor-portrait*`, which was built by hand before this script existed.
Keep them in step: the <picture> srcset in pages.py and ta_pages.py names
these exact filenames and widths.

Portraits are deliberately not run through optimize_images.py. That script
rewrites its inputs in place, so running it twice re-compresses an already
compressed file; this one always reads a source it does not touch.
"""
import os
import sys

from PIL import Image

ROOT = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

ASPECT = 4 / 5
FULL = (720, 900)
SM = (560, 700)
XS = (300, 375)


def crop_to_aspect(im, aspect):
    """Centre-crop to `aspect`, which for a portrait means taking the excess
    off the top and bottom rather than the sides - a head is horizontally
    centred far more reliably than it is vertically."""
    w, h = im.size
    if w / h > aspect:                       # too wide: trim the sides
        nw = round(h * aspect)
        left = (w - nw) // 2
        return im.crop((left, 0, left + nw, h))
    nh = round(w / aspect)                   # too tall: trim top and bottom
    top = (h - nh) // 2
    return im.crop((0, top, w, top + nh))


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src_path, stem = sys.argv[1], sys.argv[2]

    src = crop_to_aspect(Image.open(src_path).convert("RGB"), ASPECT)
    out = []

    full = src.resize(FULL, Image.LANCZOS)
    for path, im, kw in (
            (f"{stem}.jpeg", full, dict(format="JPEG", quality=82,
                                        optimize=True, progressive=True)),
            (f"{stem}.webp", full, dict(format="WEBP", quality=80, method=6)),
            (f"{stem}-sm.webp", src.resize(SM, Image.LANCZOS),
             dict(format="WEBP", quality=78, method=6)),
            (f"{stem}-xs.webp", src.resize(XS, Image.LANCZOS),
             dict(format="WEBP", quality=78, method=6))):
        dest = os.path.join(ROOT, path)
        im.save(dest, **kw)
        out.append((path, im.size, os.path.getsize(dest) / 1024))

    for path, size, kb in out:
        print(f"{path:30s} {size[0]:>4}x{size[1]:<4} {kb:7.1f} KB")


if __name__ == "__main__":
    main()
