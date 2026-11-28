"""Synthesize every sound effect and the music for "I Accidentally Started a War!".

Everything is generated from scratch with numpy (no samples, no existing music).
Usage: python3 tools/generate_audio.py
"""
import json
import os
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "audio")
SR = 44100
rng = np.random.default_rng(404)
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


def noise(d):
    return rng.standard_normal(int(d * SR))


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


def env(d, a=0.01, r=0.1):
    t = t_(d)
    return np.minimum(1, t / a) * np.clip((d - t) / r, 0, 1)


# ------------------------------------------------------------------ SFX
def clang_one(f0):
    d = 1.0
    t = t_(d)
    y = sum(np.sin(2 * np.pi * f0 * r * t + rng.uniform(0, 6)) * g * np.exp(-t * dec)
            for r, g, dec in [(1, 1, 6), (1.47, 0.6, 7), (2.09, 0.5, 9), (2.76, 0.35, 12)])
    return y * 0.4 + bp(noise(d), 1500, 8000) * np.exp(-t * 40) * 0.6


def sfx_clang():
    y = np.zeros(int(1.3 * SR))
    for _ in range(4):
        place(y, clang_one(rng.uniform(420, 760)) * rng.uniform(0.5, 1), rng.uniform(0, 0.12))
    return y * 0.6


def crowd_shout(d, n=30, lo=110, hi=260):
    t = t_(d)
    y = np.zeros_like(t)
    for v in range(n):
        st = rng.uniform(0, d - 0.6)
        ln = rng.uniform(0.4, 1.2)
        m = (t >= st) & (t < st + ln)
        tt = t[m] - st
        f = rng.uniform(lo, hi) * (1 + 0.2 * np.sin(np.pi * tt / ln))
        ph = 2 * np.pi * np.cumsum(f) / SR
        y[m] += sum(np.sin(k * ph) / k for k in range(1, 14)) * np.sin(np.pi * tt / ln) ** 0.6
    return bp(y, 500, 1400) + bp(y, 1000, 2600) * 0.4


def sfx_battle():
    """Distant battle bed: shouts, clashes, rumble (10 s)."""
    d = 10.0
    t = t_(d)
    y = crowd_shout(d, 60) * 0.25 + lp(noise(d), 200) * 1.2
    for _ in range(40):
        place(y, clang_one(rng.uniform(400, 800)) * rng.uniform(0.1, 0.4), rng.uniform(0, d - 1))
    return y * env(d, 0.2, 0.6)


def sfx_boom():
    d = 2.0
    t = t_(d)
    return np.tanh((chirp(90, 30, d) * np.exp(-t * 2.5) + lp(noise(d), 900) * np.exp(-t * 6) * 0.8) * 1.6)


def sfx_whoosh():
    d = 0.5
    t = t_(d)
    y = bp(noise(d), 400, 4500) * np.sin(np.pi * t / d) ** 2
    pan = np.linspace(-1, 1, len(t))
    return np.stack([y * (1 - pan) / 2, y * (1 + pan) / 2], 1) * 1.6


def sfx_zoom():
    d = 0.9
    t = t_(d)
    return (chirp(200, 2200, d) * 0.4 + bp(noise(d), 1000, 6000) * (t / d) * 0.6) * env(d, 0.01, 0.05)


def sfx_rewind():
    """Tape-rewind warble into the flashback."""
    d = 0.8
    t = t_(d)
    f = 400 + 2600 * (t / d) ** 2 + 300 * np.sin(2 * np.pi * 23 * t)
    y = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.25 + bp(noise(d), 2000, 8000) * 0.3
    return y * env(d, 0.02, 0.08)


def sfx_chime():
    d = 1.6
    t = t_(d)
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 3) for f in [880, 1320, 1760]) * 0.25


def sfx_pop():
    d = 0.25
    t = t_(d)
    return chirp(900, 300, d) * np.exp(-t * 22)


def sfx_ding():
    d = 1.0
    t = t_(d)
    return (np.sin(2 * np.pi * 1568 * t) + 0.4 * np.sin(2 * np.pi * 3136 * t)) * np.exp(-t * 5) * 0.5


def sfx_dash():
    """Cartoon zip-off."""
    d = 0.6
    s = chirp(300, 1800, 0.25)
    y = np.concatenate([s, np.zeros(int(d * SR) - len(s))])
    return (y * 0.5 + sfx_whoosh()[:, 0][: len(y)] if len(sfx_whoosh()) >= len(y) else y) * 0.9


