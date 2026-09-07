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

## Deployment

Live at **https://mtlbook8-stack.github.io/MOMENTUM-LINK-NEW/**

Hosted on GitHub Pages from this repository. Pushing to `main` runs
`.github/workflows/deploy.yml`, which uploads `site/` and publishes it — there is no
manual publish step. To update the live site:

```bash
python build.py
git add -A && git commit -m "Update content" && git push
```

The deploy takes about a minute; watch it under the repository's Actions tab.

To move to a custom domain later, add the domain in the repository's Pages settings,
set `BASE_URL` in `build.py` to it, and rebuild so the canonical URLs and sitemap follow.

## Still to do before this is a real public site

- Replace the placeholder email addresses (`…@momentumlink.example`) and the
  `+1 (000) 000-0000` phone number — they came from the design and are not real.
- Point the contact form at a real endpoint (see above); until then it falls back to
  opening the visitor's email client.

## What the JavaScript does

`site/assets/js/site.js` is progressive enhancement — every page is fully readable and
navigable with JavaScript disabled. It adds:

- the mobile menu, and the reading-progress bar under the header;
- the pinned scroll sequence on the home hero — which opens on a composed frame (a
  dimmed blurred field of the same picture, a pool of light, a hairline border and a
  plate caption) that clears within the first 15% of the scroll, leaving the original
  choreography untouched; falls back to a static hero without JS or under
  `prefers-reduced-motion`;
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

## The practice as a process

The six steps read as a journey along a timeline. A thread runs the full height of the
viewport beside them, sticky while you scroll: six round, cropped stills strung on a
3px line, with the travelled portion drawn in blue behind you.

**One step is open at a time.** The step nearest the reading line is the open one — its
node swells on the thread and its panel projects out of that circle into the column
alongside. Reaching the next step folds the current panel back into its own circle
before the next one projects, so the page reads project, fade, project, rather than
having two panels open at once. The panel's `transform-origin` is set from its node's
live position each scroll pass, so it genuinely grows out of that circle rather than
from a fixed corner. Clicking a node jumps to its step.

On a phone the thread lies down under the header — the same nodes on a horizontal
line, the same one-at-a-time projection.

Activation is computed in the shared scroll pass (`initProcess()` in `site.js`) rather
than from an observer, so a step is never left collapsed and unreadable if callbacks
are throttled. Under `prefers-reduced-motion` every panel is simply open.

## The technology deck

The seventeen disciplines are a deck of cards rather than a grid of equal squares.
One card faces up; the stack fans behind it. The automatic tick riffles the whole deck —
the top nine cards spread into an arc wide enough to read several faces at once,
hold for a beat, then collapse back with the next card on top (five cards on a
phone, sized from the deck's own width so the spread never pushes the page sideways).

- **Left alone it deals itself**, advancing every 4.2s.
- **It holds still whenever someone is reading**: on hover, on keyboard focus, when
  scrolled out of view, on a background tab, or when paused with the Pause button.
- **Click, swipe or ← →** to take it over — a manual move is a plain, quick change of
  card, with no fan; the flourish belongs to the automatic tick. The idle countdown
  restarts after each one.
- **"See all 17"** drops back to the plain grid — which is also exactly what someone
  with JavaScript disabled gets, so no card is ever unreachable.
- Under `prefers-reduced-motion` the fan and the auto-advance are both skipped; the
  deck still works, it just cuts straight to the next card.

Geometry and timings are `fanGeometry()` / `shuffle()` in `initDeck()` (`site.js`);
the styles are under *Card deck* in `site.css`.

## Images

The source PNGs were 92.7 MB. `build-media.py` regenerates the `site/media` folder as
WebP with JPEG fallbacks at two widths (1536 and 768); pages request the right size via
`srcset`/`sizes`, so a phone downloads roughly a quarter of what a desktop does.

```bash
python build-media.py src/media site/media
```

`src/` holds the original canvas export and its PNGs. It is gitignored (89 MB), so it
lives only in your local copy — keep it if you want to re-encode the artwork later. The
generated `site/media` files are committed, so the repository alone is enough to deploy.

## Page grounds

The cream is the constant; each page carries a different texture over it, drawn from
the same palette and kept far enough back to read as paper rather than decoration:

| Page | Ground |
|---|---|
| Home | Pools of light — the blue and rust washes the hero opens on |
| Practice | Planning paper — a fine grid with a heavier rule every fifth cell, under a light gradient |
| Industries | A drawing-board hatch |
| Technology | A schematic dot grid |
| Contact | A single wash falling off the dark hero |

All five share a fine paper grain, and the dark bands (stats, footer) carry a soft blue
gradient so they are not flat slabs against it. Each page is tagged `data-page` on
`<body>`; the rules live under *Page grounds* in `site.css`.

The whole ground is painted on one fixed pseudo-element behind the content rather than
with `background-attachment: fixed`, which forces a full repaint on every scroll — this
site does enough scroll work already. That is why the cream sits on `<html>` and `<body>`
is transparent.

## Accessibility and SEO notes

Skip link, keyboard-operable navigation and overlay, visible focus rings, labelled form
fields with live error messages, alt text on content images, `aria-current` on the active
nav item, per-page titles and meta descriptions, Open Graph tags, sitemap and robots.
Respects `prefers-reduced-motion`.
