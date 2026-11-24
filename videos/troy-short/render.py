"""Vertical Shorts renderer (1080x1920, 24 fps) with burned-in animated subtitles.
  python3 render.py stills <vo_dir> <out_dir> [shot ...]
  python3 render.py video  <vo_dir> <out.mp4> [workers]"""
import sys, os, json, math, re, subprocess, multiprocessing as mp
import cairo
from gfx import W, H, new_ctx, setc, clamp, prog, text, text_width, back_out, ease, TITLE_FONT, INK, WHITE
from scenes import SHOT_FUNCS
import scenes

FPS = 24
XFADE = 0.18
# target duration per scene from the brief (0-5, 5-12, 12-20, 20-30, 30-43, 43-55, 55-60)
TARGET = {"hook": 4.6, "discovery": 7.0, "gift": 8.0, "night": 10.0, "twist": 12.5, "ending": 12.0, "cta": 5.2}
VO_OFF = {"night": 1.4, "twist": 0.4, "ending": 0.6}     # visual beat before the voice starts
FLASH_IN = {"cta"}
KEYWORDS = {"ten-year", "war", "free", "horse", "horse!", "massive", "wooden", "take", "troy", "gift", "loved",
            "party", "sneeze", "sneeze!", "tiny", "door", "dozens", "greek", "soldiers", "army", "army!",
            "destroy", "reviews", "gifts", "subscribe", "history", "world", "safe", "accidentally"}


def build_timeline(vo_dir):
    meta = json.load(open(os.path.join(vo_dir, "timing.json")))
    shots, t = [], 0.0
    for m in meta:
        off = VO_OFF.get(m["id"], 0.0)
        d = max(TARGET.get(m["id"], 0), off + m["dur"] + m["pause"])
        sents = [[a + off, b + off, s] for a, b, s in m["sents"]]
        shots.append({"id": m["id"], "start": t, "D": d, "sents": sents, "vo": m["id"], "vo_off": off})
        t += d
    return shots, t


def make_cue(shot):
    sents = shot["sents"]

    def cue(text_, which="start", frac=None):
        for a, b, s in sents:
            if text_ in s:
                if frac is not None:
                    return a + (b - a) * frac
                return b if which == "end" else a
        raise KeyError(f"cue '{text_}' not found in shot {shot['id']}")
    return cue


def word_chunks(shots):
    """split narration into on-screen chunks (<=3 words) with per-word times (by character weight)."""
    chunks = []
    for s in shots:
        for a, b, sent in s["sents"]:
            words = sent.replace("...", "… ").split()
            weights = [len(w) + 2 for w in words]
            tot = sum(weights)
            t = s["start"] + a
            timed = []
            for w, wt in zip(words, weights):
                d = (b - a) * wt / tot
                timed.append((w, t, t + d))
                t += d
            cur = []
            for i, item in enumerate(timed):
                cur.append(item)
                if len(cur) == 3 or item[0][-1] in ",.!?…" or i == len(timed) - 1:
                    chunks.append(cur)
                    cur = []
    return chunks


def draw_subs(ctx, T, chunks):
    cur = None
    for i, c in enumerate(chunks):
        end = chunks[i + 1][0][1] if i + 1 < len(chunks) else c[-1][2] + 0.6
        end = min(end, c[-1][2] + 0.6)
        if c[0][1] <= T < end:
            cur = c
            break
    if not cur:
        return
    size = 92
    words = [w for w, _, _ in cur]
    widths = [text_width(ctx, w.upper(), size) + 30 for w in words]
    gap = 22
    total = sum(widths) + gap * (len(words) - 1)
    lines = [list(range(len(words)))]
    if total > W - 100:
        lines = [list(range(len(words) - 1)), [len(words) - 1]]
    k0 = clamp((T - cur[0][1]) / 0.12)
    for li, idxs in enumerate(lines):
        lw = sum(widths[i] for i in idxs) + gap * (len(idxs) - 1)
        x = W / 2 - lw / 2
        y = 1610 + li * 108 - (54 if len(lines) == 2 else 0)
        for i in idxs:
            w, a, b = cur[i]
            key = re.sub(r"[^a-z\-!]", "", w.lower()) in KEYWORDS or re.sub(r"[^a-z\-]", "", w.lower()) in KEYWORDS
            active = a <= T < b + 0.05
            col = (1, 0.87, 0.15) if key else WHITE
            sc = (0.6 + 0.4 * back_out(k0, 2.0)) * (1.12 if active else 1.0)
            ctx.save()
            ctx.translate(x + widths[i] / 2, y)
            ctx.scale(sc, sc)
            ctx.rotate(-0.04 if (active and key) else 0)
            text(ctx, w.upper(), 0, 0, size, col, font=TITLE_FONT, outline=13)
            ctx.restore()
            x += widths[i] + gap


