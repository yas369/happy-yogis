#!/usr/bin/env python3
"""Generate sitemap.xml from the pages themselves.

Two rules this enforces that a hand-written sitemap kept breaking:

  * every <loc> is read from that page's own <link rel="canonical">, so the
    sitemap can never disagree with the page about its own URL;
  * a page's <lastmod> only moves when the page actually changed. Restamping
    every URL on every build teaches Google to ignore the field entirely.

Image entries list the full-size photographs on each page (not the responsive
derivatives and not the social card), titled with the alt text they already
carry, which is the description written from the real photo - so a Tamil page
lists its images with their Tamil descriptions.
"""
import html as _html
import os
import re
import subprocess
import sys
from datetime import date
from urllib.parse import urljoin

# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
OUT = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date.today().isoformat()

# Ordered as a visitor would meet them: home, the location pages that carry the
# local search intent, the journal, then the legal pages.
PAGES = [
    # Tamil mirrors of the three pages a search visitor lands on. Same priority
    # as their English counterparts - neither language is the lesser one - and
    # hreflang on the pages themselves tells Google they are a pair.
    ("ta/index.html",                              "1.0", "monthly"),
    ("ta/yoga-classes-perungalathur.html",         "0.9", "monthly"),
    ("ta/yoga-classes-tambaram.html",              "0.9", "monthly"),
    ("ta/blog.html",                                 "0.7", "yearly"),
    ("ta/how-often-should-you-do-yoga.html",         "0.7", "yearly"),
    ("ta/yoga-or-gym-which-should-you-pick.html",    "0.7", "yearly"),
    ("ta/morning-or-evening-yoga-class.html",        "0.7", "yearly"),
    ("ta/yoga-for-back-pain-chennai.html",           "0.7", "yearly"),
    ("index.html",                                 "1.0", "monthly"),
    ("yoga-classes-perungalathur.html",            "0.9", "monthly"),
    ("yoga-classes-tambaram.html",                 "0.9", "monthly"),
    ("blog.html",                                  "0.6", "monthly"),
    ("hatha-yoga-in-chennai.html",                 "0.7", "yearly"),
    ("how-often-should-you-do-yoga.html",            "0.7", "yearly"),
    ("yoga-or-gym-which-should-you-pick.html",       "0.7", "yearly"),
    ("morning-or-evening-yoga-class.html",           "0.7", "yearly"),
    ("yoga-for-back-pain-chennai.html",              "0.7", "yearly"),
    ("yoga-for-weight-loss-in-chennai.html",       "0.7", "yearly"),
    ("108-suryanamaskar-challenge.html",            "0.7", "yearly"),
    ("international-yoga-day-beach.html",           "0.6", "yearly"),
    ("yoga-classes-for-children-perungalathur.html","0.7", "yearly"),
    ("yoga-classes-for-men-perungalathur.html",     "0.7", "yearly"),
    ("what-happens-in-your-first-yoga-class.html", "0.6", "yearly"),
    ("privacy-policy.html",                        "0.2", "yearly"),
    ("terms-of-service.html",                      "0.2", "yearly"),
]

CANON = re.compile(r'<link rel="canonical" href="([^"]+)"')
ROBOTS = re.compile(r'<meta name="robots" content="([^"]+)"')

# Every photograph on a page, with the description it already carries: an
# <img> with its alt, or a gallery button with its caption (the button holds
# the full-size file; its <img> is only the thumbnail).
#
# This used to be one regex anchored on the filename - `(ima\d+|instructor)`
# - and it had gone quietly wrong twice. A leading slash stopped it matching,
# so all eight Tamil pages listed no images at all; and the teacher portrait
# was renamed to instructor-portrait.jpeg, so the `instructor` branch had
# matched nothing for a long time. Matching the attribute rather than the
# filename means a new photograph is picked up because it is on the page, not
# because its name was added here.
IMG = re.compile(r'<img\s[^>]*?src="([^"]+\.jpe?g)"[^>]*?\salt="([^"]*)"')
FULL = re.compile(r'data-full="([^"]+\.jpe?g)"[^>]*?\sdata-caption="([^"]*)"')

# -xs/-sm/-md are the responsive derivatives. The sitemap lists the full-size
# file, so a thumbnail that reaches here is a duplicate of one, not a photo of
# its own.
DERIVATIVE = re.compile(r"-(?:xs|sm|md)$")


def photos(html, loc):
    """(absolute url, title) for each distinct photograph on one page.

    `loc` is the page's own canonical, so a src is resolved the way a browser
    would resolve it - which is the whole point: the Tamil pages address their
    images from the site root (/ima6.jpeg) while they themselves live a
    directory down, and joining those by hand put them in /ta/."""
    out, seen = [], set()
    for src, title in IMG.findall(html) + FULL.findall(html):
        url = urljoin(loc, src)
        stem = url.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        if DERIVATIVE.search(stem) or url in seen:
            continue
        seen.add(url)
        # The alt came out of the markup, so it is already escaped once.
        out.append((url, _html.unescape(title)))
    return out


def previous_lastmods():
    path = os.path.join(OUT, "sitemap.xml")
    if not os.path.exists(path):
        return {}
    xml = open(path).read()
    return dict(re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", xml))


def changed(page):
    """True if the page differs from the last commit, or is not committed yet."""
    r = subprocess.run(["git", "-C", OUT, "status", "--porcelain", "--", page],
                       capture_output=True, text=True)
    return bool(r.stdout.strip())


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def build():
    old = previous_lastmods()
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']

    for page, priority, freq in PAGES:
        path = os.path.join(OUT, page)
        if not os.path.exists(path):
            raise SystemExit(f"sitemap: {page} does not exist")
        html = open(path).read()

        m = CANON.search(html)
        if not m:
            raise SystemExit(f"sitemap: {page} has no canonical link")
        loc = m.group(1)

        # Never advertise a URL the page itself tells Google not to index.
        rb = ROBOTS.search(html)
        if rb and "noindex" in rb.group(1):
            print(f"  skipping {page}: it is noindex")
            continue

        lastmod = TODAY if (changed(page) or loc not in old) else old[loc]

        out += ["", "  <url>",
                f"    <loc>{esc(loc)}</loc>",
                f"    <lastmod>{lastmod}</lastmod>",
                f"    <changefreq>{freq}</changefreq>",
                f"    <priority>{priority}</priority>"]

        for url, title in photos(html, loc):
            out += ["    <image:image>",
                    f"      <image:loc>{esc(url)}</image:loc>",
                    f"      <image:title>{esc(title)}</image:title>",
                    "    </image:image>"]
        out.append("  </url>")

    out += ["", "</urlset>", ""]
    return "\n".join(out)


if __name__ == "__main__":
    xml = build()
    open(os.path.join(OUT, "sitemap.xml"), "w").write(xml)
    import xml.etree.ElementTree as ET
    ET.fromstring(xml)
    print(f"sitemap.xml: {xml.count('<loc>')} URLs, "
          f"{xml.count('<image:loc>')} images")
