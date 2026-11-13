"""Scenes for '11 MILLIONEN IN DER WAND' (STIL 3, T.HERO). Du-Form, cued to the voice.

DU = T.HERO (striped jumper). VORMIETER = black hoodie, glasses, side parting (name tag on first appearance).
The flashback is sepia + label RÜCKBLENDE, sharp and readable."""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "vicecity"))
sys.path.append(os.path.join(HERE, "..", "reich"))
import style3 as T  # noqa: E402
from style3 import Canvas, font, W, H, ease, seg, INK, WHITE, YELLOW  # noqa: E402
from timing import PHRASES, TEMPO, seq_bounds  # noqa: E402

UX = 500
SS = T.S.SS
RED, GREEN, BLUE = (220, 40, 50), (40, 140, 70), (60, 120, 230)
MONEY, BAND = (110, 190, 100), (240, 236, 220)
BOUNDS, TOTAL = seq_bounds()
VORMIETER = dict(hoodie=(36, 36, 44), hair=(30, 30, 34), hair_style="side", specs=True)
SHOCK = 0.9
WALL = (560, 470, 1000, 1180)          # the hollow part of the wall


def cue(text, last=False):
    hits = [a / TEMPO for a, b, s, t in PHRASES if t.startswith(text)]
    return hits[-1] if last else hits[0]


def blink_at(ta):
    return (ta % 2.7) < 0.1


def hero(cv, x, y, s, mood, arms="down", **kw):
    return T.character(cv, x, y, s, mood, arms, **dict(T.HERO, **kw))


def vormieter(cv, x, y, s, mood, arms="down", **kw):
    return T.character(cv, x, y, s, mood, arms, **dict(VORMIETER, **kw))


def label(cv, x, y, text, bg=WHITE, fg=INK, size=46, k=1.0):
    if k <= 0:
        return
    f = font(int(size * (0.7 + 0.3 * ease(min(1, k)))), "Black")
    tw = cv.d.textlength(text, font=T.font(f.size, "Black"))
    cv.rect((x - tw / 2 - 28, y - f.size - 12, x + tw / 2 + 28, y + 22), bg, INK, 5, r=18)
    cv.text((x, y), text, f, fg, "ms")


def pop(ta, key, d=0.2):
    return seg(ta, cue(key), cue(key) + d) * 1.0


# ------------------------------------------------------------------ props
def bundle(cv, x, y, w=130, h=58):
    cv.rect((x - w / 2, y - h / 2, x + w / 2, y + h / 2), MONEY, INK, 4, r=6)
    cv.rect((x - 14, y - h / 2, x + 14, y + h / 2), BAND)
    for k in range(3):
        cv.line([(x - w / 2 + 8, y - h / 2 + 12 + k * 14), (x - 22, y - h / 2 + 12 + k * 14)], (90, 160, 80), 3)


def bundles(cv, box, k=1.0):
    """Wall cavity full of money bundles; k = how much of it is revealed (top to bottom)."""
    x0, y0, x1, y1 = box
    cv.rect(box, (120, 90, 60), INK, 6)
    rows = int((y1 - y0 - 20) / 66)
    cols = int((x1 - x0 - 10) / 140)
    for r in range(int(rows * k + 0.999)):
        for c in range(cols):
            bundle(cv, x0 + 75 + c * 140 + (35 if r % 2 else 0) * 0, y0 + 45 + r * 66)


def wallpaper(cv, x0=0, y0=0, x1=W, y1=1300, col=(214, 200, 230)):
    cv.rect((x0, y0, x1, y1), col)
    for x in range(int(x0) + 30, int(x1), 90):
        cv.line([(x, y0), (x, y1)], tuple(c - 14 for c in col), 10)


def room(cv, night=False):
    wallpaper(cv)
    if night:
        cv.overlay((20, 20, 60), 60)
    cv.rect((0, 1300, W, H), (150, 110, 80))
    cv.rect((0, 1290, W, 1320), (240, 236, 228), INK, 3)
    cv.rect((60, 520, 420, 900), (40, 50, 90) if night else (150, 200, 240), INK, 8)    # window
    cv.line([(240, 520), (240, 900)], INK, 6)
    cv.line([(60, 710), (420, 710)], INK, 6)
    if night:
        cv.circle(340, 600, 30, (250, 245, 210))


