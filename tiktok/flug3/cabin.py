"""Shared cabin helpers copied from ../flug/scenes14.py (Flug 404) (STIL 3, T.HERO). Scenes get (t, dur, ta) – ta = absolute video time,
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




# ---- realistic cabin: 3 seats left + aisle + 3 seats right, rows going all the way to the back
ROWS6 = [0.16, 0.2, 0.25, 0.31, 0.38, 0.47, 0.58, 0.71, 0.86]   # perspective scale, back -> front
SEAT_COLORS = [(52, 72, 120), (48, 66, 112)]


def row_y(s):
    return 640 + 1000 * s  # seat-cushion line of a row


def cabin_rows(cv, mood_fn, ta, night=False, empty=(), talk_seat=None, talk=0.0, skip_front=False, look_fn=None, all_empty=False):
    """mood_fn(row, seat) -> mood. seats are 0..5 (0-2 left of the aisle, 3-5 right)."""
    rows = ROWS6[:-1] if skip_front else ROWS6
    for ri, s in enumerate(rows):
        seat_w = 205 * s
        aisle = 150 * s
        cy = row_y(s)
        head_y = cy - 330 * s
        for k in range(6):
            side = -1 if k < 3 else 1
            j = (2 - k) if k < 3 else (k - 3)          # 0 = next to the aisle
            x = UX + side * (aisle / 2 + seat_w * (j + 0.5))
            cv.rect((x - seat_w * 0.46, head_y - 120 * s, x + seat_w * 0.46, cy), SEAT_COLORS[(ri + k) % 2], INK, 3,
                    r=int(seat_w * 0.18))
            cv.rect((x - seat_w * 0.34, head_y - 110 * s, x + seat_w * 0.34, head_y - 55 * s), WHITE, None, 0, r=int(seat_w * 0.1))
            if all_empty or (ri, k) in empty:
                cv.rect((x - seat_w * 0.5, cy - 40 * s, x + seat_w * 0.5, cy + 30 * s), (40, 56, 96), INK, 3, r=int(8 * s))
                continue
            kw = PASSENGERS[(ri * 5 + k * 3) % len(PASSENGERS)]
            cs = 0.42 * s
            T.character(cv, x, head_y + 753 * cs, cs, mood_fn(ri, k), "down",
                        talk=talk if talk_seat == (ri, k) else 0.0, look=look_fn(ri, k) if look_fn else (0, 0), **kw)
            cv.rect((x - seat_w * 0.5, cy - 40 * s, x + seat_w * 0.5, cy + 30 * s), (40, 56, 96), INK, 3, r=int(8 * s))  # cushion/armrest
        # armrests between blocks + overhead light row
        for side in (-1, 1):
            cv.rect((UX + side * aisle / 2 - 8 * s, cy - 70 * s, UX + side * aisle / 2 + 8 * s, cy + 30 * s), (30, 40, 70))


def dark(cv, alpha):
    if alpha > 0:
        cv.overlay((4, 4, 12), int(alpha))




def pair_seats(cv, ta, you_mood, twin=None, twin_mood="smug", twin_talk=0.0, night=True, you_arms="down", extra=None):
    """Your seat (left) and the seat next to you (right), front view; row in front covers the legs."""
    cv.rect((0, 0, W, H), (150, 156, 176) if night else CABIN)
    cv.rect((0, 0, W, 300), (170, 176, 196), INK, 4)
    window(cv, 40, 480, 180, 300, ta, night)
    s = 0.85
    for x, who in ((330, "you"), (720, "twin")):
        seat_front(cv, x, 780, s)
        if who == "you":
            hero(cv, x, 780 + 753 * s, s, you_mood, you_arms, blink=False)
        elif twin:
            hero(cv, x, 780 + 753 * s, s, twin_mood, "down", talk=twin_talk)
    if extra:
        extra()
    cv.rect((40, 780 + 380 * s, 1040, H), SEAT_D, INK, 6, r=50)  # backs of the row in front
    for x in (330, 720):
        cv.rect((x - 180, 780 + 430 * s, x + 180, 780 + 520 * s), (30, 40, 70), INK, 3, r=12)


# ------------------------------------------------------------------ scenes (cv, t, dur, ta)



def eyelid_dummy():
    pass


def tilt(img, deg, zoom=None):
    from PIL import Image as _I
    big = img.rotate(deg, resample=_I.BICUBIC, expand=False, fillcolor=(10, 10, 14))
    return T.camera(big, zoom if zoom is not None else 0.12 * min(1, abs(deg) / 12), 540, 960)
