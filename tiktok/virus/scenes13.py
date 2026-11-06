"""Scenes for 'DAS NEUE VIRUS' (STIL 3, T.HERO). UI centred on x=500."""
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
RED, GREEN = (220, 40, 50), (40, 140, 70)
PX0, PY0, PX1, PY1 = 170, 500, 830, 1160
EXTRAS = [dict(hoodie=c, hair=h, outfit="hoodie", hair_style="fringe") for c, h in
          (((180, 70, 70), (90, 60, 40)), ((70, 120, 180), (40, 30, 26)), ((200, 160, 60), (120, 80, 50)),
           ((120, 80, 150), (60, 40, 30)), ((90, 150, 120), (150, 150, 150)))]


def hero(cv, x, y, s, mood, arms="down", **kw):
    return T.character(cv, x, y, s, mood, arms, **dict(T.HERO, **kw))


def blink_at(t, dur):
    return ((t * dur) % 2.6) < 0.1


def text_w(txt, f):
    return T.S.ImageFont.truetype(f.path, f.size).getlength(txt)


def phone(cv, title, shake=0.0):
    cv.rect((PX0 - 18 + shake, PY0 - 18, PX1 + 18 + shake, PY1 + 18), (24, 24, 30), INK, 6, r=46)
    cv.rect((PX0 + shake, PY0, PX1 + shake, PY1), (245, 247, 250))
    cv.rect((PX0 + shake, PY0, PX1 + shake, PY0 + 90), (230, 233, 240))
    cv.text((UX + shake, PY0 + 60), title, font(38, "Black"), INK, "ms")


def bubble(cv, x0, y, txt, f, left=True, maxw=520, col=(228, 231, 238), fg=INK):
    lines, cur = [], ""
    for w_ in txt.split():
        trial = (cur + " " + w_).strip()
        if text_w(trial, f) > maxw and cur:
            lines.append(cur)
            cur = w_
        else:
            cur = trial
    lines.append(cur)
    bw = max(text_w(l, f) for l in lines) + 56
    bh = 30 + (f.size + 12) * len(lines)
    if not left:
        x0 = x0 - bw
    cv.rect((x0, y, x0 + bw, y + bh), col, r=30)
    for k, l in enumerate(lines):
        cv.text((x0 + 28, y + 15 + k * (f.size + 12)), l, f, fg)
    return y + bh


# ------------------------------------------------------------------ scenes (cv, t, dur)

def s_news(cv, t, dur):
    T.bedroom(cv, night=False)
    sh = 6 * math.sin(t * dur * 50) if t < 0.25 else 0
    phone(cv, "Mitteilungen", sh)
    f = font(34, "Black")
    items = [("EILMELDUNG", "Neues Virus entdeckt"), ("EILMELDUNG", "Fälle verdoppeln sich täglich"),
             ("NEWS", "Regierung berät Maßnahmen"), ("NEWS", "Krankenhäuser in Alarmbereitschaft")]
    y = PY0 + 120
    for k, (tag, txt) in enumerate(items):
        if t > 0.05 + k * 0.15:
            cv.rect((PX0 + 25 + sh, y, PX1 - 25 + sh, y + 115), WHITE, (210, 210, 220), 3, r=18)
            cv.rect((PX0 + 45 + sh, y + 14, PX0 + 45 + sh + text_w(tag, font(22, "Black")) + 24, y + 46), RED, r=8)
            cv.text((PX0 + 57 + sh, y + 18), tag, font(22, "Black"), WHITE)
            cv.text((PX0 + 45 + sh, y + 62), txt, font(30, "Black"), INK)
            y += 130


def shelf(cv, x, y, w, h, empty=True):
    cv.rect((x, y, x + w, y + h), (230, 230, 236), INK, 5)
    for k in range(4):
        yy = y + 40 + k * (h - 60) / 4
        cv.rect((x + 10, yy + 70, x + w - 10, yy + 82), (180, 180, 190))
        if not empty or (k == 3 and x < 300):
            cv.rect((x + 30, yy + 20, x + 90, yy + 70), (240, 200, 80), INK, 3)


