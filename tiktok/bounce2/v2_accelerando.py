"""Bounce 2.0 – Video 2 „Accelerando“: neues Bounce-Muster + neue Umgebung (weißer Raum).

Physik: gedämpfter Bounce mit Stoßzahl e=0.82 -> Sprungzeiten schrumpfen geometrisch (T0*e^k). Die Summe der unendlichen
Reihe ist so gewählt, dass die Kugel exakt bei t=7.28 s zur Ruhe käme; genau dann schleudert eine Druckwelle im Boden
sie zurück auf die Starthöhe, die sie bei t=8 s erreicht = Bild 0 (Loop).
Ton: jeder Aufprall ein Keramik-"Tock" eine Stufe höher (Dur-Tonleiter) -> beschleunigender, steigender Riser.
"""
import math
import sys

import numpy as np

import kit
import rt

FPS = 60
E = 0.82
T0 = kit.DUR * (1 - E)                          # 1.44 s
R_BALL = 0.45
H0 = 2.2
G = 8 * H0 / T0 ** 2
C0 = T0 / 2
CONTACTS = [C0]
k = 1
while T0 * E ** k > 1 / 240:
    CONTACTS.append(CONTACTS[-1] + T0 * E ** k)
    k += 1
C_INF = C0 + T0 * E / (1 - E)                     # = 8 - T0/2


def ball(t):
    """centre height above the floor contact level, vertical speed"""
    if t < C0:                                    # falling from the apex (t=0)
        s = t
        return H0 - 0.5 * G * s * s, -G * s
    if t >= C_INF:                                # launch back to the apex (reached at t=8)
        s = t - C_INF
        v = G * (kit.DUR - C_INF)
        return v * s - 0.5 * G * s * s, v - G * s
    for a, b in zip(CONTACTS[:-1], CONTACTS[1:]):
        if a <= t < b:
            T = b - a
            s = t - a
            v = G * T / 2
            return v * s - 0.5 * G * s * s, v - G * s
    return 0.0, 0.0                               # resting buzz just before the launch


class WhiteFloor(rt.Floor):
    """Matte white floor with a launch shock-wave ring."""
    t = 0.0

    def albedo(self, p):
        base = np.broadcast_to(np.array([0.82, 0.82, 0.84]), p.shape).copy()
        far = np.clip((-p[:, 2] - 1.5) / 6.0, 0, 1)[:, None]               # seamless studio sweep
        base = base * (1 - far) + np.array([0.86, 0.865, 0.9]) * far
        age = self.t - C_INF if self.t >= C_INF else self.t + kit.DUR - C_INF
        if 0 <= age < 0.6:
            rad = np.hypot(p[:, 0], p[:, 2])
            ring = np.exp(-((rad - 0.3 - age * 6) / 0.08) ** 2) * (1 - age / 0.6)
            base += ring[:, None] * np.array([0.9, 0.25, 0.3]) * 1.5
        return base


def env(d):
    return rt.studio_env(d, top=(0.86, 0.87, 0.91), horizon=(0.76, 0.765, 0.8), boxes=[((0, 1, 0.3), 0.5, (1, 1, 1), 0.5)])


LIGHTS = [((-0.35, 1.0, 0.45), (0.75, 0.72, 0.68), 4.0)]


def frame(i):
    t = i / FPS
    y, vy = ball(t)
    near = [c for c in CONTACTS + [C_INF] if abs(t - c) < 0.05]
    vimp = G * T0 / 2
    depth = 0.0
    for c in near:
        idx = CONTACTS.index(c) if c in CONTACTS else 0
        v = vimp * (E ** idx if c in CONTACTS else 1.0)
        depth = max(depth, 0.24 * v / vimp)
    sy = kit.squash(t, near, depth=max(depth, 1e-4), width=0.035 + 0.02 * depth, stretch=0.07, vy=vy, vmax=vimp)
    cy = max(R_BALL * sy, R_BALL + y) if sy >= 1 else R_BALL * sy
    b = rt.Ball((0, cy, 0), R_BALL, "ceramic", color=(0.88, 0.1, 0.16), sy=sy)
    fl = WhiteFloor(0, "matte")
    fl.t = t
    sc = rt.Scene([b], fl, env, LIGHTS, ambient=0.3, floor_reflect=0.0)
    o, d = rt.camera_rays((0, 1.3, 8.2), (0, 1.45, 0), 30)
    return sc.render(o, d, depth=1, exposure=1.0)


def sound(path):
    tr = kit.Track()
    scale = [0, 2, 4, 5, 7, 9, 11]
    for k, c in enumerate(CONTACTS):
        if k > 0 and CONTACTS[k] - CONTACTS[k - 1] < 0.03:
            break
        semis = 12 * (k // 7) + scale[k % 7]
        f = 261.6 * 2 ** (semis / 12)
        v = E ** k
        tr.add(kit.impact("ceramic", f, vel=0.6 + 0.4 * v, dur=0.6, seed=k), c, 0.55 + 0.25 * (1 - v))
    tb = kit.t_axis(0.5)                                     # resting buzz (tiny bounces) right before the launch
    buzz = np.sin(2 * np.pi * 1200 * tb) * (np.sin(2 * np.pi * 60 * tb) > 0.6) * 0.3 * np.minimum(1, tb / 0.2)
    tr.add(buzz, C_INF - 0.5, 0.25)
    tl = kit.t_axis(1.2)                                     # launch: deep whoomp + bright chord
    whoomp = np.sin(2 * np.pi * np.cumsum(40 + 120 * (1 - np.exp(-tl * 6))) / kit.SR) * np.exp(-tl * 2.5)
    chord = sum(np.sin(2 * np.pi * f * tl) for f in (523.3, 659.3, 784.0)) * np.exp(-tl * 3) * 0.25
    tr.add(whoomp + chord, C_INF, 1.0)
    tr.save(path, reverb=0.2)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/bounce2_accelerando.mp4"
    sound("build/b2.wav")
    kit.encode(frame, FPS, "build/b2.wav", out, workers=4, bitrate="10M")