def sfx_run():
    d = 2.8
    y = np.zeros(int(d * SR))
    at = 0.0
    i = 0
    while at < d - 0.1:
        tt = t_(0.07)
        place(y, np.sin(2 * np.pi * (800 if i % 2 else 650) * tt) * np.exp(-tt * 60), at)
        at += 0.12
        i += 1
    return y * 0.7


def sfx_juggle():
    d = 0.35
    t = t_(d)
    return chirp(500, 1100, d) * np.sin(np.pi * t / d) * 0.4


def sfx_sharpen():
    """Blade on whetstone: shhhing."""
    d = 0.9
    t = t_(d)
    sweep = 2000 + 3000 * t / d
    y = np.zeros_like(t)
    seg = int(0.05 * SR)
    for i in range(0, len(t), seg):
        c = sweep[i]
        y[i:i + seg] = bp(rng.standard_normal(seg), c * 0.7, c * 1.3)
    ring = np.sin(2 * np.pi * 3400 * t) * 0.08
    return (y + ring) * np.sin(np.pi * t / d) ** 0.5 * 0.9


def sfx_murmur():
    d = 2.8
    return crowd_shout(d, 24, 100, 200) * 0.6 * env(d, 0.3, 0.4)


def sfx_slam():
    """Fist / scroll slammed on a wooden table."""
    d = 0.9
    t = t_(d)
    thud = lp(noise(d), 300) * np.exp(-t * 18) * 3
    knock = np.sin(2 * np.pi * 140 * t) * np.exp(-t * 20)
    rattle = sum(np.sin(2 * np.pi * rng.uniform(1500, 3500) * t) * np.exp(-t * rng.uniform(8, 14)) for _ in range(4)) * 0.08
    return np.tanh((thud + knock + rattle) * 1.4)


def sfx_shutter():
    d = 0.4
    t = t_(d)
    return (lp(noise(d), 600) * np.exp(-t * 25) * 2 + np.sin(2 * np.pi * 220 * t) * np.exp(-t * 30)) * 0.8


def sfx_steps():
    d = 1.6
    y = np.zeros(int(d * SR))
    for i in range(4):
        tt = t_(0.15)
        place(y, (np.sin(2 * np.pi * 120 * tt) + bp(rng.standard_normal(len(tt)), 900, 4000) * 0.4) * np.exp(-tt * 30), 0.1 + i * 0.35)
    k = int(0.15 * SR)
    y[k:] += y[:-k] * 0.3  # marble hall echo
    return y


def sfx_sting():
    """Ominous orchestral sting."""
    d = 1.8
    t = t_(d)
    chord = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in [110, 116.5, 164.8]) / 3
    return lp(chord, 1500) * np.exp(-t * 1.6) * 0.6 + chirp(60, 40, d) * np.exp(-t * 2) * 0.6


def sfx_crack():
    d = 0.3
    t = t_(d)
    return bp(noise(d), 1500, 7000) * np.exp(-t * 35) * 1.2


def sfx_unroll():
    d = 0.8
    t = t_(d)
    y = np.zeros_like(t)
    for _ in range(60):
        st = int(rng.uniform(0, d - 0.02) * SR)
        ln = int(0.006 * SR)
        y[st:st + ln] += rng.standard_normal(ln) * rng.uniform(0.2, 1)
    return hp(y, 1500) * 0.8 + bp(noise(d), 2000, 6000) * 0.1 * np.sin(np.pi * t / d)


def sfx_kettle():
    """Steam whistle as the king boils over."""
    d = 1.3
    t = t_(d)
    f = 1800 + 600 * np.minimum(1, t / 0.6)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3 + bp(noise(d), 3000, 8000) * 0.25
    return y * env(d, 0.2, 0.2)


def sfx_hit():
    d = 1.6
    t = t_(d)
    sub = chirp(110, 38, d) * np.exp(-t * 3)
    stab = lp(sum(np.sign(np.sin(2 * np.pi * f * t)) for f in [98, 123.5, 146.8]) / 3, 1800) * np.exp(-t * 3)
    return np.tanh(sub * 1.4 + stab * 0.5)


def sfx_gallop():
    """Horses galloping past (3-beat gait), panned left → right."""
    d = 2.6
    y = np.zeros(int(d * SR))
    at = 0.0
    while at < d - 0.3:
        for k in (0, 0.07, 0.14):
            tt = t_(0.12)
            place(y, (lp(rng.standard_normal(len(tt)), 400) * 2 + np.sin(2 * np.pi * 180 * tt)) * np.exp(-tt * 30), at + k)
        at += 0.36
    t = t_(d)
    g = np.sin(np.pi * t / d)
    pan = np.linspace(-1, 1, len(y))
    y = y * g
    return np.stack([y * (1 - pan) / 2, y * (1 + pan) / 2], 1) * 1.6


