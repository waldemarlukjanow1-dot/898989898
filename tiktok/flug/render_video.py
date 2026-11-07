"""Renders 'Flug 404' – STIL 3, every action cued to the voice, soft crossfades on every cut."""
import subprocess
import sys
from multiprocessing import Pool

from PIL import Image, ImageDraw

import scenes14 as R
import style3 as T
from script import SEQ
from timing import words, seq_bounds

FPS = 30
OUT = sys.argv[1] if len(sys.argv) > 1 else "build/flug404_raw.mp4"
MAX_CAP_W = 760
XF = 0.3  # crossfade length (s)
BOUNDS, TOTAL = seq_bounds()
WORDS = words()
CUTS = sorted([a for a, _ in BOUNDS[1:]] + R.INNER_CUTS)


def norm(w):
    return w.strip(".,:?!“„'–").lower()


HI = {i: {norm(h) for h in sq["hi"]} for i, sq in enumerate(SEQ)}


def build_chunks():
    f = T.font(70, "Black")
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


def scene_at(ta):
    i = next(k for k, (a, b) in enumerate(BOUNDS) if a <= ta < b or k == len(BOUNDS) - 1)
    a, b = BOUNDS[i]
    return i, min(1.0, (ta - a) / (b - a)), b - a


def picture(ta):
    i, p, dur = scene_at(ta)
    img = R.render(i, p, dur, ta)
    T.chip(img, *R.chip_for(i, ta), k=1.0)
    return img


def frame(n):
    ta = n / FPS
    img = picture(ta)
    for c in CUTS:  # soft crossfade: blend the last frame before the cut into the new shot
        if 0 <= ta - c < XF:
            prev = picture(c - 1 / FPS)
            img = Image.blend(prev, img, (ta - c) / XF)
            break
    for c in CHUNKS:
        if c["a"] <= ta < c["b"]:
            ws = [w["w"] for w in c["words"]]
            hi = [k for k, w in enumerate(c["words"]) if norm(w["w"]) in HI[w["seq"]]]
            vis = sum(1 for w in c["words"] if w["a"] <= ta + 0.03)
            T.caption(img, ws, hi=hi, visible=max(1, vis))
            break
    return img.tobytes()


def main():
    nframes = int(TOTAL * FPS)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{T.W}x{T.H}",
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
            Image.frombytes("RGB", (T.W, T.H), frame(n)).save(f"build/still_{n}.png")
    else:
        main()
