"""Music + SFX bed for the Short (public/short/bed.mp3), reusing the episode's synth library."""
import json, os, subprocess, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio_lib import *  # noqa
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TL = json.load(open(os.path.join(ROOT, "src/short/timeline.json")))
S = {s["id"]: s for s in TL["shots"]}
TOTAL = TL["total"]
out = np.zeros(int((TOTAL + 2) * SR)); music = np.zeros_like(out); vo = np.zeros_like(out)
def at(sid, t, x, g=1.0): place(out, x, S[sid]["start"] + t, g)
def cue(sid, txt):
    for a, b, s in S[sid]["sents"]:
        if txt in s: return a
for st, sid0, sid1, bpm in (("chase", "s_hook", "s_hook", 150), ("tunnel", "s_travel", "s_travel", 130),
                            ("tension", "s_reveal", "s_panic", 132), ("warm", "s_cliff", "s_cliff", 84)):
    a = S[sid0]["start"]; b = S[sid1]["start"] + S[sid1]["dur"]
    x = music_section(st, b - a + 0.6, bpm); f = int(0.3 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    place(music, x, max(0, a - 0.3))
at("s_hook", 0.75, sfx_click(), 1.0); at("s_hook", 1.0, sfx_portal(2.5), 1.0); at("s_hook", 2.6, sfx_whoosh(1.8), 0.8)
at("s_hook", cue("s_hook", "Worst") + 0.05, sfx_boom(), 0.6)
at("s_travel", 0, sfx_riser(1.4), 0.7)
for k in range(10): at("s_travel", k * 0.13, sfx_tick(), 0.6)
at("s_travel", 1.5, sfx_fall_whistle(0.6), 0.7); at("s_travel", 2.15, sfx_thud(), 1.0); at("s_travel", 2.17, sfx_bonk(), 0.6)
place(out, sfx_crowd(S["s_travel"]["dur"] + S["s_reveal"]["dur"], 0.3) * 0.5, S["s_travel"]["start"] + 1.4)
at("s_travel", 4.6, sfx_flip(), 0.8); at("s_travel", 5.3, sfx_ding(91), 0.6)
at("s_reveal", 1.8, sfx_whoosh(1.0), 0.5); at("s_reveal", cue("s_reveal", "Wait"), sfx_ding(70, 1.5), 0.5)
at("s_reveal", cue("s_reveal", "TITANIC"), sfx_boom(), 0.9); at("s_reveal", cue("s_reveal", "TITANIC"), sfx_scratch(), 0.8)
at("s_panic", 0.3, sfx_cheer(2.0), 0.6)
for k in range(int(8 / 0.25)): at("s_panic", 2 + k * 0.25, sfx_step(), 0.5)
at("s_panic", cue("s_panic", "Because"), sfx_ding(64, 2.0), 0.5)
at("s_cliff", 0, sfx_riser(1.6), 0.6); at("s_cliff", cue("s_cliff", "Watch"), sfx_boom(), 0.6)
place(out, sfx_horn(), S["s_cliff"]["start"] + cue("s_cliff", "Watch") + 0.5, 0.5)
at("s_cliff", cue("s_cliff", "Watch") + 0.3, sfx_pop(), 0.7)
for s in TL["shots"]:
    x, _ = sf.read(os.path.join(ROOT, "public/short/vo", s["id"] + ".wav")); place(vo, x, s["start"] + s["voOff"])
env = np.convolve(np.abs(vo), np.ones(int(0.2 * SR)) / int(0.2 * SR), "same")
duck = np.convolve(1 - 0.55 * np.clip(env / 0.03, 0, 1), np.ones(int(0.2 * SR)) / int(0.2 * SR), "same")
nm = lambda x: x / (np.abs(x).max() + 1e-9)
bed = (nm(music) * 0.16 * duck + nm(out) * 0.34)[: int(TOTAL * SR)]
bed[-int(0.6 * SR):] *= np.linspace(1, 0, int(0.6 * SR))
bed = bed / max(1.0, np.abs(bed).max() / 0.5)
wav = os.path.join(ROOT, "public/short/bed.wav")
sf.write(wav, np.stack([bed, bed], 1), SR, subtype="PCM_16")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libmp3lame", "-b:a", "160k", wav[:-4] + ".mp3"], check=True)
print("bed written", round(TOTAL, 1), "s")
