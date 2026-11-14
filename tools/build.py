"""Builds the EnerFab website for https://enerfab.lk.

Usage (from the project folder):
    python tools/build.py

Generates every page (clean folder URLs such as /solutions/biomass-gasifiers/),
sitemap.xml, robots.txt, site.webmanifest, _headers (security headers with
CSP hashes for the inline scripts) and _redirects, all inside public/.

All company facts come from efpl.org and the Tech Monitor (2007) review it
links to. Needs Python 3 and Pillow (pip install pillow) to read image sizes
and to make WebP copies of new photos.
"""
import base64, hashlib, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from articles import ARTICLES
from projects import PROJECTS
from datetime import date
from PIL import Image

# All site files live in public/ (served by the Cloudflare Worker in src/worker.js)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public"))
SITE = "https://enerfab.lk"
LEGACY = "https://efpl.org/"
PHONE, TEL = "+94 11 288 8821", "+94112888821"
PHONE_CA, TEL_CA = "+1 226 246 1363", "+12262461363"
EMAIL, EMAIL_OLD = "info@enerfab.lk", "info@efpl.org"
# Cloudflare Turnstile site key. This default is Cloudflare's public TEST key
# (always passes). Replace it with your real site key before launch.
TURNSTILE_SITE_KEY = os.environ.get("TURNSTILE_SITE_KEY", "1x00000000000000000000AA")
TODAY = date.today().isoformat()

# ---------------------------------------------------------------- assets
def asset_version(path):
    with open(os.path.join(ROOT, path), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

V = {p: asset_version(p) for p in ["css/style.css", "js/main.js", "js/plant3d.js"]}

def ensure_webp():
    """Make .webp (and -800.webp) copies of any .jpg that lacks them."""
    d = os.path.join(ROOT, "assets", "img")
    for name in os.listdir(d):
        if not name.endswith(".jpg") or name == "og-image.jpg":
            continue
        base = os.path.join(d, name[:-4])
        if os.path.exists(base + ".webp"):
            continue
        im = Image.open(os.path.join(d, name)).convert("RGB")
        im.save(base + ".webp", quality=74, method=6)
        if im.width > 900:
            im.resize((800, round(im.height * 800 / im.width)), Image.LANCZOS).save(base + "-800.webp", quality=72, method=6)

ensure_webp()
_size = {}
def size(name):
    if name not in _size:
        with Image.open(os.path.join(ROOT, "assets", "img", name)) as im:
            _size[name] = im.size
    return _size[name]

def pic(name, alt, cls="", lazy=True, sizes="(max-width: 760px) 100vw, 50vw", attrs="", priority=False):
    """<picture> with WebP sources (800w + full) and the JPG as fallback."""
    w, h = size(name)
    stem = name.rsplit(".", 1)[0]
    if name.endswith(".jpg"):
        srcset = f"/assets/img/{stem}.webp {w}w"
        if os.path.exists(os.path.join(ROOT, "assets", "img", stem + "-800.webp")):
            srcset = f"/assets/img/{stem}-800.webp 800w, " + srcset
        source = f'<source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
    else:
        source = ""
    load = ' fetchpriority="high"' if priority else (' loading="lazy" decoding="async"' if lazy else "")
    c = f' class="{cls}"' if cls else ""
    return f'<picture>{source}<img src="/assets/img/{name}" alt="{html.escape(alt)}" width="{w}" height="{h}"{c}{load}{attrs}></picture>'

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

# ---------------------------------------------------------------- divisions
DIV = [
    {"slug": "biomass-gasifiers", "name": "Biomass gasifiers", "short": "Heat and power", "img": "commissioning-250kw-gasifier.jpg",
     "card": "Gasifiers and CHP systems that replace diesel, furnace oil and LPG in boilers, kilns, dryers and generators."},
    {"slug": "fuelwood-biomass-supply", "name": "Fuelwood and biomass supply", "short": "Plantation and farmers", "img": "plantation-mature.jpg",
     "card": "A 40,000-plant energy plantation, 3,000 farmers and our own wood-handling machines."},
    {"slug": "steel-fabrication", "name": "Steel fabrication", "short": "Design and build", "img": "steel-welding.jpg",
     "card": "Lattice structures, steel buildings, penstocks, tanks and pipelines, designed to international standards."},
    {"slug": "mini-hydro-power-plants", "name": "Mini-hydro power plants", "short": "GUGLER turbines", "img": "hydro-generators.jpg",
     "card": "Sole agent in Sri Lanka for GUGLER Kaplan, Pelton and Francis turbines from 5 kW to 10 MW."},
    {"slug": "material-handling", "name": "Material handling", "short": "Cranes to 160 t", "img": "crane.jpg",
     "card": "Overhead, gantry and jib cranes up to 160 tons, and suspended access platforms."},
    {"slug": "esco-energy-solutions", "name": "ESCO and energy audits", "short": "Energy efficiency", "img": "energy-audit-pipework.jpg",
     "card": "Energy audits and turnkey energy-saving projects with a payback guarantee."},
]
DIVS = {d["slug"]: d for d in DIV}

def reading_time(a):
    words = len(re.sub(r"<[^>]+>", " ", a["body"]).split())
    return max(3, round(words / 200))

def nice_date(iso):
    return date.fromisoformat(iso).strftime("%-d %B %Y") if os.name != "nt" else date.fromisoformat(iso).strftime("%#d %B %Y")

def article_cards(arts):
    """Grid of article cards linking into the knowledge hub."""
    return '<div class="grid-3">' + "".join(
        f'''<a class="acard" href="/insights/{a["slug"]}/" data-reveal><figure class="media media--wide">{pic(a["img"], "", sizes="(max-width: 760px) 100vw, 33vw")}</figure><span class="acard__meta">{reading_time(a)} min read</span><h3>{a["title"]}</h3><p>{a["desc"]}</p><span class="link">Read the guide {ARROW}</span></a>''' for a in arts) + "</div>"

# ---------------------------------------------------------------- structured data
ORG_ID = SITE + "/#org"
ORG = {
    "@context": "https://schema.org",
    "@type": ["Organization", "LocalBusiness"],
    "@id": ORG_ID,
    "name": "EnerFab (Pvt) Ltd",
    "alternateName": ["EnerFab", "EnerFab Green Engineering", "EFPL"],
    "url": SITE + "/",
    "logo": SITE + "/assets/img/enerfab-mark.png",
    "image": SITE + "/assets/img/og-image.jpg",
    "description": "Sri Lankan renewable energy and engineering company, founded in 2005: biomass gasifiers and CHP, fuelwood supply, steel fabrication, mini-hydro, material handling and ESCO energy services.",
    "foundingDate": "2005",
    "slogan": "Re-greening Sri Lanka",
    "email": EMAIL,
    "telephone": "+94-11-288-8821",
    "address": {"@type": "PostalAddress", "streetAddress": "No. 115/3, Rampart Road", "addressLocality": "Sri Jayawardenepura Kotte", "addressRegion": "Western Province", "addressCountry": "LK"},
    "areaServed": [{"@type": "Country", "name": "Sri Lanka"}],
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "16:00"}],
    "contactPoint": [
        {"@type": "ContactPoint", "telephone": "+94-11-288-8821", "email": EMAIL, "contactType": "sales", "areaServed": "LK", "availableLanguage": ["en"]},
        {"@type": "ContactPoint", "telephone": "+1-226-246-1363", "contactType": "sales", "areaServed": "CA", "availableLanguage": ["en"]}
    ],
    "knowsAbout": ["Biomass gasification", "Producer gas", "Combined heat and power", "Dual-fuel burners", "Fuelwood plantations", "Gliricidia", "Mini-hydro turbines", "Steel fabrication", "Overhead cranes", "Energy audits"],
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "EnerFab engineering divisions", "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "@id": f"{SITE}/solutions/{d['slug']}/#service", "name": d["name"], "url": f"{SITE}/solutions/{d['slug']}/"}} for d in DIV]},
    "sameAs": [LEGACY, "https://twitter.com/enerfabsl", "https://www.facebook.com/EnerFab-111641701442166", "https://www.youtube.com/channel/UCOWz3FGpK5kuBd6PYCL0LBg", "https://instagram.com/enerfab"]
}

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"

def crumbs_ld(items):
    return ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]})

def service_ld(d, desc):
    return ld({"@context": "https://schema.org", "@type": "Service", "@id": f"{SITE}/solutions/{d['slug']}/#service", "name": d["name"],
               "serviceType": d["name"], "description": desc, "url": f"{SITE}/solutions/{d['slug']}/", "provider": {"@id": ORG_ID},
               "areaServed": {"@type": "Country", "name": "Sri Lanka"}, "image": f"{SITE}/assets/img/{d['img']}"})

# ---------------------------------------------------------------- inline scripts (hashed into the CSP)
MOTION_JS = "if(!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('motion');setTimeout(function(){if(!window.gsap)document.documentElement.classList.remove('motion')},4000)"
IMPORTMAP = json.dumps({"imports": {"three": "/js/vendor/three.module.min.js", "three/addons/": "/js/vendor/three-addons/"}}, separators=(",", ":"))
def sha(s): return "'sha256-" + base64.b64encode(hashlib.sha256(s.encode()).digest()).decode() + "'"

# ---------------------------------------------------------------- page shell
def head(path, title, desc, extra="", three=False, image="og-image.jpg", noindex=False, preload=None):
    url = SITE + path
    t = html.escape(title, quote=True); d = html.escape(desc, quote=True)
    pre = f'\n<link rel="preload" as="image" href="{preload}" type="image/webp">' if preload else ""
    three_tags = (f'\n<script type="importmap">{IMPORTMAP}</script>\n<link rel="modulepreload" href="/js/vendor/three.module.min.js">') if three else ""
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    return f"""<!doctype html>
<html lang="en-LK" class="motion-pending">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en-LK" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="robots" content="{robots}">
<meta name="author" content="EnerFab (Pvt) Ltd">
<meta property="og:site_name" content="EnerFab">
<meta property="og:locale" content="en_LK">
<meta property="og:type" content="website">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="EnerFab engineers commissioning a biomass gasifier">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@enerfabsl">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITE}/assets/img/{image}">
<meta name="theme-color" content="#0c1510">
<meta name="format-detection" content="telephone=no">
<meta name="geo.region" content="LK-11">
<meta name="geo.placename" content="Sri Jayawardenepura Kotte">
<link rel="icon" type="image/png" sizes="96x96" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/enerfab-mark.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/css/style.css?v={V['css/style.css']}">{pre}
<script>{MOTION_JS}</script>{three_tags}
<script src="/js/vendor/gsap.min.js" defer></script>
<script src="/js/vendor/ScrollTrigger.min.js" defer></script>
<script src="/js/vendor/SplitText.min.js" defer></script>
<script src="/js/vendor/lenis.min.js" defer></script>
<script src="/js/main.js?v={V['js/main.js']}" defer></script>
{ld(ORG)}
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def header(active=""):
    def cur(p): return ' aria-current="page"' if p == active else ""
    menu = '<li><a href="/solutions/">All solutions</a></li>' + "".join(
        f'<li><a href="/solutions/{d["slug"]}/"{cur(d["slug"])}>{d["name"]} <small>{d["short"]}</small></a></li>' for d in DIV)
    return f"""<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="EnerFab, home"><img src="/assets/img/enerfab-logo-light.png" alt="EnerFab Green Engineering" width="511" height="155"></a>
    <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Main">
      <a href="/"{cur('home')}>Home</a>
      <a href="/about/"{cur('about')}>About</a>
      <div class="nav__drop">
        <button type="button" aria-expanded="false">Solutions <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
        <ul class="nav__menu">{menu}</ul>
      </div>
      <a href="/projects/"{cur('projects')}>Projects</a>
      <a href="/insights/"{cur('insights')}>Insights</a>
      <a href="/faq/"{cur('faq')}>FAQ</a>
      <a href="/contact/"{cur('contact')}>Contact</a>
      <a class="nav__phone" href="tel:{TEL}">Call {PHONE}</a>
      <a class="btn" href="/contact/#inquiry">Get a quote</a>
    </nav>
  </div>
