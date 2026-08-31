# Happy Yogis Yoga Centre — website

Static site for Happy Yogis Yoga Centre, SSM Nagar, New Perungalathur, Chennai.
No build step: open `index.html`, or serve the folder with
`python3 -m http.server` and visit <http://localhost:8000>.

```
index.html                        Home
yoga-classes-perungalathur.html   Location page - Perungalathur
yoga-classes-tambaram.html        Location page - Tambaram
privacy-policy.html               Privacy policy
terms-of-service.html             Terms of service
robots.txt / sitemap.xml          Crawl rules + sitemap
site.webmanifest                  Add-to-home-screen metadata
```

## Location pages

The two location pages exist to rank for "yoga centre in Tambaram" and "yoga
classes in Perungalathur". Google only ranks these if they say genuinely
different things, so **do not** duplicate one to make a third area page.

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

- **Student quotes** in the "What students say" section must be real. If they
  cannot be attributed to actual students, remove them and use Google reviews
  instead — invented testimonials are both a trust problem and, for reviews,
  a legal one.
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

Canonicals, `og:` tags and sitemap entries assume the domain root
`https://happyyogis.com/`. If that changes, update the canonical/`og:url` tags
and JSON-LD `@id`/`url` values in each page, plus every `<loc>` in
`sitemap.xml` and the `Sitemap:` line in `robots.txt`. Icon, manifest and asset
links are relative, so those survive a move to a subfolder.

## Images

Each source photo has four committed derivatives:

| File | Purpose | Size |
| --- | --- | --- |
| `imaN.jpeg` / `imaN.webp` | full size — hero, section images, lightbox | ≤ 1280px long edge |
| `imaN-sm.jpg` / `imaN-sm.webp` | gallery tiles | 640×427 |

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

The design deliberately avoids the generic template look:

- no coloured "eyebrow" pill above every heading — use the `.kicker` label
- no icon chip on every card
- no blurred gradient blobs, shimmer buttons or glassmorphism
- real photos of real classes, never stock photography
- plain, specific copy; concrete beats aspirational

Keep one `<h1>` per page, heading levels in order, `alt` text that describes the
actual photo (`alt=""` for decorative logos), `aria-expanded` in sync on the FAQ
and menu toggles, and the `prefers-reduced-motion` block in the page `<style>`.

Header and footer are duplicated across all five pages — if you change one,
change them all.
