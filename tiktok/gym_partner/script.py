"""'SCHICK DAS DEINEM GYM-PARTNER, DER IMMER ABSAGT' – Video zum Weiterschicken. STIL 3, athletische Figur."""
TITLE = "SCHICK DAS DEINEM GYM-PARTNER"
DURATION = 54.0
_V = [p.strip().replace("\n", " ") for p in open(__file__.replace("script.py", "vo.txt"), encoding="utf-8").read().strip().split("\n\n")]
_META = [
    ("Du bist gemeint", ["Gym-Partner", "gemeint."], "Schock-Frame: ER zeigt auf dich – DU! Dann: DU (oranger Hoodie) auf dem Sofa, Handy: Video von „Gym-Partner“. Zurück: DU BIST GEMEINT."),
    ("Abgesagt", ["Montag", "komme.", "fünf:", "nicht."], "Chat: „Ich komme!“ (09:13) … 17:00: „Heute schaff ich's nicht“ → Stempel ABGESAGT."),
    ("Ausreden", ["Rücken.", "müde.", "Grillen.", "allein"], "Kalender SEINE AUSREDEN: Mi Rücken, Fr Zu müde, Sa Grillen. Dann: ER allein an der Hantelbank, daneben DEIN PLATZ mit „?“."),
    ("Er stärker, du nicht", ["Schlimmste", "stärker.", "nicht."], "Split-Screen: links ER im Gym, wird breiter (+20 kg), rechts DU auf dem Sofa (+0 kg)."),
    ("PAUSE", ["ehrlich.", "abgesagt?"], "Freeze + Pause-Symbol (einmal kurz). Zähler ABGESAGT: 0 → 47×."),
    ("Sein Angebot", ["abholt", "Tasche.", "Döner.", "zahlt."], "Angebot mit 4 Häkchen: abholen, Tasche packen, Döner danach, er zahlt. Tasche und Döner poppen ins Bild."),
    ("Bedingung", ["Bedingung:", "Ausreden"], "ER ernst, breit: NUR EINE BEDINGUNG → KEINE AUSREDEN MEHR."),
    ("Abstimmung", ["morgen", "Ja", "Nein", "absagt."], "ER wartet vor dem GYM mit deiner Tasche, Buttons JA / NEIN, @der.absager."),
]
SEQ = [dict(name=n, vo=v, hi=hi, chip=("", "white"), visual=vis) for (n, hi, vis), v in zip(_META, _V)]
CAPTION_TEXT = ("Schick das deinem Gym-Partner, der immer absagt. 💪 Kommt er morgen mit – JA oder NEIN? 👇 Markier den Absager!"
                " #gym #fitness #gympartner #storytime #duform #geschichte #fürdich #fyp")
from timing import seq_bounds as _sb  # noqa: E402
for _s, (_a, _b) in zip(SEQ, _sb()[0]):
    _s["start"], _s["end"], _s["clue"] = round(_a, 1), round(_b, 1), "—"
