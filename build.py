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
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")

# Set this to the live origin (no trailing slash) to emit absolute canonical
# and Open Graph URLs; leave empty for relative-only output.
BASE_URL = "https://mtlbook8-stack.github.io/MOMENTUM-LINK-NEW"

EMAIL_NEW = "hello@momentumlink.example"
EMAIL_CARE = "care@momentumlink.example"
PHONE = "+1 (000) 000-0000"
PHONE_HREF = "+10000000000"

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
        "label": "Understand",
        "stem": "01-practice-understand-business-workflow",
        "title": "Learning how the business actually works",
        "short": "Weeks on site mapping the real path of an order, a job, or a tenancy.",
        "body": "Before a single platform is named, we trace the operation end to end — who approves what, where the spreadsheet workarounds live, and which exceptions happen often enough to be the rule. The wall of process cards is the deliverable nobody expects and everybody keeps.",
        "deliverable": "Deliverable — operating map and exception register",
    },
    {
        "num": "02",
        "label": "Choose",
        "stem": "02-practice-select-right-foundation",
        "title": "Finding the right technological foundation",
        "short": "Platforms compared against your workflow, not a feature matrix.",
        "body": "Selection is a fit question. We score candidate foundations against the mapped operation, weighting configurability and integration surface over feature counts, and we say plainly where each one would have to bend.",
        "deliverable": "Deliverable — scored selection brief with dissenting notes",
    },
    {
        "num": "03",
        "label": "Tailor",
        "stem": "03-practice-tailored-client-workspace",
        "title": "Tailoring a shared foundation to one client",
        "short": "A common base, configured until it reads like your own system.",
        "body": "Screens, terminology, roles and approvals are shaped around the people who use them. Staff should recognise their own vocabulary on day one; training time is the honest measure of whether the tailoring worked.",
        "deliverable": "Deliverable — configured workspace and role model",
    },
    {
        "num": "04",
        "label": "Connect",
        "stem": "04-practice-existing-system-integration",
        "title": "Connecting with existing systems",
        "short": "Integration first. Replacement only where it is genuinely warranted.",
        "body": "Most businesses already run software that works. We coordinate it through a governed integration service so accounting, routing, monitoring and commerce share one dependable version of the truth.",
        "deliverable": "Deliverable — integration service and data contracts",
    },
    {
        "num": "05",
        "label": "Improve",
        "stem": "05-practice-continuous-enhancements",
        "title": "Delivering useful improvements continuously",
        "short": "Small, frequent releases measured against operational outcomes.",
        "body": "Improvement is a standing arrangement, not a follow-on project. Each release is scoped to something an operator will feel that week — a step removed, a report they can finally trust, a queue that clears earlier.",
        "deliverable": "Deliverable — release cadence and outcome reporting",
    },
    {
        "num": "06",
        "label": "Maintain",
        "stem": "06-practice-long-term-technology-care",
        "title": "A long-term technology relationship",
        "short": "Version history, personalised care, and a team that stays.",
        "body": "Systems age. We keep the record of every change, retire what stopped earning its place, and remain accountable for the platform years after the initial engagement closes.",
        "deliverable": "Deliverable — maintained version history and care plan",
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
    ("6", "Steps in every engagement, in the same order"),
    ("5", "Sectors known at the workflow level"),
    ("17", "Technology disciplines maintained in-house"),
    ("&#8734;", "Care continuing well past go-live"),
]

