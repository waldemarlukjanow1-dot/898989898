"""Renders 'Patient Null – Teil 2' in the clear style: simple motion, no flicker, text inserts."""
import math
import subprocess
import sys
from multiprocessing import Pool

from PIL import Image, ImageDraw

import scenes7 as S4
from scenes7 import S
from script import SEQ
from timing import words, seq_bounds, PHRASES, TEMPO

FPS = 30
OUT = sys.argv[1] if len(sys.argv) > 1 else "build/patient_null_teil2_raw.mp4"
MAX_CAP_W = 760
BOUNDS, TOTAL = seq_bounds()
WORDS = words()
PAUSE = S4.PAUSE


def at(text):
    return next(a / TEMPO for a, b, s, t in PHRASES if text in t)


INSERT_AT = {0: at("Und du hast dich gerade"), 2: at("Und die Zombies machen") + 0.5, 4: at("Ein Video."),
             5: at("Absichtlich."), 7: at("Ich bin das Gegenmittel."), 8: at("Zum ersten Mal"), 9: at("Noch vierundzwanzig")}


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


def hud_values(i, t, lt):
    u, z, m = SEQ[i]["hud"]
    pz, pm = (SEQ[i - 1]["hud"][1], SEQ[i - 1]["hud"][2]) if i else (z, m)
    k = min(1.0, lt / 0.8)
    z = int(round(pz + (z - pz) * k))
    m = int(round(pm + (m - pm) * k))
    return u, z, m


def zoom(img, z):
    if z < 0.002:
        return img
    w, h = img.size
    nw, nh = int(w * (1 + z)), int(h * (1 + z))
    big = img.resize((nw, nh), Image.BILINEAR)
    x0, y0 = (nw - w) // 2, (nh - h) // 2
    return big.crop((x0, y0, x0 + w, y0 + h))


def frame(n):
    t = n / FPS
    if t > TOTAL - 0.25:
        return Image.new("RGB", (S.W, S.H), (0, 0, 0)).tobytes()
    i = next(k for k, (a, b) in enumerate(BOUNDS) if a <= t < b or k == len(BOUNDS) - 1)
    a, b = BOUNDS[i]
    lt, p = t - a, min(1.0, (t - a) / (b - a))
    img = S4.render(i, p)
    img = zoom(img, 0.05 * p + (0.03 * (1 - lt / 0.15) if lt < 0.15 else 0))
    S4.hud(img, *hud_values(i, t, lt))
    ins = SEQ[i]["insert"]
    t_in = INSERT_AT.get(i, a + 0.3)
    if ins and t >= t_in and i != PAUSE:
        S4.insert(img, ins, (t - t_in) / 0.25)
    if i == PAUSE:
        img = S.glitch(img, 0.6 + 0.3 * abs(math.sin(lt * 6)), timecode=f"SP 00:00:{31 + int(lt):02d}")
    for c in CHUNKS:
        if c["a"] <= t < c["b"]:
            ws = [w["w"] for w in c["words"]]
            hi = [k for k, w in enumerate(c["words"]) if norm(w["w"]) in HI[w["seq"]]]
            vis = sum(1 for w in c["words"] if w["a"] <= t + 0.03)
            S.caption(img, ws, hi=hi, y=1210, visible=max(1, vis))
            break
    return img.tobytes()


def main():
    nframes = int(TOTAL * FPS)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{S.W}x{S.H}",
           "-r", str(FPS), "-i", "-", "-i", "build/mix.wav",
           "-c:v", "libx264", "-preset", "medium", "-b:v", "9M", "-maxrate", "12M", "-bufsize", "18M",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", OUT]
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
