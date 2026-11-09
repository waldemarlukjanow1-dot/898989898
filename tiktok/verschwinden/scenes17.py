"""Scenes for '24 STUNDEN VERSCHWINDEN' (STIL 3, T.HERO). Scenes get (t, dur, ta), cued to the voice."""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "reich"))
import style3 as T  # noqa: E402
from style3 import Canvas, font, mono, W, H, ease, seg, INK, WHITE, SKIN, YELLOW  # noqa: E402
from timing import PHRASES, TEMPO, seq_bounds  # noqa: E402

UX = 500
RED, GREEN = (220, 40, 50), (40, 140, 70)
PX0, PY0, PX1, PY1 = 170, 500, 830, 1160
BOUNDS, TOTAL = seq_bounds()
DRIVER = dict(hoodie=(22, 22, 26), hair=(20, 20, 22), outfit="hoodie", hair_style="fringe", tie=True, glasses=True)
FAMILY = [dict(hoodie=(200, 110, 130), hair=(110, 70, 50), outfit="hoodie", hair_style="fringe"),
          dict(hoodie=(80, 140, 200), hair=(140, 90, 50), outfit="hoodie", hair_style="fringe"),
          dict(hoodie=(240, 190, 70), hair=(60, 40, 30), outfit="hoodie", hair_style="fringe")]


def cue(text):
    return next(a / TEMPO for a, b, s, t in PHRASES if t.startswith(text))


def cue_end(text):
    return next(b / TEMPO for a, b, s, t in PHRASES if t.startswith(text))


def hero(cv, x, y, s, mood, arms="down", **kw):
    return T.character(cv, x, y, s, mood, arms, **dict(T.HERO, **kw))


def blink_at(ta):
    return (ta % 2.7) < 0.1


def talking(ta, text):
    return abs(math.sin(ta * 10)) if cue(text) <= ta < cue_end(text) else 0.0


def phone(cv, title=None, dark=False):
    cv.rect((PX0 - 18, PY0 - 18, PX1 + 18, PY1 + 18), (24, 24, 30), INK, 6, r=46)
    cv.rect((PX0, PY0, PX1, PY1), (20, 22, 30) if dark else (245, 247, 250))
    if title:
        cv.rect((PX0, PY0, PX1, PY0 + 90), (40, 42, 52) if dark else (230, 233, 240))
        cv.text((UX, PY0 + 60), title, font(38, "Black"), WHITE if dark else INK, "ms")


def night_street(cv):
    for y in range(0, 1100, 6):
        k = y / 1100
        cv.rect((0, y, W, y + 6), (int(14 + 20 * k), int(18 + 22 * k), int(40 + 30 * k)))
    rnd = random.Random(7)
    x = -20
    while x < W:
        bw, bh = rnd.randint(170, 260), rnd.randint(420, 700)
        cv.rect((x, 1100 - bh, x + bw, 1100), (40, 46, 72), INK, 4)
        for wy in range(1100 - bh + 40, 1060, 90):
            for wx in range(x + 30, x + bw - 50, 70):
                cv.rect((wx, wy, wx + 40, wy + 56), (255, 214, 120) if rnd.random() < 0.3 else (28, 32, 52))
        x += bw + 10
    cv.rect((0, 1100, W, 1180), (110, 110, 118), INK, 3)
    cv.rect((0, 1180, W, H), (44, 46, 54))


def suv(cv, x, y, w=640, lights=True):
    h = w * 0.42
    cv.rect((x, y - h * 0.55, x + w, y), (16, 16, 20), INK, 6, r=24)
    cv.rect((x + w * 0.1, y - h, x + w * 0.85, y - h * 0.5), (16, 16, 20), INK, 6, r=20)
    for k in range(3):
        cv.rect((x + w * (0.14 + k * 0.24), y - h * 0.92, x + w * (0.33 + k * 0.24), y - h * 0.6), (40, 46, 60), INK, 3, r=8)
    for wx in (x + w * 0.2, x + w * 0.8):
        cv.circle(wx, y, h * 0.24, (10, 10, 12), INK, 5)
        cv.circle(wx, y, h * 0.1, (90, 90, 96))
    if lights:
        cv.rect((x - 6, y - h * 0.45, x + 30, y - h * 0.32), (255, 250, 210))
        cv.poly([(x, y - h * 0.4), (x - 520, y - h * 0.9), (x - 520, y + h * 0.3)], (255, 250, 210, 60))


