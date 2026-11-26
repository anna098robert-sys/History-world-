"""Build public/audio/bed.wav: original synthesised music + sound effects, timed to src/timeline.json and
ducked under the narration (Remotion plays the narration files on top).  Usage: python3 tools/audio.py"""
import json, os, sys
import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio_lib import *  # noqa: F401,F403  (music sections + sfx generators)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TL = json.load(open(os.path.join(ROOT, "src/timeline.json")))
SHOTS, TOTAL = TL["shots"], TL["total"]

STYLE = {
    "hook": "chase", "title": "sting", "market": "playful", "buy": "playful", "travel": "tunnel",
    "aboard": "musette", "luxury": "musette", "realize": "mystery", "fact1": "mystery", "warn1": "bouncy",
    "warn2": "bouncy", "warn3": "bouncy", "fact2": "mystery", "napkin": "playful", "captain": "playful",
    "conv1": "playful", "conv2": "playful", "binoculars": "chase", "lost": "chase", "night": "night",
    "crowsnest": "tension", "impact": "mystery", "harder": "warm", "help1": "warm", "help2": "warm",
    "help3": "warm", "respect": "night", "return": "tunnel", "promise": "playful", "click": "mystery",
    "scream": "sting", "outro": "bouncy", "endcard": "bouncy",
}
BPM = {"playful": 104, "bouncy": 116, "musette": 150, "chase": 150, "tension": 132, "tunnel": 130, "night": 64,
       "mystery": 84, "warm": 80}


def cue_of(shot):
    def cue(text, frac=None):
        for a, b, s in shot["sents"]:
            if text in s:
                return a if frac is None else a + (b - a) * frac
        raise KeyError(f"{text} not in {shot['id']}")
    return cue


def build_music():
    out = np.zeros(int((TOTAL + 2) * SR))
    groups = []
    for s in SHOTS:
        st = STYLE[s["id"]]
        if groups and groups[-1][0] == st and st != "sting":
            groups[-1][2] = s["start"] + s["dur"]
        else:
            groups.append([st, s["start"], s["start"] + s["dur"]])
    XF = 0.8
    for st, a, b in groups:
        d = b - a + XF
        x = music_section(st, d, BPM.get(st, 90))
        f = int(XF * SR)
        x[:f] *= np.linspace(0, 1, f)
        x[-f:] *= np.linspace(1, 0, f)
        place(out, x, a - XF / 2)
    return out


def sfx_wave_wash(d):
    t = tt(d)
    return bp(rng.standard_normal(len(t)), 200, 2000) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.18 * t)) * 0.2


def sfx_ship_horn(d=2.2):
    t = tt(d)
    x = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((92, 1), (184, 0.5), (138, 0.4)))
    return lp(x, 900) * env_adsr(len(t), 0.2, 0.2, 0.9, 0.5) * 0.4


def sfx_scrape(d):
    t = tt(d)
    x = bp(rng.standard_normal(len(t)), 80, 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t))
    return x * env_adsr(len(t), 0.5, 0.2, 0.9, 1.0) * 0.6


