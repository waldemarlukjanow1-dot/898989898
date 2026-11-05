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


UX = 500  # horizontal centre of the safe area (right side is covered by TikTok buttons)
PX0, PY0, PX1, PY1 = 170, 500, 830, 1160  # phone screen box (below the chip, above the caption)


def text_w(txt, f):
    return T.S.ImageFont.truetype(f.path, f.size).getlength(txt)


def phone(cv, title, battery=None):
    cv.rect((PX0 - 18, PY0 - 18, PX1 + 18, PY1 + 18), (24, 24, 30), INK, 6, r=46)
    cv.rect((PX0, PY0, PX1, PY1), (245, 247, 250))
    cv.rect((PX0, PY0, PX1, PY0 + 90), (230, 233, 240))
    cv.text((UX, PY0 + 60), title, font(38, "Black"), INK, "ms")
    if battery is not None:
        cv.rect((PX1 - 110, PY0 + 30, PX1 - 30, PY0 + 62), (20, 20, 24), INK, 3, r=6)
        cv.rect((PX1 - 106, PY0 + 34, PX1 - 106 + 72 * battery, PY0 + 58), RED)
        cv.rect((PX1 - 30, PY0 + 40, PX1 - 24, PY0 + 52), (20, 20, 24))


def chat(cv, msgs, battery=None):
    """msgs: [(side 'l'|'r', text, visible)] – bubbles stacked from the top, text measured and wrapped."""
    phone(cv, "Bester Freund", battery)
    f = font(38, "Bold")
    maxw = (PX1 - PX0) - 140
    y = PY0 + 120
    for side, txt, show in msgs:
        if not show:
            continue
        lines, cur = [], ""
        for w_ in txt.split():
            trial = (cur + " " + w_).strip()
            if text_w(trial, f) > maxw and cur:
                lines.append(cur)
                cur = w_
            else:
                cur = trial
        lines.append(cur)
        bw = max(text_w(l, f) for l in lines) + 56
        bh = 30 + 50 * len(lines)
        x0 = PX0 + 30 if side == "l" else PX1 - 30 - bw
        cv.rect((x0, y, x0 + bw, y + bh), (228, 231, 238) if side == "l" else (60, 140, 250), r=30)
        for k, l in enumerate(lines):
            cv.text((x0 + 28, y + 15 + k * 50), l, f, INK if side == "l" else WHITE)
        y += bh + 22


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


TV = (130, 490, 870, 1030)        # outer frame
TVS = (160, 520, 840, 1000)       # screen


def tv_screen(cv, t, dur, on=True):
    x0, y0, x1, y1 = TV
    sx0, sy0, sx1, sy1 = TVS
    cv.rect((x0, y0, x1, y1), (20, 20, 24), INK, 8, r=18)
    cv.rect((sx0, sy0, sx1, sy1), (40, 60, 110) if on else (8, 8, 12))
    cv.rect((UX - 30, y1, UX + 30, y1 + 40), (20, 20, 24))
    cv.rect((UX - 170, y1 + 40, UX + 170, y1 + 60), (20, 20, 24), r=8)
    if not on:
        return
    cv.glow(UX, (sy0 + sy1) / 2, 380, (120, 160, 255), 90)
    # studio: desk + anchor, centred in the screen
    T.character(cv, UX, sy1 - 60, 0.46, "worry" if t < 0.5 else "shock", "down",
                talk=abs(math.sin(t * dur * 9)), hoodie=(150, 60, 70), hair=(60, 40, 30))
    cv.rect((sx0 + 70, sy1 - 220, sx1 - 70, sy1 - 140), (90, 100, 140), INK, 4, r=10)
    # LIVE badge top-left, breaking-news bar at the bottom of the screen
    cv.rect((sx0 + 24, sy0 + 24, sx0 + 150, sy0 + 76), RED, r=8)
    cv.text((sx0 + 87, sy0 + 64), "LIVE", font(34, "Black"), WHITE, "ms")
    cv.rect((sx0, sy1 - 140, sx0 + 250, sy1 - 90), (255, 214, 10))
    cv.text((sx0 + 125, sy1 - 103), "EILMELDUNG", font(30, "Black"), INK, "ms")
    cv.rect((sx0, sy1 - 90, sx1, sy1), RED)
    cv.text(((sx0 + sx1) / 2, sy1 - 30), "SONNE NICHT AUFGEGANGEN", font(44, "Black"), WHITE, "ms")


def s_tv(cv, t, dur):
    dark_room(cv)
    tv_screen(cv, t, dur)


def s_blackout(cv, t, dur):
    if t < 0.3:
        dark_room(cv)
        tv_screen(cv, 1.0, dur, on=t < 0.15)
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
    cv.glow(UX, 1500, 420, PHONE_LIGHT, 90)
    chat(cv, [("l", "Geh auf keinen Fall raus.", t > 0.65)], battery=0.12)


