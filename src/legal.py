#!/usr/bin/env python3
"""Re-wrap the two legal pages on the new shell, keeping their legal text."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import head, nav, footer, SCRIPT, BASE
import content as C

# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
OUT = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = {
    "privacy-policy.html": {
        "title": "Privacy Policy | Happy Yogis Yoga Centre",
        "desc": ("How Happy Yogis Yoga Centre in New Perungalathur, Chennai collects, "
                 "uses and protects student and website visitor information."),
        "h1": "Privacy Policy",
        "crumb": "Privacy Policy",
    },
    "terms-of-service.html": {
        "title": "Terms of Service | Happy Yogis Yoga Centre",
        "desc": ("Terms and conditions for yoga classes, bookings and memberships at "
                 "Happy Yogis Yoga Centre, New Perungalathur, Chennai."),
        "h1": "Terms of Service",
        "crumb": "Terms of Service",
    },
}

# section ids that existed on the old homepage and no longer do
FRAGMENT_FIXES = {
    "specializations": "classes",
    "testimonials": "reviews",
    "students": "reviews",
    "about": "about",
    "trainer": "teacher",
    "teacher": "teacher",
    "timings": "schedule",
    "schedule": "schedule",
    "gallery": "studio",
    "studio": "studio",
    "contact": "visit",
    "visit": "visit",
    "areas": "areas",
    "health": "health",
    "classes": "classes",
    "faq": "faq",
}


def deweight(html):
    """Instrument Serif ships a single weight. Any font-bold / font-semibold on
    a serif heading only asks the browser to smear a fake bold, so strip weight
    classes from every element that carries the display face or a d-scale size."""
    def fix(m):
        cls = m.group(1)
        if "display" in cls.split() or re.search(r"text-d[1-4]\b", cls):
            keep = [t for t in cls.split()
                    if t not in ("font-bold", "font-semibold", "font-medium")]
            return 'class="' + " ".join(keep) + '"'
        return m.group(0)
    return re.sub(r'class="([^"]*)"', fix, html)


def restyle(body):
    """Map the legal prose onto the new design system.

    The old pages were written against a Tailwind theme that no longer exists
    (deep-blue / sky-blue / wellness-green / sunrise-gold / warm-gray). Those
    class names now generate no CSS at all, so the text would render with no
    colour. Everything is remapped to the current tokens.
    """
    for a, b in [
        # old theme tokens -> current ones
        ("text-deep-blue", "text-ink"),
        ("bg-deep-blue", "bg-ink"),
        ("border-deep-blue", "border-ink"),
        ("text-sky-blue", "text-blue"),
        ("bg-sky-blue/10", "bg-blue/10"),
        ("bg-sky-blue", "bg-blue"),
        ("border-sky-blue", "border-blue"),
        ("bg-wellness-green", "bg-blue"),
        ("text-wellness-green", "text-blue"),
        ("bg-sunrise-gold/10", "bg-blue/10"),
        ("bg-sunrise-gold", "bg-blue"),
        ("text-sunrise-gold", "text-blue"),
        ("border-warm-gray", "border-line"),
        ("bg-warm-gray", "bg-sand"),
        ("text-dark-charcoal", "text-ink"),
        ("text-medium-gray", "text-muted"),
        ("bg-soft-white", "bg-sand"),
        ("from-deep-blue to-sky-blue", "bg-ink"),
        # typography
        ("font-heading", "display"),
    ]:
        body = body.replace(a, b)

    # repoint stale homepage fragments
    def frag(m):
        return f'href="index.html#{FRAGMENT_FIXES.get(m.group(1), "")}"'.replace("#\"", "\"")
    body = re.sub(r'href="index\.html#([a-z-]+)"', frag, body)

    # decorative blobs / leftover chrome
    body = re.sub(r'\s*<div class="absolute[^"]*(?:blur-3xl|rounded-full bg-white)[^"]*"[^>]*></div>', "", body)
    return body


for slug, cfg in PAGES.items():
    path = os.path.join(OUT, slug)
    html = open(path).read()
    # idempotent: prefer the already-rebuilt wrapper, fall back to the original
    m = re.search(r'<div class="legal mt-8">\n(.*?)\n        </div>\n    </div>', html, re.S)
    if not m:
        m = re.search(r'<main id="main-content">(.*?)</main>', html, re.S)
    if not m:
        raise SystemExit(f"{slug}: could not find the legal prose block")
    inner = m.group(1)

    # keep only the prose card section, drop the old coloured hero band
    inner = deweight(restyle(inner))

    # The old markup made every bulleted line a flex row, which turned the bold
    # lead-in ("Personal Information:") into its own column with the sentence
    # jammed against it. Wrap the text so the row is bullet + one block.
    inner = re.sub(
        r'(<li class="flex items-start"><span class="w-2 h-2[^"]*"></span>)(?!<span class="flex-1")(.*?)(</li>)',
        r'\1<span class="flex-1">\2</span>\3', inner, flags=re.S)

    if slug == "privacy-policy.html":
        marker = "Usage Data:</span> Information about how you interact with our website"
        assert marker in inner, "privacy policy: usage-data clause not found"
        extra = ("""
                        <div class="mt-6 border border-line rounded p-5 bg-sand">
                            <p class="text-[15px] font-medium text-ink">The enquiry form on our website</p>
                            <p class="mt-2 text-muted leading-relaxed text-[15px]">
                                Our enquiry form does not send anything to a server and we do
                                not store it on this website. When you submit it, the details
                                you typed &mdash; including anything you write in the
                                &ldquo;anything the teacher should know&rdquo; box &mdash; are
                                placed into a WhatsApp message on your own device. Nothing
                                reaches us until you press send in WhatsApp, and the message is
                                then handled by WhatsApp under their own privacy terms.
                            </p>
                            <p class="mt-3 text-muted leading-relaxed text-[15px]">
                                The health box is optional. Share only what you want your
                                teacher to know in order to keep your practice safe. We use it
                                for that purpose alone, we do not share it with anyone outside
                                the centre, and you can ask us to delete it at any time by
                                contacting us on the number below.
                            </p>
                        </div>""")
        # An earlier version of this script appended the clause on every run, so
        # the committed page carries more than one copy. Keep exactly the first.
        if inner.count(extra) > 1:
            before, _, after = inner.partition(extra)
            inner = before + extra + after.replace(extra, "")

        # Idempotent: on a re-run the clause is already in the prose we just
        # recovered, and appending it again silently duplicates it.
        if "The enquiry form on our website" not in inner:
            idx = inner.index("</ul>", inner.index(marker))
            inner = inner[:idx + len("</ul>")] + extra + inner[idx + len("</ul>"):]

    # strip the old gradient hero <section> (we render our own header below)
    inner = re.sub(r'^\s*<section class="pt-32 pb-12[^>]*>.*?</section>', "", inner,
                   count=1, flags=re.S)

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": f"{BASE}/{slug}#webpage",
             "url": f"{BASE}/{slug}", "name": cfg["title"], "description": cfg["desc"],
             "inLanguage": "en-IN", "isPartOf": {"@id": f"{BASE}/#website"},
             "about": {"@id": f"{BASE}/#business"}},
            {"@type": "BreadcrumbList", "@id": f"{BASE}/{slug}#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                 {"@type": "ListItem", "position": 2, "name": cfg["crumb"],
                  "item": f"{BASE}/{slug}"}]},
        ],
    }

    h = head(title=cfg["title"], desc=cfg["desc"], path=slug, schema=schema)

    body = f"""<body class="font-body bg-soft-white text-ink">
{nav()}
    <main id="main" class="pt-[4.5rem]">

    <nav aria-label="Breadcrumb" class="max-w-3xl mx-auto px-5 sm:px-8 pt-8">
        <ol class="flex flex-wrap items-center gap-2 text-sm text-muted">
            <li><a href="/" class="inline-block py-1 hover:text-ink">Home</a></li>
            <li aria-hidden="true">/</li>
            <li aria-current="page" class="text-ink">{cfg["crumb"]}</li>
        </ol>
    </nav>

    <div class="max-w-3xl mx-auto px-5 sm:px-8 py-10 lg:py-14">
        <h1 class="text-d1 text-ink">{cfg["h1"]}</h1>
        <div class="legal mt-8">
{inner}
        </div>
    </div>

    </main>

{footer()}
{SCRIPT}"""

    open(path, "w").write(h + body)
    print(f"{slug}: rebuilt on the new shell ({len(inner)} chars of legal text kept)")
