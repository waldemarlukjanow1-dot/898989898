"""Scenes for 'DARF ER GTA 6 SPIELEN?' – a video the viewer sends to his girlfriend (STIL 3, T.HERO).
Own art style, no game logos. Scenes get (t, dur, ta), cued to the voice."""
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "vicecity"))
sys.path.append(os.path.join(HERE, "..", "reich"))
import style3 as T  # noqa: E402
from style3 import Canvas, font, mono, W, H, ease, seg, INK, WHITE, SKIN, YELLOW  # noqa: E402
from timing import PHRASES, TEMPO, seq_bounds  # noqa: E402

UX = 500
RED, GREEN, PINK = (220, 40, 50), (40, 140, 70), (255, 80, 150)
PX0, PY0, PX1, PY1 = 170, 500, 830, 1160
BOUNDS, TOTAL = seq_bounds()
GIRL = dict(hoodie=(220, 80, 140), hair=(70, 40, 30), outfit="hoodie", hair_style="curly")


def cue(text):
    return next(a / TEMPO for a, b, s, t in PHRASES if t.startswith(text))


def hero(cv, x, y, s, mood, arms="down", **kw):
    return T.character(cv, x, y, s, mood, arms, **dict(T.HERO, **kw))


def girl(cv, x, y, s, mood, arms="down", **kw):
    return T.character(cv, x, y, s, mood, arms, **dict(GIRL, **kw))


def blink_at(ta):
    return (ta % 2.7) < 0.1


def heart(cv, x, y, r, col=PINK):
    cv.circle(x - r * 0.5, y, r * 0.55, col)
    cv.circle(x + r * 0.5, y, r * 0.55, col)
    cv.poly([(x - r * 1.02, y + r * 0.15), (x + r * 1.02, y + r * 0.15), (x, y + r * 1.2)], col)


def controller(cv, x, y, s=1.0, col=(40, 42, 50)):
    cv.rect((x - 110 * s, y - 40 * s, x + 110 * s, y + 40 * s), col, INK, 5, r=int(40 * s))
    cv.circle(x - 120 * s, y + 30 * s, 50 * s, col, INK, 5)
    cv.circle(x + 120 * s, y + 30 * s, 50 * s, col, INK, 5)
    cv.rect((x - 110 * s, y - 40 * s, x + 110 * s, y + 40 * s), col, None, 0, r=int(40 * s))
    cv.rect((x - 85 * s, y - 8 * s, x - 45 * s, y + 8 * s), WHITE)
    cv.rect((x - 73 * s, y - 20 * s, x - 57 * s, y + 20 * s), WHITE)
    for dx, dy, c in ((60, -14, (80, 200, 120)), (85, 6, RED), (60, 26, (80, 140, 240)), (35, 6, YELLOW)):
        cv.circle(x + dx * s, y + dy * s, 9 * s, c)


def living_room(cv):
    cv.rect((0, 0, W, H), (232, 214, 196))
    cv.rect((0, 1150, W, H), (150, 110, 80))
    cv.rect((180, 420, 900, 820), (24, 24, 30), INK, 8, r=14)              # TV
    cv.rect((205, 445, 875, 795), (60, 30, 90))
    for k in range(6):                                                    # neon skyline in the game
        x = 220 + k * 110
        hgt = 120 + (k * 53) % 140
        cv.rect((x, 795 - hgt, x + 90, 795), (40, 20, 70))
        cv.rect((x + 15, 795 - hgt + 20, x + 75, 795 - hgt + 34), (255, 70, 170) if k % 2 else (60, 230, 255))
    paste_logo(cv, 770, 560, 170, radius=14)
    cv.rect((440, 820, 640, 860), (24, 24, 30))
    cv.rect((40, 1180, 1040, 1420), (90, 120, 180), INK, 6, r=40)          # sofa
    cv.rect((40, 1080, 1040, 1200), (100, 132, 196), INK, 6, r=40)


