"""'5 FEHLER, WARUM DU IM GYM KEINE MUSKELN BEKOMMST' – Du-Form, STIL 3, athletische Figur."""
TITLE = "5 FEHLER IM GYM"
DURATION = 62.0
_V = [p.strip().replace("\n", " ") for p in open(__file__.replace("script.py", "vo.txt"), encoding="utf-8").read().strip().split("\n\n")]
_META = [
    ("3 Monate, 0 %", ["drei", "Monaten.", "nichts", "Warum?"], "Schock-Frame: rot, DU MACHST ES FALSCH. Dann: du vor dem Spiegel, Bizeps zeigen – im Spiegel immer noch dünn. MUSKELN: 0, großes rotes ?"),
    ("Fehler 1", ["Brust", "Arme.", "Beine?", "Glühbirne", "Streichhölzern."], "Riesiger Oberkörper auf Streichholzbeinen. BRUST + ARME / BEINE: NIE (Beine rot eingekreist). Daneben schwebt eine Glühbirne auf zwei Streichhölzern ein: „=“."),
    ("Fehler 2", ["zu", "viel", "Gewicht.", "Rücken"], "Langhantel mit 200 KG, du wackelst immer stärker, rote Schmerz-Blitze am Rücken: AUA!"),
    ("Fehler 3", ["anderes", "Plan.", "einstellen"], "Kalender „DEIN PLAN?“ füllt sich: Yoga, Boxen, Bizeps, Spinning, Bizeps → rot durchgestrichen. Du schaust verwirrt, Fragezeichen."),
    ("Fehler 4", ["hart.", "Banane.", "war's."], "Erst Schweißtropfen: HART TRAINIERT. Dann leerer Teller, nur eine Banane: NUR 1 BANANE = 0 EIWEISS."),
    ("PAUSE", ["größte", "Fehler.", "alle."], "Freeze + Pause-Symbol (einmal kurz). Du schaust geschockt: DER GRÖSSTE FEHLER – fast alle."),
    ("Fehler 5", ["drei", "Wochen", "hörst", "auf.", "anfängt."], "Fortschrittsbalken MUSKELN lädt bis 95 % – du gehst traurig zur Tür AUSGANG. „Du warst fast da.“"),
    ("Dranbleiben", ["langsam.", "wachsen.", "bleibst."], "Gleiche Szene, du bleibst: Balken 100 %, die Figur wird Stück für Stück breiter → Bizeps. DRANBLEIBEN."),
    ("Abstimmung", ["Fehler", "Nummer", "Gym-Partner,", "Arme"], "Du zeigst in die Kamera, Buttons 1–5 leuchten nacheinander, @dein.gym.partner."),
]
SEQ = [dict(name=n, vo=v, hi=hi, chip=("", "white"), visual=vis) for (n, hi, vis), v in zip(_META, _V)]
CAPTION_TEXT = ("5 Fehler, warum du im Gym keine Muskeln bekommst. 💪 Welchen hast du schon gemacht? Schreib die Nummer 👇"
                " #gym #fitness #gymtipps #storytime #duform #geschichte #fürdich #fyp")
from timing import seq_bounds as _sb  # noqa: E402
for _s, (_a, _b) in zip(SEQ, _sb()[0]):
    _s["start"], _s["end"], _s["clue"] = round(_a, 1), round(_b, 1), "—"
