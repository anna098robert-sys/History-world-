"""Synthesised score + sound effects, mixed under the narration.
Usage: python3 audio.py <vo_dir> <out.wav>"""
import sys, os, math
import numpy as np
import soundfile as sf
from scipy import signal
from render import build_timeline, make_cue

SR = 48000
rng = np.random.default_rng(7)


# ------------------------------------------------------------------ helpers
def tt(d):
    return np.arange(int(d * SR)) / SR


def env_adsr(n, a=0.01, d=0.1, s=0.7, r=0.2):
    e = np.ones(n) * s
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    na = min(na, n); e[:na] = np.linspace(0, 1, na)
    nd = min(nd, n - na); e[na:na + nd] = np.linspace(1, s, nd)
    nr = min(nr, n); e[n - nr:] *= np.linspace(1, 0, nr)
    return e


def lp(x, fc, order=2):
    b, a = signal.butter(order, min(fc / (SR / 2), 0.99), "low")
    return signal.lfilter(b, a, x)


def hp(x, fc, order=2):
    b, a = signal.butter(order, min(fc / (SR / 2), 0.99), "high")
    return signal.lfilter(b, a, x)


def bp(x, f1, f2, order=2):
    b, a = signal.butter(order, [f1 / (SR / 2), min(f2 / (SR / 2), 0.99)], "band")
    return signal.lfilter(b, a, x)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def saw(f, d, detune=0.0):
    t = tt(d)
    out = np.zeros_like(t)
    for k, dt in enumerate((-detune, 0, detune)):
        ph = (t * f * (1 + dt) + k * 0.33) % 1
        out += 2 * ph - 1
    return out / 3


def pluck(f, d, bright=0.5):
    """Karplus-Strong plucked string."""
    n = int(d * SR)
    p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p)
    out = np.zeros(n)
    idx = 0
    damp = 0.996
    for i in range(n):
        out[i] = buf[idx]
        nxt = (idx + 1) % p
        buf[idx] = damp * (bright * buf[idx] + (1 - bright) * buf[nxt]) if bright != 0.5 else damp * 0.5 * (buf[idx] + buf[nxt])
        idx = nxt
    return out * env_adsr(n, 0.002, 0.05, 1.0, min(0.08, d / 3))


_pluck_cache = {}


def pluck_c(n, d):
    key = (n, round(d, 2))
    if key not in _pluck_cache:
        _pluck_cache[key] = pluck(midi(n), d)
    return _pluck_cache[key]


def pad(notes, d, cutoff=1800, det=0.004, vol=1.0):
    out = np.zeros(int(d * SR))
    for n in notes:
        out += saw(midi(n), d, det)
    out = lp(out, cutoff) / max(1, len(notes))
    return out * env_adsr(len(out), min(0.6, d / 3), 0.2, 0.9, min(0.8, d / 3)) * vol


def flute(n, d, vib=5.0):
    t = tt(d)
    f = midi(n) * (1 + 0.006 * np.sin(2 * np.pi * vib * t) * np.clip(t * 2, 0, 1))
    ph = np.cumsum(f) / SR
    x = np.sin(2 * np.pi * ph) + 0.25 * np.sin(4 * np.pi * ph) + 0.08 * np.sin(6 * np.pi * ph)
    x += 0.03 * lp(rng.standard_normal(len(t)), 3000)
    return x * env_adsr(len(t), 0.06, 0.1, 0.8, 0.15)


def bass(n, d):
    t = tt(d)
    x = np.sin(2 * np.pi * midi(n) * t) + 0.3 * np.sin(4 * np.pi * midi(n) * t)
    return x * env_adsr(len(t), 0.005, 0.15, 0.6, 0.08)


def kick(d=0.4):
    t = tt(d)
    f = 50 + 120 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def noise_burst(d, f1=200, f2=6000, decay=10.0):
    t = tt(d)
    return bp(rng.standard_normal(len(t)), f1, f2) * np.exp(-t * decay)


def mx(*xs):
    """sum arrays of different lengths."""
    n = max(len(x) for x in xs)
    out = np.zeros(n)
    for x in xs:
        out[:len(x)] += x
    return out


def place(buf, x, t0, gain=1.0):
    i0 = int(t0 * SR)
    if i0 < 0:
        x = x[-i0:]
        i0 = 0
    i1 = min(len(buf), i0 + len(x))
    if i1 > i0:
        buf[i0:i1] += x[: i1 - i0] * gain


