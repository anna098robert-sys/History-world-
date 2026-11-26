"""Timeline for the vertical Short (src/short/timeline.json). Scene lengths follow the brief; the narration
inside each scene starts after VO_OFF seconds so the action can lead."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = {"s_hook": 5.0, "s_travel": 7.0, "s_reveal": 8.0, "s_panic": 8.0, "s_cliff": 6.5}
VO_OFF = {"s_hook": 0.15, "s_travel": 1.5, "s_reveal": 0.9, "s_panic": 0.3, "s_cliff": 0.25}
meta = json.load(open(os.path.join(ROOT, "public/short/vo/timing.json")))
shots, t = [], 0.0
for m in meta:
    off = VO_OFF[m["id"]]
    d = max(TARGET[m["id"]], off + m["dur"] + 0.3)
    shots.append({"id": m["id"], "start": round(t, 4), "dur": d, "vo": f"short/vo/{m['id']}.mp3", "voOff": off,
                  "voDur": round(m["dur"], 4), "sents": [[round(a + off, 4), round(b + off, 4), s] for a, b, s in m["sents"]]})
    t += d
json.dump({"fps": 30, "total": round(t, 4), "frames": int(round(t * 30)), "shots": shots},
          open(os.path.join(ROOT, "src/short/timeline.json"), "w"), indent=1)
print(f"{t:.1f}s, {int(round(t * 30))} frames")