</header>
<main id="main">
"""

SOCIAL = """<div class="socials">
          <a href="https://twitter.com/enerfabsl" aria-label="EnerFab on X" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.8 3h3.1l-6.8 7.7L22 21h-6.2l-4.9-6.4L5.3 21H2.2l7.3-8.3L1.9 3h6.4l4.4 5.8zm-1.1 16.2h1.7L7.4 4.7H5.6z"/></svg></a>
          <a href="https://www.facebook.com/EnerFab-111641701442166" aria-label="EnerFab on Facebook" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8V6.2c0-.8.2-1.2 1.4-1.2H17V2h-2.6C11.3 2 10 3.5 10 6v2H8v3h2v11h4V11h2.7l.3-3z"/></svg></a>
          <a href="https://www.youtube.com/channel/UCOWz3FGpK5kuBd6PYCL0LBg" aria-label="EnerFab on YouTube" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8zM9.7 15V9l5.8 3z"/></svg></a>
          <a href="https://instagram.com/enerfab" aria-label="EnerFab on Instagram" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg></a>
        </div>"""

def footer(three=False):
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="footer-brand" href="/"><img src="/assets/img/enerfab-logo-light.png" alt="EnerFab Green Engineering" width="511" height="155" loading="lazy"></a>
        <p class="muted" style="max-width:36ch">Biomass gasifiers, sustainable fuelwood and engineering services for industry in Sri Lanka since 2005.</p>
        {SOCIAL}
      </div>
      <div>
        <h4>Solutions</h4>
        <ul>{"".join(f'<li><a href="/solutions/{d["slug"]}/">{d["name"]}</a></li>' for d in DIV)}</ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/about/">About EnerFab</a></li>
          <li><a href="/projects/">Projects</a></li>
          <li><a href="/insights/">Energy insights</a></li>
          <li><a href="/faq/">Technical FAQ</a></li>
          <li><a href="/videos/">Videos</a></li>
          <li><a href="/recognition/">Recognition and press</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Head office</h4>
        <address>
        <ul>
          <li>No. 115/3, Rampart Road,<br>Sri Jayawardenepura Kotte, Sri Lanka</li>
          <li><a href="tel:{TEL}">{PHONE}</a></li>
          <li><a href="tel:{TEL_CA}">Canada: {PHONE_CA}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li class="muted">Monday to Friday, 9am to 4pm</li>
        </ul>
        </address>
      </div>
    </div>
    <p class="footer-word" aria-hidden="true">EnerFab</p>
    <div class="footer-bottom">
      <span>© 2005–<span data-year>{date.today().year}</span> EnerFab (Pvt) Ltd</span>
      <span>Re-greening Sri Lanka</span>
    </div>
  </div>
</footer>
{'<script type="module" src="/js/plant3d.js?v=' + V['js/plant3d.js'] + '"></script>' if three else ''}
</body>
</html>
"""

def page_hero(img, crumbs, h1, p):
    cr = '<li><a href="/">Home</a></li>' + "".join(
        (f'<li><a href="{u}">{n}</a></li>' if u else f'<li aria-current="page">{n}</li>') for n, u in crumbs)
    return f"""<section class="page-hero">
  <div class="page-hero__bg">{pic(img, "", lazy=False, sizes="100vw", priority=True)}</div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>{cr}</ol></nav>
    <h1 data-split="load">{h1}</h1>
    <p data-reveal>{p}</p>
  </div>
</section>
"""

def video(yt, title, label=None):
    t = html.escape(title, quote=True)
    return f"""<div class="video" data-yt="{yt}" data-title="{t}">
  <img src="https://i.ytimg.com/vi/{yt}/hqdefault.jpg" alt="" loading="lazy" decoding="async" width="480" height="360">
  <button type="button" aria-label="Play video: {t}"><span><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg></span></button>
  <div class="video__label">{label or title}</div>
</div>"""

def cta(h="Make an inquiry today.", p="Tell us what your boiler, dryer, kiln or generator runs on now. EnerFab’s engineers will be in touch to discuss your requirements."):
    return f"""<section class="sec--tight">
  <div class="wrap">
    <div class="cta" data-reveal>
      <h2>{h}</h2>
      <p>{p}</p>
      <div class="cta__row">
        <a class="btn btn--dark" href="/contact/#inquiry" data-magnetic>Get a quote {ARROW}</a>
        <a class="tel" href="tel:{TEL}">or call {PHONE}</a>
      </div>
    </div>
  </div>
</section>
"""

def plant_viewer():
    return f"""<div class="viewer" data-plant3d data-lazy>
      {pic("gasifier-plant-layout.jpg", "Isometric layout of an EnerFab gasifier power plant", cls="tour__fallback", sizes="100vw")}
      <p class="viewer__hint">Drag to turn. Tap a dot to see what each part does.</p>
    </div>"""

def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

PAGES = []  # (path, priority) for the sitemap
def page(path, rel, content, priority):
    write(rel, content); PAGES.append((path, priority))

def related(slugs):
    return '<div class="grid-3">' + "".join(
        f'<a class="panel" style="text-decoration:none;color:inherit" href="/solutions/{s}/" data-reveal><h3>{DIVS[s]["name"]}</h3><p class="muted" style="margin-bottom:18px">{DIVS[s]["card"]}</p><span class="link">Explore {ARROW}</span></a>' for s in slugs) + "</div>"

# ================================================================ HOME
tour_steps = [
    ("intro", None),
    ("Fuelwood", ("Fuel from sustainable energy plantations", "Gliricidia, Ipil Ipil, cinnamon, timber off-cuts and coconut shells, collected through a network of 3,000 farmers and grown on our own 40,000-plant plantation at Nawagaththegama.")),
    ("Hopper", ("Chopped to size, fed from above", "Fuelwood sticks are cut into small pieces for the gasifier. Our DM500 wood chopper handles 500 kg an hour, and our EWG 1 wood grab lifts a cubic metre of chips at a time.")),
    ("Reactor", ("Solid wood becomes a clean-burning gas", "Gasification converts solid fuel into a combustible gas called producer gas. EnerFab designs and fabricates its gasifiers in Sri Lanka.")),
    ("Heat", ("Heat for boilers, kilns and dryers", "Producer gas is piped just like LPG to a burner. With a dual-fuel burner you keep your boiler, and your old fuel stays on as backup. One rubber dryer has run this way since 2006, replacing 50 litres of diesel an hour.")),
    ("Power", ("Electricity from waste wood", "Producer gas runs an internal combustion engine and generator. At a wood processing plant, an EnerFab gasifier generator makes 200 kW from the factory’s own waste wood.")),
    ("Since 2005", ("Running for more than a decade", "Kandalama Hotel, Tea Factory Hotel, CW Mackie and other establishments have operated EnerFab gasifiers for over ten years, with EnerFab after-sales service throughout.")),
]
steps_html = ""
for i, (no, body) in enumerate(tour_steps):
    if i == 0:
        steps_html += f"""    <div class="step step--intro"><div class="wrap"><div class="step__card">
      <span class="label" data-reveal>Biomass renewable energy company · Sri Lanka</span>
      <h1 data-split="load">Biomass gasifiers and green energy for Sri Lankan industry</h1>
      <p class="lede" data-reveal>EnerFab replaces diesel, furnace oil and LPG with locally grown biomass, and supplies the fuelwood to keep it running. Engineering in Sri Lanka since 2005.</p>
      <div class="btn-row" data-reveal>
        <a class="btn btn--primary" href="/contact/#inquiry" data-magnetic>Get a quote {ARROW}</a>
        <a class="btn btn--ghost" href="/solutions/biomass-gasifiers/">How gasifiers work</a>
      </div>
      <p class="scroll-cue" aria-hidden="true"><span></span>Scroll to walk through a gasifier plant</p>
    </div></div></div>
"""
    else:
        h, p = body
        link = '<p><a class="link" href="/projects/">See the projects ' + ARROW + '</a></p>' if i == len(tour_steps) - 1 else ""
        steps_html += f"""    <div class="step"><div class="wrap"><div class="step__card">
      <span class="step__no">0{i} · {no}</span>
      <h2>{h}</h2>
      <p>{p}</p>{link}
    </div></div></div>
"""

