"""'REICH IN 30 TAGEN' – STIL 3, Du-Form. chip = (text, kind) shown at the top."""

TITLE = "REICH IN 30 TAGEN"
DURATION = 62.0

SEQ = [
    dict(name="Pleite", vo="Du bist zweiundzwanzig. Kontostand: dreiundvierzig Euro. Und du hast nur noch ein Ziel: reich werden. Egal wie.",
         hi=["dreiundvierzig", "reich"], chip=("KONTO: 43 €", "red"),
         visual="Dein Zimmer bei Nacht, du mit Handy, leerer Geldbeutel. Kamera zoomt langsam auf dich.", clue="—"),
    dict(name="Krypto", vo="Versuch eins: Krypto. Du setzt alles auf eine Münze, von der du noch nie gehört hast. Zwei Tage später: null.",
         hi=["Krypto.", "null."], chip=("VERSUCH 1: KRYPTO", "white"),
         visual="Großer Monitor: Kurs steigt kurz und stürzt ab. Dein Gesicht: erst Freude, dann Schock.", clue="—"),
    dict(name="Dropshipping", vo="Versuch zwei: Dropshipping. Hundert Bestellungen. Hundert Rücksendungen.",
         hi=["Rücksendungen."], chip=("100 RÜCKSENDUNGEN", "red"),
         visual="Pakete stapeln sich um dich, rote Stempel RETOURE fallen drauf.", clue="—"),
    dict(name="Der Guru", vo='Versuch drei: ein Guru auf TikTok. Reich in dreißig Tagen. Der Kurs kostet neunhundertsiebenundneunzig Euro. Dein letztes Geld.',
         hi=['Guru', 'letztes'], chip=('KURS: 997 €', 'green'),
         visual='Dein Handy groß: Guru mit Sonnenbrille vor Sportwagen. Dann fliegen deine letzten Scheine ins Handy.', clue="—"),
    dict(name="PAUSE", vo='Stopp. Dein letztes Geld?',
         hi=['letztes'], chip=('KONTO: 0 €', 'red'),
         visual='Kurzer Freeze, du schaust verlegen zur Seite.', clue="—"),
    dict(name="Die Lektion", vo="Der Kurs hat nur eine einzige Lektion: Verkauf diesen Kurs weiter.",
         hi=["Verkauf", "weiter."], chip=("LEKTION 1 VON 1", "white"),
         visual="Laptop-Bildschirm mit nur einem Kapitel: VERKAUF DIESEN KURS WEITER.", clue="—"),
    dict(name="Neuer Guru", vo="Also tust du es. Du wirst selbst zum Guru. Sportwagen gemietet. Uhr geliehen. Video gedreht.",
         hi=["Guru."], chip=("SPORTWAGEN: GEMIETET", "yellow"),
         visual="Du mit Sonnenbrille und Goldkette vor einem Sportwagen, Handy auf Stativ.", clue="—"),
    dict(name="Reich", vo='Und es funktioniert. Tausend Käufer. Dann zehntausend. Fast zehn Millionen Euro.',
         hi=['zehntausend.', 'Millionen'], chip=('9.970.000 €', 'green'),
         visual='Wie im Vorbild: Geldberge, fallende Scheine, du strahlst.', clue="—"),
    dict(name="Die Wallet", vo='Du willst auf Nummer sicher gehen. Du packst alles in eine Krypto-Wallet. Mit einem Passwort, das nur du kennst.',
         hi=['Krypto-Wallet.', 'Passwort,'], chip=('WALLET: 9.970.000 €', 'green'),
         visual='Handy groß: Wallet-App, das Geld fliegt hinein, Passwort-Feld mit Punkten.', clue="—"),
    dict(name="Passwort falsch", vo='Am nächsten Morgen: Passwort falsch. Noch zwei Versuche. Noch einer. Gesperrt. Für immer.',
         hi=['falsch.', 'Gesperrt.'], chip=('PASSWORT FALSCH', 'red'),
         visual='Handy: rotes PASSWORT FALSCH, Versuche zählen 3 → 2 → 1 → 0, dann Schloss: GESPERRT.', clue="—"),
    dict(name="Cliffhanger", vo='Zehn Millionen. Direkt vor dir. Und du kommst nie wieder ran. So viel Arbeit – für nichts. Was würdest du jetzt tun? Schreib es in die Kommentare.',
         hi=['nie', 'nichts.', 'tun?'], chip=('ZUGRIFF GESPERRT', 'red'),
         visual='Geldberg hinter einem riesigen Schloss, du sitzt davor. Buttons: WEITER RATEN / NEU ANFANGEN.', clue="—"),
]

CAPTION_TEXT = ("10 Millionen verdient … und dann das Passwort vergessen. 😭🔒 Was würdest du jetzt tun? 👇 "
                "#reichwerden #krypto #passwort #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")

if __name__ == "__main__":
    print(sum(len(s["vo"].split()) for s in SEQ), "Wörter")

# planned timing (until the voice arrives): ~2.4 words per second
_t = 0.0
for _s in SEQ:
    _d = max(2.5, len(_s["vo"].split()) / 2.4)
    _s["start"], _s["end"] = round(_t, 1), round(_t + _d, 1)
    _t += _d
