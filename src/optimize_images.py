#!/usr/bin/env python3
"""Generate web-optimised derivatives for the Happy Yogis site.

Originals are preserved in git history (commit b7e4024 / a891652); this script
rewrites the working-copy JPEG/PNG assets at display-appropriate sizes and adds
WebP siblings plus favicons.
"""
import os
from PIL import Image

# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
ROOT = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

GALLERY = [f"ima{i}.jpeg" for i in range(1, 11)]
LARGE_MAX = 1280          # long edge for full-size / lightbox use
THUMB = (640, 427)        # 3:2 gallery card (rendered 288x192 CSS px)


def center_crop_resize(im, size):
    tw, th = size
    target = tw / th
    w, h = im.size
    cur = w / h
    if cur > target:                      # too wide -> crop sides
        nw = int(h * target)
        left = (w - nw) // 2
        im = im.crop((left, 0, left + nw, h))
    else:                                 # too tall -> crop top/bottom
        nh = int(w / target)
        top = (h - nh) // 2
        im = im.crop((0, top, w, top + nh))
    return im.resize(size, Image.LANCZOS)


def fit_long_edge(im, max_edge):
    w, h = im.size
    if max(w, h) <= max_edge:
        return im
    if w >= h:
        return im.resize((max_edge, round(h * max_edge / w)), Image.LANCZOS)
    return im.resize((round(w * max_edge / h), max_edge), Image.LANCZOS)


report = []


def note(path):
    report.append((path, os.path.getsize(path) / 1024))


# --- gallery + hero/about images -------------------------------------------
for name in GALLERY:
    src = Image.open(name).convert("RGB")

    large = fit_long_edge(src, LARGE_MAX)
    large.save(name, "JPEG", quality=82, optimize=True, progressive=True)
    note(name)
    stem = name.rsplit(".", 1)[0]
    large.save(f"{stem}.webp", "WEBP", quality=80, method=6)
    note(f"{stem}.webp")

    thumb = center_crop_resize(src, THUMB)
    thumb.save(f"{stem}-sm.jpg", "JPEG", quality=80, optimize=True, progressive=True)
    note(f"{stem}-sm.jpg")
    thumb.save(f"{stem}-sm.webp", "WEBP", quality=78, method=6)
    note(f"{stem}-sm.webp")

# --- instructor portrait ----------------------------------------------------
ins = Image.open("instructor.jpeg").convert("RGB")
ins = fit_long_edge(ins, 1200)
ins.save("instructor.jpeg", "JPEG", quality=82, optimize=True, progressive=True)
note("instructor.jpeg")
ins.save("instructor.webp", "WEBP", quality=80, method=6)
note("instructor.webp")

# --- logo + favicons --------------------------------------------------------
logo = Image.open("logo.png").convert("RGBA")
lw, lh = logo.size
# rendered at 32 CSS px; 96 covers a 3x screen and 320 never did anything
logo_small = logo.resize((96, round(lh * 96 / lw)), Image.LANCZOS)
logo_small.save("logo.png", "PNG", optimize=True)
note("logo.png")
logo_small.convert("RGB").save("logo.webp", "WEBP", quality=88, method=6)
note("logo.webp")

# square canvas for icons (logo is 1180x1333 -> pad to square, white ground)
side = max(logo.size)
square = Image.new("RGBA", (side, side), (255, 255, 255, 255))
square.paste(logo, ((side - logo.size[0]) // 2, (side - logo.size[1]) // 2), logo)
square = square.convert("RGB")

for px, out in ((180, "apple-touch-icon.png"), (32, "favicon-32.png"), (16, "favicon-16.png")):
    square.resize((px, px), Image.LANCZOS).save(out, "PNG", optimize=True)
    note(out)

square.resize((512, 512), Image.LANCZOS).save("icon-512.png", "PNG", optimize=True)
note("icon-512.png")
square.resize((192, 192), Image.LANCZOS).save("icon-192.png", "PNG", optimize=True)
note("icon-192.png")

# multi-resolution .ico for legacy crawlers/browsers
square.save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
note("favicon.ico")

total = sum(kb for _, kb in report)
for path, kb in report:
    print(f"{path:26s} {kb:8.1f} KB")
print(f"{'TOTAL':26s} {total:8.1f} KB")
