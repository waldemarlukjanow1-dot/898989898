"""'DAS NEUE VIRUS' – neues Virus, Szenario wie 2020/21. STIL 3, Du-Form, T.HERO. Keine medizinischen Behauptungen –
nur der Alltag unter Maßnahmen und die Frage an die Zuschauer. chip = (text, kind)."""

TITLE = "DAS NEUE VIRUS"
DURATION = 62.0

SEQ = [
    dict(name="Eilmeldung", vo="Du wachst auf. Dein Handy explodiert. Eilmeldung: ein neues Virus. Es breitet sich schneller aus als alles davor.",
         hi=["Virus.", "schneller"], chip=("EILMELDUNG: NEUES VIRUS", "red"),
         visual="Zimmer am Morgen, Handy groß mit Eilmeldung, Benachrichtigungen stapeln sich."),
    dict(name="Leere Regale", vo="Mittags sind die Supermärkte leer. Nudeln weg. Klopapier weg. Die Leute streiten sich um das letzte Desinfektionsmittel.",
         hi=["leer.", "Klopapier"], chip=("REGALE: LEER", "red"),
         visual="Supermarkt mit leeren Regalen, zwei Leute ziehen an derselben Flasche."),
    dict(name="Maskenpflicht", vo="Am nächsten Tag: Maskenpflicht. Im Bus. Im Laden. Auf der Arbeit.",
         hi=["Maskenpflicht."], chip=("MASKENPFLICHT", "white"),
         visual="Bus mit Fahrgästen, alle mit Maske. Du setzt deine Maske auf."),
    dict(name="Ausgangssperre", vo="Eine Woche später: Ausgangssperre ab zweiundzwanzig Uhr. Die Straßen sind leer. Nur Streifenwagen.",
         hi=["Ausgangssperre", "22", "leer."], chip=("AUSGANGSSPERRE 22:00", "red"),
         visual="Leere Straße bei Nacht, Uhr 22:00, ein Streifenwagen fährt langsam vorbei."),
    dict(name="Der Brief", vo="Dann kommt der Brief: Impfung. Ohne Nachweis kein Restaurant. Kein Kino. Kein Fitnessstudio.",
         hi=["Impfung.", "Nachweis"], chip=("OHNE NACHWEIS: KEIN ZUTRITT", "red"),
         visual="Brief „IMPFNACHWEIS ERFORDERLICH“, darunter Restaurant, Kino, Fitnessstudio – rot durchgestrichen."),
    dict(name="Der Chef", vo="Dein Chef schreibt: Ohne Nachweis brauchst du gar nicht mehr zu kommen.",
         hi=["Chef", "gar", "nicht"], chip=("NACHRICHT VOM CHEF", "white"),
         visual="Handy-Chat mit „Chef“: „Ohne Nachweis brauchst du gar nicht mehr zu kommen.“"),
    dict(name="PAUSE", vo="Stopp. Kommt dir das bekannt vor?",
         hi=["bekannt"], chip=("", "white"),
         visual="Kurzer Freeze, Pausen-Symbol."),
    dict(name="Streit", vo="Deine Familie streitet beim Abendessen. Freunde schreiben dir nicht mehr. Jeder ist plötzlich Experte.",
         hi=["streitet", "Experte."], chip=("FAMILIE: STREIT", "red"),
         visual="Esstisch, alle reden durcheinander, Sprechblasen mit Ausrufezeichen."),
    dict(name="Impfzentrum", vo="Du stehst vor dem Impfzentrum. Die Schlange ist hundert Meter lang. Dein Handy vibriert: Termin in zehn Minuten.",
         hi=["Impfzentrum.", "10", "Minuten."], chip=("TERMIN: IN 10 MIN", "white"),
         visual="Gebäude mit Schild IMPFZENTRUM, lange Schlange mit Masken, du stehst mittendrin."),
    dict(name="Die Frage", vo="Und du fragst dich: Mache ich das freiwillig? Oder weil ich keine Wahl habe?",
         hi=["freiwillig?", "Wahl"], chip=("FREIWILLIG?", "white"),
         visual="Du in Nahaufnahme, zwei Gedankenblasen: FREIWILLIG? / KEINE WAHL?"),
    dict(name="Cliffhanger", vo="Macht ihr das alle wieder mit? Oder lasst ihr so etwas nicht mehr mit euch machen? Schreib es in die Kommentare.",
         hi=["wieder", "mit?", "nicht", "mehr"], chip=("UND DU?", "yellow"),
         visual="Du nimmst die Maske ab und schaust in die Kamera. Buttons: ICH MACH MIT / NICHT MEHR."),
]

CAPTION_TEXT = ("Neues Virus, neue Regeln … kommt dir das bekannt vor? 😷 Machst du wieder mit – oder nicht mehr? 👇 "
                "#gedankenexperiment #2021 #wasmachstdu #storytime #duform #geschichte #fürdich #fyp")

_t = 0.0
for _s in SEQ:
    _d = max(2.5, len(_s["vo"].split()) / 2.4)
    _s["start"], _s["end"] = round(_t, 1), round(_t + _d, 1)
    _s["clue"] = "—"
    _t += _d

if __name__ == "__main__":
    print(sum(len(s["vo"].split()) for s in SEQ), "Wörter")
