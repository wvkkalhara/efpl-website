# EnerFab: enerfab.lk security and SEO blueprint

Everything here is already built into this project unless it says **You do this**. Code blocks are copied from the generated files, so they match what you deploy.

**Hosting choice:** a Cloudflare Worker with static assets, deployed from GitHub. Cloudflare serves the site in `public/` from its network, applies `public/_headers` and `public/_redirects`, and runs the secure inquiry form handler (`src/worker.js` and `src/inquiry.js`). The settings are in `wrangler.jsonc`. All of the Cloudflare settings below assume this.

**Content rule:** every company fact on enerfab.lk comes from efpl.org, or from the Tech Monitor 2007 review that efpl.org links to (always credited). Nothing is invented: no savings figures, coordinates or client claims that EnerFab hasn't published. Section 1 explains how to add more detail using EnerFab's own project data.

---

## 1. Anti-duplicate content and outranking architecture

### URL structure

efpl.org is a flat Mobirise export: `/`, `/page1.html`, `/page2.html` (all six divisions on one page), `/testimonials.html`. enerfab.lk gives each search topic its own page:

```
https://enerfab.lk/
├── /about/
├── /solutions/                              hub page linking all six
│   ├── /solutions/biomass-gasifiers/        "biomass gasifiers Sri Lanka", "furnace oil to biomass boiler conversion"
│   ├── /solutions/fuelwood-biomass-supply/  "sustainable biomass fuel suppliers Sri Lanka"
│   ├── /solutions/steel-fabrication/        "industrial steel fabrication Sri Lanka"
│   ├── /solutions/mini-hydro-power-plants/  "mini hydro power plants Sri Lanka"
│   ├── /solutions/material-handling/        cranes, hoists, suspended access
│   └── /solutions/esco-energy-solutions/    "ESCO energy solutions Sri Lanka"
├── /projects/                               9 real projects (case studies)
├── /faq/                                    15 technical Q&As (FAQPage schema)
├── /insights/                               energy knowledge hub (6 in-depth guides, Article schema)
│   ├── /insights/how-biomass-gasification-works/
│   ├── /insights/furnace-oil-to-biomass-boiler-conversion/
│   ├── /insights/gliricidia-fuelwood-sri-lanka/
│   ├── /insights/biomass-chp-gasifier-generator/
│   ├── /insights/industrial-energy-audit-sri-lanka/
│   └── /insights/mini-hydro-turbine-selection/
├── /videos/
├── /recognition/
└── /contact/                                secure inquiry form
```

Each division page links up to `/solutions/`, across to three related divisions, and to `/projects/` and `/faq/`. This internal linking tells Google which page answers which search.

### Why Google will treat enerfab.lk as the original, more useful site

| | efpl.org | enerfab.lk |
|---|---|---|
| Pages about the six divisions | 1 combined page | 6 dedicated pages + hub |
| Copy | original Mobirise text | fully rewritten wording, plus sections efpl.org doesn't have |
| Case studies | scattered sentences | `/projects/`: 9 structured projects |
| Technical FAQ | none | `/faq/`: 15 answers, FAQPage schema |
| Knowledge content | none | `/insights/`: 6 sourced engineering guides that link to the division pages |
| Comparison data | none | gasifier conversion vs wood-fired boiler table; Tech Monitor capacity/efficiency/cost table (credited) |
| Interactive | none | 3D gasifier plant tour and viewer |
| Structured data | none | Organization, LocalBusiness, Service ×6, FAQPage, Product ×2, BreadcrumbList |
| Speed / mobile | heavy Mobirise template, autoplaying YouTube iframes | static, WebP images, YouTube loads only on tap |

**You do this. Over the next 3 months, add EnerFab's own data, which only EnerFab has:**
1. For each project on `/projects/`, collect the real numbers: fuel used before and after, fuel cost, payback period, operating hours, kW. Add them to `tools/build.py` (the `projects` list) and rebuild. Never estimate. Use only measured or invoiced figures, with the client's permission.
2. Add new projects completed since 2018. These are the strongest content you can publish.
3. Add one technical article a month to the knowledge hub (see section 7). Each article is an entry in `tools/articles.py`: copy an existing one, write the text, list its sources, then run `python tools/build.py`. The page, Article schema, sitemap entry and links from the home page and division pages are all generated automatically.
5. **Topical authority.** Broad searches such as "energy" are dominated by government bodies and the electricity board; no company site ranks first for them. The hub targets the searches buyers actually make around EnerFab's work (biomass, gasification, producer gas, furnace-oil replacement, fuelwood, CHP, energy audits, mini-hydro). Each new guide that answers a real question widens the set of energy searches where enerfab.lk can appear. Good next topics: boiler efficiency basics, steam system losses, coconut shell and rice husk as fuels, LPG-to-biomass for dryers, biomass fuel storage and drying, and the costs of running a gasifier.
4. Ask an EnerFab engineer to review each page and add a named byline. Expert authorship is an important quality signal.

### Optional canonical tags on efpl.org

efpl.org stays live. If you can edit it, add **one line** to the `<head>` of each efpl.org page. This tells Google that enerfab.lk is the main copy, without taking efpl.org down:

```html
<!-- efpl.org/index.html -->
<link rel="canonical" href="https://enerfab.lk/">
<!-- efpl.org/page1.html (About) -->
<link rel="canonical" href="https://enerfab.lk/about/">
<!-- efpl.org/page2.html (Our Solutions) -->
<link rel="canonical" href="https://enerfab.lk/solutions/">
<!-- efpl.org/testimonials.html -->
<link rel="canonical" href="https://enerfab.lk/recognition/">
```

