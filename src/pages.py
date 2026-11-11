#!/usr/bin/env python3
"""Assemble index.html, the two location pages, and the journal."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import (head, nav, footer, SCRIPT, icon, wa, BASE, PHONE_HREF,
                   PHONE_TEXT, MAPS, JOURNAL)
import content as C
from blog import newest_first

# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
OUT = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRIAL_MSG = "Hello Happy Yogis! I would like to book a 2-day trial."


# ------------------------------------------------------------------ fragments

def batch_list():
    """The timetable. A row per batch: the time set large and tabular because
    that is what people scan for, a pill saying who it suits, the length, and
    a note that opens on click. The page script marks the next one today with
    .slot--next, so the row a visitor wants is the row that is lit."""
    rows = []
    for i, (t24, label, length, who, note) in enumerate(C.BATCHES):
        plain = label.replace("&ndash;", "-")
        pill = "pill--blue" if who == "Ladies only" else "pill--quiet"
        rows.append(f"""                    <li>
                        <button type="button" class="batch slot group w-full text-left" data-start="{t24}" data-label="{plain}"
                                aria-expanded="false" aria-controls="batch-d{i}">
                            <span class="slot__t">{label}</span>
                            <span class="pill {pill}">{who}</span>
                            <span class="slot__m">{length}</span>
                        </button>
                        <div id="batch-d{i}" class="batch-detail">
                            <p class="px-[1.1rem] pb-4 text-[14px] leading-relaxed text-muted max-w-md">{note}</p>
                        </div>
                    </li>""")
    return "\n".join(rows)


def classes_section():
    """What we teach, as a grid of tiles rather than hairline rows. The rows
    read exactly like the timetable and the journal index above and below
    them; a tile with an icon reads as one of a set of parallel things, which
    is what these are. The filter chips sit directly above the grid they
    filter - they used to float opposite the intro paragraph, nowhere near
    the list they act on."""
    groups = [g for g, _ in C.CLASS_GROUPS]
    def chip(g, label, on):
        return (f'                    <button type="button" class="filter px-3.5 py-2 text-[13.5px] '
                f'border border-line rounded-full text-ink transition-colors" '
                f'data-group="{g}" aria-pressed="{"true" if on else "false"}">{label}</button>')
    filters = [chip("all", "Everything", True)]
    filters += [chip(g, g, False) for g in groups]

    # One icon per group, so a tile says which family it belongs to before
    # the heading is read.
    ICON = {groups[0] if groups else "": "sprout"}
    for g in groups:
        ICON[g] = {"Start here": "sprout", "Build strength": "flame",
                   "Breath and mind": "wind", "Beyond the batches": "sun"}.get(g, "circle")

    items = []
    for g, entries in C.CLASS_GROUPS:
        for name, desc in entries:
            items.append(f"""                <li class="class-item" data-group="{g}">
                    <div class="tile">
                        <span class="tile__i">{icon(ICON[g], 'w-[1.15rem] h-[1.15rem]')}</span>
                        <h3 class="display text-d3 text-ink">{name}</h3>
                        <p class="mt-2 text-[14.5px] leading-relaxed text-muted">{desc}</p>
                    </div>
                </li>""")
    return "\n".join(filters), "\n".join(items)


def health_list():
    """The six conditions as a bento. Spans alternate 7/5, 5/7, 6/6 so the grid
    reads as composed rather than as a table; the content is untouched."""
    spans = ["lg:col-span-7", "lg:col-span-5", "lg:col-span-5",
             "lg:col-span-7", "lg:col-span-6", "lg:col-span-6"]
    out = []
    for i, (n, d) in enumerate(C.HEALTH):
        span = spans[i] if i < len(spans) else "lg:col-span-6"
        out.append(f"""                    <div class="{span} bg-paper p-6 sm:p-7 reveal" style="--d:{i * 60}ms">
                        <dt class="display text-d3 text-ink">{n}</dt>
                        <dd class="mt-2 text-[14.5px] leading-relaxed text-muted">{d}</dd>
                    </div>""")
    return "\n".join(out)


def faq_list(level=3):
    """`level` because the same accordion is an h3 under a section heading on
    a long page, but sits directly under the h1 on faq.html, where an h3
    would skip a rank."""
    return "\\n".join(f"""                <div class="faq-item border-b border-line">
                    <h{level}>
                        <button type="button" class="faq-q w-full flex items-start justify-between gap-6 py-5 text-left">
                            <span class="text-[16px] font-medium text-ink">{q}</span>
                            <span class="shrink-0 mt-0.5 text-muted">{icon('plus', 'w-5 h-5')}</span>
                        </button>
                    </h{level}>
                    <div class="faq-a pb-5 -mt-1 text-[15px] leading-relaxed text-muted max-w-2xl">{a}</div>
                </div>""" for q, a in C.FAQS)


def gallery(limit=None):
    from PIL import Image
    tiles = []
    # The home page showed all 26, which alone was 1,932px - a sixth of the
    # whole page. Twelve still reads as "plenty of real photographs", and the
    # rest keep their sitemap entries through the blog, area and event pages
    # that also carry them.
    for i, k in enumerate(C.GALLERY if limit is None else C.GALLERY[:limit]):
        w, h = Image.open(os.path.join(OUT, f"{k}-sm.jpg")).size
        tiles.append(f"""                <button type="button" class="gallery-item group block w-full mb-4 break-inside-avoid overflow-hidden rounded reveal" style="--d:{i * 45}ms"
                        data-full="{ASSET_PREFIX}{k}.jpeg" data-full-webp="{ASSET_PREFIX}{k}.webp" data-caption="{alt_text(k)}">
                    <picture>
                        <source srcset="{ASSET_PREFIX}{k}-sm.webp" type="image/webp">
                        <img src="{ASSET_PREFIX}{k}-sm.jpg" width="{w}" height="{h}" alt="{alt_text(k)}"
                             class="block w-full h-auto transition-transform duration-500 group-hover:scale-[1.03]"
                             loading="lazy" decoding="async">
                    </picture>
                </button>""")
    return "\n".join(tiles)


def _pills(items):
    return "\n".join(
        f'''                    <li><a href="{href}" class="inline-flex items-center gap-1.5 px-3.5 py-2 text-[13.5px] font-medium text-blue border border-line rounded-full bg-paper hover:border-blue transition-colors">{label} {icon('arrow-right', 'w-3.5 h-3.5')}</a></li>'''
        for label, href in items)


def guide_pills():
    return _pills([
        ("Yoga for men", "yoga-classes-for-men-perungalathur.html"),
        ("Yoga for children", "yoga-classes-for-children-perungalathur.html"),
        ("Why children benefit", "why-yoga-is-good-for-children.html"),
        ("Yoga for good health", "yoga-for-good-health.html"),
        ("Mind relaxation", "yoga-for-mind-relaxation.html"),
        ("Back pain", "yoga-for-back-pain-chennai.html"),
        ("Weight loss", "yoga-for-weight-loss-in-chennai.html"),
        ("Your first class", "what-happens-in-your-first-yoga-class.html"),
        ("Yoga classes near me", "yoga-classes-near-me-questions-to-ask.html"),
        ("Yoga for women", "yoga-classes-near-me-for-women-chennai.html"),
        ("Choosing an instructor", "how-to-choose-a-yoga-instructor.html"),
        ("Online yoga classes", "online-yoga-classes-near-me-how-to-choose.html"),
    ])


def story_pills():
    return _pills([
        ("The 108 Suryanamaskar challenge", "108-suryanamaskar-challenge.html"),
        ("International Yoga Day on the beach", "international-yoga-day-beach.html"),
        ("Navaratri at Park 63", "navaratri-yoga-demonstration-park-63.html"),
        ("How Park 63 opened", "new-yoga-centre-park-63-perungalathur.html"),
    ])


def centre_cards():
    """Both centres as cards, for directly under the hero.

    "Where are you?" is the first thing a local business is asked, and the
    answer sat in the Visit panel nine sections down. Each card is the whole
    answer: address, teacher, hours, phone and a directions link to that
    centre's own pin. The second centre had no map link at all until its
    Google listing existed."""
    out = []
    for i, c in enumerate(C.CENTRES):
        maps = (f"""
                        <a href="{c['maps']}" target="_blank" rel="noopener"
                           class="mt-3 py-1 inline-flex items-center gap-1.5 text-[13.5px] font-medium text-blue hover:underline">
                            Get directions {icon('arrow-up-right', 'w-3.5 h-3.5')}
                        </a>""" if c["maps"] else "")
        out.append(f"""                <li>
                    <div class="card h-full p-5 sm:p-6">
                        <div class="flex flex-wrap items-start justify-between gap-x-3 gap-y-1.5">
                            <h2 class="display text-d3 text-ink">{c['name']}</h2>
                            <span class="pill {'pill--blue' if i == 0 else 'pill--quiet'} shrink-0">{'All four batches' if i == 0 else '5:30 am'}</span>
                        </div>
                        <address class="mt-2 not-italic text-[14.5px] leading-relaxed text-muted">{c['street']}, Chennai {c['postal']}</address>
                        <p class="mt-2 text-[13.5px] text-muted">Taught by {c['teacher']}</p>
                        <a href="{c['phone_href']}" class="mt-1 inline-block py-1 text-[14.5px] font-medium text-ink hover:text-blue transition-colors">{c['phone_text']}</a>{maps}
                    </div>
                </li>""")
    return "\n".join(out)


def review_cards(limit=None, *, prefix=""):
    """Reviews as plain cards.

    The home page carried all twelve in an auto-advancing carousel - 936 of
    its 2,285 words, and a thing moving on its own next to a timetable people
    are trying to read. Three cards and a link to the rest say the same thing.
    Still no AggregateRating or Review schema, for the reason reviews_section
    gives: feeding a centre's own Google reviews back to Google as markup is
    what its guidelines prohibit. These stay attributed quotes."""
    if not C.REVIEWS:
        return f"""                <li class="card p-6 sm:p-7">
                    <p class="text-[15px] leading-relaxed text-muted">
                        We are collecting reviews from our students on Google. Once they
                        are up, they will appear here &mdash; in their words, not ours.
                    </p>
                </li>"""
    picked = C.REVIEWS if limit is None else C.REVIEWS[:limit]
    return "\n".join(f"""                <li class="reveal" style="--d:{min(i, 3) * 70}ms">
                    <figure class="card h-full flex flex-col p-6 sm:p-7">
                        <span class="pill pill--amber self-start">{icon('star', 'w-3.5 h-3.5')}Google review</span>
                        <blockquote class="mt-4 display text-[18px] leading-[1.55] text-ink">&ldquo;{r['text']}&rdquo;</blockquote>
                        <figcaption class="mt-auto pt-5 text-[13px] text-ink/70">
                            {r['name']} <span aria-hidden="true">&middot;</span> <span class="text-muted">{r['when']}</span>
                        </figcaption>
                    </figure>
                </li>""" for i, r in enumerate(picked))


def reviews_section():
    """Real Google reviews in an auto-advancing carousel, or an honest empty state.

    No AggregateRating / Review schema is emitted. These reviews live on the
    centre's Google profile; marking them up here and feeding them back to
    Google is self-serving review markup, which its guidelines prohibit and
    which risks a manual action. They are presented as attributed quotes.

    The carousel is the site's one piece of continuous non-user-triggered
    motion, so it carries the controls that make that defensible: it pauses on
    hover and on keyboard focus, stops for good the moment a visitor takes
    control, has a real pause button, and does not auto-advance at all under
    prefers-reduced-motion. Without JavaScript the track is still a plain
    horizontally scrollable row of quotes - nothing is hidden behind the script.
    """
    if not C.REVIEWS:
        return f"""            <div class="border border-line rounded lift p-8 sm:p-10 max-w-2xl">
                <p class="text-[15px] leading-relaxed text-muted">
                    We are collecting reviews from our students on Google. Once they are
                    up, they will appear here &mdash; in their words, not ours.
                </p>
                <a href="{C.REVIEWS_URL}" target="_blank" rel="noopener"
                   class="mt-5 inline-flex items-center gap-1.5 text-[14px] font-medium text-blue hover:underline">
                    Find us on Google Maps {icon('arrow-up-right', 'w-4 h-4')}
                </a>
            </div>"""

    n = len(C.REVIEWS)
    slides = "\n".join(f"""                    <div class="rev-slide pr-4 flex" role="group" aria-roledescription="review" aria-label="Review {i} of {n}">
                        <figure class="flex-1 flex flex-col border border-line rounded lift p-6 sm:p-7 bg-paper">
                            <blockquote class="clamp-2 display text-[19px] leading-[1.55] text-ink">&ldquo;{r['text']}&rdquo;</blockquote>
                            <a href="{C.REVIEWS_URL}" target="_blank" rel="noopener"
                               class="mt-3 py-1 inline-flex items-center text-[13px] font-medium text-blue hover:underline">
                                See our reviews on Google {icon('arrow-up-right', 'w-3.5 h-3.5 inline-block align-[-1px] ml-1')}
                            </a>
                            <figcaption class="mt-auto pt-5 border-t border-line text-[13px] text-ink/70">
                                {r['name']} <span aria-hidden="true">&middot;</span> <span class="text-muted">{r['when']}</span>
                            </figcaption>
                        </figure>
                    </div>""" for i, r in enumerate(C.REVIEWS, 1))

    return f"""            <p class="text-[15px] leading-relaxed text-ink/75 max-w-2xl">
                {C.REVIEW_COUNT_CLAIM}. A selection, quoted as written.
                <a href="{C.REVIEWS_URL}" target="_blank" rel="noopener"
                   class="font-medium text-blue hover:underline">Read them all on Google {icon('arrow-up-right', 'w-4 h-4 inline-block align-[-2px]')}</a>
            </p>
            <div class="rev mt-8" data-rev>
                <div class="rev-track" role="region" aria-label="Student reviews" aria-live="off" tabindex="0">
{slides}
                </div>
                <div class="rev-controls mt-6 items-center gap-2">
                    <button type="button" class="rev-btn" data-rev-prev aria-label="Previous reviews">
                        {icon('chevron-left', 'w-4 h-4')}
                    </button>
                    <button type="button" class="rev-btn" data-rev-next aria-label="Next reviews">
                        {icon('chevron-right', 'w-4 h-4')}
                    </button>
                    <button type="button" class="rev-btn" data-rev-toggle aria-label="Pause the reviews">
                        <span data-rev-pause>{icon('pause', 'w-4 h-4')}</span>
                        <span data-rev-play hidden>{icon('play', 'w-4 h-4')}</span>
                    </button>
                    <div class="rev-dots flex items-center ml-1" data-rev-dots></div>
                </div>
            </div>"""


ASSET_PREFIX = ""   # "/" for pages served below the root

# Photo captions, which are also the alt text and the lightbox captions.
# ta_pages swaps this for the Tamil set the same way it swaps ASSET_PREFIX,
# and falls back per key, so a photograph with no Tamil caption yet keeps its
# English one rather than losing its description altogether.
CAPTIONS = {}


def alt_text(key):
    """Not named caption(): photo() already takes a `caption` argument, and a
    module function of that name resolves to the parameter inside it - which
    is None by default, so every call site silently became None()."""
    return CAPTIONS.get(key) or C.PHOTOS[key]

# The hero photograph's rendered width: the content rail (max-w-6xl, 1152px)
# once the viewport is wide enough, the viewport less its gutters below that.
# Named once because the <link rel=preload> and the <picture> both have to
# use it - they drifted apart once and every phone downloaded the hero twice.
# The second centre, for the places that name its teacher or its number
# directly. One lookup, so a change in content.py reaches all of them.
SRIRAM = C.CENTRE["sriram"]

HERO_SIZES = ("(min-width:1216px) 1152px, (min-width:640px) calc(100vw - 4rem), "
              "calc(100vw - 2.5rem)")


def photo(key, *, cls, sizes, box=None, priority=False, eager=False, caption=None):
    """A <picture> for one of the centre's photographs.

    Three widths, always with the real intrinsic dimensions so nothing reflows
    when the file lands. Anything not in the first screen is lazy.

    The 320w tier exists because 640w was previously the floor: the hero's two
    side tiles render about 136 CSS px wide on a phone, so every phone was
    pulling roughly three times the pixels it could show. The browser still
    picks 640w for the big hero tile, which is the LCP element and wants the
    detail - `sizes` decides that, not us.
    """
    from PIL import Image
    w, h = Image.open(os.path.join(OUT, f"{key}.jpeg")).size
    # Three tiers, not two. `priority` is for an image that is the LCP
    # element: high priority and a matching <link rel=preload>. `eager` is for
    # one that sits just below the first screen - it must not be lazy, because
    # the reader reaches it within a scroll, but boosting it would make it
    # compete with whatever is actually painting first. Everything else is
    # lazy.
    load = ('fetchpriority="high" decoding="async"' if priority
            else 'decoding="async"' if eager
            else 'loading="lazy" decoding="async"')
    img = (f'<img src="{ASSET_PREFIX}{key}.jpeg" width="{w}" height="{h}" alt="{alt_text(key)}"\n'
           f'                     class="{cls}" {load}>')
    pic = (f"""<picture>
                    <source type="image/webp" sizes="{sizes}"
                            srcset="{ASSET_PREFIX}{key}-xs.webp 320w, {ASSET_PREFIX}{key}-sm.webp 640w, {ASSET_PREFIX}{key}-md.webp 768w, {ASSET_PREFIX}{key}.webp {w}w">
                    <source type="image/jpeg" sizes="{sizes}"
                            srcset="{ASSET_PREFIX}{key}-xs.jpg 320w, {ASSET_PREFIX}{key}-sm.jpg 640w, {ASSET_PREFIX}{key}-md.jpg 768w, {ASSET_PREFIX}{key}.jpeg {w}w">
                    {img}
                </picture>""")
    if caption is None:
        return pic
    return (f"""<figure{f' class="{box}"' if box else ''}>
                {pic}
                <figcaption class="mt-2.5 text-[13px] text-muted">{caption}</figcaption>
            </figure>""")


def band(key, caption, *, h="h-[240px] sm:h-[340px] lg:h-[420px]"):
    """A photograph running the full width of the page between two sections.
    Beach frames carry a caption saying what they are - classes are taught in
    the hall, and nothing here should suggest otherwise."""
    return f"""    <section aria-label="{alt_text(key)}" class="border-y border-line">
        <figure class="par">
            {photo(key, cls=f'w-full {h} object-cover object-[center_45%] block',
                   sizes='100vw')}
            <figcaption class="max-w-6xl mx-auto px-5 sm:px-8 py-3 text-[13px] text-muted">
                {caption}
            </figcaption>
        </figure>
    </section>
