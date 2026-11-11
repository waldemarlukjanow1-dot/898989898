"""Scenes for 'SCHICK DAS DEINEM CHEF' – GTA 6 release day off (STIL 3, T.HERO).

The user's trailer clip (assets/trailer_bg.mp4, rotated upright, 30.1 s) runs the whole time behind / inside
the scenes and loops. It is timed so its last seconds (logo + 'NOVEMBER 19, 2026') land on the final scene.
Scenes get (cv, t, dur, ta) and are cued to the voice."""
import glob
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "vicecity"))
sys.path.append(os.path.join(HERE, "..", "reich"))
import style3 as T  # noqa: E402
from style3 import Canvas, font, W, H, ease, seg, INK, WHITE, YELLOW  # noqa: E402
from timing import PHRASES, TEMPO, seq_bounds  # noqa: E402

UX = 500
SS = T.S.SS
RED, GREEN, PINK, NEON = (220, 40, 50), (40, 140, 70), (255, 80, 150), (60, 230, 255)
BOUNDS, TOTAL = seq_bounds()
BOSS = dict(hoodie=(70, 74, 86), hair=(110, 100, 96), tie=True, bald=True, mustache=True)
MATE = dict(hoodie=(200, 120, 40), hair=(150, 90, 40), outfit="hoodie", hair_style="curly")

# ------------------------------------------------------------------ trailer clip
FRAMES = sorted(glob.glob(os.path.join(HERE, "build", "frames", "*.jpg")))
CLIP_LEN = len(FRAMES) / 30.0 if FRAMES else 30.1
CLIP_OFF = (2 * CLIP_LEN - TOTAL) % CLIP_LEN      # loop so the logo/date end card lands on the final scene
_FCACHE = {}


def clip_frame(ta, raw=False):
    if not FRAMES:
        return Image.new("RGB", (992, 574), (60, 30, 90))
    k = int(((ta + (0 if raw else CLIP_OFF)) % CLIP_LEN) * 30) % len(FRAMES)
    if k not in _FCACHE:
        if len(_FCACHE) > 8:
            _FCACHE.clear()
        _FCACHE[k] = Image.open(FRAMES[k]).convert("RGB")
    return _FCACHE[k]


def _cover(im, w, h, fx=0.5, fy=0.5):
    sc = max(w / im.width, h / im.height)
    nw, nh = int(im.width * sc + 1), int(im.height * sc + 1)
    im = im.resize((nw, nh), Image.BILINEAR)
    x0, y0 = int((nw - w) * fx), int((nh - h) * fy)
    return im.crop((x0, y0, x0 + w, y0 + h))