def cracks(cv, cx, cy, n=7, L=260):
    for k in range(n):
        a = k * 2 * math.pi / n + 0.3
        pts = [(cx, cy)]
        for j in range(1, 4):
            pts.append((cx + math.cos(a + 0.25 * (-1) ** j) * L * j / 3, cy + math.sin(a + 0.25 * (-1) ** j) * L * j / 3))
        cv.line(pts, INK, 7)


def drill(cv, x, y):
    cv.rect((x - 40, y - 40, x + 110, y + 20), (220, 120, 30), INK, 5, r=12)
    cv.rect((x - 30, y + 10, x + 20, y + 110), (60, 60, 70), INK, 5, r=10)
    cv.line([(x + 110, y - 10), (x + 190, y - 10)], (170, 170, 180), 10)


def frame_pic(cv, x, y):
    cv.rect((x - 110, y - 80, x + 110, y + 80), (190, 150, 70), INK, 6)
    cv.rect((x - 85, y - 55, x + 85, y + 55), (150, 210, 240))
    cv.poly([(x - 85, y + 55), (x - 20, y - 15), (x + 30, y + 30), (x + 60, y), (x + 85, y + 55)], (80, 160, 90))


def sticky(cv, x, y, lines, n):
    cv.poly([(x - 330, y - 260), (x + 330, y - 270), (x + 320, y + 280), (x - 320, y + 270)], (255, 236, 110), INK, 6)
    cv.rect((x - 60, y - 290, x + 60, y - 240), (200, 200, 190, 200))         # tape
    for k, (txt, col) in enumerate(lines[:n]):
        cv.text((x, y - 140 + k * 130), txt, font(64, "Black"), col, "ms")


def laptop(cv, x0, y0, x1, y1):
    cv.rect((x0 - 20, y0 - 20, x1 + 20, y1 + 20), (40, 42, 50), INK, 6, r=18)
    cv.rect((x0, y0, x1, y1), WHITE)
    cv.poly([(x0 - 80, y1 + 20), (x1 + 80, y1 + 20), (x1 + 40, y1 + 80), (x0 - 40, y1 + 80)], (70, 72, 80), INK, 5)


def money_bag(cv, x, y, s=1.0):
    cv.ellipse((x - 140 * s, y - 120 * s, x + 140 * s, y + 140 * s), (120, 90, 60), INK, 6)
    cv.rect((x - 50 * s, y - 170 * s, x + 50 * s, y - 100 * s), (120, 90, 60), INK, 5, r=10)
    cv.text((x, y + 50 * s), "€", font(int(130 * s), "Black"), YELLOW, "ms")


def key_icon(cv, x, y, s=1.0):
    cv.circle(x, y, 40 * s, YELLOW, INK, 5)
    cv.circle(x, y, 14 * s, (200, 170, 40))
    cv.rect((x + 30 * s, y - 10 * s, x + 170 * s, y + 10 * s), YELLOW, INK, 4)
    for k in range(2):
        cv.rect((x + (120 + k * 30) * s, y + 10 * s, x + (136 + k * 30) * s, y + 40 * s), YELLOW, INK, 3)


def door(cv, x0, y0, x1, y1, peephole=True):
    cv.rect((x0 - 20, y0 - 20, x1 + 20, y1), (230, 225, 215), INK, 6)
    cv.rect((x0, y0, x1, y1), (140, 95, 60), INK, 6)
    cv.rect((x0 + 40, y0 + 60, x1 - 40, y0 + 420), (125, 85, 55), INK, 4)
    cv.rect((x0 + 40, y0 + 480, x1 - 40, y1 - 60), (125, 85, 55), INK, 4)
    cv.circle(x1 - 50, (y0 + y1) / 2 + 40, 20, YELLOW, INK, 4)
    if peephole:
        cv.circle((x0 + x1) / 2, y0 + 250, 18, (30, 30, 40), INK, 4)


