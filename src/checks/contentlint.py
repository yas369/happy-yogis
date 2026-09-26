import os
"""The mistakes a spell checker cannot see: template braces that escaped,
entities rendered literally, doubled words, doubled punctuation, stray
placeholders, and sentences that lost a space at a tag boundary."""
import re, html, glob, os, collections

# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
_SITE = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

tagblock = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)
stripper = re.compile(r"<[^>]+>")

def visible(path):
    s = open(path, encoding="utf-8").read()
    s = tagblock.sub(" ", s)
    s = stripper.sub("\n", s)
    return html.unescape(s), s          # unescaped, raw-stripped

CHECKS = []
def check(name):
    def d(fn): CHECKS.append((name, fn)); return fn
    return d

@check("unrendered template brace")
def _(vis, raw): return re.findall(r"\{[A-Za-z_][\w\.\[\]'\"]*\}", raw)

@check("double-escaped entity")
def _(vis, raw):
    # An entity in the raw source is correct HTML. Only one that survives
    # unescaping was written twice over (&amp;rsquo;) and shows to the reader.
    return re.findall(r"&(?:mdash|ndash|nbsp|amp|quot|ldquo|rdquo|rsquo|middot|hellip);", vis)

@check("doubled word")
def _(vis, raw):
    # Same reason: only within a single run of text, not across a tag.
    return [m.group(0) for m in re.finditer(r"\b(\w{3,}) \1\b", vis, re.I)]

@check("doubled punctuation")
def _(vis, raw): return re.findall(r"[,;:]{2,}|\.{4,}|!{2,}|\?{2,}", vis)

@check("space before punctuation")
def _(vis, raw):
    # Tags are replaced with newlines, so only a real space inside one run
    # of text counts - a newline here is a tag boundary, not a typo.
    return [m.group(0) for m in re.finditer(r"\w [,.;:!?](?:\s|$)", vis)][:5]

@check("placeholder text")
def _(vis, raw): return re.findall(r"\b(?:lorem|ipsum|TODO|FIXME|TBD|XXX|Placeholder)\b", vis, re.I)

@check("None/undefined leaked")
def _(vis, raw): return re.findall(r"\b(?:None|undefined|NaN|\[object Object\])\b", vis)

@check("double space in sentence")
def _(vis, raw):
    return [m.group(0).strip() for m in re.finditer(r"\w  +\w", vis)][:4]

hits = collections.defaultdict(list)
files = sorted(glob.glob(f"{_SITE}/*.html") + glob.glob(f"{_SITE}/ta/*.html"))
for f in files:
    vis, raw = visible(f)
    for name, fn in CHECKS:
        r = fn(vis, raw)
        if r: hits[name].append((os.path.basename(f), r[:3], len(r)))

print(f"scanned {len(files)} pages (English + Tamil)\n")
if not hits: print("clean: none of the checks fired")
for name, rows in hits.items():
    total = sum(n for _,_,n in rows)
    print(f"=== {name}: {total} across {len(rows)} page(s)")
    for fn, ex, n in rows[:6]:
        print(f"    {fn:42s} {ex}")
