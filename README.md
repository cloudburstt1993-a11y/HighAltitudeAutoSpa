# High Altitude Auto Spa

Website for High Altitude Auto Spa, a car detailing shop in Grand Junction, CO.
Hand-written HTML, Tailwind v4 (standalone CLI), and one vanilla script. No
framework, no `package.json`, and no build step on the server: GitHub Pages
serves the committed files as-is.

**Before launch, work through [SETUP-TODO.md](SETUP-TODO.md).** Business
details are still `[PLACEHOLDERS]`.

## Structure

```
index.html                 home
services/*.html            interior, exterior, paint correction, ceramic coating
about.html  contact.html  privacy.html  404.html
css/style.css              compiled Tailwind, committed
src/input.css              @theme tokens + @layer components (edit this, not style.css)
js/main.js                 mobile menu, Formspree submit, GA4 events
assets/img/                favicon, touch icon, share image
```

## Working on it

Rebuild the CSS after changing any classes or `src/input.css`, and commit the
output:

```bash
tailwindcss -i ./src/input.css -o ./css/style.css --minify
```

Preview locally:

```bash
serve .
```

- **The header, footer, CTA band, and mobile call bar are duplicated on every
  page** on purpose, since there's no template engine. To change one, grep
  for it and update all nine pages. A stale nav on one page is a bug.
- Colors, fonts, and the hero type size are tokens in `src/input.css`. Add a
  token rather than a hex value or a one-off size in the markup.
- `.eyebrow` uses `canyon-dark`. Plain `canyon` text fails contrast on the
  `sand` background.
- Phone links carry `data-call="<location>"`, which is reported to GA4 as
  `click_to_call` → `link_location`. Give new phone links a unique location.
