"""Phrase timings for 'Tag 1 der Dunkelheit' (ElevenLabs take, 65.6 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.07
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.28, 0.45

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 1.04, 0, "Du wachst auf."),
    (1.51, 3.02, 0, "Es ist 6:30 Uhr."),
    (3.52, 5.56, 0, "Aber draußen ist es stockdunkel."),
    (5.97, 6.70, 1, "Keine Sonne."),
    (7.07, 8.08, 1, "Kein Morgenlicht."),
    (8.54, 9.84, 1, "Nur Dunkelheit."),
    (10.43, 11.99, 2, "Du schaltest den Fernseher ein."),
    (12.47, 14.14, 2, "Die Nachrichtensprecherin zittert:"),
    (14.66, 16.48, 2, "Die Sonne ist heute nicht aufgegangen."),
    (16.80, 17.87, 2, "Wir wissen nicht, warum."),
    (18.43, 20.10, 3, "Dann fällt der Strom aus."),
    (20.62, 21.29, 4, "Dein Handy:"),
    (21.57, 22.87, 4, "12 Prozent Akku."),
    (23.39, 25.35, 4, "Eine Nachricht von deinem besten Freund:"),
    (25.76, 27.38, 4, "Geh auf keinen Fall raus."),
    (27.87, 29.19, 5, "Du fragst: Warum?"),
    (29.66, 30.30, 5, "Er schreibt:"),
    (30.67, 32.43, 5, "Weil ich dich gerade gesehen habe."),
    (32.82, 33.32, 5, "Draußen."),
    (33.67, 34.55, 5, "Vor deiner Tür."),
    (35.09, 35.48, 6, "Stopp."),
    (35.92, 37.61, 6, "Du bist doch gerade erst aufgewacht."),
    (38.11, 39.12, 7, "In diesem Moment:"),
    (39.50, 41.65, 7, "drei laute Schläge an deiner Haustür."),
    (42.19, 43.68, 7, "Du schaust durch den Türspion."),
    (44.19, 44.89, 7, "Niemand da."),
    (45.42, 46.52, 8, "Dein Handy klingelt."),
    (46.95, 47.93, 8, "Unbekannte Nummer."),
    (48.40, 50.19, 8, "Eine verzerrte Stimme flüstert:"),
    (50.60, 51.99, 8, "Mach die Tür nicht auf."),
    (52.40, 53.80, 8, "Egal, was du hörst."),
    (54.34, 55.64, 9, "Dann hörst du sie."),
    (56.15, 57.49, 9, "Deine eigene Stimme."),
    (58.00, 59.06, 9, "Direkt vor der Tür:"),
    (59.55, 59.98, 9, "Bitte."),
    (60.41, 61.23, 9, "Lass mich rein."),
    (61.87, 63.56, 10, "Würdest du die Tür aufmachen?"),
    (63.97, 65.36, 10, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"Niemand da.": 0.25, "Deine eigene Stimme.": 0.2, "Würdest du die Tür aufmachen?": 0.5}  # dramatic beats kept a bit longer

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