"""


def photo_cta(key):
    """The one place copy sits over a photograph. A real class in the hall, not
    the beach, behind a scrim heavy enough to keep the text readable - white on
    a dark overlay, checked against the photograph rather than assumed."""
    return f"""    <section aria-labelledby="cta-h" class="relative isolate border-y border-line overflow-hidden">
        <div class="absolute inset-0 -z-10">
            {photo(key, cls='w-full h-full object-cover object-[center_40%]', sizes='100vw')}
            <div class="cta-scrim" role="presentation"></div>
        </div>
        <div class="max-w-6xl mx-auto px-5 sm:px-8 py-24 lg:py-36">
            <div class="max-w-xl">
                <h2 id="cta-h" class="text-d2 text-white">Four batches a day, Monday to Friday</h2>
                <p class="mt-4 text-[16px] leading-relaxed text-white/85">
                    Ladies, gents and children, in one hall in New Perungalathur. Most who
                    join have never done yoga before. Sit in on a batch on the 2-day trial
                    before deciding anything.
                </p>
                <div class="mt-7 flex flex-wrap gap-3">
                    <a href="{wa(TRIAL_MSG)}" target="_blank" rel="noopener"
                       class="inline-flex items-center px-5 py-3 bg-white text-ink font-medium rounded hover:bg-sand transition-colors">
                        Book a 2-day trial
                    </a>
                    <a href="#schedule"
                       class="inline-flex items-center px-5 py-3 border border-white/40 text-white font-medium rounded hover:border-white transition-colors">
                        See the schedule
                    </a>
                </div>
            </div>
        </div>
    </section>
