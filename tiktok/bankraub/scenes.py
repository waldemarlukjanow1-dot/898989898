"""Flat-vector scene renderer for the 'Bankraub' TikTok (1080x1920, 9:16).

Every scene is drawn procedurally with Pillow so the storyboard preview and the
final video use exactly the same artwork. Coordinates are in 1080x1920 space;
drawing happens at SS-times resolution and is downscaled for anti-aliasing.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
SS = 2

FONT_DIR = "/usr/share/fonts/opentype/inter/"
MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-ExtraBold.ttf"

C = {
    "night": (24, 44, 47),
    "deep": (31, 59, 61),
    "teal": (47, 90, 91),
    "teal_l": (79, 125, 122),
    "sky": (111, 154, 148),
    "fog": (150, 178, 170),
    "white": (244, 241, 234),
    "ink": (18, 28, 28),
    "pink": (255, 61, 127),
    "gold": (242, 184, 75),
    "gold_d": (196, 132, 40),
    "brown": (138, 74, 47),
    "brown_d": (98, 52, 34),
    "red": (232, 51, 58),
    "blue": (60, 120, 255),
    "steel": (120, 140, 140),
    "steel_d": (78, 96, 97),
    "steel_l": (170, 186, 184),
    "cash": (130, 170, 120),
    "cash_d": (88, 128, 84),
    "jacket": (40, 46, 52),
    "mira": (96, 62, 130),
    "oskar": (150, 80, 45),
}


def font(size, weight="Black"):
    return ImageFont.truetype(f"{FONT_DIR}Inter-{weight}.otf", int(size))


def mono(size):
    return ImageFont.truetype(MONO, int(size))


class Canvas:
    """Thin wrapper that scales 1080x1920 coordinates by SS."""

    def __init__(self, bg):
        self.img = Image.new("RGB", (W * SS, H * SS), bg)
        self.d = ImageDraw.Draw(self.img, "RGBA")

    def s(self, v):
        return [x * SS for x in v] if isinstance(v, (list, tuple)) else v * SS

    def rect(self, box, fill, outline=None, width=0, r=0):
        box = self.s(box)
        if r:
            self.d.rounded_rectangle(box, r * SS, fill=fill, outline=outline, width=width * SS)
        else:
            self.d.rectangle(box, fill=fill, outline=outline, width=width * SS)

    def ellipse(self, box, fill, outline=None, width=0):
        self.d.ellipse(self.s(box), fill=fill, outline=outline, width=width * SS)

    def circle(self, cx, cy, r, fill, outline=None, width=0):
        self.ellipse((cx - r, cy - r, cx + r, cy + r), fill, outline, width)

    def poly(self, pts, fill, outline=None, width=0):
        pts = [(x * SS, y * SS) for x, y in pts]
        self.d.polygon(pts, fill=fill)
        if outline and width:
            self.d.line(pts + [pts[0]], fill=outline, width=width * SS, joint="curve")

    def line(self, pts, fill, width):
        self.d.line([(x * SS, y * SS) for x, y in pts], fill=fill, width=int(width * SS), joint="curve")

    def arc(self, box, a0, a1, fill, width):
        self.d.arc(self.s(box), a0, a1, fill=fill, width=width * SS)

    def text(self, xy, txt, f, fill, anchor="la"):
        f2 = ImageFont.truetype(f.path, f.size * SS)
        self.d.text((xy[0] * SS, xy[1] * SS), txt, font=f2, fill=fill, anchor=anchor)

    def glow(self, cx, cy, r, color, alpha=120):
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).ellipse(self.s((cx - r, cy - r, cx + r, cy + r)), fill=color + (alpha,))
        layer = layer.filter(ImageFilter.GaussianBlur(r * SS * 0.35))
        self.img.paste(layer, (0, 0), layer)
        self.d = ImageDraw.Draw(self.img, "RGBA")

    def overlay(self, color, alpha):
        layer = Image.new("RGBA", self.img.size, color + (alpha,))
        self.img.paste(layer, (0, 0), layer)
        self.d = ImageDraw.Draw(self.img, "RGBA")

    def final(self):
        return self.img.resize((W, H), Image.LANCZOS)


# ---------------------------------------------------------------- props

def gradient_sky(cv, top, bottom, y0=0, y1=H):
    for i in range(y0, y1, 4):
        t = (i - y0) / max(1, y1 - y0)
        col = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        cv.rect((0, i, W, i + 4), col)


def rain(cv, t, n=140, seed=3, alpha=90, angle=0.18):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(-200, W)
        y = (rnd.uniform(0, H) + t * 2200 * rnd.uniform(0.8, 1.2)) % H
        ln = rnd.uniform(30, 70)
        cv.line([(x, y), (x + ln * angle, y + ln)], (200, 225, 220, alpha), 2)


def head(cv, x, y, r, mood="neutral", beanie=None, hair=None, look=0):
    """Faceless-style round head. mood: neutral|angry|shock|smirk|focus"""
    if hair:
        cv.circle(x, y - r * 0.15, r * 1.08, hair)
    cv.circle(x, y, r, C["white"], C["ink"], 4)
    ex = r * 0.36
    ey = y + r * 0.05
    er = r * 0.13
    if mood == "shock":
        for s in (-1, 1):
            cv.circle(x + s * ex + look, ey, er * 1.25, C["white"], C["ink"], 4)
            cv.circle(x + s * ex + look, ey, er * 0.55, C["ink"])
        cv.ellipse((x - r * 0.12, y + r * 0.42, x + r * 0.12, y + r * 0.7), C["ink"])
    elif mood == "focus":
        for s in (-1, 1):
            cv.line([(x + s * ex - er + look, ey), (x + s * ex + er + look, ey)], C["ink"], 6)
        cv.line([(x - r * 0.15, y + r * 0.5), (x + r * 0.15, y + r * 0.5)], C["ink"], 4)
    else:
        for s in (-1, 1):
            cv.ellipse((x + s * ex - er * 0.8 + look, ey - er * 1.3,
                        x + s * ex + er * 0.8 + look, ey + er * 1.3), C["ink"])
        if mood == "angry":
            for s in (-1, 1):
                cv.line([(x + s * (ex + er * 1.6), ey - er * 2.6),
                         (x + s * (ex - er * 1.2), ey - er * 1.4)], C["ink"], 7)
            cv.arc((x - r * 0.25, y + r * 0.45, x + r * 0.25, y + r * 0.8), 200, 340, C["ink"], 5)
        elif mood == "smirk":
            cv.arc((x - r * 0.3, y + r * 0.2, x + r * 0.3, y + r * 0.6), 20, 140, C["ink"], 5)
    if beanie:
        cv.d.chord(cv.s((x - r * 1.02, y - r * 1.15, x + r * 1.02, y + r * 0.6)), 180, 360, fill=beanie)
        cv.rect((x - r * 1.05, y - r * 0.38, x + r * 1.05, y - r * 0.12), tuple(max(0, c - 25) for c in beanie), r=6)


def body(cv, x, y, r, color, arms="down", bag=None):
    """Torso below a head centred at (x, y) with radius r."""
    top = y + r * 0.9
    cv.rect((x - r * 0.9, top, x + r * 0.9, top + r * 2.0), color, C["ink"], 4, r=int(r * 0.35))
    cv.poly([(x - r * 0.25, top), (x + r * 0.25, top), (x, top + r * 0.5)], C["white"])
    # legs
    cv.rect((x - r * 0.6, top + r * 1.9, x - r * 0.1, top + r * 3.1), C["jacket"], C["ink"], 3, r=8)
    cv.rect((x + r * 0.1, top + r * 1.9, x + r * 0.6, top + r * 3.1), C["jacket"], C["ink"], 3, r=8)
    cv.ellipse((x - r * 0.75, top + r * 2.95, x - r * 0.05, top + r * 3.25), C["white"], C["ink"], 3)
    cv.ellipse((x + r * 0.05, top + r * 2.95, x + r * 0.75, top + r * 3.25), C["white"], C["ink"], 3)
    if arms == "down":
        for s in (-1, 1):
            cv.rect((x + s * r * 0.9 - r * 0.2, top + r * 0.1, x + s * r * 0.9 + r * 0.2, top + r * 1.6),
                    color, C["ink"], 3, r=10)
            cv.circle(x + s * r * 0.9, top + r * 1.7, r * 0.2, C["white"], C["ink"], 3)
    if bag:
        cv.rect((x + r * 0.7, top + r * 1.3, x + r * 1.9, top + r * 2.2), bag, C["ink"], 4, r=14)
        cv.line([(x + r * 1.0, top + r * 1.3), (x + r * 1.0, top + r * 0.9), (x + r * 1.6, top + r * 0.9),
                 (x + r * 1.6, top + r * 1.3)], C["ink"], 4)


def name_tag(cv, x, y, role, name, tx, ty, accent=None):
    accent = accent or C["pink"]
    cv.line([(x + 60, y + 40), (tx, ty)], C["white"] + (200,), 3)
    fn = font(44, "Black")
    fr = font(16, "Bold")
    w = cv.d.textlength(name, font=ImageFont.truetype(fn.path, fn.size * SS)) / SS + 40
    cv.rect((x, y, x + w, y + 80), (20, 24, 26, 230), C["white"], 3)
    cv.rect((x, y - 22, x + 14 + len(role) * 11, y), accent)
    cv.text((x + 7, y - 20), role, fr, C["white"])
    cv.text((x + 20, y + 14), name, fn, C["white"])


def cash_stack(cv, x, y, w=110, h=46, rot=0):
    cv.rect((x, y, x + w, y + h), C["cash"], C["ink"], 3, r=6)
    cv.rect((x + w * 0.38, y, x + w * 0.62, y + h), C["white"], C["ink"], 2)
    cv.circle(x + w * 0.18, y + h / 2, h * 0.22, C["cash_d"])
    cv.circle(x + w * 0.82, y + h / 2, h * 0.22, C["cash_d"])


def gold_bar(cv, x, y, w=120, h=50):
    cv.poly([(x + 14, y), (x + w - 14, y), (x + w, y + h), (x, y + h)], C["gold"], C["ink"], 3)
    cv.poly([(x + 20, y + 6), (x + w - 20, y + 6), (x + w - 28, y + 16), (x + 28, y + 16)], (255, 222, 140))


def duffel(cv, x, y, w, h, color, open_=False, fill=0.0):
    cv.rect((x, y, x + w, y + h), color, C["ink"], 5, r=int(h * 0.45))
    cv.arc((x + w * 0.25, y - h * 0.45, x + w * 0.75, y + h * 0.35), 180, 360, C["ink"], 8)
    cv.line([(x + w * 0.12, y + h * 0.25), (x + w * 0.88, y + h * 0.25)], C["white"] + (160,), 3)
    if open_:
        cv.ellipse((x + w * 0.15, y - h * 0.08, x + w * 0.85, y + h * 0.35), C["ink"])
        for i in range(int(3 * fill) + 1):
            cash_stack(cv, x + w * 0.2 + i * 40, y - h * 0.05 - i * 6, 90, 34)


# ---------------------------------------------------------------- scenes

def scene_bank(cv, t):
    gradient_sky(cv, (38, 66, 70), (92, 128, 124), 0, 1100)
    cv.circle(820, 360, 70, (220, 230, 215, 60))
    # skyline
    rnd = random.Random(7)
    x = 0
    while x < W:
        bw = rnd.randint(90, 170)
        bh = rnd.randint(250, 520)
        cv.rect((x, 1050 - bh, x + bw, 1100), (52, 86, 88))
        for wy in range(1050 - bh + 30, 1080, 60):
            for wx in range(x + 18, x + bw - 20, 40):
                if rnd.random() < 0.25:
                    cv.rect((wx, wy, wx + 16, wy + 24), (240, 200, 120, 160))
        x += bw + 6
    # bank building
    cv.rect((150, 620, 930, 1350), C["teal_l"], C["ink"], 5)
    cv.poly([(110, 640), (540, 430), (970, 640)], C["sky"], C["ink"], 5)
    cv.rect((110, 630, 970, 680), C["fog"], C["ink"], 5)
    f = font(46, "Black")
    cv.text((540, 590), "ZENTRALBANK", f, C["ink"], "ms")
    for i in range(6):
        px = 205 + i * 130
        cv.rect((px, 700, px + 60, 1290), C["fog"], C["ink"], 4)
    cv.rect((440, 1050, 640, 1290), C["night"], C["ink"], 5)
    cv.rect((120, 1290, 960, 1350), C["fog"], C["ink"], 5)
    # street
    cv.rect((0, 1350, W, H), (36, 52, 54))
    for i in range(6):
        cv.rect((i * 220 - 40, 1600, i * 220 + 80, 1620), (230, 225, 200, 120))
    # clock on facade
    cv.circle(540, 520, 50, C["white"], C["ink"], 5)
    cv.line([(540, 520), (540, 488)], C["ink"], 6)
    cv.line([(540, 520), (562, 530)], C["ink"], 5)
    # lamp
    cv.rect((70, 900, 86, 1500), C["ink"])
    cv.rect((40, 880, 116, 910), C["ink"], r=8)
    cv.glow(78, 930, 160, (255, 220, 140), 90)
    # you, back view (big foreground)
    cv.circle(560, 1420, 150, C["ink"])
    cv.d.chord(cv.s((400, 1250, 720, 1560)), 180, 360, fill=(30, 34, 38))
    cv.rect((330, 1520, 790, H + 40), C["jacket"], C["ink"], 5, r=110)
    rain(cv, t)


def scene_crew(cv, t):
    gradient_sky(cv, (30, 52, 56), (64, 98, 98))
    cv.rect((0, 1300, W, H), (34, 50, 52))
    cv.rect((60, 360, 1020, 1300), (44, 72, 74), C["ink"], 4)
    for i in range(5):
        cv.line([(60, 450 + i * 170), (1020, 450 + i * 170)], (60, 92, 94), 3)
    cv.glow(540, 520, 360, (240, 210, 140), 60)
    cv.rect((520, 340, 560, 420), C["ink"])
    cv.poly([(470, 420), (610, 420), (580, 460), (500, 460)], (230, 220, 180))
    # Mira (left), You (center), Oskar (right)
    head(cv, 230, 900, 95, "smirk", hair=C["ink"])
    body(cv, 230, 900, 95, C["mira"])
    cv.rect((150, 1110, 320, 1220), (40, 44, 48), C["ink"], 4, r=12)  # laptop
    cv.circle(235, 1165, 14, C["white"])
    head(cv, 540, 820, 120, "focus", beanie=(40, 40, 44))
    body(cv, 540, 820, 120, C["jacket"])
    head(cv, 850, 900, 95, "neutral", hair=C["brown_d"], look=-10)
    body(cv, 850, 900, 95, C["oskar"])
    cv.circle(930, 1180, 22, C["gold"], C["ink"], 3)  # car keys
    name_tag(cv, 60, 600, "HACKERIN", "MIRA", 210, 805)
    name_tag(cv, 470, 470, "TRESORKNACKER", "DU", 540, 690, C["gold"])
    name_tag(cv, 690, 600, "FAHRER", "OSKAR", 850, 805)


def scene_hack(cv, t):
    cv.img.paste(C["night"], (0, 0) + cv.img.size)
    cv.rect((0, 1350, W, H), (26, 38, 40))
    # monitor wall
    for r_ in range(3):
        for c_ in range(3):
            x0 = 120 + c_ * 290
            y0 = 360 + r_ * 210
            cv.rect((x0, y0, x0 + 260, y0 + 180), (28, 40, 42), C["steel"], 5, r=8)
            cv.rect((x0 + 14, y0 + 14, x0 + 246, y0 + 166), (50, 92, 80))
            cv.rect((x0 + 40, y0 + 110, x0 + 220, y0 + 120), (80, 130, 110))
            cv.text((x0 + 22, y0 + 22), f"CAM {r_ * 3 + c_ + 1}", mono(20), (180, 255, 200))
            cv.text((x0 + 170, y0 + 140), "LOOP", mono(18), C["pink"])
    cv.glow(540, 560, 420, (80, 255, 160), 35)
    # Mira with laptop
    head(cv, 540, 1010, 110, "smirk", hair=C["ink"])
    body(cv, 540, 1010, 110, C["mira"], arms=None)
    cv.poly([(340, 1400), (740, 1400), (800, 1520), (280, 1520)], (52, 56, 60), C["ink"], 5)
    cv.rect((360, 1240, 720, 1400), (40, 44, 48), C["ink"], 5, r=10)
    cv.rect((380, 1260, 700, 1385), (30, 60, 50))
    for i in range(5):
        ln = 80 + (i * 53) % 170
        cv.rect((400, 1275 + i * 22, 400 + ln, 1287 + i * 22), (120, 255, 170))
    cv.glow(540, 1320, 200, (120, 255, 170), 60)


def scene_vault_crack(cv, t):
    gradient_sky(cv, (40, 52, 54), (70, 86, 88))
    cx, cy = 560, 900
    cv.circle(cx, cy, 470, C["steel_d"], C["ink"], 6)
    cv.circle(cx, cy, 420, C["steel"], C["ink"], 5)
    for a in range(0, 360, 30):
        rx = cx + 445 * math.cos(math.radians(a))
        ry = cy + 445 * math.sin(math.radians(a))
        cv.circle(rx, ry, 14, C["steel_l"], C["ink"], 3)
    cv.circle(cx, cy, 190, C["steel_l"], C["ink"], 5)
    rot = t * 300
    for i in range(40):
        a = math.radians(i * 9 + rot)
        l = 26 if i % 5 == 0 else 14
        cv.line([(cx + 175 * math.cos(a), cy + 175 * math.sin(a)),
                 (cx + (175 - l) * math.cos(a), cy + (175 - l) * math.sin(a))], C["ink"], 4)
    cv.circle(cx, cy, 80, C["steel_d"], C["ink"], 5)
    cv.poly([(cx - 10, cy - 210), (cx + 10, cy - 210), (cx, cy - 188)], C["pink"])
    # bare hand on dial
    cv.ellipse((cx + 120, cy - 40, cx + 330, cy + 120), C["white"], C["ink"], 5)
    for i in range(4):
        cv.ellipse((cx + 90 - i * 6, cy - 30 + i * 36, cx + 160, cy + 2 + i * 36), C["white"], C["ink"], 4)
    cv.rect((cx + 280, cy - 30, cx + 560, cy + 120), C["jacket"], C["ink"], 5, r=30)
    # gloves on floor
    cv.ellipse((150, 1430, 330, 1520), (30, 30, 34), C["ink"], 4)
    cv.ellipse((290, 1450, 460, 1540), (30, 30, 34), C["ink"], 4)
    # stethoscope
    cv.line([(cx - 60, cy + 30), (cx - 250, cy + 260), (cx - 120, cy + 420)], (200, 60, 60), 8)
    cv.circle(cx - 60, cy + 30, 26, C["steel_l"], C["ink"], 4)
    cv.text((200, 420), "KLICK.", font(80), C["white"])
    cv.text((640, 1400), "KLICK.", font(64), C["white"] + (170,))


def scene_vault_open(cv, t):
    cv.img.paste((30, 40, 40), (0, 0) + cv.img.size)
    cv.rect((150, 300, 930, 1500), (70, 56, 30), C["ink"], 5)
    cv.glow(540, 900, 520, C["gold"], 150)
    for row in range(4):
        y = 420 + row * 260
        cv.rect((170, y + 170, 910, y + 190), C["steel_d"], C["ink"], 3)
        for k in range(5):
            if (row + k) % 2:
                gold_bar(cv, 200 + k * 140, y + 120)
                gold_bar(cv, 220 + k * 140, y + 70, 90, 46)
            else:
                cash_stack(cv, 200 + k * 140, y + 124)
                cash_stack(cv, 205 + k * 140, y + 78)
                cash_stack(cv, 210 + k * 140, y + 32)
    # open door edge on the left
    cv.poly([(0, 260), (170, 300), (170, 1500), (0, 1560)], C["steel"], C["ink"], 6)
    cv.circle(80, 900, 50, C["steel_l"], C["ink"], 4)
    # silhouettes
    for x, hr in ((300, 75), (780, 75)):
        cv.circle(x, 1560, hr, (20, 22, 24))
        cv.rect((x - 90, 1630, x + 90, H), (20, 22, 24), r=50)


def scene_bags(cv, t):
    cv.img.paste((52, 50, 38), (0, 0) + cv.img.size)
    cv.glow(540, 500, 600, C["gold"], 70)
    cv.rect((0, 1200, W, H), (40, 40, 34))
    colors = [C["ink"], C["brown"], C["brown_d"], (40, 52, 60)]
    for i, col in enumerate(colors):
        x = 90 + (i % 2) * 470
        y = 900 + (i // 2) * 300
        duffel(cv, x, y, 400, 200, col, open_=True, fill=min(1, t + 0.3 * i))
    for i in range(9):
        rnd = random.Random(i)
        cash_stack(cv, rnd.uniform(60, 900), 360 + rnd.uniform(0, 380) + t * 220, 120, 50)
    head(cv, 540, 600, 85, "shock", beanie=(40, 40, 44))


def scene_envelope(cv, t):
    cv.img.paste((44, 40, 30), (0, 0) + cv.img.size)
    cv.glow(540, 960, 600, C["gold"], 60)
    for i in range(16):
        rnd = random.Random(i + 40)
        cash_stack(cv, rnd.uniform(40, 950), rnd.uniform(500, 1500), 130, 54)
    cv.glow(540, 960, 330, (255, 255, 255), 60)
    # envelope
    cv.rect((230, 760, 850, 1160), (236, 226, 200), C["ink"], 6)
    cv.poly([(230, 760), (540, 990), (850, 760)], (220, 208, 178), C["ink"], 5)
    cv.circle(540, 990, 40, C["red"], C["ink"], 4)
    cv.text((540, 1105), "FÜR:  ██████", font(48, "Black"), C["ink"], "ms")


def scene_photo(cv, t):
    cv.img.paste((34, 40, 40), (0, 0) + cv.img.size)
    cv.glow(540, 760, 520, (255, 240, 210), 50)
    cv.poly([(170, 400), (870, 350), (910, 1040), (210, 1090)], C["white"], C["ink"], 6)
    cv.poly([(205, 440), (835, 395), (865, 900), (240, 945)], (60, 70, 72))
    cv.circle(620, 660, 200, C["steel"], C["ink"], 4)
    cv.circle(620, 660, 76, C["steel_l"], C["ink"], 4)
    head(cv, 400, 650, 88, "focus", beanie=(40, 40, 44))
    cv.ellipse((515, 650, 605, 720), C["white"], C["ink"], 4)
    cv.circle(558, 685, 72, C["red"] + (0,), C["red"], 6)
    cv.text((235, 460), "REC 03:13", mono(30), C["red"])
    cv.poly([(400, 1000), (830, 975), (845, 1150), (415, 1175)], (250, 238, 160), C["ink"], 5)
    cv.text((435, 1020), "Danke für die", font(40, "Bold"), C["ink"])
    cv.text((435, 1070), "Fingerabdrücke.", font(40, "Bold"), C["ink"])
    cv.text((720, 1115), "– O.", font(44, "Black"), C["red"])


def scene_alarm(cv, t):
    cv.img.paste((70, 18, 22), (0, 0) + cv.img.size)
    flash = 0.5 + 0.5 * math.sin(t * math.pi * 6)
    cv.glow(540, 360, 520, C["red"], int(90 + 110 * flash))
    cv.rect((420, 300, 660, 360), C["ink"], r=10)
    cv.d.chord(cv.s((440, 180, 640, 420)), 180, 360, fill=C["red"])
    for a in (-60, -30, 0, 30, 60):
        r0, r1 = 160, 260
        ang = math.radians(a - 90)
        cv.line([(540 + r0 * math.cos(ang), 300 + r0 * math.sin(ang)),
                 (540 + r1 * math.cos(ang), 300 + r1 * math.sin(ang))], C["white"] + (int(255 * flash),), 10)
    cv.rect((0, 1350, W, H), (50, 14, 16))
    head(cv, 330, 1000, 110, "shock", beanie=(40, 40, 44))
    body(cv, 330, 1000, 110, C["jacket"], bag=C["ink"])
    head(cv, 740, 1050, 100, "shock", hair=C["ink"])
    body(cv, 740, 1050, 100, C["mira"], bag=C["brown"])
    cv.overlay(C["red"], int(40 * flash))


def scene_car(cv, t):
    gradient_sky(cv, (22, 36, 40), (52, 78, 80), 0, 1000)
    cv.rect((0, 1000, W, H), (30, 40, 42))
    cv.poly([(380, 1000), (700, 1000), (1080, 1920), (0, 1920)], (40, 52, 54))
    for i in range(6):
        y = 1050 + i * 150
        cv.rect((530, y, 550, y + 70), (230, 225, 200, 160))
    s = 1.0 - 0.45 * t
    cx, cy = 540, 1000 + 260 * s
    w, h = 520 * s, 220 * s
    cv.rect((cx - w / 2, cy - h, cx + w / 2, cy), (26, 28, 30), C["ink"], 5, r=int(30 * s))
    cv.rect((cx - w * 0.38, cy - h * 1.55, cx + w * 0.38, cy - h * 0.9), (26, 28, 30), C["ink"], 5, r=int(30 * s))
    cv.rect((cx - w * 0.32, cy - h * 1.45, cx + w * 0.32, cy - h), (60, 80, 84))
    for sgn in (-1, 1):
        cv.rect((cx + sgn * w * 0.42 - 45 * s, cy - h * 0.7, cx + sgn * w * 0.42 + 45 * s, cy - h * 0.45),
                C["red"], r=6)
        cv.glow(cx + sgn * w * 0.42, cy - h * 0.58, 120 * s, C["red"], 140)
    # Oskar's waving arm
    ax, ay = cx + w * 0.38, cy - h * 1.3
    cv.line([(ax, ay), (ax + 70 * s, ay - 90 * s)], C["oskar"], 26 * s)
    cv.circle(ax + 76 * s, ay - 100 * s, 22 * s, C["white"], C["ink"], 3)
    cv.text((cx - 70 * s, cy - h * 0.3), "OSK 4R", font(int(40 * s), "Black"), C["white"])
    # you from behind, foreground
    cv.circle(260, 1640, 120, C["ink"])
    cv.d.chord(cv.s((130, 1500, 390, 1760)), 180, 360, fill=(30, 34, 38))
    cv.rect((90, 1730, 430, H + 50), C["jacket"], C["ink"], 5, r=90)
    duffel(cv, 440, 1700, 300, 150, C["brown"])
    rain(cv, t, alpha=110)


def scene_final(cv, t):
    flash = 0.5 + 0.5 * math.sin(t * math.pi * 8)
    gradient_sky(cv, (20, 30, 40), (40, 60, 70))
    cv.glow(80, 500, 500, C["red"], int(80 + 90 * flash))
    cv.glow(1000, 520, 500, C["blue"], int(80 + 90 * (1 - flash)))
    cv.rect((0, 1300, W, H), (26, 34, 38))
    for i in range(3):
        cv.ellipse((100 + i * 320, 1420 + i * 40, 320 + i * 320, 1450 + i * 40), (90, 110, 160, 90))
    head(cv, 360, 780, 120, "focus", beanie=(40, 40, 44))
    body(cv, 360, 780, 120, C["jacket"], bag=C["ink"])
    head(cv, 720, 830, 105, "neutral", hair=C["ink"], look=-18)
    body(cv, 720, 830, 105, C["mira"], bag=C["brown"])
    # choice buttons
    cv.rect((110, 1290, 470, 1390), C["white"], C["ink"], 5, r=24)
    cv.text((290, 1357), "RENNEN", font(52), C["ink"], "ms")
    cv.rect((510, 1290, 870, 1390), C["pink"], C["ink"], 5, r=24)
    cv.text((690, 1357), "STELLEN", font(52), C["white"], "ms")
    rain(cv, t, alpha=120)


SCENES = [scene_bank, scene_crew, scene_hack, scene_vault_crack, scene_vault_open, scene_bags,
          scene_envelope, scene_envelope, scene_photo, scene_alarm, scene_car, scene_final]


# ---------------------------------------------------------------- overlays

def hud(img, beute, crew, hitze, alarm, alarm_col=None, crew_col=None):
    """Game-style stat chips (top-left, below TikTok's top tabs)."""
    d = ImageDraw.Draw(img, "RGBA")
    y = 250
    chips = [("BEUTE", f"€{beute:,}".replace(",", "."), C["white"]),
             ("CREW", str(crew), crew_col or C["white"]),
             ("HITZE", f"{hitze} %", C["pink"]),
             ("ALARM", alarm, alarm_col or C["gold"])]
    x = 50
    fl = font(17, "Bold")
    fv = font(46, "Black")
    for label, val, col in chips:
        w = int(d.textlength(val, font=fv)) + 34
        d.rounded_rectangle((x, y, x + w, y + 92), 10, fill=(14, 20, 22, 205), outline=(255, 255, 255, 60), width=2)
        d.text((x + 16, y + 10), label, font=fl, fill=(200, 210, 208))
        d.text((x + 16, y + 32), val, font=fv, fill=col)
        x += w + 14
    return img


def caption(img, words, hi=(), y=1210, visible=None):
    """Big centered caption; words whose index is in `hi` turn pink.
    `visible` = number of words already spoken (layout stays fixed)."""
    visible = len(words) if visible is None else visible
    d = ImageDraw.Draw(img, "RGBA")
    f = font(72, "Black")
    space = d.textlength(" ", font=f)
    widths = [d.textlength(w_, font=f) for w_ in words]
    total = sum(widths) + space * (len(words) - 1)
    cx = 500  # shifted left of centre so TikTok's right-hand buttons never overlap
    x = cx - total / 2
    for i, w_ in enumerate(words):
        if i >= visible:
            break
        col = C["pink"] if i in hi else C["white"]
        d.text((x, y), w_, font=f, fill=col, anchor="ls", stroke_width=6, stroke_fill=(10, 14, 14))
        x += widths[i] + space
    return img


def glitch(img, strength=1.0, timecode="SP 00:00:34"):
    """VHS pause effect: RGB split, scanlines, PAUSE label, timecode."""
    r, g, b = img.split()
    off = int(14 * strength)
    r = r.transform(img.size, Image.AFFINE, (1, 0, off, 0, 1, 0))
    b = b.transform(img.size, Image.AFFINE, (1, 0, -off, 0, 1, 0))
    img = Image.merge("RGB", (r, g, b))
    img = Image.blend(img, Image.new("RGB", img.size, (200, 200, 200)), 0.18)
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(0, H, 6):
        d.rectangle((0, y, W, y + 2), fill=(0, 0, 0, 50))
    rnd = random.Random(int(strength * 100))
    for _ in range(4):
        y = rnd.randint(300, 1500)
        band = img.crop((0, y, W, y + 26))
        img.paste(band, (rnd.randint(-40, 40), y))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle((60, 380, 80, 450), fill=C["white"])
    d.rectangle((95, 380, 115, 450), fill=C["white"])
    d.text((135, 372), "PAUSE", font=mono(78), fill=C["white"], stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((60, 1320), timecode, font=mono(56), fill=C["white"], stroke_width=3, stroke_fill=(0, 0, 0))
    return img


def render(i, t=0.5):
    cv = Canvas(C["night"])
    SCENES[i](cv, t)
    return cv.final()
