"""Jointed character rig (side view) for clear, readable motion.

A figure is drawn from a pose: torso lean, shoulder/elbow and hip/knee angles for the near
and far limb. Angles are degrees, 0 = hanging straight down, positive = towards facing.
Helpers build walk / run / carry / sit poses. All sizes scale with the head radius r.
"""
import math
from dataclasses import dataclass, field

INK = (18, 22, 24)
WHITE = (244, 241, 234)


def shade(c, k=0.72):
    return tuple(int(v * k) for v in c)


@dataclass
class Look:
    jacket: tuple = (190, 45, 50)
    pants: tuple = (38, 42, 50)
    shoes: tuple = (24, 24, 26)
    hat: tuple | None = None          # cap colour (None = no hat)
    hat_kind: str = "cap"             # cap | beanie | guard
    hair: tuple | None = None
    mask: bool = False                # balaclava
    skin: tuple = (244, 241, 234)     # face colour (zombies: green)
    name: str = ""


@dataclass
class Pose:
    lean: float = 0.0
    sh_n: float = 0.0     # near shoulder
    el_n: float = 10.0    # near elbow (bend forward)
    sh_f: float = 0.0
    el_f: float = 10.0
    hip_n: float = 0.0
    kn_n: float = 0.0     # knee bend (lower leg goes back)
    hip_f: float = 0.0
    kn_f: float = 0.0
    bob: float = 0.0      # vertical body offset in r units (negative = up)
    head_tilt: float = 0.0  # nod: positive = chin down
    mood: str = "neutral"   # neutral|happy|shock|angry|smirk|calm
    mouth: float = 0.0      # 0 closed .. 1 open (talking / laughing)
    blink: bool = False
    hold: str = ""          # "", "case", "phone", "gun-shape-free" -> case / phone in near hand


def walk(p, amp=1.0):
    s = math.sin(2 * math.pi * p)
    c = math.cos(2 * math.pi * p)
    return Pose(lean=3 * amp, sh_n=-28 * s * amp, el_n=18 + 10 * amp, sh_f=28 * s * amp, el_f=18 + 10 * amp,
                hip_n=26 * s * amp, kn_n=8 + 32 * max(0, -c) * amp, hip_f=-26 * s * amp, kn_f=8 + 32 * max(0, c) * amp,
                bob=-0.07 * abs(math.sin(4 * math.pi * p)) * amp)


def run(p):
    q = walk(p, 1.6)
    q.lean = 14
    q.el_n = q.el_f = 75
    return q


def carry(p):
    q = walk(p, 0.8)
    q.sh_n, q.el_n = 30, 60
    q.sh_f, q.el_f = 26, 60
    q.hold = "case"
    return q


def stand(t=0.0):
    return Pose(sh_n=4 + 2 * math.sin(t * 3), sh_f=-4, el_n=12, el_f=12, bob=-0.01 * math.sin(t * 3))


def sit():
    return Pose(hip_n=85, kn_n=85, hip_f=80, kn_f=85, sh_n=55, el_n=40, sh_f=50, el_f=40)


def _pt(x, y, ang, length, facing):
    a = math.radians(ang)
    return x + math.sin(a) * length * facing, y + math.cos(a) * length


def _limb(cv, a, b, width, col):
    cv.line([a, b], col, width)
    cv.circle(a[0], a[1], width / 2, col)
    cv.circle(b[0], b[1], width / 2, col)


