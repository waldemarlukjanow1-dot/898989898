"""Scenes for 'GEH EINFACH ARBEITEN' in STIL 3 (reuses ../reich/style3.py)."""
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reich"))
import style3 as T  # noqa: E402
from style3 import Canvas, font, mono, W, H, ease, seg, INK, WHITE, SKIN, YELLOW  # noqa: E402

CX, FEET, SCALE = 540, 1720, 1.2
BOSS = dict(hoodie=(70, 74, 86), hair=(110, 100, 96), tie=True, bald=True, mustache=True)
RED, GREEN = (220, 40, 50), (40, 140, 70)


def blink_at(t, dur):
    return ((t * dur) % 2.6) < 0.1


def phone_ui(cv, x0, y0, x1, y1, title=None):
    cv.rect((x0 - 16, y0 - 16, x1 + 16, y1 + 16), (24, 24, 30), INK, 6, r=40)
    cv.rect((x0, y0, x1, y1), (245, 247, 250))
    if title:
        cv.rect((x0, y0, x1, y0 + 80), (230, 233, 240))
        cv.text(((x0 + x1) / 2, y0 + 56), title, font(36, "Black"), INK, "ms")


def office(cv, boss_room=False):
    cv.rect((0, 0, W, H), (214, 222, 230) if not boss_room else (196, 186, 170))
    cv.rect((90, 140, 990, 760), (150, 200, 240), INK, 8)  # big window
    for k in range(5):
        x = 120 + k * 180
        cv.rect((x, 420 - (k % 3) * 90, x + 140, 760), (170, 190, 210), (120, 140, 160), 3)
        for wy in range(440 - (k % 3) * 90, 740, 50):
            cv.rect((x + 20, wy, x + 50, wy + 26), (210, 230, 245))
            cv.rect((x + 80, wy, x + 110, wy + 26), (210, 230, 245))
    cv.line([(540, 140), (540, 760)], INK, 8)
    cv.rect((0, 1080, W, H), (160, 160, 170) if not boss_room else (120, 80, 60))
    cv.rect((0, 760, W, 1090), (226, 230, 236) if not boss_room else (210, 198, 180))
    if boss_room:
        cv.rect((700, 820, 900, 1000), (250, 246, 236), INK, 5)  # framed diploma
        cv.text((800, 900), "CHEF", font(40, "Black"), INK, "ms")
        cv.text((800, 950), "DES JAHRES", font(24, "Black"), INK, "ms")


def desk(cv, y=1250, monitor=True):
    cv.rect((40, y, 1040, y + 60), (170, 120, 80), INK, 6, r=10)
    cv.rect((80, y + 60, 120, y + 400), (140, 100, 70), INK, 4)
    cv.rect((960, y + 60, 1000, y + 400), (140, 100, 70), INK, 4)
    if monitor:
        cv.rect((680, y - 260, 980, y - 70), (40, 42, 50), INK, 6, r=12)
        cv.rect((700, y - 240, 960, y - 90), (120, 170, 230))
        cv.rect((805, y - 70, 855, y), (40, 42, 50))
    cv.ellipse((110, y - 150, 230, y - 10), (60, 150, 80), INK, 4)  # plant
    cv.rect((140, y - 40, 200, y), (180, 90, 60), INK, 4)


def payslip(cv, x, y, k=1.0):
    cv.rect((x, y, x + 300, y + 360), (255, 255, 255, int(255 * k)), INK, 5, r=10)
    cv.text((x + 150, y + 50), "LOHNZETTEL", font(30, "Black"), INK, "ms")
    for j in range(4):
        cv.line([(x + 30, y + 90 + j * 45), (x + 270, y + 90 + j * 45)], (200, 200, 210), 6)
    cv.text((x + 150, y + 320), "2.000 €", font(52, "Black"), GREEN, "ms")


# ------------------------------------------------------------------ scenes (cv, t, dur)

def s_comment(cv, t, dur):
    T.bedroom(cv)
    T.character(cv, CX, FEET + 230, SCALE, "angry" if t > 0.45 else "neutral", "down", blink=blink_at(t, dur))
    phone_ui(cv, 140, 440, 940, 1040, "Kommentare")
    for j, (name, txt) in enumerate((("lisa_92", "Krasse Story 😳"), ("user8841", "Geh einfach arbeiten."), ("max.m", "Teil 2?!"))):
        y = 560 + j * 150
        hl = j == 1 and t > 0.2
        cv.rect((170, y, 910, y + 120), (255, 245, 200) if hl else WHITE, (200, 200, 210), 3, r=18)
        cv.circle(230, y + 60, 38, (190, 190, 200))
        cv.text((290, y + 40), name, font(28, "Bold"), (120, 120, 130))
        cv.text((290, y + 90), txt.replace(" 😳", "").replace(" ?!", "?!"), font(38, "Black" if j == 1 else "Bold"), INK)


