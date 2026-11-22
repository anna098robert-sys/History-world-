"""Render the film. Usage:
  python3 render.py stills <vo_dir> <out_dir> [shot ...]   -> PNG contact frames per shot
  python3 render.py video  <vo_dir> <out.mp4> [workers]     -> silent video (H.264)"""
import sys, os, json, math, subprocess, multiprocessing as mp
import cairo
from gfx import W, H, new_ctx, setc, clamp, prog
from scenes import SHOT_FUNCS

FPS = 24
XFADE = 0.3          # crossfade between ordinary cuts
FLASH_IN = {"tunnel1", "tunnel2", "tunnel3", "tunnel4", "pisa_arrive", "newton_arrive", "fleming_arrive",
            "return", "title"}
EXTRA = {"title": 4.0, "endcard": 7.0}


def build_timeline(vo_dir):
    meta = json.load(open(os.path.join(vo_dir, "timing.json")))
    shots, t = [], 0.0
    for m in meta:
        d = m["dur"] + m["pause"]
        shots.append({"id": m["id"], "start": t, "D": d, "sents": m["sents"], "vo": m["id"]})
        t += d
        if m["id"] == "hook":
            shots.append({"id": "title", "start": t, "D": EXTRA["title"], "sents": [], "vo": None})
            t += EXTRA["title"]
    shots.append({"id": "endcard", "start": t, "D": EXTRA["endcard"], "sents": [], "vo": None})
    t += EXTRA["endcard"]
    return shots, t


def make_cue(shot):
    sents = shot["sents"]

    def cue(text, which="start", frac=None):
        for a, b, s in sents:
            if text in s:
                if frac is not None:
                    return a + (b - a) * frac
                return b if which == "end" else a
        raise KeyError(f"cue '{text}' not found in shot {shot['id']}")
    return cue


class Renderer:
    def __init__(self, vo_dir):
        self.shots, self.total = build_timeline(vo_dir)
        self.cues = [make_cue(s) for s in self.shots]
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

    def frame(self, T):
        i = self.shot_at(T)
        s = self.shots[i]
        t = T - s["start"]
        ctx = self.draw_shot(self.surf, i, t)
        # crossfade from previous shot for ordinary cuts
        if i > 0 and t < XFADE and s["id"] not in FLASH_IN:
            p = self.shots[i - 1]
            self.draw_shot(self.surf2, i - 1, p["D"] + t)
            k = t / XFADE
            ctx.set_source_surface(self.surf2, 0, 0)
            ctx.paint_with_alpha(1 - k)
        # white flash for time jumps
        if s["id"] in FLASH_IN and i > 0:
            a = 1 - clamp(t / 0.45)
            if a > 0:
                setc(ctx, (1, 1, 1), a)
                ctx.paint()
        nxt = self.shots[i + 1]["id"] if i + 1 < len(self.shots) else None
        if nxt in FLASH_IN:
            a = clamp((t - (s["D"] - 0.25)) / 0.25)
            if a > 0:
                setc(ctx, (1, 1, 1), a)
                ctx.paint()
        if T < 0.4:
            setc(ctx, (0, 0, 0), 1 - T / 0.4)
            ctx.paint()
        self.surf.flush()
        return self.surf


def stills(vo_dir, out_dir, only):
    os.makedirs(out_dir, exist_ok=True)
    r = Renderer(vo_dir)
    for i, s in enumerate(r.shots):
        if only and s["id"] not in only:
            continue
        n = 6
        tiles = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
        tc = cairo.Context(tiles)
        for k in range(n):
            T = s["start"] + s["D"] * (k + 0.5) / n
            surf = r.frame(T)
            tc.save()
            tc.translate((k % 3) * W / 3, (k // 3) * H / 2)
            tc.scale(1 / 3, 1 / 3)
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
                           "-crf", "19", "-pix_fmt", "yuv420p", "-tune", "animation", path],
                          stdin=subprocess.PIPE)
    for f in range(f0, f1):
        surf = r.frame(f / FPS)
        ff.stdin.write(bytes(surf.get_data()))
        if (f - f0) % 480 == 0:
            print(f"  worker {f0}: {f - f0}/{f1 - f0}", flush=True)
    ff.stdin.close()
    ff.wait()
    return path


def video(vo_dir, out, workers=4):
    _, total = build_timeline(vo_dir)
    nf = int(math.ceil(total * FPS))
    print(f"total {total:.2f}s, {nf} frames")
    tmp = out + ".parts"
    os.makedirs(tmp, exist_ok=True)
    nchunks = workers * 3
    bounds = [round(nf * k / nchunks) for k in range(nchunks + 1)]
    jobs = [(vo_dir, bounds[k], bounds[k + 1], os.path.join(tmp, f"p{k:03d}.mp4")) for k in range(nchunks)]
    with mp.Pool(workers) as pool:
        parts = pool.map(_worker, jobs, chunksize=1)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    out], check=True)
    print("wrote", out)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "stills":
        stills(sys.argv[2], sys.argv[3], sys.argv[4:])
    else:
        video(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 4)
