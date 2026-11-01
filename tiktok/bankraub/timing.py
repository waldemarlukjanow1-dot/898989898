"""Phrase timings measured on the ElevenLabs take (voice_helmut.mp3).

Times are in the ORIGINAL recording (silence detection + Whisper per segment).
The video plays the voice sped up by TEMPO, so every time is divided by TEMPO.
Each phrase belongs to one sequence (index into script.SEQ).
"""

TEMPO = 1.10
VOICE = "audio/voice_helmut.mp3"

# (start, end, sequence index, text)
PHRASES = [
    (0.00, 1.08, 0, "Drei Uhr zwölf."),
    (1.57, 3.26, 0, "Du stehst vor der Zentralbank."),
    (3.67, 6.08, 0, "In neunzig Sekunden geht der Alarm wieder an."),
    (6.52, 7.99, 1, "Mira hackt die Kameras."),
    (8.29, 9.51, 1, "Oskar fährt den Wagen."),
    (9.83, 10.23, 1, "Und du?"),
    (10.75, 12.14, 1, "Du knackst den Tresor."),
    (12.73, 13.52, 2, "Mira nickt."),
    (14.03, 16.43, 2, "Die Kameras zeigen nur noch eine leere Halle."),
    (16.77, 17.81, 2, "In Dauerschleife."),
    (18.34, 19.73, 3, "Du ziehst die Handschuhe aus."),
    (20.12, 22.19, 3, "Für dieses Schloss brauchst du Gefühl."),
    (22.74, 23.11, 3, "Klick."),
    (23.46, 23.86, 3, "Klick."),
    (24.18, 24.57, 3, "Klick."),
    (25.06, 26.31, 4, "Die Tür schwingt auf."),
    (26.79, 28.96, 4, "Zwölf Komma sechs Millionen Euro."),
    (29.30, 30.51, 5, "Noch dreißig Sekunden."),
    (31.04, 32.87, 5, "Ihr stopft alles in vier Taschen."),
    (33.42, 34.43, 6, "Dann siehst du ihn."),
    (34.96, 36.00, 6, "Einen Umschlag."),
    (36.45, 37.61, 6, "Mit deinem Namen."),
    (38.14, 38.47, 7, "Stopp."),
    (38.89, 40.65, 7, "Niemand kennt deinen echten Namen."),
    (41.05, 41.70, 7, "Niemand."),
    (42.22, 42.68, 8, "Darin:"),
    (43.07, 44.20, 8, "ein Foto von dir."),
    (44.61, 45.49, 8, "Ohne Handschuhe."),
    (45.87, 46.65, 8, "Am Tresor."),
    (47.09, 48.01, 8, "Und ein Zettel:"),
    (48.51, 50.08, 8, "Danke für die Fingerabdrücke."),
    (50.60, 50.85, 9, "O."),
    (51.34, 52.26, 9, "Wie Oskar."),
    (52.79, 55.06, 9, "Und genau jetzt geht der Alarm los."),
    (55.25, 56.16, 9, "Viel zu früh."),
    (56.59, 57.48, 10, "Ihr rennt raus."),
    (57.84, 59.04, 10, "Der Fluchtwagen ist da."),
    (59.43, 60.28, 10, "Und fährt los."),
    (60.64, 61.37, 10, "Ohne euch."),
    (61.81, 63.57, 11, "Sirenen von überall."),
    (64.01, 65.14, 11, "Rennen oder stellen?"),
    (65.51, 66.75, 11, "Schreib's in die Kommentare."),
    (67.10, 68.72, 11, "Davon hängt Teil zwei ab."),
]

END_HOLD = 0.6  # seconds of picture after the last word


def words():
    """Word-level timings (video time). Word duration ~ proportional to letters."""
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
    """Video-time start of each sequence = start of its first phrase (first one at 0)."""
    starts = {}
    for a, b, seq, _ in PHRASES:
        starts.setdefault(seq, a / TEMPO)
    n = max(starts) + 1
    st = [0.0] + [starts[i] - 0.12 for i in range(1, n)]
    total = PHRASES[-1][1] / TEMPO + END_HOLD
    return [(st[i], st[i + 1] if i + 1 < n else total) for i in range(n)], total
