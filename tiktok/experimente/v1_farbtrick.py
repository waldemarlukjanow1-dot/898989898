"""Video 1 – „Der Farbtrick“ (optische Täuschung / Nachbild, Zuschauer macht mit).

0.0–5.8 s  Negativ eines farbigen Bildes (Ballon über Hügeln), Punkt in der Mitte, Fortschrittsring.
5.8–7.7 s  Schnitt auf Schwarz-Weiß: das Gehirn malt die echten Farben hinein (Nachbild).
7.7–8.0 s  Überblendung zurück ins Negativ -> Loop.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from common import W, H, SR, DUR, Track, encode, t_axis

FD = "/usr/share/fonts/opentype/inter/"
SWITCH, BACK = 5.8, 7.7


def scene():
    """Big, simple, very saturated shapes (best for the afterimage)."""
    S = 2
    im = Image.new("RGB", (W * S, H * S))
    d = ImageDraw.Draw(im)
    for y in range(H * S):                                    # sky: deep blue -> turquoise
        f = y / (H * S * 0.62)
        d.line([(0, y), (W * S, y)], fill=(int(10 + 30 * f), int(60 + 150 * f), int(220 + 20 * f)))
    d.ellipse((700 * S, 280 * S, 980 * S, 560 * S), fill=(255, 220, 0))                 # sun
    d.polygon([(0, 1250 * S), (300 * S, 1080 * S), (620 * S, 1230 * S), (1080 * S, 1060 * S), (1080 * S, 1920 * S),
               (0, 1920 * S)], fill=(20, 200, 60))                                       # hills
    d.polygon([(0, 1500 * S), (450 * S, 1350 * S), (1080 * S, 1480 * S), (1080 * S, 1920 * S), (0, 1920 * S)],
              fill=(0, 150, 40))
    cx, cy = 430 * S, 760 * S                                                          # hot-air balloon
    d.ellipse((cx - 260 * S, cy - 300 * S, cx + 260 * S, cy + 260 * S), fill=(235, 20, 40))
    for k in (-1, 1):
        d.chord((cx - 260 * S, cy - 300 * S, cx + 260 * S, cy + 260 * S), 90 + k * 0, 90, fill=(235, 20, 40))
    d.ellipse((cx - 110 * S, cy - 300 * S, cx + 110 * S, cy + 260 * S), fill=(255, 140, 0))
    d.polygon([(cx - 150 * S, cy + 200 * S), (cx + 150 * S, cy + 200 * S), (cx + 60 * S, cy + 330 * S),
               (cx - 60 * S, cy + 330 * S)], fill=(235, 20, 40))
    d.rectangle((cx - 70 * S, cy + 380 * S, cx + 70 * S, cy + 480 * S), fill=(150, 80, 20))
    for k in (-1, 1):
        d.line([(cx + k * 60 * S, cy + 330 * S), (cx + k * 60 * S, cy + 380 * S)], fill=(80, 40, 10), width=6 * S)
    for x, y, c in ((160, 1640, (255, 0, 160)), (330, 1700, (255, 230, 0)), (820, 1660, (255, 0, 160)),
                    (930, 1760, (255, 230, 0)), (620, 1790, (255, 0, 160))):                     # flowers
        d.ellipse(((x - 55) * S, (y - 55) * S, (x + 55) * S, (y + 55) * S), fill=c)
    return np.asarray(im.resize((W, H), Image.LANCZOS)).astype(np.float32)


COL = scene()
NEG = 255 - COL
# slightly brighter / more saturated negative strengthens the afterimage
NEG = np.clip((NEG - 128) * 1.15 + 128, 0, 255)
GRAY = np.repeat((COL @ np.array([0.299, 0.587, 0.114], np.float32))[:, :, None], 3, 2)


def overlay(img, t, show_ring):
    im = Image.fromarray(img.astype(np.uint8))
    d = ImageDraw.Draw(im, "RGBA")
    cx, cy = 540, 860
    if show_ring:                                             # progress ring around the dot (no text needed)
        p = min(1.0, t / SWITCH)
        d.arc((cx - 46, cy - 46, cx + 46, cy + 46), -90, -90 + 360 * p, fill=(255, 255, 255, 200), width=6)
    d.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=(0, 0, 0), outline=(255, 255, 255), width=4)
    if show_ring and t < 2.2:
        a = int(255 * min(1, (2.2 - t) / 0.3))
        f = ImageFont.truetype(FD + "Inter-SemiBold.otf", 40)
        d.text((cx, cy + 120), "stare at the dot", font=f, fill=(255, 255, 255, a), anchor="ms")
    return np.asarray(im)


def frame(i):
    t = i / 30.0
    if t < SWITCH:
        return overlay(NEG, t, True)
    if t < BACK:
        return overlay(GRAY, t, False)
    u = (t - BACK) / (DUR - BACK)
    return overlay(GRAY * (1 - u) + NEG * u, t, True)


def sound(path):
    tr = Track()
    t = t_axis(DUR)
    drone = (np.sin(2 * np.pi * 110 * t) + 0.5 * np.sin(2 * np.pi * 165 * t) + 0.3 * np.sin(2 * np.pi * 220.5 * t))
    env = np.clip(t / SWITCH, 0, 1) ** 2 * (t < SWITCH)                    # tension rises while you stare
    tr.add(drone * (0.15 + 0.85 * env) * (t < SWITCH), 0, 0.25)
    for k in range(int(SWITCH / 0.5)):                                     # soft ticking countdown
        tk = t_axis(0.05)
        tr.add(np.sin(2 * np.pi * 1800 * tk) * np.exp(-tk * 90), 0.5 + k * 0.5, 0.12 + 0.02 * k)
    ts = t_axis(2.2)                                                       # the reveal: sparkle chord
    chord = sum(np.sin(2 * np.pi * f * ts) * np.exp(-ts * 1.6) for f in (523.3, 659.3, 784.0, 1046.5, 1318.5))
    whoosh = np.convolve(np.random.default_rng(1).standard_normal(len(ts)), np.ones(40) / 40, "same") * \
        np.exp(-ts * 5) * 3
    tr.add(chord * np.minimum(1, ts / 0.01) + whoosh, SWITCH, 0.6)
    tr.save(path, reverb=0.35)


if __name__ == "__main__":
    sound("build/v1.wav")
    encode(frame, 30, "build/v1.wav", "output/video1_farbtrick.mp4")
