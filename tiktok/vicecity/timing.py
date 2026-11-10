"""Phrase timings for 'Vice City' (ElevenLabs take, 70.4 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.1
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.22, 0.38

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 1.77, 0, "Zwei Uhr dreiundvierzig."),
    (2.16, 2.94, 0, "Vice City."),
    (3.65, 6.08, 0, "Du sitzt in einem gestohlenen Lamborghini."),
    (6.48, 7.42, 0, "Auf dem Rücksitz:"),
    (7.71, 11.59, 0, "drei Festplatten mit unveröffentlichtem GTA 6 Material."),
    (12.23, 15.87, 1, "Du hast gerade das teuerste Videospiel der Welt gestohlen."),
    (16.42, 19.46, 2, "Dein Auftraggeber verspricht dir zehn Millionen Dollar."),
    (20.00, 22.02, 2, "Deine Freundin wartet am Flughafen."),
    (22.40, 23.95, 2, "Ein Privatjet steht bereit."),
    (24.59, 25.97, 3, "Dann vibriert dein Handy."),
    (26.52, 27.41, 3, "Unbekannte Nummer:"),
    (27.90, 29.07, 3, "Vertrau niemandem."),
    (29.44, 30.75, 3, "Auch nicht deiner Freundin."),
    (31.40, 32.23, 4, "Im Rückspiegel:"),
    (32.60, 33.20, 4, "Blaulicht."),
    (33.57, 34.27, 4, "Erst eins."),
    (34.63, 35.23, 4, "Dann drei."),
    (35.65, 36.43, 4, "Dann zehn."),
    (37.01, 38.13, 5, "Du trittst aufs Gas."),
    (38.36, 39.30, 5, "Zweihundert."),
    (39.45, 40.70, 5, "Zweihundertvierzig."),
    (40.90, 42.60, 5, "Die Stadt rast an dir vorbei."),
    (43.10, 43.46, 6, "Stopp."),
    (43.98, 45.71, 6, "Wie haben sie dich so schnell gefunden?"),
    (46.23, 47.54, 7, "Ein Hubschrauber über dir."),
    (47.87, 49.83, 7, "Der Suchscheinwerfer trifft dein Auto."),
    (50.28, 51.64, 7, "Straßensperre vor dir."),
    (51.79, 53.47, 8, "Du reißt das Lenkrad herum."),
    (53.81, 54.90, 8, "Durch einen Bauzaun."),
    (55.10, 56.42, 8, "Quer über die Landebahn."),
    (56.82, 57.80, 9, "Der Privatjet."),
    (57.95, 59.25, 9, "Die Motoren laufen schon."),
    (59.70, 60.75, 9, "Deine Freundin winkt:"),
    (60.90, 61.69, 9, "Steig ein!"),
    (62.18, 63.39, 10, "Noch fünfzig Meter."),
    (63.70, 65.41, 10, "Die Polizei direkt hinter dir."),
    (65.81, 66.99, 11, "Für Ablenkung sorgen –"),
    (67.33, 68.49, 11, "oder einsteigen?"),
    (68.93, 70.21, 11, "Schreib es in die Kommentare."),
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
