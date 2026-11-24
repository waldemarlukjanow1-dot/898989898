"""Video 4 – „Bildschirm kaputt?“ (vierte Wand + Zeitumkehr).

0.0–3.3 s  Pendel-Welle von oben: 16 glänzende Kugeln schwingen, eine Schlangenform entsteht, jede Kugel spielt einen Ton.
3.3–3.6 s  die mittlere Kugel schwingt plötzlich AUF DICH ZU ...
3.6 s      ... und lässt das Display zersplittern (Risse wachsen, Scherben fallen heraus -> schwarzes Loch).
6.2–8.0 s  Zurückspulen: Scherben fliegen zurück, Risse schließen sich, Bild und Ton laufen rückwärts
           bis exakt zum ersten Bild -> nahtloser Loop.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from common import W, H, SR, DUR, Track, encode, t_axis

FPS = 30
NB = 16
YS = np.linspace(330, 1470, NB)
A = 360.0
FREQ = (12 + np.arange(NB)) / 24.0                 # pendulum-wave frequencies (Hz)
HIT_N, T_GO, T_HIT, T_FALL, T_REW = 8, 3.3, 3.6, 4.3, 6.2
PENTA = [261.6, 293.7, 329.6, 392.0, 440.0]


def tc_of(t):
    """content time for display time t (forward, then a rewind that lands exactly on 0)."""
    if t < T_REW:
        return t
    u = (t - T_REW) / (DUR - T_REW)
    e = u * u * (3 - 2 * u)
    return T_REW * (1 - e)


def ball_x(n, tc):
    return 540 + A * math.cos(2 * math.pi * FREQ[n] * tc)


def sprite(col, r):
    S = 4
    im = Image.new("RGBA", (int(4 * r * S), int(4 * r * S)), (0, 0, 0, 0))
    c = 2 * r * S
    d = ImageDraw.Draw(im)
    for k in range(40):                              # glossy sphere: dark rim -> bright centre offset to the top-left
        f = k / 40
        rr = r * S * (1 - f)
        ox, oy = -0.35 * r * S * f, -0.35 * r * S * f
        cc = tuple(int(v * (0.45 + 0.75 * f) + 255 * max(0, f - 0.8) * 2.5) for v in col)
        d.ellipse((c + ox - rr, c + oy - rr, c + ox + rr, c + oy + rr), fill=tuple(min(255, x) for x in cc) + (255,))
    return im.resize((int(4 * r), int(4 * r)), Image.LANCZOS)


def hue(h):
    import colorsys
    return tuple(int(v * 255) for v in colorsys.hsv_to_rgb(h, 0.75, 1.0))


R0 = 30
SPR = [sprite(hue(0.95 - n / NB * 0.85), R0) for n in range(NB)]
BG = np.zeros((H, W, 3), np.float32)
_y = np.linspace(0, 1, H)[:, None]
BG[:] = (np.array([18, 16, 40]) * (1 - _y) + np.array([46, 18, 52]) * _y)[:, None, :]


def scene(tc):
    im = Image.fromarray(BG.astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im)
    d.line([(540, 250), (540, 1550)], fill=(90, 90, 120), width=6)                      # rail (pivots)
    top = None
    for n in range(NB):
        x, y, r, spr = ball_x(n, tc), YS[n], R0, SPR[n]
        if n == HIT_N and T_GO <= tc < T_HIT + 0.05:
            u = min(1.0, (tc - T_GO) / (T_HIT - T_GO))
            top = (x, y, 1 + 9 * u ** 2.2, spr)                                         # flies towards the viewer
            continue
        d.line([(540, y), (x, y)], fill=(150, 150, 180, 120), width=2)                   # string
        im.alpha_composite(spr, (int(x - 2 * r), int(y - 2 * r)))
    if top:
        x, y, s, spr = top
        big = spr.resize((int(spr.width * s), int(spr.height * s)), Image.LANCZOS)
        im.alpha_composite(big, (int(x - big.width / 2), int(y - big.height / 2)))
    return np.asarray(im.convert("RGB"), np.float32)


# ------------------------------------------------------------------ crack pattern (precomputed)
rng = np.random.default_rng(11)
P = np.array([ball_x(HIT_N, T_HIT), YS[HIT_N]])
RAYS = []
for k in range(17):
    a = 2 * math.pi * k / 17 + rng.uniform(-0.15, 0.15)
    pts, p, ang, L = [P.copy()], P.copy(), a, 0.0
    while 0 <= p[0] < W and 0 <= p[1] < H and L < 2200:
        ang += rng.uniform(-0.22, 0.22)
        ang = a + np.clip(ang - a, -0.35, 0.35)
        step = rng.uniform(18, 40)
        p = p + step * np.array([math.cos(ang), math.sin(ang)])
        L += step
        pts.append(p.copy())
    RAYS.append(np.array(pts))
RINGS = []
for rad in (60, 130, 230, 360, 520):
    seg = []
    for k in range(len(RAYS)):
        if rng.uniform() < 0.72:
            def at(ray, rr):
                d_ = np.linalg.norm(ray - P, axis=1)
                i = int(np.argmin(np.abs(d_ - rr)))
                return ray[i]
            a_, b_ = at(RAYS[k], rad * rng.uniform(0.9, 1.1)), at(RAYS[(k + 1) % len(RAYS)], rad * rng.uniform(0.9, 1.1))
            mid = (a_ + b_) / 2 + rng.normal(0, 6, 2)
            seg.append(np.array([a_, mid, b_]))
    RINGS.append((rad, seg))
yy, xx = np.mgrid[0:H, 0:W]
ANG = (np.arctan2(yy - P[1], xx - P[0]) % (2 * np.pi))
RAD = np.hypot(yy - P[1], xx - P[0])
ray_ang = np.sort([(math.atan2(r[min(4, len(r) - 1), 1] - P[1], r[min(4, len(r) - 1), 0] - P[0])) % (2 * np.pi) for r in RAYS])
SECTOR = np.searchsorted(ray_ang, ANG) % len(ray_ang)
RING = np.digitize(RAD, [60, 130, 230, 360, 520])
LABEL = SECTOR * 6 + RING
NL = LABEL.max() + 1
OFF = rng.integers(-5, 6, (NL, 2))                 # refraction offset per shard
TINT = rng.uniform(0.82, 1.12, NL)
FALL = [l for l in range(NL) if l % 6 in (0, 1, 2) and rng.uniform() < 0.6]   # shards near the impact fall out
FALL_V = {l: (rng.uniform(-80, 80), rng.uniform(-60, 40), rng.uniform(-200, 200)) for l in FALL}


def crack(img, tc):
    age = tc - T_HIT
    if age < 0:
        return img
    grow = min(1.0, age / 0.18)
    # refraction: every shard shows the image slightly displaced and tinted
    oy = np.clip(yy + OFF[LABEL, 1] * grow, 0, H - 1).astype(np.int32)
    ox = np.clip(xx + OFF[LABEL, 0] * grow, 0, W - 1).astype(np.int32)
    out = img[oy, ox] * (1 + (TINT[LABEL][..., None] - 1) * grow)
    pil = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    # falling shards: cut out, move with gravity + rotation, leave a black hole behind
    if tc > T_FALL:
        ft = tc - T_FALL
        hole = np.isin(LABEL, FALL)
        src = pil.copy()
        arr = np.asarray(pil).copy()
        arr[hole] = (4, 4, 6)
        pil = Image.fromarray(arr)
        for l in FALL:
            m = LABEL == l
            ys, xs = np.where(m)
            if len(ys) < 30:
                continue
            x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
            piece = src.crop((x0, y0, x1, y1)).convert("RGBA")
            mask = Image.fromarray((m[y0:y1, x0:x1] * 255).astype(np.uint8))
            piece.putalpha(mask)
            vx, vy, va = FALL_V[l]
            piece = piece.rotate(va * ft, expand=True, resample=Image.BICUBIC)
            dx = vx * ft
            dy = vy * ft + 0.5 * 2600 * ft * ft
            pil.paste(piece, (int(x0 + dx - (piece.width - (x1 - x0)) / 2), int(y0 + dy - (piece.height - (y1 - y0)) / 2)), piece)
    d = ImageDraw.Draw(pil, "RGBA")
    reach = 2600 * grow
    for ray in RAYS:
        dist = np.linalg.norm(ray - P, axis=1)
        pts = [tuple(p) for p, dd in zip(ray, dist) if dd <= reach]
        if len(pts) > 1:
            d.line(pts, fill=(0, 0, 0, 120), width=4)
            d.line(pts, fill=(255, 255, 255, 230), width=2)
    for rad, segs in RINGS:
        if rad <= reach * 0.4:
            for sgm in segs:
                d.line([tuple(p) for p in sgm], fill=(255, 255, 255, 200), width=2)
    d.ellipse((P[0] - 26, P[1] - 26, P[0] + 26, P[1] + 26), fill=(255, 255, 255, int(170 * grow)))      # crushed spot
    if age < 0.12:                                                                                      # impact flash
        d.rectangle((0, 0, W, H), fill=(255, 255, 255, int(200 * (1 - age / 0.12))))
    return np.asarray(pil, np.float32)


def frame(i):
    t = i / FPS
    tc = tc_of(t)
    img = crack(scene(tc), tc)
    if t >= T_REW:                                         # rewind look: desaturation + scan lines + icon, fades out
        k_ = min(1.0, (DUR - t) / 0.3)
        g = img.mean(2, keepdims=True)
        img = img * (1 - 0.25 * k_) + g * 0.25 * k_
        img[::4] *= 1 - 0.14 * k_
        pil = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(pil, "RGBA")
        for k in range(2):
            x = 80 + k * 46
            d.polygon([(x + 40, 300), (x + 40, 360), (x, 330)], fill=(255, 255, 255, int(255 * k_)))
        img = np.asarray(pil, np.float32)
    return np.clip(img, 0, 255).astype(np.uint8)


def sound(path):
    """Build the forward sound for content time 0..T_REW, then read it through tc_of() -> the rewind is the
    same audio running backwards (pitch rises like a tape), ending exactly at sample 0 -> seamless loop."""
    fwd = Track()
    r = np.random.default_rng(5)
    for n in range(NB):                                     # each ball 'plinks' when it crosses the rail
        f = PENTA[n % 5] * 2 ** (n // 5)
        k = 0
        while True:
            tc = (0.25 + 0.5 * k) / FREQ[n]
            if tc > T_REW:
                break
            if not (n == HIT_N and tc > T_GO):
                tk = t_axis(0.4)
                fwd.add(np.sin(2 * np.pi * f * tk) * np.exp(-tk * 9) * np.minimum(1, tk / 0.003), tc, 0.10,
                        (n / NB - 0.5) * 0.8)
            k += 1
    tk = t_axis(0.3)
    fwd.add(np.sin(2 * np.pi * np.cumsum(180 + 900 * (tk / 0.3) ** 2) / SR) * (tk / 0.3) ** 2, T_GO, 0.4)   # swoosh
    tk = t_axis(1.5)
    crack_s = r.standard_normal(len(tk)) * np.exp(-tk * 14) * 1.4
    crack_s += np.sin(2 * np.pi * np.cumsum(70 * np.exp(-tk * 6) + 40) / SR) * np.exp(-tk * 5) * 1.2
    for _ in range(40):                                     # sharp glass ticks inside the crack
        i0 = int(r.uniform(0, 0.25) * SR)
        crack_s[i0:i0 + 200] += r.standard_normal(200) * 2 * np.exp(-np.arange(200) / 40)
    fwd.add(crack_s, T_HIT, 1.0)
    for _ in range(26):                                     # shards falling: tinkles
        tk = t_axis(0.25)
        fwd.add(np.sin(2 * np.pi * r.uniform(2500, 6500) * tk) * np.exp(-tk * 30), T_FALL + r.uniform(0, 1.6), 0.15,
                r.uniform(-0.7, 0.7))
    L = int(DUR * SR)
    tdisp = np.arange(L) / SR
    tcs = np.array([tc_of(x) for x in tdisp[::48]])
    tcs = np.interp(tdisp, tdisp[::48], tcs)
    src_i = np.clip(tcs * SR, 0, L - 1)
    out = Track()
    out.L = np.interp(src_i, np.arange(L), fwd.L)
    out.R = np.interp(src_i, np.arange(L), fwd.R)
    out.save(path, reverb=0.15)


if __name__ == "__main__":
    sound("build/v4.wav")
    encode(frame, FPS, "build/v4.wav", "output/video4_bildschirm_kaputt.mp4")
