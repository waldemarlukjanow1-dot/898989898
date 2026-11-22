# Referenz-Analyse: 3 virale Physik-Simulationen („Hypnoball“)

Analysiert am 22.11.2026. Quelle: drei Bildschirmaufnahmen des Nutzers von TikTok-Videos des Kanals **Hypnoball**.

| Datei | Länge der Aufnahme | Hook-Text | Likes | Kommentare | Merken | Teilen | Alter |
|---|---|---|---|---|---|---|---|
| `video1_attends_lexplosion.mp4` | 5,78 s | „ATTENDS L'EXPLOSION…“ (Warte auf die Explosion…) | 34.851 | 122 | 2.317 | 4.279 | 12 Tage (11-10) |
| `video2_tu_dis_combien.mp4` | 7,62 s | „TU DIS COMBIEN À LA FIN ?“ (Wie viele, schätzt du, am Ende?) | 39.158 | 124 | 2.413 | 5.254 | 15 Tage (11-7) |
| `video3_la_machoire.mp4` | 7,99 s | kein Hook-Text | 1.158 | 10 | 116 | 145 | 18 Stunden |

**Methode:** Alle Videos sind mit 60 fps aufgenommen (1206×2622, Ton AAC Stereo). Ich habe jedes Video Bild für Bild mit
10 Bildern pro Sekunde über die gesamte Länge durchgesehen und Schlüsselmomente in voller Auflösung geprüft. Dazu kamen
Lautheit (EBU R128), Lautstärkeverlauf alle 100 ms, Einsatzzeiten (Onsets), dominante Frequenzen alle 0,5 s, Spektrogramme
und eine Spracherkennung (Whisper). Alle Belegbilder liegen in `analyse/`.

**Grenze der Analyse (ehrlich):** Die Aufnahmen zeigen nur die **ersten 5,8–8 Sekunden** der Videos. Video 2 zeigt im
ersten Bild die Gesamtlänge **0:40**. Wie die Videos enden, ob das Ziel (45.000 / 60.000) erreicht wird und ob es einen Loop
gibt, ist in den Dateien **nicht zu sehen**. Darüber sage ich unten nichts als Tatsache. Die Bedeutung der großen
Umriss-Zahlen oben im Bild (siehe 1.4) ist nicht eindeutig ablesbar.

---

## 1. Einzelanalyse Video 1 – „ATTENDS L'EXPLOSION…“

### 1.1 Ablauf (gemessen)
| Zeit | Bild | Ton |
|---|---|---|
| 0,00 | Schwarzer Hintergrund, dünner weißer Kreis (~88 % der Bildbreite), in der Mitte eine Nabe, 2 silberne Klingen mit Goldkante und eingraviertem „HYPNOBALL“. **Ein einzelner magentafarbener Ball** oben. Text oben: „ATTENDS L'EXPLOSION…“. Zähler unten: **1 / 45000**. | **Totale Stille** (−120 dB) |
| 0,00–0,66 | Die zwei Klingen schließen sich wie ein **Kiefer** genau dort, wo der Ball ist. | Stille |
| **0,66** | **Biss → Explosion:** Der Ball wird gelb, zerfällt in viele Bälle, weißes Aufglühen (Bloom). Zähler **30 / 45000** + blaues „+29“. Große Zahl oben: „10“. | **Bass-Schlag** (−8 dB, Sub-Bass 20–100 Hz + absteigender Pfeifton ~1,3 kHz → 660 Hz), Ausklang 1,4 s |
| 0,7–2,9 | Die gelbe Wolke fällt nach unten (Schwerkraft) und verteilt sich. Die Klingen drehen weiter. Hook-Text blendet bei 1,6–1,8 s aus. | Ausklang, dann ab 2,1 s **wieder Stille** |
| **2,96** | Die Klingen fangen ~30 gelbe Bälle unten links → Explosion in **Magenta**, Zähler **215** (+185). Oben eine große, überlappende Umriss-Zahl. | Bass-Schlag + Pfeifton (−7 dB), Ausklang bis 4,5 s |
| 3,3–5,1 | Magenta-Wolke füllt das obere rechte Viertel, die Klingen fegen hindurch. | Stille ab 4,6 s |
| **5,18–5,3** | Biss auf eine dichte Magenta-Packung → **weiß-glühende Explosion**, Farbe kühlt zu Blau/Violett mit bunten Einsprengseln, Kreis zu ~2/3 gefüllt. Zähler **1397** (+1182). | Doppelter Schlag (5,18 + 5,30) |
| 5,78 | Ende der Aufnahme (Video läuft weiter). | |

