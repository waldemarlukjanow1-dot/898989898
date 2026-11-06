"""Sound design for 'Lager 17' (numpy only) + tightened voice -> build/mix.wav."""
import subprocess
import numpy as np
import soundfile as sf

from timing import PHRASES, TEMPO, VOICE, seq_bounds, tight_layout

SR = 48000
bounds, TOTAL = seq_bounds()
N = int(TOTAL * SR) + SR
T = np.arange(N) / SR
rng = np.random.default_rng(51)


def at(text):
    return next(a / TEMPO for a, b, s, t in PHRASES if text in t)


def lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def add(buf, sig, t0, g=1.0):
    i = int(t0 * SR)
    if 0 <= i < len(buf):
        sig = sig[: len(buf) - i]
        buf[i:i + len(sig)] += sig * g


def dec(sec, rate):
    t = np.arange(int(sec * SR)) / SR
    return np.exp(-t * rate), t


# ---- voice: tighten pauses, speed up
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-ar", str(SR), "-ac", "1", "build/voice_raw.wav"], check=True)
raw, _ = sf.read("build/voice_raw.wav")
lay = tight_layout()
tight = np.zeros(int((lay[-1][2] + lay[-1][1] - lay[-1][0] + 0.5) * SR))
fade = int(0.02 * SR)
for a0, b0, n in lay:
    s_ = raw[int(a0 * SR):int(b0 * SR)].copy()
    s_[:fade] *= np.linspace(0, 1, fade)
    s_[-fade:] *= np.linspace(1, 0, fade)
    tight[int(n * SR):int(n * SR) + len(s_)] += s_
sf.write("build/voice_tight.wav", tight, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "build/voice_tight.wav", "-filter:a", f"atempo={TEMPO}",
                "build/voice_fast.wav"], check=True)

music = np.zeros(N)
sfx = np.zeros(N)

# ---- tension: pulse + drone, faster when the trouble starts
bpm = np.interp(T, [0, bounds[2][0], bounds[4][0], bounds[8][0], TOTAL], [80, 95, 110, 125, 140])
ph = np.cumsum(bpm / 60) / SR
beat = np.exp(-((ph % 1.0) * 22)) + 0.6 * np.exp(-(((ph - 0.22) % 1.0) * 22))
music += 0.55 * beat * np.sin(2 * np.pi * 45 * T)
music += 0.2 * np.sin(2 * np.pi * 41.2 * T) + 0.05 * lp(np.sign(np.sin(2 * np.pi * 82.4 * T)) + np.sign(np.sin(2 * np.pi * 87.3 * T)), 120)
# magic shimmer while the gold is shown
shim = np.zeros(N)
shim[int(at("Gold.") * SR):int(bounds[4][0] * SR)] = 1
music += 0.08 * (np.sin(2 * np.pi * 880 * T) + np.sin(2 * np.pi * 1318.5 * T)) * (0.5 + 0.5 * np.sin(2 * np.pi * 6 * T)) * lp(shim, 6000)
mask = np.ones(N)
mask[(T >= bounds[7][0]) & (T < bounds[7][1])] = 0
mask[(T >= at("Dann hörst du auf")) & (T < at("Denn jetzt"))] = 0.2
music *= lp(mask, 1200)

# ---- sfx
e, t = dec(0.25, 18)
gavel = lp(rng.standard_normal(len(e)), 20) * e * 2 + np.sin(2 * np.pi * 220 * t) * e
add(sfx, gavel, bounds[0][0] + 0.5 * (bounds[0][1] - bounds[0][0]), 0.6)                  # hammer
gn = int(1.4 * SR)
gt = np.arange(gn) / SR
add(sfx, lp(np.sign(np.sin(2 * np.pi * (14 + 8 * gt) * gt)) * rng.standard_normal(gn), 8) * np.hanning(gn), bounds[0][0] + 4.2, 0.15)  # roll door
e, t = dec(0.06, 70)
click = (rng.standard_normal(len(e)) * 0.5 + np.sin(2 * np.pi * 2200 * t)) * e
for k in range(3):
    add(sfx, click, bounds[2][0] + 0.3 + k * 0.8, 0.4)                                        # tools, day 1-3
cn = int(1.2 * SR)
ct = np.arange(cn) / SR
creak = np.sin(2 * np.pi * np.cumsum(180 + 90 * np.sin(ct * 9)) / SR) * np.hanning(cn)
add(sfx, creak, at("Dann siehst"), 0.25)                                                      # safe door
e, t = dec(0.6, 5)
cash = (np.sin(2 * np.pi * 1318 * t) + np.sin(2 * np.pi * 1760 * t)) * e
add(sfx, cash, at("Gold."), 0.35)
e, t = dec(1.6, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k_ in ("Verkaufen?", "Verstecken?", "Behalten?", "Wer das findet", "Seit einer Stunde."):
    add(sfx, boom, at(k_), 0.55)
rn = int(1.6 * SR)
rt = np.arange(rn) / SR
add(sfx, (np.sin(2 * np.pi * 900 * rt) + np.sin(2 * np.pi * 1200 * rt)) * ((rt * 3) % 1 < 0.5) * np.hanning(rn), at("Dann ruft"), 0.1)
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[7][0] - 0.1, 0.3)
pn = int(0.8 * SR)
add(sfx, lp(rng.standard_normal(pn), 4) * np.hanning(pn), at("ein Zettel"), 0.12)               # paper
idle = lp(np.sign(np.sin(2 * np.pi * 32 * T)), 40)                                           # car idling outside
im_ = np.zeros(N)
im_[int(bounds[10][0] * SR):] = 1
sfx += 0.08 * idle * lp(im_, 6000)

bed = music * 0.2 + sfx
voice, _ = sf.read("build/voice_fast.wav")
v = np.zeros(N)
v[: min(N, len(voice))] = voice[:N]
venv = lp(np.abs(v), 2400)
duck = 1.0 - 0.5 * np.clip(venv / (venv.max() * 0.25 + 1e-9), 0, 1)
mix = (v + bed * duck)[: int(TOTAL * SR)]
f = int(0.3 * SR)
mix[-f:] *= np.linspace(1, 0, f)
mix /= np.abs(mix).max() / 0.95
sf.write("build/mix.wav", np.stack([mix, mix], 1), SR)
print("mix", round(TOTAL, 2), "voice", round(len(voice) / SR, 2))
