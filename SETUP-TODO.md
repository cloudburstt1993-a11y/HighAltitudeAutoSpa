# Setup To-Do: High Altitude Auto Spa

Everything the site needs before it can go live. The pages are built and pass
QA. What's left is real business information, a few decisions only the
client can make, and the account setup.

The one fact verified so far: **High Altitude Auto Spa is a car detailing
shop in Grand Junction, CO.** Every other business detail is a `[PLACEHOLDER]`.
Nothing was invented: no phone number, address, prices, reviews, or years in
business.

---

## 1. Fill in the blanks

Every blank appears in square brackets. Replacing them all in one pass
guarantees that the business name, address, and phone (NAP) are identical on
every page, which local SEO depends on.

| Placeholder | What it is | Example format |
|---|---|---|
| `[PHONE]` | Phone number as people read it | `(970) 555-0100` |
| `[PHONE_TEL]` | Same number for tap-to-call links | `+19705550100` |
| `[EMAIL]` | Contact email | `hello@example.com` |
| `[ADDRESS_STREET]` | Street address of the shop | `123 Example Ave, Unit B` |
| `[ZIP]` | ZIP code | `81501` |
| `[HOURS]` | Hours, as shown on the site | `Mon–Fri 8am–5pm, Sat 9am–2pm` |
| `[HOURS_SCHEMA]` | Same hours, in Google's format | `Mo-Fr 08:00-17:00` |
| `[MAPS_URL]` | The Google Business Profile **Share** link | `https://maps.app.goo.gl/...` |
| `[SITE_URL]` | Live address, no trailing slash | `https://highaltitudeautospagj.com` |
| `[FORMSPREE_ID]` | Formspree form ID (step 4) | `xpzvqkab` |
| `[GA4_ID]` | GA4 Measurement ID (step 4) | `G-ABC123XYZ9` |
| `[PRICE_INTERIOR]` `[PRICE_EXTERIOR]` `[PRICE_FULL]` `[PRICE_CORRECTION]` `[PRICE_CERAMIC]` | "Starting at" prices | `$149` |
| `[ABOUT_STORY]` | 2–3 sentences in the owner's words (about.html) | Replace by hand, it's a paragraph |

**Use the exact phone, address, and hours from the Google Business Profile**,
character for character, or set the profile to match these.

**Hours with more than one range:** `[HOURS_SCHEMA]` holds one range. For
split hours, edit the `openingHours` line in `index.html` by hand:
`"openingHours": ["Mo-Fr 08:00-17:00", "Sa 09:00-14:00"],`

### Replace them all at once (PowerShell, from the project folder)

Edit the values on the right, then paste the whole block:

```powershell
$values = [ordered]@{
  '[PHONE_TEL]'        = '+19705550100'
  '[PHONE]'            = '(970) 555-0100'
  '[EMAIL]'            = 'hello@example.com'
  '[ADDRESS_STREET]'   = '123 Example Ave'
  '[ZIP]'              = '81501'
  '[HOURS_SCHEMA]'     = 'Mo-Fr 08:00-17:00'
  '[HOURS]'            = 'Mon–Fri 8am–5pm'
  '[MAPS_URL]'         = 'https://maps.app.goo.gl/XXXX'
  '[SITE_URL]'         = 'https://example.com'
  '[FORMSPREE_ID]'     = 'xxxxxxxx'
  '[GA4_ID]'           = 'G-XXXXXXXXXX'
  '[PRICE_INTERIOR]'   = '$000'
  '[PRICE_EXTERIOR]'   = '$000'
  '[PRICE_FULL]'       = '$000'
  '[PRICE_CORRECTION]' = '$000'
  '[PRICE_CERAMIC]'    = '$000'
}
Get-ChildItem -Recurse -File -Include *.html,*.js,*.xml,*.txt |
  Where-Object FullName -notmatch '\\(\.git|src)\\' |
  ForEach-Object {
    $text = [IO.File]::ReadAllText($_.FullName)
    $new = $text
    foreach ($k in $values.Keys) { $new = $new.Replace($k, $values[$k]) }
    if ($new -ne $text) { [IO.File]::WriteAllText($_.FullName, $new); "updated $($_.FullName)" }
  }
```

### Check nothing is left

```bash
grep -rnoE '\[[A-Z0-9_]{3,}\]' --include='*.html' --include='*.js' --include='*.xml' --include='*.txt' .
```

No output means every blank is filled. Today it finds 17 different
placeholders.

**Not showing prices?** Delete the `From [PRICE_…]` lines instead of filling
them: the four service cards and the "Full detail" box in `index.html`, plus
one line near the top of each page in `services/`.

---

## 2. Confirm with the client

### The name clash (important)

A **different** business called "High Altitude Auto Spa" is listed on Yelp:
a mobile detailer in Aurora, CO (Denver metro, 303 number). Search engines can
mix the two up. The site always pairs the name with "Grand Junction" (page
titles, header, structured data) to keep them apart. Also:

- [ ] Pick a domain that includes the location if the plain name is taken
  (e.g. `highaltitudeautospagj.com`)
- [ ] Claim or create the Google Business Profile (category: *Car detailing
  service*) with exactly the same name, address, and phone as the site
- [ ] Never link to or reuse anything from the Aurora listing

### Claims on the site that describe how they work

These are standard for a detailing shop, but each one is a promise. Check
that every item is true for this shop, and cut or reword any that isn't:

- [ ] **Service list.** Do they offer all four (interior, exterior, paint
  correction, ceramic coating) plus a full detail? Anything missing (headlight
  restoration, engine bay, odor treatment, RVs or boats)?
- [ ] **"What's included" checklists** on each page in `services/`
  (two-bucket hand wash, hot-water extraction, compressed-air vent purge,
  clay bar, mag chloride removal, UV protectant, etc.)
- [ ] **"Done indoors"** (home page, about page). Does the shop have an
  indoor bay, and does all work happen inside?
- [ ] **"You'll have the quote before we start"** (home page)
- [ ] **"We'll call when it's ready and walk you through what we did"** (home page)
- [ ] **"No surprise add-ons at pickup"** (about page)
- [ ] **Nearby towns:** Fruita, Palisade, Clifton, Redlands, Orchard Mesa,
  Whitewater. Add or remove any.
- [ ] **Ceramic coating:** the page doesn't state how many years a coating
  lasts. If they sell named packages with ratings, those can be added.

---

## 3. Photos and logo

- [ ] **Logo.** The mesa-and-sparkle mark is a placeholder I drew. If they
  have a real logo, send it (SVG preferred) and it replaces the header,
  favicon, and share image.
- [ ] **Before/after photos of their own work, 6–10.** A gallery is
  pre-built and commented out in `index.html` (search `GALLERY`). Run the
  photos through `asset-processor` for AVIF/WebP/JPEG sets, then uncomment.
  Never use stock photos as "our work."
- [ ] **A hero photo (optional).** The right side of the home page hero is
  open on desktop. A shot of a finished car in the shop would fill it. Keep it
  eager-loaded (it would become the LCP image).
- [ ] **Reviews.** No testimonials or star ratings are on the site. Once they
  have Google reviews, add a "Read our reviews on Google" link. Only quote
  reviews with the reviewer's permission.

---

## 4. Accounts to set up

- [ ] **Formspree.** Create a form, set the notification email to the
  shop's inbox, and copy the ID from the endpoint
  (`https://formspree.io/f/THIS_PART`) into `[FORMSPREE_ID]`. After going
  live, send one test request and confirm it arrives.
- [ ] **GA4.** Create a property and web stream, then put the Measurement ID
  in `[GA4_ID]`. Analytics stays switched off until a real ID is in. Once
  the events first fire, mark both as **key events** (Admin → Events):
  - `generate_lead`: quote form sent (only fires on a successful send)
  - `click_to_call`: any phone link tapped. `link_location` says which one
    (`hero`, `header`, `mobile-bar`, `cta-band`, `footer`, …)
- [ ] **Google Search Console.** Verify by DNS, then submit `/sitemap.xml`.
- [ ] **Google Business Profile.** Set the Website link to the home page with
  `?utm_source=google&utm_medium=organic&utm_campaign=gbp` so Maps traffic
  shows up separately in GA4.

---

## 5. Go live (GitHub Pages)

1. Create the GitHub repo (`gh repo create`), push `main`, then go to
   Settings → Pages → *Deploy from a branch* → `main` / root.
2. Add a `CNAME` file at the root containing just the domain (not created
   yet because the domain isn't chosen).
3. DNS: four A records for the apex to `185.199.108.153`,
   `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, and a CNAME for
   `www` pointing to `<github-user>.github.io`.
4. Once the certificate is issued, tick **Enforce HTTPS**.

Notes:

- `404.html` uses root paths (`/css/style.css`) so it works at any depth on
  the custom domain. On the temporary `github.io/<repo>/` address it will
  look unstyled, which is expected and fixes itself once the domain is
  connected.
- `_config.yml` keeps `README.md`, this file, and `src/` off the public
  site.

---

## 6. QA already done (October 15, 2026)

Run locally at 375px (phone) and 1366px (desktop):

- Lighthouse (mobile): Performance 99–100, Accessibility 100, Best Practices
  100 on every page. LCP 1.2–1.5s, layout shift 0. SEO shows 83 only because
  `[SITE_URL]` isn't a real URL yet (canonical + robots.txt); it clears once
  filled.
- linkinator: no broken internal links.
- Quote form: empty submit blocked, error message on a failed send,
  confirmation on success, GA4 event fires only on success.
- Mobile menu: opens, closes on Escape, focus returns to the button.
- Call button visible above the fold on a 375×667 phone, plus a fixed call
  bar at the bottom.

Re-run Lighthouse and linkinator after the placeholders are filled and again
on the live domain.
