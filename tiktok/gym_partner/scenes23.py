"""Scenes for 'SCHICK DAS DEINEM GYM-PARTNER, DER IMMER ABSAGT' (STIL 3, T.HERO athletic rig).

ER = the sender (T.HERO, black tank top, gets broader every week). DU = the friend who always cancels
(orange hoodie, curly hair) – he stays thin.

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


KUMPEL = dict(hoodie=(235, 130, 40), hair=(150, 90, 40), outfit="hoodie", hair_style="curly")
PX0, PY0, PX1, PY1 = 170, 470, 830, 1150


def kumpel(cv, x, y, s, mood, arms="down", **kw):
    return T.character(cv, x, y, s, mood, arms, **dict(KUMPEL, **kw))


def living_room(cv):
    cv.rect((0, 0, W, H), (236, 222, 200))
    cv.rect((0, 1300, W, H), (160, 120, 85))
    cv.rect((620, 560, 980, 800), (40, 40, 48), INK, 6, r=10)          # TV
    cv.rect((640, 580, 960, 780), (70, 100, 150))
    cv.rect((60, 1200, 1020, 1330), (110, 140, 90), INK, 6, r=40)       # sofa back
    cv.rect((60, 1120, 160, 1420), (100, 130, 80), INK, 6, r=30)
    cv.rect((920, 1120, 1020, 1420), (100, 130, 80), INK, 6, r=30)


def sofa_front(cv):
    cv.rect((60, 1330, 1020, 1420), (120, 150, 100), INK, 6, r=30)
    cv.rect((60, 1410, 1020, 1600), (100, 130, 80), INK, 6, r=30)


def phone(cv, title):
    cv.rect((PX0 - 18, PY0 - 18, PX1 + 18, PY1 + 18), (24, 24, 30), INK, 6, r=46)
    cv.rect((PX0, PY0, PX1, PY1), (245, 247, 250))
    cv.rect((PX0, PY0, PX1, PY0 + 90), (230, 233, 240))
    cv.text((UX, PY0 + 60), title, font(38, "Black"), INK, "ms")


def bubble(cv, y, text, mine, k=1.0, time=None):
    if k <= 0:
        return
    f = T.font(40, "Bold")
    tw = cv.d.textlength(text, font=f)
    w = tw + 60
    x0 = PX1 - 30 - w if mine else PX0 + 30
    col = (60, 180, 90) if mine else (225, 228, 235)
    cv.rect((x0, y, x0 + w, y + 80), col, None, 0, r=30)
    cv.text((x0 + 30, y + 54), text, font(40, "Bold"), WHITE if mine else INK, "ls")
    if time:
        cv.text((x0 + w - 4 if mine else x0 + 4, y + 112), time, font(26, "Bold"), (140, 140, 150), "rs" if mine else "ls")


def bench(cv, x, y):
    cv.rect((x - 260, y - 40, x + 260, y), (40, 42, 50), INK, 5, r=12)
    for sd in (-1, 1):
        cv.rect((x + sd * 200 - 15, y, x + sd * 200 + 15, y + 150), (90, 92, 100), INK, 4)
        cv.rect((x + sd * 170 - 15, y - 330, x + sd * 170 + 15, y - 40), (90, 92, 100), INK, 4)
    cv.line([(x - 330, y - 320), (x + 330, y - 320)], (110, 112, 120), 18)
    for sd in (-1, 1):
        for k in range(2):
            px = x + sd * (270 + k * 40)
            cv.rect((px - 16, y - 420, px + 16, y - 220), (40, 42, 50), INK, 4, r=6)


def doener(cv, x, y, s=1.0):
    cv.poly([(x - 110 * s, y - 60 * s), (x + 110 * s, y - 60 * s), (x + 20 * s, y + 140 * s), (x - 20 * s, y + 140 * s)],
            (230, 190, 120), INK, 5)
    for k, c in enumerate(((200, 120, 60), (90, 170, 80), (220, 60, 50), (245, 245, 240))):
        cv.ellipse((x - 95 * s + k * 45 * s, y - 85 * s, x - 45 * s + k * 45 * s, y - 35 * s), c, INK, 3)
    cv.rect((x - 70 * s, y + 20 * s, x + 70 * s, y + 70 * s), WHITE, INK, 3)
    cv.text((x, y + 60 * s), "DÖNER", font(int(28 * s), "Black"), RED, "ms")


def gymbag(cv, x, y, s=1.0):
    cv.rect((x - 90 * s, y - 60 * s, x + 90 * s, y + 60 * s), (40, 90, 200), INK, 5, r=int(26 * s))
    cv.line([(x - 50 * s, y - 60 * s), (x, y - 120 * s), (x + 50 * s, y - 60 * s)], INK, 7)


def tag(cv, x, y, text, col):
    label(cv, x, y, text, col, WHITE, 40)


# ------------------------------------------------------------------ scenes (cv, t, dur, ta)
def s_hook(cv, t, dur, ta):
    if ta < SHOCK or ta >= cue("Du bist"):            # you are meant – he points at you
        gym(cv)
        if ta < SHOCK:
            cv.overlay((255, 255, 255), int(170 * max(0, 1 - ta / 0.25)))
        hero(cv, 540, 1720, 1.0, "smug" if ta >= cue("Du bist") else "angry", "point", bulk=0.8, blink=blink_at(ta))
        label(cv, UX, 680, "DU BIST GEMEINT" if ta >= cue("Du bist") else "DU!", YELLOW, INK, 64,
              k=seg(ta, cue("Du bist") if ta >= cue("Du bist") else 0, (cue("Du bist") if ta >= cue("Du bist") else 0) + 0.2) * 1.0)
        return
    living_room(cv)
    kumpel(cv, 780, 1640, 0.62, "neutral", "phone", blink=blink_at(ta))
    sofa_front(cv)
    tag(cv, 780, 900 + 0 * 1, "DU", (235, 130, 40))
    phone(cv, "Gym-Partner")
    cv.rect((PX0 + 40, PY0 + 130, PX1 - 40, PY0 + 470), (30, 30, 40), None, 0, r=24)
    cv.poly([(UX - 40, PY0 + 250), (UX - 40, PY0 + 350), (UX + 50, PY0 + 300)], WHITE)
    cv.rect((PX0 + 40, PY0 + 500, PX1 - 40, PY0 + 590), (60, 140, 250), None, 0, r=30)
    cv.text((UX, PY0 + 558), "Schau dir das an!", font(38, "Black"), WHITE, "ms")


def s_cancel(cv, t, dur, ta):
    living_room(cv)
    phone(cv, "Gym-Partner")
    bubble(cv, PY0 + 130, "Montag Gym? 💪".replace(" 💪", "?").replace("??", "?"), False, time="Mo 09:12")
    if ta >= cue("Montag"):
        bubble(cv, PY0 + 270, "Ich komme!", True, k=seg(ta, cue("Ich komme"), cue("Ich komme") + 0.2) * 1.0, time="09:13")
    if ta >= cue("Eine Nachricht"):
        cv.rect((PX0 + 200, PY0 + 420, PX1 - 200, PY0 + 480), (230, 233, 240), None, 0, r=20)
        cv.text((UX, PY0 + 462), "17:00", font(32, "Black"), (120, 120, 130), "ms")
    if ta >= cue("Heute schaff"):
        bubble(cv, PY0 + 510, "Heute schaff ich's nicht", True, k=1.0, time="17:00")
        label(cv, UX, PY1 - 60, "ABGESAGT", RED, WHITE, 52, k=seg(ta, cue("Heute schaff") + 0.4, cue("Heute schaff") + 0.6) * 1.0)


def s_excuses(cv, t, dur, ta):
    if ta < cue("Und er steht"):
        living_room(cv)
        kumpel(cv, 540, 1700, 0.78, "worry", "down", blink=blink_at(ta))
        sofa_front(cv)
        cv.rect((90, 450, 910, 830), WHITE, INK, 6, r=20)
        cv.rect((90, 450, 910, 530), RED, None, 0, r=20)
        cv.rect((90, 510, 910, 530), RED)
        cv.text((UX, 510), "SEINE AUSREDEN", font(44, "Black"), WHITE, "ms")
        rows = [("Mittwoch", "Mi", "Rücken", "Rücken"), ("Freitag", "Fr", "Zu müde", "Zu müde"),
                ("Samstag", "Sa", "Grillen", "Grillen")]
        for k, (key, day, ekey, txt) in enumerate(rows):
            x = 110 + k * 270
            if ta >= cue(key):
                cv.text((x + 125, 610), day, font(48, "Black"), INK, "ms")
            if ta >= cue(ekey):
                cv.rect((x + 10, 650, x + 240, 740), (255, 236, 236), RED, 4, r=16)
                cv.text((x + 125, 712), txt, font(38, "Black"), RED, "ms")
                cv.line([(x + 60, 770), (x + 190, 800)], RED, 8)
                cv.line([(x + 190, 770), (x + 60, 800)], RED, 8)
        return
    gym(cv)
    bench(cv, 540, 1450)
    hero(cv, 340, 1720, 0.85, "sad", "down", bulk=0.5, blink=blink_at(ta))
    tag(cv, 340, 640, "ER", (40, 140, 70))
    cv.rect((620, 960, 900, 1700), None, (150, 150, 160), 6, r=60)          # empty place
    cv.text((760, 1250), "?", font(140, "Black"), (150, 150, 160), "ms")
    label(cv, 760, 900, "DEIN PLATZ", WHITE, INK, 40)


def s_split(cv, t, dur, ta):
    k = ease(seg(ta, cue("Er wird"), cue("Und du nicht") + 0.4))
    gym(cv, mirror=False)
    cv.rect((540, 0, W, H), (236, 222, 200))                                  # right half: your sofa
    cv.rect((540, 1300, W, H), (160, 120, 85))
    cv.rect((560, 1250, 1060, 1330), (110, 140, 90), INK, 6, r=30)
    hero(cv, 270, 1720, 0.62, "smug" if k > 0.5 else "happy", "flex" if k > 0.3 else "down", bulk=0.4 + 0.6 * k,
         blink=blink_at(ta))
    kumpel(cv, 800, 1620, 0.55, "sad" if ta >= cue("Und du nicht") else "neutral", "phone", blink=blink_at(ta + 1))
    cv.rect((560, 1330, 1060, 1420), (120, 150, 100), INK, 6, r=30)
    cv.line([(540, 0), (540, H)], INK, 10)
    tag(cv, 270, 640, "ER", (40, 140, 70))
    tag(cv, 800, 640, "DU", (235, 130, 40))
    week = 1 + int(19 * k)
    label(cv, 270, 780, f"WOCHE {week}", WHITE, INK, 40)
    label(cv, 800, 780, f"WOCHE {week}", WHITE, INK, 40)
    if ta >= cue("Er wird"):
        label(cv, 270, 900, f"+{int(20 * k)} kg", GREEN, YELLOW, 48)
    if ta >= cue("Und du nicht"):
        label(cv, 800, 900, "+0 kg", RED, WHITE, 48)


def s_pause(cv, t, dur, ta):
    living_room(cv)
    kumpel(cv, 540, 1700, 0.8, "worry" if ta < cue("Wie oft") else "shock", "down", blink=False)
    sofa_front(cv)
    if ta >= cue("Wie oft"):
        n = int(47 * ease(seg(ta, cue("Wie oft"), cue("Wie oft") + 1.6)))
        cv.rect((200, 480, 800, 760), WHITE, INK, 6, r=26)
        cv.text((UX, 560), "ABGESAGT", font(48, "Black"), RED, "ms")
        cv.text((UX, 720), f"{n}×", font(130, "Black"), INK, "ms")


def s_deal(cv, t, dur, ta):
    gym(cv)
    hero(cv, 820, 1720, 0.72, "happy", "point", bulk=0.9, blink=blink_at(ta))
    x0, y0, x1, y1 = 70, 470, 640, 1150
    cv.rect((x0, y0, x1, y1), (250, 246, 236), INK, 6, r=12)
    cv.text(((x0 + x1) / 2, y0 + 75), "SEIN ANGEBOT", font(48, "Black"), INK, "ms")
    cv.line([(x0 + 40, y0 + 105), (x1 - 40, y0 + 105)], INK, 4)
    rows = [("Er holt", "Er holt dich ab"), ("Er packt", "Er packt die Tasche"), ("Und nach", "Döner danach"),
            ("Er zahlt", "Er zahlt")]
    for k, (key, lab) in enumerate(rows):
        y = y0 + 150 + k * 115
        cv.rect((x0 + 35, y, x0 + 95, y + 60), WHITE, INK, 4, r=8)
        cv.text((x0 + 120, y + 45), lab, font(38, "Bold"), INK)
        if ta >= cue(key) + 0.3:
            cv.line([(x0 + 45, y + 30), (x0 + 63, y + 52), (x0 + 90, y + 8)], GREEN, 10)
    if ta >= cue("Er packt"):
        gymbag(cv, 860, 700, 0.8 * (0.6 + 0.4 * ease(seg(ta, cue("Er packt"), cue("Er packt") + 0.3))))
    if ta >= cue("Und nach"):
        doener(cv, 860, 880, 0.75 * (0.6 + 0.4 * ease(seg(ta, cue("Und nach"), cue("Und nach") + 0.3))))


def s_rule(cv, t, dur, ta):
    gym(cv)
    hero(cv, 540, 1720, 1.0, "angry", "down", bulk=1.0, blink=blink_at(ta))
    label(cv, UX, 650, "NUR EINE BEDINGUNG", WHITE, INK, 46)
    if ta >= cue("Ab heute"):
        label(cv, UX, 800, "KEINE AUSREDEN MEHR", RED, WHITE, 60, k=seg(ta, cue("Ab heute"), cue("Ab heute") + 0.25) * 1.0)


def s_final(cv, t, dur, ta):
    street(cv)
    hero(cv, 300, 1720, 0.8, "happy", "point", bulk=1.0, blink=blink_at(ta))
    gymbag(cv, 790, 1140, 0.8)
    label(cv, 790, 1010, "DEINE TASCHE", WHITE, INK, 32)
    if ta >= cue("Und markier"):
        label(cv, UX, 720, "@der.absager", WHITE, BLUE, 46)


def buttons(img):
    d = ImageDraw.Draw(img, "RGBA")
    f = T.font(60, "Black")
    for (x0, x1), lab, bg, fg in (((90, 460), "JA", (40, 140, 70), YELLOW), ((540, 910), "NEIN", RED, WHITE)):
        d.rounded_rectangle((x0, 1340, x1, 1450), 28, fill=bg, outline=INK, width=6)
        d.text(((x0 + x1) / 2, 1418), lab, font=f, fill=fg, anchor="ms")


SCENES = [s_hook, s_cancel, s_excuses, s_split, s_pause, s_deal, s_rule, s_final]
PAUSE = 4
UI_SCENES = (0, 1, 2, 3, 5)
INNER_CUTS = [SHOCK, cue("Du bist"), cue("Und er steht")]


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
        buttons(img)
    if i == PAUSE and ta < cue("Jetzt sei"):
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, ta):
    if i == 0 and (ta < SHOCK):
        return ("", "white")
    return [("FÜR DEN ABSAGER", "yellow"), ("MONTAG", "white"), ("ER WARTET. WIEDER.", "red"),
            ("ER: STÄRKER · DU: NICHT", "red"), ("", "white"), ("SEIN ANGEBOT", "green"),
            ("AB HEUTE", "red"), ("KOMMST DU MORGEN MIT?", "yellow")][i]
