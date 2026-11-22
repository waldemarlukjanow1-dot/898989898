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

OUT = sys.argv[1] if len(sys.argv) > 1 else "output/simulation_loop.mp4"
SOUND = "6_regen_miau"                                   # design from sounds.py
# v2: bigger balls, faster blades. 32 x 1.8 s = 57.6 s, seamless loop, 31 bites, goal 3000
CFG = dict(period=1.8, n_periods=32, rb=6.0, seed=11, targets=sim.gentle_targets(31, first=10, last=3000))
SR = 48000
STATE = "build/sim.pkl"


# ------------------------------------------------------------------ sound (own synthesis)
def lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def sound(res, path):
    """Everything is added into a circular buffer of exactly the video length -> the audio loops seamlessly too."""
    fps, dur = res["fps"], res["duration"]
    n = int(round(dur * SR))
    out = np.zeros(n)
    rng = np.random.default_rng(3)

    def add(sig, t0, g):
        i = int(round(t0 * SR)) % n
        idx = (np.arange(len(sig)) + i) % n
        np.add.at(out, idx, sig * g)

    bites = [e for e in res["events"] if e["kind"] == "bite"]
    for k, e in enumerate(bites):
        lvl = 0.45 + 0.55 * k / max(1, len(bites) - 1)       # every explosion a bit bigger
        L = 1.6
        t = np.arange(int(L * SR)) / SR
        sub = np.sin(2 * np.pi * np.cumsum(35 + 55 * np.exp(-t * 5)) / SR) * np.exp(-t * 2.6)
        noise = lp(rng.standard_normal(len(t)), 25) * np.exp(-t * 9) * 2.5
        whistle = np.sin(2 * np.pi * np.cumsum(660 + 640 * np.exp(-t * 6)) / SR) * np.exp(-t * 3.2) * 0.35
        ring = np.sin(2 * np.pi * 700 * t) * np.exp(-t * 4) * 0.12
        crack = rng.standard_normal(len(t)) * np.exp(-t * 60) * 0.6
        add(sub + noise + whistle + ring + crack, e["t"], lvl)
        for j in range(5):                                    # charge-up plings before the bite
            tt = np.arange(int(0.25 * SR)) / SR
            f0 = [392, 440, 523, 587, 659][j] * (1 + 0.012 * k)
            add(np.sin(2 * np.pi * f0 * tt) * np.exp(-tt * 14) * 0.05, e["t"] - 0.8 + j * 0.15, 1.0)
    for e in res["events"]:
        if e["kind"] == "implode":                            # reversed boom: everything is sucked in
            L = 0.55
            t = np.arange(int(L * SR)) / SR
            sw = np.sin(2 * np.pi * np.cumsum(120 + 900 * (t / L) ** 2) / SR) * (t / L) ** 2 * 0.5
            hiss = lp(rng.standard_normal(len(t)), 6) * (t / L) ** 3 * 0.8
            add(sw + hiss, e["t"], 0.9)
        if e["kind"] == "pop":                                # the new single ball
            t = np.arange(int(0.5 * SR)) / SR
            add(np.sin(2 * np.pi * 880 * t) * np.exp(-t * 9) * 0.5 + np.sin(2 * np.pi * 1320 * t) * np.exp(-t * 12) * 0.2,
                e["t"], 1.0)
    # soft thud when the single ball lands at the bottom
    pop = [e for e in res["events"] if e["kind"] == "pop"]
    if pop:
        for f in range(int(pop[0]["t"] * fps), len(res["frames"])):
            p = res["frames"][f]["pos"]
            if len(p) == 1 and p[0, 1] > sim.CY + sim.R - 12:
                t = np.arange(int(0.25 * SR)) / SR
                add(np.sin(2 * np.pi * 90 * t) * np.exp(-t * 25) * 0.4, f / fps, 1.0)
                break
    tick_t = np.arange(int(0.012 * SR)) / SR                  # collision ticks, very quiet
    for f, fr in enumerate(res["frames"]):
        for _ in range(min(6, int(np.log1p(fr["contacts"])))):
            add(np.sin(2 * np.pi * rng.uniform(2200, 6000) * tick_t) * np.exp(-tick_t * 400),
                f / fps + rng.uniform(0, 1 / fps), 0.02)
    out /= np.abs(out).max() / 0.9
    sf.write("build/raw.wav", np.stack([out, out], 1), SR)
    # -14 LUFS: gain + true-peak limiter, repeated until close to the target
    src = "build/raw.wav"
    for it in range(4):
        m = subprocess.run(["ffmpeg", "-nostats", "-i", src, "-af", "ebur128", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1])
        print(f"loudness pass {it}: {I:.1f} LUFS")
        if abs(I + 14.0) < 0.5 and it > 0:
            break
        dst = f"build/norm{it}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af",
                        f"volume={-14.0 - I + 0.3}dB,alimiter=limit=0.89:attack=1:release=80:level=disabled", dst],
                       check=True)
        src = dst
    subprocess.run(["cp", src, path], check=True)


# ------------------------------------------------------------------ video
_RES = None


def _init():
    global _RES
    _RES = pickle.load(open(STATE, "rb"))


def _frame(f):
    t = f / _RES["fps"]
    return render.render_frame(_RES["frames"][f], t, _RES["events"], _RES["goal"], _RES["rb"]).tobytes()


def main():
    res = sim.simulate_loop(**CFG, log=print)
    pickle.dump(res, open(STATE, "wb"))
    json.dump(res["events"], open("build/events.json", "w"), indent=1)
    for e in res["events"]:
        print(f"bite {e['stage']} @ {e['t']:.2f}s caught {e['caught']} -> {e['total']}")
    import sounds
    sounds.build(SOUND, res)
    subprocess.run(["cp", f"build/snd_{SOUND}.wav", "build/mix.wav"], check=True)
    nf = len(res["frames"])
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{sim.W}x{sim.H}",
           "-r", str(res["fps"]), "-i", "-", "-i", "build/mix.wav", "-c:v", "libx264", "-preset", "medium",
           "-b:v", "11M", "-maxrate", "14M", "-bufsize", "22M", "-pix_fmt", "yuv420p", "-profile:v", "high",
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