Also add a visible link on efpl.org's home page: "Visit our new website: enerfab.lk". A canonical tag is a hint that Google usually follows; a 301 redirect is the only signal that's guaranteed. If EnerFab later agrees to redirects, that is the strongest move.

---

## 2. Website security (Cloudflare, DNS, headers)

### Domain and DNS (You do this)
1. Add `enerfab.lk` to Cloudflare (free plan is enough to start). At your .lk registrar, change the nameservers to the two Cloudflare gives you.
2. In Cloudflare, go to Workers & Pages and connect this GitHub repository to your Worker. The deploy command is `npx wrangler deploy` and the build command can be empty, because the generated pages are committed. The `name` in `wrangler.jsonc` must match the Worker's name in the dashboard.
3. Worker → Settings → Domains & Routes → add the custom domains `enerfab.lk` and `www.enerfab.lk`.
4. Rules → Redirect Rules → new rule: *When* hostname equals `www.enerfab.lk` → *Then* dynamic redirect, expression `concat("https://enerfab.lk", http.request.uri.path)`, status 301, preserve query string.

### SSL/TLS (You do this)
- SSL/TLS → Overview: **Full (strict)**.
- Edge Certificates: **Always Use HTTPS** on, **Automatic HTTPS Rewrites** on, **Minimum TLS 1.2**, **TLS 1.3** on.
- **HSTS**: enable with max-age 12 months, include subdomains, preload, No-Sniff on. The same header is also sent by `_headers`. Only submit to hstspreload.org once every subdomain serves HTTPS.
- **DNSSEC**: DNS → Settings → Enable DNSSEC, then give the DS record to your .lk registrar. If the registrar can't add DS records, DNSSEC can't be completed; ask them.

### Bot and WAF protection (You do this)
- Security → Bots: **Bot Fight Mode** on.
- Security → WAF → Custom rules (free plan allows 5):

| Name | Expression | Action |
|---|---|---|
| Block exploit probes | `(http.request.uri.path contains "/wp-") or (http.request.uri.path contains ".php") or (http.request.uri.path contains "/.env") or (http.request.uri.path contains "/.git") or (http.request.uri.path contains "xmlrpc")` | Block |
| Form: POST only | `(http.request.uri.path eq "/api/inquiry" and http.request.method ne "POST")` | Block |
| Form: no empty user agent | `(http.request.uri.path eq "/api/inquiry" and http.user_agent eq "")` | Block |
| Block verified bots on form | `(http.request.uri.path eq "/api/inquiry" and cf.client.bot)` | Block |

- Security → WAF → **Rate limiting rules**: `http.request.uri.path eq "/api/inquiry"`, counting by IP, **3 requests per 10 seconds**, block for 10 seconds (the free plan limits). On Pro or higher, use 5 requests per 10 minutes and block for 1 hour.

### Security headers (built: `_headers`)

```
# Cloudflare response headers for static assets. Generated by tools/build.py; edit there.
/*
  Content-Security-Policy: default-src 'self'; script-src 'self' 'sha256-l0L9jdI9fLIosAZRIlqyAAUyAB3+rVzexFWNylXmTro=' 'sha256-viECVWUirw2hTN0FSySe+tXFU0yE0Dv1CMbpIXVrc68=' https://challenges.cloudflare.com https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob: https://i.ytimg.com; frame-src https://www.youtube-nocookie.com https://www.google.com https://maps.google.com https://challenges.cloudflare.com; connect-src 'self' https://challenges.cloudflare.com https://cloudflareinsights.com; worker-src 'self' blob:; manifest-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests
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
```

The CSP allows scripts only from enerfab.lk itself, Cloudflare Turnstile and Cloudflare Web Analytics. The two small inline scripts (the motion switch and the 3D import map) are allowed by SHA-256 hash, which `tools/build.py` recomputes on every build. YouTube is allowed only as the privacy-friendly `youtube-nocookie.com` player, which loads after a visitor taps play. Google Maps and Google Fonts are allowed. All animation and 3D libraries are self-hosted in `/js/vendor/`, so no third-party script CDN is needed.

Test after launch: securityheaders.com and the Mozilla Observatory (developer.mozilla.org/en-US/observatory). Both should report A or A+.

---

## 3. Inquiry form security (built)

Flow: browser → Cloudflare WAF and rate limit → `POST /api/inquiry` (`src/worker.js` → `src/inquiry.js`) → Turnstile check → email to info@enerfab.lk.

| Protection | How |
|---|---|
| Spam bots | Cloudflare Turnstile widget (`data-action="inquiry"`), verified on the server with the hostname and action checked; honeypot field `website` |
| CSRF | The site has no cookies or sessions, so a forged cross-site post has no credentials to abuse. The function also rejects any `Origin` other than enerfab.lk and any `Sec-Fetch-Site` other than `same-origin`, and every submission needs a fresh, single-use Turnstile token |
| Flooding | WAF rate-limiting rule (section 2), 16 KB body limit |
| Bad input | Server-side validation of every field (length, characters, valid email, interest from a fixed list, at most 2 links), control characters stripped |
| Email injection / XSS in email | Newlines stripped from the subject; HTML email body escaped |
| Info leaks | Generic error messages; honeypot hits get a fake success |

