"""Video 5 – „Unmögliche Wellen“ (flüssiges Chrom + Zeitumkehr).

Die Wellengleichung ist zeitumkehrbar. Wir starten (vorwärts) mit einem Herz aus Wellen, rechnen 4 s und spielen
das Ergebnis als Palindrom: 0–4 s rückwärts (chaotische Wellen laufen auf unmögliche Weise zu einem perfekten Herz
zusammen), 4–8 s vorwärts (das Herz zerfließt wieder). Bild 0 == Bild 8 -> perfekter Loop. Ton ebenso (Palindrom).
"""
import math

import numpy as np
from scipy.ndimage import zoom

from common import W, H, SR, DUR, Track, encode, t_axis

FPS = 30
GW, GH = 360, 640
HALF = int(DUR * FPS / 2)            # 120 frames per half
STEPS = 16
C2 = 0.2


def heart_field():
    t = np.linspace(0, 2 * np.pi, 2000)
    hx = 16 * np.sin(t) ** 3
    hy = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    s = 9.5
    px, py = GW / 2 + hx * s, GH * 0.47 + hy * s
    yy, xx = np.mgrid[0:GH, 0:GW].astype(np.float32)
    d = np.full((GH, GW), 1e9, np.float32)
    for k in range(0, len(t), 4):
        d = np.minimum(d, (xx - px[k]) ** 2 + (yy - py[k]) ** 2)
    return np.exp(-d / (2 * 5.0 ** 2)) * 14.0


def simulate():
    h = heart_field()
    hp = h.copy()                                   # zero initial velocity
    frames = [h.copy()]
    for f in range(HALF):
        for _ in range(STEPS):
            p = np.pad(h, 1, mode="edge")           # reflective walls -> rich interference, reversible
            lap = p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:] - 4 * h
            hn = 2 * h - hp + C2 * lap
            hp, h = h, hn
        frames.append(h.copy())
    return frames


FR = simulate()
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
VIGN = np.clip(1.15 - np.hypot((xx - 540) / 700, (yy - 900) / 1100), 0, 1)


def shade(h):
    hh = zoom(h, 3, order=3)
    gy, gx = np.gradient(hh)
    k = 1.6
    nx, ny, nz = -gx * k, -gy * k, np.ones_like(hh)
    inv = 1 / np.sqrt(nx * nx + ny * ny + nz * nz)
    nx, ny, nz = nx * inv, ny * inv, nz * inv
    rx, ry, rz = 2 * nz * nx, 2 * nz * ny, 2 * nz * nz - 1          # reflection of a view straight down
    az = np.arctan2(ry, rx)
    elev = np.clip(1 - rz, 0, 1)                                       # 0 = zenith (flat) ... 1 = horizon
    hue = (az / (2 * np.pi) + 0.5)
    band = np.clip(elev * 5.0, 0, 1) ** 0.8
    r_ = 0.5 + 0.5 * np.cos(2 * np.pi * (hue + 0.00))
    g_ = 0.5 + 0.5 * np.cos(2 * np.pi * (hue + 0.33))
    b_ = 0.5 + 0.5 * np.cos(2 * np.pi * (hue + 0.67))
    grad = (yy / H)[..., None]
    base = (np.array([0.22, 0.23, 0.32]) * (1 - grad) + np.array([0.05, 0.05, 0.10]) * grad) * (0.55 + 0.45 * VIGN[..., None])   # silver chrome
    col = base * (1 - band[..., None]) + np.stack([r_, g_, b_], -1) * band[..., None] * (0.75 + 0.5 * elev[..., None])
    L = np.array([-0.35, -0.45, 0.82])
    L /= np.linalg.norm(L)
    spec = np.clip(rx * L[0] + ry * L[1] + rz * L[2], 0, 1) ** 220 * 1.6                      # sharp highlights
    col = col + spec[..., None]
    return np.clip(col * 255, 0, 255).astype(np.uint8)


def frame(i):
    k = HALF - i if i < HALF else i - HALF          # palindrome: reverse into the heart, then forward
    return shade(FR[k])


def sound(path):
    half = int(DUR / 2 * SR)
    fwd = np.zeros(half)
    r = np.random.default_rng(7)
    t = np.arange(half) / SR
    chord = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((130.8, 1), (196.0, 0.7), (261.6, 0.6), (329.6, 0.5), (523.3, 0.25)))
    fwd += chord * np.exp(-t * 0.9) * 0.6
    fwd += sum(np.sin(2 * np.pi * f * t) for f in (1046.5, 1318.5, 1568.0)) * np.exp(-t * 2.5) * 0.12   # shimmer
    for _ in range(18):                                                   # liquid bloops
        t0 = r.uniform(0.2, 3.8)
        tk = t_axis(0.18)
        f0 = r.uniform(300, 700)
        b = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 1.5 * tk / 0.18)) / SR) * np.exp(-tk * 25)
        i0 = int(t0 * SR)
        fwd[i0:i0 + len(b)] += b[: half - i0] * 0.12
    from scipy.signal import fftconvolve
    tr_ = t_axis(1.8)
    ir = r.standard_normal(len(tr_)) * np.exp(-tr_ * 2.2)
    ir /= np.sqrt((ir ** 2).sum())
    fwd = fwd * 0.6 + fftconvolve(fwd, ir)[:half] * 0.4
    full = np.concatenate([fwd[::-1], fwd])                               # reverse swell into the heart, then decay
    tr = Track()
    tr.L, tr.R = full.copy(), full.copy()
    tr.save(path)


if __name__ == "__main__":
    sound("build/v5.wav")
    encode(frame, FPS, "build/v5.wav", "output/video5_unmoegliche_wellen.mp4")
