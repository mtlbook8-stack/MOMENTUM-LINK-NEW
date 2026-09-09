"""
Static site generator for the Momentum Link Professionals website.

Holds the site copy in one place and writes the five pages, so a repeated
component (a media card, a sector block) is defined once rather than pasted
forty times. Run it after editing content:

    python build.py

Output goes to ./site — the folder you deploy.
"""

import hashlib
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")

# Set this to the live origin (no trailing slash) to emit absolute canonical
# and Open Graph URLs; leave empty for relative-only output.
BASE_URL = "https://mtlbook8-stack.github.io/MOMENTUM-LINK-NEW"

try:
    with open(os.path.join(OUT, "media", "manifest.json"), encoding="utf-8") as _fh:
        MEDIA_SIZES = json.load(_fh)
except OSError:
    MEDIA_SIZES = {}

EMAIL_NEW = "hello@momentumlink.com"
EMAIL_CARE = "hello@momentumlink.com"
PHONE = "(347) 342-1302"
PHONE_HREF = "+13473421302"

# ── Content ───────────────────────────────────────────────────────────────

PAGES = [
    ("index.html", "home", "Home"),
    ("practice.html", "practice", "Practice"),
    ("industries.html", "industries", "Industries"),
    ("technology.html", "technology", "Technology"),
    ("contact.html", "contact", "Contact"),
]

PRACTICE = [
    {
        "num": "01",
        "label": "Meet",
        "stem": "43-process-meeting",
        "title": "A meeting, or a few",
        "short": "One or two conversations to establish what the project actually needs.",
        "body": "We do not open with a discovery programme. A meeting — sometimes a few — is usually enough to establish what the product has to do, who it is for, and what would count as finished. Anything still unclear goes on the list to settle at the demo rather than holding the project up.",
        "deliverable": "Deliverable — an agreed scope, in writing",
    },
    {
        "num": "02",
        "label": "Demo",
        "stem": "44-process-demo",
        "title": "A demo that shows what we understood",
        "short": "You see our understanding as something working, before it is built.",
        "body": "Rather than hand back a specification for you to imagine, we build a demo that shows what we understood and put it in front of you. You mark it up, we correct it, and the build does not start in earnest until you agree it is right.",
        "deliverable": "Deliverable — a working demo, and your notes on it",
    },
    {
        "num": "03",
        "label": "Build",
        "stem": "45-process-cicd-pipeline",
        "title": "Rapid build, tested and shipped",
        "short": "Built quickly, deployed through CI/CD, and properly tested before it ships.",
        "body": "The build moves fast because deployment is automated — a short CI/CD workflow puts each change in front of you without ceremony. Testing is not what gets cut for it: before a release goes out it goes through a comprehensive session, a good deal of it by hand, because that is what actually finds the things that matter.",
        "deliverable": "Deliverable — the working product, tested and deployed",
    },
    {
        "num": "04",
        "label": "Iterate",
        "stem": "05-practice-continuous-enhancements",
        "title": "Your feedback, for as many rounds as it takes",
        "short": "The real notes arrive after delivery. There is no limit on rounds.",
        "body": "Once it is in your hands the useful feedback starts, and it rarely arrives all at once. We keep iterating for as many rounds as it takes — the count is not capped, and asking for another pass is expected rather than an imposition. Automated tests run on every update through the iteration, so a change made for this round does not quietly break something that worked in the last.",
        "deliverable": "Deliverable — a release for every round of feedback",
    },
    {
        "num": "05",
        "label": "Handover",
        "stem": "46-process-handover",
        "title": "Complete, and handed over in full",
        "short": "When the changes stop earning their place, the work is done.",
        "body": "How long that takes depends on the product. When the iterations stop earning their place the work is complete, and the product, its code and everything needed to run it are handed over. The measure is simple: everyone is satisfied with what they got.",
        "deliverable": "Deliverable — full handover of the product and its code",
    },
    {
        "num": "06",
        "label": "Partner",
        "stem": "06-practice-long-term-technology-care",
        "title": "A long-term arrangement, where a product needs one",
        "short": "Optional — a standing relationship for products that keep moving.",
        "body": "Some products are finished at handover. Others keep moving, and for those we stay on: continued development, maintenance and accountability for as long as the product warrants it. It is an option, not a condition of working together.",
        "deliverable": "Optional — an ongoing arrangement, for the products that call for it",
    },
]