### 1.2 Hook (0–1 s)
- **Text-Versprechen** „Warte auf die Explosion…“: Es nennt das Ereignis, auf das man wartet. Die drei Punkte erzeugen offene Spannung.
- **Ein einzelner Ball in einer leeren Arena:** maximal einfach, man erfasst sofort, worauf man achten muss.
- **Zähler „1 / 45000“:** Das Ziel ist absurd groß gegenüber dem Start und damit sofort eine Frage: *Wie soll aus 1 Ball 45.000 werden?*
- **Erste Belohnung nach 0,66 s:** Das Versprechen wird sofort teilweise eingelöst. Der Zuschauer lernt die Regel (Kiefer schließt → Explosion → mehr Bälle) und will die **größere** Explosion sehen.

### 1.3 Spannung und Rhythmus
- Explosionen bei **0,66 / 2,96 / 5,18 s**, also etwa alle **2,3 s**. Die Abstände werden leicht kürzer (2,30 → 2,22 s).
- Das Wachstum ist exponentiell: 1 → 30 → 215 → 1397 (×30, ×7, ×6,5). Jede Explosion ist sichtbar **größer** als die vorige.
- **Stille zwischen den Schlägen:** Der Ton ist zwischen den Explosionen komplett aus. Dadurch wirkt jeder Schlag doppelt so stark, und das Warten wird selbst zur Spannung.
- **Drehzahl-Anzeige** (dezent oben): 13 → 14 → 15 TR/MIN. Nach jeder Explosion wird die Szene schneller, ein eingebauter Beschleuniger.

### 1.4 Visuelles
- **Farbe als Generationsanzeige:** magenta → gelb → magenta → weiß-glühend → blau/violett. Jede neue Farbe zeigt sofort *„neue Stufe“*.
- **Bloom/Glühen:** Explosionen starten weiß-überstrahlt und „kühlen“ in die neue Farbe ab. Das wirkt energiegeladen und hochwertig.
- **Große dünne Umriss-Zahlen** oben, die bei Explosionen erscheinen: „10“, dann mehrere Zahlen übereinander (wirken wie flackernde Tausender). Was sie bedeuten, ist nicht ablesbar. Sie vermitteln aber „hier passiert gerade viel“.
- **Zähler:** große, dünne, weiße Zahl + kleines „/ 45000“ + blaues „+N“ (sichtbar ~0,6 s) + dünner Fortschrittsbalken darunter.
- **„FOLLOW“** als leise graue Aufforderung direkt über dem Kreis. Sie sitzt permanent im Blickfeld, ohne zu stören.
- Kamera: **komplett statisch, ein einziger Take, kein Schnitt, kein Zoom.**

---

## 2. Einzelanalyse Video 2 – „TU DIS COMBIEN À LA FIN ?“

### 2.1 Ablauf (gemessen)
| Zeit | Bild | Ton |
|---|---|---|
| 0,00 | Gleiches Set: Kreis, zwei weiß-silberne Klingen (ohne Goldkante), ein **Magenta-Ball**. Text: „TU DIS COMBIEN À LA FIN ?“. Wasserzeichen **@hypnoball** statt FOLLOW. **Kein Zähler** sichtbar. Player-Zeit „00:00 / 00:40“. | Stille bis 0,35 s |
| 0,35–1,1 | Ball fliegt, Klingen schließen sich gegenläufig. | **Weicher Ton ~256/380 Hz** (Ball-Klang, „Pling“ mit Ausklang) |
| **~1,25–1,4** | Biss → Explosion in **Blau** (~40 Bälle). | Bass-Schlag (−12 dB) + Pfeifton |
| 1,5–3,9 | Blaue Bälle verteilen sich, sammeln sich durch die Schwerkraft am Rand, die Klingen schieben sie zusammen. Text blendet bei 2,3–2,5 s aus. | Viele **tonale Plings/Chirps** (300–900 Hz, auf- und absteigend) als Ball-Klinge-Kontakte, darüber feine Klicks 2–5 kHz |
| **~4,05** | Biss auf die blaue Packung → **gelbe** Wolke (Hunderte), füllt die Mitte. | Bass-Schlag (−14 dB) |
| 4,5–6,3 | Gelbe Masse rutscht nach rechts unten, wird vom Kiefer zu einem gelben Keil zusammengedrückt. | Chirp-Kaskade (Aufladen) |
| **~6,45** | Biss → **weiß → Mint/Türkis**, Tausende Bälle in **Hexagonal-Packung** (Kristallgitter), Kreis fast voll. | Lautester Schlag (−9 dB) |
| 7,62 | Ende der Aufnahme. | |

