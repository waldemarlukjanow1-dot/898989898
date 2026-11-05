"""Sound design for 'Tag 1 der Dunkelheit' (numpy only) + tightened voice -> build/mix.wav."""
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

# ---- dark drone + heartbeat, silence before the question
bpm = np.interp(T, [0, bounds[3][0], bounds[7][0], bounds[9][0], TOTAL], [60, 75, 100, 130, 130])
ph = np.cumsum(bpm / 60) / SR
beat = np.exp(-((ph % 1.0) * 22)) + 0.6 * np.exp(-(((ph - 0.22) % 1.0) * 22))
music += 0.6 * beat * np.sin(2 * np.pi * 45 * T) * np.clip((T - 2) / 4, 0, 1)
music += 0.25 * np.sin(2 * np.pi * 38 * T) + 0.06 * lp(np.sign(np.sin(2 * np.pi * 76 * T)) + np.sign(np.sin(2 * np.pi * 80.5 * T)), 150)
mask = np.ones(N)
mask[(T >= bounds[6][0]) & (T < bounds[6][1])] = 0
mask[(T >= at("Lass mich rein.") + 0.6) & (T < at("Würdest du"))] = 0.0
music *= lp(mask, 1200)

# ---- sfx
e, t = dec(0.6, 3)
add(sfx, np.sign(np.sin(2 * np.pi * 880 * t)) * ((t * 6) % 1 < 0.5) * e * 0.3, 0.1, 0.15)    # alarm clock beep
add(sfx, lp(rng.standard_normal(int(1.0 * SR)), 2) * np.hanning(int(1.0 * SR)), at("Du schaltest"), 0.06)  # tv static
pd_n = int(1.2 * SR)
pdt = np.arange(pd_n) / SR
powerdown = np.sin(2 * np.pi * np.cumsum(400 * np.exp(-pdt * 3) + 30) / SR) * np.exp(-pdt * 2)
add(sfx, powerdown, at("Dann fällt der Strom"), 0.35)                                        # power off
e, t = dec(0.15, 25)
ping = np.sin(2 * np.pi * 1400 * t) * e
for k_ in ("Eine Nachricht", "Weil ich dich", "Draußen."):
    add(sfx, ping, at(k_), 0.3)                                                               # chat pings
e, t = dec(0.35, 14)
knock = lp(rng.standard_normal(len(e)), 25) * e * 2 + np.sin(2 * np.pi * 80 * t) * e
seq7 = bounds[7]
for h in (0.22, 0.31, 0.40):
    add(sfx, knock, seq7[0] + h * (seq7[1] - seq7[0]), 0.9)                                  # BUMM x3
rn = int(1.8 * SR)
rt = np.arange(rn) / SR
ring = (np.sin(2 * np.pi * 900 * rt) + np.sin(2 * np.pi * 1200 * rt)) * ((rt * 3) % 1 < 0.5) * np.hanning(rn)
add(sfx, ring, at("Dein Handy klingelt"), 0.1)
e, t = dec(1.6, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k_ in ("Aber draußen", "Weil ich dich", "Niemand da.", "Deine eigene Stimme."):
    add(sfx, boom, at(k_), 0.6)
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[6][0] - 0.1, 0.3)

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
