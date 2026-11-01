"""Renders the full TikTok video: scenes + HUD + word-by-word captions + glitch,
muxed with build/mix.wav (run audio_mix.py first)."""
import math
import random
import subprocess
import sys
from multiprocessing import Pool

from PIL import Image, ImageDraw

import scenes as S
from script import SEQ
from timing import words, seq_bounds

FPS = 30
OUT = sys.argv[1] if len(sys.argv) > 1 else "build/bankraub_der_umschlag.mp4"
CAP_Y = {8: 1300}
MAX_CAP_W = 760

BOUNDS, TOTAL = seq_bounds()
WORDS = words()


def norm(w):
    return w.strip(".,:?!“„'").lower()


HI = {i: {norm(h) for h in sq["hi"]} for i, sq in enumerate(SEQ)}


def build_chunks():
    """Group words into on-screen chunks of max 3 words / MAX_CAP_W px, never across phrases."""
    f = S.font(72, "Black")
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    chunks, cur, phrase_end = [], [], None
    prev_b = None
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
        a = c[0]["a"]
        nxt = chunks[k + 1][0]["a"] if k + 1 < len(chunks) else TOTAL
        b = min(nxt, c[-1]["b"] + 0.45)
        out.append(dict(words=c, a=a, b=b))
    return out


CHUNKS = build_chunks()


def mmss(sec):
    sec = max(0, int(round(sec)))
    return f"{sec // 60:02d}:{sec % 60:02d}"


def alarm_secs(v):
    m, s = v.split(":")
    return int(m) * 60 + int(s)


def hud_values(i, lt, dur):
    beute, crew, hitze, alarm = SEQ[i]["hud"]
    prev = SEQ[i - 1]["hud"] if i else SEQ[0]["hud"]
    k = min(1.0, lt / 0.6)
    hitze = int(round(prev[2] + (hitze - prev[2]) * k))
    if i == 4:  # vault opens: counter rattles up
        k2 = min(1.0, max(0.0, (lt - 0.4) / 1.6))
        beute = int(beute * (1 - (1 - k2) ** 3) / 1000) * 1000
    a0 = alarm_secs(alarm)
    a1 = alarm_secs(SEQ[i + 1]["hud"][3]) if i + 1 < len(SEQ) else a0
    if i == 7:  # frozen during PAUSE
        a1 = a0
    alarm_val = mmss(a0 + (a1 - a0) * min(1.0, lt / dur))
    alarm_col = None
    if a0 == 0:
        alarm_col = S.C["red"] if int(lt * 4) % 2 == 0 else S.C["white"]
    crew_col = None
    if i == 10:
        if lt < 2.4:
            crew = 3
        elif lt < 3.4:
            crew_col = S.C["red"] if int(lt * 8) % 2 == 0 else S.C["white"]
    return beute, crew, hitze, alarm_val, alarm_col, crew_col


def kenburns(img, z, dx=0, dy=0):
    if z <= 0.001 and not dx and not dy:
        return img
    w, h = img.size
    nw, nh = int(w * (1 + z)), int(h * (1 + z))
    big = img.resize((nw, nh), Image.BILINEAR)
    x0 = (nw - w) // 2 + dx
    y0 = (nh - h) // 2 + dy
    return big.crop((x0, y0, x0 + w, y0 + h))


def frame(n):
    t = n / FPS
    i = next(k for k, (a, b) in enumerate(BOUNDS) if a <= t < b or k == len(BOUNDS) - 1)
    a, b = BOUNDS[i]
    dur = b - a
    lt = t - a
    p = min(1.0, lt / dur)

    if i == 7:  # PAUSE: frozen envelope frame
        img = S.render(6, 1.0)
        img = kenburns(img, 0.16)
    else:
        img = S.render(i, p)
        z = 0.02 + 0.07 * p
        if i == 6:
            z = 0.02 + 0.14 * p ** 1.5
        if i == 8:
            z = 0.03 * p
        if lt < 0.2:  # punch-in on every cut
            z += 0.07 * (1 - lt / 0.2)
        dx = dy = 0
        if i == 9:  # alarm shake
            rnd = random.Random(n)
            dx, dy = rnd.randint(-14, 14), rnd.randint(-14, 14)
        img = kenburns(img, z, dx, dy)

    S.hud(img, *hud_values(i, lt, dur))
    if i == 7:
        strength = 0.7 + 0.5 * abs(math.sin(lt * 9))
        img = S.glitch(img, strength, timecode=f"SP 00:00:{34 + int(lt):02d}")

    for c in CHUNKS:
        if c["a"] <= t < c["b"]:
            ws = [w["w"] for w in c["words"]]
            hi = [k for k, w in enumerate(c["words"]) if norm(w["w"]) in HI[w["seq"]]]
            vis = sum(1 for w in c["words"] if w["a"] <= t + 0.03)
            S.caption(img, ws, hi=hi, y=CAP_Y.get(i, 1210), visible=max(1, vis))
            break

    # white flash on big moments
    if i in (4, 9) and lt < 0.12:
        img = Image.blend(img, Image.new("RGB", img.size, (255, 255, 255)), 0.7 * (1 - lt / 0.12))
    if i == 8 and lt < 0.15:  # coming out of the pause: glitch tail
        img = S.glitch(img, 0.6, timecode="▶ PLAY")
    return img.tobytes()


def main():
    nframes = int(TOTAL * FPS)
    cmd = ["ffmpeg", "-v", "error", "-y",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{S.W}x{S.H}", "-r", str(FPS), "-i", "-",
           "-i", "build/mix.wav",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-profile:v", "high", "-movflags", "+faststart",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-shortest", OUT]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for k, buf in enumerate(pool.imap(frame, range(nframes), chunksize=4)):
            ff.stdin.write(buf)
            if k % 150 == 0:
                print(f"{k}/{nframes}", flush=True)
    ff.stdin.close()
    ff.wait()
    print("done", OUT, nframes / FPS, "s")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--still":
        for n in map(int, sys.argv[2].split(",")):
            Image.frombytes("RGB", (S.W, S.H), frame(n)).save(f"build/still_{n}.png")
    else:
        main()
