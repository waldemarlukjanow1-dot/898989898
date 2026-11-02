"""Clear, readable scenes for 'AM STEUER'. Simple motion, recognizable places, jointed figures."""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "bankraub"))
import scenes as S  # noqa: E402
from scenes import Canvas, font, mono, W, H  # noqa: E402
import rig  # noqa: E402
from rig import Look, figure, name_tag  # noqa: E402

INK = rig.INK
WHITE = rig.WHITE
C = dict(S.C)
C.update({"red_j": (200, 50, 55), "green_j": (60, 145, 85), "blue_u": (52, 84, 160), "grey_h": (110, 116, 124),
          "van": (232, 234, 236), "truck": (120, 134, 150), "road": (62, 66, 74), "walk": (140, 140, 146)})

DU_MASK = Look(jacket=C["red_j"], mask=True, name="DU")
DU = Look(jacket=C["red_j"], hair=(40, 30, 26), name="DU")
LEON = Look(jacket=C["green_j"], hat=(40, 100, 60), name="LEON · DEIN BRUDER")
GUARD = Look(jacket=C["blue_u"], pants=(40, 50, 90), hat=(36, 56, 120), hat_kind="guard", name="WACHMANN")
KOMPLIZE = Look(jacket=C["grey_h"], mask=True)


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def seg(t, a, b):
    return max(0.0, min(1.0, (t - a) / (b - a)))


# ------------------------------------------------------------------ environment

def sky(cv, top=(44, 60, 104), bottom=(236, 150, 104), y1=1000):
    for y in range(0, y1, 6):
        k = y / y1
        cv.rect((0, y, W, y + 6), tuple(int(top[i] + (bottom[i] - top[i]) * k) for i in range(3)))


def street(cv, y=1180):
    cv.rect((0, y - 40, W, y), C["walk"], INK, 3)          # sidewalk
    cv.rect((0, y, W, H), C["road"])
    for k in range(7):
        cv.rect((k * 180 - 20, y + 170, k * 180 + 80, y + 186), (230, 226, 210))


