#!/usr/bin/env python3
"""Generates every page of the site from one set of business details.

    python3 src/build.py            # writes *.html, services/*.html, sitemap.xml, robots.txt
    tailwindcss -i src/input.css -o css/style.css --minify

Business details live in SITE below. Page copy lives in src/content.py.
GitHub Pages serves the generated files as-is; src/ is excluded by _config.yml.
"""
from __future__ import annotations
import os, re, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
import content as C  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = {
    "name": "High Altitude Auto Spa",
    "short": "HAAS",
    "owner": "Ryan Clark",
    "phone": "(970) 623-0825",
    "phone_tel": "+19706230825",
    "email": "ryanclark970@gmail.com",
    "street": "2912 Hill Ave",
    "city": "Grand Junction",
    "state": "CO",
    "zip": "81504",
    "hours": "Mon–Sat 9 AM–5 PM · Sun closed",
    "hours_short": "Mon–Sat 9–5",
    "hours_schema": ["Mo-Sa 09:00-17:00"],
    "geo": (39.0748819, -108.5127816),
    "maps_url": "https://www.google.com/maps/search/?api=1&query=High+Altitude+Auto+Spa+2912+Hill+Ave+Grand+Junction+CO",
    "reviews_url": "https://www.google.com/maps/search/?api=1&query=High+Altitude+Auto+Spa+2912+Hill+Ave+Grand+Junction+CO",
    "rating": "5.0",
    "review_count": "88",
    "facebook": "https://www.facebook.com/people/High-Altitude-Auto-Spa/61581744937560/",
    "instagram": "https://www.instagram.com/highaltituteautospa/",
    "instagram_handle": "@highaltituteautospa",
    # Draft address on GitHub Pages. Swap for the real domain (no trailing slash) at launch.
    "site_url": "https://cloudburstt1993-a11y.github.io/HighAltitudeAutoSpa",
    "formspree_id": "[FORMSPREE_ID]",
    "towns": ["Fruita", "Palisade", "Clifton", "Redlands", "Orchard Mesa", "Whitewater"],
}

SERVICES = [
    # slug, nav label, one-line
    ("window-tinting", "Window tinting", "Ceramic film, cut and laid in the shop. Cooler cabin, less glare, UV blocked."),
    ("interior-detailing", "Interior detailing", "Vents, seams, carpet, seats, and glass. Dust, pet hair, spills, and smells, gone."),
    ("exterior-detailing", "Exterior detailing", "Hand wash, decontamination, and protection on paint, wheels, and glass."),
    ("ceramic-coating", "Ceramic coating", "Nasiol nano-coating applied by a certified installer. Years of gloss and easy washing."),
    ("paint-correction", "Paint correction", "Machine polishing that takes out swirl marks, light scratches, and sun haze."),
]

ICON_PHONE = '<svg class="size-5 shrink-0" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2Z"/></svg>'
ICON_PIN = '<svg class="size-5 shrink-0" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>'
ICON_CLOCK = '<svg class="size-5 shrink-0" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>'
ICON_STAR = '<svg class="size-4 shrink-0" viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true" focusable="false"><path d="m12 2 3 6.6 7 .8-5.2 4.8 1.4 7L12 17.7 5.8 21.2l1.4-7L2 9.4l7-.8Z"/></svg>'


def picture(name, widths, sizes, alt, cls="", w=None, h=None, eager=False, prefix=""):
    """<picture> with avif/webp/jpg sets for assets/img/{name}-{w}.*"""
    p = f"{prefix}assets/img/{name}"
    av = ", ".join(f"{p}-{x}.avif {x}w" for x in widths)
    wb = ", ".join(f"{p}-{x}.webp {x}w" for x in widths)
    big = widths[-1]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/avif" srcset="{av}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{wb}" sizes="{sizes}">'
            f'<img src="{p}-{big}.jpg" width="{w}" height="{h}" {load} alt="{alt}" class="{cls}"></picture>')


def call_btn(location, prefix="", label=None, cls="btn btn-call"):
    label = label or f"Call {SITE['phone']}"
    return f'<a href="tel:{SITE["phone_tel"]}" class="{cls}" data-call="{location}">{ICON_PHONE} {label}</a>'


def head(title, desc, path, prefix, schema=None, og_image=None, extra=""):
    url = f"{SITE['site_url']}/{path}" if path != "index.html" else f"{SITE['site_url']}/"
    og_image = og_image or f"{SITE['site_url']}/assets/img/og-image.jpg"
    s = f'<script type="application/ld+json">{schema}</script>' if schema else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#222222">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE['name']}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{prefix}favicon.ico" sizes="32x32">
  <link rel="icon" href="{prefix}assets/img/icon-192.png" type="image/png" sizes="192x192">
  <link rel="apple-touch-icon" href="{prefix}assets/img/apple-touch-icon.png">
  <link rel="preload" href="{prefix}assets/fonts/barlow-condensed-latin-800-italic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{prefix}assets/fonts/barlow-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{prefix}css/style.css">
  <script src="{prefix}js/main.js" defer></script>
  {extra}
  {s}