**You do this before launch:**
1. Cloudflare → Turnstile → Add site → domain `enerfab.lk`, mode *Managed*. Copy the **site key** into `TURNSTILE_SITE_KEY` at the top of `tools/build.py` and rebuild. The default in the file is Cloudflare's public test key, which always passes and gives no protection.
2. Create a free account at resend.com, add the domain `enerfab.lk`, and add the SPF and DKIM DNS records it shows you in Cloudflare DNS.
3. Worker → Settings → Variables and secrets. `MAIL_FROM` and `MAIL_TO` are already set in `wrangler.jsonc`, so only add the two secrets:
   - `TURNSTILE_SECRET_KEY` (secret): from Turnstile
   - `RESEND_API_KEY` (secret): from Resend
   - `MAIL_FROM`: `EnerFab Website <website@enerfab.lk>`
   - `MAIL_TO`: `info@enerfab.lk`
4. Add a DMARC record for enerfab.lk email: TXT `_dmarc` → `v=DMARC1; p=quarantine; rua=mailto:info@enerfab.lk`.
5. Send a test inquiry from the live site and confirm it arrives.

---

## 4. Technical SEO, .lk signals and indexing

### robots.txt (built)
```
User-agent: *
Allow: /
Disallow: /api/

Sitemap: https://enerfab.lk/sitemap.xml
```

### sitemap.xml (built, regenerated with today's date on every build)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://enerfab.lk/</loc><lastmod>2026-11-14</lastmod><priority>1.0</priority></url>
  <url><loc>https://enerfab.lk/solutions/</loc><lastmod>2026-11-14</lastmod><priority>0.9</priority></url>
  <url><loc>https://enerfab.lk/solutions/biomass-gasifiers/</loc><lastmod>2026-11-14</lastmod><priority>0.9</priority></url>
  <url><loc>https://enerfab.lk/solutions/fuelwood-biomass-supply/</loc><lastmod>2026-11-14</lastmod><priority>0.9</priority></url>
  <url><loc>https://enerfab.lk/solutions/steel-fabrication/</loc><lastmod>2026-11-14</lastmod><priority>0.9</priority></url>
  <url><loc>https://enerfab.lk/solutions/mini-hydro-power-plants/</loc><lastmod>2026-11-14</lastmod><priority>0.9</priority></url>
  <url><loc>https://enerfab.lk/solutions/material-handling/</loc><lastmod>2026-11-14</lastmod><priority>0.9</priority></url>
  <url><loc>https://enerfab.lk/solutions/esco-energy-solutions/</loc><lastmod>2026-11-14</lastmod><priority>0.9</priority></url>
  <url><loc>https://enerfab.lk/projects/</loc><lastmod>2026-11-14</lastmod><priority>0.8</priority></url>
  <url><loc>https://enerfab.lk/faq/</loc><lastmod>2026-11-14</lastmod><priority>0.8</priority></url>
  <url><loc>https://enerfab.lk/about/</loc><lastmod>2026-11-14</lastmod><priority>0.8</priority></url>
  <url><loc>https://enerfab.lk/videos/</loc><lastmod>2026-11-14</lastmod><priority>0.6</priority></url>
  <url><loc>https://enerfab.lk/recognition/</loc><lastmod>2026-11-14</lastmod><priority>0.6</priority></url>
  <url><loc>https://enerfab.lk/contact/</loc><lastmod>2026-11-14</lastmod><priority>0.8</priority></url>
</urlset>
```

### Launch steps (You do this, in this order)
1. **Google Search Console** → Add property → *Domain* → `enerfab.lk` → verify with the DNS TXT record in Cloudflare. A `.lk` domain is already geotargeted to Sri Lanka; there's no setting to change.
2. Sitemaps → submit `https://enerfab.lk/sitemap.xml`.
3. URL Inspection → *Request indexing* for `/`, `/solutions/biomass-gasifiers/`, `/solutions/fuelwood-biomass-supply/`, `/projects/` and `/faq/`.
4. **Bing Webmaster Tools** → Import from Google Search Console. Bing also powers ChatGPT search and Copilot answers.
5. Cloudflare → Caching → Configuration → **Crawler Hints** on. This tells Bing and other IndexNow engines about changes automatically.
6. **Google Business Profile** (Kotte head office): set *Website* to `https://enerfab.lk/`, add `info@enerfab.lk`, keep the name, address and phone exactly as on the site (*EnerFab (Pvt) Ltd, No. 115/3, Rampart Road, Sri Jayawardenepura Kotte, +94 11 288 8821*). Primary category: *Energy equipment and solutions*. Secondary: *Industrial equipment supplier*, *Engineering consultant*, *Steel fabricator*. Upload 20+ real project photos, and post monthly.
7. Ask past clients (hotels, factories) for Google reviews and reply to every one.
8. Update the website link on every profile to enerfab.lk: Facebook, X, Instagram, YouTube channel *About*, LinkedIn.

---

## 5. On-page SEO: head templates and heading outlines (built)

