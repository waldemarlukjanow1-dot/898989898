"""Sound design for 'Patient Null – Teil 2' (numpy only) + tightened, sped-up voice -> build/mix.wav."""
import subprocess
import numpy as np
import soundfile as sf

from timing import PHRASES, TEMPO, VOICE, seq_bounds, tight_layout

SR = 48000
bounds, TOTAL = seq_bounds()
N = int(TOTAL * SR) + SR
T = np.arange(N) / SR
rng = np.random.default_rng(41)


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


# ---- voice: cut phrases out of the take, re-place with short gaps, then speed up
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-ar", str(SR), "-ac", "1", "build/voice_raw.wav"], check=True)
raw, _ = sf.read("build/voice_raw.wav")
lay = tight_layout()
tight = np.zeros(int((lay[-1][2] + lay[-1][1] - lay[-1][0] + 0.5) * SR))
fade = int(0.02 * SR)
for a0, b0, n in lay:
    seg_ = raw[int(a0 * SR):int(b0 * SR)].copy()
    seg_[:fade] *= np.linspace(0, 1, fade)
    seg_[-fade:] *= np.linspace(1, 0, fade)
    i = int(n * SR)
    tight[i:i + len(seg_)] += seg_
sf.write("build/voice_tight.wav", tight, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "build/voice_tight.wav", "-filter:a", f"atempo={TEMPO}",
                "build/voice_fast.wav"], check=True)

music = np.zeros(N)
sfx = np.zeros(N)

# ---- music: low drone + pulse that speeds up with the countdown
bpm = np.interp(T, [0, bounds[3][0], bounds[8][0], TOTAL], [120, 90, 120, 145])
ph = np.cumsum(bpm / 60) / SR
beat = np.exp(-((ph % 1.0) * 22)) + 0.6 * np.exp(-(((ph - 0.22) % 1.0) * 22))
music += 0.5 * beat * np.sin(2 * np.pi * 45 * T)
music += 0.2 * np.sin(2 * np.pi * 41.2 * T) + 0.06 * lp(np.sign(np.sin(2 * np.pi * 82.4 * T)), 80)
mask = np.ones(N)
mask[(T >= bounds[6][0]) & (T < bounds[6][1])] = 0
music *= lp(mask, 900)

# helicopter rotor (scenes 0-2, fading out) and searchlight hum
hm = np.zeros(N)
hm[: int(bounds[3][0] * SR)] = 1
rotor = lp(rng.standard_normal(N), 30) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 11 * T)))
sfx += 0.14 * rotor * lp(hm, 6000)

# running footsteps
e, t = dec(0.1, 45)
step = lp(rng.standard_normal(len(e)), 10) * e
for k in range(int((bounds[3][0] - bounds[0][0] - 2.5) / 0.24)):
    add(sfx, step, 2.5 + k * 0.24, 0.3)

# zombie groans in the horde
for k in range(8):
    t0 = bounds[1][0] + 1.0 + k * 0.9
    n = int(0.9 * SR)
    tt = np.arange(n) / SR
    groan = np.sin(2 * np.pi * np.cumsum(90 + 25 * np.sin(tt * 7) - 20 * tt) / SR) * np.hanning(n)
    add(sfx, lp(np.sign(groan) * 0.5 + groan, 12), t0, 0.12)

# glass crunch at the lab door, laptop click + video start beep
gn = int(0.5 * SR)
add(sfx, (rng.standard_normal(gn) - lp(rng.standard_normal(gn), 4)) * np.exp(-np.arange(gn) / SR * 8), bounds[3][0] + 2.5, 0.25)
e, t = dec(0.06, 70)
click = (rng.standard_normal(len(e)) * 0.5 + np.sin(2 * np.pi * 2200 * t) * 1.0) * e
add(sfx, click, bounds[4][0] + 0.6, 0.5)
add(sfx, click, at("Du drückst auf Play") + 0.5, 0.5)

# tape stop into PAUSE
e, t = dec(0.5, 0.1)
freq = 200 * (1 - t / 0.5) ** 2 + 20
add(sfx, np.sin(2 * np.pi * np.cumsum(freq) / SR) * (1 - t / 0.5), bounds[6][0] - 0.1, 0.35)

# warning alarm + clock ticks on the monitor
an = int((bounds[10][0] - bounds[9][0]) * SR)
at_ = np.arange(an) / SR
add(sfx, np.sin(2 * np.pi * 880 * at_) * ((at_ * 2) % 1 < 0.5) * 0.5, bounds[9][0] + 0.3, 0.08)
tick = np.sin(2 * np.pi * 3000 * np.arange(int(0.02 * SR)) / SR) * np.hanning(int(0.02 * SR))
for k in range(int((TOTAL - bounds[9][0]) / 1.0)):
    add(sfx, tick, bounds[9][0] + k * 1.0, 0.12)

# impacts
e, t = dec(1.6, 2.8)
boom = np.sin(2 * np.pi * (55 * np.exp(-t * 2)) * t * 2) * e
for k in ("Und die Zombies machen", "Von dir.", "Absichtlich.", "Ich bin das Gegenmittel.", "Zum ersten Mal", "Noch vierundzwanzig"):
    add(sfx, boom, at(k), 0.6)

bed = music * 0.2 + sfx
voice, _ = sf.read("build/voice_fast.wav")
v = np.zeros(N)
v[: min(N, len(voice))] = voice[:N]
venv = lp(np.abs(v), 2400)
duck = 1.0 - 0.45 * np.clip(venv / (venv.max() * 0.25 + 1e-9), 0, 1)
mix = (v + bed * duck)[: int(TOTAL * SR)]
f = int(0.3 * SR)
mix[-f:] *= np.linspace(1, 0, f)
mix /= np.abs(mix).max() / 0.95
sf.write("build/mix.wav", np.stack([mix, mix], 1), SR)
print("mix", round(TOTAL, 2), "voice_fast", round(len(voice) / SR, 2))
