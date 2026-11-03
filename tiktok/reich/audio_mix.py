"""Sound design for 'Reich in 30 Tagen' (numpy only) + tightened voice -> build/mix.wav."""
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

# ---- light hip-hop style beat (kick, clap, hihat, bass), drops out at the PAUSE and the lock
bpm = 92
beat = 60 / bpm
e, t = dec(0.35, 14)
kick = np.sin(2 * np.pi * (50 + 80 * np.exp(-t * 30)) * t) * e
e, t = dec(0.18, 25)
clap = lp(rng.standard_normal(len(e)), 3) * e
e, t = dec(0.05, 80)
hat = (rng.standard_normal(len(e)) - lp(rng.standard_normal(len(e)), 6)) * e
bassnotes = [55.0, 55.0, 65.4, 49.0]
k = 0
tb = 0.0
while tb < TOTAL:
    add(music, kick, tb, 0.9)
    add(music, hat, tb + beat / 2, 0.25)
    if k % 2 == 1:
        add(music, clap, tb, 0.5)
    f = bassnotes[(k // 4) % 4]
    e2, t2 = dec(beat * 0.9, 3)
    add(music, np.sin(2 * np.pi * f * t2) * e2, tb, 0.5)
    tb += beat
    k += 1
mask = np.ones(N)
mask[(T >= bounds[4][0]) & (T < bounds[4][1])] = 0
mask[T >= at("Gesperrt.")] = 0.0
music *= lp(mask, 1500)
# sad pad at the end
sad = (np.sin(2 * np.pi * 220 * T) + np.sin(2 * np.pi * 261.6 * T) + np.sin(2 * np.pi * 329.6 * T)) / 3
sad_env = np.clip((T - at("Gesperrt.")) / 1.5, 0, 1) * (T < TOTAL - 0.2)
music += 0.25 * sad * sad_env

# ---- sfx
e, t = dec(0.5, 6)
cash = (np.sin(2 * np.pi * 1318 * t) + np.sin(2 * np.pi * 1760 * t)) * e  # cha-ching
fall_n = int(1.0 * SR)
ft = np.arange(fall_n) / SR
whoop_down = np.sin(2 * np.pi * np.cumsum(900 * np.exp(-ft * 2.5) + 80) / SR) * np.hanning(fall_n)
add(sfx, whoop_down, at("Zwei Tage später") + 0.2, 0.25)              # crypto crash
e, t = dec(0.3, 15)
thud = np.sin(2 * np.pi * 90 * t) * e
for j in range(10):
    add(sfx, thud, bounds[2][0] + 0.15 + j * 0.25, 0.4)              # boxes
e, t = dec(0.12, 30)
stamp = lp(rng.standard_normal(len(e)), 4) * e
for j in range(6):
    add(sfx, stamp, at("Hundert Rücksendungen") + j * 0.12, 0.5)
add(sfx, whoop_down * 0.6, at("Dein letztes Geld.") + 0.3, 0.2)        # money gone
for j in range(5):
    add(sfx, cash, at("Tausend Käufer") + j * 0.6, 0.25)                # rich
e, t = dec(0.15, 25)
ding = np.sin(2 * np.pi * 1500 * t) * e
for j in range(8):
    add(sfx, ding * 0.5, at("Mit einem Passwort") + 0.2 + j * 0.12, 0.2)  # typing
bn = int(0.35 * SR)
buzz = np.sign(np.sin(2 * np.pi * 120 * np.arange(bn) / SR)) * np.hanning(bn)
for k_ in ("Passwort falsch.", "Noch zwei", "Noch einer."):
    add(sfx, lp(buzz, 4), at(k_), 0.15)
e, t = dec(1.6, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
add(sfx, boom, at("Gesperrt."), 0.8)
e, t = dec(0.2, 20)
clunk = lp(rng.standard_normal(len(e)), 12) * e + np.sin(2 * np.pi * 180 * t) * e
add(sfx, clunk, at("Gesperrt.") + 0.05, 0.6)
# tape stop into PAUSE
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[4][0] - 0.1, 0.3)

bed = music * 0.16 + sfx
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
