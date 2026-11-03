"""Phrase timings for 'Patient Null' (ElevenLabs take, 78.9 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.20
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.18, 0.36

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 1.02, 0, "Du wachst auf."),
    (1.55, 3.91, 0, "Dreiundsechzig verpasste Anrufe."),
    (4.42, 6.06, 0, "Draußen heulen Sirenen."),
    (6.52, 8.85, 0, "Die Zombie-Apokalypse ist ausgebrochen."),
    (9.27, 11.14, 0, "Und du hast sie verschlafen."),
    (11.83, 13.01, 1, "Die Straße ist leer."),
    (13.40, 15.22, 1, "Autos stehen kreuz und quer."),
    (15.73, 16.54, 1, "Kein Mensch."),
    (16.97, 17.78, 1, "Du bist allein."),
    (18.43, 20.67, 2, "Im Autoradio eine letzte Durchsage:"),
    (21.18, 23.03, 2, "Alle Überlebenden zum Stadion."),
    (23.34, 25.33, 2, "Letzter Hubschrauber um zwölf Uhr."),
    (25.93, 27.46, 3, "Es ist elf Uhr zwanzig."),
    (27.89, 28.77, 3, "Du rennst los."),
    (29.14, 31.75, 4, "An der Kreuzung: die ersten Zombies."),
    (32.15, 32.61, 4, "Zehn."),
    (32.98, 33.70, 4, "Zwanzig."),
    (34.14, 35.48, 4, "Sie drehen sich zu dir um."),
    (36.00, 36.79, 5, "Du erstarrst."),
    (37.26, 38.24, 5, "Sie kommen näher."),
    (38.71, 41.57, 5, "Und dann laufen sie einfach an dir vorbei."),
    (42.17, 42.58, 6, "Stopp."),
    (43.10, 44.75, 6, "Warum greifen sie dich nicht an?"),
    (45.39, 46.86, 7, "Elf Uhr neunundfünfzig."),
    (47.25, 47.99, 7, "Das Stadion."),
    (48.47, 50.35, 7, "Ein Soldat richtet die Waffe auf dich:"),
    (50.63, 51.45, 7, "Stehen bleiben!"),
    (51.92, 53.25, 8, "Er scannt dein Gesicht."),
    (53.75, 55.10, 8, "Dann wird er blass."),
    (55.57, 56.50, 8, "Auf seinem Tablet:"),
    (56.93, 57.73, 8, "dein Foto."),
    (58.17, 58.76, 8, "Darunter:"),
    (59.20, 60.29, 8, "Patient Null."),
    (60.74, 62.43, 9, "Die dreiundsechzig Anrufe."),
    (62.94, 63.63, 9, "Das Labor."),
    (64.14, 65.42, 9, "Du warst der Erste."),
    (65.77, 67.32, 9, "Deshalb greifen sie dich nicht an."),
    (67.76, 70.03, 9, "Für sie bist du einer von ihnen."),
    (70.53, 71.99, 10, "Der Soldat senkt die Waffe."),
    (72.46, 73.07, 10, "Steig ein."),
    (73.70, 74.86, 10, "Du kommst ins Labor."),
    (75.34, 76.95, 10, "Mitfliegen oder fliehen?"),
    (77.38, 78.71, 10, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"Patient Null.": 0.45, "Stehen bleiben!": 0.1}  # dramatic beats kept a bit longer

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
