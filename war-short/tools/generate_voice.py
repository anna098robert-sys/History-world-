"""Short character voice lines with Kokoro (open-weight TTS, Apache-2.0).

Usage: python3 tools/generate_voice.py <dir with kokoro.onnx + voices.bin>
Writes public/audio/vo_<id>.wav and src/voiceDurations.json
"""
import json, os, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERO = "am_puck"   # the History World doodle guy
KING = "am_onyx"   # deep voice, pitched down further below

LINES = {
    "uhoh":  ("Uh-oh.", 0.9, HERO, 1.0),
    "gotit": ("Got it!", 1.1, HERO, 1.0),
    "majesty": ("Your Majesty! Special delivery!", 1.15, HERO, 1.0),
    "war":   ("WAR!", 0.8, KING, 1.22),
    "wait":  ("Wait, wait, wait! I can explain!", 1.25, HERO, 1.0),
    "mixed": ("I mixed up the letters!", 1.15, HERO, 1.0),
    "heh":   ("Heh... heh...", 1.0, HERO, 1.0),
    "oops":  ("...Oops.", 0.9, HERO, 1.0),
}

def trim(x, sr, thresh=0.01):
    idx = np.where(np.abs(x) > thresh)[0]
    if len(idx) == 0:
        return x
    return x[max(0, idx[0] - int(0.02 * sr)): min(len(x), idx[-1] + int(0.06 * sr))]

def pitch_down(x, factor):
    """Slow playback by `factor` (lower pitch + longer), via interpolation."""
    n = int(len(x) * factor)
    return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)

k = Kokoro(os.path.join(sys.argv[1], "kokoro.onnx"), os.path.join(sys.argv[1], "voices.bin"))
durs = {}
for key, (text, speed, voice, pd) in LINES.items():
    s, sr = k.create(text, voice=voice, speed=speed, lang="en-us")
    s = trim(np.asarray(s, dtype=np.float32), sr)
    if pd != 1.0:
        s = pitch_down(s, pd)
        d = int(0.05 * sr)
        s[d:] += s[:-d] * 0.35  # throne-room echo
    s = s / (np.max(np.abs(s)) + 1e-9) * 0.95
    sf.write(os.path.join(ROOT, "public", "audio", f"vo_{key}.wav"), s, sr)
    durs[key] = round(len(s) / sr, 3)
    print(key, durs[key])
json.dump(durs, open(os.path.join(ROOT, "src", "voiceDurations.json"), "w"), indent=2)
