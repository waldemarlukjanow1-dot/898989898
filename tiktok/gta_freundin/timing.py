"""Phrase timings for 'GTA 6 – Freundin' (PLANNED timing – replaced when the voice arrives).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.0
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.22, 0.38

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 3.08, 0, "Wenn dein Freund dir dieses Video geschickt hat:"),
    (3.38, 4.15, 0, "Bleib dran."),
    (4.45, 6.75, 0, "Er hat sich das gut überlegt."),
    (7.25, 8.41, 1, "GTA sechs kommt."),
    (8.71, 11.40, 1, "Er wartet seit über zehn Jahren darauf."),
    (11.70, 13.62, 1, "Länger, als ihr euch kennt."),
    (14.12, 16.43, 2, "Er will kein Wochenende in Paris."),
    (16.73, 17.88, 2, "Keine neuen Schuhe."),
    (18.18, 20.88, 2, "Nur ein paar Abende mit einem Controller."),
    (21.38, 22.92, 3, "Und denk mal nach:"),
    (23.22, 26.68, 3, "Solange er spielt, weißt du genau, wo er ist."),
    (26.98, 28.13, 3, "Auf dem Sofa."),
    (28.43, 29.20, 3, "Neben dir."),
    (29.70, 31.62, 4, "Er schreibt keiner anderen Frau."),
    (31.92, 34.23, 4, "Er fährt nur durch Vice City."),
    (34.73, 35.23, 5, "Stopp."),
    (35.53, 36.68, 5, "Klingt fair, oder?"),
    (37.18, 37.95, 6, "Sein Angebot:"),
    (38.25, 39.79, 6, "Am Wochenende spielt er."),
    (40.09, 42.02, 6, "Unter der Woche kocht er."),
    (42.32, 44.62, 6, "Und das Essen mit deinen Eltern?"),
    (44.92, 45.69, 6, "Schon zugesagt."),
    (46.19, 49.65, 7, "Und wenn du willst, bekommst du den zweiten Controller."),
    (50.15, 50.65, 8, "Also:"),
    (50.95, 52.88, 8, "Darf er GTA sechs spielen?"),
    (53.18, 55.87, 8, "Schreib Ja oder Nein in die Kommentare."),
    (56.17, 57.71, 8, "Und markier deinen Freund."),
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
