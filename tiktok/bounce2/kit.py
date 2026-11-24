"""Bounce 2.0 – Physik-, Kamera- und Klang-Baukasten.

Physik: analytische Bounce-Bahnen. Jeder Aufprall liegt auf einem vorher festgelegten Zeitpunkt (Taktraster),
dazwischen exakte Wurfparabeln -> perfektes Timing, perfekte Loops. Squash & Stretch aus Aufprall/Geschwindigkeit.
Klang: Modalsynthese pro Material (Summe gedämpfter Eigenschwingungen) + Gewichts-Thump; Lautstärke ~ Aufprallgeschw.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "experimente"))
from common import Track, encode, t_axis, SR, DUR  # noqa: E402,F401

import rt  # noqa: E402


# ------------------------------------------------------------------ physics
def hop(t, t0, t1, y0, y1, apex=None):
    """Ballistic hop between contacts at t0 (height y0) and t1 (height y1); returns y(t), vy(t), g used."""
    T = t1 - t0
    if apex is None:
        apex = max(y0, y1) + 0.2
    # parabola through (t0,y0),(t1,y1) with maximum 'apex': solve for g and vy0
    # y = y0 + v t - g t^2/2 ; apex at tv = v/g with y0 + v^2/(2g) = apex
    a = np.sqrt(max(apex - y0, 1e-9))
    b = np.sqrt(max(apex - y1, 1e-9))
    tv = T * a / (a + b)
    g = 2 * (apex - y0) / tv ** 2
    v = g * tv
    s = t - t0
    return y0 + v * s - 0.5 * g * s * s, v - g * s, g


def squash(t, contacts, depth=0.22, width=0.06, stretch=0.06, vy=0.0, vmax=1.0):
    """Squash near a contact time, slight stretch while fast in the air."""
    sy = 1.0
    for c in contacts:
        u = abs(t - c) / width
        if u < 1:
            sy = min(sy, 1 - depth * (1 - u) ** 2)
    if sy >= 1.0:
        sy = 1 + stretch * min(1.0, abs(vy) / max(vmax, 1e-6))
    return sy


# ------------------------------------------------------------------ post: depth of field
def depth_of_field(img, depth, focus, strength=3.0, max_blur=12):
    """Cheap DOF: blend between sharp and 2 blurred versions by circle of confusion."""
    a = Image.fromarray(img)
    b1 = np.asarray(a.filter(ImageFilter.GaussianBlur(max_blur * 0.4)), np.float32)
    b2 = np.asarray(a.filter(ImageFilter.GaussianBlur(max_blur)), np.float32)
    s = np.asarray(img, np.float32)
    coc = np.clip(np.abs(1 / np.maximum(depth, 1e-3) - 1 / focus) * strength * focus, 0, 1).reshape(img.shape[:2])[..., None]
    w1 = np.clip(coc * 2, 0, 1)
    w2 = np.clip(coc * 2 - 1, 0, 1)
    out = s * (1 - w1) + b1 * w1
    out = out * (1 - w2) + b2 * w2
    return np.clip(out, 0, 255).astype(np.uint8)


# ------------------------------------------------------------------ sound: modal synthesis per material
MATERIALS = {
    #           mode ratios                       amps                    decay (1/s)              base thump(Hz, gain)
    "glass":   ([1.0, 2.32, 4.25, 6.63, 9.38], [1, .55, .3, .15, .08], [3.0, 5, 8, 12, 16], (180, 0.25)),
    "ceramic": ([1.0, 2.6, 4.1, 6.9], [1, .4, .2, .08], [18, 30, 45, 60], (150, 0.55)),
    "metal":   ([1.0, 2.76, 5.40, 8.93, 13.3], [1, .7, .45, .25, .12], [1.6, 2.2, 3.5, 5, 7], (70, 1.0)),
    "rubber":  ([1.0, 1.9], [1, .3], [40, 60], (110, 1.0)),
    "chrome":  ([1.0, 2.76, 5.40, 8.93], [1, .5, .3, .15], [4, 6, 9, 12], (120, 0.5)),
    "kalimba": ([1.0, 5.4, 2.0], [1, .25, .1], [5, 14, 7], (0, 0)),
}


def impact(material, f0, vel=1.0, dur=1.6, seed=0):
    ratios, amps, decs, (tf, tg) = MATERIALS[material]
    t = t_axis(dur)
    r = np.random.default_rng(seed)
    out = np.zeros_like(t)
    for q, a, dk in zip(ratios, amps, decs):
        detune = 1 + r.normal(0, 0.002)
        # harder hits excite the upper modes more
        out += a * (vel ** (0.5 + 0.4 * q / ratios[-1])) * np.sin(2 * np.pi * f0 * q * detune * t + r.uniform(0, 6.28)) * np.exp(-t * dk)
    if tg:
        out += tg * vel * np.sin(2 * np.pi * np.cumsum(tf * (1 + 1.5 * np.exp(-t * 40))) / SR) * np.exp(-t * 22)
    click = r.standard_normal(len(t)) * np.exp(-t * 900) * 0.25 * vel
    att = np.minimum(1, t / 0.0015)
    return (out + click) * att


def shepard_note(pc, dur=1.2, base=55.0, octaves=7, decay=3.0):
    """Shepard tone for pitch class pc (in octaves, any real number): octave-spaced partials, Gaussian loudness."""
    t = t_axis(dur)
    out = np.zeros_like(t)
    for k in range(octaves):
        pos = (k + pc) % octaves
        f = base * 2 ** pos
        a = np.exp(-((pos - octaves / 2) ** 2) / 2.0)
        out += a * np.sin(2 * np.pi * f * t)
    return out * np.exp(-t * decay) * np.minimum(1, t / 0.003)
