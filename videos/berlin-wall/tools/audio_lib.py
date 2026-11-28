"""Synth + SFX library shared by History World episodes (music sections and cartoon effects)."""
import sys, os, math
import numpy as np
import soundfile as sf
from scipy import signal

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
    elif style == "musette":
        # Parisian musette waltz: accordion (detuned reeds), oom-pah-pah bass
        prog = [[57, 61, 64], [62, 66, 69], [64, 68, 71], [57, 61, 64], [62, 66, 69], [57, 61, 64], [64, 68, 71], [57, 61, 64]]
        bar3 = beat * 3
        nb = int(math.ceil(d / bar3))
        mel = [76, 74, 73, 71, 73, 74, 76, 78, 76, 73, 69, 71, 73, 74, 71, 69]
        for b in range(nb):
            c = prog[b % len(prog)]
            place(out, bass(c[0] - 24, beat * 0.8) * 0.55, b * bar3)
            for k in (1, 2):
                for n in c:
                    x = saw(midi(n), beat * 0.55, 0.006)
                    place(out, lp(x, 2200) * env_adsr(len(x), 0.01, 0.05, 0.7, 0.05) * 0.05, b * bar3 + k * beat)
            m = mel[(b * 2) % len(mel)], mel[(b * 2 + 1) % len(mel)]
            for k, n in enumerate(m):
                x = saw(midi(n), beat * 1.4, 0.008) + 0.6 * saw(midi(n) * 1.003, beat * 1.4, 0.0)
                x = lp(x, 3000) * env_adsr(len(x), 0.04, 0.1, 0.8, 0.1)
                x *= 1 + 0.15 * np.sin(2 * np.pi * 5.5 * tt(beat * 1.4))
                place(out, x * 0.09, b * bar3 + k * beat * 1.5)
    elif style == "chase":
        # galop / can-can style chase: fast oom-pah, staccato brass line, snare
        prog = [[60, 64, 67], [67, 71, 74], [60, 64, 67], [65, 69, 72]]
        line_ = [72, 74, 76, 77, 79, 77, 76, 74]
        for b in range(nbars):
            c = prog[b % 4]
            for k in range(4):
                place(out, bass(c[0] - 24 if k % 2 == 0 else c[2] - 24, beat * 0.45) * 0.55, b * bar + k * beat)
                for n in c:
                    if k % 2 == 1:
                        place(out, pluck_c(n, 0.2) * 0.08, b * bar + k * beat)
            for k in range(8):
                n = line_[(k + b * 3) % 8]
                x = saw(midi(n), beat * 0.35, 0.004)
                place(out, lp(x, 3000) * env_adsr(len(x), 0.005, 0.05, 0.6, 0.03) * 0.1, b * bar + k * beat / 2)
                place(out, noise_burst(0.06, 1500, 8000, 50) * (0.2 if k % 2 else 0.1), b * bar + k * beat / 2)
    elif style == "egypt":
        # adventure theme in the Hijaz scale: oud-like plucks, darbuka groove, ney-like flute melody
        root = 50
        hij = [0, 1, 4, 5, 7, 8, 10, 12]
        mel = [7, 8, 7, 5, 4, 5, 4, 1, 0, 1, 4, 5, 7, 8, 10, 12]
        for b in range(nbars):
            place(out, pad([root - 12, root, root + 7], bar * 1.05, cutoff=800, vol=0.35), b * bar)
            # darbuka: doum-tek-tek-doum-tek
            for k, (pos, kind) in enumerate(((0, "D"), (1, "t"), (1.5, "t"), (2, "D"), (3, "t"), (3.5, "k"))):
                if kind == "D":
                    place(out, kick(0.3) * 0.5, b * bar + pos * beat)
                else:
                    place(out, noise_burst(0.06, 1800, 9000, 60) * (0.28 if kind == "t" else 0.16), b * bar + pos * beat)
            for k in range(8):
                deg = hij[(k * 3 + b) % len(hij)]
                place(out, pluck_c(root + deg, 0.5) * 0.18, b * bar + k * beat / 2)
            if b % 2 == 1:
                for k in range(4):
                    m = mel[(b * 2 + k) % len(mel)]
                    place(out, flute(root + 12 + m, beat * 0.95, vib=6) * 0.13, b * bar + k * beat)
    elif style == "bouncy":
        # bright cartoon bounce: tuba-ish bass, pizzicato, glockenspiel
        prog = [[60, 64, 67], [65, 69, 72], [67, 71, 74], [60, 64, 67]]
        for b in range(nbars):
            c = prog[b % 4]
            for k in range(4):
                place(out, bass(c[0] - 24 + (7 if k % 2 else 0), beat * 0.6) * 0.55, b * bar + k * beat)
            for k in range(8):
                if k % 2 == 1:
                    place(out, pluck_c(c[(k // 2) % 3] + 12, 0.25) * 0.2, b * bar + k * beat / 2)
            if b % 2 == 0:
                for k, n in enumerate((c[2] + 12, c[1] + 12, c[0] + 24)):
                    place(out, sfx_ding(n, 0.6) * 0.18, b * bar + k * beat * 0.5 + beat * 2)
            place(out, noise_burst(0.05, 4000, 10000, 80) * 0.08, b * bar + beat)
            place(out, noise_burst(0.05, 4000, 10000, 80) * 0.08, b * bar + 3 * beat)
    elif style == "imperial":
        # grand march: brass-ish saw stabs, timpani, snare rolls
        prog = [[55, 59, 62], [60, 64, 67], [62, 66, 69], [55, 59, 62]]
        for b in range(nbars):
            c = prog[b % 4]
            place(out, pad(c + [c[0] - 12], bar * 1.02, cutoff=2200, det=0.006, vol=0.6), b * bar)
            for k in (0, 2):
                place(out, kick(0.5) * 0.5, b * bar + k * beat)
            for k in range(8):
                place(out, noise_burst(0.06, 1500, 8000, 50) * (0.18 if k % 2 else 0.1), b * bar + k * beat / 2)
            mel = [7, 7, 7, 12, 11, 9, 7, 4][(b % 2) * 4:(b % 2) * 4 + 4]
            for k, m in enumerate(mel):
                x = saw(midi(c[0] + 12 + m - 7 + 7), beat * 0.85, 0.004)
                place(out, lp(x, 2500) * env_adsr(len(x), 0.02, 0.1, 0.7, 0.1) * 0.16, b * bar + k * beat)
    elif style == "cathedral":
        # organ-like chords + choir pad + bells
        prog = [[50, 57, 62, 66], [47, 55, 59, 62], [52, 59, 64, 67], [45, 54, 57, 62]]
        for b in range(nbars):
            c = prog[b % 4]
            org = np.zeros(int(bar * 1.05 * SR))
            for n in c:
                tt_ = tt(bar * 1.05)
                for h, a in ((1, 1), (2, 0.5), (4, 0.25)):
                    org += a * np.sin(2 * np.pi * midi(n) * h * tt_)
            org = org / 8 * env_adsr(len(org), 0.25, 0.2, 0.9, 0.4)
            place(out, org * 0.5, b * bar)
            place(out, pad([n + 12 for n in c], bar * 1.05, cutoff=1400, det=0.008, vol=0.35), b * bar)
            if b % 2 == 0:
                place(out, sfx_ding(c[0] + 24, 3.0) * 0.5, b * bar)
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


def sfx_crowd(d, excite=0.5):
    t = tt(d)
    x = bp(rng.standard_normal(len(t)), 300, 2500) * (0.5 + excite * 0.5 * (1 + np.sin(2 * np.pi * 0.4 * t)))
    return x * env_adsr(len(t), 0.4, 0.1, 1.0, 0.6) * 0.5


def sfx_gasp():
    t = tt(1.0)
    return bp(rng.standard_normal(len(t)), 600, 4000) * np.exp(-t * 3) * np.clip(t * 20, 0, 1) * 1.2


def sfx_bell(n=50, d=4.0):
    t = tt(d)
    f = midi(n)
    x = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t * dc) for h, a, dc in
            ((1, 1, 0.6), (2.01, 0.6, 0.9), (2.76, 0.4, 1.3), (5.4, 0.25, 2)))
    return x * 0.4


def sfx_hooves(d):
    out = np.zeros(int(d * SR))
    k = 0
    while k * 0.16 < d - 0.1:
        place(out, noise_burst(0.05, 300, 2500, 70) * (0.5 if k % 4 else 0.8), k * 0.16)
        k += 1
    return out


def sfx_coins():
    out = np.zeros(int(1.0 * SR))
    for k in range(8):
        place(out, sfx_ding(96 + int(rng.integers(0, 8)), 0.4) * 0.5, k * 0.08)
    return out


def sfx_boing(d=0.5):
    t = tt(d)
    f = 180 + 120 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5) * 0.7


def sfx_slide_whistle(d=1.0, up=True):
    t = tt(d)
    f = np.linspace(500, 1800, len(t)) if up else np.linspace(1800, 500, len(t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * lp(rng.standard_normal(len(t)), 3000)
    return x * env_adsr(len(t), 0.05, 0.1, 0.9, 0.1) * 0.25


def sfx_portal(d=2.0):
    t = tt(d)
    x = np.zeros(len(t))
    for f0 in (110, 165, 220):
        f = f0 * (1 + 0.5 * t / d) * (1 + 0.02 * np.sin(2 * np.pi * 7 * t))
        x += np.sin(2 * np.pi * np.cumsum(f) / SR)
    return x / 3 * env_adsr(len(t), 0.3, 0.2, 0.9, 0.4) * 0.6 + sfx_whoosh(d) * 0.5


def sfx_horse():
    t = tt(1.0)
    f = 600 + 300 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 2)
    x = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR)
    return bp(x, 400, 3000) * np.exp(-t * 2.5) * 0.4


def sfx_splash():
    return mx(noise_burst(0.8, 400, 6000, 4) * 0.8, kick(0.3) * 0.4)


def sfx_water(d):
    t = tt(d)
    return bp(rng.standard_normal(len(t)), 200, 1500) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * t)) * 0.18


