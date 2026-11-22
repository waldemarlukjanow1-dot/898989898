"""Five pleasant, satisfying sound designs for the simulation (all own synthesis, loop-safe circular buffer).

python3 sounds.py            -> build/snd_<name>.wav (normalised to -14 LUFS) for every design
Each design: contact notes (density from blade contacts), a bite sound per explosion (grows with the stage),
the implosion and the pop of the new ball. Harmony follows a chord progression that changes with every bite.
"""
import pickle
import re
import subprocess
import sys

import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve

import sim

SR = 48000
# C major pentatonic chords cycling with the bites: C – Am – F – G (all tones stay consonant)
CHORDS = [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
PENTA = [261.6, 293.7, 329.6, 392.0, 440.0]


class Mix:
    def __init__(self, dur, seed=1):
        self.n = int(round(dur * SR))
        self.L = np.zeros(self.n)
        self.R = np.zeros(self.n)
        self.rng = np.random.default_rng(seed)

    def add(self, sig, t0, g=1.0, pan=0.0):
        i = int(round(t0 * SR)) % self.n
        idx = (np.arange(len(sig)) + i) % self.n
        gl, gr = g * np.sqrt(0.5 * (1 - pan)), g * np.sqrt(0.5 * (1 + pan))
        np.add.at(self.L, idx, sig * gl)
        np.add.at(self.R, idx, sig * gr)

    def reverb(self, wet=0.3, length=1.6, damp=3.0):
        """Simple convolution reverb with a decaying noise impulse, tail wrapped around (loop-safe)."""
        t = np.arange(int(length * SR)) / SR
        out = []
        for ch, seed in ((self.L, 11), (self.R, 12)):
            ir = np.random.default_rng(seed).standard_normal(len(t)) * np.exp(-t * damp)
            ir = np.convolve(ir, np.ones(8) / 8, mode="same")          # soften the highs
            ir /= np.sqrt((ir ** 2).sum())
            y = fftconvolve(ch, ir)
            wrapped = y[: self.n].copy()
            tail = y[self.n:]
            wrapped[: len(tail)] += tail
            out.append(ch * (1 - wet) + wrapped * wet)
        self.L, self.R = out


def tt(d):
    return np.arange(int(d * SR)) / SR


def chord_at(res, t):
    k = sum(1 for e in res["events"] if e["kind"] == "bite" and e["t"] <= t)
    return CHORDS[k % len(CHORDS)]


def contact_times(res, density, cap):
    """Note onsets from blade contacts: Poisson per frame, lambda ~ density * sqrt(contacts)."""
    rng = np.random.default_rng(5)
    fps = res["fps"]
    for f, fr in enumerate(res["frames"]):
        lam = min(cap, density * np.sqrt(fr["contacts"]))
        for _ in range(rng.poisson(lam)):
            yield f / fps + rng.uniform(0, 1 / fps)


def bites(res):
    b = [e for e in res["events"] if e["kind"] == "bite"]
    for k, e in enumerate(b):
        yield k / max(1, len(b) - 1), e


def pan_of(e):
    return float(np.clip((e["x"] - sim.CX) / sim.R, -1, 1)) * 0.6


# ------------------------------------------------------------------ 1 JELLY
def jelly(res, m):
    rng = m.rng
    bank = {}
    for t0 in contact_times(res, 0.035, 1.6):
        f0 = rng.choice(chord_at(res, t0)) * rng.choice([0.5, 1.0])
        key = round(f0, 1)
        if key not in bank:
            t = tt(0.35)
            f = f0 * (1 + 0.22 * np.exp(-t * 10) * np.sin(2 * np.pi * 13 * t))      # wobble
            ph = 2 * np.pi * np.cumsum(f) / SR
            bank[key] = (np.sin(ph) + 0.18 * np.sin(2 * ph)) * np.exp(-t * 13) * np.minimum(1, t / 0.006)
        m.add(bank[key], t0, 0.05, rng.uniform(-0.5, 0.5))
    for s, e in bites(res):
        t = tt(1.1)
        f = 110 * (1 + 1.0 * np.exp(-t * 7)) * (1 + 0.12 * np.exp(-t * 4) * np.sin(2 * np.pi * 7 * t))
        ph = 2 * np.pi * np.cumsum(f) / SR
        body = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.exp(-t * 3.5) * np.minimum(1, t / 0.01)
        squish = np.convolve(m.rng.standard_normal(len(t)), np.ones(60) / 60, "same") * np.exp(-t * 18) * 1.5
        m.add(body + squish, e["t"], 0.35 + 0.35 * s, pan_of(e))
    special(res, m, rise=lambda t, L: np.sin(2 * np.pi * np.cumsum(140 + 500 * (t / L) ** 2) / SR) * (t / L) ** 2,
            pop_f=330)
    m.reverb(0.18, 1.0, 4.0)


# ------------------------------------------------------------------ 2 GLASS
def glass(res, m):
    rng = m.rng
    bank = {}
    ratios, amps, decs = [1, 2.32, 4.25, 6.63], [1, 0.45, 0.2, 0.1], [2.5, 4.5, 8, 12]
    def ping(f0, d=1.6):
        t = tt(d)
        return sum(a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t * dc) for r, a, dc in zip(ratios, amps, decs)) \
            * np.minimum(1, t / 0.002)
    for t0 in contact_times(res, 0.02, 1.0):
        f0 = rng.choice(chord_at(res, t0)) * rng.choice([2, 4])
        key = round(f0, 1)
        if key not in bank:
            bank[key] = ping(f0)
        m.add(bank[key], t0, 0.018, rng.uniform(-0.7, 0.7))
    for s, e in bites(res):
        ch = chord_at(res, e["t"] + 0.01)
        for j, f in enumerate([ch[0] * 2, ch[1] * 2, ch[2] * 2, ch[0] * 4]):      # strummed glass chord
            m.add(ping(f, 2.4), e["t"] + j * 0.045, 0.16 + 0.12 * s, pan_of(e) + (j - 1.5) * 0.15)
        t = tt(2.5)                                                                # glass bowl hum
        m.add(np.sin(2 * np.pi * ch[0] * t) * np.exp(-t * 1.5) * np.minimum(1, t / 0.05), e["t"], 0.12 + 0.1 * s)
    special(res, m, rise=lambda t, L: ping(1046.5, L)[::-1], pop_f=2093)
    m.reverb(0.4, 2.2, 2.2)


