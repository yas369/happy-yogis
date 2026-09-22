#!/usr/bin/env python3
"""Build the whole site, with Tailwind compiled ahead of time and inlined.

The site used to pull Tailwind's Play CDN, which is a render-blocking script
that ships a compiler to every visitor and rebuilds the stylesheet in their
browser on every page load. Lighthouse measured it at 1,490 ms of render
blocking and 38 KiB of unused JavaScript.

Compiling needs the markup, and the markup needs the compiled CSS, so this runs
two passes:

    1. generate the pages with no Tailwind inlined
    2. run the Tailwind CLI over those pages
    3. generate again, inlining the result

Compiling from the CSS-free pass matters: if Tailwind scanned markup that
already carried its own output, the extractor would read selectors like
.text-muted back out of the stylesheet as though they were class names, and
each build would drift from the last.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
SITE = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN = os.path.join(HERE, ".scan")           # pass-1 markup, CSS-free
OUT = os.path.join(HERE, "tw.out.css")


def generate(tw_css=None):
    env = dict(os.environ)
    env.pop("TW_CSS", None)
    if tw_css:
        env["TW_CSS"] = tw_css
    for script in ("pages.py", "blog.py", "legal.py", "ta_pages.py"):
        r = subprocess.run([sys.executable, script], cwd=HERE, env=env,
                           capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"{script} failed:\n{r.stdout}\n{r.stderr}")


def main():
    print("pass 1: generating markup without Tailwind")
    generate(None)

    # snapshot the CSS-free markup for the extractor to read
    shutil.rmtree(SCAN, ignore_errors=True)
    os.makedirs(SCAN)
    # The Tamil pages live in a subdirectory, and until they were copied in too
    # any utility used only there - gap-x-5 in the Tamil footer, for one - was
    # scanned out of the stylesheet and silently did nothing on the page.
    for base in (SITE, os.path.join(SITE, "ta")):
        if not os.path.isdir(base):
            continue
        pre = "" if base == SITE else "ta-"
        for f in os.listdir(base):
            if f.endswith(".html"):
                shutil.copy(os.path.join(base, f), os.path.join(SCAN, pre + f))

    print("compiling Tailwind from that markup")
    r = subprocess.run(
        ["npx", "tailwindcss", "-c", "tw.config.js", "-i", "tw.in.css",
         "-o", OUT, "--minify", "--content", f"{SCAN}/*.html"],
        cwd=HERE, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"tailwind failed:\n{r.stdout}\n{r.stderr}")
    size = os.path.getsize(OUT)

    print("pass 2: regenerating with the stylesheet inlined")
    generate(OUT)

    subprocess.run([sys.executable, "sync_sprite.py"], cwd=HERE,
                   capture_output=True, text=True)
    subprocess.run([sys.executable, "sitemap.py"], cwd=HERE,
                   capture_output=True, text=True)

    shutil.rmtree(SCAN, ignore_errors=True)
    print(f"done - {size:,} bytes of CSS inlined into every page")


if __name__ == "__main__":
    main()
