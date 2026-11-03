"""Clear scenes for 'PATIENT NULL'. Reuses rig + environment helpers (geldtransporter, lotto)."""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "lotto"))
sys.path.append(os.path.join(HERE, "..", "geldtransporter"))
sys.path.append(os.path.join(HERE, "..", "bankraub"))
import scenes4 as S4  # noqa: E402
import scenes5 as S5  # noqa: E402
from scenes4 import S, Canvas, font, mono, W, H, ease, seg, sky, street, house, lamp, wheel  # noqa: E402,F401
import rig  # noqa: E402
from rig import Look, figure, name_tag  # noqa: E402

INK, WHITE = rig.INK, rig.WHITE
C = dict(S5.C)
C.update({"zskin": (150, 190, 120), "zcloth": (120, 110, 95), "olive": (96, 104, 62), "smoke": (90, 84, 86)})

DU = Look(jacket=C["red_j"], hair=(70, 45, 30), name="DU")
SOLDIER = Look(jacket=C["olive"], pants=(70, 74, 50), hat=(80, 88, 52), hat_kind="helmet", name="SOLDAT")
ZOMBIE_LOOKS = [Look(jacket=c, pants=(60, 58, 66), skin=C["zskin"], hair=h)
                for c, h in (((120, 110, 95), (60, 50, 40)), ((90, 100, 120), (30, 30, 30)),
                             ((130, 90, 90), (90, 70, 40)), ((100, 120, 100), (50, 40, 35)))]


def zpose(p):
    q = rig.walk(p, 0.5)
    q.sh_n, q.el_n = 80 + 6 * math.sin(p * 6.28), 5
    q.sh_f, q.el_f = 75, 5
    q.lean = 8
    q.mood = "zombie"
    return q


def apoc_sky(cv):
    sky(cv, (70, 50, 60), (220, 120, 80))
    for k in range(3):
        x = 150 + k * 380
        for j in range(6):
            cv.circle(x + j * 18, 420 - j * 60, 60 + j * 14, C["smoke"] + (150,))


def car(cv, x, y, col, s=1.0, door=False, angle=0):
    L = 380 * s
    cv.rect((x, y - 120 * s, x + L, y - 30 * s), col, INK, 5, r=int(30 * s))
    cv.poly([(x + L * 0.22, y - 120 * s), (x + L * 0.32, y - 190 * s), (x + L * 0.72, y - 190 * s),
             (x + L * 0.82, y - 120 * s)], col, INK, 4)
    cv.rect((x + L * 0.36, y - 180 * s, x + L * 0.68, y - 125 * s), (160, 200, 228), INK, 3)
    if door:
        cv.poly([(x + L * 0.3, y - 120 * s), (x + L * 0.1, y - 160 * s), (x + L * 0.1, y - 60 * s),
                 (x + L * 0.3, y - 40 * s)], col, INK, 4)
    for wx in (x + L * 0.2, x + L * 0.8):
        wheel(cv, wx, y - 22 * s, 36 * s, 0)


def stadium(cv):
    cv.d.chord(cv.s((-100, 380, 1180, 1300)), 180, 360, fill=(170, 176, 186))
    cv.rect((-100, 830, 1180, 1140), (170, 176, 186), INK, 5)
    for k in range(10):
        cv.line([(k * 120, 840), (k * 120, 1140)], (140, 146, 156), 4)
    cv.rect((280, 700, 800, 790), (40, 90, 160), INK, 5, r=10)
    cv.text((540, 770), "STADION", font(70, "Black"), WHITE, "ms")
    for k in range(4):
        x = 140 + k * 280
        cv.rect((x - 6, 440, x + 6, 700), (60, 60, 66))
        cv.rect((x - 60, 410, x + 60, 450), (240, 240, 220), INK, 3)