"""


def journal_block(limit=None):
    """The journal index, as cards with a thumbnail.

    These were date / serif title / two grey lines separated by hairlines,
    which is the same shape as the timetable and the class list - nothing
    said these rows were things to open and read. A picture does, and every
    post already names a photograph, so this costs no new asset."""
    posts = newest_first() if limit is None else newest_first()[:limit]
    rows = []
    for i, post in enumerate(posts):
        rows.append(f"""                <li class="reveal" style="--d:{min(i, 3) * 70}ms">
                    <a href="{post['slug']}" class="post tile !p-3 sm:!p-4">
                        <span class="post__img">
                            {photo(post['photo'], cls='', sizes='(min-width:640px) 176px, 120px')}
                        </span>
                        <span class="block min-w-0 py-1">
                            <time datetime="{post['date']}" class="text-[12.5px] text-muted">{post['date_text']}</time>
                            <span class="post__h mt-1 block display text-d3 text-ink">{post['title']}</span>
                            <span class="mt-1.5 hidden sm:block text-[14px] leading-relaxed text-muted">{post['standfirst']}</span>
                        </span>
                    </a>
                </li>""")
    return "\n".join(rows)


def areas_block():
    chips = "\n".join(
        f'                    <li class="px-3 py-1.5 border border-line rounded lift-full text-[13.5px] text-ink">{a}</li>'
        for a in C.AREAS)
    guides = "\n".join(f"""                <a href="{href}" class="group block border-t border-line py-6 transition-colors hover:bg-sand/60">
                    <span class="display text-d3 text-ink group-hover:text-blue transition-colors">{title}</span>
                    <span class="mt-1 block text-[14px] leading-relaxed text-muted max-w-md">{blurb}</span>
                </a>""" for title, href, blurb in C.AREA_PAGES)
    return chips, guides


LIGHTBOX = f"""    <div id="lightbox" class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer" aria-hidden="true">
        <button id="lightbox-close" type="button" aria-label="Close photo"
                class="absolute top-5 right-5 p-2 text-white/80 hover:text-white">{icon('x', 'w-7 h-7')}</button>
        <img id="lightbox-img" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
             alt="" class="max-w-full max-h-[85vh] object-contain rounded" decoding="async">
    </div>
