"""Phrase timings for 'GTA 6 – Freundin' (ElevenLabs take, 52.3 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.0
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.3, 0.45

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 2.60, 0, "Wenn dein Freund dir dieses Video geschickt hat:"),
    (2.96, 3.65, 0, "Bleib dran."),
    (4.03, 5.59, 0, "Er hat sich das gut überlegt."),
    (5.99, 7.66, 1, "GTA 6 kommt."),
    (8.07, 10.47, 1, "Er wartet seit über zehn Jahren darauf."),
    (10.73, 12.00, 1, "Länger, als ihr euch kennt."),
    (12.45, 14.49, 2, "Er will kein Wochenende in Paris."),
    (14.65, 15.75, 2, "Keine neuen Schuhe."),
    (16.03, 18.43, 2, "Nur ein paar Abende mit einem Controller."),
    (18.88, 19.74, 3, "Und denk mal nach:"),
    (20.12, 22.85, 3, "Solange er spielt, weißt du genau, wo er ist."),
    (23.26, 24.16, 3, "Auf dem Sofa."),
    (24.50, 25.14, 3, "Neben dir."),
    (25.60, 27.34, 4, "Er schreibt keiner anderen Frau."),
    (27.66, 29.51, 4, "Er fährt nur durch Vice City."),
    (30.08, 30.42, 5, "Stopp."),
    (30.88, 31.93, 5, "Jetzt sei mal ehrlich."),
    (32.24, 33.83, 5, "Das klingt doch fair, oder nicht?"),
    (34.32, 35.22, 6, "Sein Angebot:"),
    (35.59, 36.96, 6, "Am Wochenende spielt er."),
    (37.27, 38.64, 6, "Unter der Woche kocht er."),
    (39.05, 40.45, 6, "Und das Essen mit deinen Eltern?"),
    (40.74, 41.64, 6, "Schon zugesagt."),
    (42.01, 44.69, 7, "Und wenn du willst, bekommst du den zweiten Controller."),
    (45.11, 45.52, 8, "Also:"),
    (45.86, 47.63, 8, "Darf er GTA 6 spielen?"),
    (47.98, 50.30, 8, "Schreib Ja oder Nein in die Kommentare."),
    (50.53, 52.04, 8, "Und markier deinen Freund."),
]
EXTRA_GAP = {"Jetzt sei mal ehrlich.": 0.2, "Schon zugesagt.": 0.15}  # dramatic beats kept a bit longer

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
