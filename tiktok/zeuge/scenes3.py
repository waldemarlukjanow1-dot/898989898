"""Scene set for 'DER ZEUGE' – interrogation noir. Builds on teil2/scenes2 (noir grade)."""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "teil2"))
sys.path.append(os.path.join(HERE, "..", "bankraub"))
import scenes2 as S2  # noqa: E402
from scenes2 import S, Canvas, head, body, font, mono, W, H, noir  # noqa: E402,F401

C = dict(S2.C)
C.update({"grey_coat": (128, 132, 136), "black_coat": (16, 16, 18), "lamp": (255, 214, 150),
          "mirror": (24, 30, 36), "skin": C["white"]})
INK = C["ink"]


def lamp_cone(cv, x, y, ang, length=1300, spread=380, alpha=70):
    """Hanging lamp with a soft light cone; ang in degrees (swing)."""
    a = math.radians(ang)
    ex, ey = x + math.sin(a) * length, y + math.cos(a) * length
    px, py = math.cos(a) * spread, -math.sin(a) * spread
    layer = Image.new("RGBA", cv.img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).polygon([(u * S.SS, v * S.SS) for u, v in [(x - 30, y), (x + 30, y), (ex + px, ey + py), (ex - px, ey - py)]],
                                  fill=C["lamp"] + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(30 * S.SS))
    cv.img.paste(layer, (0, 0), layer)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")
    cv.line([(x, 0), (x, y - 40)], (10, 10, 10), 5)
    cv.poly([(x - 70, y), (x + 70, y), (x + 40, y - 50), (x - 40, y - 50)], (30, 30, 30), INK, 3)
    cv.glow(x, y + 10, 70, C["lamp"], 200)
    return ex, ey


def mirror(cv, box, inner_light=False):
    cv.rect(box, C["mirror"], (60, 66, 72), 10)
    x0, y0, x1, y1 = box
    cv.poly([(x0 + 40, y0 + 20), (x0 + 110, y0 + 20), (x0 + 30, y1 - 20), (x0 + 10, y1 - 20)], (255, 255, 255, 18))
    if inner_light:  # clue: a lamp burning on the other side
        cv.glow(x1 - 120, y0 + 90, 40, C["lamp"], 90)


def table(cv, y=1180):
    cv.poly([(80, y), (1000, y), (1080, y + 260), (0, y + 260)], (36, 30, 24), INK, 4)


def coat_man(cv, x, y, r, coat, turn=0.0, gun=False, gloves=False):
    """Man seen from behind; turn 0..1 shows profile."""
    cv.rect((x - r * 1.5, y + r * 0.8, x + r * 1.5, y + r * 5.2), coat, INK, 5, r=int(r * 0.6))
    cv.rect((x - r * 0.4, y + r * 0.7, x + r * 0.4, y + r * 1.3), tuple(min(255, c + 20) for c in coat), INK, 4)
    cv.circle(x, y, r, (30, 26, 24))  # hair, back of head
    if turn > 0:
        cv.d.chord(cv.s((x - r, y - r, x + r, y + r)), -90, -90 + 180 * turn, fill=C["white"])
        if turn > 0.5:
            cv.ellipse((x + r * 0.45, y - r * 0.15, x + r * 0.62, y + r * 0.15), INK)
    if gun:
        hand = (40, 40, 44) if gloves else C["white"]
        cv.rect((x + r * 1.2, y + r * 1.4, x + r * 2.9, y + r * 1.9), coat, INK, 4, r=12)
        cv.circle(x + r * 2.9, y + r * 1.65, r * 0.3, hand, INK, 3)
        cv.rect((x + r * 3.0, y + r * 1.5, x + r * 3.8, y + r * 1.75), (20, 20, 20))


# ------------------------------------------------------------------ scenes

