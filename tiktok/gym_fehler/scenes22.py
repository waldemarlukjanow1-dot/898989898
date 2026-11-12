"""Scenes for '5 FEHLER, WARUM DU IM GYM KEINE MUSKELN BEKOMMST' (STIL 3, T.HERO, athletic rig).

Helpers (gym, rack, calendar, label, pain, plate, mirror) come from the first gym video (scenes21).
Scenes get (cv, t, dur, ta) and are cued to the voice."""
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "vicecity"))
sys.path.append(os.path.join(HERE, "..", "reich"))
import style3 as T  # noqa: E402
from style3 import Canvas, font, W, H, ease, seg, INK, WHITE, YELLOW  # noqa: E402
from timing import PHRASES, TEMPO, seq_bounds  # noqa: E402

UX = 500
RED, GREEN, BLUE = (220, 40, 50), (40, 140, 70), (60, 120, 230)
BOUNDS, TOTAL = seq_bounds()
TANK = (30, 30, 36)                                   # black gym tank top
MATE = dict(hoodie=(200, 60, 60), hair=(150, 90, 40), outfit="tank", hair_style="curly")
SHOCK = 0.9


def cue(text, last=False):
    hits = [a / TEMPO for a, b, s, t in PHRASES if t.startswith(text)]
    return hits[-1] if last else hits[0]


def talking(ta, seqs):
    for a, b, s, _ in PHRASES:
        if s in seqs and a / TEMPO <= ta <= b / TEMPO:
            return 0.5 + 0.5 * abs(math.sin(ta * 17))
    return 0.0


def blink_at(ta):
    return (ta % 2.7) < 0.1


def hero(cv, x, y, s, mood, arms="down", bulk=0.0, tank=True, lift=0.0, **kw):
    cfg = dict(T.HERO)
    if tank:
        cfg.update(outfit="tank", hoodie=TANK)
    cfg.update(kw)
    return T.character(cv, x, y, s, mood, arms, bulk=bulk, lift=lift, **cfg)


# ------------------------------------------------------------------ places
def gym(cv, mirror=True):
    """Bright gym: grey wall, red GYM sign, mirror wall, dumbbell rack, rubber floor."""
    cv.rect((0, 0, W, H), (222, 226, 232))
    cv.rect((0, 1150, W, H), (70, 74, 82))
    for k in range(8):
        cv.line([(k * 150, 1150), (k * 150 - 80, H)], (60, 63, 70), 4)
    cv.rect((0, 1120, W, 1150), (190, 40, 50))                          # red wall stripe
    if mirror:
        cv.rect((60, 560, 1020, 1120), (200, 222, 236), INK, 8)
        for k in range(3):
            cv.line([(160 + k * 300, 600), (300 + k * 300, 1080)], (225, 240, 250), 18)
    cv.rect((790, 455, 990, 540), (200, 40, 50), INK, 5, r=14)        # sign (below the chip)
    cv.text((890, 525), "GYM", font(66, "Black"), WHITE, "ms")


def rack(cv, y=1150):
    cv.rect((60, y - 250, 400, y - 230), (90, 92, 100), INK, 4)
    cv.rect((60, y - 120, 400, y - 100), (90, 92, 100), INK, 4)
    for row, yy in enumerate((y - 240, y - 110)):
        for k in range(4):
            x = 90 + k * 85
            cv.line([(x - 25, yy - 30), (x + 25, yy - 30)], (120, 122, 130), 12)
            for sd in (-1, 1):
                cv.rect((x + sd * 28 - 12, yy - 60, x + sd * 28 + 12, yy), (40, 42, 50), INK, 3, r=5)


def street(cv):
    cv.rect((0, 0, W, H), (150, 205, 245))
    cv.rect((0, 1500, W, H), (90, 92, 100))
    cv.rect((0, 1380, W, 1500), (190, 190, 196))
    cv.rect((120, 420, 960, 1380), (210, 205, 196), INK, 8)          # building
    cv.poly([(90, 430), (990, 430), (930, 360), (150, 360)], (120, 70, 60), INK, 6)
    cv.rect((260, 470, 820, 610), (200, 40, 50), INK, 6, r=16)
    cv.text((540, 580), "GYM", font(110, "Black"), WHITE, "ms")
    for x in (170, 720):
        cv.rect((x, 680, x + 190, 920), (170, 210, 240), INK, 6)
        cv.line([(x + 95, 680), (x + 95, 920)], INK, 5)
    cv.rect((420, 1040, 660, 1380), (60, 70, 90), INK, 6)              # door
    cv.rect((440, 1060, 640, 1240), (150, 200, 235))
    cv.circle(625, 1300, 10, YELLOW, INK, 3)
    cv.text((540, 1020), "OFFEN 6–23 UHR", font(34, "Black"), INK, "ms")


