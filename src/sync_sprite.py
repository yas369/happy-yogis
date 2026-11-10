#!/usr/bin/env python3
"""Regenerate each page's inline icon sprite so it contains exactly the symbols
that page's <use> elements reference - no orphans, no dead weight."""
import os
import re

# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
_SITE = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The icons ship with the lucide-static dependency, beside this file. This
# pointed at the scratch directory the source used to live in, so a clone built
# every page with its <use> elements referencing symbols that were never
# inlined - every icon on the site silently blank.
ICONS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "node_modules", "lucide-static", "icons")


def _pages(root):
    """Every generated page, found on disk. This used to be a hand-kept list,
    and each new post meant editing it in three files; a post missing from one
    of them was silently skipped by the sprite sync, which is the check that
    keeps every icon on a page from rendering blank."""
    import glob
    out = sorted(os.path.relpath(p, root) for p in glob.glob(os.path.join(root, "*.html")))
    out += sorted(os.path.relpath(p, root) for p in glob.glob(os.path.join(root, "ta", "*.html")))
    return out


PAGES = _pages(_SITE)

SPRITE_RE = re.compile(
    r'\n<!-- Inline Lucide icon sprite.*?-->\n<svg xmlns="http://www\.w3\.org/2000/svg" '
    r'style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true" '
    r'focusable="false">\n.*?\n</svg>\n', re.S)


def symbol_for(name):
    raw = open(os.path.join(ICONS, f"{name}.svg")).read()
    body = raw[raw.index(">", raw.index("<svg")) + 1: raw.rindex("</svg>")]
    body = "".join(line.strip() for line in body.splitlines() if line.strip())
    return f'<symbol id="i-{name}" viewBox="0 0 24 24">{body}</symbol>'


for page in PAGES:
    path = f"{_SITE}/{page}"
    html = open(path).read()

    used = sorted({m.group(1) for m in re.finditer(r'<use href="#i-([a-z0-9-]+)"', html)})
    missing = [n for n in used if not os.path.exists(os.path.join(ICONS, f"{n}.svg"))]
    if missing:
        raise SystemExit(f"{page}: no such lucide icon(s): {missing}")

    sprite = (
        '\n<!-- Inline Lucide icon sprite (lucide-static v1.38.0, ISC). '
        'Replaces the former runtime unpkg.com/lucide script. -->\n'
        '<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;'
        'width:0;height:0;overflow:hidden" aria-hidden="true" focusable="false">\n'
        + "\n".join(symbol_for(n) for n in used) + '\n</svg>\n'
    )

    html, n = SPRITE_RE.subn(lambda _: sprite, html, count=1)
    if n == 0:
        # no sprite yet - insert one right after the opening <body> tag
        m = re.search(r"<body[^>]*>", html)
        if not m:
            raise SystemExit(f"{page}: no <body> tag")
        html = html[:m.end()] + sprite + html[m.end():]

    open(path, "w").write(html)

    have = {m.group(1) for m in re.finditer(r'<symbol id="i-([a-z0-9-]+)"', html)}
    assert have == set(used), f"{page}: sprite mismatch"
    print(f"{page}: sprite now holds exactly {len(used)} symbols -> {', '.join(used)}")
