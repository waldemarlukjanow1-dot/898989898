"""STIL 4 – Physik-Simulation nach dem Referenz-System (tiktok/referenz/PRODUKTION.md).

Kreis-Arena, zwei gegenläufige Klingen bilden einen „Kiefer“. Bei jedem Biss explodieren die gefangenen Bälle in
mehr Bälle der nächsten Farbe. Verlet-Integration + Positions-Korrektur (PBD), Nachbarn über cKDTree.

Nahtloser Loop: Die Klingen drehen mit konstanter Geschwindigkeit, die Gesamtlänge ist ein gerades Vielfaches der
Biss-Periode (Klingen stehen am Ende exakt wie am Anfang). Der letzte Biss ist eine IMPLOSION: alle Bälle werden in
einen Punkt gesaugt, es bleibt 1 Magenta-Ball, der nach unten fällt und genau dort liegt, wo das Video beginnt.
simulate_loop() rechnet zweimal: Lauf 1 liefert den End-Zustand, Lauf 2 startet damit -> Bild N == Bild 0.
"""
import math

import numpy as np
from scipy.spatial import cKDTree

W, H = 1080, 1920
CX, CY, R = 520.0, 880.0, 430.0
NCOL = 6   # colour cycle length (render.PALETTE)


def blade_halfwidth(s):
    """Halbe Dicke der Klinge entlang des Radius s (Stab innen, Keil außen)."""
    s = np.asarray(s)
    inner = 0.55 * R
    return np.where(s < inner, 3.0, 6.0 + 11.0 * (s - inner) / (R - inner))


def gentle_targets(n, first=12, last=6000):
    """Langsames Auffüllen: n Bisse, Ballzahl wächst gleichmäßig (geometrisch) von first bis last."""
    q = (last / first) ** (1.0 / (n - 1))
    out = [int(round(first * q ** k)) for k in range(n)]
    for k in range(1, n):
        out[k] = max(out[k], out[k - 1] + 3)
    out[-1] = last
    return out


def hook_targets(n, early=(80, 300, 650, 1000), last=3500):
    """Früh-Chaos-Kurve: riesige Sprünge in den ersten Bissen (Kreis nach ~6 s voll Action),
    danach gleichmäßiges Wachstum bis zum Ziel (jeder Biss bringt sichtbar neue Bälle)."""
    early = list(early)
    rest = n - len(early)
    step = (last - early[-1]) / rest
    return early + [int(round(early[-1] + step * (k + 1))) for k in range(rest)]


