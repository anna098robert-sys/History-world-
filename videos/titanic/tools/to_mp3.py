"""Convert narration + bed WAVs to MP3 (small enough to commit) and point the timeline at them."""
import json, os, subprocess, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for wav in glob.glob(os.path.join(ROOT, "public/vo/*.wav")) + [os.path.join(ROOT, "public/audio/bed.wav")]:
    mp3 = wav[:-4] + ".mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libmp3lame", "-b:a", "160k", mp3], check=True)
p = os.path.join(ROOT, "src/timeline.json")
tl = json.load(open(p))
for s in tl["shots"]:
    if s["vo"]:
        s["vo"] = s["vo"].replace(".wav", ".mp3")
json.dump(tl, open(p, "w"), indent=1)
print("mp3 assets written; timeline points to .mp3")