def bedroom_night(cv):
    T.bedroom(cv, night=True)


def stairs(cv):
    cv.rect((0, 0, W, H), (232, 222, 206))
    for k in range(9):
        y = 1500 - k * 110
        x = 1080 - k * 130
        cv.rect((x - 260, y - 110, W, y), (190, 160, 130), INK, 5)
    cv.line([(40, 1500), (1080, 330)], (120, 80, 50), 12)              # handrail


# ------------------------------------------------------------------ props
def calendar(cv, x, y, w, days_marked=(), title="WOCHE"):
    names = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
    cw = w / 7
    cv.rect((x, y, x + w, y + 210), WHITE, INK, 6, r=18)
    cv.rect((x, y, x + w, y + 70), RED, None, 0, r=18)
    cv.rect((x, y + 50, x + w, y + 70), RED)
    cv.text((x + w / 2, y + 52), title, font(40, "Black"), WHITE, "ms")
    for k, n in enumerate(names):
        cx = x + cw * (k + 0.5)
        cv.text((cx, y + 125), n, font(34, "Bold"), INK, "ms")
        if k in days_marked:
            cv.circle(cx, y + 165, 24, GREEN, INK, 3)
            cv.line([(cx - 11, y + 165), (cx - 2, y + 175), (cx + 13, y + 154)], WHITE, 6)


def label(cv, x, y, text, bg=WHITE, fg=INK, size=46, k=1.0):
    if k <= 0:
        return
    f = font(int(size * (0.7 + 0.3 * ease(min(1, k)))), "Black")
    tw = cv.d.textlength(text, font=T.font(f.size, "Black"))
    cv.rect((x - tw / 2 - 28, y - f.size - 12, x + tw / 2 + 28, y + 22), bg, INK, 5, r=18)
    cv.text((x, y), text, f, fg, "ms")


def pain(cv, x, y, k):
    """Red 'ouch' zig-zags."""
    for j in range(3):
        a = math.radians(-60 + j * 60)
        x0, y0 = x + math.cos(a) * 40, y + math.sin(a) * 40
        x1, y1 = x + math.cos(a) * (80 + 10 * k), y + math.sin(a) * (80 + 10 * k)
        cv.line([(x0, y0), ((x0 + x1) / 2 + 8, (y0 + y1) / 2 - 8), (x1, y1)], RED, 8)


def zzz(cv, x, y, ta):
    for j in range(3):
        ph = (ta * 0.6 + j / 3) % 1
        cv.text((x + 40 * j + 30 * ph, y - 160 * ph), "Z", font(int(50 + 20 * j), "Black"), (60, 80, 160, int(255 * (1 - ph))), "ms")


def plate(cv, x, y):
    cv.ellipse((x - 190, y - 70, x + 190, y + 70), WHITE, INK, 6)
    cv.ellipse((x - 140, y - 45, x + 140, y + 45), (240, 240, 240))
    cv.ellipse((x - 120, y - 35, x - 10, y + 25), (215, 160, 90), INK, 4)        # chicken
    for k in range(2):                                                          # eggs
        cv.ellipse((x + 10 + k * 60, y - 30, x + 60 + k * 60, y + 20), WHITE, INK, 4)
        cv.circle(x + 35 + k * 60, y - 5, 12, (250, 190, 40))
    for k in range(4):                                                          # broccoli
        cv.circle(x - 30 + k * 22, y + 30, 14, (60, 150, 70), INK, 2)


def mirror_frame(cv, x0, y0, x1, y1):
    cv.rect((x0 - 20, y0 - 20, x1 + 20, y1 + 20), (190, 150, 70), INK, 6, r=16)
    cv.rect((x0, y0, x1, y1), (210, 230, 242))
    for k in range(2):
        cv.line([(x0 + 40 + k * 140, y0 + 40), (x0 + 160 + k * 140, y1 - 60)], (232, 244, 250), 16)



