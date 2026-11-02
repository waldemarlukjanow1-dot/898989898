"""Sound design for 'Der Zeuge' (numpy only) + voice mix -> build/mix.wav."""
import subprocess
import numpy as np
import soundfile as sf

from timing import PHRASES, TEMPO, VOICE, seq_bounds

SR = 48000
bounds, TOTAL = seq_bounds()
N = int(TOTAL * SR) + SR
T = np.arange(N) / SR
rng = np.random.default_rng(11)


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


music = np.zeros(N)
sfx = np.zeros(N)

# interrogation room tone: mains hum + fluorescent buzz
room = 0.05 * np.sin(2 * np.pi * 50 * T) + 0.02 * np.sign(np.sin(2 * np.pi * 100 * T))
# sub drone with slow beating
music += 0.28 * np.sin(2 * np.pi * 38 * T) + 0.18 * np.sin(2 * np.pi * 38.6 * T)
music += 0.05 * lp(np.sign(np.sin(2 * np.pi * 98 * T)) + np.sign(np.sin(2 * np.pi * 103.8 * T)), 120)

# heartbeat following the PULS value (92 -> 170)
bpm = np.interp(T, [0, at("Er schaut"), at("Dann siehst"), at("Das Licht"), TOTAL], [80, 110, 140, 170, 170])
ph = np.cumsum(bpm / 60) / SR
beat = np.exp(-((ph % 1.0) * 22)) + 0.6 * np.exp(-(((ph - 0.22) % 1.0) * 22))
music += 0.55 * beat * np.sin(2 * np.pi * 44 * T)

# flashbacks: room tone off, music filtered/warbly
fb = np.zeros(N)
for i in (2, 5):
    fb[int(bounds[i][0] * SR):int(bounds[i][1] * SR)] = 1
fb = lp(fb, 2000)
room *= 1 - fb
warble = np.sin(2 * np.pi * 70 * T + 3 * np.sin(2 * np.pi * 0.7 * T))
music += 0.12 * warble * fb

# total silence in PAUSE and a short dead-air moment before "Er lächelt."
mask = np.ones(N)
mask[(T >= bounds[6][0]) & (T < bounds[6][1])] = 0
mask[(T >= at("Grauer Mantel")) & (T < at("Er lächelt"))] = 0.15
mask = lp(mask, 1200)
music *= mask
room *= mask

# gunshots: cold open + flashback
e, t = dec(1.2, 6)
shot = (rng.standard_normal(len(e)) * np.exp(-t * 40) * 1.2 + np.sin(2 * np.pi * 70 * t) * e) * 0.9
shot += lp(rng.standard_normal(len(e)), 30) * np.exp(-t * 2.5) * 0.5  # garage echo tail
add(sfx, shot, 0.0, 0.9)
add(sfx, shot, at("Ein Schuss."), 0.9)

# flashback enter: reverse whoosh + tape rewind chirps
wn = int(0.9 * SR)
rev = lp(rng.standard_normal(wn), 9) * np.linspace(0, 1, wn) ** 3
for i in (2, 5):
    add(sfx, rev, bounds[i][0] - 0.9, 0.45)

# pen stops (click) on the gloves question
e, t = dec(0.06, 70)
click = (rng.standard_normal(len(e)) * 0.5 + np.sin(2 * np.pi * 2600 * t)) * e
add(sfx, click, at("Und er trug"), 0.5)

# low hit on "Du lügst." / "Ein Knopf" / "Ein Geständnis."
e, t = dec(1.6, 3)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k in ("Du lügst.", "Ein Knopf", "Ein Geständnis.", "Er lächelt."):
    add(sfx, boom, at(k), 0.65)

# tape stop into PAUSE + hiss
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[6][0] - 0.1, 0.35)
add(sfx, rng.standard_normal(int((bounds[6][1] - bounds[6][0]) * SR)) * 0.02, bounds[6][0])

# earpiece: faint garbled voice (band-passed noise bursts)
a7 = at("Ein Knopf")
for k in range(10):
    n = int(rng.uniform(0.08, 0.2) * SR)
    burst = lp(rng.standard_normal(n), 3) - lp(rng.standard_normal(n), 12)
    add(sfx, burst * np.hanning(n), a7 + 0.3 + k * 0.33, 0.12)

# breath on the mirror (swelling filtered noise, twice)
bn = int(1.6 * SR)
breath = lp(rng.standard_normal(bn), 25) * np.sin(np.linspace(0, np.pi, bn)) ** 2
add(sfx, breath, at("Jemand atmet") - 0.3, 0.6)
add(sfx, breath, at("Jemand atmet") + 1.4, 0.45)

# paper slide
pn = int(0.8 * SR)
add(sfx, lp(rng.standard_normal(pn), 4) * np.hanning(pn), at("Der Kommissar schiebt") + 0.6, 0.12)

# light flicker buzz in the finale
a10 = bounds[10][0]
fl = np.zeros(N)
for k in range(14):
    t0 = a10 + 0.6 + k * 0.12 + rng.uniform(0, 0.05)
    fl[int(t0 * SR):int((t0 + 0.05) * SR)] = 1
sfx += 0.08 * np.sign(np.sin(2 * np.pi * 120 * T)) * lp(fl, 50)

# riser into the question, hard stop at the end
ra = at("Er lächelt")
rn = int((TOTAL - 0.4 - ra) * SR)
rt = np.arange(rn) / SR
riser = np.sin(2 * np.pi * np.cumsum(200 + 900 * (rt / rt[-1]) ** 2) / SR) * (rt / rt[-1]) ** 2
add(sfx, riser, ra, 0.08)

bed = music * 0.2 + room + sfx

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-filter:a", f"atempo={TEMPO}",
                "-ar", str(SR), "-ac", "1", "build/voice_fast.wav"], check=True)
voice, _ = sf.read("build/voice_fast.wav")
v = np.zeros(N)
v[: min(N, len(voice))] = voice[:N]
venv = lp(np.abs(v), 2400)
duck = 1.0 - 0.45 * np.clip(venv / (venv.max() * 0.25 + 1e-9), 0, 1)
mix = (v + bed * duck)[: int(TOTAL * SR)]
end = int((TOTAL - 0.4) * SR)
mix[end:] *= 0.0  # hard cut to silence = cliffhanger
mix /= np.abs(mix).max() / 0.95
sf.write("build/mix.wav", np.stack([mix, mix], 1), SR)
print("mix", round(TOTAL, 2))
