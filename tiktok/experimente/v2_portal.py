"""Video 2 – „Endlos-Portal“ (unendlicher Zoom + Shepard-Ton, mathematisch perfekter Loop).

Jede Bildzeile ist eine Funktion von (log r, Winkel). Wir fallen in 8 s durch genau 4 Ebenen; Farben und Formen haben
Periode 4, die Drehung beträgt genau eine Blütenblatt-Periode -> Bild 8 s == Bild 0 s. Der Ton ist eine Shepard-Risset-
Glissando, die scheinbar endlos steigt und nach 8 s exakt um eine Oktave versetzt identisch ist.
"""
import colorsys

import numpy as np

from common import W, H, SR, DUR, Track, encode, t_axis

FPS = 60
K = 1.9                       # scale factor between layers
LAYERS = 4                    # layers passed per loop (pattern period)
PET = 8                       # petals per ring
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
CX, CY = 540.0, 900.0
dx, dy = xx - CX, yy - CY
RAD = np.sqrt(dx * dx + dy * dy) + 1e-3
PHI = np.arctan2(dy, dx)
LOGR = np.log(RAD / 60.0) / np.log(K)
PAL = np.array([colorsys.hsv_to_rgb(h, 0.9, 1.0) for h in (0.92, 0.55, 0.12, 0.75)], np.float32)   # period 4


def frame(i):
    t = i / FPS
    s = LAYERS * t / DUR
    L = LOGR - s
    n = np.floor(L)
    f = L - n
    spin = 2 * np.pi / PET * (t / DUR)                        # exactly one petal period per loop
    ph = PHI + n * (np.pi / PET) + spin                       # alternate layers offset by half a petal
    petal = 0.5 + 0.5 * np.cos(PET * ph)
    shape = np.clip(1.0 - np.abs(f - 0.5) * 2.0 / (0.25 + 0.75 * petal), 0, 1) ** 1.5   # petal-shaped rings
    edge = np.exp(-((f - 0.5 - 0.42 * (petal - 0.5)) ** 2) / 0.002)                   # bright rim lines
    idx = (n.astype(np.int64) % LAYERS)
    col = PAL[idx]
    col2 = PAL[(idx + 1) % LAYERS]
    mixc = col * (1 - f[..., None]) + col2 * f[..., None]
    depth = np.clip((RAD - 20) / 240.0, 0, 1)[..., None]                  # far = dark centre
    glow = np.exp(-RAD / 90.0)[..., None] * np.array([1.0, 0.85, 0.95], np.float32) * 0.9
    pear = (np.cos(2 * PET * (ph + np.pi / (2 * PET))) > 0.93) * np.exp(-((f - 0.12) ** 2) / 0.0012)   # pearl ring
    img = mixc * (0.15 + 0.85 * shape[..., None]) * depth + edge[..., None] * 0.9 * depth + glow
    img = img + pear[..., None] * col2 * 1.3 * depth
    return np.clip(img * 255, 0, 255).astype(np.uint8)


def sound(path):
    """Shepard-Risset glissando: 8 octave-spaced sines rising, Gaussian loudness over log-frequency -> endless."""
    tr = Track()
    t = t_axis(DUR)
    out = np.zeros_like(t)
    for k in range(8):
        pos = k + t / DUR                                    # octave position, rises by exactly 1 per loop
        amp = np.exp(-((pos - 4.0) ** 2) / 3.0)
        # phase as a function of pos only (integral of 40*2^pos dt) -> partial k ends exactly where k+1 starts
        phase = 2 * np.pi * 40.0 * DUR / np.log(2) * 2 ** pos
        out += np.sin(phase) * amp
    tr.add(out, 0, 0.5)
    for k in range(LAYERS):                                  # a soft deep pulse each time a new layer is born
        tp = t_axis(1.5)
        tr.add(np.sin(2 * np.pi * 55 * tp) * np.exp(-tp * 3) + 0.3 * np.sin(2 * np.pi * 110 * tp) * np.exp(-tp * 5),
               k * DUR / LAYERS, 0.45)
    tr.save(path, reverb=0.3)


if __name__ == "__main__":
    sound("build/v2.wav")
    encode(frame, FPS, "build/v2.wav", "output/video2_endlos_portal.mp4")
