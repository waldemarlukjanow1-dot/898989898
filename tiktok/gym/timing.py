"""Phrase timings for 'Gym – ab heute'. Real phrase times from speech recognition;
pauses are tightened (each phrase re-placed with short gaps).
"""

TEMPO = 1.035
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.16, 0.3


# (start, end, sequence index, text) in the ORIGINAL recording (ElevenLabs take, 67.3 s)
RAW = [
    (0.00, 2.86, 0, "Stell dir vor, du ziehst ab heute Gym durch."),
    (3.21, 3.97, 0, "Kein Montag."),
    (4.29, 5.08, 0, "Kein Neujahr."),
    (5.54, 5.98, 0, "Heute."),
    (6.67, 7.45, 1, "Tag eins:"),
    (7.90, 10.26, 1, "Du weißt nicht, welche Maschine was macht."),
    (10.67, 11.05, 1, "Egal."),
    (11.44, 12.08, 1, "Du bist da."),
    (12.59, 13.99, 1, "Das ist der schwerste Teil."),
    (14.69, 15.58, 2, "Woche eins:"),
    (15.99, 17.76, 2, "Muskelkater überall."),
    (18.19, 19.69, 2, "Treppen werden dein Feind."),
    (20.14, 21.51, 2, "Aber du gehst trotzdem."),
    (22.22, 22.93, 3, "Tipp eins:"),
    (23.31, 24.61, 3, "Dreimal die Woche reicht."),
    (24.96, 25.63, 3, "Ganzkörper."),
    (25.91, 27.11, 3, "Fünfundvierzig Minuten."),
    (27.81, 28.48, 3, "Tipp zwei:"),
    (28.87, 31.02, 3, "Jede Woche ein bisschen mehr Gewicht."),
    (31.38, 32.11, 3, "Nur ein bisschen."),
    (32.78, 33.46, 3, "Tipp drei:"),
    (33.87, 35.22, 3, "Iss genug Eiweiß."),
    (35.51, 36.90, 3, "Und schlaf acht Stunden."),
    (37.23, 39.22, 3, "Denn im Schlaf wachsen deine Muskeln."),
    (39.93, 40.84, 4, "Monat drei:"),
    (41.26, 42.78, 4, "Dein T-Shirt sitzt enger."),
    (43.21, 44.00, 4, "An den Schultern."),
    (44.72, 45.63, 4, "Monat sechs:"),
    (45.94, 46.86, 4, "Jemand fragt dich:"),
    (47.14, 47.90, 4, "Trainierst du?"),
    (48.36, 50.79, 5, "Und nach einem Jahr schaust du in den Spiegel."),
    (51.20, 52.91, 5, "Und erkennst dich kaum wieder."),
    (53.57, 53.98, 6, "Stopp."),
    (54.48, 58.97, 6, "Das Einzige, was zwischen dir und diesem Spiegelbild steht, ist ein Wort:"),
    (59.51, 59.98, 6, "Heute."),
    (60.55, 60.96, 7, "Also:"),
    (61.39, 62.26, 7, "Wann fängst du an?"),
    (62.70, 65.06, 7, "Schreib „Tag eins“ in die Kommentare."),
    (65.33, 67.12, 7, "Und markier deinen Gym-Partner."),
]
EXTRA_GAP = {"Stopp.": 0.25, "Heute.": 0.15}

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
