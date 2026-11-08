"""Scenes for 'FLUG 404 – Teil 2: Schlafen stellen' (STIL 3, T.HERO). Scenes get (t, dur, ta) and are cued
to the spoken phrases via cue(). Helpers (cabin, seats, passengers) come from cabin.py."""
import math

from PIL import Image, ImageDraw

import cabin as C
from cabin import T, Canvas, font, W, H, ease, seg, INK, WHITE, SKIN, YELLOW, UX, RED, SEAT, SEAT_D, CABIN
from cabin import cabin_back, seat_front, seat_back, window, hero, blink_at, PASSENGERS
from timing import PHRASES, TEMPO, seq_bounds

BOUNDS, TOTAL = seq_bounds()


def cue(text):
    return next(a / TEMPO for a, b, s, t in PHRASES if t.startswith(text))


def cue_end(text):
    return next(b / TEMPO for a, b, s, t in PHRASES if t.startswith(text))



# ---- realistic cabin: 3 seats left + aisle + 3 seats right, rows going all the way to the back
ROWS6 = [0.16, 0.2, 0.25, 0.31, 0.38, 0.47, 0.58, 0.71, 0.86]   # perspective scale, back -> front
SEAT_COLORS = [(52, 72, 120), (48, 66, 112)]


def row_y(s):
    return 640 + 1000 * s  # seat-cushion line of a row


def cabin_rows(cv, mood_fn, ta, night=False, empty=(), talk_seat=None, talk=0.0, skip_front=False):
    """mood_fn(row, seat) -> mood. seats are 0..5 (0-2 left of the aisle, 3-5 right)."""
    rows = ROWS6[:-1] if skip_front else ROWS6
    for ri, s in enumerate(rows):
        seat_w = 205 * s
        aisle = 150 * s
        cy = row_y(s)
        head_y = cy - 330 * s
        for k in range(6):
            side = -1 if k < 3 else 1
            j = (2 - k) if k < 3 else (k - 3)          # 0 = next to the aisle
            x = UX + side * (aisle / 2 + seat_w * (j + 0.5))
            cv.rect((x - seat_w * 0.46, head_y - 120 * s, x + seat_w * 0.46, cy), SEAT_COLORS[(ri + k) % 2], INK, 3,
                    r=int(seat_w * 0.18))
            cv.rect((x - seat_w * 0.34, head_y - 110 * s, x + seat_w * 0.34, head_y - 55 * s), WHITE, None, 0, r=int(seat_w * 0.1))
            if (ri, k) in empty:
                continue
            kw = PASSENGERS[(ri * 5 + k * 3) % len(PASSENGERS)]
            cs = 0.42 * s
            T.character(cv, x, head_y + 753 * cs, cs, mood_fn(ri, k), "down",
                        talk=talk if talk_seat == (ri, k) else 0.0, **kw)
            cv.rect((x - seat_w * 0.5, cy - 40 * s, x + seat_w * 0.5, cy + 30 * s), (40, 56, 96), INK, 3, r=int(8 * s))  # cushion/armrest
        # armrests between blocks + overhead light row
        for side in (-1, 1):
            cv.rect((UX + side * aisle / 2 - 8 * s, cy - 70 * s, UX + side * aisle / 2 + 8 * s, cy + 30 * s), (30, 40, 70))


def dark(cv, alpha):
    if alpha > 0:
        cv.overlay((4, 4, 12), int(alpha))


def twin_kw():
    return dict(T.HERO)


def pair_seats(cv, ta, you_mood, twin=None, twin_mood="smug", twin_talk=0.0, night=True, you_arms="down", extra=None):
    """Your seat (left) and the seat next to you (right), front view; row in front covers the legs."""
    cv.rect((0, 0, W, H), (150, 156, 176) if night else CABIN)
    cv.rect((0, 0, W, 300), (170, 176, 196), INK, 4)
    window(cv, 40, 480, 180, 300, ta, night)
    s = 0.85
    for x, who in ((330, "you"), (720, "twin")):
        seat_front(cv, x, 780, s)
        if who == "you":
            hero(cv, x, 780 + 753 * s, s, you_mood, you_arms, blink=False)
        elif twin:
            hero(cv, x, 780 + 753 * s, s, twin_mood, "down", talk=twin_talk)
    if extra:
        extra()
    cv.rect((40, 780 + 380 * s, 1040, H), SEAT_D, INK, 6, r=50)  # backs of the row in front
    for x in (330, 720):
        cv.rect((x - 180, 780 + 430 * s, x + 180, 780 + 520 * s), (30, 40, 70), INK, 3, r=12)


