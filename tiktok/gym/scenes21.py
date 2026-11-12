"""Scenes for 'STELL DIR VOR, DU ZIEHST AB HEUTE GYM DURCH' (STIL 3, T.HERO).

The hero gets broader over the video: T.character(..., bulk=0..1, outfit="tank").
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


def cue(text):
    return next(a / TEMPO for a, b, s, t in PHRASES if t.startswith(text))


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


# ------------------------------------------------------------------ scenes (cv, t, dur, ta)
def s_hook(cv, t, dur, ta):
    if ta < SHOCK:   # 1-frame shock: you, in one year
        gym(cv)
        cv.overlay((255, 255, 255), int(180 * max(0, 1 - ta / 0.25)))
        hero(cv, 540, 1800, 1.08, "smug", "flex", bulk=1.0)
        label(cv, UX, 680, "DU – IN 1 JAHR", YELLOW, INK, 60, k=seg(ta, 0, 0.2) * 1.0)
        return
    street(cv)
    hero(cv, 540, 1760, 0.72, "worry" if ta < cue("Heute") else "neutral", "down", bulk=0.0, tank=False,
         blink=blink_at(ta), talk=0.0)
    cv.rect((620, 1500, 760, 1600), (40, 90, 200), INK, 5, r=20)     # gym bag
    cv.line([(640, 1500), (690, 1450), (740, 1500)], INK, 6)
    items = [("Kein Montag", "MONTAG", 120), ("Kein Neujahr", "NEUJAHR", 380)]
    for key, lab, y in items:
        if ta >= cue(key):
            label(cv, 300 + (0 if lab == "MONTAG" else 380), 720 + 0 * y, lab, WHITE, INK, 46,
                  k=seg(ta, cue(key), cue(key) + 0.2) * 1.0)
            x = 300 + (0 if lab == "MONTAG" else 380)
            cv.line([(x - 150, 700), (x + 150, 660)], RED, 12)
    if ta >= cue("Heute"):
        label(cv, UX, 860, "HEUTE ✓".replace(" ✓", "!"), GREEN, YELLOW, 70, k=seg(ta, cue("Heute"), cue("Heute") + 0.2) * 1.0)


def machine(cv, x, y):
    """A strange gym machine with cables (the one nobody understands)."""
    cv.rect((x - 20, y - 520, x + 20, y), (90, 92, 100), INK, 4)
    cv.rect((x + 180, y - 520, x + 220, y), (90, 92, 100), INK, 4)
    cv.rect((x - 40, y - 540, x + 240, y - 500), (90, 92, 100), INK, 4, r=8)
    for k in range(6):
        cv.rect((x + 30, y - 260 + k * 34, x + 170, y - 232 + k * 34), (40, 42, 50), INK, 3)
    cv.line([(x + 100, y - 500), (x + 100, y - 260)], INK, 4)
    cv.line([(x + 220, y - 480), (x + 330, y - 300), (x + 300, y - 120)], INK, 4)
    cv.rect((x + 270, y - 140, x + 340, y - 100), (200, 40, 50), INK, 3, r=10)
    cv.rect((x - 120, y - 180, x + 10, y - 140), (200, 40, 50), INK, 3, r=10)


def s_day1(cv, t, dur, ta):
    gym(cv, mirror=False)
    machine(cv, 560, 1150)
    sure = ta >= cue("Egal")
    hero(cv, 300, 1760, 0.8, "happy" if sure else "worry", "down", bulk=0.0,
         blink=blink_at(ta), look=(1, -1) if not sure else (0, 0))
    if not sure and ta >= cue("Du weißt") + 0.4:
        for j, (x, y) in enumerate(((620, 520), (780, 470), (900, 560))):
            if ta >= cue("Du weißt") + 0.4 + j * 0.3:
                cv.text((x, y), "?", font(110, "Black"), RED, "ms")
    if ta >= cue("Du bist da"):
        label(cv, 300, 560, "DU BIST DA ✓".replace(" ✓", ""), GREEN, YELLOW, 52, k=seg(ta, cue("Du bist da"), cue("Du bist da") + 0.2) * 1.0)
    if ta >= cue("Das ist der"):
        label(cv, 300, 680, "= schwerster Teil", WHITE, INK, 40)


def s_week1(cv, t, dur, ta):
    stairs(cv)
    k = ease(seg(ta, cue("Treppen"), cue("Aber du")))
    x = 330 + 260 * k                       # slowly climbing
    y = 1610 - 220 * k
    hero(cv, x, y, 0.72, "worry" if ta < cue("Aber du") else "angry", "down", bulk=0.1, tank=False,
         blink=blink_at(ta), bob=-abs(math.sin(ta * 6)) * 12 if 0 < k < 1 else 0)
    if ta >= cue("Muskelkater"):
        for (px, py) in ((x - 60, y - 180), (x + 60, y - 180), (x - 150, y - 520), (x + 150, y - 520)):
            pain(cv, px, py, math.sin(ta * 8))
        label(cv, UX, 560, "MUSKELKATER", RED, WHITE, 56, k=seg(ta, cue("Muskelkater"), cue("Muskelkater") + 0.2) * 1.0)
    if ta >= cue("Aber du"):
        label(cv, UX, 680, "trotzdem ✓".replace(" ✓", "!"), GREEN, YELLOW, 50)


def s_tips(cv, t, dur, ta):
    gym(cv)
    if ta < cue("Tipp zwei"):          # 3x per week, full body, 45 min – squat with barbell
        rack(cv)
        lift = 0.5 + 0.5 * math.sin(ta * 3.2)
        hero(cv, 640, 1800, 0.78, "angry", "bar", bulk=0.25, lift=lift, blink=blink_at(ta))
        label(cv, 300, 560, "TIPP 1", YELLOW, INK, 56)
        if ta >= cue("Dreimal"):
            calendar(cv, 90, 620, 500, days_marked=(0, 2, 4), title="3× PRO WOCHE")
        if ta >= cue("Ganzkörper"):
            label(cv, 300, 920, "GANZKÖRPER", WHITE, INK, 42)
        if ta >= cue("Fünfundvierzig"):
            label(cv, 300, 1030, "⏱ 45 MIN".replace("⏱ ", ""), WHITE, BLUE, 42)
    elif ta < cue("Tipp drei"):        # progressive overload – dumbbell curls, weight grows
        rack(cv)
        lift = 0.5 + 0.5 * math.sin(ta * 4.0)
        hero(cv, 640, 1800, 0.8, "angry", "curl", bulk=0.4, lift=lift, blink=blink_at(ta))
        label(cv, 300, 560, "TIPP 2", YELLOW, INK, 56)
        kg = 10.0 + 2.5 * min(4, int(max(0, ta - cue("Jede Woche")) / 0.6))
        cv.rect((90, 640, 510, 880), WHITE, INK, 6, r=20)
        cv.text((300, 710), "JEDE WOCHE", font(40, "Black"), INK, "ms")
        cv.text((300, 830), f"{kg:.1f} kg".replace(".0", "").replace(".", ","), font(96, "Black"), GREEN, "ms")
        if ta >= cue("Nur ein"):
            label(cv, 300, 990, "+ nur ein bisschen", WHITE, INK, 38)
    else:                              # protein + sleep
        if ta < cue("Und schlaf"):
            cv.rect((0, 0, W, H), (246, 236, 220))
            cv.rect((0, 1200, W, H), (180, 130, 90))
            hero(cv, 540, 1800, 0.8, "happy", "down", bulk=0.5, talk=0.0, blink=blink_at(ta))
            cv.rect((40, 1400, 1040, 1460), (150, 100, 70), INK, 5)               # table in front of you
            cv.rect((80, 1460, 1000, 1700), (130, 88, 60), INK, 5)
            plate(cv, 540, 1380)
            label(cv, 300, 560, "TIPP 3", YELLOW, INK, 56)
            label(cv, 700, 700, "EIWEISS", GREEN, YELLOW, 52, k=seg(ta, cue("Iss genug"), cue("Iss genug") + 0.2) * 1.0)
        else:
            T.bedroom(cv, night=True)
            cv.rect((140, 1150, 940, 1420), (240, 240, 250), INK, 6, r=30)     # bed
            cv.rect((140, 1100, 340, 1180), WHITE, INK, 5, r=20)
            cv.circle(260, 1080, 90, T.SKIN, INK, 6)                             # sleeping head
            cv.arc((200, 1050, 240, 1090), 20, 160, INK, 5)
            cv.arc((280, 1050, 320, 1090), 20, 160, INK, 5)
            cv.rect((340, 1120, 940, 1300), (80, 120, 200), INK, 6, r=24)       # blanket
            zzz(cv, 380, 980, ta)
            label(cv, 680, 700, "8 STUNDEN", WHITE, BLUE, 56)
            if ta >= cue("Denn im"):
                label(cv, 680, 820, "MUSKELN WACHSEN", GREEN, YELLOW, 44,
                      k=seg(ta, cue("Denn im"), cue("Denn im") + 0.2) * 1.0)


def s_months(cv, t, dur, ta):
    gym(cv)
    if ta < cue("Monat sechs"):        # t-shirt gets tight at the shoulders
        hero(cv, 540, 1800, 0.92, "smug", "down", bulk=0.6, tank=False, blink=blink_at(ta))
        if ta >= cue("An den"):
            for sd in (-1, 1):
                x = 540 + sd * 250
                for j in range(3):
                    cv.line([(x - 18 + j * 14, 1010), (x - 10 + j * 14, 1050)], INK, 4)
            label(cv, UX, 700, "ZU ENG!", RED, WHITE, 60, k=seg(ta, cue("An den"), cue("An den") + 0.2) * 1.0)
    else:                              # somebody asks: do you train?
        hero(cv, 330, 1800, 0.85, "smug", "down", bulk=0.8, blink=blink_at(ta))
        T.character(cv, 820, 1800, 0.7, "shock" if ta >= cue("Trainierst") else "neutral", "down",
                    talk=talking(ta, (4,)) if ta >= cue("Jemand") else 0.0, blink=blink_at(ta + 1.1),
                    **dict(hoodie=(80, 110, 200), hair=(150, 90, 40), hair_style="curly", outfit="hoodie"))
        if ta >= cue("Trainierst"):
            cv.rect((560, 560, 1000, 700), WHITE, INK, 6, r=30)
            cv.poly([(760, 696), (820, 696), (800, 760)], WHITE, INK, 6)
            cv.rect((764, 690, 816, 702), WHITE)
            cv.text((780, 650), "Trainierst du?", font(46, "Black"), INK, "ms")


def s_year(cv, t, dur, ta):
    gym(cv, mirror=False)
    mirror_frame(cv, 440, 470, 980, 1400)
    hero(cv, 710, 1500, 0.78, "shock" if ta >= cue("Und erkennst") else "happy", "flex", bulk=1.0,
         blink=blink_at(ta))                                                       # reflection
    cv.rect((0, 1400, W, H), (70, 74, 82))
    hero(cv, 250, 1860, 0.82, "shock" if ta >= cue("Und erkennst") else "neutral", "down", bulk=1.0,
         blink=blink_at(ta), look=(1, 0))
    if ta >= cue("Und erkennst"):
        label(cv, 710, 560, "BIST DAS DU?", WHITE, INK, 46, k=seg(ta, cue("Und erkennst"), cue("Und erkennst") + 0.2) * 1.0)


def s_pause(cv, t, dur, ta):
    gym(cv, mirror=False)
    mirror_frame(cv, 560, 470, 1000, 1300)
    hero(cv, 780, 1420, 0.62, "smug", "flex", bulk=1.0, blink=False)                   # the goal
    hero(cv, 280, 1800, 0.8, "worry", "down", bulk=0.0, tank=False, blink=blink_at(ta))   # you today
    label(cv, 280, 560, "DU HEUTE", WHITE, INK, 44)
    label(cv, 780, 560, "IN 1 JAHR", YELLOW, INK, 44)
    if ta >= cue("Heute") - 0.05:
        label(cv, UX, 800, "HEUTE.", GREEN, YELLOW, 110, k=seg(ta, cue("Heute") - 0.05, cue("Heute") + 0.2) * 1.0)


def s_final(cv, t, dur, ta):
    gym(cv)
    hero(cv, 540, 1800, 1.0, "happy", "flex", bulk=1.0, blink=blink_at(ta))
    # a comment typed into the comment field
    txt = "Tag 1 💪".replace(" 💪", "")
    n = int(seg(ta, cue("Schreib"), cue("Schreib") + 0.8) * len(txt) + 0.999)
    if ta >= cue("Schreib"):
        cv.rect((120, 640, 880, 760), WHITE, INK, 6, r=40)
        cv.circle(190, 700, 40, (255, 80, 150), INK, 4)
        cv.text((260, 722), txt[:n] + ("|" if n < len(txt) else ""), font(56, "Black"), INK)
    if ta >= cue("Und markier"):
        label(cv, UX, 880, "@dein.gym.partner", WHITE, BLUE, 46)


SCENES = [s_hook, s_day1, s_week1, s_tips, s_months, s_year, s_pause, s_final]
PAUSE = 6
UI_SCENES = (0, 1, 3, 6)
INNER_CUTS = [SHOCK, cue("Tipp zwei"), cue("Tipp drei"), cue("Und schlaf"), cue("Monat sechs")]


def render(i, t=0.5, dur=5.0, ta=None):
    ta = BOUNDS[i][0] + t * (BOUNDS[i][1] - BOUNDS[i][0]) if ta is None else ta
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur, ta)
    img = cv.final()
    if i in UI_SCENES:
        img = T.camera(img, 0.0, 500, 810)
    else:
        img = T.camera(img, 0.02 + 0.06 * ease(t), 540, 960)
    if i == PAUSE and ta < cue("Das Einzige"):
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, ta):
    if i == 0 and ta < SHOCK:
        return ("", "white")
    if i == 3:
        return ("FORTSCHRITT: 30 %", "green") if ta < cue("Tipp drei") else ("FORTSCHRITT: 50 %", "green")
    if i == 4:
        return ("MONAT 3", "green") if ta < cue("Monat sechs") else ("MONAT 6", "green")
    return [("AB HEUTE: GYM", "yellow"), ("TAG 1", "yellow"), ("WOCHE 1", "red"), ("", "white"), ("", "white"),
            ("1 JAHR", "green"), ("", "white"), ("WANN FÄNGST DU AN?", "yellow")][i]
