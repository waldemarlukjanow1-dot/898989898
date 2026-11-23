# PRODUKTIONSSYSTEM – abgeleitet aus den 3 Referenzvideos (siehe `ANALYSE.md`)

Diese Datei lese ich **vor jeder neuen Videoproduktion**. Sie gilt vollständig für Simulations-Videos (STIL 4) und
in Teil B für unsere Du-Geschichten.

---

## Teil A – Simulations-Videos (STIL 4: „Physik-Simulation“)

### A1. Ideen auswählen (Filter)
Eine Idee kommt nur in Produktion, wenn alle fünf Punkte erfüllt sind:
1. **Eine Regel**, die man ohne Text in < 1 s versteht (z. B. „Kiefer beißt → Ball vervielfacht sich“).
2. **Ein Start-Objekt** (1 Ball, 1 Punkt, 1 Würfel). Der Kontrast zum Ende ist die Geschichte.
3. **Sichtbare Steigerung** in Stufen (Anzahl, Fläche, Geschwindigkeit, Farbe).
4. **Ein Ziel oder eine Frage**, die nur das Ende beantwortet.
5. **Ein satisfying Moment** pro Zyklus (Explosion, Einrasten, Kristallpackung, Füllen).

Varianten, die das Format frisch halten, ohne das Set zu wechseln:
- andere Ziele (100.000, „bis der Kreis voll ist“)
- 3 statt 2 Klingen
- Kreis wird zur Sanduhr
- zwei Farben gegeneinander („Rot gegen Blau, wer füllt den Kreis?“)
- Rennen gegen einen Timer

### A2. Die ersten Sekunden (fest)
| Zeit | Muss passieren |
|---|---|
| Bild 1 | Arena, Start-Objekt, Kiefer, Ziel bzw. Hook-Text sind **sofort komplett sichtbar**. Kein Intro, kein Logo, kein Einblenden. |
| 0,6–1,0 s | **Erstes Ereignis** (Biss + Explosion + Schlag). Die Startwinkel der Klingen so setzen, dass sie den Ball sicher erwischen. |
| 1,6–2,5 s | Hook-Text blendet aus (0,2 s Fade). |

**Hook-Text-Formeln** (≤ 5 Wörter, Versalien, fett, weiß, oben bei y≈280):
- Versprechen: **WARTE AUF DIE EXPLOSION…** / **WARTE AUF DAS ENDE…**
- Schätzfrage: **WIE VIELE SIND ES AM ENDE?** (dann **ohne** Zähler, Auflösung am Ende)
- Wette: **SCHAFFT ER 100.000?** / **ROT ODER BLAU?**

### A3. Dramaturgie (Zyklus-Bauplan)
- Ein Zyklus dauert **2,2–2,8 s**: Kiefer nähert sich (~1,5 s, Ton lädt auf), dann **Biss**, dann Bloom (0,4 s, weiß → neue Farbe), dann Ausklang (~1 s).
- Pro Zyklus gibt es **genau eine** neue Information: neue Farbe und neue Zahl „+N“.
- **Beschleunigung:** Drehzahl +1 pro Biss, die Abstände werden ~3 % kürzer.
- **Wachstum:** Jede Explosion muss sichtbar größer sein als die vorige (Faktor ×4 bis ×30). Wenn eine Stufe kleiner ausfällt, wird die Simulation neu gestartet (anderer Seed) und **nicht veröffentlicht**.
- **Länge:** 30–45 s (Referenz 40 s). Das ergibt 12–16 Zyklen. Vor dem Finale kommt eine bewusst längere Anlaufphase (~4 s, das Aufladen wird hörbar dichter).
- **Finale:** der größte Biss, Kreis voll, Zähler erreicht das Ziel (bzw. die Schätzfrage wird mit großer Endzahl aufgelöst). Danach 1–1,5 s Ruhe. Das **letzte Bild ähnelt dem ersten** (leerer Kreis bzw. 1 Ball), damit das Video loopt und nochmal geschaut wird.

