"""Synthesize every sound effect and the music for the battlefield scene.

All audio is generated from scratch with numpy: no samples, no existing music.
Usage: python3 tools/generate_audio.py
Writes public/audio/sfx_<id>.wav and public/audio/music.wav
"""
import json
import os
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "public", "audio")
SR = 44100
rng = np.random.default_rng(431)  # 431 BC
TL = json.load(open(os.path.join(ROOT, "src", "timeline.json")))
B = TL["beats"]


def write(name, x):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    peak = np.max(np.abs(x)) + 1e-9
    if peak > 0.98:
        x = x / peak * 0.98
    with wave.open(os.path.join(OUT, name), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def t_(d):
    return np.arange(int(d * SR)) / SR


def lp(x, c):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / c) ** 4), len(x))


def hp(x, c):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (c / np.maximum(f, 1)) ** 4), len(x))


def bp(x, lo, hi):
    return hp(lp(x, hi), lo)


def chirp(f0, f1, d):
    t = t_(d)
    f = f0 * (f1 / f0) ** (t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def place(buf, x, at):
    st = int(at * SR)
    if st >= len(buf):
        return
    x = x[: len(buf) - st]
    if x.ndim == 1 and buf.ndim == 2:
        x = np.stack([x, x], 1)
    buf[st:st + len(x)] += x


# ------------------------------------------------------------------ SFX
def sfx_wind():
    d = 12.0
    t = t_(d)
    n = rng.standard_normal(len(t))
    gust = 0.6 + 0.4 * np.sin(2 * np.pi * 0.15 * t) * np.sin(2 * np.pi * 0.07 * t + 1)
    return lp(n, 500) * gust * 0.8 * np.minimum(1, t / 0.5) * np.clip((d - t) / 0.5, 0, 1)


def clang_one(f0=520):
    d = 1.2
    t = t_(d)
    y = sum(np.sin(2 * np.pi * f0 * r * t + rng.uniform(0, 6)) * g * np.exp(-t * dec)
            for r, g, dec in [(1, 1, 6), (1.47, 0.6, 7), (2.09, 0.5, 9), (2.76, 0.35, 12), (3.9, 0.2, 15)])
    hit = bp(rng.standard_normal(len(t)), 1500, 8000) * np.exp(-t * 40)
    return (y * 0.4 + hit * 0.6)


def sfx_clang():
    """Spears beaten on bronze shields — many hits, slightly spread."""
    y = np.zeros(int(1.6 * SR))
    for i in range(10):
        place(y, clang_one(rng.uniform(380, 700)) * rng.uniform(0.4, 1), rng.uniform(0, 0.25))
    return y * 0.5


def sfx_warcry():
    """Massed battle cry ("alala!") from hundreds of hoplites."""
    d = 1.8
    t = t_(d)
    y = np.zeros_like(t)
    for v in range(40):
        f0 = rng.uniform(110, 230)
        st = rng.uniform(0, 0.15)
        tt = np.clip(t - st, 0, None)
        f = f0 * (1 + 0.18 * np.sin(np.pi * np.minimum(tt / 1.4, 1))) * (1 + 0.02 * np.sin(2 * np.pi * 5.5 * tt + v))
        ph = 2 * np.pi * np.cumsum(f) / SR
        src = sum(np.sin(k * ph) / k for k in range(1, 18))
        env = np.minimum(1, tt / 0.08) * np.clip((1.5 - tt) / 0.4, 0, 1) * (t > st)
        y += src * env * rng.uniform(0.5, 1)
    # "ah" vowel formants
    y = bp(y, 600, 1300) * 1.2 + bp(y, 1000, 2600) * 0.5 + bp(y, 150, 500) * 0.4
    y += bp(rng.standard_normal(len(t)), 400, 3000) * 0.3 * np.clip((1.5 - t) / 0.4, 0, 1)
    for dl, g in [(0.09, 0.35), (0.21, 0.2)]:
        k = int(dl * SR)
        y[k:] += y[:-k] * g
    return np.tanh(y * 0.15) * 0.9


def sfx_march():
    """Massed footsteps + armour rattle, in step, getting louder (8.7 s)."""
    d = 8.7
    y = np.zeros(int(d * SR))
    step = 0.42
    i = 0
    while i * step < d - 0.3:
        at = i * step
        tt = t_(0.35)
        thud = lp(rng.standard_normal(len(tt)), 180) * np.exp(-tt * 14) * 3
        crunch = bp(rng.standard_normal(len(tt)), 700, 3500) * np.exp(-tt * 22) * 0.6
        rattle = sum(np.sin(2 * np.pi * rng.uniform(1800, 4200) * tt) * np.exp(-tt * 30) for _ in range(5)) * 0.06
        place(y, (thud + crunch + rattle) * (0.45 + 0.55 * at / d), at + rng.uniform(0, 0.02))
        i += 1
    return y


def sfx_whoosh():
    d = 0.5
    t = t_(d)
    n = rng.standard_normal(len(t))
    y = bp(n, 400, 4000) * np.sin(np.pi * t / d) ** 2
    pan = np.linspace(-1, 1, len(t))
    return np.stack([y * (1 - pan) / 2, y * (1 + pan) / 2], 1) * 1.6


def sfx_hit():
    d = 1.5
    t = t_(d)
    sub = chirp(110, 40, d) * np.exp(-t * 3)
    stab = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in [146.8, 174.6, 207.7]) / 3
    stab = lp(stab, 1800) * np.exp(-t * 4)
    zing = chirp(800, 2400, 0.25)
    zing = np.concatenate([zing * np.exp(-t_(0.25) * 8), np.zeros(len(t) - len(zing))])
    return np.tanh(sub * 1.4 + stab * 0.4 + zing * 0.25)