# ------------------------------------------------------------------ scenes (cv, t, dur, ta)
def s_hook(cv, t, dur, ta):
    if ta < SHOCK:   # shock: the wall bursts open, money everywhere
        room(cv)
        bundles(cv, WALL)
        cracks(cv, 780, 820, 9, 380)
        cv.overlay((255, 255, 255), int(160 * max(0, 1 - ta / 0.3)))
        T.falling_money(cv, ta * 0.4, n=18, seed=3, area=(0, 300, W, 1600))
        label(cv, UX, 640, "11.000.000 €", GREEN, YELLOW, 80, k=seg(ta, 0, 0.2) * 1.0)
        return
    room(cv, night=ta >= cue("Und du schläfst"))
    # x-ray look into the wall
    bundles(cv, WALL)
    cv.rect(WALL, None, YELLOW, 8)
    label(cv, 780, 1380, "IN DER WAND", YELLOW, INK, 40)
    if ta < cue("Und du schläfst"):
        hero(cv, 280, 1760, 0.85, "shock", "down", blink=blink_at(ta), look=(1, 0))
    else:                                       # you sleep right next to it
        cv.rect((20, 1180, 540, 1440), (240, 240, 250), INK, 6, r=30)
        cv.rect((20, 1120, 180, 1200), WHITE, INK, 5, r=20)
        cv.circle(130, 1090, 90, T.SKIN, INK, 6)
        cv.d.chord(cv.s((40, 995, 220, 1110)), 180, 360, fill=(36, 26, 20))
        cv.arc((80, 1070, 120, 1100), 20, 160, INK, 5)
        cv.arc((150, 1070, 190, 1100), 20, 160, INK, 5)
        cv.rect((180, 1140, 540, 1320), (40, 90, 60), INK, 6, r=24)
        for j in range(3):
            ph = (ta * 0.6 + j / 3) % 1
            cv.text((240 + 40 * j + 30 * ph, 980 - 150 * ph), "Z", font(50 + 15 * j, "Black"), (60, 80, 160), "ms")
        label(cv, 280, 640, "SEIT 3 JAHREN", WHITE, INK, 44, k=pop(ta, "Und du schläfst"))


def s_drill(cv, t, dur, ta):
    room(cv)
    hero(cv, 300, 1760, 0.85, "neutral" if ta < cue("Die Wand") else ("worry" if ta < cue("Und plötzlich") else "shock"),
         "point", blink=blink_at(ta))
    hole = (780, 900)
    if ta < cue("Die Wand"):
        frame_pic(cv, 780, 760)
        cv.circle(hole[0], hole[1] - 240, 8, (120, 120, 130), INK, 3)       # nail
    if ta >= cue("Die Wand"):
        label(cv, 780, 640, "HOHL?", WHITE, INK, 54, k=pop(ta, "Die Wand"))
        for j in range(3):
            r = 50 + 40 * j + 20 * math.sin(ta * 8)
            cv.arc((hole[0] - r, hole[1] - r, hole[0] + r, hole[1] + r), -50, 50, INK, 5)
    if ta >= cue("Du bohrst"):
        cv.circle(hole[0], hole[1], 30, (40, 30, 20), INK, 5)
        if ta < cue("Und plötzlich"):
            drill(cv, hole[0] - 230, hole[1] + 10)
            cracks(cv, hole[0], hole[1], 5, 80)
    if ta >= cue("Und plötzlich"):
        k = ease(seg(ta, cue("Und plötzlich") + 0.6, cue("Und plötzlich") + 1.6))
        T.bill(cv, hole[0] + 60 * math.sin(k * 6), hole[1] + 20 + 520 * k, 170, k * 3)
        label(cv, 780, 640, "GELD?!", GREEN, YELLOW, 60, k=pop(ta, "Und plötzlich", 0.3))


def s_reveal(cv, t, dur, ta):
    night = ta >= cue("Du zählst")
    room(cv, night=night)
    k = ease(seg(ta, cue("Du reißt"), cue("Hunderte") + 0.6))
    # torn wallpaper: the opening grows
    x0, y0, x1, y1 = WALL
    bundles(cv, (x0, y0, x1, y0 + (y1 - y0) * max(0.15, k)), 1.0)
    for j in range(5):                                                       # ripped edge
        cv.poly([(x0 - 10 + j * 92, y0 + (y1 - y0) * max(0.15, k) - 5), (x0 + 36 + j * 92, y0 + (y1 - y0) * max(0.15, k) + 40),
                 (x0 + 82 + j * 92, y0 + (y1 - y0) * max(0.15, k) - 5)], (214, 200, 230), INK, 3)
    T.money_pile(cv, 1520, seed=5, n=int(10 + 30 * k))
    hero(cv, 290, 1760, 0.85, "shock" if not night else "rich", "down", blink=blink_at(ta), look=(1, 0))
    if ta >= cue("Bündel"):
        label(cv, 290, 640, "BÜNDEL", WHITE, INK, 46, k=pop(ta, "Bündel"))
    if ta >= cue("Hunderte"):
        label(cv, 290, 760, "HUNDERTE", WHITE, INK, 46, k=pop(ta, "Hunderte"))
    if night:
        c = ease(seg(ta, cue("Du zählst"), cue("Elf Millionen") + 0.3))
        cv.rect((140, 520, 860, 690), WHITE, INK, 6, r=24)
        cv.text((UX, 640), f"{int(11_000_000 * c):,} €".replace(",", "."), font(84, "Black"), GREEN, "ms")


