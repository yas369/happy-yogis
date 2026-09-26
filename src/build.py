#!/usr/bin/env python3
"""Shared shell for the Happy Yogis site: head, nav, footer, CSS, JS.

Design decisions taken deliberately, after checking against the generic
AI-design tells the brief lists:
  - no tracked-out all-caps eyebrow labels (the old .kicker is gone)
  - no shadows anywhere; surfaces separate by 1px rules and ground colour
  - no arrows appended to buttons; only on links that leave the site
  - no numbered markers
Motion: one page-load moment (the next-class panel resolving). Everything
else responds to a real user action.
"""
import os
import json
from urllib.parse import quote

# The site root, derived from this file's location so a clone works
# wherever it sits. HAPPY_YOGIS_ROOT overrides it if ever needed.
OUT = os.environ.get("HAPPY_YOGIS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://happyyogis.in"
WA = "https://wa.me/919994247450"
PHONE_HREF = "tel:+919994247450"
PHONE_TEXT = "+91 99942 47450"
MAPS = ("https://www.google.com/maps/search/?api=1"
        "&query=SSM+Nagar+New+Perungalathur+Chennai")

# One family: DM Sans carries every heading, the wordmark, body copy and UI.
# Headings are set at 500 - enough to hold the hierarchy without shouting, with
# the scale still doing most of the work.
#
# Self-hosted rather than pulled from Google. Fetching it from there costs two
# DNS lookups and two TLS handshakes in series - the stylesheet has to arrive
# before the browser even learns the font URL - and if either host is
# unreachable every heading silently falls back. On the origin it is one
# already-connected request, preloaded alongside the HTML.
#
# DM Sans v17 is a variable font, so one file serves 400-600 through the weight
# axis; that is why a single src covers every weight the site uses. The
# unicode-range split is Google's own: only the latin file is fetched today, and
# latin-ext waits unused until a page needs something like a rupee sign.
FONT_FACE = """
        @font-face {
            font-family: 'DM Sans';
            font-style: normal;
            font-weight: 400 600;
            font-display: swap;
            src: url(/dm-sans-latin.woff2) format('woff2');
            unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6,
                U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC,
                U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
        }
        @font-face {
            font-family: 'DM Sans';
            font-style: normal;
            font-weight: 400 600;
            font-display: swap;
            src: url(/dm-sans-latin-ext.woff2) format('woff2');
            unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7,
                U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F,
                U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113,
                U+2C60-2C7F, U+A720-A7FF;
        }
        /* Cormorant Garamond carries the display type - headings, the wordmark
           and the italic labels. It is subset to ASCII plus the typographic
           punctuation the site actually sets, which took the pair from 77 KB
           to 36 KB; it never sets body copy, so it needs nothing more. Same
           posture as DM Sans: self-hosted, preloaded, no third-party request
           and no stylesheet standing between the browser and the font. */
        @font-face {
            font-family: 'Cormorant Garamond';
            font-style: normal;
            font-weight: 300 600;
            font-display: swap;
            src: url(/cormorant.woff2) format('woff2');
            unicode-range: U+0020-007E, U+00A0, U+00B7, U+2013-2014,
                U+2018-2019, U+201C-201D, U+2026, U+20B9;
        }
        @font-face {
            font-family: 'Cormorant Garamond';
            font-style: italic;
            font-weight: 300 500;
            font-display: swap;
            src: url(/cormorant-italic.woff2) format('woff2');
            unicode-range: U+0020-007E, U+00A0, U+00B7, U+2013-2014,
                U+2018-2019, U+201C-201D, U+2026, U+20B9;
        }
"""


def wa(msg):
    return f"{WA}?text={quote(msg)}"


def icon(name, cls="w-5 h-5"):
    return (f'<svg class="i {cls}" aria-hidden="true" focusable="false">'
            f'<use href="#i-{name}"></use></svg>')


# The compiled Tailwind stylesheet, inlined rather than linked so the page
# needs no blocking request at all. Built by buildall.py, which generates the
# markup once without it, runs the Tailwind CLI over that markup, then
# regenerates with the result in hand - compiling from CSS-free HTML so the
# extractor never reads its own output back as class names.
# Noto Sans Tamil, declared for the Tamil block only. DM Sans has no Tamil
# glyphs at all - its subsets stop at latin-ext - so without this every Tamil
# page would fall back to whatever face the device happens to carry. Scoping
# the unicode-range to Tamil means Latin text still renders in DM Sans, and an
# English page never downloads this file.
TAMIL_FACE = """
        @font-face {
            font-family: 'Noto Sans Tamil';
            font-style: normal;
            /* The shipped file is variable across 100-900, so opening the
               descriptor up costs nothing and lets Tamil headings sit at 300
               to answer the light serif on the English pages. Noto Serif Tamil
               would have been the closer match but costs 53 KB, which the
               page budget would not carry. */
            font-weight: 300 600;
            /* swap reflowed the whole Tamil hero when this arrived, which was
               almost all of the page's 0.099 CLS. optional lets the browser
               skip the swap on a load where the font is late rather than
               shift the page under the reader - and every device that reads
               Tamil ships a Tamil system font, so the fallback is never tofu.
               It is preloaded and cached, so most loads still get it. */
            font-display: optional;
            src: url(/noto-tamil.woff2) format('woff2');
            unicode-range: U+0964-0965, U+0B82-0BFA, U+200C-200D, U+20B9, U+25CC;
        }
        :lang(ta) body {
            font-family: 'Noto Sans Tamil', 'DM Sans', system-ui, sans-serif;
        }
        /* Tamil has no Cormorant, so its display type is the same Noto face
           set light and large - the weight and scale carry the character that
           the serif carries in English. */
        :lang(ta) h1, :lang(ta) h2, :lang(ta) h3, :lang(ta) .display {
            font-family: 'Noto Sans Tamil', 'Cormorant Garamond', serif;
            font-weight: 300;
        }
        /* Tamil words are long and do not hyphenate. "பெருங்களத்தூர்" alone
           measures 387px at the Latin d1 size, which is wider than a 390px
           phone - and since a grid item will not shrink below its longest
           word, that one word pushed the whole hero off the screen. The scale
           steps down until it fits, break-word catches anything longer in
           future, and the line box opens up because Tamil carries taller
           ascenders and descenders than Latin. */
        :lang(ta) h1 { font-size: clamp(2.05rem, 5.2vw, 3.5rem); line-height: 1.18; }
        /* Tamil sets wider than Latin at the same point size, so its display
           steps come down too. Left at the Latin sizes, single compounds ran
           past their columns at desktop widths - peruNGkaLattUril measured
           473px in a 416px column - and the page scrolled sideways. */
        :lang(ta) h2 { line-height: 1.22; font-size: clamp(1.5rem, 2.8vw, 2.35rem); }
        :lang(ta) h3 { font-size: clamp(1.12rem, 1.5vw, 1.4rem); }
        :lang(ta) h1, :lang(ta) h2, :lang(ta) h3, :lang(ta) .display,
        :lang(ta) p, :lang(ta) li, :lang(ta) address, :lang(ta) figcaption,
        :lang(ta) dt, :lang(ta) dd, :lang(ta) blockquote, :lang(ta) summary {
            overflow-wrap: break-word;
        }
        /* Tamil words run long, and a grid track sized `auto` cannot fall
           below the widest unbreakable word in it - so on a 320px phone one
           word like "peruNGkaLattUr" was widening the hero track past the
           screen no matter how freely the text was allowed to wrap.
           overflow-wrap alone does not help: it breaks the rendered line but
           leaves the min-content width computed from the whole word. Clearing
           the automatic minimum size lets the track shrink; the rule above
           then breaks the word to fit. */
        :lang(ta) .grid > * { min-width: 0; }
        /* Tamil compounds run to nineteen characters, and on a 320-360px
           phone the longest of them - peruNGkaLattUril, tAmparattilirundhu -
           are wider than the column at the Latin heading sizes. Breaking them
           works but splits a word mid-cluster, so the headings step down just
           on those widths and the words stay whole. Above 384px the Latin
           sizes already fit and nothing changes. */
        @media (max-width: 24rem) {
            :lang(ta) h1 { font-size: clamp(1.6rem, 8.4vw, 2.05rem); }
            :lang(ta) h2 { font-size: clamp(1.5rem, 7.7vw, 1.875rem); }
        }
"""

TAILWIND = ""
_tw = os.environ.get("TW_CSS")
if _tw and os.path.exists(_tw):
    TAILWIND = "\n" + open(_tw, encoding="utf-8").read().strip() + "\n"

CSS = FONT_FACE + TAILWIND + """
        /* These mirror the Tailwind tokens exactly. They are consumed by the
           hand-written components below - carousel, FAQ, mobile menu, lightbox
           - which would otherwise keep rendering the palette the site used
           before, while everything class-driven moved on without them. */
        :root {
            --ink:#10263A; --blue:#1F4E79; --sky:#4DA8DA;
            --sand:#E3EDF5; --paper:#F2F6FA; --line:#D3E0EA; --muted:#5A6B7B;
        }
        html { scroll-behavior: smooth; }
        body { -webkit-font-smoothing: antialiased; }
        /* The nav is fixed, so an anchor jump would otherwise land the target
           heading underneath it. Only applies when the element is scrolled to. */
        [id] { scroll-margin-top: 5rem; }

        h1, h2, h3, .display {
            font-family: 'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
            font-weight: 500;
        }
        .lede { font-size: clamp(1.0625rem, 1.35vw, 1.1875rem); line-height: 1.65; }

        /* ---- scroll reveals: opacity and transform only, once per element,
           and gated on .js so nothing is ever hidden without a script ---- */
        .js .reveal { opacity:0; transform:translateY(14px); }
        .js .reveal.is-in {
            opacity:1; transform:none;
            transition:opacity .7s cubic-bezier(.2,.7,.3,1) var(--d, 0ms),
                       transform .7s cubic-bezier(.2,.7,.3,1) var(--d, 0ms);
        }

        /* ---- bento: a 1px grid gap over the rule colour draws the dividers,
           so the tiles separate without a single shadow ---- */
        .bento { display:grid; gap:1px; background:var(--line);
                 border:1px solid var(--line); border-radius:.25rem; overflow:hidden; }
        /* The health bento ends in a photograph, which cannot sit inside the
           <dl>: a div child of a definition list has to wrap a dt/dd pair. It
           lives directly below instead, and these two join the seam so the
           whole thing still reads as one panel. The foot keeps its top border,
           which supplies the hairline the grid gap used to draw. */
        .bento-open-b { border-bottom:0; border-bottom-left-radius:0; border-bottom-right-radius:0; }
        /* Language toggle. Only rendered where the page actually has a
           counterpart, so it can never point at a page that does not exist.
           The Tamil label falls back to a system Tamil face on English pages -
           shipping the 50K webfont everywhere for one word is not worth it,
           and every platform we care about has one. */
        .lang-toggle { display:inline-flex; align-items:center; border:1px solid var(--line);
                       border-radius:999px; overflow:hidden; background:var(--paper); }
        .lang-toggle > * { padding:.3rem .6rem; font-size:12.5px; line-height:1.4;
                           color:var(--muted); text-decoration:none; }
        .lang-toggle > a:hover { color:var(--ink); background:var(--sand); }
        .lang-toggle [aria-current] { background:var(--ink); color:#fff; font-weight:500; }
        .lang-ta { font-family:'Noto Sans Tamil','Nirmala UI','Latha',sans-serif; }

        .bento-foot { border:1px solid var(--line); overflow:hidden;
                      border-bottom-left-radius:.25rem; border-bottom-right-radius:.25rem; }

        svg.i { fill: none; stroke: currentColor; stroke-width: 1.75;
                stroke-linecap: round; stroke-linejoin: round; }

        .sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px;
                   overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }
        .skip-link { position:absolute; left:50%; top:0; transform:translate(-50%,-120%);
                     z-index:100; background:var(--blue); color:#fff; padding:.75rem 1.5rem;
                     border-radius:0 0 .375rem .375rem; font-weight:600; transition:transform .2s ease; }
        .skip-link:focus { transform:translate(-50%,0); }
        a:focus-visible, button:focus-visible, input:focus-visible,
        select:focus-visible, textarea:focus-visible {
            outline:2px solid var(--blue); outline-offset:2px; border-radius:2px;
        }

        .nav-scrolled { border-bottom-color: var(--line); }

        /* ---- mobile menu ---- */
        .mobile-menu { position:fixed; inset:0; z-index:60; visibility:hidden; }
        .mobile-menu::before { content:''; position:absolute; inset:0;
            background:rgba(17,24,32,0); transition:background .3s ease; }
        .mobile-menu.open { visibility:visible; }
        .mobile-menu.open::before { background:rgba(17,24,32,.45); }
        .mobile-menu-panel { position:absolute; top:0; right:0; bottom:0; width:100%;
            max-width:21rem; background:#fff; transform:translateX(100%);
            transition:transform .3s cubic-bezier(.4,0,.2,1); display:flex; flex-direction:column; }
        .mobile-menu.open .mobile-menu-panel { transform:translateX(0); }

        /* ---- the one page-load moment: the next-class panel resolving ---- */
        @keyframes settle { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:none; } }
        .settle { animation: settle .5s cubic-bezier(.2,.7,.3,1) both; }

        /* ---- batch list (hero) ---- */
        .batch { display:block; width:100%; text-align:left; border-top:1px solid var(--line);
                 padding:.9rem 0; transition:padding-left .2s ease; }
        .batch:hover { padding-left:.35rem; }
        .batch[aria-expanded="true"] { padding-left:.35rem; }
        .batch-detail { overflow:hidden; }
        .batch-now { color:var(--blue); font-weight:600; }

        /* ---- hero fact line: flows and wraps, no boxes ----
           No separator glyph between items: the line wraps at every width the
           hero column takes, and a ::before dot orphans at the start of each
           wrapped line. Spacing carries the separation instead. */
        .factline { display:flex; flex-wrap:wrap; column-gap:2rem; row-gap:.55rem; }

        /* ---- class filter ---- */
        .filter[aria-pressed="true"] { background:var(--ink); color:#fff; border-color:var(--ink); }
        .class-item[hidden] { display:none; }

        /* ---- reviews carousel ----
           A scroll-snap track, so it swipes natively on touch and scrolls with
           the arrow keys when focused; the controls below it are added by CSS
           only once the script has wired them up (.is-ready), so nothing dead
           is shown if the script never runs. */
        .rev-track { display:flex; align-items:stretch; overflow-x:auto; overflow-y:hidden;
                     scroll-snap-type:x mandatory; scroll-behavior:smooth;
                     scrollbar-width:none; -webkit-overflow-scrolling:touch;
                     transition:height .3s ease; }
        /* The script sets the track's height to the cards actually in view, so
           one long quote does not leave a dead band under every short one; this
           class lets it measure their natural heights first. */
        .rev-track.rev-measure { align-items:flex-start; height:auto; }
        .rev-track::-webkit-scrollbar { display:none; }
        .rev-slide { flex:0 0 100%; scroll-snap-align:start; }
        @media (min-width:768px) { .rev-slide { flex-basis:50%; } }
        .rev-controls { display:none; flex-wrap:wrap; row-gap:.75rem; }
        .rev.is-ready .rev-controls { display:flex; }
        .rev-btn { display:inline-flex; align-items:center; justify-content:center;
                   width:2.25rem; height:2.25rem; border:1px solid var(--line);
                   border-radius:9999px; background:var(--paper); color:var(--ink);
                   transition:border-color .2s ease, background .2s ease; }
        .rev-btn:hover { border-color:var(--ink); background:#fff; }
        .rev-dot { display:inline-flex; align-items:center; justify-content:center;
                   width:1.5rem; height:1.5rem; }
        .rev-count { font-size:.8125rem; color:var(--muted); font-variant-numeric:tabular-nums; }
        .rev-dot::before { content:''; width:.4375rem; height:.4375rem; border-radius:9999px;
                           background:var(--line); transition:background .2s ease; }
        .rev-dot:hover::before { background:var(--muted); }
        .rev-dot[aria-current="true"]::before { background:var(--blue); }

        /* Keeps the standfirsts in the journal grid to two lines, so the rows
           line up whatever length each post's opening sentence is. */
        .clamp-2 { display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;
                   overflow:hidden; }
        /* Two lines keeps the review cards level with each other across a row.
           A phone shows one card at a time, so there is no row to level and
           two lines of a narrow column cut the quote off after a few words. */
        @media (max-width: 40rem) { .clamp-2 { -webkit-line-clamp:5; } }

        /* ---- FAQ: the plus turns into a cross while its answer is open.
           .is-open was being toggled with nothing listening to it. ---- */
        .faq-q svg { transition:transform .3s cubic-bezier(.4,0,.2,1); }
        .faq-item.is-open .faq-q svg { transform:rotate(45deg); }

        .lightbox { display:none; position:fixed; inset:0; background:rgba(12,16,20,.94);
                    z-index:100; align-items:center; justify-content:center; padding:1.5rem; }
        .lightbox.active { display:flex; }


        /* ============================================================
           Warm redesign. Everything below rides on the retuned Tailwind
           tokens, so it reaches every page at once rather than being
           re-specified per template.
           ============================================================ */

        /* Decorative tints. These never carry text - the text-safe members
           of the palette are the Tailwind tokens sky/clay/muted, each of
           which clears 4.5:1 on the lightest ground it sits on. */
        :root {
            --sage-soft:#D5E7F2; --amber-soft:#B08D57; --clay-soft:#4DA8DA;
            --card:#FFFFFF;
            /* Proportional, so the dome keeps its shape whatever the frame:
               a fixed radius turned wide boxes into near-semicircles and cut
               the tops off raised arms. */
            --arch:50% 50% .9rem .9rem / 30% 30% .9rem .9rem;
            --ease:cubic-bezier(.22,.7,.3,1);
        }

        /* Display type is the serif; body copy stays DM Sans. Cormorant sets
           light and small, so it wants a lower weight and more room. */
        h1, h2, h3, .display {
            font-family:'Cormorant Garamond', Georgia, 'Times New Roman', serif;
            font-weight:400; letter-spacing:0;
            /* Cormorant defaults to oldstyle figures, which sat oddly beside
               the sans lining figures in the same schedule row. */
            font-variant-numeric:lining-nums;
        }
        h1, .text-d1 { font-weight:300; }

        /* An italic serif label instead of a tracked-out uppercase one. */
        .lbl {
            font-family:'Cormorant Garamond', Georgia, serif; font-style:italic;
            font-size:1.2rem; line-height:1.4; color:#81663D; margin:0;
        }
        :lang(ta) .lbl { font-family:'Noto Sans Tamil', serif; font-style:normal;
                         font-size:1.05rem; }
        /* The label over the hero photograph. The brass that works on paper
           measures 2.95:1 against the scrimmed image - this lighter tone is
           5.64:1 on the same backdrop. */
        .lbl--dark { color:#F3E2C8; }
        /* A heading used as a control label is interface, not display type.
           Cormorant at 15.5px is too delicate to tap confidently, so the FAQ
           questions keep the body face even though they are h3 for structure. */
        .faq-q, .faq-q span { font-family:'DM Sans', system-ui, sans-serif; }
        /* 15ch is a good measure for the English headline but far too tight
           for Tamil, whose compounds then broke mid-cluster. */
        :lang(ta) .bleed__in h1 { max-width:24ch; }

        /* Softer geometry throughout: cards and photographs get a real
           radius, and anything that reads as a button becomes a pill. */
        .rounded { border-radius:.85rem; }
        [class~="bg-ink"][class~="rounded"],
        [class~="bg-blue"][class~="rounded"],
        [class~="bg-amber"][class~="rounded"] { border-radius:999px; }

        /* The arch: a doorway shape, used for every portrait-format photo. */
        .arch { border-radius:var(--arch); overflow:hidden; }
        .arch img, img.arch { width:100%; height:100%; object-fit:cover; display:block; }

        /* ---- transitions -------------------------------------------------
           1. between pages, 2. on scroll, 3. on hover/press, 4. on load.
           All four are transform/opacity only, so none of them can move
           the layout or cost a reflow. */

        /* 1. Page to page. Same-origin navigations cross-fade instead of
              blinking white. Costs nothing and is ignored where unsupported. */
        @view-transition { navigation: auto; }
        ::view-transition-old(root) { animation:vt-out .28s ease both; }
        ::view-transition-new(root) { animation:vt-in .38s var(--ease) both; }
        @keyframes vt-out { to { opacity:0; } }
        @keyframes vt-in { from { opacity:0; transform:translateY(10px); } }

        /* 3. Hover and press. Photographs breathe inside their frame, cards
              lift, rows warm and step aside, links draw their underline. */
        .lift { transition:transform .55s var(--ease), box-shadow .55s ease; }
        .lift:hover { transform:translateY(-6px);
                      box-shadow:0 30px 50px -34px rgba(16,38,58,.45); }
        .zoom { overflow:hidden; }
        .zoom img { transition:transform 1.1s var(--ease); }
        .zoom:hover img, a:hover > .zoom img { transform:scale(1.05); }
        .row-step { transition:background .45s ease, padding-left .45s var(--ease); }
        .row-step:hover { background:var(--card); }
        @media (min-width:52rem) { .row-step:hover { padding-left:1.5rem; } }
        .ul-draw { text-decoration:none; background-image:linear-gradient(currentColor,currentColor);
                   background-repeat:no-repeat; background-position:0 100%;
                   background-size:0% 1px; transition:background-size .45s var(--ease); }
        .ul-draw:hover, .ul-draw:focus-visible { background-size:100% 1px; }

        /* A link sitting inside a run of text has to be distinguishable by
           more than its colour. The deepened indigo reads as only 1.55:1
           against body copy - well under the 3:1 the rule wants - so links in
           prose carry a permanent underline rather than relying on hue. */
        p a.text-blue, li a.text-blue, dd a.text-blue {
            text-decoration:underline; text-underline-offset:.17em;
            text-decoration-thickness:.055em;
            text-decoration-color:color-mix(in srgb, currentColor 45%, transparent);
            transition:text-decoration-color .35s ease;
        }
        p a.text-blue:hover, li a.text-blue:hover, dd a.text-blue:hover {
            text-decoration-color:currentColor;
        }

        /* 4. Page load. The first screen arrives in order rather than all at
              once. It runs from a visible resting state, so a reader who
              never gets the animation still sees a finished page. */
        @keyframes enter { from { opacity:0; transform:translateY(16px); } }
        .js .enter > * { animation:enter .9s var(--ease) both; }
        .js .enter > :nth-child(1) { animation-delay:.05s; }
        .js .enter > :nth-child(2) { animation-delay:.15s; }
        .js .enter > :nth-child(3) { animation-delay:.25s; }
        .js .enter > :nth-child(4) { animation-delay:.35s; }
        .js .enter > :nth-child(5) { animation-delay:.45s; }

        /* Ambient: a slow warm light behind the opening screen. */
        @keyframes breathe {
            from { transform:scale(1); opacity:.8; }
            to   { transform:scale(1.12) translate3d(-2%,2%,0); opacity:1; }
        }
        /* Photographs keep their own colour. A blue was blended over them to
           unify the set, and it cost more than it bought: the room's warmth -
           the wood, the lamps, the students' shirts - went flat slate, and the
           whole site read dull. All that is left is a gentle lift, which helps
           the few frames the tube light underexposed and changes no hue. */
        .grade { position:relative; }
        .grade > img, .grade > picture > img {
            filter:saturate(1.06) contrast(1.04) brightness(1.03);
        }
        /* A face wants even less than that. */
        .grade--portrait > picture > img { filter:saturate(1.02) contrast(1.02); }

        /* The opening screen: one photograph, edge to edge, with the headline
           and a single call to action over it. Everything else waits below. */
        .bleed { position:relative; isolation:isolate; overflow:hidden;
                 background:#0E2740; }
        .bleed__img { position:absolute; inset:0; z-index:0; }
        .bleed__img img { width:100%; height:100%; object-fit:cover;
                          transform:scale(1.04); animation:slowpan 30s ease-in-out infinite alternate; }
        @keyframes slowpan { to { transform:scale(1.13) translate3d(0,-2%,0); } }
        /* Two scrims: a wash that carries the grade, and a foot that gives the
           text a floor to sit on. Measured, not guessed - see the contrast
           check in the commit. */
        /* The headline sits at the foot of the hero, so only the foot needs to
           be dark. Covering the whole frame - which is what this did, on top
           of a blue blended across every pixel - was most of why the opening
           screen looked murky. The top two thirds are now the photograph. */
        .bleed__foot { position:absolute; inset:0; z-index:2;
            background:linear-gradient(to bottom,
                rgba(6,20,34,0) 0%, rgba(6,20,34,.04) 16%, rgba(6,20,34,.22) 30%,
                rgba(6,20,34,.46) 52%, rgba(6,20,34,.74) 78%, rgba(6,20,34,.90) 100%); }
        .bleed__in { position:relative; z-index:3; }

        /* Same idea for the one band where copy sits over a photograph: the
           text is a column on the left, so the cover is heaviest there and
           thins out across the frame, instead of a flat 70% over everything. */
        .cta-scrim { position:absolute; inset:0;
            background:linear-gradient(100deg, rgba(6,20,34,.88) 0%, rgba(6,20,34,.74) 38%,
                       rgba(6,20,34,.40) 70%, rgba(6,20,34,.22) 100%); }

        .glow { position:absolute; pointer-events:none; border-radius:50%;
                background:radial-gradient(closest-side, rgba(77,168,218,.28), transparent 70%);
                animation:breathe 20s ease-in-out infinite alternate; }

        @media (prefers-reduced-motion: reduce) {
            html, .rev-track { scroll-behavior:auto; }
            .js .reveal { opacity:1 !important; transform:none !important; }
            .js .enter > * { animation:none !important; }
            @view-transition { navigation: none; }
            *, *::before, *::after {
                animation-duration:.01ms !important; animation-iteration-count:1 !important;
                transition-duration:.01ms !important;
            }
        }
"""


def head(*, title, desc, path, schema, preload=None, preload_srcset=None,
         preload_sizes=None, og_img="og-image.jpg", lang="en", alt=None, pre_path=""):
    """`lang` is the page's own language; `alt` the same page in the other one,
    as (lang, path). `pre_path` prefixes every asset URL - the Tamil pages live
    a directory down, so they address assets from the root."""
    url = f"{BASE}/{path}" if path else f"{BASE}/"
    if preload and preload_srcset:
        # Preload the same candidate <picture> will choose, or the phone fetches
        # the 1280px file and then the 640px one.
        pre = (f'\n    <link rel="preload" as="image" href="{preload}"'
               f'\n          imagesrcset="{preload_srcset}" imagesizes="{preload_sizes}"'
               f' type="image/webp" fetchpriority="high">')
    elif preload:
        pre = (f'\n    <link rel="preload" as="image" href="{preload}" '
               f'type="image/webp" fetchpriority="high">')
    else:
        pre = ""
    # hreflang has to be reciprocal - both versions naming both - or Google
    # treats the pair as unrelated duplicates. x-default points at English.
    alts = ""
    if alt:
        alt_lang, alt_path = alt
        alt_url = f"{BASE}/{alt_path}" if alt_path else f"{BASE}/"
        en_url = url if lang == "en" else alt_url
        alts = (f'\n    <link rel="alternate" hreflang="{lang}-IN" href="{url}">'
                f'\n    <link rel="alternate" hreflang="{alt_lang}-IN" href="{alt_url}">'
                f'\n    <link rel="alternate" hreflang="x-default" href="{en_url}">')
    extra_css = TAMIL_FACE if lang == "ta" else ""
    tamil_pre = ('\n    <link rel="preload" href="/noto-tamil.woff2" as="font" '
                 'type="font/woff2" crossorigin>') if lang == "ta" else ""
    locale = "ta_IN" if lang == "ta" else "en_IN"
    payload = json.dumps(schema, indent=2, ensure_ascii=False)
    assert json.loads(payload)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Google tag (gtag.js). Placed here because Google asks for it directly
         after <head>; charset and viewport keep their spot because charset has
         to fall inside the first 1024 bytes. async, so it blocks nothing. -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{GA_ID}');
    </script>

    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{url}">{alts}
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
    <meta name="theme-color" content="#1F4E79">

    <meta name="geo.region" content="IN-TN">
    <meta name="geo.placename" content="New Perungalathur, Chennai">
    <meta name="geo.position" content="12.8938068;80.1131382">
    <meta name="ICBM" content="12.8938068, 80.1131382">

    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Happy Yogis Yoga Centre">
    <meta property="og:locale" content="{locale}">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{BASE}/{og_img}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{BASE}/{og_img}">

    <link rel="icon" href="{pre_path}favicon.ico" sizes="any">
    <link rel="icon" type="image/png" sizes="32x32" href="{pre_path}favicon-32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="{pre_path}favicon-16.png">
    <link rel="apple-touch-icon" href="{pre_path}apple-touch-icon.png">
    <link rel="manifest" href="{pre_path}site.webmanifest">

    <link rel="preload" href="/dm-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/cormorant.woff2" as="font" type="font/woff2" crossorigin>{tamil_pre}{pre}

    <script>document.documentElement.className += ' js';</script>
    <style>{CSS}{extra_css}    </style>


    <script type="application/ld+json">
{payload}
    </script>
</head>
"""


# The journal's name. HTML gets a typographic apostrophe; titles, meta and
# JSON-LD get the plain one, because those are read as data.
GA_ID = "G-86VPTR7ERW"          # Happy Yogis GA4 property

JOURNAL = "Yogi&rsquo;s Upadesha"
JOURNAL_PLAIN = "Yogi's Upadesha"

NAV_LINKS = [
    ("/#schedule", "Schedule"),
    ("/#classes", "Classes"),
    ("/#teacher", "Teacher"),
    ("/#studio", "Studio"),
    ("blog.html", JOURNAL),
    ("/#visit", "Visit"),
]


# Default nav wording. A translation passes its own, so the markup, the element
# ids and the classes the script binds to all stay in one place - a second
# language cannot drift away from the behaviour the way a hand-copied nav does.
# Tamil sets wider than Latin at the same size, and the nav carries six links,
# a toggle, a phone number and a button. Tamil holds the number back to xl so
# nothing wraps; it is still in the footer, the visit panel and the mobile menu.
NAV_WORDS = dict(skip="Skip to main content", menu="Menu", open_menu="Open menu",
                 phone_cls="hidden sm:inline-flex",
                 close_menu="Close menu", trial="Book a trial",
                 trial_full="Book a 3-day trial",
                 switch=None, switch_href=None, switch_lang=None)


def nav(home=False, words=None, links_data=None, trial_msg=None,
        lang="en", alt_href=None):
    W = dict(NAV_WORDS, **(words or {}))
    data = links_data if links_data is not None else NAV_LINKS

    def href(h):
        return h.replace("index.html", "") if home and h.startswith("index.html#") else h

    links = "\n".join(
        f'                    <a href="{href(h)}" class="text-[13.5px] text-ink/70 hover:text-ink transition-colors">{t}</a>'
        for h, t in data)
    mlinks = "\n".join(
        f'                <a href="{href(h)}" class="mobile-link block px-6 py-3.5 text-[17px] text-ink border-b border-line hover:bg-sand transition-colors">{t}</a>'
        for h, t in data)
    # Two states, both always visible, so a visitor can see the other language
    # exists rather than having to discover a one-way link. Rendered only when
    # alt_href is set - i.e. only where a counterpart page really exists, the
    # same condition that decides whether hreflang is emitted.
    toggle = mtoggle = ""
    if alt_href:
        en_href = alt_href if lang == "ta" else "#"
        ta_href = alt_href if lang == "en" else "#"
        def side(code, label, href, cls, active):
            if active:
                return f'<span aria-current="true" class="{cls}">{label}</span>'
            return (f'<a href="{href}" hreflang="{code}" lang="{code}" class="{cls}">'
                    f'{label}</a>')
        en = side("en", "EN", en_href, "", lang == "en")
        ta = side("ta", "&#2980;&#2990;&#3007;&#2996;&#3021;", ta_href, "lang-ta", lang == "ta")
        toggle = ('\n                    <span class="lang-toggle" role="group" aria-label="Language">'
                  f'{en}{ta}</span>')
        mtoggle = ('\n                <div class="px-6 py-4 border-b border-line">'
                   '<span class="lang-toggle" role="group" aria-label="Language">'
                   f'{en}{ta}</span></div>')
    links += toggle
    mlinks += mtoggle
    # English pages canonicalise the homepage as "/", so linking it as
    # index.html created a second crawlable URL for the same page. Tamil
    # keeps the relative form, which resolves to /ta/index.html - its own
    # canonical.
    home_href = "#main" if home else ("index.html" if lang == "ta" else "/")

    return f"""    <a href="#main" class="skip-link">{W["skip"]}</a>

    <header>
      <nav id="navbar" aria-label="Primary" class="fixed top-0 inset-x-0 z-50 bg-paper/95 backdrop-blur-sm border-b border-transparent transition-colors">
        <div class="max-w-6xl mx-auto px-5 sm:px-8">
            <div class="flex items-center justify-between h-16">
                <a href="{home_href}" class="flex items-center gap-2.5 shrink-0">
                    <picture><source srcset="/logo.webp" type="image/webp">
                    <img src="/logo.png" alt="" width="40" height="45" class="w-8 h-auto"></picture>
                    <span class="display text-[17px] text-ink">Happy Yogis</span>
                </a>

                <div class="hidden lg:flex items-center gap-4 2xl:gap-7 whitespace-nowrap">
{links}
                </div>

                <div class="flex items-center gap-2">
                    <a href="{PHONE_HREF}" class="{W['phone_cls']} items-center gap-1.5 text-[13.5px] font-medium text-ink px-3 py-2 hover:text-blue transition-colors">
                        {icon('phone', 'w-4 h-4')}{PHONE_TEXT}
                    </a>
                    <a href="{'#enquire' if home else 'index.html#enquire'}" class="hidden sm:inline-flex items-center px-4 py-2 bg-ink text-white text-[13.5px] font-medium rounded hover:bg-blue transition-colors">
                        {W["trial"]}
                    </a>
                    <button id="menu-btn" type="button" aria-label="{W["open_menu"]}" aria-expanded="false" aria-controls="mobile-menu"
                            class="lg:hidden -mr-2 p-2 text-ink">{icon('menu', 'w-6 h-6')}</button>
                </div>
            </div>
        </div>
      </nav>
    </header>

    <div id="mobile-menu" class="mobile-menu lg:hidden" role="dialog" aria-modal="true" aria-label="Menu" aria-hidden="true">
        <div class="mobile-menu-panel">
            <div class="flex items-center justify-between px-6 h-16 border-b border-line">
                <span class="display text-[17px] text-ink">{W["menu"]}</span>
                <button id="menu-close" type="button" aria-label="{W["close_menu"]}" class="-mr-2 p-2 text-ink">{icon('x', 'w-6 h-6')}</button>
            </div>
            <nav aria-label="Mobile" class="flex-1 overflow-y-auto">
{mlinks}
            </nav>
            <div class="p-5 space-y-2.5 border-t border-line">
                <a href="{('' if home else 'index.html')}#enquire" class="mobile-link flex items-center justify-center w-full px-5 py-3.5 bg-ink text-white font-medium rounded">
                    Book a 3-day trial
                </a>
                <a href="{PHONE_HREF}" class="mobile-link flex items-center justify-center gap-2 w-full px-5 py-3.5 border border-line text-ink font-medium rounded">
                    {icon('phone', 'w-4 h-4')}{PHONE_TEXT}
                </a>
            </div>
        </div>
    </div>
"""


def footer():
    return f"""    <footer class="bg-ink text-white/65 mt-px">
        <div class="max-w-6xl mx-auto px-5 sm:px-8 py-14">
            <div class="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
                <div class="lg:col-span-2">
                    <div class="flex items-center gap-2.5 mb-4">
                        <picture><source srcset="/logo.webp" type="image/webp">
                        <img src="/logo.png" alt="" width="40" height="45" class="w-8 h-auto"></picture>
                        <span class="display text-[17px] text-white">Happy Yogis Yoga Centre</span>
                    </div>
                    <address class="not-italic text-sm leading-relaxed">
                        SSM Nagar, New Perungalathur<br>Chennai, Tamil Nadu 600063<br>
                        <a href="{PHONE_HREF}" class="inline-block py-1 text-white hover:text-sky transition-colors">{PHONE_TEXT}</a>
                    </address>
                    <p class="mt-4 text-sm">Monday to Friday, 5:30 am to 7:00 pm.<br>Closed Saturday, Sunday and public holidays.</p>
                    <p class="mt-4 text-sm">One centre, in New Perungalathur. We have no other branches.</p>
                </div>

                <nav aria-labelledby="f-site">
                    <h2 id="f-site" class="text-white font-medium text-sm mb-4">The centre</h2>
                    <ul class="space-y-0.5 text-sm">
                        <li><a href="/#schedule" class="inline-block py-1 hover:text-sky transition-colors">Batch schedule</a></li>
                        <li><a href="/#classes" class="inline-block py-1 hover:text-sky transition-colors">What we teach</a></li>
                        <li><a href="/#teacher" class="inline-block py-1 hover:text-sky transition-colors">Your teacher</a></li>
                        <li><a href="/#studio" class="inline-block py-1 hover:text-sky transition-colors">Photos</a></li>
                        <li><a href="blog.html" class="inline-block py-1 hover:text-sky transition-colors">{JOURNAL}</a></li>
                        <li><a href="/#faq" class="inline-block py-1 hover:text-sky transition-colors">Questions</a></li>
                    </ul>
                </nav>

                <nav aria-labelledby="f-areas">
                    <h2 id="f-areas" class="text-white font-medium text-sm mb-4">Areas we teach</h2>
                    <ul class="space-y-0.5 text-sm">
                        <li><a href="yoga-classes-perungalathur.html" class="inline-block py-1 hover:text-sky transition-colors">Yoga classes in Perungalathur</a></li>
                        <li><a href="yoga-classes-tambaram.html" class="inline-block py-1 hover:text-sky transition-colors">Yoga classes near Tambaram</a></li>
                        <li><a href="/#visit" class="inline-block py-1 hover:text-sky transition-colors">Visit the centre</a></li>
                    </ul>
                </nav>
            </div>

            <div class="mt-12 pt-6 border-t border-white/10 flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between text-xs">
                <p>&copy; 2026 Happy Yogis Yoga Centre.</p>
                <p class="flex gap-5">
                    <a href="privacy-policy.html" class="inline-block py-1 hover:text-sky transition-colors">Privacy Policy</a>
                    <a href="terms-of-service.html" class="inline-block py-1 hover:text-sky transition-colors">Terms &amp; Conditions</a>
                </p>
            </div>
        </div>
    </footer>

    <aside aria-label="Quick contact">
        <a href="{wa('Hello Happy Yogis! I would like to know more about your yoga classes.')}" target="_blank" rel="noopener"
           class="fixed bottom-5 right-5 z-40 inline-flex items-center gap-2 pl-3.5 pr-4 py-3 rounded-full bg-[#17843F] text-white text-sm font-medium hover:bg-[#126B33] transition-colors"
           aria-label="Chat with Happy Yogis on WhatsApp">
            {icon('message-circle', 'w-5 h-5')}<span class="hidden sm:inline">WhatsApp</span>
        </a>
    </aside>
"""


SCRIPT = """    <script>
    (function () {
        'use strict';
        var navbar = document.getElementById('navbar');
        var ticking = false;
        window.addEventListener('scroll', function () {
            if (ticking) return;
            ticking = true;
            requestAnimationFrame(function () {
                navbar.classList.toggle('nav-scrolled', window.scrollY > 8);
                ticking = false;
            });
        }, { passive: true });

        /* Keep Tab inside an open modal dialog. */
        function focusables(root) {
            return Array.prototype.filter.call(
                root.querySelectorAll('a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])'),
                function (el) { return el.offsetWidth > 0 || el.offsetHeight > 0 || el === document.activeElement; });
        }
        function makeTrap(root) {
            return function (e) {
                if (e.key !== 'Tab') return;
                var f = focusables(root);
                if (!f.length) return;
                var first = f[0], last = f[f.length - 1];
                if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
                else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
            };
        }

        /* ---------- mobile menu ---------- */
        var menu = document.getElementById('mobile-menu');
        var mBtn = document.getElementById('menu-btn');
        var mClose = document.getElementById('menu-close');
        var lastFocus = null;
        var menuTrap = makeTrap(menu);
        function openMenu() {
            lastFocus = document.activeElement;
            document.addEventListener('keydown', menuTrap, true);
            menu.classList.add('open');
            menu.setAttribute('aria-hidden', 'false');
            mBtn.setAttribute('aria-expanded', 'true');
            document.body.style.overflow = 'hidden';
            mClose.focus();
        }
        function closeMenu() {
            document.removeEventListener('keydown', menuTrap, true);
            menu.classList.remove('open');
            menu.setAttribute('aria-hidden', 'true');
            mBtn.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
            if (lastFocus) lastFocus.focus();
        }
        mBtn.addEventListener('click', openMenu);
        mClose.addEventListener('click', closeMenu);
        menu.addEventListener('click', function (e) { if (e.target === menu) closeMenu(); });
        menu.querySelectorAll('.mobile-link').forEach(function (a) { a.addEventListener('click', closeMenu); });

        /* ---------- hero: which batch is next, from the visitor's clock ----------
           Classes run Monday to Friday only. On a weekend, or after the last
           batch, this points at the next weekday morning. */
        var nextEl = document.getElementById('next-class');
        var batches = Array.prototype.map.call(
            document.querySelectorAll('[data-start]'),
            function (el) { return { el: el, start: el.getAttribute('data-start'), label: el.getAttribute('data-label') }; });

        if (nextEl && batches.length) {
            var now = new Date();
            var day = now.getDay();                       // 0 Sun .. 6 Sat
            var mins = now.getHours() * 60 + now.getMinutes();
            function toMins(hhmm) {
                var p = hhmm.split(':');
                return parseInt(p[0], 10) * 60 + parseInt(p[1], 10);
            }
            var weekday = day >= 1 && day <= 5;
            var upcoming = null;
            if (weekday) {
                for (var i = 0; i < batches.length; i++) {
                    if (toMins(batches[i].start) > mins) { upcoming = batches[i]; break; }
                }
            }
            var when;
            if (upcoming) {
                when = 'Next class today';
            } else {
                upcoming = batches[0];
                var names = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
                var d = day;
                do { d = (d + 1) % 7; } while (d < 1 || d > 5);
                when = 'Next class ' + (d === (day + 1) % 7 ? 'tomorrow' : names[d]);
            }
            nextEl.innerHTML = '<span class="batch-now">' + when + '</span> &middot; ' + upcoming.label;
            nextEl.classList.add('settle');
            upcoming.el.setAttribute('data-next', 'true');
        }

        /* ---------- hero: expanding a batch (user-triggered) ---------- */
        document.querySelectorAll('.batch').forEach(function (btn, i) {
            var detail = document.getElementById(btn.getAttribute('aria-controls'));
            if (!detail) return;
            detail.hidden = true;
            btn.addEventListener('click', function () {
                var open = btn.getAttribute('aria-expanded') === 'true';
                document.querySelectorAll('.batch').forEach(function (other) {
                    if (other === btn) return;
                    other.setAttribute('aria-expanded', 'false');
                    var d = document.getElementById(other.getAttribute('aria-controls'));
                    if (d) d.hidden = true;
                });
                btn.setAttribute('aria-expanded', String(!open));
                detail.hidden = open;
                // the enquiry CTA names whichever batch is open
                var cta = document.getElementById('batch-cta');
                if (cta) {
                    if (open) {
                        cta.textContent = 'Book a 3-day trial';
                        cta.setAttribute('href', cta.getAttribute('data-base'));
                    } else {
                        var label = btn.getAttribute('data-label');
                        cta.textContent = 'Ask about the ' + label + ' batch';
                        cta.setAttribute('href', cta.getAttribute('data-base') +
                            encodeURIComponent(' I am interested in the ' + label + ' batch.'));
                    }
                }
            });
        });

        /* ---------- classes: filter by group (user-triggered) ---------- */
        var filters = document.querySelectorAll('.filter');
        filters.forEach(function (f) {
            f.addEventListener('click', function () {
                var group = f.getAttribute('data-group');
                filters.forEach(function (o) { o.setAttribute('aria-pressed', String(o === f)); });
                document.querySelectorAll('.class-item').forEach(function (item) {
                    item.hidden = !(group === 'all' || item.getAttribute('data-group') === group);
                });
                var live = document.getElementById('filter-status');
                if (live) {
                    var n = document.querySelectorAll('.class-item:not([hidden])').length;
                    live.textContent = n + (n === 1 ? ' class' : ' classes') + ' shown';
                }
            });
        });

        /* ---------- enquiry form: composes a WhatsApp message ---------- */
        var form = document.getElementById('enquiry-form');
        if (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                var name = form.elements.name.value.trim();
                var phone = form.elements.phone.value.trim();
                var batch = form.elements.batch.value;
                var mode = form.elements.mode.value;
                var notes = form.elements.notes.value.trim();

                var msg = 'Hello Happy Yogis! I would like to book a 3-day trial.';
                if (name) msg += '\\nName: ' + name;
                if (phone) msg += '\\nPhone: ' + phone;
                if (batch) msg += '\\nPreferred batch: ' + batch;
                if (mode) msg += '\\nFormat: ' + mode;
                if (notes) msg += '\\nAnything to know: ' + notes;

                var note = document.getElementById('form-note');
                if (note) note.hidden = false;
                window.open('https://wa.me/919994247450?text=' + encodeURIComponent(msg), '_blank', 'noopener');
            });
        }

        /* ---------- gallery lightbox ---------- */
        var lb = document.getElementById('lightbox');
        if (lb) {
            var lbImg = document.getElementById('lightbox-img');
            var lbClose = document.getElementById('lightbox-close');
            var BLANK = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
            var opener = null;
            var lbTrap = makeTrap(lb);
            var webpOK = (function () {
                var c = document.createElement('canvas');
                return !!(c.getContext && c.toDataURL('image/webp').indexOf('data:image/webp') === 0);
            })();
            function openLb(t) {
                opener = t;
                document.addEventListener('keydown', lbTrap, true);
                lbImg.src = t.getAttribute(webpOK ? 'data-full-webp' : 'data-full');
                lbImg.alt = t.getAttribute('data-caption') || '';
                lb.classList.add('active');
                lb.setAttribute('aria-hidden', 'false');
                document.body.style.overflow = 'hidden';
                lbClose.focus();
            }
            function closeLb() {
                document.removeEventListener('keydown', lbTrap, true);
                lb.classList.remove('active');
                lb.setAttribute('aria-hidden', 'true');
                lbImg.src = BLANK;
                document.body.style.overflow = '';
                if (opener) { opener.focus(); opener = null; }
            }
            document.querySelectorAll('.gallery-item').forEach(function (t) {
                t.addEventListener('click', function () { openLb(t); });
            });
            lbClose.addEventListener('click', closeLb);
            lb.addEventListener('click', function (e) {
                if (e.target === lb || e.target === lbImg) closeLb();
            });
            document.addEventListener('keydown', function (e) {
                if (e.key === 'Escape' && lb.classList.contains('active')) closeLb();
            });
        }

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && menu.classList.contains('open')) closeMenu();
        });

        /* ---------- FAQ ---------- */
        document.querySelectorAll('.faq-item').forEach(function (item, i) {
            var q = item.querySelector('.faq-q'), a = item.querySelector('.faq-a');
            if (!q || !a) return;
            a.id = 'faq-a-' + i; q.id = 'faq-q-' + i;
            q.setAttribute('aria-controls', a.id);
            a.setAttribute('role', 'region');
            a.setAttribute('aria-labelledby', q.id);
            q.setAttribute('aria-expanded', 'false');
            a.hidden = true;
            q.addEventListener('click', function () {
                var open = q.getAttribute('aria-expanded') === 'true';
                q.setAttribute('aria-expanded', String(!open));
                a.hidden = open;
                item.classList.toggle('is-open', !open);
            });
        });

        /* ---------- reviews carousel ----------
           Auto-advances one screenful at a time. It holds while the pointer is
           over it, while focus is inside it and while the tab is hidden; it
           stops for good as soon as the visitor takes control (arrows, dots,
           a swipe, a key) or presses pause, and it never starts at all under
           prefers-reduced-motion. aria-live flips to polite whenever it is not
           rotating, so a screen reader hears changes the visitor caused. */
        var rev = document.querySelector('[data-rev]');
        if (rev) {
            var track = rev.querySelector('.rev-track');
            var dotBox = rev.querySelector('[data-rev-dots]');
            var toggle = rev.querySelector('[data-rev-toggle]');
            var pauseIcon = rev.querySelector('[data-rev-pause]');
            var playIcon = rev.querySelector('[data-rev-play]');
            var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
            var timer = null, dots = [], pages = 1, counter = null;
            var held = { user: false, hover: false, focus: false, hidden: false };

            var slides = [].slice.call(track.querySelectorAll('.rev-slide'));
            var clones = [];

            function pageOf(x) { return Math.round(x / track.clientWidth); }
            function perPage() {
                return Math.max(1, Math.round(track.clientWidth / slides[0].offsetWidth));
            }
            /* The page after the last one is a copy of the first, so the loop
               runs forwards off the end and is reset to the real first page
               once the scroll settles - on identical pixels, so the seam never
               shows. Copies are hidden from assistive tech. */
            function makeClones() {
                clones.forEach(function (c) { track.removeChild(c); });
                clones = [];
                for (var i = 0; i < Math.min(perPage(), slides.length); i++) {
                    var c = slides[i].cloneNode(true);
                    c.setAttribute('aria-hidden', 'true');
                    /* aria-hidden alone still leaves the copied links in the tab
                       order, so a keyboard user lands on a card no screen reader
                       will announce. inert covers modern browsers; the tabindex
                       pass covers the rest. */
                    c.inert = true;
                    [].forEach.call(c.querySelectorAll('a,button,[tabindex]'), function (el) {
                        el.setAttribute('tabindex', '-1');
                    });
                    c.removeAttribute('role');
                    c.removeAttribute('aria-roledescription');
                    c.removeAttribute('aria-label');
                    track.appendChild(c);
                    clones.push(c);
                }
            }
            /* Height of the cards on one page, measured at their natural size. */
            function fit(p) {
                if (p === undefined) p = curPage();
                if (p >= pages) p = 0;
                var per = perPage(), h = 0;
                track.classList.add('rev-measure');
                for (var i = p * per; i < Math.min(slides.length, p * per + per); i++) {
                    h = Math.max(h, slides[i].firstElementChild.offsetHeight);
                }
                track.classList.remove('rev-measure');
                track.style.height = h ? h + 'px' : '';
            }
            function onClonePage() { return track.scrollLeft >= pages * track.clientWidth - 2; }
            function curPage() {
                var p = pageOf(track.scrollLeft);
                return p >= pages ? 0 : Math.max(0, p);
            }
            /* scrollTo({behavior:'auto'}) defers to the CSS scroll-behavior,
               which is smooth here - so the seam reset would animate all the
               way back through every page. Drop the CSS rule for the one
               assignment instead; that jumps in every browser. */
            function jumpTo(px) {
                var prev = track.style.scrollBehavior;
                track.style.scrollBehavior = 'auto';
                track.scrollLeft = px;
                track.style.scrollBehavior = prev;
            }
            function goTo(p, jump) {
                p = Math.max(0, Math.min(pages - 1, p));
                if (onClonePage() && p === 0) jump = true;   /* already there */
                fit(p);
                if (jump) jumpTo(p * track.clientWidth);
                else track.scrollTo({ left: p * track.clientWidth, behavior: 'smooth' });
            }
            function mark() {
                var cur = curPage();
                if (counter) { counter.textContent = (cur + 1) + ' of ' + pages; return; }
                dots.forEach(function (d, i) {
                    if (i === cur) d.setAttribute('aria-current', 'true');
                    else d.removeAttribute('aria-current');
                });
            }
            function buildDots() {
                track.style.height = '';
                makeClones();
                pages = Math.max(1, Math.ceil(slides.length / perPage()));
                dotBox.textContent = '';
                dots = [];
                counter = null;
                /* One dot per page only works while each dot stays tappable.
                   At the 24x24 CSS px minimum a phone showing one review per
                   page would need a row of twelve, which is both unreadable
                   and wider than the screen - so past eight pages the row
                   becomes a plain "3 of 12" counter and the arrows move. */
                if (pages > 8) {
                    counter = document.createElement('span');
                    counter.className = 'rev-count';
                    dotBox.appendChild(counter);
                } else {
                    for (var i = 0; i < pages; i++) {
                        dots.push(dotBox.appendChild(makeDot(i)));
                    }
                }
                mark();
            }
            function makeDot(i) {
                var b = document.createElement('button');
                b.type = 'button';
                b.className = 'rev-dot';
                b.setAttribute('aria-label', 'Reviews ' + (i + 1) + ' of ' + pages);
                b.addEventListener('click', function () { takeOver(); goTo(i); });
                return b;
            }
            function sync() {
                var run = !reduce.matches && !held.user && !held.hover &&
                          !held.focus && !held.hidden;
                if (run && !timer) timer = setInterval(advance, 6000);
                if (!run && timer) { clearInterval(timer); timer = null; }
                track.setAttribute('aria-live', timer ? 'off' : 'polite');
                if (pauseIcon) pauseIcon.hidden = held.user;
                if (playIcon) playIcon.hidden = !held.user;
                toggle.setAttribute('aria-label',
                    held.user ? 'Play the reviews' : 'Pause the reviews');
            }
            function advance() {
                var p = pageOf(track.scrollLeft);
                if (p + 1 < pages) { goTo(p + 1); return; }
                fit(0);                                   /* the copy shows page one */
                track.scrollTo({ left: pages * track.clientWidth, behavior: 'smooth' });
            }
            /* The visitor is driving now - stop rotating and leave it stopped. */
            function takeOver() { held.user = true; sync(); }
            function step(d) {
                takeOver();
                var p = curPage() + d;
                goTo(p < 0 ? pages - 1 : p >= pages ? 0 : p);
            }

            rev.querySelector('[data-rev-prev]').addEventListener('click', function () { step(-1); });
            rev.querySelector('[data-rev-next]').addEventListener('click', function () { step(1); });
            toggle.addEventListener('click', function () { held.user = !held.user; sync(); });

            rev.addEventListener('pointerenter', function (e) {
                if (e.pointerType === 'mouse') { held.hover = true; sync(); }
            });
            rev.addEventListener('pointerleave', function (e) {
                if (e.pointerType === 'mouse') { held.hover = false; sync(); }
            });
            /* Focus inside the carousel holds it - except on the play/pause
               button itself, which focuses on click and would otherwise make
               pressing play do nothing. */
            rev.addEventListener('focusin', function (e) {
                held.focus = !toggle.contains(e.target); sync();
            });
            rev.addEventListener('focusout', function () {
                if (!rev.contains(document.activeElement)) { held.focus = false; sync(); }
            });
            document.addEventListener('visibilitychange', function () {
                held.hidden = document.hidden; sync();
            });
            track.addEventListener('touchstart', takeOver, { passive: true });
            track.addEventListener('wheel', takeOver, { passive: true });
            track.addEventListener('keydown', function (e) {
                if (e.key.indexOf('Arrow') === 0 || e.key === 'Home' || e.key === 'End') takeOver();
            });

            var scrolling = false, settled;
            track.addEventListener('scroll', function () {
                /* Off-screen cards can overflow the height we set; the track
                   clips them, but keep it pinned so nothing scrolls into view
                   vertically. */
                if (track.scrollTop) track.scrollTop = 0;
                clearTimeout(settled);
                settled = setTimeout(function () {
                    if (onClonePage()) jumpTo(0);
                    fit();
                }, 80);                                  /* after a swipe */
                if (scrolling) return;
                scrolling = true;
                requestAnimationFrame(function () { mark(); scrolling = false; });
            }, { passive: true });

            var resized;
            window.addEventListener('resize', function () {
                clearTimeout(resized);
                resized = setTimeout(function () { buildDots(); fit(); }, 150);
            });
            if (reduce.addEventListener) reduce.addEventListener('change', function () {
                toggle.hidden = reduce.matches; sync();
            });

            /* The quotes reflow whenever the stylesheet or the webfonts land -
               Tailwind compiles in the browser here, so that is after this
               script runs - and every reflow changes the height the track
               should be. Watch the quotes themselves: their height depends on
               the text and the width, never on the height we set, so this
               cannot feed back on itself. */
            function remeasure() { buildDots(); fit(); }
            if (window.ResizeObserver) {
                var settleFit;
                var ro = new ResizeObserver(function () {
                    clearTimeout(settleFit);
                    settleFit = setTimeout(remeasure, 60);
                });
                slides.forEach(function (sl) { ro.observe(sl.querySelector('blockquote')); });
            }
            window.addEventListener('load', remeasure);
            if (document.fonts && document.fonts.ready) document.fonts.ready.then(remeasure);

            buildDots();
            fit(0);
            toggle.hidden = reduce.matches;
            rev.classList.add('is-ready');
            sync();
        }

        /* ---------- scroll reveals ----------
           One fade per element, the first time it comes into view, then the
           observer lets it go. Opacity and transform only, so it stays on the
           compositor; anything above the fold is deliberately not marked. */
        var reveals = [].slice.call(document.querySelectorAll('.reveal'));
        if (reveals.length) {
            var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
            if (still || !window.IntersectionObserver) {
                reveals.forEach(function (el) { el.classList.add('is-in'); });
            } else {
                var io = new IntersectionObserver(function (entries) {
                    entries.forEach(function (e) {
                        if (!e.isIntersecting) return;
                        e.target.classList.add('is-in');
                        io.unobserve(e.target);
                    });
                }, { rootMargin: '0px 0px -8% 0px', threshold: .05 });
                reveals.forEach(function (el) { io.observe(el); });
                /* Nothing may stay invisible because the observer never fired.
                   A fast jump down the page, a script error further up, or a
                   render that never scrolls can all skip elements a reading
                   visitor would have triggered - and the failure mode is a
                   blank section, not a missing animation. After five seconds
                   everything shows regardless of where the reader is. */
                setTimeout(function () {
                    reveals.forEach(function (el) { el.classList.add('is-in'); });
                }, 5000);
            }
        }

        /* ---------- in-page links clear the fixed nav ---------- */
        /* Also catches "/#schedule": the homepage canonicalises as "/", so the
           nav points there rather than at index.html, and those links are
           same-page whenever the current path is already "/". */
        document.querySelectorAll('a[href^="#"], a[href^="/#"]').forEach(function (a) {
            a.addEventListener('click', function (e) {
                var href = a.getAttribute('href');
                var id = href.charAt(0) === '/' ? href.slice(1) : href;
                if (href.charAt(0) === '/' && location.pathname !== '/') return;
                if (id.length < 2) return;
                var t = document.querySelector(id);
                if (!t) return;
                e.preventDefault();
                window.scrollTo({
                    top: t.getBoundingClientRect().top + window.pageYOffset - navbar.offsetHeight - 8,
                    behavior: 'smooth'
                });
                t.setAttribute('tabindex', '-1');
                t.focus({ preventScroll: true });
            });
        });
    })();
    </script>
</body>
</html>
"""
