"""Generate the voice-over with Kokoro (open-weight TTS, Apache-2.0).

Usage: python3 tools/generate_voice.py <dir with kokoro.onnx + voices.bin>
Model files: https://github.com/thewh1teagle/kokoro-onnx/releases (model-files-v1.0)
Writes public/audio/vo_<id>.wav and src/voiceDurations.json
"""
import json, os, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VOICE = "am_puck"  # energetic American male

LINES = {
    "s1": ("I opened an ancient Egyptian tomb... and accidentally woke up a three-thousand-year-old mummy!", 1.22),
    "s2": ("I was exploring an Egyptian pyramid, when I found a mysterious golden door.", 1.15),
    "s3": ("Inside was a giant golden coffin. Naturally, I opened it. What could possibly go wrong?", 1.2),
    "s4": ("Suddenly, two glowing eyes appeared in the darkness. The mummy was ALIVE!", 1.15),
    "scream": ("Aaaaaaah!", 1.0),
    "s5": ("It started chasing me through the pyramid! I ran faster than I had ever run in my entire life!", 1.28),
    "s6a": ("Then it stopped... and asked me where the bathroom was.", 1.1),
    "s6b": ("WHAT?!", 1.0),
    "s6c": ("Subscribe to History World, for more historical disasters!", 1.15),
}

def trim(x, sr, thresh=0.01):
    idx = np.where(np.abs(x) > thresh)[0]
    if len(idx) == 0:
        return x
    a = max(0, idx[0] - int(0.02 * sr)); b = min(len(x), idx[-1] + int(0.06 * sr))
    return x[a:b]

k = Kokoro(os.path.join(sys.argv[1], "kokoro.onnx"), os.path.join(sys.argv[1], "voices.bin"))
durs = {}
for key, (text, speed) in LINES.items():
    s, sr = k.create(text, voice=VOICE, speed=speed, lang="en-us")
    s = trim(np.asarray(s, dtype=np.float32), sr)
    s = s / (np.max(np.abs(s)) + 1e-9) * 0.95
    sf.write(os.path.join(ROOT, "public", "audio", f"vo_{key}.wav"), s, sr)
    durs[key] = round(len(s) / sr, 3)
    print(key, durs[key])
with open(os.path.join(ROOT, "src", "voiceDurations.json"), "w") as f:
    json.dump(durs, f, indent=2)
