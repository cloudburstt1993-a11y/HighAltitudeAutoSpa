"""Page copy for High Altitude Auto Spa. Each function returns a dict for build.page()."""

SHADES = [("5", "Limo"), ("20", "Dark"), ("35", "Medium"), ("50", "Light"), ("70", "Clear")]


def shade_picker(ctx, heading_id="shade-title", compact=False, prefix=""):
    """Tint sample strip: tap a shade, the window preview darkens. Pure CSS/JS in main.js."""
    btns = "".join(
        f'<button type="button" class="shade" data-shade="{v}" aria-pressed="{"true" if v == "20" else "false"}" style="background:rgb(34 34 34 / {100 - int(v)}%)">{v}%</button>'
        for v, _ in SHADES)
    note = "" if compact else """
          <p class="mt-5 text-slate">The number is how much light gets through. Colorado lets you run 27% or darker on the back half as long as the front doors stay at 70%, and a visor strip across the top of the windshield. We'll tell you what's legal on your vehicle before any film goes on.</p>"""
    return f"""
        <div class="grid gap-8 md:grid-cols-2 md:items-center">
          <div>
            <h2 id="{heading_id}" class="h2">Pick a shade</h2>
            <p class="lede mt-3">Most people land on 20% on the back and 35% up front. Try a few.</p>{note}
          </div>
          <div data-shade-picker>
            <div class="window-preview border-4 border-black" aria-hidden="true">
              {ctx['picture']("hero-shop-wide", [640, 960], "(min-width: 768px) 50vw, 100vw", "", "absolute inset-0 h-full w-full object-cover object-bottom", 960, 720, prefix=prefix)}
              <div class="film" style="opacity:.8"></div>
            </div>
            <div class="flex gap-1.5 border-4 border-t-0 border-black bg-black p-1.5">{btns}</div>
            <p class="mt-2 text-sm text-slate" data-shade-label>20% — the dark look most people picture when they say "tinted."</p>
          </div>
        </div>"""


def review_block(ctx):
    S = ctx["SITE"]
    return f"""
    <section class="section bg-white" aria-labelledby="reviews-title">
      <div class="wrap">
        <div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <h2 id="reviews-title" class="h2">{S['rating']} stars. {S['review_count']} Google reviews.</h2>
            <p class="lede mt-3 max-w-xl">Every one of them five stars, and most of them mention Ryan by name.</p>
          </div>
          <a href="{S['reviews_url']}" class="btn btn-outline-dark shrink-0" rel="noopener">Read them on Google</a>
        </div>
        <div class="mt-10 grid gap-8 md:grid-cols-3">
          <blockquote class="quote"><p>Ryan was awesome to work with and took his time with my window tint. Very affordable and it's perfect! I'll definitely be back!</p><footer class="mt-3 text-sm font-semibold text-slate">Victoria, window tint</footer></blockquote>
          <blockquote class="quote"><p>I started by wanting my windows tinted. Ended up getting a full detailing inside. From the beginning to the end the experience was great. Ryan was very helpful and guided me on what % tint I wanted.</p><footer class="mt-3 text-sm font-semibold text-slate">Aaron, tint and interior detail</footer></blockquote>
          <blockquote class="quote"><p>I've applied tint myself and have had professionals do it, but I've never had the quality of work Ryan and his team provide. 5% ceramic on the windows and 50% ceramic on the windshield.</p><footer class="mt-3 text-sm font-semibold text-slate">Google review, ceramic tint</footer></blockquote>
        </div>
      </div>
    </section>"""