### 2.2 Hook
- **Frage statt Versprechen:** „Wie viele, schätzt du, am Ende?“ macht den Zuschauer zum **Mitspieler**. Er gibt innerlich eine Zahl ab und muss bis zum Ende schauen, um zu prüfen, ob er recht hat. Danach schreibt er die Zahl in die Kommentare.
- **Kein Zähler** im Bild ist hier konsequent: Das Ergebnis bleibt verborgen, die Neugier steigt.
- Die Gesamtlänge (40 s) ist bekannt. Die Frage „am Ende“ verlangt also, bis Sekunde 40 zu bleiben.

### 2.3 Besonderheiten
- **Der Ton ist musikalischer** als bei Video 1: Kontakte erzeugen Töne mit Tonhöhe (ein Plinken wie bei einem Glockenspiel). Kurz vor einem Biss häufen sich die Kontakte, das klingt wie ein **Aufladen**.
- Farbfolge magenta → blau → gelb → mint, starke Kontraste zwischen aufeinanderfolgenden Stufen.
- Video 2 hat die **höchsten Werte**: 39.158 Likes und 5.254 Teilungen, also 13,4 % Teilungen pro Like. Eine Mitmach-Frage ist ein starker Grund zum Teilen („Rate mal …“).

---

## 3. Einzelanalyse Video 3 – „La machoire, calm your mind“

### 3.1 Ablauf (gemessen)
| Zeit | Bild | Ton |
|---|---|---|
| 0,00 | Gleiches Set, **dunkelpinker** Ball unten, **kein Hook-Text**, Zähler **1 / 60000**, Drehzahl „10 RPM“. | **Durchgehendes Klangpolster: 528 Hz + 264 Hz** (Oktave), pulsierend (Tremolo ~3/s), dazu feine hohe Töne |
| 0–1,0 | Der Kiefer schließt sich unten um den Ball. | Polster |
| **1,01–1,12** | Biss → **Magenta**, Zähler 30 (+29), oben „10“, Drehzahl → 11 RPM. | Doppelter Bass-Schlag (−9 dB) |
| 1,2–3,7 | Magenta-Bälle schweben nach oben links, Klingen fegen. | Ab 2,4 s **dichte Klicks** (2–8 kHz) = Ball-Kontakte |
| **3,74–3,87** | Biss oben → **weiß-rosa** Wolke, Zähler **312** (+282), Drehzahl 12. | Schlag (−4 dB, lautester) |
| 4,0–6,2 | Rosa Bälle setzen sich unten in **Kristallpackung** ab, der Kiefer schiebt sie zu einem Keil zusammen. | Polster + Klicks |
| **6,27–6,40** | Biss → **gelbe** Explosion, die von unten den Kreis füllt, Zähler **1248** (+936), Drehzahl 13. | Schlag |
| 7,99 | Ende der Aufnahme. | |

### 3.2 Besonderheiten
- **Titel „La mâchoire“ („Der Kiefer“):** Das ist der Name der Mechanik. Die zwei Klingen sind ein Kiefer, der zubeißt. Das bestätigt die Regel aller drei Videos.
- **„Calm your mind“** und das **528-Hz-Polster** (in Wellness-Kreisen als „Heilfrequenz“ bekannt) machen das Video zu Entspannung und ASMR statt Spannung. Video 1 setzt dagegen auf Stille und Schläge.
- **Kein Hook-Text und die niedrigsten Zahlen.** Das Video ist aber erst 18 Stunden alt. Ein fairer Vergleich ist deshalb **nicht möglich**, nur ein Hinweis.

