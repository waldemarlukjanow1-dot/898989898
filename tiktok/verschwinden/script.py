"""'24 STUNDEN VERSCHWINDEN' – STIL 3, Du-Form."""
TITLE = "24 STUNDEN VERSCHWINDEN"
DURATION = 63.0
_V = [p.strip() for p in open(__file__.replace("script.py", "vo.txt"), encoding="utf-8").read().strip().split("\n\n")]
_META = [
    ("Das Angebot", ["Zwanzig", "Millionen", "verschwinden."], "Handy: 20.000.000 € für 24 Stunden verschwinden – KEINE FRAGEN / KEINE POLIZEI / KEINE FAMILIE."),
    ("Der Geländewagen", ["ja.", "Geländewagen"], "Du nickst. Nachts fährt ein schwarzer Geländewagen mit Scheinwerfern vor dir vor."),
    ("Gelöscht", ["zerstört.", "gelöscht.", "nicht"], "KRACH – Handy zersplittert. Register: Eintrag für Eintrag GELÖSCHT → PERSON NICHT GEFUNDEN."),
    ("Eilmeldung", ["tot", "Foto.", "Name."], "Fernseher: EILMELDUNG – UNTERNEHMER TOT AUFGEFUNDEN, dann erscheint dein Foto mit Trauerflor."),
    ("Erste Zahlung", ["fünf", "Millionen."], "Neues Konto zählt hoch auf 5.000.000 € – Zahlung 1 von 4."),
    ("PAUSE", ["toten"], "Freeze mit Pausen-Symbol, du fasst dir an den Kopf."),
    ("Der Anruf", ["schuldest."], "Hotelzimmer 1408. Das Telefon klingelt. Sprechblase der Stimme."),
    ("Der Umschlag", ["Familie.", "heute", "tot."], "Foto deiner Familie – HEUTE 07:12. Umdrehen: „Bleib tot.“"),
    ("Der Schlüssel", ["Schlüssel", "Niemand"], "Der Türgriff dreht sich, klick, Licht unter der Tür."),
    ("Zielperson", ["Zielperson"], "Dein neues Handy: „Zielperson gefunden.“ mit Fadenkreuz."),
    ("Der Fahrer", ["Fahrer", "um."], "Die Tür geht auf: der Fahrer vom SUV mit Sonnenbrille. Er sagt: „Die 24 Stunden sind um.“"),
    ("Cliffhanger", ["Angreifen", "fliehen?"], "Du und der Fahrer. Buttons: ANGREIFEN / FLIEHEN."),
]
SEQ = [dict(name=n, vo=v, hi=hi, chip=("", "white"), visual=vis) for (n, hi, vis), v in zip(_META, _V)]
CAPTION_TEXT = ("20 Millionen, um 24 Stunden zu verschwinden … am nächsten Morgen bist du offiziell tot. 💰🕶️ Angreifen oder fliehen? 👇 "
                "#mystery #thriller #20millionen #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")
from timing import seq_bounds as _sb  # noqa: E402
for _s, (_a, _b) in zip(SEQ, _sb()[0]):
    _s["start"], _s["end"], _s["clue"] = round(_a, 1), round(_b, 1), "—"