def home(ctx):
    S, pic, call = ctx["SITE"], ctx["picture"], ctx["call_btn"]
    rows = ""
    for slug, label, line in ctx["SERVICES"]:
        rows += f"""
          <div class="service-row">
            <h3 class="h3"><a href="services/{slug}.html">{label}</a></h3>
            <p class="text-slate">{line}</p>
            <a href="services/{slug}.html" class="inline-block py-2.5 font-semibold text-ink underline hover:text-orange-deep">What's included</a>
          </div>"""
    body = f"""
    <section class="on-dark relative bg-black text-white">
      <div class="wrap grid gap-0 md:grid-cols-12 md:items-stretch">
        <div class="relative z-10 py-12 md:col-span-7 md:py-20 lg:col-span-6">
          <h1 class="display text-hero">Tint, detail, and coat it for the high desert.</h1>
          <p class="lede mt-6 max-w-xl">Ceramic window film, full interior and exterior detailing, and Nasiol ceramic coatings, done in a shop on Hill Ave by the guy whose name is on the reviews.</p>
          <div class="mt-8 flex flex-col gap-3 sm:flex-row">
            {call("hero")}
            <a href="contact.html#quote" class="btn btn-outline-light">Get a quote</a>
          </div>
          <ul class="mt-10 grid gap-3 text-sm text-fog sm:grid-cols-3">
            <li class="border-l-2 border-orange pl-3"><span class="block text-2xl font-bold text-white">{S['rating']} <span class="text-orange">★</span></span>{S['review_count']} Google reviews</li>
            <li class="border-l-2 border-orange pl-3"><span class="block text-2xl font-bold text-white">5+ yrs</span>tinting and detailing</li>
            <li class="border-l-2 border-orange pl-3"><span class="block text-2xl font-bold text-white">{S['hours_short']}</span>{S['street']}, Grand Junction</li>
          </ul>
        </div>
        <div class="relative -mx-4 md:col-span-5 md:mx-0 md:-mr-6 lg:col-span-6 lg:ml-6">
          <div class="md:hidden">{pic("hero-shop-wide", [640, 960], "100vw", "Grey Nissan 370Z parked in front of the High Altitude Auto Spa shop on Hill Ave", "h-auto w-full", 960, 720, eager=True)}</div>
          <div class="absolute inset-0 hidden md:block">{pic("hero-shop", [640, 960, 1280], "(min-width: 1024px) 50vw, 42vw", "Grey Nissan 370Z parked in front of the High Altitude Auto Spa shop on Hill Ave", "h-full w-full object-cover", 1280, 1600, eager=True)}
            <div class="tint-fade absolute inset-y-0 left-0 w-1/2" aria-hidden="true"></div></div>
        </div>
      </div>
      <div class="ridge"></div>
    </section>

    <section id="services" class="section" aria-labelledby="services-title">
      <div class="wrap">
        <h2 id="services-title" class="h2">What we do</h2>
        <p class="lede mt-3 max-w-2xl">Priced by vehicle size and condition. You'll have the number before we start, and it's the number you pay.</p>
        <div class="mt-10">{rows}</div>
        <div class="mt-10 grid gap-6 md:grid-cols-[1fr_2fr] md:items-start">
          <h3 class="h3">Also in the shop</h3>
          <ul class="grid gap-x-8 gap-y-2 text-lg sm:grid-cols-2">
            <li><strong>Headlight restoration</strong>: yellowed lenses sanded, polished, and sealed.</li>
            <li><strong>Full detail</strong>: interior and exterior in one visit.</li>
            <li><strong>Graphics and vinyl</strong>: cut lettering, logos, and accent wraps.</li>
            <li><strong>Accessories</strong>: ask what we can source and fit.</li>
            <li><strong>Work vans and fleets</strong>: keep the trucks looking like the company.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section bg-glass" aria-labelledby="shade-title">
      <div class="wrap">{shade_picker(ctx)}</div>
    </section>

    {review_block(ctx)}

    <section class="section" aria-labelledby="work-title">
      <div class="wrap">
        <h2 id="work-title" class="h2">Recent work</h2>
        <p class="lede mt-3 max-w-2xl">From the shop's Instagram. More on {S['instagram_handle']}.</p>
        <div class="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <figure>{pic("work-rx7", [640, 900], "(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw", "Red Mazda RX-7 and a white sports car, both freshly detailed, parked in a driveway", "h-auto w-full", 900, 675)}<figcaption class="mt-2 text-sm text-slate">Mazda RX-7, with company.</figcaption></figure>
          <figure>{pic("work-outback", [640, 960], "(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw", "Silver Subaru Outback with clean paint and wheels in a driveway", "h-auto w-full", 960, 720)}<figcaption class="mt-2 text-sm text-slate">A daily-driver Outback, back to clean.</figcaption></figure>
          <figure>{pic("work-gloss", [640, 960], "(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw", "Close-up of deep red paint with a mirror-like ceramic coated finish", "h-auto w-full", 960, 720)}<figcaption class="mt-2 text-sm text-slate">Red paint, mirror finish.</figcaption></figure>
        </div>
        <div class="mt-12 grid gap-6 md:grid-cols-[1fr_1fr_1fr] md:items-center">
          <div>
            <h3 class="h3">Headlights, before and after</h3>
            <p class="mt-3 text-slate">Cloudy lenses are a safety problem at night and an easy fix in the shop. Wet-sanded, polished, and sealed so they stay clear.</p>
          </div>
          <figure>{pic("headlight-before", [640, 960], "(min-width: 768px) 33vw, 100vw", "Toyota Tacoma headlight, yellowed and hazy, masked with tape before restoration", "h-auto w-full", 960, 960)}</figure>
          <figure>{pic("headlight-after", [640, 960], "(min-width: 768px) 33vw, 100vw", "The same Toyota Tacoma headlight, clear and glossy after restoration", "h-auto w-full", 960, 960)}</figure>
        </div>
      </div>
    </section>

    <section class="section bg-glass" aria-labelledby="local-title">
      <div class="wrap">
        <h2 id="local-title" class="h2 max-w-2xl">What the Grand Valley does to a car</h2>
        <div class="mt-10 grid gap-8 md:grid-cols-3">
          <div>
            <h3 class="h3">Sun at 4,600 feet</h3>
            <p class="mt-3 text-slate">Thinner air, stronger UV. It fades paint, cooks dashboards, and turns a parked car into an oven. Ceramic film cuts the heat and blocks UV; a coating keeps the paint from chalking.</p>
          </div>
          <div>
            <h3 class="h3">Red dust</h3>
            <p class="mt-3 text-slate">It gets past door seals and into vents, seams, and carpet. We blow it out with compressed air and extract it instead of vacuuming the top layer.</p>
          </div>
          <div>
            <h3 class="h3">Winter mag chloride</h3>
            <p class="mt-3 text-slate">The deicer on I-70 and the Monument road clings to paint and wheels and holds moisture against metal. We dissolve it off instead of rinsing over it.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section bg-white" aria-labelledby="find-title">
      <div class="wrap grid gap-10 md:grid-cols-2 md:items-center">
        <div>{pic("shop-front", [640, 960, 1280], "(min-width: 768px) 50vw, 100vw", "The High Altitude Auto Spa shop: blue building with a HAAS sign over the door at 2912 Hill Ave", "h-auto w-full", 1280, 853)}</div>
        <div>
          <h2 id="find-title" class="h2">Hill Ave, just off 29 Road</h2>
          <p class="lede mt-3">Drop-off is easy from anywhere in the valley: {", ".join(S['towns'][:-1])}, or {S['towns'][-1]}.</p>
          <address class="mt-6 text-lg not-italic"><strong>{S['name']}</strong><br>{S['street']}<br>{S['city']}, {S['state']} {S['zip']}</address>
          <p class="mt-3 flex items-center gap-2 text-slate">{ctx['ICON_CLOCK']} {S['hours']}</p>
          <p class="mt-3"><a href="tel:{S['phone_tel']}" class="inline-block py-2 text-lg font-semibold text-ink" data-call="find-us">{S['phone']}</a></p>
          <a href="{S['maps_url']}" class="btn btn-outline-dark mt-5" rel="noopener">{ctx['ICON_PIN']} Get directions</a>
        </div>
      </div>
    </section>

    {ctx['cta_band']("")}
"""
    return dict(path="index.html",
                title="Window Tinting & Auto Detailing in Grand Junction, CO | High Altitude Auto Spa",
                desc=f"Ceramic window tint, interior and exterior detailing, paint correction, and Nasiol ceramic coating at 2912 Hill Ave, Grand Junction. 5.0 stars on Google. Call {S['phone']}.",
                body=body,
                extra_head='<link rel="preload" as="image" type="image/avif" imagesrcset="assets/img/hero-shop-wide-640.avif 640w, assets/img/hero-shop-wide-960.avif 960w" imagesizes="100vw" media="(max-width: 767px)">'
                           '<link rel="preload" as="image" type="image/avif" imagesrcset="assets/img/hero-shop-640.avif 640w, assets/img/hero-shop-960.avif 960w, assets/img/hero-shop-1280.avif 1280w" imagesizes="(min-width: 1024px) 50vw, 42vw" media="(min-width: 768px)">')