---

## 4. Detaillierter Vergleich

| Merkmal | Video 1 | Video 2 | Video 3 |
|---|---|---|---|
| Set | Kreis, 2 Klingen (Kiefer), Schwerkraft | gleich | gleich |
| Start | 1 Ball | 1 Ball | 1 Ball |
| Hook-Text | Versprechen „Warte auf die Explosion…“ | Frage „Wie viele am Ende?“ | keiner |
| Zähler / Ziel | 1 / 45000 + Balken | keiner (absichtlich) | 1 / 60000 |
| 1. Explosion | **0,66 s** | ~1,3 s | 1,01 s |
| Takt der Explosionen | 2,30 / 2,22 s | ~2,8 / 2,4 s | 2,73 / 2,53 s |
| Wachstum | ×30, ×7, ×6,5 | ~×40, ×10, ×10 (geschätzt) | ×30, ×10, ×4 |
| Farbfolge | magenta→gelb→magenta→weiß→blau | magenta→blau→gelb→mint | pink→magenta→rosa→gelb |
| Grundton | **Stille** | leise Plings | **528-Hz-Polster** |
| Explosionston | Bass-Schlag + absteigender Pfeifton, 1,4 s Ausklang | gleich | gleich, doppelt |
| Beschleunigung | Drehzahl 13→15 | (nicht lesbar) | Drehzahl 10→13 |
| Schnitte / Kamera | keine / statisch | keine / statisch | keine / statisch |
| Teilungen pro Like | 12,3 % | 13,4 % | 12,5 % (jung) |
| Merken pro Like | 6,6 % | 6,2 % | 10,0 % |

**Gemeinsam:** dasselbe „Spielbrett“, dieselbe Regel, dieselbe Dramaturgie, nur Farben, Ton und Hook variieren. Das ist ein
**Serienformat**: Der Zuschauer erkennt den Kanal sofort und weiß, was ihn erwartet.

**Teilungen ≈ 12–13 % der Likes** ist für TikTok auffällig hoch. Solche Videos werden verschickt („schau dir das an“) und
gespeichert (zum Beruhigen, zum Nochmal-Anschauen).

---

## 5. Die wichtigsten gemeinsamen Viralitätsfaktoren

1. **Sofort verständliche Regel in unter 1 Sekunde:** ein Ball, ein Kiefer. Man braucht keine Sprache, kein Vorwissen, keine Übersetzung. Deshalb funktioniert es international.
2. **Erste Belohnung in ≤ 1 s, dann alle 2,2–2,8 s eine größere.** Es gibt nie einen Moment ohne nahende Belohnung, weil man den Kiefer sich schließen *sieht*.
3. **Exponentielle Steigerung, die man sehen und zählen kann:** Zähler, „+N“, neue Farbe, mehr Fläche. Jede Stufe übertrifft die vorige.
4. **Ein absurdes Ziel („/ 45000“) oder eine offene Frage („wie viele am Ende?“).** Das Ende ist der Grund, bis zum Schluss zu bleiben.
5. **Vorhersehbarkeit plus Ungewissheit:** Man sieht den Biss kommen (Vorfreude), weiß aber nicht, *wie viele* Bälle gefangen werden. So entsteht ein Mini-Glücksspiel bei jedem Biss.
6. **Oddly satisfying:** Kristallpackung, sauberes Fegen, Abkühlen von weiß zu Farbe, Ordnung aus Chaos.
7. **Sound-Kontrast:** Stille oder ruhiges Polster gegen einen massiven Bass-Schlag. Mit Kopfhörern ist das ASMR, ohne Ton bleibt es dank Farbe und Zahl verständlich.
8. **Wiedererkennbares Serien-Set:** schwarzer Grund, weißer Kreis, gravierte Klingen, Markenname auf den Klingen.
9. **Kommentar-Auslöser:** Schätzfragen und Zahlenziele führen zu Kommentaren wie „ich sag 42.000“.

