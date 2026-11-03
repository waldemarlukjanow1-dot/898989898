"""Scenes for 'PATIENT NULL – Teil 2'. Same look as Teil 1 (reuses ../zombie/scenes6)."""
import math
import os
import sys

from PIL import ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "zombie"))
sys.path.append(os.path.join(HERE, "..", "lotto"))
sys.path.append(os.path.join(HERE, "..", "geldtransporter"))
sys.path.append(os.path.join(HERE, "..", "bankraub"))
import scenes6 as Z  # noqa: E402
from scenes6 import S, S4, S5, Canvas, font, mono, W, H, ease, seg, street, rig, figure, Look  # noqa: E402,F401

INK, WHITE, C = rig.INK, rig.WHITE, Z.C
DU, SOLDIER = Z.DU, Z.SOLDIER
LAB = Look(jacket=(245, 245, 240), hair=(70, 45, 30))


def buttons(cv, left, right, hl=None, k=1.0):
    for (x0, x1), lab, on in (((80, 480), left, hl == 0), ((520, 900), right, hl == 1)):
        bg = C["pink"] if on else WHITE
        if on:
            cv.glow((x0 + x1) / 2, 1340, 180, (255, 61, 127), int(120 * k))
        cv.rect((x0, 1290, x1, 1390), bg, INK, 5, r=24)
        cv.text(((x0 + x1) / 2, 1357), lab, font(44 if len(lab) > 10 else 48), WHITE if on else INK, "ms")


def lab_room(cv):
    S5.room(cv, (200, 214, 214), floor_y=1180, floor=(130, 140, 146))
    for k in range(3):
        cv.rect((80 + k * 330, 330, 340 + k * 330, 420), (230, 236, 236), INK, 3)


# ------------------------------------------------------------------ scenes

def s_recap(cv, t):
    Z.apoc_sky(cv)
    Z.stadium(cv)
    cv.rect((0, 1140, W, H), (90, 110, 80))
    Z.heli(cv, 700, 1050, 0.9, t)
    figure(cv, 820, 1250, 52, SOLDIER, rig.stand(t), facing=-1)
    if t < 0.45:
        figure(cv, 420, 1250, 58, DU, rig.Pose(mood="shock"), facing=-1)
        buttons(cv, "MITFLIEGEN", "FLIEHEN", hl=1, k=0.5 + 0.5 * math.sin(t * 30))
    else:
        x = 420 - 600 * seg(t, 0.45, 1.0)
        figure(cv, x, 1250, 58, DU, rig.run(t * 4), facing=-1)


def horde(cv, t, ux, base_x, n=7, spread=140, push=True, y=1330, r=50):
    for k in range(n):
        zx = base_x + k * spread
        if push:
            d = zx - ux
            if abs(d) < 190:
                zx += (190 - abs(d)) * (1 if d > 0 else -1) * 0.9
        lk = Z.ZOMBIE_LOOKS[k % 4]
        figure(cv, zx, y + (k % 2) * 60, r, lk, Z.zpose(t * 2 + k * 0.3), facing=-1)


def s_heli(cv, t):
    Z.apoc_sky(cv)
    S4.houses(cv)
    street(cv)
    hx = 200 + 300 * t
    Z.heli(cv, hx, 520, 0.6, t)
    layer_x = hx - 20
    cv.poly([(layer_x - 20, 560), (layer_x + 20, 560), (layer_x + 160, 1500), (layer_x - 160, 1500)], (255, 250, 200, 60))
    horde(cv, t, -999, 640, n=4, spread=120, push=False)
    x = 80 + 300 * seg(t, 0, 1)
    figure(cv, x, 1430, 58, DU, rig.run(t * 4), facing=1)


def s_wall(cv, t):
    Z.apoc_sky(cv)
    S4.houses(cv)
    street(cv)
    Z.heli(cv, 820 + 300 * t, 480 - 120 * t, 0.5 * (1 - 0.4 * t), t)
    ux = -40 + 1100 * seg(t, 0, 1)
    horde(cv, t, ux, 60, n=8, spread=130, push=True)
    figure(cv, ux, 1430, 58, DU, rig.run(t * 4), facing=1)