def sfx_heartbeat():
    d = 2.6
    y = np.zeros(int(d * SR))
    at = 0.0
    while at < d - 0.4:
        for k, g in [(0, 1), (0.2, 0.7)]:
            tt = t_(0.25)
            place(y, np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 18) * g, at + k)
        at += 0.55
    return lp(y, 300) * 1.5


def sfx_spears():
    """Ring of spears snapping toward him."""
    y = np.zeros(int(1.0 * SR))
    for i in range(6):
        tt = t_(0.3)
        place(y, (bp(rng.standard_normal(len(tt)), 2000, 7000) * np.exp(-tt * 25) + np.sin(2 * np.pi * 2600 * tt) * np.exp(-tt * 15) * 0.3), i * 0.07)
    return y * 0.8


def sfx_crickets():
    d = 2.2
    t = t_(d)
    gate = ((t * 3) % 1 < 0.25) * (np.sin(2 * np.pi * 40 * t) > 0)
    return np.sin(2 * np.pi * 4300 * t) * gate * 0.25 * env(d, 0.05, 0.3)


def sfx_whistle():
    """Innocent little whistle."""
    notes = [(1175, 0.22), (1568, 0.22), (1319, 0.22), (1047, 0.5)]
    y = np.concatenate([np.sin(2 * np.pi * np.cumsum(np.full(int(dd * SR), f) * (1 + 0.01 * np.sin(2 * np.pi * 6 * t_(dd)))) / SR) * env(dd, 0.02, 0.05) for f, dd in notes])
    return (y + bp(rng.standard_normal(len(y)), 1000, 3000) * 0.05) * 0.4


def sfx_dundun():
    """Dramatic 'dun dun DUN!' comedy sting."""
    y = np.zeros(int(2.2 * SR))
    for at, root, d in [(0, 146.8, 0.3), (0.34, 138.6, 0.3), (0.7, 110, 1.4)]:
        t = t_(d)
        ch = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in [root, root * 1.189, root * 1.498]) / 3
        hit = lp(ch, 2000) * np.exp(-t * (1.2 if d > 1 else 4)) * 0.6 + chirp(80, 40, d) * np.exp(-t * 3) * 0.6
        place(y, hit, at)
    return np.tanh(y * 1.3)


SFX = {k[4:]: v for k, v in dict(globals()).items() if k.startswith("sfx_") and callable(v)}

# ---------------------------------------------------------------- MUSIC
# Original score: Greek-flavoured lyre (plucked) + aulos-like reed, frame drums,
# strings. Each scene gets its own mood.
D3 = 146.83
MODE = [0, 1, 4, 5, 7, 8, 10]  # Phrygian-dominant colour


def deg(d, root=D3):
    o, k = divmod(d, 7)
    return root * 2 ** ((MODE[k] + 12 * o) / 12)


def lyre(f, d, bright=0.6):
    n = int(d * SR)
    p = max(2, int(SR / f))
    buf = lp(np.tile(rng.uniform(-1, 1, p), 4), 2500 + 5000 * bright)[:p]
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.995
    return out


def reed(f, d, vol=1.0):
    t = t_(d)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t / 0.2)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    y = lp(np.sign(np.sin(ph)) * 0.5 + np.sin(2 * ph) * 0.3, 2400)
    return y * env(d, 0.03, 0.06) * vol


def drum(d=0.45, f=80):
    t = t_(d)
    return (chirp(f * 1.5, f, d) + lp(noise(d), 900) * 0.4) * np.exp(-t * 9)


def strings(d, freqs, vol, a=0.6):
    t = t_(d)
    y = np.zeros_like(t)
    for fr in freqs:
        for det in (0.997, 1.0, 1.003):
            ph = 2 * np.pi * fr * det * t
            y += 2 * ((ph / (2 * np.pi)) % 1) - 1
    return lp(y, 1500) / (3 * len(freqs)) * env(d, a, 0.4) * vol


