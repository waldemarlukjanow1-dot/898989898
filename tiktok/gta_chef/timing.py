"""Phrase timings for 'GTA 6 – Chef'. Real phrase times from speech recognition;
pauses are tightened (each phrase re-placed with short gaps).
"""

TEMPO = 1.0
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.16, 0.3


# (start, end, sequence index, text) in the ORIGINAL recording (ElevenLabs take, 62.3 s)
RAW = [
    (0.00, 2.89, 0, "Wenn dein Mitarbeiter dir dieses Video geschickt hat:"),
    (3.26, 6.04, 0, "Lies erst zu Ende, bevor du nein sagst."),
    (6.75, 9.68, 1, "Am neunzehnten November kommt GTA sechs."),
    (10.14, 12.48, 1, "Dreizehn Jahre hat er darauf gewartet."),
    (12.90, 15.31, 1, "Und er braucht genau einen Tag Urlaub."),
    (15.76, 16.84, 1, "Den Release-Tag."),
    (17.28, 18.06, 2, "Denn mal ehrlich:"),
    (18.33, 20.63, 2, "An diesem Tag ist er sowieso nicht bei der Sache."),
    (21.06, 24.95, 2, "Er sitzt am Schreibtisch, aber im Kopf ist er schon in Vice City."),
    (25.36, 27.49, 3, "Er schaut alle fünf Minuten aufs Handy."),
    (27.85, 29.52, 3, "Er tippt Mails mit Fehlern."),
    (29.92, 32.99, 3, "Und in der Kaffeeküche redet er über nichts anderes."),
    (33.44, 33.79, 4, "Stopp."),
    (34.24, 35.38, 4, "Jetzt sei mal ehrlich."),
    (35.74, 38.05, 4, "Willst du so einen Mitarbeiter im Büro?"),
    (38.68, 39.60, 5, "Sein Angebot:"),
    (39.97, 41.14, 5, "Einen Tag frei."),
    (41.50, 44.66, 5, "Dafür arbeitet er die Woche davor eine Stunde länger."),
    (45.01, 45.87, 5, "Jeden Tag."),
    (46.22, 47.07, 5, "Ohne zu meckern."),
    (47.51, 48.91, 6, "Und danach kommt er zurück."),
    (49.23, 50.10, 6, "Ausgeschlafen."),
    (50.40, 51.01, 6, "Glücklich."),
    (51.24, 53.15, 6, "Motivierter als je zuvor."),
    (53.60, 54.00, 7, "Also:"),
    (54.41, 55.33, 7, "Bekommt er frei?"),
    (55.73, 58.23, 7, "Schreib Ja oder Nein in die Kommentare."),
    (58.56, 62.08, 7, "Und schick das jedem Kumpel, der am neunzehnten auch frei braucht."),
]
EXTRA_GAP = {"Jetzt sei mal ehrlich.": 0.2, "Willst du so einen Mitarbeiter im Büro?": 0.1}

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
