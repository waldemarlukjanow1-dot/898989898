"""Synthesises a tension bed + sound effects and mixes them under the voice.

Output: build/mix.wav (48 kHz stereo). Everything is generated with numpy, so
there are no third-party music licences to worry about.
"""
import os
import subprocess
import numpy as np
import soundfile as sf

from timing import PHRASES, TEMPO, VOICE, seq_bounds

SR = 48000
os.makedirs("build", exist_ok=True)

bounds, TOTAL = seq_bounds()
N = int(TOTAL * SR) + SR
rng = np.random.default_rng(1)
t_all = np.arange(N) / SR


def env(n, attack=0.005, release=0.2):
    e = np.ones(n)
    a = max(1, int(attack * SR))
    r = max(1, int(release * SR))
    e[:a] = np.linspace(0, 1, a)
    e[-r:] *= np.exp(-np.linspace(0, 6, r))
    return e


def add(buf, sig, at, gain=1.0):
    i = int(at * SR)
    if i >= len(buf):
        return
    sig = sig[: len(buf) - i]
    buf[i:i + len(sig)] += sig * gain


def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


music = np.zeros(N)
sfx = np.zeros(N)

# ---- drone bed (stops during the PAUSE sequence, returns harder after)
pause_a, pause_b = bounds[7]
for f, g in ((55.0, 0.22), (82.41, 0.12), (110.0, 0.06)):
    music += g * np.sin(2 * np.pi * f * t_all) * (0.75 + 0.25 * np.sin(2 * np.pi * 0.25 * t_all))
pulse_rate = np.where(t_all < bounds[9][0], 2.0, 4.0)  # heartbeat speeds up at the alarm
phase = np.cumsum(pulse_rate) / SR
kick = np.exp(-((phase % 1.0) * 18)) * np.sin(2 * np.pi * 48 * t_all)
music += 0.35 * kick
mask = np.ones(N)
mask[(t_all >= pause_a) & (t_all < pause_b)] = 0.0
music *= lowpass(mask, 2000)

# ---- clock ticks during the countdown part (seq 0..6)
tick = np.sin(2 * np.pi * 3200 * np.arange(int(0.02 * SR)) / SR) * env(int(0.02 * SR), 0.001, 0.015)
t = 0.0
while t < bounds[6][1]:
    add(sfx, tick, t, 0.10 if int(t * 2) % 2 == 0 else 0.06)
    t += 0.5

# ---- rain (scenes 0, 10, 11)
noise = lowpass(rng.standard_normal(N), 6) - lowpass(rng.standard_normal(N), 60)
rain_mask = np.zeros(N)
for i in (0, 10, 11):
    a, b = bounds[i]
    rain_mask[int(a * SR):int(b * SR)] = 1
sfx += 0.05 * noise * lowpass(rain_mask, 4000)

# ---- impacts on story beats
boom_n = int(1.4 * SR)
bt = np.arange(boom_n) / SR
boom = np.sin(2 * np.pi * (60 * np.exp(-bt * 2)) * bt * 2) * np.exp(-bt * 3.5)
for i in (0, 4, 6, 9):
    add(sfx, boom, bounds[i][0] + 0.05, 0.55)

# ---- whoosh on every cut
wn = int(0.35 * SR)
whoosh = lowpass(rng.standard_normal(wn), 12) * np.sin(np.linspace(0, np.pi, wn)) ** 2
for a, _ in bounds[1:]:
    add(sfx, whoosh, a - 0.2, 0.18)

# ---- vault clicks (on the three spoken "Klick.")
cn = int(0.06 * SR)
click = (rng.standard_normal(cn) * 0.6 + np.sin(2 * np.pi * 1800 * np.arange(cn) / SR)) * env(cn, 0.0005, 0.05)
for a, b, seq, txt in PHRASES:
    if txt == "Klick.":
        add(sfx, click, a / TEMPO, 0.5)

# ---- cash counter rattle while BEUTE counts up
a5 = bounds[4][0]
for k in range(30):
    add(sfx, click * 0.5, a5 + 0.4 + k * 0.05, 0.25)

# ---- tape stop into PAUSE
ts_n = int(0.5 * SR)
tt = np.arange(ts_n) / SR
freq = 220 * (1 - tt / 0.5) ** 2 + 20
tape = np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - tt / 0.5)
add(sfx, tape, pause_a - 0.1, 0.35)
# VHS hiss during pause
hiss = rng.standard_normal(int((pause_b - pause_a) * SR)) * 0.025
add(sfx, hiss, pause_a, 1.0)

# ---- alarm (seq 9) and sirens (seq 11)
a9, b9 = bounds[9][0], bounds[10][1]
an = int((b9 - a9) * SR)
at = np.arange(an) / SR
alarm = np.sign(np.sin(2 * np.pi * np.where((at * 2.5) % 1 < 0.5, 880, 660) * at)) * 0.5
add(sfx, lowpass(alarm, 4) * np.minimum(1, at * 4), a9, 0.07)
a11, b11 = bounds[11]
sn = int((b11 - a11) * SR)
st_ = np.arange(sn) / SR
sf_ = 750 + 250 * np.sin(2 * np.pi * 0.6 * st_)
siren = np.sin(2 * np.pi * np.cumsum(sf_) / SR) * np.minimum(1, st_ / 1.5)
add(sfx, siren, a11, 0.07)

# ---- car pulling away (seq 10)
cn2 = int(2.5 * SR)
ct = np.arange(cn2) / SR
engine = np.sin(2 * np.pi * np.cumsum(70 + 60 * ct) / SR) * np.exp(-ct * 0.8)
add(sfx, lowpass(np.sign(engine) * 0.4, 20), bounds[10][0] + 2.2, 0.35)

bed = music * 0.18 + sfx

# ---- voice: speed up (pitch preserved) and mix with ducking
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-filter:a", f"atempo={TEMPO}",
                "-ar", str(SR), "-ac", "1", "build/voice_fast.wav"], check=True)
voice, _ = sf.read("build/voice_fast.wav")
v = np.zeros(N)
v[: min(N, len(voice))] = voice[:N]
venv = lowpass(np.abs(v), 2400)
duck = 1.0 - 0.45 * np.clip(venv / (venv.max() * 0.25 + 1e-9), 0, 1)
mix = v * 1.0 + bed * duck
mix = mix[: int(TOTAL * SR)]
fade = int(0.4 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)
mix /= max(1e-9, np.abs(mix).max()) / 0.95
stereo = np.stack([mix, mix], axis=1)
sf.write("build/mix.wav", stereo, SR)
print("mix", TOTAL, "s")