def figure(cv, x, y_feet, r, look: Look, pose: Pose, facing=1, show_name=False):
    """Draw a full figure whose feet touch y_feet (when legs are straight)."""
    thigh, shin = 1.25 * r, 1.2 * r
    upper, fore = 1.05 * r, 1.0 * r
    torso_len = 1.9 * r
    hip = (x, y_feet - thigh - shin + pose.bob * r)
    lean = pose.lean
    sh = _pt(hip[0], hip[1], 180 - lean, torso_len, facing)  # straight up, leaning forward
    neck = _pt(sh[0], sh[1], 180 - lean, 0.25 * r, facing)
    head_c = _pt(neck[0], neck[1], 180 - lean - pose.head_tilt * 0.3, 0.95 * r, facing)
    head_c = (head_c[0], head_c[1] + pose.head_tilt * 0.012 * r)

    def leg(hip_a, kn, col):
        k = _pt(hip[0], hip[1], hip_a, thigh, facing)
        f = _pt(k[0], k[1], hip_a - kn, shin, facing)
        _limb(cv, hip, k, 0.52 * r, col)
        _limb(cv, k, f, 0.46 * r, col)
        sx = f[0] + 0.22 * r * facing
        cv.ellipse((sx - 0.36 * r, f[1] - 0.05 * r, sx + 0.36 * r, f[1] + 0.3 * r), look.shoes)

    def arm(sh_a, el, col, near):
        e = _pt(sh[0], sh[1], sh_a, upper, facing)
        hnd = _pt(e[0], e[1], sh_a + el, fore, facing)
        _limb(cv, sh, e, 0.42 * r, col)
        _limb(cv, e, hnd, 0.38 * r, col)
        if near and pose.hold == "case":
            cw, ch = 1.5 * r, 1.0 * r
            cv.rect((hnd[0] - cw / 2, hnd[1] - 0.1 * r, hnd[0] + cw / 2, hnd[1] + ch), (150, 150, 158), INK, 3, r=8)
            cv.rect((hnd[0] - cw / 2, hnd[1] + ch * 0.45, hnd[0] + cw / 2, hnd[1] + ch * 0.55), (110, 110, 118))
        if near and pose.hold == "phone":
            cv.rect((hnd[0] - 0.22 * r, hnd[1] - 0.75 * r, hnd[0] + 0.22 * r, hnd[1] + 0.05 * r), (20, 20, 24), INK, 2, r=5)
            cv.rect((hnd[0] - 0.16 * r, hnd[1] - 0.68 * r, hnd[0] + 0.16 * r, hnd[1] - 0.02 * r), (120, 190, 255))
        cv.circle(hnd[0], hnd[1], 0.24 * r, WHITE, INK, 3)

    # far side (darker), torso, near side
    arm(pose.sh_f, pose.el_f, shade(look.jacket), False)
    leg(pose.hip_f, pose.kn_f, shade(look.pants))
    # torso as thick rounded segment
    _limb(cv, hip, sh, 1.35 * r, look.pants)
    mid = ((hip[0] + sh[0]) / 2, (hip[1] + sh[1]) / 2 - 0.1 * r)
    _limb(cv, (mid[0], mid[1] + 0.25 * r), sh, 1.45 * r, look.jacket)
    leg(pose.hip_n, pose.kn_n, look.pants)
    head(cv, head_c[0], head_c[1], r, look, pose, facing)
    arm(pose.sh_n, pose.el_n, look.jacket, True)
    if show_name and look.name:
        name_tag(cv, head_c[0] - 1.4 * r, head_c[1] - 2.9 * r, look.name)
    return head_c