home_desc = "EnerFab builds biomass gasifiers in Sri Lanka that replace diesel, furnace oil and LPG in boilers, dryers and generators, and supplies the fuelwood. Since 2005."
home = head("/", "Biomass Gasifiers Sri Lanka | Furnace Oil to Biomass | EnerFab", home_desc, three=True,
    extra=ld({"@context": "https://schema.org", "@type": "WebSite", "@id": SITE + "/#website", "name": "EnerFab", "alternateName": ["EnerFab Sri Lanka", "enerfab.lk"], "url": SITE + "/", "publisher": {"@id": ORG_ID}, "inLanguage": "en-LK"})
) + header("home") + f"""
<section class="tour" aria-label="Inside an EnerFab gasifier plant">
  <div class="tour__stage" data-plant3d data-tour>
    {pic("gasifier-plant-layout.jpg", "", cls="tour__fallback", lazy=False, sizes="100vw")}
  </div>
  <div class="tour__progress" aria-hidden="true">{"".join('<i></i>' for _ in tour_steps)}</div>
  <div class="tour__steps">
{steps_html}  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee__track">{"".join(f"<span>{d['name']}</span>" for d in DIV) * 2}</div></div>

<section class="sec">
  <div class="wrap">
    <span class="label" data-reveal>Who we are</span>
    <p class="statement">Founded in 2005, EnerFab brings biomass renewable energy to local industry through gasifiers and CHP systems, with the fuel grown on sustainable energy plantations.</p>
    <div class="counters">
      <div class="counter"><b data-count="2005" data-from="1990" data-plain="1">2005</b><span>EnerFab founded in Sri Lanka</span></div>
      <div class="counter"><b><span data-count="3000">3,000</span></b><span>farmers in our biomass collection network</span></div>
      <div class="counter"><b><span data-count="40000">40,000</span></b><span>plants on our Nawagaththegama plantation</span></div>
      <div class="counter"><b><span data-count="200">200</span><small>kW</small></b><span>of electricity from one factory’s waste wood</span></div>
    </div>
  </div>
</section>

<section class="sec sec--line" style="padding-bottom:0">
  <div class="wrap">
    <div class="head">
      <h2 data-split>Six engineering divisions</h2>
      <p class="lede" data-reveal>Gasification is our core. Around it, the same civil and mechanical engineers design, build and install the rest.</p>
    </div>
  </div>
  <div class="hrail">
    <div class="hrail__track">
{"".join(f'''      <a class="scard" href="/solutions/{d["slug"]}/">{pic(d["img"], "", sizes="(max-width: 760px) 82vw, 460px")}<span class="scard__no">0{i+1}</span><div class="scard__body"><h3>{d["name"]}</h3><p>{d["card"]}</p><span class="scard__go">{ARROW}</span></div></a>
''' for i, d in enumerate(DIV))}    </div>
  </div>
  <p class="hrail__hint">Swipe to see all six</p>
  <div style="height:clamp(88px,13vw,180px)"></div>
</section>

<section class="sec sec--line">
  <div class="wrap split split--wr">
    <figure class="media media--tall" data-mask>{pic("producer-gas-flame.jpg", "Producer gas flame from an EnerFab gasifier", attrs=' data-parallax="6"')}<figcaption>EnerFab producer gas flame</figcaption></figure>
    <div>
      <span class="label" data-reveal>Furnace oil and diesel to biomass</span>
      <h2 data-split>Keep your boiler. Change the fuel.</h2>
      <p class="lede" data-reveal>A gasifier with a dual-fuel burner switches a diesel or furnace-oil boiler to producer gas. You keep operating the same boiler, and the fuel you used before stays available as a backup.</p>
      <p data-reveal>Compared with a wood-fired boiler, this conversion gives better efficiency, a better response to changes in load, and lower particulate emissions. It works for furnaces, kilns and dryers too.</p>
      <p data-reveal><a class="link" href="/solutions/biomass-gasifiers/">Biomass gasifiers and CHP {ARROW}</a></p>
    </div>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap split">
    <div>
      <span class="label" data-reveal>Nawagaththegama, Puttalam district</span>
      <h2 data-split>From scrubland to an energy forest</h2>
      <p data-reveal>Our model fuelwood plantation was planted in the Maha season of 2008: 40,000 plants at 2 by 1 metre spacing, on land that was scrubland. Today it is lush, mature growth that adds nitrogen to the soil, supplies fuel to industry and improves the microclimate.</p>
      <p data-reveal><a class="link" href="/solutions/fuelwood-biomass-supply/">Fuelwood and biomass supply {ARROW}</a></p>
    </div>
    <div class="ba" data-sweep data-reveal>
      {pic("plantation-scrubland.jpg", "The Nawagaththegama site as scrubland before planting")}
      {pic("plantation-mature.jpg", "The same land as a mature fuelwood plantation", cls="ba__after")}
      <span class="ba__line"></span>
      <span class="ba__tag ba__tag--l">Before</span><span class="ba__tag ba__tag--r">Today</span>
      <input type="range" min="0" max="100" value="50" aria-label="Compare the land before and after planting">
    </div>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap">
    <figure class="quote" style="max-width:1000px">
      <blockquote data-split>“In Sri Lanka, two companies are involved in the design and manufacture of gasifiers. The leading company is EnerFab (Pvt) Ltd.”</blockquote>
      <figcaption data-reveal>{pic("dr-sugathapala.jpg", "")}<div><b>Dr. A.G.T. Sugathapala</b><span>Head, Department of Mechanical Engineering, University of Moratuwa. Tech Monitor, 2007</span></div></figcaption>
    </figure>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap">
    <div class="head">
      <h2 data-split>Energy insights</h2>
      <a class="link" href="/insights/" data-reveal>All guides {ARROW}</a>
    </div>
    {article_cards(ARTICLES[:3])}
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap">
    <div class="head">
      <h2 data-split>See the plants running</h2>
      <a class="link" href="/videos/" data-reveal>All videos {ARROW}</a>
    </div>
    <div class="grid-3">
      <div data-reveal>{video("Az4ZQNXVZ7U", "Gasifier installed by EnerFab to replace 50 litres per hour of diesel in a rubber processing plant", "Replacing 50 L/hr of diesel")}</div>
      <div data-reveal>{video("334j_wDnESI", "200 kW gasifier generator by EnerFab", "200 kW gasifier generator")}</div>
      <div data-reveal>{video("tKnqCnPaES8", "EnerFab WBG 10", "EnerFab WBG 10")}</div>
    </div>
  </div>
</section>
{cta()}""" + footer(three=True)
page("/", "index.html", home, "1.0")

# ================================================================ SOLUTIONS HUB
hub = head("/solutions/", "Engineering Solutions Sri Lanka | Biomass, Hydro, Steel | EnerFab",
    "EnerFab’s six divisions: biomass gasifiers and CHP, fuelwood supply, steel fabrication, GUGLER mini-hydro, cranes and material handling, and ESCO energy audits in Sri Lanka.",
    extra=crumbs_ld([("Home", "/"), ("Solutions", "/solutions/")])
) + header() + page_hero("steel-welding.jpg", [("Solutions", None)], "Engineering for a renewable Sri Lanka",
    "Biomass gasification is our core. Around it we design, fabricate and install everything from fuelwood systems to hydro turbines and cranes.") + f"""
<section class="sec">
  <div class="wrap" style="display:grid;gap:clamp(64px,9vw,120px)">
{"".join(f'''    <article class="split{' split--wr' if i % 2 else ' split--wl'}">
      {'<a href="/solutions/' + d["slug"] + '/" class="media media--wide" data-mask>' + pic(d["img"], d["name"], attrs=' data-parallax="5"') + '</a>' if i % 2 else ''}
      <div>
        <span class="solution__no">0{i+1}</span>
        <h2 data-split>{d["name"]}</h2>
        <p class="lede" data-reveal>{d["card"]}</p>
        <p data-reveal><a class="link" href="/solutions/{d["slug"]}/">Explore {d["name"].lower()} {ARROW}</a></p>
      </div>
      {'' if i % 2 else '<a href="/solutions/' + d["slug"] + '/" class="media media--wide" data-mask>' + pic(d["img"], d["name"], attrs=' data-parallax="5"') + '</a>'}
    </article>
''' for i, d in enumerate(DIV))}  </div>
</section>
{cta()}""" + footer()
page("/solutions/", "solutions/index.html", hub, "0.9")

# ================================================================ DIVISION PAGES
def further_reading(slug):
    arts = [a for a in ARTICLES if slug in a["divs"]][:3]
    if not arts:
        return ""
    return f"""
<section class="sec sec--line">
  <div class="wrap">
    <div class="head"><h2 data-split>Further reading</h2><a class="link" href="/insights/" data-reveal>All energy guides {ARROW}</a></div>
    {article_cards(arts)}
  </div>
</section>
"""

def division(slug, title, desc, h1, intro, body, rel, three=False, extra=""):
    d = DIVS[slug]
    content = head(f"/solutions/{slug}/", title, desc, three=three,
        extra=crumbs_ld([("Home", "/"), ("Solutions", "/solutions/"), (d["name"], f"/solutions/{slug}/")]) + service_ld(d, desc) + extra
    ) + header(slug) + page_hero(d["img"], [("Solutions", "/solutions/"), (d["name"], None)], h1, intro) + body + further_reading(slug) + f"""
<section class="sec sec--line">
  <div class="wrap">
    <div class="head"><h2 data-split>Related solutions</h2></div>
    {related(rel)}
  </div>
</section>
{cta()}""" + footer(three=three)
    page(f"/solutions/{slug}/", f"solutions/{slug}/index.html", content, "0.9")