# ------------------------------------------------------------------ 3 PLOP / BUBBLES
def bubbles(res, m):
    rng = m.rng
    def bubble(f0, d):
        t = tt(d)
        f = f0 * (1 + 2.2 * t / d)                       # bubble resonance rises
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (5 / d)) * np.minimum(1, t / 0.002)
    bank = [bubble(f, d) for f in (320, 420, 520, 640, 780, 920) for d in (0.05, 0.07, 0.09)]
    for t0 in contact_times(res, 0.03, 1.5):
        m.add(bank[rng.integers(len(bank))], t0, 0.08, rng.uniform(-0.6, 0.6))
    for s, e in bites(res):
        t = tt(0.35)                                     # big water-drop "plop"
        f = 160 + 700 * (t / 0.35) ** 1.5
        plop = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11) * np.minimum(1, t / 0.003)
        m.add(plop, e["t"], 0.5 + 0.3 * s, pan_of(e))
        for j in range(int(8 + 22 * s)):                 # bubble cascade
            m.add(bank[rng.integers(len(bank))], e["t"] + 0.05 + rng.exponential(0.12), 0.12,
                  rng.uniform(-0.8, 0.8))
    special(res, m, rise=lambda t, L: np.sin(2 * np.pi * np.cumsum(200 + 800 * (t / L)) / SR) * (t / L) ** 2,
            pop_f=700)
    m.reverb(0.22, 1.2, 3.5)


# ------------------------------------------------------------------ 4 KALIMBA (wood/metal tines)
def kalimba(res, m):
    rng = m.rng
    bank = {}
    def tine(f0, d=1.4):
        t = tt(d)
        s = (np.sin(2 * np.pi * f0 * t) + 0.25 * np.sin(2 * np.pi * f0 * 5.4 * t) * np.exp(-t * 10)
             + 0.1 * np.sin(2 * np.pi * f0 * 2 * t)) * np.exp(-t * 4.0) * np.minimum(1, t / 0.002)
        s[: int(0.004 * SR)] += np.random.default_rng(int(f0)).standard_normal(int(0.004 * SR)) * 0.15
        return s
    for t0 in contact_times(res, 0.02, 0.9):
        f0 = rng.choice(chord_at(res, t0)) * rng.choice([2, 4])
        key = round(f0, 1)
        if key not in bank:
            bank[key] = tine(f0)
        m.add(bank[key], t0, 0.04, rng.uniform(-0.6, 0.6))
    evs = [e for e in res["events"] if e["kind"] == "bite"]
    for s, e in bites(res):
        ch = chord_at(res, e["t"] + 0.01)
        for j, f in enumerate([ch[0] * 2, ch[1] * 2, ch[2] * 2, ch[0] * 4, ch[1] * 4]):   # arpeggio up
            m.add(tine(f, 1.8), e["t"] + j * 0.07, 0.18 + 0.12 * s, (j - 2) * 0.2)
    # warm pad following the chords (very soft)
    marks = [0.0] + [e["t"] for e in evs] + [res["duration"]]
    for a, b in zip(marks[:-1], marks[1:]):
        ch = chord_at(res, a + 0.01)
        t = tt(b - a + 0.6)
        env = np.minimum(1, t / 0.5) * np.minimum(1, np.maximum(0, (b - a + 0.6 - t) / 0.6))
        pad = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.003 * t) for f in ch) * env
        m.add(pad, a, 0.025)
    special(res, m, rise=lambda t, L: sum(np.sin(2 * np.pi * f * t) for f in (523, 659, 784)) * (t / L) ** 3 / 3,
            pop_f=1046.5)
    m.reverb(0.3, 1.8, 2.6)