SECTORS = [
    {
        "slug": "manufacturing",
        "name": "Manufacturing",
        "count": "2 capabilities",
        "blurb": "Connected production floors where monitoring, scheduling and product costing answer to the same set of numbers.",
        "lead": ("07-industry-smart-manufacturing", "Smart Manufacturing"),
        "items": [
            ("42-industry-assembly-bom-product-cost", "Assembly, bill of materials, and true product cost"),
        ],
    },
    {
        "slug": "construction",
        "name": "Construction",
        "count": "3 capabilities",
        "blurb": "Preconstruction through final billing, with the change orders and progress claims that decide whether a job made money.",
        "lead": ("09-industry-construction-project-management", "Construction Project Management and Accounting"),
        "items": [
            ("08-industry-construction-planning", "Planning and preconstruction accounting"),
            ("38-industry-construction-change-orders-billing", "Change orders and progress billing"),
        ],
    },
    {
        "slug": "wholesale-distribution",
        "name": "Wholesale Distribution",
        "count": "6 capabilities",
        "blurb": "Ordering, fulfilment, inventory and both sides of the ledger — the density of transactions is the design problem.",
        "lead": ("11-industry-wholesale-distribution", "Wholesale Distribution and Fulfillment"),
        "items": [
            ("12-industry-wholesale-inventory-pricing", "Inventory, purchasing, and pricing"),
            ("37-industry-wholesale-customer-ordering", "Customer ordering and replenishment"),
            ("41-industry-recurring-wholesale-orders", "Recurring orders for hospitality"),
            ("10-industry-wholesale-accounts-receivable", "Accounts receivable"),
            ("39-industry-wholesale-accounts-payable", "Accounts payable and supplier reconciliation"),
        ],
    },
    {
        "slug": "property",
        "name": "Property",
        "count": "4 capabilities",
        "blurb": "Multi-property operations where leasing, maintenance and owner reporting have to reconcile every month without heroics.",
        "lead": ("13-industry-multi-property-management", "Multi-Property Operations and Accounting"),
        "items": [
            ("36-industry-property-leasing-occupancy", "Leasing and occupancy"),
            ("14-industry-property-maintenance", "Maintenance and tenant service"),
            ("40-industry-property-financial-operations", "Rent, expenses, and owner reporting"),
        ],
    },
    {
        "slug": "retail-ecommerce",
        "name": "Retail & Ecommerce",
        "count": "4 capabilities",
        "blurb": "Storefronts that stay fast under load, findable in search, and worth returning to after the first order.",
        "lead": ("15-industry-premium-retail-website", "Premium Retail Website Experience"),
        "items": [
            ("16-industry-high-traffic-ecommerce", "High-traffic ecommerce performance"),
            ("17-industry-seo-content-visibility", "Search visibility and content structure"),
            ("18-industry-conversion-retention", "Conversion and customer retention"),
        ],
    },
]

TECH = [
    ("19-technology-api-integration", "API Integration", "Secure orchestration between the systems you already run."),
    ("20-technology-cloud-native-systems", "Cloud-Native Systems", "Infrastructure that scales with demand rather than headcount."),
    ("21-technology-data-engineering", "Data Engineering", "Pipelines that turn scattered records into one dependable source."),
    ("22-technology-cross-platform-apps", "Cross-Platform Applications", "One product serving the desk, the warehouse floor, and the field."),
    ("23-technology-workflow-automation", "Workflow Automation", "Removing the manual steps nobody should still be doing."),
    ("24-technology-accessible-design", "Accessibility and Inclusive Design", "Interfaces every employee and customer can actually use."),
    ("25-technology-responsible-ai", "Responsible Artificial Intelligence", "Assistive models with human review wherever decisions carry weight."),
    ("26-technology-zero-trust-security", "Zero-Trust Security and Identity", "Identity-first access control across every service and site."),
    ("27-technology-digital-twin", "Digital Twins and Simulation", "Testing an operational change before committing to it."),
    ("28-technology-private-analytics", "Privacy-Preserving Analytics", "Insight drawn from your data without exposing it."),
    ("29-technology-modular-platform", "Scalable Modular Platforms", "Capability added in increments, never in rewrites."),
    ("30-technology-connected-ecosystem", "Connected Technology Ecosystem", "Sites, plants and stores operating as a single network."),
    ("31-technology-complexity-to-clarity", "From Complexity to Clarity", "Untangling accumulated systems into something legible."),
    ("32-technology-connected-physical-operations", "Connected Physical Operations", "Software tied to what actually moves on the ground."),
    ("33-technology-modular-product-evolution", "Modular Product Evolution", "Products that grow one considered module at a time."),
    ("34-technology-secure-data-journey", "Secure Data Journey", "Encrypted, auditable movement from capture through to report."),
    ("35-technology-continuous-improvement", "Continuous Improvement Loop", "A standing cycle of measure, adjust, and release."),
]