def s_labout(cv, t):
    Z.apoc_sky(cv)
    cv.rect((60, 480, 1020, 1140), (200, 206, 210), INK, 5)
    for r_ in range(3):
        for c_ in range(5):
            cv.rect((100 + c_ * 180, 640 + r_ * 90, 220 + c_ * 180, 700 + r_ * 90), (120, 160, 190), INK, 3)
    cv.rect((240, 530, 840, 610), (40, 120, 90), INK, 5, r=10)
    cv.text((540, 588), "BIOLABOR NORD", font(52, "Black"), WHITE, "ms")
    cv.rect((440, 900, 640, 1140), (150, 200, 220), INK, 5)
    for k in range(5):  # broken glass
        cv.line([(540, 1010), (440 + k * 50, 900 + (k % 2) * 80)], WHITE, 4)
    street(cv)
    x = 120 + 330 * ease(seg(t, 0, 0.85))
    p = rig.walk(t * 2, 0.6)
    p.lean = 18
    figure(cv, x, 1330, 60, DU, p, facing=1)


def laptop(cv, open_k=1.0, screen=None):
    cv.rect((100, 1060, 980, 1180), (150, 120, 90), INK, 5)  # desk
    cv.rect((260, 1010, 820, 1060), (60, 60, 66), INK, 4, r=8)  # base
    h = 520 * open_k
    cv.rect((260, 1010 - h, 820, 1010), (60, 60, 66), INK, 5, r=12)
    if open_k > 0.9:
        cv.rect((285, 1035 - h, 795, 985), (20, 24, 30))
        if screen:
            screen((285, 1035 - h, 795, 985))


def video_you(cv, box, t, talk=True, play=False, label="GESTERN 23:58"):
    x0, y0, x1, y1 = box
    cv.rect(box, (210, 220, 220))
    cx = (x0 + x1) / 2
    cv.rect((cx - 120, y1 - 140, cx + 120, y1), (245, 245, 240))
    rig.head(cv, cx, y1 - 220, 95, LAB, rig.Pose(mouth=abs(math.sin(t * 22)) * 0.8 if talk else 0), 0)
    cv.text((x0 + 16, y0 + 40), label, mono(26), (220, 40, 40))
    if play:
        cv.circle(cx, (y0 + y1) / 2, 60, (0, 0, 0, 140))
        cv.poly([(cx - 20, (y0 + y1) / 2 - 30), (cx - 20, (y0 + y1) / 2 + 30), (cx + 32, (y0 + y1) / 2)], WHITE)


def s_laptop(cv, t):
    lab_room(cv)
    k = ease(seg(t, 0, 0.35))
    laptop(cv, k, lambda b: video_you(cv, b, t, talk=False, play=True))


def s_video(cv, t):
    lab_room(cv)

    def scr(b):
        video_you(cv, b, t, talk=True)
        x0, y0, x1, y1 = b
        if t > 0.55:  # green ampoule held up
            cv.rect((x1 - 150, y1 - 260, x1 - 110, y1 - 120), (120, 220, 120), INK, 3, r=10)
            cv.circle(x1 - 130, y1 - 110, 22, WHITE, INK, 3)
    laptop(cv, 1.0, scr)


def s_cure(cv, t):
    lab_room(cv)

    def scr(b):
        video_you(cv, b, t, talk=True)
        x0, y0, x1, y1 = b
        k = ease(seg(t, 0.4, 0.6))
        if k > 0:
            dx, dy = x1 - 110, y0 + 150
            cv.poly([(dx, dy - 70 * k), (dx - 50 * k, dy + 20 * k), (dx + 50 * k, dy + 20 * k)], (220, 30, 40))
            cv.circle(dx, dy + 25 * k, 50 * k, (220, 30, 40))
            cv.rect((dx - 22 * k, dy + 5 * k, dx + 22 * k, dy + 45 * k), (80, 200, 100), WHITE, 3, r=8)
    laptop(cv, 1.0, scr)