def hotel_room(cv, lamp=True):
    cv.rect((0, 0, W, H), (92, 70, 64))
    for k in range(9):
        cv.line([(k * 130, 0), (k * 130, 1100)], (102, 80, 72), 6)
    cv.rect((0, 1100, W, H), (70, 40, 44))
    cv.rect((620, 380, 1000, 1180), (60, 40, 30), INK, 6)  # door
    cv.rect((650, 410, 970, 1150), (110, 76, 54), INK, 5)
    cv.circle(680 + 250, 800, 18, (220, 190, 90), INK, 4)
    cv.rect((660, 360, 960, 395), (230, 220, 200), INK, 3, r=6)
    cv.text((810, 388), "ZIMMER 1408", font(22, "Black"), INK, "ms")
    if lamp:
        cv.rect((60, 760, 220, 960), (50, 40, 34), INK, 4, r=8)
        cv.poly([(80, 760), (200, 760), (240, 640), (40, 640)], (250, 230, 180), INK, 4)
        cv.glow(140, 700, 300, (255, 220, 150), 110)


def bed(cv):
    cv.rect((40, 1180, 900, 1440), (230, 225, 215), INK, 6, r=24)
    cv.rect((40, 1260, 900, 1460), (150, 40, 50), INK, 6, r=20)
    cv.rect((60, 1140, 300, 1220), WHITE, INK, 5, r=30)


# ------------------------------------------------------------------ scenes (cv, t, dur, ta)

def s_offer(cv, t, dur, ta):
    T.bedroom(cv)
    phone(cv, "Unbekannt")
    f = font(40, "Black")
    lines = [("20.000.000 €", GREEN), ("für 24 Stunden", INK), ("verschwinden.", INK)]
    for k, (l, c) in enumerate(lines):
        if ta >= 0.2 + k * 0.6:
            cv.text((UX, PY0 + 220 + k * 80), l, font(64 if k == 0 else 44, "Black"), c, "ms")
    rules = [("Keine Fragen.", "KEINE FRAGEN"), ("Keine Polizei.", "KEINE POLIZEI"), ("Keine Familie.", "KEINE FAMILIE")]
    for k, (key, lab) in enumerate(rules):
        if ta >= cue(key):
            cv.rect((PX0 + 60, PY0 + 470 + k * 60, PX1 - 60, PY0 + 520 + k * 60), (255, 230, 230), RED, 3, r=12)
            cv.text((UX, PY0 + 508 + k * 60), "✕ " + lab if False else lab, font(30, "Black"), RED, "ms")


def s_yes(cv, t, dur, ta):
    night_street(cv)
    x = 1100 - 680 * ease(seg(ta, cue("In derselben"), cue_end("In derselben") + 0.3))
    suv(cv, x, 1560)
    nod = abs(math.sin((ta - cue("Du sagst")) * 8)) if cue("Du sagst") <= ta < cue("Du sagst") + 0.8 else 0
    hero(cv, 260, 1720 + 10 * nod, 0.95, "neutral" if ta < cue("In derselben") else "worry", "down", look=(1, 0),
         blink=blink_at(ta))