def heli(cv, x, y, s=1.0, t=0.0, lift=0.0):
    y -= lift
    cv.rect((x - 200 * s, y - 120 * s, x + 120 * s, y + 40 * s), (70, 84, 60), INK, 5, r=int(70 * s))
    cv.rect((x + 100 * s, y - 70 * s, x + 380 * s, y - 30 * s), (70, 84, 60), INK, 4, r=10)
    cv.rect((x + 340 * s, y - 130 * s, x + 380 * s, y - 30 * s), (70, 84, 60), INK, 4, r=8)
    cv.ellipse((x - 180 * s, y - 100 * s, x - 60 * s, y - 10 * s), (160, 200, 228), INK, 4)
    cv.line([(x - 150 * s, y + 70 * s), (x + 90 * s, y + 70 * s)], INK, 8)
    cv.line([(x - 40 * s, y - 120 * s), (x - 40 * s, y - 160 * s)], INK, 8)
    span = 360 * s * abs(math.cos(t * 40))
    cv.line([(x - 40 * s - span, y - 160 * s), (x - 40 * s + span, y - 160 * s)], (40, 40, 44), 10)
    cv.text((x - 40 * s, y + 20 * s), "BUNDESWEHR", font(int(26 * s), "Black"), WHITE, "ms")


# ------------------------------------------------------------------ scenes

def s_wake(cv, t):
    S5.room(cv, (160, 150, 170))
    S5.window(cv, 560, 340, 400, 380)
    cv.rect((574, 354, 946, 706), (200, 110, 80))
    for k in range(4):
        cv.circle(640 + k * 90, 560 - k * 30, 50 + k * 10, C["smoke"])
    if int(t * 6) % 2 == 0:
        cv.glow(760, 520, 140, (255, 60, 60), 90)
    # bed
    cv.rect((40, 1000, 760, 1260), (120, 90, 70), INK, 5, r=20)
    cv.rect((60, 960, 740, 1100), (120, 150, 200), INK, 5, r=30)
    cv.rect((60, 900, 230, 980), WHITE, INK, 4, r=24)
    situp = ease(seg(t, 0, 0.25))
    hx, hy = 200 + 120 * situp, 930 - 160 * situp
    cv.rect((hx - 90, hy + 80, hx + 90, hy + 260), C["red_j"], INK, 5, r=50)
    rig.head(cv, hx, hy, 85, DU, rig.Pose(mood="shock" if t > 0.3 else "neutral", blink=t < 0.12), 1)
    # phone close-up
    k = ease(seg(t, 0.15, 0.35))
    if k > 0:
        y = 1400 - 500 * k
        cv.rect((620, y - 380, 960, y + 100), (20, 20, 24), INK, 6, r=40)
        cv.rect((640, y - 350, 940, y + 70), (236, 240, 246))
        cv.text((790, y - 290), "63", font(90, "Black"), (220, 40, 40), "ms")
        cv.text((790, y - 230), "verpasste Anrufe", font(28, "Bold"), INK, "ms")
        for j in range(4):
            cv.rect((660, y - 200 + j * 62, 920, y - 150 + j * 62), (250, 250, 250), (200, 200, 210), 2, r=10)
            cv.text((680, y - 162 + j * 62), "LABOR", font(28, "Black"), INK)
            cv.circle(895, y - 175 + j * 62, 10, (220, 40, 40))


def s_alone(cv, t):
    apoc_sky(cv)
    S4.houses(cv)
    street(cv)
    car(cv, 520, 1380, (70, 110, 170), door=True)
    car(cv, -120, 1540, (200, 180, 70), door=True)
    for k in range(3):
        rnd = random.Random(k)
        x = (rnd.uniform(0, 900) + t * 300) % 1000
        cv.rect((x, 1600 - k * 50, x + 70, 1640 - k * 50), (240, 236, 220), INK, 2)
    x = 330 + 180 * ease(seg(t, 0.1, 0.8))
    figure(cv, x, 1330, 60, DU, rig.walk(t * 2.5) if 0.1 < t < 0.8 else rig.stand(t), facing=1)


def s_radio(cv, t):
    cv.img.paste((40, 42, 48), (0, 0) + cv.img.size)
    apoc_sky(cv)
    cv.rect((0, 0, W, 330), (40, 42, 48))
    cv.rect((0, 900, W, H), (50, 52, 58))
    cv.rect((0, 880, W, 940), (70, 72, 80), INK, 4)
    cv.rect((240, 960, 840, 1180), (24, 24, 28), INK, 6, r=20)
    cv.rect((280, 990, 800, 1080), (40, 90, 60))
    cv.text((540, 1050), "NOTFUNK  87.6", mono(48), (140, 255, 170), "ms")
    for k in range(3):
        r = 60 + ((t * 2 + k / 3) % 1.0) * 160
        cv.arc((540 - r, 1120 - r, 540 + r, 1120 + r), 200, 340, (140, 255, 170), 6)
    # road sign seen through the windshield
    cv.rect((660, 560, 680, 880), (60, 60, 66))
    cv.rect((520, 520, 960, 620), (40, 120, 200), INK, 5, r=10)
    cv.text((720, 590), "STADION  →", font(52, "Black"), WHITE, "ms")


