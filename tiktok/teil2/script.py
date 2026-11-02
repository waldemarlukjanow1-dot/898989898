"""Story, timing and on-screen data for 'DER UMSCHLAG – Teil 2: Rennen' (~62 s).

Darker style (see CLAUDE.md). hud = (beute, vertrauen_in_mira, hitze).
`clue` = hidden detail in the background for rewatchers.
"""

TITLE = "DER UMSCHLAG – Teil 2: Rennen"
DURATION = 62.0

SEQ = [
    dict(start=0.0, end=5.0, name="Hook",
         vo="Du rennst. Zwei Taschen. Zwölf Millionen. Und Mira direkt hinter dir.",
         hi=["rennst.", "Mira"],
         visual="Nasse Gasse, fast schwarz. Du rennst auf die Kamera zu, Blaulicht weit hinten. Wackelige Handkamera.",
         clue="In Miras Jackentasche leuchtet schon ihr Handy.",
         hud=(12600000, 90, 100)),
    dict(start=5.0, end=10.0, name="Zu leise",
         vo="Ihr biegt in eine Gasse. Die Sirenen werden leiser. Zu leise.",
         hi=["Zu", "leise."],
         visual="Enge Gasse, eine flackernde Laterne. Musik bricht weg – nur Regen und Atem.",
         clue="Am Ende der Gasse steht ein Polizeiauto. Licht aus. Es wartet.",
         hud=(12600000, 80, 70)),
    dict(start=10.0, end=15.0, name="Der Schlüssel",
         vo="Mira zieht dich in einen Hauseingang. Und schließt auf. Woher hat sie einen Schlüssel?",
         hi=["Schlüssel?"],
         visual="Detail-Insert: Hand, Schlüssel, Schloss. Rotes Licht über der Tür.",
         clue="Am Schlüsselbund hängt ein kleiner Stern – wie bei einer Marke.",
         hud=(12600000, 60, 55)),
    dict(start=15.0, end=21.0, name="Die Wand",
         vo="Drinnen: eine leere Wohnung. An der Wand der Plan der Bank. Und in der Mitte: dein Foto.",
         hi=["Plan", "dein", "Foto."],
         visual="Taschenlampen-Kegel wandert über eine Ermittlungswand mit roten Fäden. Langsamer Zoom auf dein Foto.",
         clue="Neben deinem Foto: ein Foto von Oskar – durchgestrichen.",
         hud=(12600000, 40, 40)),
    dict(start=21.0, end=26.0, name="Anruf",
         vo="Mira sagt: Ich kann das erklären. Dann leuchtet ihr Handy. Oskar ruft an.",
         hi=["Oskar"],
         visual="Mira als Silhouette, nur das Handy-Display beleuchtet ihr Gesicht von unten.",
         clue="Der Kontakt heißt nicht „Oskar“, sondern „Informant“ – kurz sichtbar.",
         hud=(12600000, 20, 40)),
    dict(start=26.0, end=30.0, name="PAUSE",
         vo="Stopp. Oskar hat dich verraten. Warum ruft er sie an?",
         hi=["verraten."],
         visual="VHS-PAUSE wie in Teil 1: Bild friert ein, RGB-Versatz, Timecode. Totale Stille.",
         clue="Im eingefrorenen Bild sieht man die Marke in Miras Jacke.",
         hud=(12600000, 20, 40)),
    dict(start=30.0, end=36.0, name="Flüstern",
         vo="Sie hebt ab und flüstert: Er hat den Umschlag gefunden. Alles läuft nach Plan.",
         hi=["nach", "Plan."],
         visual="Extreme Nahaufnahme: Miras Mund, Handy am Ohr. Herzschlag-Bass.",
         clue="—",
         hud=(12600000, 5, 40)),
    dict(start=36.0, end=42.0, name="Die Taschen",
         vo="Du reißt die Taschen auf. Kein Geld. Nur Zeitungspapier.",
         hi=["Zeitungspapier."],
         visual="Taschen aufgerissen, Zeitungen quellen raus. BEUTE stürzt auf €0.",
         clue="Schlagzeile: „BANKRAUB IN DER ZENTRALBANK“ – Datum von gestern.",
         hud=(0, 5, 40)),
    dict(start=42.0, end=48.0, name="Vier Taschen",
         vo="Vier Taschen waren im Tresor. Zwei sind mit Oskar gefahren. Mit dem echten Geld.",
         hi=["echten", "Geld."],
         visual="Rückblende im Glitch-Look: Tresor, vier Taschen, Rücklichter. Zwei Taschen leuchten gold.",
         clue="—",
         hud=(0, 5, 40)),
    dict(start=48.0, end=54.0, name="Die Marke",
         vo="Mira legt auf. Greift in ihre Jacke. Und legt eine Polizeimarke auf den Tisch.",
         hi=["Polizeimarke"],
         visual="Tisch, eine Lampe. Marke landet mit dumpfem Schlag. Draußen erste Blaulichter.",
         clue="Auf der Marke steht nicht „Mira“, sondern „O. Mirković“ (das „O.“ aus Teil 1!).",
         hud=(0, 0, 85)),
    dict(start=54.0, end=62.0, name="Der Köder",
         vo="Du warst nie Teil der Crew. Du warst der Köder. Mira oder Oskar: Wer lügt? Schreib's in die Kommentare. Und du? Du rennst.",
         hi=["Köder.", "lügt?", "rennst."],
         visual="Fenster offen, Blaulicht flutet den Raum. Du springst raus. Letztes Bild = erstes Bild (Loop).",
         clue="Das letzte Bild schneidet nahtlos auf den Anfang: „Du rennst.“",
         hud=(0, 0, 100)),
]

CAPTION_TEXT = ("Teil 2: Du bist gerannt. Aber vor wem eigentlich? 👀 Mira oder Oskar – wer lügt? 👇 "
                "#bankraub #heist #krimi #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")

if __name__ == "__main__":
    print(sum(len(s["vo"].split()) for s in SEQ), "Wörter")