def service_shell(ctx, slug, h1, lede, included, why_title, why, extra="", shade=False):
    S, call = ctx["SITE"], ctx["call_btn"]
    label = next(l for s, l, _ in ctx["SERVICES"] if s == slug)
    items = "".join(f"<li>{i}</li>" for i in included)
    shade_html = f'<section class="section bg-glass" aria-labelledby="shade-title"><div class="wrap">{shade_picker(ctx, prefix="../")}</div></section>' if shade else ""
    body = f"""
    <section class="on-dark relative bg-black text-white">
      <div class="wrap pt-8 pb-10 md:pt-14 md:pb-14">
        <nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="../">Home</a></li><li><a href="../#services">Services</a></li><li aria-current="page">{label}</li></ol></nav>
        <h1 class="h1 mt-4 max-w-3xl">{h1}</h1>
        <p class="lede mt-5 max-w-2xl">{lede}</p>
        <p class="mt-5 text-fog">Priced by vehicle size and condition. Call for a number.</p>
        <div class="mt-8 flex flex-col gap-3 sm:flex-row">
          {call("hero", prefix="../")}
          <a href="../contact.html#quote" class="btn btn-outline-light">Get a quote</a>
        </div>
      </div>
      <div class="ridge"></div>
    </section>

    <section class="section" aria-labelledby="included-title">
      <div class="wrap grid gap-12 lg:grid-cols-5">
        <div class="lg:col-span-3">
          <h2 id="included-title" class="h2">What's included</h2>
          <ul class="check-list mt-8 text-lg">{items}</ul>
        </div>
        <aside class="lg:col-span-2 border-t-4 border-black bg-white p-6" aria-labelledby="why-title">
          <h2 id="why-title" class="h3">{why_title}</h2>
          {why}
        </aside>
      </div>
    </section>
    {shade_html}
    {extra}
    {ctx['cta_band']("../")}
"""
    return body