# ---- Biomass gasifiers
division("biomass-gasifiers",
    "Biomass Gasifiers Sri Lanka | Diesel & Furnace Oil to Biomass | EnerFab",
    "Biomass gasifiers and CHP for Sri Lankan industry: dual-fuel burners that switch diesel and furnace-oil boilers to producer gas, and gasifier generators up to 250 kWe.",
    "Biomass gasifiers and CHP systems",
    "Turn wood into a gas that fires your boiler, kiln or dryer, or runs a generator. Designed and fabricated by EnerFab in Sri Lanka.",
    f"""
<section class="sec">
  <div class="wrap split split--top">
    <div>
      <span class="label" data-reveal>What we replace</span>
      <h2 data-split>Off diesel, furnace oil and LPG</h2>
      <p class="lede" data-reveal>EnerFab biomass systems can replace diesel, furnace oil (HFO) and LPG fired boilers, furnaces, kilns and dryers, and the fuel in internal combustion engines that drive electrical generators.</p>
      <p data-reveal>We can also install combined heat and power (CHP) plants that supply electricity while using the waste heat for thermal energy. EnerFab is known for proposing new ways to cut the cost of thermal and electrical systems, using gasifiers we design and fabricate ourselves.</p>
      <p data-reveal>Because we run energy plantations and an out-grower network of biomass suppliers, we can also supply your biomass on contract, so the plant always has fuel.</p>
    </div>
    <div class="panel" data-reveal>
      <h3>What EnerFab provides</h3>
      <ul class="checks">
        <li>Biomass gasifiers for industrial heating and electrical power generation</li>
        <li>Combined heat and power (CHP) systems</li>
        <li>Fuelwood from short-rotation coppicing of fast-growing leguminous trees</li>
        <li>Management contracts to operate plants supplied by EnerFab</li>
        <li>Spare parts and breakdown maintenance for every installation</li>
      </ul>
    </div>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap">
    <div class="head"><h2 data-split>Inside a gasifier plant</h2><p class="lede" data-reveal>Turn the model and tap the dots to follow fuelwood from the store to the flame and the engine.</p></div>
    <div data-reveal>{plant_viewer()}</div>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap">
    <div class="head"><h2 data-split>How the conversion works</h2></div>
    <ol class="process">
      <li data-reveal><h3>Fuelwood in</h3><p>Fuelwood such as Gliricidia is chopped into small pieces and fed to the gasifier.</p></li>
      <li data-reveal><h3>Gasification</h3><p>The gasifier converts the solid fuel into a combustible producer gas.</p></li>
      <li data-reveal><h3>Piped like LPG</h3><p>The gas is piped to a burner on your boiler or dryer, or to a gas engine.</p></li>
      <li data-reveal><h3>Heat and power</h3><p>Thermal energy, electricity, or both together as combined heat and power.</p></li>
    </ol>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap">
    <div class="head"><h2 data-split>Gasifier conversion compared</h2><p class="lede" data-reveal>Why EnerFab converts boilers with a gasifier and dual-fuel burner rather than replacing them with a wood-fired boiler.</p></div>
    <div class="table-wrap" data-reveal>
      <table>
        <caption class="sr-only">Gasifier conversion compared with a wood-fired boiler</caption>
        <thead><tr><th scope="col"></th><th scope="col">Gasifier + dual-fuel burner</th><th scope="col">Wood-fired boiler</th></tr></thead>
        <tbody>
          <tr><th scope="row">Your existing boiler</th><td>Kept and reused</td><td>Replaced</td></tr>
          <tr><th scope="row">Backup fuel</th><td>Diesel or furnace oil stays connected</td><td>None</td></tr>
          <tr><th scope="row">Efficiency</th><td>Better</td><td>Lower</td></tr>
          <tr><th scope="row">Response to load changes</th><td>Better</td><td>Slower</td></tr>
          <tr><th scope="row">Particulate emissions</th><td>Less</td><td>More</td></tr>
        </tbody>
      </table>
    </div>
    <h3 style="margin:56px 0 18px" data-reveal>Reported figures</h3>
    <div class="table-wrap" data-reveal>
      <table>
        <caption class="sr-only">Gasifier figures reported in Tech Monitor, July–August 2007</caption>
        <thead><tr><th scope="col">Application</th><th scope="col">Capacity</th><th scope="col">Efficiency (claimed)</th><th scope="col">Installed cost</th></tr></thead>
        <tbody>
          <tr><td>EnerFab gasifiers for electricity</td><td>1 – 250 kWe</td><td>about 30% overall</td><td>USD 800 – 1,500 / kW</td></tr>
          <tr><td>Thermal gasifiers in Sri Lanka</td><td>100 – 350 kW</td><td>70 – 80%</td><td>USD 200 – 300 / kW</td></tr>
        </tbody>
      </table>
    </div>
    <p class="muted" style="margin-top:14px;font-size:.92rem">Source: Dr. A.G.T. Sugathapala, University of Moratuwa, in Tech Monitor, July–August 2007. Costs are 2007 figures; ask us for a current quote.</p>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap grid-2" style="gap:56px 32px">
    <div data-reveal>
      {video("Az4ZQNXVZ7U", "Gasifier installed by EnerFab to replace 50 litres per hour of diesel in a rubber processing plant", "Thermal: replacing 50 L/hr of diesel")}
      <h3 style="margin-top:26px">Thermal applications</h3>
      <p>Gasification converts solid fuel into a combustible gas, which can be piped just like LPG to a burner on a boiler or dryer.</p>
      <p class="muted">This dryer in a rubber processing plant had a diesel burner. The EnerFab team replaced it with a producer-gas burner and a gasifier, and it has operated from 2006 to date.</p>
    </div>
    <div data-reveal>
      {video("088d9Otk_18", "EnerFab Green Engineering biomass gasifier generator set", "Electrical: gasifier generator set")}
      <h3 style="margin-top:26px">Electrical applications</h3>
      <p>Producer gas can run an internal combustion engine, which turns a generator to produce electricity.</p>
      <p class="muted">EnerFab installed this gasifier generator at a wood processing plant in Sri Lanka. It makes 200 kW of electricity from waste wood, and has an unused potential of 400 kW of thermal energy from the engine’s exhaust and cooling system.</p>
    </div>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap split">
    <figure class="media media--wide" data-mask>{pic("kandalama-gasifier.jpg", "EnerFab gasifier at Kandalama Hotel")}<figcaption>Gasifier at Kandalama Hotel</figcaption></figure>
    <div>
      <h2 data-split>Serving industry since 2005</h2>
      <p data-reveal>Kandalama Hotel and Tea Factory Hotel of the Aitken Spence Group, CW Mackie and other establishments have operated EnerFab gasifiers for more than a decade. In 2017 EnerFab installed a 200 kW electrical system, showing producer gas is clean enough to run an internal combustion engine.</p>
      <p data-reveal>We have provided after-sales service to these industries since 2005. These long-running installations have proven economical while being far kinder to the environment.</p>
      <p data-reveal><a class="link" href="/projects/">All projects {ARROW}</a> &nbsp; <a class="link" href="/faq/#gasifiers">Gasifier FAQ {ARROW}</a></p>
    </div>
  </div>
</section>
""", ["fuelwood-biomass-supply", "esco-energy-solutions", "steel-fabrication"], three=True)

# ---- Fuelwood
products = ld({"@context": "https://schema.org", "@graph": [
    {"@type": "Product", "name": "EnerFab Wood Grab EWG 1", "brand": {"@type": "Brand", "name": "EnerFab"}, "manufacturer": {"@id": ORG_ID},
     "image": SITE + "/assets/img/wood-grab-open.jpg", "description": "Wood grab for mass-scale wood handling at biomass power plants. Grabs 1 cubic metre of wood chips at 20% moisture. Length 1,930 mm; jaw diameter 1,120 mm closed and 2,200 mm open.",
     "offers": {"@type": "Offer", "price": "10000", "priceCurrency": "USD", "seller": {"@id": ORG_ID}, "url": SITE + "/solutions/fuelwood-biomass-supply/"}},
    {"@type": "Product", "name": "EnerFab Wood Chopper DM500", "brand": {"@type": "Brand", "name": "EnerFab"}, "manufacturer": {"@id": ORG_ID},
     "image": SITE + "/assets/img/wood-chopper-dm500.jpg", "description": "Wood chopper that cuts fuelwood sticks into small pieces for gasifiers. Processes 500 kg of fuelwood per hour.",
     "offers": {"@type": "Offer", "price": "5000", "priceCurrency": "USD", "seller": {"@id": ORG_ID}, "url": SITE + "/solutions/fuelwood-biomass-supply/"}}]})
division("fuelwood-biomass-supply",
    "Biomass Fuel Suppliers Sri Lanka | Fuelwood & Gliricidia | EnerFab",
    "Sustainable biomass fuel supply in Sri Lanka: EnerFab’s 40,000-plant Nawagaththegama plantation, 3,000 farmers, Gliricidia fuelwood, the DM500 wood chopper and EWG 1 wood grab.",
    "Sustainable fuelwood and biomass supply",
    "A secure fuel supply for your biomass plant: our own energy plantation, thousands of suppliers and machines we designed to handle the wood.",
    f"""
<section class="sec">
  <div class="wrap split split--top">
    <div>
      <span class="label" data-reveal>Energy partner, end to end</span>
      <h2 data-split>Your fuel, secured</h2>
      <p class="lede" data-reveal>EnerFab pioneered gasification-based biomass energy in Sri Lanka and has completed industrial energy conversions in many sectors. As your energy partner, we cover every part of the business, including fuelwood supply and plantations, to keep your plant safely supplied.</p>
      <p data-reveal>Fuelwood comes from short-rotation coppicing of fast-growing leguminous trees, collected through a network of 3,000 farmers and a supplier base of more than 2,000 across the island, outside the North and East.</p>
    </div>
    <div class="ba" data-sweep data-reveal>
      {pic("plantation-2008-seedlings.jpg", "Young fuelwood plants at 2 by 1 metre spacing in 2008")}
      {pic("plantation-mature.jpg", "The plantation at maturity", cls="ba__after")}
      <span class="ba__line"></span>
      <span class="ba__tag ba__tag--l">2008</span><span class="ba__tag ba__tag--r">Mature</span>
      <input type="range" min="0" max="100" value="50" aria-label="Compare the plantation in 2008 and at maturity">
    </div>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap">
    <div class="head"><h2 data-split>Nawagaththegama model plantation</h2><p class="lede" data-reveal>Puttalam district. Planted in the Maha season of 2008 on former scrubland.</p></div>
    <div class="counters" style="margin-top:0">
      <div class="counter"><b><span data-count="40000">40,000</span></b><span>plants</span></div>
      <div class="counter"><b>2 × 1<small>m</small></b><span>planting spacing</span></div>
      <div class="counter"><b data-count="2008" data-from="1995" data-plain="1">2008</b><span>established, Maha season</span></div>
      <div class="counter"><b><span data-count="3000">3,000</span></b><span>farmers in the collection network</span></div>
    </div>
    <p class="measure" style="margin-top:40px" data-reveal>The land was scrubland before planting. It is now lush green vegetation that enriches the soil with nitrogen, supplies fuel to industry and improves the local microclimate.</p>
    <div class="gallery" style="margin-top:40px" data-reveal>{"".join(f'<button type="button">{pic(n, a, sizes="(max-width: 760px) 50vw, 16vw")}</button>' for n, a in [("plantation-scrubland.jpg", "Nawagaththegama site before planting"), ("plantation-2008-seedlings.jpg", "Young plants at 2 by 1 metre spacing"), ("plantation-young.jpg", "Plantation establishing"), ("plantation-growing.jpg", "Plantation growing"), ("plantation-mature.jpg", "Mature energy crop"), ("plantation-hills.jpg", "The plantation across the hills")])}</div>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap grid-2">
    <div class="panel" data-reveal>
      <h3>Why a power plant needs a reliable fuelwood supplier</h3>
      <p>If you invest in a biomass power plant, you need real control over your own fuelwood supply. Authorities expect it when you plan the project and seek approvals.</p>
      <p style="margin:0">If supply networks fall short, the whole project fails unless your own supply carries it until the network recovers. In EnerFab’s view, your own share should be at least 50%.</p>
    </div>
    <div class="panel" data-reveal>
      <h3>Why choose EnerFab as your supplier</h3>
      <ul class="checks">
        <li>A market that can be linked directly with plantations</li>
        <li>More than 2,000 suppliers across Sri Lanka, outside the North and East</li>
        <li>Gliricidia, Ipil Ipil, cinnamon, timber off-cuts, coconut shells and other approved fuelwood</li>
        <li>We know each fuel’s advantages, where it grows and its seasonality</li>
        <li>Our own transport system, scalable up or down at any time</li>
      </ul>
    </div>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap">
    <div class="head"><h2 data-split>Wood-handling equipment by EnerFab</h2></div>
    <div class="grid-2">
      <div class="panel product" data-reveal>
        <div class="product__imgs">{pic("wood-grab-open.jpg", "EnerFab Wood Grab EWG 1, jaws open", sizes="180px")}{pic("wood-grab-closed.jpg", "EnerFab Wood Grab EWG 1, jaws closed", sizes="180px")}</div>
        <div>
          <h3>Wood Grab EWG 1</h3>
          <p>Designed by EnerFab engineers after extensive field trials, as one part of a complete wood-handling system at a power plant. Suitable for mass-scale wood handling.</p>
          <dl class="spec">
            <div><dt>Grabs</dt><dd>1 m³ of chips</dd></div>
            <div><dt>At moisture</dt><dd>20%</dd></div>
            <div><dt>Length</dt><dd>1,930 mm</dd></div>
            <div><dt>Jaw diameter</dt><dd>1,120 – 2,200 mm</dd></div>
            <div><dt>Price</dt><dd>US$ 10,000</dd></div>
          </dl>
          <p style="margin-top:20px"><a class="link" href="/contact/?interest=Wood%20Grab%20EWG%201#inquiry">Ask about the EWG 1 {ARROW}</a></p>
        </div>
      </div>
      <div class="panel product" data-reveal>
        <div class="product__imgs">{pic("wood-chopper-dm500.jpg", "EnerFab Wood Chopper DM500", sizes="180px")}</div>
        <div>
          <h3>Wood Chopper DM500</h3>
          <p>Chops fuelwood sticks into small pieces for gasifiers. For the power it uses, it reduces wood more effectively than any other wood chopper designed in Sri Lanka.</p>
          <dl class="spec">
            <div><dt>Throughput</dt><dd>500 kg/hr</dd></div>
            <div><dt>Use</dt><dd>Gasifier feed</dd></div>
            <div><dt>Price</dt><dd>US$ 5,000</dd></div>
          </dl>
          <p style="margin-top:20px"><a class="link" href="/contact/?interest=Wood%20Chopper%20DM500#inquiry">Ask about the DM500 {ARROW}</a></p>
        </div>
      </div>
    </div>
  </div>
</section>
<dialog class="lightbox" data-gallery><button class="lightbox__close" type="button" aria-label="Close">×</button><img src="/assets/img/plantation-mature.jpg" alt=""><p></p></dialog>
""", ["biomass-gasifiers", "material-handling", "esco-energy-solutions"], extra=products)