STATS = [
    ("100%", "Tailored solutions — never off-the-shelf shortcuts"),
    ("Fast", "Delivery times, from planning to launch"),
    ("Real", "Working agents that finish the job"),
    ("&#8734;", "Rounds of feedback — we iterate until you are satisfied"),
]

# What We Do, as the live site states it.
SERVICES = [
    ("33-technology-modular-product-evolution", "Custom Software Builds",
     "We design and build software tailored to your exact business needs — not off-the-shelf shortcuts."),
    ("31-technology-complexity-to-clarity", "System Migrations",
     "We bridge the gap between outdated systems and modern technology — handling the entire transition end to end."),
    ("25-technology-responsible-ai", "Smart Agents",
     "Working agents that handle real tasks — automation that finishes the job and frees up your team."),
    ("27-technology-digital-twin", "Tech Research &amp; Strategy",
     "We constantly research the latest technology so you always get the best option — not just an option."),
    ("35-technology-continuous-improvement", "Optimization &amp; Tuning",
     "We optimize every solution to fit your specific use case — performance, cost, and workflow all dialled in."),
    ("20-technology-cloud-native-systems", "Full Delivery",
     "From planning to launch to support — we handle the whole journey. You just use what we build."),
]

# The four points the live site makes about closing the gap.
GAP_POINTS = [
    "We research the latest technology daily",
    "We migrate you smoothly from old to new",
    "We tailor every build to your exact use case",
    "We handle the entire delivery",
]

CONTACTS = [
    ("Email", EMAIL_NEW, "mailto:" + EMAIL_NEW, "Tell us about your business. We will handle the technology."),
    ("Phone", PHONE, "tel:" + PHONE_HREF, "Speak to us directly."),
]

FIELDS = [
    ("name", "Name", "Your name", "text", True),
    ("organisation", "Organisation", "Company or group", "text", True),
    ("sector", "Sector", "Manufacturing, construction, wholesale…", "text", False),
    ("email", "Email", "you@company.com", "email", True),
]

# Image sizes hints, per layout context.
SIZES = {
    "full": "100vw",
    "card": "(max-width: 560px) 100vw, (max-width: 1240px) 34vw, 410px",
    "half": "(max-width: 560px) 100vw, (max-width: 1240px) 50vw, 620px",
    "item": "(max-width: 560px) 100vw, (max-width: 900px) 50vw, 300px",
}


# ── Helpers ───────────────────────────────────────────────────────────────

def e(text):
    return html.escape(str(text), quote=True)


def picture(stem, alt, sizes, eager=False, cls=""):
    """Responsive <picture> with a WebP source and a JPEG fallback."""
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    class_attr = f' class="{cls}"' if cls else ""
    w, h = media_size(stem)
    return (
        "<picture>"
        f'<source type="image/webp" srcset="media/{stem}-768.webp 768w, media/{stem}.webp 1536w" sizes="{sizes}">'
        f'<img{class_attr} src="media/{stem}.jpg" srcset="media/{stem}-768.jpg 768w, media/{stem}.jpg 1536w"'
        f' sizes="{sizes}" alt="{e(alt)}" width="{w}" height="{h}" {loading} decoding="async">'
        "</picture>"
    )


def layer_img(stem, alt, sizes, cls="", eager=False, attrs=""):
    """
    A <picture> whose <img> carries the layout class directly — used where the
    stylesheet positions the image itself (hero layers, band backgrounds,
    sector panels) rather than a wrapper.
    """
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    extra = f" {attrs}" if attrs else ""
    hidden = ' aria-hidden="true"' if not alt else ""
    w, h = media_size(stem)
    return (
        "<picture>"
        f'<source type="image/webp" srcset="media/{stem}-768.webp 768w, media/{stem}.webp 1536w" sizes="{sizes}">'
        f'<img class="{cls}"{extra} src="media/{stem}.jpg"'
        f' srcset="media/{stem}-768.jpg 768w, media/{stem}.jpg 1536w" sizes="{sizes}"'
        f' alt="{e(alt)}"{hidden} width="{w}" height="{h}" {loading} decoding="async">'
        "</picture>"
    )


