"""Sound design for 'Vice City' (numpy only) + tightened voice -> build/mix.wav."""
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

# ---- synthwave-ish driving beat (own synthesis), engine that revs with the speed
bpm = np.interp(T, [0, bounds[4][0], bounds[5][0], TOTAL], [100, 112, 128, 132])
ph = np.cumsum(bpm / 60) / SR
kick = np.exp(-((ph % 1.0) * 18)) * np.sin(2 * np.pi * 50 * T)
hat = (rng.standard_normal(N) - lp(rng.standard_normal(N), 6)) * np.exp(-(((ph + 0.5) % 1.0) * 30))
bassf = np.where((ph // 4) % 2 == 0, 55.0, 41.2)
bass = np.sign(np.sin(2 * np.pi * np.cumsum(bassf) / SR)) * np.exp(-(((ph * 2) % 1.0) * 6))
music += 0.8 * kick + 0.15 * hat + 0.25 * lp(bass, 30)
mask = np.ones(N)
mask[(T >= bounds[6][0]) & (T < bounds[6][1])] = 0
music *= lp(mask, 1200)
rpm = np.interp(T, [0, at("Du trittst"), at("Zweihundert."), at("Zweihundertvierzig"), at("Stopp"), bounds[7][0], TOTAL],
                [45, 45, 75, 95, 95, 85, 90])
engine = lp(np.sign(np.sin(2 * np.pi * np.cumsum(rpm) / SR)), 20)
emask = np.ones(N)
emask[(T >= bounds[2][0]) & (T < bounds[3][0])] = 0.3
emask[(T >= bounds[6][0]) & (T < bounds[6][1])] = 0
sfx += 0.12 * engine * lp(emask, 3000)

# ---- sfx
vn = int(1.4 * SR)
vt = np.arange(vn) / SR
add(sfx, np.sin(2 * np.pi * 160 * vt) * ((vt * 2.5) % 1 < 0.6), at("Dann vibriert"), 0.3)        # phone
e, t = dec(0.6, 6)
cash = (np.sin(2 * np.pi * 1318 * t) + np.sin(2 * np.pi * 1760 * t)) * e
add(sfx, cash, at("Dein Auftraggeber") + 0.6, 0.25)
e, t = dec(0.25, 15)
add(sfx, lp(rng.standard_normal(len(e)), 3) * e, BOUNDS1 if False else bounds[1][0] + 0.3, 0.6)   # TOP SECRET stamp
sirens = np.zeros(N)
s0 = at("Blaulicht")
sn = N - int(s0 * SR)
stt = np.arange(sn) / SR
sir = np.sin(2 * np.pi * np.cumsum(700 + 220 * np.sin(2 * np.pi * 0.8 * stt)) / SR)
level = np.interp(stt + s0, [s0, at("Dann drei"), at("Dann zehn"), at("Der Privatjet"), TOTAL], [0.03, 0.06, 0.12, 0.1, 0.14])
sirens[int(s0 * SR):] = sir * level
sfx += sirens * lp(mask, 1200)
rot = np.zeros(N)
rot[int(at("Ein Hubschrauber") * SR):int(at("Du reißt") * SR)] = 1
sfx += 0.14 * lp(rng.standard_normal(N), 30) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 12 * T))) * lp(rot, 3000)
sq = int(1.2 * SR)
sqt = np.arange(sq) / SR
add(sfx, np.sin(2 * np.pi * (1600 - 500 * sqt) * sqt) * np.hanning(sq), at("Du reißt") + 0.2, 0.18)  # tyre screech
jn = int((TOTAL - at("Der Privatjet")) * SR)
jt = np.arange(jn) / SR
add(sfx, lp(rng.standard_normal(jn), 4) * 0.5 + 0.3 * np.sin(2 * np.pi * 900 * jt), at("Der Privatjet"), 0.08)  # jet whine
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[6][0] - 0.1, 0.3)
e, t = dec(1.6, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k_ in ("Zwei Uhr", "Vertrau", "Dann zehn", "Straßensperre", "Noch fünfzig"):
    add(sfx, boom, at(k_), 0.55)

bed = music * 0.14 + sfx
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
