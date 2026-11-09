"""Sound design for '24 Stunden verschwinden' (numpy only) + tightened voice -> build/mix.wav."""
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
    return next(a / TEMPO for a, b, s, t in PHRASES if t.startswith(text))


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

# ---- thriller bed: ticking clock + pulse, silence at the pause and before the door
tick = np.zeros(N)
e, t = dec(0.03, 120)
tk = np.sin(2 * np.pi * 2600 * t) * e
for k in range(int(TOTAL)):
    add(tick, tk, k * 1.0, 0.18 if k % 2 == 0 else 0.1)
bpm = np.interp(T, [0, bounds[3][0], bounds[6][0], bounds[8][0], TOTAL], [80, 90, 105, 130, 140])
ph = np.cumsum(bpm / 60) / SR
beat = np.exp(-((ph % 1.0) * 22)) + 0.6 * np.exp(-(((ph - 0.22) % 1.0) * 22))
music += 0.55 * beat * np.sin(2 * np.pi * 45 * T)
music += 0.16 * np.sin(2 * np.pi * 41.2 * T) + 0.05 * lp(np.sign(np.sin(2 * np.pi * 82.4 * T)) + np.sign(np.sin(2 * np.pi * 87.3 * T)), 120)
mask = np.ones(N)
mask[(T >= bounds[5][0]) & (T < bounds[5][1])] = 0
mask[(T >= at("Die Tür geht")) & (T < at("Er sagt nur"))] = 0.1
music = music * lp(mask, 1200) + tick * lp(mask, 1200)

# ---- sfx
e, t = dec(0.6, 5)
cash = (np.sin(2 * np.pi * 1318 * t) + np.sin(2 * np.pi * 1760 * t)) * e
add(sfx, cash, 0.1, 0.3)
en = int(3.0 * SR)
et = np.arange(en) / SR
eng = lp(np.sign(np.sin(2 * np.pi * np.cumsum(40 + 6 * np.sin(et)) / SR)), 30) * np.hanning(en)
add(sfx, eng, at("In derselben"), 0.3)                                                          # SUV
gn = int(0.8 * SR)
add(sfx, (rng.standard_normal(gn) - lp(rng.standard_normal(gn), 4)) * np.exp(-np.arange(gn) / SR * 6), at("Dein Handy wird") + 0.3, 0.5)  # smash
e, t = dec(0.06, 70)
click = (rng.standard_normal(len(e)) * 0.4 + np.sin(2 * np.pi * 1800 * t)) * e
for k in range(5):
    add(sfx, click, at("Dein Name") + k * 0.4, 0.25)                                         # delete clicks
add(sfx, cash, at("fünf Millionen"), 0.3)
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[5][0] - 0.1, 0.3)
rn = int(1.8 * SR)
rt = np.arange(rn) / SR
add(sfx, (np.sin(2 * np.pi * 440 * rt) + np.sin(2 * np.pi * 480 * rt)) * ((rt * 2) % 1 < 0.6) * np.hanning(rn), at("Im Hotelzimmer"), 0.12)
pn = int(0.8 * SR)
add(sfx, lp(rng.standard_normal(pn), 4) * np.hanning(pn), at("Auf dem Bett"), 0.12)
e, t = dec(0.15, 30)
add(sfx, lp(rng.standard_normal(len(e)), 6) * e + np.sin(2 * np.pi * 900 * t) * e * 0.5, at("Dann hörst") + 0.8, 0.6)   # key click
add(sfx, np.sin(2 * np.pi * 1300 * t) * e, at("Zielperson"), 0.3)
cn = int(1.4 * SR)
ctt = np.arange(cn) / SR
add(sfx, np.sin(2 * np.pi * np.cumsum(160 + 80 * np.sin(ctt * 8)) / SR) * np.hanning(cn), at("Die Tür geht"), 0.25)  # door creak
e, t = dec(1.6, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k_ in ("Zwanzig", "Unternehmer tot", "Bleib tot.", "Zielperson", "Die 24"):
    add(sfx, boom, at(k_), 0.55)

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
