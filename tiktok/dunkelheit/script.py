"""'TAG 1 DER DUNKELHEIT' – STIL 3, Du-Form. Text = so wie in der ElevenLabs-Aufnahme. chip = (text, kind)."""

TITLE = "TAG 1 DER DUNKELHEIT"
DURATION = 64.0

SEQ = [
    dict(name="06:30", vo="Du wachst auf. Es ist 6:30 Uhr. Aber draußen ist es stockdunkel.", hi=["6:30", "stockdunkel."],
         chip=("06:30 UHR", "white"), visual="Dunkles Zimmer, Wecker leuchtet 06:30, du setzt dich auf."),
    dict(name="Keine Sonne", vo="Keine Sonne. Kein Morgenlicht. Nur Dunkelheit.", hi=["Sonne.", "Dunkelheit."],
         chip=("KEINE SONNE", "red"), visual="Du am Fenster: die Stadt komplett schwarz, kein Licht am Himmel."),
    dict(name="Nachrichten", vo="Du schaltest den Fernseher ein. Die Nachrichtensprecherin zittert: Die Sonne ist heute nicht aufgegangen. Wir wissen nicht, warum.",
         hi=["Sonne", "warum."], chip=("EILMELDUNG", "red"), visual="Fernseher: Sprecherin mit Eilmeldung „SONNE NICHT AUFGEGANGEN“."),
    dict(name="Strom aus", vo="Dann fällt der Strom aus.", hi=["Strom"], chip=("STROMAUSFALL", "red"),
         visual="Fernseher geht aus, alles schwarz – nur dein Handy leuchtet dein Gesicht an."),
    dict(name="Akku", vo="Dein Handy: 12 Prozent Akku. Eine Nachricht von deinem besten Freund: Geh auf keinen Fall raus.",
         hi=["12", "raus."], chip=("AKKU: 12 %", "red"), visual="Chat mit „Bester Freund“: „Geh auf keinen Fall raus.“"),
    dict(name="Gesehen", vo="Du fragst: Warum? Er schreibt: Weil ich dich gerade gesehen habe. Draußen. Vor deiner Tür.",
         hi=["dich", "Tür."], chip=("AKKU: 9 %", "red"), visual="Chat: „Warum?“ – „Weil ich dich gerade gesehen habe. Draußen. Vor deiner Tür.“"),
    dict(name="PAUSE", vo="Stopp. Du bist doch gerade erst aufgewacht.", hi=["aufgewacht."], chip=("", "white"),
         visual="Kurzer Freeze: du mit dem Handy, Pausen-Symbol."),
    dict(name="Drei Schläge", vo="In diesem Moment: drei laute Schläge an deiner Haustür. Du schaust durch den Türspion. Niemand da.",
         hi=["drei", "Niemand"], chip=("3 SCHLÄGE", "red"), visual="Die Haustür bebt dreimal (BUMM). Blick durch den Türspion: leerer, dunkler Flur."),
    dict(name="Anruf", vo="Dein Handy klingelt. Unbekannte Nummer. Eine verzerrte Stimme flüstert: Mach die Tür nicht auf. Egal, was du hörst.",
         hi=["Unbekannte", "nicht", "auf."], chip=("UNBEKANNTE NUMMER", "white"), visual="Eingehender Anruf: Unbekannt. Du hältst das Handy ans Ohr."),
    dict(name="Deine Stimme", vo="Dann hörst du sie. Deine eigene Stimme. Direkt vor der Tür: Bitte. Lass mich rein.",
         hi=["eigene", "Stimme.", "rein."], chip=("DEINE STIMME?!", "red"),
         visual="Die Tür von innen. Unter dem Türspalt: zwei weiße Schuhe – genau wie deine. Sprechblase: „Bitte. Lass mich rein.“"),
    dict(name="Cliffhanger", vo="Würdest du die Tür aufmachen? Schreib es in die Kommentare.", hi=["Tür", "aufmachen?"],
         chip=("TAG 1 DER DUNKELHEIT", "white"), visual="Du mit dem Rücken an der Tür, Handy-Licht. Buttons: AUFMACHEN / ZULASSEN."),
]

CAPTION_TEXT = ("06:30 Uhr – und die Sonne ist nicht aufgegangen. 🌑😨 Würdest du die Tür aufmachen? 👇 "
                "#dunkelheit #horror #mystery #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")

_t = 0.0
for _s in SEQ:
    _d = max(2.5, len(_s["vo"].split()) / 2.4)
    _s["start"], _s["end"] = round(_t, 1), round(_t + _d, 1)
    _s["clue"] = "—"
    _t += _d