def bulb(cv, x, y, s=1.0, on=True):
    if on:
        cv.glow(x, y, 150 * s, (255, 230, 120), 120)
    cv.circle(x, y, 110 * s, (255, 240, 170) if on else (230, 230, 230), INK, 6)
    cv.rect((x - 55 * s, y + 95 * s, x + 55 * s, y + 190 * s), (170, 170, 180), INK, 5, r=10)
    for k in range(3):
        cv.line([(x - 55 * s, y + (120 + k * 25) * s), (x + 55 * s, y + (120 + k * 25) * s)], INK, 4)
    cv.line([(x - 30 * s, y + 20 * s), (x - 10 * s, y - 30 * s), (x + 10 * s, y + 20 * s), (x + 30 * s, y - 30 * s)], (220, 150, 40), 6)


def matches(cv, x, y):
    for sd in (-1, 1):
        cv.line([(x + sd * 30, y), (x + sd * 30, y + 300)], (230, 200, 150), 14)
        cv.circle(x + sd * 30, y - 6, 16, RED, INK, 3)


def banana(cv, x, y, s=1.0):
    pts = [(x - 120 * s, y - 40 * s), (x - 60 * s, y + 30 * s), (x + 30 * s, y + 45 * s), (x + 110 * s, y + 5 * s),
           (x + 130 * s, y - 20 * s), (x + 70 * s, y + 5 * s), (x - 10 * s, y + 5 * s), (x - 80 * s, y - 30 * s)]
    cv.poly(pts, (250, 215, 60), INK, 5)
    cv.rect((x - 140 * s, y - 60 * s, x - 112 * s, y - 34 * s), (110, 80, 40), INK, 3)


def door(cv, x0, y0, x1, y1):
    cv.rect((x0, y0, x1, y1), (120, 90, 70), INK, 6)
    cv.circle(x1 - 30, (y0 + y1) / 2, 12, YELLOW, INK, 3)
    cv.rect((x0 + 10, y0 - 90, x1 - 10, y0 - 20), GREEN, INK, 4, r=10)
    cv.text(((x0 + x1) / 2, y0 - 35), "AUSGANG", font(36, "Black"), WHITE, "ms")


def progress(cv, y, p, col=GREEN, txt=None):
    cv.rect((120, y, 880, y + 80), WHITE, INK, 6, r=40)
    if p > 0.02:
        cv.rect((132, y + 12, 132 + (868 - 132) * min(1, p), y + 68), col, None, 0, r=30)
    cv.text((500, y + 58), txt or f"{int(p * 100)} %", font(44, "Black"), INK, "ms")


# ------------------------------------------------------------------ scenes (cv, t, dur, ta)
def s_hook(cv, t, dur, ta):
    if ta < SHOCK:   # 1-frame shock: red flash, you made it all wrong
        gym(cv)
        cv.overlay((220, 40, 50), int(150 * max(0.3, 1 - ta / 0.4)))
        hero(cv, 540, 1800, 1.0, "shock", "down", bulk=0.15, blink=False)
        label(cv, UX, 640, "DU MACHST ES FALSCH", RED, WHITE, 60, k=seg(ta, 0, 0.2) * 1.0)
        return
    gym(cv, mirror=False)
    mirror_frame(cv, 520, 590, 980, 1300)
    hero(cv, 750, 1400, 0.58, "sad", "down", bulk=0.15, blink=blink_at(ta))     # reflection: still the same
    cv.rect((0, 1400, W, H), (70, 74, 82))
    hero(cv, 270, 1830, 0.85, "worry" if ta < cue("Warum") else "shock", "flex", bulk=0.15, blink=blink_at(ta))
    if ta >= cue("Kein Muskel"):
        label(cv, 260, 640, "MUSKELN: 0", WHITE, RED, 44, k=seg(ta, cue("Kein Muskel"), cue("Kein Muskel") + 0.2) * 1.0)
    if ta >= cue("Warum"):
        cv.text((750, 760), "?", font(int(260 * (0.6 + 0.4 * ease(seg(ta, cue("Warum"), cue("Warum") + 0.3)))), "Black"),
                RED, "ms")


def s_err1(cv, t, dur, ta):
    gym(cv)
    legs = ta >= cue("Beine")
    hero(cv, 380 if ta >= cue("Du siehst") else 540, 1800, 0.95, "smug" if not legs else "worry", "flex",
         bulk=1.0, leg_scale=0.35, blink=blink_at(ta))
    label(cv, 300, 640, "BRUST + ARME", GREEN, YELLOW, 46, k=seg(ta, cue("Du trainierst"), cue("Du trainierst") + 0.2) * 1.0)
    if legs:
        label(cv, 300, 760, "BEINE: NIE", RED, WHITE, 46, k=seg(ta, cue("Beine"), cue("Beine") + 0.2) * 1.0)
        for sd in (-1, 1):
            cv.circle(380 + sd * 30 if ta >= cue("Du siehst") else 540 + sd * 30, 1640, 60, None, RED, 6)
    if ta >= cue("Du siehst"):
        k = ease(seg(ta, cue("Du siehst"), cue("Du siehst") + 0.5))
        bulb(cv, 820, 1060 + (1 - k) * 300, 0.9)
        matches(cv, 820, 1260 + (1 - k) * 300)
        label(cv, 820, 900, "=", WHITE, INK, 60)


