"""Sound design for 'Am Steuer' (numpy only) + voice mix -> build/mix.wav."""
import subprocess
import numpy as np
import soundfile as sf

from timing import PHRASES, TEMPO, VOICE, seq_bounds

SR = 48000
bounds, TOTAL = seq_bounds()
N = int(TOTAL * SR) + SR
T = np.arange(N) / SR
rng = np.random.default_rng(21)


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


music = np.zeros(N)
sfx = np.zeros(N)

# tense pulse: bass ostinato (8ths) + low drone, gets faster after the tracker
bpm = np.interp(T, [0, at("ein Peilsender"), TOTAL], [96, 120, 132])
ph = np.cumsum(bpm / 60 * 2) / SR
env8 = np.exp(-((ph % 1.0) * 9))
notes = np.where((ph // 4) % 2 == 0, 55.0, 49.0)
music += 0.35 * env8 * np.sign(np.sin(2 * np.pi * np.cumsum(notes) / SR)) * 0.5
music = lp(music, 30)
music += 0.25 * np.sin(2 * np.pi * 41.2 * T)
kick = np.exp(-(((ph / 2) % 1.0) * 25)) * np.sin(2 * np.pi * 50 * T)
music += 0.5 * kick

# silence in the PAUSE
mask = np.ones(N)
mask[(T >= bounds[6][0]) & (T < bounds[6][1])] = 0
music *= lp(mask, 1200)

# morning street ambience (scenes 0-3, 9-12): soft noise + birds
amb = lp(rng.standard_normal(N), 40) * 0.6
amask = np.zeros(N)
for i in (0, 1, 2, 3, 9, 10, 12):
    amask[int(bounds[i][0] * SR):int(bounds[i][1] * SR)] = 1
sfx += 0.05 * amb * lp(amask, 4000)
for k in range(12):
    t0 = rng.uniform(0, bounds[3][1])
    n = int(0.12 * SR)
    tt = np.arange(n) / SR
    chirp = np.sin(2 * np.pi * np.cumsum(3000 + 1500 * np.sin(tt * 60)) / SR) * np.hanning(n)
    add(sfx, chirp, t0, 0.03)

# truck arrives: engine + brake squeal
en = int(4.5 * SR)
et = np.arange(en) / SR
engine = lp(np.sign(np.sin(2 * np.pi * np.cumsum(55 - 15 * np.clip(et / 4, 0, 1)) / SR)), 25)
add(sfx, engine * np.clip(1 - et / 4.5, 0, 1), 0.0, 0.25)
sq = int(0.8 * SR)
st = np.arange(sq) / SR
add(sfx, np.sin(2 * np.pi * (2400 - 600 * st) * st) * np.hanning(sq), 3.2, 0.06)

# footsteps (run) and case thuds
e, t = dec(0.1, 45)
step = lp(rng.standard_normal(len(e)), 10) * e
a2 = at("Du springst raus")
for k in range(9):
    add(sfx, step, a2 + k * 0.22, 0.4)
e, t = dec(0.4, 12)
thud = np.sin(2 * np.pi * 90 * t) * e
a3 = bounds[3][0]
for k in range(4):
    add(sfx, thud, a3 + 0.25 + k * 0.38, 0.5)
add(sfx, engine[: int(2.5 * SR)][::-1] * 0.8, at("Leon gibt Gas"), 0.3)

# phone vibration
vn = int(1.2 * SR)
vt = np.arange(vn) / SR
add(sfx, np.sin(2 * np.pi * 160 * vt) * ((vt * 2.5) % 1 < 0.6), at("Dann vibriert"), 0.25)
e, t = dec(0.15, 30)
add(sfx, np.sin(2 * np.pi * 1300 * t) * e, at("Danke fürs"), 0.25)  # message ping

# tape stop into PAUSE
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[6][0] - 0.1, 0.35)

# case latches + tracker beeps
e, t = dec(0.06, 70)
click = (rng.standard_normal(len(e)) * 0.5 + np.sin(2 * np.pi * 2200 * t)) * e
add(sfx, click, bounds[7][0] + 0.2, 0.5)
add(sfx, click, bounds[7][0] + 0.35, 0.5)
e, t = dec(0.08, 30)
beep = np.sin(2 * np.pi * 2000 * t) * e
for k in range(int((bounds[8][0] - at("ein Peilsender")) / 0.5)):
    add(sfx, beep, at("ein Peilsender") + k * 0.5, 0.15)

# indicator ticking while turning
tick = np.sin(2 * np.pi * 900 * np.arange(int(0.03 * SR)) / SR) * np.hanning(int(0.03 * SR))
for k in range(8):
    add(sfx, tick, at("Und biegt ab") + k * 0.4, 0.15)

# warehouse roll gate rattle
gn = int(1.8 * SR)
rattle = rng.standard_normal(gn) * (np.sin(2 * np.pi * 18 * np.arange(gn) / SR) > 0.3) * np.hanning(gn)
add(sfx, lp(rattle, 6), bounds[9][0] + 0.1, 0.18)

# camera shutter clicks + stamp
for k in range(4):
    add(sfx, click, bounds[11][0] + 0.2 + k * 0.35, 0.6)
e, t = dec(1.4, 3)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k in ("Und nickt.", "ein Peilsender.", "Keine Kamera hat", "dich."):
    add(sfx, boom, at(k), 0.6)

# sirens finale
a12 = bounds[12][0] - 0.5
sn = int((TOTAL - a12) * SR)
stt = np.arange(sn) / SR
siren = np.sin(2 * np.pi * np.cumsum(650 + 200 * np.sin(2 * np.pi * 0.7 * stt)) / SR) * np.clip(stt / 1.5, 0, 1)
add(sfx, siren, a12, 0.12)

bed = music * 0.18 + sfx

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-filter:a", f"atempo={TEMPO}",
                "-ar", str(SR), "-ac", "1", "build/voice_fast.wav"], check=True)
voice, _ = sf.read("build/voice_fast.wav")
v = np.zeros(N)
v[: min(N, len(voice))] = voice[:N]
venv = lp(np.abs(v), 2400)
duck = 1.0 - 0.45 * np.clip(venv / (venv.max() * 0.25 + 1e-9), 0, 1)
mix = (v + bed * duck)[: int(TOTAL * SR)]
f = int(0.3 * SR)
mix[-f:] *= np.linspace(1, 0, f)
mix /= np.abs(mix).max() / 0.95
sf.write("build/mix.wav", np.stack([mix, mix], 1), SR)
print("mix", round(TOTAL, 2))
