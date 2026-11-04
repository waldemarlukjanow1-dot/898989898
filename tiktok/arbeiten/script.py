"""'GEH EINFACH ARBEITEN' – STIL 3, Du-Form. Antwort auf einen Kommentar. chip = (text, kind)."""

TITLE = "GEH EINFACH ARBEITEN"
DURATION = 62.0

SEQ = [
    dict(name="Der Kommentar", vo="Unter deinem letzten Video steht ein Kommentar: Geh einfach arbeiten. Okay. Lass uns das mal durchrechnen.",
         hi=["arbeiten.", "durchrechnen."], chip=("„GEH EINFACH ARBEITEN“", "white"),
         visual="Handy groß: TikTok-Kommentar „Geh einfach arbeiten.“ von einem anonymen Profil. Du hebst eine Augenbraue."),
    dict(name="Der Job", vo="Du fängst einen Job an. Zweitausend Euro netto. Klingt erstmal gut.",
         hi=["Zweitausend", "netto."], chip=("2.000 € NETTO", "green"),
         visual="Büro mit Schreibtisch, Monitor, Pflanze. Du mit Firmenausweis, Lohnzettel schwebt ins Bild."),
    dict(name="Die Kosten", vo="Miete: neunhundert. Auto: dreihundert. Essen: vierhundert. Handy, Strom, Versicherung: zweihundert.",
         hi=["Miete:", "Auto:", "Essen:"], chip=("ÜBRIG: 2.000 €", "green"),
         visual="Liste neben dir, jede Zeile poppt auf, Scheine fliegen dir aus der Hand. Der Chip zählt runter."),
    dict(name="200 Euro", vo="Übrig: zweihundert Euro. Im Monat.",
         hi=["zweihundert"], chip=("ÜBRIG: 200 €", "red"),
         visual="Du hältst zwei einzelne Scheine in der Hand und schaust traurig drauf."),
    dict(name="Urlaub", vo="Urlaub: dreißig Tage im Jahr. Und die musst du dir auch noch erlauben lassen.",
         hi=["dreißig", "erlauben"], chip=("30 VON 365 TAGEN", "white"),
         visual="Großer Kalender mit 365 Kästchen, nur 30 sind grün."),
    dict(name="Der Chef", vo="Chef, kann ich im August frei haben? Nein. Da ist Hochsaison.",
         hi=["Nein."], chip=("URLAUB: ABGELEHNT", "red"),
         visual="Chefbüro: Chef (Glatze, Schnurrbart, Anzug, Krawatte) hinter dem Schreibtisch, Stempel ABGELEHNT."),
    dict(name="PAUSE", vo="Stopp. Du fragst um Erlaubnis – für dein eigenes Leben?",
         hi=["Erlaubnis", "Leben?"], chip=("", "white"),
         visual="Kurzer Freeze: du vor dem Chef-Schreibtisch, Pausen-Symbol."),
    dict(name="33 Jahre", vo="Für eine eigene Wohnung brauchst du achtzigtausend Euro Eigenkapital. Mit zweihundert im Monat sparst du dreiunddreißig Jahre.",
         hi=["achtzigtausend", "dreiunddreißig", "Jahre."], chip=("SPARZIEL: 80.000 €", "white"),
         visual="Sparschwein und Fortschrittsbalken, der Jahre-Zähler rattert bis 33."),
    dict(name="55", vo="Dann bist du fünfundfünfzig. Und hast genau eins geschafft: durchgehalten.",
         hi=["fünfundfünfzig.", "durchgehalten."], chip=("ALTER: 55", "red"),
         visual="Du – älter, graue Haare, Brille, müde – am selben Schreibtisch."),
    dict(name="Das Profil", vo="Du klickst nochmal auf den Kommentar. Auf das Profil. Und erstarrst. Es ist dein Chef.",
         hi=["erstarrst.", "Chef."], chip=("ABSENDER: DEIN CHEF", "red"),
         visual="Handy: Profil des Kommentators öffnet sich – Avatar: dein Chef mit Schnurrbart."),
    dict(name="Cliffhanger", vo="Bleiben – oder kündigen? Schreib es in die Kommentare.",
         hi=["Bleiben", "kündigen?"], chip=("", "white"),
         visual="Du im Büro, der Chef schaut durch die Glastür. Buttons: BLEIBEN / KÜNDIGEN."),
]

CAPTION_TEXT = ("„Geh einfach arbeiten“ … wir haben gerechnet. 🧮😳 Bleiben oder kündigen? 👇 "
                "#gehArbeiten #gehalt #9to5 #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")

_t = 0.0
for _s in SEQ:
    _d = max(2.5, len(_s["vo"].split()) / 2.4)
    _s["start"], _s["end"] = round(_t, 1), round(_t + _d, 1)
    _s["clue"] = "—"
    _t += _d

if __name__ == "__main__":
    print(sum(len(s["vo"].split()) for s in SEQ), "Wörter", round(_t, 1), "s")
