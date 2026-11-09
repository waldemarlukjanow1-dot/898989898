"""Builds the one-page storyboard preview (PNG) for review before the full render."""
import sys
import textwrap
from PIL import Image, ImageDraw

import scenes17 as S2
import style3 as T
from style3 import S
from script import SEQ, TITLE, DURATION

CAP_Y = {}
OUT = sys.argv[1] if len(sys.argv) > 1 else "storyboard.png"

PW = 2160
BG = (16, 22, 23)
CARD = (27, 36, 37)
MUTED = (150, 168, 165)
WHITE = S.C["white"]
PINK = S.C["pink"]
GOLD = S.C["gold"]


def frame(i, small=True):
    sq = SEQ[i]
    a, b = S2.BOUNDS[i]
    ta = a + 0.8 * (b - a)
    im = S2.render(i, 0.8, b - a, ta)
    T.chip(im, *S2.chip_for(i, ta))
    words = sq["vo"].split()
    # show a short caption chunk the way it appears on screen (2–4 words)
    chunk_idx = next((k for k, w in enumerate(words) if w in sq["hi"]), 0)
    a = max(0, chunk_idx - 1)
    chunk = words[a:a + 3]
    while len(chunk) > 1 and len(" ".join(chunk)) > 20:
        chunk = chunk[1:] if chunk[0] not in sq["hi"] else chunk[:-1]
    T.caption(im, chunk, hi=[k for k, w in enumerate(chunk) if w in sq["hi"]])
    return im


def wrap(d, xy, txt, f, fill, width, gap=8):
    x, y = xy
    words, line = txt.split(), ""
    for w in words:
        test = (line + " " + w).strip()
        if d.textlength(test, font=f) > width and line:
            d.text((x, y), line, font=f, fill=fill)
            y += f.size + gap
            line = w
        else:
            line = test
    if line:
        d.text((x, y), line, font=f, fill=fill)
        y += f.size + gap
    return y


def tiktok_ui(im):
    """Mock TikTok interface + shaded no-go zones on a 1080x1920 frame."""
    d = ImageDraw.Draw(im, "RGBA")
    red = (255, 40, 70, 70)
    d.rectangle((0, 0, 1080, 220), fill=red)            # status bar + tabs
    d.rectangle((930, 220, 1080, 1500), fill=red)       # like/comment/share column
    d.rectangle((0, 1500, 1080, 1920), fill=red)        # username, caption, nav
    f = S.font(34, "Bold")
    d.text((540, 150), "Community   Gefolgt   Shop   Für dich", font=f, fill=WHITE, anchor="ms")
    for k, (y, lab) in enumerate([(820, "♥"), (980, "…"), (1130, "■"), (1280, "➦")]):
        d.ellipse((960, y - 45, 1050, y + 45), fill=(255, 255, 255, 60), outline=WHITE, width=3)
    d.ellipse((955, 640, 1055, 740), fill=(255, 255, 255, 90), outline=WHITE, width=4)
    d.text((40, 1600), "@deinname", font=S.font(42, "Black"), fill=WHITE)
    d.text((40, 1660), "Du hast gerade eine Bank geknackt…", font=S.font(34, "Medium"), fill=WHITE)
    d.rectangle((0, 1820, 1080, 1920), fill=(0, 0, 0, 230))
    # safe area outline
    d.rectangle((40, 230, 920, 1490), outline=(80, 255, 160), width=6)
    d.text((60, 1440), "SAFE ZONE", font=S.font(36, "Black"), fill=(80, 255, 160))
    return im