# ------------------------------------------------------------------ 5 SOFT RAIN / ASMR TAPPING
def soft_rain(res, m, bite_gain=1.0):
    rng = m.rng
    def tap(center):
        n = int(0.02 * SR)
        x = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 260)
        k = max(2, int(SR / center / 2))
        return np.convolve(x, np.ones(k) / k, "same") - np.convolve(x, np.ones(k * 4) / (k * 4), "same")
    bank = [tap(c) for c in (1500, 2000, 2600, 3200) for _ in range(4)]
    for t0 in contact_times(res, 0.05, 2.5):
        m.add(bank[rng.integers(len(bank))], t0, 0.12, rng.uniform(-0.9, 0.9))
    for s, e in bites(res):
        t = tt(0.9)
        fw = np.convolve(rng.standard_normal(len(t)), np.ones(120) / 120, "same") * \
            np.minimum(1, t / 0.03) * np.exp(-t * 5) * 6
        sub = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 6) * np.minimum(1, t / 0.01)
        ch = chord_at(res, e["t"] + 0.01)
        shimmer = sum(np.sin(2 * np.pi * f * 4 * t) for f in ch) * np.exp(-t * 3) * np.minimum(1, t / 0.08) * 0.06
        m.add(fw + 0.6 * sub + shimmer, e["t"], (0.35 + 0.3 * s) * bite_gain, pan_of(e))
    t = tt(res["duration"])                               # very soft warm bed (loop-safe: whole length)
    bed = (np.sin(2 * np.pi * 132 * t) + 0.5 * np.sin(2 * np.pi * 198 * t)) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 5.2))
    m.add(bed, 0.0, 0.012)
    special(res, m, rise=lambda t, L: np.convolve(np.random.default_rng(4).standard_normal(len(t)),
                                                   np.ones(30) / 30, "same") * (t / L) ** 3 * 4, pop_f=440)
    m.reverb(0.28, 1.6, 3.0)


def special(res, m, rise, pop_f):
    """Implosion (rising sound into the pop), pop of the new ball, soft landing thud."""
    for e in res["events"]:
        if e["kind"] == "implode":
            L = 0.55
            m.add(rise(tt(L), L), e["t"], 0.5)
        if e["kind"] == "pop":
            t = tt(0.8)
            m.add((np.sin(2 * np.pi * pop_f * t) + 0.3 * np.sin(2 * np.pi * pop_f * 1.5 * t)) * np.exp(-t * 6)
                  * np.minimum(1, t / 0.003), e["t"], 0.35)
            for f in range(int(e["t"] * res["fps"]), len(res["frames"])):
                p = res["frames"][f]["pos"]
                if len(p) == 1 and p[0, 1] > sim.CY + sim.R - 12:
                    tl = tt(0.3)
                    m.add(np.sin(2 * np.pi * 95 * tl) * np.exp(-tl * 22), f / res["fps"], 0.3)
                    break


def rain_meow(res, m):
    """Regen-Design + das Miauen des Nutzers (assets/deep_meow.mp3) bei jedem Biss der Klingen."""
    a, sr = sf.read("build/meow.wav")
    on = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, on[0] - int(0.005 * SR)): on[-1] + int(0.05 * SR)]
    fade = int(0.01 * SR)
    a[:fade] *= np.linspace(0, 1, fade)
    a[-fade * 4:] *= np.linspace(1, 0, fade * 4)
    a = a / np.abs(a).max()
    soft_rain(res, m, bite_gain=0.35)
    for s, e in bites(res):
        m.add(a, e["t"], 0.55 + 0.35 * s, pan_of(e) * 0.5)
    m.reverb(0.22, 1.6, 3.0)


DESIGNS = {"1_jelly": jelly, "2_glas": glass, "3_plopp": bubbles, "4_kalimba": kalimba, "5_regen": soft_rain, "6_regen_miau": rain_meow}


def normalise(src, dst, target=-14.0):
    cur = src
    for it in range(4):
        m = subprocess.run(["ffmpeg", "-nostats", "-i", cur, "-af", "ebur128", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        integ = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1])
        if abs(integ - target) < 0.5 and it > 0:
            break
        nxt = dst.replace(".wav", f"_n{it}.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", cur, "-af",
                        f"volume={target - integ + 0.2}dB,alimiter=limit=0.89:attack=1:release=80:level=disabled", nxt],
                       check=True)
        cur = nxt
    subprocess.run(["cp", cur, dst], check=True)
    return integ


def build(name, res):
    m = Mix(res["duration"])
    DESIGNS[name](res, m)
    peak = max(np.abs(m.L).max(), np.abs(m.R).max())
    raw = f"build/snd_{name}_raw.wav"
    sf.write(raw, np.stack([m.L, m.R], 1) / peak * 0.9, SR)
    lufs = normalise(raw, f"build/snd_{name}.wav")
    print(name, f"{lufs:.1f} LUFS")


if __name__ == "__main__":
    res = pickle.load(open("build/sim.pkl", "rb"))
    for name in (sys.argv[1:] or DESIGNS):
        build(name, res)