def media_size(stem):
    """Real intrinsic size of an image, from the manifest build-media.py writes.
    The sources are not all one shape, and a wrong width/height causes layout
    shift while the picture loads."""
    return tuple(MEDIA_SIZES.get(stem, (1536, 1024)))


def asset_version(relpath):
    """Short content hash, appended to asset URLs so a changed file is never
    served from a stale cache after a deploy."""
    try:
        with open(os.path.join(OUT, relpath), "rb") as fh:
            return hashlib.sha1(fh.read()).hexdigest()[:8]
    except OSError:
        return "dev"


def head(title, description, page, extra=""):
    canonical = ""
    og_url = ""
    filename = next(f for f, p, _ in PAGES if p == page) if page in [p for _, p, _ in PAGES] else "index.html"
    if BASE_URL:
        path = "" if filename == "index.html" else filename
        canonical = f'\n  <link rel="canonical" href="{BASE_URL}/{path}">'
        og_url = f'\n  <meta property="og:url" content="{BASE_URL}/{path}">'
    og_image = f"{BASE_URL}/media/31-technology-complexity-to-clarity.jpg" if BASE_URL else "media/31-technology-complexity-to-clarity.jpg"

    return f"""<!DOCTYPE html>
<html lang="en" class="no-js" data-media-base="media/">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <meta name="theme-color" content="#10222F">{canonical}

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Momentum Link Professionals">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:image" content="{og_image}">{og_url}
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="favicon.svg">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300&amp;family=IBM+Plex+Sans:wght@300;400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/site.css?v={asset_version("assets/css/site.css")}">
  <script>document.documentElement.className = document.documentElement.className.replace("no-js", "js");</script>
{extra}</head>
<body data-page="{page or 'home'}">
  <a class="skip-link" href="#main">Skip to content</a>
"""


def header(page):
    links = ""
    for filename, key, label in PAGES:
        current = ' aria-current="page"' if key == page else ""
        links += f'\n          <a class="nav__link" href="{filename}"{current}>{label}</a>'
    return f"""
  <header class="site-header">
    <div class="site-header__inner">
      <a class="brand" href="index.html">
        <span class="brand__mark" aria-hidden="true"></span>
        <span class="brand__text">
          <span class="brand__name">Momentum Link</span>
          <span class="brand__tag">Professionals</span>
        </span>
      </a>

      <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="site-nav" aria-label="Menu">
        <span aria-hidden="true"></span>
      </button>

      <nav class="nav" id="site-nav" aria-label="Primary">{links}
        <button class="nav__present" type="button" data-open-pres hidden>&#9654; Present</button>
      </nav>
    </div>
    <div class="progress" data-progress aria-hidden="true"></div>
  </header>
"""


def footer():
    links = "".join(
        f'\n        <a href="{filename}">{label}</a>' for filename, _, label in PAGES
    )
    return f"""
  <footer class="site-footer">
    <div class="site-footer__grid">
      <div class="site-footer__col">
        <span class="site-footer__brand">Momentum Link</span>
        <span class="site-footer__blurb">Quickly linking your business to better technology. Built for delivery, optimized for results.</span>
      </div>
      <div class="site-footer__col">
        <span class="site-footer__head">Pages</span>{links}
      </div>
      <div class="site-footer__col">
        <span class="site-footer__head">Contact</span>
        <a href="mailto:{EMAIL_NEW}">{EMAIL_NEW}</a>
        <a href="tel:{PHONE_HREF}">{PHONE}</a>
      </div>
    </div>
    <div class="site-footer__meta">
      <div>&copy; <span data-year>2026</span> Momentum Link Professionals</div>
    </div>
  </footer>

  <script src="assets/js/site.js?v={asset_version("assets/js/site.js")}" defer></script>
</body>
</html>
"""


def page(filename, key, title, description, body):
    with open(os.path.join(OUT, filename), "w", encoding="utf-8") as fh:
        fh.write(head(title, description, key) + header(key) + body + footer())
    return filename