CONTACTS = [
    ("New engagements", EMAIL_NEW, "mailto:" + EMAIL_NEW, "Send the operation, not the requirements document."),
    ("Existing clients", EMAIL_CARE, "mailto:" + EMAIL_CARE, "Care team, monitored during your working hours."),
    ("Office", PHONE, "tel:" + PHONE_HREF, "Weekdays, 08:00 – 18:00."),
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
    return (
        "<picture>"
        f'<source type="image/webp" srcset="media/{stem}-768.webp 768w, media/{stem}.webp 1536w" sizes="{sizes}">'
        f'<img{class_attr} src="media/{stem}.jpg" srcset="media/{stem}-768.jpg 768w, media/{stem}.jpg 1536w"'
        f' sizes="{sizes}" alt="{e(alt)}" width="1536" height="1024" {loading} decoding="async">'
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
    return (
        "<picture>"
        f'<source type="image/webp" srcset="media/{stem}-768.webp 768w, media/{stem}.webp 1536w" sizes="{sizes}">'
        f'<img class="{cls}"{extra} src="media/{stem}.jpg"'
        f' srcset="media/{stem}-768.jpg 768w, media/{stem}.jpg 1536w" sizes="{sizes}"'
        f' alt="{e(alt)}"{hidden} width="1536" height="1024" {loading} decoding="async">'
        "</picture>"
    )


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
        <span class="site-footer__blurb">Business software fitted to real operations — manufacturing, construction, wholesale, property, and commerce.</span>
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

def build_home():
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
          {layer_img('30-technology-connected-ecosystem', '', SIZES['full'], eager=True)}
        </div>

        <div class="stage__tint" data-stage-tint aria-hidden="true"></div>

        <div class="stage__block" data-stage-a>
          <div class="stage__inner">
            <p class="stage__kicker">Business software, built around your operation</p>
            <h1 class="stage__title">Software that fits how the work already happens.</h1>
          </div>
        </div>

        <div class="stage__block" data-stage-b>
          <div class="stage__inner">
            <p class="stage__kicker">One network — sites, plants, storefronts</p>
            <p class="stage__title stage__title--sub">Understood first. Connected second. Maintained for years.</p>
            <div class="stage__actions">
              <a class="btn btn--primary" href="practice.html">How we work</a>
              <button class="btn btn--ghost" type="button" data-open-pres hidden>&#9654; Watch the presentation</button>
              <a class="btn btn--ghost" href="industries.html">Industries we serve</a>
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
          <p class="eyebrow">01 — The problem</p>
          <h2 class="editorial__title">Most systems were bought, not fitted.</h2>
        </div>
        <div class="editorial__body">
          <p>A plant, a distributor, and a property group can run the same named platform and still have nothing in common. What differs is the workflow — the approvals, the exceptions, the way a change order or a short shipment actually gets handled.</p>
          <p>We start there. The foundation is chosen after the workflow is understood, and every configuration afterwards answers to it.</p>
        </div>
      </div>
    </section>

    <section class="card-section shell" aria-label="How we work">
      <div class="card-grid">{practice_cards()}
      </div>
    </section>

    <section class="band">
      {layer_img('30-technology-connected-ecosystem', 'Connected technology ecosystem', SIZES['full'], cls='band__bg')}
      <div class="band__veil" aria-hidden="true"></div>
      <div class="band__inner shell">
        <div class="band__copy">
          <p class="eyebrow eyebrow--blue">02 — Reach</p>
          <h2 class="band__title">One network across sites, plants, and storefronts.</h2>
          <p class="band__text">Manufacturing floors, construction schedules, distribution centres, property portfolios and commerce fronts — connected through integration rather than replacement.</p>
          <a class="btn btn--ghost btn--ghost-fill" href="technology.html">Technology capability</a>
        </div>
      </div>
    </section>

    <section class="panels-section shell" aria-label="Sectors">
      <p class="eyebrow" style="margin-bottom:16px">03 — Sectors</p>
      <div class="panels">{sector_panels()}
      </div>
      <p class="panels-hint">
        <span class="panels-hint__pointer">Hover to expand · click to open the sector</span>
        <span class="panels-hint__touch">Tap to expand · tap again to open the sector</span>
      </p>
    </section>
  </main>
"""
    return page(
        "index.html", "home",
        "Momentum Link Professionals — Business software fitted to real operations",
        "Business software built around how your operation already works. Manufacturing, construction, wholesale distribution, property and commerce — understood first, connected second, maintained for years.",
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

        steps += f"""
        <article class="step" id="step-{p['num']}" data-step>
          <div class="step__inner">
            <div class="step__media">{picture(p['stem'], p['title'], SIZES['half'])}</div>
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
      <h1 class="display">Six steps, in the same order, every engagement.</h1>
      <p class="lede">Nothing here is proprietary. It is simply the sequence that keeps a software programme honest — understand, choose, tailor, connect, improve, maintain.</p>
    </section>

    <div class="process shell" data-process>
      <nav class="process__rail" aria-label="The six steps">
        <span class="process__track" aria-hidden="true"><span class="process__fill" data-process-fill></span></span>
        <ol class="process__points">{points}
        </ol>
      </nav>

      <div class="process__steps">{steps}
      </div>
    </div>
  </main>
"""
    return page(
        "practice.html", "practice",
        "The practice — Momentum Link Professionals",
        "Six steps in the same order, every engagement: understand the workflow, choose the foundation, tailor it, connect existing systems, improve continuously, and maintain for the long term.",
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
        <p class="eyebrow eyebrow--blue">Start a conversation</p>
        <h1 class="display">Tell us how the work actually happens.</h1>
        <p class="lede">First conversations are about your operation, not our software. Expect questions about approvals, exceptions, and the reports nobody trusts.</p>
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
        "Start a conversation about your operation. Send a brief, or reach the team by email or phone — first conversations are about how the work happens, not about software.",
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