### Home page `<head>`
```html
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Biomass Gasifiers Sri Lanka | Furnace Oil to Biomass | EnerFab</title>
<meta name="description" content="EnerFab builds biomass gasifiers in Sri Lanka that replace diesel, furnace oil and LPG in boilers, dryers and generators, and supplies the fuelwood. Since 2005.">
<link rel="canonical" href="https://enerfab.lk/">
<link rel="alternate" hreflang="en-LK" href="https://enerfab.lk/">
<link rel="alternate" hreflang="x-default" href="https://enerfab.lk/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="author" content="EnerFab (Pvt) Ltd">
<meta property="og:site_name" content="EnerFab">
<meta property="og:locale" content="en_LK">
<meta property="og:type" content="website">
<meta property="og:title" content="Biomass Gasifiers Sri Lanka | Furnace Oil to Biomass | EnerFab">
<meta property="og:description" content="EnerFab builds biomass gasifiers in Sri Lanka that replace diesel, furnace oil and LPG in boilers, dryers and generators, and supplies the fuelwood. Since 2005.">
<meta property="og:url" content="https://enerfab.lk/">
<meta property="og:image" content="https://enerfab.lk/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="EnerFab engineers commissioning a biomass gasifier">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@enerfabsl">
<meta name="twitter:title" content="Biomass Gasifiers Sri Lanka | Furnace Oil to Biomass | EnerFab">
<meta name="twitter:description" content="EnerFab builds biomass gasifiers in Sri Lanka that replace diesel, furnace oil and LPG in boilers, dryers and generators, and supplies the fuelwood. Since 2005.">
<meta name="twitter:image" content="https://enerfab.lk/assets/img/og-image.jpg">
<meta name="theme-color" content="#0c1510">
<meta name="format-detection" content="telephone=no">
<meta name="geo.region" content="LK-11">
<meta name="geo.placename" content="Sri Jayawardenepura Kotte">
<link rel="icon" type="image/png" href="/assets/img/enerfab-mark.png">
<link rel="apple-touch-icon" href="/assets/img/enerfab-mark.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/css/style.css?v=335834a4">
<script>if(!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('motion');setTimeout(function(){if(!window.gsap)document.documentElement.classList.remove('motion')},4000)</script>
<script type="importmap">{"imports":{"three":"/js/vendor/three.module.min.js","three/addons/":"/js/vendor/three-addons/"}}</script>
<link rel="modulepreload" href="/js/vendor/three.module.min.js">
<script src="/js/vendor/gsap.min.js" defer></script>
<script src="/js/vendor/ScrollTrigger.min.js" defer></script>
<script src="/js/vendor/SplitText.min.js" defer></script>
<script src="/js/vendor/lenis.min.js" defer></script>
<script src="/js/main.js?v=e95d237c" defer></script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":["Organization","LocalBusiness"],"@id":"https://enerfab.lk/#org","name":"EnerFab (Pvt) Ltd","alternateName":["EnerFab","EnerFab Green Engineering","EFPL"],"url":"https://enerfab.lk/","logo":"https://enerfab.lk/assets/img/enerfab-mark.png","image":"https://enerfab.lk/assets/img/og-image.jpg","description":"Sri Lankan renewable energy and engineering company, founded in 2005: biomass gasifiers and CHP, fuelwood supply, steel fabrication, mini-hydro, material handling and ESCO energy services.","foundingDate":"2005","slogan":"Re-greening Sri Lanka","email":"info@enerfab.lk","telephone":"+94-11-288-8821","address":{"@type":"PostalAddress","streetAddress":"No. 115/3, Rampart Road","addressLocality":"Sri Jayawardenepura Kotte","addressRegion":"Western Province","addressCountry":"LK"},"areaServed":[{"@type":"Country","name":"Sri Lanka"}],"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"16:00"}],"contactPoint":[{"@type":"ContactPoint","telephone":"+94-11-288-8821","email":"info@enerfab.lk","contactType":"sales","areaServed":"LK","availableLanguage":["en"]},{"@type":"ContactPoint","telephone":"+1-226-246-1363","contactType":"sales","areaServed":"CA","availableLanguage":["en"]}],"knowsAbout":["Biomass gasification","Producer gas","Combined heat and power","Dual-fuel burners","Fuelwood plantations","Gliricidia","Mini-hydro turbines","Steel fabrication","Overhead cranes","Energy audits"],"hasOfferCatalog":{"@type":"OfferCatalog","name":"EnerFab engineering divisions","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","@id":"https://enerfab.lk/solutions/biomass-gasifiers/#service","name":"Biomass gasifiers","url":"https://enerfab.lk/solutions/biomass-gasifiers/"}},{"@type":"Offer","itemOffered":{"@type":"Service","@id":"https://enerfab.lk/solutions/fuelwood-biomass-supply/#service","name":"Fuelwood and biomass supply","url":"https://enerfab.lk/solutions/fuelwood-biomass-supply/"}},{"@type":"Offer","itemOffered":{"@type":"Service","@id":"https://enerfab.lk/solutions/steel-fabrication/#service","name":"Steel fabrication","url":"https://enerfab.lk/solutions/steel-fabrication/"}},{"@type":"Offer","itemOffered":{"@type":"Service","@id":"https://enerfab.lk/solutions/mini-hydro-power-plants/#service","name":"Mini-hydro power plants","url":"https://enerfab.lk/solutions/mini-hydro-power-plants/"}},{"@type":"Offer","itemOffered":{"@type":"Service","@id":"https://enerfab.lk/solutions/material-handling/#service","name":"Material handling","url":"https://enerfab.lk/solutions/material-handling/"}},{"@type":"Offer","itemOffered":{"@type":"Service","@id":"https://enerfab.lk/solutions/esco-energy-solutions/#service","name":"ESCO and energy audits","url":"https://enerfab.lk/solutions/esco-energy-solutions/"}}]},"sameAs":["https://efpl.org/","https://twitter.com/enerfabsl","https://www.facebook.com/EnerFab-111641701442166","https://www.youtube.com/channel/UCOWz3FGpK5kuBd6PYCL0LBg","https://instagram.com/enerfab"]}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","@id":"https://enerfab.lk/#website","name":"EnerFab","url":"https://enerfab.lk/","publisher":{"@id":"https://enerfab.lk/#org"},"inLanguage":"en-LK"}</script>
</head>
```

