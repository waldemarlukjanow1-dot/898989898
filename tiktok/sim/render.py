"""Renders simulation frames in STIL 4 (black stage, thin white ring, metal jaw, neon balls with glow, minimal HUD)."""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from sim import W, H, CX, CY, R, blade_halfwidth

SS = 2
FD = "/usr/share/fonts/opentype/inter/"
PALETTE = [(255, 43, 214), (255, 230, 0), (61, 92, 255), (92, 255, 200), (255, 122, 184), (180, 120, 255),
           (255, 255, 255)]
GOLD = (201, 168, 90)


def font(size, weight="Black"):
    return ImageFont.truetype(f"{FD}Inter-{weight}.otf", int(size))


def _background():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((x - CX) ** 2 + (y - CY) ** 2) / 900.0
    v = np.clip(20 * (1 - d), 0, 20)
    return np.repeat(v[:, :, None], 3, 2)


BG = _background()


def ball_colors(col, born, t, last_stage_mix=True):
    base = np.array(PALETTE, dtype=np.float32)[np.clip(col, 0, len(PALETTE) - 1)]
    if last_stage_mix:   # final generation: violet/blue/white mix like the reference finale
        m = col >= len(PALETTE) - 1
        if m.any():
            idx = (np.arange(len(col))[m] * 2654435761) % 3
            base[m] = np.array([(180, 120, 255), (90, 140, 255), (255, 255, 255)], np.float32)[idx]
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


def fmt(n):
    return f"{n:,}".replace(",", ".")


def render_frame(fr, t, events, goal, rb, hook="WARTE AUF DIE EXPLOSION…", hook_end=2.0):
    # ---- balls (supersampled)
    layer = Image.new("RGB", (W * SS, H * SS), (0, 0, 0))
    d = ImageDraw.Draw(layer)
    pos = fr["pos"]
    cols = ball_colors(fr["col"], fr["born"], t).astype(np.uint8)
    radii = np.where(fr["col"] == 0, rb * 2.2, rb) * SS     # the single start ball is drawn bigger
    for (x, y), c, r in zip(pos * SS, cols, radii):
        d.ellipse((x - r, y - r, x + r, y + r), fill=tuple(int(v) for v in c))
    small = layer.resize((W, H), Image.BILINEAR)
    arr = np.asarray(small, dtype=np.float32)
    # glow: blurred copy, added
    g = small.resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(4))
    glow = np.asarray(g.resize((W, H), Image.BILINEAR), dtype=np.float32)
    # extra bloom right after an explosion
    bloom = 0.0
    for e in events:
        if 0 <= t - e["t"] < 0.6:
            bloom = max(bloom, 1 - (t - e["t"]) / 0.6)
    dens = 1.0 / (1.0 + len(pos) / 1500.0)          # less glow when the arena is crowded
    g2 = np.clip(glow * (1.2 + 1.2 * bloom) * dens, 0, 255)
    base = np.clip(BG + arr, 0, 255)
    out = 255 - (255 - base) * (255 - g2) / 255.0   # screen blend: glows without burning out
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

    # ---- stage (ring, jaw, hub) drawn supersampled on top
    st = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    sd.ellipse(((CX - R) * SS, (CY - R) * SS, (CX + R) * SS, (CY + R) * SS), outline=(235, 235, 240, 230), width=3 * SS)
    for ang in (fr["a1"], fr["a2"]):
        draw_blade(sd, ang, LABEL)
    for ang in (fr["a1"], fr["a2"]):
        paste_label(st, ang, LABEL)
    sd = ImageDraw.Draw(st)
    sd.ellipse(((CX - 9) * SS, (CY - 9) * SS, (CX + 9) * SS, (CY + 9) * SS), fill=(10, 10, 12), outline=(200, 200, 205), width=2 * SS)
    st = st.resize((W, H), Image.LANCZOS)
    img.paste(st, (0, 0), st)

    # ---- HUD
    hd = ImageDraw.Draw(img, "RGBA")
    hd.text((CX, 262), f"{fr['rpm']}  U / M I N", font=font(24, "Medium"), fill=(95, 95, 102), anchor="ms")
    if t < hook_end:
        a = int(255 * min(1, (hook_end - t) / 0.2))
        hd.text((CX, 360), hook, font=font(54, "Black"), fill=(255, 255, 255, a), anchor="ms")
    hd.text((CX, CY - R - 22), "F O L L O W", font=font(24, "Medium"), fill=(110, 110, 118), anchor="ms")
    total = len(pos)
    done = total >= goal
    num = fmt(total)
    fnum = font(92, "Thin")
    fsmall = font(40, "Light")
    wnum = hd.textlength(num, font=fnum)
    wgoal = hd.textlength(f" / {fmt(goal)}", font=fsmall)
    x0 = CX - (wnum + wgoal) / 2
    yb = CY + R + 120
    hd.text((x0, yb), num, font=fnum, fill=(255, 214, 90) if done else (255, 255, 255), anchor="ls")
    hd.text((x0 + wnum, yb), f" / {fmt(goal)}", font=fsmall, fill=(150, 150, 158), anchor="ls")
    for e in events:   # blue +N next to the counter
        if 0 <= t - e["t"] < 0.8:
            a = int(255 * min(1, (0.8 - (t - e["t"])) / 0.2))
            hd.text((x0 + wnum + wgoal + 8, yb - 62), f"+{fmt(e['new'] - e['caught'])}", font=font(30, "SemiBold"),
                    fill=(74, 163, 255, a), anchor="ls")
    # progress bar
    bw = 520
    hd.rectangle((CX - bw / 2, yb + 26, CX + bw / 2, yb + 28), fill=(60, 60, 66))
    hd.rectangle((CX - bw / 2, yb + 26, CX - bw / 2 + bw * min(1, total / goal), yb + 28),
                 fill=(255, 214, 90) if done else (74, 163, 255))
    if done:
        hd.text((CX, yb + 86), "Z I E L   E R R E I C H T", font=font(28, "SemiBold"), fill=(255, 214, 90), anchor="ms")
    return img
