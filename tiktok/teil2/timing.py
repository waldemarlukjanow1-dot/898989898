"""Phrase timings measured on the ElevenLabs take (voice_helmut.mp3, Teil 2).

Times are in the ORIGINAL recording (silence detection + Whisper per segment).
The video plays the voice sped up by TEMPO, so every time is divided by TEMPO.
Each phrase belongs to one sequence (index into script.SEQ).
"""

TEMPO = 1.10
VOICE = "audio/voice_helmut.mp3"

# (start, end, sequence index, text)
PHRASES = [
    (0.00, 0.85, 0, "Du rennst."),
    (1.16, 2.03, 0, "Zwei Taschen."),
    (2.25, 5.60, 0, "Zwölf Millionen. Und Mira direkt hinter dir."),
    (6.24, 7.46, 1, "Ihr biegt in eine Gasse."),
    (7.92, 9.43, 1, "Die Sirenen werden leiser."),
    (9.95, 10.79, 1, "Zu leise."),
    (11.46, 13.46, 2, "Mira zieht dich in einen Hauseingang."),
    (13.92, 14.88, 2, "Und schließt auf."),
    (15.43, 16.94, 2, "Woher hat sie einen Schlüssel?"),
    (17.60, 18.09, 3, "Drinnen:"),
    (18.44, 19.51, 3, "eine leere Wohnung."),
    (19.96, 21.88, 3, "An der Wand der Plan der Bank."),
    (22.25, 23.04, 3, "Und in der Mitte:"),
    (23.44, 24.25, 3, "dein Foto."),
    (24.90, 25.72, 4, "Mira sagt:"),
    (26.05, 27.08, 4, "Ich kann das erklären."),
    (27.63, 28.92, 4, "Dann leuchtet ihr Handy."),
    (29.37, 30.31, 4, "Oskar ruft an."),
    (30.86, 31.24, 5, "Stopp."),
    (31.63, 32.94, 5, "Oskar hat dich verraten."),
    (33.34, 34.74, 5, "Warum ruft er sie an?"),
    (35.33, 36.74, 6, "Sie hebt ab und flüstert:"),
    (37.17, 38.76, 6, "Er hat den Umschlag gefunden."),
    (39.15, 40.35, 6, "Alles läuft nach Plan."),
    (40.98, 42.32, 7, "Du reißt die Taschen auf."),
    (42.80, 43.54, 7, "Kein Geld."),
    (43.89, 45.13, 7, "Nur Zeitungspapier."),
    (45.58, 47.26, 8, "Vier Taschen waren im Tresor."),
    (47.64, 49.37, 8, "Zwei sind mit Oskar gefahren."),
    (49.75, 50.99, 8, "Mit dem echten Geld."),
    (51.61, 52.74, 9, "Mira legt auf."),
    (53.09, 54.20, 9, "Greift in ihre Jacke."),
    (54.59, 56.97, 9, "Und legt eine Polizeimarke auf den Tisch."),
    (57.50, 59.21, 10, "Du warst nie Teil der Crew."),
    (59.73, 61.10, 10, "Du warst der Köder."),
    (61.81, 63.08, 10, "Mira oder Oskar:"),
    (63.46, 64.14, 10, "Wer lügt?"),
    (64.48, 65.74, 10, "Schreib's in die Kommentare."),
    (66.23, 66.67, 10, "Und du?"),
    (67.14, 67.98, 10, "Du rennst."),
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
