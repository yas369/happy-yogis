# Happy Yogis Yoga Centre — website

Static site for Happy Yogis Yoga Centre, SSM Nagar, New Perungalathur, Chennai.
No build step: open `index.html`, or serve the folder with
`python3 -m http.server` and visit <http://localhost:8000>.

```
index.html                            Home
yoga-classes-perungalathur.html       Location page - Perungalathur
yoga-classes-tambaram.html            Location page - Tambaram
blog.html                             Journal index
what-happens-in-your-first-...html    Journal post
privacy-policy.html                   Privacy policy
terms-of-service.html                 Terms of service
robots.txt / sitemap.xml              Crawl rules + sitemap
site.webmanifest                      Add-to-home-screen metadata
```

## Confirmed business facts

These were confirmed by the owner and must not be changed without asking:

- **Four batches, Monday to Friday:** 5:30–6:15 am (45 min) · 6:15–7:15 am ·
  10:00–11:00 am (**women only**) · 5:00–6:00 pm. There is no 8–9 am batch.
- **Opening hours 5:30 am – 7:00 pm**, Mon–Fri. Closed weekends and public holidays.
- **A 3-day trial. The price is deliberately not published anywhere on the site**,
  and no fees of any kind appear on the site.
- T-shirt provided to every student · mats can be left at the centre · online and
  in-person both offered, and students may switch between them.
- **No social media links.** `sameAs` was removed from the schema at the owner's
  instruction — do not re-add unverified profiles.

## One centre

Happy Yogis has a **single centre**, in SSM Nagar, New Perungalathur. There are
no branches. The homepage "Areas we teach" section, both location pages and the
LocalBusiness schema all say this explicitly — please keep it that way, because
a page that reads like a Tambaram branch is both misleading to visitors and a
Google Business Profile problem (you can only verify a location you occupy).

The neighbourhood list on the homepage is what it says it is: where students
travel in from, not places we teach.

## Location pages

The two location pages exist to rank for "yoga centre in Tambaram" and "yoga
classes in Perungalathur" while being clear there is one centre. Google only
ranks these if they say genuinely different things, so **do not** duplicate one
to make a third area page.

If you add another area (Chromepet, Selaiyur, Guduvanchery…), give it:

- its own `<h1>`, `<title>` and meta description naming that area
- at least 250 words that are actually specific to it — how students get here
  from there, which batch suits that commute, which landmarks are nearby
- its own entry in `sitemap.xml`, in the homepage "Areas we teach" section,
  and in the footer
- a `BreadcrumbList` in the JSON-LD, copying the pattern from an existing
  location page

A thin page that just swaps the place name is worse than no page at all.

## Things to verify or replace

These carried over from the previous version of the site and are worth a check:

- **Student quotes** are now real Google reviews supplied by the owner. Of the
  50 pasted in (all five stars), only 25 have complete written text — 12 are
  rating-only, 7 are Google's old "Positive / Quality" attribute tags, and 4
  are truncated with "… More". The 12 shown are curated from the complete ones
  and quoted as written. **Never quote a truncated review**, and never invent
  one. To refresh them, edit `REVIEWS` in the page source.
- The reviews are a **carousel**: a scroll-snap track, two cards at a time from
  768px and one below that, so it swipes natively on touch and scrolls with the
  arrow keys. It loops seamlessly — the script appends a copy of the first page
  after the last, scrolls forward onto it, then resets to the real first page on
  identical pixels. That reset must not use `scrollTo({behavior:'auto'})`:
  `auto` defers to the CSS `scroll-behavior`, which is `smooth` here, and the
  carousel visibly rewinds through every page. `jumpTo()` drops the CSS rule for
  the one assignment instead. The script sets the track's height to the cards actually in view,
  which is why one very long quote does not leave a dead band under every short
  one. Without JavaScript the track is still a scrollable row of all 12 quotes
  and the controls stay hidden — nothing is hidden behind the script.
- **No `AggregateRating` or `Review` schema is emitted, deliberately.** These
  reviews live on the centre's Google profile; marking them up here and feeding
  them back to Google is self-serving review markup, which its guidelines
  prohibit and which risks a manual action. The star rating you want in search
  results comes from the Google Business Profile itself, not from this site.
