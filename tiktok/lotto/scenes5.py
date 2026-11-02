"""Clear scenes for 'DER SCHEIN'. Reuses rig + environment helpers from ../geldtransporter."""
import math
import os
import random
import sys

from PIL import ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "geldtransporter"))
sys.path.append(os.path.join(HERE, "..", "bankraub"))
import scenes4 as S4  # noqa: E402
from scenes4 import S, Canvas, font, mono, W, H, ease, seg, sky, street, house, lamp, wheel  # noqa: E402,F401
import rig  # noqa: E402
from rig import Look, figure, name_tag  # noqa: E402

INK, WHITE = rig.INK, rig.WHITE
C = dict(S4.C)
C.update({"teal_h": (40, 150, 160), "purple": (120, 70, 140), "wall": (214, 200, 178), "wall2": (180, 196, 206),
          "floor": (150, 110, 80), "night_wall": (70, 76, 100)})

DU = Look(jacket=C["red_j"], hair=(70, 45, 30), name="DU")
MARCO = Look(jacket=C["teal_h"], hair=(25, 25, 28), name="MARCO · BESTER FREUND")
CLERK = Look(jacket=C["purple"], hair=(150, 80, 40), name="LOTTO-ZENTRALE")
NUMBERS = [7, 12, 19, 23, 31, 42]


def room(cv, wall, floor_y=1260, floor=None, night=False):
    cv.rect((0, 0, W, floor_y), wall)
    cv.rect((0, floor_y, W, H), floor or C["floor"])
    cv.rect((0, floor_y - 24, W, floor_y), tuple(int(c * 0.8) for c in wall), INK, 3)
    for k in range(8):
        cv.line([(k * 150, floor_y), (k * 150 - 120, H)], tuple(int(c * 0.85) for c in (floor or C["floor"])), 3)
    if night:
        cv.overlay((20, 26, 60), 70)


def window(cv, x, y, w, h, night=False, rain=False):
    cv.rect((x, y, x + w, y + h), (40, 60, 110) if night else (150, 200, 235), INK, 6)
    cv.line([(x + w / 2, y), (x + w / 2, y + h)], INK, 5)
    cv.line([(x, y + h / 2), (x + w, y + h / 2)], INK, 5)
    if rain:
        rnd = random.Random(3)
        for _ in range(30):
            rx, ry = rnd.uniform(x + 10, x + w - 10), rnd.uniform(y + 10, y + h - 30)
            cv.line([(rx, ry), (rx + 4, ry + 24)], (200, 220, 240), 3)


def tv(cv, x, y, w, h, k):
    cv.rect((x, y, x + w, y + h), (24, 24, 28), INK, 6, r=14)
    cv.rect((x + 18, y + 18, x + w - 18, y + h - 18), (30, 60, 140))
    cv.text((x + w / 2, y + 80), "LOTTO 6 AUS 49", font(40, "Black"), (255, 220, 80), "ms")
    for i, n in enumerate(NUMBERS):
        bx = x + 60 + i * ((w - 120) / 6)
        by = y + 150
        cv.circle(bx + 30, by + 30, 38, (255, 230, 120), INK, 4)
        cv.text((bx + 30, by + 46), str(n), font(36, "Black"), INK, "ms")
        if k * 6 > i:
            cv.circle(bx + 30, by + 110, 24, (60, 200, 90), INK, 3)
            cv.line([(bx + 18, by + 110), (bx + 28, by + 120), (bx + 44, by + 98)], WHITE, 6)
    cv.rect((x + w / 2 - 20, y + h, x + w / 2 + 20, y + h + 60), (40, 40, 44))


