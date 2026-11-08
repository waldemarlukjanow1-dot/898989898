"""Phrase timings for 'Flug 404 Teil 2' (ElevenLabs take, 62.5 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.03
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.32, 0.5

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 3.29, 0, "Du sitzt in einem fliegenden Flugzeug ohne Piloten."),
    (3.74, 6.91, 0, "Und 187 Passagiere starren dich an."),
    (7.53, 8.52, 1, "Du hast dich entschieden:"),
    (9.07, 10.06, 1, "Du setzt dich hin."),
    (10.55, 11.55, 1, "Schließt die Augen."),
    (12.07, 14.33, 1, "Und tust so, als würdest du schlafen."),
    (14.97, 16.31, 2, "Langsam atmen."),
    (16.80, 17.73, 2, "Nicht bewegen."),
    (18.24, 19.23, 2, "Nicht blinzeln."),
    (20.05, 21.71, 3, "Dann hörst du Schritte im Gang."),
    (22.23, 23.04, 3, "Sie kommen näher."),
    (23.62, 26.04, 3, "Und bleiben direkt neben deinem Sitz stehen."),
    (26.62, 28.22, 4, "Jemand beugt sich über dich."),
    (28.76, 30.95, 4, "Du spürst seinen Atem an deinem Ohr."),
    (31.55, 32.72, 5, "Eine Stimme flüstert:"),
    (33.16, 34.28, 5, "Er schläft nicht."),
    (34.69, 35.06, 6, "Stopp."),
    (35.56, 36.62, 6, "Woher wissen sie das?"),
    (37.27, 38.52, 7, "Die Schritte gehen weiter."),
    (39.07, 40.45, 7, "Du öffnest ein Auge."),
    (40.80, 41.86, 7, "Nur einen Spalt."),
    (42.43, 44.67, 8, "Der Platz neben dir ist nicht mehr leer."),
    (45.12, 46.28, 8, "Dort sitzt jemand."),
    (46.71, 48.28, 8, "In deinem grünen Pullover."),
    (48.68, 49.83, 8, "Mit deinem Gesicht."),
    (50.34, 51.90, 9, "Er lächelt dich an und sagt:"),
    (52.28, 53.43, 9, "Ich übernehme ab hier."),
    (53.95, 55.49, 10, "Dann ruckelt das Flugzeug."),
    (55.71, 57.34, 10, "Und es geht steil nach unten."),
    (57.88, 58.83, 11, "Bleibst du sitzen –"),
    (59.13, 60.54, 11, "oder rennst du ins Cockpit?"),
    (60.96, 62.28, 11, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"Er schläft nicht.": 0.15, "Mit deinem Gesicht.": 0.2}  # dramatic beats kept a bit longer

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
