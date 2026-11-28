"""Short character voice lines with Kokoro (open-weight TTS, Apache-2.0).

Usage: python3 tools/generate_voice.py <dir with kokoro.onnx + voices.bin>
"""
import json, os, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERO = "am_puck"     # History World doodle guy
PRISONER = "am_liam" # frightened young man

LINES = {
    "helpme":   ("Help me...", 0.85, PRISONER, "whisper"),
    "please":   ("Please! Help me! They'll take me at dawn!", 1.12, PRISONER, "plain"),
    "shh":      ("Shhh!", 1.0, HERO, "whisper"),
    "uhoh":     ("Uh-oh.", 0.9, HERO, "plain"),
    "whathave": ("...What have I done?", 0.9, HERO, "whisper"),
}

def trim(x, sr, thresh=0.01):
    idx = np.where(np.abs(x) > thresh)[0]
    if len(idx) == 0:
        return x
    return x[max(0, idx[0] - int(0.02 * sr)): min(len(x), idx[-1] + int(0.08 * sr))]

def whisperize(x, sr):
    """Breathy whisper: mix the voice with noise shaped by its own envelope."""
    env = np.convolve(np.abs(x), np.ones(int(0.01 * sr)) / int(0.01 * sr), mode="same")
    rng = np.random.default_rng(1)
    n = rng.standard_normal(len(x)) * env * 1.6
    X = np.fft.rfft(n); f = np.fft.rfftfreq(len(n), 1 / sr)
    n = np.fft.irfft(X * ((f > 1200) & (f < 7000)), len(n))
    return x * 0.55 + n

def stone_echo(x, sr):
    for d, g in [(0.09, 0.35), (0.2, 0.2), (0.34, 0.1)]:
        k = int(d * sr)
        x = np.concatenate([x, np.zeros(k)])
        x[k:] += x[:-k] * g
    return x

k = Kokoro(os.path.join(sys.argv[1], "kokoro.onnx"), os.path.join(sys.argv[1], "voices.bin"))
durs = {}
for key, (text, speed, voice, style) in LINES.items():
    s, sr = k.create(text, voice=voice, speed=speed, lang="en-us")
    s = trim(np.asarray(s, dtype=np.float64), sr)
    if style == "whisper":
        s = whisperize(s, sr)
    s = stone_echo(s, sr)
    s = s / (np.max(np.abs(s)) + 1e-9) * 0.95
    sf.write(os.path.join(ROOT, "public", "audio", f"vo_{key}.wav"), s, sr)
    durs[key] = round(len(s) / sr, 3)
    print(key, durs[key])
json.dump(durs, open(os.path.join(ROOT, "src", "voiceDurations.json"), "w"), indent=2)
