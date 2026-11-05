"""Phrase timings for 'Schnelle Welle' (ElevenLabs take, 70.5 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.12
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.22, 0.4

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 2.35, 0, "Der Bruder schreibt unter das letzte Video:"),
    (2.75, 3.71, 0, "Schnelle Welle."),
    (4.08, 5.23, 0, "Straßenapotheker."),
    (5.72, 6.29, 0, "Okay."),
    (6.62, 7.83, 0, "Schauen wir uns das mal an."),
    (8.47, 10.47, 1, "Du bist jetzt Straßenapotheker."),
    (10.94, 12.47, 1, "Das erste Geld kommt schnell."),
    (12.94, 13.63, 1, "Zu schnell."),
    (14.12, 16.59, 2, "Ab jetzt ist jedes Auto ein Problem."),
    (16.93, 18.42, 2, "Jeder dunkle Golf."),
    (18.70, 19.74, 2, "Jedes Blaulicht."),
    (20.13, 21.10, 2, "Sind das die Cops?"),
    (21.58, 22.70, 3, "Du schläfst nicht mehr."),
    (23.16, 26.71, 3, "Jedes Geräusch im Treppenhaus – und du stehst sofort am Fenster."),
    (27.19, 28.21, 4, "Dein Handy klingelt."),
    (28.60, 29.52, 4, "Unbekannte Nummer."),
    (29.98, 30.87, 4, "Du gehst nicht ran."),
    (31.32, 32.03, 4, "Nie mehr."),
    (32.52, 33.19, 5, "Und das Geld?"),
    (33.67, 34.83, 5, "Kannst du nicht ausgeben."),
    (35.25, 35.98, 5, "Kein Konto."),
    (36.33, 37.84, 5, "Kein Herkunftsnachweis."),
    (38.31, 39.48, 5, "Es liegt im Schuhkarton."),
    (39.99, 40.41, 6, "Stopp."),
    (40.88, 41.83, 6, "Du hast Geld –"),
    (42.10, 43.82, 6, "und kannst nichts damit machen?"),
    (44.35, 45.32, 7, "Deine Mutter fragt:"),
    (45.68, 47.17, 7, "Woher hast du die neuen Schuhe?"),
    (47.68, 48.35, 7, "Du lügst."),
    (48.62, 49.37, 7, "Schon wieder."),
    (49.82, 51.73, 8, "Dann wird dein bester Kumpel erwischt."),
    (52.23, 54.49, 8, "Und plötzlich fragst du dich nur noch eins:"),
    (54.95, 56.23, 8, "Was hat er erzählt?"),
    (56.87, 57.94, 9, "Sechs Uhr morgens."),
    (58.28, 58.91, 9, "Es klingelt."),
    (59.36, 59.99, 9, "Dreimal."),
    (60.47, 61.54, 9, "Durch den Türspion:"),
    (61.97, 62.62, 9, "Polizei."),
    (63.09, 63.97, 10, "Schnelle Welle?"),
    (64.48, 65.63, 10, "Die Welle war schnell."),
    (66.06, 67.25, 10, "Und schnell vorbei."),
    (67.76, 68.57, 10, "Lohnt sich das?"),
    (69.00, 70.31, 10, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"Polizei.": 0.35, "Und schnell vorbei.": 0.2}  # dramatic beats kept a bit longer

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
