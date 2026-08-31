# Happy Yogis Yoga Centre — website

Static marketing site for Happy Yogis Yoga Centre, SSM Nagar, New Perungalathur,
Chennai. No build step is required to work on it: open `index.html` in a browser,
or serve the folder with `python3 -m http.server` and visit
<http://localhost:8000>.

```
index.html              Home page (all sections)
privacy-policy.html     Privacy policy
terms-of-service.html   Terms of service
robots.txt              Crawl rules + sitemap pointer
sitemap.xml             URL + image sitemap
site.webmanifest        PWA / "add to home screen" metadata
```

## Deployment assumption

Every canonical URL, `og:` tag and sitemap entry assumes the site is served from
the **domain root** of `https://happyyogis.com/`. If the domain ever changes, or
the site moves to a subfolder, update:

- `<link rel="canonical">` and the `og:url` / `twitter:` tags in all three pages
- the `@id` / `url` fields in the JSON-LD block of each page
- every `<loc>` in `sitemap.xml` and the `Sitemap:` line in `robots.txt`

Icon and manifest links are **relative**, so those keep working from a subfolder.

## Images

Photos are the centre's own. Each source photo has four derivatives, all
committed:

| File | Purpose | Size |
| --- | --- | --- |
| `imaN.jpeg` / `imaN.webp` | full size — hero, bento, lightbox | ≤ 1280px long edge |
| `imaN-sm.jpg` / `imaN-sm.webp` | gallery tiles (rendered 288×192) | 640×427 |

Markup uses `<picture>` so WebP is served where supported with a JPEG fallback,
and every `<img>` carries explicit `width`/`height` to prevent layout shift.

**Adding a photo:** drop the original in, generate the four derivatives at the
sizes above, and add a tile to *both* halves of a gallery track in `index.html`.
Each `.scroll-gallery-track` must contain **exactly two identical copies** of its
photo sequence — the CSS marquee animates to `translateX(-50%)`, so if the halves
differ the loop visibly jumps. The second copy carries `aria-hidden="true"` and
`tabindex="-1"` so screen readers and keyboard users see each photo once.

The originals as first uploaded remain in git history (commits `b7e4024`,
`a891652`) if a larger crop is ever needed.

## Icons

Icons are an inline SVG sprite at the top of each `<body>`, generated from
[lucide-static](https://lucide.dev) v1.38.0 (ISC). There is no icon JavaScript at
runtime.

To use an icon: add `<symbol id="i-NAME" viewBox="0 0 24 24">…</symbol>` to that
page's sprite (copy the inner markup from the lucide-static package), then
reference it:

```html
<svg class="lucide w-5 h-5" aria-hidden="true" focusable="false">
  <use href="#i-NAME"></use>
</svg>
```

Each page's sprite holds only the symbols that page actually uses. Stroke styling
comes from the `svg.lucide` rule in the page `<style>`; add `fill-current` for a
solid icon (used by the testimonial stars).

## Styling

Tailwind is loaded from the Play CDN (`cdn.tailwindcss.com`), which compiles
utility classes in the browser. That keeps editing friction at zero — you can add
any Tailwind class to the HTML and it just works — at the cost of shipping the
compiler to every visitor.

**Recommended upgrade.** A purged, prebuilt stylesheet for this site is about
**24 KB minified**, versus roughly 400 KB of CDN JavaScript, and removes a
render-blocking script:

```bash
npm install -D tailwindcss@3
npx tailwindcss -c tailwind.config.js -i src.css -o styles.css --minify
```

with `content: ['./*.html']` and the existing colour/font `theme.extend` block
copied out of the inline `tailwind.config` script. Then replace the CDN
`<script>` with `<link rel="stylesheet" href="styles.css">`.

The trade-off: after that change, **new utility classes only appear once the
build is re-run**, so it is worth doing when someone is comfortable running the
command after each edit.

## Accessibility notes

Please keep these when editing:

- one `<h1>` per page, heading levels never skipping a step
- `alt` text that describes the actual photo (empty `alt=""` for decorative logos)
- decorative background `<div>`s marked `aria-hidden="true"`
- the skip link, `<header>` / `<main>` / `<footer>` landmarks
- `aria-expanded` kept in sync on the FAQ toggles and mobile menu button
- the `prefers-reduced-motion` block in the page `<style>`, which stops the
  marquees and float animations for visitors who ask for reduced motion