# ------------------------------------------------------------------ scenes (cv, t, dur, ta)

def s_intro(cv, t, dur, ta):
    cabin_back(cv, ta, night=True)
    cabin_rows(cv, lambda r, k: "stare", ta, night=True)
    cv.overlay((20, 0, 0), 30)
    if ta < cue("Und 187"):  # empty cockpit flash on the first line
        k = 1 - seg(ta, cue("Und 187") - 0.5, cue("Und 187"))
        layer = Canvas((0, 0, 0))
        layer.rect((0, 0, W, H), (40, 44, 56))
        layer.poly([(80, 470), (920, 470), (980, 760), (20, 760)], (30, 50, 100), INK, 6)
        layer.rect((0, 760, W, 1000), (60, 64, 76), INK, 5)
        layer.rect((360, 820, 640, 920), (10, 20, 10), (60, 220, 120), 5, r=10)
        layer.text((UX, 892), "AUTOPILOT", font(40, "Black"), (60, 220, 120), "ms")
        for x in (230, 770):
            layer.rect((x - 140, 1000, x + 140, 1460), (70, 60, 50), INK, 6, r=60)
        cv.img = Image.blend(cv.img, layer.img, k)
        cv.d = ImageDraw.Draw(cv.img, "RGBA")


def s_decide(cv, t, dur, ta):
    closed = ta >= cue("Schließt die Augen")
    pair_seats(cv, ta, "sleep" if closed else "worry")
    if closed:
        dark(cv, 70 * seg(ta, cue("Schließt die Augen"), cue("Und tust so")))


def s_breathe(cv, t, dur, ta):
    pair_seats(cv, ta, "sleep")
    dark(cv, 90)
    breath = 0.5 + 0.5 * math.sin(ta * 2.2)  # slow breathing: chest glow pulses
    cv.glow(330, 1000, 160 + 30 * breath, (140, 180, 255), 40)
    for k, (key, txt) in enumerate((("Langsam", "ATMEN …"), ("Nicht bewegen", "NICHT BEWEGEN"), ("Nicht blinzeln", "NICHT BLINZELN"))):
        if ta >= cue(key):
            a = min(1, (ta - cue(key)) / 0.25)
            cv.rect((560, 470 + k * 95, 940, 545 + k * 95), (255, 255, 255, int(220 * a)), INK, 4, r=16)
            cv.text((750, 522 + k * 95), txt, font(34, "Black"), INK, "ms")


def s_steps(cv, t, dur, ta):
    """A passenger walks down the aisle towards your row and stops right next to you."""
    cabin_back(cv, ta, night=True)
    cabin_rows(cv, lambda r, k: "stare", ta, night=True, skip_front=True)
    dark(cv, 110)
    u = ease(seg(ta, cue("Dann hörst"), cue("Und bleiben")))
    s = 0.35 + 0.55 * u
    walking = ta < cue("Und bleiben") + 0.2
    T.character(cv, UX, 1100 + 780 * u, s, "stare", "down", bob=-14 * s * abs(math.sin(ta * 6)) if walking else 0,
                **PASSENGERS[1])
    for k in range(int(seg(ta, cue("Dann hörst"), cue("Und bleiben")) * 6)):  # footstep marks
        cv.text((120 + (k % 2) * 700, 520 + k * 70), "tap", font(30 + k * 6, "Black"), (255, 214, 10, 200))