Heading outline:
```
H1: Biomass gasifiers and green energy for Sri Lankan industry
  H2: Fuel from sustainable energy plantations
  H2: Chopped to size, fed from above
  H2: Solid wood becomes a clean-burning gas
  H2: Heat for boilers, kilns and dryers
  H2: Electricity from waste wood
  H2: Running for more than a decade
  H2: Six engineering divisions
    H3: Biomass gasifiers
    H3: Fuelwood and biomass supply
    H3: Steel fabrication
    H3: Mini-hydro power plants
    H3: Material handling
    H3: ESCO and energy audits
  H2: Keep your boiler. Change the fuel.
  H2: From scrubland to an energy forest
  H2: See the plants running
  H2: Make an inquiry today.
```

### `/solutions/biomass-gasifiers/` `<head>`
```html
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Biomass Gasifiers Sri Lanka | Diesel &amp; Furnace Oil to Biomass | EnerFab</title>
<meta name="description" content="Biomass gasifiers and CHP for Sri Lankan industry: dual-fuel burners that switch diesel and furnace-oil boilers to producer gas, and gasifier generators up to 250 kWe.">
<link rel="canonical" href="https://enerfab.lk/solutions/biomass-gasifiers/">
<link rel="alternate" hreflang="en-LK" href="https://enerfab.lk/solutions/biomass-gasifiers/">
<link rel="alternate" hreflang="x-default" href="https://enerfab.lk/solutions/biomass-gasifiers/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="author" content="EnerFab (Pvt) Ltd">
<meta property="og:site_name" content="EnerFab">
<meta property="og:locale" content="en_LK">
<meta property="og:type" content="website">
<meta property="og:title" content="Biomass Gasifiers Sri Lanka | Diesel &amp; Furnace Oil to Biomass | EnerFab">
<meta property="og:description" content="Biomass gasifiers and CHP for Sri Lankan industry: dual-fuel burners that switch diesel and furnace-oil boilers to producer gas, and gasifier generators up to 250 kWe.">
<meta property="og:url" content="https://enerfab.lk/solutions/biomass-gasifiers/">
<meta property="og:image" content="https://enerfab.lk/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="EnerFab engineers commissioning a biomass gasifier">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@enerfabsl">
<meta name="twitter:title" content="Biomass Gasifiers Sri Lanka | Diesel &amp; Furnace Oil to Biomass | EnerFab">
<meta name="twitter:description" content="Biomass gasifiers and CHP for Sri Lankan industry: dual-fuel burners that switch diesel and furnace-oil boilers to producer gas, and gasifier generators up to 250 kWe.">
<meta name="twitter:image" content="https://enerfab.lk/assets/img/og-image.jpg">
<meta name="theme-color" content="#0c1510">
<meta name="format-detection" content="telephone=no">
<meta name="geo.region" content="LK-11">
<meta name="geo.placename" content="Sri Jayawardenepura Kotte">
<link rel="icon" type="image/png" href="/assets/img/enerfab-mark.png">
<link rel="apple-touch-icon" href="/assets/img/enerfab-mark.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/css/style.css?v=335834a4">
<script>if(!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('motion');setTimeout(function(){if(!window.gsap)document.documentElement.classList.remove('motion')},4000)</script>
<script type="importmap">{"imports":{"three":"/js/vendor/three.module.min.js","three/addons/":"/js/vendor/three-addons/"}}</script>
<link rel="modulepreload" href="/js/vendor/three.module.min.js">
<script src="/js/vendor/gsap.min.js" defer></script>
<script src="/js/vendor/ScrollTrigger.min.js" defer></script>
<script src="/js/vendor/SplitText.min.js" defer></script>
<script src="/js/vendor/lenis.min.js" defer></script>
<script src="/js/main.js?v=e95d237c" defer></script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":["Organization","LocalBusiness"],"@id":"https://enerfab.lk/#org","name":"EnerFab (Pvt) Ltd","alternateName":["EnerFab","EnerFab Green Engineering","EFPL"],"url":"https://enerfab.lk/","logo":"https://enerfab.lk/assets/img/enerfab-mark.png","image":"https://enerfab.lk/assets/img/og-image.jpg","description":"Sri Lankan renewable energy and engineering company, founded in 2005: biomass gasifiers and CHP, fuelwood supply, steel fabrication, mini-hydro, material handling and ESCO energy services.","foundingDate":"2005","slogan":"Re-greening Sri Lanka","email":"info@enerfab.lk","telephone":"+94-11-288-8821","address":{"@type":"PostalAddress","streetAddress":"No. 115/3, Rampart Road","addressLocality":"Sri Jayawardenepura Kotte","addressRegion":"Western Province","addressCountry":"LK"},"areaServed":[{"@type":"Country","name":"Sri Lanka"}],"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"16:00"}],"contactPoint":[{"@type":"ContactPoint","telephone":"+94-11-288-8821","email":"info@enerfab.lk","contactType":"sales","areaServed":"LK","availableLanguage":["en"]},{"@type":"ContactPoint","telephone":"+1-226-246-1363","contactType":"sales","areaServed":"CA","availableLanguage":["en"]}],"knowsAbout":["Biomass gasification","Producer gas","Combined heat and power","Dual-fuel burners","Fuelwood plantations","Gliricidia","Mini-hydro turbines","Steel fabrication","Overhead cranes","Energy audits"],"hasOfferCatalog":{"@type":"OfferCatalog","name":"EnerFab engineering divisions","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","@id":"https://enerfab.lk/solutions/biomass-gasifiers/#service","name":"Biomass gasifiers","url":"https://enerfab.lk/solutions/biomass-gasifiers/"}},{"@type":"Offer","itemOffered":{"@type":"Service","@id":"https://enerfab.lk/solutions/fuelwood-biomass-supply/#service","name":"Fuelwood and biomass supply","url":"https://enerfab.lk/solutions/fuelwood-biomass-supply/"}},{"@type":"Offer","itemOffered":{"@type":"Service","@id":"https://enerfab.lk/solutions/steel-fabrication/#service","name":"Steel fabrication","url":"https://enerfab.lk/solutions/steel-fabrication/"}},{"@type":"Offer","itemOffered":{"@type":"Service","@id":"https://enerfab.lk/solutions/mini-hydro-power-plants/#service","name":"Mini-hydro power plants","url":"https://enerfab.lk/solutions/mini-hydro-power-plants/"}},{"@type":"Offer","itemOffered":{"@type":"Service","@id":"https://enerfab.lk/solutions/material-handling/#service","name":"Material handling","url":"https://enerfab.lk/solutions/material-handling/"}},{"@type":"Offer","itemOffered":{"@type":"Service","@id":"https://enerfab.lk/solutions/esco-energy-solutions/#service","name":"ESCO and energy audits","url":"https://enerfab.lk/solutions/esco-energy-solutions/"}}]},"sameAs":["https://efpl.org/","https://twitter.com/enerfabsl","https://www.facebook.com/EnerFab-111641701442166","https://www.youtube.com/channel/UCOWz3FGpK5kuBd6PYCL0LBg","https://instagram.com/enerfab"]}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://enerfab.lk/"},{"@type":"ListItem","position":2,"name":"Solutions","item":"https://enerfab.lk/solutions/"},{"@type":"ListItem","position":3,"name":"Biomass gasifiers","item":"https://enerfab.lk/solutions/biomass-gasifiers/"}]}</script><script type="application/ld+json">{"@context":"https://schema.org","@type":"Service","@id":"https://enerfab.lk/solutions/biomass-gasifiers/#service","name":"Biomass gasifiers","serviceType":"Biomass gasifiers","description":"Biomass gasifiers and CHP for Sri Lankan industry: dual-fuel burners that switch diesel and furnace-oil boilers to producer gas, and gasifier generators up to 250 kWe.","url":"https://enerfab.lk/solutions/biomass-gasifiers/","provider":{"@id":"https://enerfab.lk/#org"},"areaServed":{"@type":"Country","name":"Sri Lanka"},"image":"https://enerfab.lk/assets/img/commissioning-250kw-gasifier.jpg"}</script>
</head>
```

