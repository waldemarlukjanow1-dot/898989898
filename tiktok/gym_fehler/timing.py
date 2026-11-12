"""Phrase timings for 'Gym – 5 Fehler'. Real phrase times from speech recognition;
pauses are tightened (each phrase re-placed with short gaps).
"""

TEMPO = 1.05
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.16, 0.3


# (start, end, sequence index, text) in the ORIGINAL recording (ElevenLabs take, 67.8 s)
RAW = [
    (0.00, 2.97, 0, "Stell dir vor, du trainierst seit drei Monaten."),
    (3.44, 4.80, 0, "Und nichts passiert."),
    (5.12, 5.90, 0, "Kein Muskel."),
    (6.19, 7.07, 0, "Kein Fortschritt."),
    (7.58, 8.04, 0, "Warum?"),
    (8.76, 9.71, 1, "Fehler eins:"),
    (10.12, 12.25, 1, "Du trainierst nur Brust und Arme."),
    (12.74, 13.16, 1, "Beine?"),
    (13.51, 14.00, 1, "Nie."),
    (14.41, 17.19, 1, "Du siehst aus wie eine Glühbirne auf Streichhölzern."),
    (17.82, 18.72, 2, "Fehler zwei:"),
    (19.18, 20.78, 2, "Du nimmst zu viel Gewicht."),
    (21.14, 24.58, 2, "Du schwingst, du wackelst, und dein Rücken schreit."),
    (25.30, 26.14, 3, "Fehler drei:"),
    (26.56, 28.48, 3, "Jedes Mal ein anderes Training."),
    (28.83, 29.58, 3, "Kein Plan."),
    (29.96, 32.51, 3, "Dein Körper weiß nie, worauf er sich einstellen soll."),
    (33.22, 34.09, 4, "Fehler vier:"),
    (34.50, 35.74, 4, "Du trainierst hart."),
    (36.11, 37.79, 4, "Und isst danach eine Banane."),
    (38.31, 38.91, 4, "Das war's."),
    (39.56, 40.00, 5, "Stopp."),
    (40.35, 42.07, 5, "Jetzt kommt der größte Fehler."),
    (42.29, 43.49, 5, "Den machen fast alle."),
    (44.08, 45.05, 6, "Fehler fünf:"),
    (45.51, 47.93, 6, "Nach drei Wochen siehst du keine Veränderung."),
    (48.36, 49.66, 6, "Und du hörst auf."),
    (50.06, 53.15, 6, "Genau dann, wenn dein Körper gerade anfängt."),
    (53.66, 55.34, 7, "Muskeln wachsen langsam."),
    (55.70, 56.98, 7, "Aber sie wachsen."),
    (57.42, 58.47, 7, "Wenn du bleibst."),
    (58.96, 59.38, 8, "Also:"),
    (59.80, 61.63, 8, "Welchen Fehler hast du schon gemacht?"),
    (62.04, 63.61, 8, "Schreib die Nummer in die Kommentare."),
    (64.07, 67.79, 8, "Und schick das deinem Gym-Partner, der immer nur Arme trainiert."),
]
EXTRA_GAP = {"Stopp.": 0.25, "Nie.": 0.1}

END_HOLD = 1.0


def tight_layout():
    """[(orig_a, orig_b, new_a)] in tightened-recording time (before TEMPO)."""
    out, t, prev_seq = [], 0.0, None
    for a, b, s, txt in RAW:
        a0, b0 = max(0.0, a - PAD_IN), b + PAD_OUT
        if prev_seq is not None:
            t += (GAP_SCENE if s != prev_seq else GAP_SAME) + EXTRA_GAP.get(txt, 0.0)
        out.append((a0, b0, t))
        t += b0 - a0
        prev_seq = s
    return out


_LAY = tight_layout()
# PHRASES in tightened time, same shape as earlier projects: (start, end, seq, text)
PHRASES = [(n + PAD_IN if a > 0 else n, n + (b0 - a0) - PAD_OUT, s, txt)
           for (a0, b0, n), (a, b, s, txt) in zip(_LAY, RAW)]


def _syl(w):
    import re
    return max(1, len(re.findall(r"[aeiouyäöü]+", w.lower())))


_ENV = None


def _envelope():
    global _ENV
    if _ENV is None:
        import os
        import numpy as np
        import soundfile as sf
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", "vo16.wav")
        if not os.path.exists(p):  # planned timing: flat envelope
            _ENV = (np.ones(16000 * 120, dtype="float32"), 16000)
            return _ENV
        a, sr = sf.read(p, dtype="float32")
        e = np.abs(a)
        k = int(0.03 * sr)
        e = np.convolve(e, np.ones(k) / k, mode="same")
        _ENV = (e, sr)
    return _ENV


def words():
    """Word timings (video time). Each phrase is split along its real loudness curve, weighted by syllables,
    so captions follow the voice word by word."""
    import numpy as np
    env, sr = _envelope()
    out = []
    for (a, b, seq, text), (oa, ob, _, _) in zip(PHRASES, RAW):
        ws = text.split()
        wts = np.array([_syl(w) + (0.6 if w[-1] in ".,:?!–" else 0) for w in ws], dtype=float)
        target = np.cumsum(wts) / wts.sum()
        seg_ = env[int(oa * sr):int(ob * sr)] + 1e-6
        cum = np.cumsum(seg_) / seg_.sum()
        ends = [float(np.searchsorted(cum, f)) / len(cum) for f in target]
        starts = [0.0] + ends[:-1]
        for w, s0, s1 in zip(ws, starts, ends):
            out.append(dict(w=w, a=(a + (b - a) * s0) / TEMPO, b=(a + (b - a) * s1) / TEMPO, seq=seq))
    return out


def seq_bounds():
    starts = {}
    for a, b, seq, _ in PHRASES:
        starts.setdefault(seq, a / TEMPO)
    n = max(starts) + 1
    st = [0.0] + [starts[i] - 0.12 for i in range(1, n)]
    total = PHRASES[-1][1] / TEMPO + END_HOLD
    return [(st[i], st[i + 1] if i + 1 < n else total) for i in range(n)], total
