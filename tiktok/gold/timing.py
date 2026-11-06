"""Phrase timings for 'Lager 17' (ElevenLabs take, 73.2 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.17
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.22, 0.4

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 3.52, 0, "Für 50 Euro ersteigerst du einen alten Lagerraum."),
    (4.01, 4.45, 0, "Drinnen:"),
    (4.79, 7.53, 0, "Staub, Kartons, ein kaputtes Fahrrad."),
    (8.04, 9.01, 1, "Und ganz hinten:"),
    (9.44, 10.28, 1, "ein Tresor."),
    (10.79, 11.41, 1, "Verschlossen."),
    (11.77, 13.01, 1, "Zu schwer zum Tragen."),
    (13.51, 15.87, 2, "Drei Tage brauchst du, um ihn aufzubekommen."),
    (16.39, 17.35, 2, "Dann siehst du es:"),
    (17.92, 18.37, 2, "Gold."),
    (18.75, 22.41, 2, "24 Barren. Über 2 Millionen Euro."),
    (22.91, 23.63, 3, "Du lachst."),
    (24.05, 25.79, 3, "Dann hörst du auf zu lachen."),
    (26.21, 27.54, 3, "Denn jetzt kommt die Frage:"),
    (28.07, 29.07, 3, "Was machst du damit?"),
    (29.60, 30.20, 4, "Verkaufen?"),
    (30.72, 32.38, 4, "Der Händler will deinen Ausweis."),
    (32.59, 34.43, 4, "Und wissen, woher das Gold kommt."),
    (34.97, 35.72, 4, "Was sagst du ihm?"),
    (36.23, 36.79, 5, "Verstecken?"),
    (37.24, 39.94, 5, "Unter deinem Bett liegen jetzt 2 Millionen."),
    (40.33, 41.95, 5, "Du schläfst keine Minute mehr."),
    (42.50, 43.09, 6, "Behalten?"),
    (43.52, 45.04, 6, "Dann ruft der Auktionator an:"),
    (45.44, 46.34, 6, "Ein Mann war hier."),
    (46.59, 48.83, 6, "Er will wissen, wer Lager 17 gekauft hat."),
    (49.33, 49.70, 7, "Stopp."),
    (50.16, 52.56, 7, "Wer sucht nach einem vergessenen Lagerraum?"),
    (53.15, 54.69, 8, "Du gehst zurück zum Tresor."),
    (55.19, 57.43, 8, "Ganz unten, unter dem letzten Barren:"),
    (57.83, 58.39, 8, "ein Zettel."),
    (58.88, 59.59, 9, "Darauf steht:"),
    (60.03, 63.76, 9, "Wer das findet, hat 24 Stunden, um es zurückzubringen."),
    (64.39, 66.68, 10, "Vor deinem Haus parkt ein schwarzes Auto."),
    (67.08, 68.23, 10, "Seit einer Stunde."),
    (68.75, 69.45, 10, "Verkaufen,"),
    (69.64, 70.31, 10, "verstecken"),
    (70.57, 71.28, 10, "oder behalten?"),
    (71.73, 73.03, 10, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"Gold.": 0.15, "Seit einer Stunde.": 0.2}  # dramatic beats kept a bit longer

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
