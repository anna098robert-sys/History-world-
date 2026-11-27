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
NARRATOR = "am_puck"   # same History World narrator voice as earlier Shorts
MACHINE = "am_michael"  # time-machine voice, processed to sound robotic

LINES = {
    "s1": ("THE ENTIRE CITY IS BURNING! And I just woke up in sixteen sixty-six!", 1.22, NARRATOR),
    "s2": ("I was walking through London, when suddenly, people started screaming. Fire was spreading everywhere!", 1.18, NARRATOR),
    "s3": ("It all started in a small bakery on Pudding Lane. But nobody expected what would happen next.", 1.12, NARRATOR),
    "s4": ("The wooden houses were catching fire, one after another. The wind was pushing the flames across the city!", 1.12, NARRATOR),
    "s5": ("I tried to escape, but every street looked like a giant wall of fire. Even the famous old Saint Paul's Cathedral was destroyed!", 1.2, NARRATOR),
    "s6": ("Four days later, most of the medieval city was in ruins. I thought I had escaped history...", 1.05, NARRATOR),
    "s7a": ("Then my time machine said:", 1.1, NARRATOR),
    "s7b": ("Destination: Pompeii.", 0.95, MACHINE),
    "s7c": ("WAIT... NOT AGAIN!", 1.1, NARRATOR),
}

def trim(x, sr, thresh=0.01):
    idx = np.where(np.abs(x) > thresh)[0]
    if len(idx) == 0:
        return x
    a = max(0, idx[0] - int(0.02 * sr)); b = min(len(x), idx[-1] + int(0.06 * sr))
    return x[a:b]

def robot(x, sr):
    t = np.arange(len(x)) / sr
    y = x * (0.6 + 0.4 * np.sin(2 * np.pi * 60 * t))  # ring-mod buzz
    d = int(0.012 * sr)
    y[d:] += y[:-d] * 0.5  # metallic comb
    return y

k = Kokoro(os.path.join(sys.argv[1], "kokoro.onnx"), os.path.join(sys.argv[1], "voices.bin"))
durs = {}
for key, (text, speed, voice) in LINES.items():
    s, sr = k.create(text, voice=voice, speed=speed, lang="en-us")
    s = trim(np.asarray(s, dtype=np.float32), sr)
    if voice == MACHINE:
        s = robot(s, sr)
    s = s / (np.max(np.abs(s)) + 1e-9) * 0.95
    sf.write(os.path.join(ROOT, "public", "audio", f"vo_{key}.wav"), s, sr)
    durs[key] = round(len(s) / sr, 3)
    print(key, durs[key])
with open(os.path.join(ROOT, "src", "voiceDurations.json"), "w") as f:
    json.dump(durs, f, indent=2)
