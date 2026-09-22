#!/usr/bin/env python3
"""Pre-flight checks for the Happy Yogis static site."""
import json
import os
import datetime
import re
import sys
from html.parser import HTMLParser

# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
ROOT = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html", "privacy-policy.html", "terms-of-service.html",
         "yoga-classes-perungalathur.html", "yoga-classes-tambaram.html",
         "blog.html", "what-happens-in-your-first-yoga-class.html", "yoga-for-weight-loss-in-chennai.html", "yoga-classes-for-men-perungalathur.html", "yoga-classes-for-children-perungalathur.html", "international-yoga-day-beach.html", "108-suryanamaskar-challenge.html",
         "hatha-yoga-in-chennai.html",
         "how-often-should-you-do-yoga.html", "yoga-or-gym-which-should-you-pick.html", "morning-or-evening-yoga-class.html", "yoga-for-back-pain-chennai.html",
         # Tamil mirrors, checked on the same terms as everything else
         "ta/index.html", "ta/yoga-classes-perungalathur.html",
         "ta/yoga-classes-tambaram.html",
         "ta/blog.html", "ta/how-often-should-you-do-yoga.html", "ta/yoga-or-gym-which-should-you-pick.html", "ta/morning-or-evening-yoga-class.html", "ta/yoga-for-back-pain-chennai.html"]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr", "path", "circle", "line",
        "rect", "polyline", "polygon", "ellipse", "use", "stop"}

errors, warnings = [], []


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            errors.append(f"  stray </{tag}> at line {self.getpos()[0]}")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    unclosed = [t for t, _ in self.stack[i + 1:]]
                    errors.append(
                        f"  </{tag}> at line {self.getpos()[0]} closes over unclosed {unclosed}")
                    del self.stack[i:]
                    break
            else:
                errors.append(f"  stray </{tag}> at line {self.getpos()[0]}")


for page in PAGES:
    path = os.path.join(ROOT, page)
    html = open(path).read()
    print(f"\n=== {page} ===")

    # 1. tag balance
    before = len(errors)
    p = Balance()
    p.feed(html)
    for tag, pos in p.stack:
        errors.append(f"  unclosed <{tag}> opened at line {pos[0]}")
    print(f"  tag balance: {'OK' if len(errors) == before else 'FAILED'}")

    # 2. exactly one <h1>, heading order sane
    h1 = re.findall(r"<h1[\s>]", html)
    if len(h1) != 1:
        errors.append(f"  {page}: expected exactly 1 <h1>, found {len(h1)}")
    levels = [int(m) for m in re.findall(r"<h([1-6])[\s>]", html)]
    prev = 0
    for lv in levels:
        if prev and lv > prev + 1:
            warnings.append(f"  {page}: heading jumps h{prev} -> h{lv}")
        prev = lv
    print(f"  headings: {len(h1)} h1, sequence {'OK' if not any(page in w for w in warnings) else 'see warnings'}")

    # 3. local asset references all resolve
    refs = set()
    refs |= set(re.findall(r'(?:src|href)="(?!https?:|mailto:|tel:|data:|#|/)([^"?#]+)"', html))
    # srcset / imagesrcset are candidate lists: "file 640w, file 1280w"
    for attr in ("srcset", "imagesrcset"):
        for group in re.findall(attr + r'="([^"]+)"', html):
            for cand in group.split(","):
                url = cand.strip().split()[0] if cand.strip() else ""
                if url and not url.startswith(("http:", "https:", "data:")):
                    refs.add(url.split("?")[0].split("#")[0])
    refs |= set(re.findall(r'(?:href|src)="/([^"?#]+)"', html))
    missing = [r for r in sorted(refs) if not os.path.exists(os.path.join(ROOT, r.lstrip("/")))]
    if missing:
        errors.append(f"  {page}: missing local files -> {missing}")
    print(f"  local refs: {len(refs)} referenced, {len(missing)} missing")

    # 4. every in-page anchor has a target
    ids = set(re.findall(r'id="([^"]+)"', html))
    anchors = {a for a in re.findall(r'href="#([^"]+)"', html)}
    dangling = sorted(anchors - ids)
    if dangling:
        errors.append(f"  {page}: anchors with no matching id -> {dangling}")
    print(f"  anchors: {len(anchors)} checked, {len(dangling)} dangling")

    # 5. duplicate ids
    all_ids = re.findall(r'id="([^"]+)"', html)
    dupes = {i for i in all_ids if all_ids.count(i) > 1}
    if dupes:
        errors.append(f"  {page}: duplicate ids -> {sorted(dupes)}")
    print(f"  ids: {len(all_ids)} total, {len(dupes)} duplicated")

    # 6. every <use href="#i-x"> has a matching <symbol id="i-x">
    symbols = set(re.findall(r'<symbol id="([^"]+)"', html))
    uses = set(re.findall(r'<use href="#([^"]+)"', html))
    orphan_uses = sorted(uses - symbols)
    unused_syms = sorted(symbols - uses)
    if orphan_uses:
        errors.append(f"  {page}: <use> with no <symbol> -> {orphan_uses}")
    if unused_syms:
        warnings.append(f"  {page}: unused sprite symbols -> {unused_syms}")
    print(f"  icons: {len(uses)} symbols referenced, {len(orphan_uses)} orphaned")

    # 7. every <img> has alt and explicit dimensions
    imgs = re.findall(r"<img\s[^>]*>", html)
    no_alt = [i for i in imgs if 'alt="' not in i]
    # The lightbox <img> is a fixed-position placeholder whose source and
    # aspect ratio are set from whichever photo was opened, so it has no
    # dimensions to declare and reserves no space in the flow to shift.
    no_dim = [i for i in imgs
              if not ("width=" in i and "height=" in i)
              and 'id="lightbox-img"' not in i]
    if no_alt:
        errors.append(f"  {page}: {len(no_alt)} <img> without alt")
    if no_dim:
        warnings.append(f"  {page}: {len(no_dim)} <img> without width/height")
    print(f"  images: {len(imgs)} total, {len(no_alt)} missing alt, {len(no_dim)} missing dimensions")

    # 8. JSON-LD parses
    for i, blob in enumerate(re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.S)):
        try:
            json.loads(blob)
        except json.JSONDecodeError as exc:
            errors.append(f"  {page}: JSON-LD block {i} invalid -> {exc}")
    print(f"  JSON-LD: {len(re.findall(r'application/ld.json', html))} block(s), parsed OK")

    # 9. head essentials
    for needle, label in [('rel="canonical"', "canonical"),
                          ('property="og:title"', "og:title"),
                          ('name="twitter:card"', "twitter:card"),
                          ('rel="apple-touch-icon"', "apple-touch-icon"),
                          ('name="description"', "meta description")]:
        if needle not in html:
            errors.append(f"  {page}: missing {label}")

    title = re.search(r"<title>(.*?)</title>", html, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)">', html, re.S)
    if title:
        n = len(title.group(1))
        print(f"  title: {n} chars {'OK' if n <= 60 else 'TOO LONG (>60)'} - {title.group(1)}")
        if n > 60:
            warnings.append(f"  {page}: title {n} chars (>60)")
    if desc:
        n = len(desc.group(1))
        print(f"  description: {n} chars {'OK' if n <= 155 else 'TOO LONG (>155)'}")
        if n > 155:
            warnings.append(f"  {page}: meta description {n} chars (>155)")

    # 10. leftovers from the audit
    if "<base target" in html:
        errors.append(f"  {page}: <base target> still present")
    if "unpkg.com/lucide" in html and "<script src" in html.split("unpkg.com/lucide")[0][-40:]:
        errors.append(f"  {page}: runtime lucide script still present")
    if "data-lucide" in html:
        errors.append(f"  {page}: unconverted data-lucide placeholder")