</head>
<body class="pb-24 md:pb-0">
  <a href="#main" class="skip-link">Skip to content</a>
"""


def header(prefix, current=None):
    def li(href, label, cls=""):
        cur = ' aria-current="page"' if current == href else ""
        c = f' class="{cls}"' if cls else ""
        return f'<li{c}><a href="{prefix}{href}"{cur}>{label}</a></li>'
    items = "".join(li(f"services/{slug}.html", label, "md:hidden") for slug, label, _ in SERVICES)
    items += li("index.html#services", "Services", "hidden md:block").replace(f'href="{prefix}index.html#services"', f'href="{prefix}#services"')
    items += li("about.html", "About") + li("contact.html", "Contact")
    return f"""
  <header class="on-dark relative z-30 bg-black text-white">
    <div class="wrap flex items-center gap-4 py-2.5">
      <a href="{prefix or './'}" class="mr-auto flex items-center gap-3 no-underline" aria-label="{SITE['name']}, home">
        <img src="{prefix}assets/img/logo-mark.png" width="740" height="465" alt="" class="h-11 w-auto md:h-12" decoding="async">
        <span class="hidden text-sm leading-tight font-semibold text-fog sm:block">Window tint, detailing<br>&amp; ceramic coating</span>
      </a>
      <button type="button" class="nav-toggle md:hidden" aria-expanded="false" aria-controls="site-nav" data-nav-toggle>
        <svg class="size-5 shrink-0" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M4 6h16M4 12h16M4 18h16"/></svg> Menu
      </button>
      <nav id="site-nav" class="site-nav" aria-label="Main" data-nav>
        <ul>{items}</ul>
      </nav>
      <div class="hidden items-center gap-5 md:flex">
        <a href="tel:{SITE['phone_tel']}" class="hidden font-semibold text-white no-underline hover:text-orange lg:inline" data-call="header">{SITE['phone']}</a>
        <a href="{prefix}contact.html#quote" class="btn btn-call">Get a quote</a>
      </div>
    </div>
  </header>

  <main id="main">
"""


def cta_band(prefix, title="Ready when you are.", text=None):
    text = text or "Call, text, or send a quote request. Tell us the vehicle and what you're after and we'll give you a straight price."
    return f"""
    <section class="on-dark bg-black text-white" aria-labelledby="cta-title">
      <div class="wrap py-14 md:flex md:items-center md:justify-between md:gap-10 md:py-20">
        <div>
          <h2 id="cta-title" class="h2">{title}</h2>
          <p class="lede mt-3 max-w-xl">{text}</p>
        </div>
        <div class="mt-8 flex flex-col gap-3 sm:flex-row md:mt-0 md:shrink-0">
          {call_btn("cta-band")}
          <a href="{prefix}contact.html#quote" class="btn btn-outline-light">Get a quote</a>
        </div>
      </div>
    </section>