def window_tinting(ctx):
    S = ctx["SITE"]
    extra = f"""
    <section class="section bg-white" aria-labelledby="film-title">
      <div class="wrap grid gap-10 md:grid-cols-2">
        <div>
          <h2 id="film-title" class="h2">Ceramic film, not dyed film</h2>
          <p class="mt-4 text-lg text-slate">Cheap dyed tint turns purple and bubbles after a couple of Grand Junction summers. Ceramic film holds its color, rejects far more heat at the same shade, and doesn't interfere with phone or GPS signal. It costs more up front and it's the only kind we put on.</p>
        </div>
        <div>
          <h2 class="h2">Windshields too</h2>
          <p class="mt-4 text-lg text-slate">A light ceramic film on the windshield (50% or 70%) is nearly invisible and takes the sting out of a west-facing commute on I-70B. We'll check what's allowed on your vehicle first.</p>
        </div>
      </div>
    </section>"""
    body = service_shell(ctx, "window-tinting",
        "Window tinting in Grand Junction",
        "Ceramic window film, computer-cut to your vehicle and laid in the shop, out of the dust. Cooler cabin, less glare, 99% of UV blocked, and a cleaner look.",
        ["Film pattern cut by machine for your exact year, make, and model",
         "Ceramic film in your choice of shade, with the legal limits explained up front",
         "Old or failing tint stripped and glass cleaned, if you're replacing film",
         "Installed indoors in a clean bay so nothing gets trapped under the film",
         "Edges shrunk and tucked, no gaps, no light lines",
         "Care instructions: leave the windows up a few days while it cures"],
        "Why tint here",
        "<p class='mt-3 text-slate'>Grand Junction gets about 300 sunny days a year at 4,600 feet. A tinted car sits cooler in the lot, the dash and seats last longer, and you're not squinting on the drive home. On an SUV with kids in the back, it's the cheapest comfort upgrade there is.</p>",
        extra=extra, shade=True)
    return dict(path="services/window-tinting.html", current="services/window-tinting.html",
                title="Ceramic Window Tinting | Grand Junction, CO | High Altitude Auto Spa",
                desc=f"Ceramic window tint for cars, trucks, and SUVs in Grand Junction, CO. Computer-cut film, installed in the shop, legal shades explained. Call {S['phone']}.",
                body=body)


