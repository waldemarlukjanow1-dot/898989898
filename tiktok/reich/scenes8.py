"""Scenes for 'REICH IN 30 TAGEN' in STIL 3."""
import math

from PIL import Image, ImageDraw

import style3 as T
from style3 import Canvas, font, mono, W, H, ease, seg, INK, WHITE, SKIN, YELLOW

CX = 540
FEET = 1720
SCALE = 1.2


def blink_at(t, dur):
    """Blink about every 2.5 s of scene time."""
    st = t * dur
    return (st % 2.6) < 0.1


def phone_ui(cv, x0, y0, x1, y1, title=None):
    cv.rect((x0 - 16, y0 - 16, x1 + 16, y1 + 16), (24, 24, 30), INK, 6, r=40)
    cv.rect((x0, y0, x1, y1), (245, 247, 250))
    if title:
        cv.rect((x0, y0, x1, y0 + 80), (230, 233, 240))
        cv.text(((x0 + x1) / 2, y0 + 56), title, font(36, "Black"), INK, "ms")


def box(cv, x, y, w, h, stamp=False):
    cv.rect((x, y, x + w, y + h), (200, 150, 90), INK, 5, r=6)
    cv.rect((x + w * 0.42, y, x + w * 0.58, y + h), (220, 180, 120))
    if stamp:
        cv.rect((x + 10, y + h * 0.35, x + w - 10, y + h * 0.65), (220, 40, 50, 230), (160, 20, 30), 4, r=6)
        cv.text((x + w / 2, y + h * 0.58), "RETOURE", font(max(18, int(w / 7)), "Black"), WHITE, "ms")


def car(cv, x, y, w=760):
    h = w * 0.3
    cv.poly([(x, y), (x + w * 0.1, y - h * 0.6), (x + w * 0.35, y - h), (x + w * 0.7, y - h), (x + w * 0.95, y - h * 0.5),
             (x + w, y)], (220, 40, 40), INK, 6)
    cv.poly([(x + w * 0.37, y - h * 0.92), (x + w * 0.62, y - h * 0.92), (x + w * 0.8, y - h * 0.55), (x + w * 0.3, y - h * 0.55)],
            (150, 200, 240), INK, 4)
    for wx in (x + w * 0.2, x + w * 0.8):
        T.S.Canvas  # noqa
        cv.circle(wx, y, h * 0.32, (30, 30, 34), INK, 5)
        cv.circle(wx, y, h * 0.14, (190, 190, 196))


# ------------------------------------------------------------------ scenes (cv, t, dur)

def s_broke(cv, t, dur):
    T.bedroom(cv)
    T.character(cv, CX, FEET, SCALE, "worry", "phone", blink=blink_at(t, dur), talk=0)


def s_crypto(cv, t, dur):
    T.bedroom(cv, lights=False)
    phone_ui(cv, 150, 450, 930, 790, "MOONCOIN")
    k = seg(t, 0.05, 0.9)
    pts = []
    for i in range(int(40 * k) + 1):
        u = i / 40
        v = 0.15 + 0.7 * min(u / 0.6, 1) if u < 0.75 else max(0.02, 0.85 - (u - 0.75) * 4.5)
        pts.append((190 + u * 700, 770 - v * 230))
    if len(pts) > 1:
        cv.line(pts, (40, 180, 80) if k < 0.55 else (220, 40, 50), 10)
    if k > 0.8:
        cv.text((540, 690), "-100 %", font(110, "Black"), (220, 40, 50), "ms")
    mood = "happy" if k < 0.75 else "shock"
    T.character(cv, CX, FEET + 120, SCALE * 0.95, mood, "phone", blink=blink_at(t, dur))


def s_drop(cv, t, dur):
    T.bedroom(cv)
    T.character(cv, CX, FEET, SCALE, "worry" if t > 0.4 else "neutral", "head" if t > 0.6 else "phone",
                blink=blink_at(t, dur))
    n = int(ease(seg(t, 0, 0.6)) * 10)
    spots = [(40, 1300), (210, 1330), (60, 1150), (780, 1300), (900, 1330), (820, 1150), (-20, 1000), (900, 1000),
             (120, 1460), (800, 1460)]
    for k, (x, y) in enumerate(spots[:n]):
        box(cv, x, y, 200, 160, stamp=t > 0.68 + k * 0.025)


