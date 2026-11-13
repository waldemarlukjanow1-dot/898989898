"""Phrase timings for '11 Millionen in der Wand'. Real phrase times from speech recognition;
pauses are tightened (each phrase re-placed with short gaps).
"""

TEMPO = 1.05
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.2, 0.35


# (start, end, sequence index, text) in the ORIGINAL recording (ElevenLabs take, 68.4 s)
RAW = [
    (0.00, 0.99, 0, "Stell dir vor:"),
    (1.51, 5.31, 0, "In der Wand deiner Wohnung sind elf Millionen Euro versteckt."),
    (5.79, 9.06, 0, "Und du schläfst seit drei Jahren direkt daneben."),
    (9.97, 11.88, 1, "Alles beginnt mit einem Nagel."),
    (12.45, 14.03, 1, "Du willst nur ein Bild aufhängen."),
    (14.50, 15.70, 1, "Die Wand klingt hohl."),
    (16.25, 16.94, 1, "Du bohrst."),
    (17.44, 20.05, 1, "Und plötzlich fällt ein Geldschein heraus."),
    (20.57, 21.80, 2, "Du reißt die Tapete ab."),
    (22.20, 22.75, 2, "Bündel."),
    (23.00, 23.62, 2, "Hunderte."),
    (24.18, 25.84, 2, "Du zählst die ganze Nacht."),
    (26.35, 28.08, 2, "Elf Millionen Euro."),
    (28.75, 30.80, 3, "Doch auf einem Bündel klebt ein Zettel:"),
    (31.26, 32.16, 3, "Nicht anfassen."),
    (32.47, 33.37, 3, "Wir kommen zurück."),
    (33.79, 34.29, 3, "Datum:"),
    (34.53, 34.99, 3, "morgen."),
    (35.75, 36.22, 4, "Stopp."),
    (36.78, 37.79, 4, "Jetzt überleg mal."),
    (38.20, 40.10, 4, "Wer hat vor dir hier gewohnt?"),
    (40.69, 41.82, 5, "Du suchst im Internet."),
    (42.24, 43.60, 5, "Und findest einen Artikel:"),
    (44.06, 45.89, 5, "Bankraub, vor drei Jahren."),
    (46.26, 46.87, 5, "Die Beute:"),
    (47.12, 48.05, 5, "elf Millionen."),
    (48.42, 49.32, 5, "Nie gefunden."),
    (49.85, 50.53, 5, "Der Täter:"),
    (50.92, 51.95, 5, "dein Vormieter."),
    (52.84, 53.89, 6, "Dann klingelt es."),
    (54.22, 54.91, 6, "Zweimal."),
    (55.44, 57.31, 6, "Durch den Spion siehst du einen Mann."),
    (57.72, 59.09, 6, "Er hält einen Schlüssel hoch."),
    (59.49, 61.53, 6, "Den Schlüssel zu deiner Wohnung."),
    (62.22, 63.45, 7, "Rufst du die Polizei?"),
    (63.88, 66.38, 7, "Oder nimmst du das Geld und verschwindest?"),
    (66.90, 68.24, 7, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"Stopp.": 0.25, "morgen.": 0.25, "dein Vormieter.": 0.3, "Den Schlüssel zu deiner Wohnung.": 0.2}

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