"""


# ------------------------------------------------------------------- homepage

def build_index():
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            C.business_node(),
            C.branch_node(),
            C.person_node(),
            C.surekha_node(),
            {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/",
             "name": "Happy Yogis Yoga Centre", "inLanguage": "en-IN",
             "publisher": {"@id": f"{BASE}/#business"}},
            {"@type": "WebPage", "@id": f"{BASE}/#webpage", "url": f"{BASE}/",
             "name": "Yoga Centre in New Perungalathur, Chennai | Happy Yogis",
             "isPartOf": {"@id": f"{BASE}/#website"},
             "about": {"@id": f"{BASE}/#business"}, "inLanguage": "en-IN"},
        ],
    }

    h = head(title="Yoga Centre in New Perungalathur, Chennai | Happy Yogis",
             desc=("Yoga classes in New Perungalathur for ladies, gents and children. "
                   "Four batches daily, Mon-Fri, plus online classes. 2-day trial."),
             # No hero preload. It had one while the photograph was the
             # largest paint, but both centres now sit between the buttons
             # and the photograph, which puts the photograph below the fold
             # and makes the headline the LCP element - measured, not
             # assumed. A high-priority preload for an offscreen image only
             # takes bandwidth from the two fonts the headline is waiting on.
             path="", schema=schema,
             alt=("ta", "ta/index.html"))

    filters, class_items = classes_section()
    chips, guides = areas_block()

    body = f"""<body class="font-body bg-paper text-ink text-[15px]">
{nav(home=True, alt_href="/ta/index.html")}
    <main id="main">

    <!-- The opening screen. Near-white: the headline is dark type on paper at
         the top of the display scale, with air around it, and the photograph
         sits beneath as a contained band. It used to be the photograph edge to
         edge with white type over a scrim, which meant the first thing a
         visitor met was a dark panel and the headline could only ever be as
         light as the scrim allowed.

         Nothing here is marked .reveal - the first screen must never wait on a
         script - and the photograph is outside .enter for the same reason: an
         element animating up from opacity 0 is not painted, so wrapping it
         would have pushed the largest paint later rather than earlier. -->
    <section aria-labelledby="hero-h" class="hero pt-20 lg:pt-24 pb-14 lg:pb-20">
        <div class="hero__wash" role="presentation"></div>

        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <div class="enter text-center">
                <p class="lbl">SSM Nagar and Park&nbsp;63 &middot; New Perungalathur, Chennai</p>
                <h1 id="hero-h" class="mt-4 text-d1 text-ink mx-auto">
                    Yoga classes in New Perungalathur, Chennai
                </h1>
                <p class="lede mt-6 text-ink/70 max-w-xl mx-auto">
                    Four small batches a day, Monday to Friday, for ladies, gents and
                    children &mdash; most of whom had never done yoga before.
                </p>
                <div class="mt-8 flex flex-wrap items-center justify-center gap-x-8 gap-y-4">
                    <a id="batch-cta" href="{wa(TRIAL_MSG)}" data-base="{wa(TRIAL_MSG)}"
                       target="_blank" rel="noopener"
                       class="inline-flex items-center px-8 py-4 bg-ink text-white font-medium rounded text-[17px] hover:bg-blue transition-colors">
                        Book a 2-day trial
                    </a>
                    <a href="#schedule" class="cue px-1 py-2 text-[15px] font-medium text-ink/70 hover:text-ink transition-colors">
                        See the timetable {icon('chevron-down', 'w-4 h-4')}
                    </a>
                </div>
            </div>

            <!-- Both centres, directly under the hero. They used to live only
                 in the Visit panel nine sections down, so "where is it?" - the
                 first question a local business gets - needed a long scroll.
                 Each card carries the address, who teaches, when it runs and
                 a directions link straight to its own Google pin. -->
            <ul class="mt-8 lg:mt-10 grid sm:grid-cols-2 gap-3 lg:gap-4 text-left">
{centre_cards()}
            </ul>

            <div class="hero__shot grade par mt-10 lg:mt-14">
                {photo('ima6', cls='object-[center_38%]', eager=True, sizes=HERO_SIZES)}
            </div>
        </div>
    </section>

    <!-- The timetable. It sits on the sand band with the rows on a white
         card, which is what lets the pills read: a tinted pill on the band
         itself measures 1.03:1 and disappears. -->
    <section aria-label="Batch times" class="bg-sand border-y border-line" id="schedule">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 py-16 lg:py-24">
            <div class="grid lg:grid-cols-12 gap-10 lg:gap-14 items-start">
                <div class="lg:col-span-5">
                    <p class="lbl">One day at the centre</p>
                    <h2 class="mt-3 text-d2 text-ink">The room fills four times over</h2>
                    <p class="mt-5 text-[17px] leading-relaxed text-ink/75">
                        Pick the hour that suits your life. You can move between
                        batches when your week changes.
                    </p>
                    <ul class="mt-7 space-y-2.5 text-[15px] text-ink/80">
                        <li class="flex items-center gap-2.5">{icon('check', 'w-4 h-4 text-blue shrink-0')}Monday to Friday, four times a day</li>
                        <li class="flex items-center gap-2.5">{icon('check', 'w-4 h-4 text-blue shrink-0')}A ladies-only batch mid-morning</li>
                        <li class="flex items-center gap-2.5">{icon('check', 'w-4 h-4 text-blue shrink-0')}Online and in person</li>
                    </ul>
                </div>

                <div class="lg:col-span-7">
                    <div class="card p-4 sm:p-5">
                        <div class="flex items-baseline justify-between gap-4 px-[1.1rem] pt-1">
                            <h3 class="display text-d4 text-ink">Today at the centre</h3>
                            <span class="pill pill--quiet">Mon&ndash;Fri</span>
                        </div>
                        <p id="next-class" class="px-[1.1rem] mt-1 text-[13.5px] text-muted">Batches run Monday to Friday.</p>

                        <ul class="mt-3">
{batch_list()}
                        </ul>

                        <p class="mx-[1.1rem] mt-3 pt-3.5 border-t border-line text-[13px] leading-relaxed text-muted">
                            Every batch is warm-up, asanas, pranayama and relaxation.
                            Select one to see who it suits.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- What we teach. Tiles in a grid, on paper so the sand timetable band
         above reads as a separate block. The chips sit directly over the grid
         they filter. -->
    <section id="classes" aria-labelledby="classes-h" class="py-16 lg:py-24">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <div class="max-w-2xl reveal">
                <p class="lbl">What we teach</p>
                <h2 id="classes-h" class="mt-3 text-d2 text-ink">Everything is taught inside the regular batch</h2>
                <p class="mt-4 text-[16px] leading-relaxed text-ink/75">
                    There is no separate course to book. Tell the teacher what you
                    are working towards and it gets built in.
                </p>
            </div>

            <div class="mt-8 flex flex-wrap gap-2 reveal" role="group" aria-label="Filter classes">
{filters}
            </div>

            <p id="filter-status" class="sr-only" role="status" aria-live="polite"></p>
            <ul class="mt-6 grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
{class_items}
            </ul>

            <!-- Guides for specific people and goals. Several of these pages
                 had a single link into them from the whole site, which is a
                 large part of why Google had discovered them without ever
                 crawling them. -->
            <div class="mt-10 reveal">
                <h3 class="text-[13.5px] font-medium text-ink">Looking for something specific?</h3>
                <ul class="mt-3 flex flex-wrap gap-2">
{guide_pills()}
                </ul>
            </div>
        </div>
    </section>

    <!-- Health -->
    <section id="health" aria-labelledby="health-h" class="py-16 lg:py-24 bg-sand border-y border-line">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-10 lg:gap-16">
            <div class="lg:col-span-4 reveal">
                <h2 id="health-h" class="text-d2 text-ink">Practising around a health condition</h2>
                <p class="mt-4 text-[16px] leading-relaxed text-ink/75">
                    Many of our students come because a doctor suggested it. Tell us what
                    you are dealing with before your first class, so the teacher can plan
                    around it.
                </p>
                <p class="mt-4 text-[13.5px] leading-relaxed text-muted">
                    Yoga supports treatment; it does not replace it. If you are under
                    medical care, please keep your doctor in the loop.
                </p>
            </div>
            <div class="lg:col-span-8">
                <dl class="bento bento-open-b sm:grid-cols-2 lg:grid-cols-12">
{health_list()}
                </dl>
                <div class="bento-foot bg-paper">
                    {photo('ima5', cls='w-full h-[230px] sm:h-[280px] object-cover object-[center_45%] block',
                           sizes='(min-width:1024px) 768px, 100vw')}
                </div>
            </div>
        </div>
    </section>

    <!-- Teachers. Two of them since the Sriram Apartments room opened, so this
         is a pair of columns rather than one portrait and a bio. Karthika's
         column runs longer; items-start lets it, instead of centring Surekha's
         shorter one against nothing. -->
    <section id="teacher" aria-labelledby="teacher-h" class="py-16 lg:py-24">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <div class="max-w-2xl reveal">
                <p class="lbl">Who teaches</p>
                <h2 id="teacher-h" class="mt-3 text-d2 text-ink">Two teachers, two centres</h2>
                <p class="mt-4 text-[16px] leading-relaxed text-ink/75">
                    Batches are small enough that the teacher knows what each person
                    is working with &mdash; a bad knee, a desk job, a first week of
                    yoga &mdash; and the practice is adjusted around that.
                </p>
            </div>

            <div class="mt-12 lg:mt-16 grid md:grid-cols-2 gap-10 lg:gap-16 items-start">
                <div class="reveal">
                    <div class="arch zoom grade grade--portrait w-full max-w-xs">
                        <picture>
                            <source type="image/webp"
                                    srcset="instructor-portrait-xs.webp 300w, instructor-portrait-sm.webp 560w, instructor-portrait.webp 720w"
                                    sizes="(min-width:768px) 320px, 80vw">
                            <img src="instructor-portrait.jpeg" width="720" height="900"
                                 alt="Karthika, yoga teacher at Happy Yogis Yoga Centre, New Perungalathur"
                                 class="w-full aspect-[4/5] object-cover" loading="lazy" decoding="async">
                        </picture>
                    </div>
                    <h3 class="mt-7 text-d3 display text-ink">Karthika</h3>
                    <p class="mt-1 text-[14px] text-muted">Teaches every batch at SSM Nagar</p>
                    <div class="mt-4 space-y-4 text-[16px] leading-relaxed text-ink/80">
                        <p>
                            Karthika has practised and taught yoga for more than ten years,
                            and takes every batch at the SSM Nagar centre herself.
                        </p>
                        <p>
                            She meets people where they are. Beginners are not pushed into
                            postures they are not ready for, and anyone working around an
                            injury or a health condition gets the practice adapted rather
                            than being told to sit it out.
                        </p>
                    </div>
                    <a href="{PHONE_HREF}" class="mt-5 inline-flex items-center gap-2 py-1 text-blue font-medium hover:underline">
                        {icon('phone', 'w-4 h-4')}{PHONE_TEXT}
                    </a>
                </div>

                <div class="reveal" style="--d:90ms">
                    <div class="arch zoom grade grade--portrait w-full max-w-xs">
                        <picture>
                            <source type="image/webp"
                                    srcset="surekha-portrait-xs.webp 300w, surekha-portrait-sm.webp 560w, surekha-portrait.webp 720w"
                                    sizes="(min-width:768px) 320px, 80vw">
                            <img src="surekha-portrait.jpeg" width="720" height="900"
                                 alt="Surekha, yoga teacher at the Happy Yogis centre at Park 63, New Perungalathur"
                                 class="w-full aspect-[4/5] object-cover" loading="lazy" decoding="async">
                        </picture>
                    </div>
                    <h3 class="mt-7 text-d3 display text-ink">Surekha</h3>
                    <p class="mt-1 text-[14px] text-muted">Teaches the morning batch at Park 63</p>
                    <div class="mt-4 space-y-4 text-[16px] leading-relaxed text-ink/80">
                        <p>
                            Surekha takes the 5:30&ndash;6:30 am batch, Monday to Friday, in
                            the yoga room at Tower&nbsp;20, Park&nbsp;63. It is the same
                            practice taught at SSM Nagar, a short walk from home for anyone
                            living on the campus.
                        </p>
                    </div>
                    <a href="{SRIRAM['phone_href']}" class="mt-5 inline-flex items-center gap-2 py-1 text-blue font-medium hover:underline">
                        {icon('phone', 'w-4 h-4')}{SRIRAM['phone_text']}
                    </a>
                </div>
            </div>

            <div class="mt-12 lg:mt-14 reveal">
                <a href="{wa('Hello Happy Yogis! I would like to book a 2-day trial.')}"
                   target="_blank" rel="noopener"
                   class="inline-flex items-center px-5 py-3 bg-ink text-white font-medium rounded hover:bg-blue transition-colors">
                    Book a 2-day trial
                </a>
            </div>
        </div>
    </section>

    <!-- Studio photos -->
    <section id="studio" aria-labelledby="studio-h" class="py-16 lg:py-24 bg-sand border-y border-line">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <div class="max-w-xl reveal">
                <h2 id="studio-h" class="text-d2 text-ink">Inside the centre</h2>
                <p class="mt-3 text-[16px] leading-relaxed text-ink/75">
                    Real batches, real students, photographed at the centre. Select any
                    photo to see it larger.
                </p>
            </div>
            <div class="mt-8 columns-2 sm:columns-3 lg:columns-4 xl:columns-6 gap-3">
{gallery(12)}
            </div>

            <div class="mt-10 reveal">
                <h3 class="text-[13.5px] font-medium text-ink">The stories behind the photos</h3>
                <ul class="mt-3 flex flex-wrap gap-2">
{story_pills()}
                </ul>
            </div>
        </div>
    </section>

    <!-- Reviews. Twelve of these used to sit here, 936 words of the home
         page's 2,285. Three and a link carry the same signal. -->
    <section id="reviews" aria-labelledby="reviews-h" class="py-16 lg:py-24">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <div class="sm:flex sm:items-end sm:justify-between sm:gap-10">
                <div class="max-w-xl reveal">
                    <p class="lbl">In their words</p>
                    <h2 id="reviews-h" class="mt-3 text-d2 text-ink">What students say</h2>
                </div>
                <a href="reviews.html"
                   class="mt-5 sm:mt-0 inline-flex shrink-0 items-center gap-1.5 px-4 py-2.5 border border-line rounded-full text-[14px] font-medium text-ink hover:border-ink transition-colors">
                    All {len(C.REVIEWS)} reviews {icon('arrow-right', 'w-4 h-4')}
                </a>
            </div>
            <ul class="mt-8 grid md:grid-cols-3 gap-4">
{review_cards(3)}
            </ul>
        </div>
    </section>

    <!-- Yogi's Upadesha: newest posts, from the same list the section renders -->
    <section id="journal" aria-labelledby="journal-h" class="py-16 lg:py-24 bg-sand border-y border-line">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <div class="sm:flex sm:items-end sm:justify-between sm:gap-10">
                <div class="max-w-xl reveal">
                    <p class="lbl">Yogi&rsquo;s Upadesha</p>
                    <h2 id="journal-h" class="mt-3 text-d2 text-ink">What people ask before they start</h2>
                </div>
                <a href="blog.html"
                   class="mt-5 sm:mt-0 inline-flex shrink-0 items-center gap-1.5 px-4 py-2.5 border border-line rounded-full text-[14px] font-medium text-ink hover:border-ink transition-colors">
                    All entries {icon('arrow-right', 'w-4 h-4')}
                </a>
            </div>

            <ul class="mt-8 grid sm:grid-cols-2 gap-4">
{journal_block(2)}
            </ul>
        </div>
    </section>

    <!-- Areas -->
    <section id="areas" aria-labelledby="areas-h" class="py-16 lg:py-24">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-10 lg:gap-16">
            <div class="lg:col-span-5 reveal">
                <h2 id="areas-h" class="text-d2 text-ink">Two centres, both in New Perungalathur</h2>
                <p class="mt-4 text-[16px] leading-relaxed text-ink/75">
                    Both are just off the GST Road stretch between Tambaram and Vandalur,
                    close to Perungalathur railway station. SSM Nagar runs all four
                    batches; the yoga room at Tower&nbsp;20, Park&nbsp;63 has run the
                    early morning batch since October. Students travel in from the
                    neighbourhoods nearby, and we teach online for anyone who cannot
                    travel to either.
                </p>
                <h3 class="mt-8 text-[13.5px] font-medium text-ink">Students travel in from</h3>
                <ul class="mt-3 flex flex-wrap gap-2">
{chips}
                </ul>
            </div>
            <div class="lg:col-span-7 lg:pt-1 reveal" style="--d:90ms">
{guides}
                <div class="border-t border-line"></div>
            </div>
        </div>
    </section>

    <!-- Enquiry + visit -->
    <section id="visit" aria-labelledby="visit-h" class="py-16 lg:py-24 bg-sand border-y border-line">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-10 lg:gap-16">

            <div class="lg:col-span-6 reveal" id="enquire">
                <h2 id="visit-h" class="text-d2 text-ink">Book a 2-day trial</h2>
                <p class="mt-3 text-[16px] leading-relaxed text-ink/75 max-w-lg">
                    Fill this in and it opens WhatsApp with your details ready to send. We
                    will tell you which batches have room.
                </p>

                <form id="enquiry-form" class="mt-7 space-y-4 max-w-lg" novalidate>
                    <div>
                        <label for="f-name" class="block text-[13.5px] font-medium text-ink">Your name</label>
                        <input id="f-name" name="name" type="text" autocomplete="name" required
                               class="mt-1.5 w-full px-3.5 py-2.5 bg-paper border border-line rounded lift text-[16px] text-ink placeholder:text-muted">
                    </div>
                    <div>
                        <label for="f-phone" class="block text-[13.5px] font-medium text-ink">Phone number</label>
                        <input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required
                               class="mt-1.5 w-full px-3.5 py-2.5 bg-paper border border-line rounded lift text-[16px] text-ink placeholder:text-muted">
                    </div>
                    <div class="sm:grid sm:grid-cols-2 sm:gap-4 space-y-4 sm:space-y-0">
                        <div>
                            <label for="f-batch" class="block text-[13.5px] font-medium text-ink">Preferred batch</label>
                            <select id="f-batch" name="batch"
                                    class="mt-1.5 w-full px-3.5 py-2.5 bg-paper border border-line rounded lift text-[16px] text-ink">
                                <option value="">No preference</option>
{chr(10).join(f'                                <option>{lbl.replace("&ndash;", "-")}{" (ladies only)" if who == "Ladies only" else ""}</option>' for _, lbl, _, who, _ in C.BATCHES)}
                            </select>
                        </div>
                        <div>
                            <label for="f-mode" class="block text-[13.5px] font-medium text-ink">Format</label>
                            <select id="f-mode" name="mode"
                                    class="mt-1.5 w-full px-3.5 py-2.5 bg-paper border border-line rounded lift text-[16px] text-ink">
                                <option value="">Either</option>
                                <option>At the centre</option>
                                <option>Online</option>
                            </select>
                        </div>
                    </div>
                    <div>
                        <label for="f-notes" class="block text-[13.5px] font-medium text-ink">
                            Anything the teacher should know
                            <span class="font-normal text-muted">(optional)</span>
                        </label>
                        <textarea id="f-notes" name="notes" rows="3"
                                  class="mt-1.5 w-full px-3.5 py-2.5 bg-paper border border-line rounded lift text-[16px] text-ink placeholder:text-muted"
                                  placeholder="Knee pain, PCOD, pregnancy, a goal you have in mind&hellip;"></textarea>
                        <p class="mt-1.5 text-[12.5px] leading-relaxed text-muted">
                            Only shared with your teacher. See our
                            <a href="privacy-policy.html" class="underline hover:text-ink">privacy policy</a>.
                        </p>
                    </div>
                    <button type="submit"
                            class="inline-flex items-center gap-2 px-5 py-3 bg-[#17843F] text-white font-medium rounded hover:bg-[#126B33] transition-colors">
                        {icon('message-circle', 'w-4 h-4')}Open WhatsApp with my details
                    </button>
                    <p id="form-note" hidden role="status"
                       class="text-[13.5px] leading-relaxed text-ink bg-paper border border-line rounded lift px-4 py-3">
                        WhatsApp should have opened in a new tab with your message ready.
                        Press send there and we will get back to you. If nothing opened,
                        call us on <a href="{PHONE_HREF}" class="underline">{PHONE_TEXT}</a>.
                    </p>
                </form>
            </div>

            <div class="lg:col-span-6 reveal" style="--d:90ms">
                <h2 class="text-d2 text-ink">Visit us</h2>

                <!-- bento: the map holds the wide tile, the three facts sit under it -->
                <div class="bento mt-6 sm:grid-cols-2">
                    <div class="sm:col-span-2 bg-paper">
                        <iframe title="Map showing the Happy Yogis centre at SSM Nagar, New Perungalathur"
                                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3887.8938068!2d80.1131382!3d12.8938068!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a5259bd7762301f%3A0xbb838e445fc93a!2sHAPPY%20YOGIS%20YOGA%20CENTRE!5e0!3m2!1sen!2sin!4v1234567890"
                                width="100%" height="280" style="border:0;display:block" allowfullscreen=""
                                loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                    </div>
                    <div class="bg-paper p-6">
                        <p class="text-[13px] text-muted">SSM Nagar &middot; all four batches</p>
                        <address class="mt-1.5 not-italic display text-d3 text-ink">SSM Nagar, New Perungalathur,<br>Chennai, Tamil Nadu 600063</address>
                        <p class="mt-2 text-[14px] text-muted">Taught by Karthika</p>
                        <a href="{PHONE_HREF}" class="mt-1 block py-1 text-[15px] font-medium text-ink hover:text-blue transition-colors">{PHONE_TEXT}</a>
                        <a href="{MAPS}" target="_blank" rel="noopener"
                           class="mt-3 py-1 inline-flex items-center gap-1.5 text-[14px] font-medium text-blue hover:underline">
                            Get directions {icon('arrow-up-right', 'w-4 h-4')}
                        </a>
                    </div>
                    <div class="bg-paper p-6">
                        <p class="text-[13px] text-muted">Park 63 &middot; 5:30 &ndash; 6:30 am</p>
                        <address class="mt-1.5 not-italic display text-d3 text-ink">Yoga Room, Tower 20,<br>Park 63, New Perungalathur</address>
                        <p class="mt-2 text-[14px] text-muted">Taught by Surekha &middot; open since October</p>
                        <a href="{SRIRAM['phone_href']}" class="mt-1 block py-1 text-[15px] font-medium text-ink hover:text-blue transition-colors">{SRIRAM['phone_text']}</a>
                        <a href="{SRIRAM['maps']}" target="_blank" rel="noopener"
                           class="mt-3 py-1 inline-flex items-center gap-1.5 text-[14px] font-medium text-blue hover:underline">
                            Get directions {icon('arrow-up-right', 'w-4 h-4')}
                        </a>
                    </div>
                    <div class="sm:col-span-2 bg-paper p-6">
                        <p class="text-[13px] text-muted">Open</p>
                        <p class="mt-1.5 text-[15px] leading-relaxed text-ink">{C.HOURS_TEXT}</p>
                        <p class="text-[14px] text-muted">{C.CLOSED_TEXT}</p>
                        <p class="mt-2 text-[14px] text-muted">Online classes run at all four times, from either centre.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    </main>

