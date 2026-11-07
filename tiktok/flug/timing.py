"""Phrase timings for 'Flug 404' (ElevenLabs take, 63.3 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.05
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.32, 0.5

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 3.16, 0, "Du steigst in einen Flug von Frankfurt nach New York."),
    (3.53, 4.75, 0, "Neun Stunden Flug."),
    (5.14, 5.96, 0, "Fensterplatz."),
    (6.59, 8.71, 1, "Nach zwei Stunden fällt dir etwas auf:"),
    (9.22, 11.31, 1, "Das Flugzeug ist komplett still."),
    (11.85, 12.92, 1, "Kein Babygeschrei."),
    (13.28, 14.03, 1, "Kein Husten."),
    (14.42, 14.95, 1, "Nichts."),
    (15.50, 17.04, 2, "Alle Passagiere schlafen."),
    (17.49, 18.27, 2, "Gleichzeitig."),
    (18.77, 19.85, 2, "Auch die Stewardess."),
    (20.19, 20.98, 2, "Mitten im Gang."),
    (21.59, 22.89, 3, "Du drückst den Rufknopf."),
    (23.42, 24.14, 3, "Niemand kommt."),
    (24.67, 26.09, 4, "Auf dem Bildschirm vor dir:"),
    (26.49, 27.84, 4, "Ankunft in New York –"),
    (28.16, 29.16, 4, "vor drei Tagen."),
    (29.73, 30.13, 5, "Stopp."),
    (30.68, 34.30, 5, "Wie kann ein Flug schon angekommen sein, in dem du gerade sitzt?"),
    (34.88, 36.59, 6, "Du gehst nach vorne zum Cockpit."),
    (37.07, 37.96, 6, "Die Tür ist offen."),
    (38.44, 39.55, 6, "Beide Sitze leer."),
    (39.97, 41.22, 6, "Der Autopilot fliegt."),
    (41.81, 43.34, 7, "Dann knackt der Lautsprecher."),
    (43.84, 44.88, 7, "Eine ruhige Stimme:"),
    (45.42, 46.83, 7, "Bitte bleiben Sie sitzen."),
    (47.44, 50.22, 7, "Sie sind der einzige Passagier, der aufgewacht ist."),
    (50.78, 51.62, 8, "Du drehst dich um."),
    (52.14, 54.27, 8, "Alle Passagiere haben die Augen offen."),
    (54.71, 55.79, 8, "Und schauen dich an."),
    (56.40, 57.62, 9, "Weckst du die anderen –"),
    (57.87, 61.23, 9, "oder setzt du dich wieder hin und tust so, als würdest du schlafen?"),
    (61.74, 63.11, 9, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"vor drei Tagen.": 0.2, "Und schauen dich an.": 0.4}  # dramatic beats kept a bit longer

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
