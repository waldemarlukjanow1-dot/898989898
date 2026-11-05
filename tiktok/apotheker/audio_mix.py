"""Sound design for 'Schnelle Welle' (numpy only) + tightened voice -> build/mix.wav."""
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

# ---- tense dark beat: low drone + heartbeat that gets faster, stops at the bell
bpm = np.interp(T, [0, bounds[2][0], bounds[8][0], bounds[9][0], TOTAL], [70, 95, 115, 135, 135])
ph = np.cumsum(bpm / 60) / SR
beat = np.exp(-((ph % 1.0) * 22)) + 0.6 * np.exp(-(((ph - 0.22) % 1.0) * 22))
music += 0.6 * beat * np.sin(2 * np.pi * 45 * T)
music += 0.22 * np.sin(2 * np.pi * 41.2 * T) + 0.05 * lp(np.sign(np.sin(2 * np.pi * 98 * T)) + np.sign(np.sin(2 * np.pi * 103.8 * T)), 120)
mask = np.ones(N)
mask[(T >= bounds[6][0]) & (T < bounds[6][1])] = 0
mask[(T >= at("Es klingelt.")) & (T < at("Schnelle Welle?"))] = 0.15
music *= lp(mask, 1200)

# ---- sfx
e, t = dec(0.15, 25)
add(sfx, np.sin(2 * np.pi * 1500 * t) * e, 0.3, 0.3)                         # comment notification
e, t = dec(0.5, 6)
add(sfx, (np.sin(2 * np.pi * 1318 * t) + np.sin(2 * np.pi * 1760 * t)) * e, at("Das erste Geld"), 0.15)
# night street ambience
amb = np.zeros(N)
amb[int(bounds[1][0] * SR):int(bounds[3][0] * SR)] = 1
sfx += 0.04 * lp(rng.standard_normal(N), 50) * lp(amb, 4000)
# car passing (engine swell)
cn = int(4.0 * SR)
ct = np.arange(cn) / SR
eng = lp(np.sign(np.sin(2 * np.pi * np.cumsum(45 + 10 * np.sin(ct)) / SR)), 30) * np.hanning(cn)
add(sfx, eng, bounds[2][0] + 0.5, 0.3)
# footsteps in the stairwell (night)
e, t = dec(0.12, 40)
stepn = lp(rng.standard_normal(len(e)), 14) * e
for j in range(4):
    add(sfx, stepn, at("Jedes Geräusch") + 0.2 + j * 0.45, 0.35)
# phone vibration
vn = int(2.0 * SR)
vt = np.arange(vn) / SR
add(sfx, np.sin(2 * np.pi * 160 * vt) * ((vt * 2.5) % 1 < 0.6), at("Dein Handy"), 0.3)
# tape stop into PAUSE
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[6][0] - 0.1, 0.3)
# message ping
e, t = dec(0.15, 25)
add(sfx, np.sin(2 * np.pi * 1300 * t) * e, bounds[8][0] + 0.3, 0.3)
# doorbell x3
e, t = dec(0.6, 4)
bell = (np.sin(2 * np.pi * 660 * t) + 0.6 * np.sin(2 * np.pi * 523 * t)) * e
for j in range(3):
    add(sfx, bell, at("Es klingelt.") + j * 0.55, 0.35)
# impacts
e, t = dec(1.6, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k_ in ("Sind das die Cops?", "Kein Herkunftsnachweis.", "Was hat er erzählt?", "Polizei."):
    add(sfx, boom, at(k_), 0.6)
# far siren at the end
a12 = at("Polizei.")
sn = int((TOTAL - a12) * SR)
stt = np.arange(sn) / SR
add(sfx, np.sin(2 * np.pi * np.cumsum(650 + 200 * np.sin(2 * np.pi * 0.7 * stt)) / SR) * np.clip(stt / 2, 0, 1), a12, 0.06)

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
