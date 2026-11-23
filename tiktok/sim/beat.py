"""STIL 4 – BEAT-Version: Klingen-Choreografie im Takt (120 BPM) + eigener Beat als Soundtrack.

- dickere Klingen, größere Bälle, schnellere und abwechslungsreiche Bewegung (Chomps auf einer Seite, Sweeps,
  Dreifach-Bisse, langsamer Breakdown mit Drehung, schneller Drop, Beschleunigung bis zur Implosion)
- jeder Biss liegt exakt auf dem Beat-Raster; der Biss-Sound ist Teil des Beats (kein Miauen)
- Ballzahl wächst mit der Zeit (Spannung, aber nach wenigen Sekunden schon Action), nahtloser Implosions-Loop

python3 beat.py output/NAME.mp4
"""
import math
import pickle
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf
from scipy.spatial import cKDTree

import render
import sim
import sounds
from sim import CX, CY, R, W, H

BPM = 120
BEAT = 60.0 / BPM
BARS = 28
T = BARS * 4 * BEAT                       # 56 s
FPS = 60
RB = 8.0                                  # bigger balls
GOAL = 1800
SR = sounds.SR


def blade_halfwidth(s):
    """Dickere Klingen: Stab 4 px, Keil 9 -> 24 px."""
    s = np.asarray(s)
    inner = 0.5 * R
    return np.where(s < inner, 4.0, 9.0 + 15.0 * (s - inner) / (R - inner))


# ------------------------------------------------------------------ choreography
def schedule():
    """Bisse in Beats: (beat, Treffpunkt-Winkel c, Öffnung o davor, Extra-Drehungen, Art)."""
    s = []
    for k, b in enumerate(range(1, 16, 2)):                       # A: chomps on one side
        s.append((b, 90, 70 if k % 2 == 0 else 45, 0, "bite"))
    for b, c in zip((19, 23, 27, 31), (0, 180, 90, 270)):          # B: big sweeps, meeting point travels
        s.append((b, c, 165, 0, "bite"))
    for bar, c in zip(range(4), (45, 135, 45, 135)):              # C: triple chomps left / right
        b0 = 33 + bar * 4
        for j, d in enumerate((0, 0.5, 1.0)):
            s.append((b0 + d, c, 60 if j == 0 else 28, 0, "bite"))
    s.append((55, 135, 160, 1, "bite"))                            # D: slow breakdown with full spins
    s.append((63, 90, 160, 1, "bite"))
    c = 90
    for b in range(65, 97, 2):                                    # E: drop, meeting point jumps 120°
        c = (c + 120) % 360
        s.append((b, c, 100, 0, "bite"))
        if b % 8 == 7:                                            # quick double at the end of every 4 bars
            s.append((b + 0.5, c, 30, 0, "bite"))
    for b, cc, o in ((97, 90, 120), (99, 45, 90), (101, 135, 90), (102, 90, 60), (103, 90, 40), (104, 45, 50),
                     (104.5, 45, 28), (105, 135, 50), (105.5, 135, 28), (106, 90, 50), (106.5, 90, 28)):
        s.append((b, cc, o, 0, "bite"))                            # F: accelerating outro
    s.append((109, 90, 150, 1, "implode"))                         # implosion -> 1 ball -> loop
    return [dict(t=b * BEAT, c=float(c), o=float(o), spin=sp, kind=k) for b, c, o, sp, k in s]


SCHED = schedule()


def jaw(t):
    """Blade angles (a1, a2) at time t; periodic with period T (seamless loop)."""
    t = t % T
    times = [e["t"] for e in SCHED]
    i = np.searchsorted(times, t, side="right")
    nxt = SCHED[i % len(SCHED)]
    prv = SCHED[i - 1] if i > 0 else SCHED[-1]
    t0 = prv["t"] - (T if i == 0 else 0)
    t1 = nxt["t"] + (T if i == len(SCHED) else 0)
    u = (t - t0) / (t1 - t0)
    o = nxt["o"] * math.sin(math.pi * u ** 0.75)                   # opens fast, snaps shut on the beat
    d = ((nxt["c"] - prv["c"] + 180) % 360) - 180 + 360 * nxt["spin"]
    e = u * u * (3 - 2 * u)
    c = prv["c"] + d * e
    return c - o, c + o


