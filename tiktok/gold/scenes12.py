"""Scenes for 'LAGER 17' (STIL 3, new main character T.HERO). All UI centred on x=500 (safe centre)."""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "reich"))
import style3 as T  # noqa: E402
from style3 import Canvas, font, mono, W, H, ease, seg, INK, WHITE, SKIN, YELLOW  # noqa: E402

UX, CX, FEET, SCALE = 500, 540, 1720, 1.2
RED = (220, 40, 50)
GOLD, GOLD_D, GOLD_L = (245, 190, 40), (190, 130, 20), (255, 236, 150)
PX0, PY0, PX1, PY1 = 170, 500, 830, 1160


def hero(cv, x, y, s, mood, arms="down", **kw):
    return T.character(cv, x, y, s, mood, arms, **dict(T.HERO, **kw))


def blink_at(t, dur):
    return ((t * dur) % 2.6) < 0.1


def text_w(txt, f):
    return T.S.ImageFont.truetype(f.path, f.size).getlength(txt)


# ------------------------------------------------------------------ props

def gold_bar(cv, x, y, w=150, h=60, shine=0.0):
    cv.poly([(x + w * 0.12, y), (x + w * 0.88, y), (x + w, y + h), (x, y + h)], GOLD, INK, 4)
    cv.poly([(x + w * 0.18, y + h * 0.12), (x + w * 0.82, y + h * 0.12), (x + w * 0.76, y + h * 0.4),
             (x + w * 0.24, y + h * 0.4)], GOLD_L)
    cv.text((x + w / 2, y + h * 0.88), "999,9", font(max(12, int(h * 0.32)), "Black"), GOLD_D, "ms")
    if shine > 0:
        sx = x + w * (0.1 + 0.8 * shine)
        cv.line([(sx, y + 4), (sx - 14, y + h - 4)], (255, 255, 255, 180), 6)


def gold_stack(cv, x, y, rows=4, per=3, w=150, h=60, t=0.0):
    for r_ in range(rows):
        n = per - (r_ % 2)
        off = (w * 0.5) * (r_ % 2)
        for k in range(n):
            gold_bar(cv, x + off + k * w, y - r_ * (h - 6), w, h, shine=(t * 1.5 + k * 0.2 + r_ * 0.1) % 1.0)


def sparkles(cv, t, cx, cy, n=10, rad=300, seed=3):
    rnd = random.Random(seed)
    for _ in range(n):
        a = rnd.uniform(0, 6.28)
        d = rnd.uniform(0.3, 1) * rad
        ph = (t * 2 + rnd.random()) % 1.0
        s = 18 * math.sin(math.pi * ph)
        px, py = cx + math.cos(a) * d, cy + math.sin(a) * d * 0.6
        cv.poly([(px, py - s), (px + s * 0.3, py), (px, py + s), (px - s * 0.3, py)], (255, 250, 210))
        cv.poly([(px - s, py), (px, py - s * 0.3), (px + s, py), (px, py + s * 0.3)], (255, 250, 210))


def safe(cv, x, y, w=420, h=460, open_k=0.0, inner=None):
    cv.rect((x, y, x + w, y + h), (90, 96, 104), INK, 7, r=18)
    cv.rect((x + 25, y + 25, x + w - 25, y + h - 25), (40, 40, 46), INK, 4, r=10)
    if inner:
        inner(x + 25, y + 25, x + w - 25, y + h - 25)
    if open_k < 1:  # door swings open to the left (gets narrower)
        dw = (w - 50) * (1 - open_k)
        cv.rect((x + 25, y + 25, x + 25 + dw, y + h - 25), (120, 126, 134), INK, 5, r=10)
        if dw > 120:
            cx_, cy_ = x + 25 + dw * 0.55, y + h / 2
            cv.circle(cx_, cy_, 60, (170, 176, 184), INK, 5)
            for k in range(12):
                a = math.radians(k * 30)
                cv.line([(cx_ + math.cos(a) * 44, cy_ + math.sin(a) * 44), (cx_ + math.cos(a) * 56, cy_ + math.sin(a) * 56)], INK, 4)
            cv.rect((cx_ + 90, cy_ - 12, cx_ + 140, cy_ + 12), (170, 176, 184), INK, 4, r=6)


