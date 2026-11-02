"""Darker scene set for Teil 2. Reuses the drawing helpers from ../bankraub/scenes.py
and adds a 'noir' post-process (desaturation, vignette, grain, flicker)."""
import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bankraub"))
import scenes as S  # noqa: E402
from scenes import Canvas, head, body, duffel, cash_stack, gold_bar, font, mono, rain, W, H  # noqa: E402,F401

C = dict(S.C)
C.update({
    "void": (8, 11, 14),
    "wall": (22, 27, 32),
    "wall_l": (34, 41, 48),
    "wet": (16, 20, 25),
    "blue": (40, 90, 255),
    "red": (220, 30, 40),
    "paper": (196, 190, 172),
    "mira_d": (58, 40, 78),
})
INK = C["ink"]


def silhouette(cv, x, y, r, col=(6, 8, 10)):
    cv.circle(x, y, r, col)
    cv.rect((x - r * 1.3, y + r * 0.8, x + r * 1.3, y + r * 4), col, r=int(r * 0.6))


def beanie_head(cv, x, y, r, mood="focus", look=0):
    head(cv, x, y, r, mood, beanie=(34, 34, 40), look=look)


# ------------------------------------------------------------------ scenes

def s_run(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    # alley walls in perspective
    cv.poly([(0, 0), (330, 520), (330, 1250), (0, 1920)], C["wall"])
    cv.poly([(1080, 0), (750, 520), (750, 1250), (1080, 1920)], C["wall_l"])
    cv.poly([(0, 1920), (330, 1250), (750, 1250), (1080, 1920)], C["wet"])
    flash = 0.5 + 0.5 * math.sin(t * 30)
    cv.glow(540, 900, 160, C["blue"], int(70 + 80 * flash))
    cv.glow(540, 900, 120, C["red"], int(60 + 70 * (1 - flash)))
    # reflections
    for k in range(5):
        cv.rect((420 + k * 40, 1300 + k * 90, 470 + k * 40, 1320 + k * 90), (60, 90, 200, 50))
    # Mira behind (smaller), phone glow in pocket = clue
    head(cv, 700, 900, 62, "neutral", hair=INK, look=-6)
    body(cv, 700, 900, 62, C["mira_d"])
    cv.glow(745, 1010, 30, (150, 220, 255), 160)
    # you running toward camera (big, slight bob)
    bob = 18 * math.sin(t * 40)
    beanie_head(cv, 420, 820 + bob, 150, "shock")
    body(cv, 420, 820 + bob, 150, C["jacket"], arms=None)
    duffel(cv, 110, 1150 + bob, 260, 150, (30, 30, 34))
    duffel(cv, 560, 1180 - bob, 260, 150, C["brown_d"])
    rain(cv, t, n=120, alpha=70)


def s_alley(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    cv.poly([(0, 0), (400, 600), (400, 1150), (0, 1920)], C["wall"])
    cv.poly([(1080, 0), (680, 600), (680, 1150), (1080, 1920)], C["wall_l"])
    cv.poly([(0, 1920), (400, 1150), (680, 1150), (1080, 1920)], C["wet"])
    # bricks
    for y in range(200, 1700, 70):
        cv.line([(0, y), (300, y + 60)], (30, 36, 42), 3)
    # flickering lamp
    on = (int(t * 37) % 7) != 0
    cv.rect((180, 380, 200, 560), (10, 10, 12))
    cv.rect((150, 360, 260, 390), (10, 10, 12), r=8)
    if on:
        cv.glow(205, 420, 260, (255, 200, 120), 90)
    # dark police car at the end of the alley (clue)
    cv.rect((440, 1040, 640, 1130), (14, 16, 20), (40, 50, 70), 3, r=16)
    cv.rect((480, 1000, 600, 1050), (14, 16, 20), (40, 50, 70), 3, r=12)
    cv.rect((515, 988, 565, 1002), (40, 50, 110))
    # two silhouettes walking in
    silhouette(cv, 330, 1260, 70)
    silhouette(cv, 760, 1290, 64)
    rain(cv, t, n=110, alpha=60)


def s_key(cv, t):
    cv.img.paste((14, 12, 14), (0, 0) + cv.img.size)
    cv.rect((180, 260, 900, 1700), (40, 30, 30), INK, 6)
    cv.glow(540, 330, 260, C["red"], 140)
    cv.rect((470, 300, 610, 340), C["red"], INK, 3, r=6)
    # lock plate
    cv.rect((620, 760, 760, 1060), (110, 104, 92), INK, 5, r=20)
    cv.circle(690, 860, 32, (40, 40, 40), INK, 4)
    # hand + key turning
    ang = -40 * min(1, t * 2)
    cv.ellipse((330, 790, 560, 940), C["white"], INK, 5)
    for i in range(4):
        cv.ellipse((480, 790 + i * 34, 580, 822 + i * 34), C["white"], INK, 4)
    cv.rect((560, 850, 690, 872), (180, 170, 120), INK, 3)
    cv.circle(560, 861, 30, (180, 170, 120), INK, 4)
    # keyring with star (clue)
    cv.circle(470, 980, 50, None, (170, 170, 170), 5)
    star = [(470 + 40 * math.cos(math.radians(a)) * (1 if k % 2 == 0 else 0.45),
             1060 + 40 * math.sin(math.radians(a)) * (1 if k % 2 == 0 else 0.45))
            for k, a in enumerate(range(-90, 270, 36))]
    cv.poly(star, (210, 180, 70), INK, 3)
    cv.rect((0, 560, 340, 1500), (60, 40, 80))  # Mira's sleeve
    cv.text((640, 1250), "klick.", font(60), (180, 170, 160))


def s_wall(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    cv.rect((70, 340, 1010, 1380), (30, 30, 30))
    # bank plan
    cv.rect((110, 380, 470, 640), (40, 60, 90), (120, 150, 190), 3)
    for k in range(5):
        cv.line([(130, 420 + k * 45), (450, 420 + k * 45)], (120, 150, 190), 2)
    cv.text((125, 600), "ZENTRALBANK", mono(26), (190, 210, 240))
    # photos
    def photo(x, y, who, crossed=False):
        cv.rect((x, y, x + 180, y + 210), C["paper"], INK, 4)
        cv.rect((x + 12, y + 12, x + 168, y + 160), (60, 66, 70))
        if who == "you":
            beanie_head(cv, x + 90, y + 95, 50, "focus")
        elif who == "oskar":
            head(cv, x + 90, y + 95, 50, "neutral", hair=C["brown_d"])
        else:
            head(cv, x + 90, y + 95, 50, "smirk", hair=INK)
        if crossed:
            cv.line([(x, y), (x + 180, y + 210)], C["red"], 10)
            cv.line([(x + 180, y), (x, y + 210)], C["red"], 10)
        cv.circle(x + 90, y + 6, 10, C["red"])
    pins = [(540, 680), (220, 860), (820, 520), (780, 1000), (300, 1150)]
    for a in pins[1:]:
        cv.line([pins[0], a], C["red"], 4)
    photo(450, 650, "you")
    photo(130, 830, "mira")
    photo(730, 490, "oskar", crossed=True)
    cv.rect((700, 960, 960, 1140), C["paper"], INK, 3)
    cv.text((720, 990), "03:12", mono(40), INK)
    cv.text((720, 1050), "TRESOR", mono(30), INK)
    # flashlight cone
    cx = 300 + 400 * t
    layer = Image.new("L", cv.img.size, 0)
    ImageDraw.Draw(layer).ellipse(cv.s((cx - 330, 520, cx + 330, 1180)), fill=255)
    layer = layer.filter(ImageFilter.GaussianBlur(60))
    dark = Image.new("RGB", cv.img.size, (4, 5, 6))
    cv.img = Image.composite(cv.img, Image.blend(cv.img, dark, 0.8), layer)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")


def s_phone(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    cv.glow(540, 900, 380, (120, 180, 255), 60 + int(40 * (t > 0.3)))
    # Mira's silhouette with face lit from below
    cv.circle(540, 760, 210, (230, 236, 240))
    cv.d.chord(cv.s((330, 550, 750, 940)), 180, 360, fill=(6, 8, 10))
    cv.ellipse((440, 760, 490, 830), INK)
    cv.ellipse((590, 760, 640, 830), INK)
    cv.rect((290, 960, 790, 1500), (12, 10, 18), r=120)
    # phone
    cv.rect((420, 1020, 660, 1440), (20, 20, 24), INK, 6, r=30)
    cv.rect((440, 1050, 640, 1410), (40, 70, 120))
    cv.text((540, 1140), "INFORMANT" if t < 0.25 else "OSKAR", mono(28), C["white"], "ms")
    cv.circle(500, 1330, 34, (60, 200, 90))
    cv.circle(580, 1330, 34, C["red"])


def s_whisper(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    # extreme close-up: half lit face
    cv.circle(560, 900, 560, (220, 224, 228))
    layer = Image.new("RGBA", cv.img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rectangle(cv.s((0, 0, 470 + 40 * math.sin(t * 6), H)), fill=(4, 5, 6, 235))
    cv.img.paste(layer, (0, 0), layer)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")
    cv.ellipse((640, 700, 760, 860), INK)
    m = 30 + 25 * abs(math.sin(t * 20))
    cv.ellipse((600, 1130 - m / 2, 820, 1130 + m / 2), (60, 10, 16))
    cv.rect((860, 700, 1080, 1250), (20, 20, 24), INK, 6, r=40)  # phone at ear


def s_bags(cv, t):
    cv.img.paste((12, 12, 12), (0, 0) + cv.img.size)
    cv.glow(540, 700, 420, (255, 230, 190), 50)
    for i, col in enumerate([(30, 30, 34), C["brown_d"]]):
        x = 90 + i * 470
        duffel(cv, x, 1000, 400, 220, col)
        cv.ellipse((x + 60, 960, x + 340, 1060), (6, 6, 6))
    # newspapers spilling
    for k in range(6):
        rnd = random.Random(k)
        x = rnd.uniform(80, 760)
        y = rnd.uniform(560, 960) - t * 60 * (k % 3)
        cv.rect((x, y, x + 230, y + 150), C["paper"], INK, 3)
        for j in range(4):
            cv.line([(x + 15, y + 50 + j * 22), (x + 210, y + 50 + j * 22)], (120, 116, 104), 4)
        cv.rect((x + 15, y + 12, x + 210, y + 34), (80, 76, 66))
    # headline (clue)
    cv.rect((180, 360, 900, 620), C["paper"], INK, 5)
    cv.text((540, 450), "BANKRAUB IN DER", font(54, "Black"), INK, "ms")
    cv.text((540, 520), "ZENTRALBANK", font(70, "Black"), INK, "ms")
    cv.text((540, 590), "Ausgabe vom 01.11. – 06:00 Uhr", font(30, "Bold"), (90, 30, 30), "ms")


def s_flashback(cv, t):
    cv.img.paste((20, 18, 12), (0, 0) + cv.img.size)
    cv.rect((120, 320, 960, 1400), (40, 34, 20), INK, 5)
    for i in range(4):
        x = 150 + (i % 2) * 420
        y = 600 + (i // 2) * 360
        glowing = i in (1, 2)
        if glowing:
            cv.glow(x + 190, y + 100, 230, C["gold"], 120)
        duffel(cv, x, y, 380, 190, C["gold"] if glowing else (30, 30, 30))
        cv.text((x + 190, y + 120), "ECHT" if glowing else "PAPIER", font(42), INK if glowing else (150, 150, 150), "ms")
    for s_ in (-1, 1):
        cv.glow(540 + s_ * 160, 1520, 90, C["red"], 140)


def s_badge(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    flash = 0.5 + 0.5 * math.sin(t * 25)
    cv.glow(950, 500, 400, C["blue"], int(40 + 60 * flash))
    cv.rect((0, 1050, W, 1500), (26, 22, 18))
    cv.glow(540, 820, 360, (255, 220, 160), 70)
    cv.line([(540, 200), (540, 560)], (10, 10, 10), 6)
    cv.poly([(440, 560), (640, 560), (600, 620), (480, 620)], (40, 40, 40))
    drop = max(0, 1 - t * 4) * -250
    cx, cy = 540, 960 + drop
    star = [(cx + 150 * math.cos(math.radians(a)) * (1 if k % 2 == 0 else 0.5),
             cy - 40 + 150 * math.sin(math.radians(a)) * (1 if k % 2 == 0 else 0.5))
            for k, a in enumerate(range(-90, 270, 36))]
    cv.rect((cx - 210, cy - 210, cx + 210, cy + 220), (30, 24, 20), INK, 5, r=30)
    cv.poly(star, (215, 180, 70), INK, 5)
    cv.text((cx, cy + 150), "KRIMINALPOLIZEI", font(34, "Black"), (215, 180, 70), "ms")
    cv.text((cx, cy + 195), "O. MIRKOVIĆ", mono(30), (200, 200, 200), "ms")


def s_final(cv, t):
    flash = 0.5 + 0.5 * math.sin(t * 30)
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    # window
    cv.rect((300, 330, 900, 1180), (10, 14, 30), (60, 60, 70), 10)
    cv.glow(600, 750, 420, C["blue"], int(90 + 100 * flash))
    cv.glow(600, 750, 300, C["red"], int(70 + 90 * (1 - flash)))
    cv.line([(600, 330), (600, 1180)], (60, 60, 70), 10)
    # you jumping out (silhouette, moves right)
    jx = 480 + 280 * t
    silhouette(cv, jx, 700 - 120 * t, 70, (4, 4, 6))
    # Mira foreground silhouette, badge glints
    silhouette(cv, 200, 1150, 150, (2, 2, 3))
    cv.glow(260, 1350, 40, (255, 210, 90), 180)
    rain(cv, t, n=60, alpha=50)


SCENES = [s_run, s_alley, s_key, s_wall, s_phone, s_phone, s_whisper, s_bags, s_flashback, s_badge, s_final]


# ------------------------------------------------------------------ noir post-process

_rng = np.random.default_rng(0)
_yy, _xx = np.mgrid[0:H, 0:W]
_VIG = 1.0 - 0.75 * np.clip(((_xx - W / 2) / (W * 0.62)) ** 2 + ((_yy - H * 0.45) / (H * 0.6)) ** 2, 0, 1)
_VIG = _VIG[..., None].astype(np.float32)


def noir(img, n=0, flicker=True, desat=0.45):
    a = np.asarray(img).astype(np.float32)
    grey = a.mean(axis=2, keepdims=True)
    a = a * (1 - desat) + grey * desat
    # keep pure reds as accent
    red = (np.asarray(img)[..., 0] > 150) & (np.asarray(img)[..., 1] < 90)
    a[red] = np.asarray(img).astype(np.float32)[red]
    a *= _VIG
    if flicker:
        a *= 0.93 + 0.07 * random.Random(n).random()
    a += np.random.default_rng(n).normal(0, 9, (H // 2, W // 2, 1)).repeat(2, 0).repeat(2, 1)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def render(i, t=0.5):
    cv = Canvas(C["void"])
    SCENES[i](cv, t)
    return cv.final()


def hud(img, beute, vertrauen, hitze, v_col=None):
    d = ImageDraw.Draw(img, "RGBA")
    y, x = 250, 50
    chips = [("BEUTE", f"€{beute:,}".replace(",", "."), C["white"] if beute else C["red"]),
             ("VERTRAUEN · MIRA", f"{vertrauen} %", v_col or (C["white"] if vertrauen > 50 else C["red"])),
             ("HITZE", f"{hitze} %", C["pink"])]
    fl, fv = font(17, "Bold"), font(46, "Black")
    for label, val, col in chips:
        w = int(max(d.textlength(val, font=fv), d.textlength(label, font=fl))) + 34
        d.rounded_rectangle((x, y, x + w, y + 92), 10, fill=(6, 8, 10, 215), outline=(255, 255, 255, 40), width=2)
        d.text((x + 16, y + 10), label, font=fl, fill=(170, 176, 176))
        d.text((x + 16, y + 32), val, font=fv, fill=col)
        x += w + 14
    return img
