"""Build the shared timeline (src/timeline.json) from the narration timing.
Remotion reads it for scene timing + subtitles; tools/audio.py reads it for music + SFX.
Usage: python3 tools/timeline.py"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FPS = 30
EXTRA_AFTER = {"hook": ("title", 4.5)}        # visual-only shots inserted after a narrated shot
PAD = {"impact": 1.5, "respect": 1.8, "scream": 1.2, "travel": 0.6, "click": 0.4}
END = ("endcard", 7.0)

meta = json.load(open(os.path.join(ROOT, "public/vo/timing.json")))
shots, t = [], 0.0
for m in meta:
    d = m["dur"] + m["pause"] + PAD.get(m["id"], 0.0)
    shots.append({"id": m["id"], "start": round(t, 4), "dur": round(d, 4), "vo": f"vo/{m['id']}.wav",
                  "voDur": round(m["dur"], 4), "sents": [[round(a, 4), round(b, 4), s] for a, b, s in m["sents"]]})
    t += d
    if m["id"] in EXTRA_AFTER:
        sid, ed = EXTRA_AFTER[m["id"]]
        shots.append({"id": sid, "start": round(t, 4), "dur": ed, "vo": None, "voDur": 0, "sents": []})
        t += ed
shots.append({"id": END[0], "start": round(t, 4), "dur": END[1], "vo": None, "voDur": 0, "sents": []})
t += END[1]
out = {"fps": FPS, "total": round(t, 4), "frames": int(round(t * FPS)), "shots": shots}
json.dump(out, open(os.path.join(ROOT, "src/timeline.json"), "w"), indent=1)
print(f"{len(shots)} shots, {t:.1f}s = {int(t // 60)}:{int(t % 60):02d}, {out['frames']} frames")
