"""Builds a STIL-4 simulation video: simulate -> sound -> render frames (parallel) -> mp4 (60 fps, -14 LUFS).

python3 make_video.py OUT.mp4 [duration]
"""
import json
import pickle
import re
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf

import render
import sim

OUT = sys.argv[1] if len(sys.argv) > 1 else "output/test_15s.mp4"
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 15.0
CFG = dict(duration=DUR, goal=6000, targets=(30, 180, 700, 2000, 4000, 6000), period0=2.6, speedup=0.95,
           rb=3.8, seed=7)
SR = 48000
STATE = "build/sim.pkl"


# ------------------------------------------------------------------ sound (own synthesis)
def lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def sound(res, path):
    fps = res["fps"]
    n = int(DUR * SR) + SR
    out = np.zeros(n)
    rng = np.random.default_rng(3)

    def add(sig, t0, g):
        i = int(t0 * SR)
        if 0 <= i < n:
            sig = sig[: n - i]
            out[i:i + len(sig)] += sig * g

    for k, e in enumerate(res["events"]):
        lvl = min(1.0, 0.55 + 0.09 * k)                       # every explosion a bit bigger
        L = 1.6
        t = np.arange(int(L * SR)) / SR
        sub = np.sin(2 * np.pi * np.cumsum(35 + 55 * np.exp(-t * 5)) / SR) * np.exp(-t * 2.6)
        noise = lp(rng.standard_normal(len(t)), 25) * np.exp(-t * 9) * 2.5
        whistle_f = 660 + 640 * np.exp(-t * 6)                 # 1.3 kHz -> 660 Hz, like the reference
        whistle = np.sin(2 * np.pi * np.cumsum(whistle_f) / SR) * np.exp(-t * 3.2) * 0.35
        ring = np.sin(2 * np.pi * 700 * t) * np.exp(-t * 4) * 0.12
        crack = rng.standard_normal(len(t)) * np.exp(-t * 60) * 0.6
        add(sub + noise + whistle + ring + crack, e["t"], lvl)
        # charge-up: rising soft plings in the 0.8 s before the bite
        for j in range(5):
            tt = np.arange(int(0.25 * SR)) / SR
            f0 = [392, 440, 523, 587, 659][j] * (1 + 0.1 * k)
            add(np.sin(2 * np.pi * f0 * tt) * np.exp(-tt * 14) * 0.05, e["t"] - 0.8 + j * 0.15, 1.0)
    # collision ticks: density from blade contacts, very quiet, high pitched
    tick_t = np.arange(int(0.012 * SR)) / SR
    for f, fr in enumerate(res["frames"]):
        c = fr["contacts"]
        m = min(6, int(np.log1p(c)))
        for _ in range(m):
            fq = rng.uniform(2200, 6000)
            add(np.sin(2 * np.pi * fq * tick_t) * np.exp(-tick_t * 400), f / fps + rng.uniform(0, 1 / fps), 0.02)
    out = out[: int(DUR * SR)]
    out /= np.abs(out).max() / 0.9
    sf.write("build/raw.wav", np.stack([out, out], 1), SR)
    # -14 LUFS (measure, then linear gain + true-peak limiter; keeps the silence silent)
    m = subprocess.run(["ffmpeg", "-nostats", "-i", "build/raw.wav", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1])
    gain = -14.0 - I
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "build/raw.wav", "-af",
                    f"volume={gain}dB,alimiter=limit=0.89:attack=1:release=60:level=disabled", path], check=True)


# ------------------------------------------------------------------ video
_RES = None


def _init():
    global _RES
    _RES = pickle.load(open(STATE, "rb"))


def _frame(f):
    t = f / _RES["fps"]
    return render.render_frame(_RES["frames"][f], t, _RES["events"], _RES["goal"], _RES["rb"]).tobytes()


def main():
    res = sim.simulate(**CFG, log=lambda m: None)
    pickle.dump(res, open(STATE, "wb"))
    json.dump(res["events"], open("build/events.json", "w"), indent=1)
    for e in res["events"]:
        print(f"bite {e['stage']} @ {e['t']:.2f}s caught {e['caught']} -> {e['total']}")
    sound(res, "build/mix.wav")
    nf = len(res["frames"])
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{sim.W}x{sim.H}",
           "-r", str(res["fps"]), "-i", "-", "-i", "build/mix.wav", "-c:v", "libx264", "-preset", "medium",
           "-b:v", "14M", "-maxrate", "18M", "-bufsize", "28M", "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-shortest", OUT]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(4, initializer=_init) as pool:
        for k, buf in enumerate(pool.imap(_frame, range(nf), chunksize=4)):
            ff.stdin.write(buf)
            if k % 120 == 0:
                print(f"{k}/{nf}", flush=True)
    ff.stdin.close()
    ff.wait()
    print("done", OUT)


if __name__ == "__main__":
    main()
