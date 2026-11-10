"""Phrase timings for 'Vice City' (PLANNED timing – replaced when the voice arrives).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.0
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.22, 0.38

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 1.15, 0, "Zwei Uhr dreiundvierzig."),
    (1.45, 2.22, 0, "Vice City."),
    (2.52, 4.83, 0, "Du sitzt in einem gestohlenen Lamborghini."),
    (5.13, 6.28, 0, "Auf dem Rücksitz:"),
    (6.58, 9.28, 0, "drei Festplatten mit unveröffentlichtem GTA sechs Material."),
    (9.78, 13.24, 1, "Du hast gerade das teuerste Videospiel der Welt gestohlen."),
    (13.74, 16.43, 2, "Dein Auftraggeber verspricht dir zehn Millionen Dollar."),
    (16.73, 18.65, 2, "Deine Freundin wartet am Flughafen."),
    (18.95, 20.49, 2, "Ein Privatjet steht bereit."),
    (20.99, 22.53, 3, "Dann vibriert dein Handy."),
    (22.83, 23.60, 3, "Unbekannte Nummer:"),
    (23.90, 24.67, 3, "Vertrau niemandem."),
    (24.97, 26.51, 3, "Auch nicht deiner Freundin."),
    (27.01, 27.78, 4, "Im Rückspiegel:"),
    (28.08, 28.58, 4, "Blaulicht."),
    (28.88, 29.65, 4, "Erst eins."),
    (29.95, 30.72, 4, "Dann drei."),
    (31.02, 31.78, 4, "Dann zehn."),
    (32.28, 33.82, 5, "Du trittst aufs Gas."),
    (34.12, 34.62, 5, "Zweihundert."),
    (34.92, 35.42, 5, "Zweihundertvierzig."),
    (35.72, 38.03, 5, "Die Stadt rast an dir vorbei."),
    (38.53, 39.03, 6, "Stopp."),
    (39.33, 42.02, 6, "Wie haben sie dich so schnell gefunden?"),
    (42.52, 44.06, 7, "Ein Hubschrauber über dir."),
    (44.36, 46.28, 7, "Der Suchscheinwerfer trifft dein Auto."),
    (46.58, 47.74, 7, "Straßensperre vor dir."),
    (48.24, 50.16, 8, "Du reißt das Lenkrad herum."),
    (50.46, 51.62, 8, "Durch einen Bauzaun."),
    (51.92, 53.45, 8, "Quer über die Landebahn."),
    (53.95, 54.72, 9, "Der Privatjet."),
    (55.02, 56.56, 9, "Die Motoren laufen schon."),
    (56.86, 58.02, 9, "Deine Freundin winkt:"),
    (58.32, 59.08, 9, "Steig ein!"),
    (59.58, 60.74, 10, "Noch fünfzig Meter."),
    (61.04, 62.96, 10, "Die Polizei direkt hinter dir."),
    (63.46, 66.54, 11, "Steigst du ein – oder fährst du weiter?"),
    (66.84, 68.76, 11, "Schreib es in die Kommentare."),
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
