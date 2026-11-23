"""Generate the deep-voice narration with Kokoro TTS.
Each sentence is synthesised separately so the animation can sync to exact sentence times.
Usage: python3 narrate.py <kokoro.onnx> <voices.bin> <outdir>"""
import sys, os, re, json, subprocess
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from story import SHOTS

model, voices, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
k = Kokoro(model, voices)
# deep male timbre: mostly Onyx with a little Fenrir for grit
voice = 0.8 * k.get_voice_style("am_onyx") + 0.2 * k.get_voice_style("am_fenrir")
GAP = 0.2  # silence between sentences (s)


def sentences(text):
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p for p in parts if p]


meta = []
for sid, text, pause in SHOTS:
    chunks, sents, pos, sr = [], [], 0.0, 24000
    for sent in sentences(text):
        s, sr = k.create(sent, voice=voice, speed=0.86, lang="en-us")
        # trim leading/trailing near-silence
        nz = np.where(np.abs(s) > 0.01)[0]
        if len(nz):
            s = s[max(0, nz[0] - 600): nz[-1] + 1200]
        sents.append([pos, pos + len(s) / sr, sent])
        chunks.append(s)
        chunks.append(np.zeros(int(GAP * sr), dtype=s.dtype))
        pos += len(s) / sr + GAP
    raw = f"{out}/{sid}_raw.wav"
    sf.write(raw, np.concatenate(chunks[:-1]), sr)
    fin = f"{out}/{sid}.wav"
    # pitch down ~2 semitones (formants preserved), warm low end, gentle compression
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
        "rubberband=pitch=0.88:formant=preserved,"
        "equalizer=f=110:t=q:w=1:g=4,equalizer=f=3500:t=q:w=1.5:g=2,highpass=f=50,"
        "acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
        "aresample=48000", "-ac", "1", fin], check=True)
    d = sf.info(fin).duration
    meta.append({"id": sid, "dur": d, "pause": pause, "text": text, "sents": sents})
    print(f"{sid:16s} {d:6.2f}s  {len(sents)} sentences")
json.dump(meta, open(f"{out}/timing.json", "w"), indent=1)
print("total", sum(m["dur"] + m["pause"] for m in meta))
