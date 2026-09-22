#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds the Tamil pages into /ta/.

Only the three pages a search visitor lands on: the homepage and the two area
pages. The journal and the legal pages stay English, and hreflang says so
rather than leaving Google to guess.

Structure is shared with the English build - the same photo(), band() and
gallery() helpers, the same schedule data, the same batch times - so the two
cannot drift on facts. Only the prose differs, and it lives in ta_strings.
"""
import os
import html as _html

import build as B
import content as C
import pages as P
import ta_strings as T

OUT = os.path.join(B.OUT, "ta")


def wa(msg):
    return B.wa(msg)


TRIAL_MSG = "வணக்கம் Happy Yogis! 3 நாள் முயற்சி வகுப்பு பற்றி அறிய விரும்புகிறேன்."


# ------------------------------------------------------------------ chrome

def nav(home=False):
    """Delegates to the shared nav so the ids and classes the script binds to
    can never drift - a hand-copied nav is what broke the reveals here once."""
    return B.nav(
        home=home,
        words=dict(skip=T.SKIP, menu=T.MENU, open_menu=T.OPEN_MENU,
                   close_menu=T.CLOSE_MENU, trial=T.BOOK_TRIAL_SHORT,
                   trial_full=T.BOOK_TRIAL,
                   phone_cls="hidden xl:inline-flex"),
        links_data=T.NAV_LINKS,
        trial_msg=TRIAL_MSG,
        lang="ta",
        alt_href=("/" if home else PAGE_EN_ABS[CURRENT[0]]))


def footer():
    F = T.FOOTER
    cols = [
        (F["centre"], [("index.html#schedule", F["schedule"]),
                       ("index.html#classes", F["teach"]),
                       ("index.html#teacher", F["teacher"]),
                       ("index.html#studio", F["photos"])]),
        (F["areas"], [("yoga-classes-perungalathur.html", "பெருங்களத்தூர்"),
                      ("yoga-classes-tambaram.html", "தாம்பரம்"),
                      ("index.html#faq", F["questions"])]),
    ]
    blocks = "\n".join(f"""                <div>
                    <p class="text-[13px] font-medium text-white">{title}</p>
                    <ul class="mt-3 space-y-0.5">
{chr(10).join(f'                        <li><a href="{h}" class="inline-block py-1 text-[14px] hover:text-white transition-colors">{t}</a></li>' for h, t in items)}
                    </ul>
                </div>""" for title, items in cols)

    return f"""    <footer class="bg-ink text-white/65 mt-px">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 py-14 lg:py-16">
            <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10">
                <div class="lg:col-span-2">
                    <p class="display text-[19px] text-white">Happy Yogis Yoga Centre</p>
                    <p class="mt-3 text-[14px] leading-relaxed max-w-xs">{F["one_centre"]}</p>
                    <address class="mt-4 not-italic text-[14px] leading-relaxed">
                        SSM Nagar, New Perungalathur,<br>Chennai, Tamil Nadu 600063
                    </address>
                    <p class="mt-3 text-[14px]">
                        <a href="{B.PHONE_HREF}" class="inline-block py-1 hover:text-white transition-colors">{B.PHONE_TEXT}</a>
                    </p>
                    <p class="mt-4 text-[13.5px] leading-relaxed">{T.HOURS}<br>{T.CLOSED}</p>
                </div>
{blocks}
            </div>
            <div class="mt-12 pt-6 border-t border-white/15 flex flex-wrap items-center justify-between gap-4 text-[13px]">
                <p>&copy; 2026 Happy Yogis Yoga Centre</p>
                <p class="flex flex-wrap items-center gap-x-5 gap-y-2">
                    <a href="/privacy-policy.html" hreflang="en" lang="en" class="inline-block py-1 hover:text-white transition-colors">{F["privacy"]}</a>
                    <a href="/terms-of-service.html" hreflang="en" lang="en" class="inline-block py-1 hover:text-white transition-colors">{F["terms"]}</a>
                    <a href="{PAGE_EN_ABS[CURRENT[0]]}" hreflang="en" lang="en" class="inline-block py-1 hover:text-white transition-colors">{F["english"]}</a>
                </p>
            </div>
        </div>
    </footer>