def ticket(cv, x, y, s=1.0, rot_label="LOTTO"):
    cv.rect((x, y, x + 200 * s, y + 280 * s), (250, 246, 230), INK, 4, r=8)
    cv.rect((x, y, x + 200 * s, y + 50 * s), (230, 50, 60))
    cv.text((x + 100 * s, y + 38 * s), rot_label, font(int(30 * s), "Black"), WHITE, "ms")
    for r_ in range(4):
        for c_ in range(4):
            cv.rect((x + 20 * s + c_ * 44 * s, y + 70 * s + r_ * 44 * s, x + 50 * s + c_ * 44 * s,
                     y + 100 * s + r_ * 44 * s), (240, 220, 220), (200, 120, 120), 2)
    for k in range(12):
        cv.rect((x + 20 * s + k * 14 * s, y + 250 * s, x + 26 * s + k * 14 * s, y + 270 * s), INK)


def sofa(cv, x, y):
    cv.rect((x, y - 220, x + 560, y - 60), (90, 110, 150), INK, 5, r=40)
    cv.rect((x - 30, y - 140, x + 590, y), (100, 122, 166), INK, 5, r=30)
    cv.rect((x - 50, y - 200, x + 30, y), (90, 110, 150), INK, 5, r=30)
    cv.rect((x + 530, y - 200, x + 610, y), (90, 110, 150), INK, 5, r=30)


def door(cv, x, y_floor, open_=0.0):
    cv.rect((x, y_floor - 720, x + 330, y_floor), (120, 80, 56), INK, 6)
    cv.rect((x + 30, y_floor - 690, x + 300, y_floor - 380), (136, 92, 64), INK, 3)
    cv.rect((x + 30, y_floor - 350, x + 300, y_floor - 40), (136, 92, 64), INK, 3)
    cv.circle(x + 165, y_floor - 560, 14, (220, 200, 120), INK, 3)  # peephole
    cv.circle(x + 290, y_floor - 360, 16, (230, 190, 70), INK, 3)
    cv.rect((x - 20, y_floor - 10, x + 350, y_floor + 30), (110, 70, 60), INK, 3, r=6)  # doormat


def wet_shoes(cv, x, y, drip=0.0):
    cv.ellipse((x - 60, y + 40, x + 360, y + 110), (120, 170, 220, 160))
    for k in range(2):
        sx = x + k * 170
        cv.poly([(sx, y + 60), (sx + 10, y - 20), (sx + 80, y - 30), (sx + 160, y + 20), (sx + 160, y + 60)],
                (60, 50, 46), INK, 5)
        cv.rect((sx, y + 50, sx + 160, y + 70), WHITE, INK, 3)
        for d in range(3):
            dy = ((drip * 3 + d / 3) % 1.0) * 90
            cv.ellipse((sx + 40 + d * 40, y + 70 + dy, sx + 52 + d * 40, y + 88 + dy), (140, 190, 240))


def gas_station(cv, t):
    sky(cv, (14, 18, 40), (40, 46, 80), 900)
    cv.rect((0, 900, W, H), (52, 54, 60))
    cv.rect((60, 520, 1020, 580), (240, 240, 240), INK, 5)
    cv.text((540, 568), "TANKSTELLE", font(52, "Black"), (220, 40, 40), "ms")
    for x in (120, 960):
        cv.rect((x - 12, 580, x + 12, 960), (200, 200, 205), INK, 3)
    cv.glow(540, 760, 380, (255, 250, 220), 60)
    for x in (300, 700):
        cv.rect((x - 50, 760, x + 50, 960), (240, 60, 60), INK, 4, r=10)
        cv.rect((x - 34, 780, x + 34, 830), (40, 40, 44))
    cv.rect((80, 640, 260, 860), (30, 30, 34), INK, 4)
    for k, p in enumerate(("1,79", "1,89", "1,69")):
        cv.text((170, 700 + k * 60), p, mono(40), (255, 210, 60), "ms")
    cv.rect((760, 600, 1000, 960), (230, 220, 190), INK, 5)
    cv.text((880, 650), "KASSE", font(34, "Black"), INK, "ms")