{footer()}
{LIGHTBOX}
{SCRIPT}"""
    return h + body


# ------------------------------------------------------- location landing pages

LOCATIONS = {
    "yoga-classes-perungalathur.html": {
        "area": "Perungalathur",
        # Google chose a different canonical for this page than the one we
        # declared. The home page now targets "New Perungalathur, Chennai" and
        # this page was a thin 312 words sharing a third of its phrasing with
        # the Tambaram page, so it read as a duplicate of one or the other.
        # It now carries what only it can: both centres, side by side.
        "title": "Yoga Classes in Perungalathur: Two Centres | Happy Yogis",
        "desc": ("Happy Yogis has two centres in New Perungalathur: SSM Nagar with "
                 "four daily batches, and Park 63 at 5:30 am. Ladies-only batch. "
                 "2-day trial."),
        "h1": "Yoga classes in Perungalathur",
        "lede": ("Happy Yogis has two centres in New Perungalathur &mdash; SSM Nagar and "
                 "the yoga room at Tower 20, Park 63. If you live in "
                 "Perungalathur, this is your local class, not a drive across the city."),
        "body": [
            ("Two centres, both in New Perungalathur",
             "Both are just off the GST Road stretch running down towards Vandalur, "
             "and students walk or ride in from New Perungalathur, Old Perungalathur "
             "and the streets around. Which one suits you is mostly a question of "
             "the hour you want."),
            ("SSM Nagar: four batches a day",
             "The original centre, close to Perungalathur railway station, and the "
             "one that runs all four batches: 5:30 to 6:15 am, 6:15 to 7:15 am, a "
             "ladies-only 10:00 to 11:00 am and 5:00 to 6:00 pm. Karthika teaches "
             "every one of them."),
            ("Park 63: the early morning batch",
             "The yoga room at Tower&nbsp;20, Park&nbsp;63, open since October, runs "
             "one batch &mdash; 5:30 to 6:30 am, Monday to Friday &mdash; taught by "
             "Surekha. If you live in the complex, there is no journey to fail. "
             "<a href=\"new-yoga-centre-park-63-perungalathur.html\" "
             "class=\"text-blue font-medium hover:underline\">Read how it opened</a>."),
            ("Who practises here",
             "Genuinely mixed &mdash; school children before class, people fitting a "
             "session in before the commute, women in the mid-morning ladies batch, "
             "retired members there for the joint mobility and the company. Most who "
             "join have never done yoga before. Men often ask whether it is a "
             "women's class; "
             "<a href=\"yoga-classes-for-men-perungalathur.html\" "
             "class=\"text-blue font-medium hover:underline\">it is not</a>."),
            ("What a class looks like",
             "Every batch: warm-up, asanas, pranayama and a closing relaxation, in 45 "
             "or 60 minutes. "
             "If you are working around a knee problem, back pain, PCOD or a thyroid "
             "condition, tell the teacher beforehand and the practice is adjusted for "
             "you. "
             "<a href=\"what-happens-in-your-first-yoga-class.html\" "
             "class=\"text-blue font-medium hover:underline\">Here is what the hour "
             "holds</a>."),
            ("Children and families",
             "Children practise in the regular batches, next to a parent, rather than "
             "in a separate class. "
             "<a href=\"yoga-classes-for-children-perungalathur.html\" "
             "class=\"text-blue font-medium hover:underline\">How it works for "
             "children</a>, and "
             "<a href=\"why-yoga-is-good-for-children.html\" "
             "class=\"text-blue font-medium hover:underline\">why yoga suits them</a>."),
            ("Getting started",
             "Message us on WhatsApp for a 2-day trial in whichever batch has room. "
             "Bring a mat if you have one; once you join, you can leave it at the "
             "centre."),
        ],
        "photo": "ima1", "og": "og-perungalathur.jpg",
        "nearby": [("Yoga classes near Tambaram", "yoga-classes-tambaram.html"),
                   ("A second centre: the yoga room at Park 63",
                    "new-yoga-centre-park-63-perungalathur.html")],
    },
    "yoga-classes-tambaram.html": {
        "area": "Tambaram",
        "title": "Yoga Classes near Tambaram, Chennai | Happy Yogis",
        "desc": ("Yoga centre a short run down GST Road from Tambaram, in New "
                 "Perungalathur. Morning and evening batches, ladies-only batch, "
                 "online classes."),
        "h1": "Yoga classes near Tambaram",
        "lede": ("Happy Yogis has two centres, both in New Perungalathur &mdash; "
                 "the next stop down the GST Road and the suburban line from Tambaram. "
                 "There is no Tambaram branch, but many of our regulars travel in from "
                 "East Tambaram, West Tambaram and Selaiyur."),
        "body": [
            ("Getting here from Tambaram",
             "SSM Nagar, New Perungalathur, near Perungalathur railway station &mdash; "
             "one stop along the Chengalpattu line from Tambaram, or a straight run "
             "south on the GST Road. Students from Selaiyur and East Tambaram usually "
             "come by two-wheeler."),
            ("Which batch suits a Tambaram commute",
             "Heading into the city afterwards, the 5:30 am and 6:15 am batches at "
             "SSM Nagar work best. The 5:00 pm batch is the popular one for school and college "
             "students travelling back from Tambaram. The 10:00 am batch is women "
             "only."),
            ("Or practise from home",
             "We also teach online, which several Tambaram-side students use when the "
             "GST Road traffic is not worth it. Same teacher, same batch structure; "
             "switch between online and the centre as your week allows."),
            ("What we teach",
             "Beginner yoga, weight-loss and stamina work, flexibility and posture, "
             "pranayama and meditation, plus practice adapted around PCOD, thyroid, "
             "knee pain, back problems and pregnancy. Children practise alongside "
             "their parents."),
        ],
        "photo": "ima6", "og": "og-tambaram.jpg",
        "nearby": [("Yoga classes in Perungalathur", "yoga-classes-perungalathur.html")],
    },
}


def build_location(slug, cfg):
    area = cfg["area"]
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            C.business_node(),
            C.branch_node(),
            {"@type": "WebPage", "@id": f"{BASE}/{slug}#webpage",
             "url": f"{BASE}/{slug}", "name": cfg["title"], "description": cfg["desc"],
             "inLanguage": "en-IN", "isPartOf": {"@id": f"{BASE}/#website"},
             "about": {"@id": f"{BASE}/#business"}},
            {"@type": "BreadcrumbList", "@id": f"{BASE}/{slug}#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                 {"@type": "ListItem", "position": 2, "name": f"Yoga classes in {area}",
                  "item": f"{BASE}/{slug}"}]},
        ],
    }

    sections = "\n".join(f"""            <h2 class="text-d2 text-ink mt-12">{t}</h2>
            <p class="mt-3 text-[16px] leading-relaxed text-ink/80">{p}</p>""" for t, p in cfg["body"])

    rows = "\n".join(
        f'                    <li class="flex justify-between gap-4 border-t border-line py-3">'
        f'<span class="text-ink">{lbl}</span>'
        f'<span class="{"text-blue font-medium" if who == "Ladies only" else "text-muted"}">{who}</span></li>'
        for _, lbl, _, who, _ in C.BATCHES)

    nearby = "\n".join(
        f'                <li><a href="{h}" class="inline-block py-1 text-blue font-medium hover:underline">{n}</a></li>'
        for n, h in cfg["nearby"])

    # Both centres, with their own address, teacher, hours and directions. This
    # block said "All classes are taught at this address - it is our only
    # centre" on every area page after the second one opened.
    centres = "\n".join(f"""                <div>
                    <p class="font-medium text-ink">{c['name']} &middot; {'all four batches' if c['key'] == 'ssm' else '5:30 am'}</p>
                    <address class="not-italic text-muted mt-1">{c['street']}, Chennai {c['postal']}</address>
                    <p class="text-muted mt-1.5">Taught by {c['teacher']}</p>
                    <a href="{c['maps']}" target="_blank" rel="noopener"
                       class="mt-2 py-1 inline-flex items-center gap-1.5 font-medium text-blue hover:underline">
                        Get directions {icon('arrow-up-right', 'w-4 h-4')}
                    </a>
                </div>""" for c in C.CENTRES)

    head_html = head(title=cfg["title"], desc=cfg["desc"], path=slug, schema=schema,
                     og_img=cfg["og"], alt=("ta", f"ta/{slug}"))

    body = f"""<body class="font-body bg-paper text-ink text-[15px]">
{nav(alt_href=f"/ta/{slug}")}
    <main id="main" class="pt-16">

    <nav aria-label="Breadcrumb" class="max-w-3xl mx-auto px-5 sm:px-8 pt-8">
        <ol class="flex flex-wrap items-center gap-2 text-[13.5px] text-muted">
            <li><a href="/" class="inline-block py-1 hover:text-ink">Home</a></li>
            <li aria-hidden="true">/</li>
            <li aria-current="page" class="text-ink">Yoga classes in {area}</li>
        </ol>
    </nav>

    <article class="max-w-3xl mx-auto px-5 sm:px-8 py-10 lg:py-14">
        <h1 class="text-d1 text-ink">{cfg["h1"]}</h1>
        <p class="mt-5 text-[17px] leading-relaxed text-ink/80">{cfg["lede"]}</p>
        <div class="mt-7 flex flex-wrap gap-3">
            <a href="{wa(f'Hello Happy Yogis! I am from {area} and would like to book a 2-day trial.')}"
               target="_blank" rel="noopener"
               class="inline-flex items-center px-5 py-3 bg-ink text-white font-medium rounded hover:bg-blue transition-colors">
                Book a 2-day trial
            </a>
            <a href="{PHONE_HREF}" class="inline-flex items-center gap-2 px-5 py-3 border border-line text-ink font-medium rounded hover:border-ink transition-colors">
                {icon('phone', 'w-4 h-4')}{PHONE_TEXT}
            </a>
        </div>

        <!-- The lead image is the largest thing on the first screen, so it
             carries the real widths and is fetched eagerly. Left lazy it was
             the LCP element and the browser deferred it. -->
        <picture>
            <source type="image/webp" sizes="(min-width:768px) 720px, 92vw"
                    srcset="{cfg['photo']}-xs.webp 320w, {cfg['photo']}-sm.webp 640w, {cfg['photo']}-md.webp 768w, {cfg['photo']}.webp 1280w">
            <source type="image/jpeg" sizes="(min-width:768px) 720px, 92vw"
                    srcset="{cfg['photo']}-xs.jpg 320w, {cfg['photo']}-sm.jpg 640w, {cfg['photo']}-md.jpg 768w, {cfg['photo']}.jpeg 1280w">
            <img src="{cfg['photo']}.jpeg" width="1280" height="960" alt="{alt_text(cfg['photo'])}"
                 class="w-full rounded mt-10" fetchpriority="high" decoding="async">
        </picture>