# ---- Steel
division("steel-fabrication",
    "Industrial Steel Fabrication Sri Lanka | Structures & Tanks | EnerFab",
    "Industrial steel fabrication in Sri Lanka by EnerFab’s civil and mechanical engineers: lattice structures, steel buildings, penstocks, HFO and diesel tanks and pipelines.",
    "Industrial steel fabrication",
    "Design, fabrication and installation by qualified civil and mechanical engineers, to international design standards.",
    f"""
<section class="sec">
  <div class="wrap split split--top">
    <div>
      <span class="label" data-reveal>A core competency</span>
      <h2 data-split>Engineered before it is welded</h2>
      <p class="lede" data-reveal>Design and fabrication is one of EnerFab’s core competencies. We employ qualified, experienced civil and mechanical engineers and work to international design standards.</p>
      <p data-reveal>Our design process uses analytical, computational and software modelling. That lets us offer designs that are stronger and better made, at a lower cost. EnerFab also specialises in corrosion protection.</p>
    </div>
    <div class="panel" data-reveal>
      <h3>We design, fabricate and install</h3>
      <ul class="checks">
        <li>Steel lattice structures</li><li>Steel buildings</li><li>Large advertising structures</li><li>Steel penstock pipelines</li>
        <li>Liquid storage tanks for water, diesel and HFO</li><li>Small-scale hydro power plants</li><li>Water, diesel and HFO pipelines</li><li>Other civil engineering works</li>
      </ul>
    </div>
  </div>
</section>
<section class="sec sec--line">
  <div class="wrap grid-2">
    <figure class="media media--wide" data-mask>{pic("steel-lattice.jpg", "Steel lattice structure fabricated by EnerFab", attrs=' data-parallax="5"')}</figure>
    <figure class="media media--wide" data-mask>{pic("steel-sections.jpg", "Fabricated steel box sections", attrs=' data-parallax="5"')}</figure>
  </div>
</section>
""", ["mini-hydro-power-plants", "material-handling", "biomass-gasifiers"])

# ---- Hydro
division("mini-hydro-power-plants",
    "Mini Hydro Power Plants Sri Lanka | GUGLER Turbines | EnerFab",
    "EnerFab is sole agent for GUGLER water turbines in Sri Lanka: Kaplan, Pelton and Francis turbines from 5 kW to 10 MW, with design, installation and servicing.",
    "Mini-hydro power plants",
    "EnerFab (Pvt) Ltd is the sole agent for GUGLER Water Turbines in Sri Lanka.",
    f"""
<section class="sec">
  <div class="wrap split split--top">
    <div>
      <span class="label" data-reveal>Turnkey hydro engineering</span>
      <h2 data-split>Every head, every output</h2>
      <p class="lede" data-reveal>We offer the entire range of hydro power equipment and services: design, engineering, manufacturing, installation and servicing, for all heads and outputs and all types of turbine, in horizontal or vertical orientation.</p>
      <p data-reveal>GUGLER is one of the world’s technology leaders in water turbines, supplying Kaplan, Pelton and Francis turbines with outputs from 5 kW to 10 MW.</p>
      <ul class="tags" data-reveal><li>Kaplan</li><li>Pelton</li><li>Francis</li><li>5 kW – 10 MW</li><li>Horizontal and vertical</li></ul>
    </div>
    <figure class="media media--wide" data-mask>{pic("hydro-generators.jpg", "Turbine generators at a mini-hydro power plant", attrs=' data-parallax="5"')}</figure>
  </div>
</section>
<section class="sec sec--line">
  <div class="wrap split split--top">
    <h2 data-split>Completed projects</h2>
    <ol class="timeline"><span class="timeline__fill"></span>
      <li data-reveal><span class="timeline__year">Dec 2009</span><h3>Aitken Spence Power</h3><p>Aitken Spence Power signed for GUGLER hydro turbines for one of its mini-hydro development sites. EnerFab was assigned the installation of the machinery and local technical support.</p></li>
      <li data-reveal><span class="timeline__year">Mar 2010</span><h3>Kirkoswald hydropower project</h3><p>Bogo Power (Pvt) Ltd, a holding company of the Stassen Group, awarded GUGLER Water Turbines a turnkey contract for three Francis turbines with an installed capacity of 4.5 MW, including all electromechanical equipment.</p></li>
    </ol>
  </div>
</section>
""", ["steel-fabrication", "biomass-gasifiers", "esco-energy-solutions"])

# ---- Material handling
division("material-handling",
    "Cranes & Material Handling Sri Lanka | Up to 160 Tons | EnerFab",
    "Overhead travelling, gantry, suspension and jib cranes up to 160 tons and suspended access platforms in Sri Lanka, from EnerFab with ATT Lifting Equipment.",
    "Material handling and cranes",
    "Supply and installation of standard cranes and hoists, and a design-and-build service for special requirements.",
    f"""
<section class="sec">
  <div class="wrap split split--top">
    <div>
      <span class="label" data-reveal>Lifting, handling, access</span>
      <h2 data-split>Loads up to 160 tons</h2>
      <p class="lede" data-reveal>Our cranes handle a wide range of loads with simple push-button control. EnerFab supplies and installs standard cranes and hoists, and offers a design and manufacturing service for special requirements.</p>
      <p data-reveal>International partner: ATT Lifting Equipment Technology JSC (<a href="https://www.attecranes.com" rel="noopener" target="_blank">attecranes.com</a>).</p>
      <h3 style="margin-top:36px" data-reveal>Suspended powered access</h3>
      <ul class="checks checks--cols" data-reveal><li>Temporary suspended access</li><li>Permanent suspended access</li><li>Industry-specific products</li><li>Safety systems</li></ul>
    </div>
    <div>
      <figure class="media media--wide" style="margin-bottom:24px" data-mask>{pic("crane.jpg", "Heavy crane on site", attrs=' data-parallax="5"')}</figure>
      <div class="table-wrap" data-reveal>
        <table>
          <caption class="sr-only">Crane types with maximum load and span</caption>
          <thead><tr><th scope="col">Crane type</th><th scope="col">Load</th><th scope="col">Span</th></tr></thead>
          <tbody>
            <tr><td>Single girder overhead travelling</td><td>12.5 t</td><td>30 m</td></tr>
            <tr><td>Double girder overhead travelling</td><td>160 t</td><td>30 m</td></tr>
            <tr><td>Single girder suspension</td><td>12.5 t</td><td>30 m</td></tr>
            <tr><td>Jib crane</td><td>5 t</td><td>8 m</td></tr>
            <tr><td>Light crane</td><td>2 t</td><td>12 m</td></tr>
            <tr><td>Gantry and semi-gantry</td><td>160 t</td><td>50 m</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>
""", ["steel-fabrication", "fuelwood-biomass-supply", "mini-hydro-power-plants"])

# ---- ESCO
division("esco-energy-solutions",
    "ESCO Energy Solutions Sri Lanka | Energy Audits | EnerFab",
    "ESCO energy services for Sri Lankan factories: preliminary and detailed energy audits and turnkey energy-saving projects with a payback guarantee. 15+ detailed audits completed.",
    "ESCO and energy audits",
    "We find where your factory loses energy, then fix it on a turnkey basis with a payback guarantee.",
    f"""
<section class="sec">
  <div class="wrap">
    <div class="grid-2">
      <div class="panel" data-reveal><h3>Consultancy services</h3><ul class="checks"><li>Preliminary energy audits</li><li>Detailed energy audits</li><li>Other energy studies</li></ul></div>
      <div class="panel" data-reveal><h3>Energy-saving implementation</h3><p style="margin:0">EnerFab implements energy-saving projects on a turnkey basis, with a payback guarantee.</p></div>
      <div class="panel" data-reveal><h3>Metering instruments</h3><p style="margin:0">EnerFab is equipped with modern energy metering instruments for on-site measurement.</p></div>
      <div class="panel" data-reveal><h3>Experience</h3><p style="margin:0">More than 15 detailed energy audits completed in knitted-garment factories, tea factories and other sectors.</p></div>
    </div>
  </div>
</section>
<section class="sec sec--line">
  <div class="wrap split">
    <figure class="media media--wide" data-mask>{pic("energy-audit-pipework.jpg", "Industrial pipework and metering", attrs=' data-parallax="5"')}</figure>
    <div>
      <h2 data-split>Audit first, then switch fuels</h2>
      <p data-reveal>An energy audit shows where heat and power are lost. Where a boiler, dryer or kiln still burns diesel, furnace oil or LPG, a biomass gasifier conversion is often the next step.</p>
      <p data-reveal><a class="link" href="/solutions/biomass-gasifiers/">Biomass gasifiers {ARROW}</a></p>
    </div>
  </div>
</section>
""", ["biomass-gasifiers", "fuelwood-biomass-supply", "steel-fabrication"])