def s_job(cv, t, dur):
    office(cv)
    desk(cv)
    T.character(cv, CX, FEET, SCALE, "happy", "down", blink=blink_at(t, dur))
    cv.rect((500, 1060, 580, 1150), WHITE, INK, 4, r=8)  # company badge
    cv.line([(510, 960), (540, 1060), (570, 960)], (40, 90, 200), 6)
    k = ease(seg(t, 0.2, 0.5))
    if k > 0:
        payslip(cv, 690, 500 + 120 * (1 - k), k)


COSTS = [("Miete", 900), ("Auto", 300), ("Essen", 400), ("Handy, Strom,\nVersicherung", 200)]


def costs_shown(t):
    return min(4, int(seg(t, 0.05, 0.95) * 4.0 + 0.5) if t > 0.05 else 0)


def s_costs(cv, t, dur):
    office(cv)
    T.character(cv, 380, FEET, SCALE * 0.95, "worry", "down", blink=blink_at(t, dur))
    n = costs_shown(t)
    cv.rect((560, 470, 1010, 1000), WHITE, INK, 6, r=24)
    cv.text((785, 530), "AUSGABEN", font(40, "Black"), INK, "ms")
    for j in range(n):
        lab, val = COSTS[j]
        y = 590 + j * 100
        cv.text((590, y + 40), lab.split("\n")[0], font(34 if "\n" not in lab else 28, "Bold"), INK)
        cv.text((980, y + 40), f"-{val} €", font(38, "Black"), RED, "rs")
    for j in range(n):  # a bill flies away for each cost
        u = min(1.0, max(0.0, (t - j * 0.22 - 0.05) / 0.2))
        if 0 < u < 1:
            T.bill(cv, 420 + 300 * u, 1100 - 500 * u, 150, u * 5)


def remaining(t):
    return 2000 - sum(v for _, v in COSTS[:costs_shown(t)])


def s_200(cv, t, dur):
    office(cv)
    T.character(cv, CX, FEET, SCALE, "sad", "down", blink=blink_at(t, dur))
    for j in range(2):
        T.bill(cv, 380 + j * 320, 1260 - j * 10, 170, -0.2 + j * 0.4)


def s_holiday(cv, t, dur):
    office(cv)
    T.character(cv, CX, FEET + 230, SCALE, "worry", "down", blink=blink_at(t, dur))
    cv.rect((110, 450, 970, 1050), WHITE, INK, 6, r=24)
    cv.rect((110, 450, 970, 530), RED)
    cv.text((540, 510), "DEIN JAHR", font(46, "Black"), WHITE, "ms")
    k = seg(t, 0.15, 0.8)
    for d in range(365):
        c, r = d % 26, d // 26
        x = 140 + c * 31
        y = 555 + r * 34
        free = d % 12 == 0 and d < 360 or d in (200, 201, 202, 203, 204, 205)
        col = (80, 200, 110) if free and d / 365 < k else (226, 228, 234)
        cv.rect((x, y, x + 25, y + 26), col)


def s_boss(cv, t, dur):
    office(cv, boss_room=True)
    T.character(cv, 300, FEET + 40, SCALE * 0.9, "worry", "down", blink=blink_at(t, dur), look=(1, 0))
    talk = abs(math.sin(t * dur * 9)) if t > 0.45 else 0
    T.character(cv, 760, 1560, 0.85, "angry", "down", talk=talk, **BOSS)
    cv.rect((520, 1320, 1080, 1380), (110, 70, 50), INK, 6, r=10)  # boss desk
    cv.rect((540, 1380, 1060, 1700), (90, 56, 40), INK, 6)
    if t < 0.45:  # your speech bubble
        cv.rect((60, 500, 520, 660), WHITE, INK, 5, r=30)
        cv.text((290, 565), "Chef, frei im", font(40, "Black"), INK, "ms")
        cv.text((290, 625), "August?", font(40, "Black"), INK, "ms")
    else:
        cv.rect((560, 500, 1010, 660), WHITE, INK, 5, r=30)
        cv.text((785, 570), "NEIN.", font(60, "Black"), RED, "ms")
        cv.text((785, 630), "Hochsaison.", font(36, "Bold"), INK, "ms")
    if t > 0.7:  # stamp on the request
        k = ease(seg(t, 0.7, 0.8))
        cv.rect((600, 1180, 980, 1310), WHITE, INK, 4)
        cv.text((790, 1220), "Urlaubsantrag", font(28, "Bold"), INK, "ms")
        cv.rect((640, 1230, 940, 1300), (220, 40, 50, int(220 * k)), RED, 5, r=8)
        cv.text((790, 1285), "ABGELEHNT", font(46, "Black"), WHITE, "ms")


