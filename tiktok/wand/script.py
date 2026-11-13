"""'11 MILLIONEN IN DER WAND' – Du-Geschichte mit Twists. STIL 3."""
TITLE = "11 MILLIONEN IN DEINER WAND"
DURATION = 62.0
_V = [p.strip().replace("\n", " ") for p in open(__file__.replace("script.py", "vo.txt"), encoding="utf-8").read().strip().split("\n\n")]
_META = [
    ("11 Millionen", ["Wand", "elf", "Millionen", "schläfst", "daneben."], "Schock-Frame: Die Wand platzt auf, Geld fliegt, 11.000.000 €. Dann: Röntgenblick in deine Wand – Geldbündel. Du schläfst direkt daneben, SEIT 3 JAHREN."),
    ("Der Nagel", ["Nagel.", "Bild", "hohl.", "bohrst.", "Geldschein"], "Du willst ein Bild aufhängen → die Wand klingt HOHL? → Bohrer, Risse → ein Geldschein fällt aus dem Loch: GELD?!"),
    ("Die Bündel", ["Tapete", "Bündel.", "Hunderte.", "Nacht.", "Millionen"], "Tapete reißt, die Wand ist voller Bündel, Geldberg am Boden. Nacht: Zähler läuft bis 11.000.000 €."),
    ("Der Zettel", ["Zettel:", "anfassen.", "zurück.", "morgen."], "Gelber Zettel auf den Bündeln: NICHT ANFASSEN. WIR KOMMEN ZURÜCK. DATUM: 14.11. → = MORGEN!"),
    ("PAUSE", ["überleg", "gewohnt?"], "Freeze + Pause-Symbol (einmal kurz). Du grübelst: WER WOHNTE VOR DIR HIER?"),
    ("Der Vormieter", ["Bankraub,", "Beute:", "gefunden.", "Vormieter."], "Laptop: BANKRAUB IN DEINER STRASSE · 11 MIO. € · NIE GEFUNDEN. Dann RÜCKBLENDE (Sepia): der VORMIETER trägt einen Geldsack in deine Wohnung."),
    ("Es klingelt", ["klingelt", "Zweimal.", "Spion", "Schlüssel", "Wohnung."], "DING DONG ×2 an deiner Tür. Durch den Spion (runder Fischaugen-Blick): der Vormieter hält einen Schlüssel hoch – DEIN SCHLÜSSEL."),
    ("Abstimmung", ["Polizei?", "Geld", "verschwindest?"], "Du zwischen Handy (110) und Geldsack, Buttons POLIZEI / GELD NEHMEN."),
]
SEQ = [dict(name=n, vo=v, hi=hi, chip=("", "white"), visual=vis) for (n, hi, vis), v in zip(_META, _V)]
CAPTION_TEXT = ("11 Millionen in deiner Wand – und morgen kommen sie zurück. 💰🚪 Polizei oder Geld nehmen? 👇"
                " #geld #millionen #wohnung #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")
from timing import seq_bounds as _sb  # noqa: E402
for _s, (_a, _b) in zip(SEQ, _sb()[0]):
    _s["start"], _s["end"], _s["clue"] = round(_a, 1), round(_b, 1), "—"