class Renderer:
    def __init__(self, vo_dir):
        self.shots, self.total = build_timeline(vo_dir)
        self.cues = [make_cue(s) for s in self.shots]
        scenes.TIMELINE = {s["id"]: (s, c) for s, c in zip(self.shots, self.cues)}
        self.chunks = word_chunks(self.shots)
        self.surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
        self.surf2 = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)

    def shot_at(self, T):
        for i, s in enumerate(self.shots):
            if T < s["start"] + s["D"]:
                return i
        return len(self.shots) - 1

    def draw_shot(self, surf, i, t):
        s = self.shots[i]
        ctx = new_ctx(surf)
        ctx.save()
        SHOT_FUNCS[s["id"]](ctx, t, s["D"], self.cues[i])
        ctx.restore()
        return ctx

    def frame(self, T, subs=True):
        i = self.shot_at(T)
        s = self.shots[i]
        t = T - s["start"]
        ctx = self.draw_shot(self.surf, i, t)
        if i > 0 and t < XFADE and s["id"] not in FLASH_IN:
            p = self.shots[i - 1]
            self.draw_shot(self.surf2, i - 1, p["D"] + t)
            ctx.set_source_surface(self.surf2, 0, 0)
            ctx.paint_with_alpha(1 - t / XFADE)
        if s["id"] in FLASH_IN and i > 0:
            a = 1 - clamp(t / 0.35)
            if a > 0:
                setc(ctx, (1, 1, 1), a)
                ctx.paint()
        if subs:
            draw_subs(ctx, T, self.chunks)
        self.surf.flush()
        return self.surf


def stills(vo_dir, out_dir, only):
    os.makedirs(out_dir, exist_ok=True)
    r = Renderer(vo_dir)
    for i, s in enumerate(r.shots):
        if only and s["id"] not in only:
            continue
        n = 8
        tiles = cairo.ImageSurface(cairo.FORMAT_RGB24, W * 2, H)
        tc = cairo.Context(tiles)
        for k in range(n):
            T = s["start"] + s["D"] * (k + 0.5) / n
            surf = r.frame(T)
            tc.save()
            tc.translate((k % 4) * W / 2, (k // 4) * H / 2)
            tc.scale(0.5, 0.5)
            tc.set_source_surface(surf, 0, 0)
            tc.paint()
            tc.restore()
        tiles.write_to_png(os.path.join(out_dir, f"{i:02d}_{s['id']}.png"))
        print("still", s["id"], f"{s['start']:.1f}s +{s['D']:.1f}s")


def _worker(args):
    vo_dir, f0, f1, path = args
    r = Renderer(vo_dir)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr0",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                           "-crf", "19", "-pix_fmt", "yuv420p", "-tune", "animation", path], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        ff.stdin.write(bytes(r.frame(f / FPS).get_data()))
    ff.stdin.close()
    ff.wait()
    return path


def video(vo_dir, out, workers=4):
    _, total = build_timeline(vo_dir)
    nf = int(math.ceil(total * FPS))
    print(f"total {total:.2f}s, {nf} frames")
    tmp = out + ".parts"
    os.makedirs(tmp, exist_ok=True)
    n = workers * 3
    bounds = [round(nf * k / n) for k in range(n + 1)]
    jobs = [(vo_dir, bounds[k], bounds[k + 1], os.path.join(tmp, f"p{k:03d}.mp4")) for k in range(n)]
    with mp.Pool(workers) as pool:
        parts = pool.map(_worker, jobs, chunksize=1)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out],
                   check=True)
    print("wrote", out)


if __name__ == "__main__":
    if sys.argv[1] == "stills":
        stills(sys.argv[2], sys.argv[3], sys.argv[4:])
    else:
        video(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 4)
