"""Story, timing and on-screen data for 'AM STEUER' (Geldtransporter, ~62 s).

hud = (beute, vertrauen_leon %, verdacht_du %). `insert` = big text insert (key info, readable without sound).
"""

TITLE = "AM STEUER"
DURATION = 62.0

SEQ = [
    dict(start=0, end=5, name="Hook",
         vo="Sechs Uhr morgens. Vor dir hält ein Geldtransporter. Dreißig Millionen Euro. In neunzig Sekunden gehören sie dir.",
         hi=["Geldtransporter.", "Dreißig", "Millionen"], insert="€30.000.000",
         visual="Straße mit Häusern bei Morgendämmerung. Der Geldtransporter fährt ins Bild und hält.",
         clue="—", hud=(0, 100, 0)),
    dict(start=5, end=10, name="Der Plan",
         vo="Sechs Monate Planung. Zwei Komplizen sperren die Straße. Dein Bruder Leon bleibt im Wagen. Am Steuer.",
         hi=["Leon", "Steuer."], insert="LEON BLEIBT IM WAGEN",
         visual="Zwei Komplizen schieben eine Absperrung. Leon (grüne Jacke, Namensschild) sitzt im Lieferwagen.",
         clue="Leon trägt als Einziger keine Maske – er muss ja nicht raus.", hud=(0, 100, 0)),
    dict(start=10, end=16, name="Der Überfall",
         vo="Jetzt. Du springst raus. Die Wachleute legen sich auf den Boden. Einer schaut dich an. Und nickt.",
         hi=["nickt."], insert="ER NICKT?!",
         visual="Du rennst (Maske, rote Jacke) zum Transporter. Zwei Wachleute liegen am Boden, einer hebt den Kopf und nickt.",
         clue="—", hud=(0, 100, 10)),
    dict(start=16, end=20, name="Die Koffer",
         vo="Vier Koffer in den Wagen. Leon gibt Gas.",
         hi=["Vier", "Koffer"], insert="4 KOFFER",
         visual="Du trägst die Koffer zum Lieferwagen, dann fährt der Wagen davon.",
         clue="—", hud=(30000000, 100, 20)),
    dict(start=20, end=25, name="Die Maske",
         vo="Kein Schuss. Keine Verletzten. Du ziehst die Maske runter und lachst.",
         hi=["Maske"], insert="",
         visual="Im Wagen: Du ziehst die Maske ab und lachst. Draußen hängt eine Kamera an einer Laterne.",
         clue="Die Kamera an der Laterne zeigt genau auf dich.", hud=(30000000, 100, 30)),
    dict(start=25, end=30, name="Die Nachricht",
         vo="Dann vibriert dein Handy. Unbekannte Nummer: Danke fürs Tragen.",
         hi=["Danke", "Tragen."], insert="",
         visual="Dein Handy groß im Bild, die Nachricht erscheint.",
         clue="—", hud=(30000000, 80, 30)),
    dict(start=30, end=33, name="PAUSE",
         vo="Stopp. Wer wusste von den Koffern? Nur ihr vier.",
         hi=["vier."], insert="WER WUSSTE ES?",
         visual="Kurze PAUSE: vier Gesichter nebeneinander – DU, LEON, zwei Komplizen.",
         clue="—", hud=(30000000, 70, 30)),
    dict(start=33, end=38, name="Der Peilsender",
         vo="Du reißt einen Koffer auf. Unter dem Geld: ein Peilsender.",
         hi=["Peilsender."], insert="PEILSENDER",
         visual="Der Koffer klappt auf: Geld, darunter ein kleines Gerät mit rotem Licht.",
         clue="—", hud=(30000000, 60, 40)),
    dict(start=38, end=43, name="Falsche Richtung",
         vo="Leon bleibt ruhig. Viel zu ruhig. Und biegt ab. Falsche Richtung.",
         hi=["ruhig.", "Falsche", "Richtung."], insert="FALSCHE RICHTUNG",
         visual="Leon lenkt ruhig, das Navi zeigt einen Pfeil in die andere Richtung.",
         clue="—", hud=(30000000, 30, 40)),
    dict(start=43, end=48, name="Die Lagerhalle",
         vo="Er hält vor einer Lagerhalle. Dort wartet der Wachmann. Der, der genickt hat.",
         hi=["Wachmann.", "genickt"], insert="DER WACHMANN",
         visual="Lagerhalle mit Schild „LAGERHALLE 7“, das Tor geht hoch, der Wachmann kommt heraus.",
         clue="—", hud=(30000000, 10, 50)),
    dict(start=48, end=53, name="Nie gesehen",
         vo="Leon nimmt die Koffer und steigt aus. Er war nie draußen. Keine Kamera hat ihn gesehen.",
         hi=["nie", "draußen.", "Keine", "Kamera"], insert="LEON: 0 KAMERABILDER",
         visual="Leon trägt die Koffer zur Halle. Einblendung: LEON – 0 Kamerabilder.",
         clue="—", hud=(30000000, 0, 70)),
    dict(start=53, end=58, name="Nur du",
         vo="Aber dich. Ohne Maske. Für die Polizei gibt es nur einen Täter: dich.",
         hi=["dich.", "Täter:"], insert="DU: 14 KAMERABILDER",
         visual="Bildschirm mit vier Kamerabildern von dir ohne Maske, Stempel „TATVERDÄCHTIG“.",
         clue="—", hud=(0, 0, 100)),
    dict(start=58, end=62, name="Cliffhanger",
         vo="Sirenen. Fliehen oder Leon jagen? Schreib es in die Kommentare.",
         hi=["Fliehen", "Leon", "jagen?"], insert="",
         visual="Du allein vor der Lagerhalle, Polizeiautos fahren von beiden Seiten heran. Buttons: FLIEHEN / LEON JAGEN.",
         clue="—", hud=(0, 0, 100)),
]

CAPTION_TEXT = ("30 Millionen. Perfekter Plan. Nur eine Person ist auf den Kameras: du. 😳🎥 Fliehen oder Leon jagen? 👇 "
                "#geldtransporter #überfall #verrat #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")

if __name__ == "__main__":
    print(sum(len(s["vo"].split()) for s in SEQ), "Wörter")
