"""Synthesize all SFX and music for "I Saved a Man Who Was Supposed to Die!".

Everything is generated from scratch with numpy — no samples, no existing music.
Usage: python3 tools/generate_audio.py
"""
import json
import os
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "audio")
SR = 44100
rng = np.random.default_rng(1793)
TL = json.load(open(os.path.join(ROOT, "src", "timeline.json")))
SC = {s["id"]: s for s in TL["scenes"]}


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


def noise(d):
    return rng.standard_normal(int(d * SR))


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


def env(d, a=0.01, r=0.1):
    t = t_(d)
    return np.minimum(1, t / a) * np.clip((d - t) / r, 0, 1)


def place(buf, x, at):
    st = int(at * SR)
    if st >= len(buf):
        return
    x = x[: len(buf) - st]
    if x.ndim == 1 and buf.ndim == 2:
        x = np.stack([x, x], 1)
    buf[st:st + len(x)] += x


def echo(y, taps=((0.11, 0.35), (0.24, 0.2), (0.4, 0.1))):
    y = np.concatenate([y, np.zeros(int(0.5 * SR))])
    for d, g in taps:
        k = int(d * SR)
        y[k:] += y[:-k] * g
    return y


# ------------------------------------------------------------------ SFX
def sfx_boom():
    d = 2.2
    t = t_(d)
    return np.tanh((chirp(80, 30, d) * np.exp(-t * 2) + lp(noise(d), 600) * np.exp(-t * 5) * 0.7) * 1.5)


def sfx_chains():
    y = np.zeros(int(1.6 * SR))
    for _ in range(26):
        tt = t_(0.12)
        f = rng.uniform(2200, 5200)
        place(y, (np.sin(2 * np.pi * f * tt) + np.sin(2 * np.pi * f * 1.37 * tt) * 0.5) * np.exp(-tt * 40) * rng.uniform(0.2, 0.8), rng.uniform(0, 1.3))
    return echo(y) * 0.6


def sfx_heartbeat():
    d = 2.8
    y = np.zeros(int(d * SR))
    at = 0.0
    while at < d - 0.4:
        for k, g in [(0, 1), (0.2, 0.7)]:
            tt = t_(0.25)
            place(y, np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 18) * g, at + k)
        at += 0.6
    return lp(y, 280) * 1.6


def sfx_ghost():
    """Shadows swelling on the walls: rising, breathy whoom."""
    d = 1.4
    t = t_(d)
    y = bp(noise(d), 200, 1500) * np.sin(np.pi * t / d) ** 2 + chirp(90, 180, d) * 0.3 * np.sin(np.pi * t / d)
    return y * 1.2


def sfx_zoom():
    d = 0.6
    t = t_(d)
    return (chirp(200, 2000, d) * 0.4 + bp(noise(d), 1000, 6000) * (t / d) * 0.6) * env(d, 0.01, 0.05)


def sfx_hit():
    d = 1.8
    t = t_(d)
    sub = chirp(100, 36, d) * np.exp(-t * 2.5)
    stab = lp(sum(np.sign(np.sin(2 * np.pi * f * t)) for f in [110, 130.8, 155.6]) / 3, 1600) * np.exp(-t * 2.5)
    return np.tanh(sub * 1.4 + stab * 0.5)


def sfx_gust():
    d = 1.5
    t = t_(d)
    return lp(noise(d), 700) * np.sin(np.pi * t / d) ** 2 * 1.2


def sfx_drips():
    d = 8.0
    y = np.zeros(int(d * SR))
    at = 0.3
    while at < d - 0.3:
        tt = t_(0.15)
        f = rng.uniform(900, 1600)
        place(y, np.sin(2 * np.pi * np.cumsum(f * (1 + 2 * np.exp(-tt * 40))) / SR) * np.exp(-tt * 30) * 0.5, at)
        at += rng.uniform(0.6, 1.4)
    return echo(y) * 0.8


def stone_step(g=1.0):
    tt = t_(0.18)
    return (np.sin(2 * np.pi * 95 * tt) * np.exp(-tt * 30) + bp(rng.standard_normal(len(tt)), 900, 4000) * np.exp(-tt * 45) * 0.6) * g


def sfx_steps():
    y = np.zeros(int(2.8 * SR))
    for i in range(6):
        place(y, stone_step(0.9 if i % 2 else 1), 0.1 + i * 0.42)
    return echo(y)


