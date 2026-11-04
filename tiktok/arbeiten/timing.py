"""Phrase timings for 'Geh einfach arbeiten' (ElevenLabs take, 63.6 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.07
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.3, 0.45

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 2.37, 0, "Der Bruder schreibt unter das letzte Video:"),
    (2.82, 4.29, 0, "Geh einfach arbeiten."),
    (4.91, 5.43, 0, "Okay."),
    (5.85, 7.34, 0, "Lass uns das mal durchrechnen."),
    (7.85, 9.16, 1, "Du fängst einen Job an."),
    (9.52, 11.10, 1, "2.000 Euro netto."),
    (11.45, 12.40, 1, "Klingt erstmal gut."),
    (12.86, 13.37, 2, "Miete:"),
    (13.56, 14.35, 2, "900."),
    (14.65, 16.05, 2, "Auto: 300."),
    (16.41, 17.75, 2, "Essen: 400."),
    (18.17, 20.92, 2, "Handy, Strom, Versicherung: 200."),
    (21.27, 21.74, 3, "Übrig:"),
    (22.08, 23.20, 3, "200 Euro."),
    (23.74, 24.53, 3, "Im Monat."),
    (25.06, 25.60, 4, "Urlaub:"),
    (25.90, 27.27, 4, "30 Tage im Jahr."),
    (27.60, 29.56, 4, "Und die musst du dir auch noch erlauben lassen."),
    (29.99, 32.03, 5, "Chef, kann ich im August frei haben?"),
    (32.36, 32.83, 5, "Nein."),
    (33.09, 34.07, 5, "Da ist Hochsaison."),
    (34.54, 35.06, 6, "Stopp."),
    (35.47, 37.11, 6, "Du fragst um Erlaubnis –"),
    (37.43, 38.89, 6, "für dein eigenes Leben?"),
    (39.44, 43.43, 7, "Für eine eigene Wohnung brauchst du 80.000 Euro Eigenkapital."),
    (43.81, 47.04, 7, "Mit 200 im Monat sparst du 33 Jahre."),
    (47.37, 49.03, 8, "Dann bist du 55."),
    (49.35, 51.09, 8, "Und hast genau eins geschafft:"),
    (51.58, 52.35, 8, "durchgehalten."),
    (52.91, 54.79, 9, "Du klickst nochmal auf den Kommentar."),
    (55.23, 56.13, 9, "Auf das Profil."),
    (56.71, 57.71, 9, "Und erstarrst."),
    (58.27, 59.42, 9, "Es ist dein Chef."),
    (59.98, 60.55, 10, "Bleiben –"),
    (60.87, 61.61, 10, "oder kündigen?"),
    (62.12, 63.63, 10, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"Es ist dein Chef.": 0.2, "Nein.": 0.1}  # dramatic beats kept a bit longer

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
