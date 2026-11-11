"""'SCHICK DAS DEINEM CHEF' – GTA 6: ein Tag frei am Release-Tag. Video zum Weiterschicken. STIL 3."""
TITLE = "SCHICK DAS DEINEM CHEF"
DURATION = 62.0
_V = [p.strip().replace("\n", " ") for p in open(__file__.replace("script.py", "vo.txt"), encoding="utf-8").read().strip().split("\n\n")]
_META = [
    ("Geschickt", ["Mitarbeiter", "Ende,", "nein"], "1. Sekunde: Trailer + GTA-VI-Logo „FÜR DEINEN CHEF“. Dann: der Chef bekommt ein Video von „Dein Mitarbeiter“ – der Trailer läuft auf dem Handy."),
    ("19. November", ["neunzehnten", "November", "Dreizehn", "Release-Tag."], "Trailer scharf oben, Logo. Kalender 19 NOVEMBER → Zähler 2013→2026 → Urlaubsantrag mit Stempel RELEASE-TAG."),
    ("Kopf in Vice City", ["sowieso", "Vice", "City."], "Er sitzt am Schreibtisch mit leerem Blick. Gedankenblase: der Trailer läuft darin – VICE CITY."),
    ("Abgelenkt", ["Handy.", "Fehlern.", "nichts", "anderes."], "3 Mini-Szenen: Trailer auf dem Handy (9× in 5 Min.) · Mail mit roten Tippfehlern „Herr Vice City“ · Kaffeeküche: Sprechblase mit Trailer, Kollege genervt."),
    ("PAUSE", ["ehrlich.", "Büro?"], "Freeze + Pause-Symbol (einmal kurzer Glitch). Chef schaut: „So einer im Büro?“"),
    ("Sein Angebot", ["frei.", "Stunde", "länger.", "meckern."], "Urlaubsantrag vor dem laufenden Trailer: 4 Häkchen (1 Tag frei · +1 Std. · jeden Tag · ohne Meckern)."),
    ("Zurück", ["Ausgeschlafen.", "Glücklich.", "Motivierter"], "Er läuft strahlend ins Büro, im Fenster läuft Vice City. Stempel: AUSGESCHLAFEN · GLÜCKLICH · MOTIVATION 200 %."),
    ("Abstimmung", ["frei?", "Ja", "Nein", "Kumpel,"], "Chef grübelt, im Fenster das Trailer-Ende mit Logo + Datum. Buttons JA / NEIN, @dein.kumpel."),
]
SEQ = [dict(name=n, vo=v, hi=hi, chip=("", "white"), visual=vis) for (n, hi, vis), v in zip(_META, _V)]
CAPTION_TEXT = ("Schick das deinem Chef. 🎮🌴 Bekommt er am 19.11. frei – JA oder NEIN? 👇 Markier deinen Kumpel, der auch frei braucht!"
                " #gta6 #gtavi #büro #storytime #duform #geschichte #fürdich #fyp")
from timing import seq_bounds as _sb  # noqa: E402
for _s, (_a, _b) in zip(SEQ, _sb()[0]):
    _s["start"], _s["end"], _s["clue"] = round(_a, 1), round(_b, 1), "—"
