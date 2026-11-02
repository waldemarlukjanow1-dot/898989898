"""Story, timing and on-screen data for 'DER ZEUGE' (~62 s).

Dark style (see CLAUDE.md). hud = (glaubwuerdigkeit %, verhoer_minute "mm:ss", puls bpm).
`clue` = hidden detail in the background for rewatchers.
"""

TITLE = "DER ZEUGE"
DURATION = 62.0

SEQ = [
    dict(start=0.0, end=5.5, name="Hook",
         vo="Du hast einen Mord gesehen. Jetzt sitzt du im Verhörraum. Und die Polizei glaubt dir nicht.",
         hi=["Mord", "glaubt", "nicht."],
         visual="Harter Schnitt: Mündungsblitz (1 Frame) → schwarzer Raum, eine schwingende Lampe, du am Tisch, dahinter der Spiegel.",
         clue="Im Spiegel ist eine zweite Lampe zu sehen – auf der anderen Seite brennt Licht.",
         hud=(50, "47:00", 92)),
    dict(start=5.5, end=10.0, name="Der Kommissar",
         vo="Der Kommissar setzt sich. Erzähl es nochmal. Von Anfang an.",
         hi=["nochmal."],
         visual="Kommissar als Silhouette gegenüber, nur seine Hände im Lichtkegel. Aufnahmegerät, rotes REC-Licht.",
         clue="Er trägt einen Ohrstöpsel – sehr klein, fast unsichtbar.",
         hud=(50, "48:10", 96)),
    dict(start=10.0, end=16.0, name="Rückblende 1",
         vo="Gestern Nacht. Parkhaus, Ebene drei. Ein Mann im grauen Mantel. Ein Schuss.",
         hi=["grauen", "Mantel.", "Schuss."],
         visual="Glitch-Rückblende: Parkhaus, Neonröhren, Mann im GRAUEN Mantel von hinten, Mündungsblitz, Körper fällt.",
         clue="Auf dem Boden liegt ein Ring. Merk ihn dir.",
         hud=(50, "49:30", 110)),
    dict(start=16.0, end=22.0, name="Handschuhe",
         vo="Der Kommissar nickt. Und er trug schwarze Handschuhe, richtig? Du hast nie Handschuhe erwähnt.",
         hi=["Handschuhe,", "nie"],
         visual="Nahaufnahme: sein Stift stoppt. Du starrst ihn an. Lampe hört auf zu schwingen.",
         clue="In seiner Akte steckt schon ein Foto vom Tatort – mit Uhrzeit VOR dem Notruf.",
         hud=(45, "51:05", 118)),
    dict(start=22.0, end=27.5, name="Der Blick",
         vo="Er schaut zum Spiegel. Nur kurz. Dann sagt er: Du lügst.",
         hi=["Spiegel.", "lügst."],
         visual="Zeitlupe: sein Kopf dreht sich zum Spiegel. Harter Schnitt zurück: „Du lügst.“",
         clue="—",
         hud=(20, "52:40", 124)),
    dict(start=27.5, end=33.5, name="Rückblende 2",
         vo="Du schließt die Augen. Ebene drei. Der Mantel ist jetzt schwarz. Und der Mann dreht sich um.",
         hi=["schwarz.", "dreht"],
         visual="Gleiche Rückblende – aber verändert: Mantel SCHWARZ, Handschuhe. Er dreht den Kopf … Bild reißt ab.",
         clue="Der Ring auf dem Boden ist verschwunden.",
         hud=(20, "54:00", 138)),
    dict(start=33.5, end=37.0, name="PAUSE",
         vo="Stopp. Gestern war der Mantel grau. Oder?",
         hi=["grau.", "Oder?"],
         visual="VHS-PAUSE auf dem halb umgedrehten Mann. Totale Stille. Beide Mäntel nebeneinander (grau / schwarz).",
         clue="—",
         hud=(20, "54:00", 138)),
    dict(start=37.0, end=43.0, name="Der Knopf im Ohr",
         vo="Dann siehst du es. Ein Knopf im Ohr des Kommissars. Er hört nicht dir zu.",
         hi=["Knopf", "Ohr"],
         visual="Extreme Nahaufnahme Ohr, kleines rotes Licht blinkt im Takt einer fremden Stimme.",
         clue="Er nickt, obwohl niemand im Raum spricht.",
         hud=(10, "55:20", 142)),
    dict(start=43.0, end=49.0, name="Der Spiegel",
         vo="Der Spiegel beschlägt. Jemand atmet dagegen. Von der anderen Seite.",
         hi=["atmet", "anderen", "Seite."],
         visual="Spiegel in Großaufnahme, ein Atemfleck wächst von innen. Herzschlag-Bass.",
         clue="Im Atemfleck erkennt man kurz den Abdruck eines Rings.",
         hud=(5, "56:45", 150)),
    dict(start=49.0, end=55.0, name="Das Geständnis",
         vo="Der Kommissar schiebt dir ein Blatt hin. Ein Geständnis. Mit deinem Namen.",
         hi=["Geständnis.", "deinem", "Namen."],
         visual="Blatt im Lichtkegel, Stift daneben. Unterschrift-Linie leuchtet rot. GLAUBWÜRDIGKEIT 0 %.",
         clue="Die Handschrift auf dem Blatt ist DEINE.",
         hud=(0, "58:10", 160)),
    dict(start=55.0, end=62.0, name="Cliffhanger",
         vo="Das Licht flackert. Für eine Sekunde siehst du durch den Spiegel. Grauer Mantel. Er lächelt. Unterschreiben oder schweigen?",
         hi=["Grauer", "Mantel.", "lächelt."],
         visual="Lampe flackert aus – der Spiegel wird durchsichtig: Mann im grauen Mantel, Ring, Lächeln. Schwarz. Buttons: UNTERSCHREIBEN / SCHWEIGEN.",
         clue="Er trägt den Ring aus der ersten Rückblende.",
         hud=(0, "59:59", 170)),
]

CAPTION_TEXT = ("Du hast einen Mord gesehen – aber wer sitzt hinter dem Spiegel? 👁️ Unterschreiben oder schweigen? 👇 "
                "#krimi #verhör #mord #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")

if __name__ == "__main__":
    print(sum(len(s["vo"].split()) for s in SEQ), "Wörter")
