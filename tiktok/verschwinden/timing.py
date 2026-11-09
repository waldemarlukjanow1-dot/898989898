"""Phrase timings for '24 Stunden verschwinden' (ElevenLabs take, 72.6 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.12
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.22, 0.38

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 1.99, 0, "Zwanzig Millionen Euro."),
    (2.51, 5.24, 0, "Dafür musst du nur 24 Stunden verschwinden."),
    (5.73, 6.47, 0, "Keine Fragen."),
    (6.81, 7.71, 0, "Keine Polizei."),
    (8.01, 8.99, 0, "Keine Familie."),
    (9.55, 10.48, 1, "Du sagst ja."),
    (11.13, 14.63, 1, "In derselben Nacht hält ein schwarzer Geländewagen vor deiner Tür."),
    (15.04, 16.45, 2, "Dein Handy wird zerstört."),
    (16.78, 19.23, 2, "Dein Name aus jeder Datenbank gelöscht."),
    (19.63, 20.28, 2, "Offiziell"),
    (20.59, 21.69, 2, "gibt es dich nicht mehr."),
    (22.33, 23.26, 3, "Am nächsten Morgen:"),
    (23.60, 24.29, 3, "Eilmeldung."),
    (24.54, 26.20, 3, "Unternehmer tot aufgefunden."),
    (26.59, 27.33, 3, "Dein Foto."),
    (27.66, 28.38, 3, "Dein Name."),
    (28.89, 30.16, 4, "Auf deinem neuen Konto:"),
    (30.35, 31.48, 4, "fünf Millionen."),
    (31.68, 32.91, 4, "Die erste Zahlung."),
    (33.48, 33.95, 5, "Stopp."),
    (34.45, 36.92, 5, "Wer zahlt so viel für einen toten Mann?"),
    (37.54, 39.60, 6, "Im Hotelzimmer klingelt das Telefon."),
    (40.06, 41.15, 6, "Eine Stimme flüstert:"),
    (41.58, 43.99, 6, "Du hast vergessen, wem du das Geld schuldest."),
    (44.57, 46.32, 7, "Auf dem Bett liegt ein Umschlag."),
    (46.71, 48.19, 7, "Ein Foto deiner Familie."),
    (48.56, 49.42, 7, "Von heute Morgen."),
    (49.90, 50.86, 7, "Auf der Rückseite:"),
    (51.29, 52.21, 7, "Bleib tot."),
    (52.79, 54.76, 8, "Dann hörst du einen Schlüssel im Schloss."),
    (55.28, 57.48, 8, "Niemand weiß, in welchem Hotel du bist."),
    (57.90, 59.32, 9, "Dein neues Handy leuchtet:"),
    (59.67, 61.08, 9, "Zielperson gefunden."),
    (61.65, 62.66, 10, "Die Tür geht auf."),
    (63.05, 65.10, 10, "Es ist der Fahrer vom SUV."),
    (65.52, 66.24, 10, "Er sagt nur:"),
    (66.65, 68.52, 10, "Die 24 Stunden sind um."),
    (69.22, 70.63, 11, "Angreifen oder fliehen?"),
    (71.08, 72.39, 11, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"Bleib tot.": 0.2, "Die 24 Stunden sind um.": 0.2}  # dramatic beats kept a bit longer

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