**Wahrscheinlich nicht entscheidend (zufällig oder austauschbar):** die französische Sprache, die konkreten Farben, die genaue
Zielzahl, die Goldkante an den Klingen, ob „FOLLOW“ oder „@name“ dasteht, die genaue Drehzahl.

---

## 6. Hook-Strategien (konkret)

| Typ | Beispiel (Referenz) | Deutsch für uns | Wirkt durch |
|---|---|---|---|
| **Versprechen** | ATTENDS L'EXPLOSION… | WARTE AUF DIE EXPLOSION… | offene Erwartung, sofortige Teil-Einlösung |
| **Schätzfrage** | TU DIS COMBIEN À LA FIN ? | WIE VIELE SIND ES AM ENDE? | Mitspielen, bis zum Ende bleiben, Zahl kommentieren |
| **Absurdes Ziel** | 1 / 45000 | 1 / 100.000 | „Wie soll das gehen?“ |
| **Stille Mechanik** | (Video 3: nur Kiefer + Ball) | – | wirkt nur mit starker Serien-Bekanntheit |

**Regeln für den Hook:**
- Text höchstens 5 Wörter, Versalien, fett, weiß, oben. Er bleibt bis kurz nach der 1. Explosion stehen (1,6–2,5 s) und blendet dann aus.
- Das **erste Ereignis innerhalb von 0,7–1,0 s**. Die Startposition wird so gewählt, dass der Kiefer den Ball sofort erwischt.
- Ab Bild 1 ist alles zu sehen: Arena, Ball, Kiefer, Ziel. Es gibt kein Intro, kein Logo, keine Einblendung.

---

## 7. Storytelling- und Spannungsstrategien

Auch ohne Worte haben die Videos einen klaren Bogen:
1. **Ausgangslage:** 1 Ball, leere Welt, riesiges Ziel. Das ist der Außenseiter.
2. **Regel lernen:** Der erste Biss zeigt die Mechanik.
3. **Steigerung in Stufen:** jede Stufe mit neuer Farbe, mehr Masse, höherem Tempo (Drehzahl +1).
4. **Mikro-Spannung pro Zyklus:** Der Kiefer nähert sich, Bälle sammeln sich (im Ton aufladend), es kommt zum Biss, Bloom und Schlag, dann zu Ruhe und Stille. Danach beginnt der nächste Zyklus.
5. **Makro-Spannung:** Schafft es das Ziel? Wie voll wird der Kreis? Wann ist die Arena voll?

**Spannungswerkzeuge:** sichtbares Herannahen (der Kiefer als Countdown), Ungewissheit über die Ausbeute, wachsende
Geschwindigkeit, Stille vor dem Knall, Zahlen mit Delta „+N“.

---

## 8. Visuelle und technische Gestaltungsmuster

- **Format:** 9:16, eine statische Einstellung, **60 fps**, sehr flüssige Bewegung.
- **Bühne:** reines Schwarz mit leichter radialer Aufhellung in der Mitte. Ein **dünner weißer Kreis** (~2 px) mit ~88 % der Bildbreite sitzt bei ~45 % der Bildhöhe.
- **Kiefer:** zwei keilförmige Klingen (Metall-Verlauf, Gravur des Kanalnamens, dünne Goldkante). Sie hängen an dünnen dunklen Stäben an einer Nabe in der Mitte und **drehen gegenläufig**. Sie treffen sich etwa alle 2,5 s, wobei der Treffpunkt wandert.
- **Bälle:** kleine Kreise mit Glühen. Jede Generation hat **eine gesättigte Neonfarbe**. Explosionen sind zunächst weiß-überstrahlt und kühlen in ~0,4 s auf die neue Farbe ab. Bei vielen Bällen bildet sich eine **Hexagonal-Packung**.
- **Physik:** Schwerkraft nach unten, Bälle prallen am Kreis und an den Klingen ab, die Klingen schieben die Bälle (Fegen).
- **HUD:**
  - **Hook-Text** oben (fett, Versalien)
  - eine **dezente Drehzahl** ganz oben
  - **„FOLLOW“ oder „@name“** grau über dem Kreis
  - **große dünne Umriss-Zahlen** bei Explosionen
  - **Zähler** unten (dünne Ziffern „N / ZIEL“, blaues „+N“, Fortschrittsbalken)