{sections}

        <aside class="mt-14 border border-line rounded lift p-6 sm:p-8 bg-sand">
            <h2 class="text-d3 text-ink">Batch timings</h2>
            <p class="mt-1.5 text-[13.5px] text-muted">{C.HOURS_TEXT}. {C.CLOSED_TEXT}.</p>
            <ul class="mt-5">
{rows}
                <li class="border-t border-line"></li>
            </ul>
            <div class="mt-6 grid sm:grid-cols-2 gap-6 text-[14px]">
{centres}
            </div>
        </aside>

        <nav aria-labelledby="nearby-h" class="mt-12">
            <h2 id="nearby-h" class="text-[13.5px] font-medium text-ink">Nearby</h2>
            <ul class="mt-3 space-y-0.5">
{nearby}
                <li><a href="/#areas" class="inline-block py-1 text-blue font-medium hover:underline">All areas we teach</a></li>
            </ul>
        </nav>

        <div class="mt-10 border-t border-line pt-5">
            <h2 class="text-[13.5px] font-medium text-ink">From {JOURNAL}</h2>
            <a href="hatha-yoga-in-chennai.html" class="group mt-3 block">
                <span class="display text-d3 text-ink group-hover:text-blue transition-colors">Hatha yoga in Chennai for a working week</span>
                <span class="mt-1.5 block text-[14px] leading-relaxed text-muted">
                    What the practice is, why it suits desk work and long commutes, and
                    which of the four batches fits your day.
                </span>
            </a>
        </div>
    </article>

    </main>

