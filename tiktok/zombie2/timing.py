"""Phrase timings for 'Patient Null – Teil 2' (ElevenLabs take, 64.9 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.06
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.25, 0.4

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 1.60, 0, "Du bist Patient Null."),
    (2.11, 3.79, 0, "Die Zombies greifen dich nicht an."),
    (4.28, 6.84, 0, "Und du hast dich gerade für die Flucht entschieden."),
    (7.24, 9.11, 1, "Hinter dir startet der Hubschrauber."),
    (9.44, 10.19, 1, "Er folgt dir."),
    (10.59, 12.31, 1, "Du rennst mitten in die Horde."),
    (12.67, 14.38, 2, "Und die Zombies machen dir Platz."),
    (14.79, 17.18, 2, "Wie eine Mauer schließen sie sich hinter dir."),
    (17.59, 20.76, 3, "Du versteckst dich im einzigen Ort, an dem dich keiner sucht."),
    (21.17, 21.96, 3, "Deinem Labor."),
    (22.49, 23.55, 4, "Auf deinem Schreibtisch:"),
    (23.91, 24.57, 4, "dein Laptop."),
    (25.03, 25.63, 4, "Ein Video."),
    (26.07, 27.23, 4, "Aufgenommen gestern."),
    (27.60, 28.13, 4, "Von dir."),
    (28.59, 29.72, 5, "Du drückst auf Play."),
    (30.19, 32.30, 5, "Wenn du das siehst, hat es funktioniert."),
    (32.72, 34.31, 5, "Ich habe es mir selbst gespritzt."),
    (34.70, 35.41, 5, "Absichtlich."),
    (35.84, 36.32, 6, "Stopp."),
    (36.73, 38.87, 6, "Du hast dich absichtlich infiziert?"),
    (39.32, 40.63, 7, "Das Video läuft weiter."),
    (41.03, 42.28, 7, "Ich bin nicht der Anfang."),
    (42.68, 43.93, 7, "Ich bin das Gegenmittel."),
    (44.33, 45.54, 7, "Es ist in meinem Blut."),
    (46.03, 48.24, 8, "Die Zombies vor dem Fenster drehen sich um."),
    (48.65, 50.88, 8, "Zum ersten Mal schauen sie dich an."),
    (51.36, 53.21, 9, "Auf dem Monitor blinkt eine Warnung:"),
    (53.58, 55.01, 9, "Immunität lässt nach."),
    (55.35, 56.83, 9, "Noch vierundzwanzig Stunden."),
    (57.45, 59.29, 10, "Dein Blut kann die Welt retten."),
    (59.69, 63.06, 10, "Zurück zum Soldaten oder das Gegenmittel allein herstellen?"),
    (63.44, 64.73, 10, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"Absichtlich.": 0.2, "Ich bin das Gegenmittel.": 0.2}  # dramatic beats kept a bit longer

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