# ================================================================ PROJECTS
proj = head("/projects/", "Biomass Gasifier Projects Sri Lanka | Case Studies | EnerFab",
    "EnerFab projects since 2005: gasifiers at Kandalama and Tea Factory hotels, a 200 kW gasifier generator, a diesel dryer converted in 2006, GUGLER mini-hydro and energy audits.",
    extra=crumbs_ld([("Home", "/"), ("Projects", "/projects/")]) + ld({"@context": "https://schema.org", "@type": "CollectionPage", "url": SITE + "/projects/",
        "name": "EnerFab projects", "publisher": {"@id": ORG_ID},
        "hasPart": [{"@type": "Article", "headline": pr["name"], "url": f"{SITE}/projects/{pr['slug']}/"} for pr in PROJECTS]})
) + header("projects") + page_hero("kandalama-gasifier.jpg", [("Projects", None)], "Projects running since 2005",
    "Gasifiers, plantations, hydro and energy audits delivered by EnerFab across Sri Lanka.") + f"""
<section class="sec">
  <div class="wrap" style="display:grid;gap:clamp(56px,8vw,100px)">
{"".join(f'''    <article class="split{' split--wr' if i % 2 == 0 else ' split--wl'}">
      {'<a class="media media--wide" data-mask href="/projects/' + pr["slug"] + '/" tabindex="-1" aria-hidden="true">' + pic(pr["img"], pr["name"]) + '</a>' if i % 2 == 0 else ''}
      <div>
        <span class="solution__no">{pr["tag"]}</span>
        <h2 data-split style="font-size:clamp(1.8rem,3.6vw,3rem)"><a href="/projects/{pr["slug"]}/" style="color:inherit;text-decoration:none">{pr["name"]}</a></h2>
        <p class="lede" data-reveal style="color:var(--green)">{pr["sub"]}</p>
        <p data-reveal>{pr["card"]}</p>
        <p data-reveal><a class="link" href="/projects/{pr["slug"]}/">Read the project {ARROW}</a> &nbsp; <a class="link" href="/solutions/{pr["div"]}/">{DIVS[pr["div"]]["name"]} {ARROW}</a></p>
      </div>
      {'' if i % 2 == 0 else '<a class="media media--wide" data-mask href="/projects/' + pr["slug"] + '/" tabindex="-1" aria-hidden="true">' + pic(pr["img"], pr["name"]) + '</a>'}
    </article>
''' for i, pr in enumerate(PROJECTS))}  </div>
</section>
{cta()}""" + footer()
page("/projects/", "projects/index.html", proj, "0.8")

def project_cards(prs):
    return '<div class="grid-3">' + "".join(
        f'<a class="panel" style="text-decoration:none;color:inherit" href="/projects/{o["slug"]}/" data-reveal><span class="solution__no">{o["tag"]}</span><h3>{o["name"]}</h3><p class="muted" style="margin-bottom:18px">{o["card"]}</p><span class="link">Read the project {ARROW}</span></a>' for o in prs) + "</div>"

for n, pr in enumerate(PROJECTS):
    url = f"{SITE}/projects/{pr['slug']}/"
    pr_ld = ld({"@context": "https://schema.org", "@type": "Article", "@id": url + "#article", "headline": pr["name"] + ": " + pr["sub"],
        "description": pr["desc"], "image": f"{SITE}/assets/img/{pr['img']}", "datePublished": "2026-11-14",
        "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "mainEntityOfPage": url, "inLanguage": "en-LK",
        "about": {"@id": f"{SITE}/solutions/{pr['div']}/#service"}})
    facts = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in pr["facts"])
    vids = "".join(f'<div data-reveal style="margin:28px 0">{video(v, t)}</div>' for v, t in pr["video"])
    gal = ""
    if len(pr["gallery"]) > 1:
        gal = '<div class="gallery" style="margin:28px 0;grid-template-columns:repeat(3,1fr)" data-reveal>' + "".join(f'<button type="button">{pic(i, a, sizes="(max-width: 760px) 33vw, 16vw")}</button>' for i, a in pr["gallery"]) + "</div>" + f'<dialog class="lightbox" data-gallery><button class="lightbox__close" type="button" aria-label="Close">×</button><img src="/assets/img/{pr["gallery"][0][0]}" alt=""><p></p></dialog>'
    elif pr["gallery"]:
        i, a = pr["gallery"][0]
        gal = f'<figure class="media media--wide" style="margin:28px 0" data-mask>{pic(i, a)}</figure>'
    src = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{html.escape(t)}</a></li>' for t, u in pr["sources"])
    guides = [a for a in ARTICLES if a["slug"] in pr["guides"]]
    others = [PROJECTS[(n + k) % len(PROJECTS)] for k in (1, 2, 3)]
    h, how = pr["how"]
    content = head(f"/projects/{pr['slug']}/", pr["seo"], pr["desc"], image=pr["img"],
        extra=crumbs_ld([("Home", "/"), ("Projects", "/projects/"), (pr["name"], f"/projects/{pr['slug']}/")]) + pr_ld
    ) + header("projects") + page_hero(pr["img"], [("Projects", "/projects/"), (pr["name"], None)], pr["name"], pr["sub"]) + f"""
<section class="sec">
  <div class="wrap article">
    <aside class="article__side">
      <div class="panel" data-reveal>
        <h2 style="font-size:1.1rem;margin-bottom:16px">Project facts</h2>
        <dl class="facts">{facts}</dl>
      </div>
      <a class="btn btn--primary" href="/contact/#inquiry" data-magnetic>Plan a similar project {ARROW}</a>
    </aside>
    <article class="prose">
      <span class="solution__no">{pr["tag"]}</span>
      <h2>The project</h2>
      {pr["body"]}
      {vids}{gal}
      <h2>{h}</h2>
      {how}
      <h2>Source</h2>
      <ul class="sources">{src}</ul>
      <p>Related: <a href="/solutions/{pr["div"]}/">{DIVS[pr["div"]]["name"]}</a></p>
    </article>
  </div>
</section>
{'<section class="sec sec--line"><div class="wrap"><div class="head"><h2 data-split>Related guides</h2><a class="link" href="/insights/" data-reveal>All guides ' + ARROW + '</a></div>' + article_cards(guides) + '</div></section>' if guides else ''}
<section class="sec sec--line">
  <div class="wrap">
    <div class="head"><h2 data-split>More projects</h2><a class="link" href="/projects/" data-reveal>All projects {ARROW}</a></div>
    {project_cards(others)}
  </div>
</section>
{cta()}""" + footer()
    page(f"/projects/{pr['slug']}/", f"projects/{pr['slug']}/index.html", content, "0.7")

# ================================================================ FAQ
faq_groups = [
    ("gasifiers", "Biomass gasifiers", [
        ("What can an EnerFab biomass gasifier replace?", "Diesel, furnace oil (HFO) and LPG fired boilers, furnaces, kilns and dryers, and the fuel in internal combustion engines that drive electrical generators."),
        ("Do I need to replace my boiler to switch to biomass?", "No. A biomass gasifier with a dual-fuel burner switches your diesel or furnace-oil boiler to producer gas. You keep operating the same boiler, and your previous fuel stays available as a backup."),
        ("Why use a gasifier instead of a wood-fired boiler?", "EnerFab’s conversion method gives better efficiency, a better response to load variation and lower particulate emissions than a wood-fired boiler."),
        ("Can a gasifier generate electricity?", "Yes. Producer gas can run an internal combustion engine that turns a generator. EnerFab installed a gasifier generator at a wood processing plant that makes 200 kW from waste wood, with a further 400 kW of thermal energy available from the engine’s exhaust and cooling system. EnerFab also builds combined heat and power plants."),
        ("What sizes and efficiencies are EnerFab gasifiers?", "A University of Moratuwa review in Tech Monitor (2007) reported EnerFab gasifiers for electricity from 1 to 250 kWe with about 30% overall efficiency, and thermal gasifiers in Sri Lanka from 100 to 350 kW with claimed efficiencies of 70 to 80%. Each system is sized to your load, so contact us for current figures."),
        ("How long do EnerFab gasifiers last?", "Kandalama Hotel, Tea Factory Hotel, CW Mackie and other establishments have operated EnerFab gasifiers for more than a decade. A rubber processing dryer converted from diesel has operated from 2006 to date."),
        ("Who operates and maintains the plant?", "EnerFab offers management contracts to operate the plants it supplies, and provides spare parts and breakdown maintenance for every installation it has completed. We have provided after-sales service since 2005."),
    ]),
    ("fuelwood", "Fuelwood and biomass supply", [
        ("What fuelwood can be used?", "Gliricidia, Ipil Ipil, cinnamon, timber off-cuts, coconut shells and other approved fuelwood trees. A wood processing plant can run a gasifier on its own waste wood."),
        ("Can EnerFab supply biomass on contract?", "Yes. EnerFab supplies biomass on a contractual basis from its energy plantations and an out-grower network: a collection network of 3,000 farmers and a supplier base of more than 2,000 across Sri Lanka, outside the North and East."),
        ("How much of a power plant’s fuel should it control itself?", "In EnerFab’s view, at least 50%. If outside supply networks fall short, your own supply has to carry the plant until they recover."),
        ("What wood-handling equipment does EnerFab make?", "The EWG 1 wood grab, which grabs 1 m³ of chips at 20% moisture (US$ 10,000), and the DM500 wood chopper, which processes 500 kg of fuelwood an hour (US$ 5,000)."),
    ]),
    ("engineering", "Steel, hydro, cranes and ESCO", [
        ("What steel structures does EnerFab fabricate?", "Steel lattice structures, steel buildings, large advertising structures, steel penstock pipelines, water, diesel and HFO storage tanks and pipelines, small hydro power plants and other civil works, designed to international standards with corrosion protection."),
        ("Which hydro turbines does EnerFab supply?", "EnerFab is the sole agent in Sri Lanka for GUGLER Water Turbines: Kaplan, Pelton and Francis turbines from 5 kW to 10 MW, horizontal or vertical, with design, installation and servicing."),
        ("What crane capacities are available?", "Single girder overhead travelling and suspension cranes to 12.5 tons over 30 m, double girder overhead travelling cranes to 160 tons over 30 m, gantry and semi-gantry cranes to 160 tons over 50 m, jib cranes to 5 tons and light cranes to 2 tons."),
        ("What do EnerFab’s ESCO services include?", "Preliminary and detailed energy audits, other energy studies, and turnkey energy-saving projects with a payback guarantee. EnerFab has completed more than 15 detailed energy audits."),
    ]),
]
faq_ld = ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, _, qs in faq_groups for q, a in qs]})
faqp = head("/faq/", "Biomass Gasifier FAQ Sri Lanka | Technical Questions | EnerFab",
    "Technical answers on biomass gasifiers, furnace oil to biomass boiler conversion, fuelwood supply, GUGLER mini-hydro turbines, cranes and ESCO energy audits in Sri Lanka.",
    extra=crumbs_ld([("Home", "/"), ("FAQ", "/faq/")]) + faq_ld
) + header("faq") + page_hero("producer-gas-flame.jpg", [("FAQ", None)], "Technical questions, answered",
    "What industrial buyers ask us most about gasifiers, fuel supply and our engineering divisions.") + f"""
<section class="sec">
  <div class="wrap" style="display:grid;gap:clamp(64px,9vw,120px)">
{"".join(f'''    <div class="split split--top" id="{gid}">
      <h2 data-split>{gname}</h2>
      <div class="faq" data-reveal>{"".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in qs)}</div>
    </div>
''' for gid, gname, qs in faq_groups)}  </div>
</section>
{cta("Have a question we didn’t answer?", "Send us your details and our engineers will get back to you.")}""" + footer()
page("/faq/", "faq/index.html", faqp, "0.8")