"""


# --------------------------------------------------------------- fragments

def batch_list():
    rows = []
    for i, (t24, label, length, who, _note) in enumerate(C.BATCHES):
        plain = label.replace("&ndash;", "-")
        ta_who = T.LADIES_ONLY if who == "Ladies only" else T.EVERYONE
        mins = length.split()[0]
        rows.append(f"""                    <li>
                        <button type="button" class="batch group" data-start="{t24}" data-label="{plain}"
                                aria-expanded="false" aria-controls="batch-d{i}">
                            <span class="flex items-baseline justify-between gap-4">
                                <span class="display text-[17px] text-ink">{label}</span>
                                <span class="text-[13px] text-muted whitespace-nowrap">{mins} {T.MIN}</span>
                            </span>
                            <span class="mt-0.5 block text-[13px] {'text-blue font-medium' if who == 'Ladies only' else 'text-muted'}">{ta_who}</span>
                        </button>
                        <div id="batch-d{i}" class="batch-detail">
                            <p class="pb-4 text-[14px] leading-relaxed text-muted max-w-md">{T.BATCH_NOTES[i]}</p>
                        </div>
                    </li>""")
    return "\n".join(rows)


def classes_section():
    groups = [g for g, _ in T.CLASS_GROUPS]
    filters = [f'                    <button type="button" class="filter px-3 py-1.5 text-[13.5px] border border-line rounded lift-full text-ink transition-colors" data-group="all" aria-pressed="true">{T.EVERYTHING}</button>']
    for g in groups:
        filters.append(f'                    <button type="button" class="filter px-3 py-1.5 text-[13.5px] border border-line rounded lift-full text-ink transition-colors" data-group="{g}" aria-pressed="false">{g}</button>')
    items = []
    for g, entries in T.CLASS_GROUPS:
        for name, desc in entries:
            items.append(f"""                <li class="class-item border-t border-line py-6" data-group="{g}">
                    <div class="sm:flex sm:items-baseline sm:gap-8">
                        <h3 class="display text-d3 text-ink sm:w-64 sm:shrink-0">{name}</h3>
                        <p class="mt-1.5 sm:mt-0 text-[15px] leading-relaxed text-muted max-w-2xl">{desc}</p>
                    </div>
                </li>""")
    return "\n".join(filters), "\n".join(items)


def health_list():
    spans = ["lg:col-span-7", "lg:col-span-5", "lg:col-span-5",
             "lg:col-span-7", "lg:col-span-6", "lg:col-span-6"]
    out = []
    for i, (n, d) in enumerate(T.HEALTH):
        out.append(f"""                    <div class="{spans[i]} bg-paper p-6 sm:p-7 reveal" style="--d:{i * 60}ms">
                        <dt class="display text-d3 text-ink">{n}</dt>
                        <dd class="mt-2 text-[14.5px] leading-relaxed text-muted">{d}</dd>
                    </div>""")
    return "\n".join(out)


def faq_list():
    return "\n".join(f"""                <div class="faq-item border-b border-line">
                    <h3>
                        <button type="button" class="faq-q w-full flex items-start justify-between gap-6 py-5 text-left">
                            <span class="text-[16px] font-medium text-ink">{q}</span>
                            <span class="shrink-0 mt-0.5 text-muted">{B.icon('plus', 'w-5 h-5')}</span>
                        </button>
                    </h3>
                    <div class="faq-a pb-5 -mt-1 text-[15px] leading-relaxed text-muted max-w-2xl">{a}</div>
                </div>""" for q, a in T.FAQS)


def reviews_section():
    """The quotes stay exactly as their authors wrote them. Translating a
    review would put words in a named person's mouth that they never said, so
    only the framing around them is Tamil."""
    n = len(C.REVIEWS)
    slides = "\n".join(f"""                    <div class="rev-slide pr-4 flex" role="group" aria-roledescription="review" aria-label="Review {i} of {n}">
                        <figure class="flex-1 flex flex-col border border-line rounded lift p-6 sm:p-7 bg-paper">
                            <blockquote lang="en" class="clamp-2 display text-[19px] leading-[1.55] text-ink">&ldquo;{r['text']}&rdquo;</blockquote>
                            <a href="{C.REVIEWS_URL}" target="_blank" rel="noopener"
                               class="mt-3 py-1 inline-flex items-center text-[13px] font-medium text-blue hover:underline">
                                {T.READ_FULL_GOOGLE} {B.icon('arrow-up-right', 'w-3.5 h-3.5 inline-block align-[-1px] ml-1')}
                            </a>
                            <figcaption class="mt-auto pt-5 border-t border-line text-[13px] text-ink/70">
                                {r['name']} <span aria-hidden="true">&middot;</span> <span class="text-muted">{r['when']}</span>
                            </figcaption>
                        </figure>
                    </div>""" for i, r in enumerate(C.REVIEWS, 1))

    return f"""            <p class="text-[15px] leading-relaxed text-ink/75 max-w-2xl">
                Google-இல் 45-க்கும் மேற்பட்ட ஐந்து நட்சத்திர மதிப்புரைகள். {T.REVIEWS_INTRO_TAIL}
                <a href="{C.REVIEWS_URL}" target="_blank" rel="noopener"
                   class="font-medium text-blue hover:underline">{T.READ_ALL_GOOGLE} {B.icon('arrow-up-right', 'w-4 h-4 inline-block align-[-2px]')}</a>
            </p>
            <p class="mt-2 text-[13px] text-muted max-w-2xl">{T.REVIEWS_NOTE}</p>
            <div class="rev mt-8" data-rev>
                <div class="rev-track" role="region" aria-label="மாணவர் மதிப்புரைகள்" aria-live="off" tabindex="0">
{slides}
                </div>
                <div class="rev-controls mt-6 items-center gap-2">
                    <button type="button" class="rev-btn" data-rev-prev aria-label="Previous">{B.icon('chevron-left', 'w-5 h-5')}</button>
                    <button type="button" class="rev-btn" data-rev-next aria-label="Next">{B.icon('chevron-right', 'w-5 h-5')}</button>
                    <button type="button" class="rev-btn" data-rev-toggle aria-label="Pause">
                        <span data-rev-pause>{B.icon('pause', 'w-4 h-4')}</span>
                        <span data-rev-play hidden>{B.icon('play', 'w-4 h-4')}</span>
                    </button>
                    <div class="flex items-center gap-1.5 ml-2" data-rev-dots></div>
                </div>
            </div>"""


def areas_block():
    chips = "\n".join(
        f'                    <li class="px-3 py-1.5 border border-line rounded lift-full text-[13.5px] text-ink">{a}</li>'
        for a in C.AREAS)
    guides = "\n".join(f"""                <a href="{href}" class="group block border-t border-line py-6 transition-colors hover:bg-sand/60">
                    <span class="display text-d3 text-ink group-hover:text-blue transition-colors">{title}</span>
                    <span class="mt-1 block text-[14px] leading-relaxed text-muted max-w-md">{blurb}</span>
                </a>""" for title, href, blurb in [
        ("பெருங்களத்தூரில் யோகா வகுப்புகள்", "yoga-classes-perungalathur.html",
         "மையம் இந்தப் பகுதியில்தான். நாங்கள் எங்கே இருக்கிறோம், வகுப்பு எப்படி இருக்கும்."),
        ("தாம்பரம் அருகே யோகா வகுப்புகள்", "yoga-classes-tambaram.html",
         "தாம்பரம், செலையூரிலிருந்து வருவது எப்படி, எந்த வகுப்பு பொருத்தம்."),
    ])
    return chips, guides


def photo_cta(key):
    return f"""    <section aria-labelledby="cta-h" class="relative isolate border-y border-line overflow-hidden">
        <div class="absolute inset-0 -z-10">
            {P.photo(key, cls='w-full h-full object-cover object-[center_40%]', sizes='100vw')}
            <div class="absolute inset-0 bg-ink/70"></div>
        </div>
        <div class="max-w-6xl mx-auto px-5 sm:px-8 py-20 lg:py-28">
            <div class="max-w-xl">
                <h2 id="cta-h" class="text-d2 text-white">{T.CTA_H}</h2>
                <p class="mt-4 text-[16px] leading-relaxed text-white/85">{T.CTA_BODY}</p>
                <div class="mt-7 flex flex-wrap gap-3">
                    <a href="{wa(TRIAL_MSG)}" target="_blank" rel="noopener"
                       class="inline-flex items-center px-5 py-3 bg-white text-ink font-medium rounded hover:bg-sand transition-colors">
                        {T.BOOK_TRIAL}
                    </a>
                    <a href="#schedule"
                       class="inline-flex items-center px-5 py-3 border border-white/40 text-white font-medium rounded hover:border-white transition-colors">
                        {T.SEE_SCHEDULE}
                    </a>
                </div>
            </div>
        </div>
    </section>