def s_guru(cv, t, dur):
    T.bedroom(cv)
    if t < 0.78:
        phone_ui(cv, 160, 470, 920, 1180, "@reich.in.30.tagen")
        cv.rect((180, 560, 900, 1160), (120, 190, 240))
        cv.rect((180, 1000, 900, 1160), (90, 90, 96))
        car(cv, 260, 1110, 560)
        T.character(cv, 680, 1130, 0.42, "smug", "point", glasses=True, chain=True, hoodie=(30, 30, 36))
        cv.rect((200, 590, 880, 680), (0, 0, 0, 150), r=10)
        cv.text((540, 655), "REICH IN 30 TAGEN", font(52, "Black"), YELLOW, "ms")
    else:
        T.character(cv, CX, FEET, SCALE, "worry", "phone", blink=blink_at(t, dur))
        k = seg(t, 0.78, 1.0)
        for j in range(3):  # last bills fly into the phone
            u = max(0.0, min(1.0, k * 1.6 - j * 0.25))
            if 0 < u < 1:
                T.bill(cv, 150 + (680 - 150) * u, 1350 - (1350 - 1020) * u, 150 * (1 - 0.6 * u), u * 3)


def s_pause(cv, t, dur):
    T.bedroom(cv)
    T.character(cv, CX, FEET, SCALE, "closed", "down", look=(1, 0))


def s_lesson(cv, t, dur):
    T.bedroom(cv, lights=False)
    cv.rect((120, 450, 960, 900), (40, 42, 50), INK, 8, r=24)
    cv.rect((150, 480, 930, 870), (245, 247, 250))
    cv.rect((150, 480, 930, 570), (60, 120, 220))
    cv.text((540, 542), "REICH IN 30 TAGEN – KURS", font(40, "Black"), WHITE, "ms")
    cv.rect((190, 620, 890, 760), (230, 245, 230), (40, 150, 70), 4, r=16)
    cv.text((220, 670), "KAPITEL 1", font(32, "Black"), (40, 150, 70))
    cv.text((220, 730), "Verkauf diesen Kurs weiter.", font(42, "Bold"), INK)
    for j in range(1):
        cv.rect((190, 790 + j * 90, 890, 860 + j * 90), (238, 238, 242), (200, 200, 210), 3, r=16)
        cv.text((540, 840 + j * 90), "– leer –", font(30, "Bold"), (170, 170, 180), "ms")
    T.character(cv, CX, FEET + 230, SCALE * 0.95, "shock", "down", blink=blink_at(t, dur))


def s_newguru(cv, t, dur):
    for y in range(0, 1100, 6):
        k = y / 1100
        cv.rect((0, y, W, y + 6), (int(120 + 110 * k), int(190 + 40 * k), 250))
    cv.circle(860, 320, 80, (255, 230, 120))
    cv.rect((0, 1100, W, H), (150, 150, 156))
    cv.rect((0, 1080, W, 1110), (200, 200, 206), INK, 3)
    car(cv, 40, 1250, 700)
    T.character(cv, 680, FEET, SCALE * 0.95, "smug", "point", glasses=True, chain=True, hoodie=(30, 30, 36),
                bob=-8 * abs(math.sin(t * 8)))
    # phone on tripod
    cv.line([(160, 1560), (230, 1300), (300, 1560)], INK, 8)
    cv.line([(230, 1300), (230, 1560)], INK, 8)
    cv.rect((180, 1180, 280, 1310), (30, 30, 36), INK, 4, r=12)
    cv.circle(230, 1205, 10, (220, 40, 50))


def s_rich(cv, t, dur):
    T.bedroom(cv)
    T.falling_money(cv, t * dur / 3, n=16)
    T.character(cv, CX, FEET, SCALE, "rich", "up", blink=blink_at(t, dur), bob=-14 * abs(math.sin(t * dur * 4)))
    T.money_pile(cv, 1460)


def night(cv):
    T.bedroom(cv, lights=False)
    cv.overlay((10, 12, 30), 140)


def wallet_phone(cv, x0=70, y0=440, x1=590, y1=1000):
    phone_ui(cv, x0, y0, x1, y1, "KRYPTO-WALLET")