# ================================================================ ABOUT
about = head("/about/", "About EnerFab | Renewable Energy Company Sri Lanka Since 2005",
    "EnerFab (Pvt) Ltd, founded in 2005, is a Sri Lankan renewable energy and engineering company. Our vision of re-greening Sri Lanka, our mission and our milestones.",
    extra=crumbs_ld([("Home", "/"), ("About", "/about/")]) + ld({"@context": "https://schema.org", "@type": "AboutPage", "url": SITE + "/about/", "about": {"@id": ORG_ID}})
) + header("about") + page_hero("gasifier-installation.jpg", [("About", None)], "Re-greening Sri Lanka since 2005",
    "A Sri Lankan engineering company replacing imported fossil fuel with locally grown, renewable biomass.") + f"""
<section class="sec">
  <div class="wrap split">
    <div>
      <span class="label" data-reveal>Who we are</span>
      <h2 data-split>Technology, plus the fuel to run it</h2>
      <p class="lede" data-reveal>EnerFab was founded in 2005 with a vision to provide biomass-based renewable energy solutions to local industry.</p>
      <p data-reveal>Since then, EnerFab has delivered turnkey biomass technology together with biomass from sustainable energy plantations, collected through a network of 3,000 farmers. Our qualified civil and mechanical engineers also deliver steel fabrication, mini-hydro, material handling and energy-efficiency projects.</p>
    </div>
    <figure class="media media--wide" data-mask>{pic("commissioning-250kw-gasifier.jpg", "EnerFab engineers checking a gasifier with a thermal camera", attrs=' data-parallax="5"')}<figcaption>Commissioning a gasifier</figcaption></figure>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap split split--top">
    <div>
      <span class="label" data-reveal>Vision</span>
      <ul class="checks" style="font-size:1.15rem" data-reveal>
        <li>Re-greening Sri Lanka</li>
        <li>Restoring Sri Lanka’s pristine environment</li>
        <li>Revitalising rural employment and prosperity throughout Sri Lanka</li>
        <li>Re-appreciating Sri Lanka’s natural resources</li>
      </ul>
    </div>
    <div>
      <span class="label" data-reveal>Mission</span>
      <ul class="checks" data-reveal>
        <li>To promote growing trees, shrubs, plantations and living organisms as a natural, renewable source of food, fertility and fuel.</li>
        <li>To promote building and installing equipment that processes Sri Lanka’s natural, renewable resources to generate electricity and heat in an environmentally sound way, through solar, hydro, biomass and wind.</li>
        <li>To design, fabricate, install and operate the structures and equipment to achieve this.</li>
      </ul>
    </div>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap split">
    <div data-reveal>{video("P8rSUtO4fnU", "Energy Plantation", "Energy plantation")}</div>
    <div>
      <h2 data-split>The late Founder Chairman</h2>
      <p data-reveal>EnerFab’s late Founder Chairman championed energy plantations as the way to re-green Sri Lanka. His film on the Energy Plantation, above, still sums up why EnerFab exists.</p>
    </div>
  </div>
</section>

<section class="sec sec--line" id="milestones">
  <div class="wrap split split--top">
    <div>
      <h2 data-split>Milestones</h2>
      <p class="lede" data-reveal>EnerFab-installed gasifiers have operated for over a decade in several Sri Lankan industries.</p>
    </div>
    <ol class="timeline"><span class="timeline__fill"></span>
      <li data-reveal><span class="timeline__year">2005</span><h3>EnerFab founded</h3><p>Set up to bring biomass renewable energy to local industry.</p></li>
      <li data-reveal><span class="timeline__year">2006</span><h3>Diesel dryer converted</h3><p>A rubber processing dryer moved from a diesel burner to producer gas, and has operated from 2006 to date.</p></li>
      <li data-reveal><span class="timeline__year">2007</span><h3>Named the leading gasifier maker</h3><p>A University of Moratuwa review in Tech Monitor named EnerFab the leading designer and manufacturer of gasifiers in Sri Lanka.</p></li>
      <li data-reveal><span class="timeline__year">2008</span><h3>Nawagaththegama plantation</h3><p>40,000 fuelwood plants planted on former scrubland in the Puttalam district.</p></li>
      <li data-reveal><span class="timeline__year">2009</span><h3>GUGLER hydro installation</h3><p>EnerFab installed GUGLER turbines and provided technical support at an Aitken Spence Power mini-hydro site.</p></li>
      <li data-reveal><span class="timeline__year">2017</span><h3>200 kW electrical system</h3><p>A gasifier generator running on waste wood proved producer gas can run an internal combustion engine.</p></li>
      <li data-reveal><span class="timeline__year">2018</span><h3>Poultry farm, Puttalam</h3><p>EnerFab undertook a gasification plant to replace LPG at a poultry farm.</p></li>
    </ol>
  </div>
</section>
{cta()}""" + footer()
page("/about/", "about/index.html", about, "0.8")

# ================================================================ VIDEOS
vids = [
    ("tKnqCnPaES8", "EnerFab WBG 10", "Gasifier", "An EnerFab WBG 10 biomass gasifier in operation."),
    ("glipBEVnmcc", "EnerFab – Sri Lanka", "Company", "An introduction to EnerFab Green Engineering."),
    ("Az4ZQNXVZ7U", "Replacing 50 litres per hour of diesel", "Thermal", "A rubber processing dryer switched from a diesel burner to an EnerFab gasifier in 2006, running to date."),
    ("088d9Otk_18", "Biomass gasifier generator set", "Electrical", "Producer gas runs an engine and generator, making 200 kW from a wood processing plant’s waste wood."),
    ("334j_wDnESI", "200 kW gasifier generator", "Electrical", "EnerFab’s 200 kW gasifier generator."),
    ("P8rSUtO4fnU", "Energy Plantation", "Plantation", "The energy plantation vision of EnerFab’s late Founder Chairman."),
]
vp = head("/videos/", "Biomass Gasifier Videos | EnerFab Sri Lanka",
    "Watch EnerFab biomass gasifiers at work in Sri Lanka: the WBG 10, a 200 kW gasifier generator, a dryer taken off 50 litres an hour of diesel, and our energy plantation.",
    extra=crumbs_ld([("Home", "/"), ("Videos", "/videos/")])
) + header() + page_hero("commissioning-250kw-gasifier.jpg", [("Videos", None)], "See the plants running",
    "Gasifiers, generators and plantations, filmed in Sri Lankan industry.") + f"""
<section class="sec">
  <div class="wrap grid-2" style="gap:72px 32px">
{"".join(f'''    <article class="vcard" data-reveal>{video(y, t)}<h2>{t}</h2><p><span style="color:var(--ember)">{tag}.</span> {d}</p></article>
''' for y, t, tag, d in vids)}  </div>
  <div class="wrap"><p class="muted" style="margin-top:64px">More on the <a href="https://www.youtube.com/channel/UCOWz3FGpK5kuBd6PYCL0LBg" target="_blank" rel="noopener">EnerFab YouTube channel</a>.</p></div>
</section>
{cta()}""" + footer()
page("/videos/", "videos/index.html", vp, "0.6")

# ================================================================ RECOGNITION
rp = head("/recognition/", "Recognition & Press | EnerFab Biomass Gasifiers Sri Lanka",
    "Independent recognition for EnerFab: the University of Moratuwa’s Tech Monitor review naming EnerFab Sri Lanka’s leading gasifier maker, the Sunday Times, Daily News and UNDP.",
    extra=crumbs_ld([("Home", "/"), ("Recognition", "/recognition/")])
) + header() + page_hero("tea-factory-hotel.jpg", [("Recognition", None)], "Recognised by industry, academia and the press",
    "Independent reports and articles on EnerFab’s work in biomass gasification.") + f"""
<section class="sec">
  <div class="wrap">
    <figure class="quote">
      <blockquote data-split>“In Sri Lanka, two companies are involved in the design and manufacture of gasifiers. The leading company is EnerFab (Pvt) Ltd., which produces gasifiers for both thermal and electricity generation applications.”</blockquote>
      <p class="measure muted" data-reveal>The review reported EnerFab gasifiers for electricity from 1 to 250 kWe with overall efficiency of about 30%, and thermal gasifiers in Sri Lanka from 100 to 350 kW with claimed efficiencies of 70 to 80%.</p>
      <figcaption data-reveal style="margin-top:28px">{pic("dr-sugathapala.jpg", "")}<div><b>Dr. A.G.T. Sugathapala</b><span>Head, Department of Mechanical Engineering, Faculty of Engineering, University of Moratuwa. Tech Monitor, July–August 2007</span></div></figcaption>
    </figure>
    <p style="margin-top:36px" data-reveal><a class="btn btn--ghost" href="/assets/docs/tech-monitor-2007-biomass-gasification.pdf" target="_blank" rel="noopener">Read the Tech Monitor article (PDF)</a></p>
  </div>
</section>
<section class="sec sec--line">
  <div class="wrap">
    <div class="head"><h2 data-split>Press and reports</h2></div>
    <div class="press" data-reveal>
      <button type="button" class="press__item" data-open="clip"><div class="press__logo">{pic("logo-sunday-times.jpg", "The Sunday Times")}</div><h3>The Sunday Times</h3><p>Article by journalist Quintus Perera on biomass power as an answer to costly fossil fuels.</p><span class="link">View the clipping</span></button>
      <a class="press__item" href="http://archives.dailynews.lk/2007/11/05/bus10.asp" target="_blank" rel="noopener"><div class="press__logo">{pic("tea-factory-hotel.jpg", "Tea Factory Hotel")}</div><h3>Daily News: Tea Factory Hotel</h3><p>The Tea Factory Hotel’s EnerFab biomass gasifier, November 2007.</p><span class="link">Read the article</span></a>
      <a class="press__item" href="/assets/docs/tech-monitor-2007-biomass-gasification.pdf" target="_blank" rel="noopener"><div class="press__logo">{pic("dr-sugathapala.jpg", "")}</div><h3>Tech Monitor review</h3><p>Biomass gasification in Sri Lanka, by Dr. A.G.T. Sugathapala, July–August 2007.</p><span class="link">Read the PDF</span></a>
      <a class="press__item" href="https://www.ctc-n.org/technologies/biomass-heating" target="_blank" rel="noopener"><div class="press__logo"><img src="/assets/img/logo-ctcn.png" alt="UN Climate Technology Centre and Network" width="240" height="240" loading="lazy"></div><h3>UN Climate Technology Centre and Network</h3><p>The UNFCCC technology centre’s reference on biomass heating.</p><span class="link">Visit CTCN</span></a>
      <a class="press__item" href="https://www.eartheval.org/sites/ceval/files/evaluations/363%20Biomass%20Energy%20Development%20Project.pdf" target="_blank" rel="noopener"><div class="press__logo"><img src="/assets/img/logo-gov-sri-lanka.png" alt="Government of Sri Lanka" width="240" height="238" loading="lazy"></div><h3>Government of Sri Lanka and UNDP</h3><p>Biomass Energy Development Project: report of the final evaluation, January 2006.</p><span class="link">Read the report</span></a>
      <a class="press__item" href="/videos/"><div class="press__logo"><img src="/assets/img/enerfab-mark.png" alt="" width="256" height="273" loading="lazy"></div><h3>EnerFab videos</h3><p>Our gasifiers, plantation and installations at work.</p><span class="link">Watch the videos</span></a>
    </div>
  </div>
</section>
<dialog class="lightbox" id="clip"><button class="lightbox__close" type="button" aria-label="Close">×</button>{pic("press-clipping.jpg", "Sunday Times article: biomass power, answer to costly fossil fuels")}<p>The Sunday Times: biomass power as an answer to costly fossil fuels</p></dialog>
{cta()}""" + footer()
page("/recognition/", "recognition/index.html", rp, "0.6")