- `REVIEW_COUNT_CLAIM` says "More than 45" rather than an exact figure, so it
  stays true as reviews accumulate. Update it if the count ever drops.
- **Social links** in the JSON-LD (`instagram.com/happyyogis`,
  `facebook.com/happyyogis`, `youtube.com/happyyogis`) are unverified. Wrong
  `sameAs` links weaken Google's entity matching — fix or remove them.
- **`instructor.jpeg` / `instructor.webp`** are still in the repo but no longer
  used on any page. The photo is a night-time personal portrait, which reads
  poorly in a "your teacher" section, so the teacher block currently uses a
  class photo instead. Drop in a proper portrait of Karthika teaching and wire
  it back into the `#trainer` section.
- **Geography** on the location pages (GST Road, Perungalathur railway station,
  one stop from Tambaram) is written from your own map coordinates. Read it
  once and correct anything that is off — no travel times or distances are
  claimed, deliberately.

## Deployment assumption

The site is served from **`https://happyyogis.in/`**. That domain is set in
exactly one place — `BASE` in the page generator — and every canonical,
`og:url`, `og:image`, JSON-LD `@id`/`url` and breadcrumb `item` is built from
it, so a domain change is a one-line edit plus a rebuild. The two files that do
not come from the generator are `robots.txt` (its `Sitemap:` line) and
`sitemap.xml`, which is generated by its own script — see below. Icon, manifest
and asset links are relative, so those survive a move to a subfolder.

The site was originally built against `happyyogis.com`, which **is not a domain
this business owns** — it was wrong from the first commit. Every canonical,
`og:url` and JSON-LD `@id` pointed at it, which tells Google the real copy of
each page lives on someone else's domain. There is nothing to redirect; the
references were simply a mistake, and `validate.py` now fails the build if a
second domain ever appears across the pages, the sitemap and `robots.txt`.

URLs are **non-`www`** and keep their `.html` endings, matching what the host
serves without a redirect. A sitemap entry that redirects still works, but
Search Console flags every one of them, so if the host form ever changes, this
file and the canonicals change with it.

## The sitemap

`sitemap.xml` is generated, not hand-edited. It reads each page's own
`<link rel="canonical">` for the `<loc>`, so the sitemap can never disagree
with a page about its URL, and it skips any page marked `noindex`. A page's
`<lastmod>` only moves when that page actually changed since the last commit —
restamping every URL on every build is how a sitemap teaches Google to ignore
`lastmod` altogether. Image entries list the full-size photographs on each page,
titled with the alt text written from the real photo.

Adding a page means adding it to the `PAGES` list in the generator (with a
priority and change frequency) and re-running it. Submit the sitemap once at
<https://happyyogis.in/sitemap.xml>; after that Google re-reads it on its own.

## Images

Each source photo has four committed derivatives:

| File | Purpose | Size |
| --- | --- | --- |
| `imaN.jpeg` / `imaN.webp` | full size — hero, section images, lightbox | ≤ 1280px long edge |
| `imaN-sm.jpg` / `imaN-sm.webp` | gallery tiles | 640px wide, natural height |

The gallery thumbnails keep each photo's **natural aspect ratio** — the source
photos range from a 0.75 portrait to a 2.22 panorama, and an earlier version
cropped them all to one fixed tile, which cut people out of frame. The gallery
is a CSS multi-column masonry, so mixed shapes flow without any cropping. When
you add a photo, generate the thumbnail at 640px wide and let the height fall
where it does — do not crop it to match the others.

Pages use `<picture>` so WebP is served where supported, every `<img>` carries
`width`/`height` to prevent layout shift, and the lightbox feature-detects WebP
and loads `data-full-webp` where it can.

Originals as first uploaded are in git history (commits `b7e4024`, `a891652`).

## Icons

