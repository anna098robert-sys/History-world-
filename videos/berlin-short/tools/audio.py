"""Original music + SFX bed for the Short (public/audio/bed.mp3), ducked under the narration."""
import json, os, subprocess, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio_lib import *  # noqa
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TL = json.load(open(os.path.join(ROOT, "src/timeline.json")))
S = {s["id"]: s for s in TL["shots"]}
TOTAL = TL["total"]
out = np.zeros(int((TOTAL + 2) * SR)); music = np.zeros_like(out); amb = np.zeros_like(out); vo = np.zeros_like(out)
def at(sid, t, x, g=1.0): place(out, x, S[sid]["start"] + t, g)
def cue(sid, txt):
    for a, b, s in S[sid]["sents"]:
        if txt in s: return a
    raise KeyError(txt)
# score: tension hook -> mystery crowd -> sombre division -> rising -> joyful -> warm reunion -> tension end
for st, a_id, b_id, bpm in (("tension", "b_hook", "b_hook", 132), ("mystery", "b_crowd", "b_crowd", 96), ("night", "b_divided", "b_divided", 64),
                            ("tension", "b_cross", "b_cross", 120), ("bouncy", "b_hammer", "b_hammer", 120), ("warm", "b_hug", "b_hug", 76),
                            ("tension", "b_end", "b_end", 140)):
    a = S[a_id]["start"]; b = S[b_id]["start"] + S[b_id]["dur"]
    x = music_section(st, b - a + 0.6, bpm); f = int(0.3 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    place(music, x, max(0, a - 0.3))
for sid in ("b_hook", "b_crowd", "b_cross", "b_hammer", "b_end"):
    place(amb, sfx_crowd(S[sid]["dur"], 0.6), S[sid]["start"])
place(amb, amb_wind(S["b_divided"]["dur"]) * 0.8, S["b_divided"]["start"])
place(amb, sfx_crowd(S["b_hug"]["dur"], 0.1) * 0.5, S["b_hug"]["start"])
at("b_hook", 0.0, sfx_boom(), 1.0)
for k in range(8): at("b_hook", 0.2 + k * 0.55, sfx_thud(), 0.35)
at("b_hook", cue("b_hook", "DESTROYING"), sfx_snap(), 1.0)
at("b_hook", cue("b_hook", "1989"), sfx_scratch(), 0.9)
at("b_hook", S["b_hook"]["dur"] - 0.6, sfx_whoosh(0.6), 0.8)
for k in range(int(6 / 0.24)): at("b_crowd", k * 0.24, sfx_step(), 0.4)
at("b_divided", 0.3, sfx_ding(57, 3.0), 0.4)
at("b_divided", cue("b_divided", "Families"), sfx_ding(52, 3.0), 0.35)
at("b_cross", 0.2, sfx_boom(), 0.5)
t_some = cue("b_cross", "something unbelievable")
at("b_cross", t_some + 0.6, sfx_creak(1.0), 0.6)
at("b_cross", t_some + 1.4, sfx_cheer(4.0), 1.0)
at("b_cross", cue("b_cross", "People started") + 0.6, sfx_horn(), 0.7)
for k in range(int(6.8 / 0.42)):
    at("b_hammer", 0.1 + k * 0.42, mx(sfx_clunk(), sfx_ding(96 + (k % 3) * 2, 0.25) * 0.5), 0.6)
at("b_hammer", 0.0, sfx_cheer(6.0), 0.8)
for k in range(4): at("b_hammer", 0.4 + k * 1.6, sfx_boom() * 0.4, 0.4)
at("b_hug", 0.3, sfx_sparkle(1.5), 0.5)
at("b_hug", cue("b_hug", "people could"), sfx_sparkle(1.5), 0.4)
t_f = cue("b_end", "until my time")
for k in range(10): at("b_end", t_f + k * 0.22, sfx_ding(100, 0.18), 0.7)
at("b_end", t_f + 1.2, sfx_scratch(), 0.9)
at("b_end", cue("b_end", "SUBSCRIBE") - 0.2, sfx_whoosh(0.6), 0.8)
at("b_end", cue("b_end", "SUBSCRIBE"), sfx_boom(), 0.7)
at("b_end", cue("b_end", "SUBSCRIBE") + 0.4, sfx_pop(), 0.8)
for s in TL["shots"]:
    x, _ = sf.read(os.path.join(ROOT, "public/vo", s["id"] + ".wav")); place(vo, x, s["start"] + s["voOff"])
w = int(0.2 * SR)
env = np.convolve(np.abs(vo), np.ones(w) / w, "same")
duck = np.convolve(1 - 0.55 * np.clip(env / 0.03, 0, 1), np.ones(w) / w, "same")
nm = lambda x: x / (np.abs(x).max() + 1e-9)
bed = (nm(music) * 0.17 * duck + nm(out) * 0.3 + nm(amb) * 0.12 * duck)[: int(TOTAL * SR)]
bed[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))
bed = bed / max(1.0, np.abs(bed).max() / 0.5)
wav = os.path.join(ROOT, "public/audio/bed.wav")
sf.write(wav, np.stack([bed, bed], 1), SR, subtype="PCM_16")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libmp3lame", "-b:a", "160k", wav[:-4] + ".mp3"], check=True)
print("bed", round(TOTAL, 1), "s")
