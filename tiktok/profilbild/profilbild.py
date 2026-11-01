"""TikTok profile pictures in the same flat style as the videos (1080x1080, safe for the round crop)."""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bankraub"))
import scenes as S  # noqa: E402

C = S.C
N = 1080
OUT = os.path.dirname(os.path.abspath(__file__))


class Square(S.Canvas):
    def __init__(self, bg):
        self.img = Image.new("RGB", (N * S.SS, N * S.SS), bg)
        self.d = ImageDraw.Draw(self.img, "RGBA")

    def final(self):
        return self.img.resize((N, N), Image.LANCZOS)


def backdrop(cv, inner, outer):
    for r in range(760, 0, -8):
        k = r / 760
        col = tuple(int(inner[i] * (1 - k) + outer[i] * k) for i in range(3))
        cv.circle(540, 540, r, col)


def character(cv, cx, cy, r, mood="focus"):
    # shoulders / jacket
    cv.rect((cx - r * 1.45, cy + r * 0.85, cx + r * 1.45, cy + r * 3.2), C["jacket"], C["ink"], 8, r=int(r * 0.7))
    cv.poly([(cx - r * 0.3, cy + r * 0.88), (cx + r * 0.3, cy + r * 0.88), (cx, cy + r * 1.45)], C["white"])
    cv.line([(cx - r * 0.3, cy + r * 0.9), (cx, cy + r * 1.45), (cx + r * 0.3, cy + r * 0.9)], C["ink"], 6)
    S.head(cv, cx, cy, r, "smirk" if mood == "smirk" else "neutral")
    if mood != "smirk":  # determined brows
        for sg in (-1, 1):
            cv.line([(cx + sg * r * 0.55, cy - r * 0.32), (cx + sg * r * 0.18, cy - r * 0.2)], C["ink"], r * 0.07)
    beanie(cv, cx, cy, r)


def beanie(cv, cx, cy, r):
    dome, band = (44, 46, 54), (66, 70, 82)
    cv.d.chord(cv.s((cx - r * 1.04, cy - r * 1.2, cx + r * 1.04, cy + r * 0.5)), 180, 360, fill=dome,
               outline=C["ink"], width=7 * S.SS)
    cv.rect((cx - r * 1.08, cy - r * 0.5, cx + r * 1.08, cy - r * 0.3), band, C["ink"], 7, r=int(r * 0.08))
    for k in range(-8, 9):
        x = cx + k * r * 0.12
        cv.line([(x, cy - r * 0.47), (x, cy - r * 0.33)], (50, 54, 64), 4)
    cv.circle(cx, cy - r * 1.22, r * 0.14, band, C["ink"], 6)


def rain(cv, alpha=70):
    import random
    rnd = random.Random(5)
    for _ in range(70):
        x, y = rnd.uniform(0, N), rnd.uniform(0, N)
        ln = rnd.uniform(25, 55)
        cv.line([(x, y), (x + ln * 0.18, y + ln)], (210, 230, 225, alpha), 3)


def tag(cv, x, y, txt, fill, color):
    f = S.font(84, "Black")
    w = cv.d.textlength(txt, font=S.ImageFont.truetype(f.path, f.size * S.SS)) / S.SS + 56
    cv.rect((x, y, x + w, y + 120), fill, C["ink"], 7, r=22)
    cv.text((x + w / 2, y + 90), txt, f, color, "ms")


def variant_a():
    """Hero: beanie character, pink 'DU' tag — the account's signature."""
    cv = Square(C["night"])
    backdrop(cv, (70, 120, 116), C["night"])
    cv.glow(540, 470, 330, (255, 220, 150), 55)
    rain(cv)
    character(cv, 540, 520, 230)
    tag(cv, 640, 205, "DU", C["pink"], C["white"])
    cv.line([(700, 330), (640, 380)], C["white"], 7)
    return cv.final()


def variant_b():
    """Pink background, character in the middle — pops in a feed."""
    cv = Square(C["pink"])
    backdrop(cv, (255, 110, 160), (200, 30, 90))
    character(cv, 540, 540, 245, "smirk")
    return cv.final()


def variant_c():
    """Glitch version: RGB split + PAUSE bars, like the twist moment."""
    img = variant_a()
    r, g, b = img.split()
    r = r.transform(img.size, Image.AFFINE, (1, 0, 12, 0, 1, 0))
    b = b.transform(img.size, Image.AFFINE, (1, 0, -12, 0, 1, 0))
    img = Image.merge("RGB", (r, g, b))
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(0, N, 8):
        d.rectangle((0, y, N, y + 3), fill=(0, 0, 0, 40))
    d.rectangle((215, 230, 250, 340), fill=C["white"])
    d.rectangle((275, 230, 310, 340), fill=C["white"])
    return img


def preview(imgs, labels):
    """Shows each option as TikTok crops it (circle), large and tiny."""
    P = Image.new("RGB", (1500, 790), (16, 22, 23))
    d = ImageDraw.Draw(P)
    d.text((50, 40), "PROFILBILD – 3 VARIANTEN", font=S.font(44, "Black"), fill=C["white"])
    d.text((50, 100), "So sieht es in TikTok aus (rund) – groß im Profil und klein im Feed",
           font=S.font(28, "Medium"), fill=(150, 168, 165))
    mask = Image.new("L", (N, N), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, N, N), fill=255)
    for k, (im, lab) in enumerate(zip(imgs, labels)):
        x = 50 + k * 480
        for size, (ox, oy) in ((400, (x, 180)), (90, (x + 155, 660))):
            P.paste(im.resize((size, size), Image.LANCZOS), (ox, oy), mask.resize((size, size), Image.LANCZOS))
        d.text((x + 200, 640), lab, font=S.font(34, "Black"), fill=C["pink"] if k == 0 else C["white"], anchor="ms")
    return P


if __name__ == "__main__":
    imgs = [variant_a(), variant_b(), variant_c()]
    names = ["A_klassisch", "B_pink", "C_glitch"]
    for im, nm in zip(imgs, names):
        im.save(f"{OUT}/profilbild_{nm}.png")
    preview(imgs, ["A · Klassisch", "B · Pink", "C · Glitch"]).save(f"{OUT}/vorschau.png")
    print("ok")