def s_erase(cv, t, dur, ta):
    if ta < cue("Dein Name"):  # phone smashed
        cv.rect((0, 0, W, H), (24, 26, 34))
        phone(cv, None, dark=True)
        k = ease(seg(ta, cue("Dein Handy") + 0.3, cue("Dein Handy") + 0.6))
        if k > 0:
            for j in range(9):
                a = j * 0.7
                cv.line([(UX, 830), (UX + math.cos(a) * 320 * k, 830 + math.sin(a) * 300 * k)], WHITE, 4)
            cv.text((UX, 1270), "KRACH!", font(90, "Black"), YELLOW, "ms")
        return
    cv.rect((0, 0, W, H), (14, 20, 30))
    cv.rect((120, 480, 880, 1150), (20, 30, 44), (60, 220, 120), 5, r=16)
    cv.text((UX, 550), "EINWOHNERREGISTER", mono(34), (60, 220, 120), "ms")
    cv.rect((180, 600, 820, 680), (10, 16, 24), (60, 220, 120), 3)
    cv.text((210, 655), "SUCHE: [DEIN NAME]", mono(30), (60, 220, 120))
    k = seg(ta, cue("Dein Name"), cue("Offiziell"))
    for j in range(5):  # records get deleted line by line
        y = 720 + j * 70
        if j / 5 >= k:
            cv.rect((180, y, 820, y + 50), (30, 60, 50))
            cv.text((200, y + 37), ["Geburtsdatum", "Adresse", "Konto", "Ausweis", "Steuer-ID"][j], mono(26), (150, 255, 180))
        else:
            cv.rect((180, y, 820, y + 50), (60, 20, 20))
            cv.text((200, y + 37), "GELÖSCHT", mono(26), (255, 120, 120))
    if ta >= cue("Offiziell"):
        cv.rect((180, 1060, 820, 1130), RED, r=10)
        cv.text((UX, 1110), "PERSON NICHT GEFUNDEN", mono(34), WHITE, "ms")


def tv(cv, ta, show_face):
    cv.rect((110, 470, 890, 1060), (20, 20, 24), INK, 8, r=18)
    cv.rect((140, 500, 860, 1030), (40, 60, 110))
    cv.rect((160, 520, 290, 570), RED, r=8)
    cv.text((225, 560), "LIVE", font(34, "Black"), WHITE, "ms")
    if show_face:  # your portrait, framed like a news photo, with black mourning ribbon
        fx0, fy0, fx1, fy1 = 330, 560, 670, 860
        cv.rect((fx0 - 10, fy0 - 10, fx1 + 10, fy1 + 10), WHITE, INK, 4)
        sub = Canvas((200, 210, 225))
        T.character(sub, 540, 960 + 753 * 1.6 - 520, 1.6, "neutral", "down", **T.HERO)
        crop = sub.final().crop((200, 110, 880, 710)).resize(((fx1 - fx0) * T.S.SS, (fy1 - fy0) * T.S.SS))
        cv.img.paste(crop, (fx0 * T.S.SS, fy0 * T.S.SS))
        cv.d = ImageDraw.Draw(cv.img, "RGBA")
        cv.rect((fx0, fy0, fx1, fy1), None, INK, 4)
        cv.poly([(fx1 - 70, fy0), (fx1, fy0), (fx1, fy0 + 70)], (10, 10, 10))
    cv.rect((140, 920, 860, 1030), RED)
    cv.rect((140, 880, 400, 920), YELLOW)
    cv.text((270, 912), "EILMELDUNG", font(30, "Black"), INK, "ms")
    cv.text((UX, 995), "UNTERNEHMER TOT AUFGEFUNDEN", font(38, "Black"), WHITE, "ms")
    cv.rect((UX - 30, 1060, UX + 30, 1100), (20, 20, 24))


def s_news(cv, t, dur, ta):
    cv.rect((0, 0, W, H), (60, 50, 50))
    tv(cv, ta, show_face=ta >= cue("Dein Foto"))
    hero(cv, 780, 1180 + 753 * 0.55, 0.55, "shock" if ta >= cue("Dein Foto") else "worry", "down", blink=blink_at(ta))


def s_bank(cv, t, dur, ta):
    hotel_room(cv)
    phone(cv, "NEUES KONTO")
    k = ease(seg(ta, cue("Auf deinem"), cue("Die erste")))
    cv.text((UX, PY0 + 260), "Kontostand", font(34, "Bold"), (120, 120, 130), "ms")
    cv.text((UX, PY0 + 360), f"{int(5000000 * k):,} €".replace(",", "."), font(76, "Black"), GREEN, "ms")
    if ta >= cue("Die erste"):
        cv.rect((PX0 + 60, PY0 + 430, PX1 - 60, PY0 + 520), (230, 245, 230), GREEN, 3, r=14)
        cv.text((UX, PY0 + 490), "Zahlung 1 von 4", font(36, "Black"), GREEN, "ms")