def target(t):
    """Ballzahl über die Zeit: schnell sichtbar, dann stetig bis GOAL (Spannung statt sofortiger Flut)."""
    return int(round(8 + (GOAL - 8) * min(1.0, t / 53.0) ** 1.6))


# ------------------------------------------------------------------ physics (same core as sim.py)
def simulate(init=None, seed=5, substeps=6, iters=2, gravity=900.0, implode_dur=0.55, log=print):
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
    sched_t = np.array([e["t"] for e in SCHED])
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
        for k in range(substeps):
            ts0, ts1 = t + k * h, t + (k + 1) * h
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
            # scheduled bite inside this substep?
            for j in np.where((sched_t > ts0 - 1e-9) & (sched_t <= ts1 + 1e-9))[0]:
                ev = SCHED[j]
                if ev["kind"] == "implode" and imp is None and len(pos):
                    pt = np.array([CX, CY + rb + 14.0])
                    imp = dict(t=t, p0=pos.copy(), pt=pt, col=col.copy(), born=born.copy(), done=False)
                    events.append(dict(t=ev["t"], kind="implode", x=float(pt[0]), y=float(pt[1]), new=0,
                                       caught=int(len(pos)), total=int(len(pos))))
                    log(f"implosion @ {ev['t']:.2f}s: {len(pos)} -> 1")
                    pos, prev = np.zeros((0, 2)), np.zeros((0, 2))
                    col, born = np.zeros(0, np.int16), np.zeros(0)
                    continue
                if ev["kind"] != "bite" or len(pos) == 0:
                    continue
                rel = pos - (CX, CY)
                phi = np.degrees(np.arctan2(rel[:, 1], rel[:, 0]))
                dist = np.sqrt((rel * rel).sum(1))
                dphi = np.abs(((phi - ev["c"]) + 180) % 360 - 180)
                caught = np.where((dphi < 16.0) & (dist > 0.12 * R))[0]
                if not len(caught):
                    events.append(dict(t=ev["t"], kind="bite", x=CX + math.cos(math.radians(ev["c"])) * 0.7 * R,
                                       y=CY + math.sin(math.radians(ev["c"])) * 0.7 * R, new=0, caught=0,
                                       total=int(len(pos))))
                    continue
                keep = np.setdiff1d(np.arange(len(pos)), caught)
                n_new = max(len(caught) + 1, target(ev["t"]) - len(keep))
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
                born = np.concatenate([born[keep], np.full(n_new, ev["t"])])
                events.append(dict(t=ev["t"], kind="bite", x=float(cen[0]), y=float(cen[1]), new=int(n_new),
                                   caught=int(len(caught)), total=int(len(pos))))
        frames[-1]["contacts"] = contacts
        if f % 600 == 0:
            log(f"t={t:.1f}s balls={len(pos)}")
    end = None
    if len(pos) == 1:
        v = pos[0] - prev[0]
        end = (float(pos[0, 0]), float(pos[0, 1]), float(v[0]), float(v[1]))
    return dict(frames=frames, events=events, fps=FPS, rb=rb, goal=GOAL, duration=T, end=end)


def simulate_loop(log=print):
    log("pass 1")
    r1 = simulate(log=lambda m: None)
    assert r1["end"] is not None
    log(f"end ball {r1['end']}")
    log("pass 2")
    r2 = simulate(init=r1["end"], log=log)
    e1, e2 = np.array(r1["end"]), np.array(r2["end"])
    log(f"loop error: pos {np.abs(e1[:2] - e2[:2]).max():.4f}px vel {np.abs(e1[2:] - e2[2:]).max():.5f}")
    return r2


