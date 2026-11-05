"""Scenes for 'SCHNELLE WELLE' in STIL 3. No drugs shown – only stress, fear and consequences."""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "reich"))
sys.path.append(os.path.join(HERE, "..", "arbeiten"))
import style3 as T  # noqa: E402
from style3 import Canvas, font, mono, W, H, ease, seg, INK, WHITE, SKIN, YELLOW  # noqa: E402
import scenes9 as A  # noqa: E402  (phone_ui, office helpers)

CX, FEET, SCALE = 540, 1720, 1.2
RED, GREEN = (220, 40, 50), (40, 140, 70)
HOOD_DARK = (44, 50, 70)
POLICE = (30, 60, 120)


def blink_at(t, dur):
    return ((t * dur) % 2.6) < 0.1


def night_street(cv, t=0.0):
    for y in range(0, 1100, 6):
        k = y / 1100
        cv.rect((0, y, W, y + 6), (int(20 + 30 * k), int(24 + 30 * k), int(50 + 40 * k)))
    rnd = random.Random(4)
    x = -20
    while x < W:
        bw, bh = rnd.randint(160, 260), rnd.randint(450, 750)
        cv.rect((x, 1100 - bh, x + bw, 1100), (50, 56, 84), INK, 4)
        for wy in range(1100 - bh + 40, 1060, 90):
            for wx in range(x + 30, x + bw - 50, 70):
                cv.rect((wx, wy, wx + 40, wy + 56), (255, 214, 120) if rnd.random() < 0.3 else (34, 38, 60))
        x += bw + 10
    cv.rect((0, 1100, W, 1180), (120, 120, 128), INK, 3)  # sidewalk
    cv.rect((0, 1180, W, H), (52, 54, 62))
    for k in range(6):
        cv.rect((k * 200 - 40, 1500, k * 200 + 80, 1520), (220, 220, 200))
    cv.rect((900, 560, 916, 1100), (40, 40, 46))  # street lamp
    cv.rect((860, 540, 960, 570), (40, 40, 46), r=8)
    cv.glow(910, 600, 260, (255, 220, 140), 110)


def dark_car(cv, x, y, w=620, lights=True):
    h = w * 0.3
    cv.rect((x, y - h * 0.55, x + w, y), (30, 32, 40), INK, 6, r=30)
    cv.poly([(x + w * 0.2, y - h * 0.55), (x + w * 0.32, y - h), (x + w * 0.72, y - h), (x + w * 0.86, y - h * 0.55)],
            (30, 32, 40), INK, 5)
    cv.poly([(x + w * 0.34, y - h * 0.92), (x + w * 0.7, y - h * 0.92), (x + w * 0.8, y - h * 0.58), (x + w * 0.3, y - h * 0.58)],
            (60, 70, 90), INK, 4)
    for wx in (x + w * 0.2, x + w * 0.8):
        cv.circle(wx, y, h * 0.3, (20, 20, 22), INK, 5)
    if lights:
        cv.rect((x + w - 30, y - h * 0.45, x + w + 4, y - h * 0.3), (255, 250, 200))
        cv.poly([(x + w, y - h * 0.42), (x + w + 520, y - h * 0.9), (x + w + 520, y + h * 0.3)], (255, 250, 200, 70))


def police_officer(cv, x, y_feet, s, mood="neutral"):
    hy = T.character(cv, x, y_feet, s, mood, "down", hoodie=POLICE, hair=(40, 30, 26))
    r = 150 * s
    cv.d.chord(cv.s((x - r * 1.05, hy - r * 1.15, x + r * 1.05, hy + r * 0.25)), 180, 360, fill=(20, 40, 90))
    cv.rect((x - r * 1.1, hy - r * 0.48, x + r * 1.1, hy - r * 0.3), (16, 30, 70), r=6)
    cv.rect((x - r * 0.18, hy - r * 0.95, x + r * 0.18, hy - r * 0.65), YELLOW, r=6)
    cv.text((x, hy + r * 1.95), "POLIZEI", font(int(44 * s), "Black"), WHITE, "ms")


def mom(cv, x, y_feet, s, mood="worry", talk=0.0):
    hy = T.character(cv, x, y_feet, s, mood, "point", talk=talk, hoodie=(200, 110, 130), hair=(110, 70, 50))
    r = 150 * s
    cv.circle(x, hy - r * 1.05, r * 0.38, (110, 70, 50), INK, 5)  # bun
    cv.rect((x - 120 * s, hy + r * 1.5, x + 120 * s, hy + r * 3.6), (250, 240, 220), INK, 5, r=int(20 * s))  # apron