def storage_hall(cv):
    cv.rect((0, 0, W, H), (196, 200, 206))
    cv.rect((0, 1150, W, H), (150, 152, 158))
    for k in range(3):
        x0 = 30 + k * 350
        cv.rect((x0, 430, x0 + 320, 1150), (120, 130, 150), INK, 5)
        for j in range(14):
            cv.line([(x0 + 10, 470 + j * 48), (x0 + 310, 470 + j * 48)], (100, 110, 130), 4)
        cv.rect((x0 + 80, 380, x0 + 240, 430), (250, 214, 10) if k == 1 else (230, 230, 236), INK, 4, r=8)
        cv.text((x0 + 160, 420), ("LAGER 16", "LAGER 17", "LAGER 18")[k], font(30, "Black"), INK, "ms")


def dusty_unit(cv):
    cv.rect((0, 0, W, H), (70, 64, 60))
    cv.rect((0, 1150, W, H), (96, 88, 80))
    cv.poly([(0, 0), (120, 330), (120, 1150), (0, 1300)], (60, 54, 50))
    cv.poly([(W, 0), (960, 330), (960, 1150), (W, 1300)], (60, 54, 50))
    for (x, y, w, h) in ((150, 900, 220, 180), (180, 760, 170, 140), (760, 940, 200, 160)):
        cv.rect((x, y, x + w, y + h), (180, 140, 90), INK, 4, r=6)
        cv.rect((x + w * 0.4, y, x + w * 0.6, y + h), (200, 165, 115))
    cv.circle(830, 870, 60, None, INK, 6)  # broken bike
    cv.circle(950, 880, 60, None, INK, 6)
    cv.line([(830, 870), (880, 800), (950, 880), (830, 870)], (180, 40, 40), 6)
    rnd = random.Random(1)
    for _ in range(40):
        cv.circle(rnd.uniform(0, W), rnd.uniform(300, 1300), rnd.uniform(2, 5), (220, 210, 190, 120))


def bedroom_night(cv):
    T.bedroom(cv, lights=False)
    cv.overlay((10, 12, 30), 110)


# ------------------------------------------------------------------ scenes (cv, t, dur)

def s_auction(cv, t, dur):
    storage_hall(cv)
    # auctioneer with hammer (left)
    hero_kw = dict(hoodie=(60, 60, 70), hair=(150, 150, 156), hair_style="fringe", outfit="hoodie", mustache=False, goatee=False)
    T.character(cv, 230, 1640, 0.75, "neutral", "point", talk=abs(math.sin(t * dur * 8)) if t < 0.6 else 0,
                **{k: v for k, v in hero_kw.items()})
    if t > 0.45:  # hammer down
        k = ease(seg(t, 0.45, 0.55))
        cv.rect((330, 760 + 60 * k, 420, 800 + 60 * k), (120, 70, 40), INK, 4, r=8)
        cv.line([(375, 800 + 60 * k), (330, 880)], (120, 70, 40), 12)
        if k >= 1:
            cv.text((380, 720), "VERKAUFT!", font(56, "Black"), RED, "ms")
    hero(cv, 720, FEET, SCALE * 0.9, "happy" if t > 0.5 else "neutral", "up" if 0.2 < t < 0.5 else "down",
         blink=blink_at(t, dur))


def s_safe_found(cv, t, dur):
    dusty_unit(cv)
    k = ease(seg(t, 0.0, 0.5))
    layer = Image.new("L", cv.img.size, 0)  # spotlight on the safe
    ImageDraw.Draw(layer).ellipse(cv.s((UX - 330, 520, UX + 330, 1250)), fill=int(255 * k))
    cv.img = Image.composite(cv.img, Image.blend(cv.img, Image.new("RGB", cv.img.size, (0, 0, 0)), 0.55), layer)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")
    safe(cv, UX - 210, 640, 420, 460)
    hero(cv, 880, FEET + 80, SCALE * 0.75, "shock", "head", look=(-1, 0))


