"""'FLUG 404' – STIL 3, Du-Form. Texte = Aufnahme. hi = gelbe Schlagwörter je Szene."""
TITLE = "FLUG 404"
DURATION = 63.0
SEQ = [
    dict(name="Boarding", vo="Du steigst in einen Flug von Frankfurt nach New York. Neun Stunden Flug. Fensterplatz.", hi=["Frankfurt", "New", "York.", "Fensterplatz."],
         chip=("FLUG 404 · FRA → JFK", "white"), visual="Du im Fensterplatz, Wolken ziehen vorbei, du freust dich und schaust raus."),
    dict(name="Stille", vo="Nach zwei Stunden fällt dir etwas auf: Das Flugzeug ist komplett still. Kein Babygeschrei. Kein Husten. Nichts.",
         hi=["still.", "Nichts."], chip=("STILLE", "white"), visual="Kabine, du schaust dich unruhig um, Einblendungen BABY: 0 dB / HUSTEN: – / NICHTS."),
    dict(name="Alle schlafen", vo="Alle Passagiere schlafen. Gleichzeitig. Auch die Stewardess. Mitten im Gang.", hi=["schlafen.", "Gleichzeitig.", "Stewardess."],
         chip=("ALLE SCHLAFEN", "red"), visual="Alle mit geschlossenen Augen, Zzz – die Stewardess schläft stehend im Gang."),
    dict(name="Rufknopf", vo="Du drückst den Rufknopf. Niemand kommt.", hi=["Rufknopf.", "Niemand"],
         chip=("RUFKNOPF", "white"), visual="Finger drückt den Knopf, er leuchtet orange – dann wieder die schlafende Kabine."),
    dict(name="Bildschirm", vo="Auf dem Bildschirm vor dir: Ankunft in New York – vor drei Tagen.", hi=["drei", "Tagen."],
         chip=("ANKUNFT: VOR 3 TAGEN", "red"), visual="Sitzbildschirm mit Flugkarte FRA → JFK, unten rot: VOR 3 TAGEN. Du geschockt."),
    dict(name="PAUSE", vo="Stopp. Wie kann ein Flug schon angekommen sein, in dem du gerade sitzt?", hi=["angekommen"],
         chip=("", "white"), visual="Freeze mit Pausen-Symbol, du fasst dir an den Kopf."),
    dict(name="Cockpit", vo="Du gehst nach vorne zum Cockpit. Die Tür ist offen. Beide Sitze leer. Der Autopilot fliegt.", hi=["Cockpit.", "leer.", "Autopilot"],
         chip=("COCKPIT: LEER", "red"), visual="Du gehst durch den Gang nach vorne – Cockpittür öffnet sich – zwei leere Sitze, AUTOPILOT leuchtet."),
    dict(name="Durchsage", vo="Dann knackt der Lautsprecher. Eine ruhige Stimme: Bitte bleiben Sie sitzen. Sie sind der einzige Passagier, der aufgewacht ist.",
         hi=["Lautsprecher.", "einzige"], chip=("PASSAGIERE WACH: 1", "red"), visual="Lautsprecher in der Decke mit Schallwellen, Textblase mit der Durchsage, du erschrickst."),
    dict(name="Alle schauen", vo="Du drehst dich um. Alle Passagiere haben die Augen offen. Und schauen dich an.", hi=["Augen", "offen.", "dich"],
         chip=("PASSAGIERE WACH: 187", "red"), visual="Du drehst dich um – Gegenschnitt: die ganze Kabine starrt dich mit weit offenen Augen an, langsamer Zoom."),
    dict(name="Cliffhanger", vo="Weckst du die anderen – oder setzt du dich wieder hin und tust so, als würdest du schlafen? Schreib es in die Kommentare.",
         hi=["Weckst", "schlafen?"], chip=("FLUG 404", "white"), visual="Du im Sitz, geschockt. Buttons: WECKEN / SCHLAFEN STELLEN."),
]
CAPTION_TEXT = ("9 Stunden Flug – und plötzlich schlafen alle. Gleichzeitig. ✈️😨 Weckst du sie oder stellst du dich schlafend? 👇 "
                "#flugzeug #mystery #horror #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")
from timing import seq_bounds as _sb  # noqa: E402
for _s, (_a, _b) in zip(SEQ, _sb()[0]):
    _s["start"], _s["end"], _s["clue"] = round(_a, 1), round(_b, 1), "—"
