"""Phrase timings for 'Reich in 30 Tagen' (ElevenLabs take, 80.7 s).

The take is long, so pauses are tightened first (each phrase is cut out and re-placed with
short gaps), then the result is sped up by TEMPO. All public times are video times.
"""

TEMPO = 1.25
VOICE = "audio/voice_helmut.mp3"
PAD_IN, PAD_OUT = 0.06, 0.10
GAP_SAME, GAP_SCENE = 0.16, 0.34

# (start, end, sequence index, text) in the ORIGINAL recording
RAW = [
    (0.00, 1.73, 0, "Du bist zweiundzwanzig."),
    (2.10, 2.83, 0, "Kontostand:"),
    (3.04, 4.31, 0, "dreiundvierzig Euro."),
    (4.83, 6.48, 0, "Und du hast nur noch ein Ziel:"),
    (6.91, 7.75, 0, "reich werden."),
    (8.01, 8.98, 0, "Egal wie."),
    (9.52, 10.42, 1, "Versuch eins:"),
    (10.73, 11.24, 1, "Krypto."),
    (11.65, 15.21, 1, "Du setzt alles auf eine Münze, von der du noch nie gehört hast."),
    (15.62, 16.67, 1, "Zwei Tage später:"),
    (17.05, 17.43, 1, "null."),
    (17.95, 18.83, 2, "Versuch zwei:"),
    (19.10, 19.89, 2, "Dropshipping."),
    (20.32, 21.33, 2, "Hundert Bestellungen."),
    (21.74, 22.91, 2, "Hundert Rücksendungen."),
    (23.40, 24.29, 3, "Versuch drei:"),
    (24.59, 26.17, 3, "ein Guru auf TikTok."),
    (26.51, 28.24, 3, "Reich in dreißig Tagen."),
    (28.66, 31.27, 3, "Der Kurs kostet 997 Euro."),
    (31.58, 32.70, 3, "Dein letztes Geld."),
    (33.25, 33.71, 4, "Stopp."),
    (34.13, 35.37, 4, "Dein letztes Geld?"),
    (35.79, 37.88, 5, "Der Kurs hat nur eine einzige Lektion:"),
    (38.24, 39.99, 5, "Verkauf diesen Kurs weiter."),
    (40.43, 41.49, 6, "Also tust du es."),
    (41.89, 43.37, 6, "Du wirst selbst zum Guru."),
    (43.75, 45.04, 6, "Sportwagen gemietet."),
    (45.28, 46.05, 6, "Uhr geliehen."),
    (46.29, 47.28, 6, "Video gedreht."),
    (47.67, 48.94, 7, "Und es funktioniert."),
    (49.23, 50.22, 7, "Tausend Käufer."),
    (50.54, 51.85, 7, "Dann zehntausend."),
    (52.08, 54.14, 7, "Fast zehn Millionen Euro."),
    (54.59, 56.03, 8, "Du willst auf Nummer sicher gehen."),
    (56.29, 58.42, 8, "Du packst alles in eine Krypto-Wallet."),
    (58.68, 61.16, 8, "Mit einem Passwort, das nur du kennst."),
    (61.60, 62.54, 9, "Am nächsten Morgen:"),
    (62.93, 63.85, 9, "Passwort falsch."),
    (64.30, 65.43, 9, "Noch zwei Versuche."),
    (65.86, 66.49, 9, "Noch einer."),
    (66.96, 67.61, 9, "Gesperrt."),
    (68.00, 68.77, 9, "Für immer."),
    (69.22, 70.38, 10, "Zehn Millionen."),
    (70.69, 71.75, 10, "Direkt vor dir."),
    (72.04, 74.13, 10, "Und du kommst nie wieder ran."),
    (74.57, 75.79, 10, "So viel Arbeit –"),
    (76.12, 77.01, 10, "für nichts."),
    (77.51, 78.82, 10, "Was würdest du jetzt tun?"),
    (79.20, 80.46, 10, "Schreib es in die Kommentare."),
]
EXTRA_GAP = {"Gesperrt.": 0.2, "für nichts.": 0.2}  # dramatic beats kept a bit longer

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
