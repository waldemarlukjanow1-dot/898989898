"""Scenes for 'VICE CITY – 02:43' (STIL 3, T.HERO). Own art style – no game logos/look. (t, dur, ta), cued to the voice."""
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
RED, GREEN, BLUE = (220, 40, 50), (40, 140, 70), (60, 110, 255)
PINK_N, CYAN_N = (255, 70, 170), (60, 230, 255)
CAR = (250, 200, 30)
PX0, PY0, PX1, PY1 = 170, 500, 830, 1160
BOUNDS, TOTAL = seq_bounds()
GIRL = dict(hoodie=(220, 80, 140), hair=(70, 40, 30), outfit="hoodie", hair_style="curly")


def cue(text):
    return next(a / TEMPO for a, b, s, t in PHRASES if t.startswith(text))


def cue_end(text):
    return next(b / TEMPO for a, b, s, t in PHRASES if t.startswith(text))


def talking(ta, text):
    return abs(math.sin(ta * 10)) if cue(text) <= ta < cue_end(text) else 0.0


def hero(cv, x, y, s, mood, arms="down", **kw):
    return T.character(cv, x, y, s, mood, arms, **dict(T.HERO, **kw))


def blink_at(ta):
    return (ta % 2.7) < 0.1


# ------------------------------------------------------------------ world pieces

