"""'VICE CITY – 02:43' – STIL 3, Du-Form, eigene Optik (keine Spiel-Logos)."""
TITLE = "VICE CITY – 02:43"
DURATION = 63.0
_V = [p.strip() for p in open(__file__.replace("script.py", "vo.txt"), encoding="utf-8").read().strip().split("\n\n")]
_META = [
    ("02:43", ["Vice", "City.", "Lamborghini."], "Neon-Stadt, gelber Sportwagen fährt, du nur im Seitenfenster sichtbar. Einblendung 3 × GTA6 FESTPLATTEN."),
    ("Die Festplatten", ["teuerste", "Videospiel"], "Rückbank: drei Festplatten „GTA6 FESTPLATTE“, Stempel TOP SECRET."),
    ("Der Deal", ["zehn", "Millionen", "Privatjet"], "Handy: 10.000.000 $ zählt hoch, Freundin am Flughafen, PRIVATJET BEREIT."),
    ("Die Warnung", ["niemandem.", "Freundin."], "Du am Steuer, Nachricht: „Vertrau niemandem. Auch nicht deiner Freundin.“"),
    ("Rückspiegel", ["Blaulicht.", "zehn."], "Rückspiegel: 1 → 3 → 10 Blaulichter. Chip POLIZEI zählt mit."),
    ("Vollgas", ["Gas.", "Zweihundertvierzig."], "Auto rast, großer Tacho zeigt 120 → 200 → 240 km/h, Polizei hinter dir."),
    ("PAUSE", ["gefunden?"], "Freeze mit Pausen-Symbol."),
    ("Hubschrauber", ["Hubschrauber", "Straßensperre"], "Hubschrauber mit Suchscheinwerfer auf dein Auto, Straßensperre vorne."),
    ("Lenkrad", ["Lenkrad", "Landebahn."], "Du reißt das Lenkrad herum – dann rast dein Auto direkt über die Landebahn."),
    ("Der Jet", ["Privatjet.", "Steig"], "Privatjet mit laufenden Triebwerken, Freundin winkt: „Steig ein!“"),
    ("50 Meter", ["fünfzig", "Polizei"], "Dein Auto rast auf den Jet zu, Polizei dicht dahinter."),
    ("Cliffhanger", ["Ablenkung", "einsteigen?"], "Du am Steuer, entschlossen. Buttons: ABLENKEN / EINSTEIGEN."),
]
SEQ = [dict(name=n, vo=v, hi=hi, chip=("", "white"), visual=vis) for (n, hi, vis), v in zip(_META, _V)]
CAPTION_TEXT = ("02:43 Uhr. Vice City. Auf deinem Rücksitz: das teuerste Videospiel der Welt. 🚗💨 Für Ablenkung sorgen oder einsteigen? 👇 "
                "#gta6 #vicecity #verfolgungsjagd #storytime #duform #geschichte #spannung #fürdich #fyp")
from timing import seq_bounds as _sb  # noqa: E402
for _s, (_a, _b) in zip(SEQ, _sb()[0]):
    _s["start"], _s["end"], _s["clue"] = round(_a, 1), round(_b, 1), "—"