def s_market(cv, t, dur):
    cv.rect((0, 0, W, H), (240, 236, 226))
    cv.rect((60, 480, 940, 570), (40, 140, 70), INK, 5, r=10)
    cv.text((UX, 548), "SUPERMARKT", font(60, "Black"), WHITE, "ms")
    cv.rect((0, 1200, W, H), (200, 196, 186))
    shelf(cv, 40, 610, 300, 540)
    shelf(cv, 660, 610, 300, 540)
    k = math.sin(t * dur * 6) * 20
    T.character(cv, 360, 1640, 0.75, "angry", "point", **EXTRAS[0])
    T.character(cv, 720, 1640, 0.75, "angry", "point", **EXTRAS[1])
    cv.rect((520 + k - 40, 1000, 520 + k + 40, 1150), (120, 200, 240), INK, 4, r=10)
    cv.rect((520 + k - 20, 970, 520 + k + 20, 1000), WHITE, INK, 3)


def bus(cv):
    cv.rect((0, 0, W, H), (190, 210, 220))
    cv.rect((0, 300, W, 1180), (240, 200, 60), INK, 6)
    for k in range(3):
        cv.rect((40 + k * 340, 360, 340 + k * 340, 720), (170, 210, 235), INK, 5, r=14)
    cv.rect((0, 1180, W, H), (120, 120, 128))
    cv.line([(0, 860), (W, 860)], (150, 150, 160), 10)


def s_mask(cv, t, dur):
    bus(cv)
    for k, x in enumerate((120, 880)):
        T.character(cv, x, 1500, 0.6, "neutral", "down", facemask=True, **EXTRAS[k + 2])
    on = t > 0.25
    hero(cv, CX, FEET, SCALE, "worry", "down" if on else "phone", facemask=on, blink=blink_at(t, dur))


def s_curfew(cv, t, dur):
    for y in range(0, 1100, 6):
        k = y / 1100
        cv.rect((0, y, W, y + 6), (int(18 + 20 * k), int(22 + 22 * k), int(48 + 30 * k)))
    rnd = random.Random(5)
    x = -20
    while x < W:
        bw, bh = rnd.randint(160, 260), rnd.randint(420, 700)
        cv.rect((x, 1100 - bh, x + bw, 1100), (46, 52, 80), INK, 4)
        for wy in range(1100 - bh + 40, 1060, 90):
            for wx in range(x + 30, x + bw - 50, 70):
                cv.rect((wx, wy, wx + 40, wy + 56), (255, 214, 120) if rnd.random() < 0.35 else (30, 34, 56))
        x += bw + 10
    cv.rect((0, 1100, W, H), (50, 52, 60))
    cv.rect((380, 520, 620, 620), (20, 20, 26), INK, 5, r=14)
    cv.text((UX, 595), "22:00", mono(76), (255, 80, 80), "ms")
    px = -500 + 1600 * t
    cv.rect((px, 1260, px + 460, 1380), (240, 242, 244), INK, 5, r=26)
    cv.rect((px + 110, 1200, px + 340, 1262), (240, 242, 244), INK, 4, r=14)
    cv.rect((px, 1300, px + 460, 1328), (40, 120, 90))
    cv.text((px + 230, 1365), "POLIZEI", font(34, "Black"), (40, 120, 90), "ms")
    on = int(t * dur * 4) % 2 == 0
    cv.rect((px + 190, 1180, px + 260, 1200), (60, 110, 255) if on else (30, 50, 120))
    if on:
        cv.glow(px + 225, 1190, 90, (60, 110, 255), 140)
    for wx in (px + 90, px + 370):
        cv.circle(wx, 1380, 40, (20, 20, 22), INK, 4)


def icon_box(cv, x, y, label, crossed):
    cv.rect((x, y, x + 180, y + 180), WHITE, INK, 4, r=20)
    cv.text((x + 90, y + 115), label[0], font(90, "Black"), INK, "ms")
    cv.text((x + 90, y + 230), label, font(28, "Black"), INK, "ms")
    if crossed:
        cv.line([(x + 10, y + 10), (x + 170, y + 170)], RED, 12)
        cv.line([(x + 170, y + 10), (x + 10, y + 170)], RED, 12)


def s_letter(cv, t, dur):
    T.bedroom(cv, night=False)
    cv.rect((130, 470, 870, 1180), (250, 246, 236), INK, 6, r=12)
    cv.text((UX, 560), "AMTLICHES SCHREIBEN", font(36, "Black"), (120, 120, 130), "ms")
    cv.rect((170, 600, 830, 690), RED, r=10)
    cv.text((UX, 663), "IMPFNACHWEIS ERFORDERLICH", font(40, "Black"), WHITE, "ms")
    labels = ["RESTAURANT", "KINO", "FITNESS"]
    for k, lab in enumerate(labels):
        icon_box(cv, 170 + k * 230, 760, lab, t > (0.4, 0.66, 0.78)[k])