def s_lean(cv, t, dur, ta):
    k = ease(seg(ta, cue("Jemand beugt"), cue("Du spürst"))) if ta < cue("Du spürst") else 1.0

    whisper = cue("Er schläft") <= ta < cue_end("Er schläft")

    def leaner():  # a passenger standing in the aisle bends down to your ear (upper body only, row in front hides the rest)
        x = 900 - 340 * k
        y = 640 + 120 * k
        T.character(cv, x, y + 753 * 0.8, 0.8, "stare", "down", talk=abs(math.sin(ta * 11)) if whisper else 0.0,
                    **PASSENGERS[1])
    pair_seats(cv, ta, "sleep", extra=leaner)
    dark(cv, 80)
    if cue("Du spürst") <= ta < cue("Eine Stimme"):
        for j in range(3):  # breath lines between his mouth and your ear
            ph = (ta * 1.5 + j / 3) % 1.0
            cv.arc((440 + 20 * ph, 760 + j * 22, 520 + 30 * ph, 820 + j * 22), 120, 240,
                   (220, 230, 255, int(255 * (1 - ph))), 5)


def s_whisper(cv, t, dur, ta):
    s_lean(cv, 1.0, dur, ta)
    if ta >= cue("Er schläft"):
        a = min(1, (ta - cue("Er schläft")) / 0.2)
        cv.rect((480, 470, 900, 610), (20, 20, 26, int(230 * a)), (255, 214, 10), 4, r=26)
        cv.text((690, 560), "Er schläft nicht.", font(42, "Black"), (255, 240, 180), "ms")


def s_pause(cv, t, dur, ta):
    s_whisper(cv, 1.0, dur, cue("Er schläft") + 1.0)


def eyelid(cv, open_k):
    """POV through one barely opened eye: dark lids top and bottom."""
    gap = 40 + 520 * open_k
    cy = 900
    layer = Image.new("L", cv.img.size, 255)
    ImageDraw.Draw(layer).ellipse(cv.s((-200, cy - gap, W + 200, cy + gap)), fill=0)
    black = Image.new("RGB", cv.img.size, (6, 6, 10))
    cv.img = Image.composite(black, cv.img, layer)
    cv.d = ImageDraw.Draw(cv.img, "RGBA")


def s_open_eye(cv, t, dur, ta):
    cabin_back(cv, ta, night=True)
    cabin_rows(cv, lambda r, k: "sleep", ta, night=True)  # everyone is back in their seats … asleep?
    k = 0.0 if ta < cue("Du öffnest") else 0.25 * ease(seg(ta, cue("Du öffnest"), cue("Nur einen Spalt") + 0.3))
    eyelid(cv, k)


def s_twin(cv, t, dur, ta):
    shown = ta >= cue("Dort sitzt")
    pair_seats(cv, ta, "shock" if shown else "worry", twin=shown, twin_mood="smug")
    if ta < cue("Dort sitzt"):
        cv.rect((560, 600, 880, 700), (255, 255, 255, 220), INK, 4, r=16)
        cv.text((720, 665), "LEER?", font(44, "Black"), INK, "ms")
    if ta >= cue("In deinem"):
        cv.circle(720, 1040, 150, None, (255, 214, 10), 8)     # the sweater
    if ta >= cue("Mit deinem"):
        cv.circle(720, 640, 130, None, RED, 8)                 # the face
    eyelid(cv, 0.25 + 0.75 * ease(seg(ta, cue("Der Platz"), cue("Dort sitzt"))))


def s_takeover(cv, t, dur, ta):
    talk = abs(math.sin(ta * 10)) if cue("Ich übernehme") <= ta < cue_end("Ich übernehme") else 0
    pair_seats(cv, ta, "shock", twin=True, twin_mood="smug", twin_talk=talk)
    if cue("Ich übernehme") <= ta:
        cv.poly([(700, 600), (740, 600), (735, 650)], WHITE, INK, 5)
        cv.rect((500, 470, 920, 600), WHITE, INK, 5, r=30)
        cv.text((710, 553), "Ich übernehme ab hier.", font(34, "Black"), INK, "ms")


def tilt(img, deg):
    big = img.rotate(deg, resample=Image.BICUBIC, expand=False, fillcolor=(10, 10, 14))
    return T.camera(big, 0.12 * min(1, abs(deg) / 12), 540, 960)