def main():
    TH_W, TH_H = 456, 810
    COLS, GAP, MARGIN = 4, 40, 70
    card_w = (PW - 2 * MARGIN - (COLS - 1) * GAP) // COLS
    TEXT_H = 600
    rows = (len(SEQ) + COLS - 1) // COLS
    header_h = 760
    grid_h = rows * (TH_H + TEXT_H + GAP)
    safe_h = 1250
    footer_h = 380
    PH = header_h + grid_h + safe_h + footer_h
    page = Image.new("RGB", (PW, PH), BG)
    d = ImageDraw.Draw(page)

    # ---------- header
    d.text((MARGIN, 70), "STORYBOARD · TIKTOK #17 · THRILLER", font=S.font(34, "Bold"), fill=PINK)
    d.text((MARGIN, 120), TITLE, font=S.font(104, "Black"), fill=WHITE)
    d.text((MARGIN, 260), "20 Millionen dafür, 24 Stunden zu verschwinden. Am nächsten Morgen bist du offiziell tot – und jemand will, dass du es bleibst.",
           font=S.font(38, "Medium"), fill=MUTED)
    d.text((MARGIN, 310), "Jede Szene ein neuer Schock, Chip oben erzählt mit, Mund nur beim Sprechen, Karaoke-Untertitel. Ende: Die 24 Stunden sind um.",
           font=S.font(38, "Medium"), fill=MUTED)
    chips = [("LÄNGE", "~62 Sek."), ("FORMAT", "9:16 · 1080×1920"), ("SEQUENZEN", str(len(SEQ))),
             ("STIMME", "Deutsch, männlich, ruhig"), ("TWIST", "Die 24 Stunden sind um")]
    x = MARGIN
    for lab, val in chips:
        fv = S.font(40, "Black")
        w = int(max(d.textlength(val, font=fv), d.textlength(lab, font=S.font(22, "Bold")))) + 50
        d.rounded_rectangle((x, 400, x + w, 520), 16, fill=CARD, outline=(60, 76, 76), width=2)
        d.text((x + 25, 418), lab, font=S.font(22, "Bold"), fill=MUTED)
        d.text((x + 25, 452), val, font=fv, fill=WHITE)
        x += w + 20
    d.text((MARGIN, 580), "Spannungsbogen:", font=S.font(36, "Black"), fill=GOLD)
    arc = "20 Mio. Angebot  →  schwarzer SUV  →  Identität gelöscht  →  du bist offiziell tot  →  5 Mio. auf dem Konto  →  PAUSE  →  Anruf: du schuldest es  →  Foto deiner Familie: Bleib tot  →  Schlüssel im Schloss  →  Zielperson gefunden  →  der Fahrer: Zeit ist um  →  Verstecken oder fliehen?"
    wrap(d, (MARGIN + 360, 584), arc, S.font(34, "Medium"), WHITE, PW - 2 * MARGIN - 360)

    # ---------- grid
    y0 = header_h
    for i, sq in enumerate(SEQ):
        r, c = divmod(i, COLS)
        x = MARGIN + c * (card_w + GAP)
        y = y0 + r * (TH_H + TEXT_H + GAP)
        d.rounded_rectangle((x, y, x + card_w, y + TH_H + TEXT_H), 22, fill=CARD)
        th = frame(i).resize((TH_W, TH_H), Image.LANCZOS)
        page.paste(th, (x + (card_w - TH_W) // 2, y + 18))
        ty = y + TH_H + 36
        d.text((x + 24, ty), f"{i + 1:02d}", font=S.font(44, "Black"), fill=PINK)
        d.text((x + 90, ty + 4), sq["name"].upper(), font=S.font(36, "Black"), fill=WHITE)
        tc = f"{sq['start']:04.1f}s – {sq['end']:04.1f}s"
        d.text((x + 24, ty + 58), tc, font=S.mono(26), fill=GOLD)
        ty += 106
        ty = wrap(d, (x + 24, ty), "„" + sq["vo"] + "“", S.font(27, "SemiBold"), WHITE, card_w - 48, 6)
        ty += 8
        ty = wrap(d, (x + 24, ty), sq["visual"], S.font(24, "Medium"), MUTED, card_w - 48, 5)
        if sq.get("clue", "—") != "—":
            wrap(d, (x + 24, ty + 6), "HINWEIS: " + sq["clue"], S.font(23, "SemiBold"), GOLD, card_w - 48, 5)

    # ---------- safe zone section
    sy = y0 + grid_h + 20
    d.text((MARGIN, sy), "ABSTÄNDE · TIKTOK-SAFE-ZONE", font=S.font(34, "Bold"), fill=PINK)
    demo = frame(11)
    demo = tiktok_ui(demo).resize((585, 1040), Image.LANCZOS)
    page.paste(demo, (MARGIN, sy + 70))
    tx = MARGIN + 640
    lines = [
        ("Oben 220 px frei", "Uhrzeit, Kamera-Insel und die Tabs „Gefolgt / Für dich“. Das HUD startet erst bei 250 px."),
        ("Rechts 150 px frei", "Like, Kommentar, Merken, Teilen und Profilbild. Untertitel sind deshalb leicht nach links "
                               "versetzt (Mitte bei x = 500 statt 540) und maximal 760 px breit."),
        ("Unten 420 px frei", "Benutzername, Beschreibung, Musik/Suche und Navigationsleiste. Keine Schrift, keine Buttons "
                              "unter y = 1500. Die Untertitel stehen bei y ≈ 1210 – genau wie im Vorbild."),
        ("Grüner Rahmen", "Hier passiert alles Wichtige: Figuren, Namens-Tags, HUD, Untertitel, PAUSE-Glitch."),
    ]
    ly = sy + 90
    for head, body in lines:
        d.text((tx, ly), head, font=S.font(46, "Black"), fill=WHITE)
        ly = wrap(d, (tx, ly + 64), body, S.font(34, "Medium"), MUTED, PW - tx - MARGIN, 8) + 40
    d.text((tx, ly), "Rot = TikTok-Bedienelemente · Grün = sicherer Bereich", font=S.font(30, "Bold"), fill=PINK)

    # ---------- footer
    fy = PH - footer_h + 40
    d.rounded_rectangle((MARGIN, fy, PW - MARGIN, PH - 70), 26, fill=(44, 18, 30), outline=PINK, width=4)
    d.text((MARGIN + 50, fy + 50), "Passt alles?", font=S.font(56, "Black"), fill=WHITE)
    d.text((MARGIN + 50, fy + 130), "Schick mir die ElevenLabs-MP3 + „Du darfst“ – dann rendere ich das komplette Video.",
           font=S.font(38, "SemiBold"), fill=WHITE)
    d.text((MARGIN + 50, fy + 190), "Oder sag mir, welche Szene / welcher Satz geändert werden soll.",
           font=S.font(38, "Medium"), fill=MUTED)

    page.save(OUT, optimize=True)
    print(OUT, page.size)


if __name__ == "__main__":
    main()