Heading outline:
```
H1: Biomass gasifiers and CHP systems
  H2: Off diesel, furnace oil and LPG
    H3: What EnerFab provides
  H2: Inside a gasifier plant
  H2: How the conversion works
    H3: Fuelwood in
    H3: Gasification
    H3: Piped like LPG
    H3: Heat and power
  H2: Gasifier conversion compared
    H3: Reported figures
    H3: Thermal applications
    H3: Electrical applications
  H2: Serving industry since 2005
  H2: Related solutions
    H3: Fuelwood and biomass supply
    H3: ESCO and energy audits
    H3: Steel fabrication
  H2: Make an inquiry today.
```

Every page has its own keyword-led title (under 65 characters), a description of about 150–160 characters, a self-referencing canonical, `hreflang="en-LK"`, Open Graph and Twitter cards, and breadcrumbs.

---

## 6. JSON-LD structured data (built)

### Organization + LocalBusiness (every page)

`sameAs` includes efpl.org, so Google connects the old site's brand history to the enerfab.lk entity, and `hasOfferCatalog` lists all six divisions.

```json
{
  "@context": "https://schema.org",
  "@type": [
    "Organization",
    "LocalBusiness"
  ],
  "@id": "https://enerfab.lk/#org",
  "name": "EnerFab (Pvt) Ltd",
  "alternateName": [
    "EnerFab",
    "EnerFab Green Engineering",
    "EFPL"
  ],
  "url": "https://enerfab.lk/",
  "logo": "https://enerfab.lk/assets/img/enerfab-mark.png",
  "image": "https://enerfab.lk/assets/img/og-image.jpg",
  "description": "Sri Lankan renewable energy and engineering company, founded in 2005: biomass gasifiers and CHP, fuelwood supply, steel fabrication, mini-hydro, material handling and ESCO energy services.",
  "foundingDate": "2005",
  "slogan": "Re-greening Sri Lanka",
  "email": "info@enerfab.lk",
  "telephone": "+94-11-288-8821",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "No. 115/3, Rampart Road",
    "addressLocality": "Sri Jayawardenepura Kotte",
    "addressRegion": "Western Province",
    "addressCountry": "LK"
  },
  "areaServed": [
    {
      "@type": "Country",
      "name": "Sri Lanka"
    }
  ],
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday"
      ],
      "opens": "09:00",
      "closes": "16:00"
    }
  ],
  "contactPoint": [
    {
      "@type": "ContactPoint",
      "telephone": "+94-11-288-8821",
      "email": "info@enerfab.lk",
      "contactType": "sales",
      "areaServed": "LK",
      "availableLanguage": [
        "en"
      ]
    },
    {
      "@type": "ContactPoint",
      "telephone": "+1-226-246-1363",
      "contactType": "sales",
      "areaServed": "CA",
      "availableLanguage": [
        "en"
      ]
    }
  ],
  "knowsAbout": [
    "Biomass gasification",
    "Producer gas",
    "Combined heat and power",
    "Dual-fuel burners",
    "Fuelwood plantations",
    "Gliricidia",
    "Mini-hydro turbines",
    "Steel fabrication",
    "Overhead cranes",
    "Energy audits"
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "EnerFab engineering divisions",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "@id": "https://enerfab.lk/solutions/biomass-gasifiers/#service",
          "name": "Biomass gasifiers",
          "url": "https://enerfab.lk/solutions/biomass-gasifiers/"
        }
      },
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "@id": "https://enerfab.lk/solutions/fuelwood-biomass-supply/#service",
          "name": "Fuelwood and biomass supply",
          "url": "https://enerfab.lk/solutions/fuelwood-biomass-supply/"
        }
      },
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "@id": "https://enerfab.lk/solutions/steel-fabrication/#service",
          "name": "Steel fabrication",
          "url": "https://enerfab.lk/solutions/steel-fabrication/"
        }
      },
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "@id": "https://enerfab.lk/solutions/mini-hydro-power-plants/#service",
          "name": "Mini-hydro power plants",
          "url": "https://enerfab.lk/solutions/mini-hydro-power-plants/"
        }
      },
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "@id": "https://enerfab.lk/solutions/material-handling/#service",
          "name": "Material handling",
          "url": "https://enerfab.lk/solutions/material-handling/"
        }
      },
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "@id": "https://enerfab.lk/solutions/esco-energy-solutions/#service",
          "name": "ESCO and energy audits",
          "url": "https://enerfab.lk/solutions/esco-energy-solutions/"
        }
      }
    ]
  },
  "sameAs": [
    "https://efpl.org/",
    "https://twitter.com/enerfabsl",
    "https://www.facebook.com/EnerFab-111641701442166",
    "https://www.youtube.com/channel/UCOWz3FGpK5kuBd6PYCL0LBg",
    "https://instagram.com/enerfab"
  ]
}
```