def s_boss(cv, t, dur):
    T.bedroom(cv, night=False)
    phone(cv, "Chef")
    f = font(38, "Bold")
    y = PY0 + 130
    if t > 0.1:
        y = bubble(cv, PX0 + 30, y, "Ohne Nachweis brauchst du gar nicht mehr zu kommen.", f) + 24
    if t > 0.7:
        cv.text((PX0 + 40, y + 20), "Gelesen 07:42", font(26, "Bold"), (140, 140, 150))


def s_pause(cv, t, dur):
    s_boss(cv, 1.0, dur)


def s_family(cv, t, dur):
    cv.rect((0, 0, W, H), (236, 220, 196))
    cv.rect((0, 1100, W, H), (170, 130, 100))
    cv.rect((60, 1180, 1020, 1260), (140, 90, 60), INK, 6, r=12)
    for k, (x, ex) in enumerate(((180, 0), (420, 1), (660, 2), (890, 3))):
        T.character(cv, x, 1520, 0.5, "angry", "point" if k % 2 else "down",
                    talk=abs(math.sin(t * dur * (8 + k))), **EXTRAS[ex])
    for k, (x, y) in enumerate(((150, 560), (430, 470), (690, 560))):
        if t > 0.08 + k * 0.1:
            cv.rect((x, y, x + 200, y + 120), WHITE, INK, 5, r=30)
            cv.text((x + 100, y + 95), "!!" if k != 1 else "?!", font(80, "Black"), RED, "ms")
    if t > 0.45:
        cv.rect((260, 820, 740, 920), WHITE, INK, 4, r=20)
        cv.text((UX, 885), "Freunde: zuletzt online …", font(32, "Bold"), (120, 120, 130), "ms")


def s_center(cv, t, dur):
    cv.rect((0, 0, W, H), (200, 220, 236))
    cv.rect((80, 450, 1000, 1130), (236, 238, 242), INK, 6)
    cv.rect((180, 480, 900, 570), (40, 110, 200), INK, 5, r=10)
    cv.text((540, 548), "IMPFZENTRUM", font(60, "Black"), WHITE, "ms")
    cv.rect((440, 820, 640, 1130), (120, 160, 200), INK, 5)
    cv.rect((0, 1130, W, H), (170, 170, 176))
    for k in range(6):  # queue
        T.character(cv, 60 + k * 175, 1560 - (k % 2) * 20, 0.48, "neutral", "down", facemask=True, **EXTRAS[k % 5])
    hero(cv, 540, FEET + 40, SCALE * 0.75, "worry", "phone", facemask=True, blink=blink_at(t, dur))
    if t > 0.74:
        cv.rect((620, 640, 980, 760), WHITE, INK, 5, r=24)
        cv.text((800, 690), "Termin in", font(32, "Bold"), INK, "ms")
        cv.text((800, 740), "10 Minuten", font(40, "Black"), RED, "ms")


def s_question(cv, t, dur):
    T.bedroom(cv, night=False)
    hero(cv, CX, FEET, SCALE, "worry", "head", facemask=True, blink=blink_at(t, dur), look=(0, -1))
    for k, (x, txt) in enumerate(((60, "FREIWILLIG?"), (540, "KEINE WAHL?"))):
        if t > (0.1, 0.58)[k]:
            cv.circle(x + 40 + 180, 860, 18, WHITE, INK, 4)
            cv.circle(x + 60 + 160, 800, 26, WHITE, INK, 4)
            cv.rect((x, 480, x + 400, 680), WHITE, INK, 5, r=60)
            cv.text((x + 200, 605), txt, font(44, "Black"), INK, "ms")


def s_final(cv, t, dur):
    T.bedroom(cv, night=False)
    off = t > 0.2
    hero(cv, CX, FEET - 40, SCALE * 0.95, "neutral", "down", facemask=not off, blink=blink_at(t, dur))
    for (x0, x1), lab, bg, fg in (((60, 480), "ICH MACH MIT", WHITE, INK), ((520, 920), "NICHT MEHR", RED, WHITE)):
        cv.rect((x0, 1330, x1, 1440), bg, INK, 6, r=28)
        cv.text(((x0 + x1) / 2, 1405), lab, font(50, "Black"), fg, "ms")


SCENES = [s_news, s_market, s_mask, s_curfew, s_letter, s_boss, s_pause, s_family, s_center, s_question, s_final]
PAUSE = 6
UI_SCENES = (0, 4, 5, 6)


def render(i, t=0.5, dur=5.0):
    cv = Canvas((0, 0, 0))
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
