"""Story, timing and on-screen data for 'DER SCHEIN' (Lotto-Mystery, ~62 s).

hud = (gewinn €, vertrauen_marco %, erinnerung (int % or "???")). `insert` = key-info text insert.
"""

TITLE = "DER SCHEIN"
DURATION = 62.0

SEQ = [
    dict(start=0, end=6, name="Hook",
         vo="Du hast gerade siebenundvierzig Millionen im Lotto gewonnen. Niemand weiß davon. Und so muss es bleiben.",
         hi=["siebenundvierzig", "Millionen", "Niemand"], insert="€47.000.000",
         visual="Wohnzimmer, Fernseher zeigt die Lottozahlen – alle sechs Haken grün. Du springst vom Sofa, Schein in der Hand.",
         clue="—", hud=(47000000, 100, 100)),
    dict(start=6, end=12, name="Marco",
         vo="Morgen um neun bringst du den Schein zur Lotto-Zentrale. Du erzählst es nur einem: deinem besten Freund Marco.",
         hi=["Marco."], insert="NUR MARCO WEISS ES",
         visual="Geteiltes Bild: du telefonierst links, Marco (türkiser Hoodie, Namensschild) rechts.",
         clue="An deiner Garderobe hängt die rote Jacke – der Schein steckt in der Brusttasche.", hud=(47000000, 100, 100)),
    dict(start=12, end=18, name="Der Zettel",
         vo="Nachts klopft es. Durch den Türspion: niemand. Auf der Fußmatte liegt ein Zettel. Gratuliere.",
         hi=["niemand.", "Gratuliere."], insert="GRATULIERE.",
         visual="Flur bei Nacht: du gehst zur Tür, Blick durch den Türspion (leerer Hausflur), Zettel auf der Fußmatte.",
         clue="Die Handschrift auf dem Zettel sieht aus wie deine.", hud=(47000000, 80, 100)),
    dict(start=18, end=22, name="Der Anruf",
         vo="Du rufst Marco an. Er schwört: Ich habe es keinem gesagt.",
         hi=["schwört:"], insert="",
         visual="Marco groß im Bild am Handy, Mund bewegt sich, Sprechblase „Ich hab's keinem gesagt!“.",
         clue="—", hud=(47000000, 60, 100)),
    dict(start=22, end=27, name="Nasse Schuhe",
         vo="Am Morgen sind deine Schuhe nass. Komisch. Du warst doch die ganze Nacht zu Hause.",
         hi=["Schuhe", "nass."], insert="NASSE SCHUHE?",
         visual="Morgens im Flur: deine Schuhe in einer Pfütze, Tropfen fallen. Uhr: 07:30.",
         clue="Neben den Schuhen liegt eine Quittung der Tankstelle.", hud=(47000000, 60, 70)),
    dict(start=27, end=33, name="Die Kopie",
         vo="Lotto-Zentrale. Die Frau prüft den Schein. Dann sagt sie: Das ist eine Kopie. Der echte wurde heute Nacht eingelöst.",
         hi=["Kopie.", "eingelöst."], insert="KOPIE!",
         visual="Gebäude mit Schild LOTTO-ZENTRALE, drinnen der Schalter. Scanner piept, Bildschirm zeigt rot: KOPIE.",
         clue="—", hud=(0, 50, 70)),
    dict(start=33, end=37, name="PAUSE",
         vo="Stopp. Der Schein war die ganze Nacht in deiner Jacke. Wer hat ihn getauscht?",
         hi=["Jacke.", "getauscht?"], insert="",
         visual="Kurze PAUSE: die rote Jacke am Haken, Schein in der Tasche, großes Fragezeichen.",
         clue="—", hud=(0, 40, 70)),
    dict(start=37, end=44, name="Die Tankstelle",
         vo="Sie zeigt dir das Kamerabild der Tankstelle an der Ecke. Zwei Uhr vierzehn. Ein Mann in deiner Jacke.",
         hi=["Tankstelle", "deiner", "Jacke."], insert="TANKSTELLE · 02:14 UHR",
         visual="Monitor: Kamerabild einer Tankstelle (Zapfsäulen, Preistafel). Ein Mann in roter Jacke geht zur Kasse.",
         clue="—", hud=(0, 20, 50)),
    dict(start=44, end=48, name="Nicht Marco",
         vo="Er dreht sich um. Es ist nicht Marco.",
         hi=["nicht", "Marco."], insert="NICHT MARCO",
         visual="Zoom auf den Monitor: Der Mann dreht langsam den Kopf zur Kamera.",
         clue="—", hud=(0, 100, 30)),
    dict(start=48, end=52, name="Es bist du",
         vo="Es bist du.",
         hi=["du."], insert="DU?!",
         visual="Geteiltes Bild: links das Kamerabild – dein Gesicht. Rechts du am Schalter, geschockt.",
         clue="—", hud=(0, 100, 0)),
    dict(start=52, end=62, name="Cliffhanger",
         vo="Nasse Schuhe. Keine Erinnerung. Zwilling, Doppelgänger, oder warst du es wirklich? Schreib es in die Kommentare.",
         hi=["Zwilling,", "Doppelgänger,", "wirklich?"], insert="",
         visual="Du allein im Flur, die nassen Schuhe vor dir. Drei Buttons: ZWILLING / DOPPELGÄNGER / ICH.",
         clue="—", hud=(0, 100, "???")),
]

CAPTION_TEXT = ("47 Millionen gewonnen – aber jemand hat deinen Schein schon eingelöst. Und die Kamera zeigt … dich. 😳🎟️ "
                "Zwilling, Doppelgänger oder du? 👇 #lotto #mystery #doppelgänger #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")

if __name__ == "__main__":
    print(sum(len(s["vo"].split()) for s in SEQ), "Wörter")
