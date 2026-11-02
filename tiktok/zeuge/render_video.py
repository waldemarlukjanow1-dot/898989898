"""Renders Der Zeuge: interrogation noir + HUD (GLAUBWÜRDIGKEIT) + captions + glitch flashbacks."""
import math
import random
import subprocess
import sys
from multiprocessing import Pool

from PIL import Image, ImageDraw

import scenes3 as S2
from scenes3 import S
from script import SEQ
from timing import words, seq_bounds, PHRASES, TEMPO

FPS = 30
OUT = sys.argv[1] if len(sys.argv) > 1 else "build/der_zeuge_raw.mp4"
MAX_CAP_W = 760
BOUNDS, TOTAL = seq_bounds()
WORDS = words()
PAUSE = 6
FLASHBACKS = (2, 5)


def at(text):
    return next(a / TEMPO for a, b, s, t in PHRASES if text in t)


T_HITS = ((at("Du lügst."), (220, 30, 40)), (at("Ein Geständnis."), (255, 255, 255)), (at("Er lächelt."), (255, 255, 255)))


def norm(w):
    return w.strip(".,:?!“„'").lower()


HI = {i: {norm(h) for h in sq["hi"]} for i, sq in enumerate(SEQ)}


def build_chunks():
    f = S.font(72, "Black")
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    chunks, cur, prev_b = [], [], None
    for w in WORDS:
        new_phrase = prev_b is not None and w["a"] - prev_b > 0.05
        trial = " ".join(x["w"] for x in cur + [w])
        if cur and (len(cur) >= 3 or new_phrase or d.textlength(trial, font=f) > MAX_CAP_W):
            chunks.append(cur)
            cur = []
        cur.append(w)
        prev_b = w["b"]
    chunks.append(cur)
    out = []
    for k, c in enumerate(chunks):
        nxt = chunks[k + 1][0]["a"] if k + 1 < len(chunks) else TOTAL
        out.append(dict(words=c, a=c[0]["a"], b=min(nxt, c[-1]["b"] + 0.45)))
    return out


CHUNKS = build_chunks()


def mm(v):
    m, sec = v.split(":")
    return int(m) * 60 + int(sec)


def hud_values(i, t, lt):
    glaub, minute, puls = SEQ[i]["hud"]
    prev = SEQ[i - 1]["hud"] if i else SEQ[0]["hud"]
    k = min(1.0, lt / 0.8)
    glaub = int(round(prev[0] + (glaub - prev[0]) * k))
    puls = int(round(prev[2] + (puls - prev[2]) * k + 3 * math.sin(t * 7)))
    m0 = mm(minute)
    m1 = mm(SEQ[i + 1]["hud"][1]) if i + 1 < len(SEQ) else m0
    if i == PAUSE:
        m1 = m0
    a, b = BOUNDS[i]
    cur = int(m0 + (m1 - m0) * min(1.0, lt / (b - a)))
    g_col = None
    if glaub <= 20:
        g_col = S2.C["red"] if int(t * 3) % 2 == 0 else S2.C["white"]
    return glaub, f"{cur // 60:02d}:{cur % 60:02d}", puls, g_col


def kenburns(img, z, dx=0, dy=0):
    w, h = img.size
    nw, nh = int(w * (1 + z)), int(h * (1 + z))
    big = img.resize((nw, nh), Image.BILINEAR)
    x0, y0 = (nw - w) // 2 + dx, (nh - h) // 2 + dy
    return big.crop((x0, y0, x0 + w, y0 + h))


def rewind(img, n, label):
    rr, g, bb = img.split()
    off = 6 + (n % 3) * 4
    rr = rr.transform(img.size, Image.AFFINE, (1, 0, off, 0, 1, 0))
    bb = bb.transform(img.size, Image.AFFINE, (1, 0, -off, 0, 1, 0))
    img = Image.merge("RGB", (rr, g, bb))
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(0, S.H, 6):
        d.rectangle((0, y, S.W, y + 2), fill=(0, 0, 0, 60))
    rnd = random.Random(n)
    for _ in range(3):
        y = rnd.randint(380, 1450)
        band = img.crop((0, y, S.W, y + 20))
        img.paste(band, (rnd.randint(-50, 50), y))
    d = ImageDraw.Draw(img, "RGBA")
    d.text((60, 380), label, font=S.mono(48), fill=S.C["white"], stroke_width=3, stroke_fill=(0, 0, 0))
    return img


def frame(n):
    t = n / FPS
    if n < 2:  # cold open: muzzle flash
        return Image.new("RGB", (S.W, S.H), (255, 236, 200)).tobytes()
    if n < 5 or t > TOTAL - 0.4:  # black beat / hard cut at the end
        return Image.new("RGB", (S.W, S.H), (0, 0, 0)).tobytes()
    i = next(k for k, (a, b) in enumerate(BOUNDS) if a <= t < b or k == len(BOUNDS) - 1)
    a, b = BOUNDS[i]
    lt, p = t - a, min(1.0, (t - a) / (b - a))

    if i == PAUSE:
        img = kenburns(S2.render(5, 0.95), 0.10)
    else:
        img = S2.render(i, p)
        z = 0.03 + 0.08 * p
        if i in (4, 8, 9):  # creeping push-ins: the look, the mirror, the confession
            z = 0.02 + 0.16 * p ** 1.3
        if lt < 0.2:
            z += 0.07 * (1 - lt / 0.2)
        dx = dy = 0
        if i in FLASHBACKS or i == 10:
            rnd = random.Random(n)
            dx, dy = rnd.randint(-8, 8), rnd.randint(-8, 8)
        img = kenburns(img, z, dx, dy)

    img = S2.noir(img, n, flicker=i != PAUSE)
    S2.hud(img, *hud_values(i, t, lt))

    if i == PAUSE:
        img = S.glitch(img, 0.7 + 0.5 * abs(math.sin(lt * 9)), timecode=f"SP 00:00:{34 + int(lt):02d}")
    if i in FLASHBACKS:
        img = rewind(img, n, "◀◀ GESTERN 23:41" if i == 2 else "◀◀ GESTERN 23:41 ?")

    for c in CHUNKS:
        if c["a"] <= t < c["b"]:
            ws = [w["w"] for w in c["words"]]
            hi = [k for k, w in enumerate(c["words"]) if norm(w["w"]) in HI[w["seq"]]]
            vis = sum(1 for w in c["words"] if w["a"] <= t + 0.03)
            S.caption(img, ws, hi=hi, y=1210, visible=max(1, vis))
            break

    for tf, col in T_HITS:
        if 0 <= t - tf < 0.15:
            img = Image.blend(img, Image.new("RGB", img.size, col), 0.6 * (1 - (t - tf) / 0.15))
    if i == PAUSE + 1 and lt < 0.15:
        img = S.glitch(img, 0.6, timecode="▶ PLAY")
    return img.tobytes()


def main():
    nframes = int(TOTAL * FPS)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{S.W}x{S.H}",
           "-r", str(FPS), "-i", "-", "-i", "build/mix.wav",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-movflags", "+faststart", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", OUT]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for k, buf in enumerate(pool.imap(frame, range(nframes), chunksize=4)):
            ff.stdin.write(buf)
            if k % 300 == 0:
                print(f"{k}/{nframes}", flush=True)
    ff.stdin.close()
    ff.wait()
    print("done", OUT)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--still":
        for n in map(int, sys.argv[2].split(",")):
            Image.frombytes("RGB", (S.W, S.H), frame(n)).save(f"build/still_{n}.png")
    else:
        main()