def s_gold(cv, t, dur):
    dusty_unit(cv)
    day = 1 + min(2, int(seg(t, 0.05, 0.45) * 3))
    open_k = ease(seg(t, 0.45, 0.6))

    def inner(a, b, c, d):
        if open_k > 0:
            for r_ in range(4):
                for k in range(3):
                    gold_bar(cv, a + 15 + k * 115, d - 60 - r_ * 52, 110, 50, shine=(t * 2 + k * 0.3) % 1)
    safe(cv, UX - 210, 600, 420, 460, open_k, inner)
    if open_k > 0:
        cv.glow(UX, 830, 420 * open_k, GOLD, int(150 * open_k))
        sparkles(cv, t * dur / 3, UX, 830, 12, 320)
    if t < 0.45:
        cv.rect((UX - 110, 480, UX + 110, 560), WHITE, INK, 5, r=16)
        cv.text((UX, 538), f"TAG {day}", font(50, "Black"), INK, "ms")
    hero(cv, 860, FEET + 60, SCALE * 0.75, "shock" if open_k > 0.5 else "worry", "down", blink=blink_at(t, dur))


def s_laugh(cv, t, dur):
    T.bedroom(cv)
    cv.glow(300, 1300, 360, GOLD, 120)
    gold_stack(cv, 60, 1380, rows=4, per=3, w=150, h=60, t=t)
    sparkles(cv, t * dur / 3, 300, 1250, 8, 260)
    laughing = t < 0.4
    hero(cv, 680, FEET, SCALE, "happy" if laughing else "worry", "up" if laughing else "head",
         talk=abs(math.sin(t * dur * 10)) if laughing else 0, bob=-12 * abs(math.sin(t * dur * 6)) if laughing else 0)


def s_sell(cv, t, dur):
    cv.rect((0, 0, W, H), (232, 222, 200))
    cv.rect((60, 450, 940, 545), (40, 40, 46), INK, 5, r=10)
    cv.text((UX, 522), "GOLDANKAUF", font(70, "Black"), GOLD, "ms")
    cv.rect((0, 1150, W, H), (150, 120, 90))
    # dealer behind the counter
    T.character(cv, 300, 1380, 0.8, "neutral", "point", talk=abs(math.sin(t * dur * 8)) if t < 0.7 else 0,
                hoodie=(70, 70, 80), hair=(90, 90, 96), outfit="hoodie", hair_style="fringe", specs=True, tie=True)
    cv.rect((0, 1120, W, 1180), (120, 90, 60), INK, 5)
    cv.rect((0, 1180, W, 1400), (100, 74, 50), INK, 5)
    gold_bar(cv, 160, 1060, 160, 62)
    # form
    k = ease(seg(t, 0.25, 0.45))
    if k > 0:
        cv.rect((560, 580 + 40 * (1 - k), 940, 1060), WHITE, INK, 5, r=10)
        cv.text((750, 640), "FORMULAR", font(36, "Black"), INK, "ms")
        cv.text((590, 710), "Name: ______", font(32, "Bold"), INK)
        cv.text((590, 780), "Ausweis-Nr.: ___", font(32, "Bold"), INK)
        cv.text((590, 870), "HERKUNFT:", font(36, "Black"), RED)
        cv.rect((590, 900, 910, 980), (255, 240, 240), RED, 4, r=8)
        if t > 0.75:
            cv.text((750, 960), "???", font(50, "Black"), RED, "ms")


def s_hide(cv, t, dur):
    bedroom_night(cv)
    cv.rect((60, 1180, 1020, 1420), (60, 90, 170), INK, 7, r=24)  # bed in front
    cv.rect((60, 1420, 1020, 1470), (90, 60, 40), INK, 6)
    cv.glow(540, 1500, 380, GOLD, int(110 + 40 * math.sin(t * 12)))
    for k in range(5):
        gold_bar(cv, 120 + k * 160, 1470, 150, 50)
    cv.rect((300, 420, 560, 520), (20, 20, 26), INK, 5, r=14)
    cv.text((430, 498), "03:12", mono(70), (255, 80, 80), "ms")
    hero(cv, 540, 1240, 0.75, "worry", "down", blink=False, look=(0, 1))


