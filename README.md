# EnerFab — enerfab.lk

Website for EnerFab (Pvt) Ltd, a Sri Lankan biomass and renewable-energy engineering company (since 2005). It runs as a **Cloudflare Worker** with static assets, deployed from GitHub with `npx wrangler deploy` (config: `wrangler.jsonc`). Company facts come from the older site, efpl.org, which stays online.

**Launch, security and SEO steps: [SEO-SECURITY-BLUEPRINT.md](SEO-SECURITY-BLUEPRINT.md).**

## Pages

| URL | What it is |
|---|---|
| `/` | Home: scroll-driven 3D tour of a gasifier plant |
| `/solutions/` | Hub for the six divisions |
| `/solutions/biomass-gasifiers/` and five more | One page per division |
| `/projects/` | Case studies |
| `/faq/` | Technical FAQ |
| `/insights/` | Energy knowledge hub: 6 guides (edit in `tools/articles.py`) |
| `/about/`, `/videos/`, `/recognition/`, `/contact/` | Company pages |

## Folders

```
public/                 the website (everything Cloudflare serves)
src/worker.js           Worker: serves public/, sends /api/inquiry to src/inquiry.js
src/inquiry.js          secure form handler (Turnstile, validation, email via Resend)
wrangler.jsonc          Cloudflare config (Worker name must match the dashboard)
tools/build.py          generates every page in public/, plus sitemap.xml, robots.txt, _headers, _redirects
tools/articles.py       knowledge hub articles (text, key points, sources)
tools/serve.py          local preview that applies the same security headers as Cloudflare
public/css/style.css    all styles
public/js/main.js       menu, motion (GSAP, ScrollTrigger, SplitText, Lenis), form, videos
public/js/plant3d.js    the 3D gasifier plant (three.js)
public/js/vendor/       self-hosted libraries (no third-party script CDNs)
public/assets/img/      photos (.jpg plus .webp copies)
```

## Edit and preview

Change text in `tools/build.py`, then:

```bash
python tools/build.py
```

```bash
python tools/serve.py
```

Open http://localhost:8080. Don't hand-edit the generated `index.html` files: the next build overwrites them. New photos go in `public/assets/img/` as `.jpg`; the build makes WebP copies automatically (needs `pip install pillow`).

To test with Cloudflare's real runtime instead, run `npx wrangler dev`. The form only sends emails on Cloudflare. Set it up as described in section 3 of the blueprint.
