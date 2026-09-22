#!/usr/bin/env python3
"""Replace runtime Lucide <i data-lucide> placeholders with an inline SVG sprite.

Removes the external unpkg.com/lucide dependency (render-blocking JS + 133
runtime DOM insertions + icon FOUC) in favour of a per-page <symbol> sprite.
Icon geometry is taken verbatim from lucide-static (ISC licensed).
"""
import os
import re

# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
ROOT = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = ("/tmp/claude-0/-home-user-happy-yogis/a6357452-d0ea-57e6-a208-ae557941866f/"
         "scratchpad/node_modules/lucide-static/icons")
PAGES = ["index.html", "privacy-policy.html", "terms-of-service.html"]

TAG = re.compile(r'<i data-lucide="([a-z0-9-]+)" class="([^"]*)"></i>')


def symbol_for(name):
    with open(os.path.join(ICONS, f"{name}.svg")) as fh:
        raw = fh.read()
    # take everything between the opening <svg ...> and closing </svg>
    body = raw[raw.index(">", raw.index("<svg")) + 1: raw.rindex("</svg>")]
    body = "".join(line.strip() for line in body.splitlines() if line.strip())
    return f'<symbol id="i-{name}" viewBox="0 0 24 24">{body}</symbol>'


for page in PAGES:
    path = os.path.join(ROOT, page)
    with open(path) as fh:
        html = fh.read()

    used = sorted({m.group(1) for m in TAG.finditer(html)})
    if not used:
        print(f"{page}: no lucide placeholders found")
        continue

    def sub(m):
        name, cls = m.group(1), m.group(2)
        return (f'<svg class="lucide {cls}" aria-hidden="true" focusable="false">'
                f'<use href="#i-{name}"></use></svg>')

    html, count = TAG.subn(sub, html)

    symbols = "\n".join(symbol_for(n) for n in used)
    sprite = (
        '\n<!-- Inline Lucide icon sprite (lucide-static v1.38.0, ISC). '
        'Replaces the former runtime unpkg.com/lucide script. -->\n'
        '<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;'
        'width:0;height:0;overflow:hidden" aria-hidden="true" focusable="false">\n'
        f'{symbols}\n</svg>\n'
    )

    # insert immediately after the opening <body ...> tag
    bodym = re.search(r"<body[^>]*>", html)
    html = html[:bodym.end()] + sprite + html[bodym.end():]

    with open(path, "w") as fh:
        fh.write(html)
    print(f"{page}: {count} icons inlined, {len(used)} symbols")
