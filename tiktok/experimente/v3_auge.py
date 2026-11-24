"""Video 3 – „Der Schwarm sieht dich“ (Partikel-Assemblage + vierte Wand).

0.0 s  6.000 bunte Partikel wirbeln über den ganzen Bildschirm (was wird das?)
0.4–2.6 s  sie fließen in ein Raster und werden zu einem riesigen Auge (LED-Wand-Look)
2.7–4.3 s  das Auge schaut links, rechts ... dann DICH an
4.9 s  es blinzelt, 5.9 s die Pupille wird riesig
6.5–7.9 s  der Schwarm explodiert und wirbelt wieder -> nahtloser Loop (alles ist 8-s-periodisch)
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from common import W, H, SR, DUR, Track, encode, t_axis

FPS = 30
GX, GY = 84, 60                      # particle grid of the eye
X0, X1, Y0, Y1 = 40, 1040, 560, 1330
rng = np.random.default_rng(4)
gx, gy = np.meshgrid(np.linspace(X0, X1, GX), np.linspace(Y0, Y1, GY))
G = np.stack([gx.ravel(), gy.ravel()], 1)
N = len(G)
# swarm = a rotating spiral galaxy (3 arms); one full turn per loop -> periodic
RHO = 40 + 560 * np.sqrt(rng.uniform(0, 1, N))
ARM = rng.integers(0, 3, N)
TH0 = ARM * 2 * np.pi / 3 + RHO * 0.0085 + rng.normal(0, 0.28, N) * (1.2 - RHO / 700)
GAL_C = np.array([540.0, 930.0])
HUE = (0.55 + RHO / 700 * 0.6 + ARM * 0.07) % 1
DIST = np.linalg.norm((G - (540, 945)) / (500, 385), axis=1)
DELAY = 0.15 + 0.9 * np.clip(DIST, 0, 1.4) / 1.4 + rng.uniform(0, 0.25, N)


def hsv(h, s, v):
    h = (h % 1) * 6
    i = np.floor(h).astype(int) % 6
    f = h - np.floor(h)
    p, q, t_ = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    r = np.choose(i, [v, q, p, p, t_, v])
    g = np.choose(i, [t_, v, v, q, p, p])
    b = np.choose(i, [p, p, t_, v, v, q])
    return np.stack([r, g, b], 1)


RAINBOW = hsv(HUE, 0.85, 1.0) * 255
OVAL = np.clip(1.25 - DIST, 0, 1) ** 0.8          # soft oval: the eye floats in the dark, no square block


def ease(u):
    u = np.clip(u, 0, 1)
    return u * u * (3 - 2 * u)


def gaze(t):
    """(gx, gy, blink 0..1, pupil scale)"""
    keys = [(0, 0, 0), (2.6, 0, 0), (3.0, -0.55, 0.05), (3.4, -0.55, 0.05), (3.8, 0.55, -0.05), (4.2, 0.55, -0.05),
            (4.5, 0.0, 0.0), (8.0, 0.0, 0.0)]
    for (ta, xa, ya), (tb, xb, yb) in zip(keys[:-1], keys[1:]):
        if ta <= t <= tb:
            u = float(ease((t - ta) / (tb - ta)))
            gx_, gy_ = xa + (xb - xa) * u, ya + (yb - ya) * u
            break
    blink = float(max(0.0, 1 - abs(t - 5.0) / 0.16)) if 4.84 < t < 5.16 else 0.0
    pupil = 0.30 - 0.06 * float(ease((t - 4.4) / 0.3)) + 0.34 * float(ease((t - 5.8) / 0.5))
    return gx_, gy_, blink, pupil


def eye_colors(t):
    """Render the eye at grid resolution (supersampled) and return the colour of every particle."""
    S = 6
    w, h = GX * S, GY * S
    im = Image.new("RGB", (w, h), (232, 176, 150))                           # skin
    d = ImageDraw.Draw(im)
    gx_, gy_, blink, pupil = gaze(t)
    cx, cy = w / 2, h / 2 + 0.03 * h
    ew, eh = 0.47 * w, 0.40 * h * (1 - 0.97 * blink)
    d.ellipse((cx - ew - 18, cy - 0.40 * h - 30, cx + ew + 18, cy + 0.40 * h + 10), fill=(205, 140, 120))  # shading
    # sclera (almond shape)
    pts = [(cx + ew * math.cos(a), cy + eh * math.sin(a) * (1.0 if math.sin(a) > 0 else 1.15))
           for a in np.linspace(0, 2 * math.pi, 80)]
    d.polygon(pts, fill=(245, 243, 238))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    iris = Image.new("RGB", (w, h), (245, 243, 238))
    di = ImageDraw.Draw(iris)
    ix, iy, ir = cx + gx_ * 0.42 * w, cy + gy_ * 0.3 * h, 0.27 * h
    for k in range(30):                                                       # iris: radial gradient + streaks
        rr = ir * (1 - k / 30)
        c = (int(30 + 40 * k / 30), int(110 + 120 * k / 30), int(140 + 60 * k / 30))
        di.ellipse((ix - rr, iy - rr, ix + rr, iy + rr), fill=c)
    for a in np.linspace(0, 2 * math.pi, 48, endpoint=False):
        di.line([(ix + math.cos(a) * ir * 0.35, iy + math.sin(a) * ir * 0.35),
                 (ix + math.cos(a) * ir * 0.98, iy + math.sin(a) * ir * 0.98)], fill=(20, 70, 90), width=3)
    di.ellipse((ix - ir, iy - ir, ix + ir, iy + ir), outline=(15, 40, 55), width=8)
    pr = ir * pupil * 1.9
    di.ellipse((ix - pr, iy - pr, ix + pr, iy + pr), fill=(8, 8, 10))
    di.ellipse((ix - ir * 0.55, iy - ir * 0.6, ix - ir * 0.25, iy - ir * 0.3), fill=(255, 255, 255))   # highlight
    im.paste(iris, (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.line(pts[:41], fill=(60, 35, 30), width=10)                             # lower lid line
    d.line(pts[40:] + [pts[0]], fill=(40, 22, 20), width=16)                  # upper lid line
    for a in np.linspace(math.pi * 1.08, math.pi * 1.92, 14):                 # lashes
        x0, y0 = cx + ew * math.cos(a), cy + eh * 1.15 * math.sin(a)
        d.line([(x0, y0), (x0 + 30 * math.cos(a), y0 + 46 * math.sin(a) - 10)], fill=(30, 18, 16), width=7)
    sm = np.asarray(im.resize((GX, GY), Image.BOX), dtype=np.float32)
    return sm.reshape(-1, 3)


def state(t):
    w_in = ease((t - 0.4 - DELAY * 1.2) / 1.0)
    w_out = ease((t - 6.5 - (1.4 - np.clip(DIST, 0, 1.4)) * 0.25) / 1.0)
    w = w_in * (1 - w_out)
    th = TH0 + 2 * np.pi * t / DUR
    S = GAL_C + np.stack([np.cos(th) * RHO, np.sin(th) * RHO * 0.82], 1)
    bump = np.sin(np.pi * np.clip((t - 6.5) / 1.4, 0, 1)) ** 2
    out = (G - (540, 945)) / (np.linalg.norm(G - (540, 945), axis=1)[:, None] + 1) * 420 * bump
    pos = S * (1 - w[:, None]) + G * w[:, None] + out
    return pos, w


def frame(i):
    t = i / FPS
    pos, w = state(t)
    ec = eye_colors(t)
    col = RAINBOW * (1 - w[:, None]) + ec * (OVAL[:, None] * w[:, None])
    S = 2
    im = Image.new("RGB", (W * S, H * S), (6, 6, 10))
    d = ImageDraw.Draw(im)
    r = (5.0 + 1.6 * w) * S
    for (x, y), c, rr in zip(pos * S, col, r):
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(int(c[0]), int(c[1]), int(c[2])))
    small = im.resize((W, H), Image.BILINEAR)
    glow = small.resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(5)).resize((W, H), Image.BILINEAR)
    a = np.asarray(small, np.float32)
    g = np.asarray(glow, np.float32) * 0.9
    out = 255 - (255 - a) * (255 - g) / 255.0
    return np.clip(out, 0, 255).astype(np.uint8)


def sound(path):
    tr = Track()
    r = np.random.default_rng(2)
    t = t_axis(DUR)
    # swarm: swirling filtered noise, quieter while assembled
    env = np.clip(1 - np.clip((t - 1.0) / 1.5, 0, 1) + np.clip((t - 6.4) / 1.0, 0, 1), 0.08, 1)
    sw = np.convolve(r.standard_normal(len(t)), np.ones(30) / 30, "same") * (0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * t))
    tr.add(sw * env, 0, 0.5)
    for k in range(10):                                         # assembling: rising crystal notes
        tk = t_axis(0.6)
        f = 523.3 * 2 ** ([0, 2, 4, 7, 9, 12, 14, 16, 19, 21][k] / 12)
        tr.add(np.sin(2 * np.pi * f * tk) * np.exp(-tk * 6), 0.6 + k * 0.2, 0.12, (k % 3 - 1) * 0.4)
    for tt, pan in ((3.0, -0.6), (3.8, 0.6)):                    # eye moves: soft whooshes
        tk = t_axis(0.35)
        tr.add(np.convolve(r.standard_normal(len(tk)), np.ones(60) / 60, "same") * np.sin(np.pi * tk / 0.35) * 2, tt, 0.4, pan)
    for k in range(3):                                          # it looks at YOU: heartbeat
        tk = t_axis(0.3)
        hb = np.sin(2 * np.pi * 55 * tk) * np.exp(-tk * 18)
        tr.add(hb, 4.45 + k * 0.5, 1.0)
        tr.add(hb, 4.62 + k * 0.5, 0.7)
    tk = t_axis(0.12)                                           # blink: wet click
    tr.add(np.convolve(r.standard_normal(len(tk)), np.ones(4) / 4, "same") * np.exp(-tk * 50), 4.9, 0.6)
    tk = t_axis(0.8)                                            # pupil grows: low swell
    tr.add(np.sin(2 * np.pi * np.cumsum(70 - 30 * tk / 0.8) / SR) * np.sin(np.pi * tk / 0.8), 5.8, 0.6)
    tk = t_axis(1.2)                                            # burst
    tr.add(np.sin(2 * np.pi * np.cumsum(90 * np.exp(-tk * 4) + 30) / SR) * np.exp(-tk * 3) +
           np.convolve(r.standard_normal(len(tk)), np.ones(8) / 8, "same") * np.exp(-tk * 6) * 2, 6.55, 0.9)
    tr.save(path, reverb=0.25)


if __name__ == "__main__":
    sound("build/v3.wav")
    encode(frame, FPS, "build/v3.wav", "output/video3_schwarm_sieht_dich.mp4")
