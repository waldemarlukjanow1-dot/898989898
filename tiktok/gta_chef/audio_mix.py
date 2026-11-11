"""Sound design for 'Schick das deinem Chef' (numpy only) + tightened voice -> build/mix.wav."""
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

# ---- light, cheeky retro-synth groove (own synthesis)
bpm = 104
ph = np.cumsum(np.full(N, bpm / 60)) / SR
kick = np.exp(-((ph % 1.0) * 16)) * np.sin(2 * np.pi * 55 * T)
snap = lp(rng.standard_normal(N), 3) * np.exp(-(((ph + 0.5) % 1.0) * 26))
notes = np.array([261.6, 329.6, 392.0, 329.6, 293.7, 349.2, 440.0, 349.2])
step = ((ph * 2) // 1).astype(int) % 8
arp = np.sin(2 * np.pi * np.cumsum(notes[step]) / SR) * np.exp(-(((ph * 2) % 1.0) * 5))
bass = np.sin(2 * np.pi * np.cumsum(np.where((ph // 4) % 2 == 0, 65.4, 73.4)) / SR)
music += 0.7 * kick + 0.12 * snap + 0.18 * arp + 0.25 * bass
mask = np.ones(N)
mask[(T >= bounds[4][0]) & (T < bounds[4][1])] = 0.0
music *= lp(mask, 1200)

# ---- sfx
e, t = dec(1.4, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
add(sfx, boom, 0.05, 0.8)                                   # logo hit at the start
add(sfx, boom, at("Am neun"), 0.6)
add(sfx, boom, bounds[7][0] + 0.1, 0.5)                     # final question
e, t = dec(0.15, 25)
ping = np.sin(2 * np.pi * 1400 * t) * e
add(sfx, ping, 1.3, 0.3)                                    # message arrives
add(sfx, ping, at("Er schaut"), 0.3)
add(sfx, ping, at("Er schaut") + 0.5, 0.25)
e, t = dec(0.08, 40)
tick = np.sin(2 * np.pi * 2400 * t) * e
for k in range(13):
    add(sfx, tick, at("Dreizehn") + k * 0.12, 0.15)          # years counting
e, t = dec(0.25, 18)
thump = lp(rng.standard_normal(len(e)), 30) * e * 3
for k_ in ("Den Release", "Ausgeschlafen", "Glücklich", "Motivierter"):
    add(sfx, thump, at(k_) + 0.05, 0.6)                     # stamps
e, t = dec(0.04, 90)
click = lp(rng.standard_normal(len(e)), 2) * e
for k in range(14):
    add(sfx, click, at("Er tippt") + k * 0.09 + (k % 3) * 0.01, 0.25)   # typing
e, t = dec(0.6, 5)
ding = (np.sin(2 * np.pi * 1318 * t) + np.sin(2 * np.pi * 1760 * t)) * e
add(sfx, ding, at("Er sitzt") + 1.0, 0.2)                   # thought bubble
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[4][0] - 0.1, 0.3)   # record stop
e, t = dec(0.12, 30)
pen = lp(rng.standard_normal(len(e)), 4) * e
for k_ in ("Einen Tag", "Dafür", "Jeden Tag", "Ohne zu"):
    add(sfx, pen, at(k_) + 0.3, 0.5)                          # tick marks

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
