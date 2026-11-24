"""Bounce 2.0 – Video 1 „Kristall“: neues Material.

Glaskugel (Brechung + Fresnel, leicht aquamarin) springt exakt 1x pro Sekunde auf einem schwarzen Spiegel.
Die Kamera umkreist sie in 8 s genau einmal (Loop). Farbige Softboxen werden in der Kugel gebrochen und gespiegelt.
Ton: Glas-Modalsynthese ("ting") + weicher Gewichts-Thump, Tonhöhe folgt einer ruhigen Pentatonik.
"""
import math
import sys

import numpy as np

import kit
import rt

FPS = 60
R_BALL = 0.5
APEX = 1.55
BOXES = [((-0.6, 1.4, 0.3), 0.30, (1.0, 1.0, 1.0), 3.0), ((0.9, 1.0, -0.2), 0.22, (0.2, 0.9, 1.0), 2.6),
         ((-0.9, 0.9, -0.6), 0.22, (1.0, 0.25, 0.7), 2.6), ((0.1, 1.2, -1.0), 0.26, (1.0, 0.7, 0.3), 1.8)]


def env(d):
    base = rt.studio_env(d, top=(0.004, 0.004, 0.007), horizon=(0.018, 0.018, 0.026), boxes=BOXES)
    az = np.arctan2(d[:, 0], d[:, 2]) / (2 * np.pi)
    band = np.exp(-(d[:, 1] / 0.12) ** 2)[:, None]                        # glowing pastel horizon ring
    ring = np.stack([0.5 + 0.5 * np.cos(2 * np.pi * (az + k / 3)) for k in range(3)], 1) * 0.55 + 0.25
    return base + band * ring * 0.6


LIGHTS = [((-0.6, 1.0, 0.3), (1.0, 0.98, 0.95), 10.0)]


def ball_state(t):
    c = math.floor(t)
    y, vy, _ = kit.hop(t, c, c + 1, R_BALL, R_BALL, APEX)
    sy = kit.squash(t, [c, c + 1], depth=0.16, width=0.045, stretch=0.05, vy=vy, vmax=4.0)
    y = max(y, R_BALL * sy)
    return y if sy >= 1 else R_BALL * sy, sy


def frame(i):
    t = i / FPS
    y, sy = ball_state(t)
    b = rt.Ball((0, y, 0), R_BALL, "glass", sy=sy, ior=1.52, tint=(0.82, 0.97, 0.98))
    sc = rt.Scene([b], rt.Floor(0, "mirror", tile=((0.05, 0.05, 0.06), (0.006, 0.006, 0.008), 0.5)), env, LIGHTS, ambient=0.05, floor_reflect=0.85)
    th = 2 * math.pi * t / kit.DUR
    o, d = rt.camera_rays((5.4 * math.sin(th), 1.25, 5.4 * math.cos(th)), (0, 1.0, 0), 34)
    return sc.render(o, d, depth=3, exposure=1.15)


def sound(path):
    tr = kit.Track()
    notes = [1568.0, 1760.0, 1975.5, 2349.3, 1975.5, 1760.0, 2093.0, 1760.0]      # calm glass melody, 8 bounces
    for k in range(8):
        s = kit.impact("glass", notes[k] / 2, vel=1.0, dur=2.5, seed=k)
        tr.add(s, k * 1.0, 0.35, 0.25 * math.sin(2 * math.pi * k / 8))         # pan follows the orbit
    tr.save(path, reverb=0.35)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/bounce1_kristall.mp4"
    sound("build/b1.wav")
    kit.encode(frame, FPS, "build/b1.wav", out, workers=4, bitrate="14M")
