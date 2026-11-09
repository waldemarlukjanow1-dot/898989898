"""Scenes for 'FLUG 404 – Teil 3: Ins Cockpit' (STIL 3, T.HERO). Scenes get (t, dur, ta), cued to the voice."""
import math
import random

from PIL import Image, ImageDraw, ImageFilter

import cabin as C
from cabin import T, Canvas, font, mono, W, H, ease, seg, INK, WHITE, SKIN, YELLOW, UX, RED, SEAT, SEAT_D
from cabin import cabin_back, cabin_rows, pair_seats, hero, blink_at, tilt
from timing import PHRASES, TEMPO, seq_bounds

BOUNDS, TOTAL = seq_bounds()
GREEN_UI = (60, 220, 120)


def cue(text):
    return next(a / TEMPO for a, b, s, t in PHRASES if t.startswith(text))


def cue_end(text):
    return next(b / TEMPO for a, b, s, t in PHRASES if t.startswith(text))


# ------------------------------------------------------------------ cockpit pieces

def windshield(cv, ta, pitch=0.0, runway=0.0, ground=1.0, night=True):
    """View through the cockpit windows. pitch>0: nose down (ground fills the view).
    runway 0..1: runway lights approach."""
    x0, y0, x1, y1 = 60, 470, 940, 900
    sub = Canvas((0, 0, 0))
    horizon = 700 - 700 * pitch
    sky_top, sky_bot = ((10, 14, 40), (40, 50, 90)) if night else ((120, 170, 230), (190, 220, 245))
    for y in range(0, H, 8):
        k = y / H
        sub.rect((0, y, W, y + 8), tuple(int(sky_top[i] + (sky_bot[i] - sky_top[i]) * k) for i in range(3)))
    sub.rect((0, horizon, W, H), (24, 30, 26) if night else (90, 120, 70))
    rnd = random.Random(4)
    if ground:
        for k in range(9):  # glowing road grid of a city below
            f = (k + 1) / 9
            yy = horizon + f ** 1.6 * (H - horizon)
            sub.line([(0, yy), (W, yy)], (255, 190, 90, 160), 2 + 6 * f)
        for k in range(-6, 7):
            sub.line([(UX + k * 40, horizon), (UX + k * 400, H)], (255, 190, 90, 120), 4)
    for _ in range(160 if ground else 0):  # city lights below
        gx = rnd.uniform(0, W)
        gy = horizon + rnd.uniform(0.02, 1) ** 1.5 * (H - horizon)
        sz = 3 + 10 * (gy - horizon) / (H - horizon + 1)
        sub.circle(gx, gy, sz, (255, 220, 130))
    if runway > 0:  # two converging rows of runway lights
        for k in range(14):
            f = ((k / 14) + runway * 0.6) % 1.0
            yy = horizon + 10 + f ** 2 * (H - horizon)
            spread = 30 + f ** 2 * 700
            r_ = 3 + 10 * f ** 2
            for side in (-1, 1):
                sub.circle(UX + side * spread, yy, r_, (255, 250, 220))
                sub.glow(UX + side * spread, yy, r_ * 4, (255, 240, 180), 60)
    img = sub.final().crop((x0, y0, x1, y1))
    cv.img.paste(img.resize(((x1 - x0) * T.S.SS, (y1 - y0) * T.S.SS)), (x0 * T.S.SS, y0 * T.S.SS))
    cv.d = ImageDraw.Draw(cv.img, "RGBA")
    cv.poly([(x0, y0), (x1, y0), (x1, y0 + 40), (x0, y0 + 40)], (40, 44, 56))
    cv.line([(UX, y0), (UX, y1)], (40, 44, 56), 16)
    cv.rect((x0, y0, x1, y1), None, INK, 8, r=20)


