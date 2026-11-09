"""Phrase timings for 'Flug 404 Teil 3' (ElevenLabs take, 68.8 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.1
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.22, 0.38

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 1.55, 0, "Noch neunzig Sekunden,"),
    (1.86, 4.07, 0, "dann kracht dieses Flugzeug in den Boden."),
    (4.52, 7.23, 0, "Und du bist der Einzige, der es verhindern kann."),
    (7.89, 8.52, 1, "Du rennst."),
    (8.83, 9.54, 1, "Durch den Gang."),
    (9.90, 12.96, 1, "Die Passagiere drehen ihre Köpfe. Alle gleichzeitig."),
    (13.38, 15.44, 2, "Die Cockpittür knallt hinter dir zu."),
    (15.84, 16.99, 2, "Zwei leere Sitze."),
    (17.36, 18.86, 2, "Rote Lampen überall."),
    (19.20, 20.14, 2, "Ein Alarm schreit:"),
    (20.43, 20.96, 2, "Pull up."),
    (21.18, 21.75, 2, "Pull up."),
    (22.33, 23.51, 3, "Du bist noch nie geflogen."),
    (23.91, 25.17, 3, "Aber du packst das Steuer."),
    (25.42, 27.58, 3, "Und ziehst. Mit aller Kraft."),
    (28.00, 29.19, 4, "Die Nase hebt sich."),
    (29.47, 30.08, 4, "Langsam."),
    (30.58, 32.96, 4, "Der Höhenmesser stoppt bei 300 Metern."),
    (33.37, 33.82, 5, "Stopp."),
    (34.32, 36.69, 5, "Wer hat eigentlich den Autopiloten ausgeschaltet?"),
    (37.23, 38.89, 6, "Durchs Fenster siehst du Lichter."),
    (39.26, 40.08, 6, "Eine Landebahn."),
    (40.46, 41.55, 6, "Mitten in der Nacht."),
    (41.85, 43.34, 6, "Mitten im Nirgendwo."),
    (43.86, 44.59, 7, "Du landest."),
    (44.85, 45.26, 7, "Hart."),
    (45.61, 46.80, 7, "Die Reifen kreischen."),
    (47.18, 49.23, 7, "Alles fühlt sich an wie in einem Traum."),
    (49.77, 50.63, 8, "Du drehst dich um."),
    (51.12, 52.53, 8, "Die Kabine ist leer."),
    (52.97, 55.88, 8, "Alle 187 Passagiere sind weg."),
    (56.30, 59.32, 9, "Nur einer sitzt noch auf Platz 32B."),
    (59.66, 60.09, 9, "Du."),
    (60.47, 61.76, 9, "Und er klatscht."),
    (62.41, 64.25, 10, "Hast du das Flugzeug gerettet –"),
    (64.57, 66.87, 10, "oder genau das getan, was sie wollten?"),
    (67.28, 68.60, 10, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"Du.": 0.2, "Alles fühlt sich an wie in einem Traum.": 0.2}  # dramatic beats kept a bit longer

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