def sfx_tiptoe():
    y = np.zeros(int(2.4 * SR))
    for i in range(6):
        place(y, stone_step(0.35), 0.1 + i * 0.36)
    return echo(y)


def sfx_creak():
    d = 1.4
    t = t_(d)
    f = 60 + 30 * np.sin(2 * np.pi * 0.8 * t) + 20 * np.sin(2 * np.pi * 3.3 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
    return echo(bp(saw, 300, 2600) * env(d, 0.1, 0.3) * 0.8)


def sfx_squeak():
    y = np.zeros(int(0.6 * SR))
    for k in range(3):
        tt = t_(0.09)
        place(y, np.sin(2 * np.pi * np.cumsum(3000 + 1500 * np.sin(np.pi * tt / 0.09)) / SR) * np.sin(np.pi * tt / 0.09) * 0.4, k * 0.13)
    return y


def sfx_boing():
    d = 0.7
    t = t_(d)
    f = 180 + 240 * np.exp(-t * 4) * (1 + 0.3 * np.sin(2 * np.pi * 14 * t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4)


def sfx_rattle():
    """Prisoner shaking the iron bars."""
    y = np.zeros(int(1.0 * SR))
    for i in range(7):
        tt = t_(0.2)
        clank = sum(np.sin(2 * np.pi * f * tt) * np.exp(-tt * dd) for f, dd in [(340, 20), (720, 25), (1180, 30)])
        place(y, (clank * 0.4 + lp(rng.standard_normal(len(tt)), 900) * np.exp(-tt * 30)) * (1 - i * 0.08), i * 0.11)
    return echo(y) * 0.9


def sfx_bell():
    """Distant church bell at dawn."""
    d = 3.5
    y = np.zeros(int(d * SR))
    for hit in [0, 1.4]:
        st = int(hit * SR)
        tt = np.arange(len(y) - st) / SR
        y[st:] += sum(np.sin(2 * np.pi * 196 * r * tt) * g * np.exp(-tt * dc) for r, g, dc in [(0.5, 0.5, 0.8), (1, 1, 1.1), (1.19, 0.5, 1.5), (1.5, 0.35, 2), (2.0, 0.3, 2.5)])
    return lp(y, 2500) * 0.4


def sfx_jingle():
    y = np.zeros(int(0.9 * SR))
    for _ in range(10):
        tt = t_(0.2)
        f = rng.uniform(2500, 5500)
        place(y, np.sin(2 * np.pi * f * tt) * np.exp(-tt * 25) * rng.uniform(0.3, 0.9), rng.uniform(0, 0.5))
    return y * 0.5


def sfx_ding():
    d = 1.2
    t = t_(d)
    return (np.sin(2 * np.pi * 1760 * t) + 0.4 * np.sin(2 * np.pi * 3520 * t)) * np.exp(-t * 4) * 0.5


def sfx_click():
    d = 0.5
    t = t_(d)
    y = np.zeros_like(t)
    for at in [0.0, 0.18, 0.3]:
        k = int(at * SR)
        n = int(0.03 * SR)
        y[k:k + n] += bp(rng.standard_normal(n), 1500, 6000) * np.exp(-np.arange(n) / (n / 4))
    return y * 1.2


def sfx_clunk():
    d = 0.8
    t = t_(d)
    return echo((lp(noise(d), 500) * np.exp(-t * 20) * 2 + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 15) + np.sin(2 * np.pi * 900 * t) * np.exp(-t * 25) * 0.3))


def sfx_whoosh():
    d = 0.6
    t = t_(d)
    y = bp(noise(d), 400, 4500) * np.sin(np.pi * t / d) ** 2
    pan = np.linspace(-1, 1, len(t))
    return np.stack([y * (1 - pan) / 2, y * (1 + pan) / 2], 1) * 1.6


def sfx_run():
    y = np.zeros(int(2.0 * SR))
    for i in range(10):
        place(y, stone_step(1 - i * 0.09), i * 0.17)
    return echo(y)


def sfx_rooster():
    d = 1.4
    t = t_(d)
    f = np.interp(t, [0, 0.2, 0.5, 0.9, 1.4], [500, 900, 1000, 950, 600])
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = sum(np.sin(k * ph) / k for k in range(1, 8))
    return bp(y, 600, 3500) * env(d, 0.05, 0.3) * 0.5


def sfx_crowd():
    """Parisian crowd murmur (11 s)."""
    d = 11.0
    t = t_(d)
    y = np.zeros_like(t)
    for v in range(50):
        st = rng.uniform(0, d - 1.5)
        ln = rng.uniform(0.5, 1.4)
        m = (t >= st) & (t < st + ln)
        tt = t[m] - st
        f = rng.uniform(100, 260) * (1 + 0.15 * np.sin(2 * np.pi * rng.uniform(1, 3) * tt))
        ph = 2 * np.pi * np.cumsum(f) / SR
        y[m] += sum(np.sin(k * ph) / k for k in range(1, 10)) * np.sin(np.pi * tt / ln) * rng.uniform(0.3, 1)
    y = bp(y, 300, 1800) + bp(noise(d), 200, 1500) * 0.15
    return y * env(d, 0.5, 0.8) * 0.35


def sfx_paper():
    d = 0.7
    y = np.zeros(int(d * SR))
    for _ in range(50):
        st = int(rng.uniform(0, d - 0.02) * SR)
        n = int(0.008 * SR)
        y[st:st + n] += rng.standard_normal(n) * rng.uniform(0.2, 1)
    t = t_(d)
    return hp(y, 1500) * 0.8 + bp(noise(d), 1500, 5000) * 0.25 * np.sin(np.pi * t / d)


def sfx_sting():
    d = 2.0
    t = t_(d)
    cl = sum(np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 5 * t)) for f in [220, 233.1, 311.1, 466.2]) / 4
    return lp(cl, 2500) * np.minimum(1, t / 0.03) * np.exp(-t * 1.2) * 0.7 + chirp(70, 40, d) * np.exp(-t * 2) * 0.5