"""


# ------------------------------------------------------------------ pages

PAGE_EN = {
    "ta/index.html": "",
    "ta/yoga-classes-perungalathur.html": "yoga-classes-perungalathur.html",
    "ta/yoga-classes-tambaram.html": "yoga-classes-tambaram.html",
}
PAGE_EN_ABS = {k: "/" + v for k, v in PAGE_EN.items()}
CURRENT = ["ta/index.html"]


def schema_for(path, title, desc):
    en = PAGE_EN[path]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": f"{B.BASE}/{path}",
             "url": f"{B.BASE}/{path}", "name": title, "description": desc,
             "inLanguage": "ta-IN",
             "isPartOf": {"@id": f"{B.BASE}/#website"},
             "about": {"@id": f"{B.BASE}/#business"},
             "translationOfWork": {"@id": f"{B.BASE}/{en}" if en else f"{B.BASE}/"}},
        ],
    }


def build_index():
    CURRENT[0] = "ta/index.html"
    meta = T.META["index"]
    chips, guides = areas_block()
    filters, items = classes_section()

    h = B.head(title=meta["title"], desc=meta["desc"], path="ta/index.html",
               schema=schema_for("ta/index.html", meta["title"], meta["desc"]),
               preload="/ima6.webp",
               preload_srcset=("/ima6-xs.webp 320w, /ima6-sm.webp 640w, "
                               "/ima6-md.webp 768w, /ima6.webp 1280w"),
               preload_sizes="100vw",
               lang="ta", alt=("en", ""), pre_path="/")

    body = f"""<body class="font-body bg-paper text-ink text-[15px]">
{nav(home=True)}
    <main id="main">

    <!-- Same opening as the English page: one photograph edge to edge with
         the headline and a single call to action, the timetable directly under it. -->
    <section aria-labelledby="hero-h" class="bleed min-h-[78svh] flex items-end pt-16">
        <div class="bleed__img">
            {P.photo('ima6', cls='w-full h-full object-cover object-[center_38%]', sizes='100vw', priority=True)}
        </div>
        <div class="bleed__wash" role="presentation"></div>
        <div class="bleed__foot" role="presentation"></div>

        <div class="bleed__in w-full max-w-6xl mx-auto px-5 sm:px-8 pb-14 lg:pb-20 pt-28 enter">
            <p class="lbl lbl--dark">{T.EYEBROW}</p>
            <h1 id="hero-h" class="mt-4 text-d1 text-white max-w-[15ch]">{T.H1}</h1>
            <p class="lede mt-6 text-white/85 max-w-xl">{T.LEDE}</p>
            <div class="mt-9">
                <a id="batch-cta" href="{wa(TRIAL_MSG)}" data-base="{wa(TRIAL_MSG)}"
                   target="_blank" rel="noopener"
                   class="inline-flex items-center px-8 py-4 bg-paper text-ink font-medium rounded text-[17px] hover:bg-white transition-colors">
                    {T.BOOK_TRIAL}
                </a>
            </div>
        </div>
    </section>

    <section aria-label="{T.TODAY}" class="bg-paper" id="schedule">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 pt-14 lg:pt-20">
            <div class="grid lg:grid-cols-12 gap-10 lg:gap-14">
                <div class="lg:col-span-5">
                    <p class="lbl">{T.SCHEDULE_LBL}</p>
                    <h2 class="mt-3 text-d2 text-ink">{T.SCHEDULE_H}</h2>
                    <p class="mt-5 text-[17px] leading-relaxed text-ink/75">{T.SCHEDULE_LEDE}</p>
                    <div class="mt-7">
                        <a href="#classes" class="inline-flex items-center px-5 py-3 border border-line text-ink font-medium rounded hover:border-ink transition-colors">
                            {T.SEE_CLASSES}
                        </a>
                    </div>
                </div>

                <div class="lg:col-span-7">
                    <div class="border border-line rounded lift p-6 sm:p-7 bg-sand/60">
                        <div class="flex items-baseline justify-between gap-4">
                            <h3 class="display text-d4 text-ink">{T.TODAY}</h3>
                            <span class="text-[13px] text-muted">{T.MON_FRI}</span>
                        </div>
                        <p id="next-class" class="mt-1.5 text-[13.5px] text-muted">{T.RUNS_MON_FRI}</p>
                        <ul class="mt-5">
{batch_list()}
                        </ul>
                        <p class="mt-5 pt-4 border-t border-line text-[13px] leading-relaxed text-muted">{T.BATCH_NOTE}</p>
                    </div>
                </div>
            </div>

            <ul class="factline pb-14 lg:pb-20 pt-6 border-t border-line text-[15px] text-ink/80">
{chr(10).join(f'                <li>{x}</li>' for x in T.FACTLINE)}
            </ul>
        </div>
    </section>

    <!-- About -->
    <section id="about" aria-labelledby="about-h" class="py-16 lg:py-24">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-10 lg:gap-16">
            <div class="lg:col-span-4">
                <h2 id="about-h" class="text-d2 text-ink reveal">{T.ABOUT_H}</h2>
            </div>
            <div class="lg:col-span-8 space-y-4 text-[16px] leading-relaxed text-ink/80 max-w-2xl reveal" style="--d:90ms">
{chr(10).join(f'                <p>{x}</p>' for x in T.ABOUT)}
                <p class="display text-d3 text-ink pt-2">{T.ABOUT_PULL}</p>
            </div>
            <div class="lg:col-span-12 reveal" style="--d:120ms">
                <div class="overflow-hidden rounded zoom grade">
                    {P.photo('ima4', cls='w-full h-[220px] sm:h-[300px] lg:h-[360px] object-cover object-[center_45%]', sizes='(min-width:1024px) 1152px, 100vw')}
                </div>
                <p class="mt-2.5 text-[13px] text-muted">{T.ABOUT_CAPTION}</p>
            </div>
        </div>
    </section>

    <!-- Classes -->
    <section id="classes" aria-labelledby="classes-h" class="py-16 lg:py-24 bg-sand border-y border-line">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <div class="lg:flex lg:items-end lg:justify-between lg:gap-10">
                <div class="max-w-xl reveal">
                    <h2 id="classes-h" class="text-d2 text-ink">{T.CLASSES_H}</h2>
                    <p class="mt-3 text-[16px] leading-relaxed text-ink/75">{T.CLASSES_INTRO}</p>
                </div>
                <div class="mt-6 lg:mt-0 flex flex-wrap gap-2 reveal" style="--d:60ms">
{filters}
                </div>
            </div>
            <ul class="mt-10 border-b border-line">
{items}
            </ul>
        </div>
    </section>