def s_seen(cv, t, dur):
    cv.rect((0, 0, W, H), (8, 8, 14))
    cv.glow(UX, 1500, 420, PHONE_LIGHT, 90)
    chat(cv, [("l", "Geh auf keinen Fall raus.", True), ("r", "Warum?", t > 0.05),
              ("l", "Weil ich dich gerade gesehen habe.", t > 0.4),
              ("l", "Draußen. Vor deiner Tür.", t > 0.68)], battery=0.09)


def s_pause(cv, t, dur):
    cv.rect((0, 0, W, H), (8, 8, 14))
    lit_character(cv, CX, FEET, SCALE, "shock", "phone", strength=140)


def door(cv, x0=210, x1=790, shake=0.0, gap_feet=False):
    """Door below the chip (top 470) and centred on x=500."""
    cv.rect((x0 - 30 + shake, 470, x1 + 30 + shake, 1460), (40, 30, 26), INK, 6)
    cv.rect((x0 + shake, 500, x1 + shake, 1440), (110, 76, 54), INK, 6)
    for (a, b) in ((550, 900), (960, 1380)):
        cv.rect((x0 + 50 + shake, a, x1 - 50 + shake, b), (124, 86, 62), INK, 4)
    cv.circle((x0 + x1) / 2 + shake, 700, 16, (200, 190, 140), INK, 4)  # peephole
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
                bx, by = ((40, 760), (640, 600), (640, 1000))[k]
                cv.text((bx, by), "BUMM", font(90, "Black"), (255, 220, 80), "la")
        cv.glow(540, 600, 500, PHONE_LIGHT, 40)
    else:  # peephole view: empty dark corridor
        cv.rect((0, 0, W, H), (6, 6, 10))
        cv.circle(UX, 840, 380, (40, 44, 56))
        cv.poly([(UX - 230, 1150), (UX + 230, 1150), (UX + 95, 760), (UX - 95, 760)], (60, 56, 52))
        cv.rect((UX - 95, 600, UX + 95, 760), (24, 26, 34))
        cv.circle(UX, 840, 380, None, (6, 6, 10), 40)
        if t > 0.8:
            cv.text((UX, 1130), "NIEMAND DA.", font(60, "Black"), (255, 220, 80), "ms")


def s_call(cv, t, dur):
    cv.rect((0, 0, W, H), (8, 8, 14))
    if t < 0.32:
        cv.glow(UX, 800, 420, PHONE_LIGHT, 90)
        sh = 8 * math.sin(t * dur * 60)
        cv.rect((PX0 - 18 + sh, PY0 - 18, PX1 + 18 + sh, PY1 + 18), (24, 24, 30), INK, 6, r=46)
        cv.rect((PX0 + sh, PY0, PX1 + sh, PY1), (245, 247, 250))
        cv.text((UX + sh, PY0 + 90), "Eingehender Anruf", font(38, "Bold"), (120, 120, 130), "ms")
        cv.circle(UX + sh, PY0 + 260, 110, (190, 190, 200))
        cv.text((UX + sh, PY0 + 470), "Unbekannt", font(70, "Black"), INK, "ms")
        cv.circle(UX - 170 + sh, PY1 - 110, 60, (60, 200, 90))
        cv.circle(UX + 170 + sh, PY1 - 110, 60, RED)
    else:
        lit_character(cv, CX, FEET, SCALE, "worry", "head", strength=140, look=(-1, 0))
        k = ease(seg(t, 0.55, 0.62))
        if k > 0:
            cv.rect((UX - 280, 480, UX + 280, 660), (20, 20, 26, int(230 * k)), (120, 120, 140), 4, r=30)
            cv.text((UX, 550), "Mach die Tür", font(46, "Black"), (200, 210, 255), "ms")
            cv.text((UX, 620), "nicht auf …", font(46, "Black"), (200, 210, 255), "ms")


def s_voice(cv, t, dur):
    cv.rect((0, 0, W, H), (14, 14, 22))
    door(cv, gap_feet=t > 0.2)
    cv.glow(UX, 1450, 300, (255, 240, 200), int(90 * min(1, t * 3)))
    if t > 0.62:
        k = ease(seg(t, 0.62, 0.72))
        cv.rect((UX - 240, 860, UX + 240, 1040), (250, 250, 252, int(240 * k)), INK, 5, r=34)
        cv.text((UX, 930), "Bitte.", font(50, "Black"), INK, "ms")
        cv.text((UX, 1000), "Lass mich rein.", font(46, "Black"), INK, "ms")


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
    if i in (2, 3, 4, 5, 7, 8, 9, 10):  # screens, chats, doors: fixed framing, perfectly aligned
        z, cx, cy = 0.0, 500, 810
    else:
        z, cx, cy = 0.04 + 0.12 * ease(t), 540, 820
    img = T.camera(img, z, cx, cy)
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
