"""Story and on-screen data for 'PATIENT NULL' (Zombie-Apokalypse).

hud = (uhrzeit "hh:mm", zombies, mensch % or "???"). `insert` = key-info text insert.
Sequence times come from timing.py (voice), the start/end values here are only the plan.
"""

TITLE = "PATIENT NULL"
DURATION = 64.0

SEQ = [
    dict(start=0, end=9, name="Aufwachen",
         vo="Du wachst auf. Dreiundsechzig verpasste Anrufe. Draußen heulen Sirenen. Die Zombie-Apokalypse ist ausgebrochen. Und du hast sie verschlafen.",
         hi=["Zombie-Apokalypse", "verschlafen."], insert="ZOMBIE-APOKALYPSE",
         visual="Schlafzimmer: Du setzt dich im Bett auf. Handy: „63 verpasste Anrufe – LABOR“. Fenster: Rauch und rotes Licht über der Stadt.",
         clue="Alle Anrufe kommen von „LABOR“.", hud=("11:02", 0, 100)),
    dict(start=9, end=14, name="Allein",
         vo="Die Straße ist leer. Autos stehen kreuz und quer. Kein Mensch. Du bist allein.",
         hi=["allein."], insert="ÜBERLEBENDE: 1",
         visual="Du trittst aus der Haustür. Straße mit Häusern, verlassene Autos mit offenen Türen, Zeitungen wehen.",
         clue="—", hud=("11:08", 0, 100)),
    dict(start=14, end=20, name="Durchsage",
         vo="Im Autoradio eine letzte Durchsage: Alle Überlebenden zum Stadion. Letzter Hubschrauber um zwölf Uhr.",
         hi=["Stadion.", "Hubschrauber"], insert="HUBSCHRAUBER: 12:00",
         visual="Autoradio mit Anzeige NOTFUNK, Schallwellen. Schild mit Pfeil: STADION.",
         clue="—", hud=("11:15", 0, 100)),
    dict(start=20, end=23, name="Los",
         vo="Es ist elf Uhr zwanzig. Du rennst los.",
         hi=["rennst"], insert="NOCH 40 MINUTEN",
         visual="Uhr an der Apotheke zeigt 11:20. Du rennst die Straße entlang.",
         clue="—", hud=("11:20", 0, 100)),
    dict(start=23, end=28, name="Zombies",
         vo="An der Kreuzung: die ersten Zombies. Zehn. Zwanzig. Sie drehen sich zu dir um.",
         hi=["Zombies.", "dir"], insert="20 ZOMBIES",
         visual="Kreuzung mit Ampel. Grüne Zombies mit zerrissener Kleidung schlurfen mit ausgestreckten Armen, drehen sich zu dir.",
         clue="—", hud=("11:31", 20, 100)),
    dict(start=28, end=33, name="Vorbei",
         vo="Du erstarrst. Sie kommen näher. Und dann laufen sie einfach an dir vorbei.",
         hi=["vorbei."], insert="SIE IGNORIEREN DICH?!",
         visual="Du stehst still in der Mitte, die Zombies laufen links und rechts an dir vorbei.",
         clue="Kein Zombie schaut dich an – als wärst du einer von ihnen.", hud=("11:33", 20, 100)),
    dict(start=33, end=36, name="PAUSE",
         vo="Stopp. Warum greifen sie dich nicht an?",
         hi=["Warum"], insert="",
         visual="Kurze PAUSE: du in der Mitte, die Zombies um dich eingefroren.",
         clue="—", hud=("11:33", 20, 100)),
    dict(start=36, end=41, name="Stadion",
         vo="Elf Uhr neunundfünfzig. Das Stadion. Ein Soldat richtet die Waffe auf dich: Stehen bleiben!",
         hi=["Soldat", "Stehen", "bleiben!"], insert="11:59",
         visual="Stadion mit Schriftzug, Hubschrauber mit drehenden Rotoren. Ein Soldat mit Helm stellt sich dir in den Weg.",
         clue="—", hud=("11:59", 35, 100)),
    dict(start=41, end=49, name="Patient Null",
         vo="Er scannt dein Gesicht. Dann wird er blass. Auf seinem Tablet: dein Foto. Darunter: Patient Null.",
         hi=["Foto.", "Patient", "Null."], insert="PATIENT NULL",
         visual="Tablet groß im Bild: dein Foto, roter Balken PATIENT NULL, Logo LABOR.",
         clue="Auf dem Tablet steht dein Name als Mitarbeiter des Labors.", hud=("12:00", 35, 100)),
    dict(start=49, end=56, name="Der Erste",
         vo="Die dreiundsechzig Anrufe. Das Labor. Du warst der Erste. Deshalb greifen sie dich nicht an. Für sie bist du einer von ihnen.",
         hi=["Erste.", "einer", "ihnen."], insert="DU WARST DER ERSTE",
         visual="RÜCKBLENDE (Sepia): du im Laborkittel, ein Glas zerbricht, grüner Dampf. MENSCH springt auf ???.",
         clue="—", hud=("12:00", 50, "???")),
    dict(start=56, end=64, name="Cliffhanger",
         vo="Der Soldat senkt die Waffe. Steig ein. Du kommst ins Labor. Mitfliegen oder fliehen? Schreib es in die Kommentare.",
         hi=["Labor.", "Mitfliegen", "fliehen?"], insert="",
         visual="Soldat zeigt auf den Hubschrauber, Zombies am Rand. Buttons: MITFLIEGEN / FLIEHEN.",
         clue="—", hud=("12:00", 80, "???")),
]

CAPTION_TEXT = ("Du hast die Zombie-Apokalypse verschlafen – und die Zombies greifen dich nicht an. Warum? 🧟‍♂️😳 "
                "Mitfliegen oder fliehen? 👇 #zombie #apokalypse #patientnull #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")