# ---- sitemap agrees with the pages, and every page names one domain ----
import xml.etree.ElementTree as ET

SNS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9",
       "i": "http://www.google.com/schemas/sitemap-image/1.1"}
sm_path = f"{ROOT}/sitemap.xml"
if not os.path.exists(sm_path):
    errors.append("sitemap.xml is missing")
else:
    try:
        sm = ET.parse(sm_path).getroot()
    except ET.ParseError as e:
        errors.append(f"sitemap.xml does not parse: {e}")
        sm = None
    if sm is not None:
        locs = [u.findtext("s:loc", "", SNS) for u in sm.findall("s:url", SNS)]
        canon = {}
        for page in PAGES:
            html = open(f"{ROOT}/{page}").read()
            m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
            canon[page] = m.group(1) if m else None
        for page, c in canon.items():
            if c and c not in locs:
                errors.append(f"{page}: canonical {c} is not in sitemap.xml")
        for loc in locs:
            if loc not in canon.values():
                errors.append(f"sitemap.xml: {loc} matches no page canonical")
        for img in sm.findall(".//i:loc", SNS):
            f = img.text.rsplit("/", 1)[-1]
            if not os.path.exists(f"{ROOT}/{f}"):
                errors.append(f"sitemap.xml: image {f} does not exist")
        # one domain across pages, sitemap and robots
        domains = {re.match(r"https?://[^/]+", c).group(0) for c in canon.values() if c}
        robots = open(f"{ROOT}/robots.txt").read()
        domains |= {re.match(r"https?://[^/]+", l).group(0) for l in locs}
        domains |= set(re.findall(r"Sitemap:\s*(https?://[^/]+)", robots))
        if len(domains) > 1:
            errors.append(f"more than one domain in use: {sorted(domains)}")
        else:
            print(f"\n=== sitemap.xml ===\n  {len(locs)} URLs, all canonical-matched")
            print(f"  {len(sm.findall('.//i:image', SNS))} image entries, all present")
            print(f"  one domain throughout: {domains.pop()}")

# A post dated after today is either a scheduling slip or a fabricated
# freshness signal, and a crawler that sees datePublished in the future reads
# it as the latter. Cheap to check, so check it every build.
_today = datetime.date.today().isoformat()
for _f in PAGES:
    _path = os.path.join(ROOT, _f)
    if not os.path.exists(_path):
        continue
    for _d in set(re.findall(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})', open(_path, encoding="utf-8").read())
                  ) | set(re.findall(r'<time datetime="(\d{4}-\d{2}-\d{2})"', open(_path, encoding="utf-8").read())):
        if _d > _today:
            errors.append(f"{_f}: dated {_d}, which is after today ({_today})")

print("\n" + "=" * 60)
if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(w)
if errors:
    print(f"\nERRORS ({len(errors)}):")
    for e in errors:
        print(e)
    sys.exit(1)
print("\nAll checks passed.")
