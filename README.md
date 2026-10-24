# High Altitude Auto Spa

Website for High Altitude Auto Spa (HAAS), Ryan Clark's window tinting and
detailing shop at 2912 Hill Ave, Grand Junction, CO. Hand-written HTML generated
from one Python file, Tailwind v4 (CLI), and one vanilla script. No framework
and no build step on the server: GitHub Pages serves the committed files as-is.

**Before launch, work through [SETUP-TODO.md](SETUP-TODO.md).** The business
details are real now; what's left is the form endpoint, analytics, and the domain.

## Structure

```
src/build.py               business details (SITE) + the page shell; run it to regenerate every page
src/content.py             the copy for each page
src/input.css              @theme tokens + @layer components (edit this, not css/style.css)
index.html                 home
services/*.html            window tinting, interior, exterior, ceramic coating, paint correction
about.html  contact.html  privacy.html  404.html
css/style.css              compiled Tailwind, committed
js/main.js                 mobile menu, tint shade picker, Formspree submit, GA4 events
assets/img/                logo marks, icons, share image, photo sets (AVIF/WebP/JPEG)
assets/fonts/              Barlow + Barlow Condensed, self-hosted
```

## Working on it

Change the phone, hours, or address in **one place**, `SITE` in `src/build.py`,
then regenerate the pages and rebuild the CSS:

```bash
python3 src/build.py
npx @tailwindcss/cli -i ./src/input.css -o ./css/style.css --minify
```

Commit the generated HTML and CSS. Preview locally with `python3 -m http.server`.

- **Don't hand-edit the HTML pages.** They're overwritten by `build.py`. Copy
  lives in `src/content.py`; the header, footer, CTA band, and mobile call bar
  live once in `build.py`.
- Colors and fonts are tokens in `src/input.css`. `black` is the logo's own
  #222. `orange` (from the business card) is for the call button only.
- Photos: drop originals in a folder and adapt `process.py` from the build
  notes (crops into `assets/img/<name>-<w>.{avif,webp,jpg}`), then reference
  them with `picture(...)` in `content.py`.
- Phone links carry `data-call="<location>"`, reported to GA4 as
  `click_to_call` → `link_location`. The shade picker reports `select_shade`.
