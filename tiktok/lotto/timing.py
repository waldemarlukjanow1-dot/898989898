"""Phrase timings measured on the ElevenLabs take (voice_helmut.mp3, Der Schein).

Times are in the ORIGINAL recording (silence detection + Whisper per segment).
The video plays the voice sped up by TEMPO, so every time is divided by TEMPO.
Each phrase belongs to one sequence (index into script.SEQ).
"""

TEMPO = 1.09
VOICE = "audio/voice_helmut.mp3"

# (start, end, sequence index, text)
PHRASES = [
    (0.00, 3.53, 0, "Du hast gerade siebenundvierzig Millionen im Lotto gewonnen."),
    (3.84, 5.07, 0, "Niemand weiß davon."),
    (5.39, 6.88, 0, "Und so muss es bleiben."),
    (7.52, 10.54, 1, "Morgen um neun bringst du den Schein zur Lotto-Zentrale."),
    (10.95, 12.45, 1, "Du erzählst es nur einem:"),
    (12.85, 14.58, 1, "deinem besten Freund Marco."),
    (15.42, 16.83, 2, "Nachts klopft es."),
    (17.31, 18.39, 2, "Durch den Türspion:"),
    (18.88, 19.39, 2, "niemand."),
    (19.93, 21.55, 2, "Auf der Fußmatte liegt ein Zettel."),
    (22.01, 22.84, 2, "Gratuliere."),
    (23.39, 24.46, 3, "Du rufst Marco an."),
    (24.82, 27.41, 3, "Er schwört: Ich habe es keinem gesagt."),
    (28.02, 29.95, 4, "Am Morgen sind deine Schuhe nass."),
    (30.37, 31.01, 4, "Komisch."),
    (31.36, 33.10, 4, "Du warst doch die ganze Nacht zu Hause."),
    (33.76, 34.77, 5, "Lotto-Zentrale."),
    (35.24, 36.64, 5, "Die Frau prüft den Schein."),
    (37.06, 37.80, 5, "Dann sagt sie:"),
    (38.25, 39.26, 5, "Das ist eine Kopie."),
    (39.69, 41.75, 5, "Der echte wurde heute Nacht eingelöst."),
    (42.20, 42.61, 6, "Stopp."),
    (43.04, 45.47, 6, "Der Schein war die ganze Nacht in deiner Jacke."),
    (45.86, 47.18, 6, "Wer hat ihn getauscht?"),
    (47.75, 50.59, 7, "Sie zeigt dir das Kamerabild der Tankstelle an der Ecke."),
    (51.01, 52.23, 7, "Zwei Uhr vierzehn."),
    (52.64, 54.34, 7, "Ein Mann in deiner Jacke."),
    (54.78, 55.64, 8, "Er dreht sich um."),
    (56.08, 57.23, 8, "Es ist nicht Marco."),
    (57.66, 58.56, 9, "Es bist du."),
    (59.29, 60.22, 10, "Nasse Schuhe."),
    (60.56, 61.60, 10, "Keine Erinnerung."),
    (62.07, 62.64, 10, "Zwilling,"),
    (62.98, 63.65, 10, "Doppelgänger,"),
    (64.01, 65.59, 10, "oder warst du es wirklich?"),
    (65.98, 67.36, 10, "Schreib es in die Kommentare."),
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
