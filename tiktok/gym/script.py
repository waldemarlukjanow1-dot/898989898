"""'STELL DIR VOR, DU ZIEHST AB HEUTE GYM DURCH' – Motivation + 3 Gym-Tipps. STIL 3, Figur wird breiter."""
TITLE = "AB HEUTE ZIEHST DU GYM DURCH"
DURATION = 62.0
_V = [p.strip().replace("\n", " ") for p in open(__file__.replace("script.py", "vo.txt"), encoding="utf-8").read().strip().split("\n\n")]
_META = [
    ("Ab heute", ["Gym", "Montag.", "Neujahr.", "Heute."], "Schock-Frame: DU – IN 1 JAHR (breit, Bizeps). Dann: du, dünn, vor dem GYM mit Sporttasche. MONTAG und NEUJAHR durchgestrichen → HEUTE!"),
    ("Tag 1", ["Maschine", "Egal.", "da.", "schwerste"], "Im Gym vor einer komplizierten Maschine, rote Fragezeichen. Dann lächelst du: DU BIST DA = schwerster Teil."),
    ("Woche 1", ["Muskelkater", "Treppen", "trotzdem."], "Du kletterst mühsam eine Treppe hoch, rote Schmerz-Blitze an Beinen und Armen. MUSKELKATER → trotzdem!"),
    ("3 Tipps", ["Dreimal", "Ganzkörper.", "Gewicht.", "Eiweiß.", "acht", "Schlaf"], "TIPP 1: Kniebeuge mit Langhantel + Kalender Mo/Mi/Fr, 45 MIN. TIPP 2: Bizeps-Curls, Gewicht zählt 10 → 20 kg. TIPP 3: Teller mit Hähnchen, Eiern, Brokkoli → Bett, 8 STUNDEN, Zzz. Figur wird sichtbar breiter."),
    ("Monat 3 & 6", ["T-Shirt", "Schultern.", "Trainierst"], "Dein gestreifter Pulli spannt an den Schultern: ZU ENG! Monat 6: Ein Kollege staunt: „Trainierst du?“"),
    ("1 Jahr", ["Jahr", "Spiegel.", "kaum"], "Du stehst vor dem Spiegel – breit, Bizeps im Spiegelbild. „BIST DAS DU?“"),
    ("PAUSE", ["Einzige", "Spiegelbild", "Heute."], "Freeze + Pause-Symbol (einmal kurz). Links DU HEUTE (dünn), rechts im Spiegel IN 1 JAHR. Groß: HEUTE."),
    ("Tag 1", ["anfängst", "Tag", "eins", "Gym-Partner."], "Du flext im Gym. Ein Kommentar tippt sich: „Tag 1“. @dein.gym.partner."),
]
SEQ = [dict(name=n, vo=v, hi=hi, chip=("", "white"), visual=vis) for (n, hi, vis), v in zip(_META, _V)]
CAPTION_TEXT = ("Stell dir vor, du ziehst ab heute durch. 💪 Wann fängst du an? Schreib „Tag 1“ 👇 und markier deinen Gym-Partner!"
                " #gym #fitness #motivation #storytime #duform #geschichte #fürdich #fyp")
from timing import seq_bounds as _sb  # noqa: E402
for _s, (_a, _b) in zip(SEQ, _sb()[0]):
    _s["start"], _s["end"], _s["clue"] = round(_a, 1), round(_b, 1), "—"
