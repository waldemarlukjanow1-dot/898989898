"""Sound design for '11 Millionen in der Wand' (numpy only) + tightened voice -> build/mix.wav."""
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

# ---- dark suspense bed (own synthesis): sub-bass pulse, heartbeat, high drone, slowly rising
grow = np.clip(T / TOTAL, 0, 1)
bpm = 92
ph = np.cumsum(np.full(N, bpm / 60)) / SR
sub = np.sin(2 * np.pi * 41.2 * T) * (0.55 + 0.45 * np.exp(-((ph % 1.0) * 5)))
heart = np.exp(-((ph % 1.0) * 22)) * np.sin(2 * np.pi * 60 * T) + 0.7 * np.exp(-(((ph - 0.22) % 1.0) * 22)) * np.sin(2 * np.pi * 55 * T)
drone = (np.sin(2 * np.pi * 659 * T) + 0.6 * np.sin(2 * np.pi * 698.5 * T)) * (0.3 + 0.7 * grow)
pulse = np.sin(2 * np.pi * 110 * T) * np.exp(-(((ph * 2) % 1.0) * 8)) * grow
music += 0.5 * sub + 0.6 * heart * (T > bounds[2][0]) + 0.05 * drone + 0.15 * pulse
mask = np.ones(N)
mask[(T >= bounds[4][0]) & (T < at("Jetzt"))] = 0.0                     # freeze: silence
mask[(T >= at("Der Täter")) & (T < bounds[6][0])] = 0.6
music *= lp(mask, 1200)

# ---- sfx
e, t = dec(1.4, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
add(sfx, boom, 0.03, 0.9)                                    # wall bursts
add(sfx, boom, at("morgen"), 0.7)
add(sfx, boom, at("dein Vormieter"), 0.8)
add(sfx, boom, at("Den Schlüssel"), 0.8)
e, t = dec(0.5, 6)
rustle = lp(rng.standard_normal(len(e)), 3) * e
for k in range(4):
    add(sfx, rustle, 0.1 + k * 0.15, 0.25)                    # money flying
e, t = dec(0.12, 30)
knock = lp(rng.standard_normal(len(e)), 20) * e * 3 + np.sin(2 * np.pi * 140 * t) * e
for k in range(3):
    add(sfx, knock, at("Die Wand") + 0.2 + k * 0.3, 0.6)      # hollow knocking
dn = int(1.0 * SR)
drill = (np.sign(np.sin(2 * np.pi * 180 * np.arange(dn) / SR)) * 0.3 + lp(rng.standard_normal(dn), 2) * 0.3) * np.hanning(dn)
add(sfx, drill, at("Du bohrst"), 0.25)
add(sfx, rustle, at("Und plötzlich") + 0.6, 0.3)             # bill falls out
rn = int(0.7 * SR)
rip = lp(rng.standard_normal(rn), 2) * np.linspace(1, 0.2, rn) * np.hanning(rn)
add(sfx, rip, at("Du reißt") + 0.3, 0.35)                    # wallpaper rips
e, t = dec(0.08, 40)
tick = np.sin(2 * np.pi * 2400 * t) * e
for k in range(16):
    add(sfx, tick, at("Du zählst") + k * 0.15, 0.12)          # counting
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[4][0] - 0.1, 0.3)   # record stop
e, t = dec(0.04, 90)
click = lp(rng.standard_normal(len(e)), 2) * e
for k in range(10):
    add(sfx, click, at("Du suchst") + k * 0.09, 0.3)          # typing
wn = int(0.8 * SR)
whoosh = lp(rng.standard_normal(wn), 6) * np.hanning(wn)
add(sfx, whoosh, at("Der Täter") - 0.3, 0.4)                  # into the flashback
e, t = dec(1.2, 2.5)
ding = np.sin(2 * np.pi * 659 * t) * e
dong = np.sin(2 * np.pi * 523 * t) * e
for k in range(2):                                           # doorbell, twice
    add(sfx, ding, at("Dann klingelt") + 0.2 + k * 1.1, 0.35)
    add(sfx, dong, at("Dann klingelt") + 0.6 + k * 1.1, 0.35)

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