{footer()}
{SCRIPT}"""
    return head_html + body


def build_simple(*, slug, title, desc, lbl, h1, lede, inner, extra_nodes=(),
                 crumb, alt=None):
    """A short standalone page: breadcrumb, heading, one block of content.

    reviews.html and faq.html are built with it. Both were sections of the
    home page; between them they were a quarter of its words, and neither is
    something a visitor reads on the way to booking a class."""
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            C.business_node(),
            {"@type": "WebPage", "@id": f"{BASE}/{slug}#webpage",
             "url": f"{BASE}/{slug}", "name": title, "description": desc,
             "inLanguage": "en-IN", "isPartOf": {"@id": f"{BASE}/#website"},
             "about": {"@id": f"{BASE}/#business"}},
            {"@type": "BreadcrumbList", "@id": f"{BASE}/{slug}#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                 {"@type": "ListItem", "position": 2, "name": crumb,
                  "item": f"{BASE}/{slug}"}]},
            *extra_nodes,
        ],
    }
    body = f"""<body class="font-body bg-paper text-ink text-[15px]">
{nav(alt_href=alt[1] if alt else None)}
    <main id="main" class="pt-16">

    <nav aria-label="Breadcrumb" class="max-w-4xl mx-auto px-5 sm:px-8 pt-8">
        <ol class="flex flex-wrap items-center gap-2 text-[13.5px] text-muted">
            <li><a href="/" class="inline-block py-1 hover:text-ink transition-colors">Home</a></li>
            <li aria-hidden="true">/</li>
            <li><span aria-current="page" class="text-ink">{crumb}</span></li>
        </ol>
    </nav>

    <header class="max-w-4xl mx-auto px-5 sm:px-8 pt-8 pb-12 lg:pb-16">
        <p class="lbl">{lbl}</p>
        <h1 class="mt-3 text-d2 text-ink">{h1}</h1>
        <p class="lede mt-5 text-ink/75 max-w-2xl">{lede}</p>
    </header>