# ================================================================ CONTACT
interests = [d["name"] for d in DIV] + ["Wood Grab EWG 1", "Wood Chopper DM500", "Something else"]
cp = head("/contact/", "Contact EnerFab | Biomass Gasifier Quotes Sri Lanka",
    f"Request a quote for a biomass gasifier, fuelwood supply, mini-hydro, steel fabrication, cranes or an energy audit. Call {PHONE} or email {EMAIL}. Kotte, Sri Lanka.",
    extra=crumbs_ld([("Home", "/"), ("Contact", "/contact/")]) + ld({"@context": "https://schema.org", "@type": "ContactPage", "url": SITE + "/contact/", "about": {"@id": ORG_ID}})
    + '\n<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>'
) + header("contact") + page_hero("gliricidia-leaves.jpg", [("Contact", None)], "Let’s talk about your energy",
    "Fill out the form and we will be in touch to discuss your requirements.") + f"""
<section class="sec">
  <div class="wrap contact-grid">
    <div>
      <h2 data-split>Head office</h2>
      <ul class="contact-list" data-reveal>
        <li><b>Address</b><span>No. 115/3, Rampart Road,<br>Sri Jayawardenepura Kotte, Sri Lanka</span></li>
        <li><b>Phone</b><span><a href="tel:{TEL}">Sri Lanka: {PHONE}</a><br><a href="tel:{TEL_CA}">Canada: {PHONE_CA}</a></span></li>
        <li><b>Email</b><span><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="mailto:{EMAIL_OLD}">{EMAIL_OLD}</a></span></li>
        <li><b>Hours</b><span>Monday to Friday, 9am to 4pm</span></li>
      </ul>
      <div class="map" data-reveal>
        <iframe title="EnerFab head office on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
          src="https://maps.google.com/maps?q=115%2F3%20Rampart%20Road%2C%20Sri%20Jayawardenepura%20Kotte%2C%20Sri%20Lanka&amp;z=15&amp;output=embed"></iframe>
      </div>
    </div>
    <form class="form js-inquiry" id="inquiry" action="/api/inquiry" method="post" novalidate data-reveal>
      <h2>Make an inquiry today</h2>
      <p class="muted">Tell us what your plant runs on now and what you need. Fields marked * are required.</p>
      <div style="position:absolute;left:-9999px" aria-hidden="true"><label for="f-web">Leave empty</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
      <div class="form__row">
        <div class="field"><label for="f-name">Name *</label><input id="f-name" name="name" autocomplete="name" required minlength="2" maxlength="100"></div>
        <div class="field"><label for="f-company">Company</label><input id="f-company" name="company" autocomplete="organization" maxlength="150"></div>
      </div>
      <div class="form__row">
        <div class="field"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="254"></div>
        <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" maxlength="40" pattern="[0-9+()\\-\\s.]*"></div>
      </div>
      <div class="field"><label for="f-interest">I’m interested in</label>
        <select id="f-interest" name="interest"><option value="">Choose a solution</option>{"".join(f"<option>{html.escape(i)}</option>" for i in interests)}</select>
      </div>
      <div class="field"><label for="f-msg">Message *</label><textarea id="f-msg" name="message" required minlength="10" maxlength="3000" placeholder="For example: what fuel your boiler, dryer or generator uses now, and roughly how much."></textarea></div>
      <div class="cf-turnstile" data-sitekey="{TURNSTILE_SITE_KEY}" data-action="inquiry" data-theme="dark" style="margin-bottom:18px"></div>
      <button class="btn btn--primary" type="submit">Send inquiry {ARROW}</button>
      <p class="form__note">Or email <a href="mailto:{EMAIL}">{EMAIL}</a>. Your details are used only to answer your inquiry.</p>
      <div class="form__status" role="status" aria-live="polite"></div>
    </form>
  </div>
</section>
""" + footer()
page("/contact/", "contact/index.html", cp, "0.8")

# ================================================================ INSIGHTS (knowledge hub)
ins = head("/insights/", "Energy Insights Sri Lanka | Biomass, Gasification, CHP | EnerFab",
    "Practical guides on biomass gasification, furnace oil to biomass conversion, Gliricidia fuelwood, biomass CHP, factory energy audits and mini-hydro turbines in Sri Lanka.",
    extra=crumbs_ld([("Home", "/"), ("Insights", "/insights/")]) + ld({"@context": "https://schema.org", "@type": "CollectionPage", "url": SITE + "/insights/",
        "name": "EnerFab energy insights", "publisher": {"@id": ORG_ID},
        "hasPart": [{"@type": "Article", "headline": a["title"], "url": f"{SITE}/insights/{a['slug']}/"} for a in ARTICLES]})
) + header("insights") + page_hero("gliricidia-leaves.jpg", [("Insights", None)], "Energy insights for Sri Lankan industry",
    "Practical engineering guides on biomass, gasification, combined heat and power, energy efficiency and small hydro.") + f"""
<section class="sec">
  <div class="wrap">
    {article_cards(ARTICLES)}
  </div>
</section>
{cta("Have an energy question?", "Tell us about your plant and EnerFab’s engineers will be in touch.")}""" + footer()
page("/insights/", "insights/index.html", ins, "0.8")

for a in ARTICLES:
    url = f"{SITE}/insights/{a['slug']}/"
    art_ld = ld({"@context": "https://schema.org", "@type": "Article", "@id": url + "#article", "headline": a["title"], "description": a["desc"],
        "image": f"{SITE}/assets/img/{a['img']}", "datePublished": a["date"], "dateModified": a.get("modified", a["date"]),
        "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "mainEntityOfPage": url, "inLanguage": "en-LK",
        "about": [{"@id": f"{SITE}/solutions/{s}/#service"} for s in a["divs"]]})
    src = "".join(f'<li><a href="{u}"{"" if u.startswith("/") else " rel=\"noopener\" target=\"_blank\""}>{html.escape(n)}</a></li>' for n, u in a["sources"])
    others = [o for o in ARTICLES if o["slug"] != a["slug"]][:3]
    content = head(f"/insights/{a['slug']}/", a["seo"], a["desc"], image="og-image.jpg",
        extra=crumbs_ld([("Home", "/"), ("Insights", "/insights/"), (a["title"], f"/insights/{a['slug']}/")]) + art_ld
    ) + header("insights") + page_hero(a["img"], [("Insights", "/insights/"), (a["title"], None)], a["title"], a["desc"]) + f"""
<section class="sec">
  <div class="wrap article">
    <aside class="article__side">
      <p class="article__meta">EnerFab engineering<br>{nice_date(a["date"])}<br>{reading_time(a)} min read</p>
      <div class="panel takeaways" data-reveal>
        <h2>Key points</h2>
        <ul class="checks">{"".join(f"<li>{t}</li>" for t in a["takeaways"])}</ul>
      </div>
    </aside>
    <article class="prose">
      {a["body"]}
      <h2>Sources</h2>
      <ul class="sources">{src}</ul>
      <p class="muted note">General engineering guidance. Every plant is different: ask EnerFab’s engineers before you design or buy.</p>
      <p>Related: {" · ".join(f'<a href="/solutions/{s}/">{DIVS[s]["name"]}</a>' for s in a["divs"])}</p>
    </article>
  </div>
</section>
<section class="sec sec--line">
  <div class="wrap">
    <div class="head"><h2 data-split>More energy guides</h2><a class="link" href="/insights/" data-reveal>All guides {ARROW}</a></div>
    {article_cards(others)}
  </div>
</section>
{cta()}""" + footer()
    page(f"/insights/{a['slug']}/", f"insights/{a['slug']}/index.html", content, "0.7")

# ================================================================ 404
nf = head("/404.html", "Page not found | EnerFab", "This page could not be found. Explore EnerFab biomass gasifiers and engineering solutions.", noindex=True
) + header() + page_hero("plantation-hills.jpg", [("Page not found", None)], "This page could not be found",
    "The link may be old or mistyped. These pages should help.") + f"""
<section class="sec"><div class="wrap">{related(["biomass-gasifiers", "fuelwood-biomass-supply", "esco-energy-solutions"])}
<p style="margin-top:40px"><a class="btn btn--primary" href="/">Go to the home page</a></p></div></section>
""" + footer()
write("404.html", nf)

# ================================================================ sitemap, robots, manifest, headers, redirects
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join(f"  <url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in PAGES) + "</urlset>\n")
write("robots.txt", f"""User-agent: *
Allow: /
Disallow: /api/

Sitemap: {SITE}/sitemap.xml
""")
write("site.webmanifest", json.dumps({"name": "EnerFab Green Engineering", "short_name": "EnerFab", "start_url": "/", "display": "standalone",
      "background_color": "#0c1510", "theme_color": "#0c1510", "icons": [{"src": "/assets/img/enerfab-mark.png", "sizes": "256x256", "type": "image/png"}]}, indent=2) + "\n")

CSP = "; ".join([
    "default-src 'self'",
    f"script-src 'self' {sha(MOTION_JS)} {sha(IMPORTMAP)} https://challenges.cloudflare.com https://static.cloudflareinsights.com",
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src 'self' https://fonts.gstatic.com",
    "img-src 'self' data: blob: https://i.ytimg.com",
    "frame-src https://www.youtube-nocookie.com https://www.google.com https://maps.google.com https://challenges.cloudflare.com",
    "connect-src 'self' https://challenges.cloudflare.com https://cloudflareinsights.com",
    "worker-src 'self' blob:",
    "manifest-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    "upgrade-insecure-requests",
])
write("_headers", f"""# Cloudflare response headers for static assets. Generated by tools/build.py; edit there.
/*
  Content-Security-Policy: {CSP}
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), magnetometer=(), gyroscope=(), accelerometer=(), browsing-topics=(), fullscreen=(self "https://www.youtube-nocookie.com")
  Cross-Origin-Opener-Policy: same-origin
  X-Permitted-Cross-Domain-Policies: none

/js/vendor/*
  Cache-Control: public, max-age=31536000, immutable
/css/*
  Cache-Control: public, max-age=31536000, immutable
/js/*
  Cache-Control: public, max-age=31536000, immutable
/assets/img/*
  Cache-Control: public, max-age=2592000, stale-while-revalidate=86400
/assets/docs/*
  Cache-Control: public, max-age=2592000
/*.html
  Cache-Control: public, max-age=0, must-revalidate
/api/*
  Cache-Control: no-store
""")
write("_redirects", """# Old flat URLs from earlier builds -> clean silo URLs
/index.html            /                   301
/about.html            /about/             301
/solutions.html        /solutions/         301
/videos.html           /videos/            301
/testimonials.html     /recognition/       301
/contact.html          /contact/           301
/page1.html            /about/             301
/page2.html            /solutions/         301
""")
print(f"built {len(PAGES)} pages")