- **Typografie:** dünne, elegante Ziffern statt fetter Gaming-Schrift. Das wirkt ruhig und „premium“.
- Der Kreis überlappt rechts die TikTok-Symbole. Die Aktion spielt aber in der Mitte, deshalb stört es nicht.

---

## 9. Audio- und Sounddesign-Strategien

| Element | Messung | Funktion |
|---|---|---|
| **Explosion** | Breitband-Schlag mit Schwerpunkt **20–100 Hz** (Sub-Bass), dazu ein **absteigender Pfeifton** (~1,3 kHz → 660 Hz) und ein Klingeln bei 600–900 Hz, Ausklang **1,3–1,6 s**, Spitzen −4 bis −9 dBFS | Belohnung, körperlich spürbar |
| **Stille** (Video 1) | zwischen den Schlägen −120 dB, also digital still | maximaler Kontrast, Spannung |
| **Klangpolster** (Video 3) | 528 Hz + 264 Hz, pulsierend ~3 Hz | Entspannung, „calm your mind“ |
| **Kontakt-Töne** (Video 2) | tonale Plings 250–900 Hz, auf- und absteigend, gehäuft vor einem Biss | musikalisch, Aufladen |
| **Kollisions-Klicks** | feine Ticks 2–8 kHz, Dichte wächst mit der Ballzahl | Masse hörbar machen, ASMR |
| **Sprache/Musik** | keine (Spracherkennung fand nur „Klingeln/ruhige Musik“) | international, keine Sprachbarriere |
| **Lautheit** | −10,7 / −16,8 / −13,9 LUFS integriert | Wir bleiben bei −14 LUFS mit hohen Spitzen (Dynamik!) |

---

## 10. Schnitt- und Tempo-Strategien

- **Null Schnitte.** Das Tempo entsteht durch **Ereignisse in der Szene**, nicht durch Montage.
- **Zyklus von 2,2–2,8 s:** Anlauf (~1,5 s), Biss, Bloom (0,4 s), Ausklang (~1 s). Die Abstände werden leicht kürzer (Drehzahl +1 pro Biss).
- **Informationsdichte:** pro Zyklus genau **eine** neue Information (neue Farbe und neue Zahl).
- Der Hook-Text verschwindet nach der ersten Einlösung. Danach ist das Bild frei für die Mechanik.

---

## 11. Häufige Fehler, die wir vermeiden müssen

1. Der erste Höhepunkt kommt später als 1 s.
2. Ruhephasen über 3 s ohne sichtbar herannahendes Ereignis.
3. Die Steigerung stagniert, weil eine Explosion kleiner ist als die vorige oder Farben sich nicht abheben.
4. Zu viel HUD oder fette Effekte (Rahmen, Emojis, Wackeln). Die Referenzen sind **minimalistisch**.
5. Hintergrundmusik, die die Stille zerstört. Wenn Musik, dann nur ein leises, ruhiges Polster.
6. Kein Ziel und keine Frage, also kein Grund, bis zum Ende zu bleiben.
7. Ein Ende, das die Frage nicht auflöst (bei der Schätzfrage muss die Endzahl groß gezeigt werden).
8. Ruckelnde Bewegung: Unter 60 fps wirkt die Physik billig.
9. Unklare Regel, etwa zu viele Mechaniken gleichzeitig.
10. Ton ohne Bass. Auf Handy-Lautsprechern trägt der Pfeifton (660–1300 Hz) die Explosion, mit Kopfhörern der Sub-Bass. Beides ist nötig.

---

## 12. Produktionssystem

Die kompakte Arbeitsanweisung steht in **`PRODUKTION.md`**. Sie gilt für alle Videos im **Simulations-Format (STIL 4)**.
Ihre Prinzipien übertrage ich auch auf unsere Du-Geschichten (siehe dort Abschnitt „Übertragung auf Geschichten“).

## 13. Checkliste

Die Checkliste steht am Ende von **`PRODUKTION.md`** und wird vor jeder Veröffentlichung abgehakt.
