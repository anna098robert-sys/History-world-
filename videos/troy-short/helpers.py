"""Helpers shared with earlier episodes (camera, horse, fire, VHS rewind...)."""
import math, random
import cairo
from gfx import *

GOLD = (1, 0.84, 0.3)
GOLD_D = hexc("#b8892a")
GOLD_L = hexc("#ffe28a")

def cam(ctx, cx, cy, z=1.0, rot=0.0, shake=0.0, t=0.0):
    sx = shake * (math.sin(t * 47) + math.sin(t * 31)) * 0.5
    sy = shake * (math.cos(t * 53) + math.sin(t * 37)) * 0.5
    ctx.translate(W / 2 + sx, H / 2 + sy)
    ctx.rotate(rot)
    ctx.scale(z, z)
    ctx.translate(-cx, -cy)


def paper_bg(ctx, c=hexc("#f3e9d2")):
    bg_fill(ctx, c)
    for i in range(0, W, 60):
        line(ctx, i, 0, i, H, 1.5, (0.8, 0.72, 0.6), 0.45)
    for j in range(0, H, 60):
        line(ctx, 0, j, W, j, 1.5, (0.8, 0.72, 0.6), 0.45)


def cloud(ctx, x, y, s=1.0, c=WHITE, a=0.95):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for dx, dy, r in ((-80, 10, 50), (-20, -20, 70), (60, 0, 55), (110, 20, 38)):
        circle(ctx, dx, dy, r)
    ctx.rectangle(-130, 10, 270, 48)
    setc(ctx, c, a)
    ctx.fill()
    ctx.restore()


def snow(ctx, t, n=90, a=0.8, seed=2):
    rnd = random.Random(seed)
    for i in range(n):
        x = (rnd.random() * W * 1.2 + math.sin(t * 0.8 + i) * 40 + t * 30) % (W + 100) - 50
        y = (rnd.random() * H + t * (60 + rnd.random() * 60)) % (H + 40) - 20
        circle(ctx, x, y, 2 + rnd.random() * 3)
        setc(ctx, WHITE, a * (0.5 + 0.5 * rnd.random()))
        ctx.fill()


def warm_glow(ctx, x, y, r, a=0.35, c=(1, 0.8, 0.45)):
    g = cairo.RadialGradient(x, y, r * 0.1, x, y, r)
    g.add_color_stop_rgba(0, c[0], c[1], c[2], a)
    g.add_color_stop_rgba(1, c[0], c[1], c[2], 0)
    ctx.set_source(g)
    circle(ctx, x, y, r)
    ctx.fill()


def horse(ctx, x, y, s, t, ph=0.0, moving=True):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    w = math.sin(t * 9 + ph) if moving else 0
    for k, (lx, dx) in enumerate(((-55, 1), (-35, -1), (45, -1), (65, 1))):
        a = dx * w * 0.4
        line(ctx, lx, 30, lx + math.sin(a) * 70, 30 + math.cos(a) * 70, 10, INK)
    ellipse(ctx, 5, 10, 90, 42)
    fs(ctx, WHITE, lw=6)
    ctx.move_to(70, -10)
    ctx.line_to(100, -80)
    ctx.line_to(130, -70)
    ctx.line_to(95, 10)
    ctx.close_path()
    fs(ctx, WHITE, lw=6)
    ellipse(ctx, 128, -78, 32, 18)
    fs(ctx, WHITE, lw=6)
    circle(ctx, 125, -84, 4)
    fs(ctx, INK, lw=0)
    ctx.move_to(98, -86)
    ctx.curve_to(80, -70, 76, -40, 72, -20)
    setc(ctx, hexc("#c9c9c9"))
    ctx.set_line_width(10)
    ctx.stroke()
    # plume
    ctx.move_to(108, -96)
    ctx.curve_to(100, -140, 130, -150, 120, -170)
    setc(ctx, RED)
    ctx.set_line_width(10)
    ctx.stroke()
    ctx.move_to(-85, 0)
    ctx.curve_to(-120, 10, -120, 60, -110, 80)
    setc(ctx, hexc("#c9c9c9"))
    ctx.set_line_width(12)
    ctx.stroke()
    ctx.restore()


def fire(ctx, x, y, r, t):
    if r <= 1:
        return
    g = cairo.RadialGradient(x, y, r * 0.2, x, y, r * 3.2)
    g.add_color_stop_rgba(0, 1, 0.75, 0.3, 0.55)
    g.add_color_stop_rgba(1, 1, 0.5, 0.1, 0)
    ctx.set_source(g)
    circle(ctx, x, y, r * 3.2)
    ctx.fill()
    for k, (c, sc) in enumerate((((0.95, 0.3, 0.1), 1.0), ((1, 0.6, 0.15), 0.72), ((1, 0.92, 0.5), 0.42))):
        ctx.save()
        ctx.translate(x, y + r * 0.3)
        fl = 1 + 0.12 * math.sin(t * 17 + k * 2) + 0.08 * math.sin(t * 29 + k)
        ctx.scale(r * sc, r * sc * fl)
        ctx.move_to(0, -1.6 + 0.15 * math.sin(t * 11 + k))
        ctx.curve_to(0.55, -0.7, 0.85, -0.1, 0.6, 0.45)
        ctx.curve_to(0.4, 0.85, -0.4, 0.85, -0.6, 0.45)
        ctx.curve_to(-0.85, -0.1, -0.55, -0.7, 0, -1.6 + 0.15 * math.sin(t * 11 + k))
        ctx.restore()
        setc(ctx, c, 0.95)
        ctx.fill()


def smoke(ctx, x, y, t, s=1.0, night=False):
    for k in range(7):
        ph = (t * 0.35 + k / 7) % 1
        rr = (20 + ph * 70) * s
        circle(ctx, x + math.sin(ph * 5 + k) * 30 * s + ph * 80 * s, y - ph * 360 * s, rr)
        c = (0.55, 0.55, 0.58) if not night else (0.35, 0.33, 0.38)
        setc(ctx, c, 0.5 * (1 - ph))
        ctx.fill()


def torch(ctx, x, y, t, rot=0.0, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    line(ctx, 0, 0, 0, 110, 14, hexc("#6b4428"))
    ellipse(ctx, 0, -6, 20, 14)
    fs(ctx, hexc("#3a2a1a"), lw=4)
    ctx.restore()
    fire(ctx, x + math.sin(rot) * 20 * s, y - 40 * s, 32 * s, t)


def vhs(ctx, t, strength=1.0):
    rnd = random.Random(int(t * 30))
    for i in range(10):
        y = rnd.random() * H
        ctx.rectangle(0, y, W, 3 + rnd.random() * 12)
        setc(ctx, WHITE, 0.15 * strength)
        ctx.fill()
    for y in range(0, H, 6):
        ctx.rectangle(0, y, W, 2)
    setc(ctx, (0, 0, 0), 0.12 * strength)
    ctx.fill()


def rewind_icon(ctx, x, y, s, a=1.0):
    for k in range(2):
        poly(ctx, [(x - k * 60 * s, y), (x + 60 * s - k * 60 * s, y - 45 * s), (x + 60 * s - k * 60 * s, y + 45 * s)])
        setc(ctx, WHITE, a)
        ctx.fill()

