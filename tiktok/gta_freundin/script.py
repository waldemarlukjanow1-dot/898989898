"""'DARF ER GTA 6 SPIELEN?' – Video zum Weiterschicken an die Freundin. STIL 3."""
TITLE = "DARF ER GTA 6 SPIELEN?"
DURATION = 60.0
_V = [p.strip() for p in open(__file__.replace("script.py", "vo.txt"), encoding="utf-8").read().strip().split("\n\n")]
_META = [
    ("Geschickt", ["Freund", "dran."], "Freundin bekommt ein Video von „Schatz ♥“ – „Bitte ganz anschauen!“"),
    ("Seit 2013", ["zehn", "Jahren", "Länger,"], "Kalender zählt 2013 → 2026: „länger als ihr zwei“."),
    ("Seine Wünsche", ["Paris.", "Schuhe.", "Controller."], "PARIS und SCHUHE durchgestrichen, daneben nur ein Controller: NUR DAS."),
    ("Sofa", ["wo", "Sofa.", "dir."], "Beide auf dem Sofa vor dem Fernseher, Standort: Sofa, Herz."),
    ("Keine andere", ["keiner", "anderen", "Vice", "City."], "Handy: Keine neuen Nachrichten – 0. Unten fährt nur ein kleines Auto durchs Spiel."),
    ("PAUSE", ["ehrlich.", "fair,"], "Freeze mit Pausen-Symbol."),
    ("Vertrag", ["Wochenende", "kocht", "zugesagt."], "Vertrag mit drei Häkchen: Wochenende spielen, Mo–Fr kochen, Essen bei deinen Eltern."),
    ("Player 2", ["zweiten", "Controller."], "Er reicht ihr den pinken zweiten Controller, Herzen steigen auf."),
    ("Abstimmung", ["Ja", "Nein", "markier"], "Er mit Hundeblick, @dein.freund, Buttons JA / NEIN."),
]
SEQ = [dict(name=n, vo=v, hi=hi, chip=("", "white"), visual=vis) for (n, hi, vis), v in zip(_META, _V)]
CAPTION_TEXT = ("Schick das deiner Freundin. 🎮❤️ Darf er GTA 6 spielen – JA oder NEIN? 👇 Markier deinen Freund!"
                " #gta6 #paare #beziehung #freundin #storytime #duform #fürdich #fyp")
from timing import seq_bounds as _sb  # noqa: E402
for _s, (_a, _b) in zip(SEQ, _sb()[0]):
    _s["start"], _s["end"], _s["clue"] = round(_a, 1), round(_b, 1), "—"