def s_window(cv, t):
    lab_room(cv)
    cv.rect((120, 480, 960, 1120), (60, 70, 80), INK, 8)
    cv.rect((130, 490, 950, 1110), (170, 120, 100))
    for k in range(4):
        x = 230 + k * 200
        turn = ease(seg(t, 0.1 + k * 0.08, 0.5 + k * 0.08))
        lk = Z.ZOMBIE_LOOKS[k]
        cv.rect((x - 70, 900, x + 70, 1110), lk.jacket, INK, 4, r=30)
        if turn < 0.5:
            cv.circle(x, 820, 72, lk.hair, INK, 4)
        else:
            rig.head(cv, x, 820, 72, lk, rig.Pose(mood="zombie"), 0)
    cv.line([(540, 480), (540, 1120)], (60, 70, 80), 10)
    cv.line([(120, 800), (960, 800)], (60, 70, 80), 10)


def s_monitor(cv, t):
    lab_room(cv)
    cv.rect((140, 500, 940, 1100), (24, 24, 28), INK, 8, r=20)
    cv.rect((170, 530, 910, 1070), (20, 30, 40))
    on = int(t * 4) % 2 == 0
    cv.rect((170, 560, 910, 680), (220, 40, 40) if on else (140, 20, 20))
    cv.text((540, 640), "IMMUNITÄT LÄSST NACH", font(50, "Black"), WHITE, "ms")
    secs = 24 * 3600 - int(t * 6)
    cv.text((540, 880), f"{secs // 3600:02d}:{secs // 60 % 60:02d}:{secs % 60:02d}", mono(130), (255, 90, 90), "ms")
    cv.rect((240, 960, 840, 1000), (60, 60, 66))
    cv.rect((240, 960, 240 + 600 * 0.2, 1000), (220, 40, 40))


def s_final(cv, t):
    lab_room(cv)
    cv.rect((40, 480, 400, 1000), (60, 70, 80), INK, 8)
    cv.rect((50, 490, 390, 990), (170, 120, 100))
    for k in range(2):
        rig.head(cv, 130 + k * 160, 720, 60, Z.ZOMBIE_LOOKS[k], rig.Pose(mood="zombie"), 0)
        cv.rect((70 + k * 160, 790, 190 + k * 160, 990), Z.ZOMBIE_LOOKS[k].jacket, INK, 3, r=20)
    cv.rect((700, 460, 980, 1180), (120, 80, 56), INK, 6)
    cv.glow(840, 640, 160 + 30 * math.sin(t * 6), (255, 250, 210), 150)
    cv.rect((740, 520, 940, 760), (250, 250, 230), INK, 4)
    figure(cv, 540, 1180, 60, DU, rig.Pose(mood="shock", sh_n=-10, sh_f=10), facing=1)
    buttons(cv, "ZUM SOLDATEN", "ALLEIN")


SCENES = [s_recap, s_heli, s_wall, s_labout, s_laptop, s_video, s_video, s_cure, s_window, s_monitor, s_final]
PAUSE = 6


def render(i, t=0.5):
    cv = Canvas((30, 34, 42))
    SCENES[i](cv, t)
    return cv.final()


def hud(img, uhr, zombies, immun):
    d = ImageDraw.Draw(img, "RGBA")
    y, x = 250, 50
    im = f"{immun} %" if isinstance(immun, int) else immun
    chips = [("UHRZEIT", uhr, (255, 210, 80)), ("ZOMBIES", str(zombies), (150, 220, 120)),
             ("IMMUNITÄT", im, WHITE if isinstance(immun, int) and immun > 50 else (255, 90, 90))]
    fl, fv = font(17, "Bold"), font(46, "Black")
    for label, val, col in chips:
        w = int(max(d.textlength(val, font=fv), d.textlength(label, font=fl))) + 34
        d.rounded_rectangle((x, y, x + w, y + 92), 10, fill=(14, 18, 22, 225), outline=(255, 255, 255, 60), width=2)
        d.text((x + 16, y + 10), label, font=fl, fill=(190, 196, 196))
        d.text((x + 16, y + 32), val, font=fv, fill=col)
        x += w + 14
    return img


insert = Z.insert