# ── Fragments ─────────────────────────────────────────────────────────────

def practice_cards():
    out = ""
    for p in PRACTICE:
        out += f"""
          <figure class="card" data-card data-reveal>
            {picture(p['stem'], p['title'], SIZES['card'])}
            <figcaption>
              <span class="card__num">{p['num']}</span>
              <span class="card__title">{e(p['title'])}</span>
              <span class="card__sub">{e(p['short'])}</span>
            </figcaption>
          </figure>"""
    return out


def sector_panels():
    out = ""
    for i, s in enumerate(SECTORS):
        stem, alt = s["lead"]
        open_cls = " is-open" if i == 0 else ""
        out += f"""
          <a class="panel{open_cls}" data-panel href="industries.html#{s['slug']}">
            {layer_img(stem, alt, SIZES['half'])}
            <span class="panel__rail">{e(s['name'])}</span>
            <span class="panel__body">
              <span class="panel__count">{e(s['count'])}</span>
              <span class="panel__name">{e(s['name'])}</span>
              <span class="panel__blurb">{e(s['blurb'])}</span>
            </span>
          </a>"""
    return out


def stats_band():
    items = ""
    for n, label in STATS:
        items += f"""
          <div class="stats__item">
            <div class="stats__n">{n}</div>
            <div class="stats__label">{e(label)}</div>
          </div>"""
    return f"""
    <section class="stats" aria-label="Practice at a glance">
      <div class="shell">
        <div class="stats__grid">{items}
        </div>
      </div>
    </section>
"""


# ── Pages ─────────────────────────────────────────────────────────────────

def service_cards():
    out = ""
    for stem, title, blurb in SERVICES:
        out += f"""
          <figure class="card card--tech" data-card data-reveal>
            {picture(stem, title.replace("&amp;", "and"), SIZES['card'])}
            <figcaption>
              <span class="card__title">{title}</span>
              <span class="card__sub">{e(blurb)}</span>
            </figcaption>
          </figure>"""
    return out


