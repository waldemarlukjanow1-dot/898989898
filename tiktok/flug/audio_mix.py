"""Sound design for 'Flug 404' (numpy only) + tightened voice -> build/mix.wav."""
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

# ---- cabin hum all the time (engines), music only drone + heartbeat, silence at key beats
cabin = lp(rng.standard_normal(N), 90) * 1.5 + 0.3 * np.sin(2 * np.pi * 110 * T)
sfx += 0.05 * cabin
bpm = np.interp(T, [0, bounds[1][0], bounds[4][0], bounds[7][0], TOTAL], [0.01, 70, 95, 120, 130])
ph = np.cumsum(bpm / 60) / SR
beat = np.exp(-((ph % 1.0) * 22)) + 0.6 * np.exp(-(((ph - 0.22) % 1.0) * 22))
music += 0.55 * beat * np.sin(2 * np.pi * 45 * T) * np.clip((T - bounds[1][0]) / 2, 0, 1)
music += 0.18 * np.sin(2 * np.pi * 38 * T) * np.clip((T - bounds[1][0]) / 3, 0, 1)
mask = np.ones(N)
mask[(T >= bounds[5][0]) & (T < bounds[5][1])] = 0
mask[(T >= at("Alle Passagiere haben")) & (T < at("Weckst du"))] = 0.0
music *= lp(mask, 1200)
# happy boarding chime at start
e, t = dec(0.8, 3)
add(sfx, (np.sin(2 * np.pi * 660 * t) + np.sin(2 * np.pi * 880 * t * 1.0)) * e * 0.5, 0.2, 0.3)
add(sfx, np.sin(2 * np.pi * 523 * t) * e * 0.5, 0.75, 0.3)

# ---- sfx
e, t = dec(0.06, 70)
click = (rng.standard_normal(len(e)) * 0.5 + np.sin(2 * np.pi * 2200 * t)) * e
add(sfx, click, at("Du drückst") + 0.6, 0.6)                                     # call button
e, t = dec(0.6, 4)
add(sfx, np.sin(2 * np.pi * 740 * t) * e, at("Du drückst") + 0.65, 0.3)          # call chime (no answer)
e, t = dec(0.15, 30)
add(sfx, np.sin(2 * np.pi * 1300 * t) * e, at("vor drei Tagen"), 0.3)          # screen ping
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[5][0] - 0.1, 0.3)
e, t = dec(0.12, 40)
step = lp(rng.standard_normal(len(e)), 12) * e
for k in range(int((at("Die Tür ist offen") - at("Du gehst")) / 0.45)):
    add(sfx, step, at("Du gehst") + k * 0.45, 0.35)                              # footsteps
dn = int(1.0 * SR)
dt_ = np.arange(dn) / SR
add(sfx, lp(rng.standard_normal(dn), 30) * np.hanning(dn), at("Die Tür ist offen"), 0.25)   # door slide
for k in range(4):
    add(sfx, np.sin(2 * np.pi * 1600 * t) * e[: len(t)] if False else click, at("Der Autopilot") + k * 0.4, 0.15)  # cockpit beeps
kn = int(0.25 * SR)
add(sfx, rng.standard_normal(kn) * np.exp(-np.arange(kn) / SR * 20), at("Dann knackt"), 0.5)   # speaker crackle
e, t = dec(1.6, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k_ in ("Alle Passagiere schlafen", "vor drei Tagen", "Beide Sitze", "Sie sind der einzige", "Alle Passagiere haben"):
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
