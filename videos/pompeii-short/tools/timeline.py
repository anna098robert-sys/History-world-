"""Timeline for the Short (src/timeline.json): scene lengths from the brief (45 s), stretched only where narration needs it."""
import json, os, subprocess, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = {"p_hook": 4.0, "p_city": 7.0, "p_erupt": 7.0, "p_run": 7.4, "p_bury": 6.6, "p_escape": 6.0, "p_dig": 7.0}
VO_OFF = {"p_hook": 0.05, "p_city": 0.12, "p_erupt": 0.9, "p_run": 0.3, "p_bury": 0.8, "p_escape": 0.15, "p_dig": 0.2}
meta = json.load(open(os.path.join(ROOT, "public/vo/timing.json")))
shots, t = [], 0.0
for m in meta:
    off = VO_OFF[m["id"]]
    d = round(max(TARGET[m["id"]], off + m["dur"] + 0.2), 3)
    shots.append({"id": m["id"], "start": round(t, 4), "dur": d, "vo": f"vo/{m['id']}.mp3", "voOff": off, "voDur": round(m["dur"], 4),
                  "sents": [[round(a + off, 4), round(b + off, 4), s] for a, b, s in m["sents"]]})
    t += d
json.dump({"fps": 30, "total": round(t, 4), "frames": int(round(t * 30)), "shots": shots}, open(os.path.join(ROOT, "src/timeline.json"), "w"), indent=1)
for w in glob.glob(os.path.join(ROOT, "public/vo/*.wav")):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", w, "-c:a", "libmp3lame", "-b:a", "160k", w[:-4] + ".mp3"], check=True)
print(f"{t:.2f}s")
for s in shots: print(s["id"], round(s["start"], 2), s["dur"])
