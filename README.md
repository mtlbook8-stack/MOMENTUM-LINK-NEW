# Momentum Link Professionals — website

A working static website built from the `Multi-page website design.zip` canvas export.
The original was a single design-canvas file that simulated five pages with an internal
template language; this is real HTML, CSS and JavaScript with five separate URLs.

## What to deploy

Deploy the **`site/`** folder. It is plain static files — no build step, no server code.
It works on Netlify, Vercel, GitHub Pages, Cloudflare Pages, S3, or any web host.

```
site/
  index.html          Home
  practice.html       The practice — six steps
  industries.html     Five sectors, with #anchors per sector
  technology.html     Seventeen disciplines
  contact.html        Contact details and brief form
  404.html            Not-found page
  sitemap.xml, robots.txt, favicon.svg
  assets/css/site.css
  assets/js/site.js
  media/              168 images (WebP + JPEG, 1536w and 768w)
```

## Running it locally

```bash
python -m http.server 8123 --directory site
```

Then open <http://localhost:8123>. Opening `index.html` directly from the file system
also works, but a server is closer to production.

## Editing content

Copy lives in **`build.py`**, not in the HTML — the practice steps, sectors, technology
list, stats, contact details and form fields are Python data structures at the top of
the file. Change them there and regenerate:

```bash
python build.py
```

This rewrites the five pages plus `404.html`, `sitemap.xml`, `robots.txt` and the favicon.
Editing the HTML directly works too, but the next `build.py` run overwrites it.

Presentation slides are the exception: they are in `site/assets/js/site.js` (`SLIDES`),
because the overlay is built in the browser.

## Making the contact form send

The form validates in the browser and then does one of two things:

- **No endpoint configured (current state):** it opens the visitor's email client with
  the brief pre-filled, addressed to `hello@momentumlink.example`.
- **Endpoint configured:** it POSTs the fields as `FormData` and shows a success or
  failure message without leaving the page.

To switch it on, set the endpoint on the `<form>` in `build.py` (`build_contact`, the
`data-endpoint` attribute) and rebuild:

```html
<form ... data-endpoint="https://formspree.io/f/yourid" ...>
```

Any service that accepts a `multipart/form-data` POST works (Formspree, Basin, Netlify
Forms, or your own handler). Fields sent: `name`, `organisation`, `sector`, `email`,
`message`.

**Replace the placeholder contact details before going live** — the email addresses
(`…@momentumlink.example`) and phone number in `build.py` are the design's placeholders,
not real ones.

## Before launch

- Set `BASE_URL` in `build.py` to the live origin (e.g. `https://momentumlink.com`) and
  rebuild — this fills in canonical URLs, Open Graph URLs and `sitemap.xml`.
- Replace the placeholder email addresses and phone number.
- Point the contact form at a real endpoint.

## What the JavaScript does

`site/assets/js/site.js` is progressive enhancement — every page is fully readable and
navigable with JavaScript disabled. It adds:

- the mobile menu, and the reading-progress bar under the header;
- the pinned scroll sequence on the home hero (falls back to a static hero without JS
  or under `prefers-reduced-motion`);
- scroll reveals, with a failsafe sweep so nothing is ever stranded invisible;
- the expanding sector accordion on the home page (see below);
- the presentation overlay — 12 slides, autoplay, arrow keys, Space to pause,
  Esc to close, focus trapped while open and restored on close;
- contact form validation and submission.

## The sector accordion (home page)

An expanding image accordion — five photo panels sharing one flex container. The
active panel takes `flex: 3.4` while the other four fall to `flex: 1`, with the flex
value itself transitioned over `.95s cubic-bezier(.19, 1, .22, 1)` so the sizes glide
instead of snapping. Inside, the image counter-scales `1.18 → 1.04` (and `.55 → 1`
opacity) so it settles rather than smears, the caption cross-fades up from 26px, and
the spine label rotates out as it fades.

The same mechanic runs on both axes — only the orientation changes:

| | Desktop (>900px) | Mobile (≤900px) |
|---|---|---|
| Container | flex row | flex column |
| Panel grows | width, 158px → 537px | height, 88px → 299px |
| Collapsed floor | `min-width: 56px` | `min-height: 58px` |
| Spine label | vertical (`writing-mode: vertical-rl`) | horizontal |
| Trigger | hover | first tap expands, second follows the link |

Ratio, easing, duration and counter-scale are shared; the mobile rules in the
`max-width: 900px` block only swap the axis, the label orientation and the hint text.
Keyboard focus expands a panel on both. Styles live under *Sector panels* in
`site.css`; the trigger logic is `initPanels()` in `site.js`.

## Images

The source PNGs were 92.7 MB. `build-media.py` regenerates the `site/media` folder as
WebP with JPEG fallbacks at two widths (1536 and 768); pages request the right size via
`srcset`/`sizes`, so a phone downloads roughly a quarter of what a desktop does.

```bash
python build-media.py src/media site/media
```

`src/` holds the original canvas export and its PNGs. It is not part of the deployed
site — keep it if you want to re-encode the artwork later, delete it otherwise.

## Accessibility and SEO notes

Skip link, keyboard-operable navigation and overlay, visible focus rings, labelled form
fields with live error messages, alt text on content images, `aria-current` on the active
nav item, per-page titles and meta descriptions, Open Graph tags, sitemap and robots.
Respects `prefers-reduced-motion`.