{P.band("ima15", "சர்வதேச யோகா தினம் 2026, சென்னை புளூ ஃபிளாக் கடற்கரை, 12 ஜூன் 2026 &mdash; ஒரு நாள் நிகழ்வு. வழக்கமான வகுப்புகள் எஸ்.எஸ்.எம். நகர், புதிய பெருங்களத்தூர் மையத்தில் நடைபெறுகின்றன.")}
    <!-- Health -->
    <section id="health" aria-labelledby="health-h" class="py-16 lg:py-24">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-10 lg:gap-16">
            <div class="lg:col-span-4 reveal">
                <h2 id="health-h" class="text-d2 text-ink">{T.HEALTH_H}</h2>
                <p class="mt-4 text-[16px] leading-relaxed text-ink/75">{T.HEALTH_INTRO}</p>
                <p class="mt-4 text-[13.5px] leading-relaxed text-muted">{T.HEALTH_DISCLAIMER}</p>
            </div>
            <div class="lg:col-span-8">
                <dl class="bento bento-open-b sm:grid-cols-2 lg:grid-cols-12">
{health_list()}
                </dl>
                <div class="bento-foot bg-paper">
                    {P.photo('ima5', cls='w-full h-[230px] sm:h-[280px] object-cover object-[center_45%] block', sizes='(min-width:1024px) 768px, 100vw')}
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
                                srcset="/instructor-portrait-xs.webp 300w, /instructor-portrait-sm.webp 560w, /instructor-portrait.webp 720w"
                                sizes="(min-width:1024px) 320px, 80vw">
                        <img src="/instructor-portrait.jpeg" width="720" height="900"
                             alt="கார்த்திகா, Happy Yogis யோகா மையத்தின் ஆசிரியர், புதிய பெருங்களத்தூர்"
                             class="w-full aspect-[4/5] object-cover" loading="lazy" decoding="async">
                    </picture>
                </div>
            </div>
            <div class="lg:col-span-8 reveal" style="--d:90ms">
                <h2 id="teacher-h" class="text-d2 text-ink">கார்த்திகா</h2>
                <p class="mt-1 text-[14px] text-muted">{T.TEACHER_ROLE}</p>
                <div class="mt-5 space-y-4 text-[16px] leading-relaxed text-ink/80 max-w-2xl">
{chr(10).join(f'                    <p>{x}</p>' for x in T.TEACHER)}
                </div>
                <a href="{wa(TRIAL_MSG)}" target="_blank" rel="noopener"
                   class="mt-7 inline-flex items-center px-5 py-3 bg-ink text-white font-medium rounded hover:bg-blue transition-colors">
                    {T.BOOK_TRIAL}
                </a>
            </div>
        </div>
    </section>

    <!-- Studio -->
    <section id="studio" aria-labelledby="studio-h" class="py-16 lg:py-24">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <div class="max-w-xl reveal">
                <h2 id="studio-h" class="text-d2 text-ink">{T.STUDIO_H}</h2>
                <p class="mt-3 text-[16px] leading-relaxed text-ink/75">{T.STUDIO_INTRO}</p>
            </div>
            <div class="mt-10 columns-2 lg:columns-3 xl:columns-4 gap-4">
{P.gallery()}
            </div>
        </div>
    </section>

    <!-- Reviews -->
    <section id="reviews" aria-labelledby="reviews-h" class="py-16 lg:py-24 bg-sand border-y border-line">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <h2 id="reviews-h" class="text-d2 text-ink reveal">{T.REVIEWS_H}</h2>
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
                <h2 id="areas-h" class="text-d2 text-ink">{T.AREAS_H}</h2>
                <p class="mt-4 text-[16px] leading-relaxed text-ink/75">{T.AREAS_INTRO}</p>
                <h3 class="mt-8 text-[13.5px] font-medium text-ink">{T.AREAS_FROM}</h3>
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

    <!-- Visit -->
    <section id="visit" aria-labelledby="visit-h" class="py-16 lg:py-24 bg-sand border-y border-line">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 grid lg:grid-cols-12 gap-10 lg:gap-16">
            <div class="lg:col-span-6 reveal" id="enquire">
                <h2 id="visit-h" class="text-d2 text-ink">{T.VISIT_H}</h2>
                <p class="mt-3 text-[16px] leading-relaxed text-ink/75 max-w-lg">{T.VISIT_INTRO}</p>
                <form id="enquiry-form" class="mt-7 space-y-4 max-w-lg" novalidate>
                    <div>
                        <label for="f-name" class="block text-[13.5px] font-medium text-ink">{T.FORM["name"]}</label>
                        <input type="text" id="f-name" name="name" autocomplete="name"
                               class="mt-1.5 w-full px-3.5 py-2.5 bg-paper border border-line rounded lift text-[16px] text-ink placeholder:text-muted">
                    </div>
                    <div>
                        <label for="f-phone" class="block text-[13.5px] font-medium text-ink">{T.FORM["phone"]}</label>
                        <input type="tel" id="f-phone" name="phone" autocomplete="tel"
                               class="mt-1.5 w-full px-3.5 py-2.5 bg-paper border border-line rounded lift text-[16px] text-ink placeholder:text-muted">
                    </div>
                    <div>
                        <label for="f-batch" class="block text-[13.5px] font-medium text-ink">{T.FORM["batch"]}</label>
                        <select id="f-batch" name="batch"
                                class="mt-1.5 w-full px-3.5 py-2.5 bg-paper border border-line rounded lift text-[16px] text-ink">
                            <option value="">{T.FORM["batch_any"]}</option>
{chr(10).join(f'                            <option>{lbl.replace("&ndash;", "-")}</option>' for _t, lbl, _l, _w, _n in C.BATCHES)}
                        </select>
                    </div>
                    <div>
                        <label for="f-goal" class="block text-[13.5px] font-medium text-ink">{T.FORM["goal"]}</label>
                        <input type="text" id="f-goal" name="goal" placeholder="{T.FORM['goal_ph']}"
                               class="mt-1.5 w-full px-3.5 py-2.5 bg-paper border border-line rounded lift text-[16px] text-ink placeholder:text-muted">
                    </div>
                    <div>
                        <label for="f-msg" class="block text-[13.5px] font-medium text-ink">{T.FORM["message"]}</label>
                        <textarea id="f-msg" name="message" rows="3" placeholder="{T.FORM['message_ph']}"
                                  class="mt-1.5 w-full px-3.5 py-2.5 bg-paper border border-line rounded lift text-[16px] text-ink placeholder:text-muted"></textarea>
                        <p class="mt-1.5 text-[12.5px] leading-relaxed text-muted">{T.FORM["privacy"]}</p>
                    </div>
                    <button type="submit"
                            class="inline-flex items-center gap-2 px-5 py-3 bg-[#17843F] text-white font-medium rounded hover:bg-[#126B33] transition-colors">
                        {B.icon('message-circle', 'w-4 h-4')}{T.FORM["submit"]}
                    </button>
                    <p id="form-note" hidden role="status"
                       class="text-[13.5px] leading-relaxed text-ink bg-paper border border-line rounded lift px-4 py-3">
                        {T.FORM["note"]} <a href="{B.PHONE_HREF}" class="underline">{B.PHONE_TEXT}</a>.
                    </p>
                </form>
            </div>

            <div class="lg:col-span-6 reveal" style="--d:90ms">
                <h2 class="text-d2 text-ink">{T.VISIT_CENTRE}</h2>
                <div class="bento mt-6 sm:grid-cols-2">
                    <div class="sm:col-span-2 bg-paper">
                        <iframe title="Happy Yogis Yoga Centre, New Perungalathur"
                                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3887.8938068!2d80.1131382!3d12.8938068!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a5259bd7762301f%3A0xbb838e445fc93a!2sHAPPY%20YOGIS%20YOGA%20CENTRE!5e0!3m2!1sen!2sin!4v1234567890"
                                width="100%" height="280" style="border:0;display:block" allowfullscreen=""
                                loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                    </div>
                    <div class="sm:col-span-2 bg-paper p-6">
                        <p class="text-[13px] text-muted">{T.ADDRESS_L}</p>
                        <address class="mt-1.5 not-italic display text-d3 text-ink" lang="en">SSM Nagar, New Perungalathur,<br>Chennai, Tamil Nadu 600063</address>
                        <a href="{B.MAPS}" target="_blank" rel="noopener"
                           class="mt-3 py-1 inline-flex items-center gap-1.5 text-[14px] font-medium text-blue hover:underline">
                            {T.DIRECTIONS} {B.icon('arrow-up-right', 'w-4 h-4')}
                        </a>
                    </div>
                    <div class="bg-paper p-6">
                        <p class="text-[13px] text-muted">{T.PHONE_L}</p>
                        <a href="{B.PHONE_HREF}" class="mt-1.5 block display text-d3 text-ink hover:text-blue transition-colors">{B.PHONE_TEXT}</a>
                    </div>
                    <div class="bg-paper p-6">
                        <p class="text-[13px] text-muted">{T.OPEN_L}</p>
                        <p class="mt-1.5 text-[15px] leading-relaxed text-ink">{T.HOURS}</p>
                        <p class="text-[14px] text-muted">{T.CLOSED}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- FAQ -->
    <section id="faq" aria-labelledby="faq-h" class="py-16 lg:py-24">
        <div class="max-w-3xl mx-auto px-5 sm:px-8">
            <h2 id="faq-h" class="text-d2 text-ink reveal">{T.FAQ_H}</h2>
            <div class="mt-8 border-t border-line reveal" style="--d:90ms">
{faq_list()}
            </div>
        </div>
    </section>

    </main>