def clip(cv, ta, box, shape="rect", r=0, dim=0.0, blur=0, fx=0.5, fy=0.5, border=None, alpha=255, raw=False):
    """Paste the playing trailer into box (1080x1920 coords). shape: rect (rounded by r) or ellipse."""
    x0, y0, x1, y1 = [int(v * SS) for v in box]
    w, h = x1 - x0, y1 - y0
    im = _cover(clip_frame(ta, raw), w, h, fx, fy)
    if blur:
        im = im.resize((max(1, w // 6), max(1, h // 6)), Image.BILINEAR).filter(
            ImageFilter.GaussianBlur(blur)).resize((w, h), Image.BILINEAR)
    if dim:
        im = Image.blend(im, Image.new("RGB", im.size, (8, 6, 20)), dim)
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    if shape == "ellipse":
        md.ellipse((0, 0, w - 1, h - 1), fill=alpha)
    else:
        md.rounded_rectangle((0, 0, w - 1, h - 1), r * SS, fill=alpha)
    cv.img.paste(im, (x0, y0), mask)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")
    if border:
        col, bw = border
        if shape == "ellipse":
            cv.ellipse(box, None, col, bw)
        else:
            cv.rect(box, None, col, bw, r=r)


def trailer_backdrop(cv, ta, dim=0.45):
    """Full-screen trailer: blurred cover fill + sharp 16:9 band in the upper half."""
    clip(cv, ta, (0, 0, W, H), blur=6, dim=0.55)
    clip(cv, ta, (0, 250, W, 250 + 625), dim=dim * 0.3)


# ------------------------------------------------------------------ helpers
def cue(text):
    return next(a / TEMPO for a, b, s, t in PHRASES if t.startswith(text))


def talking(ta, seqs):
    """Mouth opening 0..1 while a phrase of the given sequences is spoken."""
    for a, b, s, _ in PHRASES:
        if s in seqs and a / TEMPO <= ta <= b / TEMPO:
            return 0.5 + 0.5 * abs(math.sin(ta * 17))
    return 0.0


def hero(cv, x, y, s, mood, arms="down", **kw):
    return T.character(cv, x, y, s, mood, arms, **dict(T.HERO, **kw))


def boss(cv, x, y, s, mood, arms="down", **kw):
    return T.character(cv, x, y, s, mood, arms, **dict(BOSS, **kw))


def blink_at(ta):
    return (ta % 2.7) < 0.1


_LOGO = None


def paste_logo(cv, cx, cy, w, k=1.0, radius=40):
    global _LOGO
    if k <= 0:
        return
    if _LOGO is None:
        _LOGO = Image.open(os.path.join(HERE, "assets", "logo_gta6.jpg")).convert("RGB")
    sc = 0.7 + 0.3 * ease(min(1, k))
    ww = int(w * sc * SS)
    hh = int(ww * _LOGO.height / _LOGO.width)
    im = _LOGO.resize((ww, hh), Image.LANCZOS)
    a = int(255 * min(1, k * 1.5))
    mask = Image.new("L", (ww, hh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, ww - 1, hh - 1), radius * SS, fill=a)
    x0, y0 = int(cx * SS - ww / 2), int(cy * SS - hh / 2)
    cv.d.rounded_rectangle((x0 - 10 * SS, y0 - 10 * SS, x0 + ww + 10 * SS, y0 + hh + 10 * SS),
                           (radius + 8) * SS, fill=(255, 255, 255, a))
    cv.img.paste(im, (x0, y0), mask)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")


def office(cv, ta, window_clip=False, boss_room=False):
    wall = (196, 186, 170) if boss_room else (214, 222, 230)
    cv.rect((0, 0, W, H), wall)
    if window_clip:
        clip(cv, ta, (90, 230, 990, 800), dim=0.05)
    else:
        cv.rect((90, 230, 990, 800), (150, 200, 240))
        for k in range(5):
            x = 120 + k * 180
            top = 470 - (k % 3) * 90
            cv.rect((x, top, x + 140, 800), (170, 190, 210), (120, 140, 160), 3)
            for wy in range(top + 20, 780, 50):
                cv.rect((x + 20, wy, x + 50, wy + 26), (210, 230, 245))
                cv.rect((x + 80, wy, x + 110, wy + 26), (210, 230, 245))
    cv.rect((90, 230, 990, 800), None, INK, 10)
    cv.line([(540, 230), (540, 800)], INK, 8)
    cv.rect((0, 800, W, 1120), (226, 230, 236) if not boss_room else (210, 198, 180))
    cv.rect((0, 1110, W, H), (160, 160, 170) if not boss_room else (120, 80, 60))
    if boss_room:
        cv.rect((690, 850, 900, 1030), (250, 246, 236), INK, 5)
        cv.text((795, 935), "CHEF", font(40, "Black"), INK, "ms")
        cv.text((795, 985), "DES JAHRES", font(24, "Black"), INK, "ms")
    else:
        cv.rect((700, 850, 880, 940), (40, 120, 60), INK, 4, r=8)   # office sign
        cv.text((790, 908), "BÜRO", font(40, "Black"), WHITE, "ms")


def desk(cv, y=1300, monitor=True):
    cv.rect((40, y, 1040, y + 60), (170, 120, 80), INK, 6, r=10)
    cv.rect((40, y + 60, 1040, y + 330), (150, 105, 70), INK, 6, r=8)
    if monitor:
        cv.rect((690, y - 270, 990, y - 80), (40, 42, 50), INK, 6, r=12)
        cv.rect((710, y - 250, 970, y - 100), (120, 170, 230))
        cv.rect((815, y - 80, 865, y), (40, 42, 50))
    cv.ellipse((110, y - 150, 230, y - 10), (60, 150, 80), INK, 4)
    cv.rect((140, y - 40, 200, y), (180, 90, 60), INK, 4)


def bubble_clip(cv, ta, cx, cy, rx, ry, tail=None, k=1.0):
    """Thought/speech bubble with the trailer playing inside."""
    if k <= 0:
        return
    s = 0.6 + 0.4 * ease(min(1, k))
    rx, ry = rx * s, ry * s
    if tail:
        for j, (tx, ty, tr) in enumerate(tail):
            cv.circle(tx, ty, tr * s, WHITE, INK, 5)
    cv.ellipse((cx - rx - 14, cy - ry - 14, cx + rx + 14, cy + ry + 14), WHITE, INK, 6)
    clip(cv, ta, (cx - rx, cy - ry, cx + rx, cy + ry), shape="ellipse")


def stamp(cv, x, y, text, col, k=1.0, rot_box=True, size=54):
    if k <= 0:
        return
    s = 1.6 - 0.6 * ease(min(1, k))
    f = font(int(size * s), "Black")
    tw = cv.d.textlength(text, font=T.font(int(size * s), "Black"))
    cv.rect((x - tw / 2 - 26, y - size * s * 0.95, x + tw / 2 + 26, y + size * s * 0.45), WHITE, col, 8, r=14)
    cv.text((x, y), text, f, col, "ms")


# ------------------------------------------------------------------ scenes (cv, t, dur, ta)
SHOCK = 1.3


def s_hook(cv, t, dur, ta):
    if ta < SHOCK:  # first second: trailer + logo → instantly clear what this is about
        clip(cv, ta + 0.3, (0, 0, W, H), dim=0.25, raw=True, fx=0.62)   # trailer opening: sunset over the city
        paste_logo(cv, UX, 760, 640, k=seg(ta, 0.0, 0.3) * 3)
        cv.rect((260, 1110, 740, 1190), YELLOW, INK, 5, r=20)
        cv.text((UX, 1170), "FÜR DEINEN CHEF", font(46, "Black"), INK, "ms")
        return
    office(cv, ta, boss_room=True)
    boss(cv, 800, 1780, 0.92, "neutral" if ta < cue("Lies erst") else "angry", "phone", blink=blink_at(ta))
    # big phone: a video from "Dein Mitarbeiter" with the trailer playing
    x0, y0, x1, y1 = 120, 500, 640, 1150
    k = ease(seg(ta, SHOCK, SHOCK + 0.35))
    dy = (1 - k) * 700
    cv.rect((x0 - 16, y0 - 16 + dy, x1 + 16, y1 + 16 + dy), (24, 24, 30), INK, 6, r=44)
    cv.rect((x0, y0 + dy, x1, y1 + dy), (245, 247, 250))
    cv.rect((x0, y0 + dy, x1, y0 + 90 + dy), (230, 233, 240))
    cv.text(((x0 + x1) / 2, y0 + 60 + dy), "Dein Mitarbeiter", font(36, "Black"), INK, "ms")
    clip(cv, ta, (x0 + 30, y0 + 120 + dy, x1 - 30, y0 + 420 + dy), r=20)
    cv.rect((x0 + 30, y0 + 450 + dy, x1 - 30, y0 + 540 + dy), (60, 140, 250), None, 0, r=30)
    cv.text(((x0 + x1) / 2, y0 + 508 + dy), "Bitte ganz ansehen!", font(36, "Black"), WHITE, "ms")
    cv.text(((x0 + x1) / 2, y0 + 610 + dy), "Betreff: 19.11.", font(32, "Bold"), (120, 120, 130), "ms")


def s_date(cv, t, dur, ta):
    trailer_backdrop(cv, ta)
    paste_logo(cv, 860, 780, 240, k=1.0, radius=18)
    if ta < cue("Dreizehn"):          # release date
        k = ease(seg(ta, cue("Am neun") + 0.3, cue("Am neun") + 0.7))
        cv.rect((290, 920, 710, 1190), WHITE, INK, 6, r=22)
        cv.rect((290, 920, 710, 1000), RED, None, 0, r=22)
        cv.rect((290, 975, 710, 1000), RED)
        cv.text((UX, 982), "NOVEMBER", font(44, "Black"), WHITE, "ms")
        cv.text((UX, 1160), "19", font(int(150 * (0.6 + 0.4 * k)), "Black"), INK, "ms")
    elif ta < cue("Und er braucht"):  # 13 years
        yr = int(2013 + 13 * ease(seg(ta, cue("Dreizehn"), cue("Dreizehn") + 1.6)))
        cv.rect((290, 920, 710, 1190), WHITE, INK, 6, r=22)
        cv.text((UX, 990), "GEWARTET SEIT", font(38, "Black"), (120, 120, 130), "ms")
        cv.text((UX, 1140), str(yr), font(130, "Black"), INK, "ms")
    else:                             # one day off: the release day
        cv.rect((200, 920, 800, 1190), (250, 246, 236), INK, 6, r=16)
        cv.text((UX, 990), "URLAUBSANTRAG", font(44, "Black"), INK, "ms")
        cv.text((UX, 1060), "1 Tag · 19.11.", font(44, "Bold"), INK, "ms")
        stamp(cv, UX, 1150, "RELEASE-TAG", RED, k=seg(ta, cue("Den Release"), cue("Den Release") + 0.3) * 1.0)


def s_desk(cv, t, dur, ta):
    office(cv, ta)
    in_head = ta >= cue("Er sitzt")
    hero(cv, 380, 1720, 0.9, "stare" if in_head else "neutral", "down", blink=blink_at(ta), look=(1, -1) if in_head else (0, 0))
    desk(cv)
    cv.rect((730, 1080, 950, 1180), (250, 250, 250), INK, 3)          # boring spreadsheet on the monitor
    for k in range(4):
        cv.line([(745, 1100 + k * 22), (935, 1100 + k * 22)], (170, 180, 190), 3)
    if ta < cue("Er sitzt"):
        cv.rect((600, 900, 960, 990), WHITE, INK, 4, r=18)
        cv.text((780, 960), "Kopf: 0 %", font(46, "Black"), RED, "ms")
    k = seg(ta, cue("Er sitzt") + 1.0, cue("Er sitzt") + 1.5)
    bubble_clip(cv, ta, 680, 640, 300, 180, tail=[(470, 890, 22), (520, 850, 32)], k=k * 1.0)
    if ta >= cue("Er sitzt") + 2.2:
        cv.rect((540, 790, 820, 860), NEON, INK, 4, r=16)
        cv.text((680, 842), "VICE CITY", font(42, "Black"), INK, "ms")


def mail_window(cv, ta):
    x0, y0, x1, y1 = 110, 430, 900, 1130
    cv.rect((x0, y0, x1, y1), WHITE, INK, 6, r=18)
    cv.rect((x0, y0, x1, y0 + 80), (60, 120, 220), None, 0, r=18)
    cv.rect((x0, y0 + 50, x1, y0 + 80), (60, 120, 220))
    cv.text((x0 + 30, y0 + 55), "Neue E-Mail an: Chef", font(36, "Black"), WHITE)
    lines = [("Betref: Quartalsbericht", "Betref"), ("Sehr geehrter Herr Vice City,", "Vice City"),
             ("anbei der Berricht. Ich", "Berricht."), ("bin morgen fruh im Büro.", "fruh")]
    n = int(seg(ta, cue("Er tippt"), cue("Er tippt") + 1.2) * len(lines) + 0.999)
    for k, (txt, bad) in enumerate(lines[:n]):
        y = y0 + 170 + k * 100
        f = T.font(40, "Bold")
        cv.text((x0 + 40, y), txt, font(40, "Bold"), INK)
        i = txt.index(bad)
        xa = x0 + 40 + cv.d.textlength(txt[:i], font=T.font(40 * SS, "Bold")) / SS
        xb = xa + cv.d.textlength(bad, font=T.font(40 * SS, "Bold")) / SS
        pts = [(xa + j * 12, y + 14 + (6 if j % 2 else 0)) for j in range(int((xb - xa) / 12) + 1)]
        cv.line(pts, RED, 4)
        del f
    if ta >= cue("Er tippt") + 1.4:
        stamp(cv, 640, 1080, "4 FEHLER", RED, k=seg(ta, cue("Er tippt") + 1.4, cue("Er tippt") + 1.7) * 1.0, size=46)


def s_distract(cv, t, dur, ta):
    if ta < cue("Er tippt"):           # phone every five minutes – the trailer on his phone
        office(cv, ta)
        hero(cv, 540, 1760, 0.95, "happy", "phone", blink=blink_at(ta), look=(0, 1))
        desk(cv, 1420, monitor=False)
        x0, y0, x1, y1 = 260, 430, 820, 790
        cv.rect((x0 - 14, y0 - 14, x1 + 14, y1 + 14), (24, 24, 30), INK, 6, r=30)
        clip(cv, ta, (x0, y0, x1, y1), r=10)
        cv.rect((640, 830, 960, 910), WHITE, INK, 4, r=18)
        cv.circle(690, 870, 24, None, INK, 5)
        cv.line([(690, 870), (690, 854)], INK, 4)
        cv.line([(690, 870), (702, 878)], INK, 4)
        n = 1 + int(max(0, ta - cue("Er schaut")) / 0.5)
        cv.text((820, 890), f"{min(n, 9)}× in 5 Min.", font(34, "Black"), INK, "ms")
    elif ta < cue("Und in der Kaffee"):
        office(cv, ta)
        hero(cv, 800, 1760, 0.75, "happy", "down", blink=blink_at(ta))
        desk(cv, 1450, monitor=False)
        mail_window(cv, ta)
    else:                              # coffee kitchen: talks about nothing else
        cv.rect((0, 0, W, H), (236, 226, 210))
        cv.rect((0, 1110, W, H), (180, 160, 140))
        cv.rect((40, 860, 1040, 1120), (120, 140, 160), INK, 6, r=8)        # counter
        cv.rect((620, 640, 820, 860), (50, 52, 60), INK, 6, r=14)           # coffee machine
        cv.rect((680, 760, 760, 860), (30, 30, 34))
        cv.rect((690, 800, 750, 860), WHITE, INK, 3, r=6)
        cv.rect((740, 470, 1000, 550), (60, 110, 60), INK, 4, r=10)
        cv.text((870, 527), "KAFFEEKÜCHE", font(36, "Black"), WHITE, "ms")
        hero(cv, 300, 1760, 0.85, "happy", "point", talk=talking(ta, (3,)), blink=blink_at(ta))
        T.character(cv, 800, 1760, 0.85, "worry" if ta > cue("Und in der Kaffee") + 1.5 else "neutral",
                    "down", blink=blink_at(ta + 1.3), **MATE)
        bubble_clip(cv, ta, 420, 620, 260, 160, tail=[(360, 830, 26)], k=seg(ta, cue("Und in der Kaffee") + 0.4,
                                                                              cue("Und in der Kaffee") + 0.9) * 1.0)
        if ta >= cue("Und in der Kaffee") + 1.6:
            cv.rect((640, 860, 990, 940), WHITE, INK, 4, r=18)
            cv.text((815, 917), "Schon wieder…", font(40, "Black"), INK, "ms")


def s_pause(cv, t, dur, ta):
    office(cv, ta, boss_room=True)
    boss(cv, 540, 1760, 1.0, "angry" if ta >= cue("Willst du") else "neutral", "down",
         blink=blink_at(ta), look=(0, 0))
    if ta >= cue("Willst du"):
        cv.rect((140, 400, 860, 560), WHITE, INK, 6, r=26)
        cv.text((UX, 470), "So einer", font(52, "Black"), INK, "ms")
        cv.text((UX, 535), "im Büro?", font(52, "Black"), RED, "ms")


def s_deal(cv, t, dur, ta):
    trailer_backdrop(cv, ta, dim=0.6)
    hero(cv, 830, 1800, 0.75, "happy", "point", blink=blink_at(ta), talk=0.0)
    x0, y0, x1, y1 = 80, 430, 700, 1180
    cv.rect((x0, y0, x1, y1), (250, 246, 236), INK, 6, r=12)
    cv.text(((x0 + x1) / 2, y0 + 80), "URLAUBSANTRAG", font(50, "Black"), INK, "ms")
    cv.line([(x0 + 40, y0 + 110), (x1 - 40, y0 + 110)], INK, 4)
    rows = [("Einen Tag", "19.11.: 1 Tag frei"), ("Dafür", "Woche davor: +1 Std."),
            ("Jeden Tag", "Jeden Tag. Mo–Fr"), ("Ohne zu", "Ohne Meckern")]
    for k, (key, lab) in enumerate(rows):
        y = y0 + 170 + k * 130
        cv.rect((x0 + 40, y, x0 + 100, y + 60), WHITE, INK, 4, r=8)
        cv.text((x0 + 125, y + 45), lab, font(38, "Bold"), INK)
        if ta >= cue(key) + 0.3:
            cv.line([(x0 + 50, y + 30), (x0 + 68, y + 52), (x0 + 95, y + 8)], GREEN, 10)
    if ta >= cue("Ohne zu") + 0.6:
        cv.text(((x0 + x1) / 2, y1 - 40), "Unterschrift: Dein Mitarbeiter", font(30, "Bold"), (40, 60, 160), "ms")


def s_back(cv, t, dur, ta):
    office(cv, ta, window_clip=True)
    k = ease(seg(ta, cue("Und danach"), cue("Und danach") + 1.4))
    x = 1250 - 710 * k
    walk = 0 if k >= 1 else math.sin(ta * 12) * 10
    hero(cv, x, 1760 - abs(walk), 0.95, "rich" if k >= 1 else "happy", "down", blink=blink_at(ta))
    labels = [("Ausgeschlafen", "AUSGESCHLAFEN", 520, GREEN), ("Glücklich", "GLÜCKLICH", 640, GREEN),
              ("Motivierter", "MOTIVATION 200 %", 760, (200, 120, 0))]
    for key, lab, y, col in labels:
        if ta >= cue(key):
            stamp(cv, UX, y + 50, lab, col, k=seg(ta, cue(key), cue(key) + 0.25) * 1.0, size=50)


def s_final(cv, t, dur, ta):
    office(cv, ta, window_clip=True, boss_room=True)
    boss(cv, 540, 1760, 1.0, "worry", "down", blink=blink_at(ta), look=(1, -1))   # thinking
    if ta >= cue("Und schick"):
        cv.rect((250, 480, 750, 570), WHITE, INK, 4, r=20)
        cv.text((UX, 542), "@dein.kumpel", font(46, "Black"), (60, 120, 230), "ms")


def buttons(img):
    d = ImageDraw.Draw(img, "RGBA")
    f = T.font(60, "Black")
    for (x0, x1), lab, bg, fg in (((90, 460), "JA", (40, 140, 70), YELLOW), ((540, 910), "NEIN", RED, WHITE)):
        d.rounded_rectangle((x0, 1340, x1, 1450), 28, fill=bg, outline=INK, width=6)
        d.text(((x0 + x1) / 2, 1418), lab, font=f, fill=fg, anchor="ms")


SCENES = [s_hook, s_date, s_desk, s_distract, s_pause, s_deal, s_back, s_final]
PAUSE = 4
UI_SCENES = (0, 1, 3, 5)
INNER_CUTS = [SHOCK, cue("Er tippt"), cue("Und in der Kaffee")]


def render(i, t=0.5, dur=5.0, ta=None):
    ta = BOUNDS[i][0] + t * (BOUNDS[i][1] - BOUNDS[i][0]) if ta is None else ta
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur, ta)
    img = cv.final()
    if i in UI_SCENES:
        img = T.camera(img, 0.0, 500, 810)
    else:
        img = T.camera(img, 0.02 + 0.06 * ease(t), 540, 960)
    if i == len(SCENES) - 1:
        buttons(img)
    if i == PAUSE and ta < cue("Willst du"):
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, ta):
    if i == 0 and ta < SHOCK:
        return ("GTA 6", "yellow")
    return [("GTA 6 · FÜR DEINEN CHEF", "yellow"), ("19. NOVEMBER", "yellow"), ("IM KOPF: VICE CITY", "red"),
            ("PRODUKTIVITÄT: 0 %", "red"), ("", "white"), ("SEIN ANGEBOT", "green"),
            ("ZURÜCK MIT 200 %", "green"), ("BEKOMMT ER FREI?", "yellow")][i]