def s_err2(cv, t, dur, ta):
    gym(cv)
    rack(cv)
    heavy = ta >= cue("Du nimmst")
    wob = math.sin(ta * 9) * (22 if ta >= cue("Du schwingst") else 6)
    lift = 0.45 + 0.15 * math.sin(ta * 5)
    hero(cv, 560 + wob, 1800, 0.8, "angry" if ta < cue("Du schwingst") else "shock", "bar", bulk=0.4,
         lift=lift, blink=blink_at(ta))
    if heavy:
        label(cv, 300, 640, "200 KG", RED, WHITE, 64, k=seg(ta, cue("Du nimmst"), cue("Du nimmst") + 0.2) * 1.0)
    if ta >= cue("Du schwingst") + 1.4:
        pain(cv, 560 + wob, 1330, math.sin(ta * 10))
        label(cv, 800, 1000, "AUA!", RED, WHITE, 56)


def s_err3(cv, t, dur, ta):
    gym(cv)
    hero(cv, 720, 1800, 0.8, "worry", "down", bulk=0.25, blink=blink_at(ta), look=(-1, -1))
    names = ["Mo", "Di", "Mi", "Do", "Fr"]
    acts = ["Yoga", "Boxen", "Bizeps", "Spinning", "Bizeps"]
    cv.rect((70, 560, 560, 1150), WHITE, INK, 6, r=20)
    cv.rect((70, 560, 560, 640), RED, None, 0, r=20)
    cv.rect((70, 620, 560, 640), RED)
    cv.text((315, 620), "DEIN PLAN?", font(42, "Black"), WHITE, "ms")
    n = int(seg(ta, cue("Jedes Mal"), cue("Jedes Mal") + 1.6) * 5 + 0.999)
    for k in range(n):
        y = 700 + k * 92
        cv.text((110, y + 40), names[k], font(40, "Black"), INK)
        cv.text((230, y + 40), acts[k], font(40, "Bold"), (120, 60, 160))
    if ta >= cue("Kein Plan"):
        cv.line([(90, 600), (540, 1130)], RED, 14)
        cv.line([(540, 600), (90, 1130)], RED, 14)
    if ta >= cue("Dein Körper"):
        for j, (x, y) in enumerate(((640, 720), (790, 660), (920, 740))):
            if ta >= cue("Dein Körper") + j * 0.3:
                cv.text((x, y), "?", font(100, "Black"), RED, "ms")


def s_err4(cv, t, dur, ta):
    cv.rect((0, 0, W, H), (246, 236, 220))
    cv.rect((0, 1200, W, H), (180, 130, 90))
    hero(cv, 540, 1800, 0.85, "happy" if ta < cue("Und isst") else "sad", "down", bulk=0.3, blink=blink_at(ta))
    cv.rect((40, 1400, 1040, 1460), (150, 100, 70), INK, 5)
    cv.rect((80, 1460, 1000, 1700), (130, 88, 60), INK, 5)
    cv.ellipse((350, 1310, 730, 1450), WHITE, INK, 6)                          # empty plate
    cv.ellipse((400, 1335, 680, 1425), (240, 240, 240))
    if ta < cue("Und isst"):
        for j in range(3):                                                      # sweat = hard training
            ph = (ta * 0.9 + j / 3) % 1
            cv.circle(420 + j * 110, 820 + 120 * ph, 14, (120, 190, 240), INK, 2)
        label(cv, 300, 640, "HART TRAINIERT", GREEN, YELLOW, 46)
    else:
        k = ease(seg(ta, cue("Und isst"), cue("Und isst") + 0.4))
        banana(cv, 540, 1370 - 30 * k, 0.9)
        label(cv, 300, 640, "NUR 1 BANANE", RED, WHITE, 50, k=k * 1.0)
    if ta >= cue("Das war"):
        label(cv, 750, 800, "= 0 EIWEISS", WHITE, RED, 46)