{footer()}
{P.LIGHTBOX}
{B.SCRIPT}"""
    return h + body


def build_location(slug, cfg):
    path = f"ta/{slug}"
    CURRENT[0] = path
    body_html = "\n".join(f"""            <h2 class="mt-10 text-d2 text-ink reveal">{t}</h2>
            <p class="mt-3 text-[16px] leading-relaxed text-ink/80">{p}</p>""" for t, p in cfg["body"])

    h = B.head(title=cfg["title"], desc=cfg["desc"], path=path,
               schema=schema_for(path, cfg["title"], cfg["desc"]),
               og_img=cfg["og"], lang="ta", alt=("en", PAGE_EN[path]), pre_path="/")

    body = f"""<body class="font-body bg-paper text-ink text-[15px]">
{nav()}
    <main id="main">
    <article class="max-w-3xl mx-auto px-5 sm:px-8 pt-32 pb-20">
        <nav aria-label="Breadcrumb" class="text-[13px] text-muted">
            <a href="index.html" class="inline-block py-1 hover:text-ink transition-colors">Happy Yogis</a>
            <span aria-hidden="true"> / </span>{cfg["h1"]}
        </nav>
        <h1 class="mt-4 text-d1 text-ink">{cfg["h1"]}</h1>
        <p class="mt-5 text-[17px] leading-relaxed text-ink/80">{cfg["lede"]}</p>

        <div class="mt-10 overflow-hidden rounded reveal grade">
            {P.photo(cfg["photo"], cls='w-full h-[240px] sm:h-[340px] object-cover', sizes='(min-width:768px) 768px, 100vw')}
        </div>

