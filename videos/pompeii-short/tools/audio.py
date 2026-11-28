"""Original cinematic score + volcano SFX for the Short (public/audio/bed.mp3), ducked under the narration.
Everything is synthesised (tools/audio_lib.py); no samples or copyrighted material."""
import json, os, subprocess, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio_lib import *  # noqa
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TL = json.load(open(os.path.join(ROOT, "src/timeline.json")))
S = {s["id"]: s for s in TL["shots"]}
TOTAL = TL["total"]
out = np.zeros(int((TOTAL + 3) * SR)); music = np.zeros_like(out); amb = np.zeros_like(out); vo = np.zeros_like(out)
def at(sid, t, x, g=1.0): place(out, x, S[sid]["start"] + t, g)
def cue(sid, txt):
    for a, b, s in S[sid]["sents"]:
        if txt in s: return a
    raise KeyError(txt)
def rumble(d, f=60):
    t = tt(d)
    x = lp(rng.standard_normal(len(t)), f) * 6
    return x * (0.6 + 0.4 * np.sin(2 * np.pi * 3.1 * t)) * np.minimum(1, t * 3) * np.minimum(1, (d - t) * 2)
def big_boom():
    return mx(sfx_boom() * 1.3, kick(0.8) * 0.8, noise_burst(1.6, 60, 1200, 2.5) * 1.2)
def falling_ash(d):
    return hp(lp(rng.standard_normal(int(d * SR)), 3000), 300) * 0.08
def pebbles(d, rate=6):
    o = np.zeros(int(d * SR)); t0 = 0.0
    while t0 < d - 0.1:
        place(o, noise_burst(0.05, 1500, 6000, 80) * rng.uniform(0.2, 0.6), t0); t0 += rng.exponential(1 / rate)
    return o
for st, sid, bpm, g in (("tension", "p_hook", 140, 1.0), ("italy", "p_city", 100, 0.8), ("tension", "p_erupt", 120, 1.0), ("chase", "p_run", 150, 1.0),
                        ("night", "p_bury", 60, 1.0), ("night", "p_escape", 56, 0.9), ("warm", "p_dig", 84, 1.0)):
    a = S[sid]["start"]; d = S[sid]["dur"]
    x = music_section(st, d + 0.5, bpm) * g; f = int(0.25 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    place(music, x, max(0, a - 0.25))
# a low drone under the whole disaster (cinematic weight)
a = S["p_erupt"]["start"]; b = S["p_escape"]["start"] + S["p_escape"]["dur"]
place(music, pad([38, 45, 50], b - a, cutoff=600) * 0.5, a)
# hook
at("p_hook", 0.0, rumble(0.5), 0.8)
at("p_hook", 0.35, big_boom(), 1.0)
at("p_hook", 0.35, rumble(3.6, 80), 1.0)
at("p_hook", 1.0, pebbles(3.0, 10), 0.8)
at("p_hook", cue("p_hook", "WHAT IS"), sfx_whoosh(0.4), 0.5)
# ordinary day
place(amb, sfx_crowd(S["p_city"]["dur"], 0.25), S["p_city"]["start"])
place(amb, amb_birds(S["p_city"]["dur"]), S["p_city"]["start"])
at("p_city", 0.3, sfx_pop(), 0.4)
# eruption
at("p_erupt", 0.2, rumble(0.6), 0.9)
at("p_erupt", 0.55, big_boom(), 1.0)
at("p_erupt", 0.55, rumble(6.0, 70), 1.0)
tc = cue("p_erupt", "A giant cloud")
at("p_erupt", tc, sfx_gasp(), 0.7)
at("p_erupt", tc, sfx_whoosh(0.3), 0.5)
at("p_erupt", tc + 1.7, sfx_whoosh(0.3), 0.5)
at("p_erupt", tc + 1.0, sfx_boom(), 0.5)
# running, ash
place(amb, sfx_crowd(S["p_run"]["dur"], 0.95), S["p_run"]["start"])
at("p_run", 0.0, pebbles(S["p_run"]["dur"], 8), 0.7)
for k in range(int(5 / 0.18)): at("p_run", k * 0.18, sfx_step(), 0.3)
at("p_run", 0.0, rumble(S["p_run"]["dur"], 60), 0.7)
for k in range(5): at("p_run", cue("p_run", "Nobody") + 0.2 + k * 0.32, noise_burst(0.2, 800, 4000, 12), 0.25)
for sid in ("p_run", "p_bury", "p_escape"):
    place(amb, falling_ash(S[sid]["dur"]), S[sid]["start"])
    place(amb, amb_wind(S[sid]["dur"]), S[sid]["start"])
# burial / escape
at("p_bury", 0.0, rumble(S["p_bury"]["dur"], 50), 1.0)
at("p_bury", 0.2, sfx_boom(), 0.6)
at("p_bury", 3.0, sfx_boom(), 0.5)
at("p_escape", 0.0, rumble(S["p_escape"]["dur"], 45), 0.8)
for k in range(int(3.2 / 0.5)): at("p_escape", k * 0.5, sfx_step(), 0.25)
at("p_escape", cue("p_escape", "Pompeii would"), sfx_bell(45, 4.0), 0.4)
# discovery
place(amb, amb_birds(S["p_dig"]["dur"]) * 0.8, S["p_dig"]["start"])
for k in range(10): at("p_dig", 0.6 + k * 0.45, noise_burst(0.12, 2000, 8000, 30), 0.12)
at("p_dig", cue("p_dig", "Almost 2,000"), sfx_sparkle(1.5), 0.6)
ts = cue("p_dig", "SUBSCRIBE")
at("p_dig", ts - 0.2, sfx_whoosh(0.5), 0.7)
at("p_dig", ts, sfx_boom(), 0.5)
at("p_dig", ts + 0.4, sfx_pop(), 0.8)
for s in TL["shots"]:
    x, _ = sf.read(os.path.join(ROOT, "public/vo", s["id"] + ".wav")); place(vo, x, s["start"] + s["voOff"])
w = int(0.2 * SR)
env = np.convolve(np.abs(vo), np.ones(w) / w, "same")
duck = np.convolve(1 - 0.5 * np.clip(env / 0.03, 0, 1), np.ones(w) / w, "same")
nm = lambda x: x / (np.abs(x).max() + 1e-9)
bed = (nm(music) * 0.2 * duck + nm(out) * 0.32 + nm(amb) * 0.14 * duck)[: int(TOTAL * SR)]
bed[-int(0.4 * SR):] *= np.linspace(1, 0, int(0.4 * SR))
bed = bed / max(1.0, np.abs(bed).max() / 0.5)
os.makedirs(os.path.join(ROOT, "public/audio"), exist_ok=True)
wav = os.path.join(ROOT, "public/audio/bed.wav")
sf.write(wav, np.stack([bed, bed], 1), SR, subtype="PCM_16")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libmp3lame", "-b:a", "160k", wav[:-4] + ".mp3"], check=True)
os.remove(wav)
print("bed", round(TOTAL, 1), "s")