"""


def footer(prefix):
    links = "".join(f'<li><a href="{prefix}services/{slug}.html">{label}</a></li>' for slug, label, _ in SERVICES)
    return f"""
  </main>

  <footer class="on-dark border-t border-coal-line bg-black text-fog">
    <div class="wrap grid gap-10 py-14 sm:grid-cols-2 lg:grid-cols-4">
      <div>
        <a href="{prefix or './'}" class="inline-block no-underline" aria-label="{SITE['name']}, home">
          <img src="{prefix}assets/img/logo-mark.png" width="740" height="465" alt="" class="h-16 w-auto" loading="lazy" decoding="async">
        </a>
        <p class="mt-4">Window tinting, detailing, and ceramic coating in Grand Junction, Colorado. Owner-run by {SITE['owner']}.</p>
        <p class="mt-3 flex items-center gap-1.5 text-white">{ICON_STAR} {SITE['rating']} on Google, {SITE['review_count']} reviews</p>
      </div>
      <div>
        <h2 class="font-display text-xl font-bold text-white">Visit</h2>
        <address class="mt-3 not-italic">
          {SITE['name']}<br>
          {SITE['street']}<br>
          {SITE['city']}, {SITE['state']} {SITE['zip']}
        </address>
        <a href="{SITE['maps_url']}" class="mt-2 inline-block py-2 font-semibold text-white hover:text-orange">Get directions</a>
      </div>
      <div>
        <h2 class="font-display text-xl font-bold text-white">Hours and contact</h2>
        <p class="mt-3">{SITE['hours']}</p>
        <ul class="mt-3 space-y-0.5 [&_a]:inline-block [&_a]:py-1.5">
          <li><a href="tel:{SITE['phone_tel']}" class="font-semibold text-white hover:text-orange" data-call="footer">{SITE['phone']}</a></li>
          <li><a href="mailto:{SITE['email']}" class="text-white hover:text-orange">{SITE['email']}</a></li>
          <li><a href="{SITE['instagram']}" class="text-white hover:text-orange" rel="noopener">Instagram {SITE['instagram_handle']}</a></li>
          <li><a href="{SITE['facebook']}" class="text-white hover:text-orange" rel="noopener">Facebook</a></li>
        </ul>
      </div>
      <div>
        <h2 class="font-display text-xl font-bold text-white">Explore</h2>
        <ul class="mt-3 space-y-0.5 [&_a]:inline-block [&_a]:py-1.5 [&_a]:text-white [&_a]:hover:text-orange">
            {links}
            <li><a href="{prefix}about.html">About</a></li>
            <li><a href="{prefix}contact.html">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="border-t border-coal-line">
      <div class="wrap flex flex-col gap-2 py-6 text-sm sm:flex-row sm:justify-between">
        <p>&copy; <span data-year>{datetime.date.today().year}</span> {SITE['name']}</p>
        <a href="{prefix}privacy.html" class="inline-block py-2 text-fog hover:text-white">Privacy</a>
      </div>
    </div>
  </footer>

  <div class="mobile-cta on-dark">
    {call_btn("mobile-bar", label="Call now", cls="btn btn-call flex-1")}
    <a href="{prefix}contact.html#quote" class="btn btn-outline-light flex-1">Get a quote</a>
  </div>
</body>
</html>
"""


def business_schema():
    offers = ",".join(
        f'{{"@type":"Offer","itemOffered":{{"@type":"Service","name":"{label}","url":"{SITE["site_url"]}/services/{slug}.html"}}}}'
        for slug, label, _ in SERVICES)
    area = ",".join(f'{{"@type":"Place","name":"{t}, CO"}}' for t in ["Grand Junction"] + SITE["towns"])
    hours = ",".join(f'"{h}"' for h in SITE["hours_schema"])
    return (f'{{"@context":"https://schema.org","@type":"AutoRepair","@id":"{SITE["site_url"]}/#business",'
            f'"name":"{SITE["name"]}","alternateName":"HAAS",'
            f'"description":"Window tinting, auto detailing, paint correction, and ceramic coating shop in Grand Junction, Colorado.",'
            f'"url":"{SITE["site_url"]}/","telephone":"{SITE["phone_tel"]}","email":"{SITE["email"]}",'
            f'"image":"{SITE["site_url"]}/assets/img/og-image.jpg","logo":"{SITE["site_url"]}/assets/img/apple-touch-icon.png",'
            f'"founder":{{"@type":"Person","name":"{SITE["owner"]}"}},'
            f'"address":{{"@type":"PostalAddress","streetAddress":"{SITE["street"]}","addressLocality":"{SITE["city"]}","addressRegion":"{SITE["state"]}","postalCode":"{SITE["zip"]}","addressCountry":"US"}},'
            f'"geo":{{"@type":"GeoCoordinates","latitude":{SITE["geo"][0]},"longitude":{SITE["geo"][1]}}},'
            f'"openingHours":[{hours}],"hasMap":"{SITE["maps_url"]}",'
            f'"sameAs":["{SITE["facebook"]}","{SITE["instagram"]}"],'
            f'"areaServed":[{area}],"makesOffer":[{offers}]}}')


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)


def page(path, title, desc, body, current=None, schema=None, extra_head=""):
    prefix = "../" if "/" in path else ""
    html = head(title, desc, path, prefix, schema, extra=extra_head) + header(prefix, current) + body + footer(prefix)
    write(path, html)


def main():
    ctx = dict(SITE=SITE, SERVICES=SERVICES, picture=picture, call_btn=call_btn, cta_band=cta_band,
               ICON_PHONE=ICON_PHONE, ICON_PIN=ICON_PIN, ICON_CLOCK=ICON_CLOCK, ICON_STAR=ICON_STAR)
    for p in C.pages(ctx):
        page(p["path"], p["title"], p["desc"], p["body"], p.get("current"),
             business_schema() if p["path"] == "index.html" else p.get("schema"), p.get("extra_head", ""))

    # sitemap + robots
    urls = ["", "about.html", "contact.html", "privacy.html"] + [f"services/{s}.html" for s, _, _ in SERVICES]
    today = datetime.date.today().isoformat()
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += f"  <url><loc>{SITE['site_url']}/{u}</loc><lastmod>{today}</lastmod></url>\n"
    write("sitemap.xml", sm + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['site_url']}/sitemap.xml\n")


if __name__ == "__main__":
    main()