{body_html}

        <div class="mt-12 border border-line rounded lift p-6 sm:p-8 bg-sand/60 reveal">
            <h2 class="display text-d3 text-ink">{T.VISIT_H}</h2>
            <p class="mt-2 text-[15px] leading-relaxed text-ink/75">{T.VISIT_INTRO}</p>
            <div class="mt-5 flex flex-wrap gap-3">
                <a href="{wa(TRIAL_MSG)}" target="_blank" rel="noopener"
                   class="inline-flex items-center gap-2 px-5 py-3 bg-[#17843F] text-white font-medium rounded hover:bg-[#126B33] transition-colors">
                    {B.icon('message-circle', 'w-4 h-4')}WhatsApp
                </a>
                <a href="{B.PHONE_HREF}" class="inline-flex items-center px-5 py-3 border border-line rounded lift text-ink font-medium hover:border-ink transition-colors">
                    {B.PHONE_TEXT}
                </a>
            </div>
        </div>

        <div class="mt-10 border-t border-line pt-5">
            <h2 class="text-[13.5px] font-medium text-ink">{T.NEARBY}</h2>
{chr(10).join(f'''            <a href="{h2}" class="group mt-3 block">
                <span class="display text-d3 text-ink group-hover:text-blue transition-colors">{t2}</span>
            </a>''' for t2, h2 in cfg["nearby"])}
        </div>
    </article>
    </main>