def s_pause(cv, t, dur):
    s_boss(cv, 0.9, dur)


def piggy(cv, x, y, s=1.0):
    cv.ellipse((x - 170 * s, y - 120 * s, x + 170 * s, y + 120 * s), (250, 170, 190), INK, 6)
    cv.circle(x + 160 * s, y - 10 * s, 50 * s, (250, 170, 190), INK, 6)
    cv.circle(x + 150 * s, y - 20 * s, 8 * s, INK)
    cv.circle(x + 175 * s, y - 20 * s, 8 * s, INK)
    cv.rect((x - 40 * s, y - 130 * s, x + 40 * s, y - 112 * s), INK, r=6)
    for lx in (-100, -30, 40, 110):
        cv.rect((x + lx * s - 18 * s, y + 100 * s, x + lx * s + 18 * s, y + 160 * s), (250, 170, 190), INK, 5)


def s_years(cv, t, dur):
    office(cv)
    T.character(cv, 300, FEET, SCALE * 0.9, "shock" if t > 0.6 else "worry", "down", blink=blink_at(t, dur))
    piggy(cv, 760, 1180, 0.9)
    k = ease(seg(t, 0.1, 0.9))
    cv.rect((100, 500, 980, 590), WHITE, INK, 6, r=30)
    cv.rect((110, 510, 110 + 860 * k, 580), (80, 200, 110), r=26)
    cv.text((540, 565), f"{int(80000 * k):,} €".replace(",", "."), font(44, "Black"), INK, "ms")
    years = int(33 * k)
    cv.text((760, 860), f"{years} JAHRE", font(80, "Black"), RED, "ms")


def s_old(cv, t, dur):
    office(cv)
    desk(cv)
    T.character(cv, CX, FEET, SCALE, "sad", "down", blink=blink_at(t, dur), hair=(200, 200, 206), specs=True)
    for j in range(5):  # wrinkles
        pass


def s_profile(cv, t, dur):
    T.bedroom(cv, lights=False)
    T.character(cv, CX, FEET + 230, SCALE, "shock" if t > 0.6 else "neutral", "down", blink=blink_at(t, dur))
    phone_ui(cv, 180, 440, 900, 1080, "Profil")
    k = ease(seg(t, 0.35, 0.6))
    cv.circle(540, 700, 150, (220, 222, 230), INK, 5)
    if k > 0:
        T.character(cv, 540, 700 + 150 + 150 * 0.4 * 0 + 520 * 0.5, 0.5, "smug", "down", **BOSS)
        cv.rect((180, 860, 900, 1080), (245, 247, 250))
    cv.text((540, 930), "user8841" if k < 0.5 else "Dein Chef", font(60, "Black"), INK, "ms")
    cv.text((540, 1000), "Kommentar: „Geh einfach arbeiten.“", font(28, "Bold"), (120, 120, 130), "ms")


def s_final(cv, t, dur):
    office(cv)
    desk(cv)
    T.character(cv, 380, FEET, SCALE * 0.95, "worry", "phone", blink=blink_at(t, dur))
    cv.rect((760, 460, 1020, 1090), (190, 220, 240, 180), INK, 6)  # glass door
    T.character(cv, 890, 1560, 0.55, "smug", "down", **BOSS)
    for (x0, x1), lab, bg, fg in (((60, 480), "BLEIBEN", WHITE, INK), ((520, 920), "KÜNDIGEN", RED, WHITE)):
        cv.rect((x0, 1330, x1, 1440), bg, INK, 6, r=28)
        cv.text(((x0 + x1) / 2, 1405), lab, font(52, "Black"), fg, "ms")


SCENES = [s_comment, s_job, s_costs, s_200, s_holiday, s_boss, s_pause, s_years, s_old, s_profile, s_final]
PAUSE = 6


def render(i, t=0.5, dur=5.0):
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur)
    img = cv.final()
    z = 0.04 + 0.12 * ease(t)
    if i in (0, 2, 4, 5, 6, 7, 9, 10):
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
    """Dynamic chip text (counts down in the cost scene)."""
    from script import SEQ
    text, kind = SEQ[i]["chip"]
    if i == 2:
        r = remaining(t)
        text, kind = f"ÜBRIG: {r:,} €".replace(",", "."), ("green" if r > 1000 else "red")
    return text, kind
