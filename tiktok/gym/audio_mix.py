"""Sound design for 'Gym – ab heute' (numpy only) + tightened voice -> build/mix.wav."""
import subprocess
import numpy as np
import soundfile as sf

from timing import PHRASES, TEMPO, VOICE, seq_bounds, tight_layout

SR = 48000
bounds, TOTAL = seq_bounds()
N = int(TOTAL * SR) + SR
T = np.arange(N) / SR
rng = np.random.default_rng(51)


def at(text, last=False):
    hits = [a / TEMPO for a, b, s, t in PHRASES if t.startswith(text)]
    return hits[-1] if last else hits[0]


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

# ---- driving workout beat that grows with the hero (own synthesis)
bpm = 120
ph = np.cumsum(np.full(N, bpm / 60)) / SR
grow = np.clip(T / TOTAL, 0, 1)
kick = np.exp(-((ph % 1.0) * 14)) * np.sin(2 * np.pi * 52 * T)
clap = lp(rng.standard_normal(N), 3) * np.exp(-(((ph + 0.5) % 2.0) * 22))
hat = rng.standard_normal(N) * np.exp(-(((ph * 2) % 1.0) * 60))
roots = np.array([55.0, 55.0, 65.4, 49.0])
bar_ = ((ph // 4) % 4).astype(int)
bass = np.sign(np.sin(2 * np.pi * np.cumsum(roots[bar_]) / SR)) * np.exp(-(((ph * 2) % 1.0) * 4))
lead = np.sin(2 * np.pi * np.cumsum(roots[bar_] * 4) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * T * 0.25))
music += 0.8 * kick + (0.1 + 0.15 * grow) * clap + 0.05 * hat * (T > bounds[1][0]) + 0.18 * lp(bass, 6) \
    + 0.1 * lead * grow
mask = np.ones(N)
mask[(T >= bounds[6][0]) & (T < at("Heute.", last=True))] = 0.0
music *= lp(mask, 1200)

# ---- sfx
e, t = dec(1.4, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
add(sfx, boom, 0.03, 0.9)                                    # shock frame
add(sfx, boom, at("Heute."), 0.6)
add(sfx, boom, at("Heute.", last=True), 0.9)
e, t = dec(0.25, 18)
thump = lp(rng.standard_normal(len(e)), 30) * e * 3
for k_ in ("Kein Montag", "Kein Neujahr", "Muskelkater", "Und erkennst"):
    add(sfx, thump, at(k_) + 0.05, 0.5)
e, t = dec(0.35, 14)
clonk = (np.sin(2 * np.pi * 180 * t) + 0.6 * np.sin(2 * np.pi * 530 * t) + 0.3 * lp(rng.standard_normal(len(t)), 2)) * e
for k in range(5):
    add(sfx, clonk, at("Tipp eins") + 0.6 + k * 1.0, 0.25)  # barbell
for k in range(4):
    add(sfx, clonk, at("Tipp zwei") + 0.5 + k * 0.8, 0.2)    # dumbbells
e, t = dec(0.6, 5)
ding = (np.sin(2 * np.pi * 1318 * t) + np.sin(2 * np.pi * 1760 * t)) * e
for k_ in ("Du bist da", "Tipp eins", "Tipp zwei", "Tipp drei", "Trainierst"):
    add(sfx, ding, at(k_), 0.18)
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[6][0] - 0.1, 0.3)   # record stop
e, t = dec(0.04, 90)
click = lp(rng.standard_normal(len(e)), 2) * e
for k in range(5):
    add(sfx, click, at("Schreib") + k * 0.15, 0.3)          # typing the comment

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
