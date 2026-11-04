# Source for happyyogis.in

**The `.html` files in the repository root are generated. Do not edit them.**
Change things here and rebuild, or your edit is overwritten on the next build.

Until now this source lived only in a temporary directory, which meant the site
was one container restart away from being maintainable by hand-editing 25
machine-generated files. That is why it is here.

## Build it

```bash
cd src
npm install          # once: tailwindcss, playwright, axe-core
npm run build        # regenerates every page into the repo root
npm run check        # validate: links, canonicals, schema, sitemap, dates
```

`npm run build` runs two passes, which is the one non-obvious thing about it.
Tailwind needs the markup to know which classes to keep, and the markup needs
the compiled CSS to inline. So `buildall.py`:

1. generates every page with no CSS,
2. runs the Tailwind CLI over *that* output,
3. generates again with the result inlined.

Compiling from the CSS-free pass matters. If Tailwind scanned markup that
already carried its own output it would read selectors like `.text-muted` back
out of the stylesheet as class names, and each build would drift from the last.

## Where things are

| File | What it holds |
|---|---|
| `build.py` | The shared shell: `<head>`, nav, footer, the whole stylesheet, the page JS |
| `content.py` | Batch times, the reviews, FAQs, photo captions, area pages |
| `pages.py` | Home and the area pages, plus the shared `photo()` helper |
| `blog.py` | Every English post, its sources and the health disclaimer |
| `posts_more.py` | Four further English posts, split out to break an import cycle |
| `legal.py` | Privacy policy and terms |
| `ta_strings.py` | All Tamil interface copy |
| `ta_posts.py` | Tamil post bodies |
| `ta_pages.py` | Builds every Tamil page from the above |
| `sitemap.py` | `sitemap.xml`, including the image entries |
| `validate.py` | The build guard — run it before committing |
| `make_portrait.py` | Teacher portraits: `<source> <stem>` → 4:5 at 720/560/300 |
| `tw.config.js` | Colour tokens, the display/body faces and the type scale |

Design changes usually belong in **two** places: the colour tokens and type
scale in `tw.config.js`, and the hand-written CSS at the top of `build.py`.
The `:root` block there mirrors the Tailwind tokens and is read by the
components written by hand — the review carousel, the FAQ, the mobile menu,
the lightbox. If the two ever disagree, those components silently keep the old
palette while everything class-driven moves on.

The site is **near-white**: `paper` is `#FAFCFE` and `sand` `#EEF4F9`. Two
things follow from that and are easy to undo by accident.

- **`line` did not lighten with them.** A hairline at `#E2EAF1` measures
  1.18:1 against the new paper, which is a rule nobody can see. Held at
  `#D3E0EA` it reads 1.31:1, so the rules got *crisper* as the grounds got
  lighter. Lighten `line` and the whole grid quietly disappears.
- **Text at `ink/60` now fails.** It composites to 4.17:1 on the new paper.
  Nothing on the site goes below `ink/70` (5.75:1); keep it that way.

## Checks

```bash
npm run serve    # in one terminal, serves the repo root on :8123
npm run axe      # 25 pages x 2 widths, WCAG 2.0/2.1 A and AA
npm run mobile   # overflow, tap targets, text size, iOS input zoom
npm run align    # content-rail alignment and grid consistency
npm run perf     # LCP/FCP/CLS on a throttled Moto G Power profile
```

Two things the checks get wrong if you write your own:

- **Reveal before auditing.** `.reveal` elements sit at `opacity: 0` until
  scrolled to, and axe skips anything invisible — so an audit that does not
  force them visible silently ignores most of the page.
- **Kill transitions first.** Otherwise axe samples a half-faded colour and
  reports contrast failures that exist only mid-animation.

`checks/axeall.js` does both; copy from it.

## Things that will bite

- **Fonts are self-hosted and subset.** `subset.py` cuts Cormorant to the
  characters the site actually sets. If you add a glyph outside that set —
  a currency symbol, an accented name in a heading — it will fall back
  silently. Re-run `getfonts.py` then `subset.py`.
- **A preload must resolve to the same file as its `srcset`.** They drifted
  apart once and every phone downloaded the hero twice, one of them wasted.
  The home hero's width is now a single constant, `HERO_SIZES` in `pages.py`,
  which both the `<link rel=preload>` and the `<picture>` use. The English
  page preloads it and the Tamil page does not, because measurement says the
  Tamil largest paint is the headline, not the photograph.
- **Tamil sets wider than Latin** at the same size, so its headings have their
  own smaller steps in `build.py`. Long compounds otherwise overflow their
  column and scroll the page sideways.
- **The sitemap's image entries come from the markup, not from a list of
  filenames.** They used to be matched by a regex anchored on the filename,
  which went wrong silently twice: a leading slash stopped it matching, so
  every Tamil page advertised no images at all, and the teacher portrait was
  renamed to `instructor-portrait.jpeg`, after which the `instructor` branch
  matched nothing. Both were invisible because `validate.py` only checked an
  image's *basename* against the site root. It resolves the full path now.
- **The Tamil pages carry English `alt` text on their photographs** - 32 of
  their 34 image entries. `P.photo()` reads `C.PHOTOS`, which is English
  only, so a Tamil reader on a screen reader hears English descriptions.
  Fixing it means Tamil captions for the ten gallery photographs, which wants
  a native speaker rather than a machine.

## Not in here

`vercel.json` (redirects and cache headers), the images and the fonts live in
the repository root, because they are served rather than built.
