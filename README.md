# EnerFab Green Engineering — Website

The redesigned website for [EnerFab (Pvt) Ltd](https://efpl.org), a biomass renewable-energy company in Sri Lanka. Its content comes from the original efpl.org site.

It's a plain static site (HTML, CSS and a little JavaScript), so there's no build step and nothing to install.

## Pages

| File | Page |
|---|---|
| `index.html` | Home |
| `about.html` | About: who we are, vision, mission, milestones |
| `solutions.html` | Gasifiers, fuelwood, steel fabrication, mini-hydro, material handling, ESCO |
| `videos.html` | All EnerFab videos (YouTube, loaded only when played) |
| `testimonials.html` | Recognition and press |
| `contact.html` | Contact details, map and inquiry form |

## Folder structure

```
css/style.css      all styles (colours and fonts are set at the top in :root)
js/main.js         mobile menu, animations, video player, gallery, inquiry form
assets/img/        photos and logos
assets/docs/       PDF articles
.nojekyll          tells GitHub Pages to serve files as they are
```

## Preview locally

Open `index.html` in a browser, or run a small local server:

```bash
python -m http.server 8080
```

Then go to http://localhost:8080.

## Publish with GitHub Pages

1. Push this folder to a GitHub repository.
2. In the repository, go to **Settings → Pages**.
3. Under **Source**, choose **Deploy from a branch**, pick `main` and `/ (root)`, then click **Save**.
4. After a minute the site is live at `https://<your-username>.github.io/<repo-name>/`.

To use the real domain (efpl.org), add it under **Settings → Pages → Custom domain**, then point the domain's DNS at GitHub Pages.

## Contact form

The inquiry form sends messages to **info@efpl.org** through [FormSubmit](https://formsubmit.co) (free, no account). The first time someone submits the form on the live site, FormSubmit emails info@efpl.org an activation link. Someone at EnerFab must click it once; after that, inquiries arrive normally.

The endpoint is set by `data-endpoint` on the `<form>` in `contact.html`. If you remove it, the form falls back to opening the visitor's email app.

## Editing

- **Text:** edit the HTML files directly.
- **Header and footer:** these are repeated in every page. If you change one, change all five.
- **Images:** put them in `assets/img/` and keep them under about 300 KB each.