def music():
    total = TL["durationSec"] + 0.5
    L = np.zeros((int(total * SR), 2))

    # HOOK: epic battle drums + strings
    s, e = SC["hook"]["start"], SC["hook"]["end"]
    place(L, strings(e - s - 0.6, [D3 / 2, D3 * 0.75, D3], 0.5, 0.02), s)
    for i, at in enumerate(np.arange(s, e - 0.7, 0.3)):
        place(L, drum(0.4, 60) * (0.9 if i % 2 == 0 else 0.5), at)

    # MISSION: bright, bouncy lyre tune (a happy-go-lucky messenger)
    s, e = SC["mission"]["start"], SC["mission"]["end"]
    beat = 60 / 140
    tune = [7, 9, 11, 9, 7, 4, 7, 9, 11, 14, 11, 9, 7, 9, 7, 4]
    for i in range(int((e - s) / beat)):
        at = s + i * beat
        place(L, lyre(deg(tune[i % 16] - 7, D3 * 2) * 1.0, 0.5) * 0.45, at)
        place(L, lyre(D3 / 2 if i % 2 == 0 else D3 * 0.75, 0.5, 0.3) * 0.5, at)
        place(L, drum(0.2, 140) * 0.25, at + beat / 2)

    # TENSION: low drone, ticking drum, reed motif
    s, e = SC["tension"]["start"], SC["tension"]["end"]
    place(L, strings(e - s, [D3 / 2, D3 / 2 * 2 ** (1 / 12)], 0.45), s)
    for i, at in enumerate(np.arange(s, e, 0.5)):
        place(L, drum(0.3, 90) * (0.5 if i % 4 == 0 else 0.2), at)
    for i, d_ in enumerate([0, 1, 0, -1, 0, 1, 4, 1]):
        place(L, reed(deg(d_, D3 * 2), 0.9, 0.22), s + 1 + i * 0.9)

    # MISTAKE: suspense, then the king's rage
    s, e = SC["mistake"]["start"], SC["mistake"]["end"]
    place(L, strings(5.2, [D3, D3 * 2 ** (1 / 12)], 0.3), s)
    for at in np.arange(s, s + 5.2, 0.25):
        place(L, drum(0.08, 300) * 0.1, at)
    place(L, strings(e - 25.2, [D3 / 2, D3 * 0.6, D3 * 0.75], 0.6, 0.05), 25.2)
    for at in np.arange(27.6, e, 0.3):
        place(L, drum(0.4, 60) * 0.7, at)

    # CHAOS: full war groove
    s, e = SC["chaos"]["start"], SC["chaos"]["end"]
    beat = 60 / 150
    riff = [0, 0, 1, 0, 4, 3, 1, 0]
    for i in range(int((e - s) / beat)):
        at = s + i * beat
        place(L, drum(0.45, 55) * 0.85, at)
        place(L, drum(0.2, 160) * (0.5 if i % 2 else 0.2), at + beat / 2)
        place(L, reed(deg(riff[i % 8], D3 * 2), beat * 0.9, 0.22), at)
    place(L, strings(e - s, [D3 / 2, D3 * 0.75, D3], 0.45, 0.1), s)

    # EXPLAIN: nervous pizzicato-style lyre plinks
    s, e = SC["explain"]["start"], SC["explain"]["end"]
    for i, at in enumerate(np.arange(s, e - 2.5, 0.3)):
        place(L, lyre(deg([0, 4, 1, 4][i % 4], D3 * 2), 0.3, 0.7) * 0.3, at)
    place(L, strings(e - s, [D3 / 2], 0.25), s)

    # ENDING: innocent lyre, then everything stops for the sting
    s, e = SC["ending"]["start"], SC["ending"]["end"]
    for i, d_ in enumerate([7, 9, 7, 4, 7, 9, 11, 9]):
        place(L, lyre(deg(d_ - 7, D3 * 2), 0.6, 0.5) * 0.3, s + 0.3 + i * 0.5)
    place(L, strings(4.0, [D3 / 2, D3 * 0.75], 0.3), s)

    fade = np.ones(len(L))
    fe = int(TL["durationSec"] * SR)
    fs = int((TL["durationSec"] - 0.5) * SR)
    fade[fs:fe] = np.linspace(1, 0, fe - fs)
    fade[fe:] = 0
    L *= fade[:, None]
    L[:, 1] = np.roll(L[:, 1], int(0.01 * SR))
    for dl, g in [(0.11, 0.2), (0.27, 0.1)]:
        k = int(dl * SR)
        L[k:] += L[:-k] * g
    return np.tanh(L * 1.1) * 0.85


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SFX.items():
        write(f"sfx_{name}.wav", fn())
    write("music.wav", music())
    print("generated:", ", ".join(SFX), "+ music")