def s_note(cv, t, dur, ta):
    cv.rect((0, 0, W, H), (120, 90, 60))
    for r in range(14):                                                      # close-up: wall of bundles
        for c in range(5):
            bundle(cv, 100 + c * 230 + (115 if r % 2 else 0) - 60, 260 + r * 120, 210, 92)
    cv.overlay((0, 0, 0), 70)
    lines = [("NICHT ANFASSEN.", RED), ("WIR KOMMEN", INK), ("ZURÜCK.", INK), ("DATUM: 14.11.", BLUE)]
    n = 0
    for key, m in (("Nicht", 1), ("Wir kommen", 3), ("Datum", 4)):
        if ta >= cue(key):
            n = m
    k = ease(seg(ta, cue("Doch auf"), cue("Doch auf") + 0.4))
    sticky(cv, UX, 760 + (1 - k) * 900, lines, n)
    hero(cv, 860, 1900, 0.7, "shock" if ta >= cue("Nicht") else "worry", "down", blink=blink_at(ta))
    if ta >= cue("morgen"):
        label(cv, UX, 1160, "= MORGEN!", RED, WHITE, 70, k=pop(ta, "morgen"))


def s_pause(cv, t, dur, ta):
    room(cv, night=True)
    bundles(cv, WALL)
    hero(cv, 290, 1760, 0.85, "worry", "head", blink=False, look=(1, -1))
    if ta >= cue("Wer hat"):
        label(cv, UX, 660, "WER WOHNTE", WHITE, INK, 58, k=pop(ta, "Wer hat"))
        label(cv, UX, 780, "VOR DIR HIER?", RED, WHITE, 58, k=pop(ta, "Wer hat"))


def s_article(cv, t, dur, ta):
    if ta < cue("Der Täter"):
        room(cv, night=True)
        laptop(cv, 110, 470, 890, 1060)
        cv.rect((110, 470, 890, 550), (30, 30, 40))
        cv.text((140, 525), "NEWS", font(40, "Black"), RED)
        cv.text((UX, 525), "Bankraub Vormieter", font(28, "Bold"), (180, 180, 190), "ls")
        if ta >= cue("Und findest"):
            cv.text((150, 630), "BANKRAUB IN", font(58, "Black"), INK)
            cv.text((150, 700), "DEINER STRASSE", font(58, "Black"), INK)
            cv.text((150, 760), "vor 3 Jahren", font(34, "Bold"), (120, 120, 130))
            cv.rect((150, 790, 850, 800), (220, 220, 225))
        if ta >= cue("Die Beute"):
            cv.text((150, 880), "Beute:", font(46, "Bold"), INK)
            cv.text((330, 880), "11 MIO. €", font(58, "Black"), GREEN)
        if ta >= cue("Nie gefunden"):
            cv.rect((150, 920, 640, 1010), RED, INK, 4, r=14)
            cv.text((395, 985), "NIE GEFUNDEN", font(50, "Black"), WHITE, "ms")
        hero(cv, 800, 1820, 0.6, "shock" if ta >= cue("Nie gefunden") else "worry", "down", blink=blink_at(ta))
        return
    # flashback (sepia applied in render): the previous tenant carries bags into YOUR flat
    wallpaper(cv, 0, 0, W, 1320, (200, 196, 186))
    cv.rect((0, 1300, W, H), (150, 110, 80))
    door(cv, 620, 760, 940, 1310, peephole=False)
    cv.rect((660, 640, 900, 720), WHITE, INK, 4, r=8)
    cv.text((780, 695), "WOHNUNG 3", font(36, "Black"), INK, "ms")
    k = ease(seg(ta, cue("Der Täter"), cue("Der Täter") + 1.6))
    vormieter(cv, 200 + 300 * k, 1760, 0.85, "smug", "down", blink=blink_at(ta))
    money_bag(cv, 200 + 300 * k + 190, 1500, 0.8)
    label(cv, 200 + 300 * k, 640 - 0, "VORMIETER", (36, 36, 44), WHITE, 42)