def dashboard(cv, ta, alarm=False, alt=None, autopilot=None, pull_up=False):
    cv.rect((0, 900, W, 1180), (54, 58, 70), INK, 6)
    rnd = random.Random(int(ta * 3))
    for k in range(10):
        x = 50 + (k % 5) * 180
        y = 930 + (k // 5) * 110
        cv.rect((x, y, x + 150, y + 80), (16, 20, 24), INK, 3, r=10)
        on = rnd.random() < 0.6
        cv.circle(x + 30, y + 40, 12, (RED if alarm else GREEN_UI) if on else (60, 60, 60))
    if alt is not None:  # altimeter
        cv.rect((330, 940, 670, 1070), (8, 12, 10), (60, 220, 120), 5, r=12)
        cv.text((UX, 985), "HÖHE", font(26, "Black"), (60, 220, 120), "ms")
        cv.text((UX, 1052), f"{int(alt):,} m".replace(",", "."), mono(56), (255, 80, 80) if alt < 800 else GREEN_UI, "ms")
    if autopilot is not None:
        cv.rect((330, 1090, 670, 1160), (10, 20, 10), RED if not autopilot else GREEN_UI, 4, r=10)
        cv.text((UX, 1140), "AUTOPILOT: " + ("AN" if autopilot else "AUS"), font(32, "Black"),
                RED if not autopilot else GREEN_UI, "ms")
    if pull_up:
        on = int(ta * 3) % 2 == 0
        cv.rect((300, 560, 700, 680), (RED if on else (120, 20, 20)), INK, 6, r=20)
        cv.text((UX, 645), "PULL UP!", font(70, "Black"), WHITE, "ms")
    if alarm:
        cv.overlay((200, 0, 0), int(35 + 25 * math.sin(ta * 6)))


def seats_from_behind(cv, you=True):
    for x in (250, 750):
        cv.rect((x - 170, 1180, x + 170, 1700), (70, 60, 50), INK, 6, r=70)
        cv.rect((x - 110, 1200, x + 110, 1300), (90, 80, 70), INK, 4, r=30)
    if you:  # back of your head (dark boxer cut) above the captain's seat
        hair = T.HERO["hair"]
        for side in (-1, 1):
            cv.circle(250 + side * 112, 1150, 26, SKIN, INK, 4)
        cv.circle(250, 1130, 110, (110, 100, 96), INK, 5)
        cv.d.chord(cv.s((140, 1020, 360, 1200)), 180, 360, fill=hair)
        cv.rect((150, 1240, 350, 1300), T.HERO["hoodie"], INK, 4, r=30)


def yoke(cv, x, y, s=1.0, angle=0.0):
    a = math.radians(angle)
    cv.rect((x - 18 * s, y, x + 18 * s, y + 260 * s), (40, 40, 46), INK, 4)
    pts = [(-170, -40), (-150, 40), (-60, 40), (-40, 0), (40, 0), (60, 40), (150, 40), (170, -40), (120, -40), (100, 10),
           (-100, 10), (-120, -40)]
    rp = [(x + (px * math.cos(a) - py * math.sin(a)) * s, y + (px * math.sin(a) + py * math.cos(a)) * s) for px, py in pts]
    cv.poly(rp, (60, 60, 68), INK, 5)
    for side in (-1, 1):  # your hands on the grips
        hx = x + (side * 145 * math.cos(a)) * s
        hy = y + (side * 145 * math.sin(a)) * s
        cv.circle(hx, hy - 10 * s, 42 * s, SKIN, INK, 5)


def pilot_seat_you(cv, ta, mood, pull=0.0):
    """You in the captain's seat, front view, hands on the yoke."""
    cv.rect((0, 0, W, H), (40, 44, 56))
    cv.rect((220, 700, 860, 1600), (70, 60, 50), INK, 6, r=80)
    cv.rect((300, 720, 780, 860), (90, 80, 70), INK, 4, r=40)
    hero(cv, 540, 860 + 753 * 1.05 - 60 * pull, 1.05, mood, "down", blink=blink_at(ta))
    yoke(cv, 540, 1250 - 80 * pull, 1.4, angle=6 * math.sin(ta * 4) * (1 - pull))
    cv.rect((0, 1500, W, H), (54, 58, 70), INK, 6)


# ------------------------------------------------------------------ scenes (cv, t, dur, ta)

def s_hook(cv, t, dur, ta):
    cv.rect((0, 0, W, H), (40, 44, 56))
    windshield(cv, ta, pitch=0.55 + 0.25 * t)
    alt = 2400 - 1600 * ease(t)
    dashboard(cv, ta, alarm=True, alt=alt)
    seats_from_behind(cv, you=False)
    if ta >= cue("Und du bist"):  # cut: you, the only one standing, in the falling cabin
        cabin_back(cv, ta, night=True)
        cabin_rows(cv, lambda r, k: "stare", ta, night=True, skip_front=True)
        cv.overlay((200, 0, 0), 40)
        hero(cv, UX, 1880, 0.85, "shock", "down", blink=blink_at(ta))


def s_run(cv, t, dur, ta):
    cabin_back(cv, ta, night=True)
    turned = ta >= cue("Die Passagiere") + 0.3
    u = seg(ta, cue("Du rennst"), cue_end("Die Passagiere") + 0.4)

    def look(r, k):
        if not turned:
            return (0, 0)
        return (1, 0) if k < 3 else (-1, 0)
    cabin_rows(cv, lambda r, k: "stare", ta, night=True, skip_front=True, look_fn=look)
    s = 0.4 + 0.5 * u
    hero(cv, UX, 1080 + 820 * u, s, "shock", "down", bob=-22 * s * abs(math.sin(ta * 9)))
    cv.overlay((180, 0, 0), 25)


def s_cockpit(cv, t, dur, ta):
    cv.rect((0, 0, W, H), (40, 44, 56))
    windshield(cv, ta, pitch=0.85)
    dashboard(cv, ta, alarm=ta >= cue("Rote Lampen"), alt=900 - 300 * t, pull_up=ta >= cue("Ein Alarm"))
    seats_from_behind(cv, you=False)
    if cue("Die Cockpittür") <= ta < cue("Die Cockpittür") + 0.8:
        cv.text((UX, 820), "BAMM!", font(110, "Black"), YELLOW, "ms")


def s_yoke(cv, t, dur, ta):
    pull = ease(seg(ta, cue("Und ziehst"), cue_end("Und ziehst")))
    mood = "worry" if ta < cue("Aber du packst") else ("angry" if ta >= cue("Und ziehst") else "shock")
    pilot_seat_you(cv, ta, mood, pull)


def s_level(cv, t, dur, ta):
    cv.rect((0, 0, W, H), (40, 44, 56))
    k = ease(seg(ta, cue("Die Nase"), cue("Der Höhenmesser")))
    windshield(cv, ta, pitch=0.85 * (1 - k))
    stop = ta >= cue("Der Höhenmesser") + 0.8
    alt = 300 if stop else 620 - 320 * seg(ta, cue("Die Nase"), cue("Der Höhenmesser") + 0.8)
    dashboard(cv, ta, alarm=not stop, alt=alt)
    seats_from_behind(cv)


def s_pause(cv, t, dur, ta):
    cv.rect((0, 0, W, H), (40, 44, 56))
    windshield(cv, ta, pitch=0.0)
    dashboard(cv, ta, alt=300, autopilot=False)
    seats_from_behind(cv)


def s_runway(cv, t, dur, ta):
    cv.rect((0, 0, W, H), (40, 44, 56))
    windshield(cv, ta, pitch=0.12, runway=0.2 + 0.8 * t, ground=0)
    dashboard(cv, ta, alt=300 - 200 * t)
    if ta >= cue("Mitten im Nirgendwo"):
        cv.rect((330, 920 - 380, 670, 1000 - 380), (255, 255, 255, 220), INK, 4, r=14)
        cv.text((UX, 595), "KEIN FLUGHAFEN", font(34, "Black"), INK, "ms")
    seats_from_behind(cv)


def s_land(cv, t, dur, ta):
    cv.rect((0, 0, W, H), (40, 44, 56))
    windshield(cv, ta, pitch=0.18, runway=1.0 + t * 3, ground=0)
    dashboard(cv, ta, alt=0)
    if cue("Die Reifen") <= ta < cue("Alles fühlt"):
        cv.text((UX, 820), "KREISCH!", font(96, "Black"), YELLOW, "ms")
    seats_from_behind(cv)


def s_empty(cv, t, dur, ta):
    cabin_back(cv, ta, night=True)
    cabin_rows(cv, lambda r, k: "stare", ta, night=True, all_empty=ta >= cue("Die Kabine"), skip_front=True)
    hero(cv, UX, 1880, 0.82, "shock", "down", blink=blink_at(ta))


def s_32b(cv, t, dur, ta):
    clap = ta >= cue("Und er klatscht")
    shown = ta >= cue("Du.")

    def label():
        cv.rect((640, 520, 800, 590), WHITE, INK, 4, r=12)
        cv.text((720, 572), "32B", font(44, "Black"), INK, "ms")
    pair_seats(cv, ta, "shock", twin=shown, twin_mood="happy" if clap else "smug", extra=label)
    if clap:  # clapping hands in front of the twin's chest
        g = abs(math.sin(ta * 9))
        for side in (-1, 1):
            cv.circle(720 + side * (20 + 50 * g), 1010, 40, SKIN, INK, 5)
        if g > 0.8:
            cv.text((720, 940), "klatsch", font(36, "Black"), YELLOW, "ms")


def s_final(cv, t, dur, ta):
    pair_seats(cv, ta, "shock", twin=True, twin_mood="smug")


def buttons(img):
    d = ImageDraw.Draw(img, "RGBA")
    f = T.font(44, "Black")
    for (x0, x1), lab, bg, fg in (((40, 470), "GERETTET", (40, 140, 70), YELLOW), ((500, 930), "REINGELEGT", RED, WHITE)):
        d.rounded_rectangle((x0, 1330, x1, 1440), 28, fill=bg, outline=INK, width=6)
        d.text(((x0 + x1) / 2, 1405), lab, font=f, fill=fg, anchor="ms")


SCENES = [s_hook, s_run, s_cockpit, s_yoke, s_level, s_pause, s_runway, s_land, s_empty, s_32b, s_final]
PAUSE = 5
INNER_CUTS = [cue("Und du bist")]


def render(i, t=0.5, dur=5.0, ta=None):
    ta = BOUNDS[i][0] + t * (BOUNDS[i][1] - BOUNDS[i][0]) if ta is None else ta
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur, ta)
    img = cv.final()
    if i in (2, 4, 5, 6, 7):
        img = T.camera(img, 0.0, 500, 810)
    else:
        img = T.camera(img, 0.02 + 0.07 * ease(t), 540, 860)
    if i == 0 and ta >= cue("Und du bist"):
        img = tilt(img, -9, 0.12)
    if i == 3:  # nose comes up: the picture rotates back while you pull
        deg = 10 * (1 - ease(seg(ta, cue("Und ziehst"), cue_end("Und ziehst") + 0.5)))
        img = tilt(img, deg, 0.1)
    if i == 7 and cue("Du landest") <= ta < cue("Du landest") + 0.5:  # touchdown jolt
        img = tilt(img, 2.5 * math.sin((ta - cue("Du landest")) * 40), 0.05)
    if i == 7 and ta >= cue("Alles fühlt"):  # dreamy: soft glow + blur
        k = seg(ta, cue("Alles fühlt"), cue_end("Alles fühlt"))
        glow = img.filter(ImageFilter.GaussianBlur(14))
        img = Image.blend(img, Image.blend(glow, Image.new("RGB", img.size, (255, 250, 235)), 0.25), 0.7 * k)
    if i == 10:
        buttons(img)
    if i == PAUSE:
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, ta):
    if i == 0:
        left = max(0, 90 - int((ta - BOUNDS[0][0]) * 1.0))
        return (f"NOCH {left} SEKUNDEN", "red")
    return [None, ("ALLE SCHAUEN DICH AN", "red"), ("PULL UP!", "red"), ("DU FLIEGST", "white"),
            ("HÖHE: 300 m", "green"), ("AUTOPILOT: AUS", "red"), ("LANDEBAHN?", "white"),
            ("GELANDET", "green"), ("PASSAGIERE: 0", "red"), ("PLATZ 32B", "red"), ("FLUG 404", "white")][i]
