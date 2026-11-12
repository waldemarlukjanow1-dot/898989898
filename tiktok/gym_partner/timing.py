"""Phrase timings for 'Gym-Partner'. Real phrase times from speech recognition;
pauses are tightened (each phrase re-placed with short gaps).
"""

TEMPO = 1.0
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.3, 0.5


# (start, end, sequence index, text) in the ORIGINAL recording (ElevenLabs take, 49.2 s)
RAW = [
    (0.00, 2.91, 0, "Wenn dein Gym-Partner dir dieses Video geschickt hat:"),
    (3.44, 4.31, 0, "Du bist gemeint."),
    (4.98, 6.02, 1, "Montag sagst du:"),
    (6.33, 6.91, 1, "Ich komme."),
    (7.36, 7.78, 1, "Und dann?"),
    (8.29, 9.45, 1, "Eine Nachricht um fünf:"),
    (9.89, 11.05, 1, "Heute schaff ich's nicht."),
    (11.51, 12.01, 2, "Mittwoch:"),
    (12.37, 12.80, 2, "Rücken."),
    (13.27, 13.95, 2, "Freitag:"),
    (14.29, 15.15, 2, "Zu müde."),
    (15.57, 16.27, 2, "Samstag:"),
    (16.58, 17.06, 2, "Grillen."),
    (17.59, 20.29, 2, "Und er steht wieder allein an der Hantelbank."),
    (20.81, 22.32, 3, "Und weißt du, was das Schlimmste ist?"),
    (22.69, 24.47, 3, "Er wird jede Woche stärker."),
    (24.95, 25.75, 3, "Und du nicht."),
    (26.21, 26.55, 4, "Stopp."),
    (26.96, 27.98, 4, "Jetzt sei mal ehrlich."),
    (28.21, 30.33, 4, "Wie oft hast du dieses Jahr abgesagt?"),
    (30.86, 31.79, 5, "Sein Angebot:"),
    (32.13, 32.86, 5, "Er holt dich ab."),
    (33.25, 34.65, 5, "Er packt dir sogar die Tasche."),
    (35.03, 36.86, 5, "Und nach dem Training gibt's Döner."),
    (37.17, 37.78, 5, "Er zahlt."),
    (38.22, 39.27, 6, "Nur eine Bedingung:"),
    (39.63, 41.58, 6, "Ab heute keine Ausreden mehr."),
    (42.05, 42.43, 7, "Also:"),
    (42.79, 43.64, 7, "Kommst du morgen mit?"),
    (44.05, 46.21, 7, "Schreib Ja oder Nein in die Kommentare."),
    (46.56, 49.16, 7, "Und markier den Kumpel, der immer absagt."),
]
EXTRA_GAP = {"Stopp.": 0.3, "Und du nicht.": 0.25, "Er zahlt.": 0.2, "Ab heute keine Ausreden mehr.": 0.25}

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
