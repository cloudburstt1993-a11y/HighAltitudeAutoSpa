# Setup To-Do: High Altitude Auto Spa

The site now carries the real business: name, address, phone, hours, Ryan's
name, the HAAS logo, the shop's own photos, and the Google rating. What's left
is account setup, a few things to confirm with Ryan, and the domain.

## 1. Confirm with Ryan (five minutes on the phone)

Everything below was taken from the Facebook page, the Google Business Profile,
Instagram, and the business card. Check it once:

- [ ] **ZIP.** Google, Yelp, and MapQuest say **81504**; the Facebook page says
  81505. The site uses 81504. Fix whichever one is wrong so the listings match.
- [ ] **Hours.** Google says Mon–Sat 9–5, closed Sunday. Facebook hides hours
  behind a login.
- [ ] **Email.** The site uses ryanclark970@gmail.com (from Facebook). If he'd
  rather use a business address, change `SITE["email"]` in `src/build.py`.
- [ ] **Instagram handle.** It's spelled `highaltituteautospa` on Instagram and
  Facebook (not "altitude"). The site links to it exactly as spelled. Worth
  mentioning to him; renaming the Instagram would be a good idea.
- [ ] **Services.** The site lists window tinting, interior, exterior, ceramic
  coating, paint correction, plus headlight restoration, graphics/vinyl,
  accessories, and fleet work. All come from his own posts and card. Cut any
  he's stopped doing.
- [ ] **Claims to verify:** "ceramic film only" (tinting page), "5+ years"
  (his Facebook intro says "over five years"), "Nasiol Pro Club certified"
  (certificate posted Oct 2026), "quote before we start, no add-ons".
- [ ] **Colorado tint law wording** (home + tinting page). It says 27% on the
  back half with 70% fronts, and a windshield visor strip. Have him confirm
  that matches what he installs; laws change.
- [ ] **Reviews.** Three Google reviews are quoted by first name (Victoria,
  Aaron) or as "Google review". They're public, but ask if he'd rather use
  different ones or none.
- [ ] **Prices.** None shown. If he wants "from" prices, add a line per service
  in `src/content.py`.

## 2. Accounts

- [ ] **Formspree.** Create a form, set the notification email, and put the ID
  in `SITE["formspree_id"]` in `src/build.py`. Until then the form posts
  nowhere; the phone number is the real CTA.
- [ ] **GA4.** Put the Measurement ID in `js/main.js` (`GA4_ID`). Mark
  `generate_lead` and `click_to_call` as key events once they fire.
- [ ] **Google Business Profile.** It has **no website** on it right now. Add
  the site URL with `?utm_source=google&utm_medium=organic&utm_campaign=gbp`.
  Primary category is already "Window tinting service"; add "Auto detailing"
  and "Car detailing service" as secondary categories if they aren't.
- [ ] **Google Search Console.** Verify, submit `/sitemap.xml`.

## 3. Domain and go-live

- [ ] Pick a domain. Watch the **name clash**: a different "High Altitude Auto
  Spa" is a mobile detailer in Aurora, CO. Something with GJ in it
  (`haasgj.com`, `highaltitudeautospagj.com`) keeps them apart in search.
- [ ] Set `SITE["site_url"]` in `src/build.py` to the real domain (no trailing
  slash), run `python3 src/build.py`, commit.
- [ ] Add a `CNAME` file at the root with the domain. DNS: A records to
  185.199.108.153 / .109 / .110 / .111 and a CNAME for `www`. Enforce HTTPS.

## 4. Nice-to-haves after launch

- More photos: a tinted car with the shade visible, an interior before/after,
  the Nasiol certificate framed on the wall. The home gallery takes three
  cards; swap in his best.
- A short video from one of his reels in the hero (they get 1–4K views each).
- Lead and review automation like the MTF / RAM packages.

## QA done (Oct 24, 2026)

Lighthouse mobile on the home page: Performance 96, Accessibility 100, Best
Practices 100, SEO 100. No horizontal scroll at 360/375/768/1366. All internal
links resolve. Mobile menu, shade picker, and form validation work. Every
link and button clears the 24px target minimum; primary actions are 48px.
