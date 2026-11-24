# Ball Bounce 2.0 – neues Produktionssystem (24.11.2026)

Ordner: `tiktok/bounce2/` (komplett getrennt, alte Projekte unverändert).
Code: `rt.py` (3D-Raytracer), `kit.py` (Physik, Klang, Tiefenunschärfe), `v1_…py` bis `v5_…py` (je ein Video).
Videos: `output/bounce1_…mp4` bis `output/bounce5_…mp4`. Bild- und Ton-Rendering mit `python3 vN_….py`.

## Phase 1 – Analyse der bisherigen Ball-Videos (sim v1–v8, Experimente)

| Aspekt | Bisher | Bewertung |
|---|---|---|
| Darstellung | 2D, flache Neon-Kreise mit Glühen (PIL), kein Material, keine Schatten | Tiefe und Material fehlen, „Spiel-Look“ |
| Perspektive | immer Draufsicht, statische Kamera, Kreis-Arena mittig | sehr repetitiv |
| Bälle | tausende kleine identische Punkte | Masse statt Einzelball-Qualität |
| Physik | Verlet + PBD, Schwerkraft nach unten, Klingen schieben | glaubwürdig, aber ohne Squash, Rotation oder Elastizität |
| Rhythmus | Biss alle 1,8–2,6 s bzw. Kicks des Beats | gut, aber immer dasselbe Ereignis (Explosion) |
| Ton | Synth-Bass, Plopp, Miau, Beats | nicht an Material und Aufprall gekoppelt |
| Loop | Implosion → 1 Ball → Start | funktioniert, aber jedes Mal derselbe Trick |
| Hintergrund | schwarz | nie hell, nie Raum, nie Boden |

**Zu oft verwendet:** Kreis-Arena, Draufsicht, Neon auf Schwarz, „1 → viele“, Implosions-Loop.
**Nie getestet:** echte Materialien (Glas, Metall, Keramik), Licht und Schatten, Kamerafahrt, Bodenperspektive,
helle Räume, einzelne Bälle in Großaufnahme, Squash & Stretch, materialgetreuer Klang.

## Phase 2 – Die neue Produktionslogik

Bounce 2.0 plant ein Video über **fünf Achsen**, die unabhängig kombiniert werden. So entstehen viele Videos, ohne dass sie sich wie Kopien anfühlen:

1. **Material** (`rt.Ball(mat=…)`): glass, chrome, gold, ceramic, rubber, plus Boden: mirror, wet, matte, Treppe.
2. **Bounce-Muster (Timing zuerst):** Zuerst werden die **Aufprall-Zeitpunkte** festgelegt (Taktraster, geometrische Reihe,
   Zählmuster), dann füllt `kit.hop()` exakte Wurfparabeln dazwischen. So ist das Timing immer präzise und loopfähig.
3. **Kamera:** Orbit, Froschperspektive mit Tiefenunschärfe, schräg von oben, Verfolgungsfahrt. Die Kamerabewegung ist immer periodisch zur Videolänge.
4. **Umgebung/Licht:** Studio-Umgebung mit Softboxen (Reflexionen), Horizont-Ringe, weißer Raum, Neon-Seitenlichter, Pastell-Himmel.
5. **Klang = Physik:** Jeder Aufprall erzeugt seinen Ton per **Modalsynthese** aus dem Material (Eigenfrequenz-Verhältnisse
   und Dämpfung von Glas, Keramik, Metall, Gummi), die Lautstärke folgt der Aufprallgeschwindigkeit. Musikalische Ebene: Tonhöhen
   folgen Tonleitern bzw. Shepard-Skalen.

**Loop-Regeln:** Länge = ganzzahliges Vielfaches aller Perioden (Bounce, Kamera, Farbzyklus). Der Ton läuft in einem Ringpuffer,
Nachklänge laufen also in den Anfang hinein. Der Loop wird jedes Mal geprüft (Bild 0 gegen Bild N).

## Phase 8 – Technischer Workflow

- **Warum kein KI-Video-Modell und kein Blender:** In dieser Umgebung gibt es keine generativen Videomodelle. Blender/Cycles
  würde ohne GPU mehrere Minuten pro Bild brauchen. Deshalb ein **eigener vektorisierter Raytracer** (NumPy). Für Ball-Videos ist das ideal:
  Kugeln und Ebenen werden *exakt* geschnitten, die Physik ist analytisch, und es gibt keine KI-Artefakte und keine deformierten Bälle.
- **Raytracer-Funktionen:** Ellipsoide (Squash & Stretch), Fresnel, Brechung mit Totalreflexion (Glas), Spiegelung (Chrom/Gold),
  Klarlack (Keramik), weiche Kugel-Schatten und Ambient Occlusion (analytisch), Kaustik-Fleck unter Glas, Schachbrett-Boden mit
  Entfernungs-Fade gegen Moiré, Treppe aus schwebenden Blöcken, Tonemapping + Gamma 2.2.
- **Post:** Tiefenunschärfe aus dem Tiefenpuffer (`kit.depth_of_field`).
- **Ausgabe:** 1080×1920, **60 fps**, exakt 8,000 s, H.264 10–14 Mbit/s, AAC 192 kbit/s, −14 LUFS.
- **Renderzeit:** ca. 3–10 s pro Bild (CPU), 4 Prozesse parallel, also ca. 10–20 min pro Video.

## Einstellungen der 5 Videos (Kurzfassung)

| Video | Material | Physik | Kamera | Umgebung | Ton |
|---|---|---|---|---|---|
| 1 Kristall | Glas IOR 1,52, aquamarin | 1 Bounce/s, Squash 16 % | Orbit 360° in 8 s, r = 5,4 | schwarzer Schachbrett-Spiegel, Pastell-Horizontring, 4 Softboxen, Kaustik | Glas-Modalsynthese, Pentatonik |
| 2 Accelerando | Keramik rot | Stoßzahl e = 0,82, 30 Aufpralle, Reihe endet bei 7,28 s, Druckwelle startet neu | Seitenansicht, statisch | weißer Studio-Raum, weiche Schatten | Keramik-„Tock“, Dur-Tonleiter aufwärts + Start-Whoomp |
| 3 Bounce-Welle | Keramik, 9 Farben | Kugel i: 4+i Sprünge in 8 s, Höhe ~ T² | schräg von oben, langsames Pendeln | nasser dunkler Boden | Kalimba-Pentatonik pro Kugel |
| 4 Bodenkamera | Gold (Spiegel) | BUMM 1,5 s + tick 0,5 s | 14 cm über dem Boden, 66° Weitwinkel, Tiefenunschärfe | nasser schwarzer Boden, Neon magenta/cyan | Metall-Glockenmoden + Sub-Boom |
| 5 Endlose Treppe | Chrom | 2 Hüpfer/s, eine Stufe pro Hüpfer | Verfolgung von oben/hinten | schwebende Pastell-Blöcke, Himmel | Shepard-Töne, 1/8 Oktave tiefer pro Stufe |
