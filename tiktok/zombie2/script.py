"""Story and on-screen data for 'PATIENT NULL – Teil 2: Fliehen'.

hud = (uhrzeit, zombies, immunitaet % or text). `insert` = key-info text insert.
"""

TITLE = "PATIENT NULL – Teil 2"
DURATION = 63.0

SEQ = [
    dict(start=0, end=7, name="Rückblick", vo="Du bist Patient Null. Die Zombies greifen dich nicht an. Und du hast dich gerade für die Flucht entschieden.",
         hi=["Patient", "Null.", "Flucht"], insert="TEIL 2: FLIEHEN",
         visual="Stadion aus Teil 1, der Button FLIEHEN leuchtet auf. Du rennst los.", clue="—", hud=("12:01", 80, 100)),
    dict(start=7, end=12, name="Hubschrauber", vo="Hinter dir startet der Hubschrauber. Er folgt dir. Du rennst mitten in die Horde.",
         hi=["Hubschrauber.", "Horde."], insert="",
         visual="Hubschrauber über der Straße mit Suchscheinwerfer. Vor dir: die Zombie-Horde.", clue="—", hud=("12:03", 200, 100)),
    dict(start=12, end=17, name="Die Mauer", vo="Und die Zombies machen dir Platz. Wie eine Mauer schließen sie sich hinter dir.",
         hi=["Platz.", "Mauer"], insert="SIE BESCHÜTZEN DICH",
         visual="Die Zombies weichen zur Seite, du läufst durch, sie schließen sich wieder. Der Hubschrauber dreht ab.", clue="—", hud=("12:04", 200, 100)),
    dict(start=17, end=22, name="Das Labor", vo="Du versteckst dich im einzigen Ort, an dem dich keiner sucht. Deinem Labor.",
         hi=["Labor."], insert="DEIN LABOR",
         visual="Laborgebäude mit Schild BIOLABOR NORD, zerbrochene Glastür. Du schleichst hinein.", clue="Dein Name steht auf dem Klingelschild.", hud=("12:20", 200, 100)),
    dict(start=22, end=27, name="Der Laptop", vo="Auf deinem Schreibtisch: dein Laptop. Ein Video. Aufgenommen gestern. Von dir.",
         hi=["Video.", "dir."], insert="VIDEO VON DIR",
         visual="Schreibtisch, der Laptop klappt auf. Video-Vorschau: dein Gesicht, Datum GESTERN 23:58.", clue="—", hud=("12:22", 200, 100)),
    dict(start=27, end=34, name="Absichtlich", vo="Du drückst auf Play. Wenn du das siehst, hat es funktioniert. Ich habe es mir selbst gespritzt. Absichtlich.",
         hi=["selbst", "Absichtlich."], insert="ABSICHTLICH?!",
         visual="Im Video: du im Laborkittel, sprichst in die Kamera, hältst eine grüne Ampulle hoch.", clue="—", hud=("12:23", 200, 100)),
    dict(start=34, end=38, name="PAUSE", vo="Stopp. Du hast dich absichtlich infiziert?",
         hi=["absichtlich"], insert="",
         visual="Kurze PAUSE auf dem Video-Standbild.", clue="—", hud=("12:23", 200, 100)),
    dict(start=38, end=44, name="Gegenmittel", vo="Das Video läuft weiter. Ich bin nicht der Anfang. Ich bin das Gegenmittel. Es ist in meinem Blut.",
         hi=["Gegenmittel.", "Blut."], insert="GEGENMITTEL = DEIN BLUT",
         visual="Im Video zeigt dein früheres Ich auf eine Grafik: Blutstropfen mit grünem Schild.", clue="—", hud=("12:24", 200, 90)),
    dict(start=44, end=50, name="Sie sehen dich", vo="Die Zombies vor dem Fenster drehen sich um. Zum ersten Mal schauen sie dich an.",
         hi=["ersten", "Mal", "dich"], insert="SIE SEHEN DICH",
         visual="Laborfenster: Zombie-Köpfe drehen sich langsam zu dir. IMMUNITÄT fällt.", clue="—", hud=("12:25", 200, 40)),
    dict(start=50, end=55, name="24 Stunden", vo="Auf dem Monitor blinkt eine Warnung: Immunität lässt nach. Noch vierundzwanzig Stunden.",
         hi=["Immunität", "vierundzwanzig", "Stunden."], insert="NOCH 24 STUNDEN",
         visual="Monitor mit rotem Warnbalken, Countdown 24:00:00 läuft.", clue="—", hud=("12:26", 200, 20)),
    dict(start=55, end=63, name="Cliffhanger", vo="Dein Blut kann die Welt retten. Zurück zum Soldaten oder das Gegenmittel allein herstellen? Schreib es in die Kommentare.",
         hi=["Soldaten", "allein"], insert="",
         visual="Du zwischen Fenster (Zombies) und Tür (Hubschrauber-Licht). Buttons: ZUM SOLDATEN / ALLEIN.", clue="—", hud=("12:27", 200, 20)),
]

CAPTION_TEXT = ("Teil 2: Du bist geflohen – und hast ein Video von dir selbst gefunden. 😳🧟 Zurück zum Soldaten oder allein? 👇 "
                "#zombie #apokalypse #patientnull #teil2 #storytime #duform #geschichte #plottwist #fürdich #fyp")