def neon_city(cv, ta, scroll=0.0):
    for y in range(0, 1100, 6):
        k = y / 1100
        cv.rect((0, y, W, y + 6), (int(40 + 60 * k), int(10 + 20 * k), int(70 + 40 * k)))
    cv.circle(820, 300, 90, (255, 120, 180, 140))
    rnd = random.Random(11)
    x = -((scroll * 900) % 260) - 20
    i = 0
    while x < W + 260:
        r2 = random.Random(int((x + scroll * 900) // 260) + 99)
        bw, bh = 230, r2.randint(380, 720)
        cv.rect((x, 1100 - bh, x + bw, 1100), (30, 20, 50), INK, 4)
        for wy in range(1100 - bh + 40, 1060, 80):
            for wx in range(int(x) + 25, int(x) + bw - 40, 60):
                cv.rect((wx, wy, wx + 30, wy + 46), (255, 220, 140) if r2.random() < 0.35 else (50, 36, 80))
        cv.rect((x + 30, 1100 - bh + 20, x + bw - 30, 1100 - bh + 60), PINK_N if i % 2 else CYAN_N, r=10)
        x += bw + 30
        i += 1
    for k in range(5):  # palms
        px = ((k * 260 - scroll * 1400) % (W + 300)) - 150
        cv.line([(px, 1180), (px + 20, 860)], (40, 30, 30), 18)
        for a in range(6):
            ang = math.radians(200 + a * 28)
            cv.line([(px + 20, 860), (px + 20 + math.cos(ang) * 130, 860 + math.sin(ang) * 70 + 40)], (20, 90, 60), 16)
    cv.rect((0, 1100, W, 1180), (90, 80, 110), INK, 3)
    cv.rect((0, 1180, W, H), (36, 32, 46))
    for k in range(7):
        lx = ((k * 200 - scroll * 3000) % (W + 200)) - 100
        cv.rect((lx, 1480, lx + 110, 1500), (240, 240, 210))


def sports_car(cv, x, y, w=620, speed=0.0, driver=True):
    """Low wedge supercar (own design): long flat hood, short cabin far back, rear spoiler."""
    h = w * 0.2
    body = [(x, y - h * 0.15), (x + w * 0.02, y - h * 0.55), (x + w * 0.3, y - h * 0.75), (x + w * 0.46, y - h * 1.05),
            (x + w * 0.66, y - h * 1.05), (x + w * 0.86, y - h * 0.6), (x + w, y - h * 0.4), (x + w, y)]
    cv.poly(body + [(x, y)], CAR, INK, 6)
    win = [(x + w * 0.47, y - h * 0.98), (x + w * 0.64, y - h * 0.98), (x + w * 0.78, y - h * 0.62), (x + w * 0.38, y - h * 0.62)]
    cv.poly(win, (60, 80, 120), INK, 4)
    if driver:
        T.character(cv, x + w * 0.58, y - h * 0.62 + 753 * 0.11 - 30, 0.11, "neutral", "down", **T.HERO)
        cv.poly(win, (120, 160, 220, 90), INK, 4)
    cv.rect((x - 10, y - h * 0.9, x + w * 0.12, y - h * 0.78), (30, 30, 34), INK, 4)   # rear spoiler
    cv.line([(x + w * 0.05, y - h * 0.78), (x + w * 0.05, y - h * 0.5)], INK, 6)
    cv.line([(x + w * 0.1, y - h * 0.35), (x + w * 0.9, y - h * 0.35)], (200, 150, 20), 5)  # side line
    for wx in (x + w * 0.2, x + w * 0.8):
        cv.circle(wx, y, h * 0.42, (16, 16, 20), INK, 5)
        cv.circle(wx, y, h * 0.2, (180, 180, 190))
        if speed > 0:
            a = speed * 40
            cv.line([(wx, y), (wx + math.cos(a) * h * 0.18, y + math.sin(a) * h * 0.18)], INK, 4)
    cv.rect((x + w - 24, y - h * 0.38, x + w + 4, y - h * 0.22), (255, 250, 210))
    for k in range(int(speed * 6)):  # speed lines
        yy = y - h * (0.2 + 0.18 * k)
        cv.line([(x - 60 - k * 40, yy), (x - 260 - k * 60, yy)], (255, 255, 255, 140), 6)


def police_car(cv, x, y, s, ta, k=0):
    L = 400 * s
    cv.rect((x, y - 130 * s, x + L, y - 30 * s), (240, 242, 244), INK, 5, r=int(24 * s))
    cv.rect((x + L * 0.25, y - 200 * s, x + L * 0.75, y - 128 * s), (240, 242, 244), INK, 4, r=int(14 * s))
    cv.rect((x, y - 100 * s, x + L, y - 74 * s), (40, 80, 160))
    on = int(ta * 6 + k) % 2 == 0
    cv.rect((x + L * 0.38, y - 222 * s, x + L * 0.5, y - 200 * s), BLUE if on else (30, 40, 90))
    cv.rect((x + L * 0.5, y - 222 * s, x + L * 0.62, y - 200 * s), RED if not on else (90, 20, 20))
    cv.glow(x + L * 0.5, y - 210 * s, 90 * s, BLUE if on else RED, 140)
    for wx in (x + L * 0.2, x + L * 0.8):
        cv.circle(wx, y - 20 * s, 36 * s, (20, 20, 22), INK, 4)


def phone(cv, title=None, dark=False):
    cv.rect((PX0 - 18, PY0 - 18, PX1 + 18, PY1 + 18), (24, 24, 30), INK, 6, r=46)
    cv.rect((PX0, PY0, PX1, PY1), (20, 22, 30) if dark else (245, 247, 250))
    if title:
        cv.rect((PX0, PY0, PX1, PY0 + 90), (40, 42, 52) if dark else (230, 233, 240))
        cv.text((UX, PY0 + 60), title, font(38, "Black"), WHITE if dark else INK, "ms")


def cockpit_you(cv, ta, mood, lean=0.0, wheel=0.0):
    """You behind the wheel, seen through the windscreen (front view)."""
    neon_city(cv, ta, scroll=ta * 0.3)
    cv.rect((60, 620, 940, 1500), (30, 26, 40), INK, 8, r=60)            # car interior frame
    cv.rect((90, 650, 910, 1100), (70, 90, 130, 120), None, 0, r=40)      # windscreen tint
    hero(cv, UX + lean * 60, 900 + 753 * 0.95, 0.95, mood, "down", blink=blink_at(ta))
    a = math.radians(wheel)
    cx, cy, r = UX, 1250, 210
    cv.circle(cx, cy, r, None, (20, 20, 24), 34)
    cv.line([(cx - math.cos(a) * r, cy - math.sin(a) * r), (cx + math.cos(a) * r, cy + math.sin(a) * r)], (20, 20, 24), 26)
    cv.circle(cx, cy, 50, CAR, INK, 5)
    for side in (-1, 1):
        cv.circle(cx + side * math.cos(a) * r, cy + side * math.sin(a) * r, 46, SKIN, INK, 5)
    cv.rect((0, 1480, W, H), (24, 22, 30), INK, 6)


# ------------------------------------------------------------------ scenes (cv, t, dur, ta)

def s_open(cv, t, dur, ta):
    neon_city(cv, ta, scroll=ta * 0.1)
    sports_car(cv, 220, 1430, 640)
    if ta >= cue("Auf dem Rücksitz"):
        cv.rect((300, 520, 700, 640), (20, 20, 26, 230), CYAN_N, 4, r=20)
        cv.text((UX, 600), "3 × PROJEKT 6", font(48, "Black"), CYAN_N, "ms")


def drives(cv, ta, glow=True):
    cv.rect((0, 0, W, H), (30, 26, 40))
    cv.rect((60, 1050, 1020, 1500), (60, 50, 70), INK, 6, r=40)          # leather back seat
    for k in range(3):
        x = 170 + k * 250
        cv.rect((x, 760, x + 200, 1060), (40, 42, 50), INK, 6, r=16)
        cv.rect((x + 20, 790, x + 180, 900), (20, 22, 28), INK, 3, r=8)
        cv.text((x + 100, 860), "P6", font(60, "Black"), CYAN_N, "ms")
        cv.circle(x + 100, 1010, 12, GREEN)
        if glow:
            cv.glow(x + 100, 900, 160, CYAN_N, 60)


def s_drives(cv, t, dur, ta):
    drives(cv, ta)
    cv.rect((200, 520, 800, 640), (20, 20, 26, 230), YELLOW, 4, r=20)
    cv.text((UX, 600), "UNVERÖFFENTLICHT", font(48, "Black"), YELLOW, "ms")


def s_deal(cv, t, dur, ta):
    neon_city(cv, ta, scroll=0.0)
    cv.overlay((10, 6, 20), 120)
    phone(cv, "Auftraggeber", dark=True)
    k = ease(seg(ta, cue("Dein Auftraggeber"), cue("Deine Freundin")))
    cv.text((UX, PY0 + 220), f"{int(10000000 * k):,} $".replace(",", "."), font(72, "Black"), (80, 230, 120), "ms")
    if ta >= cue("Deine Freundin"):
        cv.rect((PX0 + 40, PY0 + 290, PX1 - 40, PY0 + 520), (40, 42, 52), None, 0, r=24)
        T.character(cv, PX0 + 140, PY0 + 500, 0.22, "happy", "down", **GIRL)
        cv.text((PX0 + 230, PY0 + 380), "Flughafen", font(40, "Black"), WHITE)
        cv.text((PX0 + 230, PY0 + 440), "wartet auf dich ♥".replace(" ♥", ""), font(32, "Bold"), (200, 200, 210))
    if ta >= cue("Ein Privatjet"):
        cv.rect((PX0 + 40, PY0 + 550, PX1 - 40, PY0 + 640), (30, 60, 40), None, 0, r=20)
        cv.text((UX, PY0 + 610), "PRIVATJET BEREIT", font(38, "Black"), (80, 230, 120), "ms")


def s_warning(cv, t, dur, ta):
    cockpit_you(cv, ta, "worry" if ta < cue("Vertrau") else "shock")
    sh = 6 * math.sin(ta * 60) if ta < cue("Unbekannte") else 0
    cv.rect((180 + sh, 480, 820 + sh, 760), (245, 247, 250), INK, 6, r=30)
    cv.text((UX + sh, 540), "Unbekannte Nummer", font(32, "Bold"), (120, 120, 130), "ms")
    if ta >= cue("Vertrau"):
        cv.text((UX, 625), "Vertrau niemandem.", font(46, "Black"), INK, "ms")
    if ta >= cue("Auch nicht"):
        cv.text((UX, 700), "Auch nicht deiner Freundin.", font(38, "Black"), RED, "ms")


def s_mirror(cv, t, dur, ta):
    cockpit_you(cv, ta, "shock")
    cv.rect((290, 470, 710, 640), (20, 20, 26), INK, 8, r=40)            # rear-view mirror
    n = 0 if ta < cue("Erst eins") else (1 if ta < cue("Dann drei") else (3 if ta < cue("Dann zehn") else 10))
    for k in range(n):
        x = 320 + (k * 37) % 360
        y = 520 + (k % 3) * 34
        on = int(ta * 6 + k) % 2 == 0
        cv.circle(x, y, 12, BLUE if on else RED)
        cv.glow(x, y, 40, BLUE if on else RED, 120)
    cv.rect((290, 470, 710, 640), None, INK, 8, r=40)


def s_speed(cv, t, dur, ta):
    v = 0 if ta < cue("Zweihundert.") else (200 if ta < cue("Zweihundertvierzig") else 240)
    neon_city(cv, ta, scroll=ta * (0.2 + v / 300))
    sports_car(cv, 260, 1430, 600, speed=min(1.0, v / 240 + 0.2))
    for k in range(min(3, 1 + int((ta - BOUNDS[5][0]) * 0.8))):
        police_car(cv, -80 - k * 260 + 120 * t, 1460 + k * 30, 0.6, ta, k)
    cv.circle(UX, 600, 110, (20, 20, 26), INK, 6)                         # speedometer
    a = math.radians(140 + 260 * v / 300)
    cv.line([(UX, 600), (UX + math.cos(a) * 90, 600 + math.sin(a) * 90)], RED, 8)
    cv.text((UX, 690), f"{v} km/h", font(36, "Black"), WHITE, "ms")


def s_pause(cv, t, dur, ta):
    cockpit_you(cv, ta, "shock", wheel=0)


def s_heli(cv, t, dur, ta):
    neon_city(cv, ta, scroll=ta * 0.6)
    hx = 520 + 40 * math.sin(ta)
    cone = Image.new("RGBA", cv.img.size, (0, 0, 0, 0))
    ImageDraw.Draw(cone).polygon([(u * T.S.SS, v * T.S.SS) for u, v in ((hx - 20, 560), (hx + 20, 560), (680, 1460), (220, 1460))],
                                 fill=(255, 250, 210, 80 if ta >= cue("Der Suchscheinwerfer") else 0))
    cv.img.paste(cone, (0, 0), cone)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")
    cv.rect((hx - 120, 470, hx + 80, 560), (30, 30, 36), INK, 5, r=40)   # helicopter
    cv.rect((hx + 60, 500, hx + 220, 524), (30, 30, 36), INK, 4)
    span = 220 * abs(math.cos(ta * 30))
    cv.line([(hx - 20 - span, 460), (hx - 20 + span, 460)], (30, 30, 36), 8)
    sports_car(cv, 180, 1440, 560, speed=0.8)
    if ta >= cue("Straßensperre"):
        for k in range(3):
            cv.rect((760 + k * 0, 1220 + k * 70, 1060, 1260 + k * 70), (240, 240, 240), INK, 4)
            for j in range(4):
                cv.rect((780 + j * 70, 1220 + k * 70, 810 + j * 70, 1260 + k * 70), RED)


def runway(cv, ta, jet_x=None):
    for y in range(0, 1100, 6):
        k = y / 1100
        cv.rect((0, y, W, y + 6), (int(20 + 30 * k), int(14 + 20 * k), int(50 + 40 * k)))
    cv.rect((0, 1100, W, H), (40, 40, 48))
    cv.poly([(380, 1100), (620, 1100), (1080, H), (-80, H)], (60, 60, 68))
    for k in range(8):
        f = (k / 8 + ta * 0.4) % 1.0
        yy = 1100 + f ** 2 * (H - 1100)
        cv.rect((UX - 6 - 30 * f, yy, UX + 6 + 30 * f, yy + 10 + 60 * f), (240, 240, 210))
        for side in (-1, 1):
            cv.circle(UX + side * (120 + 500 * f), yy, 4 + 8 * f, (255, 220, 120))


def jet(cv, x, y, s=1.0):
    cv.rect((x - 330 * s, y - 90 * s, x + 330 * s, y + 20 * s), WHITE, INK, 6, r=int(55 * s))
    cv.poly([(x + 260 * s, y - 80 * s), (x + 360 * s, y - 230 * s), (x + 400 * s, y - 230 * s), (x + 330 * s, y - 60 * s)], WHITE, INK, 5)
    cv.poly([(x - 60 * s, y), (x + 120 * s, y), (x + 220 * s, y + 90 * s), (x + 40 * s, y + 90 * s)], (220, 222, 228), INK, 5)
    for k in range(6):
        cv.circle(x - 200 * s + k * 70 * s, y - 50 * s, 16 * s, (90, 130, 190), INK, 3)
    cv.rect((x - 300 * s, y - 70 * s, x - 230 * s, y + 10 * s), (240, 220, 140), INK, 4, r=8)   # open door
    cv.poly([(x - 300 * s, y + 10 * s), (x - 230 * s, y + 10 * s), (x - 210 * s, y + 140 * s), (x - 320 * s, y + 140 * s)],
            (200, 200, 206), INK, 4)                                                           # stairs


def s_fence(cv, t, dur, ta):
    if ta < cue("Quer über"):
        neon_city(cv, ta, scroll=ta * 0.6)
        cv.rect((620, 1060, 1080, 1460), None, (200, 200, 210), 0)
        for k in range(10):  # construction fence
            cv.line([(620 + k * 46, 1060), (620 + k * 46, 1460)], (200, 200, 210), 6)
        cv.rect((620, 1060, 1080, 1100), (255, 160, 40), INK, 4)
        x = 40 + 560 * ease(seg(ta, cue("Du reißt"), cue("Quer über")))
        sports_car(cv, x, 1440, 560, speed=0.9)
        if ta >= cue("Durch einen"):
            cv.text((760, 950), "KRACH!", font(100, "Black"), YELLOW, "ms")
        return
    runway(cv, ta)
    sports_car(cv, 220, 1640, 600, speed=1.0)


def s_jet(cv, t, dur, ta):
    runway(cv, ta)
    jet(cv, 560, 1150, 1.0)
    for side in (-1, 1):  # engines running
        cv.glow(560 + side * 40, 1200, 80, (255, 150, 60), 120)
    T.character(cv, 300, 1300, 0.42, "happy", "up" if ta >= cue("Deine Freundin") else "down",
                talk=talking(ta, "Steig ein"), **GIRL)
    if ta >= cue("Steig ein"):
        cv.rect((80, 470, 460, 600), WHITE, INK, 5, r=30)
        cv.poly([(250, 600), (290, 600), (280, 660)], WHITE, INK, 5)
        cv.text((270, 556), "Steig ein!", font(56, "Black"), INK, "ms")


def s_last(cv, t, dur, ta):
    runway(cv, ta)
    jet(cv, 620, 1100, 0.7)
    T.character(cv, 440, 1180, 0.3, "happy", "up", **GIRL)
    sports_car(cv, 140, 1600, 600, speed=1.0)
    for k in range(3):
        police_car(cv, -120 - k * 180 + 60 * t, 1760 + k * 30, 0.55, ta, k)


def s_final(cv, t, dur, ta):
    cockpit_you(cv, ta, "angry", wheel=8 * math.sin(ta * 3))


def buttons(img):
    d = ImageDraw.Draw(img, "RGBA")
    f = T.font(44, "Black")
    for (x0, x1), lab, bg, fg in (((50, 470), "EINSTEIGEN", (40, 140, 70), YELLOW), ((510, 930), "WEITERFAHREN", RED, WHITE)):
        d.rounded_rectangle((x0, 1330, x1, 1440), 28, fill=bg, outline=INK, width=6)
        d.text(((x0 + x1) / 2, 1405), lab, font=f, fill=fg, anchor="ms")


SCENES = [s_open, s_drives, s_deal, s_warning, s_mirror, s_speed, s_pause, s_heli, s_fence, s_jet, s_last, s_final]
PAUSE = 6
UI_SCENES = (2, 3, 4, 6, 11)
INNER_CUTS = [cue("Quer über")]


def render(i, t=0.5, dur=5.0, ta=None):
    ta = BOUNDS[i][0] + t * (BOUNDS[i][1] - BOUNDS[i][0]) if ta is None else ta
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur, ta)
    img = cv.final()
    if i in UI_SCENES:
        img = T.camera(img, 0.0, 500, 810)
    else:
        img = T.camera(img, 0.02 + 0.07 * ease(t), 540, 960)
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
    if i == 4:
        n = 0 if ta < cue("Erst eins") else (1 if ta < cue("Dann drei") else (3 if ta < cue("Dann zehn") else 10))
        return (f"POLIZEI: {n}", "red")
    if i == 5:
        v = 0 if ta < cue("Zweihundert.") else (200 if ta < cue("Zweihundertvierzig") else 240)
        return (f"{v} KM/H", "red" if v else "white")
    if i == 10:
        return ("NOCH 50 METER", "red")
    return [("02:43 · VICE CITY", "white"), ("TEUERSTES SPIEL DER WELT", "yellow"), ("+ 10.000.000 $", "green"),
            ("UNBEKANNTE NUMMER", "red"), None, None, ("", "white"), ("HUBSCHRAUBER", "red"),
            ("LANDEBAHN", "white"), ("PRIVATJET", "green"), None, ("EINSTEIGEN?", "yellow")][i]
