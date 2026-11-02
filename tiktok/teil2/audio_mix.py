"""Dark sound design for Teil 2 (numpy only) + voice mix -> build/mix.wav."""
import subprocess
import numpy as np
import soundfile as sf

from timing import PHRASES, TEMPO, VOICE, seq_bounds

SR = 48000
bounds, TOTAL = seq_bounds()
N = int(TOTAL * SR) + SR
T = np.arange(N) / SR
rng = np.random.default_rng(7)


def at(text):
    """Video time where the phrase containing `text` starts."""
    for a, b, s, t in PHRASES:
        if text in t:
            return a / TEMPO
    raise KeyError(text)


def lp(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


def add(buf, sig, t0, g=1.0):
    i = int(t0 * SR)
    if 0 <= i < len(buf):
        sig = sig[: len(buf) - i]
        buf[i:i + len(sig)] += sig * g


def decay(n_sec, rate):
    n = int(n_sec * SR)
    return np.exp(-np.arange(n) / SR * rate), np.arange(n) / SR


music = np.zeros(N)
sfx = np.zeros(N)

# sub-bass drone + detuned dissonant pad
music += 0.30 * np.sin(2 * np.pi * 41.2 * T) + 0.18 * np.sin(2 * np.pi * 55 * T + 0.3 * np.sin(2 * np.pi * 0.1 * T))
pad = sum(np.sign(np.sin(2 * np.pi * f * T)) for f in (110.0, 116.5, 164.8))
music += 0.05 * lp(pad, 90)

# heartbeat (lub-dub), faster after the whisper
bpm = np.where(T < at("Sie hebt ab"), 70, 110)
ph = np.cumsum(bpm / 60) / SR
beat = np.exp(-((ph % 1.0) * 22)) + 0.6 * np.exp(-(((ph - 0.22) % 1.0) * 22))
music += 0.5 * beat * np.sin(2 * np.pi * 45 * T)

# silences: after "Zu leise" until the door, and the PAUSE sequence
mask = np.ones(N)
s1 = at("Zu leise")
mask[(T >= s1) & (T < at("Mira zieht"))] = 0.0
mask[(T >= bounds[5][0]) & (T < bounds[5][1])] = 0.0
music *= lp(mask, 1500)

# rain
rain = lp(rng.standard_normal(N), 5) - lp(rng.standard_normal(N), 70)
rmask = np.zeros(N)
for i in (0, 1, 10):
    rmask[int(bounds[i][0] * SR):int(bounds[i][1] * SR)] = 1
sfx += 0.06 * rain * lp(rmask, 3000)

# running footsteps + breathing in the hook
e, t = decay(0.12, 40)
step = lp(rng.standard_normal(len(e)), 8) * e
for k in range(int(bounds[1][1] / 0.32)):
    if k * 0.32 < s1:
        add(sfx, step, k * 0.32, 0.35)

# key + lock
e, t = decay(0.08, 60)
click = (rng.standard_normal(len(e)) * 0.5 + np.sin(2 * np.pi * 2200 * t)) * e
add(sfx, click, at("Und schließt auf") + 0.1, 0.5)
add(sfx, click, at("Und schließt auf") + 0.35, 0.6)

# phone vibration
vib_n = int(1.4 * SR)
vt = np.arange(vib_n) / SR
vib = np.sin(2 * np.pi * 160 * vt) * ((vt * 2.5) % 1 < 0.6)
add(sfx, vib, at("Dann leuchtet"), 0.25)

# tape stop into PAUSE + hiss
e, t = decay(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[5][0] - 0.1, 0.35)
add(sfx, rng.standard_normal(int((bounds[5][1] - bounds[5][0]) * SR)) * 0.02, bounds[5][0])

# impacts
e, t = decay(1.6, 3)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for key in ("Du rennst.", "dein Foto.", "Kein Geld.", "Und legt eine Polizeimarke", "Du warst der Köder."):
    add(sfx, boom, at(key), 0.6)

# paper rustle
add(sfx, lp(rng.standard_normal(int(0.9 * SR)), 3) * np.hanning(int(0.9 * SR)), at("Du reißt"), 0.12)

# reverse whoosh into flashback + glitch stutter
wn = int(0.8 * SR)
wh = lp(rng.standard_normal(wn), 10) * np.linspace(0, 1, wn) ** 3
add(sfx, wh, bounds[8][0] - 0.8, 0.4)

# distant -> loud sirens (seq 9 -> 10)
a9 = bounds[9][0]
sn = int((TOTAL - a9) * SR)
st = np.arange(sn) / SR
sfreq = 700 + 220 * np.sin(2 * np.pi * 0.55 * st)
siren = np.sin(2 * np.pi * np.cumsum(sfreq) / SR) * np.clip(st / (TOTAL - a9), 0.05, 1) ** 1.5
add(sfx, lp(siren, 6), a9, 0.10)

# whoosh on every cut
wn = int(0.3 * SR)
cutw = lp(rng.standard_normal(wn), 14) * np.sin(np.linspace(0, np.pi, wn)) ** 2
for a, _ in bounds[1:]:
    add(sfx, cutw, a - 0.15, 0.15)

bed = music * 0.2 + sfx

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-filter:a", f"atempo={TEMPO}",
                "-ar", str(SR), "-ac", "1", "build/voice_fast.wav"], check=True)
voice, _ = sf.read("build/voice_fast.wav")
v = np.zeros(N)
v[: min(N, len(voice))] = voice[:N]
venv = lp(np.abs(v), 2400)
duck = 1.0 - 0.45 * np.clip(venv / (venv.max() * 0.25 + 1e-9), 0, 1)
mix = (v + bed * duck)[: int(TOTAL * SR)]
f = int(0.15 * SR)
mix[-f:] *= np.linspace(1, 0, f)
mix /= np.abs(mix).max() / 0.95
sf.write("build/mix.wav", np.stack([mix, mix], 1), SR)
print("mix", round(TOTAL, 2))