def interior(ctx):
    S = ctx["SITE"]
    body = service_shell(ctx, "interior-detailing",
        "Interior detailing in Grand Junction",
        "Everything you touch, see, or breathe inside the car: vents, seams, carpet, seats, headliner, and glass. Dust, pet hair, spills, and smells, gone.",
        ["Compressed-air purge of vents, seams, and tracks before any vacuuming",
         "Thorough vacuum including under seats and in the trunk or cargo area",
         "Hot-water extraction on carpet and cloth seats; leather cleaned and conditioned",
         "Dash, console, doors, and trim cleaned and dressed with a matte UV protectant",
         "Interior glass streak-free, including the inside of the windshield",
         "Odor treatment available for smoke, pets, and spills"],
        "Why it matters here",
        "<p class='mt-3 text-slate'>Red desert dust gets past every seal and settles into seams and carpet fibers. Vacuuming takes the top layer; air and extraction take the rest. And the same sun that fades paint dries out leather and cracks dashboards, so we finish with UV protection, not shine.</p>")
    return dict(path="services/interior-detailing.html", current="services/interior-detailing.html",
                title="Interior Detailing | Grand Junction, CO | High Altitude Auto Spa",
                desc=f"Deep interior detailing in Grand Junction, CO: extraction, leather, odor removal, and UV protection. Call {S['phone']} for a quote.",
                body=body)


def exterior(ctx):
    S = ctx["SITE"]
    body = service_shell(ctx, "exterior-detailing",
        "Exterior detailing in Grand Junction",
        "A proper hand wash, the contamination you can feel but can't see lifted out of the paint, and protection on paint, wheels, and glass.",
        ["Pre-rinse and foam to lift grit before anything touches the paint",
         "Two-bucket hand wash with clean mitts, never a brush",
         "Iron remover and clay bar to pull embedded brake dust, sap, and overspray",
         "Wheels, wheel wells, and tires cleaned and dressed",
         "Mag chloride dissolved off the lower panels and wheels in winter",
         "Paint sealant or spray ceramic for months of protection and easy washing"],
        "Why it matters here",
        "<p class='mt-3 text-slate'>The deicer on I-70 and the Monument road clings all winter and holds moisture against metal. In summer it's bugs, sap, and dust baked on by the sun. A detailed and sealed car sheds all of it at the next wash instead of grinding it in.</p>")
    return dict(path="services/exterior-detailing.html", current="services/exterior-detailing.html",
                title="Exterior Detailing | Grand Junction, CO | High Altitude Auto Spa",
                desc=f"Hand wash, decontamination, and paint protection in Grand Junction, CO. Call {S['phone']} for a quote.",
                body=body)


def ceramic(ctx):
    S = ctx["SITE"]
    extra = """
    <section class="section bg-white" aria-labelledby="nasiol-title">
      <div class="wrap grid gap-10 md:grid-cols-2 md:items-center">
        <div>
          <h2 id="nasiol-title" class="h2">Certified Nasiol installer</h2>
          <p class="mt-4 text-lg text-slate">Ryan is a Nasiol Pro Club certified installer, which means the coatings we apply are the real product, prepped and cured the way the manufacturer specifies, and backed by them. Ask to see the certificate; it's on the wall.</p>
        </div>
        <div class="border-t-4 border-black bg-paper p-6">
          <h3 class="h3">What a coating is</h3>
          <p class="mt-3 text-slate">A liquid nano-ceramic that bonds to the clear coat and hardens into a glass-like layer. Harder than wax, far longer lasting than a sealant. Water and dirt slide off, UV is blocked, and the gloss stays.</p>
        </div>
      </div>
    </section>"""
    body = service_shell(ctx, "ceramic-coating",
        "Ceramic coating in Grand Junction",
        "A hard, slick layer bonded to your paint: deeper gloss, easier washing, and a shield against UV, mag chloride, and bug and bird etching. Applied by a Nasiol-certified installer.",
        ["Full wash and decontamination",
         "Paint polished or corrected so the coating locks in a clean finish, not swirl marks",
         "Panel wipe to strip oils so the coating bonds to the clear coat",
         "Nasiol coating applied panel by panel, indoors, under good light",
         "Cure time in the shop, out of dust and weather",
         "Aftercare: how to wash it so it lasts, and a maintenance plan if you want one"],
        "Why it matters here",
        "<p class='mt-3 text-slate'>Coatings earn their keep in the Grand Valley: UV that fades paint, mag chloride that clings all winter, and desert dust that rinses off a slick surface instead of grinding in. A coated car is also faster to wash, which matters when the dust is back the next day.</p>",
        extra=extra)
    return dict(path="services/ceramic-coating.html", current="services/ceramic-coating.html",
                title="Ceramic Coating by a Nasiol Certified Installer | Grand Junction, CO",
                desc=f"Nasiol ceramic coating in Grand Junction, CO, applied by a certified installer. Gloss, UV protection, and easy washing for years. Call {S['phone']}.",
                body=body)


