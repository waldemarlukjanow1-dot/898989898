"""Story, timing and on-screen data for 'BANKRAUB – Der Umschlag' (62 s).

One entry per sequence. `vo` is the narrator line (Du-Form), `hi` lists words
that are highlighted pink in the captions, `hud` is (beute, crew, hitze, alarm).
"""

TITLE = "BANKRAUB – Der Umschlag"
DURATION = 62.0

SEQ = [
    dict(start=0.0, end=4.5, name="Hook",
         vo="Drei Uhr zwölf. Du stehst vor der Zentralbank. In neunzig Sekunden geht der Alarm wieder an.",
         hi=["neunzig", "Sekunden"],
         visual="Bank bei Nacht im Regen, du von hinten im Vordergrund. Langsamer Zoom auf den Eingang.",
         hud=(0, 3, 0, "01:30")),
    dict(start=4.5, end=9.5, name="Die Crew",
         vo="Mira hackt die Kameras. Oskar fährt den Wagen. Und du? Du knackst den Tresor.",
         hi=["Mira", "Oskar", "Tresor."],
         visual="Lagerhalle, Lampe. Drei Figuren mit Namens-Tags poppen nacheinander auf.",
         hud=(0, 3, 0, "01:22")),
    dict(start=9.5, end=14.0, name="Kameras",
         vo="Mira nickt. Die Kameras zeigen nur noch eine leere Halle. In Dauerschleife.",
         hi=["leere", "Halle."],
         visual="Monitorwand, alle Kameras auf LOOP. Mira grinst am Laptop.",
         hud=(0, 3, 5, "01:14")),
    dict(start=14.0, end=20.0, name="Der Tresor",
         vo="Du ziehst die Handschuhe aus. Für dieses Schloss brauchst du Gefühl. Klick. Klick. Klick.",
         hi=["Handschuhe", "Klick."],
         visual="Riesige Tresortür, Zahlenrad dreht sich, nackte Hand. Handschuhe liegen am Boden (Setup!).",
         hud=(0, 3, 10, "01:03")),
    dict(start=20.0, end=25.0, name="Die Beute",
         vo="Die Tür schwingt auf. Zwölf Komma sechs Millionen Euro.",
         hi=["Zwölf", "Komma", "sechs", "Millionen"],
         visual="Goldenes Licht, Regale voller Goldbarren und Geld. BEUTE-Zähler rattert hoch.",
         hud=(12600000, 3, 20, "00:54")),
    dict(start=25.0, end=29.5, name="Taschen",
         vo="Noch dreißig Sekunden. Ihr stopft alles in vier Taschen.",
         hi=["dreißig", "Sekunden."],
         visual="Vier Taschen füllen sich, Geldbündel fliegen. Schnelle Schnitte.",
         hud=(12600000, 3, 35, "00:30")),
    dict(start=29.5, end=33.5, name="Der Umschlag",
         vo="Dann siehst du ihn. Einen Umschlag. Mit deinem Namen.",
         hi=["deinem", "Namen."],
         visual="Zwischen dem Geld: ein versiegelter Umschlag. Name geschwärzt. Zoom rein.",
         hud=(12600000, 3, 40, "00:22")),
    dict(start=33.5, end=37.0, name="PAUSE",
         vo="Stopp. Niemand kennt deinen echten Namen. Niemand.",
         hi=["Niemand."],
         visual="VHS-Glitch: PAUSE + Timecode, RGB-Versatz, Bild friert ein (wie im Vorbild).",
         hud=(12600000, 3, 40, "00:22")),
    dict(start=37.0, end=44.5, name="Das Foto",
         vo="Darin: ein Foto von dir. Ohne Handschuhe. Am Tresor. Und ein Zettel: Danke für die Fingerabdrücke.",
         hi=["Foto", "Fingerabdrücke."],
         visual="Polaroid: du, nackte Hand am Zahlenrad, rot eingekreist. Zettel: „Danke für die Fingerabdrücke. – O.“",
         hud=(12600000, 3, 60, "00:15")),
    dict(start=44.5, end=49.5, name="Alarm",
         vo="O. Wie Oskar. Und genau jetzt geht der Alarm los. Viel zu früh.",
         hi=["Oskar.", "Alarm"],
         visual="Alles rot, Sirene blinkt, Screen-Shake. HITZE springt auf 100 %.",
         hud=(12600000, 3, 100, "00:00")),
    dict(start=49.5, end=55.0, name="Fluchtwagen",
         vo="Ihr rennt raus. Der Fluchtwagen ist da. Und fährt los. Ohne euch.",
         hi=["Ohne", "euch."],
         visual="Rücklichter im Regen, Oskar winkt aus dem Fenster. CREW fällt von 3 auf 2.",
         hud=(12600000, 2, 100, "00:00")),
    dict(start=55.0, end=62.0, name="Cliffhanger",
         vo="Sirenen von überall. Rennen oder stellen? Schreib's in die Kommentare. Davon hängt Teil zwei ab.",
         hi=["Rennen", "stellen?", "Kommentare."],
         visual="Blau-rotes Licht, du und Mira mit Taschen. Zwei Buttons: RENNEN / STELLEN.",
         hud=(12600000, 2, 100, "00:00")),
]

CAPTION_TEXT = ("Du hast gerade eine Bank geknackt – und dann liegt da ein Umschlag mit deinem Namen 😳💰 "
                "Rennen oder stellen? 👇 #bankraub #storytime #duform #heist #fyp #fürdich")
