"""Scenes for 'FLUG 404' (STIL 3, T.HERO). Scenes get (t, dur, ta) – ta = absolute video time,
so every action is cued to the spoken phrase via CUE[...]."""
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
CABIN, CABIN_D = (222, 226, 232), (180, 186, 196)
SEAT, SEAT_D = (52, 72, 120), (38, 54, 92)
BOUNDS, TOTAL = seq_bounds()


def cue(text):
    return next(a / TEMPO for a, b, s, t in PHRASES if t.startswith(text))


PASSENGERS = [dict(hoodie=c, hair=h, outfit="hoodie", hair_style="fringe") for c, h in
              (((180, 70, 70), (90, 60, 40)), ((70, 120, 180), (40, 30, 26)), ((200, 160, 60), (120, 80, 50)),
               ((120, 80, 150), (60, 40, 30)), ((90, 150, 120), (150, 150, 150)), ((200, 110, 60), (30, 30, 30)),
               ((100, 100, 110), (170, 120, 70)))]
STEWARDESS = dict(hoodie=(30, 50, 110), hair=(160, 90, 40), outfit="hoodie", hair_style="fringe", tie=True)


def hero(cv, x, y, s, mood, arms="down", **kw):
    return T.character(cv, x, y, s, mood, arms, **dict(T.HERO, **kw))


def blink_at(ta):
    return (ta % 2.7) < 0.1


def seated(cv, x, head_y, s, mood, look=(0, 0), blink=False, hero_look=False, kw=None, talk=0.0):
    """Character whose head is at head_y; the seat back drawn by the caller hides the legs."""
    y_feet = head_y + 753 * s
    if hero_look:
        hero(cv, x, y_feet, s, mood, "down", look=look, blink=blink, talk=talk)
    else:
        T.character(cv, x, y_feet, s, mood, "down", look=look, blink=blink, talk=talk, **(kw or {}))


def seat_back(cv, x, top, w, h, col=SEAT):
    """Back of a seat seen from behind (= the row in front of a person, closer to the camera)."""
    cv.rect((x - w / 2, top, x + w / 2, top + h), col, INK, 5, r=int(w * 0.18))
    cv.rect((x - w * 0.3, top + h * 0.2, x + w * 0.3, top + h * 0.5), tuple(int(c * 0.85) for c in col), INK, 3, r=10)


def seat_front(cv, x, head_y, s):
    """Seat a person sits in, seen from the front: tall back with white headrest cover."""
    w = 380 * s
    cv.rect((x - w / 2, head_y - 230 * s, x + w / 2, head_y + 600 * s), SEAT, INK, 5, r=int(w * 0.2))
    cv.rect((x - w * 0.36, head_y - 215 * s, x + w * 0.36, head_y - 90 * s), WHITE, None, 0, r=int(w * 0.1))


def window(cv, x, y, w, h, t, night=False):
    cv.rect((x - 10, y - 10, x + w + 10, y + h + 10), CABIN_D, INK, 5, r=int(w * 0.45))
    cv.rect((x, y, x + w, y + h), (20, 30, 70) if night else (120, 180, 240), INK, 4, r=int(w * 0.42))
    rnd = random.Random(int(x))
    for k in range(3):
        cx = x + ((rnd.uniform(0, w) - t * 160 + k * w * 0.5) % (w + 120)) - 60
        cy = y + h * (0.3 + 0.2 * k)
        if x + 10 < cx < x + w - 10:
            cv.ellipse((cx - 40, cy - 14, cx + 40, cy + 14), (255, 255, 255, 200 if not night else 60))