def s_pause(cv, t, dur, ta):
    gym(cv)
    hero(cv, 540, 1800, 1.0, "shock", "down", bulk=0.3, blink=False)
    if ta >= cue("Jetzt kommt"):
        label(cv, UX, 700, "DER GRÖSSTE FEHLER", RED, WHITE, 62, k=seg(ta, cue("Jetzt kommt"), cue("Jetzt kommt") + 0.2) * 1.0)
    if ta >= cue("Den machen"):
        label(cv, UX, 830, "fast alle", WHITE, INK, 46)


def s_err5(cv, t, dur, ta):
    gym(cv, mirror=False)
    door(cv, 780, 760, 1010, 1300)
    quits = ta >= cue("Und du hörst")
    k = ease(seg(ta, cue("Und du hörst"), cue("Und du hörst") + 1.4))
    x = 420 + 520 * k
    hero(cv, x, 1800, 0.8, "sad", "down", bulk=0.3, blink=blink_at(ta),
         bob=-abs(math.sin(ta * 10)) * 10 if 0 < k < 1 else 0)
    p = 0.95 * ease(seg(ta, cue("Fehler fünf"), cue("Und du hörst")))
    progress(cv, 600, p, GREEN if not quits else (230, 160, 40), txt=f"MUSKELN {int(p * 100)} %")
    if ta >= cue("Nach drei"):
        label(cv, 300, 800, "3 WOCHEN", WHITE, INK, 44)
    if ta >= cue("Genau dann"):
        label(cv, 420, 1000, "Du warst fast da.", YELLOW, INK, 54, k=seg(ta, cue("Genau dann"), cue("Genau dann") + 0.2) * 1.0)


def s_stay(cv, t, dur, ta):
    gym(cv)
    g = ease(seg(ta, cue("Muskeln wachsen"), cue("Wenn du bleibst") + 0.8))
    hero(cv, 540, 1800, 0.95, "happy" if g < 0.9 else "smug", "flex" if g > 0.5 else "down", bulk=0.3 + 0.7 * g,
         blink=blink_at(ta))
    progress(cv, 600, 0.95 + 0.05 * g, GREEN, txt=f"MUSKELN {int((0.95 + 0.05 * g) * 100)} %")
    if ta >= cue("Wenn du bleibst"):
        label(cv, UX, 800, "DRANBLEIBEN", GREEN, YELLOW, 60, k=seg(ta, cue("Wenn du bleibst"), cue("Wenn du bleibst") + 0.2) * 1.0)


def s_final(cv, t, dur, ta):
    gym(cv)
    hero(cv, 540, 1800, 0.95, "smug", "point", bulk=1.0, blink=blink_at(ta))
    if ta >= cue("Und schick"):
        label(cv, UX, 860, "@dein.gym.partner", WHITE, BLUE, 46)


def buttons(img, ta):
    d = ImageDraw.Draw(img, "RGBA")
    f = T.font(64, "Black")
    for k in range(5):
        x = 140 + k * 180
        hot = ta >= cue("Schreib") and int((ta - cue("Schreib")) * 3) % 5 == k
        d.ellipse((x - 70, 1330, x + 70, 1470), fill=YELLOW if hot else WHITE, outline=INK, width=6)
        d.text((x, 1428), str(k + 1), font=f, fill=RED if hot else INK, anchor="ms")


SCENES = [s_hook, s_err1, s_err2, s_err3, s_err4, s_pause, s_err5, s_stay, s_final]
PAUSE = 5
UI_SCENES = (0, 3, 6)
INNER_CUTS = [SHOCK]


def render(i, t=0.5, dur=5.0, ta=None):
    ta = BOUNDS[i][0] + t * (BOUNDS[i][1] - BOUNDS[i][0]) if ta is None else ta
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur, ta)
    img = cv.final()
    if i in UI_SCENES:
        img = T.camera(img, 0.0, 500, 810)
    else:
        img = T.camera(img, 0.02 + 0.06 * ease(t), 540, 960)
    if i == len(SCENES) - 1:
        buttons(img, ta)
    if i == PAUSE and ta < cue("Jetzt kommt"):
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, ta):
    if i == 0 and ta < SHOCK:
        return ("", "white")
    return [("3 MONATE: 0 %", "red"), ("FEHLER 1", "red"), ("FEHLER 2", "red"), ("FEHLER 3", "red"),
            ("FEHLER 4", "red"), ("", "white"), ("FEHLER 5", "red"), ("WENN DU BLEIBST", "green"),
            ("WELCHER FEHLER?", "yellow")][i]
