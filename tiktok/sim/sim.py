"""STIL 4 – Physik-Simulation nach dem Referenz-System (tiktok/referenz/PRODUKTION.md).

Kreis-Arena, zwei gegenläufige Klingen bilden einen „Kiefer“. Wenn er zubeißt, explodieren alle Bälle im Keil
in viele neue Bälle der nächsten Farbe. Verlet-Integration + Positions-Korrektur (PBD), Nachbarn über cKDTree.

simulate(cfg) -> dict mit Frames (Positionen, Farbindex, Geburtszeit) + Ereignisliste (für Ton und HUD).
"""
import math

import numpy as np
from scipy.spatial import cKDTree

W, H = 1080, 1920
CX, CY, R = 520.0, 880.0, 430.0


def blade_halfwidth(s):
    """Halbe Dicke der Klinge entlang des Radius s (Stab innen, Keil außen)."""
    s = np.asarray(s)
    inner = 0.55 * R
    return np.where(s < inner, 3.0, 6.0 + 11.0 * (s - inner) / (R - inner))


def simulate(fps=60, duration=15.0, rb=3.8, goal=10000, targets=(30, 200, 900, 2700, 6000, 10000),
             first_bite=0.8, period0=2.4, speedup=0.94, gravity=900.0, substeps=4, iters=2, seed=7,
             log=print):
    rng = np.random.default_rng(seed)
    dt = 1.0 / fps
    h = dt / substeps
    # blade angles (deg, screen coords, y down): a1 increases, a2 decreases; first meet at the bottom (90°)
    omega = 180.0 / period0
    a1 = 90.0 - omega * first_bite
    a2 = 90.0 + omega * first_bite
    # start: one ball resting at the bottom, right where the jaw will bite
    pos = np.array([[CX, CY + R - rb - 1]], dtype=np.float64)
    prev = pos.copy()
    col = np.array([0], dtype=np.int16)
    born = np.array([-10.0])
    stage = 0
    rpm = 12
    armed = True
    events = []
    frames = []
    nframes = int(round(duration * fps))
    for f in range(nframes):
        t = f * dt
        contacts = 0
        for _ in range(substeps):
            a1_old, a2_old = a1, a2
            a1 += omega * h
            a2 -= omega * h
            # integrate (Verlet)
            vel = (pos - prev) * 0.999
            prev = pos.copy()
            pos = pos + vel
            pos[:, 1] += gravity * h * h
            for _ in range(iters):
                # ball-ball
                if len(pos) > 1:
                    tree = cKDTree(pos)
                    pr = tree.query_pairs(2 * rb, output_type="ndarray")
                    if len(pr):
                        d = pos[pr[:, 1]] - pos[pr[:, 0]]
                        dist = np.sqrt((d * d).sum(1)) + 1e-6
                        ov = (2 * rb - dist) / dist * 0.5
                        ov = np.minimum(ov * dist, 2.5)[:, None] / dist[:, None]
                        corr = d * ov
                        np.add.at(pos, pr[:, 0], -corr)
                        np.add.at(pos, pr[:, 1], corr)
                # blades (push out to the side the ball was on before)
                for ang, ang_old in ((a1, a1_old), (a2, a2_old)):
                    u = np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
                    n = np.array([-u[1], u[0]])
                    uo = np.array([math.cos(math.radians(ang_old)), math.sin(math.radians(ang_old))])
                    no = np.array([-uo[1], uo[0]])
                    rel = pos - (CX, CY)
                    s = rel @ u
                    p = rel @ n
                    po = (prev - (CX, CY)) @ no
                    side = np.where(np.abs(po) > 1e-3, np.sign(po), np.sign(p) + (p == 0))
                    hw = blade_halfwidth(np.clip(s, 0, R)) + rb
                    hit = (s > -rb) & (s < R) & (np.abs(p) < hw)
                    if hit.any():
                        contacts += int(hit.sum())
                        push = (side[hit] * hw[hit] - p[hit])
                        pos[hit] += push[:, None] * n
                # circle wall
                rel = pos - (CX, CY)
                dist = np.sqrt((rel * rel).sum(1))
                out = dist > R - rb
                if out.any():
                    pos[out] = (CX, CY) + rel[out] / dist[out, None] * (R - rb)
            # bite?
            gap = (a2 - a1) % 360.0
            if gap > 90.0:
                armed = True
            if gap < 7.0 and armed and stage < len(targets):
                armed = False
                rel = pos - (CX, CY)
                phi = np.degrees(np.arctan2(rel[:, 1], rel[:, 0]))
                dist = np.sqrt((rel * rel).sum(1))
                inwedge = (((phi - a1) % 360.0) < gap + 9.0) & (dist > 0.1 * R)
                caught = np.where(inwedge)[0]
                if len(caught):
                    keep = np.setdiff1d(np.arange(len(pos)), caught)
                    n_new = max(len(caught), targets[stage] - len(keep))
                    cen = pos[caught].mean(0)
                    # spawn disk big enough for the new balls at ~3x density
                    rad = math.sqrt(n_new * (2 * rb) ** 2 * 0.33 / math.pi) + 6
                    rel_c = cen - (CX, CY)
                    dc = np.linalg.norm(rel_c)
                    if dc + rad > R - rb:
                        cen = (CX, CY) + rel_c / (dc + 1e-6) * max(0.0, R - rb - rad)
                    ang_r = rng.uniform(0, 2 * math.pi, n_new)
                    rr = rad * np.sqrt(rng.uniform(0, 1, n_new))
                    newp = cen + np.stack([np.cos(ang_r) * rr, np.sin(ang_r) * rr], 1)
                    spd = rng.uniform(120, 420 + 0.05 * n_new, n_new) * h
                    newv = np.stack([np.cos(ang_r), np.sin(ang_r)], 1) * spd[:, None]
                    pos = np.concatenate([pos[keep], newp])
                    prev = np.concatenate([prev[keep], newp - newv])
                    col = np.concatenate([col[keep], np.full(n_new, stage + 1, np.int16)])
                    born = np.concatenate([born[keep], np.full(n_new, t)])
                    events.append(dict(t=t, caught=int(len(caught)), new=int(n_new), total=int(len(pos)),
                                       stage=stage + 1, x=float(cen[0]), y=float(cen[1]), rpm=rpm + 1))
                    log(f"bite {stage + 1} @ {t:.2f}s: caught {len(caught)} -> total {len(pos)}")
                    stage += 1
                    rpm += 1
                    omega *= 1.0 / speedup
        frames.append(dict(pos=pos.astype(np.float32), col=col.copy(), born=born.astype(np.float32),
                           a1=a1 % 360, a2=a2 % 360, contacts=contacts, rpm=rpm))
        if f % 60 == 0:
            log(f"t={t:.1f}s balls={len(pos)}")
    return dict(frames=frames, events=events, goal=goal, fps=fps, rb=rb)
