"""Phrase timings for 'Flug 404 Teil 3' (PLANNED timing – replaced when the voice arrives).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.0
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.32, 0.5

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 4.00, 0, "Noch neunzig Sekunden, dann kracht dieses Flugzeug in den Boden."),
    (4.35, 7.95, 0, "Und du bist der Einzige, der es verhindern kann."),
    (8.50, 9.30, 1, "Du rennst."),
    (9.65, 10.85, 1, "Durch den Gang."),
    (11.20, 13.20, 1, "Die Passagiere drehen ihre Köpfe."),
    (13.55, 14.35, 1, "Alle gleichzeitig."),
    (14.90, 17.30, 2, "Die Cockpittür knallt hinter dir zu."),
    (17.65, 18.85, 2, "Zwei leere Sitze."),
    (19.20, 20.40, 2, "Rote Lampen überall."),
    (20.75, 21.95, 2, "Ein Alarm schreit:"),
    (22.30, 23.10, 2, "Pull up."),
    (23.45, 24.25, 2, "Pull up."),
    (24.80, 26.80, 3, "Du bist noch nie geflogen."),
    (27.15, 29.15, 3, "Aber du packst das Steuer."),
    (29.50, 30.30, 3, "Und ziehst."),
    (30.65, 31.85, 3, "Mit aller Kraft."),
    (32.40, 34.00, 4, "Die Nase hebt sich."),
    (34.35, 34.85, 4, "Langsam."),
    (35.20, 37.60, 4, "Der Höhenmesser stoppt bei dreihundert Metern."),
    (38.15, 38.65, 5, "Stopp."),
    (39.00, 41.40, 5, "Wer hat eigentlich den Autopiloten ausgeschaltet?"),
    (41.95, 43.95, 6, "Durchs Fenster siehst du Lichter."),
    (44.30, 45.10, 6, "Eine Landebahn."),
    (45.45, 47.05, 6, "Mitten in der Nacht."),
    (47.40, 48.60, 6, "Mitten im Nirgendwo."),
    (49.15, 49.95, 7, "Du landest."),
    (50.30, 50.80, 7, "Hart."),
    (51.15, 52.35, 7, "Die Reifen kreischen."),
    (52.70, 55.90, 7, "Alles fühlt sich an wie in einem Traum."),
    (56.45, 58.05, 8, "Du drehst dich um."),
    (58.40, 60.00, 8, "Die Kabine ist leer."),
    (60.35, 62.35, 8, "Alle hundertsiebenundachtzig Passagiere sind weg."),
    (62.90, 66.10, 9, "Nur einer sitzt noch auf Platz zweiunddreißig B."),
    (66.45, 66.95, 9, "Du."),
    (67.30, 68.50, 9, "Und er klatscht."),
    (69.05, 74.25, 10, "Hast du das Flugzeug gerettet – oder genau das getan, was sie wollten?"),
    (74.60, 76.60, 10, "Schreib es in die Kommentare."),
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
