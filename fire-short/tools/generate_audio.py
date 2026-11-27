"""Procedurally synthesize all sound effects and the background music.

Everything here is generated from scratch with numpy (no samples, no
copyrighted material). Usage: python3 tools/generate_audio.py
Writes public/audio/sfx_<id>.wav and public/audio/music.wav (Great Fire of London Short)
"""
import json
import os
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "public", "audio")
SR = 44100
rng = np.random.default_rng(7)

with open(os.path.join(ROOT, "src", "timeline.json")) as f:
    TL = json.load(f)


def write(name, x):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    peak = np.max(np.abs(x)) + 1e-9
    if peak > 0.98:
        x = x / peak * 0.98
    data = (x * 32767).astype(np.int16)
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def t_(d):
    return np.arange(int(d * SR)) / SR


def env(n, a=0.005, r=0.1, total=None):
    total = total or n / SR
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4))
    e *= np.clip((total - t) / max(r, 1e-4), 0, 1)
    return e


def lowpass(x, cutoff):
    """One-pole low-pass; cutoff may be an array."""
    cutoff = np.broadcast_to(np.asarray(cutoff, dtype=np.float64), x.shape)
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.zeros_like(x)
    prev = 0.0
    for i in range(len(x)):
        prev = (1 - a[i]) * x[i] + a[i] * prev
        y[i] = prev
    return y