def sofa_front(cv):
    """Seat cushions + front of the sofa drawn over the legs, so people sit instead of stand."""
    cv.rect((40, 1170, 1040, 1250), (110, 142, 206), INK, 6, r=30)
    cv.rect((40, 1240, 1040, 1440), (90, 120, 180), INK, 6, r=30)


_LOGO = None


def logo_img():
    global _LOGO
    if _LOGO is None:
        _LOGO = Image.open(os.path.join(HERE, "assets", "logo_gta6.jpg")).convert("RGB")
    return _LOGO


def paste_logo(cv, cx, cy, w, k=1.0, radius=40):
    """Paste the supplied GTA VI logo centred at (cx, cy), width w, with rounded corners; k = pop-in 0..1."""
    if k <= 0:
        return
    lg = logo_img()
    sc = 0.7 + 0.3 * ease(k)
    ww = int(w * sc * T.S.SS)
    hh = int(ww * lg.height / lg.width)
    im = lg.resize((ww, hh), Image.LANCZOS)
    mask = Image.new("L", (ww, hh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, ww - 1, hh - 1), radius * T.S.SS, fill=int(255 * min(1, k * 1.5)))
    x0, y0 = int(cx * T.S.SS - ww / 2), int(cy * T.S.SS - hh / 2)
    cv.d.rounded_rectangle((x0 - 10 * T.S.SS, y0 - 10 * T.S.SS, x0 + ww + 10 * T.S.SS, y0 + hh + 10 * T.S.SS),
                           (radius + 8) * T.S.SS, fill=(255, 255, 255, int(255 * min(1, k * 1.5))))
    cv.img.paste(im, (x0, y0), mask)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")


def phone(cv, title=None):
    cv.rect((PX0 - 18, PY0 - 18, PX1 + 18, PY1 + 18), (24, 24, 30), INK, 6, r=46)
    cv.rect((PX0, PY0, PX1, PY1), (245, 247, 250))
    if title:
        cv.rect((PX0, PY0, PX1, PY0 + 90), (230, 233, 240))
        cv.text((UX, PY0 + 60), title, font(38, "Black"), INK, "ms")


# ------------------------------------------------------------------ scenes (cv, t, dur, ta)

def s_hook(cv, t, dur, ta):
    if ta < cue("Bleib dran"):  # first words: show right away what this is about
        cv.rect((0, 0, W, H), (232, 90, 160))
        for k in range(14):
            cv.line([(0, 200 + k * 130), (W, 80 + k * 130)], (240, 120, 180), 30)
        paste_logo(cv, UX, 800, 620, k=seg(ta, 0.0, 0.35) * 3)
        girl(cv, 880, 1760, 0.55, "shock", "down")
        return
    T.bedroom(cv, night=False)
    girl(cv, 760, 1720, 0.95, "neutral" if ta < cue("Bleib dran") else "smug", "phone", blink=blink_at(ta))
    phone(cv, "Schatz")
    heart(cv, PX0 + 245, PY0 + 48, 14)
    cv.rect((PX0 + 40, PY0 + 130, PX1 - 40, PY0 + 480), (30, 30, 40), None, 0, r=24)
    cv.poly([(UX - 40, PY0 + 255), (UX - 40, PY0 + 355), (UX + 50, PY0 + 305)], WHITE)     # play icon
    cv.rect((PX0 + 40, PY0 + 510, PX1 - 40, PY0 + 600), (60, 140, 250), None, 0, r=30)
    cv.text((UX, PY0 + 568), "Bitte ganz anschauen 🙏".replace(" 🙏", "!"), font(38, "Black"), WHITE, "ms")