**You do this:** add the exact office coordinates. In Google Maps, right-click the office pin, copy the two numbers, and add this to `ORG` in `tools/build.py`:
```json
"geo": { "@type": "GeoCoordinates", "latitude": 0.0, "longitude": 0.0 },
"hasMap": "https://maps.google.com/?cid=YOUR_BUSINESS_PROFILE_CID"
```
They are left out on purpose rather than guessed.

### Service (each division page; biomass gasifiers shown)
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://enerfab.lk/solutions/biomass-gasifiers/#service",
  "name": "Biomass gasifiers",
  "serviceType": "Biomass gasifiers",
  "description": "Biomass gasifiers and CHP for Sri Lankan industry: dual-fuel burners that switch diesel and furnace-oil boilers to producer gas, and gasifier generators up to 250 kWe.",
  "url": "https://enerfab.lk/solutions/biomass-gasifiers/",
  "provider": {
    "@id": "https://enerfab.lk/#org"
  },
  "areaServed": {
    "@type": "Country",
    "name": "Sri Lanka"
  },
  "image": "https://enerfab.lk/assets/img/commissioning-250kw-gasifier.jpg"
}
```

### FAQPage (`/faq/`)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What can an EnerFab biomass gasifier replace?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Diesel, furnace oil (HFO) and LPG fired boilers, furnaces, kilns and dryers, and the fuel in internal combustion engines that drive electrical generators."
      }
    },
    {
      "@type": "Question",
      "name": "Do I need to replace my boiler to switch to biomass?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. A biomass gasifier with a dual-fuel burner switches your diesel or furnace-oil boiler to producer gas. You keep operating the same boiler, and your previous fuel stays available as a backup."
      }
    },
    {
      "@type": "Question",
      "name": "Why use a gasifier instead of a wood-fired boiler?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "EnerFab’s conversion method gives better efficiency, a better response to load variation and lower particulate emissions than a wood-fired boiler."
      }
    },
    {
      "@type": "Question",
      "name": "Can a gasifier generate electricity?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Producer gas can run an internal combustion engine that turns a generator. EnerFab installed a gasifier generator at a wood processing plant that makes 200 kW from waste wood, with a further 400 kW of thermal energy available from the engine’s exhaust and cooling system. EnerFab also builds combined heat and power plants."
      }
    },
    {
      "@type": "Question",
      "name": "What sizes and efficiencies are EnerFab gasifiers?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A University of Moratuwa review in Tech Monitor (2007) reported EnerFab gasifiers for electricity from 1 to 250 kWe with about 30% overall efficiency, and thermal gasifiers in Sri Lanka from 100 to 350 kW with claimed efficiencies of 70 to 80%. Each system is sized to your load, so contact us for current figures."
      }
    },
    {
      "@type": "Question",
      "name": "How long do EnerFab gasifiers last?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Kandalama Hotel, Tea Factory Hotel, CW Mackie and other establishments have operated EnerFab gasifiers for more than a decade. A rubber processing dryer converted from diesel has operated from 2006 to date."
      }
    },
    {
      "@type": "Question",
      "name": "Who operates and maintains the plant?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "EnerFab offers management contracts to operate the plants it supplies, and provides spare parts and breakdown maintenance for every installation it has completed. We have provided after-sales service since 2005."
      }
    },
    {
      "@type": "Question",
      "name": "What fuelwood can be used?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Gliricidia, Ipil Ipil, cinnamon, timber off-cuts, coconut shells and other approved fuelwood trees. A wood processing plant can run a gasifier on its own waste wood."
      }
    },
    {
      "@type": "Question",
      "name": "Can EnerFab supply biomass on contract?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. EnerFab supplies biomass on a contractual basis from its energy plantations and an out-grower network: a collection network of 3,000 farmers and a supplier base of more than 2,000 across Sri Lanka, outside the North and East."
      }
    },
    {
      "@type": "Question",
      "name": "How much of a power plant’s fuel should it control itself?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "In EnerFab’s view, at least 50%. If outside supply networks fall short, your own supply has to carry the plant until they recover."
      }
    },
    {
      "@type": "Question",
      "name": "What wood-handling equipment does EnerFab make?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The EWG 1 wood grab, which grabs 1 m³ of chips at 20% moisture (US$ 10,000), and the DM500 wood chopper, which processes 500 kg of fuelwood an hour (US$ 5,000)."
      }
    },
    {
      "@type": "Question",
      "name": "What steel structures does EnerFab fabricate?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Steel lattice structures, steel buildings, large advertising structures, steel penstock pipelines, water, diesel and HFO storage tanks and pipelines, small hydro power plants and other civil works, designed to international standards with corrosion protection."
      }
    },
    {
      "@type": "Question",
      "name": "Which hydro turbines does EnerFab supply?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "EnerFab is the sole agent in Sri Lanka for GUGLER Water Turbines: Kaplan, Pelton and Francis turbines from 5 kW to 10 MW, horizontal or vertical, with design, installation and servicing."
      }
    },
    {
      "@type": "Question",
      "name": "What crane capacities are available?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Single girder overhead travelling and suspension cranes to 12.5 tons over 30 m, double girder overhead travelling cranes to 160 tons over 30 m, gantry and semi-gantry cranes to 160 tons over 50 m, jib cranes to 5 tons and light cranes to 2 tons."
      }
    },
    {
      "@type": "Question",
      "name": "What do EnerFab’s ESCO services include?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Preliminary and detailed energy audits, other energy studies, and turnkey energy-saving projects with a payback guarantee. EnerFab has completed more than 15 detailed energy audits."
      }
    }
  ]
}
```

