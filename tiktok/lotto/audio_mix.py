"""Sound design for 'Der Schein' (numpy only) + voice mix -> build/mix.wav."""
import subprocess
import numpy as np
import soundfile as sf

from timing import PHRASES, TEMPO, VOICE, seq_bounds

SR = 48000
bounds, TOTAL = seq_bounds()
N = int(TOTAL * SR) + SR
T = np.arange(N) / SR
rng = np.random.default_rng(31)


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

# mystery bed: music-box-like minor arpeggio (first part) -> low pulse (after the copy)
notes = [220.0, 261.6, 329.6, 261.6, 207.7, 261.6, 311.1, 261.6]
step = 0.36
for k in range(int(bounds[5][0] / step)):
    f = notes[k % len(notes)]
    e, t = dec(0.6, 6)
    add(music, (np.sin(2 * np.pi * f * 2 * t) + 0.3 * np.sin(2 * np.pi * f * 4 * t)) * e, k * step, 0.12)
bpm = np.interp(T, [0, bounds[5][0], bounds[8][0], TOTAL], [90, 100, 125, 140])
ph = np.cumsum(bpm / 60) / SR
beat = np.exp(-((ph % 1.0) * 22)) + 0.6 * np.exp(-(((ph - 0.22) % 1.0) * 22))
pulse_on = np.clip((T - bounds[5][0]) * 2, 0, 1)
music += 0.5 * beat * np.sin(2 * np.pi * 46 * T) * pulse_on
music += 0.22 * np.sin(2 * np.pi * 41.2 * T)
mask = np.ones(N)
mask[(T >= bounds[6][0]) & (T < bounds[6][1])] = 0
mask[(T >= at("Es ist nicht Marco.") + 0.9) & (T < at("Es bist du."))] = 0.05  # breath before the reveal
music *= lp(mask, 900)

# lotto jingle pops as the numbers tick
e, t = dec(0.18, 25)
pop = np.sin(2 * np.pi * 880 * t) * e
for k in range(6):
    add(sfx, pop, 0.3 + k * 0.6, 0.25)
add(sfx, np.sin(2 * np.pi * 1320 * t) * e, 3.9, 0.3)

# phone ring tone (call scenes)
rn = int(0.8 * SR)
rt = np.arange(rn) / SR
ring = np.sin(2 * np.pi * 1000 * rt) * (np.sin(2 * np.pi * 20 * rt) > 0) * np.hanning(rn)
add(sfx, ring, bounds[1][0] + 0.2, 0.08)
add(sfx, ring, at("Du rufst Marco"), 0.08)

# three knocks
e, t = dec(0.15, 35)
knock = lp(rng.standard_normal(len(e)), 20) * e + np.sin(2 * np.pi * 120 * t) * e
for k in range(3):
    add(sfx, knock, at("Nachts klopft") + 0.15 + k * 0.28, 0.8)

# rain + drips in the shoes scene
rm = np.zeros(N)
rm[int(bounds[4][0] * SR):int(bounds[4][1] * SR)] = 1
sfx += 0.05 * (lp(rng.standard_normal(N), 5) - lp(rng.standard_normal(N), 60)) * lp(rm, 3000)
e, t = dec(0.08, 50)
drip = np.sin(2 * np.pi * (1800 - 6000 * t) * t) * e
for k in range(8):
    add(sfx, drip, bounds[4][0] + 0.3 + k * 0.55, 0.2)

# scanner beep + error buzz on "Kopie"
e, t = dec(0.12, 20)
add(sfx, np.sin(2 * np.pi * 1600 * t) * e, at("Die Frau prüft") + 0.6, 0.3)
bn = int(0.6 * SR)
buzz = np.sign(np.sin(2 * np.pi * 110 * np.arange(bn) / SR)) * np.hanning(bn)
add(sfx, lp(buzz, 4), at("Das ist eine Kopie"), 0.12)

# tape stop + hiss for PAUSE
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[6][0] - 0.1, 0.35)

# CCTV hum in the monitor scenes
cm = np.zeros(N)
cm[int(bounds[7][0] * SR):int(bounds[9][1] * SR)] = 1
sfx += 0.03 * np.sign(np.sin(2 * np.pi * 60 * T)) * lp(cm, 2000)

# impacts
e, t = dec(1.6, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k in ("Gratuliere.", "Das ist eine Kopie.", "Es bist du."):
    add(sfx, boom, at(k), 0.7)

# riser into the reveal
ra, rb = at("Er dreht sich um"), at("Es bist du.")
rn = int((rb - ra) * SR)
rt = np.arange(rn) / SR
add(sfx, np.sin(2 * np.pi * np.cumsum(200 + 900 * (rt / rt[-1]) ** 2) / SR) * (rt / rt[-1]) ** 2, ra, 0.1)

bed = music * 0.2 + sfx

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