def sfx_drums():
    """Revolutionary military snare drums (march rhythm)."""
    d = 2.6
    y = np.zeros(int(d * SR))
    pattern = [0, 0.15, 0.3, 0.45, 0.6, 0.675, 0.75, 0.9, 1.05, 1.2, 1.275, 1.35, 1.5, 1.65, 1.8, 1.875, 1.95, 2.1, 2.25]
    for at in pattern:
        tt = t_(0.18)
        place(y, (bp(rng.standard_normal(len(tt)), 1500, 7000) * 0.7 + np.sin(2 * np.pi * 190 * tt) * 0.5) * np.exp(-tt * 22), at)
    return y


def sfx_boots():
    y = np.zeros(int(2.6 * SR))
    for i in range(10):
        tt = t_(0.2)
        place(y, (lp(rng.standard_normal(len(tt)), 300) * 2 + bp(rng.standard_normal(len(tt)), 1500, 5000) * 0.3) * np.exp(-tt * 25), i * 0.25)
    return y


def sfx_puff():
    d = 0.6
    t = t_(d)
    return bp(noise(d), 300, 2500) * np.exp(-t * 8) * 1.2


SFX = {k[4:]: v for k, v in dict(globals()).items() if k.startswith("sfx_") and callable(v)}

# ---------------------------------------------------------------- MUSIC
# Original score: harpsichord (18th-century colour) + low strings + drums.
A2 = 110.0


def semi(n, root=A2):
    return root * 2 ** (n / 12)


def harpsichord(f, d, vol=1.0):
    t = t_(d)
    y = np.zeros_like(t)
    for k in range(1, 12):
        y += np.sin(2 * np.pi * f * k * t) * (1 / k) * np.exp(-t * (2 + k * 0.9))
    y += np.sin(2 * np.pi * f * 2.003 * t) * 0.3 * np.exp(-t * 4)  # second 8' choir
    return y * np.minimum(1, t / 0.002) * vol * 0.5


def strings(d, notes, vol, a=0.8):
    t = t_(d)
    y = np.zeros_like(t)
    for n in notes:
        for det in (0.997, 1.0, 1.003):
            ph = 2 * np.pi * semi(n) * det * t
            y += 2 * ((ph / (2 * np.pi)) % 1) - 1
    return lp(y, 1300) / (3 * len(notes)) * env(d, a, 0.6) * vol


def drum(d=0.45, f=70):
    t = t_(d)
    return (chirp(f * 1.5, f, d) + lp(noise(d), 800) * 0.4) * np.exp(-t * 8)


