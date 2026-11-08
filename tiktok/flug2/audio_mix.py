"""Sound design for 'Flug 404 Teil 2' (numpy only) + tightened voice -> build/mix.wav."""
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

# ---- cabin hum, slow heartbeat that speeds up; near-silence while your eyes are closed
cabin = lp(rng.standard_normal(N), 90) * 1.5 + 0.3 * np.sin(2 * np.pi * 110 * T)
quiet = np.ones(N)
quiet[(T >= at("Schließt die Augen")) & (T < at("Dann ruckelt"))] = 0.45
sfx += 0.05 * cabin * lp(quiet, 4000)
bpm = np.interp(T, [0, bounds[2][0], bounds[4][0], bounds[8][0], bounds[10][0], TOTAL], [60, 62, 85, 115, 140, 140])
ph = np.cumsum(bpm / 60) / SR
beat = np.exp(-((ph % 1.0) * 22)) + 0.6 * np.exp(-(((ph - 0.22) % 1.0) * 22))
music += 0.6 * beat * np.sin(2 * np.pi * 45 * T)
music += 0.16 * np.sin(2 * np.pi * 38 * T)
mask = np.ones(N)
mask[(T >= bounds[6][0]) & (T < bounds[6][1])] = 0
mask[(T >= at("Mit deinem")) & (T < at("Er lächelt"))] = 0.15
music *= lp(mask, 1200)

# ---- sfx
e, t = dec(0.12, 40)
step = lp(rng.standard_normal(len(e)), 12) * e
s0, s1 = at("Dann hörst"), at("Und bleiben") + 1.4
for k in range(int((s1 - s0) / 0.55)):
    add(sfx, step, s0 + k * 0.55, 0.2 + 0.4 * k / max(1, (s1 - s0) / 0.55))       # footsteps getting louder
for k in range(4):
    add(sfx, step, at("Die Schritte gehen") + k * 0.5, 0.35 - k * 0.08)          # walking away
bn = int(1.6 * SR)
bt = np.arange(bn) / SR
breath = lp(rng.standard_normal(bn), 25) * np.sin(np.pi * bt / bt[-1]) ** 2
add(sfx, breath, at("Du spürst") + 0.2, 0.5)                                     # breath at the ear
for k in range(3):
    add(sfx, breath[: int(0.9 * SR)] * 0.6, at("Langsam") + k * 1.3, 0.25)        # your slow breathing
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[6][0] - 0.1, 0.3)
jn = int(0.6 * SR)
add(sfx, lp(rng.standard_normal(jn), 6) * np.exp(-np.arange(jn) / SR * 6), at("Dann ruckelt"), 0.9)   # jolt
dn = int((TOTAL - at("Und es geht")) * SR)
dt_ = np.arange(dn) / SR
add(sfx, lp(rng.standard_normal(dn), 20) * np.clip(dt_ / 1.5, 0, 1), at("Und es geht"), 0.18)        # wind roar
an = int(3.0 * SR)
at_ = np.arange(an) / SR
add(sfx, np.sin(2 * np.pi * 900 * at_) * ((at_ * 2) % 1 < 0.5) * 0.4, at("Und es geht") + 0.3, 0.12)  # cabin alarm
e, t = dec(1.6, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k_ in ("Du sitzt", "Er schläft nicht.", "Mit deinem", "Ich übernehme", "Und es geht"):
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