### A3b. Früh-Chaos-Kurve (Wunsch 23.11.2026, gilt ab jetzt)
Der Zuschauer muss **in den ersten 6 Sekunden** Chaos und Masse sehen, nicht erst in der Mitte.
- Biss 1 (≤ 1 s): **1 → 80** Bälle. Biss 2: 300. Biss 3: 650. Biss 4 (~6 s): **1.000**. Der Kreis ist sichtbar voller Action.
- Danach gleichmäßig **~+90 Bälle pro Biss** bis zum Ziel (~3.500 bei großen Bällen). Jeder Biss bleibt sichtbar.
- Die ersten 4 Explosionen sind **1,8× wuchtiger** (Bälle fliegen schneller auseinander).
- Code: `sim.hook_targets(n)` statt `gentle_targets`.

### A4. Bildgestaltung (Design-Tokens)
- 1080×1920, **60 fps**, eine statische Einstellung, **keine Schnitte, kein Zoom, kein Wackeln**.
- Hintergrund `#000000` mit radialer Aufhellung zur Mitte (max. `#141418`).
- Kreis: Mittelpunkt (520, 880), Radius 430, Linie 3 px weiß (90 % Deckkraft).
- Klingen:
  - Keil von 0,55 R bis 1,0 R, Metall-Verlauf (`#e8e8ec` → `#8a8a92`), Goldkante `#c9a85a` 2 px
  - Gravur mit unserem Kanalnamen (z. B. „DU-GESCHICHTEN“), Stab zur Nabe 4 px `#2a2a30`, Nabe Ø 18 px
- Bälle: Radius 7–12 px (kleiner, je mehr es werden), Kern 100 % Farbe, Glühen = Weichzeichnung der Kopie mit 35 % Deckkraft, additiv gemischt.
- **Farbleiter** (immer starker Kontrast zur Vorstufe): Magenta `#ff2bd6` → Gelb `#ffe600` → Blau `#3d5cff` → Mint `#5cffc8` → Rosa `#ff7ab8` → Weiß-Violett-Mix.
- Explosion: 0,1 s weiß überstrahlt, dann über 0,4 s auf die Zielfarbe abkühlen, die Bälle fliegen radial mit Streuung auseinander.
- **HUD (minimal):**
  - Hook-Text oben
  - Drehzahl ganz oben (Grau `#5a5a60`, 26 px, gesperrt: „12 U/MIN“)
  - „FOLLOW“ in Grau über dem Kreis
  - Zähler unter dem Kreis: dünne Ziffern 80 px, „/ ZIEL“ in 40 px Grau, blaues „+N“ (`#4aa3ff`) 0,6 s sichtbar, 2 px Fortschrittsbalken
- Schriften dünn und elegant (Inter Light oder Thin für Ziffern, Inter Black nur für den Hook-Text).

### A5. Physik (Simulations-Rezept)
- Schwerkraft nach unten (~900 px/s²), Stoßzahl am Kreis 0,6, Ball-Ball-Kollisionen über ein Raster (Spatial Hash).
- Klingen als dicke Liniensegmente, die die Bälle schieben. Sie drehen **gegenläufig**, ω₀ ≈ 70°/s, nach jedem Biss +6 %.
- **Biss:** Der Winkel zwischen den Klingen ist kleiner als die Klingenbreite. Alle Bälle im Keil davor werden zu neuen Bällen der nächsten Farbe (Faktor k = 6–30, abnehmend mit der Gesamtzahl), mit radialem Impuls.
- Obergrenze ~15.000 sichtbare Bälle. Darüber zählt der Zähler weiter und die Darstellung verdichtet sich zur Kristallpackung.
- Fester Zufalls-Seed. Bei der Vorschau prüfen, dass jede Stufe größer wird.

### A6. Ton (Rezept)
- **Grundton nach Wahl:** (a) **Stille** zwischen den Ereignissen (Spannungs-Variante) oder (b) leises Polster 528 + 264 Hz mit Tremolo 3 Hz bei −30 dB (Entspannungs-Variante). Keine Musik mit Beat.
- **Explosion:**
  - Sinus-Sweep 90 → 35 Hz (0,6 s) plus Rauschstoß (Tiefpass)
  - **absteigender Pfeifton** 1,3 kHz → 660 Hz mit Klingeln bei ~700 Hz
  - Ausklang 1,4 s, Spitze −3 dBFS
  - Lautstärke steigt mit der Stufe (+1 dB pro Stufe, gedeckelt)
