"""Original music + SFX bed for the long-form film (public/audio/bed.mp3), ducked under the narration.
Everything is synthesised in tools/audio_lib.py; no samples or copyrighted material."""
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
SCORE = [("tension", "hook", "hook", 132), ("bouncy", "title", "glitch", 120), ("playful", "map", "escape", 104), ("night", "night61", "morning", 64),
         ("tension", "schumann", "schumann", 112), ("night", "concrete", "concrete", 64), ("chase", "jump", "jump", 140), ("bouncy", "kennedy", "kennedy", 116),
         ("tunnel", "tunnel", "tunnel", 96), ("warm", "balloon", "balloon", 84), ("night", "memorial", "memorial", 56), ("mystery", "reagan", "reagan", 90),
         ("warm", "leipzig", "leipzig", 76), ("mystery", "press", "when", 96), ("chase", "tv", "tv", 130), ("tension", "bornholmer", "bornholmer", 120),
         ("bouncy", "flood", "woodpeckers", 124), ("warm", "reunite", "reunite", 70), ("playful", "after", "home", 104), ("warm", "lesson", "lesson", 76),
         ("bouncy", "outro", "endcard", 124)]
for st, a_id, b_id, bpm in SCORE:
    a = S[a_id]["start"]; b = S[b_id]["start"] + S[b_id]["dur"]
    x = music_section(st, b - a + 0.6, bpm); f = int(0.3 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    if a_id == "memorial": x *= 0.6
    place(music, x, max(0, a - 0.3))
# ambience
for sid, ex in (("hook", 0.7), ("kennedy", 0.6), ("leipzig", 0.2), ("tv", 0.4), ("bornholmer", 0.5), ("flood", 0.8), ("party", 0.9), ("woodpeckers", 0.3)):
    place(amb, sfx_crowd(S[sid]["dur"], ex), S[sid]["start"])
for sid in ("night61", "concrete", "balloon", "memorial"):
    place(amb, amb_wind(S[sid]["dur"]) * 0.8, S[sid]["start"])
for sid in ("morning", "schumann", "after"):
    place(amb, amb_street(S[sid]["dur"]) * 0.7, S[sid]["start"])
place(amb, amb_birds(S["reunite"]["dur"]) * 0.4, S["reunite"]["start"])
# hook + title
at("hook", 0.0, sfx_boom(), 0.8)
tb = cue("hook", "history is breaking")
for k in range(6): at("hook", tb + 0.2 + k * 0.35, mx(sfx_clunk(), sfx_ding(96, 0.2) * 0.4), 0.5)
at("hook", cue("hook", "Literally"), sfx_crunch(), 1.0)
at("hook", cue("hook", "Literally") + 0.1, sfx_snap(), 0.8)
at("title", 0.0, sfx_whoosh(0.6), 0.8)
for k in range(3): at("title", 0.15 + k * 0.4, sfx_pop(), 0.6)
# glitch
tp = cue("glitch", "I pressed")
at("glitch", tp + 0.3, sfx_click(), 0.9)
at("glitch", tp + 0.4, sfx_riser(1.0), 0.6)
at("glitch", tp + 1.3, sfx_portal(2.5), 0.8)
at("glitch", cue("glitch", "Not in 1989") + 1.2, sfx_scratch(), 0.8)
at("glitch", cue("glitch", "In 1961") + 0.5, sfx_thud(), 1.0)
at("glitch", cue("glitch", "In 1961") + 0.8, sfx_boing(), 0.5)
# map / escape
at("map", cue("map", "After World War"), sfx_pop(), 0.6)
at("map", cue("map", "West Germany"), sfx_snap(), 0.5)
at("map", cue("map", "And Berlin"), sfx_whoosh(0.8), 0.6)
at("map", cue("map", "Half the city"), sfx_sparkle(1.2), 0.5)
for k in range(int(9 / 0.3)): at("escape", k * 0.3, sfx_step(), 0.25)
for k, w in enumerate(("Doctors",)):
    for j in range(3): at("escape", cue("escape", w) + j * 0.8, sfx_pop(), 0.6)
at("escape", cue("escape", "The East German government"), sfx_fall_whistle(), 0.5)
# 1961
at("night61", 0.6, sfx_creak(3.0), 0.4)
for k in range(10): at("night61", 0.8 + k * 0.7, sfx_clunk(), 0.25)
for j in range(3): at("night61", cue("night61", "Streets") + j * 0.9 + 0.4, sfx_snap(), 0.6)
at("night61", cue("night61", "Overnight"), sfx_ding(52, 2.0), 0.5)
at("morning", cue("morning", "I tried") + 1.6, sfx_gasp(), 0.6)
tj = cue("schumann", "A photographer") + 0.1
for k in range(6): at("schumann", tj - 2.0 + k * 0.25, sfx_step(), 0.5)
at("schumann", tj - 0.55, sfx_whoosh(0.6), 0.7)
at("schumann", tj, sfx_camera(), 1.0)
at("schumann", cue("schumann", "It became"), sfx_sparkle(1.5), 0.5)
at("concrete", 0.4, sfx_boom(), 0.6)
at("concrete", cue("concrete", "Then two walls") + 0.2, sfx_boom(), 0.5)
at("concrete", cue("concrete", "Watchtowers"), sfx_thud(), 0.6)
at("concrete", cue("concrete", "Floodlights"), sfx_hum(1.0), 0.6)
at("concrete", cue("concrete", "Dogs"), sfx_bark(), 0.6)
# jump
for k in range(10): at("jump", 0.1 + k * 0.25, sfx_ding(100, 0.15), 0.5)
at("jump", cue("jump", "Whoosh") - 0.2, sfx_portal(2.0), 0.8)
at("jump", S["jump"]["dur"] - 0.4, sfx_whoosh(0.5), 0.6)
# 1963-1987
at("kennedy", cue("kennedy", "Kennedy came") + 1.6, sfx_cheer(3.0), 0.8)
at("kennedy", cue("kennedy", "Some people") + 0.4, sfx_boing(), 0.5)
at("kennedy", cue("kennedy", "But Berliners") + 1.0, sfx_cheer(4.0), 1.0)
for k in range(int(S["tunnel"]["dur"] / 0.6)): at("tunnel", k * 0.6, sfx_step(), 0.15)
at("tunnel", cue("tunnel", "It's still called"), sfx_ding(76, 1.2), 0.5)
at("balloon", 0.5, sfx_fire(2.0), 0.5)
at("balloon", cue("balloon", "Total legends"), sfx_cheer(2.0), 0.7)
at("memorial", 0.3, sfx_bell(45, 5.0), 0.3)
at("reagan", 0.0, sfx_whoosh(0.5), 0.4)
at("reagan", lerp_t := cue("reagan", "U S President") + (cue("reagan", "Everyone thought") - cue("reagan", "U S President")) * 0.55, sfx_cheer(2.5), 0.6)
at("reagan", cue("reagan", "Not in our"), sfx_boing(), 0.4)
# 1989
at("leipzig", 0.0, sfx_flip(), 0.8)
at("leipzig", 1.4, sfx_whoosh(0.6), 0.5)
at("leipzig", cue("leipzig", "Hungary") + 1.1, sfx_snap(), 0.9)
at("leipzig", cue("leipzig", "Nobody fired"), sfx_bell(57, 3.0), 0.3)
for k in range(int(S["press"]["dur"] / 1.6)): at("press", 0.5 + k * 1.6, sfx_camera(), 0.3)
at("when", cue("when", "He shuffled"), sfx_flip(), 0.8)
at("when", cue("when", "He shuffled") + 0.4, sfx_flip(), 0.6)
tf = cue("when", "The whole room")
for k in range(int((cue("when", "Oops") - tf) / 0.5)): at("when", tf + k * 0.5, sfx_tick(), 0.5)
at("when", cue("when", "Oops"), sfx_boing(), 0.8)
at("when", cue("when", "Oops"), sfx_pop(), 0.7)
at("tv", cue("tv", "So they went"), sfx_bell_door(), 0.5)
at("tv", cue("tv", "Thousands of them"), sfx_whoosh(0.6), 0.6)
for k in range(int(4 / 0.25)): at("tv", cue("tv", "Thousands of them") + k * 0.25, sfx_step(), 0.3)
to = cue("bornholmer", "He opened")
at("bornholmer", cue("bornholmer", "The crowd chanted"), sfx_cheer(2.0), 0.6)
at("bornholmer", cue("bornholmer", "Finally"), sfx_tick(), 0.8)
at("bornholmer", to, sfx_creak(1.2), 0.8)
at("bornholmer", to + 0.6, sfx_cheer(4.0), 1.0)
tt_ = cue("flood", "Driving")
at("flood", tt_ + 0.8, sfx_horn(), 0.8)
at("flood", tt_ + 2.2, sfx_horn(), 0.6)
at("flood", cue("flood", "People who had"), sfx_sparkle(1.5), 0.5)
for k in range(4): at("party", 0.4 + k * 1.8, sfx_boom() * 0.5, 0.5)
at("party", cue("party", "Somebody handed") + 0.6, sfx_pop(), 0.6)
for k in range(int(S["woodpeckers"]["dur"] / 0.42)):
    at("woodpeckers", 0.1 + k * 0.42, mx(sfx_clunk(), sfx_ding(96 + (k % 3) * 2, 0.2) * 0.4), 0.4)
for j in range(3): at("woodpeckers", cue("woodpeckers", "Tap tap") + j * 0.4, sfx_tick(), 1.0)
at("woodpeckers", cue("woodpeckers", "Everyone wanted") + 0.3, sfx_sparkle(1.0), 0.6)
at("reunite", cue("reunite", "It was an old man") + 2.5, sfx_sparkle(2.0), 0.3)
# after / home / lesson / outro
at("after", 0.2, sfx_flip(), 0.7)
at("after", 4.4, sfx_cheer(2.5), 0.6)
for k in range(3): at("after", 4.6 + k * 0.6, sfx_boom() * 0.4, 0.4)
at("after", cue("after", "Today, pieces") - 0.1, sfx_whoosh(0.5), 0.5)
for j in range(6): at("after", cue("after", "Today, pieces") + 0.3 + j * 0.35, sfx_pop(), 0.4)
at("after", cue("after", "And in Berlin") - 0.1, sfx_whoosh(0.5), 0.5)
at("home", 0.0, sfx_portal(1.0), 0.5)
at("home", 1.0, sfx_thud(), 1.0)
at("home", cue("home", "A little piece"), sfx_sparkle(1.5), 0.6)
tl = cue("lesson", "But it was brought") + 3.0
for k in range(5): at("lesson", tl + k * 0.25, sfx_boom() * 0.6, 0.5)
at("lesson", tl + 1.4, sfx_cheer(2.0), 0.6)
at("lesson", cue("lesson", "And a few"), sfx_pop(), 0.6)
tbp = cue("outro", "Because my time machine") + 0.6
for k in range(10): at("outro", tbp + k * 0.22, sfx_ding(100, 0.18), 0.6)
at("endcard", 1.0, sfx_pop(), 0.8)
at("endcard", 2.6, sfx_click(), 0.8)
at("endcard", 2.7, sfx_sparkle(1.2), 0.6)
for s in TL["shots"]:
    if s["vo"]:
        x, _ = sf.read(os.path.join(ROOT, "public/vo", s["id"] + ".wav")); place(vo, x, s["start"] + s["voOff"])
w = int(0.2 * SR)
env = np.convolve(np.abs(vo), np.ones(w) / w, "same")
duck = np.convolve(1 - 0.55 * np.clip(env / 0.03, 0, 1), np.ones(w) / w, "same")
nm = lambda x: x / (np.abs(x).max() + 1e-9)
bed = (nm(music) * 0.15 * duck + nm(out) * 0.28 + nm(amb) * 0.1 * duck)[: int(TOTAL * SR)]
bed[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))
bed = bed / max(1.0, np.abs(bed).max() / 0.5)
os.makedirs(os.path.join(ROOT, "public/audio"), exist_ok=True)
wav = os.path.join(ROOT, "public/audio/bed.wav")
sf.write(wav, np.stack([bed, bed], 1), SR, subtype="PCM_16")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libmp3lame", "-b:a", "160k", wav[:-4] + ".mp3"], check=True)
print("bed", round(TOTAL, 1), "s")
