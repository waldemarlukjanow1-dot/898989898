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
    dict(name="Der Guru", vo="Versuch drei: ein Guru auf TikTok. Reich in dreißig Tagen. Der Kurs kostet neunhundertsiebenundneunzig Euro. Du leihst dir das Geld. Von deiner Mutter.",
         hi=["Guru", "Mutter."], chip=("KURS: 997 €", "green"),
         visual="Dein Handy groß: Guru mit Sonnenbrille vor Sportwagen. Dann: Mamas Hand gibt dir Geldscheine.", clue="—"),
    dict(name="PAUSE", vo="Stopp. Von deiner Mutter?", hi=["Mutter?"], chip=("GELIEHEN VON: MAMA", "red"),
         visual="Kurzer Freeze, du schaust verlegen zur Seite.", clue="—"),
    dict(name="Die Lektion", vo="Der Kurs hat nur eine einzige Lektion: Verkauf diesen Kurs weiter.",
         hi=["Verkauf", "weiter."], chip=("LEKTION 1 VON 1", "white"),
         visual="Laptop-Bildschirm mit nur einem Kapitel: VERKAUF DIESEN KURS WEITER.", clue="—"),
    dict(name="Neuer Guru", vo="Also tust du es. Du wirst selbst zum Guru. Sportwagen gemietet. Uhr geliehen. Video gedreht.",
         hi=["Guru."], chip=("SPORTWAGEN: GEMIETET", "yellow"),
         visual="Du mit Sonnenbrille und Goldkette vor einem Sportwagen, Handy auf Stativ.", clue="—"),
    dict(name="Reich", vo="Und es funktioniert. Tausend Käufer. Dann zehntausend. Du bist reich.",
         hi=["zehntausend.", "reich."], chip=("9.970.000 €", "green"),
         visual="Wie im Vorbild: Geldberge, fallende Scheine, du strahlst.", clue="Unter den Käufer-Benachrichtigungen blitzt kurz „Mama“ auf."),
    dict(name="Die Nachricht", vo="Eines Nachts eine Nachricht: Ich habe alles in deinen Kurs gesteckt. Jetzt habe ich nichts mehr.",
         hi=["alles", "nichts"], chip=("1 NEUE NACHRICHT", "white"),
         visual="Zimmer im Dunkeln, nur dein Handy leuchtet. Die Nachricht erscheint.", clue="—"),
    dict(name="Mama", vo="Du öffnest das Profil. Es ist deine Mutter.",
         hi=["Mutter."], chip=("ABSENDER: MAMA", "white"),
         visual="Handy groß: Profil MAMA mit Herz. Dein Gesicht: Träne.", clue="—"),
    dict(name="Cliffhanger", vo="Aufhören und alles zurückzahlen – oder weitermachen? Schreib es in die Kommentare.",
         hi=["zurückzahlen", "weitermachen?"], chip=("", "white"),
         visual="Du zwischen Geldbergen, Buttons: ZURÜCKZAHLEN / WEITERMACHEN.", clue="—"),
]

CAPTION_TEXT = ("Du wolltest nur reich werden … und dann kam diese Nachricht. 😳💸 Zurückzahlen oder weitermachen? 👇 "
                "#reichwerden #guru #geld #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")

if __name__ == "__main__":
    print(sum(len(s["vo"].split()) for s in SEQ), "Wörter")

# planned timing (until the voice arrives): ~2.4 words per second
_t = 0.0
for _s in SEQ:
    _d = max(2.5, len(_s["vo"].split()) / 2.4)
    _s["start"], _s["end"] = round(_t, 1), round(_t + _d, 1)
    _t += _d
