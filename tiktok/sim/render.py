"""Renders simulation frames in STIL 4 (black stage, thin white ring, metal jaw, neon balls with glow, minimal HUD)."""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from sim import W, H, CX, CY, R, blade_halfwidth

SS = 2
FD = "/usr/share/fonts/opentype/inter/"
PALETTE = [(255, 43, 214), (255, 230, 0), (61, 92, 255), (92, 255, 200), (255, 122, 184), (170, 110, 255)]
GOLD = (201, 168, 90)


def font(size, weight="Black"):
    return ImageFont.truetype(f"{FD}Inter-{weight}.otf", int(size))


def _background():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((x - CX) ** 2 + (y - CY) ** 2) / 900.0
    v = np.clip(20 * (1 - d), 0, 20)
    return np.repeat(v[:, :, None], 3, 2)


BG = _background()


def ball_colors(col, born, t):
    base = np.array(PALETTE, dtype=np.float32)[np.asarray(col) % len(PALETTE)]
    age = np.clip((t - born) / 0.45, 0, 1)[:, None]          # white-hot -> cools into its colour
    return base * age + 255 * (1 - age)


def draw_blade(d, ang, label_img):
    u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    n = (-u[1], u[0])
    inner = 0.55 * R
    # rod to the hub
    d.line([(CX * SS, CY * SS), ((CX + u[0] * inner) * SS, (CY + u[1] * inner) * SS)], fill=(60, 60, 68), width=4 * SS)
    # metal wedge in strips (light -> dark across the width)
    hw0, hw1 = blade_halfwidth(inner), blade_halfwidth(R - 2)
    steps = 6
    for k in range(steps):
        f0, f1 = -1 + 2 * k / steps, -1 + 2 * (k + 1) / steps
        c = int(235 - 110 * abs((f0 + f1) / 2 + 0.3))
        pts = [(CX + u[0] * inner + n[0] * hw0 * f0, CY + u[1] * inner + n[1] * hw0 * f0),
               (CX + u[0] * (R - 2) + n[0] * hw1 * f0, CY + u[1] * (R - 2) + n[1] * hw1 * f0),
               (CX + u[0] * (R - 2) + n[0] * hw1 * f1, CY + u[1] * (R - 2) + n[1] * hw1 * f1),
               (CX + u[0] * inner + n[0] * hw0 * f1, CY + u[1] * inner + n[1] * hw0 * f1)]
        d.polygon([(x * SS, y * SS) for x, y in pts], fill=(c, c, c + 6))
    for sgn in (-1, 1):   # thin gold edges
        d.line([((CX + u[0] * inner + n[0] * hw0 * sgn) * SS, (CY + u[1] * inner + n[1] * hw0 * sgn) * SS),
                ((CX + u[0] * (R - 2) + n[0] * hw1 * sgn) * SS, (CY + u[1] * (R - 2) + n[1] * hw1 * sgn) * SS)],
               fill=GOLD, width=2 * SS)
    return u


def paste_label(img, ang, label_img):
    """Engraved channel name along the blade."""
    rot = label_img.rotate(-ang, resample=Image.BICUBIC, expand=True)
    mid = 0.78 * R
    x = (CX + math.cos(math.radians(ang)) * mid) * SS - rot.width / 2
    y = (CY + math.sin(math.radians(ang)) * mid) * SS - rot.height / 2
    img.paste(rot, (int(x), int(y)), rot)


def make_label():
    f = font(15 * SS, "Bold")
    txt = "DU-GESCHICHTEN"
    w = int(f.getlength(txt)) + 8
    im = Image.new("RGBA", (w, 24 * SS), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4, 2), txt, font=f, fill=(70, 70, 80, 220))
    return im


LABEL = make_label()


# ---- optional style (set by the video script)
RING = "white"            # "white" | "rainbow"
BLADE = None              # None = metal wedge, or dict(colors=[(inner, outer), (inner, outer)])


def hsv(h, s=1.0, v=1.0):
    import colorsys
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


def draw_ring_rainbow(d, t, pulse):
    n = 180
    for k in range(n):
        a0, a1 = 360 * k / n, 360 * (k + 1) / n + 0.6
        col = hsv(k / n + t * 0.04, 0.85, 1.0)
        box = ((CX - R - 3) * SS, (CY - R - 3) * SS, (CX + R + 3) * SS, (CY + R + 3) * SS)
        gbox = ((CX - R - 9) * SS, (CY - R - 9) * SS, (CX + R + 9) * SS, (CY + R + 9) * SS)
        d.arc(gbox, a0, a1, fill=col + (int(50 + 110 * pulse),), width=int((14 + 10 * pulse) * SS))
        d.arc(box, a0, a1, fill=col + (255,), width=int((4 + 2 * pulse) * SS))


