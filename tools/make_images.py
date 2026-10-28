"""Generates all self-made images for the Happy Paws course project."""
import math
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..")
IMG = os.path.join(ROOT, "img")
os.makedirs(IMG, exist_ok=True)

# palette
CREAM = (253, 246, 236)
ORANGE = (242, 153, 74)
BROWN = (74, 44, 26)
GREEN = (107, 163, 104)
SKY = (174, 217, 224)
SUN = (247, 201, 72)
WHITE = (255, 255, 255)
DARKGREEN = (86, 130, 84)


def font(size):
    return ImageFont.load_default(size=size)


def sky_gradient(draw, w, h, top, bottom):
    for y in range(h):
        t = y / h
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(0, y), (w, y)], fill=c)


def cloud(draw, x, y, s=20, c=WHITE):
    draw.ellipse([x, y, x + 2 * s, y + s], fill=c)
    draw.ellipse([x + s // 1.4, y - s // 2, x + 2.4 * s, y + s // 1.6], fill=c)
    draw.ellipse([x - s // 1.6, y + s // 3, x + s, y + s], fill=c)


def tree(draw, x, base, s=40):
    draw.rectangle([x - s // 6, base - s, x + s // 6, base], fill=BROWN)
    draw.ellipse([x - s, base - 2.4 * s, x + s, base - 0.4 * s], fill=GREEN)
    draw.ellipse([x - 0.7 * s, base - 2.9 * s, x + 0.7 * s, base - 1.4 * s], fill=DARKGREEN)


def dog(draw, x, ground, step=0, scale=1.0, color=(120, 81, 45)):
    """Side-view dog walking. x = front paw position-ish, ground = y of paws."""
    s = scale
    body_top = ground - 46 * s
    # legs (alternate)
    for i, (lx, phase) in enumerate([(x - 26 * s, 0), (x - 26 * s, 1), (x + 20 * s, 1), (x + 20 * s, 0)]):
        off = 8 * s if (step + phase) % 2 == 0 else -8 * s
        draw.line([(lx, body_top + 18 * s), (lx + off, ground)], fill=color, width=max(2, int(4 * s)))
    # tail
    draw.line([(x + 34 * s, body_top + 6 * s), (x + 52 * s, body_top - 14 * s)], fill=color, width=max(2, int(5 * s)))
    # body
    draw.ellipse([x - 34 * s, body_top, x + 36 * s, body_top + 22 * s], fill=color)
    # head
    hx = x + 40 * s
    hy = body_top - 6 * s
    draw.ellipse([hx, hy, hx + 26 * s, hy + 22 * s], fill=color)
    # ear
    draw.polygon([(hx + 6 * s, hy + 2 * s), (hx + 14 * s, hy - 10 * s), (hx + 18 * s, hy + 6 * s)], fill=BROWN)
    # eye + snout
    draw.ellipse([hx + 16 * s, hy + 7 * s, hx + 20 * s, hy + 11 * s], fill=WHITE)
    draw.ellipse([hx + 22 * s, hy + 10 * s, hx + 28 * s, hy + 14 * s], fill=color)
    return (hx + 13 * s, hy + 14 * s)  # collar point


def walker(draw, x, ground, step=0, scale=1.0):
    """Stick person with leash arm to the right."""
    s = scale
    head_r = 11 * s
    hy = ground - 92 * s
    draw.ellipse([x - head_r, hy, x + head_r, hy + 2 * head_r], fill=ORANGE, outline=BROWN, width=max(2, int(2 * s)))
    neck = hy + 2 * head_r
    hip = ground - 42 * s
    draw.line([(x, neck), (x, hip)], fill=BROWN, width=max(3, int(5 * s)))
    # legs
    for phase in (0, 1):
        off = 10 * s if (step + phase) % 2 == 0 else -10 * s
        draw.line([(x, hip), (x + off, ground)], fill=BROWN, width=max(3, int(5 * s)))
    # arms: back arm swing, front arm holds leash forward
    sh = neck + 10 * s
    draw.line([(x, sh), (x - 14 * s, sh + 22 * s)], fill=BROWN, width=max(2, int(4 * s)))
    draw.line([(x, sh), (x + 18 * s, sh + 16 * s)], fill=BROWN, width=max(2, int(4 * s)))
    return (x + 18 * s, sh + 16 * s)  # hand


def leash(draw, hand, collar):
    draw.line([hand, collar], fill=(60, 60, 60), width=2)


def park_scene(w, h, step=0, wx=None, sky_top=(196, 228, 235), sky_bot=(232, 244, 240),
               ground=GREEN, sun_x=0.82, clouds=(0.15, 0.45), extra_dog=False):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    gy = int(h * 0.72)
    sky_gradient(d, w, gy, sky_top, sky_bot)
    # sun
    sx, sy = int(w * sun_x), int(h * 0.16)
    d.ellipse([sx - 34, sy - 34, sx + 34, sy + 34], fill=SUN)
    # clouds
    for cf in clouds:
        cloud(d, int(w * cf), int(h * 0.12), s=max(14, w // 45))
    # ground
    d.rectangle([0, gy, w, h], fill=ground)
    d.line([(0, gy), (w, gy)], fill=DARKGREEN, width=5)
    # path
    d.polygon([(int(w * 0.1), h), (int(w * 0.35), gy), (int(w * 0.62), gy), (w, h)], fill=(226, 211, 189))
    # trees
    for tf in (0.06, 0.9, 0.97):
        tree(d, int(w * tf), gy + 8, s=max(28, w // 26))
    # walkers
    if wx is None:
        wx = int(w * 0.42)
    hand = walker(d, wx, gy - 4, step)
    collar = dog(d, wx + int(w * 0.09), gy - 4, step + 1, scale=max(0.8, w / 900))
    leash(d, hand, collar)
    if extra_dog:
        dog(d, wx - int(w * 0.16), gy + 26, step, scale=max(0.7, w / 1100), color=(94, 60, 32))
    return img


def paw_icon(size, color=ORANGE, alpha=255):
    """Paw print with transparent background."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size
    c = color + (alpha,)
    # main pad
    d.ellipse([s * 0.24, s * 0.44, s * 0.76, s * 0.88], fill=c)
    # toes
    d.ellipse([s * 0.10, s * 0.22, s * 0.32, s * 0.46], fill=c)
    d.ellipse([s * 0.36, s * 0.10, s * 0.58, s * 0.36], fill=c)
    d.ellipse([s * 0.63, s * 0.12, s * 0.84, s * 0.38], fill=c)
    d.ellipse([s * 0.80, s * 0.32, s * 0.97, s * 0.56], fill=c)
    return img


# ---------- logo with transparent background ----------
logo = Image.new("RGBA", (520, 160), (0, 0, 0, 0))
ld = ImageDraw.Draw(logo)
paw = paw_icon(120)
logo.paste(paw, (10, 20), paw)
ld.text((150, 34), "Happy Paws", font=font(64), fill=BROWN)
ld.text((153, 100), "Vaasa dog walking service", font=font(26), fill=(120, 81, 45))
logo.save(os.path.join(IMG, "logo.png"))

# small paw icon (used as link button)
paw_icon(96).save(os.path.join(IMG, "paw.png"))
paw_icon(32).save(os.path.join(IMG, "favicon.png"))

# ---------- hero: same scene cropped 3 ways ----------
big = park_scene(1700, 1000, step=1, wx=640, extra_dog=True)
# desktop 16:9
big.crop((0, 0, 1600, 900)).resize((1200, 675)).save(os.path.join(IMG, "hero-lg.jpg"), quality=82)
# tablet 4:3 (crop center)
big.crop((250, 100, 1050, 700)).resize((800, 600)).save(os.path.join(IMG, "hero-md.jpg"), quality=82)
# phone 9:16 portrait (tight crop around walker+dog)
big.crop((480, 90, 894, 826)).resize((480, 854)).save(os.path.join(IMG, "hero-sm.jpg"), quality=82)

# ---------- gallery scenes (800x600 shown, thumbs 160x120) ----------
variants = [
    dict(sky_top=(176, 216, 235), ground=GREEN, sun_x=0.8, clouds=(0.1, 0.5), extra_dog=False, step=0),
    dict(sky_top=(245, 218, 180), sky_bot=(250, 236, 214), ground=(160, 158, 105), sun_x=0.2, clouds=(0.55,), extra_dog=True, step=1),   # sunset
    dict(sky_top=(214, 226, 240), sky_bot=(238, 244, 248), ground=(235, 240, 244), sun_x=0.9, clouds=(0.2, 0.6, 0.75), extra_dog=False, step=1),  # winter
    dict(sky_top=(180, 224, 200), sky_bot=(224, 244, 230), ground=(120, 168, 120), sun_x=0.5, clouds=(), extra_dog=True, step=0),  # lush
    dict(sky_top=(168, 205, 235), sky_bot=(210, 236, 240), ground=(150, 130, 96), sun_x=0.15, clouds=(0.35,), extra_dog=False, step=0),  # beach-ish
    dict(sky_top=(120, 140, 175), sky_bot=(170, 190, 215), ground=(100, 110, 90), sun_x=0.88, clouds=(0.2, 0.6), extra_dog=True, step=1),  # stormy
]
for i, v in enumerate(variants, 1):
    img = park_scene(800, 600, **v)
    img.save(os.path.join(IMG, f"g{i}.jpg"), quality=82)
    img.resize((160, 120)).save(os.path.join(IMG, f"t{i}.jpg"), quality=80)

# ---------- featured image for index ----------
park_scene(800, 500, step=1, wx=330, extra_dog=True, sun_x=0.15).save(os.path.join(IMG, "week.jpg"), quality=82)

# ---------- about portrait ----------
ap = Image.new("RGB", (500, 620), CREAM)
ad = ImageDraw.Draw(ap)
sky_gradient(ad, 500, 620, (196, 228, 235), (240, 246, 242))
gy = 470
ad.rectangle([0, gy, 500, 620], fill=GREEN)
hand = walker(ad, 200, gy, step=1, scale=1.15)
c1 = dog(ad, 300, gy, step=0, scale=1.0)
leash(ad, hand, c1)
c2 = dog(ad, 120, gy, step=2, scale=0.8, color=(94, 60, 32))
ad.text((60, 30), "Anna & the pack", font=font(34), fill=BROWN)
ap.save(os.path.join(IMG, "about.jpg"), quality=85)

# ---------- wireframes ----------
def wireframe(path, title, boxes_main):
    img = Image.new("RGB", (640, 760), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, 634, 754], outline=BROWN, width=3)
    d.text((20, 16), title, font=font(24), fill=BROWN)
    y = 60

    def box(x, y, w, h, label, fill=(238, 230, 218)):
        d.rectangle([x, y, x + w, y + h], fill=fill, outline=(90, 90, 90), width=2)
        d.text((x + 8, y + h // 2 - 10), label, font=font(16), fill=(50, 50, 50))

    def arrow(x1, y1, x2, y2):
        d.line([(x1, y1), (x2, y2)], fill=(200, 60, 60), width=3)
        ang = math.atan2(y2 - y1, x2 - x1)
        for da in (2.6, -2.6):
            d.line([(x2, y2), (x2 + 14 * math.cos(ang + da), y2 + 14 * math.sin(ang + da))], fill=(200, 60, 60), width=3)

    box(20, y, 600, 50, "HEADER: logo (link to Home) + company name")
    y += 60
    box(20, y, 600, 40, "NAV: Home | Services | Gallery | About | Report")
    y += 55
    for label, h in boxes_main:
        box(20, y, 600, h, label, fill=(250, 245, 238))
        y += h + 12
    box(20, 690, 600, 55, "FOOTER: contact + hours + sitemap links", fill=(238, 230, 218))
    arrow(320, 640, 320, 690)  # flow arrow into footer
    img.save(path)

wireframe(os.path.join(IMG, "wireframe-home.png"), "Wireframe: Home page", [
    ("HERO: <picture> 16:9 / 4:3 / 9:16 + H1 welcome", 130),
    ("WHY US: 3 cards in a grid (grows 1->3 cols)", 110),
    ("FEATURED: walk of the week, image + text", 150),
    ("TEASER: link to Services + animated paw", 90),
])
wireframe(os.path.join(IMG, "wireframe-sub.png"), "Wireframe: sub page (Services)", [
    ("H1 + intro text", 80),
    ("CARDS: flex, wrap on mobile", 160),
    ("PRICE TABLE + SVG chart", 170),
    ("CTA: link to About/Contact", 70),
])

# ---------- palette ----------
pal = Image.new("RGB", (700, 240), WHITE)
pd = ImageDraw.Draw(pal)
swatches = [(ORANGE, "#F2994A primary"), (BROWN, "#4A2C1A text"), (GREEN, "#6BA368 nature"),
            (CREAM, "#FDF6EC background"), ((174, 217, 224), "#AED9E0 sky")]
for i, (c, label) in enumerate(swatches):
    x = 20 + (i % 3) * 230
    y = 20 + (i // 3) * 110
    pd.rectangle([x, y, x + 200, y + 70], fill=c, outline=(120, 120, 120))
    pd.text((x, y + 74), label, font=font(18), fill=(40, 40, 40))
pal.save(os.path.join(IMG, "palette.png"))

# ---------- font sample ----------
fs = Image.new("RGB", (700, 260), WHITE)
fd = ImageDraw.Draw(fs)
fd.text((20, 20), "Font choice", font=font(28), fill=BROWN)
fd.text((20, 70), "Fredoka (headings)", font=font(24), fill=(40, 40, 40))
fd.text((20, 104), "Aa Bb Cc 0123 - friendly, rounded, playful", font=font(22), fill=(90, 90, 90))
fd.text((20, 150), "Nunito (body text)", font=font(24), fill=(40, 40, 40))
fd.text((20, 184), "Aa Bb Cc 0123 - soft, readable, modern", font=font(22), fill=(90, 90, 90))
fd.text((20, 228), "Both from Google Fonts (Open Font License)", font=font(18), fill=(130, 130, 130))
fs.save(os.path.join(IMG, "fonts.png"))

print("images done:", sorted(os.listdir(IMG)))