def s_years(cv, t, dur, ta):
    if ta < cue("Er wartet"):
        cv.rect((0, 0, W, H), (232, 90, 160))
        paste_logo(cv, UX, 790, 600, k=seg(ta, cue("GTA 6 kommt"), cue("GTA 6 kommt") + 0.25) * 3)
        cv.rect((330, 1120, 670, 1190), YELLOW, INK, 5, r=20)
        cv.text((UX, 1173), "KOMMT BALD", font(46, "Black"), INK, "ms")
        return
    T.bedroom(cv, night=False)
    hero(cv, 760, 1720, 0.95, "worry", "phone", blink=blink_at(ta))
    k = ease(seg(ta, cue("Er wartet"), cue("Länger")))
    year = int(2013 + 13 * k)
    cv.rect((90, 470, 560, 820), WHITE, INK, 6, r=20)
    cv.rect((90, 470, 560, 560), RED, None, 0, r=20)
    cv.text((325, 535), "KALENDER", font(40, "Black"), WHITE, "ms")
    cv.text((325, 720), str(year), font(130, "Black"), INK, "ms")
    if ta >= cue("Länger"):
        cv.rect((90, 850, 560, 930), YELLOW, INK, 4, r=16)
        cv.text((325, 905), "länger als ihr zwei", font(36, "Black"), INK, "ms")


def s_wishes(cv, t, dur, ta):
    T.bedroom(cv, night=False)
    hero(cv, 540, 1720, 1.0, "happy", "down", blink=blink_at(ta))
    items = [("Er will kein", "PARIS", 120, 500), ("Keine neuen", "SCHUHE", 120, 700)]
    for key, lab, x, y in items:
        if ta >= cue(key):
            cv.rect((x, y, x + 330, y + 150), WHITE, INK, 5, r=24)
            cv.text((x + 165, y + 95), lab, font(54, "Black"), INK, "ms")
            cv.line([(x + 20, y + 20), (x + 310, y + 130)], RED, 12)
    if ta >= cue("Nur ein paar"):
        cv.rect((600, 520, 960, 820), WHITE, (40, 140, 70), 7, r=24)
        controller(cv, 780, 650, 1.0)
        cv.text((780, 790), "NUR DAS", font(44, "Black"), GREEN, "ms")


def s_sofa(cv, t, dur, ta):
    living_room(cv)
    hero(cv, 380, 1360, 0.7, "happy", "down", blink=blink_at(ta))
    girl(cv, 690, 1360, 0.68, "happy" if ta >= cue("Auf dem Sofa") else "neutral", "phone", blink=blink_at(ta + 1))
    sofa_front(cv)
    controller(cv, 380, 1140, 0.55)
    if ta >= cue("Auf dem Sofa"):
        cv.rect((300, 470, 700, 560), WHITE, INK, 4, r=18)
        cv.circle(340, 515, 18, RED)
        cv.text((520, 530), "Standort: Sofa", font(40, "Black"), INK, "ms")
    if ta >= cue("Neben dir"):
        heart(cv, 540, 1010, 40)


def s_chat(cv, t, dur, ta):
    living_room(cv)
    phone(cv, "Nachrichten")
    cv.text((UX, PY0 + 300), "Keine neuen", font(52, "Black"), (150, 150, 160), "ms")
    cv.text((UX, PY0 + 370), "Nachrichten", font(52, "Black"), (150, 150, 160), "ms")
    cv.circle(UX, PY0 + 520, 70, None, (200, 200, 210), 8)
    cv.text((UX, PY0 + 548), "0", font(80, "Black"), (200, 200, 210), "ms")
    if ta >= cue("Er fährt"):  # tiny car on the TV-like phone bottom: he only drives in the game
        cv.rect((PX0 + 40, PY1 - 170, PX1 - 40, PY1 - 40), (60, 30, 90), None, 0, r=20)
        x = PX0 + 60 + ((ta * 220) % 420)
        cv.rect((x, PY1 - 110, x + 120, PY1 - 70), (250, 200, 30), INK, 3, r=10)
        cv.circle(x + 25, PY1 - 68, 12, INK)
        cv.circle(x + 95, PY1 - 68, 12, INK)


def s_pause(cv, t, dur, ta):
    s_sofa(cv, 1.0, dur, BOUNDS[3][1] - 0.1)