def draw_blade_leaf(d, ang, inner, outer):
    """Leaf/spindle blade following blade_halfwidth (same shape as the physics), two-tone with a bright core."""
    u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    n = (-u[1], u[0])
    ss = np.linspace(0, R - 1, 40)
    hw = blade_halfwidth(ss)
    for scale, col, a in ((1.7, outer, 60), (1.0, outer, 255), (0.45, inner, 255)):
        left = [((CX + u[0] * s_ + n[0] * w * scale) * SS, (CY + u[1] * s_ + n[1] * w * scale) * SS) for s_, w in zip(ss, hw)]
        right = [((CX + u[0] * s_ - n[0] * w * scale) * SS, (CY + u[1] * s_ - n[1] * w * scale) * SS) for s_, w in zip(ss, hw)]
        d.polygon(left + right[::-1], fill=col + (a,))


def fmt(n):
    return f"{n:,}".replace(",", ".")


def render_frame(fr, t, events, goal, rb):
    # ---- balls (supersampled)
    layer = Image.new("RGB", (W * SS, H * SS), (0, 0, 0))
    d = ImageDraw.Draw(layer)
    pos = fr["pos"]
    cols = ball_colors(fr["col"], fr["born"], t).astype(np.uint8)
    radii = np.full(len(pos), (rb * 2.2 if len(pos) == 1 else rb) * SS)   # a lone ball is drawn bigger
    for (x, y), c, r in zip(pos * SS, cols, radii):
        d.ellipse((x - r, y - r, x + r, y + r), fill=tuple(int(v) for v in c))
    for e in events:   # white flash where the single ball is born after the implosion
        if e["kind"] == "pop" and 0 <= t - e["t"] < 0.35:
            rr = (10 + 60 * (1 - (t - e["t"]) / 0.35)) * SS
            d.ellipse((e["x"] * SS - rr, e["y"] * SS - rr, e["x"] * SS + rr, e["y"] * SS + rr), fill=(255, 255, 255))
    small = layer.resize((W, H), Image.BILINEAR)
    arr = np.asarray(small, dtype=np.float32)
    # glow: blurred copy, added
    g = small.resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(4))
    glow = np.asarray(g.resize((W, H), Image.BILINEAR), dtype=np.float32)
    # extra bloom right after an explosion
    bloom = 0.0
    for e in events:
        if e["kind"] in ("bite", "pop") and 0 <= t - e["t"] < 0.6:
            bloom = max(bloom, (1 - (t - e["t"]) / 0.6) * (1.0 if e["kind"] == "bite" else 0.6))
    dens = 1.0 / (1.0 + len(pos) / 1500.0)          # less glow when the arena is crowded
    g2 = np.clip(glow * (1.2 + 1.2 * bloom) * dens, 0, 255)
    base = np.clip(BG + arr, 0, 255)
    out = 255 - (255 - base) * (255 - g2) / 255.0   # screen blend: glows without burning out
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

    # ---- stage (ring, jaw, hub) drawn supersampled on top
    st = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    if RING == "rainbow":
        draw_ring_rainbow(sd, t, bloom)
    else:
        sd.ellipse(((CX - R) * SS, (CY - R) * SS, (CX + R) * SS, (CY + R) * SS), outline=(235, 235, 240, 230), width=3 * SS)
    for k, ang in enumerate((fr["a1"], fr["a2"])):
        if BLADE:
            inner, outer = BLADE["colors"][k]
            draw_blade_leaf(sd, ang, inner, outer)
        else:
            draw_blade(sd, ang, LABEL)
    sd = ImageDraw.Draw(st)
    sd.ellipse(((CX - 9) * SS, (CY - 9) * SS, (CX + 9) * SS, (CY + 9) * SS), fill=(10, 10, 12), outline=(200, 200, 205), width=2 * SS)
    st = st.resize((W, H), Image.LANCZOS)
    img.paste(st, (0, 0), st)

    # ---- only text: small thin "follow for more"
    hd = ImageDraw.Draw(img, "RGBA")
    hd.text((CX, CY - R - 24), "f o l l o w   f o r   m o r e", font=font(26, "Light"), fill=(125, 125, 132), anchor="ms")
    return img
