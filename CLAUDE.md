# TikTok-Kanal „Du-Geschichten“ – Arbeitsregeln

Dieses Repo produziert TikTok-Videos: Geschichten in der **Du-Form**, flacher 2D-Vektor-Stil,
gesichtslose Figuren mit runden weißen Köpfen. Vorlage und Code: `tiktok/bankraub/`.

## Ablauf (immer einhalten)
1. Zuerst ein **Storyboard-Bild** mit allen Sequenzen + überprüfbarem Prompt (`PROMPT.md`).
2. Erst wenn der Nutzer **„Du darfst“** schreibt, das komplette Video rendern.
3. Stimme: Der Nutzer erzeugt sie bei ElevenLabs (Stimme „Helmut – German Epic Trailer Voice“)
   und lädt die MP3 hoch. Danach Timing per Spracherkennung, Video darauf synchronisieren.
4. Länge ca. **62 Sekunden**, 1080×1920, 30 fps, Lautheit −14 LUFS.

## Safe-Zone (TikTok-UI nicht verdecken)
Oben 220 px, rechts 150 px, unten 420 px frei. Untertitel bei y≈1210, Mitte x=500, max. 760 px breit.

## Stil-Wünsche des Nutzers (ab Video 2)
- **Düstere Stimmung**, aber über Farben und Hintergrund (dunkle Räume, Rot als Akzent,
  tiefer Sub-Bass, Stille als Spannungsmittel) – NICHT über unleserliches Bild.

### Verständlichkeit hat Vorrang (Feedback nach Video 3 „Der Zeuge“)
Der Nutzer hat bei „Der Zeuge“ nicht verstanden, worum es geht. Deshalb ab sofort:
- **Kein Flackern**, kein Filmkorn, keine Dauer-Glitches, keine Wackelkamera.
  Glitch nur einmal kurz bei der PAUSE.
- **Simpel und deutlich animieren:** ruhiger, sanfter Zoom; Figuren/Objekte gleiten oder poppen
  klar ins Bild; eine Bewegung pro Szene, die man sofort versteht.
- **Was gesagt wird, sieht man:** Jede Szene zeigt genau EINE klare Sache, die zum Satz passt.
- **Hauptmotiv immer hell und kontrastreich** beleuchtet, groß im Bild; keine Silhouetten für
  wichtige Figuren, keine fast-schwarzen Szenen.
- **Figuren eindeutig:** feste Farben/Merkmale pro Figur, Namens-Schild beim ersten Auftritt.
- **Rückblenden klar markiert** (z. B. Sepia-Ton + Label „RÜCKBLENDE“), aber scharf und lesbar.
- **Schlüsselinfos als Text-Insert** (z. B. „MANTEL: GRAU“ → „MANTEL: SCHWARZ“), damit Twists
  auch ohne Ton verständlich sind.
- **Orte und Gebäude klar erkennbar:** Häuser mit Dach, Fenstern, Tür, Schild (z. B. „BANK“,
  „POLIZEI“), Straße/Bürgersteig; Innenräume mit typischen Möbeln, damit man sofort weiß, wo man ist.
- **Figuren bewegen sich richtig:** Laufen mit schwingenden Armen und Beinen (Gehzyklus),
  Kopf dreht sich, Hände greifen, Mund bewegt sich beim Sprechen, Blinzeln; Figuren gehen
  von A nach B statt nur still dazustehen oder zu wackeln. Gliedmaßen als Gelenk-Rig zeichnen.
- Versteckte Hinweise dürfen bleiben, aber nur zusätzlich – die Haupthandlung muss beim ersten
  Ansehen klar sein.
- **Jederzeit ist ein Plottwist möglich:** jede Figur wirkt verdächtig, kleine Twists ca. alle
  15 Sekunden, falsche Fährten, ein Finale, das den Anfang umdeutet; Ende möglichst als Loop
  zum ersten Satz. Ein HUD-Wert wie „VERTRAUEN“ oder „MISSTRAUEN“ zeigt die Unsicherheit.
- **Die ersten Sekunden** sagen sofort, worum es geht, und müssen sehr aufregend sein (z. B. 1-Frame-Schock + Prämisse im ersten Satz).
- Ende immer mit Cliffhanger + Frage an die Zuschauer (Kommentare entscheiden Teil 2).
- Videos wegen Größe mit ~9 Mbit/s ausgeben (Filmkorn bläht sonst auf >300 MB).

## STIL 3 (ab Video „Reich in 30 Tagen“, Vorlage: Screenrecording 03.11.) – aktueller Standard
- **Cartoon-Figur MIT Gesicht** (frontal): Hautfarbe, braune Haare mit Pony, große runde Augen mit
  Glanzpunkt, rosa Wangen, ausdrucksstarker Mund (staunen, Sorge, verlegen …), blauer Hoodie mit
  Kordeln, Handy in der Hand. Code: `tiktok/reich/style3.py`.
- Figur groß und mittig; Kamera startet weit und zoomt langsam auf die Figur.
- Einfache, helle Hintergründe (z. B. Zimmer bei Nacht mit Stadtfenster), fallende Objekte
  (Geldscheine), Geldberge im Vordergrund.
- **Ein Info-Chip oben** (z. B. grün „100.000.000 $“, rot „⚠ KEIN HERKUNFTSNACHWEIS“) statt Spiel-HUD.
- Untertitel weiß mit schwarzer Kontur, Schlagwort **gelb** hervorgehoben.
- Erzählung bleibt in der Du-Form.
- **Hauptfigur ab Video 12 (Wunsch 06.11.):** dunkle Haare, neue Frisur, **dunkelgrüner Pullover mit
  waagerechten hellgrünen Streifen** (Rundhals, kein Hoodie). Im Code immer `character(..., **T.HERO)`
  verwenden (`tiktok/reich/style3.py`). Festgelegt: **Frisur A = Seitenscheitel mit kurzen Seiten** (`side`) und
  **dünner Schnauzer, der um die Mundwinkel nach unten hängt** (`mustache=True`) – beides ist in `HERO` enthalten. Vorschau: `tiktok/reich/figur_neu_vorschau.png`.

## Kanal
- Name: **Du-Geschichten 🎭** (@du.geschichten), Profilbild: `tiktok/profilbild/profilbild_B_pink.png`
- Bio: „Jede Geschichte passiert DIR. 🎭 / Teil 2 entscheidest du in den Kommentaren 👇“
- Hashtags: 3 Themen-Tags + #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp
