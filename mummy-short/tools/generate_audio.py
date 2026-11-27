"""Procedurally synthesize all sound effects and the background music.

Everything here is generated from scratch with numpy (no samples, no
copyrighted material). Usage: python3 tools/generate_audio.py
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
    sub = s * np.exp(-t * 2.2)
    n = lp_fast(rng.standard_normal(len(t)), 900) * np.exp(-t * 6)
    hit = lp_fast(rng.standard_normal(len(t)), 4000) * np.exp(-t * 30)
    y = sub * 1.0 + n * 0.8 + hit * 0.5
    return np.tanh(y * 1.6)


def sfx_glow():
    d = 1.6
    t = t_(d)
    y = np.zeros_like(t)
    for k, f in enumerate([660, 990, 1320, 1760]):
        y += np.sin(2 * np.pi * f * t + 3 * np.sin(2 * np.pi * 5 * t)) / (k + 1)
    e = np.minimum(1, t / 0.5) * np.exp(-np.maximum(0, t - 0.6) * 3)
    s, _ = chirp(200, 1200, d)
    return (y * 0.35 + s * 0.25) * e


def sfx_sparkle():
    d = 1.4
    y = np.zeros(int(d * SR))
    for i in range(18):
        st = int(rng.uniform(0, d - 0.25) * SR)
        f = rng.uniform(2000, 6000)
        tt = t_(0.25)
        y[st:st + len(tt)] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 18) * rng.uniform(0.3, 1)
    return y * 0.5


def sfx_creak():
    d = 1.6
    t = t_(d)
    f = 70 + 40 * np.sin(2 * np.pi * 0.7 * t) + 25 * np.sin(2 * np.pi * 3.1 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
    y = bandpass(saw, 300, 3000)
    rumble = lp_fast(rng.standard_normal(len(t)), 200)
    e = np.minimum(1, t / 0.1) * np.clip((d - t) / 0.3, 0, 1)
    return (y * 0.7 + rumble * 0.6) * e


def sfx_grind():
    d = 1.6
    t = t_(d)
    n = rng.standard_normal(len(t))
    am = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 9 * t + 2 * np.sin(2 * np.pi * 1.3 * t)))
    y = bandpass(n, 80, 900) * am
    thud = np.sin(2 * np.pi * 50 * t) * np.exp(-np.maximum(0, t - 1.35) * 10) * (t > 1.35)
    e = np.minimum(1, t / 0.08) * np.clip((d - t) / 0.2, 0, 1)
    return (y * 1.4 + thud * 1.2) * e


def sfx_hiss():
    d = 2.0
    t = t_(d)
    y = hp_fast(rng.standard_normal(len(t)), 2500)
    e = np.minimum(1, t / 0.3) * np.clip((d - t) / 1.0, 0, 1)
    return y * e * 0.5


def sfx_zap():
    d = 0.35
    t = t_(d)
    sq = np.sign(np.sin(2 * np.pi * 120 * t)) * 0.4
    n = bandpass(rng.standard_normal(len(t)), 1500, 7000)
    gate = (np.sin(2 * np.pi * 37 * t) > -0.2)
    return (sq + n * 0.7) * gate * np.exp(-t * 8) * 0.8


def sfx_groan():
    d = 2.0
    t = t_(d)
    f0 = 85 + 15 * np.sin(2 * np.pi * 0.8 * t) - 15 * t / d
    ph = 2 * np.pi * np.cumsum(f0) / SR
    src = sum(np.sin(k * ph) / k for k in range(1, 30))
    # crude "ohhh" vowel formants
    y = bandpass(src, 250, 800) * 1.2 + bandpass(src, 800, 1200) * 0.5
    y += bandpass(rng.standard_normal(len(t)), 200, 1000) * 0.15
    e = np.minimum(1, t / 0.3) * np.clip((d - t) / 0.6, 0, 1)
    return np.tanh(y * 3) * e * 0.8


def sfx_boing():
    d = 0.8
    t = t_(d)
    f = 180 + 260 * np.exp(-t * 4) * (1 + 0.3 * np.sin(2 * np.pi * 14 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 3.5)


def sfx_slide():
    s, _ = chirp(500, 1800, 0.5)
    s2, _ = chirp(1800, 400, 0.5)
    y = np.concatenate([s, s2])
    t = t_(1.0)
    vib = 1 + 0.02 * np.sin(2 * np.pi * 6 * t)
    return y * np.sin(np.pi * t) ** 0.5 * 0.6 * vib


def sfx_scratch():
    d = 0.7
    t = t_(d)
    n = rng.standard_normal(len(t))
    f = 400 + 3000 * np.abs(np.sin(2 * np.pi * 2.2 * t))
    y = lowpass(n, f)
    s, _ = chirp(1500, 150, d)
    return (y * 1.8 + s * 0.4) * np.exp(-t * 2.5)


def sfx_pop():
    d = 0.25
    t = t_(d)
    s, _ = chirp(900, 300, d)
    return s * np.exp(-t * 22)


def sfx_steps():
    d = 2.8
    y = np.zeros(int(d * SR))
    for i in range(7):
        st = int((0.1 + i * 0.38) * SR)
        tt = t_(0.15)
        thump = np.sin(2 * np.pi * 110 * tt) * np.exp(-tt * 35)
        scuff = bandpass(rng.standard_normal(len(tt)), 800, 4000) * np.exp(-tt * 40) * 0.5
        y[st:st + len(tt)] += (thump + scuff) * (0.8 if i % 2 else 1)
    # cavernous echo
    for dl, g in [(0.18, 0.35), (0.37, 0.18)]:
        k = int(dl * SR)
        y[k:] += y[:-k] * g
    return y


def sfx_run():
    d = 6.2
    y = np.zeros(int(d * SR))
    i = 0
    tpos = 0.0
    while tpos < d - 0.1:
        st = int(tpos * SR)
        tt = t_(0.07)
        f = 900 if i % 2 else 700
        tap = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 70)
        y[st:st + len(tt)] += tap
        tpos += 0.105
        i += 1
    e = np.clip((d - t_(d)) / 0.3, 0, 1)
    return y * e * 0.7


SFX = {
    "whoosh": sfx_whoosh, "boom": sfx_boom, "glow": sfx_glow, "sparkle": sfx_sparkle,
    "creak": sfx_creak, "grind": sfx_grind, "hiss": sfx_hiss, "zap": sfx_zap,
    "groan": sfx_groan, "boing": sfx_boing, "slide": sfx_slide, "scratch": sfx_scratch,
    "pop": sfx_pop, "steps": sfx_steps, "run": sfx_run,
}

# --------------------------------------------------------------- MUSIC
# Original score in a Hijaz-flavoured mode (D Eb F# G A Bb C) — the classic
# "ancient Egypt" colour, written from scratch.
D3 = 146.83
HIJAZ = [0, 1, 4, 5, 7, 8, 10]


def note_hz(deg, octave=0, root=D3):
    o, d = divmod(deg, 7)
    return root * 2 ** ((HIJAZ[d] + 12 * (o + octave)) / 12)


def pluck(freq, d, bright=0.5):
    """Karplus-Strong oud-like pluck."""
    n = int(d * SR)
    p = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, p)
    buf = lp_fast(np.tile(buf, 4), 3000 + 6000 * bright)[:p]
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out


def kick(d=0.4):
    t = t_(d)
    s, _ = chirp(120, 40, d)
    return s * np.exp(-t * 9)


def tom(f=110, d=0.5):
    t = t_(d)
    s, _ = chirp(f * 1.4, f, d)
    return (s + lp_fast(rng.standard_normal(len(t)), 1500) * 0.3) * np.exp(-t * 8)


def shaker(d=0.08):
    t = t_(d)
    return hp_fast(rng.standard_normal(len(t)), 6000) * np.exp(-t * 50)


def clap(d=0.2):
    t = t_(d)
    return bandpass(rng.standard_normal(len(t)), 900, 4000) * np.exp(-t * 25)


def drone(d, f, vol=1.0):
    t = t_(d)
    y = np.zeros_like(t)
    for k, g in [(1, 1), (2, 0.5), (3, 0.25), (1.5, 0.35)]:
        y += np.sin(2 * np.pi * f * k * t + 0.4 * np.sin(2 * np.pi * 0.2 * k * t)) * g
    return y * vol


def place(buf, x, at):
    st = int(at * SR)
    if st >= len(buf):
        return
    x = x[: len(buf) - st]
    if x.ndim == 1 and buf.ndim == 2:
        x = np.stack([x, x], 1)
    buf[st:st + len(x)] += x


def music():
    total = TL["durationSec"] + 0.5
    L = np.zeros((int(total * SR), 2))
    sc = {s["id"]: s for s in TL["scenes"]}

    # 1) HOOK: dark drone + war-drum hits + riser
    s, e = sc["hook"]["start"], sc["hook"]["end"]
    dr = drone(e - s, D3 / 2, 0.25) * np.minimum(1, t_(e - s) / 0.05)
    place(L, dr, s)
    for at in [0.0, 0.8, 1.6, 2.2, 2.6, 3.4, 4.2, 4.5]:
        place(L, tom(80, 0.6) * 0.9, s + at)
    r, _ = chirp(200, 1600, 1.4)
    place(L, r * np.linspace(0, 0.25, len(r)), s + 3.5)

    # 2) TOMB: mysterious oud melody over drone, 96 bpm
    s, e = sc["tomb"]["start"], sc["tomb"]["end"]
    place(L, drone(e - s, D3 / 2, 0.18) * np.minimum(1, t_(e - s) / 0.5), s)
    beat = 60 / 96
    mel = [0, 1, 2, 1, 3, 2, 1, 0, 4, 3, 2, 1, 2, 1, 0, -1]
    for i, deg in enumerate(mel):
        at = s + 0.3 + i * beat * 0.5
        if at > e - 0.3:
            break
        place(L, pluck(note_hz(deg, 1), 0.9, 0.6) * 0.45, at)
    for i in range(int((e - s) / beat)):
        place(L, tom(140, 0.3) * (0.35 if i % 2 == 0 else 0.15), s + i * beat)
        place(L, shaker() * 0.1, s + i * beat + beat / 2)

    # 3) COFFIN: tension pulse — tremolo strings, accelerating
    s, e = sc["coffin"]["start"], sc["coffin"]["end"]
    t = t_(e - s)
    trem = 0.5 + 0.5 * np.sin(2 * np.pi * (6 + 4 * t / (e - s)) * t)
    y = (np.sin(2 * np.pi * note_hz(0, 0) * t) + np.sin(2 * np.pi * note_hz(1, 0) * t) * 0.7
         + np.sin(2 * np.pi * note_hz(4, 0) * t) * 0.5) * trem
    y *= np.linspace(0.08, 0.28, len(t))
    place(L, y, s)
    place(L, drone(e - s, D3 / 2, 0.2), s)
    for i in range(int((e - s) / 0.5)):
        place(L, kick() * 0.5, s + i * 0.5)

    # 4) AWAKE: horror stings + heartbeat
    s, e = sc["awake"]["start"], sc["awake"]["end"]
    place(L, drone(e - s, D3 / 4, 0.35), s)
    t = t_(e - s)
    cluster = sum(np.sin(2 * np.pi * D3 * 2 ** (k / 12) * t) for k in [0, 1, 2, 6]) * 0.05
    place(L, cluster * np.minimum(1, t / 2), s)
    hb = 0.0
    while hb < e - s - 0.4:
        place(L, kick(0.25) * 0.7, s + hb)
        place(L, kick(0.25) * 0.5, s + hb + 0.22)
        hb += 0.75 - 0.25 * hb / (e - s)
    place(L, sfx_boom() * 0.4, s + 3.2)

    # 5) CHASE: frantic 160 bpm comedy-adventure groove
    s, e = sc["chase"]["start"], sc["chase"]["end"]
    beat = 60 / 160
    n_beats = int((e - s) / beat)
    bass = [0, 0, 4, 3, 0, 0, 5, 4]
    lead = [7, 8, 7, 5, 4, 5, 4, 2, 1, 2, 4, 5, 4, 2, 1, 0]
    for i in range(n_beats):
        at = s + i * beat
        place(L, kick() * 0.75, at)
        if i % 2 == 1:
            place(L, clap() * 0.5, at)
        place(L, shaker() * 0.18, at + beat / 2)
        place(L, pluck(note_hz(bass[i % 8], -1), 0.4, 0.3) * 0.7, at)
        place(L, pluck(note_hz(bass[i % 8], -1), 0.3, 0.3) * 0.4, at + beat / 2)
        place(L, pluck(note_hz(lead[i % 16], 1), 0.35, 0.9) * 0.35, at)
        place(L, pluck(note_hz(lead[(i + 3) % 16], 1), 0.3, 0.9) * 0.22, at + beat / 2)
    place(L, drone(e - s, D3 / 2, 0.12), s)

    # 6) ENDING: hard stop, comedic "wah-wah", then upbeat outro
    s, e = sc["ending"]["start"], sc["ending"]["end"]
    for k, deg in enumerate([2, 1, 0, -1]):
        f = note_hz(deg, 0)
        d = 0.35 if k < 3 else 0.9
        t = t_(d)
        wah = sum(np.sin(2 * np.pi * f * h * t) / h for h in range(1, 8))
        wah = lowpass(wah, 400 + 1500 * (0.5 + 0.5 * np.sin(2 * np.pi * 3 * t - np.pi / 2)))
        if k == 3:
            wah *= 1 + 0.15 * np.sin(2 * np.pi * 6 * t)
        place(L, wah * env(len(t), 0.02, 0.15) * 0.35, s + 0.9 + k * 0.38)
    beat = 60 / 128
    st = s + 3.15
    major = [0, 4, 7, 12]
    i = 0
    while st + i * beat < e + 0.3:
        at = st + i * beat
        place(L, kick() * 0.6, at)
        if i % 2:
            place(L, clap() * 0.4, at)
        place(L, shaker() * 0.15, at + beat / 2)
        f = D3 * 2 ** (major[i % 4] / 12) * 2
        place(L, pluck(f, 0.4, 0.9) * 0.35, at)
        place(L, pluck(D3 / 2 * (1 if i % 4 < 2 else 1.335), 0.4, 0.3) * 0.5, at)
        i += 1
    fade = np.ones(len(L))
    fe = int((TL["durationSec"]) * SR)
    fs = int((TL["durationSec"] - 0.8) * SR)
    fade[fs:fe] = np.linspace(1, 0, fe - fs)
    fade[fe:] = 0
    L *= fade[:, None]

    # gentle stereo width + room
    L[:, 1] = np.roll(L[:, 1], int(0.012 * SR))
    for dl, g in [(0.09, 0.2), (0.21, 0.12)]:
        k = int(dl * SR)
        L[k:] += L[:-k] * g
    return np.tanh(L * 1.2) * 0.9


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SFX.items():
        write(f"sfx_{name}.wav", fn())
        print("sfx", name)
    write("music.wav", music())
    print("music done")
