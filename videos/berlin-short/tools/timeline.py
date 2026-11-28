"""Timeline for the Short (src/timeline.json): scene lengths from the brief, stretched only where narration needs it."""
import json, os, subprocess, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = {"b_hook": 4.0, "b_crowd": 6.2, "b_divided": 7.0, "b_cross": 7.2, "b_hammer": 6.8, "b_hug": 6.2, "b_end": 4.0}
VO_OFF = {"b_hook": 0.1, "b_crowd": 0.4, "b_divided": 0.15, "b_cross": 0.4, "b_hammer": 0.5, "b_hug": 0.8, "b_end": 0.15}
meta = json.load(open(os.path.join(ROOT, "public/vo/timing.json")))
shots, t = [], 0.0
for m in meta:
    off = VO_OFF[m["id"]]
    d = round(max(TARGET[m["id"]], off + m["dur"] + 0.25), 3)
    shots.append({"id": m["id"], "start": round(t, 4), "dur": d, "vo": f"vo/{m['id']}.mp3", "voOff": off, "voDur": round(m["dur"], 4),
                  "sents": [[round(a + off, 4), round(b + off, 4), s] for a, b, s in m["sents"]]})
    t += d
json.dump({"fps": 30, "total": round(t, 4), "frames": int(round(t * 30)), "shots": shots}, open(os.path.join(ROOT, "src/timeline.json"), "w"), indent=1)
for w in glob.glob(os.path.join(ROOT, "public/vo/*.wav")):
    if not w.endswith("_raw.wav"):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", w, "-c:a", "libmp3lame", "-b:a", "160k", w[:-4] + ".mp3"], check=True)
print(f"{t:.1f}s")
for s in shots: print(s["id"], round(s["start"], 1), s["dur"])