def sfx_heartbeat():
    d = 5.5
    y = np.zeros(int(d * SR))
    at, gap = 0.0, 0.75
    while at < d - 0.4:
        for k, g in [(0, 1), (0.2, 0.7)]:
            tt = t_(0.25)
            place(y, np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 18) * g, at + k)
        at += gap
        gap = max(0.42, gap * 0.92)
    return lp(y, 300) * 1.4


def sfx_rise():
    d = 2.4
    t = t_(d)
    return (chirp(300, 1500, d) * 0.3 + bp(rng.standard_normal(len(t)), 2000, 6000) * 0.1) * (t / d) ** 2


def sfx_gulp():
    d = 0.45
    t = t_(d)
    f = 260 * np.exp(-((t - 0.12) ** 2) / 0.002) + 120
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-((t - 0.13) ** 2) / 0.004)
    return lp(y, 900) * 1.2


SFX = {k[4:]: v for k, v in dict(globals()).items() if k.startswith("sfx_") and callable(v)}


# ---------------------------------------------------------------- MUSIC
# Original score. The melody instrument imitates an aulos (the Greek double
# reed pipe; Spartan phalanxes famously advanced in step to aulos players),
# in a Dorian-flavoured mode over a drone, with frame drums and low strings.
E3 = 164.81
MODE = [0, 2, 3, 5, 7, 8, 10]


def deg(d, root=E3):
    o, k = divmod(d, 7)
    return root * 2 ** ((MODE[k] + 12 * o) / 12)


def aulos(f, d, vol=1.0):
    t = t_(d)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.25)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    reed = np.sign(np.sin(ph)) * 0.5 + np.sin(2 * ph) * 0.3 + np.sin(3 * ph) * 0.2
    reed2 = np.sign(np.sin(ph * 1.003)) * 0.3  # the second pipe, slightly beating
    y = lp(reed + reed2, 2400) + bp(rng.standard_normal(len(t)), 1500, 4000) * 0.05
    return y * np.minimum(1, t / 0.03) * np.clip((d - t) / 0.06, 0, 1) * vol


def drum(d=0.5, f=90):
    t = t_(d)
    return (chirp(f * 1.5, f, d) * 1.1 + lp(rng.standard_normal(len(t)), 900) * 0.5) * np.exp(-t * 9)


def strings(d, freqs, vol):
    t = t_(d)
    y = np.zeros_like(t)
    for fr in freqs:
        for det in (0.997, 1.0, 1.003):
            ph = 2 * np.pi * fr * det * t
            y += 2 * ((ph / (2 * np.pi)) % 1) - 1
    y = lp(y, 1400) / (3 * len(freqs))
    return y * np.minimum(1, t / 0.8) * np.clip((d - t) / 0.5, 0, 1) * vol


def music():
    total = TL["durationSec"] + 0.5
    L = np.zeros((int(total * SR), 2))
    # tension intro: drone + soft drum taps
    place(L, strings(B["marchStart"] + 0.4, [E3 / 2, E3 * 0.75], 0.35), 0)
    for at in np.arange(0, B["warCry"], 0.84):
        place(L, drum(0.4, 80) * 0.35, at)
    place(L, drum(1.2, 55) * 1.0, B["warCry"])
    # march: tempo locked to the footsteps (0.42 s per step)
    step = 0.42
    s0 = B["marchStart"]
    n = int((total - s0) / step)
    melody = [0, 0, 3, 2, 3, 4, 3, 2, 0, 1, 2, 0, -1, 0, 4, 5, 4, 3, 2, 3, 4, 4, 5, 6, 7, 6, 5, 4]
    for i in range(n):
        at = s0 + i * step
        place(L, drum(0.45, 70) * (0.8 if i % 2 == 0 else 0.45), at)
        place(L, aulos(deg(melody[i % len(melody)], E3 * 2), step * 0.95, 0.32), at)
    place(L, strings(total - s0, [E3 / 2, E3 * 0.75, E3], 0.4), s0)
    # rising dread after the eyes widen
    t0 = B["eyesWiden"]
    place(L, strings(total - t0, [E3 * 2 ** (1 / 12), E3 * 2 ** (7 / 12) / 2], 0.3), t0)
    fade = np.ones(len(L))
    fe, fs = int(TL["durationSec"] * SR), int((TL["durationSec"] - 0.4) * SR)
    fade[fs:fe] = np.linspace(1, 0, fe - fs)
    fade[fe:] = 0
    L *= fade[:, None]
    L[:, 1] = np.roll(L[:, 1], int(0.01 * SR))
    for dl, g in [(0.12, 0.2), (0.29, 0.1)]:
        k = int(dl * SR)
        L[k:] += L[:-k] * g
    return np.tanh(L * 1.1) * 0.85


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SFX.items():
        write(f"sfx_{name}.wav", fn())
    write("music.wav", music())
    print("generated:", ", ".join(SFX), "+ music")