{footer()}
{B.SCRIPT}"""
    return h + body


LOCATIONS = {
    "yoga-classes-perungalathur.html": dict(
        T.META["perungalathur"], photo="ima1", og="og-perungalathur.jpg",
        nearby=[("தாம்பரம் அருகே யோகா வகுப்புகள்", "yoga-classes-tambaram.html")]),
    "yoga-classes-tambaram.html": dict(
        T.META["tambaram"], photo="ima6", og="og-tambaram.jpg",
        nearby=[("பெருங்களத்தூரில் யோகா வகுப்புகள்", "yoga-classes-perungalathur.html")]),
}


# ------------------------------------------------------------ Tamil journal

import ta_posts as TP
import blog as BL


def _ta_body(sections):
    """Render a Tamil post body. A section is (heading, content) where content
    is a list of paragraphs, or a dict carrying bullets / qa / a trailing
    paragraph. Citations are placeholders so the same source list serves both
    languages - the URL does not change because the prose did."""
    cites = {
        "{cite_who}": BL.cite("who_pa", "WHO உடல் செயல்பாட்டு வழிகாட்டுதல்"),
        "{cite_pain}": BL.cite("nccih_pain", "வலிக்கான யோகா குறித்து NCCIH"),
    }

    def fill(t):
        for k, v in cites.items():
            t = t.replace(k, v)
        return t

    out = []
    for heading, content in sections:
        out.append(f'            <h2 class="text-d2 text-ink mt-12">{heading}</h2>')
        if isinstance(content, list):
            out.append(BL.para(*[fill(x) for x in content]))
        else:
            if content.get("bullets"):
                out.append(BL.bullets(*[fill(x) for x in content["bullets"]]))
            if content.get("qa"):
                out.append(BL.qa([(fill(q), fill(a)) for q, a in content["qa"]]))
            if content.get("after"):
                out.append(BL.para(fill(content["after"])))
    return "\n".join(out)


def build_post(p):
    path = f"ta/{p['slug']}"
    CURRENT[0] = path
    PAGE_EN[path] = p["slug"]
    PAGE_EN_ABS[path] = "/" + p["slug"]

    pts = "\n".join(f"                    <li>{t}</li>" for t in p["short"])
    w, h = BL.dims(p["photo"])

    schema = {
        "@context": "https://schema.org",
        "@graph": [{
            "@type": "BlogPosting", "@id": f"{B.BASE}/{path}",
            "headline": p["title"], "description": p["meta"],
            "inLanguage": "ta-IN", "datePublished": p["date"],
            "image": f"{B.BASE}/{p['photo']}.jpeg",
            "author": {"@type": "Organization", "name": "Happy Yogis Yoga Centre"},
            "publisher": {"@id": f"{B.BASE}/#business"},
            "translationOfWork": {"@id": f"{B.BASE}/{p['slug']}"},
            "mainEntityOfPage": {"@id": f"{B.BASE}/{path}"},
        }],
    }

    head = B.head(title=f"{p['title']} | Happy Yogis", desc=p["meta"], path=path,
                  schema=schema, lang="ta", alt=("en", p["slug"]), pre_path="/")

    body = f"""<body class="font-body bg-paper text-ink text-[15px]">
{nav()}
    <main id="main">
    <article class="max-w-3xl mx-auto px-5 sm:px-8 pt-32 pb-20">
        <nav aria-label="Breadcrumb" class="text-[13px] text-muted">
            <a href="blog.html" class="inline-block py-1 hover:text-ink transition-colors">யோகியின் உபதேசம்</a>
            <span aria-hidden="true"> / </span>{p["date_text"]}
        </nav>
        <h1 class="mt-4 text-d1 text-ink">{p["title"]}</h1>
        <p class="mt-5 text-[17px] leading-relaxed text-ink/80">{p["standfirst"]}</p>
        <aside class="mt-8 border-l-2 border-line pl-5" aria-label="சுருக்கமாக">
            <p class="text-[13px] font-medium text-ink">சுருக்கமாக</p>
            <ul class="mt-2 space-y-1.5 text-[15px] leading-relaxed text-ink/75 list-disc pl-5 marker:text-muted">
{pts}
            </ul>
        </aside>

        <figure class="mt-8">
            <div class="rounded zoom grade">
            <picture>
                <source type="image/webp" sizes="(min-width:768px) 720px, 92vw"
                        srcset="/{p['photo']}-xs.webp 320w, /{p['photo']}-sm.webp 640w, /{p['photo']}-md.webp 768w, /{p['photo']}.webp {w}w">
                <source type="image/jpeg" sizes="(min-width:768px) 720px, 92vw"
                        srcset="/{p['photo']}-xs.jpg 320w, /{p['photo']}-sm.jpg 640w, /{p['photo']}-md.jpg 768w, /{p['photo']}.jpeg {w}w">
                <img src="/{p['photo']}.jpeg" width="{w}" height="{h}" alt="{C.PHOTOS[p['photo']]}"
                     class="w-full rounded" loading="lazy" decoding="async">
            </picture>
            </div>
        </figure>

{_ta_body(p["body"])}

        <aside class="mt-12 border border-line rounded lift p-5 sm:p-6 bg-sand/60 text-[13.5px] leading-relaxed text-muted">
            {TP.DISCLAIMER_TA}
        </aside>

        <div class="mt-10 border border-line rounded lift p-6 sm:p-8 bg-sand/60">
            <h2 class="display text-d3 text-ink">{T.VISIT_H}</h2>
            <p class="mt-2 text-[15px] leading-relaxed text-ink/75">{T.VISIT_INTRO}</p>
            <div class="mt-5 flex flex-wrap gap-3">
                <a href="{wa(TRIAL_MSG)}" target="_blank" rel="noopener"
                   class="inline-flex items-center gap-2 px-5 py-3 bg-[#17843F] text-white font-medium rounded hover:bg-[#126B33] transition-colors">
                    {B.icon('message-circle', 'w-4 h-4')}WhatsApp
                </a>
                <a href="{B.PHONE_HREF}" class="inline-flex items-center px-5 py-3 border border-line rounded lift text-ink font-medium hover:border-ink transition-colors">
                    {B.PHONE_TEXT}
                </a>
            </div>
        </div>
    </article>
    </main>

{footer()}
{B.SCRIPT}"""
    return head + body


def build_blog_index():
    path = "ta/blog.html"
    CURRENT[0] = path
    PAGE_EN[path] = "blog.html"
    PAGE_EN_ABS[path] = "/blog.html"
    I = TP.INDEX

    rows = "\n".join(f"""                <li class="border-t border-line reveal" style="--d:{min(i, 3) * 70}ms">
                    <a href="{p['slug']}" class="group block py-6 sm:pr-6">
                        <time datetime="{p['date']}" class="text-[13px] text-muted">{p['date_text']}</time>
                        <h2 class="mt-1.5 display text-d3 text-ink group-hover:text-blue transition-colors">{p['title']}</h2>
                        <p class="mt-1.5 text-[15px] leading-relaxed text-muted max-w-2xl">{p['standfirst']}</p>
                    </a>
                </li>""" for i, p in enumerate(sorted(TP.POSTS, key=lambda x: x["date"], reverse=True)))

    schema = {
        "@context": "https://schema.org",
        "@graph": [{"@type": "Blog", "@id": f"{B.BASE}/{path}",
                    "name": I["h1"], "description": I["desc"],
                    "inLanguage": "ta-IN",
                    "publisher": {"@id": f"{B.BASE}/#business"},
                    "translationOfWork": {"@id": f"{B.BASE}/blog.html"}}],
    }

    head = B.head(title=I["title"], desc=I["desc"], path=path, schema=schema,
                  lang="ta", alt=("en", "blog.html"), pre_path="/")

    body = f"""<body class="font-body bg-paper text-ink text-[15px]">
{nav()}
    <main id="main">
    <section class="max-w-4xl mx-auto px-5 sm:px-8 pt-32 pb-20">
        <h1 class="text-d1 text-ink">{I["h1"]}</h1>
        <p class="mt-5 text-[17px] leading-relaxed text-ink/80 max-w-2xl">{I["lede"]}</p>
        <p class="mt-3 text-[14px] leading-relaxed text-muted max-w-2xl">{TP.ONLY_FOUR}</p>
        <ul class="mt-10 border-b border-line">
{rows}
        </ul>
    </section>
    </main>

{footer()}
{B.SCRIPT}"""
    return head + body


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    P.ASSET_PREFIX = "/"
    try:
        open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(build_index())
        print("ta/index.html written")
        for slug, cfg in LOCATIONS.items():
            open(os.path.join(OUT, slug), "w", encoding="utf-8").write(build_location(slug, cfg))
            print(f"ta/{slug} written")
        open(os.path.join(OUT, "blog.html"), "w", encoding="utf-8").write(build_blog_index())
        print("ta/blog.html written")
        for post in TP.POSTS:
            open(os.path.join(OUT, post["slug"]), "w", encoding="utf-8").write(build_post(post))
            print(f"ta/{post['slug']} written")
    finally:
        P.ASSET_PREFIX = ""