def correction(ctx):
    S = ctx["SITE"]
    body = service_shell(ctx, "paint-correction",
        "Paint correction in Grand Junction",
        "Machine polishing that removes swirl marks, light scratches, water spots, and sun-faded haze, so the paint looks the way it did on the lot.",
        ["Wash, decontamination, and paint-depth check before any polishing",
         "Test spot to choose the pad and compound your paint needs",
         "One-step polish for swirls and haze; two-step compound and polish for deeper defects",
         "Trim and edges taped so nothing gets burned",
         "Panel wipe and inspection under LED lights",
         "Finished with sealant, or a ceramic coating to lock it in"],
        "Why it matters here",
        "<p class='mt-3 text-slate'>Automatic washes and dusty towels leave fine scratches that scatter light and make dark paint look grey. Add strong sun and the clear coat hazes. Correction removes a few microns of clear coat to level those defects, which is why we check depth first and always finish with protection.</p>")
    return dict(path="services/paint-correction.html", current="services/paint-correction.html",
                title="Paint Correction | Grand Junction, CO | High Altitude Auto Spa",
                desc=f"Swirl and scratch removal by machine polishing in Grand Junction, CO. Call {S['phone']} for a quote.",
                body=body)


def about(ctx):
    S, pic = ctx["SITE"], ctx["picture"]
    body = f"""
    <section class="on-dark relative bg-black text-white">
      <div class="wrap pt-8 pb-10 md:pt-14 md:pb-14">
        <h1 class="h1 max-w-3xl">A one-bay shop on Hill Ave that does it right</h1>
        <p class="lede mt-5 max-w-2xl">High Altitude Auto Spa is owner-run by {S['owner']}. He's been tinting and detailing for more than five years, and he's the one who answers the phone, quotes the job, and does the work.</p>
      </div>
      <div class="ridge"></div>
    </section>

    <section class="section" aria-labelledby="story-title">
      <div class="wrap grid gap-10 md:grid-cols-2 md:items-center">
        <div>{pic("shop-front", [640, 960, 1280], "(min-width: 768px) 50vw, 100vw", "The High Altitude Auto Spa shop front with the HAAS sign over the door", "h-auto w-full", 1280, 853)}</div>
        <div>
          <h2 id="story-title" class="h2">How we work</h2>
          <ul class="mt-6 grid gap-4 text-lg">
            <li><strong>You get the price before we start</strong>, and it's the price you pay. No add-ons at pickup.</li>
            <li><strong>Work happens indoors.</strong> Tint and coatings need a clean, lit bay to go on right. A driveway isn't one.</li>
            <li><strong>Ceramic film and real ceramic coatings only.</strong> Ryan is a Nasiol Pro Club certified installer.</li>
            <li><strong>We'll tell you what you don't need.</strong> Half the cars that come in for a coating need a good correction more.</li>
          </ul>
        </div>
      </div>
    </section>

    {review_block(ctx)}

    <section class="section bg-glass" aria-labelledby="visit-title">
      <div class="wrap grid gap-10 md:grid-cols-2">
        <div>
          <h2 id="visit-title" class="h2">Visit</h2>
          <address class="mt-5 text-lg not-italic"><strong>{S['name']}</strong><br>{S['street']}<br>{S['city']}, {S['state']} {S['zip']}</address>
          <p class="mt-3 text-slate">{S['hours']}</p>
          <p class="mt-3"><a href="tel:{S['phone_tel']}" class="inline-block py-2 text-lg font-semibold text-ink" data-call="about">{S['phone']}</a></p>
          <a href="{S['maps_url']}" class="btn btn-outline-dark mt-5" rel="noopener">{ctx['ICON_PIN']} Get directions</a>
        </div>
        <div>
          <h2 class="h2">Follow the work</h2>
          <p class="mt-5 text-lg text-slate">Before-and-afters, tint jobs, and the occasional fleet of work vans go up on Instagram and Facebook most weeks.</p>
          <ul class="mt-4 space-y-0.5 text-lg [&_a]:inline-block [&_a]:py-1.5">
            <li><a href="{S['instagram']}" class="font-semibold text-ink underline hover:text-orange-deep" rel="noopener">Instagram {S['instagram_handle']}</a></li>
            <li><a href="{S['facebook']}" class="font-semibold text-ink underline hover:text-orange-deep" rel="noopener">Facebook</a></li>
          </ul>
        </div>
      </div>
    </section>

    {ctx['cta_band']("")}
"""
    return dict(path="about.html", current="about.html",
                title="About | High Altitude Auto Spa, Grand Junction",
                desc=f"Owner-run tint and detailing shop at 2912 Hill Ave, Grand Junction, CO. Ryan Clark, Nasiol certified installer, 5.0 stars on Google.",
                body=body)