def head(cv, x, y, r, look, pose, facing):
    skin = (34, 34, 38) if look.mask else look.skin
    if look.hair and not look.mask:
        cv.circle(x - 0.08 * r * facing, y - 0.12 * r, r * 1.04, look.hair)
    cv.circle(x, y, r, skin, INK, 4)
    ex = x + 0.28 * r * facing
    ey = y - 0.02 * r
    if look.mask:  # balaclava eye slit
        cv.rect((ex - 0.45 * r, ey - 0.22 * r, ex + 0.45 * r, ey + 0.2 * r), WHITE, r=10)
    gap = 0.34 * r
    for k in (0, 1):
        exk = ex + (k - 0.5) * gap
        if pose.blink:
            cv.line([(exk - 0.09 * r, ey), (exk + 0.09 * r, ey)], INK, 5)
        elif pose.mood == "zombie":
            cv.circle(exk, ey, 0.11 * r, (250, 250, 220), INK, 3)
        elif pose.mood == "shock":
            cv.circle(exk, ey, 0.12 * r, WHITE, INK, 3)
            cv.circle(exk, ey, 0.05 * r, INK)
        else:
            cv.ellipse((exk - 0.07 * r, ey - 0.13 * r, exk + 0.07 * r, ey + 0.13 * r), INK)
    if pose.mood in ("angry",):
        cv.line([(ex - 0.32 * r, ey - 0.3 * r), (ex + 0.25 * r, ey - 0.2 * r)], INK, 5)
    if not look.mask:
        mx, my = x + 0.25 * r * facing, y + 0.45 * r
        if pose.mouth > 0.05 or pose.mood == "shock":
            o = max(pose.mouth, 0.5 if pose.mood == "shock" else 0)
            cv.ellipse((mx - 0.17 * r, my - 0.06 * r, mx + 0.17 * r, my + (0.06 + 0.22 * o) * r), (90, 20, 26), INK, 3)
        elif pose.mood in ("happy", "smirk"):
            a0, a1 = (20, 160) if pose.mood == "happy" else (30, 110)
            cv.arc((mx - 0.22 * r, my - 0.22 * r, mx + 0.22 * r, my + 0.12 * r), a0, a1, INK, 5)
        else:
            cv.line([(mx - 0.12 * r, my), (mx + 0.12 * r, my)], INK, 4)
    if look.hat:
        if look.hat_kind == "guard":
            cv.d.chord(cv.s((x - r, y - 1.15 * r, x + r, y + 0.5 * r)), 180, 360, fill=look.hat)
            cv.rect((x - r * 0.4 + 0.5 * r * facing, y - 0.45 * r, x + r * 0.4 + 0.9 * r * facing, y - 0.3 * r),
                    shade(look.hat), r=6)
            cv.rect((x - 0.15 * r, y - 0.95 * r, x + 0.15 * r, y - 0.7 * r), (230, 190, 70), r=4)
        elif look.hat_kind == "helmet":
            cv.d.chord(cv.s((x - 1.08 * r, y - 1.25 * r, x + 1.08 * r, y + 0.45 * r)), 180, 360, fill=look.hat)
            cv.rect((x - 1.15 * r, y - 0.42 * r, x + 1.15 * r, y - 0.28 * r), shade(look.hat), r=6)
        elif look.hat_kind == "beanie":
            cv.d.chord(cv.s((x - 1.02 * r, y - 1.2 * r, x + 1.02 * r, y + 0.55 * r)), 180, 360, fill=look.hat)
            cv.rect((x - 1.05 * r, y - 0.45 * r, x + 1.05 * r, y - 0.25 * r), shade(look.hat, 1.2), r=6)
        else:  # cap with visor towards facing
            cv.d.chord(cv.s((x - r, y - 1.1 * r, x + r, y + 0.45 * r)), 180, 360, fill=look.hat)
            vx = x + 0.55 * r * facing
            cv.rect((min(vx, vx + 0.75 * r * facing), y - 0.4 * r, max(vx, vx + 0.75 * r * facing), y - 0.26 * r),
                    shade(look.hat), r=6)


def name_tag(cv, x, y, text, accent=(255, 61, 127)):
    import scenes as S  # bankraub/scenes
    from PIL import ImageFont
    f = S.font(34, "Black")
    w = cv.d.textlength(text, font=ImageFont.truetype(f.path, f.size * S.SS)) / S.SS + 30
    cv.rect((x, y, x + w, y + 58), (20, 24, 26, 235), WHITE, 3, r=8)
    cv.rect((x, y + 52, x + w, y + 58), accent)
    cv.text((x + 15, y + 10), text, f, WHITE)