def build_sfx():
    out = np.zeros(int((TOTAL + 2) * SR))
    amb = np.zeros_like(out)
    for s in SHOTS:
        a, D, sid = s["start"], s["dur"], s["id"]
        cue = cue_of(s) if s["sents"] else None
        P = lambda x, t, g=1.0: place(out, x, a + t, g)
        if sid in ("market", "buy"):
            place(amb, amb_birds(D) * 0.6, a)
            place(amb, sfx_crowd(D, 0.1) * 0.25, a)
        if sid in ("aboard", "warn3", "binoculars"):
            place(amb, sfx_wave_wash(D), a)
            place(amb, amb_wind(D) * 0.4, a)
        if sid in ("luxury", "warn1", "warn2", "napkin"):
            place(amb, sfx_crowd(D, 0.15) * 0.3, a)
        if sid in ("night", "crowsnest", "harder", "help1", "help2", "help3", "impact"):
            place(amb, amb_wind(D) * 0.5, a)
        if sid == "hook":
            P(sfx_boom(), 0.0, 0.9)
            P(sfx_sparkle(1.2), 0.1, 0.6)
            P(sfx_riser(1.2), cue("Ten seconds") - 1.2, 0.6)
            P(sfx_portal(1.5), cue("Ten seconds") - 0.3, 0.8)
            P(sfx_ship_horn(), cue("Ten seconds") + 1.0, 0.8)
            P(sfx_scratch(), D - 0.6, 1.0)
        elif sid == "title":
            P(sfx_boom(), 0.0, 0.6)
            for k in range(3):
                P(sfx_pop(), 0.15 + k * 0.4, 0.6)
        elif sid == "market":
            for k in range(int(cue("And then I saw it") / 0.45)):
                P(sfx_step(), k * 0.45, 0.5)
            P(sfx_ding(88), cue("And then I saw it"), 0.6)
            P(sfx_sparkle(1.4), cue("A dusty brass"), 0.6)
            P(sfx_bonk(), cue("Time machine") + 0.6, 0.4)
        elif sid == "buy":
            P(sfx_pop(), 1.0, 0.4)
            t2 = cue("So, obviously")
            P(sfx_coins(), t2 + 0.3, 0.7)
            P(sfx_whoosh(0.6), t2 + 1.8, 0.6)
            P(sfx_clunk(), t2 + 3.4, 1.0)
        elif sid == "travel":
            P(sfx_creak(cue("My room turned")), 0.0, 0.7)
            for k in range(int(cue("My room turned") / 0.12)):
                P(sfx_tick(), k * 0.12, 0.6)
            P(sfx_portal(3.0), cue("My room turned") - 0.3, 1.0)
            P(sfx_riser(3.0), cue("My room turned"), 0.5)
            P(sfx_ding(91), cue("And a little screen") + 0.6, 0.6)
        elif sid == "aboard":
            P(sfx_fall_whistle(0.5), 0.1, 0.7)
            P(sfx_thud(), 0.6, 0.9)
            P(sfx_bonk(), 0.62, 0.6)
            P(sfx_ship_horn(2.5), cue("A ship so big"), 0.9)
        elif sid == "luxury":
            P(sfx_sparkle(1.5), 0.3, 0.6)
            tg = cue("A gym")
            for k in range(3):
                P(sfx_pop(), tg + k * (cue("I ate four") - tg) / 3.2, 0.6)
            for k in range(4):
                P(sfx_crunch(), cue("I ate four") + k * 0.7, 0.5)
        elif sid == "realize":
            P(sfx_flip(), 0.2, 0.8)
            P(sfx_pop(), cue("I read it once"), 0.4)
            P(sfx_pop(), cue("I read it once") + 1.4, 0.4)
            P(sfx_ding(70, 1.5), cue("And my brain"), 0.4)
        elif sid == "fact1":
            P(sfx_whoosh(1.2), 0.6, 0.4)
            P(sfx_pop(), cue("Newspapers called"), 0.5)
            P(sfx_boom(), cue("And on the night") + 0.5, 0.5)
            P(sfx_scratch(), cue("That was tonight"), 0.8)
        elif sid == "warn1":
            P(sfx_boing(), 0.3, 0.6)
            P(sfx_boom(), cue("I jumped", 0.55), 0.6)
            P(sfx_ding(96, 0.5), cue("A waiter") + 1.2, 0.6)
            P(sfx_ding(98, 0.5), cue("A waiter") + 1.35, 0.5)
        elif sid == "warn2":
            P(sfx_horn(), 0.4, 0.5)
            P(sfx_bonk(), cue("A lady in") + 3.0, 0.5)
        elif sid == "warn3":
            P(sfx_whoosh(0.4), 0.3, 0.5)
            P(sfx_cheer(1.5) * 0.3, cue("He laughed"), 0.5)
        elif sid == "fact2":
            tb = cue("The Titanic had")
            for k in range(20):
                P(sfx_pop() * 0.5, tb + 0.2 + k * 0.08, 0.4)
            P(sfx_ding(70, 2.0), cue("But there were") + 1.8, 0.5)
        elif sid == "napkin":
            P(bp(rng.standard_normal(int(2.5 * SR)), 2000, 7000) * 0.06, 0.3, 1.0)
            P(sfx_cheer(2.5) * 0.6, cue("Everyone clapped"), 0.8)
        elif sid == "captain":
            for k in range(10):
                P(sfx_step(), cue("Talk to the captain") + k * 0.18, 0.6)
            P(sfx_ship_horn(1.6), cue("I found Captain"), 0.4)
        elif sid == "conv1":
            P(sfx_ding(84, 0.6), cue("He raised"), 0.4)
            P(sfx_tick(), cue("Somewhere") + 0.8, 0.6)
            P(sfx_tick(), cue("Somewhere") + 1.3, 0.6)
        elif sid == "conv2":
            P(sfx_scratch(), cue("I saw it in a movie") + 0.3, 0.5)
            P(sfx_bonk(), cue("What is a movie"), 0.6)
        elif sid == "binoculars":
            P(sfx_flip(), cue("The key"), 0.6)
            P(sfx_sparkle(1.0), cue("The key") + 0.2, 0.5)
            for k in range(int((D - cue("So I ran")) / 0.18)):
                P(sfx_step(), cue("So I ran") + k * 0.18, 0.6)
        elif sid == "lost":
            for k in range(int(cue("I did not") / 0.18)):
                P(sfx_step(), k * 0.18, 0.5)
            seg = cue("I did not") / 4
            P(sfx_bonk(), seg * 0.5, 0.4)
            P(sfx_flip(), seg * 1.3, 0.6)
            P(sfx_clunk(), seg * 2.3, 0.6)
            P(sfx_slide_whistle(1.0, up=True), seg * 3, 0.4)
            P(sfx_bonk(), cue("I did not") + 0.4, 0.5)
        elif sid == "night":
            P(sfx_whoosh(1.5, up=False), 0.3, 0.4)
            P(sfx_ding(76, 3.0), cue("Just stars"), 0.3)
        elif sid == "crowsnest":
            P(sfx_riser(2.0), cue("The lookout squinted"), 0.4)
            for k in range(3):
                P(sfx_bell(64, 1.8), cue("Three rings") + k * 0.45, 0.7)
            P(sfx_boom(), cue("Iceberg, right ahead"), 0.6)
        elif sid == "impact":
            P(sfx_scrape(cue("Upstairs") - 0.3), 0.3, 0.9)
            P(sfx_creak(3.0), cue("It didn't feel"), 0.4)
            for k in range(5):
                P(sfx_ding(96 + k, 0.3), cue("Upstairs") + 1.0 + k * 0.5, 0.3)
        elif sid == "harder":
            P(sfx_click(), cue("Changing history is") + 0.2, 0.6)
            for k in range(4):
                P(sfx_click(), cue("Changing history is") + 0.6 + k * 0.4, 0.4)
        elif sid == "help1":
            tk = cue("I knocked")
            for k in range(6):
                P(sfx_clunk() * 0.6, tk + 0.2 + k * 0.32, 0.6)
            for k in range(10):
                P(sfx_step(), cue("I showed") + k * 0.35, 0.4)
        elif sid == "help2":
            P(sfx_creak(3.0), 0.5, 0.3)
        elif sid == "help3":
            P(sfx_sparkle(1.0), cue("I helped") + 3.0, 0.4)
            # the band: a gentle violin-like line
            tb = cue("And all around us")
            for k, n in enumerate((67, 69, 71, 72, 71, 69, 67, 64)):
                x = flute(n, 0.6, vib=6)
                P(x * 0.12, tb + k * 0.6, 1.0)
        elif sid == "respect":
            place(amb, sfx_wave_wash(D) * 0.7, a)
        elif sid == "return":
            P(sfx_hum(2.0), cue("I felt", 0.5), 0.6)
            P(sfx_portal(2.0), cue("The dials spun"), 0.9)
            P(sfx_splash(), cue("The dials spun") + 1.4, 0.7)
        elif sid == "promise":
            P(sfx_ding(84), cue("No more time travel"), 0.5)
            for k in range(6):
                P(sfx_step(), cue("I'm putting you") + k * 0.4, 0.5)
        elif sid == "click":
            P(sfx_fall_whistle(0.8), 1.0, 0.6)
            P(sfx_thud(), 2.2, 0.9)
            P(sfx_click(), cue("And then I tripped", 0.85), 1.0)
            P(sfx_riser(1.5), cue("The screen lit up") - 0.5, 0.5)
            P(sfx_boom(), cue("The screen lit up") + 1.0, 0.7)
        elif sid == "scream":
            P(sfx_boom(), 0.0, 0.8)
            P(sfx_creak(2.0), 0.0, 0.3)
        elif sid == "outro":
            P(sfx_pop(), 0.3, 0.6)
            P(sfx_pop(), 1.4, 0.6)
        elif sid == "endcard":
            P(sfx_pop(), 0.3, 0.6)
            P(sfx_cheer(3.0) * 0.5, 0.3, 0.5)
            P(sfx_pop(), 1.0, 0.7)
            P(sfx_click(), 2.6, 1.0)
            P(sfx_ding(91), 2.65, 0.6)
    return out, amb