def shoebox(cv, x, y, open_k=1.0):
    cv.rect((x, y, x + 360, y + 160), (230, 120, 60), INK, 6, r=8)
    if open_k > 0:
        for j in range(5):
            T.bill(cv, x + 60 + j * 60, y + 30 - j * 4, 130, -0.3 + j * 0.15)
    cv.rect((x - 10, y - 30 - 60 * open_k, x + 370, y - 0 - 60 * open_k), (240, 140, 80), INK, 6, r=8)


# ------------------------------------------------------------------ scenes (cv, t, dur)

def s_comment(cv, t, dur):
    T.bedroom(cv)
    T.character(cv, CX, FEET + 230, SCALE, "angry" if t > 0.5 else "neutral", "down", blink=blink_at(t, dur))
    A.phone_ui(cv, 140, 440, 940, 1040, "Kommentare")
    rows = (("lisa_92", "Krasse Story"), ("bruder.1987", "Schnelle Welle. Straßenapotheker."), ("max.m", "Teil 2?!"))
    for j, (name, txt) in enumerate(rows):
        y = 560 + j * 150
        hl = j == 1 and t > 0.15
        cv.rect((170, y, 910, y + 120), (255, 245, 200) if hl else WHITE, (200, 200, 210), 3, r=18)
        cv.circle(230, y + 60, 38, (190, 190, 200))
        cv.text((290, y + 40), name, font(28, "Bold"), (120, 120, 130))
        cv.text((290, y + 90), txt, font(32 if j == 1 else 36, "Black" if j == 1 else "Bold"), INK)


def s_money(cv, t, dur):
    night_street(cv)
    look = (-1, 0) if (t * dur) % 2 < 1 else (1, 0)
    T.character(cv, CX, FEET, SCALE, "worry", "phone", look=look, hoodie=HOOD_DARK, blink=blink_at(t, dur))
    k = ease(seg(t, 0.1, 0.4))
    for j in range(3):
        if k > j / 3:
            T.bill(cv, 690 + j * 30, 1010 - j * 18, 140, 0.4 - j * 0.2)


def s_car(cv, t, dur):
    night_street(cv)
    duck = ease(seg(t, 0.3, 0.5))
    T.character(cv, 300, FEET + 120 * duck, SCALE * 0.95, "shock" if t > 0.3 else "worry", "down",
                hoodie=HOOD_DARK, look=(1, 0))
    x = -700 + 1500 * seg(t, 0.0, 1.0)
    dark_car(cv, x, 1430, 640)


def s_nosleep(cv, t, dur):
    T.bedroom(cv, lights=False)
    cv.overlay((10, 12, 30), 120)
    cv.rect((620, 620, 900, 800), (20, 20, 26), INK, 5, r=14)
    cv.text((760, 735), "03:47", mono(76), (255, 80, 80), "ms")
    T.character(cv, 330, FEET, SCALE * 0.95, "worry", "head", look=(-1, 0), hoodie=HOOD_DARK, blink=False)


def s_phone(cv, t, dur):
    T.bedroom(cv, lights=False)
    cv.overlay((10, 12, 30), 90)
    T.character(cv, CX, FEET + 230, SCALE, "shock", "down", hoodie=HOOD_DARK)
    shake = 8 * math.sin(t * dur * 60) if int(t * dur * 2) % 2 == 0 else 0
    A.phone_ui(cv, 280 + shake, 460, 800 + shake, 1060, "Eingehender Anruf")
    cv.circle(540 + shake, 650, 90, (190, 190, 200))
    cv.text((540 + shake, 820), "Unbekannt", font(60, "Black"), INK, "ms")
    cv.circle(400 + shake, 960, 50, (60, 200, 90))
    cv.circle(680 + shake, 960, 50, RED)


def s_box(cv, t, dur):
    T.bedroom(cv)
    shoebox(cv, 520, 1360, open_k=1.0)
    T.character(cv, 330, FEET, SCALE * 0.9, "worry", "down", look=(1, 1), hoodie=HOOD_DARK, blink=blink_at(t, dur))


def s_pause(cv, t, dur):
    s_box(cv, 0.3, dur)


def kitchen(cv):
    cv.rect((0, 0, W, H), (240, 226, 196))
    for k in range(6):
        cv.rect((60 + k * 160, 300, 200 + k * 160, 520), (200, 160, 120), INK, 4)
    cv.rect((0, 900, W, 960), (180, 140, 100), INK, 4)
    cv.rect((0, 960, W, 1080), (220, 200, 170))
    cv.rect((0, 1080, W, H), (170, 150, 130))
    cv.rect((780, 640, 940, 900), (230, 230, 236), INK, 4)  # fridge-ish