def s_keep(cv, t, dur):
    T.bedroom(cv)
    cv.rect((PX0 - 18, PY0 - 18, PX1 + 18, PY1 + 18), (24, 24, 30), INK, 6, r=46)
    cv.rect((PX0, PY0, PX1, PY1), (245, 247, 250))
    if t < 0.3:
        cv.text((UX, PY0 + 90), "Eingehender Anruf", font(38, "Bold"), (120, 120, 130), "ms")
        cv.circle(UX, PY0 + 270, 110, (190, 190, 200))
        cv.text((UX, PY0 + 480), "Auktionshaus", font(64, "Black"), INK, "ms")
        cv.circle(UX - 170, PY1 - 110, 60, (60, 200, 90))
        cv.circle(UX + 170, PY1 - 110, 60, RED)
    else:
        cv.text((UX, PY0 + 90), "Auktionshaus · 00:14", font(36, "Bold"), (120, 120, 130), "ms")
        cv.circle(UX, PY0 + 260, 100, (190, 190, 200))
        k = ease(seg(t, 0.35, 0.5))
        cv.rect((PX0 + 40, PY0 + 400, PX1 - 40, PY0 + 600), (228, 231, 238, int(255 * k)), None, 0, r=30)
        cv.text((UX, PY0 + 480), "Ein Mann fragt,", font(42, "Black"), INK, "ms")
        cv.text((UX, PY0 + 550), "wer LAGER 17 hat.", font(42, "Black"), RED, "ms")


def s_note_find(cv, t, dur):
    dusty_unit(cv)
    cv.glow(UX, 860, 360, GOLD, 90)

    def inner(a, b, c, d):
        lift = ease(seg(t, 0.3, 0.6)) * 120
        gold_bar(cv, a + 130, d - 70 - lift, 110, 50)
        if lift > 60:
            cv.poly([(a + 120, d - 40), (a + 250, d - 50), (a + 255, d - 10), (a + 125, d - 4)], (250, 246, 230), INK, 3)
    safe(cv, UX - 210, 600, 420, 460, 1.0, inner)
    hero(cv, 860, FEET + 60, SCALE * 0.75, "shock" if t > 0.6 else "neutral", "down")


def s_note(cv, t, dur):
    cv.rect((0, 0, W, H), (60, 54, 50))
    cv.poly([(130, 500), (880, 470), (900, 1120), (150, 1150)], (250, 244, 225), INK, 6)
    for k in range(9):
        cv.line([(170, 560 + k * 64), (860, 545 + k * 64)], (210, 205, 190), 3)
    f = font(50, "Black")
    lines = ["Wer das findet,", "hat 24 Stunden,", "um es zurück-", "zubringen."]
    for k, l in enumerate(lines):
        if t > 0.1 + k * 0.15:
            cv.text((200, 640 + k * 110), l, f, (40, 30, 30))
    if t > 0.75:
        cv.text((720, 1080), "– L.17", font(40, "Black"), RED)


def s_final(cv, t, dur):
    bedroom_night(cv)
    # black car seen through the window, headlights on
    cv.rect((120, 640, 560, 800), (16, 16, 20), INK, 5, r=30)
    cv.rect((190, 580, 480, 660), (16, 16, 20), INK, 5, r=20)
    cv.rect((540, 690, 570, 720), (255, 250, 200))
    cv.poly([(570, 700), (760, 650), (760, 770)], (255, 250, 200, 60))
    for wx in (200, 480):
        cv.circle(wx, 800, 34, (8, 8, 10), INK, 4)
    hero(cv, 740, FEET, SCALE * 0.9, "worry", "phone", look=(-1, 0), blink=blink_at(t, dur))
    xs = [(40, 330, "VERKAUFEN"), (345, 655, "VERSTECKEN"), (670, 940, "BEHALTEN")]
    cols = [(40, 120, 60), WHITE, RED]
    for (x0, x1, lab), bg in zip(xs, cols):
        cv.rect((x0, 1330, x1, 1440), bg, INK, 6, r=24)
        f = font(40, "Black")
        cv.text(((x0 + x1) / 2, 1402), lab, f, YELLOW if bg == (40, 120, 60) else (INK if bg == WHITE else WHITE), "ms")


SCENES = [s_auction, s_safe_found, s_gold, s_laugh, s_sell, s_hide, s_keep, s_keep, s_note_find, s_note, s_final]
PAUSE = 7
UI_SCENES = (4, 6, 7, 9, 10)


def render(i, t=0.5, dur=5.0):
    cv = Canvas((0, 0, 0))
    if i == PAUSE:
        SCENES[i](cv, 1.0, dur)
    else:
        SCENES[i](cv, t, dur)
    img = cv.final()
    if i in UI_SCENES:
        z, cx, cy = 0.0, 500, 810
    else:
        z, cx, cy = 0.03 + 0.1 * ease(t), 540, 860
    img = T.camera(img, z, cx, cy)
    if i == PAUSE:
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, t):
    from script import SEQ
    return SEQ[i]["chip"]
