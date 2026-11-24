"""Bounce 2.0 – Video 5 „Endlose Treppe“: das radikalste Experiment.

Eine Chromkugel hüpft im Takt (2 Hüpfer/s) eine unendliche, schwebende Pastell-Treppe hinunter; die Kamera fährt
mit. Nach 16 Stufen ist alles wieder identisch (Farbzyklus 4) -> nahtloser Loop, der wie ein ewiger Abstieg wirkt.
Ton: jede Landung spielt einen Shepard-Ton, der 1/8 Oktave tiefer liegt als der vorige -> eine Tonleiter, die
scheinbar endlos fällt (nach 16 Schritten = 2 Oktaven -> identisch = Loop auch im Ton).
"""
import math
import sys

import numpy as np

import kit
import rt

FPS = 60
RUN, RISE = 1.0, 0.55
R_B = 0.3
TP = 0.5
STEPS = int(kit.DUR / TP)                           # 16
VX, VY = RUN / TP, -RISE / TP
COLORS = [(0.95, 0.92, 0.88), (0.95, 0.52, 0.55), (0.55, 0.74, 0.97), (0.62, 0.9, 0.72)]


def env(d):
    y = np.clip(d[:, 1:2], -1, 1)
    top = np.array([0.55, 0.65, 0.9])
    hor = np.array([1.0, 0.82, 0.72])
    low = np.array([0.45, 0.4, 0.6])
    col = np.where(y > 0, hor * (1 - y) + top * y, hor * (1 + y) + low * (-y))
    sun = np.clip((d @ rt.norm(np.array([-0.5, 0.7, 0.5]))), 0, 1) ** 60 * 4
    return col * 0.9 + sun[:, None] * np.array([1.0, 0.95, 0.85])


LIGHTS = [((-0.5, 1.0, 0.6), (0.95, 0.9, 0.85), 5.0)]


def ball(t):
    k = int(t // TP)
    s = t - k * TP
    x0, x1 = (k + 0.5) * RUN, (k + 1.5) * RUN
    y0, y1 = -k * RISE + R_B, -(k + 1) * RISE + R_B
    y, vy, _ = kit.hop(s, 0.0, TP, y0, y1, apex=y0 + 0.55)
    x = x0 + (x1 - x0) * s / TP
    dc = min(s, TP - s)
    if dc < 0.035:
        sy = 1 - 0.16 * (1 - dc / 0.035) ** 2
        yy = (y0 if s < TP / 2 else y1) - R_B + R_B * sy
        return (x, yy, 0.0), sy
    return (x, y, 0.0), 1 + 0.05 * abs(vy) / 5


def frame(i):
    t = i / FPS
    c, sy = ball(t)
    b = rt.Ball(c, R_B, "chrome", color=(0.95, 0.95, 1.0), sy=sy)
    ax, ay = 0.5 * RUN + VX * t, R_B + VY * t                   # camera anchor glides along the stairs
    k0 = int(math.floor(ax / RUN))
    st = rt.Stairs(RUN, RISE, kmin=k0 - 3, kmax=k0 + 13, colors=COLORS, mat="ceramic_floor", width=1.25, thick=0.3)
    sc = rt.Scene([b], st, env, LIGHTS, ambient=0.45, floor_reflect=0.35)
    o, d = rt.camera_rays((ax - 2.3, ay + 2.6, 0.5), (ax + 2.6, ay - 2.0, 0), 52)
    return sc.render(o, d, depth=2, exposure=1.0)


def sound(path):
    tr = kit.Track()
    for k in range(STEPS):
        pc = -k / 8.0                                          # 1/8 octave lower each step -> endless descent
        tr.add(kit.shepard_note(pc, dur=1.0, base=55.0, decay=4.0), k * TP, 0.35)
        tr.add(kit.impact("chrome", 1500, vel=0.6, dur=0.4, seed=k), k * TP, 0.18, -0.2 + 0.4 * (k % 2))
    tr.save(path, reverb=0.3)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/bounce5_endlose_treppe.mp4"
    sound("build/b5.wav")
    kit.encode(frame, FPS, "build/b5.wav", out, workers=4, bitrate="12M")