def simulate(fps=60, period=2.6, n_periods=22, first_bite=0.8, rb=3.8, targets=None, gravity=900.0,
             substeps=4, iters=2, seed=7, init=None, implode_dur=0.55, log=print):
    """init = (x, y, vx_per_substep, vy_per_substep) of the single start ball (from a previous run)."""
    rng = np.random.default_rng(seed)
    dt = 1.0 / fps
    h = dt / substeps
    duration = period * n_periods
    nframes = int(round(duration * fps))
    omega = 180.0 / period
    n_bites = n_periods - 1                      # last meeting (top) = implosion
    targets = targets or gentle_targets(n_bites)
    a1 = 90.0 - omega * first_bite
    a2 = 90.0 + omega * first_bite
    if init is None:
        init = (CX, CY + R - rb - 1, 0.0, 0.0)
    pos = np.array([[init[0], init[1]]], dtype=np.float64)
    prev = pos - np.array([[init[2], init[3]]])
    col = np.array([0], dtype=np.int16)
    born = np.array([-10.0])
    stage = 0
    armed = True
    events, frames = [], []
    imp = None            # implosion animation state
    for f in range(nframes):
        t = f * dt
        # ---------------- frame = state at time t (before stepping)
        if imp is not None:
            u = min(1.0, (t - imp["t"]) / implode_dur)
            e = u * u * (3 - 2 * u)
            rp = imp["p0"] + (imp["pt"] - imp["p0"]) * e
            fpos = np.concatenate([rp, pos]) if u < 1 else pos
            fcol = np.concatenate([imp["col"], col]) if u < 1 else col
            fborn = np.concatenate([imp["born"], born]) if u < 1 else born
        else:
            fpos, fcol, fborn = pos, col, born
        frames.append(dict(pos=fpos.astype(np.float32), col=fcol.copy(), born=fborn.astype(np.float32),
                           a1=a1 % 360, a2=a2 % 360, contacts=0, imp=None if imp is None else
                           dict(t=imp["t"], x=float(imp["pt"][0]), y=float(imp["pt"][1]))))
        contacts = 0
        # implosion finished -> the single magenta ball appears
        if imp is not None and t >= imp["t"] + implode_dur and not imp["done"]:
            pos = imp["pt"][None, :].copy()
            prev = pos.copy()
            col = np.array([0], np.int16)
            born = np.array([t])
            imp["done"] = True
            events.append(dict(t=t, kind="pop", total=1, new=1, caught=0, stage=stage, x=float(pos[0, 0]),
                               y=float(pos[0, 1])))
        for _ in range(substeps):
            a1_old, a2_old = a1, a2
            a1 += omega * h
            a2 -= omega * h
            vel = (pos - prev) * 0.999
            prev = pos.copy()
            pos = pos + vel
            pos[:, 1] += gravity * h * h
            for _ in range(iters):
                if len(pos) > 1:
                    pr = cKDTree(pos).query_pairs(2 * rb, output_type="ndarray")
                    if len(pr):
                        d = pos[pr[:, 1]] - pos[pr[:, 0]]
                        dist = np.sqrt((d * d).sum(1)) + 1e-6
                        mag = np.minimum((2 * rb - dist) * 0.5, 2.5) / dist
                        corr = d * mag[:, None]
                        np.add.at(pos, pr[:, 0], -corr)
                        np.add.at(pos, pr[:, 1], corr)
                for ang, ang_old in ((a1, a1_old), (a2, a2_old)):
                    u_ = np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
                    n_ = np.array([-u_[1], u_[0]])
                    uo = np.array([math.cos(math.radians(ang_old)), math.sin(math.radians(ang_old))])
                    no = np.array([-uo[1], uo[0]])
                    rel = pos - (CX, CY)
                    s = rel @ u_
                    p = rel @ n_
                    po = (prev - (CX, CY)) @ no
                    side = np.where(np.abs(po) > 1e-3, np.sign(po), np.sign(p) + (p == 0))
                    hw = blade_halfwidth(np.clip(s, 0, R)) + rb
                    hit = (s > -rb) & (s < R) & (np.abs(p) < hw)
                    if hit.any():
                        contacts += int(hit.sum())
                        pos[hit] += (side[hit] * hw[hit] - p[hit])[:, None] * n_
                rel = pos - (CX, CY)
                dist = np.sqrt((rel * rel).sum(1))
                out = dist > R - rb
                if out.any():
                    pos[out] = (CX, CY) + rel[out] / dist[out, None] * (R - rb)
            # ---------------- bite / implosion
            gap = (a2 - a1) % 360.0
            if gap > 90.0:
                armed = True
            if gap < 7.0 and armed and imp is None:
                armed = False
                rel = pos - (CX, CY)
                phi = np.degrees(np.arctan2(rel[:, 1], rel[:, 0]))
                dist = np.sqrt((rel * rel).sum(1))
                if stage < len(targets):
                    caught = np.where((((phi - a1) % 360.0) < gap + 9.0) & (dist > 0.1 * R))[0]
                    if len(caught):
                        keep = np.setdiff1d(np.arange(len(pos)), caught)
                        n_new = max(len(caught), targets[stage] - len(keep))
                        cen = pos[caught].mean(0)
                        rad = math.sqrt(n_new * (2 * rb) ** 2 * 0.33 / math.pi) + 8
                        rel_c = cen - (CX, CY)
                        dc = np.linalg.norm(rel_c)
                        if dc + rad > R - rb:
                            cen = (CX, CY) + rel_c / (dc + 1e-6) * max(0.0, R - rb - rad)
                        ang_r = rng.uniform(0, 2 * math.pi, n_new)
                        rr = rad * np.sqrt(rng.uniform(0, 1, n_new))
                        newp = cen + np.stack([np.cos(ang_r) * rr, np.sin(ang_r) * rr], 1)
                        boost = 1.8 if stage < 4 else 1.0          # punchier explosions at the start
                        spd = rng.uniform(100 * boost, (300 + 0.04 * n_new) * boost, n_new) * h
                        newv = np.stack([np.cos(ang_r), np.sin(ang_r)], 1) * spd[:, None]
                        pos = np.concatenate([pos[keep], newp])
                        prev = np.concatenate([prev[keep], newp - newv])
                        col = np.concatenate([col[keep], np.full(n_new, (stage + 1) % NCOL, np.int16)])
                        born = np.concatenate([born[keep], np.full(n_new, t)])
                        events.append(dict(t=t, kind="bite", caught=int(len(caught)), new=int(n_new),
                                           total=int(len(pos)), stage=stage + 1, x=float(cen[0]), y=float(cen[1])))
                        log(f"bite {stage + 1} @ {t:.2f}s: caught {len(caught)} -> total {len(pos)}")
                        stage += 1
                else:
                    # IMPLOSION at the meeting point: everything is sucked into one point
                    # target just below the hub: from there the new ball falls freely to the bottom (start spot)
                    pt = np.array([CX, CY + rb + 14.0])
                    imp = dict(t=t, p0=pos.copy(), pt=pt, col=col.copy(), born=born.copy(), done=False)
                    events.append(dict(t=t, kind="implode", total=int(len(pos)), new=0, caught=int(len(pos)),
                                       stage=stage, x=float(pt[0]), y=float(pt[1])))
                    log(f"implosion @ {t:.2f}s: {len(pos)} balls -> 1")
                    pos = np.zeros((0, 2))
                    prev = np.zeros((0, 2))
                    col = np.zeros(0, np.int16)
                    born = np.zeros(0)
        frames[-1]["contacts"] = contacts
        if f % 600 == 0:
            log(f"t={t:.1f}s balls={len(pos)}")
    end = None
    if len(pos) == 1:
        v = pos[0] - prev[0]
        end = (float(pos[0, 0]), float(pos[0, 1]), float(v[0]), float(v[1]))
    return dict(frames=frames, events=events, goal=targets[-1], fps=fps, rb=rb, end=end, duration=duration)


def simulate_loop(log=print, **kw):
    """Run twice so that the last frame flows seamlessly into the first one."""
    log("pass 1 (find end state)")
    r1 = simulate(log=lambda m: None, **kw)
    assert r1["end"] is not None, "implosion did not leave exactly one ball"
    log(f"end ball: {r1['end']}")
    log("pass 2 (start from end state)")
    r2 = simulate(init=r1["end"], log=log, **kw)
    assert r2["end"] is not None, "pass 2 did not end with one ball"
    e1, e2 = np.array(r1["end"]), np.array(r2["end"])
    log(f"loop error: pos {np.abs(e1[:2] - e2[:2]).max():.4f}px  vel {np.abs(e1[2:] - e2[2:]).max():.5f}")
    return r2