Product schema for the EWG 1 wood grab and DM500 chopper is on the fuelwood page. Check every page with the Rich Results Test (search.google.com/test/rich-results) after launch.

---

## 7. Core Web Vitals and the 60-day authority plan

### Performance (built)
- **No render-blocking JavaScript:** all scripts use `defer` or `module`; the 3D engine loads only on the two pages that use it, and on the gasifier page only when the viewer scrolls near.
- **3D only while visible:** the render loop stops when the model is off-screen or the tab is hidden. Pixel ratio is capped on phones.
- **YouTube facade:** a lightweight thumbnail until the visitor taps play, then the privacy-enhanced player.
- **Images:** WebP in two sizes (800 px for phones, full size for desktop) with JPG fallback, explicit width and height (no layout shift), lazy-loading below the fold, high priority for the page hero image.
- **Caching (`_headers`):** CSS, JS and vendor files are cached for a year; their URLs carry a content hash (`?v=…`) that changes on every edit. Images are cached for 30 days, HTML is always revalidated.
- **Motion respects the visitor:** smooth scrolling only on mouse and trackpad (touch scrolling stays native); everything is static for visitors who turn on *reduce motion*; content stays visible if scripts fail.
- **Measured locally** on the gasifier page (phone viewport, local server): content loaded in about 0.1 s, largest paint about 0.13 s, layout shift 0, no console errors. Real-world numbers depend on the network, so test after launch with **PageSpeed Insights** (pagespeed.web.dev) on mobile for `/` and `/solutions/biomass-gasifiers/`. A Lighthouse run wasn't possible in this session.

**Optional extras:** turn on Cloudflare **Web Analytics** (cookie-free; already allowed by the CSP), and **Early Hints** and **HTTP/3** under Speed → Optimization.

### 60-day authority plan (You do this)

| Days | Actions |
|---|---|
| 1–7 | Launch; Search Console, Bing, sitemap; update Google Business Profile and all social links to enerfab.lk; add the canonical lines and the "new website" link to efpl.org |
| 8–14 | Create a LinkedIn company page (add it to `sameAs` in `tools/build.py`); post the 3D tour video and a launch post. Ask staff to list EnerFab with an enerfab.lk link on their LinkedIn profiles |
| 15–21 | Directories: Sri Lanka Sustainable Energy Authority (energy.gov.lk) supplier and ESCO lists; Ceylon Chamber of Commerce member directory; National Chamber of Commerce; Bioenergy Association of Sri Lanka; Yellow Pages Sri Lanka (yellowpages.lk). Use identical name, address and phone everywhere |
| 22–30 | Partners: ask GUGLER Water Turbines and ATT Lifting Equipment to list EnerFab as their Sri Lanka partner with a link to the matching enerfab.lk page. Ask the University of Moratuwa mechanical engineering department about a mention or a student project link |
| 31–40 | Press release: "EnerFab, Sri Lanka's leading gasifier maker since 2005, launches enerfab.lk", built around one real case study with real figures. Send it to the Daily FT, the Sunday Times business section, EconomyNext, Daily Mirror Business and LankaBusinessOnline |
| 41–50 | Customers: ask the hotels and factories that run EnerFab gasifiers to mention them on their sustainability pages with a link, and to leave Google reviews |
| 51–60 | Have an EnerFab engineer review the six launch guides in `/insights/`, publish one new guide, share each guide on LinkedIn, and review Search Console: which searches appear, which pages need work |

Monthly after that: one article, one Google Business Profile post, one new project or update, check Search Console and reply to reviews.
