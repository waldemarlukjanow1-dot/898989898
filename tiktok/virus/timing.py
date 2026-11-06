"""Phrase timings for 'Neues Virus' (ElevenLabs take, 70.2 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.15
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.22, 0.4

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 1.02, 0, "Du wachst auf."),
    (1.35, 2.79, 0, "Dein Handy explodiert."),
    (3.23, 5.29, 0, "Eilmeldung: ein neues Virus."),
    (5.50, 8.07, 0, "Es breitet sich schneller aus als alles davor."),
    (8.65, 10.62, 1, "Mittags sind die Supermärkte leer."),
    (10.94, 11.90, 1, "Nudeln weg."),
    (12.19, 13.51, 1, "Klopapier weg."),
    (13.92, 16.99, 1, "Die Leute streiten sich um das letzte Desinfektionsmittel."),
    (17.59, 18.48, 2, "Am nächsten Tag:"),
    (18.79, 19.72, 2, "Maskenpflicht."),
    (19.99, 21.41, 2, "Im Bus. Im Laden."),
    (21.64, 22.43, 2, "Auf der Arbeit."),
    (22.99, 24.05, 3, "Eine Woche später:"),
    (24.35, 26.66, 3, "Ausgangssperre ab 22 Uhr."),
    (27.07, 28.46, 3, "Die Straßen sind leer."),
    (28.78, 29.94, 3, "Nur Streifenwagen."),
    (30.51, 31.72, 4, "Dann kommt der Brief:"),
    (32.13, 32.61, 4, "Impfung."),
    (32.99, 34.82, 4, "Ohne Nachweis kein Restaurant."),
    (35.09, 37.18, 4, "Kein Kino. Kein Fitnessstudio."),
    (37.56, 38.48, 5, "Dein Chef schreibt:"),
    (38.75, 41.10, 5, "Ohne Nachweis brauchst du gar nicht mehr zu kommen."),
    (41.80, 42.26, 6, "Stopp."),
    (42.79, 43.92, 6, "Kommt dir das bekannt vor?"),
    (44.38, 46.67, 7, "Deine Familie streitet beim Abendessen."),
    (46.95, 48.50, 7, "Freunde schreiben dir nicht mehr."),
    (48.77, 50.81, 7, "Jeder ist plötzlich Experte."),
    (51.36, 53.01, 8, "Du stehst vor dem Impfzentrum."),
    (53.26, 55.20, 8, "Die Schlange ist 100 Meter lang."),
    (55.60, 56.64, 8, "Dein Handy vibriert:"),
    (56.93, 58.41, 8, "Termin in 10 Minuten."),
    (58.88, 59.81, 9, "Und du fragst dich:"),
    (60.19, 61.62, 9, "Mache ich das freiwillig?"),
    (61.92, 63.34, 9, "Oder weil ich keine Wahl habe?"),
    (64.10, 65.79, 10, "Macht ihr das alle wieder mit?"),
    (66.14, 68.37, 10, "Oder lasst ihr so etwas nicht mehr mit euch machen?"),
    (68.71, 70.01, 10, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"Kommt dir das bekannt vor?": 0.3, "Macht ihr das alle wieder mit?": 0.3}  # dramatic beats kept a bit longer

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


def words():
    out = []
    for a, b, seq, text in PHRASES:
        ws = text.split()
        weights = [len(w.strip(".,:?!'")) + 1.5 for w in ws]
        tot = sum(weights)
        t = a
        for w, wt in zip(ws, weights):
            d = (b - a) * wt / tot
            out.append(dict(w=w, a=t / TEMPO, b=(t + d) / TEMPO, seq=seq))
            t += d
    return out


def seq_bounds():
    starts = {}
    for a, b, seq, _ in PHRASES:
        starts.setdefault(seq, a / TEMPO)
    n = max(starts) + 1
    st = [0.0] + [starts[i] - 0.12 for i in range(1, n)]
    total = PHRASES[-1][1] / TEMPO + END_HOLD
    return [(st[i], st[i + 1] if i + 1 < n else total) for i in range(n)], total
