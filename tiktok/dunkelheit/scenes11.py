"""Scenes for 'TAG 1 DER DUNKELHEIT' (STIL 3). Dark world, but the character is always lit and readable."""
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "reich"))
sys.path.append(os.path.join(HERE, "..", "arbeiten"))
import style3 as T  # noqa: E402
from style3 import Canvas, font, mono, W, H, ease, seg, INK, WHITE, SKIN, YELLOW  # noqa: E402
import scenes9 as A  # noqa: E402

CX, FEET, SCALE = 540, 1720, 1.2
RED = (220, 40, 50)
PHONE_LIGHT = (150, 200, 255)


def blink_at(t, dur):
    return ((t * dur) % 2.6) < 0.1


def dark_room(cv, k=1.0):
    """Bedroom with a pitch-black window (no city lights, no moon)."""
    cv.rect((0, 0, W, H), (34, 38, 64))
    cv.rect((60, 120, 760, 900), (6, 6, 10), INK, 8)
    cv.line([(410, 120), (410, 900)], (40, 40, 50), 8)
    cv.rect((760, 100, 1020, 1000), (90, 40, 60), INK, 6)
    cv.rect((0, 1080, W, H), (60, 44, 36))
    cv.rect((0, 900, W, 1090), (40, 44, 80))
    cv.rect((-60, 880, 300, 1150), (40, 60, 120), INK, 7, r=20)
    cv.rect((-60, 820, 260, 910), (180, 180, 190), INK, 7, r=30)
    cv.overlay((0, 0, 8), int(90 * k))


def lit_character(cv, x, y, s, mood, arms="phone", glow=PHONE_LIGHT, strength=110, **kw):
    cv.glow(x + 60 * s, y - 760 * s, 330 * s, glow, strength)
    return T.character(cv, x, y, s, mood, arms, **kw)


def chat(cv, msgs, t0=0.0):
    A.phone_ui(cv, 140, 440, 940, 1060, "Bester Freund")
    y = 560
    for side, txt, show in msgs:
        if not show:
            continue
        f = font(36, "Bold")
        w = cv.d.textlength(txt, font=T.S.ImageFont.truetype(f.path, f.size * T.S.SS)) / T.S.SS + 50
        x0 = 170 if side == "l" else 910 - w
        cv.rect((x0, y, x0 + w, y + 90), (230, 233, 240) if side == "l" else (60, 140, 250), None, 0, r=28)
        cv.text((x0 + 25, y + 60), txt, f, INK if side == "l" else WHITE)
        y += 110


# ------------------------------------------------------------------ scenes (cv, t, dur)

def s_wake(cv, t, dur):
    dark_room(cv)
    cv.rect((30, 960, 300, 1060), (20, 20, 26), INK, 5, r=14)  # alarm clock on the bed side
    cv.text((165, 1038), "06:30", mono(70), (255, 80, 80), "ms")
    cv.glow(165, 1010, 200, (255, 80, 80), 90)
    lit_character(cv, 640, FEET, SCALE, "neutral" if t < 0.5 else "worry", "down", glow=(255, 120, 120),
                  blink=t < 0.15)


def s_window(cv, t, dur):
    dark_room(cv, 0.6)
    lit_character(cv, 420, FEET, SCALE, "shock", "head", strength=60, look=(0, -1))


def s_tv(cv, t, dur):
    dark_room(cv)
    cv.rect((160, 430, 920, 900), (20, 20, 24), INK, 8, r=16)
    cv.rect((185, 455, 895, 875), (40, 60, 110))
    cv.glow(540, 660, 380, (120, 160, 255), 100)
    T.character(cv, 540, 1060, 0.42, "worry" if t < 0.5 else "shock", "down", talk=abs(math.sin(t * dur * 9)),
                hoodie=(150, 60, 70), hair=(60, 40, 30))
    cv.rect((185, 790, 895, 875), RED)
    cv.text((540, 848), "SONNE NICHT AUFGEGANGEN", font(42, "Black"), WHITE, "ms")
    cv.rect((380, 900, 700, 930), (20, 20, 24))
    lit_character(cv, 540, FEET + 380, SCALE, "shock", "down", glow=(120, 160, 255), strength=80)


def s_blackout(cv, t, dur):
    if t < 0.3:
        s_tv(cv, 1.0, dur)
        cv.overlay((0, 0, 0), int(255 * seg(t, 0.15, 0.3)))
        return
    cv.rect((0, 0, W, H), (6, 6, 10))
    k = ease(seg(t, 0.35, 0.7))
    cv.glow(CX + 90, 1000, 360 * k + 1, PHONE_LIGHT, int(150 * k))
    if k > 0.05:
        T.character(cv, CX, FEET, SCALE, "shock", "phone")
        cv.overlay((0, 0, 0), int(170 * (1 - k)))


def s_battery(cv, t, dur):
    cv.rect((0, 0, W, H), (8, 8, 14))
    lit_character(cv, CX, FEET + 230, SCALE, "worry", "down", strength=140)
    chat(cv, [("l", "Geh auf keinen Fall raus.", t > 0.65)])
    cv.rect((790, 470, 900, 510), (20, 20, 24), INK, 3, r=6)
    cv.rect((794, 474, 794 + 100 * 0.12, 506), RED)


def s_seen(cv, t, dur):
    cv.rect((0, 0, W, H), (8, 8, 14))
    lit_character(cv, CX, FEET + 230, SCALE, "shock" if t > 0.7 else "worry", "down", strength=140)
    chat(cv, [("l", "Geh auf keinen Fall raus.", True), ("r", "Warum?", t > 0.05),
              ("l", "Weil ich dich gerade", t > 0.4), ("l", "gesehen habe.", t > 0.45),
              ("l", "Draußen. Vor deiner Tür.", t > 0.68)])


