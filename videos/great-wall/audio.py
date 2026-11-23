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
    """Karplus-Strong plucked string (vectorised with an IIR comb filter)."""
    n = int(d * SR)
    p = max(2, int(SR / f))
    x = np.zeros(n)
    x[:p] = rng.uniform(-1, 1, min(p, n))
    a = np.zeros(p + 2)
    a[0] = 1.0
    a[p] = -0.498
    a[p + 1] = -0.498
    out = signal.lfilter([1.0], a, x)
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
    elif style == "china":
        # pentatonic guzheng-like plucks with tremolo, low drum, erhu-ish flute line
        pent = [0, 2, 4, 7, 9]
        root = 62
        prog = [[root, root + 7], [root - 3, root + 4], [root + 2, root + 9], [root - 5, root + 2]]
        mel = [9, 7, 4, 2, 4, 7, 9, 12, 14, 12, 9, 7]
        for b in range(nbars):
            c = prog[b % 4]
            place(out, pad([c[0] - 12, c[0], c[1]], bar * 1.05, cutoff=900, vol=0.35), b * bar)
            for k in range(8):
                deg = pent[(k * 2 + b) % 5] + (12 if k >= 4 else 0)
                place(out, pluck_c(root + deg, 0.7) * 0.2, b * bar + k * beat / 2)
            place(out, kick(0.5) * 0.35, b * bar)
            place(out, kick(0.4) * 0.2, b * bar + beat * 2.5)
            if b % 2 == 1:
                for k in range(3):
                    m = mel[(b * 3 + k) % len(mel)]
                    place(out, flute(root + 12 + m, beat * 1.2, vib=6) * 0.12, b * bar + k * beat * 1.3)
    elif style == "tension":
        for b in range(nbars):
            for k in range(8):
                place(out, kick(0.3) * (0.55 if k % 2 == 0 else 0.3), b * bar + k * beat / 2)
            for k in range(16):
                n = [50, 50, 53, 50, 55, 50, 53, 48][k % 8]
                place(out, bass(n - 12, beat / 4 * 0.9) * 0.35, b * bar + k * beat / 4)
            place(out, pad([62, 65, 69], bar, cutoff=1300, vol=0.3), b * bar)
            place(out, noise_burst(0.3, 300, 3000, 12) * 0.25, b * bar + beat * 3.5)
    elif style == "night":
        root = 57
        for b in range(nbars):
            place(out, pad([root - 12, root, root + 3, root + 7], bar * 1.05, cutoff=700, vol=0.6), b * bar)
            for k in (0, 3, 5):
                place(out, pluck_c(root + 12 + [0, 3, 7, 10, 12][(k + b) % 5], 1.2) * 0.12, b * bar + k * beat / 2)
    elif style == "sting":
        place(out, sfx_boom() * 0.8, 0)
        place(out, pad([50, 57, 62, 66, 69], 3.5, cutoff=3000, vol=1.2), 0.05)
        place(out, sfx_sparkle(1.5) * 0.6, 0.2)
    return out[: int(d * SR)]