def contact(ctx):
    S, call = ctx["SITE"], ctx["call_btn"]
    opts = "".join(f"<option>{l}</option>" for _, l, _ in ctx["SERVICES"]) + "<option>Full detail (inside and out)</option><option>Headlight restoration</option><option>Graphics or vinyl</option><option>Fleet or work vehicles</option><option>Not sure yet</option>"
    body = f"""
    <section class="on-dark relative bg-black text-white">
      <div class="wrap pt-8 pb-10 md:pt-14 md:pb-14">
        <h1 class="h1 max-w-3xl">Get a quote</h1>
        <p class="lede mt-5 max-w-2xl">Fastest is a call or text to <a href="tel:{S['phone_tel']}" class="inline-block py-1 font-semibold text-white underline" data-call="contact-lede">{S['phone']}</a>. Or send the form and we'll get back to you with a price.</p>
      </div>
      <div class="ridge"></div>
    </section>

    <section class="section" aria-labelledby="quote-title">
      <div class="wrap grid gap-12 lg:grid-cols-5">
        <div class="lg:col-span-3">
          <h2 id="quote-title" class="h2">Tell us about the vehicle</h2>
          <form id="quote" class="mt-8 grid gap-5" action="https://formspree.io/f/{S['formspree_id']}" method="POST" data-quote-form>
            <div class="grid gap-5 sm:grid-cols-2">
              <div class="grid gap-1.5"><label class="label" for="name">Name</label><input class="input" id="name" name="name" type="text" autocomplete="name" required></div>
              <div class="grid gap-1.5"><label class="label" for="phone">Phone</label><input class="input" id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
            </div>
            <div class="grid gap-1.5"><label class="label" for="email">Email <span class="font-normal text-slate">(optional)</span></label><input class="input" id="email" name="email" type="email" autocomplete="email"></div>
            <div class="grid gap-1.5"><label class="label" for="vehicle">Vehicle</label><input class="input" id="vehicle" name="vehicle" type="text" aria-describedby="vehicle-hint" required><p id="vehicle-hint" class="text-sm text-slate">Year, make, and model, e.g. 2019 Toyota Tacoma</p></div>
            <div class="grid gap-1.5"><label class="label" for="service">Service</label><select class="input" id="service" name="service" required><option value="">Choose one</option>{opts}</select></div>
            <div class="grid gap-1.5"><label class="label" for="message">Anything we should know? <span class="font-normal text-slate">(optional)</span></label><textarea class="input" id="message" name="message" rows="4" aria-describedby="message-hint"></textarea><p id="message-hint" class="text-sm text-slate">Tint shade you're thinking of, pet hair, scratches, odors, or when you need it back.</p></div>
            <div class="hidden" aria-hidden="true"><label>Leave this empty <input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
            <input type="hidden" name="_subject" value="New quote request from the High Altitude Auto Spa website">
            <button type="submit" class="btn btn-call w-full sm:w-auto sm:justify-self-start">Send quote request</button>
            <p class="text-sm text-slate">We only use your details to reply to this request. See our <a href="privacy.html" class="inline-block py-1 underline">privacy policy</a>.</p>
            <p class="border-l-4 border-l-orange bg-white p-4 font-semibold" role="alert" data-form-error hidden>Your request didn't go through. Please try again, or call <a href="tel:{S['phone_tel']}" class="underline" data-call="form-error">{S['phone']}</a>.</p>
          </form>
          <div class="mt-8 border-l-4 border-l-orange bg-white p-6" tabindex="-1" data-form-success hidden>
            <h3 class="h3">Got it. We'll be in touch.</h3>
            <p class="mt-3 text-lg text-slate">Expect a call or text with a quote. If you need an answer today, call <a href="tel:{S['phone_tel']}" class="font-semibold underline" data-call="form-success">{S['phone']}</a>.</p>
          </div>
        </div>
        <aside class="space-y-5 lg:col-span-2">
          <div class="border-t-4 border-black bg-white p-6">
            <h2 class="h3">The shop</h2>
            <address class="mt-3 text-slate not-italic">{S['name']}<br>{S['street']}<br>{S['city']}, {S['state']} {S['zip']}</address>
            <p class="mt-3 flex items-start gap-2 text-slate">{ctx['ICON_CLOCK']} <span>{S['hours']}</span></p>
            <p class="mt-3"><a href="tel:{S['phone_tel']}" class="inline-block py-2 text-lg font-semibold text-ink" data-call="contact">{S['phone']}</a></p>
            <a href="{S['maps_url']}" class="btn btn-outline-dark mt-5" rel="noopener">{ctx['ICON_PIN']} Get directions</a>
          </div>
          <div class="border-t-4 border-black bg-white p-6">
            <h2 class="h3">Email or DM</h2>
            <ul class="mt-3 space-y-0.5 [&_a]:inline-block [&_a]:py-1.5">
              <li><a href="mailto:{S['email']}" class="font-semibold text-ink underline">{S['email']}</a></li>
              <li><a href="{S['instagram']}" class="font-semibold text-ink underline" rel="noopener">Instagram {S['instagram_handle']}</a></li>
              <li><a href="{S['facebook']}" class="font-semibold text-ink underline" rel="noopener">Facebook Messenger</a></li>
            </ul>
          </div>
        </aside>
      </div>
    </section>
"""
    return dict(path="contact.html", current="contact.html",
                title="Get a Quote | High Altitude Auto Spa, Grand Junction",
                desc=f"Call {S['phone']} or send a quote request for window tint, detailing, or ceramic coating at 2912 Hill Ave, Grand Junction, CO.",
                body=body)


