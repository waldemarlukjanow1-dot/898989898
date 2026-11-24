"""Bounce 2.0 – Video 3 „Bounce-Welle“: mehrere Bälle, perfekte Synchronisation.

9 glänzende Keramikkugeln in einer Reihe. Kugel i springt in 8 s genau (4+i)-mal (Periode 8/(4+i) s, Sprunghöhe ~ T²).
t=0: alle landen gleichzeitig (Akkord) -> Wellen, Treppen, Spiralen entstehen -> t=4: gerade/ungerade Gruppen im
Wechsel -> t=8: wieder alle zusammen = Bild 0 (Loop). Jede Kugel hat einen eigenen Ton (Kalimba, Pentatonik).
Kamera: leicht erhöht, schräg von vorne, ganz langsames Schwenken (periodisch).
"""
import colorsys
import math
import sys

import numpy as np

import kit
import rt

FPS = 60
N = 9
R_B = 0.26
SP = 0.72
ANG = 2 * np.pi * np.arange(N) / N - np.pi / 2            # ring; tallest ball at the back
RING = 0.95
COUNTS = 4 + np.arange(N)
PER = kit.DUR / COUNTS
G = 5.2
HGT = G * PER ** 2 / 8                       # apex height above rest
COLS = [colorsys.hsv_to_rgb((0.98 - k / N) % 1, 0.85, 0.95) for k in range(N)]
PENTA = [261.6, 293.7, 329.6, 392.0, 440.0, 523.3, 587.3, 659.3, 784.0]


def env(d):
    return rt.studio_env(d, top=(0.006, 0.007, 0.012), horizon=(0.025, 0.027, 0.04),
                         boxes=[((-0.5, 1.2, 0.6), 0.35, (1, 1, 1), 2.4), ((0.8, 0.9, -0.4), 0.25, (0.6, 0.8, 1.0), 1.6)])


LIGHTS = [((-0.4, 1.0, 0.55), (1.0, 0.97, 0.92), 6.0), ((0.6, 0.5, -0.3), (0.25, 0.3, 0.45), 4.0)]


def balls(t):
    out = []
    for i in range(N):
        T = PER[i]
        s = t % T
        v0 = G * T / 2
        y = v0 * s - 0.5 * G * s * s
        vy = v0 - G * s
        dc = min(s, T - s)
        sy = 1 - 0.2 * max(0.0, 1 - dc / 0.04) ** 2 if dc < 0.04 else 1 + 0.06 * abs(vy) / v0
        cy = R_B * sy if dc < 0.04 else R_B + y
        out.append(rt.Ball((RING * math.cos(ANG[i]), cy, RING * math.sin(ANG[i])), R_B, "ceramic", color=COLS[i], sy=sy))
    return out


def frame(i):
    t = i / FPS
    sc = rt.Scene(balls(t), rt.Floor(0, "wet", (0.035, 0.037, 0.05)), env, LIGHTS, ambient=0.12, floor_reflect=0.6)
    a = 0.22 * math.sin(2 * math.pi * t / kit.DUR)          # slow periodic swing of the camera
    o, d = rt.camera_rays((7.2 * math.sin(a), 3.9, 7.2 * math.cos(a)), (0, 0.95, 0), 38)
    return sc.render(o, d, depth=2, exposure=1.05)


def sound(path):
    tr = kit.Track()
    for i in range(N):
        for k in range(COUNTS[i]):
            t0 = k * PER[i]
            tr.add(kit.impact("kalimba", PENTA[i], vel=1.0, dur=1.2, seed=i * 31 + k), t0, 0.2, 0.8 * math.cos(ANG[i]))
            tr.add(kit.impact("ceramic", 900 + 60 * i, vel=0.5, dur=0.2, seed=k), t0, 0.12, 0.8 * math.cos(ANG[i]))
    tr.save(path, reverb=0.25)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/bounce3_welle.mp4"
    sound("build/b3.wav")
    kit.encode(frame, FPS, "build/b3.wav", out, workers=4, bitrate="12M")