# ------------------------------------------------------------------ SFX library
def sfx_whoosh(d=0.6, up=True):
    t = tt(d)
    x = rng.standard_normal(len(t))
    fc = np.linspace(300, 4000, len(t)) if up else np.linspace(4000, 300, len(t))
    out = np.zeros_like(x)
    # time-varying lowpass via short blocks
    blk = 512
    zi = None
    for i in range(0, len(x), blk):
        b, a = signal.butter(2, fc[i] / (SR / 2), "low")
        if zi is None:
            zi = signal.lfilter_zi(b, a) * 0
        out[i:i + blk], zi = signal.lfilter(b, a, x[i:i + blk], zi=zi)
    e = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    return out * e * 0.8


def sfx_pop():
    t = tt(0.12)
    f = 900 * np.exp(-t * 18) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35) * 0.7


def sfx_ding(n=84, d=1.2):
    t = tt(d)
    f = midi(n)
    x = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6)
    return x * np.exp(-t * 3.5) * 0.45


def sfx_sparkle(d=1.2):
    out = np.zeros(int(d * SR))
    for i in range(14):
        n = 88 + int(rng.integers(0, 12))
        place(out, sfx_ding(n, 0.5) * 0.4, rng.uniform(0, d - 0.5))
    return out


def sfx_thud():
    return mx(kick(0.5) * 1.1, noise_burst(0.2, 80, 900, 25) * 0.6)


def sfx_boom():
    t = tt(2.5)
    f = 40 + 60 * np.exp(-t * 4)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)
    return x + lp(rng.standard_normal(len(t)), 400) * np.exp(-t * 3) * 0.6


def sfx_creak(d=2.5):
    t = tt(d)
    f = 90 + 25 * np.sin(2 * np.pi * 0.7 * t) + 15 * np.sin(2 * np.pi * 3.1 * t)
    ph = np.cumsum(f) / SR
    x = signal.sawtooth(2 * np.pi * ph) * (0.6 + 0.4 * np.sin(2 * np.pi * 11 * t))
    x = bp(x, 80, 1200)
    rumble = lp(rng.standard_normal(len(t)), 120) * 2
    return (x * 0.6 + rumble * 0.5) * env_adsr(len(t), 0.3, 0.2, 0.9, 0.6)


def sfx_snap():
    return mx(noise_burst(0.08, 1500, 9000, 50) * 1.2, noise_burst(0.25, 300, 3000, 20) * 0.6)


def sfx_fall_whistle(d=0.9):
    t = tt(d)
    f = np.linspace(1800, 500, len(t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env_adsr(len(t), 0.05, 0.1, 0.8, 0.1) * 0.25


def sfx_horn():
    t = tt(0.55)
    x = signal.square(2 * np.pi * 330 * t, 0.4) * 0.5 + signal.square(2 * np.pi * 392 * t, 0.4) * 0.5
    x = lp(x, 1500)
    e = env_adsr(len(t), 0.01, 0.05, 0.9, 0.08)
    e[int(0.22 * SR):int(0.3 * SR)] *= 0.1
    return x * e * 0.4


def sfx_sneeze():
    a = noise_burst(0.5, 400, 3000, 1.0) * np.linspace(0, 1, int(0.5 * SR)) ** 2 * 0.3
    b = noise_burst(0.35, 1500, 8000, 9) * 1.3
    out = np.zeros(int(0.9 * SR))
    place(out, a, 0)
    place(out, b, 0.5)
    return out


def sfx_growl(d=1.0):
    t = tt(d)
    f = 60 + 20 * np.sin(2 * np.pi * 7 * t)
    x = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR)
    return lp(x, 300) * env_adsr(len(t), 0.1, 0.1, 0.8, 0.3) * 0.6


def sfx_step():
    return noise_burst(0.07, 200, 2500, 60) * 0.35


def sfx_clunk():
    return mx(noise_burst(0.15, 200, 1500, 30) * 0.7, kick(0.2) * 0.3)


def sfx_tick():
    return noise_burst(0.03, 2000, 8000, 150) * 0.5


def sfx_flip():
    return noise_burst(0.06, 1000, 6000, 60) * 0.5


def sfx_riser(d):
    t = tt(d)
    f = np.geomspace(200, 1600, len(t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.15
    return x * np.linspace(0, 1, len(t)) ** 2 + sfx_whoosh(d) * 0.6


def sfx_bonk():
    t = tt(0.3)
    f = 500 * np.exp(-t * 10) + 200
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14) * 0.7


def amb_rain(d):
    x = rng.standard_normal(int(d * SR))
    return hp(lp(x, 5000), 600) * 0.06


def amb_birds(d):
    out = np.zeros(int(d * SR))
    t0 = 0.3
    while t0 < d - 0.5:
        n = int(rng.integers(2, 5))
        base = rng.uniform(2500, 4200)
        for k in range(n):
            tt_ = tt(0.09)
            f = base * (1 + 0.25 * np.sin(np.linspace(0, np.pi, len(tt_))))
            place(out, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.hanning(len(tt_)) * 0.08, t0 + k * 0.12)
        t0 += rng.uniform(1.2, 3.0)
    return out


def amb_wind(d):
    x = rng.standard_normal(int(d * SR))
    t = tt(d)
    return lp(x, 500) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.15 * t)) * 0.12