def music():
    total = TL["durationSec"] + 0.5
    L = np.zeros((int(total * SR), 2))
    # A minor motif for the harpsichord
    motif = [12, 15, 19, 15, 12, 11, 12, 8, 7, 8, 11, 7]

    # HOOK: shock cluster + low drone
    s, e = SC["hook"]["start"], SC["hook"]["end"]
    place(L, strings(e - s, [0, 1, 7], 0.5, 0.05), s)
    place(L, drum(1.2, 45) * 0.9, 3.35)

    # PRISON: creeping harpsichord motif, slow pulse, drone
    s, e = SC["prison"]["start"], SC["prison"]["end"]
    place(L, strings(e - s, [-12, 0], 0.4, 1.0), s)
    for i, n in enumerate(motif * 2):
        at = s + 0.4 + i * 0.36
        if at > e - 0.3:
            break
        place(L, harpsichord(semi(n), 0.8, 0.5), at)
    for at in np.arange(s, e, 0.72):
        place(L, drum(0.3, 60) * 0.3, at)

    # PRISONER: emotional, sad strings (A minor → F → C → E)
    s, e = SC["prisoner"]["start"], SC["prisoner"]["end"]
    for i, ch in enumerate([[0, 3, 7], [-4, 0, 3], [-9, -5, -2], [-5, -1, 2]]):
        place(L, strings(2.4, [n + 12 for n in ch] + [ch[0]], 0.45), s + i * 2.25)
    for i, n in enumerate([24, 22, 20, 19, 20, 17, 19, 15]):
        place(L, harpsichord(semi(n), 1.0, 0.35), s + 0.5 + i * 1.05)

    # DECISION: ticking tension → release as the door opens
    s, e = SC["decision"]["start"], SC["decision"]["end"]
    place(L, strings(6.0, [0, 1], 0.4, 0.4), s)
    for i, at in enumerate(np.arange(s, s + 5.8, 0.3)):
        place(L, harpsichord(semi(12 if i % 2 == 0 else 13), 0.25, 0.25), at)
    place(L, strings(e - 27.9, [-12, -5, 0, 3], 0.55, 0.05), 27.9)
    for at in np.arange(29.5, e, 0.25):
        place(L, drum(0.25, 90) * 0.35, at)

    # REVEAL: morning (major, light) → horror at the poster
    s, e = SC["reveal"]["start"], SC["reveal"]["end"]
    for i, n in enumerate([12, 16, 19, 24, 19, 16, 12, 16, 19, 16]):
        place(L, harpsichord(semi(n), 0.6, 0.35), s + 0.3 + i * 0.4)
    place(L, strings(5.0, [0, 4, 7], 0.3), s)
    place(L, strings(e - 37.0, [0, 1, 6], 0.5, 0.3), 37.0)

    # CONSEQUENCE: urgent military drums + strings
    s, e = SC["consequence"]["start"], SC["consequence"]["end"]
    for i, at in enumerate(np.arange(s, e, 0.4)):
        place(L, drum(0.4, 55) * (0.8 if i % 2 == 0 else 0.4), at)
    for i, ch in enumerate([[0, 3, 7], [-2, 2, 5], [-4, 0, 3], [-5, -1, 2]]):
        place(L, strings(2.6, [n + 12 for n in ch], 0.45, 0.2), s + i * 2.5)
    for i, n in enumerate(motif):
        place(L, harpsichord(semi(n), 0.4, 0.35), s + 0.2 + i * 0.4)

    # TWIST: dark, sparse, fade to black
    s, e = SC["twist"]["start"], SC["twist"]["end"]
    place(L, strings(e - s + 0.3, [-12, -11, 0], 0.4, 1.0), s)
    for i, n in enumerate([12, 11, 8, 7]):
        place(L, harpsichord(semi(n), 1.4, 0.3), s + 0.3 + i * 1.2)

    fade = np.ones(len(L))
    fe = int(TL["durationSec"] * SR)
    fs = int((TL["durationSec"] - 1.2) * SR)
    fade[fs:fe] = np.linspace(1, 0, fe - fs)
    fade[fe:] = 0
    L *= fade[:, None]
    L[:, 1] = np.roll(L[:, 1], int(0.012 * SR))
    for dl, g in [(0.13, 0.22), (0.31, 0.12)]:
        k = int(dl * SR)
        L[k:] += L[:-k] * g
    return np.tanh(L * 1.1) * 0.85


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SFX.items():
        write(f"sfx_{name}.wav", fn())
    write("music.wav", music())
    print("generated:", ", ".join(SFX), "+ music")