Icons are an inline SVG sprite at the top of each `<body>`, generated from
[lucide-static](https://lucide.dev) v1.38.0 (ISC). There is no icon JavaScript.
The homepage uses eight icons; earlier versions used thirty-five, most of them
decorative chips on cards. Keep it lean — an icon should mean something
(phone, location, time), not just fill space.

To add one: paste the `<symbol id="i-NAME" viewBox="0 0 24 24">…</symbol>` into
that page's sprite, then:

```html
<svg class="lucide w-5 h-5" aria-hidden="true" focusable="false">
  <use href="#i-NAME"></use>
</svg>
```

## Styling

Tailwind loads from the Play CDN, which compiles classes in the browser — zero
friction to edit, but it ships the compiler to every visitor. A purged build of
this site is about **23 KB minified** versus roughly 400 KB of CDN JavaScript:

```bash
npm install -D tailwindcss@3
npx tailwindcss -c tailwind.config.js -i src.css -o styles.css --minify
```

with `content: ['./*.html']` and the colour/font `theme.extend` block copied
from the inline `tailwind.config` script, then swap the CDN `<script>` for
`<link rel="stylesheet" href="styles.css">`. Trade-off: after that, new utility
classes only work once you re-run the build.

## House style

Type is **Instrument Serif** (every heading and the wordmark, via the `display`
class) and **Inter** (body copy and UI). Two families, no third. Colour tokens
are unchanged: `ink #16202b` · `blue #1F4E79` · `sky #4DA8DA` · `sand #F6F3EE` ·
`paper #FBFAF8` · `line #E4E0D9` · `muted #6B7480`.

**Instrument Serif ships one weight (400).** Never put `font-bold`,
`font-semibold` or `font-medium` on a heading or on anything carrying
`display` — the browser fakes the weight and it looks smeared. Scale and
spacing carry the emphasis instead; `text-d1`/`d2`/`d3` are fluid `clamp()`
sizes, so they adapt without breakpoint jumps.

Sections are laid out asymmetrically rather than as centred bands: the hero
runs a large serif headline and the class photograph down the left with the
live schedule held to the right, and the health and visit blocks are **bento
grids** — a 1px grid gap over the rule colour draws the dividers, which is how
tiles separate here without a single shadow. Use `.bento` for that; do not add
a bento to a section that reads better as a list (the classes list filters, so
it stayed a list).

The design deliberately avoids the generic template look. Please keep to this:

- **no eyebrow labels** — no small tracked-out all-caps line above headings
- **no shadows anywhere** — surfaces separate with a 1px `border-line` rule or a
  change of ground colour (`bg-sand` against `bg-paper`)
- no icon chip on every card; an icon must mean something
- **no arrows appended to buttons** — an arrow only on a link that leaves the site
- no numbered markers unless the content is genuinely a sequence (the legal pages
  number their clauses, which is a real sequence)
- real photos of real classes, never stock photography
- plain, specific copy; concrete beats aspirational

**Motion:** three kinds, and no more.

1. The "next class today" line in the hero resolving on load.
2. **Scroll reveals** — one fade-and-lift per element the first time it enters
   view, then the observer releases it. Opacity and transform only. Mark an
   element with `class="reveal"` and stagger a group with `style="--d:90ms"`.
   The rule is gated on `.js` (set by a one-line script in `<head>`), so
   nothing is ever hidden when the script does not run, and the whole thing is
   disabled under `prefers-reduced-motion`. **Never mark hero content** — the
   first screen must not wait on a script.
3. The reviews carousel advancing, which earns it by being controllable (see
   below).

Everything else responds to a real action: expanding a batch, filtering
classes, opening the menu, submitting the form.

## The hero schedule panel

The hero is built around the schedule rather than around a headline. The panel
reads the visitor's clock and names the next batch; on a weekend or after the
last class it points at the next weekday morning. Selecting a batch expands it
and rewrites the call to action to name that batch.

If you change a batch time, update `BATCHES` — the 24-hour `data-start` value on
each row is what the next-class logic reads, so it must match the label.

## The enquiry form

The form does not post anywhere. On submit it composes a WhatsApp message from
the fields and opens `wa.me` — nothing is stored on the site and nothing reaches
you until the visitor presses send in WhatsApp. That trade-off is deliberate (no
third-party service, no signup), but it does mean **abandoned submissions are
lost**. If you later want every submission captured, Vercel supports form
handling and the privacy policy would need revisiting.

The optional health box is covered by a dedicated clause in the privacy policy —
if you change what the form collects, update that clause too.

Keep one `<h1>` per page, heading levels in order, `alt` text that describes the
actual photo (`alt=""` for decorative logos), `aria-expanded` in sync on the FAQ
and menu toggles, and the `prefers-reduced-motion` block in the page `<style>`.

Header and footer are duplicated across all five pages — if you change one,
change them all.
