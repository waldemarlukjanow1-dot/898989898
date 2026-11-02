"""Phrase timings measured on the ElevenLabs take (voice_helmut.mp3, Am Steuer).

Times are in the ORIGINAL recording (silence detection + Whisper per segment).
The video plays the voice sped up by TEMPO, so every time is divided by TEMPO.
Each phrase belongs to one sequence (index into script.SEQ).
"""

TEMPO = 1.12
VOICE = "audio/voice_helmut.mp3"

# (start, end, sequence index, text)
PHRASES = [
    (0.00, 1.20, 0, "Sechs Uhr morgens."),
    (1.52, 3.43, 0, "Vor dir hält ein Geldtransporter."),
    (3.79, 5.48, 0, "Dreißig Millionen Euro."),
    (5.89, 8.00, 0, "In neunzig Sekunden gehören sie dir."),
    (8.54, 9.92, 1, "Sechs Monate Planung."),
    (10.35, 12.31, 1, "Zwei Komplizen sperren die Straße."),
    (12.63, 14.40, 1, "Dein Bruder Leon bleibt im Wagen."),
    (14.79, 15.42, 1, "Am Steuer."),
    (15.82, 16.30, 2, "Jetzt."),
    (16.72, 17.70, 2, "Du springst raus."),
    (18.00, 19.73, 2, "Die Wachleute legen sich auf den Boden."),
    (20.15, 21.28, 2, "Einer schaut dich an."),
    (21.83, 22.40, 2, "Und nickt."),
    (22.78, 24.12, 3, "Vier Koffer in den Wagen."),
    (24.40, 25.49, 3, "Leon gibt Gas."),
    (25.76, 26.45, 4, "Kein Schuss."),
    (26.65, 27.55, 4, "Keine Verletzten."),
    (27.87, 30.10, 4, "Du ziehst die Maske runter und lachst."),
    (30.54, 31.87, 5, "Dann vibriert dein Handy."),
    (32.23, 33.13, 5, "Unbekannte Nummer:"),
    (33.50, 34.58, 5, "Danke fürs Tragen."),
    (35.06, 35.46, 6, "Stopp."),
    (35.82, 37.18, 6, "Wer wusste von den Koffern?"),
    (37.60, 38.68, 6, "Nur ihr vier."),
    (39.12, 40.55, 7, "Du reißt einen Koffer auf."),
    (40.85, 41.66, 7, "Unter dem Geld:"),
    (41.93, 43.01, 7, "ein Peilsender."),
    (43.42, 44.69, 8, "Leon bleibt ruhig."),
    (45.08, 46.12, 8, "Viel zu ruhig."),
    (46.46, 47.16, 8, "Und biegt ab."),
    (47.51, 48.44, 8, "Falsche Richtung."),
    (48.87, 50.36, 9, "Er hält vor einer Lagerhalle."),
    (50.71, 52.00, 9, "Dort wartet der Wachmann."),
    (52.34, 53.63, 9, "Der, der genickt hat."),
    (54.02, 56.12, 10, "Leon nimmt die Koffer und steigt aus."),
    (56.43, 57.60, 10, "Er war nie draußen."),
    (57.90, 59.55, 10, "Keine Kamera hat ihn gesehen."),
    (59.96, 60.69, 11, "Aber dich."),
    (61.05, 61.88, 11, "Ohne Maske."),
    (62.22, 64.68, 11, "Für die Polizei gibt es nur einen Täter:"),
    (65.17, 65.56, 11, "dich."),
    (65.97, 66.63, 12, "Sirenen."),
    (66.94, 68.62, 12, "Fliehen oder Leon jagen?"),
    (68.95, 70.29, 12, "Schreib es in die Kommentare."),
]

END_HOLD = 1.0  # seconds of picture after the last word


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