def s_door(cv, t, dur, ta):
    view = ta >= cue("Durch den")
    if not view:
        wallpaper(cv, 0, 0, W, 1320, (226, 220, 206))
        cv.rect((0, 1300, W, H), (150, 110, 80))
        door(cv, 330, 560, 750, 1310)
        hero(cv, 200, 1780, 0.75, "shock", "down", blink=blink_at(ta), look=(1, 0))
        if ta >= cue("Dann klingelt"):
            label(cv, 870, 760, "DING DONG", YELLOW, INK, 44, k=pop(ta, "Dann klingelt"))
        if ta >= cue("Zweimal"):
            label(cv, 870, 880, "×2", RED, WHITE, 60, k=pop(ta, "Zweimal"))
        return
    # through the peephole: fisheye circle, the previous tenant holds up a key
    cv.rect((0, 0, W, H), (200, 196, 186))
    cv.rect((0, 1350, W, H), (120, 110, 100))
    vormieter(cv, UX, 1600, 0.9, "smug", "up" if ta >= cue("Er hält") else "down", blink=blink_at(ta))
    if ta >= cue("Er hält"):
        key_icon(cv, 725, 700, 1.1)
    mask = Image.new("L", cv.img.size, 255)
    ImageDraw.Draw(mask).ellipse([v * SS for v in (40, 380, 1040, 1380)], fill=0)
    cv.img.paste((10, 10, 14), (0, 0), mask)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")
    cv.ellipse((40, 380, 1040, 1380), None, (60, 60, 70), 14)
    if ta >= cue("Den Schlüssel"):
        label(cv, UX, 1470, "DEIN SCHLÜSSEL", RED, WHITE, 56, k=pop(ta, "Den Schlüssel"))


def s_final(cv, t, dur, ta):
    room(cv, night=True)
    bundles(cv, WALL)
    hero(cv, 380, 1760, 0.85, "worry", "down", blink=blink_at(ta), look=(1 if ta >= cue("Oder nimmst") else -1, 0))
    money_bag(cv, 780, 1500, 0.9)
    cv.rect((40, 980, 220, 1290), (30, 30, 36), INK, 6, r=20)               # phone with 110
    cv.rect((55, 1010, 205, 1260), (240, 245, 250))
    cv.text((130, 1160), "110", font(60, "Black"), RED, "ms")


def buttons(img):
    d = ImageDraw.Draw(img, "RGBA")
    f = T.font(48, "Black")
    for (x0, x1), lab, bg, fg in (((70, 470), "POLIZEI", BLUE, WHITE), ((530, 930), "GELD NEHMEN", (40, 140, 70), YELLOW)):
        d.rounded_rectangle((x0, 1340, x1, 1450), 28, fill=bg, outline=INK, width=6)
        d.text(((x0 + x1) / 2, 1412), lab, font=f, fill=fg, anchor="ms")


SCENES = [s_hook, s_drill, s_reveal, s_note, s_pause, s_article, s_door, s_final]
PAUSE = 4
UI_SCENES = (3, 5, 6)
INNER_CUTS = [SHOCK, cue("Der Täter"), cue("Durch den")]


def sepia(img):
    g = img.convert("L")
    return ImageOps.colorize(g, black=(46, 30, 14), white=(255, 238, 204)).convert("RGB")


def render(i, t=0.5, dur=5.0, ta=None):
    ta = BOUNDS[i][0] + t * (BOUNDS[i][1] - BOUNDS[i][0]) if ta is None else ta
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur, ta)
    img = cv.final()
    if i in UI_SCENES:
        img = T.camera(img, 0.0, 500, 810)
    else:
        img = T.camera(img, 0.02 + 0.06 * ease(t), 540, 960)
    if i == 5 and ta >= cue("Der Täter"):
        img = sepia(img)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 420, 550), 18, fill=(40, 26, 12, 220))
        d.text((240, 528), "RÜCKBLENDE", font=T.font(44, "Black"), fill=(255, 238, 204), anchor="ms")
    if i == len(SCENES) - 1:
        buttons(img)
    if i == PAUSE and ta < cue("Jetzt"):
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, ta):
    if i == 0 and ta < SHOCK:
        return ("", "white")
    if i == 5 and ta >= cue("Der Täter"):
        return ("TÄTER: DEIN VORMIETER", "red")
    if i == 6 and ta >= cue("Durch den"):
        return ("ER HAT EINEN SCHLÜSSEL", "red")
    return [("11.000.000 €", "green"), ("NUR EIN BILD AUFHÄNGEN", "white"), ("11.000.000 €", "green"),
            ("WIR KOMMEN ZURÜCK", "red"), ("", "white"), ("BANKRAUB · 11 MIO.", "red"), ("ES KLINGELT", "red"),
            ("POLIZEI ODER GELD?", "yellow")][i]
