"""'FLUG 404 – Teil 2: Schlafen stellen' – STIL 3, Du-Form."""
TITLE = "FLUG 404 – TEIL 2"
DURATION = 63.0
SEQ = [
    dict(name="Ohne Piloten", vo="Du sitzt in einem fliegenden Flugzeug ohne Piloten. Und 187 Passagiere starren dich an.", hi=["Piloten.", "starren"],
         chip=("OHNE PILOTEN", "red"), visual="Kurz das leere Cockpit mit AUTOPILOT, dann die starrende Kabine aus Teil 1."),
    dict(name="Schlafen stellen", vo="Du hast dich entschieden: Du setzt dich hin. Schließt die Augen. Und tust so, als würdest du schlafen.", hi=["Augen.", "schlafen."],
         chip=("SCHLAFEN STELLEN", "white"), visual="Du im Sitz, Platz daneben leer. Du schließt die Augen, das Bild wird dunkler."),
    dict(name="Atmen", vo="Langsam atmen. Nicht bewegen. Nicht blinzeln.", hi=["atmen.", "blinzeln."],
         chip=("NICHT BLINZELN", "red"), visual="Du mit geschlossenen Augen, ruhiges Atmen; Einblendungen ATMEN … / NICHT BEWEGEN / NICHT BLINZELN."),
    dict(name="Schritte", vo="Dann hörst du Schritte im Gang. Sie kommen näher. Und bleiben direkt neben deinem Sitz stehen.", hi=["Schritte", "näher.", "stehen."],
         chip=("SCHRITTE", "white"), visual="Ein Passagier mit starrenden Augen läuft durch den dunklen Gang auf dich zu und bleibt stehen."),
    dict(name="Atem am Ohr", vo="Jemand beugt sich über dich. Du spürst seinen Atem an deinem Ohr.", hi=["beugt", "Atem"],
         chip=("ATEM AM OHR", "red"), visual="Der Passagier beugt sich zu deinem Ohr, Atemlinien, langsamer Zoom."),
    dict(name="Flüstern", vo="Eine Stimme flüstert: Er schläft nicht.", hi=["schläft", "nicht."],
         chip=("ER SCHLÄFT NICHT", "red"), visual="Sprechblase: „Er schläft nicht.“"),
    dict(name="PAUSE", vo="Stopp. Woher wissen sie das?", hi=["Woher"], chip=("", "white"), visual="Freeze mit Pausen-Symbol."),
    dict(name="Ein Auge", vo="Die Schritte gehen weiter. Du öffnest ein Auge. Nur einen Spalt.", hi=["Auge.", "Spalt."],
         chip=("EIN AUGE OFFEN", "white"), visual="Schwarz – dann durch einen schmalen Lidspalt die dunkle Kabine."),
    dict(name="Der Zwilling", vo="Der Platz neben dir ist nicht mehr leer. Dort sitzt jemand. In deinem grünen Pullover. Mit deinem Gesicht.",
         hi=["grünen", "Pullover.", "Gesicht."], chip=("DAS BIST … DU?!", "red"),
         visual="Auge geht auf: neben dir sitzt jemand – grüner Streifenpullover (gelb markiert), dein Gesicht (rot markiert). Du geschockt."),
    dict(name="Übernahme", vo="Er lächelt dich an und sagt: Ich übernehme ab hier.", hi=["übernehme"],
         chip=("„ICH ÜBERNEHME“", "red"), visual="Dein Doppelgänger grinst und spricht. Sprechblase."),
    dict(name="Sturzflug", vo="Dann ruckelt das Flugzeug. Und es geht steil nach unten.", hi=["ruckelt", "steil"],
         chip=("STURZFLUG", "red"), visual="Ruck, das Bild kippt nach vorne, Sauerstoffmasken fallen, Passagiere geschockt, rotes Licht."),
    dict(name="Cliffhanger", vo="Bleibst du sitzen – oder rennst du ins Cockpit? Schreib es in die Kommentare.", hi=["sitzen", "Cockpit?"],
         chip=("STURZFLUG", "red"), visual="Du und dein Doppelgänger nebeneinander, Bild gekippt. Buttons: SITZEN BLEIBEN / INS COCKPIT."),
]
CAPTION_TEXT = ("Teil 2: Du stellst dich schlafend … und neben dir sitzt plötzlich DU. ✈️😨 Sitzen bleiben oder ins Cockpit? 👇 "
                "#flugzeug #mystery #teil2 #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp")
from timing import seq_bounds as _sb  # noqa: E402
for _s, (_a, _b) in zip(SEQ, _sb()[0]):
    _s["start"], _s["end"], _s["clue"] = round(_a, 1), round(_b, 1), "—"
