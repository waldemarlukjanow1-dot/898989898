# Bounce 2.0 – Ergebnisse der 5 Testvideos (24.11.2026)

Alle Videos: 1080×1920, **60 fps**, exakt **8,000 s**, −13,8 bis −14,4 LUFS, nahtloser Loop, keine Schrift.
Gerendert mit dem eigenen 3D-Raytracer (`rt.py`). Ton per Modalsynthese aus dem Material (`kit.py`). Methode: `SYSTEM.md`.

## Video 1 – „Kristall“ (`output/bounce1_kristall.mp4`)
- **Beschreibung:** Eine aquamarinfarbene Glaskugel springt exakt 1-mal pro Sekunde, die Kamera umkreist sie in 8 s genau einmal.
- **Material:** Glas (Brechungsindex 1,52, Fresnel, Absorption), dazu ein Kaustik-Lichtfleck auf dem Boden.
- **Physik:** konstante Sprunghöhe, Squash 16 % bei der Landung, leichtes Strecken im Flug.
- **Kamera:** Orbit 360°, Abstand 5,4, leicht erhöht.
- **Umgebung:** schwarzer Schachbrett-Spiegel, pastellfarbener Horizontring, 4 farbige Softboxen.
- **Ton:** Glas-Modalsynthese („ting“), ruhige 8-Ton-Melodie, das Panorama folgt der Kamera.
- **Was satisfying ist:** Das Schachbrett erscheint in der Kugel gebrochen und auf dem Kopf, die Horizontfarbe wandert, alles im gleichmäßigen Puls.
- **Neue Technik:** Brechung, Fresnel und Kaustik, Kamerafahrt.
- **Erkenntnis:** Glas wirkt nur mit Struktur dahinter. Vor Schwarz sieht es aus wie eine dunkle Kugel. Das Schachbrett war die Lösung.

## Video 2 – „Accelerando“ (`output/bounce2_accelerando.mp4`)
- **Beschreibung:** Eine rote Keramikkugel im weißen Studio springt mit jedem Mal niedriger und schneller (30 Aufpralle). Kurz vor dem Stillstand schleudert eine Druckwelle sie zurück auf die Starthöhe.
- **Material:** Keramik mit Klarlack (Glanzlicht + Spiegelung).
- **Physik:** Stoßzahl e = 0,82. Sprungzeiten schrumpfen geometrisch, die Summe der Reihe ist exakt so gewählt, dass der Loop bei 8 s schließt.
- **Kamera:** Seitenansicht, statisch, auf Augenhöhe der Mitte.
- **Umgebung:** weißer Raum mit weichem Schlagschatten.
- **Ton:** Keramik-„Tock“, jeder Aufprall eine Stufe höher (Dur-Tonleiter, über 4 Oktaven). Zum Schluss ein Summen, dann ein Whoomp mit Akkord.
- **Was satisfying ist:** der beschleunigende, steigende Klang. Man *hört* die Physik und wartet auf den Neustart.
- **Neue Technik:** heller Raum, Bounce-Muster als geometrische Reihe, Musik aus der Physik.
- **Erkenntnis:** Am stärksten wirkt die Kopplung von Ton und Bewegung.

## Video 3 – „Bounce-Welle“ (`output/bounce3_welle.mp4`)
- **Beschreibung:** 9 bunte Keramikkugeln im Kreis. Kugel i springt in 8 s genau (4+i)-mal. Am Anfang und am Ende landen alle gleichzeitig, dazwischen entstehen Wendeltreppen und Wellen.
- **Material:** glänzende Keramik in 9 Farben.
- **Physik:** Sprunghöhe ~ Periode², höchste Kugel hinten (2,6 Einheiten) bis zur flachsten (0,29).
- **Kamera:** schräg von oben, pendelt langsam ±13°.
- **Umgebung:** nasser dunkler Boden mit Spiegelung.
- **Ton:** jede Kugel ein Kalimba-Ton (Pentatonik) + Keramik-Klick. Bei 0 s und 8 s erklingen alle als Akkord.
- **Was satisfying ist:** Ordnung, Chaos, wieder Ordnung, und man versteht das Muster.
- **Neue Technik:** mehrere Bälle mit mathematischer Synchronisation (Prinzip der Pendel-Welle auf Bounces übertragen).
- **Erkenntnis:** Bei 9:16 müssen mehrere Bälle in die Tiefe angeordnet werden (Kreis), nicht nebeneinander.