# ------------------------------------------------------------------ the beat (own synthesis, A minor, 120 BPM)
ROOTS = [110.0, 87.31, 130.81, 98.0]                  # Am – F – C – G (one chord per bar)
CHORD = [[220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [261.6, 329.6, 392.0], [196.0, 246.9, 293.7]]


def section(bar):
    return "A" if bar < 4 else "B" if bar < 8 else "C" if bar < 12 else "D" if bar < 16 else "E" if bar < 24 else "F"


def make_beat(res, path):
    m = sounds.Mix(T, seed=9)
    rng = m.rng
    tt = sounds.tt
    t = tt(0.4)
    kick = np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-t * 28)) / SR) * np.exp(-t * 7) * np.minimum(1, t / 0.002)
    t = tt(0.06)
    hat = np.convolve(rng.standard_normal(len(t)), [1, -1], "same") * np.exp(-t * 70)
    t = tt(0.3)
    ohat = np.convolve(rng.standard_normal(len(t)), [1, -1], "same") * np.exp(-t * 12)
    t = tt(0.25)
    clap = sum(np.convolve(rng.standard_normal(len(t)), np.ones(3) / 3, "same") * np.exp(-(t - d).clip(0) * 25) *
               (t >= d) for d in (0, 0.012, 0.024))
    for bar in range(BARS):
        sec = section(bar)
        b0 = bar * 4 * BEAT
        root, ch = ROOTS[bar % 4], CHORD[bar % 4]
        for beat in range(4):
            tb = b0 + beat * BEAT
            if sec in "BCE" or (sec == "F" and bar < 26):
                m.add(kick, tb, 0.9)
            if sec in "CE" and beat in (1, 3):
                m.add(clap, tb, 0.35)
            for e8 in range(2):
                if sec in "BCE":
                    m.add(hat, tb + e8 * BEAT / 2, 0.10 if e8 else 0.06, 0.3)
                if sec == "E" and e8 == 1:
                    m.add(ohat, tb + BEAT / 2, 0.07, -0.3)
            if sec == "F" and bar < 27:
                for s16 in range(4):
                    m.add(hat, tb + s16 * BEAT / 4, 0.05 + 0.03 * (bar - 24), 0.2)
            # bass: off-beat (house) in B/C/E, long notes in A/D
            if sec in "BCE":
                tl = tt(BEAT / 2 * 0.9)
                ph = 2 * np.pi * root * tl
                bass = (np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)) * np.exp(-tl * 4) * np.minimum(1, tl / 0.005)
                m.add(bass, tb + BEAT / 2, 0.45)
            if sec == "E":                                          # pluck arpeggio (16ths)
                for s16 in range(4):
                    f0 = ch[(beat * 4 + s16) % 3] * (2 if s16 % 2 else 1)
                    tl = tt(0.25)
                    pl = (np.sin(2 * np.pi * f0 * tl) + 0.3 * np.sin(4 * np.pi * f0 * tl)) * np.exp(-tl * 14)
                    m.add(pl, tb + s16 * BEAT / 4, 0.06, 0.4 * (-1) ** s16)
        if sec in "AD" or bar >= 27:                                # soft pad + sub
            tl = tt(4 * BEAT + 0.3)
            env = np.minimum(1, tl / 0.4) * np.minimum(1, np.maximum(0, (4 * BEAT + 0.3 - tl) / 0.4))
            pad = sum(np.sin(2 * np.pi * f * tl) + 0.4 * np.sin(2 * np.pi * f * 1.004 * tl) for f in ch) * env
            m.add(pad, b0, 0.05 if sec == "A" else 0.07)
            m.add(np.sin(2 * np.pi * root * tl) * env, b0, 0.12)
    # riser into the implosion (bars 26-27)
    imp_t = [e["t"] for e in res["events"] if e["kind"] == "implode"][0]
    L = imp_t - 52.0
    tl = tt(L)
    riser = np.convolve(rng.standard_normal(len(tl)), np.ones(4) / 4, "same") * (tl / L) ** 2 * 0.6 + \
        np.sin(2 * np.pi * np.cumsum(200 + 1400 * (tl / L) ** 2) / SR) * (tl / L) ** 2 * 0.15
    m.add(riser, 52.0, 0.5)
    # bite = "chomp": water-drop plop + snap, bigger later; part of the groove
    bites = [e for e in res["events"] if e["kind"] == "bite"]
    for k, e in enumerate(bites):
        s = e["t"] / T
        tl = tt(0.3)
        f = 180 + 650 * (tl / 0.3) ** 1.5
        plop = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tl * 12) * np.minimum(1, tl / 0.002)
        snap = np.convolve(rng.standard_normal(len(tl)), np.ones(6) / 6, "same") * np.exp(-tl * 60) * 1.5
        thump = np.sin(2 * np.pi * np.cumsum(60 + 90 * np.exp(-tl * 30)) / SR) * np.exp(-tl * 14)
        m.add(plop + snap + 0.8 * thump, e["t"], 0.45 + 0.25 * s, sounds.pan_of(e))
    for e in res["events"]:
        if e["kind"] == "implode":
            L = 0.55
            tl = tt(L)
            m.add(np.convolve(rng.standard_normal(len(tl)), np.ones(3) / 3, "same") * (tl / L) ** 3, e["t"], 0.6)
        if e["kind"] == "pop":
            tl = tt(1.2)
            m.add((np.sin(2 * np.pi * 440 * tl) + 0.5 * np.sin(2 * np.pi * 660 * tl)) * np.exp(-tl * 3), e["t"], 0.3)
            m.add(kick, e["t"], 0.8)
    # shaker driven by blade contacts, quantised to 16ths (the physics plays along with the beat)
    sx = BEAT / 4
    acc = np.zeros(int(T / sx) + 1)
    for f, fr in enumerate(res["frames"]):
        acc[int(round(f / FPS / sx)) % len(acc)] += fr["contacts"]
    tl = tt(0.05)
    shk = np.convolve(rng.standard_normal(len(tl)), [1, -1], "same") * np.exp(-tl * 90)
    for i, a in enumerate(acc):
        if a > 0:
            m.add(shk, i * sx, min(0.08, 0.006 * np.sqrt(a)), rng.uniform(-0.6, 0.6))
    m.reverb(0.16, 1.2, 3.5)
    peak = max(np.abs(m.L).max(), np.abs(m.R).max())
    sf.write("build/beat_raw.wav", np.stack([m.L, m.R], 1) / peak * 0.9, SR)
    print("beat", f"{sounds.normalise('build/beat_raw.wav', path):.1f} LUFS")


# ------------------------------------------------------------------ video
render.blade_halfwidth = blade_halfwidth            # thicker blades in the drawing too
render.PALETTE = [(255, 43, 214), (0, 229, 255), (255, 230, 0), (124, 255, 92), (255, 120, 60), (170, 110, 255)]
_RES = None


def _init():
    global _RES
    _RES = pickle.load(open("build/beat_sim.pkl", "rb"))


def _frame(f):
    return render.render_frame(_RES["frames"][f], f / FPS, _RES["events"], GOAL, RB).tobytes()


def main(out):
    res = simulate_loop()
    pickle.dump(res, open("build/beat_sim.pkl", "wb"))
    nb = [e for e in res["events"] if e["kind"] == "bite"]
    print("bites", len(nb), "empty", sum(1 for e in nb if e["new"] == 0), "final", nb[-1]["total"])
    make_beat(res, "build/beat_mix.wav")
    nf = len(res["frames"])
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", "build/beat_mix.wav", "-c:v", "libx264", "-preset", "medium", "-b:v", "11M",
           "-maxrate", "14M", "-bufsize", "22M", "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
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
    main(sys.argv[1] if len(sys.argv) > 1 else "output/simulation_beat.mp4")