def turning_head(cv, x, y, r, look, turn):
    """turn < 0.5 = back of head (hair), >= 0.5 = face towards camera."""
    if turn >= 0.5:
        rig.head(cv, x, y, r * 1.02, look, rig.Pose(mood="neutral"), 0)
    else:
        cv.circle(x, y, r * 1.02, look.hair, INK, 4)
        cv.circle(x + r * (0.9 - 1.6 * turn), y + 0.1 * r, r * 0.18, WHITE, INK, 3)  # ear moving round


# ------------------------------------------------------------------ scenes

def s_hook(cv, t):
    room(cv, C["wall2"])
    window(cv, 70, 330, 260, 300, night=True)
    tv(cv, 380, 420, 600, 360, ease(seg(t, 0, 0.6)))
    sofa(cv, 220, 1450)
    jump = math.sin(seg(t, 0.6, 1.0) * math.pi) * 120
    p = rig.Pose(mood="shock" if t < 0.6 else "happy", mouth=0.8 if t > 0.6 else 0,
                 sh_n=150 if t > 0.6 else 60, el_n=10, sh_f=150 if t > 0.6 else 20, hold="")
    hc = figure(cv, 470, 1430 - jump, 72, DU, p, facing=1)
    ticket(cv, 520, 760 - jump if t > 0.6 else 1100, 0.7)


def s_marco(cv, t):
    # left: you, right: Marco – split screen
    room(cv, C["wall2"])
    cv.rect((540, 0, W, H), C["wall"])
    cv.rect((532, 0, 548, H), INK)
    cv.rect((60, 330, 300, 470), (250, 246, 236), INK, 4)
    cv.text((180, 385), "MORGEN", font(30, "Black"), INK, "ms")
    cv.text((180, 445), "9:00 LOTTO", font(30, "Black"), (220, 40, 40), "ms")
    # coat hook with red jacket (clue)
    cv.rect((330, 360, 470, 380), (90, 60, 40))
    cv.poly([(340, 380), (460, 380), (480, 640), (320, 640)], C["red_j"], INK, 4)
    ticket(cv, 410, 420, 0.25)
    talk = abs(math.sin(t * 20))
    p1 = rig.Pose(sh_n=150, el_n=150, hold="phone", mood="happy", mouth=talk * 0.7 if t < 0.5 else 0)
    figure(cv, 270, 1440, 75, DU, p1, facing=1)
    p2 = rig.Pose(sh_n=150, el_n=150, hold="phone", mood="neutral", mouth=talk * 0.7 if t >= 0.5 else 0)
    figure(cv, 810, 1440, 75, MARCO, p2, facing=-1)
    name_tag(cv, 600, 640, "MARCO · BESTER FREUND", accent=C["teal_h"])


def s_note(cv, t):
    room(cv, C["night_wall"], night=True)
    door(cv, 560, 1260)
    if t < 0.45:
        x = 120 + 330 * ease(seg(t, 0, 0.4))
        figure(cv, x, 1330, 55, DU, rig.walk(t * 3) if t < 0.4 else rig.stand(), facing=1)
    else:  # peephole view: empty corridor through a fisheye circle
        cv.rect((0, 0, W, H), (10, 12, 20))
        cv.circle(540, 820, 420, (60, 66, 80))
        cv.poly([(300, 1100), (780, 1100), (640, 700), (440, 700)], (90, 80, 70))
        cv.rect((440, 560, 640, 700), (40, 44, 56))
        cv.circle(540, 820, 420, None, (10, 12, 20), 40)
        if t > 0.75:  # note on the doormat
            k = ease(seg(t, 0.75, 0.85))
            cv.rect((300, 1200, 780, 1500), (250, 246, 236, int(255 * k)), INK, 5, r=8)
            cv.text((540, 1380), "Gratuliere.", font(70, "Black"), INK, "ms")