def cabin_back(cv, t, night=False):
    """Cabin seen from the front, looking down the aisle to the rear galley (one-point perspective)."""
    cv.rect((0, 0, W, H), CABIN if not night else (150, 156, 176))
    vx, vy = UX, 640
    cv.poly([(0, 0), (W, 0), (vx + 160, vy - 120), (vx - 160, vy - 120)], (236, 238, 242) if not night else (160, 166, 186))
    cv.poly([(0, 0), (vx - 160, vy - 120), (vx - 160, vy + 220), (0, 980)], (200, 205, 215) if not night else (130, 136, 156))
    cv.poly([(W, 0), (vx + 160, vy - 120), (vx + 160, vy + 220), (W, 980)], (200, 205, 215) if not night else (130, 136, 156))
    for side in (-1, 1):  # overhead bins
        cv.poly([(UX + side * 560, 140), (vx + side * 175, vy - 100), (vx + side * 175, vy - 30), (UX + side * 560, 380)],
                (236, 238, 242) if not night else (170, 176, 196), INK, 4)
    cv.rect((vx - 150, vy - 120, vx + 150, vy + 220), (190, 196, 206), INK, 4)  # rear wall + galley curtain
    cv.rect((vx - 60, vy - 80, vx + 60, vy + 220), (150, 156, 168), INK, 4, r=8)
    cv.poly([(vx - 150, vy + 220), (vx + 150, vy + 220), (W, H), (0, H)], (70, 80, 110))  # carpet
    cv.poly([(vx - 40, vy + 220), (vx + 40, vy + 220), (UX + 220, H), (UX - 220, H)], (110, 70, 80))  # aisle runner
    for k in range(6):  # floor lights
        yy = vy + 240 + k * 160
        f = (yy - vy) / (H - vy)
        for side in (-1, 1):
            cv.circle(UX + side * (60 + 200 * f), yy, 4 + 6 * f, (255, 220, 120))


ROWS = [(0.25, 760), (0.42, 880), (0.62, 1040), (0.85, 1250)]  # (scale, seat top y) back -> front


def cabin_rows(cv, mood_fn, t, night=False, stewardess=False, zzz=False):
    """Passengers left and right of the aisle. mood_fn(row, k) -> mood."""
    for ri, (s, top) in enumerate(ROWS):
        off = 120 + 520 * (s - 0.2)
        for side in (-1, 1):
            for k in range(2):
                x = UX + side * (off + k * 230 * s * 1.6)
                head_y = top - 70 * s
                kw = PASSENGERS[(ri * 4 + k * 2 + (side > 0)) % len(PASSENGERS)]
                seat_front(cv, x, head_y, s * 0.55)
                seated(cv, x, head_y, s * 0.55, mood_fn(ri, k), kw=kw)
                seat_back(cv, x, top + 60 * s, 300 * s, 420 * s)
                if zzz and (ri + k) % 2 == 0:
                    ph = (t * 1.2 + ri * 0.3 + k * 0.5) % 1.0
                    cv.text((x + 60 * s, head_y - 120 * s - 60 * ph), "z", font(int(36 + 30 * s), "Black"),
                            (90, 110, 170, int(255 * (1 - ph))))
        if stewardess and ri == 2:
            sx = UX + 20
            T.character(cv, sx, top + 620 * s, s * 0.62, "sleep", "down", **STEWARDESS)
            cv.rect((sx + 80, top + 240 * s, sx + 260, top + 520 * s), (200, 204, 212), INK, 4, r=8)  # trolley


# ------------------------------------------------------------------ scenes (cv, t, dur, ta)

def you_seated(cv, x, head_y, s, mood, ta, look=(0, 0), arms="down", talk=0.0):
    seat_front(cv, x, head_y, s)
    hero(cv, x, head_y + 753 * s, s, mood, arms, look=look, blink=blink_at(ta), talk=talk)
    cv.rect((x - 330 * s, head_y + 380 * s, x + 330 * s, head_y + 1200 * s), SEAT_D, INK, 6, r=int(60 * s))  # row in front
    cv.rect((x - 220 * s, head_y + 420 * s, x + 220 * s, head_y + 520 * s), (30, 40, 70), INK, 3, r=12)  # tray table latch area


def seat_view(cv, t, ta, mood, look=(0, 0), night=False, arms="down"):
    """You in your window seat."""
    cv.rect((0, 0, W, H), CABIN if not night else (150, 156, 176))
    cv.rect((0, 0, W, 300), (236, 238, 242) if not night else (170, 176, 196), INK, 4)  # bin
    window(cv, 60, 520, 230, 340, ta, night)
    you_seated(cv, 620, 760, 1.15, mood, ta, look, arms)


def s_board(cv, t, dur, ta):
    seat_view(cv, t, ta, "happy", look=(-1, 0) if ta > cue("Fensterplatz") else (0, 0))


