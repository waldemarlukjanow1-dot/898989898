"""STIL 4 – Video zum Nutzer-Beat (assets/trap_beat.mp3, nur Drums via Demucs, Musik entfernt).

- Die Klingen schlagen auf JEDEM Kick zusammen, abwechselnd auf beiden Seiten des Kreises (sie drehen gegenläufig;
  Treffer k liegt auf der Achse, Treffer k+1 genau gegenüber). Das unregelmäßige Kick-Muster macht sie von selbst
  mal schnell, mal langsam; in der Drum-Pause gibt es einen langsamen Bogen.
- Nur wenn beim Treffer Bälle dazwischen sind, vermehren sie sich (max. x3 pro Treffer, Gesamtzahl folgt einer Zeitkurve).
- Die Treffer-Achse dreht sich einmal pro Video. Nahtloser Implosions-Loop (Audio-Segment = 40 Takte).

python3 trap.py output/NAME.mp4
"""
import json
import math
import pickle
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf
from scipy.spatial import cKDTree

import beat
import render
import sounds
from sim import CX, CY, R, W, H

FPS = 60
RB = 8.0
GOAL = 1600
ON = json.load(open("build/trap_onsets.json"))
PER = ON["period"]
FIRST_KICK = min(k for k in ON["kicks"] if k > 23.5)
SEG0 = FIRST_KICK - 2 * PER                  # 2 silent beats before the first kick (drop-in hook)
T = 160 * PER                                # 40 bars
blade_halfwidth = beat.blade_halfwidth


def meetings():
    ks = [k - SEG0 for k in ON["kicks"] if SEG0 - 1e-3 <= k < SEG0 + T - 1e-3]
    out = []
    for k in ks:
        if not out or k - out[-1] > 0.3:
            out.append(k)
    if len(out) % 2:                         # even count -> blades end exactly where they started
        gaps = np.diff(out)
        out.pop(int(np.argmin(gaps)) + 1)
    return out


MEET = meetings()
# implosion on the meeting closest to 1.25 s before the loop point; meetings after it are dry
IMP = int(np.argmin([abs(m - (T - 1.25)) for m in MEET]))


def axis(t):
    return 90.0 + 360.0 * (t / T)


def jaw(t):
    t = t % T
    i = int(np.searchsorted(MEET, t, side="right"))     # number of meetings passed
    if i == 0:
        t0, t1, k = MEET[-1] - T, MEET[0], -1
    elif i == len(MEET):
        t0, t1, k = MEET[-1], MEET[0] + T, len(MEET) - 1
    else:
        t0, t1, k = MEET[i - 1], MEET[i], i - 1
    u = (t - t0) / (t1 - t0)
    o = 180.0 * (k + u ** 1.4)                          # speeds into every hit
    c = axis(t)
    return c - o, c + o


def meet_point(k):
    return (axis(MEET[k]) + 180.0 * (k % 2)) % 360


def target(t):
    return int(round(1 + (GOAL - 1) * min(1.0, t / (MEET[IMP] - 1.0)) ** 1.5))