def s_deal(cv, t, dur, ta):
    T.bedroom(cv, night=False)
    hero(cv, 800, 1720, 0.85, "happy", "point", blink=blink_at(ta))
    cv.rect((90, 470, 620, 1150), (250, 246, 236), INK, 6, r=12)
    cv.text((355, 545), "VERTRAG", font(50, "Black"), INK, "ms")
    rows = [("Am Wochenende", "Wochenende: Er spielt"), ("Unter der Woche", "Mo–Fr: Er kocht"),
            ("Und das Essen", "Essen bei deinen Eltern")]
    for k, (key, lab) in enumerate(rows):
        y = 620 + k * 150
        cv.rect((120, y, 180, y + 60), WHITE, INK, 4, r=8)
        cv.text((200, y + 45), lab, font(32, "Bold"), INK)
        if ta >= cue(key) + 0.3:
            cv.line([(130, y + 30), (148, y + 52), (175, y + 8)], GREEN, 10)
    if ta >= cue("Schon zugesagt"):
        cv.text((355, 1100), "✍ Dein Freund".replace("✍ ", ""), font(46, "Black"), (40, 60, 160), "ms")


def s_controller2(cv, t, dur, ta):
    living_room(cv)
    hero(cv, 380, 1360, 0.7, "happy", "down", blink=blink_at(ta))
    k = ease(seg(ta, cue("Und wenn du willst"), cue("Und wenn du willst") + 1.0))
    girl(cv, 690, 1360, 0.68, "happy", "down", blink=blink_at(ta + 1))
    sofa_front(cv)
    controller(cv, 380, 1140, 0.55)
    controller(cv, 450 + 240 * k, 1140, 0.55, (230, 80, 150))
    for j in range(3):
        if k >= 1:
            ph = (ta * 0.8 + j / 3) % 1
            heart(cv, 480 + j * 60, 1000 - 200 * ph, 22, PINK + (int(255 * (1 - ph)),))


def s_final(cv, t, dur, ta):
    T.bedroom(cv, night=False)
    hero(cv, 540, 1720, 1.05, "worry", "down", look=(0, -1), blink=blink_at(ta))   # puppy eyes
    if ta >= cue("Und markier"):
        cv.rect((260, 470, 740, 560), WHITE, INK, 4, r=20)
        cv.text((UX, 532), "@dein.freund", font(44, "Black"), (60, 120, 230), "ms")


def buttons(img):
    d = ImageDraw.Draw(img, "RGBA")
    f = T.font(60, "Black")
    for (x0, x1), lab, bg, fg in (((90, 460), "JA", (40, 140, 70), YELLOW), ((540, 910), "NEIN", RED, WHITE)):
        d.rounded_rectangle((x0, 1330, x1, 1440), 28, fill=bg, outline=INK, width=6)
        d.text(((x0 + x1) / 2, 1408), lab, font=f, fill=fg, anchor="ms")


SCENES = [s_hook, s_years, s_wishes, s_sofa, s_chat, s_pause, s_deal, s_controller2, s_final]
PAUSE = 5
UI_SCENES = (0, 1, 4)
INNER_CUTS = [cue("Bleib dran"), cue("Er wartet")]


def render(i, t=0.5, dur=5.0, ta=None):
    ta = BOUNDS[i][0] + t * (BOUNDS[i][1] - BOUNDS[i][0]) if ta is None else ta
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur, ta)
    img = cv.final()
    if i in UI_SCENES:
        img = T.camera(img, 0.0, 500, 810)
    else:
        img = T.camera(img, 0.02 + 0.06 * ease(t), 540, 960)
    if i == 8:
        buttons(img)
    if i == PAUSE:
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, ta):
    if i == 1 and ta < cue("Er wartet"):
        return ("GTA 6", "yellow")
    return [("GTA 6 · FÜR DEINE FREUNDIN", "yellow"), ("SEIT 2013", "yellow"), ("SEINE WÜNSCHE", "white"),
            ("STANDORT: SOFA", "green"), ("ANDERE FRAUEN: 0", "green"), ("", "white"),
            ("SEIN ANGEBOT", "green"), ("PLAYER 2", "green"), ("DARF ER?", "yellow")][i]