def build_home():
    gap = "".join("<li>" + e(point) + "</li>" for point in GAP_POINTS)

    body = f"""
  <main id="main">
    <section class="stage" data-stage aria-label="Introduction">
      <div class="stage__pin">
        <div class="stage__backdrop" data-stage-backdrop aria-hidden="true">
          {layer_img('31-technology-complexity-to-clarity', '', SIZES['full'], eager=True)}
        </div>
        <div class="stage__glow" data-stage-glow aria-hidden="true"></div>
        <div class="stage__frame" data-stage-frame aria-hidden="true"></div>

        {layer_img('31-technology-complexity-to-clarity', 'From complexity to a clear system', SIZES['full'], eager=True, cls='stage__l1', attrs='data-stage-l1')}

        <div class="stage__intro" data-stage-intro aria-hidden="true">
          <p class="stage__plate">Plate 01</p>
          <p class="stage__caption">From complexity to a clear system</p>
        </div>

        <div class="stage__l2" data-stage-l2 aria-hidden="true">
          {layer_img('30-technology-connected-ecosystem', '', SIZES['full'])}
        </div>

        <div class="stage__tint" data-stage-tint aria-hidden="true"></div>

        <div class="stage__block" data-stage-a>
          <div class="stage__inner">
            <p class="stage__kicker">Modern technology solutions</p>
            <h1 class="stage__title">Quickly linking your business to better tech.</h1>
          </div>
        </div>

        <div class="stage__block" data-stage-b>
          <div class="stage__inner">
            <p class="stage__kicker">Build &middot; Migrate &middot; Deliver</p>
            <p class="stage__title stage__title--sub">We build, migrate, and deliver modern software solutions — so your technology works for you, not the other way around.</p>
            <div class="stage__actions">
              <a class="btn btn--primary" href="contact.html">Get started</a>
              <button class="btn btn--ghost" type="button" data-open-pres hidden>&#9654; Watch the presentation</button>
              <a class="btn btn--ghost" href="practice.html">How we work</a>
            </div>
          </div>
        </div>

        <div class="stage__meter" aria-hidden="true">
          <span class="stage__count" data-stage-count>01 / 02</span>
          <span class="stage__track"><span class="stage__bar" data-stage-bar></span></span>
        </div>

        <div class="stage__cue" data-stage-cue aria-hidden="true">Scroll</div>
      </div>
    </section>
{stats_band()}
    <section class="editorial shell">
      <div class="editorial__grid">
        <div>
          <p class="eyebrow">01 — The gap</p>
          <h2 class="editorial__title">Tech moves fast. We make sure you do too.</h2>
        </div>
        <div class="editorial__body">
          <p>Most businesses cannot keep up with the technology industry. There is no time to research every option, evaluate the noise, and migrate to better systems — so they stay on what they have, and miss the upside.</p>
          <p>That is exactly the gap we close.</p>
          <ul class="editorial__list">{gap}
          </ul>
        </div>
      </div>
    </section>

    <section class="card-section shell" aria-label="What we do">
      <p class="eyebrow" style="margin-bottom:20px">02 — What we do</p>
      <div class="card-grid card-grid--tech">{service_cards()}
      </div>
    </section>

    <section class="band">
      {layer_img('30-technology-connected-ecosystem', 'Connected technology ecosystem', SIZES['full'], cls='band__bg')}
      <div class="band__veil" aria-hidden="true"></div>
      <div class="band__inner shell">
        <div class="band__copy">
          <p class="eyebrow eyebrow--blue">03 — Smart agents</p>
          <h2 class="band__title">Smart agents. Real work.</h2>
          <p class="band__text">Not magic. Not buzzwords. Just technology that actually gets the job done. We build agents that handle real tasks — they do the work, finish the job, and free up your team.</p>
          <a class="btn btn--ghost btn--ghost-fill" href="technology.html">Technology capability</a>
        </div>
      </div>
    </section>

    <section class="panels-section shell" aria-label="Sectors">
      <p class="eyebrow" style="margin-bottom:16px">04 — Sectors</p>
      <div class="panels">{sector_panels()}
      </div>
      <p class="panels-hint">
        <span class="panels-hint__pointer">Hover to expand &middot; click to open the sector</span>
        <span class="panels-hint__touch">Tap to expand &middot; tap again to open the sector</span>
      </p>
    </section>

    <section class="closing shell">
      <p class="eyebrow">Ready to move forward?</p>
      <h2 class="closing__title">Let&#8217;s link your business to better technology.</h2>
      <a class="btn btn--dark" href="contact.html">Get in touch</a>
    </section>
  </main>
"""
    return page(
        "index.html", "home",
        "Momentum Link Professionals — Quickly linking your business to better tech",
        "We build, migrate, and deliver modern software solutions — so your technology works for you, not the other way around. Custom builds, system migrations and smart agents that do real work.",
        body,
    )


def build_practice():
    points = ""
    steps = ""
    for i, p in enumerate(PRACTICE):
        points += f"""
          <li class="process__item" data-process-point="{i}">
            <a class="process__point" href="#step-{p['num']}">
              <span class="process__thumb">{picture(p['stem'], "", "220px")}</span>
              <span class="process__meta">
                <span class="process__num">{p['num']}</span>
                <span class="process__label">{e(p['label'])}</span>
              </span>
            </a>
          </li>"""

        w, h = media_size(p["stem"])
        # The frame takes the picture's own proportions rather than forcing a
        # crop; a panoramic one drops the side-by-side layout and runs the
        # full width of the panel, where there is room for it.
        wide = " step__inner--wide" if w / h >= 2.2 else ""

        steps += f"""
        <article class="step" id="step-{p['num']}" data-step>
          <div class="step__inner{wide}">
            <div class="step__media" style="--media-ratio:{w}/{h}">{picture(p['stem'], p['title'], SIZES['half'])}</div>
            <div class="step__copy">
              <p class="step__num">{p['num']} &middot; {e(p['label'])}</p>
              <h2 class="step__title">{e(p['title'])}</h2>
              <p class="step__body">{e(p['body'])}</p>
              <p class="step__deliverable">{e(p['deliverable'])}</p>
            </div>
          </div>
        </article>"""

    body = f"""
  <main id="main">
    <section class="page-head shell">
      <p class="eyebrow">The practice</p>
      <h1 class="display">From the first meeting to handover, in five steps.</h1>
      <p class="lede">Short scoping, a demo before the build, rapid delivery on a tested pipeline, and as many rounds of your feedback as it takes. A sixth step — staying on for the long term — is there for the products that need it.</p>
    </section>

    <div class="process shell" data-process>
      <div class="process__pin">
        <nav class="process__rail" aria-label="The six steps">
          <span class="process__track" aria-hidden="true"><span class="process__fill" data-process-fill></span></span>
          <ol class="process__points">{points}
          </ol>
        </nav>

        <div class="process__stage">{steps}
        </div>
      </div>
    </div>
  </main>
"""
    return page(
        "practice.html", "practice",
        "The practice — Momentum Link Professionals",
        "How we work: a meeting or two to scope it, a demo that shows what we understood, a rapid build on a tested CI/CD pipeline, unlimited rounds of your feedback, and a full handover.",
        body,
    )