def lp_fast(x, cutoff):
    """Constant-cutoff low-pass via FFT brick-ish rolloff (fast)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


def hp_fast(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (cutoff / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X, len(x))


def bandpass(x, lo, hi):
    return hp_fast(lp_fast(x, hi), lo)


def chirp(f0, f1, d, shape="exp"):
    t = t_(d)
    if shape == "exp":
        f = f0 * (f1 / f0) ** (t / d)
    else:
        f = f0 + (f1 - f0) * t / d
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph), f


# ----------------------------------------------------------------- SFX
def sfx_whoosh():
    d = 0.6
    t = t_(d)
    n = rng.standard_normal(len(t))
    cut = 300 + 5000 * np.sin(np.pi * t / d) ** 2
    y = lowpass(n, cut) * np.sin(np.pi * t / d) ** 1.5
    pan = np.linspace(-0.8, 0.8, len(t))
    return np.stack([y * (1 - pan) / 2, y * (1 + pan) / 2], 1) * 2.2


def sfx_boom():
    d = 2.2
    t = t_(d)
    s, _ = chirp(90, 32, d)
    n = lp_fast(rng.standard_normal(len(t)), 900) * np.exp(-t * 6)
    hit = lp_fast(rng.standard_normal(len(t)), 4000) * np.exp(-t * 30)
    return np.tanh((s * np.exp(-t * 2.2) + n * 0.8 + hit * 0.5) * 1.6)


def crackles(d, rate, vol=1.0):
    y = np.zeros(int(d * SR))
    n = int(d * rate)
    for _ in range(n):
        st = int(rng.uniform(0, d - 0.02) * SR)
        ln = int(rng.uniform(0.001, 0.006) * SR)
        y[st:st + ln] += rng.standard_normal(ln) * rng.uniform(0.2, 1) * np.exp(-np.arange(ln) / (ln / 3))
    return hp_fast(y, 1200) * vol


def sfx_roar():
    """Big fire: low rumbling roar + dense crackle, 9.5 s."""
    d = 9.5
    t = t_(d)
    rumble = lp_fast(rng.standard_normal(len(t)), 260)
    breath = bandpass(rng.standard_normal(len(t)), 300, 1600)
    am = 0.7 + 0.3 * lp_fast(rng.standard_normal(len(t)), 2) * 20
    y = rumble * 2.2 * am + breath * 0.6 * am + crackles(d, 90, 1.2)
    e = np.minimum(1, t / 0.25) * np.clip((d - t) / 0.6, 0, 1)
    return np.tanh(y * 1.3) * e


def sfx_crackle():
    d = 7.2
    t = t_(d)
    y = crackles(d, 45, 1.4) + bandpass(rng.standard_normal(len(t)), 200, 900) * 0.25 * np.minimum(1, t / 3)
    return y * np.clip((d - t) / 0.4, 0, 1)


def sfx_ignite():
    d = 1.4
    t = t_(d)
    n = rng.standard_normal(len(t))
    cut = 200 + 3000 * np.exp(-t * 2.5)
    y = lowpass(n, cut) * np.minimum(1, t / 0.05) * np.exp(-t * 1.6)
    return (y * 2.5 + crackles(d, 60, 0.8)) * 0.9


def sfx_crowd():
    """Crowd panic: many detuned formant 'voices' with pitch swoops."""
    d = 4.8
    t = t_(d)
    y = np.zeros_like(t)
    for v in range(14):
        f0 = rng.uniform(170, 420)
        st = rng.uniform(0, d - 1.2)
        ln = rng.uniform(0.6, 1.4)
        mask = (t >= st) & (t < st + ln)
        tt = t[mask] - st
        f = f0 * (1 + 0.25 * np.sin(np.pi * tt / ln)) * (1 + 0.03 * np.sin(2 * np.pi * 6 * tt))
        ph = 2 * np.pi * np.cumsum(f) / SR
        src = sum(np.sin(k * ph) / k for k in range(1, 12))
        y[mask] += src * np.sin(np.pi * tt / ln) ** 0.7 * rng.uniform(0.4, 1)
    y = bandpass(y, 500, 3000) + bandpass(y, 250, 700) * 0.4
    y += bandpass(rng.standard_normal(len(t)), 300, 2500) * 0.4
    for dl, g in [(0.07, 0.4), (0.15, 0.25)]:
        k = int(dl * SR)
        y[k:] += y[:-k] * g
    return y * np.minimum(1, t / 0.3) * np.clip((d - t) / 0.5, 0, 1) * 0.5


def sfx_bell():
    """Church bell toll (bells rang to raise the alarm)."""
    d = 3.0
    y = np.zeros(int(d * SR))
    for hit in [0.0, 1.0, 2.0]:
        tt = t_(d - hit)
        tone = sum(np.sin(2 * np.pi * 220 * r * tt) * g * np.exp(-tt * dec)
                   for r, g, dec in [(0.5, 0.6, 0.8), (1, 1, 1.2), (1.19, 0.5, 1.6), (1.5, 0.4, 2), (2, 0.35, 2.5), (2.74, 0.2, 3.5)])
        y[int(hit * SR):] += tone * (1 - hit * 0.15)
    return y * 0.5


def sfx_hit():
    """Orchestral impact."""
    d = 1.8
    t = t_(d)
    s, _ = chirp(70, 40, d)
    brass = sum(np.sign(np.sin(2 * np.pi * f * t)) * g for f, g in [(73.4, 1), (110, 0.6), (146.8, 0.5)])
    brass = lp_fast(brass, 1200) * np.exp(-t * 3)
    return np.tanh((s * np.exp(-t * 3) * 1.5 + brass * 0.35 + lp_fast(rng.standard_normal(len(t)), 3000) * np.exp(-t * 20) * 0.6) * 1.4)


def sfx_crash():
    """Timber collapse: thud + wood cracks + debris."""
    d = 2.5
    t = t_(d)
    thud = lp_fast(rng.standard_normal(len(t)), 150) * np.exp(-t * 3) * 3
    cracks = np.zeros_like(t)
    for _ in range(25):
        st = int(rng.uniform(0, 1.5) * SR)
        ln = int(0.03 * SR)
        cracks[st:st + ln] += bandpass(rng.standard_normal(ln), 600, 5000) * rng.uniform(0.3, 1)
    debris = bandpass(rng.standard_normal(len(t)), 1000, 6000) * np.exp(-t * 1.5) * 0.3
    return np.tanh((thud + cracks * 1.5 + debris) * 1.2)


def sfx_wind():
    d = 3.0
    t = t_(d)
    n = rng.standard_normal(len(t))
    cut = 300 + 1500 * np.sin(np.pi * t / d) ** 2
    y = lowpass(n, cut)
    s = np.sin(2 * np.pi * (400 + 200 * np.sin(np.pi * t / d)) * t) * 0.05
    return (y * 1.5 + s) * np.sin(np.pi * t / d)


def sfx_ash():
    """Fire dying down: falling hiss + low wind."""
    d = 3.0
    t = t_(d)
    hiss = hp_fast(rng.standard_normal(len(t)), 3000) * np.exp(-t * 1.2) * 0.4
    return hiss + crackles(d, 10, 0.5) * np.exp(-t) + lp_fast(rng.standard_normal(len(t)), 300) * 0.6 * np.sin(np.pi * t / d)


def sfx_steps():
    d = 2.8
    y = np.zeros(int(d * SR))
    for i in range(7):
        st = int((0.1 + i * 0.38) * SR)
        tt = t_(0.15)
        thump = np.sin(2 * np.pi * 110 * tt) * np.exp(-tt * 35)
        scuff = bandpass(rng.standard_normal(len(tt)), 800, 4000) * np.exp(-tt * 40) * 0.5
        y[st:st + len(tt)] += (thump + scuff) * (0.8 if i % 2 else 1)
    return y


def sfx_run():
    d = 4.6
    y = np.zeros(int(d * SR))
    tpos, i = 0.0, 0
    while tpos < d - 0.1:
        st = int(tpos * SR)
        tt = t_(0.08)
        tap = np.sin(2 * np.pi * (140 if i % 2 else 120) * tt) * np.exp(-tt * 40)
        tap += bandpass(rng.standard_normal(len(tt)), 1000, 5000) * np.exp(-tt * 50) * 0.5
        y[st:st + len(tt)] += tap
        tpos += 0.16
        i += 1
    return y * np.clip((d - t_(d)) / 0.3, 0, 1)


def sfx_beep():
    y = np.zeros(int(0.5 * SR))
    for k, f in enumerate([1320, 1760]):
        tt = t_(0.09)
        y[int(k * 0.13 * SR):int(k * 0.13 * SR) + len(tt)] += np.sign(np.sin(2 * np.pi * f * tt)) * 0.3
    return y


def sfx_powerup():
    s, _ = chirp(150, 1400, 1.0)
    t = t_(1.0)
    return (s + 0.3 * np.sign(s)) * np.minimum(1, t / 0.05) * np.clip((1 - t) / 0.2, 0, 1) * 0.5


def sfx_alarm():
    d = 1.8
    t = t_(d)
    f = np.where((t * 4) % 1 < 0.5, 880, 660)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sign(np.sin(ph)) * 0.25 * np.clip((d - t) / 0.1, 0, 1)


def sfx_portal():
    d = 1.6
    t = t_(d)
    s, f = chirp(80, 2400, d)
    wob = np.sin(2 * np.pi * np.cumsum(f * 1.01) / SR)
    n = lowpass(rng.standard_normal(len(t)), 300 + 6000 * t / d)
    return (s * 0.4 + wob * 0.3 + n * 1.2) * np.minimum(1, t / 0.1) * np.clip((d - t) / 0.25, 0, 1)


def sfx_pop():
    d = 0.25
    t = t_(d)
    s, _ = chirp(900, 300, d)
    return s * np.exp(-t * 22)


def sfx_sparkle():
    d = 1.4
    y = np.zeros(int(d * SR))
    for i in range(18):
        st = int(rng.uniform(0, d - 0.25) * SR)
        tt = t_(0.25)
        y[st:st + len(tt)] += np.sin(2 * np.pi * rng.uniform(2000, 6000) * tt) * np.exp(-tt * 18) * rng.uniform(0.3, 1)
    return y * 0.5


SFX = {k[4:]: v for k, v in dict(globals()).items() if k.startswith("sfx_") and callable(v)}

# --------------------------------------------------------------- MUSIC
# Original dramatic score in D minor: low strings, war drums, brass stabs.
D2 = 73.42


def semi(n, root=D2):
    return root * 2 ** (n / 12)


def strings(d, notes, vol=1.0, swell=True):
    t = t_(d)
    y = np.zeros_like(t)
    for n in notes:
        for det in (-0.12, 0.0, 0.11):
            f = semi(n + det)
            ph = 2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 5 * t)
            y += 2 * ((ph / (2 * np.pi)) % 1) - 1
    y = lp_fast(y, 1800) / (len(notes) * 3)
    e = np.minimum(1, t / (0.6 if swell else 0.02)) * np.clip((d - t) / 0.4, 0, 1)
    return y * e * vol


def brass(d, notes, vol=1.0):
    t = t_(d)
    y = np.zeros_like(t)
    for n in notes:
        ph = 2 * np.pi * semi(n) * t
        y += 2 * ((ph / (2 * np.pi)) % 1) - 1
    cut = 400 + 2600 * np.exp(-t * 4)
    y = lowpass(y / len(notes), cut)
    return y * np.minimum(1, t / 0.03) * np.exp(-t * 1.2) * vol


def taiko(f=60, d=0.9):
    t = t_(d)
    s, _ = chirp(f * 1.6, f, 0.3)
    s = np.concatenate([s, np.zeros(len(t) - len(s))])
    return (s * 1.2 + lp_fast(rng.standard_normal(len(t)), 800) * 0.4) * np.exp(-t * 4.5)


def snare(d=0.25):
    t = t_(d)
    return (bandpass(rng.standard_normal(len(t)), 1500, 7000) * 0.7 + np.sin(2 * np.pi * 190 * t) * 0.5) * np.exp(-t * 18)


def place(buf, x, at):
    st = int(at * SR)
    if st >= len(buf):
        return
    x = x[: len(buf) - st]
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    buf[st:st + len(x)] += x


DM, BB, GM, A7, F, C = [0, 3, 7], [-4, 0, 3], [-7, -4, 0], [-5, -1, 2], [3, 7, 10], [-2, 2, 5]


def music():
    total = TL["durationSec"] + 0.5
    L = np.zeros((int(total * SR), 2))
    sc = {s["id"]: s for s in TL["scenes"]}

    # HOOK: immediate impact, war drums, brass stabs
    s, e = sc["hook"]["start"], sc["hook"]["end"]
    place(L, strings(e - s, [0, 7, 12], 0.5, swell=False), s)
    for at in [0, 0.5, 1.0, 1.25, 1.5, 2.0, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75]:
        place(L, taiko(55) * 0.9, s + at)
    place(L, brass(1.4, [0, 3, 7, 12], 0.5), s)
    place(L, brass(1.4, [-2, 2, 5, 10], 0.5), s + 2.0)

    # STREET: uneasy, pizzicato-like pulse, rising
    s, e = sc["street"]["start"], sc["street"]["end"]
    prog = [DM, BB, GM, A7]
    for i, ch in enumerate(prog):
        place(L, strings(1.8, [n + 12 for n in ch], 0.35), s + i * 1.75)
    beat = 60 / 110
    for i in range(int((e - s) / beat)):
        place(L, taiko(70, 0.4) * (0.5 if i % 2 == 0 else 0.25), s + i * beat)
        if s + i * beat > 6.3:
            place(L, snare() * 0.25, s + i * beat + beat / 2)

    # BAKERY: suspense — low drone, ticking, swells at ignition
    s, e = sc["bakery"]["start"], sc["bakery"]["end"]
    place(L, strings(e - s, [0, 1, 12], 0.35), s)
    for i in range(int((e - s) / 0.5)):
        place(L, snare(0.06) * 0.12, s + i * 0.5)
    place(L, brass(2.0, [0, 3, 7], 0.6), 13.3)
    place(L, strings(2.2, [3, 7, 10, 15], 0.5), 15.8)

    # BURNS: full epic ostinato 128 bpm
    s, e = sc["burns"]["start"], sc["burns"]["end"]
    beat = 60 / 128
    prog = [DM, BB, F, C]
    bar = beat * 4
    for b in range(int((e - s) / bar) + 1):
        ch = prog[b % 4]
        place(L, strings(bar, [n + 12 for n in ch] + [ch[0]], 0.45, swell=False), s + b * bar)
        place(L, brass(0.8, [n + 12 for n in ch], 0.35), s + b * bar)
    for i in range(int((e - s) / beat)):
        place(L, taiko(55) * 0.8, s + i * beat)
        place(L, snare() * (0.45 if i % 2 else 0.2), s + i * beat + beat / 2)
        # ostinato
        place(L, brass(0.2, [prog[(i // 4) % 4][i % 3] + 24], 0.18), s + i * beat)

    # CATASTROPHE: heavier, slower, choir-like strings + bells
    s, e = sc["catastrophe"]["start"], sc["catastrophe"]["end"]
    prog = [DM, GM, BB, A7]
    for i, ch in enumerate(prog):
        place(L, strings(2.4, [n + 12 for n in ch] + [n + 24 for n in ch], 0.5), s + i * 2.25)
    beat = 60 / 96
    for i in range(int((e - s) / beat)):
        place(L, taiko(50, 1.0) * 0.9, s + i * beat)
    place(L, brass(2.5, [0, 3, 7, 12], 0.8), 34.4)

    # AFTERMATH: sombre, sparse
    s, e = sc["aftermath"]["start"], sc["aftermath"]["end"]
    place(L, strings(4.2, [0, 7, 15], 0.35), s)
    place(L, strings(4.0, [-4, 3, 12], 0.35), s + 4.0)

    # TWIST: tension ticks → stinger → upbeat end card
    s, e = sc["twist"]["start"], sc["twist"]["end"]
    for i in range(int(3.2 / 0.25)):
        place(L, snare(0.05) * (0.1 + i * 0.02), s + 0.2 + i * 0.25)
    place(L, strings(3.2, [0, 1, 6], 0.3), s)
    place(L, brass(1.5, [0, 3, 6, 12], 0.8), 47.35)
    beat = 60 / 128
    st = 48.4
    i = 0
    while st + i * beat < total:
        ch = [F, C, DM, BB][(i // 4) % 4]
        place(L, taiko(60, 0.5) * 0.6, st + i * beat)
        if i % 2:
            place(L, snare() * 0.35, st + i * beat)
        if i % 4 == 0:
            place(L, brass(1.2, [n + 12 for n in ch], 0.45), st + i * beat)
        i += 1

    fade = np.ones(len(L))
    fe = int(TL["durationSec"] * SR)
    fs = int((TL["durationSec"] - 0.6) * SR)
    fade[fs:fe] = np.linspace(1, 0, fe - fs)
    fade[fe:] = 0
    L *= fade[:, None]
    L[:, 1] = np.roll(L[:, 1], int(0.011 * SR))
    for dl, g in [(0.11, 0.22), (0.27, 0.12)]:
        k = int(dl * SR)
        L[k:] += L[:-k] * g
    return np.tanh(L * 1.1) * 0.9


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SFX.items():
        write(f"sfx_{name}.wav", fn())
    print("sfx:", ", ".join(SFX))
    write("music.wav", music())
    print("music done")