## Video 4 – „Bodenkamera“ (`output/bounce4_bodenkamera.mp4`)
- **Beschreibung:** Die Kamera liegt 14 cm über einem nassen schwarzen Boden. Eine schwere Goldkugel kracht direkt vor der Linse auf: BUMM, tick.
- **Material:** Gold-Spiegel.
- **Physik:** schwere Kugel, großer Sprung 1,5 s, kleines Nachhüpfen 0,5 s, Squash 20 % bzw. 10 %.
- **Kamera:** Froschperspektive, 66° Weitwinkel, Tiefenunschärfe mit Fokus auf der Kugel, langsame periodische Bewegung.
- **Umgebung:** Neon-Seitenlichter magenta und cyan, warmes Licht von oben, Horizont-Glühen.
- **Ton:** Metall (Glocken-Moden) + Sub-Boom, Nachhüpfer heller und leiser.
- **Was satisfying ist:** Wucht und Gewicht, dazu eine edle Spiegelung.
- **Neue Technik:** Bodenperspektive und Tiefenunschärfe.
- **Erkenntnis:** Spiegelnde Materialien brauchen eine helle Umgebung. Die große Lichtquelle oben ist als Fleck sichtbar und lenkt etwas ab. Nächstes Mal sollte sie außerhalb des Bildes liegen.

## Video 5 – „Endlose Treppe“ (`output/bounce5_endlose_treppe.mp4`)
- **Beschreibung:** Eine Chromkugel hüpft eine unendliche Treppe aus schwebenden Pastell-Blöcken hinunter, die Kamera fliegt hinterher.
- **Material:** Chrom, das die bunten Stufen spiegelt.
- **Physik:** 2 Hüpfer pro Sekunde, eine Stufe pro Hüpfer, exakte Parabeln zwischen den Stufen.
- **Kamera:** Verfolgung von oben hinten, gleitet mit konstanter Geschwindigkeit.
- **Umgebung:** schwebende Blöcke, Pastell-Himmel mit Sonne.
- **Ton:** Shepard-Töne, die mit jeder Stufe 1/8 Oktave tiefer klingen. Eine Tonleiter, die *endlos* fällt.
- **Was satisfying ist:** Bewegung, die nie aufhört, im Bild wie im Ton.
- **Neue Technik:** prozedurale unendliche Geometrie, Verfolgungskamera, Shepard-Illusion.
- **Erkenntnis:** Die Bildwirkung ist eher traumhaft als knackig. Die Treppe liest sich teils als Streifen. Seitenkanten und Schatten müssten stärker sein.

## Bewertungen (eigene Einschätzung 1–10, keine echten TikTok-Daten)

| Video | Bildqualität | Physik | Satisfying | Ton | Loop | Kreativität | TikTok |
|---|---|---|---|---|---|---|---|
| 1 Kristall | 8 | 8 | 7 | 8 | 10 | 7 | 7 |
| 2 Accelerando | 8 | 9 | 9 | 9 | 9 | 8 | 9 |
| 3 Bounce-Welle | 7 | 9 | 9 | 8 | 10 | 8 | 8 |
| 4 Bodenkamera | 7 | 7 | 7 | 8 | 10 | 7 | 7 |
| 5 Endlose Treppe | 6 | 7 | 7 | 9 | 10 | 9 | 8 |

**Empfehlung:** Video 2 und Video 3 zuerst posten. Beide verbinden präzise Physik mit hörbarer Mathematik.

## Selbstkontrolle (geprüft an den fertigen MP4-Dateien)
- Alle Dateien exakt 8,000 s, 1080×1920, 60 fps. Loops geprüft (Video 1, 3, 4: periodisch; Video 2: Start = Apex = Ende; Video 5: Bild 0 = Bild 480, rechnerisch identisch).
- Bekannte Schwächen:
  - leichtes Treppchen an Kanten (kein Supersampling)
  - Glas-Kaustik ist ein Näherungsfleck
  - Lichtquelle in Video 4 im Bild
  - Treppe in Video 5 liest sich teils als Streifen
  - keine echte Bewegungsunschärfe