def build_industries():
    sections = ""
    for s in SECTORS:
        lead_stem, lead_alt = s["lead"]
        items = ""
        for stem, title in s["items"]:
            items += f"""
          <figure class="card card--plain" data-reveal>
            {picture(stem, title, SIZES['item'])}
            <figcaption>{e(title)}</figcaption>
          </figure>"""
        sections += f"""
    <section class="sector shell" id="{s['slug']}" aria-labelledby="{s['slug']}-title">
      <div class="sector__head">
        <div>
          <p class="sector__count">{e(s['count'])}</p>
          <h2 class="sector__name" id="{s['slug']}-title">{e(s['name'])}</h2>
          <p class="sector__blurb">{e(s['blurb'])}</p>
        </div>
        <div class="sector__lead" data-reveal>{picture(lead_stem, lead_alt, SIZES['half'])}</div>
      </div>
      <div class="card-grid card-grid--items">{items}
      </div>
    </section>"""

    body = f"""
  <main id="main">
    <section class="page-head shell">
      <p class="eyebrow">Industries</p>
      <h1 class="display">Five sectors we know at the workflow level.</h1>
      <p class="lede">Each of these carries its own accounting shape, its own exceptions, and its own reasons a generic implementation fails.</p>
    </section>
{sections}
  </main>
"""
    return page(
        "industries.html", "industries",
        "Industries — Momentum Link Professionals",
        "Manufacturing, construction, wholesale distribution, property and retail commerce — five sectors understood at the workflow level, each with its own accounting shape and exceptions.",
        body,
    )


def build_technology():
    total = len(TECH)
    cards = ""
    for stem, title, blurb in TECH:
        cards += f"""
        <figure class="card card--tech" data-card data-reveal>
          {picture(stem, title, SIZES['card'])}
          <figcaption>
            <span class="card__title">{e(title)}</span>
            <span class="card__sub">{e(blurb)}</span>
          </figcaption>
        </figure>"""

    body = f"""
  <main id="main">
    <section class="page-head shell">
      <p class="eyebrow">Technology</p>
      <h1 class="display">Capability, held to the same standard.</h1>
      <p class="lede">Seventeen disciplines we build and maintain in-house. None of them is a product pitch — each exists because a client operation needed it to work properly.</p>
    </section>

    <section class="card-section shell" style="padding-top:0" aria-label="Technology disciplines" data-deck-section>
      <div class="deck-bar" data-deck-bar hidden>
        <p class="deck-count"><b data-deck-index>01</b> / {total} &middot; <span data-deck-title></span></p>
        <div class="deck-actions">
          <span class="deck-nav" data-deck-nav>
            <button class="deck-btn" type="button" data-deck-auto aria-pressed="true" hidden>&#10073;&#10073; Pause</button>
            <button class="deck-btn" type="button" data-deck-prev aria-label="Previous card">&larr;</button>
            <button class="deck-btn" type="button" data-deck-next aria-label="Next card">&rarr;</button>
          </span>
          <button class="deck-btn deck-btn--primary" type="button" data-deck-toggle>See all {total}</button>
        </div>
      </div>

      <div class="card-grid card-grid--tech" data-deck>{cards}
      </div>

      <p class="deck-hint" data-deck-hint hidden>Shuffles on its own &middot; click or swipe to take over</p>
      <p class="deck-live visually-hidden" data-deck-live role="status" aria-live="polite"></p>
    </section>
  </main>
"""
    return page(
        "technology.html", "technology",
        "Technology capability — Momentum Link Professionals",
        "Seventeen technology disciplines built and maintained in-house: integration, cloud-native systems, data engineering, automation, zero-trust security, digital twins and more.",
        body,
    )


