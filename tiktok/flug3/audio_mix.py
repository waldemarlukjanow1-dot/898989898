"""Sound design for 'Flug 404 Teil 3' (numpy only) + tightened voice -> build/mix.wav."""
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

# ---- engine roar + alarm until the plane is level, then calm; dreamy pad at the landing
cabin = lp(rng.standard_normal(N), 70) * 1.6 + 0.3 * np.sin(2 * np.pi * 110 * T)
roar = np.interp(T, [0, at("Die Nase"), at("Der Höhenmesser"), at("Du landest"), at("Alles fühlt"), TOTAL], [1.6, 1.6, 0.6, 0.8, 0.15, 0.15])
sfx += 0.06 * cabin * roar
bpm = np.interp(T, [0, at("Der Höhenmesser"), at("Durchs Fenster"), at("Die Kabine"), TOTAL], [150, 150, 95, 110, 120])
ph = np.cumsum(bpm / 60) / SR
beat = np.exp(-((ph % 1.0) * 22)) + 0.6 * np.exp(-(((ph - 0.22) % 1.0) * 22))
music += 0.6 * beat * np.sin(2 * np.pi * 45 * T)
music += 0.16 * np.sin(2 * np.pi * 38 * T)
mask = np.ones(N)
mask[(T >= bounds[5][0]) & (T < bounds[5][1])] = 0
mask[(T >= at("Alles fühlt")) & (T < at("Du drehst"))] = 0.1
music *= lp(mask, 1200)
dream = np.zeros(N)
dream[int(at("Alles fühlt") * SR):int(at("Du drehst") * SR)] = 1
music += 0.12 * (np.sin(2 * np.pi * 523 * T) + np.sin(2 * np.pi * 659 * T) + np.sin(2 * np.pi * 784 * T)) / 3 * lp(dream, 8000) / 0.2

# ---- sfx
an = int((at("Die Nase") - 0.0) * SR)
at_ = np.arange(an) / SR
add(sfx, np.sign(np.sin(2 * np.pi * 760 * at_)) * ((at_ * 2.5) % 1 < 0.5) * 0.3, 0.0, 0.07)           # cockpit alarm
e, t = dec(0.12, 40)
step = lp(rng.standard_normal(len(e)), 12) * e
for k in range(int((at("Die Cockpittür") - at("Du rennst")) / 0.28)):
    add(sfx, step, at("Du rennst") + k * 0.28, 0.4)                                                   # running
e, t = dec(0.5, 10)
slam = lp(rng.standard_normal(len(e)), 20) * e * 2 + np.sin(2 * np.pi * 70 * t) * e
add(sfx, slam, at("Die Cockpittür") + 0.4, 0.9)                                                    # door slam
pu = np.zeros(1)
e, t = dec(0.35, 6)
gpws = np.sign(np.sin(2 * np.pi * 440 * t)) * e
for k_ in ("Pull up.",):
    pass
cr = int(2.2 * SR)
crt = np.arange(cr) / SR
creak = lp(rng.standard_normal(cr), 40) * np.sin(np.pi * crt / crt[-1])
add(sfx, creak, at("Und ziehst"), 0.35)                                                            # yoke strain
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[5][0] - 0.1, 0.3)
e, t = dec(0.6, 6)
thump = lp(rng.standard_normal(len(e)), 10) * e * 2 + np.sin(2 * np.pi * 60 * t) * e
add(sfx, thump, at("Du landest") + 0.3, 1.0)                                                      # touchdown
sq = int(1.2 * SR)
sqt = np.arange(sq) / SR
add(sfx, np.sin(2 * np.pi * (1800 - 400 * sqt) * sqt) * np.hanning(sq), at("Die Reifen"), 0.15)   # tyre screech
e, t = dec(0.08, 50)
clap = lp(rng.standard_normal(len(e)), 3) * e
for k in range(8):
    add(sfx, clap, at("Und er klatscht") + 0.3 + k * 0.33, 0.5)                                   # clapping
e, t = dec(1.6, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k_ in ("Noch neunzig", "Ein Alarm", "Der Höhenmesser", "Die Kabine", "Du."):
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