def s_silence(cv, t, dur, ta):
    cabin_back(cv, ta)
    cabin_rows(cv, lambda r, k: "sleep", ta)
    # you peek over the seat in the foreground, looking left/right
    look = (-1, 0) if (ta * 0.8) % 2 < 1 else (1, 0)
    you_seated(cv, 760, 1250, 0.75, "worry", ta, look)
    for k, (key, txt) in enumerate((("Kein Baby", "BABY: 0 dB"), ("Kein Husten", "HUSTEN: –"), ("Nichts.", "NICHTS"))):
        if ta >= cue(key):
            a = min(1, (ta - cue(key)) / 0.25)
            cv.rect((60, 470 + k * 90, 380, 540 + k * 90), (255, 255, 255, int(230 * a)), INK, 4, r=16)
            cv.text((220, 520 + k * 90), txt, font(34, "Black"), INK, "ms")


def s_asleep(cv, t, dur, ta):
    cabin_back(cv, ta)
    cabin_rows(cv, lambda r, k: "sleep", ta, stewardess=ta >= cue("Auch die Stewardess") - 0.1, zzz=True)
    if ta >= cue("Mitten im Gang"):
        k = min(1, (ta - cue("Mitten im Gang")) / 0.3)
        cv.circle(UX + 20, 900, 150, None, (255, 214, 10, int(255 * k)), 10)


def s_call(cv, t, dur, ta):
    if ta < cue("Niemand kommt"):
        cv.rect((0, 0, W, H), (200, 205, 215))
        cv.rect((140, 520, 860, 980), (236, 238, 242), INK, 6, r=30)  # overhead panel close-up
        for k, x in enumerate((260, 500)):
            cv.circle(x, 700, 70, (250, 230, 160) if k == 0 else (60, 60, 66), INK, 5)
        pressed = ta > cue("Du drückst") + 0.6
        cv.circle(740, 700, 80, (255, 140, 40) if pressed else (200, 200, 206), INK, 6)
        if pressed:
            cv.glow(740, 700, 160, (255, 140, 40), 160)
        T.character(cv, 740, 700 + 20 + 400 * 0.09, 0.09, "neutral", "down", **STEWARDESS)  # call icon figure
        cv.rect((180, 840, 820, 940), (60, 60, 66), r=12)
        cv.text((UX, 905), "RUFEN", font(46, "Black"), WHITE, "ms")
        # your finger
        fy = 860 - 60 * ease(seg(ta, cue("Du drückst"), cue("Du drückst") + 0.6))
        cv.rect((700, fy, 780, fy + 400), SKIN, INK, 5, r=40)
    else:
        cabin_back(cv, ta)
        cabin_rows(cv, lambda r, k: "sleep", ta, stewardess=True)
        you_seated(cv, 760, 1250, 0.75, "worry", ta, (-1, 0))


def screen_ui(cv, ta, x0=150, y0=480, x1=850, y1=1100):
    cv.rect((x0 - 20, y0 - 20, x1 + 20, y1 + 20), (24, 24, 30), INK, 6, r=24)
    cv.rect((x0, y0, x1, y1), (20, 40, 80))
    # world map blobs + route
    for (cx, cy, rx, ry) in ((x0 + 170, y0 + 300, 140, 120), (x0 + 520, y0 + 260, 120, 110), (x0 + 560, y0 + 420, 70, 60)):
        cv.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), (40, 90, 70))
    a, b = (x0 + 540, y0 + 250), (x0 + 170, y0 + 280)
    pts = [(a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u - 120 * math.sin(math.pi * u)) for u in [i / 20 for i in range(21)]]
    cv.line(pts, (255, 255, 255, 160), 4)
    u = 0.38
    px, py = pts[int(u * 20)]
    cv.circle(px, py, 16, WHITE, INK, 3)
    cv.text((a[0], a[1] + 50), "FRA", font(30, "Black"), WHITE, "ms")
    cv.text((b[0], b[1] + 50), "JFK", font(30, "Black"), WHITE, "ms")
    cv.rect((x0, y1 - 180, x1, y1), (10, 20, 50))
    cv.text((x0 + 30, y1 - 120), "ANKUNFT NEW YORK (JFK)", font(32, "Bold"), (180, 200, 230))
    if ta >= cue("vor drei Tagen"):
        k = min(1, (ta - cue("vor drei Tagen")) / 0.25)
        cv.text((x0 + 30, y1 - 45), "VOR 3 TAGEN", font(64, "Black"), (255, 80 + int(40 * (1 - k)), 80))
    else:
        cv.text((x0 + 30, y1 - 45), "--:--", font(64, "Black"), (180, 200, 230))