def privacy(ctx):
    S = ctx["SITE"]
    body = f"""
    <section class="on-dark relative bg-black text-white">
      <div class="wrap pt-8 pb-10 md:pt-14 md:pb-14"><h1 class="h1">Privacy</h1><p class="lede mt-4">Short version: we only use what you send us to reply to you.</p></div>
      <div class="ridge"></div>
    </section>
    <section class="section"><div class="wrap max-w-3xl space-y-6 text-lg">
      <p><strong>Quote form.</strong> When you send a quote request, your name, phone, email, vehicle, and message go to Formspree (our form service) and then to our inbox. We use them to reply to your request and nothing else. We don't sell or share them.</p>
      <p><strong>Phone calls and texts.</strong> If you call or text {S['phone']}, we keep the conversation so we can follow up on your job.</p>
      <p><strong>Analytics.</strong> We may use Google Analytics to see which pages get visited and how many people tap the phone number. It doesn't tell us who you are.</p>
      <p><strong>Cookies.</strong> This site sets no cookies of its own. Analytics, if enabled, sets its own; your browser's settings control it.</p>
      <p><strong>Questions.</strong> Email <a href="mailto:{S['email']}" class="font-semibold underline">{S['email']}</a>.</p>
    </div></section>
"""
    return dict(path="privacy.html", current="privacy.html",
                title="Privacy | High Altitude Auto Spa", desc="How High Altitude Auto Spa uses the information you send through this site.", body=body)


def not_found(ctx):
    S = ctx["SITE"]
    body = f"""
    <section class="on-dark relative bg-black text-white">
      <div class="wrap pt-8 pb-10 md:pt-14 md:pb-14"><h1 class="h1">That page isn't here</h1><p class="lede mt-4">The link may be old. Everything we do is on the home page.</p>
      <div class="mt-8 flex flex-col gap-3 sm:flex-row"><a href="./" class="btn btn-light">Go to the home page</a>{ctx['call_btn']("404")}</div></div>
      <div class="ridge"></div>
    </section>
"""
    return dict(path="404.html", title="Page not found | High Altitude Auto Spa", desc="Page not found.", body=body)


def pages(ctx):
    return [home(ctx), window_tinting(ctx), interior(ctx), exterior(ctx), ceramic(ctx), correction(ctx),
            about(ctx), contact(ctx), privacy(ctx), not_found(ctx)]
