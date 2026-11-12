"""STIL 3: friendly cartoon character with a face (front view), bright simple rooms,
falling money, one info chip on top, white captions with a yellow keyword.

Everything is drawn in 1080x1920 coordinates on the shared Canvas (2x supersampling).
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "bankraub"))
import scenes as S  # noqa: E402
from scenes import Canvas, font, mono, W, H  # noqa: E402

INK = (22, 22, 30)
WHITE = (255, 255, 255)
SKIN = (250, 214, 168)
HAIR = (128, 82, 44)
HOODIE = (40, 112, 222)
HOODIE_D = (30, 86, 180)
PANTS = (24, 26, 40)
BLUSH = (246, 160, 170)
YELLOW = (255, 214, 10)
# Main character look from video 12 on (user request 06.11.): dark hair, new hairstyle,
# dark-green jumper with horizontal stripes. Use as: character(..., **HERO)
HERO = dict(hair=(36, 26, 20), hoodie=(28, 84, 52), outfit="sweater", stripe=(70, 140, 92), hair_style="boxer",
            mustache=True, goatee=True)
MONEY = (110, 190, 100)
MONEY_D = (60, 140, 70)


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def seg(t, a, b):
    return max(0.0, min(1.0, (t - a) / (b - a)))


# ------------------------------------------------------------------ character

def eye(cv, x, y, r, mood, look=(0, 0), blink=False):
    if blink or mood in ("closed", "sleep"):
        cv.arc((x - r, y - r * 0.6, x + r, y + r * 0.9), 200, 340, INK, 7)
        return
    rr = r * (1.12 if mood in ("shock", "stare") else 1.0)
    cv.circle(x, y, rr, WHITE, INK, 7)
    pr = r * (0.32 if mood == "shock" else (0.22 if mood == "stare" else 0.42))
    px, py = x + look[0] * r * 0.3, y + look[1] * r * 0.3
    cv.circle(px, py, pr, INK)
    cv.circle(px - pr * 0.35, py - pr * 0.35, pr * 0.32, WHITE)


def face(cv, x, y, r, mood="neutral", blink=False, look=(0, 0), talk=0.0, glasses=False, tear=False):
    ex, ey, er = r * 0.38, y + r * 0.05, r * 0.27
    for s in (-1, 1):
        eye(cv, x + s * ex, ey, er, mood, look, blink)
    # brows
    if mood in ("worry", "sad"):
        for s in (-1, 1):
            cv.line([(x + s * (ex + er * 0.9), ey - er * 1.25), (x + s * (ex - er * 0.7), ey - er * 1.6)], INK, 7)
    elif mood == "angry":
        for s in (-1, 1):
            cv.line([(x + s * (ex + er * 0.9), ey - er * 1.7), (x + s * (ex - er * 0.7), ey - er * 1.25)], INK, 7)
    else:
        lift = 1.85 if mood == "shock" else 1.5
        for s in (-1, 1):
            cv.arc((x + s * ex - er * 0.8, ey - er * lift - er * 0.4, x + s * ex + er * 0.8, ey - er * lift + er * 0.6),
                   200, 340, INK, 6)
    # blush
    for s in (-1, 1):
        cv.ellipse((x + s * r * 0.62 - r * 0.15, y + r * 0.36, x + s * r * 0.62 + r * 0.15, y + r * 0.48), BLUSH)
    # mouth
    mx, my = x, y + r * 0.55
    if talk > 0.05 or mood == "shock":
        o = max(talk, 0.6 if mood == "shock" else 0)
        cv.ellipse((mx - r * 0.09, my - r * 0.05, mx + r * 0.09, my + r * (0.05 + 0.16 * o)), (120, 40, 50), INK, 4)
    elif mood in ("happy", "rich"):
        cv.d.chord(cv.s((mx - r * 0.22, my - r * 0.14, mx + r * 0.22, my + r * 0.2)), 0, 180, fill=(120, 40, 50))
        cv.arc((mx - r * 0.22, my - r * 0.14, mx + r * 0.22, my + r * 0.2), 0, 180, INK, 5)
    elif mood in ("worry", "closed"):
        pts = [(mx - r * 0.16 + k * r * 0.08, my + (r * 0.03 if k % 2 else -r * 0.03)) for k in range(5)]
        cv.line(pts, INK, 5)
    elif mood == "sad":
        cv.arc((mx - r * 0.16, my, mx + r * 0.16, my + r * 0.24), 200, 340, INK, 5)
    elif mood == "smug":
        cv.arc((mx - r * 0.2, my - r * 0.18, mx + r * 0.2, my + r * 0.08), 20, 120, INK, 6)
    else:
        cv.line([(mx - r * 0.07, my), (mx + r * 0.07, my)], INK, 5)
    if glasses:
        for s in (-1, 1):
            cv.rect((x + s * ex - er * 1.2, ey - er * 0.8, x + s * ex + er * 1.2, ey + er * 0.8), (20, 20, 26), INK, 4, r=14)
        cv.line([(x - ex + er * 1.2, ey - er * 0.3), (x + ex - er * 1.2, ey - er * 0.3)], INK, 6)
    if tear:
        cv.ellipse((x - ex - er * 0.3, ey + er * 1.0, x - ex + er * 0.15, ey + er * 1.7), (120, 190, 255), INK, 3)


def character(cv, x, y_feet, s=1.0, mood="neutral", arms="phone", blink=False, talk=0.0, look=(0, 0),
              glasses=False, chain=False, tear=False, bob=0.0, hoodie=HOODIE, hair=HAIR, tie=False,
              bald=False, mustache=False, specs=False, hair_style="fringe", outfit="hoodie", stripe=None,
              goatee=False, facemask=False, bulk=0.0, lift=0.0):
    """Front-view character. s=1 -> about 1000 px tall.
    bulk 0..1 = muscular build (broad shoulders, big arms, V-taper); outfit "tank" = gym tank top.
    Extra arm poses for the athletic body: "flex" (double biceps), "bar" (barbell, lift 0..1), "curl" (dumbbell, lift 0..1)."""
    r = 150 * s
    y_feet += bob
    hip_y = y_feet - 300 * s
    sh_y = hip_y - 330 * s
    hy = sh_y - r * 0.82
    athletic = bulk > 0 or outfit == "tank" or arms in ("flex", "bar", "curl")
    if athletic:
        _athletic_body(cv, x, y_feet, s, r, hy, hip_y, sh_y, arms, hoodie, outfit, stripe, bulk, lift)
    else:
        # legs + shoes
        for sx in (-1, 1):
            cv.rect((x + sx * 70 * s - 52 * s, hip_y - 20 * s, x + sx * 70 * s + 52 * s, y_feet - 30 * s), PANTS, INK, 6, r=int(16 * s))
            cv.ellipse((x + sx * 75 * s - 78 * s, y_feet - 58 * s, x + sx * 75 * s + 78 * s, y_feet + 8 * s), WHITE, INK, 6)
        # arms behind / beside the body
        def arm(side, kind):
            ax = x + side * 175 * s
            if kind == "down":
                cv.rect((ax - 44 * s, sh_y + 20 * s, ax + 44 * s, hip_y + 10 * s), hoodie, INK, 6, r=int(40 * s))
                if outfit == "sweater":
                    st = stripe or tuple(min(255, int(c * 1.55)) for c in hoodie)
                    y = sh_y + 70 * s
                    while y < hip_y - 20 * s:
                        cv.rect((ax - 38 * s, y, ax + 38 * s, y + 26 * s), st)
                        y += 70 * s
                    cv.rect((ax - 44 * s, sh_y + 20 * s, ax + 44 * s, hip_y + 10 * s), None, INK, 6, r=int(40 * s))
                cv.circle(ax, hip_y + 30 * s, 42 * s, SKIN, INK, 6)
            elif kind == "up":
                cv.line([(ax, sh_y + 40 * s), (ax + side * 70 * s, sh_y - 230 * s)], INK, 96 * s)
                cv.line([(ax, sh_y + 40 * s), (ax + side * 70 * s, sh_y - 230 * s)], hoodie, 84 * s)
                cv.circle(ax + side * 70 * s, sh_y - 260 * s, 44 * s, SKIN, INK, 6)
        left = "up" if arms == "up" else "down"
        right = "up" if arms == "up" else ("none" if arms in ("phone", "point", "head") else "down")
        arm(-1, left)
        if right != "none":
            arm(1, right)
        # torso (hoodie)
        cv.rect((x - 190 * s, sh_y - 10 * s, x + 190 * s, hip_y + 30 * s), hoodie, INK, 7, r=int(90 * s))
        if outfit == "sweater":  # crew-neck jumper with horizontal stripes and ribbed hem
            st = stripe or tuple(min(255, int(c * 1.55)) for c in hoodie)
            y = sh_y + 70 * s
            while y < hip_y - 10 * s:
                cv.rect((x - 183 * s, y, x + 183 * s, y + 26 * s), st)
                y += 70 * s
            cv.rect((x - 190 * s, sh_y - 10 * s, x + 190 * s, hip_y + 30 * s), None, INK, 7, r=int(90 * s))
            cv.rect((x - 186 * s, hip_y - 6 * s, x + 186 * s, hip_y + 26 * s), tuple(int(c * 0.8) for c in hoodie), INK, 4, r=int(14 * s))
            cv.d.chord(cv.s((x - 95 * s, sh_y - 55 * s, x + 95 * s, sh_y + 45 * s)), 0, 180, fill=tuple(int(c * 0.75) for c in hoodie))
            cv.d.arc(cv.s((x - 95 * s, sh_y - 55 * s, x + 95 * s, sh_y + 45 * s)), 0, 180, fill=INK, width=int(5 * s * 2))
        else:
            cv.rect((x - 100 * s, hip_y - 130 * s, x + 100 * s, hip_y - 40 * s), HOODIE_D, INK, 5, r=int(20 * s))
            cv.d.chord(cv.s((x - 150 * s, sh_y - 70 * s, x + 150 * s, sh_y + 90 * s)), 0, 180, fill=HOODIE_D)  # hood rim
            for sx in (-1, 1):
                cv.line([(x + sx * 45 * s, sh_y + 20 * s), (x + sx * 45 * s, sh_y + 130 * s)], WHITE, 7 * s)
                cv.circle(x + sx * 45 * s, sh_y + 136 * s, 9 * s, WHITE, INK, 2)
        if tie:
            cv.poly([(x - 30 * s, sh_y + 20 * s), (x + 30 * s, sh_y + 20 * s), (x + 40 * s, sh_y + 220 * s), (x, sh_y + 270 * s),
                     (x - 40 * s, sh_y + 220 * s)], (200, 40, 50), INK, 5)
        if chain:
            cv.arc((x - 110 * s, sh_y - 40 * s, x + 110 * s, sh_y + 150 * s), 20, 160, YELLOW, int(14 * s))
            cv.circle(x, sh_y + 150 * s, 26 * s, YELLOW, INK, 4)
            cv.text((x, sh_y + 162 * s), "$", font(30 * s, "Black"), INK, "ms")
        # right arm in front holding phone
        if arms == "phone":
            cv.rect((x + 30 * s, sh_y + 60 * s, x + 210 * s, sh_y + 160 * s), hoodie, INK, 6, r=int(46 * s))
            cv.rect((x + 40 * s, sh_y + 10 * s, x + 140 * s, sh_y + 190 * s), (50, 120, 230), INK, 6, r=int(16 * s))
            cv.rect((x + 54 * s, sh_y + 24 * s, x + 126 * s, sh_y + 176 * s), (110, 170, 255))
            cv.circle(x + 90 * s, sh_y + 165 * s, 38 * s, SKIN, INK, 6)
        elif arms == "point":
            cv.line([(x + 175 * s, sh_y + 40 * s), (x + 330 * s, sh_y - 40 * s)], INK, 96 * s)
            cv.line([(x + 175 * s, sh_y + 40 * s), (x + 330 * s, sh_y - 40 * s)], hoodie, 84 * s)
            cv.circle(x + 345 * s, sh_y - 50 * s, 42 * s, SKIN, INK, 6)
        elif arms == "head":
            cv.line([(x + 175 * s, sh_y + 40 * s), (x + 160 * s, hy - 40 * s)], INK, 96 * s)
            cv.line([(x + 175 * s, sh_y + 40 * s), (x + 160 * s, hy - 40 * s)], hoodie, 84 * s)
    # head
    for sx in (-1, 1):
        cv.circle(x + sx * r * 0.98, hy + r * 0.1, r * 0.2, SKIN, INK, 6)
    cv.circle(x, hy, r, SKIN, INK, 7)
    # hair: cap + jagged fringe
    if bald:  # only a hair ring on the sides
        for sx in (-1, 1):
            cv.ellipse((x + sx * r * 0.62 - r * 0.42, hy - r * 0.55, x + sx * r * 0.62 + r * 0.42, hy + r * 0.2), hair)
    elif hair_style == "side":  # side part, short sides, volume on top, loose strands over the forehead
        import math as _m
        top = []
        for a_ in range(200, 341, 4):
            t_ = (a_ - 200) / 140
            rad = r * (1.05 + 0.2 * _m.sin(_m.pi * t_) + 0.035 * _m.sin(t_ * _m.pi * 9))
            top.append((x + _m.cos(_m.radians(a_)) * rad, hy - r * 0.02 + _m.sin(_m.radians(a_)) * rad))
        low = [(x + r * 0.98, hy - r * 0.4), (x + r * 0.72, hy - r * 0.44),
               (x + r * 0.52, hy - r * 0.2), (x + r * 0.38, hy - r * 0.46),        # strand 1
               (x + r * 0.1, hy - r * 0.52),
               (x - r * 0.12, hy - r * 0.14), (x - r * 0.3, hy - r * 0.44),        # strand 2 (longest)
               (x - r * 0.55, hy - r * 0.4),
               (x - r * 0.7, hy - r * 0.24), (x - r * 0.8, hy - r * 0.38),          # strand 3
               (x - r * 0.99, hy - r * 0.34)]
        cv.poly(top + low, hair, INK, 5)
        light = tuple(min(255, c + 45) for c in hair)
        cv.line([(x - r * 0.45, hy - r * 1.12), (x - r * 0.55, hy - r * 0.55)], light, 6)   # parting
        cv.line([(x + r * 0.05, hy - r * 1.15), (x + r * 0.3, hy - r * 0.62)], light, 5)
        cv.line([(x + r * 0.45, hy - r * 1.05), (x + r * 0.62, hy - r * 0.6)], light, 4)
        # one loose curl hanging free in front
        curl = [(x + r * 0.2, hy - r * 0.5), (x + r * 0.28, hy - r * 0.32), (x + r * 0.22, hy - r * 0.16),
                (x + r * 0.12, hy - r * 0.12)]
        cv.line(curl, INK, r * 0.1)
        cv.line(curl, hair, r * 0.06)
    elif hair_style == "boxer":  # Boxerschnitt: sides almost shaved (stubble), short top
        import math as _m
        stub = tuple(int(c * 0.55 + h * 0.45) for c, h in zip(SKIN, hair))
        side = [(x + _m.cos(_m.radians(a_)) * r * 1.01, hy + _m.sin(_m.radians(a_)) * r * 1.01) for a_ in range(165, 376, 5)]
        side += [(x + r * 0.95, hy - r * 0.05), (x + r * 0.7, hy - r * 0.55), (x - r * 0.7, hy - r * 0.55), (x - r * 0.95, hy - r * 0.05)]
        cv.poly(side, stub)
        cv.circle(x, hy, r, None, INK, 7)
        top = []
        for a_ in range(210, 331, 4):
            t_ = (a_ - 210) / 120
            rad = r * (1.04 + 0.08 * _m.sin(_m.pi * t_) + 0.02 * _m.sin(t_ * _m.pi * 11))
            top.append((x + _m.cos(_m.radians(a_)) * rad, hy - r * 0.02 + _m.sin(_m.radians(a_)) * rad))
        low = [(x + r * 0.62, hy - r * 0.6), (x + r * 0.3, hy - r * 0.62), (x + r * 0.05, hy - r * 0.56),
               (x - r * 0.1, hy - r * 0.62), (x - r * 0.4, hy - r * 0.6), (x - r * 0.62, hy - r * 0.6)]
        cv.poly(top + low, hair, INK, 5)
        light = tuple(min(255, c + 40) for c in hair)
        for k in range(4):
            cx_ = x - r * 0.35 + k * r * 0.22
            cv.line([(cx_, hy - r * 1.02), (cx_ + r * 0.05, hy - r * 0.7)], light, 4)
    elif hair_style == "curly":
        cv.d.chord(cv.s((x - r * 1.04, hy - r * 1.05, x + r * 1.04, hy + r * 0.6)), 180, 360, fill=hair)
        import math as _m
        for k in range(11):
            a_ = _m.radians(195 + k * 15)
            cx_, cy_ = x + _m.cos(a_) * r * 0.92, hy - r * 0.08 + _m.sin(a_) * r * 0.95
            cv.circle(cx_, cy_, r * 0.27, hair, INK, 4)
        for k in range(5):
            cv.circle(x - r * 0.6 + k * r * 0.3, hy - r * 0.45, r * 0.2, hair)
    elif hair_style == "quiff":  # short sides, volume swept up at the front
        import math as _m
        top = []
        for a_ in range(185, 356, 5):
            t_ = (a_ - 185) / 170
            bump = 0.28 * _m.exp(-((t_ - 0.4) / 0.22) ** 2)
            top.append((x + _m.cos(_m.radians(a_)) * r * (1.06 + bump), hy - r * 0.02 + _m.sin(_m.radians(a_)) * r * (1.06 + bump)))
        low = [(x + r * 1.05, hy - r * 0.15), (x + r * 0.7, hy - r * 0.42), (x + r * 0.2, hy - r * 0.55),
               (x - r * 0.3, hy - r * 0.5), (x - r * 0.75, hy - r * 0.38), (x - r * 1.04, hy - r * 0.1)]
        cv.poly(top + low, hair, INK, 5)
        cv.line([(x - r * 0.3, hy - r * 1.1), (x + r * 0.1, hy - r * 0.62)], tuple(min(255, c + 45) for c in hair), 6)
    else:
        cv.d.chord(cv.s((x - r * 1.04, hy - r * 1.08, x + r * 1.04, hy + r * 0.7)), 180, 360, fill=hair)
        fringe = [(x - r * 1.0, hy - r * 0.2)]
        for k in range(7):
            fx = x - r * 0.95 + k * r * 0.32
            fringe += [(fx + r * 0.16, hy - r * (0.5 if k % 2 else 0.32)), (fx + r * 0.32, hy - r * 0.2)]
        fringe += [(x + r * 1.0, hy - r * 0.6), (x, hy - r * 1.1), (x - r * 1.0, hy - r * 0.6)]
        cv.poly(fringe, hair, INK, 5)
    face(cv, x, hy + r * 0.12, r, mood, blink, look, talk, glasses, tear)
    if mustache:  # short, thin moustache, slightly drooping at the ends
        my = hy + r * 0.6
        for sx in (-1, 1):
            pts = [(x, my - r * 0.03), (x + sx * r * 0.1, my - r * 0.04), (x + sx * r * 0.17, my + r * 0.0),
                   (x + sx * r * 0.2, my + r * 0.06)]
            cv.line(pts, INK, r * 0.08)
            cv.line(pts, hair, r * 0.045)
    if goatee:  # small chin beard below the mouth
        cy_ = hy + r * 0.93
        pts = [(x - r * 0.13, cy_), (x - r * 0.06, cy_ - r * 0.03), (x + r * 0.06, cy_ - r * 0.03), (x + r * 0.13, cy_),
               (x + r * 0.1, cy_ + r * 0.13), (x, cy_ + r * 0.22), (x - r * 0.1, cy_ + r * 0.13)]
        cv.poly(pts, hair, INK, 4)
    if facemask:  # light-blue surgical mask with ear loops
        mx0, mx1 = x - r * 0.48, x + r * 0.48
        my0, my1 = hy + r * 0.42, hy + r * 0.92
        for sx in (-1, 1):
            cv.line([(x + sx * r * 0.48, hy + r * 0.5), (x + sx * r * 0.95, hy + r * 0.12)], (230, 236, 240), 5)
        cv.rect((mx0, my0, mx1, my1), (190, 225, 245), INK, 4, r=int(r * 0.12))
        for k in range(3):
            yy = my0 + (my1 - my0) * (0.28 + k * 0.22)
            cv.line([(mx0 + r * 0.06, yy), (mx1 - r * 0.06, yy)], (150, 195, 225), 4)
    if specs:
        for sx in (-1, 1):
            cv.circle(x + sx * r * 0.38, hy + r * 0.17, r * 0.33, None, INK, 6)
        cv.line([(x - r * 0.05, hy + r * 0.12), (x + r * 0.05, hy + r * 0.12)], INK, 6)
    if arms == "head" and not athletic:
        cv.circle(x + 160 * s, hy - 60 * s, 46 * s, SKIN, INK, 6)
    return hy


def _limb(cv, pts, w, col):
    """Thick rounded limb through pts (outlined)."""
    cv.line(pts, INK, w + 12)
    for p in pts:
        cv.circle(p[0], p[1], (w + 12) / 2, INK)
    cv.line(pts, col, w)
    for p in pts:
        cv.circle(p[0], p[1], w / 2, col)


def _athletic_body(cv, x, y_feet, s, r, hy, hip_y, sh_y, arms, shirt, outfit, stripe, B, lift):
    """Muscular front-view body; B = bulk 0..1. Arms are skin-coloured in a tank top."""
    shw = (190 + 85 * B) * s            # half shoulder width
    waw = (172 + 12 * B) * s             # half waist width
    armw = (84 + 44 * B) * s
    hand = (42 + 14 * B) * s
    acol = SKIN if outfit == "tank" else shirt
    dark = tuple(int(c * 0.78) for c in shirt)
    skin_d = (226, 180, 136)
    # legs
    legw, legx = 52 * (1 + 0.35 * B) * s, 70 * (1 + 0.2 * B) * s
    for sx in (-1, 1):
        cv.rect((x + sx * legx - legw, hip_y - 20 * s, x + sx * legx + legw, y_feet - 30 * s), PANTS, INK, 6, r=int(16 * s))
        cv.ellipse((x + sx * (legx + 5 * s) - 78 * s, y_feet - 58 * s, x + sx * (legx + 5 * s) + 78 * s, y_feet + 8 * s), WHITE, INK, 6)
    shoulder = {sd: (x + sd * (shw - 40 * s), sh_y + 55 * s) for sd in (-1, 1)}
    hands = {}

    def arm(sd, pose):
        sx_, sy_ = shoulder[sd]
        if pose == "down":
            el = (sx_ + sd * 22 * s * (1 + B), sy_ + 170 * s)
            hd = (sx_ + sd * 26 * s * (1 + B), hip_y + 20 * s)
            _limb(cv, [(sx_, sy_), el, hd], armw, acol)
            if B > 0.15:                  # biceps / forearm shape
                cv.circle(el[0] - sd * armw * 0.05, sy_ + 95 * s, armw * (0.5 + 0.12 * B), acol)
        elif pose == "flex":
            el = (sx_ + sd * (135 + 25 * B) * s, sy_ - 5 * s)
            hd = (el[0] - sd * 10 * s, sy_ - 185 * s)
            _limb(cv, [(sx_, sy_), el], armw, acol)
            _limb(cv, [el, hd], armw * 0.86, acol)
            mx, my = (sx_ + el[0]) / 2, sy_ - armw * 0.35
            cv.circle(mx, my, armw * (0.36 + 0.2 * B), acol, INK, 6)    # biceps peak
            cv.line([(mx - armw * 0.25, my + armw * 0.25), (mx + armw * 0.25, my + armw * 0.25)], acol, armw * 0.5)
        elif pose == "up":
            hd = (sx_ + sd * 70 * s, sh_y - 260 * s)
            _limb(cv, [(sx_, sy_), hd], armw, acol)
        elif pose == "point":
            hd = (x + sd * (330 + 60 * B) * s, sh_y - 50 * s)
            _limb(cv, [(sx_, sy_), hd], armw, acol)
        elif pose == "bar":               # overhead / front press, lift 0..1
            hy_ = sh_y + 40 * s - 300 * s * lift
            hd = (sx_ + sd * 40 * s, hy_)
            el = (sx_ + sd * (110 + 30 * B) * s, (sy_ + hy_) / 2 + 60 * s)
            _limb(cv, [(sx_, sy_), el, hd], armw * 0.95, acol)
        elif pose == "curl":              # dumbbell curl, lift 0..1
            el = (sx_ + sd * 10 * s, sy_ + 200 * s)
            ang = math.radians(90 - 160 * lift)
            hd = (el[0] + sd * 40 * s * math.sin(math.radians(160 * lift)), el[1] + math.sin(ang) * 190 * s)
            _limb(cv, [(sx_, sy_), el], armw, acol)
            cv.circle((sx_ + el[0]) / 2, (sy_ + el[1]) / 2, armw * (0.5 + 0.25 * B * lift + 0.1 * B), acol)
            _limb(cv, [el, hd], armw * 0.85, acol)
        hands[sd] = hd

    poses = {"flex": ("flex", "flex"), "bar": ("bar", "bar"), "up": ("up", "up"), "point": ("down", "point"),
             "curl": ("down", "curl")}.get(arms, ("down", "down"))
    arm(-1, poses[0])
    arm(1, poses[1])
    # neck / traps
    cv.poly([(x - 0.42 * shw, sh_y + 20 * s), (x - r * 0.42, hy + r * 0.6), (x + r * 0.42, hy + r * 0.6),
             (x + 0.42 * shw, sh_y + 20 * s)], SKIN, INK, 6)
    # torso: V-taper
    torso = [(x - shw + 40 * s, sh_y - 5 * s), (x + shw - 40 * s, sh_y - 5 * s), (x + shw, sh_y + 80 * s),
             (x + waw, hip_y + 30 * s), (x - waw, hip_y + 30 * s), (x - shw, sh_y + 80 * s)]
    if outfit == "tank":
        cv.poly(torso, SKIN, INK, 7)
        tank = [(x - 0.62 * shw, sh_y - 5 * s), (x - 0.38 * shw, sh_y - 5 * s), (x - 0.2 * shw, sh_y + 90 * s),
                (x + 0.2 * shw, sh_y + 90 * s), (x + 0.38 * shw, sh_y - 5 * s), (x + 0.62 * shw, sh_y - 5 * s),
                (x + 0.86 * shw, sh_y + 200 * s), (x + waw, hip_y + 30 * s), (x - waw, hip_y + 30 * s),
                (x - 0.86 * shw, sh_y + 200 * s)]
        cv.poly(tank, shirt, INK, 6)
        if B > 0.3:                       # pecs + abs hints
            for sd in (-1, 1):
                cv.arc((x + sd * 0.45 * shw - 0.45 * shw, sh_y + 60 * s, x + sd * 0.45 * shw + 0.45 * shw, sh_y + 230 * s),
                       20 if sd < 0 else 40, 140 if sd < 0 else 160, dark, int(7 * s))
            for k in range(2):
                yy = sh_y + (260 + 60 * k) * s
                cv.line([(x - 50 * s, yy), (x + 50 * s, yy)], dark, 5 * s)
            cv.line([(x, sh_y + 240 * s), (x, hip_y - 20 * s)], dark, 5 * s)
    else:
        cv.poly(torso, shirt, INK, 7)
        if outfit == "sweater":
            st = stripe or tuple(min(255, int(c * 1.55)) for c in shirt)
            y = sh_y + 70 * s
            while y < hip_y - 10 * s:
                f = (y - sh_y) / (hip_y - sh_y)
                hw = shw + (waw - shw) * f - 8 * s
                cv.rect((x - hw, y, x + hw, y + 26 * s), st)
                y += 70 * s
            cv.poly(torso, None, INK, 7)
        cv.d.chord(cv.s((x - 95 * s, sh_y - 55 * s, x + 95 * s, sh_y + 45 * s)), 0, 180, fill=dark)
    cv.rect((x - waw + 4 * s, hip_y - 2 * s, x + waw - 4 * s, hip_y + 34 * s), PANTS, INK, 4, r=int(10 * s))
    # deltoids over the torso edge
    for sd in (-1, 1):
        if poses[0 if sd < 0 else 1] in ("down", "point", "bar", "curl", "up", "flex"):
            px_, py_ = shoulder[sd]
            cv.circle(px_, py_ - 5 * s, armw * 0.52, acol, INK, 6)
            cv.circle(px_ - sd * armw * 0.1, py_ + 6 * s, armw * 0.42, acol)
    # hands (+ props)
    if arms == "bar":
        y_ = hands[-1][1]
        cv.line([(x - shw - 230 * s, y_), (x + shw + 230 * s, y_)], (90, 92, 100), 22 * s)
        for sd in (-1, 1):
            for k, (ww_, hh_) in enumerate(((44, 230), (34, 180))):
                px_ = x + sd * (shw + 150 * s + k * 50 * s)
                cv.rect((px_ - ww_ * s / 2, y_ - hh_ * s / 2, px_ + ww_ * s / 2, y_ + hh_ * s / 2), (40, 42, 50), INK, 5, r=int(8 * s))
    if arms == "curl":
        hx, hy2 = hands[1]
        cv.line([(hx - 70 * s, hy2), (hx + 70 * s, hy2)], (90, 92, 100), 20 * s)
        for sd in (-1, 1):
            cv.rect((hx + sd * 70 * s - 22 * s, hy2 - 55 * s, hx + sd * 70 * s + 22 * s, hy2 + 55 * s), (40, 42, 50), INK, 5, r=int(8 * s))
    for sd, (hx, hy2) in hands.items():
        cv.circle(hx, hy2, hand, SKIN, INK, 6)
        if arms in ("flex",):
            cv.arc((hx - hand * 0.6, hy2 - hand * 0.5, hx + hand * 0.6, hy2 + hand * 0.4), 200, 340, skin_d, int(5 * s))


# ------------------------------------------------------------------ props / backgrounds

def bill(cv, x, y, w=150, rot=0):
    h = w * 0.45
    ca, sa = math.cos(rot), math.sin(rot)
    def p(u, v):
        return (x + u * ca - v * sa, y + u * sa + v * ca)
    cv.poly([p(-w / 2, -h / 2), p(w / 2, -h / 2), p(w / 2, h / 2), p(-w / 2, h / 2)], MONEY, INK, 4)
    cv.poly([p(-w * 0.12, -h / 2), p(w * 0.12, -h / 2), p(w * 0.12, h / 2), p(-w * 0.12, h / 2)], (230, 240, 220))
    cx, cy = p(-w * 0.32, 0)
    cv.circle(cx, cy, h * 0.22, MONEY_D)


def falling_money(cv, t, n=14, seed=1, area=(0, 300, W, 1500)):
    rnd = random.Random(seed)
    for _ in range(n):
        x0 = rnd.uniform(area[0], area[2])
        sp = rnd.uniform(250, 420)
        y = area[1] + ((rnd.uniform(0, 1500) + t * sp * 6) % (area[3] - area[1]))
        rot = rnd.uniform(0, 6.28) + t * rnd.uniform(-3, 3)
        bill(cv, x0 + 30 * math.sin(t * 5 + x0), y, rnd.uniform(110, 160), rot)


def money_pile(cv, y_top=1380, seed=2, n=70):
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(-60, W + 60)
        dist = abs(x - 540) / 540
        y = y_top + dist * -120 + rnd.uniform(0, 600)
        bill(cv, x, y, rnd.uniform(130, 190), rnd.uniform(-0.6, 0.6))


def bedroom(cv, night=True, lights=True):
    cv.rect((0, 0, W, H), (54, 62, 120) if night else (150, 170, 220))
    # window with city
    cv.rect((60, 120, 760, 900), (20, 26, 60), INK, 8)
    rnd = random.Random(3)
    x = 70
    while x < 750:
        bw = rnd.randint(70, 130)
        bh = rnd.randint(260, 620)
        cv.rect((x, 890 - bh, x + bw, 890), (30, 38, 80))
        for wy in range(890 - bh + 20, 880, 46):
            for wx in range(x + 12, x + bw - 16, 28):
                if lights and rnd.random() < 0.45:
                    cv.rect((wx, wy, wx + 14, wy + 22), (255, 220, 90))
        x += bw + 8
    cv.circle(640, 220, 46, (250, 250, 230))
    cv.rect((760, 100, 1020, 1000), (180, 70, 110), INK, 6)  # curtain
    for k in range(4):
        cv.line([(790 + k * 60, 110), (790 + k * 60, 990)], (150, 50, 90), 6)
    cv.rect((0, 1080, W, H), (120, 80, 60))  # floor
    cv.rect((0, 900, W, 1090), (64, 74, 140))  # wall bottom
    # bed (left)
    cv.rect((-60, 880, 300, 1150), (60, 100, 200), INK, 7, r=20)
    cv.rect((-60, 820, 260, 910), WHITE, INK, 7, r=30)
    cv.rect((-60, 1130, 320, 1190), (120, 70, 50), INK, 6)


def chip(img, text, kind="green", k=1.0, y=330, warn=None):
    """Top info chip: green (money), red (warning, with triangle icon), white or yellow."""
    if not text or k <= 0:
        return img
    warn = (kind == "red") if warn is None else warn
    d = ImageDraw.Draw(img, "RGBA")
    size = 70
    while True:
        f = font(int(size * (0.75 + 0.25 * ease(k))), "Black")
        tw = d.textlength(text, font=f)
        if tw + (90 if warn else 0) < 820 or size < 36:
            break
        size -= 4
    fs = f.size
    cx = 500
    bg, fg = {"green": ((40, 120, 60), YELLOW), "red": ((220, 40, 50), WHITE),
              "white": ((255, 255, 255), INK), "yellow": (YELLOW, INK)}[kind]
    a = int(255 * min(1, k * 2))
    pad = 30
    iw = fs * 1.1 if warn else 0
    box = (cx - (tw + iw) / 2 - pad, y, cx + (tw + iw) / 2 + pad, y + fs + 40)
    d.rounded_rectangle((box[0] - 6, box[1] - 6, box[2] + 6, box[3] + 6), 22, fill=(255, 255, 255, a))
    d.rounded_rectangle(box, 18, fill=bg + (a,), outline=INK, width=4)
    tx = box[0] + pad
    if warn:
        ty = y + 20
        d.polygon([(tx + fs * 0.45, ty), (tx + fs * 0.92, ty + fs * 0.85), (tx, ty + fs * 0.85)], fill=WHITE)
        d.rectangle((tx + fs * 0.41, ty + fs * 0.28, tx + fs * 0.5, ty + fs * 0.58), fill=bg)
        d.rectangle((tx + fs * 0.41, ty + fs * 0.65, tx + fs * 0.5, ty + fs * 0.74), fill=bg)
        tx += iw
    d.text((tx, y + 20), text, font=f, fill=fg)
    return img


def caption(img, words, hi=(), y=1260, visible=None):
    """White caption, black outline, keyword in yellow (reference style)."""
    visible = len(words) if visible is None else visible
    d = ImageDraw.Draw(img, "RGBA")
    size = 70
    while True:
        f = font(size, "Black")
        space = d.textlength(" ", font=f)
        widths = [d.textlength(w_, font=f) for w_ in words]
        total = sum(widths) + space * (len(words) - 1)
        if total <= 820 or size <= 40:
            break
        size -= 4
    x = 500 - total / 2
    for i, w_ in enumerate(words):
        if i >= visible:
            break
        d.text((x, y), w_, font=f, fill=YELLOW if i in hi else WHITE, anchor="ls", stroke_width=7, stroke_fill=INK)
        x += widths[i] + space
    return img


def camera(img, z, cx=540, cy=900):
    """Zoom towards (cx, cy) by factor (1+z)."""
    if z < 0.002:
        return img
    w, h = img.size
    nw, nh = int(w * (1 + z)), int(h * (1 + z))
    big = img.resize((nw, nh), Image.BILINEAR)
    x0 = int(cx * (1 + z) - cx)
    y0 = int(cy * (1 + z) - cy)
    return big.crop((x0, y0, x0 + w, y0 + h))