def z_room(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    mirror(cv, (120, 330, 960, 1000), inner_light=True)
    swing = 14 * math.sin(t * 7)
    lamp_cone(cv, 540, 360, swing, alpha=60)
    table(cv)
    head(cv, 540, 900, 130, "shock")
    cv.d.chord(cv.s((405, 755, 675, 1000)), 180, 360, fill=(34, 34, 40))
    cv.rect((395, 1030, 685, 1240), C["jacket"], INK, 5, r=60)
    cv.ellipse((380, 1170, 470, 1230), C["white"], INK, 4)
    cv.ellipse((610, 1170, 700, 1230), C["white"], INK, 4)


def z_kommissar(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    lamp_cone(cv, 540, 300, 4 * math.sin(t * 5), alpha=55)
    table(cv, 1100)
    # commissioner, back to camera, huge
    cv.circle(560, 760, 236, (120, 100, 70))  # rim light from the lamp
    cv.rect((204, 914, 916, 1500), (120, 100, 70), r=160)
    cv.circle(560, 766, 230, (10, 11, 13))
    cv.rect((210, 924, 910, 1500), (10, 11, 13), r=160)
    cv.glow(355, 790, 14, (255, 255, 255), 230)  # earpiece glint (clue)
    # hands + recorder
    cv.ellipse((260, 1150, 420, 1230), C["white"], INK, 4)
    cv.ellipse((660, 1150, 820, 1230), C["white"], INK, 4)
    cv.rect((470, 1130, 640, 1220), (30, 30, 34), INK, 4, r=12)
    if int(t * 6) % 2 == 0:
        cv.circle(500, 1160, 12, C["red"])
    cv.text((520, 1172), "REC", mono(26), C["red"])


def garage(cv, t, coat, ring=True, turn=0.0, gloves=False, flash=False, body_down=True):
    cv.img.paste((16, 20, 18), (0, 0) + cv.img.size)
    cv.poly([(0, 1200), (1080, 1200), (1080, 1920), (0, 1920)], (30, 34, 32))
    for k in range(4):
        x = 80 + k * 300
        cv.rect((x, 420, x + 90, 1250), (46, 52, 50), INK, 4)
    for k in range(3):
        on = (int(t * 23 + k * 5) % 9) != 0
        cv.rect((150 + k * 300, 360, 380 + k * 300, 384), (190, 230, 210) if on else (50, 60, 58))
        if on:
            cv.glow(265 + k * 300, 372, 140, (160, 230, 200), 50)
    cv.rect((800, 470, 1000, 560), (220, 190, 60), INK, 4)
    cv.text((900, 535), "EBENE 3", font(40), INK, "ms")
    coat_man(cv, 380, 760, 85, coat, turn=turn, gun=True, gloves=gloves)
    if flash:
        cv.glow(720, 920, 160, (255, 220, 140), 230)
    if body_down:
        cv.rect((640, 1300, 960, 1370), (40, 40, 44), INK, 4, r=30)
        cv.circle(980, 1330, 45, C["white"], INK, 4)
    if ring:
        cv.circle(560, 1420, 24, None, (230, 190, 70), 8)


def z_flash1(cv, t):
    garage(cv, t, C["grey_coat"], ring=True, flash=0.45 < t < 0.55)


def z_gloves(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    lamp_cone(cv, 540, 300, 0, alpha=60)
    # your shocked face in the background (blurred feel: smaller, darker)
    head(cv, 540, 560, 90, "shock")
    cv.d.chord(cv.s((450, 465, 630, 630)), 180, 360, fill=(34, 34, 40))
    table(cv, 820)
    # folder with crime-scene photo (clue: timestamp)
    cv.rect((140, 900, 620, 1280), (170, 150, 100), INK, 5, r=10)
    cv.rect((180, 940, 460, 1140), (40, 48, 46), INK, 3)
    cv.rect((240, 1050, 400, 1080), (60, 60, 64))
    cv.text((190, 1180), "23:41  TATORT", mono(30), INK)
    # hand with pen, stopped
    cv.ellipse((640, 1000, 860, 1130), C["white"], INK, 5)
    cv.line([(700, 1060), (900, 920)], (20, 20, 22), 14)
    cv.text((640, 1250), "Notruf: 23:52", mono(30), (200, 60, 60))


def z_look(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    mirror(cv, (420, 300, 1060, 1100), inner_light=True)
    lamp_cone(cv, 300, 280, 0, alpha=50)
    turn = min(1.0, t * 1.6)
    # commissioner profile turning toward the mirror
    cx, cy, r = 300, 820, 170
    cv.circle(cx, cy, r, C["white"], INK, 5)
    cv.d.chord(cv.s((cx - r, cy - r, cx + r, cy + r)), 90 + 90 * turn, 270 + 90 * turn, fill=(20, 18, 16))
    cv.ellipse((cx + r * 0.35 * turn, cy - 25, cx + r * 0.35 * turn + 36, cy + 25), INK)
    cv.rect((cx - 220, cy + 160, cx + 220, cy + 700), (14, 14, 18), r=120)
    cv.glow(cx + 175 if turn < 0.5 else cx - 175, cy + 10, 12, (255, 60, 60), 200)


def z_flash2(cv, t):
    garage(cv, t, C["black_coat"], ring=False, turn=min(0.7, t * 1.2), gloves=True)


def z_ear(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    cv.circle(540, 900, 520, (210, 206, 200))
    cv.ellipse((420, 640, 700, 1160), (190, 182, 176), INK, 8)
    cv.ellipse((480, 720, 640, 1080), (160, 150, 146), INK, 6)
    cv.circle(560, 900, 60, (24, 24, 26), INK, 5)
    on = (int(t * 14) % 3) != 0
    cv.circle(560, 900, 16, C["red"] if on else (60, 20, 20))
    if on:
        cv.glow(560, 900, 60, C["red"], 160)
    cv.line([(560, 960), (600, 1500)], (24, 24, 26), 8)
    layer = Image.new("RGBA", cv.img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rectangle(cv.s((0, 0, 300, H)), fill=(4, 5, 6, 230))
    cv.img.paste(layer, (0, 0), layer)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")


def z_mirror(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    mirror(cv, (90, 280, 990, 1420))
    # breath fog growing from the other side
    r = 120 + 260 * t
    layer = Image.new("RGBA", cv.img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(cv.s((560 - r, 820 - r * 0.7, 560 + r, 820 + r * 0.7)), fill=(200, 210, 215, 110))
    layer = layer.filter(ImageFilter.GaussianBlur(40 * S.SS))
    cv.img.paste(layer, (0, 0), layer)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")
    if t > 0.5:  # ring imprint
        cv.circle(640, 880, 26, None, (230, 230, 230, 120), 6)
    for k in range(4):  # finger marks
        if t > 0.7:
            cv.ellipse((500 + k * 40, 700, 524 + k * 40, 780), (230, 230, 230, 70))


def z_confession(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    lamp_cone(cv, 540, 260, 0, alpha=70)
    table(cv, 700)
    cv.poly([(220, 560), (860, 520), (900, 1240), (250, 1280)], (226, 220, 204), INK, 5)
    cv.text((560, 640), "GESTÄNDNIS", font(60, "Black"), INK, "ms")
    for k in range(7):
        y = 700 + k * 52
        cv.line([(300, y), (820, y - 6)], (120, 116, 108), 5)
    cv.text((310, 1090), "Name: ████████", font(40, "Bold"), INK)
    cv.line([(310, 1190), (820, 1180)], C["red"], 6)
    cv.text((310, 1230), "Unterschrift", font(26, "Bold"), C["red"])
    cv.line([(760, 1320), (940, 1080)], (20, 20, 22), 16)
    cv.ellipse((900, 1050, 960, 1110), C["white"], INK, 4)


def z_reveal(cv, t):
    cv.img.paste(C["void"], (0, 0) + cv.img.size)
    see = 0.25 < t < 0.75 or (int(t * 40) % 5 == 0)
    mirror(cv, (90, 280, 990, 1180))
    if see:  # the glass turns transparent: grey coat, ring, smile
        cv.rect((100, 290, 980, 1170), (40, 40, 38))
        cv.glow(540, 400, 260, C["lamp"], 120)
        cv.rect((300, 860, 780, 1170), C["grey_coat"], INK, 6, r=120)
        cv.rect((480, 840, 600, 920), (150, 154, 158), INK, 4)
        cv.circle(540, 700, 160, C["white"], INK, 6)
        cv.d.chord(cv.s((380, 540, 700, 860)), 180, 360, fill=(10, 10, 12))  # hat shadow over the eyes
        cv.rect((330, 575, 750, 615), (22, 22, 24), INK, 4, r=14)  # fedora brim
        cv.rect((420, 450, 660, 590), (22, 22, 24), INK, 4, r=30)  # crown
        cv.circle(485, 680, 9, (255, 255, 255))
        cv.circle(595, 680, 9, (255, 255, 255))
        cv.arc((420, 650, 660, 800), 25, 155, INK, 7)
        cv.circle(760, 1020, 24, None, (230, 190, 70), 8)
        cv.ellipse((700, 990, 800, 1060), C["white"], INK, 4)
    # choice buttons (inside safe zone)
    cv.rect((70, 1290, 520, 1390), C["white"], INK, 5, r=24)
    cv.text((295, 1357), "UNTERSCHREIBEN", font(44), INK, "ms")
    cv.rect((560, 1290, 900, 1390), C["pink"], INK, 5, r=24)
    cv.text((730, 1357), "SCHWEIGEN", font(44), C["white"], "ms")


SCENES = [z_room, z_kommissar, z_flash1, z_gloves, z_look, z_flash2, z_flash2, z_ear, z_mirror, z_confession, z_reveal]
FLASHBACKS = (2, 5)


def render(i, t=0.5):
    cv = Canvas(C["void"])
    SCENES[i](cv, t)
    return cv.final()


def hud(img, glaub, minute, puls, g_col=None):
    d = ImageDraw.Draw(img, "RGBA")
    y, x = 250, 50
    chips = [("GLAUBWÜRDIGKEIT", f"{glaub} %", g_col or (C["white"] if glaub > 30 else C["red"])),
             ("VERHÖR-MINUTE", minute, C["gold"]),
             ("PULS", f"{puls}", C["pink"])]
    fl, fv = font(17, "Bold"), font(46, "Black")
    for label, val, col in chips:
        w = int(max(d.textlength(val, font=fv), d.textlength(label, font=fl))) + 34
        d.rounded_rectangle((x, y, x + w, y + 92), 10, fill=(6, 8, 10, 215), outline=(255, 255, 255, 40), width=2)
        d.text((x + 16, y + 10), label, font=fl, fill=(170, 176, 176))
        d.text((x + 16, y + 32), val, font=fv, fill=col)
        x += w + 14
    return img
