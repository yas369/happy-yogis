import os
"""Spell-check the visible English text of every page.

Reads the rendered HTML, strips script/style, and checks word by word.
Proper nouns and yoga vocabulary live in ALLOW so the real misspellings
are not buried under three hundred false positives.
"""
import re, html, glob, os, collections
from spellchecker import SpellChecker

# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
_SITE = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ALLOW = set("""
perungalathur tambaram chennai karthika yogis yogi upadesha ssm nagar tamil
nadu whatsapp asana asanas pranayama pranayamas namaskar namaskars surya
hatha iyengar sivananda satyananda vinyasa savasana bhujangasana yogic
sukhasana padmasana vajrasana trikonasana tadasana vrikshasana
adho mukha svanasana marjaryasana bitilasana setu bandha sarvangasana
balasana paschimottanasana ardha matsyendrasana
pcod thyroid hormonal perumbakkam medavakkam velachery adyar alwarpet
nungambakkam ambattur porur thoraipakkam anna omr gst
mam sir ji namaste pranayam kriya mudra bandha chakra
prenatal postnatal ayurveda ayurvedic wellbeing
online offline whatsapp google maps
nhs nih ncbi who cdc
sitemap html css js webp jpeg png svg utm
covid
""".split())

sp = SpellChecker()
tag = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)
strip = re.compile(r"<[^>]+>")
word = re.compile(r"[A-Za-z][A-Za-z'’\-]*")

def text_of(path):
    s = open(path, encoding="utf-8").read()
    s = tag.sub(" ", s)
    s = strip.sub(" ", s)
    return html.unescape(s)

found = collections.defaultdict(set)
files = sorted(glob.glob(f"{_SITE}/*.html"))
for f in files:
    txt = text_of(f)
    words = set()
    for w in word.findall(txt):
        lw = w.lower().strip("'’-")
        if not lw or lw in ALLOW or len(lw) < 3:
            continue
        if any(c.isupper() for c in w[1:]):     # acronyms / camel
            continue
        words.add(lw)
    for bad in sp.unknown(words):
        found[bad].add(os.path.basename(f))

print(f"checked {len(files)} English pages\n")
if not found:
    print("no unrecognised words")
for w in sorted(found):
    pages = sorted(found[w])
    where = pages[0] if len(pages) == 1 else f"{len(pages)} pages"
    print(f"  {w:22s} {where}   suggestion: {sp.correction(w)}")