def house(cv, x, w, h, col, y=1140, roof=(120, 60, 50), sign=None, lit=(), door=True):
    cv.rect((x, y - h, x + w, y), col, INK, 4)
    cv.poly([(x - 14, y - h), (x + w / 2, y - h - 90), (x + w + 14, y - h)], roof, INK, 4)
    rows = int((h - 120) // 120)
    for r_ in range(rows):
        for c_ in range(int(w // 110)):
            wx = x + 30 + c_ * 110
            wy = y - h + 40 + r_ * 120
            on = (r_ * 7 + c_) in lit
            cv.rect((wx, wy, wx + 60, wy + 76), (250, 214, 130) if on else (70, 88, 110), INK, 3)
            cv.line([(wx + 30, wy), (wx + 30, wy + 76)], INK, 2)
    if door:
        cv.rect((x + w / 2 - 38, y - 130, x + w / 2 + 38, y), (90, 60, 44), INK, 4)
        cv.circle(x + w / 2 + 22, y - 65, 6, (230, 190, 70))
    if sign:
        f = font(34, "Black")
        cv.rect((x + 18, y - 200, x + w - 18, y - 146), (250, 246, 236), INK, 3, r=6)
        cv.text((x + w / 2, y - 160), sign, f, INK, "ms")


def houses(cv, y=1140):
    house(cv, -40, 300, 520, (196, 170, 140), y, sign="BÄCKEREI", lit=(0, 8))
    house(cv, 270, 260, 620, (150, 172, 190), y, roof=(80, 70, 90), lit=(1, 7))
    house(cv, 540, 300, 480, (210, 196, 170), y, sign="APOTHEKE", lit=(2,))
    house(cv, 850, 280, 580, (170, 150, 170), y, roof=(90, 60, 70), lit=(0, 9))


def lamp(cv, x, y=1140, camera=False):
    cv.rect((x - 8, y - 560, x + 8, y), (40, 44, 50))
    cv.rect((x - 8, y - 560, x + 90, y - 548), (40, 44, 50))
    cv.poly([(x + 60, y - 548), (x + 120, y - 548), (x + 104, y - 520), (x + 76, y - 520)], (40, 44, 50))
    cv.glow(x + 90, y - 520, 60, (255, 220, 150), 120)
    if camera:
        cv.rect((x - 70, y - 470, x - 8, y - 430), (30, 30, 34), INK, 3, r=6)
        cv.circle(x - 70, y - 450, 10, (20, 20, 24))
        cv.circle(x - 30, y - 462, 6, (230, 40, 40))


def wheel(cv, x, y, r, rot):
    cv.circle(x, y, r, (24, 24, 26))
    cv.circle(x, y, r * 0.5, (170, 170, 176), INK, 3)
    for k in range(4):
        a = rot + k * math.pi / 2
        cv.line([(x, y), (x + math.cos(a) * r * 0.45, y + math.sin(a) * r * 0.45)], INK, 4)


def truck(cv, x, y, s=1.0, rot=0.0):
    """Armoured cash transporter, side view, facing right. (x, y) = rear-bottom."""
    L, Hh = 620 * s, 330 * s
    cv.rect((x, y - Hh - 40 * s, x + L * 0.72, y - 40 * s), C["truck"], INK, 5, r=int(14 * s))
    cv.rect((x + L * 0.72, y - Hh * 0.78 - 40 * s, x + L, y - 40 * s), C["truck"], INK, 5, r=int(30 * s))
    cv.rect((x + L * 0.78, y - Hh * 0.7 - 40 * s, x + L * 0.95, y - Hh * 0.38 - 40 * s), (150, 190, 220), INK, 4)
    cv.rect((x + 30 * s, y - Hh * 0.62 - 40 * s, x + L * 0.66, y - Hh * 0.38 - 40 * s), (236, 200, 70), INK, 3)
    cv.text((x + L * 0.36, y - Hh * 0.43 - 40 * s), "GELDTRANSPORT", font(int(40 * s), "Black"), INK, "ms")
    for wx in (x + L * 0.2, x + L * 0.82):
        wheel(cv, wx, y - 30 * s, 52 * s, rot)


def van(cv, x, y, s=1.0, rot=0.0, driver=None, door_open=False, cases=0, facing=1):
    """White getaway van, side view. driver: Look drawn in the cab window."""
    L, Hh = 560 * s, 300 * s
    x0 = x
    body = (x0, y - Hh - 30 * s, x0 + L * 0.74, y - 30 * s)
    cab = (x0 + L * 0.74, y - Hh * 0.8 - 30 * s, x0 + L, y - 30 * s)
    if facing < 0:
        body = (x0 + L * 0.26, body[1], x0 + L, body[3])
        cab = (x0, cab[1], x0 + L * 0.26, cab[3])
    cv.rect(body, C["van"], INK, 5, r=int(16 * s))
    cv.rect(cab, C["van"], INK, 5, r=int(30 * s))
    cv.rect((body[0], body[3] - 70 * s, body[2], body[3] - 50 * s), (60, 110, 200))
    win = (cab[0] + 18 * s, cab[1] + 18 * s, cab[2] - 18 * s, cab[1] + Hh * 0.38)
    cv.rect(win, (160, 200, 228), INK, 4)
    if driver is not None:
        hx = (win[0] + win[2]) / 2
        p = rig.stand()
        rig.head(cv, hx, win[3] - 30 * s, 52 * s, driver, p, facing)
    if door_open:
        cv.rect((body[0] + 40 * s, body[1] + 30 * s, body[0] + 260 * s, body[3] - 10 * s), (40, 40, 44), INK, 4)
        for k in range(cases):
            cx = body[0] + 60 * s + (k % 2) * 100 * s
            cy = body[3] - 60 * s - (k // 2) * 70 * s
            cv.rect((cx, cy - 55 * s, cx + 90 * s, cy), (150, 150, 158), INK, 3, r=6)
    for wx in ((x0 + L * 0.2, x0 + L * 0.84) if facing > 0 else (x0 + L * 0.16, x0 + L * 0.8)):
        wheel(cv, wx, y - 22 * s, 46 * s, rot)


def warehouse(cv, gate=0.0, y=1140):
    cv.rect((60, 520, 1020, y), (150, 120, 96), INK, 5)
    cv.poly([(40, 520), (540, 420), (1040, 520)], (110, 86, 70), INK, 5)
    for k in range(10):
        cv.line([(80 + k * 96, 540), (80 + k * 96, y - 10)], (130, 102, 80), 3)
    cv.rect((300, 560, 780, 640), (250, 246, 236), INK, 4, r=8)
    cv.text((540, 620), "LAGERHALLE 7", font(56, "Black"), INK, "ms")
    gx0, gx1, gy0 = 340, 740, 700
    cv.rect((gx0, gy0, gx1, y), (30, 30, 34), INK, 4)
    gh = (y - gy0) * (1 - gate)
    cv.rect((gx0, gy0, gx1, gy0 + gh), (176, 180, 186), INK, 4)
    for k in range(int(gh // 40)):
        cv.line([(gx0, gy0 + k * 40), (gx1, gy0 + k * 40)], (140, 144, 150), 3)


def police(cv, x, y, s=1.0, phase=0.0, facing=1):
    L = 420 * s
    cv.rect((x, y - 150 * s, x + L, y - 30 * s), (240, 242, 244), INK, 5, r=int(26 * s))
    cv.poly([(x + L * 0.25, y - 150 * s), (x + L * 0.35, y - 230 * s), (x + L * 0.7, y - 230 * s),
             (x + L * 0.8, y - 150 * s)], (240, 242, 244), INK, 4)
    cv.rect((x, y - 110 * s, x + L, y - 80 * s), (40, 120, 90))
    cv.text((x + L / 2, y - 45 * s), "POLIZEI", font(int(34 * s), "Black"), (40, 120, 90), "ms")
    on = int(phase * 4) % 2 == 0
    cv.rect((x + L * 0.42, y - 252 * s, x + L * 0.5, y - 230 * s), (60, 110, 255) if on else (30, 50, 120))
    cv.rect((x + L * 0.5, y - 252 * s, x + L * 0.58, y - 230 * s), (30, 50, 120) if on else (60, 110, 255))
    if on:
        cv.glow(x + L * 0.46, y - 240 * s, 70 * s, (60, 110, 255), 150)
    for wx in (x + L * 0.2, x + L * 0.8):
        wheel(cv, wx, y - 22 * s, 40 * s, phase * 20)


def lying_guard(cv, x, y, nod=0.0, facing=1):
    cv.rect((x - 160, y - 70, x + 60, y - 10), C["blue_u"], INK, 4, r=28)
    cv.rect((x - 300, y - 55, x - 150, y - 15), (40, 50, 90), INK, 3, r=18)
    cv.ellipse((x - 340, y - 60, x - 290, y - 10), (24, 24, 26))
    hy = y - 50 - 40 * nod
    p = rig.Pose()
    rig.head(cv, x + 110, hy, 55, GUARD, p, 1)
    cv.circle(x + 40, y - 20, 18, WHITE, INK, 3)


# ------------------------------------------------------------------ scenes

def s_hook(cv, t):
    sky(cv)
    houses(cv)
    street(cv)
    lamp(cv, 990)
    van(cv, 760, 1330, 0.9, rot=0)
    tx = -700 + 740 * ease(t / 0.7)
    truck(cv, tx, 1300, 0.95, rot=-tx / 50)


def s_plan(cv, t):
    sky(cv)
    houses(cv)
    street(cv)
    van(cv, 420, 1330, 1.15, driver=LEON)
    name_tag(cv, 640, 860, "LEON · DEIN BRUDER", accent=C["green_j"])
    cv.line([(760, 918), (770, 990)], WHITE, 4)
    bx = -260 + 360 * ease(t)
    for k in range(2):
        figure(cv, bx + 30 + k * 190, 1540, 46, KOMPLIZE, rig.walk(t * 2.2 + k * 0.5))
    cv.rect((bx + 230, 1400, bx + 520, 1450), (230, 50, 50), INK, 4)
    for k in range(4):
        cv.rect((bx + 250 + k * 70, 1400, bx + 285 + k * 70, 1450), WHITE)
    cv.text((bx + 375, 1500), "GESPERRT", font(36, "Black"), WHITE, "ms")


def s_attack(cv, t):
    sky(cv)
    houses(cv)
    street(cv)
    truck(cv, -120, 1300, 0.95)
    lying_guard(cv, 380, 1480)
    lying_guard(cv, 700, 1600, nod=abs(math.sin(seg(t, 0.8, 1.0) * math.pi * 2)) if t > 0.8 else 0)
    x = 960 - 380 * ease(t / 0.5)
    pose = rig.run(t * 3) if t < 0.5 else rig.stand(t)
    figure(cv, x, 1430, 50, DU_MASK, pose, facing=-1)


def s_cases(cv, t):
    sky(cv)
    houses(cv)
    street(cv)
    vx = 560 + (900 * ease(seg(t, 0.62, 1.0)))
    van(cv, vx, 1360, 1.0, rot=vx / 40, door_open=t < 0.62, cases=min(4, int(t * 7) + 1))
    if t < 0.62:
        x = 120 + 360 * seg(t, 0, 0.6)
        figure(cv, x, 1560, 50, DU_MASK, rig.carry(t * 4))


def front_seat(cv, x, y, look, mood="neutral", mouth=0.0, mask_up=1.0, wheel_hands=False, blink=False):
    cv.rect((x - 130, y + 90, x + 130, y + 420), look.jacket, INK, 5, r=70)
    cv.rect((x - 40, y + 80, x + 40, y + 130), look.jacket, INK, 4)
    p = rig.Pose(mood=mood, mouth=mouth, blink=blink)
    plain = Look(jacket=look.jacket, hair=look.hair, hat=look.hat, hat_kind=look.hat_kind)
    rig.head(cv, x, y, 110, plain, p, 0)
    if mask_up < 1.0:  # balaclava, partly pulled up
        top = y - 112
        bottom = y + 112 - 224 * mask_up
        cv.d.chord(cv.s((x - 112, top - 0, x + 112, top + 224)), 180, 360, fill=(34, 34, 38))
        cv.rect((x - 112, top + 100, x + 112, max(top + 100, bottom)), (34, 34, 38))
        if mask_up < 0.3:
            cv.rect((x - 70, y - 25, x + 70, y + 20), WHITE, r=10)
            cv.ellipse((x - 45, y - 18, x - 25, y + 14), INK)
            cv.ellipse((x + 25, y - 18, x + 45, y + 14), INK)
    if wheel_hands:
        cv.circle(x - 80, y + 300, 26, WHITE, INK, 3)
        cv.circle(x + 80, y + 300, 26, WHITE, INK, 3)


def van_inside(cv, t, road_shift=0.0, camera=True, turn=0.0):
    sky(cv, (60, 80, 130), (240, 170, 120), 900)
    houses(cv, 900)
    cv.rect((0, 900, W, H), C["road"])
    for k in range(6):
        y = 930 + k * 80
        cv.rect((520 + turn * k * 40 - 10, y, 520 + turn * k * 40 + 10, y + 40), (230, 226, 210))
    if camera:
        lamp(cv, 820 - road_shift, 900, camera=True)
    # cab frame
    cv.rect((0, 0, W, 330), (40, 42, 48))
    cv.rect((0, 0, 70, H), (40, 42, 48))
    cv.rect((1010, 0, W, H), (40, 42, 48))
    cv.rect((0, 1300, W, H), (52, 54, 60))
    cv.rect((0, 1260, W, 1320), (70, 72, 80), INK, 4)


def s_mask(cv, t):
    van_inside(cv, t, road_shift=300 * t)
    front_seat(cv, 300, 1030, LEON, "calm", wheel_hands=True)
    cv.circle(300, 1330, 150, None, (24, 24, 26), 26)
    k = ease(seg(t, 0.1, 0.55))
    laugh = abs(math.sin(t * 18)) if t > 0.55 else 0
    front_seat(cv, 760, 1030, DU, "happy", mouth=laugh * 0.9, mask_up=k)


def s_phone(cv, t):
    cv.img.paste((36, 40, 48), (0, 0) + cv.img.size)
    cv.glow(540, 900, 520, (120, 160, 220), 70)
    cv.rect((300, 420, 780, 1420), (20, 20, 24), INK, 8, r=60)
    cv.rect((330, 470, 750, 1370), (236, 240, 246))
    cv.rect((330, 470, 750, 560), (210, 216, 226))
    cv.text((540, 530), "Unbekannt", font(40, "Black"), INK, "ms")
    cv.circle(380, 515, 26, (150, 150, 160))
    k = ease(seg(t, 0.25, 0.5))
    if k > 0:
        y = 700 + 60 * (1 - k)
        cv.rect((360, y, 720, y + 170), (225, 228, 234), INK, 3, r=30)
        cv.text((390, y + 40), "Danke fürs", font(46, "Bold"), INK)
        cv.text((390, y + 100), "Tragen.", font(46, "Bold"), INK)
    # hand
    cv.rect((640, 1330, 980, 1700), C["red_j"], INK, 6, r=60)
    cv.ellipse((600, 1290, 790, 1440), WHITE, INK, 6)
    cv.ellipse((270, 1180, 360, 1260), WHITE, INK, 5)


def s_four(cv, t):
    cv.img.paste((30, 34, 42), (0, 0) + cv.img.size)
    who = [("DU", Look(jacket=C["red_j"], hair=(40, 30, 26))), ("LEON", Look(jacket=C["green_j"], hat=(40, 100, 60))),
           ("KOMPLIZE 1", Look(jacket=C["grey_h"], hair=(80, 60, 40))), ("KOMPLIZE 2", Look(jacket=C["grey_h"], hair=(30, 30, 30)))]
    for k, (n, lk) in enumerate(who):
        x = 300 + (k % 2) * 400
        y = 640 + (k // 2) * 420
        cv.rect((x - 150, y - 180, x + 150, y + 220), (50, 56, 66), WHITE, 4, r=20)
        cv.rect((x - 90, y + 80, x + 90, y + 220), lk.jacket)
        rig.head(cv, x, y, 100, lk, rig.Pose(), 0)
        cv.text((x, y + 200), n, font(36, "Black"), WHITE, "ms")


def s_tracker(cv, t):
    cv.img.paste((44, 40, 38), (0, 0) + cv.img.size)
    cv.glow(540, 900, 520, (255, 230, 180), 60)
    # case base
    cv.rect((160, 820, 920, 1300), (150, 150, 158), INK, 6, r=24)
    cv.rect((190, 850, 890, 1270), (60, 60, 66))
    for k in range(5):
        S.cash_stack(cv, 220 + k * 130, 880, 120, 50)
        S.cash_stack(cv, 230 + k * 130, 950, 120, 50)
    k = ease(seg(t, 0.35, 0.7))
    if k > 0.3:  # money lifted -> tracker visible
        cv.rect((420, 1080, 660, 1220), (30, 30, 34), INK, 5, r=16)
        cv.rect((450, 1110, 600, 1140), (60, 200, 90))
        on = int(t * 6) % 2 == 0
        cv.circle(625, 1125, 16, (240, 40, 40) if on else (90, 20, 20))
        if on:
            cv.glow(625, 1125, 50, (240, 40, 40), 140)
        cv.line([(640, 1200), (720, 1250)], INK, 6)
    # lid swings open (from flat to upright)
    lh = 480 * (1 - 0.15) * k
    cv.rect((160, 820 - lh, 920, 830), (150, 150, 158), INK, 6, r=24)
    cv.rect((440, 800 - lh * 0.5, 640, 840 - lh * 0.5), (110, 110, 118), INK, 4, r=10)


def s_wrong(cv, t):
    van_inside(cv, t, camera=False, turn=-ease(t))
    front_seat(cv, 420, 1030, LEON, "smirk", wheel_hands=True, blink=0.48 < t < 0.52)
    cv.circle(420, 1330, 150, None, (24, 24, 26), 26)
    # sat-nav on the dashboard
    cv.rect((680, 1040, 960, 1250), (20, 20, 24), INK, 6, r=16)
    cv.rect((700, 1060, 940, 1230), (40, 70, 110))
    ang = -math.pi / 2 - ease(t) * math.pi * 0.6
    cx, cy = 820, 1150
    tip = (cx + math.cos(ang) * 70, cy + math.sin(ang) * 70)
    cv.line([(cx, cy), tip], (250, 80, 80), 16)
    cv.circle(tip[0], tip[1], 18, (250, 80, 80))


def s_warehouse(cv, t):
    sky(cv)
    warehouse(cv, gate=ease(seg(t, 0, 0.4)))
    street(cv)
    van(cv, -40, 1360, 1.0, driver=LEON)
    gx = 560 - 260 * ease(seg(t, 0.35, 0.9))
    pose = rig.walk(t * 3) if 0.35 < t < 0.9 else rig.stand(t)
    figure(cv, gx, 1340, 50, GUARD, pose, facing=-1)
    if t > 0.85:
        name_tag(cv, gx - 90, 930, "DER WACHMANN", accent=C["blue_u"])


def s_carry(cv, t):
    sky(cv)
    warehouse(cv, gate=1.0)
    street(cv)
    van(cv, -40, 1360, 1.0, driver=DU)
    figure(cv, 640, 1340, 50, GUARD, rig.stand(t), facing=-1)
    x = 360 + 220 * seg(t, 0, 1)
    figure(cv, x, 1400, 50, LEON, rig.carry(t * 3))
    # "never on camera": crossed-out camera icon
    cv.rect((820, 760, 960, 840), (30, 30, 34), INK, 4, r=10)
    cv.circle(830, 800, 18, (20, 20, 24))
    cv.line([(800, 740), (980, 860)], (230, 40, 40), 12)


def s_wanted(cv, t):
    cv.img.paste((30, 34, 42), (0, 0) + cv.img.size)
    cv.rect((90, 480, 990, 1460), (20, 22, 26), (120, 130, 140), 8, r=20)
    cv.rect((90, 480, 990, 550), (40, 120, 90))
    shots = [(130, 580), (560, 580), (130, 980), (560, 980)]
    for k, (x, y) in enumerate(shots):
        if t * 5 > k:
            cv.rect((x, y, x + 390, y + 340), (70, 80, 90), WHITE, 3)
            rig.head(cv, x + 195, y + 150, 80, DU, rig.Pose(mood="happy", mouth=0.6 if k % 2 else 0), 0)
            cv.rect((x + 120, y + 230, x + 270, y + 340), C["red_j"])
            cv.text((x + 14, y + 14), f"CAM {k * 3 + 2:02d}", mono(26), (255, 80, 80))
    if t > 0.85:
        k = ease(seg(t, 0.85, 0.95))
        cv.rect((180, 1340 - 30 * k, 900, 1450), (230, 40, 40, int(220 * k)), WHITE, 6, r=14)
        cv.text((540, 1425), "TATVERDÄCHTIG", font(78, "Black"), WHITE, "ms")


def s_final(cv, t):
    sky(cv, (40, 50, 90), (180, 120, 110))
    warehouse(cv, gate=0.0)
    street(cv)
    figure(cv, 540, 1170, 56, DU, rig.Pose(mood="shock", sh_n=-10, sh_f=10), facing=1)
    lx = -470 + 380 * ease(t / 0.6)
    rx = 1100 - 380 * ease(t / 0.6)
    police(cv, lx, 1560, 1.0, phase=t * 3)
    police(cv, rx, 1600, 1.0, phase=t * 3 + 0.5)
    cv.rect((70, 1290, 470, 1390), WHITE, INK, 5, r=24)
    cv.text((270, 1357), "FLIEHEN", font(50), INK, "ms")
    cv.rect((510, 1290, 900, 1390), C["pink"], INK, 5, r=24)
    cv.text((705, 1357), "LEON JAGEN", font(50), WHITE, "ms")


SCENES = [s_hook, s_plan, s_attack, s_cases, s_mask, s_phone, s_four, s_tracker, s_wrong, s_warehouse,
          s_carry, s_wanted, s_final]
PAUSE = 6


def render(i, t=0.5):
    cv = Canvas((30, 34, 42))
    SCENES[i](cv, t)
    return cv.final()


def hud(img, beute, vertrauen, verdacht):
    d = ImageDraw.Draw(img, "RGBA")
    y, x = 250, 50
    chips = [("BEUTE", f"€{beute:,}".replace(",", "."), WHITE if beute else (255, 90, 90)),
             ("VERTRAUEN · LEON", f"{vertrauen} %", WHITE if vertrauen > 40 else (255, 90, 90)),
             ("VERDACHT · DU", f"{verdacht} %", C["pink"])]
    fl, fv = font(17, "Bold"), font(46, "Black")
    for label, val, col in chips:
        w = int(max(d.textlength(val, font=fv), d.textlength(label, font=fl))) + 34
        d.rounded_rectangle((x, y, x + w, y + 92), 10, fill=(14, 18, 22, 225), outline=(255, 255, 255, 60), width=2)
        d.text((x + 16, y + 10), label, font=fl, fill=(190, 196, 196))
        d.text((x + 16, y + 32), val, font=fv, fill=col)
        x += w + 14
    return img


def insert(img, text, k=1.0):
    """Big, clear key-info insert under the HUD. k = pop-in progress 0..1."""
    if not text or k <= 0:
        return img
    d = ImageDraw.Draw(img, "RGBA")
    size = int(64 * (0.6 + 0.4 * ease(k)))
    f = font(size, "Black")
    w = d.textlength(text, font=f)
    cx, y = 490, 400
    d.rounded_rectangle((cx - w / 2 - 28, y, cx + w / 2 + 28, y + size + 36), 16,
                        fill=(250, 246, 236, int(240 * min(1, k * 2))), outline=(18, 22, 24), width=5)
    d.text((cx, y + 18), text, font=f, fill=(200, 30, 50), anchor="ma")
    return img