def build_contact():
    items = ""
    for label, value, href, note in CONTACTS:
        items += f"""
          <div class="contact-item">
            <p class="contact-item__label">{e(label)}</p>
            <a class="contact-item__value" href="{href}">{e(value)}</a>
            <p class="contact-item__note">{e(note)}</p>
          </div>"""

    fields = ""
    for name, label, placeholder, kind, required in FIELDS:
        req = " required" if required else ""
        star = " *" if required else ""
        fields += f"""
              <div class="field">
                <label class="field__label" for="f-{name}">{e(label)}{star}</label>
                <input type="{kind}" id="f-{name}" name="{name}" placeholder="{e(placeholder)}"
                       autocomplete="{'email' if kind == 'email' else 'organization' if name == 'organisation' else 'name' if name == 'name' else 'off'}"{req}>
                <p class="field__error" id="f-{name}-error" aria-live="polite"></p>
              </div>"""

    body = f"""
  <main id="main">
    <section class="band band--contact contact-hero">
      {layer_img('06-practice-long-term-technology-care', 'A long-term technology relationship', SIZES['full'], cls='band__bg', eager=True)}
      <div class="band__veil" aria-hidden="true"></div>
      <div class="band__inner shell">
        <p class="eyebrow eyebrow--blue">Get started</p>
        <h1 class="display">Let&#8217;s get to work.</h1>
        <p class="lede">Tell us about your business — we will handle the technology. A meeting or two is usually all it takes before you are looking at a working demo.</p>
      </div>
    </section>

    <section class="contact-grid shell">
      <div class="contact-list">{items}
      </div>

      <form class="form-card" data-contact-form data-endpoint="" data-mailto="{EMAIL_NEW}"
            action="mailto:{EMAIL_NEW}" method="post" enctype="text/plain" novalidate>
        <h2 class="form-card__title">Send a brief</h2>
        <div class="form-fields">{fields}
          <div class="field">
            <label class="field__label" for="f-message">What is not working *</label>
            <textarea id="f-message" name="message" rows="4"
                      placeholder="The process, the system, the report — wherever the friction is." required></textarea>
            <p class="field__error" id="f-message-error" aria-live="polite"></p>
          </div>
        </div>
        <button class="btn btn--dark" type="submit">Send brief</button>
        <p class="form-status" data-form-status role="status" aria-live="polite"></p>
      </form>
    </section>
  </main>
"""
    return page(
        "contact.html", "contact",
        "Contact — Momentum Link Professionals",
        "Tell us about your business and we will handle the technology. Reach Momentum Link Professionals by email or phone, or send a brief.",
        body,
    )


def build_404():
    body = """
  <main id="main">
    <section class="page-head shell">
      <p class="eyebrow">404</p>
      <h1 class="display">That page is not here.</h1>
      <p class="lede">The link may be out of date. Everything on the site is reachable from the five pages below.</p>
      <p style="margin-top:32px"><a class="btn btn--dark" href="index.html">Back to the home page</a></p>
    </section>
  </main>
"""
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(
            head("Page not found — Momentum Link Professionals",
                 "The requested page could not be found.", "home")
            + header("")
            + body
            + footer()
        )
    return "404.html"


def build_extras():
    written = []

    favicon = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240">'
        '<rect width="240" height="240" fill="#10222F"/>'
        '<rect x="98" y="98" width="44" height="44" rx="4" fill="#4A9BE8" transform="rotate(45 120 120)"/>'
        '<rect x="72" y="168" width="96" height="3" fill="#F2EFE8" opacity="0.7"/>'
        "</svg>\n"
    )
    with open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(favicon)
    written.append("favicon.svg")

    root = BASE_URL or "https://example.com"
    urls = "".join(
        f"\n  <url><loc>{root}/{'' if f == 'index.html' else f}</loc></url>"
        for f, _, _ in PAGES
    )
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"{urls}\n</urlset>\n"
        )
    written.append("sitemap.xml")

    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"User-agent: *\nAllow: /\n\nSitemap: {root}/sitemap.xml\n")
    written.append("robots.txt")

    return written


def main():
    os.makedirs(OUT, exist_ok=True)
    made = [
        build_home(),
        build_practice(),
        build_industries(),
        build_technology(),
        build_contact(),
        build_404(),
    ] + build_extras()
    print("Wrote " + ", ".join(made))


if __name__ == "__main__":
    main()