def s_dive(cv, t, dur, ta):
    cabin_back(cv, ta, night=True)
    cabin_rows(cv, lambda r, k: "shock" if ta >= cue("Und es geht") else "sleep", ta, night=True)
    if ta >= cue("Und es geht"):  # oxygen masks drop
        k = ease(seg(ta, cue("Und es geht"), cue("Und es geht") + 0.6))
        for x in (180, 330, 670, 820):
            cv.line([(x, 300), (x, 300 + 260 * k)], (230, 230, 230), 4)
            cv.ellipse((x - 34, 280 + 260 * k, x + 34, 340 + 260 * k), (250, 200, 60), INK, 3)
        cv.overlay((180, 0, 0), int(40 + 30 * math.sin(ta * 6)))


def s_final(cv, t, dur, ta):
    pair_seats(cv, ta, "shock", twin=True, twin_mood="smug")
    cv.overlay((180, 0, 0), 30)


def buttons(img):
    d = ImageDraw.Draw(img, "RGBA")
    f = T.font(42, "Black")
    for (x0, x1), lab, bg, fg in (((40, 470), "SITZEN BLEIBEN", WHITE, INK), ((500, 930), "INS COCKPIT", RED, WHITE)):
        d.rounded_rectangle((x0, 1330, x1, 1440), 28, fill=bg, outline=INK, width=6)
        d.text(((x0 + x1) / 2, 1405), lab, font=f, fill=fg, anchor="ms")


SCENES = [s_intro, s_decide, s_breathe, s_steps, s_lean, s_whisper, s_pause, s_open_eye, s_twin, s_takeover, s_dive, s_final]
PAUSE = 6
INNER_CUTS = [cue("Und 187"), cue("Dort sitzt")]
TILT_FROM = cue("Dann ruckelt")


def render(i, t=0.5, dur=5.0, ta=None):
    ta = BOUNDS[i][0] + t * (BOUNDS[i][1] - BOUNDS[i][0]) if ta is None else ta
    cv = Canvas((0, 0, 0))
    SCENES[i](cv, t, dur, ta)
    img = cv.final()
    z = 0.02 + 0.07 * ease(t)
    if i in (4, 5, 6):  # creeping push-in on the whisper
        z = 0.04 + 0.14 * ease(seg(ta, BOUNDS[4][0], BOUNDS[6][1]))
        img = T.camera(img, z, 420, 820)
    else:
        img = T.camera(img, z, 540, 860)
    if ta >= TILT_FROM and i >= 10:  # nose dives: picture tilts, a short jolt on "ruckelt"
        jolt = 3 * math.sin((ta - TILT_FROM) * 30) * max(0, 1 - (ta - TILT_FROM) / 0.6)
        deg = -12 * ease(seg(ta, cue("Und es geht"), cue("Und es geht") + 1.0)) + jolt
        img = tilt(img, deg)
    if i == 11:
        buttons(img)
    if i == PAUSE:
        img = Image.blend(img, img.convert("L").convert("RGB"), 0.6)
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle((60, 470, 200, 610), 20, fill=(0, 0, 0, 160))
        d.rectangle((95, 500, 120, 580), fill=WHITE)
        d.rectangle((140, 500, 165, 580), fill=WHITE)
    return img


def chip_for(i, ta):
    if i == 0:
        return ("OHNE PILOTEN", "red")
    if i == 1:
        return ("SCHLAFEN STELLEN", "white")
    if i == 2:
        return ("NICHT BLINZELN", "red")
    if i == 3:
        return ("SCHRITTE", "white")
    if i in (4, 5, 6):
        return ("ER SCHLÄFT NICHT", "red") if ta >= cue("Er schläft") else ("ATEM AM OHR", "red")
    if i == 7:
        return ("EIN AUGE OFFEN", "white")
    if i == 8:
        return ("DAS BIST … DU?!", "red") if ta >= cue("Mit deinem") else ("PLATZ 32B", "white")
    if i == 9:
        return ("„ICH ÜBERNEHME“", "red")
    return ("STURZFLUG", "red")
