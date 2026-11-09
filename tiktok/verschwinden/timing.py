"""Phrase timings for '24 Stunden verschwinden' (PLANNED timing – replaced when the voice arrives).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.0
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.22, 0.38

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 1.15, 0, "Zwanzig Millionen Euro."),
    (1.45, 4.15, 0, "Dafür musst du nur vierundzwanzig Stunden verschwinden."),
    (4.45, 5.22, 0, "Keine Fragen."),
    (5.52, 6.28, 0, "Keine Polizei."),
    (6.58, 7.35, 0, "Keine Familie."),
    (7.85, 9.01, 1, "Du sagst ja."),
    (9.31, 13.15, 1, "In derselben Nacht hält ein schwarzer SUV vor deiner Tür."),
    (13.65, 15.19, 2, "Dein Handy wird zerstört."),
    (15.49, 17.80, 2, "Dein Name aus jeder Datenbank gelöscht."),
    (18.10, 20.41, 2, "Offiziell gibt es dich nicht mehr."),
    (20.91, 22.06, 3, "Am nächsten Morgen:"),
    (22.36, 22.86, 3, "Eilmeldung."),
    (23.16, 24.32, 3, "Unternehmer tot aufgefunden."),
    (24.62, 25.38, 3, "Dein Foto."),
    (25.68, 26.45, 3, "Dein Name."),
    (26.95, 28.49, 4, "Auf deinem neuen Konto:"),
    (28.79, 29.56, 4, "fünf Millionen."),
    (29.86, 31.02, 4, "Die erste Zahlung."),
    (31.52, 32.02, 5, "Stopp."),
    (32.32, 35.39, 5, "Wer zahlt so viel für einen toten Mann?"),
    (35.89, 37.82, 6, "Im Hotelzimmer klingelt das Telefon."),
    (38.12, 39.27, 6, "Eine Stimme flüstert:"),
    (39.57, 42.65, 6, "Du hast vergessen, wem du das Geld schuldest."),
    (43.15, 45.45, 7, "Auf dem Bett liegt ein Umschlag."),
    (45.75, 47.29, 7, "Ein Foto deiner Familie."),
    (47.59, 48.75, 7, "Von heute Morgen."),
    (49.05, 50.20, 7, "Auf der Rückseite:"),
    (50.50, 51.27, 7, "Bleib tot."),
    (51.77, 54.46, 8, "Dann hörst du einen Schlüssel im Schloss."),
    (54.76, 57.45, 8, "Niemand weiß, in welchem Hotel du bist."),
    (57.95, 59.49, 9, "Dein neues Handy leuchtet:"),
    (59.79, 60.56, 9, "Zielperson gefunden."),
    (61.06, 62.60, 10, "Die Tür geht auf."),
    (62.90, 65.21, 10, "Es ist der Fahrer vom SUV."),
    (65.51, 66.66, 10, "Er sagt nur:"),
    (66.96, 68.88, 10, "Die vierundzwanzig Stunden sind um."),
    (69.38, 70.54, 11, "Verstecken oder fliehen?"),
    (70.84, 72.76, 11, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {}  # dramatic beats kept a bit longer

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
