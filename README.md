# EnerFab — enerfab.lk

Website for EnerFab (Pvt) Ltd, a Sri Lankan biomass and renewable-energy engineering company (since 2005). It runs on **Cloudflare Pages**. Company facts come from the older site, efpl.org, which stays online.

**Launch, security and SEO steps: [SEO-SECURITY-BLUEPRINT.md](SEO-SECURITY-BLUEPRINT.md).**

## Pages

| URL | What it is |
|---|---|
| `/` | Home: scroll-driven 3D tour of a gasifier plant |
| `/solutions/` | Hub for the six divisions |
| `/solutions/biomass-gasifiers/` and five more | One page per division |
| `/projects/` | Case studies |
| `/faq/` | Technical FAQ |
| `/about/`, `/videos/`, `/recognition/`, `/contact/` | Company pages |

## Folders

```
tools/build.py          generates every page, sitemap.xml, robots.txt, _headers, _redirects
tools/serve.py          local preview that applies the same security headers as Cloudflare
css/style.css           all styles
js/main.js              menu, motion (GSAP, ScrollTrigger, SplitText, Lenis), form, videos
js/plant3d.js           the 3D gasifier plant (three.js)
js/vendor/              self-hosted libraries (no third-party script CDNs)
functions/api/inquiry.js  secure form handler (Cloudflare Pages Function)
assets/img/             photos (.jpg plus .webp copies)
```

## Edit and preview

Change text in `tools/build.py`, then:

```bash
python tools/build.py
```

```bash
python tools/serve.py
```

Open http://localhost:8080. Don't hand-edit the generated `index.html` files: the next build overwrites them. New photos go in `assets/img/` as `.jpg`; the build makes WebP copies automatically (needs `pip install pillow`).

The form only sends on Cloudflare. Set it up as described in section 3 of the blueprint.