def s_call(cv, t):
    room(cv, C["wall"])
    window(cv, 650, 340, 300, 330)
    talk = abs(math.sin(t * 22))
    p = rig.Pose(sh_n=150, el_n=150, hold="phone", mood="neutral", mouth=talk * 0.8)
    figure(cv, 430, 1500, 80, MARCO, p, facing=1)
    k = ease(seg(t, 0.35, 0.5))
    if k > 0:
        cv.rect((520, 720, 960, 900), (250, 250, 250), INK, 5, r=30)
        cv.poly([(560, 900), (620, 900), (560, 950)], (250, 250, 250), INK, 5)
        cv.text((740, 790), "Ich hab's", font(48, "Black"), INK, "ms")
        cv.text((740, 860), "keinem gesagt!", font(48, "Black"), INK, "ms")


def s_shoes(cv, t):
    room(cv, C["wall2"], floor_y=900, floor=(170, 150, 130))
    window(cv, 90, 520, 300, 300, rain=True)
    cv.circle(780, 680, 110, WHITE, INK, 6)
    cv.text((780, 705), "07:30", mono(56), INK, "ms")
    wet_shoes(cv, 300, 1000, drip=t)
    cv.rect((660, 1100, 860, 1160), (250, 246, 236), INK, 3)  # gas-station receipt (clue)
    cv.text((760, 1140), "TANKSTELLE", mono(22), INK, "ms")


def s_copy(cv, t):
    room(cv, (196, 206, 214), floor_y=1180, floor=(120, 126, 136))
    cv.rect((120, 540, 960, 630), (230, 50, 60), INK, 5, r=10)
    cv.text((540, 610), "LOTTO-ZENTRALE", font(60, "Black"), WHITE, "ms")
    figure(cv, 720, 1010, 55, CLERK, rig.Pose(sh_n=60, el_n=40, mood="neutral"), facing=-1)
    cv.rect((100, 960, 980, 1180), (160, 120, 90), INK, 6)  # counter
    cv.rect((420, 860, 640, 980), (30, 30, 34), INK, 4, r=10)
    bad = t > 0.45
    cv.rect((440, 880, 620, 960), (230, 40, 40) if bad else (60, 80, 120))
    cv.text((530, 935), "KOPIE" if bad else "...", font(40, "Black"), WHITE, "ms")
    ticket(cv, 230, 760, 0.6)
    if bad:
        cv.line([(220, 750), (360, 940)], (230, 40, 40), 10)
        cv.line([(360, 750), (220, 940)], (230, 40, 40), 10)


def s_jacket(cv, t):
    room(cv, C["night_wall"], night=True)
    cv.rect((380, 420, 700, 450), (90, 60, 40), INK, 3)
    cv.poly([(400, 450), (680, 450), (740, 1050), (340, 1050)], C["red_j"], INK, 6)
    cv.rect((560, 600, 680, 700), tuple(int(c * 0.8) for c in C["red_j"]), INK, 4)
    ticket(cv, 585, 520, 0.4)
    cv.text((850, 900), "?", font(260, "Black"), (255, 220, 80), "ms")


def s_monitor(cv, t, zoom=0.0, turn=0.0, show_face=False):
    room(cv, (196, 206, 214), floor_y=1180, floor=(120, 126, 136))
    m = 60 * zoom
    box = (90 - m, 520 - m, 990 + m, 1120 + m)
    cv.rect((box[0] - 20, box[1] - 20, box[2] + 20, box[3] + 20), (30, 30, 34), INK, 6, r=20)
    # gas station footage inside the monitor (drawn on a sub-canvas and pasted)
    sub = Canvas((10, 10, 10))
    gas_station(sub, t)
    walk_x = 380 + 240 * ease(seg(t, 0, 0.7)) if not show_face else 620
    if not show_face:
        p = rig.walk(t * 3) if t < 0.7 else rig.stand()
        hc = figure(sub, walk_x, 1000, 60, Look(jacket=C["red_j"], hair=(70, 45, 30)), p, facing=1)
        if turn > 0:
            turning_head(sub, hc[0], hc[1], 60, DU, turn)
    else:
        cv_face = sub
        cv_face.rect((360, 700, 760, 1200), C["red_j"], INK, 6, r=80)
        rig.head(cv_face, 560, 560, 170, DU, rig.Pose(mood="neutral"), 0)
    img = sub.final().crop((0, 420, W, 1320)).resize((int(box[2] - box[0]), int(box[3] - box[1])))
    cv.img.paste(img.resize((img.width * S.SS, img.height * S.SS)), (int(box[0] * S.SS), int(box[1] * S.SS)))
    cv.d = ImageDraw.Draw(cv.img, "RGBA")
    cv.text((box[0] + 20, box[1] + 50), "CAM 2 · 02:14", mono(34), (255, 80, 80))
    cv.circle(box[2] - 40, box[1] + 36, 14, (255, 60, 60))


