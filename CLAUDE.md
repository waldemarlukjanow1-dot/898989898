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
- Versteckte Hinweise dürfen bleiben, aber nur zusätzlich – die Haupthandlung muss beim ersten
  Ansehen klar sein.
- **Jederzeit ist ein Plottwist möglich:** jede Figur wirkt verdächtig, kleine Twists ca. alle
  15 Sekunden, falsche Fährten, ein Finale, das den Anfang umdeutet; Ende möglichst als Loop
  zum ersten Satz. Ein HUD-Wert wie „VERTRAUEN“ oder „MISSTRAUEN“ zeigt die Unsicherheit.
- **Die ersten Sekunden** sagen sofort, worum es geht, und müssen sehr aufregend sein (z. B. 1-Frame-Schock + Prämisse im ersten Satz).
- Ende immer mit Cliffhanger + Frage an die Zuschauer (Kommentare entscheiden Teil 2).
- Videos wegen Größe mit ~9 Mbit/s ausgeben (Filmkorn bläht sonst auf >300 MB).

## Kanal
- Name: **Du-Geschichten 🎭** (@du.geschichten), Profilbild: `tiktok/profilbild/profilbild_B_pink.png`
- Bio: „Jede Geschichte passiert DIR. 🎭 / Teil 2 entscheidest du in den Kommentaren 👇“
- Hashtags: 3 Themen-Tags + #storytime #duform #geschichte #plottwist #spannung #fürdich #fyp
