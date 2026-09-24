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
TRIAL_MSG = "Hello Happy Yogis! I would like to book a 3-day trial."


# ------------------------------------------------------------------ fragments

def batch_list():
    """The hero's schedule panel. Each row expands on click; the CTA below
    rewrites itself to name whichever batch is open."""
    rows = []
    for i, (t24, label, length, who, note) in enumerate(C.BATCHES):
        plain = label.replace("&ndash;", "-")
        rows.append(f"""                    <li>
                        <button type="button" class="batch group" data-start="{t24}" data-label="{plain}"
                                aria-expanded="false" aria-controls="batch-d{i}">
                            <span class="flex items-baseline justify-between gap-4">
                                <span class="display text-[17px] text-ink">{label}</span>
                                <span class="text-[13px] text-muted whitespace-nowrap">{length}</span>
                            </span>
                            <span class="mt-0.5 block text-[13px] {'text-blue font-medium' if who == 'Ladies only' else 'text-muted'}">{who}</span>
                        </button>
                        <div id="batch-d{i}" class="batch-detail">
                            <p class="pb-4 text-[14px] leading-relaxed text-muted max-w-md">{note}</p>
                        </div>
                    </li>""")
    return "\n".join(rows)


def classes_section():
    groups = [g for g, _ in C.CLASS_GROUPS]
    filters = ['                    <button type="button" class="filter px-3 py-1.5 text-[13.5px] border border-line rounded lift-full text-ink transition-colors" data-group="all" aria-pressed="true">Everything</button>']
    for g in groups:
        filters.append(f'                    <button type="button" class="filter px-3 py-1.5 text-[13.5px] border border-line rounded lift-full text-ink transition-colors" data-group="{g}" aria-pressed="false">{g}</button>')

    items = []
    for g, entries in C.CLASS_GROUPS:
        for name, desc in entries:
            items.append(f"""                <li class="class-item border-t border-line py-6" data-group="{g}">
                    <div class="sm:flex sm:items-baseline sm:gap-8">
                        <h3 class="display text-d3 text-ink sm:w-64 sm:shrink-0">{name}</h3>
                        <p class="mt-1.5 sm:mt-0 text-[15px] leading-relaxed text-muted max-w-2xl">{desc}</p>
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


def faq_list():
    return "\n".join(f"""                <div class="faq-item border-b border-line">
                    <h3>
                        <button type="button" class="faq-q w-full flex items-start justify-between gap-6 py-5 text-left">
                            <span class="text-[16px] font-medium text-ink">{q}</span>
                            <span class="shrink-0 mt-0.5 text-muted">{icon('plus', 'w-5 h-5')}</span>
                        </button>
                    </h3>
                    <div class="faq-a pb-5 -mt-1 text-[15px] leading-relaxed text-muted max-w-2xl">{a}</div>
                </div>""" for q, a in C.FAQS)


def gallery():
    from PIL import Image
    tiles = []
    for i, k in enumerate(C.GALLERY):
        w, h = Image.open(os.path.join(OUT, f"{k}-sm.jpg")).size
        tiles.append(f"""                <button type="button" class="gallery-item group block w-full mb-4 break-inside-avoid overflow-hidden rounded reveal" style="--d:{i * 45}ms"
                        data-full="{ASSET_PREFIX}{k}.jpeg" data-full-webp="{ASSET_PREFIX}{k}.webp" data-caption="{C.PHOTOS[k]}">
                    <picture>
                        <source srcset="{ASSET_PREFIX}{k}-sm.webp" type="image/webp">
                        <img src="{ASSET_PREFIX}{k}-sm.jpg" width="{w}" height="{h}" alt="{C.PHOTOS[k]}"
                             class="block w-full h-auto transition-transform duration-500 group-hover:scale-[1.03]"
                             loading="lazy" decoding="async">
                    </picture>
                </button>""")
    return "\n".join(tiles)


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


def photo(key, *, cls, sizes, box=None, priority=False, caption=None):
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
    load = ('fetchpriority="high" decoding="async"' if priority
            else 'loading="lazy" decoding="async"')
    img = (f'<img src="{ASSET_PREFIX}{key}.jpeg" width="{w}" height="{h}" alt="{C.PHOTOS[key]}"\n'
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
    return f"""    <section aria-label="{C.PHOTOS[key]}" class="border-y border-line">
        <figure>
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
        <div class="max-w-6xl mx-auto px-5 sm:px-8 py-20 lg:py-28">
            <div class="max-w-xl">
                <h2 id="cta-h" class="text-d2 text-white">Four batches a day, Monday to Friday</h2>
                <p class="mt-4 text-[16px] leading-relaxed text-white/85">
                    Ladies, gents and children, in one hall in New Perungalathur. Most who
                    join have never done yoga before. Sit in on a batch on the 3-day trial
                    before deciding anything.
                </p>
                <div class="mt-7 flex flex-wrap gap-3">
                    <a href="{wa(TRIAL_MSG)}" target="_blank" rel="noopener"
                       class="inline-flex items-center px-5 py-3 bg-white text-ink font-medium rounded hover:bg-sand transition-colors">
                        Book a 3-day trial
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
    """Every post, two to a row. A list rather than a carousel: six headlines
    are read in a glance, where a slider would show two and hide the rest
    behind a wait - and the page already has one thing moving on its own."""
    posts = newest_first() if limit is None else newest_first()[:limit]
    rows = []
    for i, post in enumerate(posts):
        rows.append(f"""                <li class="border-t border-line reveal" style="--d:{min(i, 3) * 70}ms">
                    <a href="{post['slug']}" class="group block py-5 sm:pr-6">
                        <time datetime="{post['date']}" class="text-[13px] text-muted">{post['date_text']}</time>
                        <h3 class="mt-1.5 display text-d3 text-ink group-hover:text-blue transition-colors">{post['title']}</h3>
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
            C.person_node(),
            {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/",
             "name": "Happy Yogis Yoga Centre", "inLanguage": "en-IN",
             "publisher": {"@id": f"{BASE}/#business"}},
            {"@type": "WebPage", "@id": f"{BASE}/#webpage", "url": f"{BASE}/",
             "name": "Yoga Centre in Perungalathur & Tambaram | Happy Yogis",
             "isPartOf": {"@id": f"{BASE}/#website"},
             "about": {"@id": f"{BASE}/#business"}, "inLanguage": "en-IN"},
            {"@type": "FAQPage", "@id": f"{BASE}/#faq",
             "mainEntity": [{"@type": "Question", "name": q,
                             "acceptedAnswer": {"@type": "Answer", "text": a}}
                            for q, a in C.FAQS]},
        ],
    }

    h = head(title="Yoga Centre in Perungalathur & Tambaram | Happy Yogis",
             desc=("Yoga classes in New Perungalathur for ladies, gents and children. "
                   "Four batches daily, Mon-Fri, plus online classes. 3-day trial."),
             path="", schema=schema, preload="ima6.webp",
             # must match the hero <picture> exactly - if the preload and the
             # element resolve to different widths the browser fetches both
             preload_srcset=("ima6-xs.webp 320w, ima6-sm.webp 640w, "
                             "ima6-md.webp 768w, ima6.webp 1280w"),
             preload_sizes="100vw",
             alt=("ta", "ta/index.html"))

    filters, class_items = classes_section()
    chips, guides = areas_block()

    body = f"""<body class="font-body bg-paper text-ink text-[15px]">
{nav(home=True, alt_href="/ta/index.html")}
    <main id="main">

    <!-- Hero: serif headline and the class photograph on the left, the live
         schedule held to the right as a narrow column. Nothing here is marked
         .reveal - the first screen must never wait on a script. -->
    <!-- The opening screen is one photograph, edge to edge, carrying the
         headline and a single call to action. The timetable follows directly
         beneath it, where it can be read rather than competed with. Nothing
         here is marked .reveal - the first screen must never wait on a script. -->
    <section aria-labelledby="hero-h" class="bleed min-h-[78svh] flex items-end pt-16">
        <div class="bleed__img">
            {photo('ima6', cls='w-full h-full object-cover object-[center_38%]',
                   sizes='100vw', priority=True)}
        </div>
        <div class="bleed__foot" role="presentation"></div>

        <div class="bleed__in w-full max-w-6xl mx-auto px-5 sm:px-8 pb-14 lg:pb-20 pt-28 enter">
            <p class="lbl lbl--dark">SSM Nagar, New Perungalathur &middot; Chennai</p>
            <h1 id="hero-h" class="mt-4 text-d1 text-white max-w-[15ch]">
                Yoga classes in Perungalathur and Tambaram
            </h1>
            <p class="lede mt-6 text-white/85 max-w-xl">
                Four small batches a day, Monday to Friday, for ladies, gents and
                children. Most who join have never done yoga before; the practice is
                adjusted person by person.
            </p>
            <div class="mt-9">
                <a id="batch-cta" href="{wa(TRIAL_MSG)}" data-base="{wa(TRIAL_MSG)}"
                   target="_blank" rel="noopener"
                   class="inline-flex items-center px-8 py-4 bg-paper text-ink font-medium rounded text-[17px] hover:bg-white transition-colors">
                    Book a 3-day trial
                </a>
            </div>
        </div>
    </section>

    <section aria-label="Batch times" class="bg-paper" id="schedule">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 pt-14 lg:pt-20">
            <div class="grid lg:grid-cols-12 gap-10 lg:gap-14">
                <div class="lg:col-span-5">
                    <p class="lbl">One day at the centre</p>
                    <h2 class="mt-3 text-d2 text-ink">The room fills four times over</h2>
                    <p class="mt-5 text-[17px] leading-relaxed text-ink/75">
                        Each batch has its own character. Pick the hour that suits your
                        life &mdash; you can move between them when your week changes.
                    </p>
                    <div class="mt-7">
                        <a href="#classes" class="inline-flex items-center px-5 py-3 border border-line text-ink font-medium rounded hover:border-ink transition-colors">
                            See what we teach
                        </a>
                    </div>
                </div>

                <div class="lg:col-span-7">
                    <div class="border border-line rounded lift p-6 sm:p-7 bg-sand/60">
                        <div class="flex items-baseline justify-between gap-4">
                            <h3 class="display text-d4 text-ink">Today at the centre</h3>
                            <span class="text-[13px] text-muted">Mon&ndash;Fri</span>
                        </div>
                        <p id="next-class" class="mt-1.5 text-[13.5px] text-muted">Batches run Monday to Friday.</p>

                        <ul class="mt-5">
{batch_list()}
                        </ul>

                        <p class="mt-5 pt-4 border-t border-line text-[13px] leading-relaxed text-muted">
                            Every batch is warm-up, asanas, pranayama and relaxation.
                            Select a batch to see who it suits.
                        </p>
                    </div>
                </div>
            </div>

            <ul class="factline pb-14 lg:pb-20 pt-6 border-t border-line text-[15px] text-ink/80">
                <li>Four classes a day</li>
                <li>Monday to Friday</li>
                <li>Special care for women</li>
                <li>Online and in person</li>
            </ul>
        </div>
    </section>

    <!-- About -->
    <section id="about" aria-labelledby="about-h" class="py-16 lg:py-24">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-10 lg:gap-16">
            <div class="lg:col-span-4">
                <h2 id="about-h" class="text-d2 text-ink reveal">A neighbourhood centre, not a fitness chain</h2>
            </div>
            <div class="lg:col-span-8 space-y-4 text-[16px] leading-relaxed text-ink/80 max-w-2xl reveal" style="--d:90ms">
                <p>
                    Happy Yogis runs out of a hall in SSM Nagar, New Perungalathur. On any
                    morning, school children, people on their way to work, homemakers and
                    retired members share the mats. That mix is deliberate; it keeps the
                    room relaxed.
                </p>
                <p>
                    Batches are small enough that the teacher knows what each person is
                    working with &mdash; a bad knee, a desk job, a thyroid condition, a first
                    week of yoga &mdash; and the practice is adjusted around that.
                </p>
                <p class="display text-d3 text-ink pt-2">
                    It does not matter whether you can put your leg behind your head. It
                    matters that you turn up, breathe properly, and leave better than you
                    walked in.
                </p>
            </div>

            <div class="lg:col-span-12 reveal" style="--d:120ms">
                <div class="overflow-hidden rounded zoom grade">
                    {photo('ima4', cls='w-full h-[220px] sm:h-[300px] lg:h-[360px] object-cover object-[center_45%]',
                           sizes='(min-width:1024px) 1152px, 100vw')}
                </div>
                <p class="mt-2.5 text-[13px] text-muted">
                    A weekday morning batch &mdash; children and adults on the mats together.
                </p>
            </div>
        </div>
    </section>

    <!-- Classes -->
    <section id="classes" aria-labelledby="classes-h" class="py-16 lg:py-24 bg-sand border-y border-line">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <div class="lg:flex lg:items-end lg:justify-between lg:gap-10">
                <div class="max-w-xl reveal">
                    <h2 id="classes-h" class="text-d2 text-ink">What we teach</h2>
                    <p class="mt-3 text-[16px] leading-relaxed text-ink/75">
                        All of it is taught inside the regular batches; there is no separate
                        course to book. Tell us what you are working towards and the teacher
                        builds it in.
                    </p>
                </div>
                <div class="mt-6 lg:mt-0 flex flex-wrap gap-2" role="group" aria-label="Filter classes">
{filters}
                </div>
            </div>

            <p id="filter-status" class="sr-only" role="status" aria-live="polite"></p>
            <ul class="mt-10 border-b border-line">
{class_items}
            </ul>

            <div class="mt-10 grid grid-cols-3 gap-3 reveal">
                <div class="overflow-hidden rounded zoom grade">
                    {photo('ima8', cls='w-full h-[150px] sm:h-[230px] lg:h-[280px] object-cover',
                           sizes='(min-width:1024px) 370px, 33vw')}
                </div>
                <div class="overflow-hidden rounded zoom grade">
                    {photo('ima20', cls='w-full h-[150px] sm:h-[230px] lg:h-[280px] object-cover object-[center_40%]',
                           sizes='(min-width:1024px) 370px, 33vw')}
                </div>
                <div class="overflow-hidden rounded zoom grade">
                    {photo('ima25', cls='w-full h-[150px] sm:h-[230px] lg:h-[280px] object-cover object-[center_40%]',
                           sizes='(min-width:1024px) 370px, 33vw')}
                </div>
            </div>
        </div>
    </section>

    <!-- Yogi's Upadesha: newest posts, from the same list the section renders -->
    <section id="journal" aria-labelledby="journal-h" class="py-16 lg:py-24">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <div class="sm:flex sm:items-end sm:justify-between sm:gap-10">
                <div class="max-w-xl reveal">
                    <h2 id="journal-h" class="text-d2 text-ink">What people ask before they start</h2>
                    <p class="mt-3 text-[16px] leading-relaxed text-ink/75">
                        The questions we get on the phone, answered properly &mdash; what an
                        hour contains, who each batch suits, and what yoga does and does not
                        do.
                    </p>
                </div>
                <a href="blog.html"
                   class="mt-5 sm:mt-0 inline-flex shrink-0 items-center px-4 py-2.5 border border-line rounded lift text-[14px] font-medium text-ink hover:border-ink transition-colors">
                    All entries
                </a>
            </div>

            <ul class="mt-10 border-b border-line grid sm:grid-cols-2 sm:gap-x-12">
{journal_block()}
            </ul>
        </div>
    </section>

{band("ima15", f"{C.EVENT['name']} at {C.EVENT['place']}, {C.EVENT['date']} &mdash; a one-off. Regular batches are taught at the centre in SSM Nagar, New Perungalathur.")}
    <!-- Health -->
    <section id="health" aria-labelledby="health-h" class="py-16 lg:py-24">
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

    <!-- Teacher -->
    <section id="teacher" aria-labelledby="teacher-h" class="py-16 lg:py-24 bg-sand border-y border-line">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-10 lg:gap-16 items-center">
            <div class="lg:col-span-4 reveal">
                <div class="arch zoom grade grade--portrait w-full max-w-xs">
                    <picture>
                        <source type="image/webp"
                                srcset="instructor-portrait-xs.webp 300w, instructor-portrait-sm.webp 560w, instructor-portrait.webp 720w"
                                sizes="(min-width:1024px) 320px, 80vw">
                        <img src="instructor-portrait.jpeg" width="720" height="900"
                             alt="Karthika, yoga teacher at Happy Yogis Yoga Centre, New Perungalathur"
                             class="w-full aspect-[4/5] object-cover" loading="lazy" decoding="async">
                    </picture>
                </div>
            </div>
            <div class="lg:col-span-8 reveal" style="--d:90ms">
                <h2 id="teacher-h" class="text-d2 text-ink">Karthika</h2>
                <p class="mt-1 text-[14px] text-muted">Teaches every batch at the centre</p>
                <div class="mt-5 space-y-4 text-[16px] leading-relaxed text-ink/80 max-w-2xl">
                    <p>
                        Karthika has practised and taught yoga for more than ten years, and
                        takes every batch at the centre herself.
                    </p>
                    <p>
                        She meets people where they are. Beginners are not pushed into
                        postures they are not ready for, and anyone working around an injury
                        or a health condition gets the practice adapted rather than being
                        told to sit it out.
                    </p>
                </div>
                <a href="{wa('Hello Happy Yogis! I would like to book a 3-day trial with Karthika.')}"
                   target="_blank" rel="noopener"
                   class="mt-7 inline-flex items-center px-5 py-3 bg-ink text-white font-medium rounded hover:bg-blue transition-colors">
                    Book a 3-day trial
                </a>
            </div>
        </div>
    </section>

    <!-- Studio photos -->
    <section id="studio" aria-labelledby="studio-h" class="py-16 lg:py-24">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <div class="max-w-xl reveal">
                <h2 id="studio-h" class="text-d2 text-ink">Inside the centre</h2>
                <p class="mt-3 text-[16px] leading-relaxed text-ink/75">
                    Real batches, real students, photographed at the centre. Select any
                    photo to see it larger.
                </p>
            </div>
            <div class="mt-10 columns-2 lg:columns-3 xl:columns-4 gap-4">
{gallery()}
            </div>
        </div>
    </section>

    <!-- Reviews -->
    <section id="reviews" aria-labelledby="reviews-h" class="py-16 lg:py-24 bg-sand border-y border-line">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <h2 id="reviews-h" class="text-d2 text-ink reveal">What students say</h2>
            <div class="mt-4 reveal" style="--d:90ms">
{reviews_section()}
            </div>
        </div>
    </section>

{photo_cta("ima1")}
    <!-- Areas -->
    <section id="areas" aria-labelledby="areas-h" class="py-16 lg:py-24">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-10 lg:gap-16">
            <div class="lg:col-span-5 reveal">
                <h2 id="areas-h" class="text-d2 text-ink">One centre, in New Perungalathur</h2>
                <p class="mt-4 text-[16px] leading-relaxed text-ink/75">
                    One centre, in SSM Nagar &mdash; just off the GST Road stretch between
                    Tambaram and Vandalur, close to Perungalathur railway station. There are
                    no other branches. Students travel in from the neighbourhoods nearby,
                    and we teach online for anyone who cannot travel.
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

{band("ima13", f"The whole group at {C.EVENT['name']} &mdash; students, parents and teachers together.", h="h-[220px] sm:h-[300px] lg:h-[380px]")}
    <!-- Enquiry + visit -->
    <section id="visit" aria-labelledby="visit-h" class="py-16 lg:py-24 bg-sand border-y border-line">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-10 lg:gap-16">

            <div class="lg:col-span-6 reveal" id="enquire">
                <h2 id="visit-h" class="text-d2 text-ink">Book a 3-day trial</h2>
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
                <h2 class="text-d2 text-ink">Visit the centre</h2>

                <!-- bento: the map holds the wide tile, the three facts sit under it -->
                <div class="bento mt-6 sm:grid-cols-2">
                    <div class="sm:col-span-2 bg-paper">
                        <iframe title="Map showing Happy Yogis Yoga Centre, New Perungalathur"
                                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3887.8938068!2d80.1131382!3d12.8938068!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a5259bd7762301f%3A0xbb838e445fc93a!2sHAPPY%20YOGIS%20YOGA%20CENTRE!5e0!3m2!1sen!2sin!4v1234567890"
                                width="100%" height="280" style="border:0;display:block" allowfullscreen=""
                                loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                    </div>
                    <div class="sm:col-span-2 bg-paper p-6">
                        <p class="text-[13px] text-muted">Address</p>
                        <address class="mt-1.5 not-italic display text-d3 text-ink">SSM Nagar, New Perungalathur,<br>Chennai, Tamil Nadu 600063</address>
                        <a href="{MAPS}" target="_blank" rel="noopener"
                           class="mt-3 py-1 inline-flex items-center gap-1.5 text-[14px] font-medium text-blue hover:underline">
                            Get directions {icon('arrow-up-right', 'w-4 h-4')}
                        </a>
                    </div>
                    <div class="bg-paper p-6">
                        <p class="text-[13px] text-muted">Phone</p>
                        <a href="{PHONE_HREF}" class="mt-1.5 block display text-d3 text-ink hover:text-blue transition-colors">{PHONE_TEXT}</a>
                    </div>
                    <div class="bg-paper p-6">
                        <p class="text-[13px] text-muted">Open</p>
                        <p class="mt-1.5 text-[15px] leading-relaxed text-ink">{C.HOURS_TEXT}</p>
                        <p class="text-[14px] text-muted">{C.CLOSED_TEXT}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- FAQ -->
    <section id="faq" aria-labelledby="faq-h" class="py-16 lg:py-24">
        <div class="max-w-3xl mx-auto px-5 sm:px-8">
            <h2 id="faq-h" class="text-d2 text-ink reveal">Before you join</h2>
            <div class="mt-8 border-t border-line reveal" style="--d:90ms">
{faq_list()}
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
        "title": "Yoga Classes in Perungalathur, Chennai | Happy Yogis",
        "desc": ("Yoga centre in New Perungalathur, SSM Nagar. Four daily batches for "
                 "ladies, gents and children, Mon-Fri. 3-day trial available."),
        "h1": "Yoga classes in Perungalathur",
        "lede": ("Happy Yogis is a yoga centre in SSM Nagar, New Perungalathur &mdash; our "
                 "only location. If you live in Perungalathur, this is your local "
                 "class, not a drive across the city."),
        "body": [
            ("Where we are",
             "SSM Nagar, New Perungalathur, close to Perungalathur railway station and "
             "just off the GST Road stretch running down towards Vandalur. Students "
             "walk or ride in from New Perungalathur, Old Perungalathur and the "
             "streets around."),
            ("Who practises here",
             "Genuinely mixed &mdash; school children before class, people fitting a "
             "session in before the commute, women in the mid-morning ladies batch, "
             "retired members there for the joint mobility and the company. Most who "
             "join have never done yoga before."),
            ("What a class looks like",
             "Every batch: warm-up, asanas, pranayama and a closing relaxation, in 45 "
             "or 60 minutes. "
             "If you are working around a knee problem, back pain, PCOD or a thyroid "
             "condition, tell the teacher beforehand and the practice is adjusted for "
             "you."),
            ("Getting started",
             "Message us on WhatsApp for a 3-day trial in whichever batch has room. "
             "Bring a mat if you have one; once you join, you can leave it at the "
             "centre."),
        ],
        "photo": "ima1", "og": "og-perungalathur.jpg",
        "nearby": [("Yoga classes near Tambaram", "yoga-classes-tambaram.html")],
    },
    "yoga-classes-tambaram.html": {
        "area": "Tambaram",
        "title": "Yoga Classes near Tambaram, Chennai | Happy Yogis",
        "desc": ("Yoga centre a short run down GST Road from Tambaram, in New "
                 "Perungalathur. Morning and evening batches, ladies-only batch, "
                 "online classes."),
        "h1": "Yoga classes near Tambaram",
        "lede": ("Happy Yogis teaches from a single centre in New Perungalathur &mdash; "
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
             "Heading into the city afterwards, the 5:30 am and 6:15 am batches work "
             "best. The 5:00 pm batch is the popular one for school and college "
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
            <a href="{wa(f'Hello Happy Yogis! I am from {area} and would like to book a 3-day trial.')}"
               target="_blank" rel="noopener"
               class="inline-flex items-center px-5 py-3 bg-ink text-white font-medium rounded hover:bg-blue transition-colors">
                Book a 3-day trial
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
            <img src="{cfg['photo']}.jpeg" width="1280" height="960" alt="{C.PHOTOS[cfg['photo']]}"
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
            <div class="mt-6 text-[14px]">
                <p class="font-medium text-ink">Happy Yogis Yoga Centre</p>
                <address class="not-italic text-muted mt-1">SSM Nagar, New Perungalathur, Chennai 600063</address>
                <p class="text-muted mt-2">All classes are taught at this address &mdash; it is our only centre.</p>
                <a href="{MAPS}" target="_blank" rel="noopener"
                   class="mt-3 py-1 inline-flex items-center gap-1.5 font-medium text-blue hover:underline">
                    Get directions {icon('arrow-up-right', 'w-4 h-4')}
                </a>
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


if __name__ == "__main__":
    open(os.path.join(OUT, "index.html"), "w").write(build_index())
    print("index.html written")
    for slug, cfg in LOCATIONS.items():
        open(os.path.join(OUT, slug), "w").write(build_location(slug, cfg))
        print(f"{slug} written")