def s_run(cv, t):
    apoc_sky(cv)
    S4.houses(cv)
    street(cv)
    cv.circle(690, 760, 70, WHITE, INK, 5)
    cv.text((690, 780), "11:20", mono(36), INK, "ms")
    x = -60 + 900 * seg(t, 0, 1)
    figure(cv, x, 1400, 62, DU, rig.run(t * 4), facing=1)


def zombies_crowd(cv, t, xs, y, facing=-1, r=52, speed=1.0, dx=0.0):
    for k, x in enumerate(xs):
        lk = ZOMBIE_LOOKS[k % len(ZOMBIE_LOOKS)]
        figure(cv, x + dx, y + (k % 3) * 40, r, lk, zpose(t * speed + k * 0.37), facing=facing)


def s_zombies(cv, t):
    apoc_sky(cv)
    S4.houses(cv)
    street(cv)
    cv.rect((900, 640, 930, 1140), (50, 50, 56))
    cv.rect((870, 600, 960, 760), (30, 30, 34), INK, 4, r=10)
    for k, col in enumerate(((220, 50, 50), (70, 70, 60), (70, 70, 60))):
        cv.circle(915, 630 + k * 50, 18, col)
    figure(cv, 160, 1430, 62, DU, rig.Pose(mood="shock"), facing=1)
    n = 2 + int(ease(seg(t, 0, 0.6)) * 4)
    xs = [560 + (k % 3) * 160 for k in range(n)]
    zombies_crowd(cv, t * 3, xs, 1330 + 0, facing=-1, dx=120 * (1 - ease(t)))


def s_pass(cv, t):
    apoc_sky(cv)
    S4.houses(cv)
    street(cv)
    zombies_crowd(cv, t * 3, [180, 420], 1300, facing=1, dx=-260 + 380 * t)
    figure(cv, 540, 1450, 66, DU, rig.Pose(mood="shock", sh_n=-5, sh_f=5), facing=1)
    zombies_crowd(cv, t * 3 + 0.5, [700, 940], 1560, facing=-1, dx=260 - 520 * t)


def s_stadium(cv, t):
    apoc_sky(cv)
    stadium(cv)
    cv.rect((0, 1140, W, H), (90, 110, 80))
    heli(cv, 680, 1050, 0.9, t)
    p = rig.Pose(sh_n=85, el_n=0, sh_f=80, el_f=0, mood="angry", mouth=0.7 if t > 0.75 else 0)
    figure(cv, 760, 1450, 62, SOLDIER, p, facing=-1)
    cv.rect((560, 1110, 680, 1135), (30, 30, 34), r=4)  # weapon shape (no details)
    figure(cv, 240, 1450, 62, DU, rig.Pose(mood="shock", sh_n=150, sh_f=150, el_n=10, el_f=10), facing=1)


def s_tablet(cv, t):
    cv.img.paste((44, 48, 40), (0, 0) + cv.img.size)
    cv.rect((170, 420, 910, 1420), (24, 24, 28), INK, 8, r=40)
    cv.rect((200, 450, 880, 1390), (236, 240, 246))
    cv.rect((200, 450, 880, 540), (40, 90, 160))
    cv.text((540, 512), "LABOR · MITARBEITER", font(36, "Black"), WHITE, "ms")
    scan = seg(t, 0, 0.35)
    cv.rect((300, 600, 780, 1060), (200, 210, 220), INK, 4)
    cv.rect((420, 900, 660, 1060), C["red_j"])
    rig.head(cv, 540, 780, 120, DU, rig.Pose(), 0)
    if scan < 1:
        y = 600 + 460 * scan
        cv.rect((300, y - 6, 780, y + 6), (60, 255, 120))
    k = ease(seg(t, 0.8, 0.9))
    if k > 0:
        cv.rect((200, 1070, 880, 1170), (220, 40, 40, int(255 * k)))
        cv.text((540, 1148), "PATIENT NULL", font(72, "Black"), WHITE, "ms")
    cv.text((540, 585), "Status: INFIZIERT · symptomfrei", font(30, "Bold"), (160, 40, 40), "ms")