def sfx_cheer(d=3.0):
    t = tt(d)
    x = bp(rng.standard_normal(len(t)), 500, 4000) * env_adsr(len(t), 0.2, 0.3, 0.8, 0.8)
    out = x * 0.6
    for k in range(10):
        place(out, sfx_ding(84 + int(rng.integers(0, 12)), 0.2) * 0.0, rng.uniform(0, d - 0.3))
    return out


def sfx_click():
    return noise_burst(0.02, 2000, 9000, 300) * 0.9


def sfx_hum(d=1.0):
    t = tt(d)
    return (np.sin(2 * np.pi * 110 * t) + 0.4 * np.sin(2 * np.pi * 220 * t)) * env_adsr(len(t), 0.1, 0.1, 0.8, 0.2) * 0.3


def sfx_camera():
    return mx(sfx_click(), noise_burst(0.12, 1000, 6000, 40) * 0.4)


def sfx_cat():
    t = tt(0.6)
    f = 700 + 300 * np.sin(np.pi * t / 0.6)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.6) * 0.25


def sfx_crunch():
    return noise_burst(0.2, 800, 6000, 20) * 0.6


def sfx_whistle_police(d=0.9):
    t = tt(d)
    f = 2700 + 250 * np.sign(np.sin(2 * np.pi * 28 * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * bp(rng.standard_normal(len(t)), 2000, 4000)
    return x * env_adsr(len(t), 0.02, 0.05, 0.9, 0.08) * 0.3


def sfx_bark():
    t = tt(0.25)
    f = 500 * np.exp(-t * 6) + 250
    x = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR)
    return bp(x, 300, 3000) * np.exp(-t * 10) * 0.6


def amb_museum(d):
    x = lp(rng.standard_normal(int(d * SR)), 300) * 0.05
    out = x.copy()
    k = 0.7
    while k < d - 0.5:
        place(out, sfx_step() * 0.25, k)
        k += rng.uniform(1.0, 2.2)
    return out


def amb_paris(d):
    out = lp(rng.standard_normal(int(d * SR)), 900) * 0.06
    k = 0.3
    while k < d - 1.0:
        place(out, sfx_hooves(1.0) * 0.12, k)
        k += rng.uniform(2.5, 5.0)
    return out


def sfx_ticket_glow(d=2.0):
    return mx(sfx_hum(d) * 0.6, sfx_sparkle(d) * 0.7)


def sfx_type(d):
    out = np.zeros(int(d * SR))
    k = 0.0
    while k < d - 0.05:
        place(out, sfx_click() * 0.35, k)
        k += rng.uniform(0.08, 0.16)
    return out


def sfx_bell_door():
    return mx(sfx_ding(88, 0.8) * 0.8, sfx_ding(84, 0.8) * 0.0)