def s_pause(cv, t, dur, ta):
    cv.rect((0, 0, W, H), (60, 50, 50))
    tv(cv, ta, True)
    hero(cv, 780, 1180 + 753 * 0.55, 0.55, "shock", "head")


def s_call(cv, t, dur, ta):
    hotel_room(cv)
    bed(cv)
    ringing = ta < cue("Eine Stimme")
    cv.rect((300, 1080, 500, 1180), (230, 225, 210), INK, 5, r=14)   # hotel phone on the nightstand
    cv.rect((320, 1050, 480, 1090), (60, 60, 66), INK, 4, r=12)
    if ringing:
        for r_ in range(3):
            ph = (ta * 2 + r_ / 3) % 1
            cv.arc((400 - 60 - 80 * ph, 1060 - 60 - 80 * ph, 400 + 60 + 80 * ph, 1060 + 60 + 80 * ph), 200, 340,
                   (255, 214, 10, int(255 * (1 - ph))), 6)
    hero(cv, 640, 1720, 0.95, "worry" if ringing else "shock", "head" if not ringing else "down", look=(-1, 0),
         blink=blink_at(ta))
    if ta >= cue("Du hast vergessen"):
        cv.rect((70, 470, 590, 650), (20, 20, 26, 230), (255, 214, 10), 4, r=26)
        cv.text((330, 545), "Du hast vergessen, wem", font(34, "Black"), (255, 240, 180), "ms")
        cv.text((330, 605), "du das Geld schuldest.", font(34, "Black"), (255, 240, 180), "ms")


def s_envelope(cv, t, dur, ta):
    cv.rect((0, 0, W, H), (150, 40, 50))  # bed cover close-up
    back = ta >= cue("Auf der Rückseite")
    if not back:
        cv.rect((170, 520, 830, 1060), WHITE, INK, 6, r=8)
        cv.rect((200, 550, 800, 960), (130, 180, 220))
        cv.rect((200, 860, 800, 960), (90, 140, 80))
        WIFE = dict(hoodie=(200, 110, 130), hair=(110, 70, 50), outfit="hoodie", hair_style="curly")
        KID1 = dict(hoodie=(80, 140, 200), hair=(60, 40, 30), outfit="hoodie", hair_style="fringe")
        KID2 = dict(hoodie=(240, 190, 70), hair=(140, 90, 50), outfit="hoodie", hair_style="curly")
        T.character(cv, 300, 955, 0.36, "happy", "down", **T.HERO)        # you
        T.character(cv, 450, 955, 0.33, "happy", "down", **WIFE)          # wife
        T.character(cv, 590, 955, 0.24, "happy", "down", **KID1)          # child 1
        T.character(cv, 710, 955, 0.2, "happy", "down", **KID2)           # child 2
        cv.text((780, 1035), "HEUTE · 07:12", mono(28), RED, "rs")
    else:
        cv.rect((170, 520, 830, 1060), (245, 242, 232), INK, 6, r=8)
        cv.text((UX, 830), "Bleib tot.", font(110, "Black"), RED, "ms")


def s_lock(cv, t, dur, ta):
    hotel_room(cv, lamp=False)
    cv.overlay((10, 10, 20), 60)
    turn = ease(seg(ta, cue("Dann hörst"), cue_end("Dann hörst")))
    cx, cy = 930, 800
    a = math.radians(-60 * turn)
    cv.line([(cx, cy), (cx - math.cos(a) * 90, cy + math.sin(a) * 90)], (230, 200, 100), 22)  # handle turns
    cv.glow(810, 1150, 220, (255, 240, 200), 90)  # light under the door
    if ta >= cue("Dann hörst") + 0.3:
        cv.text((780, 700), "klick", font(54, "Black"), YELLOW, "ms")
    hero(cv, 300, 1720, 0.95, "shock", "down", look=(1, 0))


