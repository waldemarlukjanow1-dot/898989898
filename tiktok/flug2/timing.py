"""Phrase timings for 'Flug 404 Teil 2' (PLANNED timing – replaced when the voice arrives).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.0
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.32, 0.5

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 3.20, 0, "Du sitzt in einem fliegenden Flugzeug ohne Piloten."),
    (3.55, 5.95, 0, "Und hundertsiebenundachtzig Passagiere starren dich an."),
    (6.50, 8.10, 1, "Du hast dich entschieden:"),
    (8.45, 10.05, 1, "Du setzt dich hin."),
    (10.40, 11.60, 1, "Schließt die Augen."),
    (11.95, 14.75, 1, "Und tust so, als würdest du schlafen."),
    (15.30, 16.10, 2, "Langsam atmen."),
    (16.45, 17.25, 2, "Nicht bewegen."),
    (17.60, 18.40, 2, "Nicht blinzeln."),
    (18.95, 21.35, 3, "Dann hörst du Schritte im Gang."),
    (21.70, 22.90, 3, "Sie kommen näher."),
    (23.25, 26.05, 3, "Und bleiben direkt neben deinem Sitz stehen."),
    (26.60, 28.60, 4, "Jemand beugt sich über dich."),
    (28.95, 31.75, 4, "Du spürst seinen Atem an deinem Ohr."),
    (32.30, 33.50, 5, "Eine Stimme flüstert:"),
    (33.85, 35.05, 5, "Er schläft nicht."),
    (35.60, 36.10, 6, "Stopp."),
    (36.45, 38.05, 6, "Woher wissen sie das?"),
    (38.60, 40.20, 7, "Die Schritte gehen weiter."),
    (40.55, 42.15, 7, "Du öffnest ein Auge."),
    (42.50, 43.70, 7, "Nur einen Spalt."),
    (44.25, 47.45, 8, "Der Platz neben dir ist nicht mehr leer."),
    (47.80, 49.00, 8, "Dort sitzt jemand."),
    (49.35, 50.95, 8, "In deinem grünen Pullover."),
    (51.30, 52.50, 8, "Mit deinem Gesicht."),
    (53.05, 55.45, 9, "Er lächelt dich an und sagt:"),
    (55.80, 57.40, 9, "Ich übernehme ab hier."),
    (57.95, 59.55, 10, "Dann ruckelt das Flugzeug."),
    (59.90, 62.30, 10, "Und es geht steil nach unten."),
    (62.85, 66.45, 11, "Bleibst du sitzen – oder rennst du ins Cockpit?"),
    (66.80, 68.80, 11, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {}  # dramatic beats kept a bit longer

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