def amb_street(d):
    x = lp(rng.standard_normal(int(d * SR)), 700) * 0.12
    return x


# ------------------------------------------------------------------ music
SCALE_MAJ = [0, 2, 4, 5, 7, 9, 11]


def chords_major(root):
    # I - vi - IV - V
    return [[root, root + 4, root + 7], [root + 9, root + 12, root + 16], [root + 5, root + 9, root + 12],
            [root + 7, root + 11, root + 14]]


def chords_minor(root):
    # i - VI - III - VII
    return [[root, root + 3, root + 7], [root - 4, root, root + 3], [root + 3, root + 7, root + 10],
            [root - 2, root + 2, root + 5]]


def music_section(style, d, bpm=100):
    out = np.zeros(int(d * SR) + SR)
    beat = 60 / bpm
    bar = beat * 4
    nbars = int(math.ceil(d / bar))
    if style == "mystery":
        prog = chords_minor(50)
        for b in range(nbars):
            c = prog[b % 4]
            place(out, pad([n for n in c] + [c[0] - 12], bar * 1.05, cutoff=900, vol=0.7), b * bar)
            for k in range(8):
                n = c[k % 3] + 12 + (12 if k % 4 == 3 else 0)
                place(out, pluck_c(n, 0.6) * 0.18, b * bar + k * beat / 2)
    elif style == "playful":
        prog = chords_major(60)
        for b in range(nbars):
            c = prog[b % 4]
            place(out, bass(c[0] - 24, beat * 0.9) * 0.5, b * bar)
            place(out, bass(c[0] - 17, beat * 0.9) * 0.4, b * bar + 2 * beat)
            for k in range(8):
                if k in (1, 3, 5, 7) or k == 4:
                    n = c[(k * 2) % 3] + 12
                    place(out, pluck_c(n, 0.4) * 0.22, b * bar + k * beat / 2)
            place(out, pad(c, bar, cutoff=1200, vol=0.25), b * bar)
    elif style == "italy":
        prog = [[57, 61, 64], [62, 66, 69], [64, 68, 71], [57, 61, 64]]  # A major-ish, mandolin
        for b in range(nbars):
            c = prog[b % 4]
            place(out, bass(c[0] - 24, beat) * 0.5, b * bar)
            place(out, bass(c[0] - 17, beat) * 0.4, b * bar + 2 * beat)
            for k in range(16):  # tremolo mandolin arpeggio
                n = c[(k // 2) % 3] + 12
                place(out, pluck_c(n, 0.25) * 0.14, b * bar + k * beat / 4)
            place(out, pad(c, bar, cutoff=1400, vol=0.2), b * bar)
    elif style == "pastoral":
        prog = chords_major(55)
        mel = [7, 9, 11, 14, 12, 11, 9, 7]
        for b in range(nbars):
            c = prog[b % 4]
            place(out, pad(c + [c[0] - 12], bar * 1.05, cutoff=1100, vol=0.5), b * bar)
            for k in range(4):
                place(out, pluck_c(c[k % 3] + 12, 0.8) * 0.15, b * bar + k * beat)
            if b % 2 == 0:
                for k, m in enumerate(mel[:4] if b % 4 == 0 else mel[4:]):
                    place(out, flute(55 + 12 + m, beat * 0.95) * 0.13, b * bar + k * beat)
    elif style == "jazz":
        prog = [[53, 57, 60, 64], [50, 53, 57, 60], [55, 58, 62, 65], [48, 52, 55, 58]]
        walk = [0, 4, 7, 9]
        for b in range(nbars):
            c = prog[b % 4]
            for k in range(4):
                place(out, bass(c[0] - 24 + walk[k], beat * 0.85) * 0.55, b * bar + k * beat)
            for k in (1, 3):
                for n in c:
                    place(out, pluck_c(n + 12, 0.3) * 0.08, b * bar + k * beat + beat * 0.66)
            for k in range(8):  # brushed hats with swing
                sw = beat / 2 * (0.66 if k % 2 else 0)
                place(out, noise_burst(0.05, 5000, 12000, 80) * 0.08, b * bar + (k // 2) * beat + sw)
    elif style == "tunnel":
        for b in range(nbars):
            for k in range(16):
                n = [62, 65, 69, 72, 74, 77, 81, 84][(k + b * 3) % 8]
                place(out, pluck_c(n, 0.3) * 0.12, b * bar + k * beat / 4)
        place(out, pad([50, 57, 62, 65], d + 0.5, cutoff=1500, vol=0.5), 0)
    elif style == "warm":
        prog = chords_major(53)
        for b in range(nbars):
            c = prog[b % 4]
            place(out, pad(c + [c[0] - 12, c[1] + 12], bar * 1.05, cutoff=1600, vol=0.6), b * bar)
            for k in range(8):
                place(out, pluck_c(c[k % 3] + 12 + (12 if k >= 4 else 0), 0.7) * 0.15, b * bar + k * beat / 2)
            place(out, kick(0.3) * 0.25, b * bar)
            place(out, kick(0.3) * 0.15, b * bar + 2 * beat)
    elif style == "sting":
        place(out, sfx_boom() * 0.8, 0)
        place(out, pad([50, 57, 62, 66, 69], 3.5, cutoff=3000, vol=1.2), 0.05)
        place(out, sfx_sparkle(1.5) * 0.6, 0.2)
    return out[: int(d * SR)]


STYLE = {
    "hook": "mystery", "title": "sting", "cap": "playful", "museum": "playful", "touch": "mystery",
    "tunnel1": "tunnel", "pisa_arrive": "italy", "pisa_basket": "italy", "pisa_soil": "italy",
    "pisa_carry": "italy", "pisa_lean": "mystery", "pisa_fact": "italy", "tunnel2": "tunnel",
    "newton_arrive": "pastoral", "newton_think": "pastoral", "newton_climb": "pastoral",
    "newton_fall": "pastoral", "newton_idea": "warm", "tunnel3": "tunnel",
    "fleming_arrive": "jazz", "fleming_bact": "mystery", "fleming_sneeze": "jazz", "fleming_return": "mystery",
    "fleming_fact": "warm", "tunnel4": "tunnel", "return": "mystery", "gallery": "mystery", "ending": "warm",
    "outro": "playful", "endcard": "warm",
}


def build_music(shots, total):
    out = np.zeros(int((total + 2) * SR))
    # merge consecutive shots of the same style into one continuous section
    groups = []
    for s in shots:
        st = STYLE[s["id"]]
        if groups and groups[-1][0] == st and st not in ("sting",):
            groups[-1][2] = s["start"] + s["D"]
        else:
            groups.append([st, s["start"], s["start"] + s["D"]])
    XF = 0.6
    for st, a, b in groups:
        d = b - a + XF
        bpm = {"italy": 112, "jazz": 120, "tunnel": 130, "playful": 104}.get(st, 90)
        x = music_section(st, d, bpm)
        fade = int(XF * SR)
        x[:fade] *= np.linspace(0, 1, fade)
        x[-fade:] *= np.linspace(1, 0, fade)
        place(out, x, a - XF / 2)
    return out


# ------------------------------------------------------------------ SFX timeline
def build_sfx(shots, total):
    out = np.zeros(int((total + 2) * SR))
    amb = np.zeros_like(out)
    for s in shots:
        a, D, sid = s["start"], s["D"], s["id"]
        cue = make_cue(s)
        P = lambda x, t, g=1.0: place(out, x, a + t, g)
        if sid in ("museum", "touch", "return", "outro"):
            place(amb, amb_rain(D + 0.3), a)
        if sid.startswith("pisa"):
            place(amb, amb_wind(D) * 0.6, a)
        if sid.startswith("newton"):
            place(amb, amb_birds(D), a)
            place(amb, amb_wind(D) * 0.4, a)
        if sid == "fleming_arrive":
            place(amb, amb_street(cue("A tiny")), a)
        if sid.startswith("tunnel"):
            P(sfx_riser(min(D, 3.0)), 0, 0.9)
            for k in range(int(D / 0.12)):
                P(sfx_tick(), k * 0.12, 0.6)
        if sid in ("pisa_arrive", "newton_arrive", "fleming_arrive", "return", "tunnel1", "tunnel2", "tunnel3",
                   "tunnel4"):
            P(sfx_whoosh(0.7, up=False), 0, 0.9)
        if sid == "hook":
            for w in ("tower", "apple", "mould"):
                P(sfx_whoosh(0.5), cue(w) - 0.1, 0.7)
                P(sfx_pop(), cue(w) + 0.35, 0.6)
            P(sfx_boom(), cue("My accidents") - 0.2, 0.7)
        elif sid == "cap":
            P(sfx_pop(), cue("Red."), 0.8)
            P(sfx_fall_whistle(0.4), cue("Slightly") + 0.15, 0.8)
            P(sfx_ding(91), cue("Remember"), 0.6)
        elif sid == "museum":
            t_ac = cue("The air")
            for k in range(int(t_ac / 0.32)):
                P(sfx_step(), k * 0.32, 0.7)
            P(sfx_ding(88), cue("Then I saw"), 0.5)
            for k in range(6):
                P(sfx_step(), cue("Then I saw") + 0.3 + k * 0.33, 0.7)
            P(sfx_sparkle(1.2), cue("Then I saw") + 1.0, 0.5)
        elif sid == "touch":
            P(sfx_sparkle(1.5), D * 0.7, 0.8)
            P(sfx_riser(1.2), D - 1.2, 0.8)
        elif sid == "pisa_arrive":
            P(sfx_fall_whistle(0.6), 0.2, 0.7)
            P(sfx_thud(), 0.9, 0.9)
            P(sfx_pop(), cue("Perfectly") + 0.4, 0.5)
        elif sid == "pisa_basket":
            P(sfx_thud(), 1.3, 0.6)
            P(sfx_clunk(), 1.35, 0.6)
            P(sfx_pop(), cue("Free lunch"), 0.7)
        elif sid == "pisa_soil":
            P(sfx_creak(2.0), cue("The ground"), 0.5)
            for i in range(3):
                P(sfx_pop(), cue("Clay") + i * 0.7, 0.5)
            P(sfx_whoosh(0.5), cue("Building") - 0.3, 0.6)
            P(sfx_creak(1.6), cue("Building") + 0.9, 0.4)
        elif sid == "pisa_carry":
            k = 0
            while 0.2 + k * 1.35 < D:
                base = 0.2 + k * 1.35
                for j in range(4):
                    P(sfx_step(), base + j * 0.2, 0.6)
                P(sfx_clunk(), base + 0.81, 0.7)
                k += 1
            P(sfx_ding(84), cue("I was very proud"), 0.6)
        elif sid == "pisa_lean":
            P(sfx_creak(cue("The whole tower") + 2.8), 0.1, 1.0)
            P(sfx_boom(), cue("The whole tower") + 2.4, 0.5)
            P(sfx_bonk(), cue("Then they stared"), 0.6)
        elif sid == "pisa_fact":
            for i in range(4):
                P(sfx_pop(), 0.4 + i * 0.6, 0.5)
            P(sfx_pop(), cue("Today") + 0.8, 0.6)
            P(sfx_pop(), cue("You're welcome"), 0.7)
        elif sid == "newton_think":
            P(sfx_growl(1.2), cue("I was hungry"), 0.8)
        elif sid == "newton_climb":
            for k in range(8):
                P(sfx_step(), cue("I climbed") + k * 0.3, 0.5)
            st = cue("And the branch", frac=0.75)
            P(sfx_snap(), st, 1.0)
            P(sfx_fall_whistle(0.9), st + 0.1, 0.8)
            P(sfx_thud(), st + 1.0, 0.8)
        elif sid == "newton_fall":
            P(sfx_fall_whistle(cue("Newton watched")), 0, 0.5)
            P(sfx_boom(), cue("Down."), 0.4)
            P(sfx_bonk(), cue("Newton watched") + 1.0, 0.7)
            P(sfx_sparkle(1.3), cue("Newton watched") + 1.6, 0.6)
        elif sid == "newton_idea":
            P(sfx_ding(86), 0.3, 0.6)
            P(sfx_pop(), cue("Twenty one") + 0.6, 0.6)
            P(sfx_bonk(), cue("Lying") + 0.8, 0.5)
        elif sid == "fleming_arrive":
            P(sfx_horn(), 0.6, 0.9)
            P(sfx_ding(76, 2.5), cue("Big Ben"), 0.5)
        elif sid == "fleming_bact":
            P(sfx_pop(), 1.0, 0.5)
            P(sfx_boom(), cue("There was no cure"), 0.4)
        elif sid == "fleming_sneeze":
            P(sfx_flip(), cue("I lifted") + 0.1, 0.8)
            P(sfx_whoosh(1.2), cue("Just then"), 0.5)
            P(sfx_sneeze(), cue("I sneezed") - 0.5, 1.0)
            P(sfx_clunk(), cue("I sneezed") + 0.25, 0.5)
        elif sid == "fleming_return":
            tb = cue("Fleming was back")
            for k in range(int((tb - 0.2) / 0.18)):
                P(sfx_flip(), 0.2 + k * 0.18, 0.6)
            P(sfx_ding(81), cue("Then he stopped"), 0.5)
            P(sfx_sparkle(1.2), cue("And all around") + 1.4, 0.5)
        elif sid == "fleming_fact":
            P(sfx_sparkle(1.5), cue("And from it") + 0.2, 0.7)
            P(sfx_ding(84), cue("In nineteen"), 0.6)
        elif sid == "return":
            P(sfx_thud(), 0.5, 0.8)
            P(sfx_boom(), cue("My cap was gone"), 0.6)
        elif sid == "gallery":
            for w in ("A leaning", "A young man", "And a messy"):
                P(sfx_ding(79, 1.5), cue(w) + 1.0, 0.5)
        elif sid == "ending":
            P(sfx_pop(), cue("Changing"), 0.6)
            P(sfx_boom(), cue("By accident"), 0.5)
        elif sid == "outro":
            P(sfx_sparkle(1.0), cue("Probably") + 0.5, 0.6)
        elif sid == "endcard":
            P(sfx_pop(), 0.4, 0.6)
            P(sfx_pop(), 1.0, 0.7)
            P(sfx_fall_whistle(0.8), 2.2, 0.7)
            P(sfx_bonk(), 3.0, 0.8)
            P(sfx_ding(91), 3.05, 0.5)
    return out, amb


def build_vo(shots, total, vo_dir):
    out = np.zeros(int((total + 2) * SR))
    for s in shots:
        if s["vo"]:
            x, sr = sf.read(os.path.join(vo_dir, s["vo"] + ".wav"))
            assert sr == SR
            place(out, x, s["start"])
    return out


def main(vo_dir, out_path):
    shots, total = build_timeline(vo_dir)
    vo = build_vo(shots, total, vo_dir)
    music = build_music(shots, total)
    sfx, amb = build_sfx(shots, total)
    # duck music under the voice
    env = np.abs(vo)
    win = int(0.25 * SR)
    env = np.convolve(env, np.ones(win) / win, mode="same")
    duck = 1 - 0.55 * np.clip(env / 0.03, 0, 1)
    duck = np.convolve(duck, np.ones(win) / win, mode="same")
    norm = lambda x: x / (np.max(np.abs(x)) + 1e-9)
    mix = norm(vo) * 0.95 + norm(music) * 0.26 * duck + norm(sfx) * 0.45 + amb * 0.9
    n = int(total * SR)
    mix = mix[:n]
    # fade the tail
    mix[-int(1.0 * SR):] *= np.linspace(1, 0, int(1.0 * SR))
    mix = mix / max(1.0, np.max(np.abs(mix)) / 0.98)
    stereo = np.stack([mix, mix], axis=1)
    sf.write(out_path, stereo, SR, subtype="PCM_16")
    print("wrote", out_path, f"{total:.2f}s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
