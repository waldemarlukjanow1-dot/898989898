"""'FLUG 404 – Teil 3: Ins Cockpit' – STIL 3, Du-Form."""
TITLE = "FLUG 404 – TEIL 3"
DURATION = 63.0
_V = [p.strip() for p in open(__file__.replace("script.py", "vo.txt"), encoding="utf-8").read().strip().split("\n\n")]
_META = [
    ("Hook", ["neunzig", "Sekunden,", "Einzige,"], "Durchs Cockpitfenster rast die Stadt auf dich zu, Höhe fällt, dann du allein stehend in der gekippten Kabine."),
    ("Rennen", ["rennst.", "gleichzeitig."], "Du rennst durch den Gang auf die Kamera zu – alle Passagiere drehen gleichzeitig die Köpfe."),
    ("Cockpit", ["leere", "Pull", "up."], "BAMM – Tür zu. Zwei leere Sitze, rote Lampen, PULL UP! blinkt."),
    ("Das Steuer", ["Steuer.", "Kraft."], "Du im Kapitänssitz, Hände am Steuer: erst Angst, dann ziehst du mit aller Kraft – das Bild dreht sich zurück."),
    ("Abgefangen", ["Nase", "dreihundert"], "Der Horizont wird gerade, die Höhe stoppt bei 300 m. Dein Hinterkopf im Pilotensitz."),
    ("PAUSE", ["Autopiloten"], "Freeze: Anzeige AUTOPILOT: AUS."),
    ("Landebahn", ["Landebahn.", "Nirgendwo."], "Lichterreihen einer Landebahn im Dunkeln. Einblendung: KEIN FLUGHAFEN."),
    ("Landung", ["landest.", "Traum."], "Aufsetzen mit Ruck, KREISCH! – dann wird das Bild weich und hell wie in einem Traum."),
    ("Leer", ["leer.", "weg."], "Du drehst dich um: Die Kabine ist komplett leer."),
    ("Platz 32B", ["Du.", "klatscht."], "Nur auf Platz 32B sitzt einer – du – und klatscht."),
    ("Cliffhanger", ["gerettet", "wollten?"], "Du und dein Doppelgänger. Buttons: GERETTET / REINGELEGT."),
]
SEQ = [dict(name=n, vo=v, hi=hi, chip=("", "white"), visual=vis) for (n, hi, vis), v in zip(_META, _V)]
CAPTION_TEXT = ("Teil 3: Kein Pilot. 90 Sekunden. Nur du. ✈️🔥 Hast du das Flugzeug gerettet – oder wurdest du reingelegt? 👇 "
                "#flugzeug #mystery #teil3 #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")
from timing import seq_bounds as _sb  # noqa: E402
for _s, (_a, _b) in zip(SEQ, _sb()[0]):
    _s["start"], _s["end"], _s["clue"] = round(_a, 1), round(_b, 1), "—"