- **Kontakte:** kurze Töne 250–900 Hz (Tonhöhe nach Ball-Farbe/Stufe, pentatonisch), Lautstärke ∝ Aufprall, max. 12 gleichzeitig.
- **Masse:** Klicks 2–8 kHz, Dichte ∝ Zahl der Kollisionen, sehr leise.
- **Aufladen:** In den 0,8 s vor dem Biss erzeugen die Kontakte im Keil steigende Töne.
- Gesamt −14 LUFS integriert mit großer Dynamik (Spitzen bis −1 dBTP). Keine Sprache.

### A7. Ende, Interaktion und Teilen
- Ein Finale, das das Versprechen bzw. die Frage einlöst (große Endzahl 1 s stehen lassen).
- Loop: Das letzte Bild ähnelt dem ersten.
- Beschreibung: kurze Mitmach-Frage + 3–5 Hashtags, z. B. „Wie viele hättest du geschätzt? 👇 #physics #simulation #asmr #oddlysatisfying #fyp“.
- Serien-Wiedererkennung: gleiches Set, gleiche Typografie und Klingen-Gravur in jedem Video. Variiert werden nur Farben, Ziel und Hook.

---

## Teil B – Übertragung auf unsere Du-Geschichten (STIL 3)

Die Mechanismen gelten auch dort:
1. **Payoff in ≤ 1 s:** Im ersten Bild passiert bereits das Spektakel (z. B. Wand platzt, Geld fliegt), nicht erst die Erklärung.
2. **Ein sichtbares Ziel oder eine Frage** im Bild, die das Ende beantwortet, etwa ein Zähler „11.000.000 €“ oder „TAG 1 / 365“.
3. **Ereignis-Takt 2,5–4 s:** Jede Szene bringt eine neue, größere Information (Chip ändert sich, Zahl steigt, Wendung).
4. **Steigerung, die man zählen kann:** Zahlen mit „+N“ und Farbwechsel als Stufenanzeige.
5. **Stille als Werkzeug:** vor jedem Twist 0,3–0,6 s fast Stille, dann ein Schlag (Sub-Bass + absteigender Pfeifton).
6. **Minimalistisches HUD:** ein Chip, dünne Zähler-Ziffern, keine überladenen Effekte.
7. **Mitmach-Hook:** Schätz- oder Entscheidungsfrage schon im ersten Satz, Auflösung bzw. Abstimmung am Ende.
8. **Loop:** Der letzte Satz bzw. das letzte Bild führt zum ersten zurück.

---

## Checkliste vor jeder Veröffentlichung

**Hook**
- [ ] Das erste Bild zeigt alles Wichtige, kein Intro.
- [ ] Erstes Ereignis bzw. erster Payoff ≤ 1,0 s.
- [ ] Hook-Text ≤ 5 Wörter, Versprechen, Frage oder Wette.

**Spannung und Tempo**
- [ ] Keine Phase > 3 s ohne sichtbar herannahendes Ereignis.
- [ ] Jede Stufe ist größer als die vorige (Zahl, Fläche, Lautstärke).
- [ ] Beschleunigung spürbar (Drehzahl oder Takt).
- [ ] Ziel oder Frage sichtbar und am Ende aufgelöst.

**Bild**
- [ ] 60 fps (Simulation) bzw. 30 fps (Geschichte), flüssig, kein Ruckeln.
- [ ] Jede Stufe hat eine neue, kontrastreiche Farbe, Glühen und Abkühlen funktionieren.
- [ ] HUD minimal, alles Wichtige innerhalb der Safe-Zone (Aktion in der Mitte).
- [ ] Letztes Bild führt zum ersten zurück (Loop).

**Ton**
- [ ] Stille bzw. Polster als Kontrast, Explosion mit Sub-Bass **und** Pfeifton (Handy-Lautsprecher-Test).
- [ ] −14 LUFS integriert, keine Übersteuerung, Dynamik erhalten.

**Veröffentlichung**
- [ ] Beschreibung mit Mitmach-Frage + 3–5 Hashtags.
- [ ] Ohne Ton angeschaut: Ist alles verständlich?
