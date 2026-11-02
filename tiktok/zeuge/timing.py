"""Phrase timings measured on the ElevenLabs take (voice_helmut.mp3, Der Zeuge).

Times are in the ORIGINAL recording (silence detection + Whisper per segment).
The video plays the voice sped up by TEMPO, so every time is divided by TEMPO.
Each phrase belongs to one sequence (index into script.SEQ).
"""

TEMPO = 1.05
VOICE = "audio/voice_helmut.mp3"

# (start, end, sequence index, text)
PHRASES = [
    (0.00, 1.63, 0, "Du hast einen Mord gesehen."),
    (2.11, 3.77, 0, "Jetzt sitzt du im Verhörraum."),
    (4.27, 5.88, 0, "Und die Polizei glaubt dir nicht."),
    (6.47, 7.83, 1, "Der Kommissar setzt sich."),
    (8.38, 9.42, 1, "Erzähl es nochmal."),
    (9.68, 10.70, 1, "Von Anfang an."),
    (11.41, 12.28, 2, "Gestern Nacht."),
    (12.60, 14.18, 2, "Parkhaus, Ebene drei."),
    (14.64, 16.12, 2, "Ein Mann im grauen Mantel."),
    (16.52, 17.16, 2, "Ein Schuss."),
    (17.66, 18.70, 3, "Der Kommissar nickt."),
    (19.23, 21.67, 3, "Und er trug schwarze Handschuhe, richtig?"),
    (22.19, 23.81, 3, "Du hast nie Handschuhe erwähnt."),
    (24.37, 25.55, 4, "Er schaut zum Spiegel."),
    (25.91, 26.67, 4, "Nur kurz."),
    (26.93, 27.64, 4, "Dann sagt er:"),
    (28.15, 28.94, 4, "Du lügst."),
    (29.45, 30.52, 5, "Du schließt die Augen."),
    (31.06, 31.90, 5, "Ebene drei."),
    (32.22, 34.05, 5, "Der Mantel ist jetzt schwarz."),
    (34.48, 35.72, 5, "Und der Mann dreht sich um."),
    (36.14, 36.50, 6, "Stopp."),
    (37.06, 38.66, 6, "Gestern war der Mantel grau."),
    (39.01, 39.33, 6, "Oder?"),
    (39.87, 40.87, 7, "Dann siehst du es."),
    (41.28, 43.38, 7, "Ein Knopf im Ohr des Kommissars."),
    (43.83, 45.00, 7, "Er hört nicht dir zu."),
    (45.48, 46.69, 8, "Der Spiegel beschlägt."),
    (47.03, 48.55, 8, "Jemand atmet dagegen."),
    (48.80, 49.96, 8, "Von der anderen Seite."),
    (50.45, 52.30, 9, "Der Kommissar schiebt dir ein Blatt hin."),
    (52.80, 53.81, 9, "Ein Geständnis."),
    (54.03, 55.07, 9, "Mit deinem Namen."),
    (55.55, 56.62, 10, "Das Licht flackert."),
    (56.94, 59.36, 10, "Für eine Sekunde siehst du durch den Spiegel."),
    (59.86, 60.78, 10, "Grauer Mantel."),
    (61.31, 61.96, 10, "Er lächelt."),
    (62.44, 63.33, 10, "Unterschreiben"),
    (63.74, 64.59, 10, "oder schweigen?"),
]

END_HOLD = 1.2  # seconds of picture after the last word


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