def s_pause(cv, t, dur):
    cv.rect((0, 0, W, H), (8, 8, 14))
    lit_character(cv, CX, FEET, SCALE, "shock", "phone", strength=140)


def door(cv, x0=240, x1=840, shake=0.0, gap_feet=False):
    cv.rect((x0 - 30 + shake, 300, x1 + 30 + shake, 1460), (40, 30, 26), INK, 6)
    cv.rect((x0 + shake, 330, x1 + shake, 1440), (110, 76, 54), INK, 6)
    for (a, b) in ((380, 820), (900, 1360)):
        cv.rect((x0 + 50 + shake, a, x1 - 50 + shake, b), (124, 86, 62), INK, 4)
    cv.circle((x0 + x1) / 2 + shake, 600, 16, (200, 190, 140), INK, 4)  # peephole
    cv.circle(x1 - 60 + shake, 920, 22, (210, 180, 90), INK, 4)
    if gap_feet:  # light under the door + two white sneakers, exactly like yours
        cv.rect((x0 + shake, 1440, x1 + shake, 1460), (255, 240, 200))
        for sx in (-1, 1):
            cv.ellipse(((x0 + x1) / 2 + sx * 90 - 80, 1442, (x0 + x1) / 2 + sx * 90 + 80, 1462), WHITE)


def s_knock(cv, t, dur):
    if t < 0.55:
        cv.rect((0, 0, W, H), (14, 14, 22))
        hits = [0.22, 0.31, 0.40]
        sh = 0.0
        for h in hits:
            if 0 <= t - h < 0.05:
                sh = 14 * math.sin((t - h) * 400)
        door(cv, shake=sh)
        for k, h in enumerate(hits):
            if t > h:
                bx, by = ((60, 900), (700, 720), (690, 1100))[k]
                cv.text((bx, by), "BUMM", font(90, "Black"), (255, 220, 80), "la")
        cv.glow(540, 600, 500, PHONE_LIGHT, 40)
    else:  # peephole view: empty dark corridor
        cv.rect((0, 0, W, H), (6, 6, 10))
        cv.circle(540, 900, 450, (40, 44, 56))
        cv.poly([(300, 1260), (780, 1260), (640, 820), (440, 820)], (60, 56, 52))
        cv.rect((440, 640, 640, 820), (24, 26, 34))
        cv.circle(540, 900, 450, None, (6, 6, 10), 40)
        if t > 0.8:
            cv.text((540, 1460), "NIEMAND DA.", font(60, "Black"), (255, 220, 80), "ms")


def s_call(cv, t, dur):
    cv.rect((0, 0, W, H), (8, 8, 14))
    if t < 0.32:
        lit_character(cv, CX, FEET + 230, SCALE, "shock", "down", strength=140)
        sh = 8 * math.sin(t * dur * 60)
        A.phone_ui(cv, 280 + sh, 460, 800 + sh, 1060, "Eingehender Anruf")
        cv.circle(540 + sh, 650, 90, (190, 190, 200))
        cv.text((540 + sh, 820), "Unbekannt", font(60, "Black"), INK, "ms")
        cv.circle(400 + sh, 960, 50, (60, 200, 90))
        cv.circle(680 + sh, 960, 50, RED)
    else:
        lit_character(cv, CX, FEET, SCALE, "worry", "head", strength=140, look=(-1, 0))
        k = ease(seg(t, 0.55, 0.62))
        if k > 0:
            cv.rect((90, 470, 620, 640), (20, 20, 26, int(230 * k)), (120, 120, 140), 4, r=30)
            cv.text((355, 535), "Mach die Tür", font(44, "Black"), (200, 210, 255), "ms")
            cv.text((355, 600), "nicht auf …", font(44, "Black"), (200, 210, 255), "ms")


def s_voice(cv, t, dur):
    cv.rect((0, 0, W, H), (14, 14, 22))
    door(cv, gap_feet=t > 0.2)
    cv.glow(540, 1450, 300, (255, 240, 200), int(90 * min(1, t * 3)))
    if t > 0.62:
        k = ease(seg(t, 0.62, 0.72))
        cv.rect((300, 860, 780, 1040), (250, 250, 252, int(240 * k)), INK, 5, r=34)
        cv.text((540, 930), "Bitte.", font(50, "Black"), INK, "ms")
        cv.text((540, 1000), "Lass mich rein.", font(46, "Black"), INK, "ms")


def s_final(cv, t, dur):
    cv.rect((0, 0, W, H), (14, 14, 22))
    door(cv, 460, 1000, gap_feet=True)
    cv.glow(730, 1450, 260, (255, 240, 200), 80)
    lit_character(cv, 330, FEET + 40, SCALE * 0.9, "shock", "phone", strength=150, look=(1, 0))
    for (x0, x1), lab, bg, fg in (((60, 480), "AUFMACHEN", RED, WHITE), ((520, 920), "ZULASSEN", WHITE, INK)):
        cv.rect((x0, 1330, x1, 1440), bg, INK, 6, r=28)
        cv.text(((x0 + x1) / 2, 1405), lab, font(52, "Black"), fg, "ms")


SCENES = [s_wake, s_window, s_tv, s_blackout, s_battery, s_seen, s_pause, s_knock, s_call, s_voice, s_final]
PAUSE = 6


def render(i, t=0.5, dur=5.0):
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur)
    img = cv.final()
    z = 0.04 + 0.12 * ease(t)
    if i in (2, 4, 5, 7, 8, 9, 10):
        z = 0.02 + 0.05 * ease(t)
    img = T.camera(img, z, 540, 820)
    if i == PAUSE:
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, t):
    from script import SEQ
    return SEQ[i]["chip"]
