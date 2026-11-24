"""Gemeinsame Helfer für die 5 Experimente: Video-Encoding (1080x1920, exakt 8 s) + Ton (-14 LUFS, Loop-sicher)."""
import re
import subprocess
from multiprocessing import Pool

import numpy as np
import soundfile as sf

W, H = 1080, 1920
DUR = 8.0
SR = 48000


def encode(render, fps, wav, out, workers=4, bitrate="12M"):
    """render(i) -> HxWx3 uint8 array; frames are rendered in parallel and piped to ffmpeg."""
    n = int(round(DUR * fps))
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
           "-i", "-", "-i", wav, "-c:v", "libx264", "-preset", "slow", "-b:v", bitrate, "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR:.3f}", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(workers) as pool:
        for k, fr in enumerate(pool.imap(render, range(n), chunksize=2)):
            ff.stdin.write(np.ascontiguousarray(fr, dtype=np.uint8).tobytes())
    ff.stdin.close()
    ff.wait()
    print("done", out)


def t_axis(d):
    return np.arange(int(d * SR)) / SR


class Track:
    """Circular stereo buffer of exactly DUR seconds (everything that runs over the end wraps to the start)."""

    def __init__(self):
        self.n = int(DUR * SR)
        self.L = np.zeros(self.n)
        self.R = np.zeros(self.n)

    def add(self, sig, t0, g=1.0, pan=0.0):
        i = int(round(t0 * SR)) % self.n
        idx = (np.arange(len(sig)) + i) % self.n
        np.add.at(self.L, idx, sig * g * np.sqrt(0.5 * (1 - pan)))
        np.add.at(self.R, idx, sig * g * np.sqrt(0.5 * (1 + pan)))

    def save(self, path, target=-14.0, reverb=0.0):
        L, R = self.L, self.R
        if reverb:
            from scipy.signal import fftconvolve
            t = t_axis(1.4)
            out = []
            for ch, sd in ((L, 1), (R, 2)):
                ir = np.random.default_rng(sd).standard_normal(len(t)) * np.exp(-t * 3)
                ir = np.convolve(ir, np.ones(8) / 8, "same")
                ir /= np.sqrt((ir ** 2).sum())
                y = fftconvolve(ch, ir)
                w = y[: self.n].copy()
                w[: len(y) - self.n] += y[self.n:]
                out.append(ch * (1 - reverb) + w * reverb)
            L, R = out
        peak = max(np.abs(L).max(), np.abs(R).max()) + 1e-9
        raw = path.replace(".wav", "_raw.wav")
        sf.write(raw, np.stack([L, R], 1) / peak * 0.9, SR)
        cur = raw
        for it in range(4):
            m = subprocess.run(["ffmpeg", "-nostats", "-i", cur, "-af", "ebur128", "-f", "null", "-"],
                               capture_output=True, text=True).stderr
            integ = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", m)[-1])
            if abs(integ - target) < 0.6 and it > 0:
                break
            nxt = path.replace(".wav", f"_n{it}.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", cur, "-af",
                            f"volume={target - integ + 0.2}dB,alimiter=limit=0.89:attack=1:release=60:level=disabled",
                            nxt], check=True)
            cur = nxt
        subprocess.run(["cp", cur, path], check=True)
        print("audio", path, f"{integ:.1f} LUFS")