{inner}

    </main>
{footer()}
{SCRIPT}"""
    return head(title=title, desc=desc, path=slug, schema=schema,
                alt=alt) + body


def build_reviews():
    inner = f"""    <section aria-label="Reviews" class="pb-20 lg:pb-28">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <ul class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
{review_cards()}
            </ul>
            <p class="mt-10 text-[15px] text-muted max-w-2xl">
                These are the reviews students have left on our Google profile,
                quoted as written. We do not mark them up as rating data here
                &mdash; a business feeding its own reviews back to Google as
                structured data is what its guidelines prohibit.
            </p>
            <a href="{C.REVIEWS_URL}" target="_blank" rel="noopener"
               class="mt-5 inline-flex items-center gap-1.5 text-[15px] font-medium text-blue hover:underline">
                Read them on Google {icon('arrow-up-right', 'w-4 h-4')}
            </a>
        </div>
    </section>"""
    return build_simple(
        slug="reviews.html",
        title="What students say | Happy Yogis Yoga Centre",
        desc=("Reviews from students at Happy Yogis Yoga Centre, New Perungalathur, "
              "quoted from our Google profile."),
        lbl="In their words", h1="What students say",
        lede=("Left by students on our Google profile, quoted as written."),
        crumb="Reviews", inner=inner)


def build_faq():
    faq_node = {"@type": "FAQPage", "@id": f"{BASE}/faq.html#faq",
                "mainEntity": [{"@type": "Question", "name": q,
                                "acceptedAnswer": {"@type": "Answer", "text": a}}
                               for q, a in C.FAQS]}
    inner = f"""    <section aria-label="Questions" class="pb-20 lg:pb-28">
        <div class="max-w-3xl mx-auto px-5 sm:px-8">
            <div class="card px-5 sm:px-7">
{faq_list(2)}
            </div>
            <section aria-labelledby="faq-more" class="mt-10">
                <h2 id="faq-more" class="display text-d3 text-ink">Read more</h2>
                <p class="mt-2 text-[15px] leading-relaxed text-ink/75">
                    Longer guides on the questions above, and on getting to the centre.
                </p>
                <ul class="mt-4 flex flex-wrap gap-2">
{guide_pills()}
                </ul>
                <ul class="mt-3 flex flex-wrap gap-2">
{_pills([(t, h) for t, h, _ in C.AREA_PAGES])}
                </ul>
            </section>
            <div class="mt-10 card px-5 py-6 sm:p-7">
                <h2 class="display text-d3 text-ink">Still not sure?</h2>
                <p class="mt-2 text-[15px] leading-relaxed text-ink/75">
                    Ask us on WhatsApp, or call the centre. Nobody is put on a list.
                </p>
                <div class="mt-5 flex flex-wrap gap-3">
                    <a href="{wa(TRIAL_MSG)}" target="_blank" rel="noopener"
                       class="inline-flex items-center px-5 py-3 bg-ink text-white font-medium rounded hover:bg-blue transition-colors">
                        Book a 2-day trial
                    </a>
                    <a href="{PHONE_HREF}"
                       class="inline-flex items-center gap-2 px-5 py-3 border border-line text-ink font-medium rounded hover:border-ink transition-colors">
                        {icon('phone', 'w-4 h-4')}{PHONE_TEXT}
                    </a>
                </div>
            </div>
        </div>
    </section>"""
    return build_simple(
        slug="faq.html",
        title="Questions before you join | Happy Yogis Yoga Centre",
        desc=("Common questions about yoga classes at Happy Yogis, New Perungalathur "
              "- batches, what to bring, and who the classes suit."),
        lbl="Before you join", h1="Questions people ask",
        lede=("What an hour contains, what to bring, and who each batch suits."),
        crumb="Questions", inner=inner, extra_nodes=(faq_node,))


if __name__ == "__main__":
    open(os.path.join(OUT, "index.html"), "w").write(build_index())
    print("index.html written")
    for name, fn in (("reviews.html", build_reviews), ("faq.html", build_faq)):
        open(os.path.join(OUT, name), "w").write(fn())
        print(f"{name} written")
    for slug, cfg in LOCATIONS.items():
        open(os.path.join(OUT, slug), "w").write(build_location(slug, cfg))
        print(f"{slug} written")
