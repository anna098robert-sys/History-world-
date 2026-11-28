"""Build src/timeline.json from the narration timing (scene timing + subtitles; also read by tools/audio.py).
Usage: python3 tools/timeline.py"""
import json, os, subprocess, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30
VO_OFF = 0.15
EXTRA_AFTER = {"hook": ("title", 4.5)}
PAD = {"glitch": 0.6, "schumann": 0.6, "jump": 0.4, "memorial": 2.2, "when": 0.8, "bornholmer": 0.8, "reunite": 2.0, "lesson": 0.8}
END = ("endcard", 7.0)

meta = json.load(open(os.path.join(ROOT, "public/vo/timing.json")))
shots, t = [], 0.0
for m in meta:
    d = VO_OFF + m["dur"] + m["pause"] + PAD.get(m["id"], 0.0)
    shots.append({"id": m["id"], "start": round(t, 4), "dur": round(d, 4), "vo": f"vo/{m['id']}.mp3", "voOff": VO_OFF, "voDur": round(m["dur"], 4),
                  "sents": [[round(a + VO_OFF, 4), round(b + VO_OFF, 4), s] for a, b, s in m["sents"]]})
    t += d
    if m["id"] in EXTRA_AFTER:
        sid, ed = EXTRA_AFTER[m["id"]]
        shots.append({"id": sid, "start": round(t, 4), "dur": ed, "vo": None, "voOff": 0, "voDur": 0, "sents": []})
        t += ed
shots.append({"id": END[0], "start": round(t, 4), "dur": END[1], "vo": None, "voOff": 0, "voDur": 0, "sents": []})
t += END[1]
out = {"fps": FPS, "total": round(t, 4), "frames": int(round(t * FPS)), "shots": shots}
json.dump(out, open(os.path.join(ROOT, "src/timeline.json"), "w"), indent=1)
for w in glob.glob(os.path.join(ROOT, "public/vo/*.wav")):
    mp3 = w[:-4] + ".mp3"
    if not os.path.exists(mp3):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", w, "-c:a", "libmp3lame", "-b:a", "160k", mp3], check=True)
print(f"{len(shots)} shots, {t:.1f}s = {int(t // 60)}:{int(t % 60):02d}, {out['frames']} frames")