# ------------------------------------------------------------------ physics
def simulate(init=None, seed=3, substeps=6, iters=2, gravity=900.0, implode_dur=0.55, log=print):
    rng = np.random.default_rng(seed)
    dt = 1.0 / FPS
    h = dt / substeps
    nframes = int(round(T * FPS))
    rb = RB
    if init is None:
        init = (CX, CY + R - rb - 1, 0.0, 0.0)
    pos = np.array([[init[0], init[1]]], dtype=np.float64)
    prev = pos - np.array([[init[2], init[3]]])
    col = np.array([0], np.int16)
    born = np.array([-10.0])
    events, frames = [], []
    imp = None
    nb = 0
    catch_t = np.array(MEET) - 0.04
    a1, a2 = jaw(0.0)
    for f in range(nframes):
        t = f * dt
        if imp is not None and t < imp["t"] + implode_dur:
            u = (t - imp["t"]) / implode_dur
            e = u * u * (3 - 2 * u)
            fpos = imp["p0"] + (imp["pt"] - imp["p0"]) * e
            fcol, fborn = imp["col"], imp["born"]
        else:
            fpos, fcol, fborn = pos, col, born
        frames.append(dict(pos=fpos.astype(np.float32), col=fcol.copy(), born=fborn.astype(np.float32),
                           a1=a1 % 360, a2=a2 % 360, contacts=0))
        if imp is not None and not imp["done"] and t >= imp["t"] + implode_dur:
            pos = imp["pt"][None, :].copy()
            prev = pos.copy()
            col = np.array([0], np.int16)
            born = np.array([t])
            imp["done"] = True
            events.append(dict(t=t, kind="pop", x=float(pos[0, 0]), y=float(pos[0, 1]), new=1, caught=0, total=1))
        contacts = 0
        for s_ in range(substeps):
            ts0, ts1 = t + s_ * h, t + (s_ + 1) * h
            a1_old, a2_old = a1, a2
            a1, a2 = jaw(ts1)
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
                        mag = np.minimum((2 * rb - dist) * 0.5, 3.0) / dist
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
            for j in np.where((catch_t > ts0 + 1e-9) & (catch_t <= ts1 + 1e-9))[0]:
                tm = MEET[j]
                c = meet_point(j)
                if j == IMP and imp is None and len(pos):
                    pt = np.array([CX, CY + rb + 14.0])
                    imp = dict(t=t, p0=pos.copy(), pt=pt, col=col.copy(), born=born.copy(), done=False)
                    events.append(dict(t=tm, kind="implode", x=float(pt[0]), y=float(pt[1]), new=0,
                                       caught=int(len(pos)), total=int(len(pos))))
                    log(f"implosion @ {tm:.2f}s: {len(pos)} -> 1")
                    pos, prev = np.zeros((0, 2)), np.zeros((0, 2))
                    col, born = np.zeros(0, np.int16), np.zeros(0)
                    continue
                events.append(dict(t=tm, kind="hit", x=CX + math.cos(math.radians(c)) * 0.75 * R,
                                   y=CY + math.sin(math.radians(c)) * 0.75 * R, new=0, caught=0, total=int(len(pos))))
                if j > IMP or len(pos) == 0:
                    continue                                 # after the implosion: dry hits (loop)
                rel = pos - (CX, CY)
                phi = np.degrees(np.arctan2(rel[:, 1], rel[:, 0]))
                dist = np.sqrt((rel * rel).sum(1))
                dphi = np.abs(((phi - c) + 180) % 360 - 180)
                ca, cb = jaw(ts1)
                g = (cb - ca) % 360
                o_gap = min(g, 360 - g) / 2
                caught = np.where((dphi < max(14.0, o_gap + 9.0)) & (dist > 0.12 * R))[0]
                if not len(caught):
                    continue                                 # nothing between the blades -> no multiplication
                keep = np.setdiff1d(np.arange(len(pos)), caught)
                n_new = int(np.clip(target(tm) - len(keep), len(caught) + 1, len(caught) * 3))
                cen = pos[caught].mean(0)
                rad = math.sqrt(n_new * (2 * rb) ** 2 * 0.33 / math.pi) + 10
                rel_c = cen - (CX, CY)
                dc = np.linalg.norm(rel_c)
                if dc + rad > R - rb:
                    cen = (CX, CY) + rel_c / (dc + 1e-6) * max(0.0, R - rb - rad)
                ang_r = rng.uniform(0, 2 * math.pi, n_new)
                rr = rad * np.sqrt(rng.uniform(0, 1, n_new))
                newp = cen + np.stack([np.cos(ang_r) * rr, np.sin(ang_r) * rr], 1)
                spd = rng.uniform(150, 450, n_new) * h
                newv = np.stack([np.cos(ang_r), np.sin(ang_r)], 1) * spd[:, None]
                pos = np.concatenate([pos[keep], newp])
                prev = np.concatenate([prev[keep], newp - newv])
                nb += 1
                col = np.concatenate([col[keep], np.full(n_new, nb % len(render.PALETTE), np.int16)])
                born = np.concatenate([born[keep], np.full(n_new, tm)])
                events[-1].update(kind="bite", x=float(cen[0]), y=float(cen[1]), new=int(n_new),
                                  caught=int(len(caught)), total=int(len(pos)))
        frames[-1]["contacts"] = contacts
        if f % 600 == 0:
            log(f"t={t:.1f}s balls={len(pos)}")
    end = None
    if len(pos) == 1:
        v = pos[0] - prev[0]
        end = (float(pos[0, 0]), float(pos[0, 1]), float(v[0]), float(v[1]))
    return dict(frames=frames, events=events, fps=FPS, rb=rb, goal=GOAL, duration=T, end=end)


def simulate_loop(log=print):
    log(f"segment {SEG0:.3f}s + {T:.2f}s, {len(MEET)} hits, implosion at hit {IMP} ({MEET[IMP]:.2f}s)")
    r1 = simulate(log=lambda m: None)
    assert r1["end"] is not None
    log(f"end ball {r1['end']}")
    r2 = simulate(init=r1["end"], log=log)
    e1, e2 = np.array(r1["end"]), np.array(r2["end"])
    log(f"loop error: pos {np.abs(e1[:2] - e2[:2]).max():.4f}px vel {np.abs(e1[2:] - e2[2:]).max():.5f}")
    return r2


# ------------------------------------------------------------------ audio: the user's beat, drums only
def make_audio(path):
    a, sr = sf.read("build/sep/htdemucs/trap_beat/drums.wav")
    seg = a[int(round(SEG0 * sr)): int(round((SEG0 + T) * sr))].copy()
    n = int(round(T * sr))
    seg = np.pad(seg, ((0, max(0, n - len(seg))), (0, 0)))[:n]
    fade = int(0.03 * sr)
    seg[-fade:] *= np.linspace(1, 0, fade)[:, None]
    sf.write("build/trap_seg.wav", seg, sr)
    print("audio", f"{sounds.normalise('build/trap_seg.wav', path):.1f} LUFS")


# ------------------------------------------------------------------ video
render.blade_halfwidth = blade_halfwidth
render.PALETTE = [(255, 43, 214), (255, 230, 0), (0, 229, 255), (255, 90, 60), (124, 255, 92), (170, 110, 255)]
_RES = None


def _init():
    global _RES
    _RES = pickle.load(open("build/trap_sim.pkl", "rb"))


def _frame(f):
    return render.render_frame(_RES["frames"][f], f / FPS, _RES["events"], GOAL, RB).tobytes()


def main(out):
    res = simulate_loop()
    pickle.dump(res, open("build/trap_sim.pkl", "wb"))
    b = [e for e in res["events"] if e["kind"] == "bite"]
    print("hits", len(MEET), "multiplications", len(b), "final", b[-1]["total"])
    make_audio("build/trap_mix.wav")
    nf = len(res["frames"])
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", "build/trap_mix.wav", "-c:v", "libx264", "-preset", "medium", "-b:v", "10M",
           "-maxrate", "13M", "-bufsize", "20M", "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
           "-c:a", "aac", "-b:a", "192k", "-shortest", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(4, initializer=_init) as pool:
        for k, buf in enumerate(pool.imap(_frame, range(nf), chunksize=4)):
            ff.stdin.write(buf)
            if k % 300 == 0:
                print(f"{k}/{nf}", flush=True)
    ff.stdin.close()
    ff.wait()
    print("done", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "output/simulation_trap.mp4")
