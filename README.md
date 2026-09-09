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

## The contact form

Both forms — the one on the contact page and the one in the Get in touch modal —
are built from `contact_form()` in `build.py`, so they cannot drift apart. They post
to Web3Forms, which emails the submission to the address the key is registered to.

The access key lives in `build.py`:

```python
WEB3FORMS_KEY = "9cf20289-3ef2-48a5-9e5a-fce82434f151"
```

It is a publishable key by design — Web3Forms keys sit in client-side HTML and only
allow submitting to the inbox they are bound to. Clearing it makes both forms fall
back to opening the visitor's mail client, so a message is never silently dropped.

Fields sent: `name`, `organisation`, `sector`, `email`, `message` from the contact
page; `name`, `email`, `message` from the modal. A hidden `botcheck` honeypot goes
with them.

## Deployment

Two workflows live in `.github/workflows`:

| Workflow | Target | Needs |
|---|---|---|
| `azure-static-web-apps.yml` | Azure Static Web Apps — the real site | `AZURE_STATIC_WEB_APPS_API_TOKEN` secret |
| `deploy.yml` | GitHub Pages — the staging copy | nothing |

Both publish the `site/` folder on a push to `main`. To update:

```bash
python build.py
git add -A && git commit -m "Update content" && git push
```

### Putting this on momentumlinkpro.com

The live site runs on Azure Static Web Apps (`www.momentumlinkpro.com` resolves
to `salmon-pond-077c4980f.7.azurestaticapps.net`), so this replaces it in place:

1. In the Azure portal, open the Static Web App that serves the domain.
2. **Manage deployment token** → copy it.
3. In this repository: **Settings → Secrets and variables → Actions → New
   repository secret**, named `AZURE_STATIC_WEB_APPS_API_TOKEN`.
4. Set the origin in `build.py`, then rebuild, commit and push:

   ```python
   BASE_URL = "https://www.momentumlinkpro.com"
   ```

   Everything absolute follows from it — canonical links, Open Graph URLs, the
   sitemap and the schema.org graph.

If the existing Static Web App is wired to another repository, either repoint
it here or create a new one and move the custom domain across; the deployment
token is what decides where a push lands.

`staticwebapp.config.json` ships in `site/` and is written by `build.py`. It
sets the 404 page and the cache lifetimes: a year for `media/` (stable
filenames), a day for `assets/` (same filenames, busted by the `?v=` hash),
ten minutes for HTML.

`CUSTOM_DOMAIN` in `build.py` writes a `CNAME` file, which is only how GitHub
Pages is told about a domain. Azure does not read it — leave it empty unless
Pages is serving the domain.

### Making the repository private

Azure Static Web Apps deploys from a private repository without changing
anything. **GitHub Pages does not** — on the free plan, a private repository
cannot publish Pages, so `deploy.yml` will start failing. Once Azure is
serving the site, delete `.github/workflows/deploy.yml` (or keep it and accept
the failed runs).

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

**The section is pinned, and one step is open at a time.** The steps do not scroll
past — the whole process holds still in the middle of the screen and scrolling only
decides which step is projected. Each step owns a slice of the section's height; on
reaching its slice, its node swells on the thread and its panel projects out of that
circle into the centre of the screen, while the previous one folds back into its own
circle. Never two at once, and nothing inside the pinned area scrolls. The panel's
`transform-origin` is set from its node's live position each scroll pass, so it
genuinely grows out of that circle rather than from a fixed corner. Clicking a node
scrolls to that step's slice.

On a phone the thread lies across the top of the pinned area and the panel fills what
is left, sized to fit without a scrollbar of its own.

Activation is computed in the shared scroll pass (`initProcess()` in `site.js`) rather
than from an observer, so a step is never left collapsed and unreadable if callbacks
are throttled. Under `prefers-reduced-motion` the section is not pinned at all — the
steps stay a plain readable column, which is also what a visitor without JavaScript gets.

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
