"""Sound design for 'Das neue Virus' (numpy only) + tightened voice -> build/mix.wav."""
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

# ---- uneasy pulse + drone; silence after the question in the pause
bpm = np.interp(T, [0, bounds[3][0], bounds[5][0], bounds[8][0], TOTAL], [85, 100, 110, 120, 120])
ph = np.cumsum(bpm / 60) / SR
beat = np.exp(-((ph % 1.0) * 22)) + 0.6 * np.exp(-(((ph - 0.22) % 1.0) * 22))
music += 0.5 * beat * np.sin(2 * np.pi * 45 * T)
music += 0.2 * np.sin(2 * np.pi * 41.2 * T) + 0.05 * lp(np.sign(np.sin(2 * np.pi * 98 * T)) + np.sign(np.sin(2 * np.pi * 103.8 * T)), 120)
mask = np.ones(N)
mask[(T >= bounds[6][0]) & (T < bounds[6][1])] = 0
mask[T >= bounds[10][0]] = 0.35
music *= lp(mask, 1200)

# ---- sfx
vn = int(1.6 * SR)
vt = np.arange(vn) / SR
add(sfx, np.sin(2 * np.pi * 160 * vt) * ((vt * 3) % 1 < 0.6), at("Dein Handy explodiert"), 0.3)    # phone buzzing
e, t = dec(0.15, 25)
ping = np.sin(2 * np.pi * 1400 * t) * e
for k in range(4):
    add(sfx, ping, at("Dein Handy explodiert") + 0.2 + k * 0.45, 0.25)
crowd = lp(rng.standard_normal(N), 25)
cm = np.zeros(N)
cm[int(bounds[1][0] * SR):int(bounds[1][1] * SR)] = 1
sfx += 0.06 * crowd * lp(cm, 3000)                                                                 # supermarket chaos
bus = lp(np.sign(np.sin(2 * np.pi * 38 * T)), 60)
bm = np.zeros(N)
bm[int(bounds[2][0] * SR):int(bounds[2][1] * SR)] = 1
sfx += 0.06 * bus * lp(bm, 3000)                                                                   # bus engine
a3 = bounds[3][0]
sn = int((bounds[4][0] - a3) * SR)
stt = np.arange(sn) / SR
add(sfx, np.sin(2 * np.pi * np.cumsum(650 + 200 * np.sin(2 * np.pi * 0.7 * stt)) / SR) * np.hanning(sn), a3, 0.05)   # far siren
pn = int(0.8 * SR)
add(sfx, lp(rng.standard_normal(pn), 4) * np.hanning(pn), at("Dann kommt der Brief"), 0.12)       # paper
bn = int(0.35 * SR)
buzz = np.sign(np.sin(2 * np.pi * 120 * np.arange(bn) / SR)) * np.hanning(bn)
for k_ in ("Ohne Nachweis kein", "Kein Kino"):
    add(sfx, lp(buzz, 4), at(k_), 0.12)
add(sfx, ping, at("Ohne Nachweis brauchst"), 0.3)
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[6][0] - 0.1, 0.3)
fam = np.zeros(N)
fam[int(bounds[7][0] * SR):int(bounds[7][1] * SR)] = 1
sfx += 0.05 * lp(rng.standard_normal(N), 18) * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * T)) * lp(fam, 2000)   # arguing murmur
add(sfx, np.sin(2 * np.pi * 160 * vt) * ((vt * 3) % 1 < 0.6), at("Dein Handy vibriert"), 0.3)
e, t = dec(1.6, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k_ in ("Eilmeldung", "Maskenpflicht.", "Ausgangssperre", "Impfung.", "Macht ihr das"):
    add(sfx, boom, at(k_), 0.5)

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
