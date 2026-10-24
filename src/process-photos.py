"""Turn the Facebook pulls into site assets. Run from haas-src; writes into the repo's assets/img."""
from PIL import Image, ImageOps, ImageFilter
import os, shutil

SRC = "/path/to/originals"  # folder with logo.jpg, cover.jpg, p1-clean.jpg, p2.jpg ... from the Oct 2026 Facebook pulls
OUT = "/home/claude/highaltitudeautospa/assets/img"
os.makedirs(OUT, exist_ok=True)

# ---------- Logo: white art on #222 -> white art on transparent ----------
logo = Image.open(f"{SRC}/logo.jpg").convert("L")
# Crop to the art (ridge top ~y=215, tagline bottom ~y=650, x 140..860)
art = logo.crop((130, 200, 870, 665))
# luminance -> alpha, with a little contrast so JPEG noise in the black goes fully transparent
alpha = art.point(lambda v: 0 if v < 60 else (255 if v > 200 else int((v - 60) * 255 / 140)))
w, h = art.size
white = Image.new("RGBA", (w, h), (255, 255, 255, 0))
white.putalpha(alpha)
white.save(f"{OUT}/logo-mark.png", optimize=True)           # white mark, for dark backgrounds
black = Image.new("RGBA", (w, h), (34, 34, 34, 0)); black.putalpha(alpha)
black.save(f"{OUT}/logo-mark-dark.png", optimize=True)      # dark mark, for light backgrounds
print("mark", w, h)

# Ridge only (the sketched mountains): rows above the HAAS word
ridge = logo.crop((130, 200, 870, 372))
ra = ridge.point(lambda v: 0 if v < 60 else (255 if v > 200 else int((v - 60) * 255 / 140)))
rw, rh = ridge.size
rimg = Image.new("RGBA", (rw, rh), (255, 255, 255, 0)); rimg.putalpha(ra)
rimg.save(f"{OUT}/ridge.png", optimize=True)
print("ridge", rw, rh)

# ---------- Favicons / touch icon / OG ----------
sq = Image.open(f"{SRC}/logo.jpg").convert("RGB").crop((110, 180, 850, 690))  # tight on the art
side = max(sq.size)
canvas = Image.new("RGB", (side, side), (34, 34, 34)); canvas.paste(sq, ((side - sq.width) // 2, (side - sq.height) // 2))
canvas.resize((180, 180), Image.LANCZOS).save(f"{OUT}/apple-touch-icon.png", optimize=True)
canvas.resize((64, 64), Image.LANCZOS).save("/home/claude/highaltitudeautospa/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
# 512 PNG for a manifest-less modern icon link
canvas.resize((192, 192), Image.LANCZOS).save(f"{OUT}/icon-192.png", optimize=True)
if os.path.exists(f"{OUT}/favicon.svg"): os.remove(f"{OUT}/favicon.svg")

og = Image.new("RGB", (1200, 630), (34, 34, 34))
m = white.copy(); m.thumbnail((760, 400), Image.LANCZOS)
og.paste(m, ((1200 - m.width) // 2, 70), m)
og.save(f"{OUT}/og-image.jpg", quality=88, optimize=True)

# ---------- Photos ----------
def sets(name, im, widths, ratio=None, anchor=(0.5, 0.5), q=80):
    """Write name-{w}.avif/.webp/.jpg. ratio = w/h crop, anchor = focus point."""
    im = ImageOps.exif_transpose(im).convert("RGB")
    if ratio:
        W, H = im.size
        if W / H > ratio:   # too wide
            nw = int(H * ratio); x = int((W - nw) * anchor[0]); im = im.crop((x, 0, x + nw, H))
        else:
            nh = int(W / ratio); y = int((H - nh) * anchor[1]); im = im.crop((0, y, W, y + nh))
    for w in widths:
        if w > im.width: w = im.width
        r = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        r.save(f"{OUT}/{name}-{w}.jpg", quality=q, optimize=True, progressive=True)
        r.save(f"{OUT}/{name}-{w}.webp", quality=q - 2, method=6)
        r.save(f"{OUT}/{name}-{w}.avif", quality=max(40, q - 18), speed=4)
    print(name, im.size, [os.path.getsize(f"{OUT}/{name}-{w}.avif") // 1024 for w in widths if w <= im.width])
    return im.size

# Hero: 370Z in front of the shop. Portrait source; use 4:5 on desktop column, and a 4:3 crop for the mobile stack.
shop = Image.open(f"{SRC}/p1-clean.jpg")
sets("hero-shop", shop, [640, 960, 1280], ratio=4/5, anchor=(0.5, 0.55))
sets("hero-shop-wide", shop, [640, 960], ratio=4/3, anchor=(0.5, 0.62))
# Gallery
sets("work-rx7", Image.open(f"{SRC}/cover.jpg"), [640, 960], ratio=4/3, anchor=(0.45, 0.5))
sets("work-outback", Image.open(f"{SRC}/p4.jpg"), [640, 960], ratio=4/3, anchor=(0.5, 0.6))
sets("work-gloss", Image.open(f"{SRC}/p7.jpg"), [640, 960], ratio=4/3, anchor=(0.5, 0.4))
sets("headlight-after", Image.open(f"{SRC}/p2.jpg"), [640, 960], ratio=1, anchor=(0.5, 0.45))
sets("headlight-before", Image.open(f"{SRC}/p3.jpg"), [640, 960], ratio=1, anchor=(0.5, 0.45))
# About/contact: the shop front, landscape crop from the top of the photo (sign + building)
sets("shop-front", shop, [640, 960, 1280], ratio=3/2, anchor=(0.5, 0.25))
