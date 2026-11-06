"""'LAGER 17' – Gold gefunden. STIL 3, Du-Form, neue Hauptfigur (T.HERO). chip = (text, kind)."""

TITLE = "LAGER 17"
DURATION = 62.0

SEQ = [
    dict(name="Die Auktion", vo="Für fünfzig Euro ersteigerst du einen alten Lagerraum. Drinnen: Staub, Kartons, ein kaputtes Fahrrad.",
         hi=["50", "Lagerraum."], chip=("GEBOT: 50 €", "white"),
         visual="Lagerhalle mit Rolltor „LAGER 17“, Auktionator mit Hammer. Du hebst die Hand – zugeschlagen."),
    dict(name="Der Tresor", vo="Und ganz hinten: ein Tresor. Verschlossen. Zu schwer zum Tragen.",
         hi=["Tresor."], chip=("LAGER 17", "white"),
         visual="Im staubigen Lagerraum fällt ein Lichtkegel auf einen alten, schweren Tresor."),
    dict(name="Gold", vo="Drei Tage brauchst du, um ihn aufzubekommen. Dann siehst du es: Gold. Vierundzwanzig Barren. Über zwei Millionen Euro.",
         hi=["Gold.", "2", "Millionen"], chip=("24 BARREN GOLD", "green"),
         visual="TAG 1, 2, 3 – du am Tresor. Die Tür schwingt auf, goldenes Licht, 24 Barren."),
    dict(name="Und jetzt?", vo="Du lachst. Dann hörst du auf zu lachen. Denn jetzt kommt die Frage: Was machst du damit?",
         hi=["lachst.", "damit?"], chip=("WERT: 2.000.000 €+", "green"),
         visual="Du lachst neben dem Goldstapel – dann friert dein Lachen ein."),
    dict(name="Verkaufen?", vo="Verkaufen? Der Händler will deinen Ausweis. Und wissen, woher das Gold kommt. Was sagst du ihm?",
         hi=["Verkaufen?", "Ausweis.", "woher"], chip=("VERKAUFEN?", "red"),
         visual="Laden „GOLDANKAUF“, Händler mit Lupe hinter dem Tresen, Formular: HERKUNFT: ____"),
    dict(name="Verstecken?", vo="Verstecken? Unter deinem Bett liegen jetzt zwei Millionen. Du schläfst keine Minute mehr.",
         hi=["Verstecken?", "keine", "Minute"], chip=("VERSTECKEN?", "red"),
         visual="Nachts: Goldschimmer unter deinem Bett, du liegst wach, Wecker 03:12."),
    dict(name="Behalten?", vo="Behalten? Dann ruft der Auktionator an: Ein Mann war hier. Er will wissen, wer Lager siebzehn gekauft hat.",
         hi=["Behalten?", "Mann", "17"], chip=("BEHALTEN?", "red"),
         visual="Eingehender Anruf: Auktionshaus. Sprechblase: „Ein Mann fragt nach Lager 17.“"),
    dict(name="PAUSE", vo="Stopp. Wer sucht nach einem vergessenen Lagerraum?",
         hi=["vergessenen"], chip=("", "white"),
         visual="Kurzer Freeze, Pausen-Symbol."),
    dict(name="Der Zettel", vo="Du gehst zurück zum Tresor. Ganz unten, unter dem letzten Barren: ein Zettel.",
         hi=["Zettel."], chip=("BARREN 24", "white"),
         visual="Du hebst den letzten Barren an – darunter ein gefalteter Zettel."),
    dict(name="24 Stunden", vo="Darauf steht: Wer das findet, hat vierundzwanzig Stunden, um es zurückzubringen.",
         hi=["24", "Stunden,"], chip=("24:00:00", "red"),
         visual="Zettel groß: „Wer das findet, hat 24 Stunden, um es zurückzubringen.“"),
    dict(name="Cliffhanger", vo="Vor deinem Haus parkt ein schwarzes Auto. Seit einer Stunde. Verkaufen, verstecken oder behalten? Schreib es in die Kommentare.",
         hi=["schwarzes", "Auto.", "Verkaufen,", "verstecken", "behalten?"], chip=("23:00:00", "red"),
         visual="Du am Fenster, unten ein schwarzes Auto mit laufendem Motor. Buttons: VERKAUFEN / VERSTECKEN / BEHALTEN."),
]

CAPTION_TEXT = ("Für 50 € einen Lagerraum gekauft – und 24 Barren Gold gefunden. 🥇😰 Verkaufen, verstecken oder behalten? 👇 "
                "#gold #lagerraum #storytime #duform #geschichte #plottwist #spannung #wasmachstdu #fürdich #fyp")

_t = 0.0
for _s in SEQ:
    _d = max(2.5, len(_s["vo"].split()) / 2.4)
    _s["start"], _s["end"] = round(_t, 1), round(_t + _d, 1)
    _s["clue"] = "—"
    _t += _d

if __name__ == "__main__":
    print(sum(len(s["vo"].split()) for s in SEQ), "Wörter")