def s_lie(cv, t, dur):
    kitchen(cv)
    talk = abs(math.sin(t * dur * 9)) if t < 0.5 else 0
    mom(cv, 320, FEET, SCALE * 0.85, "worry", talk)
    T.character(cv, 780, FEET, SCALE * 0.85, "closed" if t > 0.6 else "worry", "down", look=(1, 0), hoodie=HOOD_DARK)
    # shiny new sneakers highlight
    cv.glow(780, FEET - 20, 120, (255, 255, 200), 120)


def s_friend(cv, t, dur):
    T.bedroom(cv, lights=False)
    cv.overlay((10, 12, 30), 90)
    T.character(cv, CX, FEET + 230, SCALE, "shock" if t > 0.3 else "worry", "down", hoodie=HOOD_DARK)
    A.phone_ui(cv, 140, 440, 940, 1040, "Chat")
    k = ease(seg(t, 0.05, 0.25))
    if k > 0:
        cv.rect((180, 560, 860, 700), (230, 233, 240), (200, 200, 210), 3, r=26)
        cv.text((210, 645), "Sie haben Deniz geholt.", font(42, "Black"), INK)
    if t > 0.72:
        cv.rect((180, 740, 700, 860), (230, 233, 240), (200, 200, 210), 3, r=26)
        cv.text((210, 815), "Was hat er erzählt?", font(38, "Bold"), (120, 120, 130))


def s_door(cv, t, dur):
    if t < 0.52:  # the bell rings, you stare at the door
        T.bedroom(cv, lights=False)
        cv.overlay((10, 12, 30), 90)
        cv.rect((640, 380, 980, 1250), (110, 80, 60), INK, 6)
        cv.circle(810, 640, 16, (220, 200, 120), INK, 3)
        rings = int(t * dur * 1.6) % 3
        for r_ in range(rings + 1):
            cv.arc((900 - 50 - r_ * 40, 760 - 50 - r_ * 40, 900 + 50 + r_ * 40, 760 + 50 + r_ * 40), 300, 60, YELLOW, 8)
        T.character(cv, 360, FEET, SCALE * 0.95, "shock", "down", hoodie=HOOD_DARK, look=(1, 0))
        return
    cv.rect((0, 0, W, H), (10, 12, 20))
    cv.circle(540, 900, 470, (90, 96, 110))
    on = int(t * dur * 3) % 2 == 0
    cv.glow(540, 520, 400, (60, 110, 255) if on else (220, 40, 50), 120)
    police_officer(cv, 380, 1640, 0.8, "neutral")
    police_officer(cv, 710, 1660, 0.8, "angry")
    ring = Image.new("L", cv.img.size, 0)  # fisheye mask: darken outside the peephole circle
    ImageDraw.Draw(ring).ellipse(cv.s((70, 430, 1010, 1370)), fill=255)
    dark = Image.new("RGB", cv.img.size, (10, 12, 20))
    cv.img = Image.composite(cv.img, dark, ring)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")
    cv.circle(540, 900, 470, None, (40, 40, 46), 30)


def s_final(cv, t, dur):
    T.bedroom(cv, lights=False)
    cv.overlay((10, 12, 30), 110)
    on = int(t * dur * 3) % 2 == 0
    cv.rect((760, 380, 1060, 1250), (110, 80, 60), INK, 6)  # door
    cv.glow(760, 800, 260, (60, 110, 255) if on else (220, 40, 50), 140)
    T.character(cv, 420, FEET + 40, SCALE * 0.9, "sad", "head", hoodie=HOOD_DARK, tear=t > 0.4)
    for (x0, x1), lab, bg, fg in (((60, 480), "LOHNT SICH", WHITE, INK), ((520, 920), "NIEMALS", RED, WHITE)):
        cv.rect((x0, 1330, x1, 1440), bg, INK, 6, r=28)
        cv.text(((x0 + x1) / 2, 1405), lab, font(52, "Black"), fg, "ms")


SCENES = [s_comment, s_money, s_car, s_nosleep, s_phone, s_box, s_pause, s_lie, s_friend, s_door, s_final]
PAUSE = 6


def render(i, t=0.5, dur=5.0):
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur)
    img = cv.final()
    z = 0.04 + 0.12 * ease(t)
    if i in (0, 4, 8, 9, 10):
        z = 0.02 + 0.04 * ease(t)
    img = T.camera(img, z, 540, 820)
    if i == PAUSE:
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, t):
    from script import SEQ
    text, kind = SEQ[i]["chip"]
    if text.startswith("⚠ "):
        text = text[2:]
    return text, kind
