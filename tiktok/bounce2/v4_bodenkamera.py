"""Bounce 2.0 – Video 4 „Bodenkamera“: neue Kamera + neue Umgebung.

Kamera liegt fast auf dem Boden (Froschperspektive, Weitwinkel), eine schwere Goldkugel kracht direkt vor der Linse auf.
Nasser schwarzer Boden spiegelt magenta/cyan Neon-Seitenlichter, Tiefenunschärfe (Fokus auf der Kugel).
Rhythmus: BUMM (großer Sprung 1.5 s) – tick (kleines Nachhüpfen 0.5 s) – 4 Zyklen = 8 s. Kamera schiebt sich langsam
seitlich und zurück (periodisch). Ton: schweres Metall (Glocken-Moden + Sub-Bass), Nachhüpfer leiser und heller.
"""
import math
import sys

import numpy as np

import kit
import rt

FPS = 60
R_B = 0.42
CYC = 2.0
BIG, SMALL = 1.5, 0.5
G = 9.0


def env(d):
    base = rt.studio_env(d, top=(0.03, 0.025, 0.02), horizon=(0.02, 0.018, 0.02),
                         boxes=[((-1.0, 0.35, -0.2), 0.34, (1.0, 0.15, 0.6), 3.5), ((1.0, 0.3, -0.25), 0.34, (0.1, 0.8, 1.0), 3.5),
                                ((0.0, 1.0, 0.1), 0.75, (1.0, 0.9, 0.7), 2.2), ((0.0, 0.2, 1.0), 0.5, (1.0, 0.85, 0.6), 1.2)])
    band = np.exp(-(d[:, 1] / 0.08) ** 2)[:, None] * np.array([0.5, 0.35, 0.2])      # warm glow on the horizon
    return base + band


LIGHTS = [((-0.9, 0.5, -0.1), (0.9, 0.15, 0.55), 6.0), ((0.9, 0.45, -0.2), (0.1, 0.7, 0.95), 6.0), ((0, 1, 0.3), (0.4, 0.38, 0.35), 4.0)]


def ball(t):
    s = t % CYC
    if s < BIG:
        T, u = BIG, s
    else:
        T, u = SMALL, s - BIG
    v0 = G * T / 2
    y = v0 * u - 0.5 * G * u * u
    vy = v0 - G * u
    contacts = [0.0, BIG, CYC]
    dc = min(abs(s - c) for c in contacts)
    near_big = min(abs(s - 0.0), abs(s - CYC)) < 0.05
    depth = 0.2 if near_big else 0.1
    if dc < 0.04:
        sy = 1 - depth * (1 - dc / 0.04) ** 2
        return R_B * sy, sy
    return R_B + y, 1 + 0.05 * abs(vy) / (G * BIG / 2)


def frame(i):
    t = i / FPS
    cy, sy = ball(t)
    b = rt.Ball((0, cy, 0), R_B, "gold", sy=sy)
    sc = rt.Scene([b], rt.Floor(0, "wet", (0.01, 0.01, 0.013)), env, LIGHTS, ambient=0.05, floor_reflect=1.0)
    ph = 2 * math.pi * t / kit.DUR
    cam = (0.55 * math.sin(ph), 0.14, 1.75 + 0.25 * math.cos(ph))
    o, d = rt.camera_rays(cam, (0, 0.95, 0), 66)
    img = sc.render(o, d, depth=2, exposure=1.2)
    tt, _ = sc.nearest(o, d)
    depth = np.where(np.isfinite(tt), tt, 40.0)
    focus = math.dist(cam, (0, cy, 0))
    return kit.depth_of_field(img, depth, focus, strength=1.6, max_blur=14)


def sound(path):
    tr = kit.Track()
    for k in range(4):
        t0 = k * CYC
        tr.add(kit.impact("metal", 196.0, vel=1.0, dur=2.5, seed=k), t0, 0.8)
        tb = kit.t_axis(0.6)
        tr.add(np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-tb * 18)) / kit.SR) * np.exp(-tb * 5), t0, 1.0)   # sub boom
        tr.add(kit.impact("metal", 392.0, vel=0.45, dur=1.2, seed=10 + k), t0 + BIG, 0.45)
    tr.save(path, reverb=0.3)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/bounce4_bodenkamera.mp4"
    sound("build/b4.wav")
    kit.encode(frame, FPS, "build/b4.wav", out, workers=4, bitrate="12M")