def s_screen(cv, t, dur, ta):
    cv.rect((0, 0, W, H), SEAT_D)
    screen_ui(cv, ta)
    mood = "shock" if ta >= cue("vor drei Tagen") else "worry"
    you_seated(cv, 780, 1320, 0.55, mood, ta)


def s_pause(cv, t, dur, ta):
    cv.rect((0, 0, W, H), SEAT_D)
    screen_ui(cv, cue("vor drei Tagen") + 1)
    you_seated(cv, 780, 1320, 0.55, "shock", ta, arms="head")


def s_cockpit(cv, t, dur, ta):
    if ta < cue("Die Tür ist offen"):  # walking down the aisle towards the cockpit door
        cabin_back(cv, ta)
        cabin_rows(cv, lambda r, k: "sleep", ta, stewardess=True)
        u = seg(ta, cue("Du gehst"), cue("Die Tür ist offen"))
        s = 0.55 + 0.3 * u
        hero(cv, UX, 1400 + 480 * u, s, "worry", "down", bob=-16 * s * abs(math.sin(ta * 7)), blink=blink_at(ta))
        return
    cv.rect((0, 0, W, H), (40, 44, 56))
    # cockpit windows
    cv.poly([(80, 470), (920, 470), (980, 760), (20, 760)], (30, 50, 100), INK, 6)
    cv.line([(UX, 470), (UX, 760)], INK, 10)
    for k in range(6):
        cv.circle(150 + k * 140, 520 + (k % 2) * 60, 3, WHITE)
    cv.rect((0, 760, W, 1000), (60, 64, 76), INK, 5)  # dashboard
    rnd = random.Random(int(ta * 4))
    for k in range(12):
        x = 60 + (k % 6) * 150
        y = 800 + (k // 6) * 90
        cv.rect((x, y, x + 110, y + 60), (20, 26, 30), INK, 3, r=8)
        cv.circle(x + 25, y + 30, 10, (60, 220, 120) if rnd.random() < 0.6 else (220, 160, 40))
    if ta >= cue("Der Autopilot") - 0.1:
        cv.rect((360, 820, 640, 920), (10, 20, 10), (60, 220, 120), 5, r=10)
        cv.text((UX, 892), "AUTOPILOT", font(40, "Black"), (60, 220, 120), "ms")
    for x in (230, 770):  # two empty pilot seats (seen from behind)
        cv.rect((x - 140, 1000, x + 140, 1460), (70, 60, 50), INK, 6, r=60)
        cv.rect((x - 90, 1020, x + 90, 1110), (90, 80, 70), INK, 4, r=30)
    if ta < cue("Beide Sitze"):  # door frame still visible while it opens
        k = ease(seg(ta, cue("Die Tür ist offen"), cue("Beide Sitze")))
        cv.rect((0, 380, 140 + 260 * (1 - k), 1500), (150, 156, 168), INK, 5)
        cv.rect((W - 140 - 260 * (1 - k), 380, W, 1500), (150, 156, 168), INK, 5)


def s_speaker(cv, t, dur, ta):
    cabin_back(cv, ta, night=True)
    cabin_rows(cv, lambda r, k: "sleep", ta, night=True)
    # speaker in the ceiling
    cv.circle(UX, 470, 60, (60, 60, 66), INK, 5)
    for k in range(5):
        cv.line([(UX - 40, 450 + k * 10), (UX + 40, 450 + k * 10)], (30, 30, 34), 3)
    if ta >= cue("Dann knackt"):
        for r_ in range(3):
            ph = (ta * 1.5 + r_ / 3) % 1.0
            rr = 80 + ph * 160
            cv.arc((UX - rr, 470 - rr, UX + rr, 470 + rr), 20, 160, (255, 214, 10, int(255 * (1 - ph))), 6)
    you_seated(cv, 760, 1250, 0.75, "shock" if ta >= cue("Bitte bleiben") else "worry", ta, (-1, -1))
    for key, lines, y in (("Bitte bleiben", ["Bitte bleiben", "Sie sitzen."], 640),
                          ("Sie sind der einzige", ["Sie sind der einzige", "Passagier, der", "aufgewacht ist."], 640)):
        nxt = cue("Sie sind der einzige") if key == "Bitte bleiben" else 1e9
        if cue(key) <= ta < nxt:
            k = min(1, (ta - cue(key)) / 0.25)
            h = 70 * len(lines) + 40
            cv.rect((90, y, 590, y + h), (20, 20, 26, int(230 * k)), (255, 214, 10), 4, r=26)
            for j, l in enumerate(lines):
                cv.text((340, y + 75 + j * 70), l, font(40, "Black"), (255, 240, 180), "ms")


def s_turn(cv, t, dur, ta):
    if ta < cue("Alle Passagiere haben"):
        cabin_back(cv, ta, night=True)
        cabin_rows(cv, lambda r, k: "sleep", ta, night=True)
        hero(cv, UX, 1880, 0.82, "worry", "down", look=(0, 0), blink=blink_at(ta))
        return
    # the turn: everyone has their eyes open and stares at you (= at the camera)
    cabin_back(cv, ta, night=True)
    cabin_rows(cv, lambda r, k: "stare", ta, night=True)
    cv.overlay((20, 0, 0), int(40 * seg(ta, cue("Alle Passagiere haben"), cue("Und schauen"))))


def s_final(cv, t, dur, ta):
    seat_view(cv, t, ta, "shock", look=(1, 0), night=True)
    for (x0, x1), lab, bg, fg in (((40, 470), "WECKEN", WHITE, INK), ((500, 930), "SCHLAFEN STELLEN", RED, WHITE)):
        cv.rect((x0, 1330, x1, 1440), bg, INK, 6, r=28)
        cv.text(((x0 + x1) / 2, 1405), lab, font(40, "Black"), fg, "ms")


SCENES = [s_board, s_silence, s_asleep, s_call, s_screen, s_pause, s_cockpit, s_speaker, s_turn, s_final]
PAUSE = 5
UI_SCENES = (3, 4, 5)
# extra hard cuts inside scenes (absolute times) – get the same soft crossfade as scene changes
INNER_CUTS = [cue("Niemand kommt"), cue("Die Tür ist offen"), cue("Alle Passagiere haben")]


def render(i, t=0.5, dur=5.0, ta=None):
    ta = BOUNDS[i][0] + t * (BOUNDS[i][1] - BOUNDS[i][0]) if ta is None else ta
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur, ta)
    img = cv.final()
    if i in UI_SCENES:
        z, cx, cy = 0.0, 500, 810
    else:
        z, cx, cy = 0.02 + 0.07 * ease(t), 540, 860
    if i == 8 and ta >= cue("Alle Passagiere haben"):  # slow creepy push-in on the staring cabin
        z = 0.02 + 0.14 * ease(seg(ta, cue("Alle Passagiere haben"), BOUNDS[8][1]))
        cx, cy = 500, 900
    img = T.camera(img, z, cx, cy)
    if i == PAUSE:
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, ta):
    if i == 0:
        return ("FLUG 404 · FRA → JFK", "white")
    if i in (1,):
        return ("STILLE", "white")
    if i == 2:
        return ("ALLE SCHLAFEN", "red")
    if i == 3:
        return ("RUFKNOPF", "white") if ta < cue("Niemand kommt") else ("NIEMAND KOMMT", "red")
    if i in (4, 5):
        return ("ANKUNFT: VOR 3 TAGEN", "red") if ta >= cue("vor drei Tagen") else ("FLUG 404", "white")
    if i == 6:
        return ("COCKPIT: LEER", "red") if ta >= cue("Beide Sitze") else ("COCKPIT", "white")
    if i == 7:
        return ("PASSAGIERE WACH: 1", "red") if ta >= cue("Sie sind der einzige") else ("DURCHSAGE", "white")
    if i == 8:
        return ("PASSAGIERE WACH: 187", "red") if ta >= cue("Alle Passagiere haben") else ("PASSAGIERE WACH: 1", "red")
    return ("FLUG 404", "white")