def lock_icon(cv, x, y, s=1.0, col=(220, 40, 50)):
    cv.arc((x - 70 * s, y - 150 * s, x + 70 * s, y + 10 * s), 180, 360, INK, int(34 * s))
    cv.arc((x - 70 * s, y - 150 * s, x + 70 * s, y + 10 * s), 180, 360, (170, 170, 180), int(24 * s))
    cv.rect((x - 110 * s, y - 70 * s, x + 110 * s, y + 110 * s), col, INK, 6, r=int(20 * s))
    cv.circle(x, y + 10 * s, 22 * s, INK)
    cv.rect((x - 8 * s, y + 10 * s, x + 8 * s, y + 60 * s), INK)


def s_wallet(cv, t, dur):
    T.bedroom(cv)
    T.character(cv, 790, FEET, SCALE * 0.85, "happy" if t < 0.6 else "smug", "point", blink=blink_at(t, dur))
    wallet_phone(cv)
    k = ease(seg(t, 0.05, 0.5))
    cv.text((330, 640), f"{int(9970000 * k):,} €".replace(",", "."), font(54, "Black"), (40, 140, 70), "ms")
    for j in range(4):  # bills flying into the wallet
        u = max(0.0, min(1.0, t * 2.2 - j * 0.25))
        if 0 < u < 1:
            T.bill(cv, 700 - 380 * u + j * 30, 1300 - 650 * u, 140 * (1 - 0.5 * u), u * 4)
    if t > 0.55:
        cv.rect((110, 760, 550, 850), WHITE, (180, 180, 190), 4, r=16)
        n = min(10, int(seg(t, 0.55, 0.9) * 10) + 1)
        cv.text((140, 805), "•" * n, font(60, "Black"), INK, "lm")
        cv.text((330, 900), "Passwort", font(30, "Bold"), (120, 120, 130), "ms")


def s_password(cv, t, dur):
    night(cv)
    tries = 2 if t < 0.56 else (1 if t < 0.72 else 0)
    locked = tries == 0
    wrong = t >= 0.2
    T.character(cv, 790, FEET, SCALE * 0.85, "shock" if locked else "worry", "head" if locked else "down", blink=blink_at(t, dur))
    wallet_phone(cv)
    if not locked:
        cv.rect((110, 560, 550, 650), WHITE, (220, 40, 50) if wrong else (180, 180, 190), 6, r=16)
        cv.text((140, 605), "•" * min(8, int(t * 60) + 1), font(60, "Black"), INK, "lm")
        if wrong:
            cv.text((330, 740), "PASSWORT FALSCH", font(44, "Black"), (220, 40, 50), "ms")
            cv.text((330, 820), f"Noch {tries} Versuch" + ("e" if tries != 1 else ""), font(40, "Bold"), INK, "ms")
    else:
        lock_icon(cv, 330, 720, 1.1)
        cv.text((330, 940), "GESPERRT", font(62, "Black"), (220, 40, 50), "ms")


def s_final(cv, t, dur):
    T.bedroom(cv)
    T.money_pile(cv, 1100, seed=5, n=60)
    for k in range(9):  # bars of a vault in front of the money
        cv.rect((60 + k * 120, 820, 84 + k * 120, 1300), (150, 150, 160), INK, 4)
    cv.rect((40, 800, 1040, 840), (150, 150, 160), INK, 4)
    lock_icon(cv, 890, 1010, 0.9)
    T.character(cv, CX, FEET + 60, SCALE * 0.9, "sad", "down", tear=t > 0.3, blink=blink_at(t, dur))
    for (x0, x1), lab, bg, fg in (((60, 500), "WEITER RATEN", WHITE, INK), ((530, 920), "NEU ANFANGEN", (40, 120, 60), YELLOW)):
        cv.rect((x0, 1330, x1, 1440), bg, INK, 6, r=28)
        cv.text(((x0 + x1) / 2, 1405), lab, font(46, "Black"), fg, "ms")


SCENES = [s_broke, s_crypto, s_drop, s_guru, s_pause, s_lesson, s_newguru, s_rich, s_wallet, s_password, s_final]
PAUSE = 4
FOCUS = {i: (540, 820) for i in range(11)}


def render(i, t=0.5, dur=5.0):
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur)
    img = cv.final()
    z = 0.04 + 0.14 * ease(t)  # wide -> closer, like the reference
    if i in (1, 5, 8, 9, 10):  # scenes with screens/buttons: gentle zoom only
        z = 0.02 + 0.05 * ease(t)
    img = T.camera(img, z, *FOCUS[i])
    if i == PAUSE:
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img
