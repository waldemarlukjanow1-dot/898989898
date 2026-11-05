"""'SCHNELLE WELLE' – STIL 3, Du-Form, Antwort auf Kommentar. Abschreckend: Stress, Angst, kein Leben.
Keine Drogen im Bild, keine Anleitung – nur die Folgen. chip = (text, kind)."""

TITLE = "SCHNELLE WELLE"
DURATION = 62.0

SEQ = [
    dict(name="Der Kommentar", vo="Der Bruder schreibt unter das letzte Video: Schnelle Welle. Straßenapotheker. Okay. Schauen wir uns das mal an.",
         hi=["Bruder", "Straßenapotheker.", "an."], chip=("„SCHNELLE WELLE“", "white"),
         visual="Handy: Kommentar von bruder.1987 „Schnelle Welle. Straßenapotheker.“ Du schaust skeptisch."),
    dict(name="Schnelles Geld", vo="Du bist jetzt Straßenapotheker. Das erste Geld kommt schnell. Zu schnell.",
         hi=["schnell.", "Zu"], chip=("+ 2.400 €", "green"),
         visual="Nachts unter einer Laterne, Kapuze auf. Ein paar Scheine in deiner Hand – du schaust dich um."),
    dict(name="Jedes Auto", vo="Ab jetzt ist jedes Auto ein Problem. Jeder dunkle Golf. Jedes Blaulicht. Sind das die Amcas?",
         hi=["Golf.", "Amcas?"], chip=("⚠ ZIVILSTREIFE?", "red"),
         visual="Straße bei Nacht, ein dunkles Auto fährt langsam vorbei, Scheinwerfer streifen dich. Du duckst dich."),
    dict(name="Kein Schlaf", vo="Du schläfst nicht mehr. Jedes Geräusch im Treppenhaus – und du stehst sofort am Fenster.",
         hi=["schläfst", "Fenster."], chip=("SCHLAF: 3 STUNDEN", "red"),
         visual="Dein Zimmer, 03:47 Uhr. Du stehst am Fenster und schaust durch den Vorhangspalt nach unten."),
    dict(name="Das Handy", vo="Dein Handy klingelt. Unbekannte Nummer. Du gehst nicht ran. Nie mehr.",
         hi=["Unbekannte", "Nie"], chip=("UNBEKANNTE NUMMER", "white"),
         visual="Handy vibriert auf dem Tisch, Anzeige: Unbekannt. Du starrst es nur an."),
    dict(name="Das Geld", vo="Und das Geld? Kannst du nicht ausgeben. Kein Konto. Kein Herkunftsnachweis. Es liegt im Schuhkarton.",
         hi=["Herkunftsnachweis.", "Schuhkarton."], chip=("KEIN HERKUNFTSNACHWEIS", "red"),
         visual="Schuhkarton unter dem Bett mit Scheinen. Du schiebst ihn nervös zurück."),
    dict(name="PAUSE", vo="Stopp. Du hast Geld – und kannst nichts damit machen?",
         hi=["nichts"], chip=("", "white"),
         visual="Kurzer Freeze: du vor dem Schuhkarton, Pausen-Symbol."),
    dict(name="Die Lüge", vo="Deine Mutter fragt: Woher hast du die neuen Schuhe? Du lügst. Schon wieder.",
         hi=["Mutter", "lügst."], chip=("LÜGE NR. 47", "red"),
         visual="Küche: Mutter mit Schürze zeigt auf deine neuen Schuhe. Du schaust weg."),
    dict(name="Der Kumpel", vo="Dann wird dein bester Kumpel erwischt. Und plötzlich fragst du dich nur noch eins: Was hat er erzählt?",
         hi=["erwischt.", "erzählt?"], chip=("KUMPEL: FESTGENOMMEN", "red"),
         visual="Handy: Nachricht „Sie haben Deniz geholt.“ Du wirst blass."),
    dict(name="06:00", vo="Sechs Uhr morgens. Es klingelt. Dreimal. Durch den Türspion: Polizei.",
         hi=["Polizei."], chip=("06:00 UHR", "red"),
         visual="Wohnungstür, Blick durch den Türspion: zwei Polizisten, Blaulicht im Treppenhaus."),
    dict(name="Cliffhanger", vo="Schnelle Welle? Die Welle war schnell. Und schnell vorbei. Lohnt sich das? Schreib es in die Kommentare.",
         hi=["vorbei.", "Lohnt"], chip=("", "white"),
         visual="Du sitzt auf dem Boden an der Tür, Blaulicht durch den Spalt. Buttons: LOHNT SICH / NIEMALS."),
]

CAPTION_TEXT = ("„Schnelle Welle“ … so sieht der Alltag wirklich aus. 😰🚔 Lohnt sich das? 👇 "
                "#antwort #kommentar #realtalk #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")

_t = 0.0
for _s in SEQ:
    _d = max(2.5, len(_s["vo"].split()) / 2.4)
    _s["start"], _s["end"] = round(_t, 1), round(_t + _d, 1)
    _s["clue"] = "—"
    _t += _d

if __name__ == "__main__":
    print(sum(len(s["vo"].split()) for s in SEQ), "Wörter")