def s_station(cv, t):
    s_monitor(cv, t)


def s_turn(cv, t):
    s_monitor(cv, 0.99, zoom=ease(t), turn=ease(seg(t, 0.2, 0.9)))


def s_you(cv, t):
    room(cv, (196, 206, 214), floor_y=1180, floor=(120, 126, 136))
    cv.rect((0, 0, 540, H), (30, 30, 34))
    cv.rect((40, 520, 500, 1120), (60, 64, 76), WHITE, 4)
    cv.rect((150, 880, 390, 1120), C["red_j"])
    rig.head(cv, 270, 760, 130, DU, rig.Pose(mood="neutral"), 0)
    cv.text((60, 570), "CAM 2 · 02:14", mono(28), (255, 80, 80))
    cv.rect((680, 880, 920, 1180), C["red_j"], INK, 5, r=60)
    rig.head(cv, 800, 760, 130, DU, rig.Pose(mood="shock"), 0)
    cv.text((800, 500), "JETZT", font(40, "Black"), INK, "ms")


def s_final(cv, t):
    room(cv, C["night_wall"], night=True)
    door(cv, 680, 1180)
    wet_shoes(cv, 160, 1060, drip=t)
    p = rig.Pose(mood="shock", sh_n=-8, sh_f=8)
    figure(cv, 520, 1170, 66, DU, p, facing=1)
    labels = [("ZWILLING", WHITE, INK), ("DOPPELGÄNGER", WHITE, INK), ("ICH", C["pink"], WHITE)]
    xs = [(60, 300), (320, 690), (710, 900)]
    for (lab, bg, fg), (x0, x1) in zip(labels, xs):
        cv.rect((x0, 1290, x1, 1390), bg, INK, 5, r=24)
        cv.text(((x0 + x1) / 2, 1357), lab, font(42), fg, "ms")


SCENES = [s_hook, s_marco, s_note, s_call, s_shoes, s_copy, s_jacket, s_station, s_turn, s_you, s_final]
PAUSE = 6


def render(i, t=0.5):
    cv = Canvas((30, 34, 42))
    SCENES[i](cv, t)
    return cv.final()


def hud(img, gewinn, vertrauen, erinnerung):
    d = ImageDraw.Draw(img, "RGBA")
    y, x = 250, 50
    er = f"{erinnerung} %" if isinstance(erinnerung, int) else erinnerung
    chips = [("GEWINN", f"€{gewinn:,}".replace(",", "."), WHITE if gewinn else (255, 90, 90)),
             ("VERTRAUEN · MARCO", f"{vertrauen} %", WHITE if vertrauen > 40 else (255, 90, 90)),
             ("ERINNERUNG", er, C["pink"])]
    fl, fv = font(17, "Bold"), font(46, "Black")
    for label, val, col in chips:
        w = int(max(d.textlength(val, font=fv), d.textlength(label, font=fl))) + 34
        d.rounded_rectangle((x, y, x + w, y + 92), 10, fill=(14, 18, 22, 225), outline=(255, 255, 255, 60), width=2)
        d.text((x + 16, y + 10), label, font=fl, fill=(190, 196, 196))
        d.text((x + 16, y + 32), val, font=fv, fill=col)
        x += w + 14
    return img


insert = S4.insert