STYLE = {
    "hook": "tension", "rewind": "tension", "title": "sting", "intro": "playful", "museum": "playful",
    "touch": "mystery", "tunnel1": "tunnel", "arrive": "china", "wallfact": "china", "ming": "china",
    "bricks": "china", "stamp": "china", "rice": "playful", "ricefact": "china", "spill": "playful",
    "night": "night", "beacon": "tension", "beaconfact": "tension", "panic": "tension", "twist": "mystery",
    "battle": "tension", "hero": "warm", "peace": "china", "myth": "mystery", "tunnel2": "tunnel",
    "return": "mystery", "ending": "warm", "outro": "playful", "endcard": "warm",
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
        bpm = {"italy": 112, "jazz": 120, "tunnel": 130, "playful": 104, "tension": 132, "china": 84, "night": 70}.get(st, 90)
        x = music_section(st, d, bpm)
        fade = int(XF * SR)
        x[:fade] *= np.linspace(0, 1, fade)
        x[-fade:] *= np.linspace(1, 0, fade)
        place(out, x, a - XF / 2)
    return out


# ------------------------------------------------------------------ SFX timeline
def sfx_fire(d):
    t = tt(d)
    x = lp(rng.standard_normal(len(t)), 900) * 0.5
    crack = np.zeros(len(t))
    for k in range(int(d * 14)):
        i0 = int(rng.uniform(0, max(0.01, d - 0.05)) * SR)
        b = noise_burst(0.02, 1500, 7000, 200)
        crack[i0:i0 + len(b)] += b[: len(crack) - i0] * rng.uniform(0.3, 1.0)
    return (x + crack) * env_adsr(len(t), 0.2, 0.1, 1.0, 0.4)


def sfx_gong():
    t = tt(4.0)
    x = np.zeros(len(t))
    for f, a, dcy in ((110, 1, 0.8), (167, 0.6, 1.0), (232, 0.5, 1.3), (351, 0.35, 1.7), (529, 0.2, 2.2)):
        x += a * np.sin(2 * np.pi * f * t * (1 + 0.004 * np.exp(-t))) * np.exp(-t * dcy)
    return x * 0.5


def sfx_war_drum():
    return mx(kick(0.6) * 1.2, noise_burst(0.15, 100, 800, 20) * 0.4)


def sfx_horn_war(d=1.6):
    t = tt(d)
    x = signal.sawtooth(2 * np.pi * 110 * t * (1 + 0.01 * np.sin(2 * np.pi * 5 * t)))
    return lp(x, 900) * env_adsr(len(t), 0.25, 0.1, 0.8, 0.4) * 0.5


def sfx_cannon():
    return mx(sfx_boom() * 1.2, noise_burst(0.3, 200, 5000, 12) * 0.8)


def sfx_scratch():
    t = tt(0.35)
    f = 900 * (1 + np.sin(2 * np.pi * 9 * t))
    return bp(rng.standard_normal(len(t)), 300, 4000) * np.abs(np.sin(2 * np.pi * 6 * t)) * 0.8


def sfx_vhs(d):
    t = tt(d)
    x = bp(rng.standard_normal(len(t)), 800, 6000) * 0.25
    f = np.linspace(1200, 300, len(t))
    x += np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.15
    return x


def build_sfx(shots, total):
    out = np.zeros(int((total + 2) * SR))
    amb = np.zeros_like(out)
    for s in shots:
        a, D, sid = s["start"], s["D"], s["id"]
        cue = make_cue(s)
        P = lambda x, t, g=1.0: place(out, x, a + t, g)
        if sid in ("arrive", "wallfact", "ming", "bricks", "stamp", "rice", "spill", "hero"):
            place(amb, amb_wind(D) * 0.5, a)
            place(amb, amb_birds(D) * 0.6, a)
        if sid in ("night", "panic", "twist", "battle"):
            place(amb, amb_wind(D) * 1.0, a)
        if sid in ("hook", "panic", "twist", "battle"):
            place(amb, sfx_fire(D) * 0.25, a)
        if sid.startswith("tunnel"):
            P(sfx_riser(min(D, 3.0)), 0, 0.9)
            for k in range(int(D / 0.12)):
                P(sfx_tick(), k * 0.12, 0.6)
        if sid in ("arrive", "return", "tunnel1", "tunnel2"):
            P(sfx_whoosh(0.7, up=False), 0, 0.9)
        if sid == "hook":
            # instant impact on frame one
            P(sfx_cannon(), 0.0, 1.0)
            P(sfx_whoosh(0.6), 0.0, 0.9)
            for k in range(8):
                P(sfx_whoosh(0.5, up=True), 0.15 + k * 0.45, 0.35)
            P(sfx_war_drum(), cue("The year"), 0.9)
            for k in range(6):
                P(sfx_war_drum(), cue("Enemies") + k * 0.35, 0.8)
            P(sfx_horn_war(), cue("Enemies") + 0.2, 0.8)
            P(sfx_scratch(), cue("That's me") + 0.45, 1.0)
            P(sfx_boom(), cue("At least") + 0.4, 0.6)
        elif sid == "rewind":
            P(sfx_vhs(D), 0, 1.0)
        elif sid == "intro":
            P(sfx_pop(), 0.3, 0.6)
            P(sfx_whoosh(0.5), cue("Last time"), 0.5)
            P(sfx_pop(), cue("So I made"), 0.6)
            P(sfx_ding(88), cue("No more") + 0.8, 0.6)
        elif sid == "museum":
            for k in range(int(cue("And in the middle") / 0.32)):
                P(sfx_step(), k * 0.32, 0.7)
            for w in ("Old.", "Grey.", "Boring."):
                P(sfx_pop(), cue(w), 0.5)
        elif sid == "touch":
            for k in range(4):
                P(sfx_tick(), k * D * 0.2, 1.0)
            P(sfx_sparkle(1.2), D * 0.75, 0.8)
            P(sfx_riser(1.0), D - 1.0, 0.8)
        elif sid == "arrive":
            P(sfx_fall_whistle(0.6), 0.1, 0.7)
            P(sfx_thud(), 0.7, 0.9)
            P(sfx_gong(), cue("And in front") + 0.3, 0.6)
        elif sid == "wallfact":
            P(sfx_pop(), cue("It's many walls"), 0.6)
            for k in range(6):
                P(sfx_whoosh(0.4), cue("It's many walls") + 0.6 + k * 0.55, 0.3)
            P(sfx_ding(84), cue("Put all") + 2.2, 0.6)
        elif sid == "ming":
            for k in range(int(D / 0.9)):
                P(sfx_clunk(), 0.4 + k * 0.9, 0.25)
            P(sfx_gong(), cue("And a famous") + 0.6, 0.4)
        elif sid == "bricks":
            P(sfx_pop(), cue("And many bricks") + 0.3, 0.5)
            P(sfx_snap(), cue("If a brick") + 0.3, 0.8)
            P(sfx_bonk(), cue("If a brick") + 1.0, 0.6)
        elif sid == "stamp":
            P(sfx_thud(), cue("A tiny cap") + 0.25, 0.8)
            P(sfx_ding(91), cue("Remember"), 0.6)
        elif sid == "rice":
            P(sfx_growl(1.0), cue("I was starving"), 0.8)
            P(sfx_horn(), cue("I grabbed", frac=0.7), 0.6)
            P(sfx_boom(), cue("It was glue"), 0.4)
        elif sid == "ricefact":
            for k in range(3):
                P(sfx_pop(), 0.2 + k * 1.2, 0.6)
            P(sfx_ding(84), cue("Some of those"), 0.6)
        elif sid == "spill":
            P(sfx_fall_whistle(0.6), cue("And I, of course") + 0.3, 0.7)
            P(sfx_thud(), cue("And I, of course") + 1.2, 0.9)
            P(sfx_whoosh(0.8), cue("A whole sack"), 0.5)
            P(sfx_pop(), cue("Double sticky"), 0.7)
            for k in range(4):
                P(sfx_clunk(), cue("Then he shrugged") + 1.2 + k * 0.5, 0.4)
        elif sid == "night":
            P(sfx_whoosh(1.5, up=False), cue("The wind"), 0.6)
            P(sfx_ding(76), cue("And a torch"), 0.4)
        elif sid == "beacon":
            P(sfx_fire(D), 0.2, 0.6)
            P(sfx_boom(), cue("That was the alarm"), 0.7)
            t0 = cue("The moment") + 0.6
            for k in range(8):
                P(sfx_whoosh(0.5, up=True), t0 + k * 0.9, 0.5)
                P(sfx_war_drum(), t0 + k * 0.9, 0.5)
        elif sid == "beaconfact":
            for w, n in (("One fire", 1), ("Two fires", 2), ("Three fires", 3)):
                for k in range(n):
                    P(sfx_cannon(), cue(w) + 0.3 + k * 0.35, 0.45)
            P(sfx_fire(D - cue("Thanks to the wind")), cue("Thanks to the wind"), 0.6)
        elif sid == "panic":
            for k in range(int(D / 0.45)):
                P(sfx_war_drum(), k * 0.45, 0.7)
            P(sfx_horn_war(2.0), cue("Horns"), 0.9)
            for k in range(int(D / 0.3)):
                P(sfx_step(), k * 0.3, 0.6)
        elif sid == "twist":
            P(sfx_boom(), cue("Down below"), 0.6)
            P(sfx_ding(70, 2.0), cue("Right under"), 0.5)
        elif sid == "battle":
            for k in range(6):
                P(sfx_clunk(), cue("They threw") + k * 0.4, 0.6)
            for k in range(int((cue("But that section") - cue("They pushed")) / 0.4)):
                P(sfx_war_drum(), cue("They pushed") + k * 0.4, 0.5)
            P(sfx_gong(), cue("Not one brick"), 0.7)
            for k in range(8):
                P(sfx_step(), cue("The raiders looked", frac=0.8) + k * 0.3, 0.5)
        elif sid == "hero":
            P(sfx_gong(), 0.2, 0.4)
            P(sfx_sparkle(1.2), 0.3, 0.5)
        elif sid == "peace":
            P(sfx_whoosh(1.0), 0.2, 0.5)
            P(sfx_gong(), 1.2, 0.5)
            P(sfx_bonk(), cue("I definitely"), 0.5)
        elif sid == "myth":
            P(sfx_boom(), cue("It isn't"), 0.6)
            P(sfx_whoosh(1.0), cue("In two thousand"), 0.5)
        elif sid == "return":
            P(sfx_thud(), 0.5, 0.8)
            P(sfx_ding(84), cue("In the corner") + 1.6, 0.6)
        elif sid == "ending":
            P(sfx_fire(1.0), cue("I set it on fire"), 0.5)
            P(sfx_gong(), cue("But it's still"), 0.6)
            P(sfx_pop(), cue("You're welcome"), 0.6)
        elif sid == "outro":
            P(sfx_ding(91), cue("Probably"), 0.5)
        elif sid == "endcard":
            P(sfx_pop(), 0.4, 0.6)
            P(sfx_pop(), 1.0, 0.7)
            P(sfx_fall_whistle(0.6), 2.4, 0.6)
            P(sfx_thud(), 3.0, 0.7)
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