def s_flashback(cv, t):
    cv.img.paste((214, 200, 170), (0, 0) + cv.img.size)
    cv.rect((0, 1150, W, H), (180, 160, 130))
    cv.rect((380, 980, 1020, 1160), (150, 140, 120), INK, 5)  # lab bench
    for k in range(4):
        x = 120 + k * 220
        cv.rect((x, 860, x + 60, 980), (200, 220, 210), INK, 3, r=10)
    lab = Look(jacket=(245, 245, 240), hair=(70, 45, 30))
    figure(cv, 260, 1150, 66, lab, rig.Pose(sh_n=70, el_n=30, mood="shock" if t > 0.3 else "neutral"), facing=1)
    k = ease(seg(t, 0.2, 0.5))
    fx, fy = 640, 860 + 240 * k
    if k < 1:
        cv.poly([(fx - 40, fy - 90), (fx + 40, fy - 90), (fx + 70, fy), (fx - 70, fy)], (200, 230, 210), INK, 4)
        cv.rect((fx - 60, fy - 40, fx + 60, fy), (100, 200, 110))
    else:
        for j in range(7):
            a = j / 7 * math.pi
            cv.poly([(fx + 120 * math.cos(a), 1100 - 60 * math.sin(a)),
                     (fx + 150 * math.cos(a), 1090 - 80 * math.sin(a)),
                     (fx + 130 * math.cos(a) + 15, 1110 - 60 * math.sin(a))], (200, 230, 210), INK, 3)
        cv.glow(fx, 1000, 260 * ease(seg(t, 0.5, 0.8)), (120, 220, 120), 160)
    cv.rect((60, 560, 400, 630), (120, 90, 50), INK, 4, r=10)
    cv.text((230, 610), "RÜCKBLENDE", font(40, "Black"), WHITE, "ms")


def s_final(cv, t):
    apoc_sky(cv)
    stadium(cv)
    cv.rect((0, 1140, W, H), (90, 110, 80))
    heli(cv, 680, 1050, 0.9, t)
    p = rig.Pose(sh_n=110 * ease(seg(t, 0, 0.3)), el_n=0, sh_f=-10, mood="neutral", mouth=abs(math.sin(t * 20)) * 0.6 if 0.1 < t < 0.4 else 0)
    figure(cv, 760, 1250, 58, SOLDIER, p, facing=-1)
    figure(cv, 300, 1250, 58, DU, rig.Pose(mood="shock"), facing=1)
    zombies_crowd(cv, t * 2, [-40], 1150, facing=1, r=40)
    cv.rect((80, 1290, 480, 1390), WHITE, INK, 5, r=24)
    cv.text((280, 1357), "MITFLIEGEN", font(48), INK, "ms")
    cv.rect((520, 1290, 900, 1390), C["pink"], INK, 5, r=24)
    cv.text((710, 1357), "FLIEHEN", font(48), WHITE, "ms")


SCENES = [s_wake, s_alone, s_radio, s_run, s_zombies, s_pass, s_pass, s_stadium, s_tablet, s_flashback, s_final]
PAUSE = 6


def render(i, t=0.5):
    cv = Canvas((30, 34, 42))
    SCENES[i](cv, t)
    img = cv.final()
    if i == 9:  # sepia flashback, sharp and readable
        g = img.convert("L")
        img = Image.merge("RGB", [g.point(lambda v: min(255, int(v * 1.07 + 10))), g, g.point(lambda v: int(v * 0.82))])
    return img


def hud(img, uhr, zombies, mensch):
    d = ImageDraw.Draw(img, "RGBA")
    y, x = 250, 50
    me = f"{mensch} %" if isinstance(mensch, int) else mensch
    chips = [("UHRZEIT", uhr, (255, 210, 80)), ("ZOMBIES", str(zombies), (150, 220, 120)),
             ("MENSCH", me, WHITE if isinstance(mensch, int) else C["pink"])]
    fl, fv = font(17, "Bold"), font(46, "Black")
    for label, val, col in chips:
        w = int(max(d.textlength(val, font=fv), d.textlength(label, font=fl))) + 34
        d.rounded_rectangle((x, y, x + w, y + 92), 10, fill=(14, 18, 22, 225), outline=(255, 255, 255, 60), width=2)
        d.text((x + 16, y + 10), label, font=fl, fill=(190, 196, 196))
        d.text((x + 16, y + 32), val, font=fv, fill=col)
        x += w + 14
    return img


insert = S4.insert