def main():
    vo = np.zeros(int((TOTAL + 2) * SR))
    for s in SHOTS:
        if s["vo"]:
            x, sr = sf.read(os.path.join(ROOT, "public", s["vo"]))
            place(vo, x if x.ndim == 1 else x.mean(axis=1), s["start"])
    music = build_music()
    sfx, amb = build_sfx()
    env = np.convolve(np.abs(vo), np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
    duck = 1 - 0.6 * np.clip(env / 0.03, 0, 1)
    duck = np.convolve(duck, np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
    norm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
    bed = norm(music) * 0.13 * duck + norm(sfx) * 0.32 + amb * 0.6
    n = int(TOTAL * SR)
    bed = bed[:n]
    bed[-int(SR):] *= np.linspace(1, 0, int(SR))
    bed = bed / max(1.0, np.max(np.abs(bed)) / 0.45)
    os.makedirs(os.path.join(ROOT, "public/audio"), exist_ok=True)
    sf.write(os.path.join(ROOT, "public/audio/bed.wav"), np.stack([bed, bed], axis=1), SR, subtype="PCM_16")
    sp = env[:n] > 0.02
    r = lambda x: 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)
    print(f"wrote public/audio/bed.wav {TOTAL:.1f}s | voice {r(vo[:n][sp]):.1f} dB, music under voice {r((norm(music) * 0.13 * duck)[:n][sp]):.1f} dB")


if __name__ == "__main__":
    main()