def s_target(cv, t, dur, ta):
    hotel_room(cv, lamp=False)
    cv.overlay((10, 10, 20), 90)
    phone(cv, "Nachricht", dark=True)
    if ta >= cue("Zielperson gefunden") - 0.1:
        cv.rect((PX0 + 30, PY0 + 140, PX1 - 30, PY0 + 290), (60, 60, 70), None, 0, r=26)
        cv.text((UX, PY0 + 235), "Zielperson gefunden.", font(46, "Black"), (255, 120, 120), "ms")
        cv.circle(UX, PY0 + 480, 120, None, RED, 6)
        cv.line([(UX - 150, PY0 + 480), (UX + 150, PY0 + 480)], RED, 4)
        cv.line([(UX, PY0 + 330), (UX, PY0 + 630)], RED, 4)


def s_driver(cv, t, dur, ta):
    hotel_room(cv, lamp=False)
    k = ease(seg(ta, cue("Die Tür geht"), cue("Es ist der")))
    cv.rect((650, 410, 650 + 320 * (1 - k), 1150), (110, 76, 54), INK, 5)  # door swings open
    cv.glow(810, 780, 320 * k + 1, (255, 240, 200), int(120 * k))
    if ta >= cue("Es ist der"):
        T.character(cv, 810, 1200, 0.62, "neutral", "down", talk=talking(ta, "Die 24"), **DRIVER)
    hero(cv, 300, 1720, 0.95, "shock", "down", look=(1, 0))
    if ta >= cue("Die 24"):
        cv.rect((520, 470, 960, 610), WHITE, INK, 5, r=30)
        cv.poly([(780, 610), (820, 610), (805, 660)], WHITE, INK, 5)
        cv.text((740, 528), "Die 24 Stunden", font(38, "Black"), INK, "ms")
        cv.text((740, 585), "sind um.", font(38, "Black"), RED, "ms")


def s_final(cv, t, dur, ta):
    hotel_room(cv, lamp=False)
    cv.rect((650, 410, 650 + 40, 1150), (110, 76, 54), INK, 5)
    cv.glow(810, 780, 320, (255, 240, 200), 120)
    T.character(cv, 810, 1200, 0.62, "neutral", "down", **DRIVER)
    hero(cv, 300, 1720, 0.95, "shock", "down", look=(1, 0))


def buttons(img):
    d = ImageDraw.Draw(img, "RGBA")
    f = T.font(48, "Black")
    for (x0, x1), lab, bg, fg in (((60, 470), "ANGREIFEN", WHITE, INK), ((510, 920), "FLIEHEN", RED, WHITE)):
        d.rounded_rectangle((x0, 1330, x1, 1440), 28, fill=bg, outline=INK, width=6)
        d.text(((x0 + x1) / 2, 1405), lab, font=f, fill=fg, anchor="ms")


SCENES = [s_offer, s_yes, s_erase, s_news, s_bank, s_pause, s_call, s_envelope, s_lock, s_target, s_driver, s_final]
PAUSE = 5
UI_SCENES = (0, 2, 3, 4, 5, 7, 9)
INNER_CUTS = []


def render(i, t=0.5, dur=5.0, ta=None):
    ta = BOUNDS[i][0] + t * (BOUNDS[i][1] - BOUNDS[i][0]) if ta is None else ta
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur, ta)
    img = cv.final()
    if i in UI_SCENES:
        img = T.camera(img, 0.0, 500, 810)
    else:
        img = T.camera(img, 0.02 + 0.07 * ease(t), 540, 860)
    if i == 11:
        buttons(img)
    if i == PAUSE:
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, ta):
    left = max(0, 24 - int((ta / TOTAL) * 24))
    clock = f"NOCH {left:02d}:00 STUNDEN"
    return [("ANGEBOT: 20.000.000 €", "green"), ("DU SAGST JA", "white"), ("IDENTITÄT: GELÖSCHT", "red"),
            ("OFFIZIELL: TOT", "red"), ("+ 5.000.000 €", "green"), ("", "white"), ("UNBEKANNTER ANRUF", "red"),
            ("VON HEUTE MORGEN", "red"), ("NIEMAND KENNT DAS HOTEL", "red"), ("ZIELPERSON: DU", "red"),
            ("00:00 – ZEIT UM", "red"), ("ANGREIFEN ODER FLIEHEN?", "yellow")][i]
