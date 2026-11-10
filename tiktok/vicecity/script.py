"""'VICE CITY – 02:43' – STIL 3, Du-Form, eigene Optik (keine Spiel-Logos)."""
TITLE = "VICE CITY – 02:43"
DURATION = 63.0
_V = [p.strip() for p in open(__file__.replace("script.py", "vo.txt"), encoding="utf-8").read().strip().split("\n\n")]
_META = [
    ("02:43", ["Vice", "City.", "Lamborghini."], "Neon-Stadt mit Palmen, gelber Sportwagen, du am Steuer. Einblendung 3 × PROJEKT 6."),
    ("Die Festplatten", ["teuerste", "Videospiel"], "Rückbank: drei leuchtende Festplatten P6, UNVERÖFFENTLICHT."),
    ("Der Deal", ["zehn", "Millionen", "Privatjet"], "Handy: 10.000.000 $ zählt hoch, Freundin am Flughafen, PRIVATJET BEREIT."),
    ("Die Warnung", ["niemandem.", "Freundin."], "Du am Steuer, Nachricht: „Vertrau niemandem. Auch nicht deiner Freundin.“"),
    ("Rückspiegel", ["Blaulicht.", "zehn."], "Rückspiegel: 1 → 3 → 10 Blaulichter. Chip POLIZEI zählt mit."),
    ("Vollgas", ["Gas.", "Zweihundertvierzig."], "Seitenansicht, Tacho springt auf 200 → 240, Polizei hinter dir."),
    ("PAUSE", ["gefunden?"], "Freeze mit Pausen-Symbol."),
    ("Hubschrauber", ["Hubschrauber", "Straßensperre"], "Hubschrauber mit Suchscheinwerfer auf dein Auto, Straßensperre vorne."),
    ("Bauzaun", ["Lenkrad", "Landebahn."], "KRACH durch den Bauzaun – dann auf der Landebahn."),
    ("Der Jet", ["Privatjet.", "Steig"], "Privatjet mit laufenden Triebwerken, Freundin winkt: „Steig ein!“"),
    ("50 Meter", ["fünfzig", "Polizei"], "Dein Auto rast auf den Jet zu, Polizei dicht dahinter."),
    ("Cliffhanger", ["ein", "weiter?"], "Du am Steuer, entschlossen. Buttons: EINSTEIGEN / WEITERFAHREN."),
]
SEQ = [dict(name=n, vo=v, hi=hi, chip=("", "white"), visual=vis) for (n, hi, vis), v in zip(_META, _V)]
CAPTION_TEXT = ("02:43 Uhr. Vice City. Auf deinem Rücksitz: das teuerste Videospiel der Welt. 🚗💨 Einsteigen oder weiterfahren? 👇 "
                "#gta6 #vicecity #verfolgungsjagd #storytime #duform #geschichte #spannung #fürdich #fyp")
from timing import seq_bounds as _sb  # noqa: E402
for _s, (_a, _b) in zip(SEQ, _sb()[0]):
    _s["start"], _s["end"], _s["clue"] = round(_a, 1), round(_b, 1), "—"
