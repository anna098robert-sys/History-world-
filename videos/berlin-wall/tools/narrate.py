"""Young, energetic narrator (Kokoro TTS, Liam/Puck blend), one sentence at a time for exact sync.
Usage: python3 narrate.py <kokoro.onnx> <voices.bin> <outdir>"""
import sys, os, re, json, subprocess
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
import importlib
SHOTS = importlib.import_module(os.environ.get('STORY', 'story')).SHOTS

model, voices, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
k = Kokoro(model, voices)
voice = 0.6 * k.get_voice_style("am_liam") + 0.4 * k.get_voice_style("am_puck")
GAP = 0.32
SPEED = float(os.environ.get("SPEED", "0.93"))


def sentences(text):
    return [p for p in re.split(r'(?<=[.!?])\s+', text.strip()) if p]


meta = []
for sid, text, pause in SHOTS:
    chunks, sents, pos, sr = [], [], 0.0, 24000
    for sent in sentences(text):
        # shouted words get a little more energy (slightly faster)
        sp = SPEED * (1.06 if sent.isupper() or sent.endswith("!") else 1.0)
        s, sr = k.create(sent, voice=voice, speed=sp, lang="en-us")
        nz = np.where(np.abs(s) > 0.01)[0]
        if len(nz):
            s = s[max(0, nz[0] - 600): nz[-1] + 1200]
        sents.append([pos, pos + len(s) / sr, sent])
        chunks += [s, np.zeros(int(GAP * sr), dtype=s.dtype)]
        pos += len(s) / sr + GAP
    raw = f"{out}/{sid}_raw.wav"
    sf.write(raw, np.concatenate(chunks[:-1]), sr)
    fin = f"{out}/{sid}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
        "highpass=f=70,equalizer=f=3000:t=q:w=1.2:g=2.5,equalizer=f=200:t=q:w=1:g=1,"
        "acompressor=threshold=-20dB:ratio=3:attack=5:release=120,aresample=48000", "-ac", "1", fin], check=True)
    d = sf.info(fin).duration
    meta.append({"id": sid, "dur": d, "pause": pause, "text": text, "sents": sents})
json.dump(meta, open(f"{out}/timing.json", "w"), indent=1)
print("total", round(sum(m["dur"] + m["pause"] for m in meta), 1))
