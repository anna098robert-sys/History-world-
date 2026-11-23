"""Shots for 'I Accidentally Became a Pharaoh!'.
Each shot: fn(ctx, t, D, cue). cue(text) -> start time (s) of the sentence containing text."""
import math, random
import cairo
from gfx import *
from helpers import *

TIMELINE = {}          # filled by render.Renderer: id -> (shot, cue)

SAND = hexc("#f2cf7a")
SAND_D = hexc("#d9a94f")
SAND_L = hexc("#f8e2a6")
LIME = hexc("#fbf6e8")           # polished limestone casing
LIME_D = hexc("#e3d8bd")
STONE = hexc("#c9a46a")
NILE = hexc("#3d8fd1")
NILE_D = hexc("#2a6ea8")
LAPIS = hexc("#1f4fa8")
OCHRE = hexc("#c9803a")
FIELD = hexc("#6fbf4a")
FIELD_D = hexc("#4e9a36")
MUD = hexc("#4a3424")
SKY_T = hexc("#4fb3f0")
SKY_B = hexc("#cdeefc")
SKIN = hexc("#f2f0ea")


# ====================================================================== small helpers
def lerp2(p, q, u):
    return (lerp(p[0], q[0], u), lerp(p[1], q[1], u))


def polyline_part(ctx, pts, frac, lw, color, a=1.0):
    """stroke the first `frac` (0..1) of a polyline."""
    if frac <= 0 or len(pts) < 2:
        return
    seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    total = sum(seg)
    want = total * clamp(frac)
    ctx.move_to(*pts[0])
    acc = 0
    for i, L in enumerate(seg):
        if acc + L >= want:
            u = (want - acc) / max(L, 1e-6)
            ctx.line_to(*lerp2(pts[i], pts[i + 1], u))
            break
        ctx.line_to(*pts[i + 1])
        acc += L
    setc(ctx, color, a)
    ctx.set_line_width(lw)
    ctx.stroke()


def point_on(pts, frac):
    seg = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    want = sum(seg) * clamp(frac)
    acc = 0
    for i, L in enumerate(seg):
        if acc + L >= want:
            u = (want - acc) / max(L, 1e-6)
            p = lerp2(pts[i], pts[i + 1], u)
            ang = math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0])
            return p[0], p[1], ang
        acc += L
    return pts[-1][0], pts[-1][1], 0.0


def caption(ctx, place, year, t, dur=4.0):
    if t < 0 or t > dur + 0.6:
        return
    k = ease_out(prog(t, 0, 0.5)) - ease_in(prog(t, dur, dur + 0.5))
    x = lerp(-900, 70, k)
    rrect(ctx, x, 850, 760, 150, 18)
    fs(ctx, (0.1, 0.07, 0.05, 0.82), lw=0)
    ctx.rectangle(x, 850, 14, 150)
    setc(ctx, GOLD)
    ctx.fill()
    text(ctx, place, x + 40, 898, 46, WHITE, align="left", outline=0, shadow=False)
    text(ctx, year, x + 40, 958, 52, GOLD, align="left", outline=0, shadow=False)


def bc_counter(ctx, t, D, y0=2026, y1=-2500):
    k = ease(prog(t, 0.3, D - 0.4))
    y = int(round(lerp(y0, y1, k)))
    lab = f"{y} AD" if y > 0 else f"{-y} BC"
    rrect(ctx, W / 2 - 260, 60, 520, 130, 30)
    fs(ctx, (0.05, 0.03, 0.1, 0.75), lw=5, stroke=GOLD)
    text(ctx, lab, W / 2, 125, 90, GOLD, outline=0, shadow=False)


def confetti(ctx, t, n=60, seed=3, a=1.0):
    rnd = random.Random(seed)
    cols = [GOLD, LAPIS, RED, hexc("#2bb36b"), hexc("#ff8ad8"), WHITE]
    for i in range(n):
        x = (rnd.random() * W + math.sin(t * 2 + i) * 40) % W
        y = (rnd.random() * H + t * (180 + rnd.random() * 120)) % (H + 40) - 20
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(t * 4 + i)
        ctx.rectangle(-8, -4, 16, 8)
        setc(ctx, cols[i % len(cols)], a)
        ctx.fill()
        ctx.restore()


# ====================================================================== hieroglyphs
def glyph(ctx, kind, x, y, s=1.0, c=INK):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    setc(ctx, c)
    ctx.set_line_width(5)
    if kind == "bird":
        ctx.move_to(-20, 10); ctx.curve_to(-10, -18, 18, -18, 22, -4); ctx.line_to(30, -8); ctx.line_to(24, 2)
        ctx.curve_to(16, 14, -10, 16, -20, 10); ctx.close_path(); ctx.fill()
        line(ctx, -2, 12, -6, 26, 4, c); line(ctx, 6, 12, 6, 26, 4, c)
    elif kind == "eye":
        ctx.move_to(-26, 0); ctx.curve_to(-10, -16, 10, -16, 26, 0); ctx.curve_to(10, 12, -10, 12, -26, 0); ctx.stroke()
        circle(ctx, 0, -1, 6); ctx.fill()
        ctx.move_to(-4, 8); ctx.curve_to(-6, 20, -14, 24, -20, 18); ctx.stroke()
    elif kind == "ankh":
        ellipse(ctx, 0, -16, 9, 12); ctx.stroke()
        line(ctx, -16, -2, 16, -2, 5, c); line(ctx, 0, -4, 0, 26, 5, c)
    elif kind == "water":
        ctx.move_to(-24, 0)
        for k in range(6):
            ctx.line_to(-24 + k * 8 + 4, -6 if k % 2 == 0 else 6)
        ctx.line_to(24, 0); ctx.stroke()
    elif kind == "snake":
        ctx.move_to(-24, 14); ctx.curve_to(-10, -4, 0, 24, 12, 4); ctx.curve_to(18, -6, 20, -14, 26, -14); ctx.stroke()
        circle(ctx, 26, -14, 5); ctx.fill()
    elif kind == "dog":   # Anubis head
        ctx.move_to(-14, 24); ctx.line_to(-14, -2); ctx.line_to(-8, -26); ctx.line_to(-2, -6); ctx.line_to(22, 2)
        ctx.line_to(20, 8); ctx.line_to(-2, 10); ctx.line_to(2, 24); ctx.close_path(); ctx.fill()
    elif kind == "sun":
        circle(ctx, 0, 0, 14); ctx.stroke(); circle(ctx, 0, 0, 4); ctx.fill()
    elif kind == "cap":
        ctx.restore()
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s * 0.17, s * 0.17)
        draw_cap(ctx, c if c != INK else RED)
    ctx.restore()


def glyph_column(ctx, x, y0, n, s, c, seed=1, kinds=("bird", "eye", "ankh", "water", "snake", "sun", "dog")):
    rnd = random.Random(seed)
    for i in range(n):
        glyph(ctx, kinds[rnd.randrange(len(kinds))], x, y0 + i * 64 * s, s, c)


# ====================================================================== props
def golden_box(ctx, x, y, s, t, glow=0.0, pressed=0.0, buzz=0.0):
    ctx.save()
    ctx.translate(x + math.sin(t * 60) * 4 * buzz, y)
    ctx.scale(s, s)
    if glow > 0:
        warm_glow(ctx, 0, -20, 420, 0.6 * glow, (1, 0.85, 0.4))
    # body
    rrect(ctx, -160, -60, 320, 150, 14)
    g = cairo.LinearGradient(0, -60, 0, 90)
    g.add_color_stop_rgb(0, *GOLD_L)
    g.add_color_stop_rgb(1, *GOLD_D)
    ctx.set_source(g)
    ctx.fill_preserve()
    setc(ctx, INK)
    ctx.set_line_width(7)
    ctx.stroke()
    # lid
    poly(ctx, [(-175, -60), (-140, -110), (140, -110), (175, -60)])
    g = cairo.LinearGradient(0, -110, 0, -60)
    g.add_color_stop_rgb(0, *GOLD_L)
    g.add_color_stop_rgb(1, *GOLD)
    ctx.set_source(g)
    ctx.fill_preserve()
    setc(ctx, INK)
    ctx.set_line_width(7)
    ctx.stroke()
    for i, k in enumerate(("bird", "eye", "snake", "dog", "ankh", "water")):
        glyph(ctx, k, -120 + (i % 3) * 50 + (150 if i >= 3 else 0), 10 + (i % 2) * 40, 0.75, hexc("#6a4a10"))
    # red button
    ellipse(ctx, 0, -110, 46, 16)
    fs(ctx, hexc("#7a0a10"), lw=5)
    ctx.save()
    ctx.translate(0, -118 + 10 * pressed)
    ellipse(ctx, 0, 0, 38, 14)
    ctx.rectangle(-38, 0, 76, 12 * (1 - pressed))
    setc(ctx, RED)
    ctx.fill()
    ellipse(ctx, 0, 0, 38, 14)
    fs(ctx, hexc("#ff4a4a"), lw=5)
    ellipse(ctx, -12, -4, 12, 4)
    setc(ctx, WHITE, 0.7)
    ctx.fill()
    ctx.restore()
    if glow > 0.2:
        warm_glow(ctx, 0, -118, 90, 0.7 * glow, (1, 0.2, 0.2))
    ctx.restore()


def pizza_box(ctx, x, y, s=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    poly(ctx, [(-110, 0), (110, 0), (130, -30), (-90, -30)])
    fs(ctx, hexc("#d9b07a"), lw=6)
    ctx.rectangle(-110, 0, 220, 26)
    fs(ctx, hexc("#c99a5e"), lw=6)
    text(ctx, "PIZZA", 10, -15, 26, RED, outline=0, shadow=False)
    ctx.restore()


def pyramid_pts(x, base, w, h):
    return (x, base - h), (x - w / 2, base), (x + w / 2, base)


def pyramid(ctx, x, base, w, h, cased=True, built=1.0, sparkle_t=None):
    apex, lb, rb = pyramid_pts(x, base, w, h)
    top = base - h * built
    if cased:
        # sunlit right face, shaded left face, golden capstone
        poly(ctx, [lerp2(lb, apex, built), lb, (x, base), (x, top)] if built < 1 else [apex, lb, (x, base)])
        fs(ctx, LIME_D, lw=6)
        poly(ctx, [(x, top), (x, base), rb, lerp2(rb, apex, built)] if built < 1 else [apex, (x, base), rb])
        fs(ctx, LIME, lw=6)
        if built >= 1:
            cap = 0.09
            poly(ctx, [apex, lerp2(apex, lb, cap), (x, apex[1] + h * cap)])
            fs(ctx, GOLD_D, lw=5)
            poly(ctx, [apex, (x, apex[1] + h * cap), lerp2(apex, rb, cap)])
            fs(ctx, GOLD, lw=5)
        if sparkle_t is not None:
            sparkle(ctx, x + w * 0.12, base - h * 0.7, 26 * w / 600, sparkle_t)
            sparkle(ctx, x + w * 0.25, base - h * 0.35, 20 * w / 600, sparkle_t + 1.3)
    else:
        n = 9
        for i in range(n):
            y0 = base - h * i / n
            y1 = base - h * (i + 1) / n
            hw0 = w / 2 * (1 - i / n)
            ctx.rectangle(x - hw0, y1, hw0 * 2, y0 - y1)
            fs(ctx, [STONE, hexc("#b8925a")][i % 2], lw=4)


def slide_path(x, base, w, h, n=60):
    """a wiggly slide down the right face of a pyramid, ending in a ramp lip."""
    apex, lb, rb = pyramid_pts(x, base, w, h)
    pts = []
    for i in range(n + 1):
        u = i / n
        px, py = lerp2((apex[0] + 10, apex[1] + 20), (rb[0] - 30, rb[1] - 12), u)
        off = math.sin(u * math.pi * 3) * 40 * (1 - u * 0.5)
        pts.append((px + off * 0.5, py - abs(off) * 0.4 - 8))
    end = pts[-1]
    pts += [(end[0] + 120, end[1] + 4), (end[0] + 260, end[1] - 10), (end[0] + 330, end[1] - 60)]
    return pts


def draw_slide(ctx, pts, frac=1.0, t=0.0):
    if frac <= 0:
        return
    polyline_part(ctx, pts, frac, 46, INK)
    polyline_part(ctx, pts, frac, 36, hexc("#ff9a2e"))
    polyline_part(ctx, pts, frac, 12, hexc("#ffd36a"))
    # supports
    for i in range(4, int(len(pts) * frac) - 1, 6):
        px, py = pts[i]
        line(ctx, px, py + 16, px + 8, py + 60, 6, hexc("#8a5a2b"))


def chariot(ctx, x, y, s, t, moving=True, rider=None, driver=True):
    """two-horse chariot facing right; (x, y) = ground under the wheel."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    horse(ctx, 330, -120, 1.0, t * (1.6 if moving else 0), ph=0, moving=moving)
    horse(ctx, 300, -105, 1.05, t * (1.6 if moving else 0), ph=1.5, moving=moving)
    line(ctx, 60, -120, 240, -110, 9, hexc("#8a5a2b"))
    if driver:
        doodle(ctx, 10, -330, 0.32, hair=wig_black, cap=False, body=hexc("#f2e6c8"), face=0.9,
               expr="shock" if moving else "flat", larm=(0.3, 0.2), rarm=(-1.6, 0.3), show_legs=False,
               blink=doodle_auto_blink(t, 9))
    if rider:
        rider(ctx)
    # car
    ctx.move_to(-110, -210)
    ctx.line_to(80, -210)
    ctx.curve_to(110, -150, 90, -100, 60, -90)
    ctx.line_to(-110, -90)
    ctx.close_path()
    fs(ctx, GOLD, lw=7)
    for k in range(3):
        glyph(ctx, ["sun", "eye", "ankh"][k], -70 + k * 50, -150, 0.7, hexc("#6a4a10"))
    # wheel
    ctx.save()
    ctx.translate(-20, -70)
    circle(ctx, 0, 0, 70)
    fs(ctx, hexc("#8a5a2b"), lw=7)
    circle(ctx, 0, 0, 54)
    fs(ctx, None, lw=4)
    rot = t * 10 if moving else 0
    for k in range(6):
        a = rot + k * math.pi / 3
        line(ctx, 0, 0, math.cos(a) * 54, math.sin(a) * 54, 6, hexc("#5a3a1a"))
    circle(ctx, 0, 0, 12)
    fs(ctx, GOLD, lw=4)
    ctx.restore()
    ctx.restore()


def crook(ctx, x, y, s=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ctx.move_to(0, 90)
    ctx.line_to(0, -60)
    ctx.curve_to(0, -100, 40, -100, 40, -70)
    setc(ctx, INK)
    ctx.set_line_width(16)
    ctx.stroke_preserve()
    ctx.set_line_width(10)
    ctx.set_dash([12, 10])
    setc(ctx, GOLD)
    ctx.stroke_preserve()
    ctx.set_dash([12, 10], 11)
    setc(ctx, LAPIS)
    ctx.stroke()
    ctx.restore()


def flail(ctx, x, y, s=1.0, rot=0.0, t=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    line(ctx, 0, 90, 0, -60, 14, INK)
    line(ctx, 0, 88, 0, -58, 8, GOLD)
    for k in range(3):
        sw = math.sin(t * 5 + k) * 0.15
        line(ctx, 0, -60, -40 + k * 20 + sw * 40, -20 + sw * 10, 7, LAPIS)
    ctx.restore()


def grapes(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for r, row in enumerate((3, 2, 1)):
        for k in range(row):
            circle(ctx, (k - (row - 1) / 2) * 22, r * 20, 12)
            fs(ctx, hexc("#8a3ab8"), lw=3)
    line(ctx, 0, -12, 4, -28, 4, hexc("#5a3a1a"))
    ctx.restore()


def honey_cake(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ellipse(ctx, 0, 0, 34, 14)
    fs(ctx, hexc("#d98a3a"), lw=4)
    ellipse(ctx, 0, -6, 28, 9)
    fs(ctx, hexc("#ffc14a"), lw=3)
    ctx.restore()


def cat(ctx, x, y, s, t, look=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(40, 20)
    ctx.curve_to(90, 10 + math.sin(t * 3) * 10, 100, -40, 80, -60)
    setc(ctx, INK)
    ctx.set_line_width(10)
    ctx.stroke()
    ellipse(ctx, 0, 0, 60, 40)
    fs(ctx, hexc("#d9a24a"), lw=6)
    circle(ctx, -40, -40, 34)
    fs(ctx, hexc("#d9a24a"), lw=6)
    for sx in (-1, 1):
        poly(ctx, [(-40 + sx * 12, -66), (-40 + sx * 32, -88), (-40 + sx * 30, -54)])
        fs(ctx, hexc("#d9a24a"), lw=5)
    for sx in (-1, 1):
        ellipse(ctx, -40 + sx * 12 + look * 6, -44, 4, 7)
        fs(ctx, INK, lw=0)
    ctx.move_to(-46, -28)
    ctx.curve_to(-43, -24, -37, -24, -34, -28)
    setc(ctx, INK)
    ctx.set_line_width(3)
    ctx.stroke()
    line(ctx, -72, -14, -50, -14, 3, GOLD)
    ellipse(ctx, -40, -10, 30, 8)
    fs(ctx, GOLD, lw=3)
    circle(ctx, -40, -2, 6)
    fs(ctx, LAPIS, lw=2)
    ctx.restore()


def feather_fan(ctx, x, y, s, rot):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    line(ctx, 0, 0, 0, -260, 9, hexc("#8a5a2b"))
    for k in range(7):
        a = -0.9 + k * 0.3
        ctx.save()
        ctx.translate(0, -260)
        ctx.rotate(a)
        ellipse(ctx, 0, -60, 20, 60)
        fs(ctx, [WHITE, hexc("#f2e6c8")][k % 2], lw=4)
        ctx.restore()
    ctx.restore()


def shaduf(ctx, x, y, s, t, phase=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    line(ctx, -40, 0, -10, -260, 12, hexc("#8a5a2b"))
    line(ctx, 40, 0, 10, -260, 12, hexc("#8a5a2b"))
    a = 0.45 * math.sin(t * 2 + phase)
    ctx.save()
    ctx.translate(0, -255)
    ctx.rotate(a)
    line(ctx, -260, 0, 160, 0, 12, hexc("#6b4428"))
    circle(ctx, 160, 0, 36)
    fs(ctx, hexc("#7a6a5a"), lw=6)
    line(ctx, -260, 0, -260, 140, 4, INK)
    ctx.restore()
    bx = -260 * math.cos(a)
    by = -255 - 260 * math.sin(a) + 160
    ellipse(ctx, bx, by, 28, 22)
    fs(ctx, hexc("#a0703a"), lw=5)
    ctx.restore()


def mud_house(ctx, x, y, s):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rectangle(-90, -130, 180, 130)
    fs(ctx, hexc("#c9925a"), lw=6)
    ctx.rectangle(-100, -142, 200, 16)
    fs(ctx, hexc("#a8763f"), lw=5)
    rrect(ctx, -22, -80, 44, 80, 8)
    fs(ctx, hexc("#5a3a1a"), lw=4)
    ctx.rectangle(40, -110, 26, 26)
    fs(ctx, hexc("#5a3a1a"), lw=4)
    ctx.restore()


def palm(ctx, x, y, h, t=0.0):
    ctx.move_to(x, y)
    ctx.curve_to(x + 10, y - h * 0.4, x - 10, y - h * 0.7, x + 6, y - h)
    setc(ctx, hexc("#8a5a2b"))
    ctx.set_line_width(16)
    ctx.stroke()
    for k in range(6):
        a = -math.pi / 2 + (k - 2.5) * 0.55 + math.sin(t + k) * 0.05
        ctx.move_to(x + 6, y - h)
        ctx.curve_to(x + 6 + math.cos(a) * h * 0.25, y - h + math.sin(a) * h * 0.25 - 20,
                     x + 6 + math.cos(a) * h * 0.4, y - h + math.sin(a) * h * 0.4,
                     x + 6 + math.cos(a) * h * 0.45, y - h + math.sin(a) * h * 0.45 + 30)
        setc(ctx, hexc("#3e8a3a"))
        ctx.set_line_width(18)
        ctx.stroke()


def market_stall(ctx, x, y, s, c):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for sx in (-110, 110):
        line(ctx, sx, 0, sx, -200, 8, hexc("#8a5a2b"))
    poly(ctx, [(-140, -200), (140, -200), (120, -250), (-120, -250)])
    fs(ctx, c, lw=6)
    ctx.rectangle(-120, -70, 240, 70)
    fs(ctx, hexc("#b8864a"), lw=6)
    for k in range(5):
        circle(ctx, -90 + k * 45, -84, 18)
        fs(ctx, [hexc("#ff9a2e"), hexc("#8a3ab8"), hexc("#e8d040"), RED, hexc("#6fbf4a")][k], lw=3)
    ctx.restore()


def camel(ctx, x, y, s, t):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for lx in (-50, -20, 40, 70):
        line(ctx, lx, 0, lx + math.sin(t * 3 + lx) * 6, 110, 10)
    ctx.move_to(-80, 0)
    ctx.curve_to(-80, -80, -30, -110, -10, -60)
    ctx.curve_to(10, -110, 70, -100, 90, 0)
    ctx.close_path()
    fs(ctx, hexc("#d9a24a"), lw=6)
    ctx.move_to(-80, -10)
    ctx.curve_to(-120, -30, -120, -110, -140, -120)
    setc(ctx, INK)
    ctx.set_line_width(26)
    ctx.stroke_preserve()
    setc(ctx, hexc("#d9a24a"))
    ctx.set_line_width(18)
    ctx.stroke()
    ellipse(ctx, -150, -122, 30, 18)
    fs(ctx, hexc("#d9a24a"), lw=6)
    circle(ctx, -156, -128, 4)
    fs(ctx, INK, lw=0)
    ctx.restore()


# ====================================================================== characters
def wig_black(c):
    c.move_to(-112, 60)
    c.curve_to(-130, -150, 130, -150, 112, 60)
    c.line_to(80, 60)
    c.curve_to(90, -20, 60, -60, 0, -60)
    c.curve_to(-60, -60, -90, -20, -80, 60)
    c.close_path()
    fs(c, hexc("#1a1a22"), lw=LW)
    c.move_to(-90, -40)
    c.curve_to(-40, -80, 40, -80, 90, -40)
    setc(c, GOLD)
    c.set_line_width(10)
    c.stroke()


def nemes(stripe1=GOLD, stripe2=LAPIS, uraeus=True, crown=None):
    def f(c):
        # side lappets
        for sx in (-1, 1):
            poly(c, [(sx * 96, -20), (sx * 120, 40), (sx * 110, 170), (sx * 70, 170), (sx * 78, 40)])
            fs(c, stripe1, lw=LW)
            for k in range(4):
                line(c, sx * 76, 50 + k * 30, sx * 116, 50 + k * 30, 9, stripe2)
        # head cloth
        c.move_to(-112, 10)
        c.curve_to(-126, -150, 126, -150, 112, 10)
        c.curve_to(70, -50, -70, -50, -112, 10)
        fs(c, stripe1, lw=LW)
        for k in range(5):
            a0 = math.pi + 0.35 + k * 0.6
            line(c, math.cos(a0) * 70, math.sin(a0) * 60 - 40, math.cos(a0) * 112, math.sin(a0) * 104 - 20, 9, stripe2)
        c.move_to(-104, -14)
        c.curve_to(-60, -56, 60, -56, 104, -14)
        setc(c, stripe2)
        c.set_line_width(12)
        c.stroke()
        if uraeus:
            c.move_to(0, -48)
            c.curve_to(-10, -70, 10, -86, 0, -100)
            setc(c, GOLD)
            c.set_line_width(12)
            c.stroke()
            ellipse(c, 0, -104, 12, 10)
            fs(c, GOLD, lw=3)
        if crown:
            crown(c)
    return f


def beard(fx=0.0):
    def f(c):
        mx = 8 + fx * 34
        rrect(c, mx - 12, 52, 24, 70, 8)
        fs(c, hexc("#2a3a7a"), lw=5)
        for k in range(3):
            line(c, mx - 12, 76 + k * 18, mx + 12, 76 + k * 18, 4, GOLD)
    return f


def combo(*fs_):
    def f(c):
        for g in fs_:
            g(c)
    return f


def gold_collar(c, part, *a):
    if part == "body":
        c.move_to(-58, 80)
        c.curve_to(-70, 160, 70, 160, 58, 80)
        c.close_path()
        fs(c, GOLD, lw=5)
        c.move_to(-48, 96)
        c.curve_to(-54, 140, 54, 140, 48, 96)
        setc(c, LAPIS)
        c.set_line_width(9)
        c.stroke()
        c.move_to(-40, 106)
        c.curve_to(-44, 130, 44, 130, 40, 106)
        setc(c, hexc("#2bb3a0"))
        c.set_line_width(7)
        c.stroke()


def kilt(c, part, *a):
    if part == "body":
        line(c, -62, 230, 62, 230, 10, GOLD)
        poly(c, [(-20, 232), (20, 232), (14, 320), (-14, 320)])
        fs(c, GOLD, lw=4)


def leopard(c, part, *a):
    if part == "body":
        c.move_to(-50, 80)
        c.line_to(60, 250)
        c.line_to(30, 280)
        c.line_to(-60, 120)
        c.close_path()
        fs(c, hexc("#e8b44a"), lw=5)
        rnd = random.Random(4)
        for i in range(8):
            u = rnd.random()
            circle(c, lerp(-40, 40, u) + rnd.uniform(-10, 10), lerp(100, 250, u), 6)
            fs(c, hexc("#5a3a1a"), lw=0)


def guy(ctx, x, y, s, t, crown=0.0, **kw):
    """THE hero (reference design). crown>0 draws the giant golden crown on top of his red cap."""
    kw.setdefault("blink", doodle_auto_blink(t))
    hands = doodle(ctx, x, y, s, **kw)
    if crown > 0:
        hero_crown(ctx, x, y, s, t, crown, kw.get("tilt", 0.0))
    return hands


def hero_crown(ctx, x, y, s, t, k=1.0, tilt=0.0):
    """giant golden pharaoh crown, comically balanced on top of the red cap."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rotate(tilt)
    wob = math.sin(t * 2.3) * 0.06
    ctx.translate(10, -150)
    ctx.rotate(wob)
    ctx.scale(k, k)
    # tall body
    ctx.move_to(-90, 0)
    ctx.curve_to(-120, -120, -80, -260, 0, -300)
    ctx.curve_to(80, -260, 120, -120, 90, 0)
    ctx.close_path()
    g = cairo.LinearGradient(-90, 0, 90, -300)
    g.add_color_stop_rgb(0, *GOLD_D)
    g.add_color_stop_rgb(0.5, *GOLD_L)
    g.add_color_stop_rgb(1, *GOLD)
    ctx.set_source(g)
    ctx.fill_preserve()
    setc(ctx, INK)
    ctx.set_line_width(7)
    ctx.stroke()
    for k2 in range(5):
        for j in range(3):
            circle(ctx, -40 + j * 40 + (20 if k2 % 2 else 0), -50 - k2 * 45, 9)
            fs(ctx, LAPIS, lw=3)
    rrect(ctx, -104, -24, 208, 40, 10)
    fs(ctx, GOLD, lw=6)
    for k2 in range(5):
        circle(ctx, -72 + k2 * 36, -4, 10)
        fs(ctx, [RED, LAPIS, hexc("#2bb36b"), LAPIS, RED][k2], lw=3)
    # uraeus cobra
    ctx.move_to(0, -24)
    ctx.curve_to(-14, -60, 18, -80, 0, -100)
    setc(ctx, INK)
    ctx.set_line_width(18)
    ctx.stroke_preserve()
    setc(ctx, GOLD)
    ctx.set_line_width(11)
    ctx.stroke()
    ellipse(ctx, 0, -104, 16, 12)
    fs(ctx, GOLD, lw=4)
    ctx.move_to(-70, -40)
    ctx.curve_to(-80, -140, -50, -220, -20, -260)
    setc(ctx, WHITE, 0.45)
    ctx.set_line_width(12)
    ctx.stroke()
    ctx.restore()


def egyptian(ctx, x, y, s, t, role="worker", seed=0, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, seed + 2))
    if role == "guard":
        kw.setdefault("body", hexc("#f2e6c8"))
        return doodle(ctx, x, y, s, hair=nemes(hexc("#3a6ad6"), WHITE, uraeus=False), cap=False, extra=kilt, **kw)
    if role == "priest":
        kw.setdefault("body", WHITE)
        return doodle(ctx, x, y, s, hair=None, cap=False, extra=leopard, **kw)
    if role == "architect":
        kw.setdefault("body", hexc("#f2e6c8"))
        return doodle(ctx, x, y, s, hair=wig_black, cap=False, extra=gold_collar, **kw)
    if role == "pharaoh":
        kw.setdefault("body", hexc("#f6f0e0"))
        fx = kw.get("face", 0.0)
        return doodle(ctx, x, y, s, hair=combo(nemes(), beard(fx)), cap=False, extra=gold_collar, **kw)
    if role == "servant":
        kw.setdefault("body", hexc("#f6f0e0"))
        return doodle(ctx, x, y, s, hair=wig_black, cap=False, **kw)
    # worker / farmer
    kw.setdefault("body", [hexc("#f2e6c8"), hexc("#e8d8b0"), hexc("#f6eedc")][seed % 3])

    def band(c):
        c.move_to(-100, -30)
        c.curve_to(-100, -150, 100, -150, 100, -30)
        c.curve_to(60, -70, -60, -70, -100, -30)
        fs(c, hexc("#2a2420"), lw=LW)
        c.move_to(-98, -36)
        c.curve_to(-50, -78, 50, -78, 98, -36)
        setc(c, [RED, LAPIS, hexc("#2bb36b")][seed % 3])
        c.set_line_width(12)
        c.stroke()
    return doodle(ctx, x, y, s, hair=band, cap=False, extra=kilt if seed % 2 else None, **kw)


def spear(ctx, x, y, s=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    line(ctx, 0, 120, 0, -200, 9, hexc("#8a5a2b"))
    poly(ctx, [(-14, -196), (0, -250), (14, -196)])
    fs(ctx, hexc("#c9ccd2"), lw=4)
    ctx.restore()


# ====================================================================== backgrounds
def egypt_sky(ctx, t, sun=(1600, 170), sunset=0.0):
    top = lerpc(SKY_T, hexc("#ff8a4a"), sunset)
    bot = lerpc(SKY_B, hexc("#ffd8a0"), sunset)
    vgrad(ctx, -1500, -1200, 5000, 2400, top, bot)
    if sun:
        warm_glow(ctx, sun[0], sun[1], 300, 0.6, (1, 0.95, 0.6))
        circle(ctx, sun[0], sun[1], 85)
        fs(ctx, (1, 0.88, 0.35), lw=6)


def desert_bg(ctx, t, pyramids=True, horizon=720, cased=True, dunes=True):
    egypt_sky(ctx, t)
    for i in range(3):
        cloud(ctx, ((i * 900 + t * 15) % 3400) - 700, 140 + i * 60, 0.8, a=0.6)
    if pyramids:
        pyramid(ctx, 560, horizon + 10, 520, 340, cased, sparkle_t=t)
        pyramid(ctx, 1150, horizon + 10, 760, 500, cased, sparkle_t=t + 0.7)
        pyramid(ctx, 1640, horizon + 10, 380, 250, cased, sparkle_t=t + 1.4)
    ctx.rectangle(-1500, horizon, 5000, 1600)
    fs(ctx, SAND, lw=6)
    if dunes:
        for k in range(-3, 9):
            ctx.move_to(k * 420 - 200, horizon + 120 + (k % 2) * 60)
            ctx.curve_to(k * 420 - 60, horizon + 60 + (k % 2) * 60, k * 420 + 120, horizon + 60 + (k % 2) * 60,
                         k * 420 + 260, horizon + 120 + (k % 2) * 60)
            setc(ctx, SAND_D)
            ctx.set_line_width(5)
            ctx.stroke()
    palm(ctx, 140, horizon + 30, 260, t)
    palm(ctx, 1850, horizon + 40, 220, t + 1)


def palace_bg(ctx, t, dim=0.0, throne=True, window_boat=0.0):
    vgrad(ctx, -1200, -800, 4400, 2200, hexc("#f2dcae"), hexc("#e2c48a"))
    # painted frieze
    ctx.rectangle(-1200, 80, 4400, 90)
    fs(ctx, LAPIS, lw=5)
    for k in range(-20, 60):
        glyph(ctx, ["bird", "eye", "ankh", "sun", "water", "snake"][k % 6], k * 80, 125, 0.9, GOLD)
    ctx.rectangle(-1200, 760, 4400, 600)
    fs(ctx, hexc("#c9a46a"), lw=6)
    for k in range(-20, 60):
        line(ctx, k * 120, 760, k * 160 - 200, 1300, 3, hexc("#a8864a"), 0.7)
    # window to the Nile
    wx, wy = 1430, 260
    ctx.save()
    rrect(ctx, wx, wy, 300, 300, 20)
    ctx.clip()
    vgrad(ctx, wx, wy, 300, 300, SKY_T, SKY_B)
    ctx.rectangle(wx, wy + 200, 300, 100)
    setc(ctx, NILE)
    ctx.fill()
    palm(ctx, wx + 40, wy + 210, 120, t)
    if window_boat > 0:
        bx = lerp(wx + 150, wx + 360, window_boat)
        ctx.move_to(bx - 70, wy + 210)
        ctx.curve_to(bx - 40, wy + 240, bx + 40, wy + 240, bx + 70, wy + 210)
        ctx.close_path()
        fs(ctx, GOLD, lw=4)
        line(ctx, bx, wy + 210, bx, wy + 120, 5, hexc("#6b4428"))
        poly(ctx, [(bx + 4, wy + 125), (bx + 4, wy + 200), (bx + 54, wy + 200)])
        fs(ctx, WHITE, lw=3)
    ctx.restore()
    rrect(ctx, wx, wy, 300, 300, 20)
    fs(ctx, None, lw=10, stroke=GOLD_D)
    # columns with lotus capitals
    for cx in (-260, 330, 1250, 2150):
        ctx.rectangle(cx - 55, 170, 110, 600)
        fs(ctx, hexc("#e8d4a8"), lw=6)
        for k in range(4):
            line(ctx, cx - 55, 260 + k * 130, cx + 55, 260 + k * 130, 8, [LAPIS, RED, hexc("#2bb3a0"), GOLD][k])
        poly(ctx, [(cx - 95, 170), (cx + 95, 170), (cx + 60, 230), (cx - 60, 230)])
        fs(ctx, hexc("#2bb3a0"), lw=6)
    if throne:
        # dais + throne
        for k in range(3):
            ctx.rectangle(640 - k * 50, 700 + k * 22, 640 + k * 100, 26)
            fs(ctx, hexc("#d8bf8a"), lw=4)
        rrect(ctx, 820, 330, 280, 240, 30)
        fs(ctx, GOLD, lw=7)
        rrect(ctx, 850, 360, 220, 180, 20)
        fs(ctx, LAPIS, lw=5)
        glyph(ctx, "ankh", 960, 440, 1.6, GOLD)
        ctx.rectangle(800, 560, 320, 60)
        fs(ctx, GOLD_D, lw=6)
        for sx in (790, 1130):
            line(ctx, sx, 560, sx, 700, 14, GOLD_D)
            # lion paw feet
            ellipse(ctx, sx, 704, 24, 12)
            fs(ctx, GOLD, lw=4)
    if dim > 0:
        setc(ctx, (0.05, 0.03, 0.02), dim)
        ctx.paint()


def bedroom_bg(ctx, t, glow_under=0.0, morning=True):
    vgrad(ctx, -600, -400, 3200, 1600, hexc("#bfe0f2"), hexc("#a6cfe6"))
    ctx.rectangle(-600, 800, 3200, 600)
    fs(ctx, hexc("#c9925a"), lw=6)
    for k in range(-6, 30):
        line(ctx, k * 140, 800, k * 140 - 60, 1200, 3, hexc("#a8763f"))
    # window
    rrect(ctx, 1260, 150, 420, 330, 16)
    fs(ctx, hexc("#ffe9a0") if morning else hexc("#2a3a6a"), lw=10)
    line(ctx, 1470, 150, 1470, 480, 8)
    line(ctx, 1260, 315, 1680, 315, 8)
    circle(ctx, 1580, 230, 40)
    fs(ctx, (1, 0.85, 0.35), lw=4)
    # posters: pyramid + space
    ctx.save()
    ctx.translate(420, 260)
    ctx.rotate(-0.04)
    rrect(ctx, -120, -150, 240, 300, 8)
    fs(ctx, hexc("#ffd36a"), lw=6)
    pyramid(ctx, 0, 90, 180, 130)
    text(ctx, "EGYPT", 0, -100, 40, RED, outline=0, shadow=False)
    ctx.restore()
    ctx.save()
    ctx.translate(780, 230)
    ctx.rotate(0.05)
    rrect(ctx, -100, -110, 200, 220, 8)
    fs(ctx, hexc("#2a2a5a"), lw=6)
    circle(ctx, -20, 0, 50)
    fs(ctx, hexc("#ff8a4a"), lw=5)
    for k in range(6):
        circle(ctx, -70 + k * 30, -80 + (k % 2) * 140, 4)
        fs(ctx, WHITE, lw=0)
    ctx.restore()
    # bed
    rrect(ctx, 200, 560, 900, 220, 20)
    fs(ctx, hexc("#3a6ad6"), lw=7)
    rrect(ctx, 170, 420, 60, 380, 16)
    fs(ctx, hexc("#8a5a2b"), lw=7)
    rrect(ctx, 240, 500, 220, 90, 40)
    fs(ctx, WHITE, lw=6)
    ctx.rectangle(200, 770, 900, 30)
    fs(ctx, hexc("#2a3a7a"), lw=6)
    # dark gap under bed
    ctx.rectangle(220, 800, 860, 10)
    setc(ctx, (0, 0, 0), 0.0)
    ctx.fill()
    if glow_under > 0:
        warm_glow(ctx, 700, 820, 420, 0.7 * glow_under)
    # clutter
    for k, (cx, cc) in enumerate(((1250, hexc("#ff6a6a")), (1420, hexc("#6fbf4a")), (1600, hexc("#ffd36a")))):
        ellipse(ctx, cx, 860 + (k % 2) * 30, 70, 18)
        fs(ctx, cc, lw=5)
    # sock
    ctx.move_to(1750, 880)
    ctx.line_to(1750, 940)
    ctx.line_to(1810, 940)
    setc(ctx, INK)
    ctx.set_line_width(26)
    ctx.stroke_preserve()
    setc(ctx, WHITE)
    ctx.set_line_width(18)
    ctx.stroke()


def nile_bg(ctx, t, level=0.0, sunset=0.0, night=0.0, fields_wet=0.0, flood_reach=0.0, channels=0.0):
    """river on the left, farms + village on the right. level 0..1 raises the river."""
    egypt_sky(ctx, t, sun=(300, 160), sunset=sunset)
    # far bank
    ctx.rectangle(-1500, 520, 5000, 80)
    fs(ctx, hexc("#9fd46a"), lw=5)
    for k in range(8):
        palm(ctx, -200 + k * 300, 560, 140, t + k)
    # ground
    ctx.rectangle(-1500, 600, 5000, 1000)
    fs(ctx, SAND, lw=6)
    # fields (grid)
    for r in range(3):
        for c in range(5):
            x0, y0 = 860 + c * 220, 660 + r * 120
            wet = clamp(fields_wet * 3 - (c + r) * 0.3)
            ctx.rectangle(x0, y0, 200, 100)
            fs(ctx, lerpc(hexc("#d8c070"), FIELD, wet), lw=4)
            for k in range(5):
                line(ctx, x0 + 20 + k * 40, y0 + 80, x0 + 20 + k * 40, y0 + 40 - 20 * wet, 4,
                     lerpc(hexc("#b8a050"), FIELD_D, wet))
    # village
    for k in range(4):
        mud_house(ctx, 1980 + k * 200, 760 + (k % 2) * 40, 0.8)
    # river band, rises with level
    top = 600 - 10 - 70 * level
    ctx.move_to(-1500, top)
    for x in range(-1500, 900, 40):
        ctx.line_to(x, top + math.sin(x * 0.02 + t * 3) * 8)
    ctx.line_to(820 + 260 * level, 1400)
    ctx.line_to(-1500, 1400)
    ctx.close_path()
    fs(ctx, NILE, lw=6)
    for k in range(10):
        ph = (t * 0.4 + k / 10) % 1
        x = -300 + k * 120 + ph * 80
        line(ctx, x, top + 60 + (k % 3) * 80, x + 60, top + 60 + (k % 3) * 80, 5, WHITE, 0.6)
    # flood tongue creeping toward the village
    if flood_reach > 0:
        fx = lerp(820, 2350, flood_reach)
        ctx.move_to(780, 600)
        ctx.line_to(fx - 40, 610)
        for k in range(13):
            yy = 610 + k * 40
            ctx.line_to(fx + 30 * math.sin(k * 1.3 + t * 4), yy)
        ctx.line_to(780, 1100)
        ctx.close_path()
        fs(ctx, NILE, lw=5, alpha=0.78)
        for k in range(6):
            yy = 640 + k * 70
            line(ctx, fx - 120, yy, fx - 40, yy, 5, WHITE, 0.7)
    if channels > 0:
        for path in channel_paths():
            polyline_part(ctx, path, 1.0, 34, MUD)
            polyline_part(ctx, path, channels, 22, NILE)
    if night > 0:
        setc(ctx, (0.04, 0.05, 0.15), 0.55 * night)
        ctx.paint()


def channel_paths():
    return [
        [(820, 640), (880, 640), (900, 650), (1980, 650)],
        [(820, 640), (880, 760), (1980, 770)],
        [(820, 640), (880, 880), (1980, 890)],
    ]


def paper_lesson(ctx, title, t, color=RED):
    paper_bg(ctx, hexc("#f6e8c4"))
    pop_text(ctx, title, 960, 90, 70, t - 0.2, color, outline=0)


def tomb_painting(ctx, x, y, w, h, t, cap=1.0):
    """flat ancient-Egyptian-style wall painting, with the hero (and his cap) in it."""
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    ctx.translate(x, y)
    ctx.scale(w / 1000, h / 600)
    vgrad(ctx, 0, 0, 1000, 600, hexc("#e8c98a"), hexc("#d8b070"))
    line(ctx, 0, 40, 1000, 40, 8, hexc("#8a3a1a"))
    line(ctx, 0, 560, 1000, 560, 8, hexc("#8a3a1a"))
    # channel & water register
    ctx.rectangle(0, 470, 1000, 50)
    setc(ctx, hexc("#3d7fb1"))
    ctx.fill()
    for k in range(14):
        glyph(ctx, "water", 40 + k * 70, 495, 0.9, WHITE)
    # wheat
    for k in range(18):
        line(ctx, 620 + k * 20, 460, 620 + k * 20, 380, 4, hexc("#4e7a26"))
        ellipse(ctx, 620 + k * 20, 376, 5, 12)
        setc(ctx, hexc("#d9a020"))
        ctx.fill()
    # profile workers with hoes
    for k in range(3):
        px = 80 + k * 110
        circle(ctx, px, 300, 22)
        setc(ctx, hexc("#9a4a24"))
        ctx.fill()
        ctx.rectangle(px - 16, 322, 32, 90)
        ctx.fill()
        ctx.rectangle(px - 20, 410, 40, 40)
        setc(ctx, WHITE)
        ctx.fill()
        line(ctx, px + 10, 340, px + 70, 430, 7, hexc("#5a3a1a"))
        ctx.save()
        circle(ctx, px, 300, 22)
        ctx.clip()
        ctx.rectangle(px - 30, 270, 44, 60)
        setc(ctx, INK)
        ctx.fill()
        ctx.restore()
        circle(ctx, px + 10, 296, 3)
        setc(ctx, WHITE)
        ctx.fill()
    # the crowd carrying the hero
    for k in range(4):
        px = 420 + k * 50
        circle(ctx, px, 330, 18)
        setc(ctx, hexc("#9a4a24"))
        ctx.fill()
        ctx.rectangle(px - 13, 348, 26, 80)
        ctx.fill()
        line(ctx, px, 350, px + 6, 300, 6, hexc("#9a4a24"))
    ctx.rectangle(400, 288, 190, 14)
    setc(ctx, GOLD_D)
    ctx.fill()
    # the little white figure in a red cap
    ctx.save()
    ctx.translate(495, 240)
    ctx.scale(0.17, 0.17)
    ctx.rectangle(-50, 70, 100, 200)
    setc(ctx, hexc("#f4efe2"))
    ctx.fill()
    circle(ctx, 0, 0, 100)
    setc(ctx, hexc("#f4efe2"))
    ctx.fill()
    circle(ctx, 30, -10, 11)
    setc(ctx, INK)
    ctx.fill()
    if cap > 0:
        draw_cap(ctx, hexc("#c8282d"))
    ctx.restore()
    # hieroglyph columns + cartouche
    glyph_column(ctx, 960, 90, 6, 0.8, hexc("#2a3a7a"), seed=3)
    glyph_column(ctx, 905, 90, 6, 0.8, hexc("#8a3a1a"), seed=8)
    rrect(ctx, 820, 70, 50, 260, 25)
    fs(ctx, None, lw=4, stroke=hexc("#2a3a7a"))
    glyph(ctx, "cap", 845, 120, 0.8)
    glyph(ctx, "eye", 845, 190, 0.6, hexc("#2a3a7a"))
    glyph(ctx, "water", 845, 260, 0.6, hexc("#2a3a7a"))
    # age cracks + vignette
    rnd = random.Random(2)
    for i in range(8):
        x0, y0 = rnd.random() * 1000, rnd.random() * 600
        ctx.move_to(x0, y0)
        for k in range(4):
            x0 += rnd.uniform(-40, 40)
            y0 += rnd.uniform(10, 40)
            ctx.line_to(x0, y0)
        setc(ctx, hexc("#6a4a2a"), 0.5)
        ctx.set_line_width(2)
        ctx.stroke()
    g = cairo.RadialGradient(500, 300, 200, 500, 300, 650)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0.3, 0.15, 0.0, 0.45)
    ctx.set_source(g)
    ctx.rectangle(0, 0, 1000, 600)
    ctx.fill()
    ctx.restore()


# ====================================================================== SHOTS
def hook_scene(ctx, t, D, cue, freeze=None):
    tt = t if freeze is None else min(t, freeze)
    t_below = cue("Below me")
    t_tome = cue("To me!")
    t_real = cue("the real Pharaoh")
    t_how = cue("So how did")
    t_acc = cue("Total accident")
    px, pb, pw, ph = 960, 980, 1500, 980
    apex = (px, pb - ph)
    gx, gy = apex[0] + 8, apex[1] - 125
    if tt < t_below:
        k = ease(prog(tt, 0, t_below))
        cx, cy, z = lerp(gx, gx, k), lerp(gy - 140, gy - 60, k), lerp(2.6, 2.1, k)
    elif tt < t_real:
        k = ease(prog(tt, t_below, t_below + 2.4))
        cx, cy, z = lerp(gx, 960, k), lerp(gy - 60, 520, k), lerp(2.1, 0.62, k)
    elif tt < t_how:
        k = ease(prog(tt, t_real, t_real + 1.0))
        cx, cy, z = lerp(960, 1900, k), lerp(520, 860, k), lerp(0.62, 1.0, k)
    else:
        k = ease_out(prog(tt, t_how, t_how + 0.6))
        cx, cy, z = lerp(1900, gx, k), lerp(860, gy - 30, k), lerp(1.0, 2.2, k)
    ctx.save()
    cam(ctx, cx, cy, z, t=tt)
    egypt_sky(ctx, tt, sun=(1500, -250))
    for i in range(4):
        cloud(ctx, ((i * 800 + tt * 20) % 3600) - 900, -200 + i * 120, 1.2, a=0.7)
    ctx.rectangle(-1500, pb - 40, 5000, 1600)
    fs(ctx, SAND, lw=6)
    pyramid(ctx, -500, pb, 700, 460, sparkle_t=tt)
    pyramid(ctx, 2500, pb, 800, 520, sparkle_t=tt + 1)
    pyramid(ctx, px, pb, pw, ph, sparkle_t=tt + 2)
    # bowing crowd at the base
    for i in range(36):
        cxp = -200 + i * 70
        bow = 0.5 + 0.5 * math.sin(tt * 3 + i * 0.4)
        egyptian(ctx, cxp, pb + 60 + (i % 3) * 30, 0.16, tt, role="worker", seed=i, face=0.0,
                 tilt=0.6 * bow, larm=(2.6, 0.2), rarm=(-2.6, -0.2), show_legs=False, expr="happy")
    # real Pharaoh's chariot on the horizon
    if tt > t_real - 0.5:
        k = prog(tt, t_real - 0.5, D)
        cxr = lerp(2600, 2150, k)

        def rider(c):
            egyptian(c, -40, -330, 0.32, tt, role="pharaoh", face=-0.4, expr="frown", brows="angry",
                     larm=(0.3, 0.2), rarm=(-0.3, -0.2), show_legs=False)
        ctx.save()
        ctx.translate(cxr, pb + 120)
        ctx.scale(-1, 1)
        chariot(ctx, 0, 0, 0.55, tt, moving=True, rider=rider, driver=False)
        ctx.restore()
        for k2 in range(6):
            ph_ = (tt * 0.8 + k2 / 6) % 1
            circle(ctx, cxr + 120 + ph_ * 300, pb + 100 - ph_ * 60, 30 + ph_ * 50)
            setc(ctx, SAND_L, 0.6 * (1 - ph_))
            ctx.fill()
    proud = tt < t_how
    guy(ctx, gx, gy, 0.42, tt, crown=1.0, expr="grin" if proud else "worried", face=0.0 if proud else 0.0,
        larm=(0.3, 0.2) if tt < t_tome else (2.6, -0.2), rarm=(-2.6, 0.2) if tt > t_tome and proud else (-0.3, -0.2),
        brows="worried" if not proud else None, look=(0, 0))
    if not proud:
        sweat(ctx, gx + 50, gy - 20, 0.5, tt)
    ctx.restore()
    return t_acc


def sh_hook(ctx, t, D, cue):
    t_acc = cue("Total accident")
    frozen = t > t_acc + 0.2
    hook_scene(ctx, t, D, cue, freeze=t_acc + 0.2 if frozen else None)
    if frozen:
        setc(ctx, (0.15, 0.08, 0.0), 0.25)
        ctx.paint()
    t_below, t_tome, t_real = cue("Below me"), cue("To me!"), cue("the real Pharaoh")
    if t > 0.4:
        pop_text(ctx, "THIS IS ME.", 960, 980, 90, t - 0.4, WHITE, hold=t_below - 0.6)
    if t > t_tome:
        pop_text(ctx, "10,000 PEOPLE BOWING... TO ME!", 960, 120, 70, t - t_tome, GOLD, hold=t_real - t_tome)
    if t > t_real + 0.6:
        pop_text(ctx, "THE REAL PHARAOH", 760, 140, 80, t - t_real - 0.6, RED, hold=cue("So how did") - t_real - 0.6)
    if t > cue("Honestly"):
        pop_text(ctx, "TOTAL ACCIDENT.", 960, 980, 110, t - t_acc, RED, rot=-0.03)


def sh_rewind(ctx, t, D, cue):
    hs, hc = TIMELINE["hook"]
    th = hs["D"] * (1 - ease_in(prog(t, 0, D)))
    hook_scene(ctx, max(0.0, th), hs["D"], hc)
    setc(ctx, (0.1, 0.1, 0.3), 0.25)
    ctx.paint()
    vhs(ctx, t)
    rewind_icon(ctx, 220, 120, 1.0, 0.9)
    text(ctx, "REWIND", 330, 122, 70, WHITE, align="left", outline=0, shadow=False)


def sh_title(ctx, t, D, cue):
    vgrad(ctx, 0, 0, W, H, hexc("#ffb84a"), hexc("#e8762a"))
    ctx.save()
    ctx.translate(W / 2, 1300)
    ctx.rotate(t * 0.15)
    for k in range(24):
        ctx.move_to(0, 0)
        ctx.arc(0, 0, 2400, k * math.pi / 12, k * math.pi / 12 + math.pi / 24)
        ctx.close_path()
        setc(ctx, WHITE, 0.12)
        ctx.fill()
    ctx.restore()
    pyramid(ctx, 300, 1080, 700, 420)
    pyramid(ctx, 1650, 1080, 600, 360)
    for x in range(0, W, 90):
        glyph(ctx, ["bird", "eye", "ankh", "sun", "water", "snake", "dog"][(x // 90) % 7], x + 45, 40, 0.9, hexc("#7a3a0a"))

    def row(words, y, size, t0):
        total = sum(text_width(ctx, w, size) for w, _ in words) + 36 * (len(words) - 1)
        x = W / 2 - total / 2
        for i, (w, c) in enumerate(words):
            ww = text_width(ctx, w, size)
            tt = t - t0 - i * 0.15
            if tt > 0:
                k = back_out(tt / 0.45, 2.4) if tt < 0.45 else 1
                ctx.save()
                ctx.translate(x + ww / 2, y)
                ctx.scale(max(k, 1e-3), max(k, 1e-3))
                ctx.rotate(-0.03 + 0.01 * math.sin(t * 3 + i))
                text(ctx, w, 0, 0, size, c, outline=14)
                ctx.restore()
            x += ww + 36
    row([("I", WHITE), ("ACCIDENTALLY", WHITE)], 300, 130, 0.15)
    row([("BECAME", WHITE), ("A", WHITE)], 470, 130, 0.5)
    row([("PHARAOH!", GOLD_L)], 660, 190, 0.85)
    k = ease_out(prog(t, 1.2, 1.8))
    if k > 0:
        guy(ctx, 1600, lerp(1500, 780, k), 0.6, t, crown=1.0, expr="grin", face=-0.3,
            larm=(2.6, -0.3), rarm=(-0.3, 0))
    text(ctx, "HISTORY WORLD", W / 2, 1000, 48, WHITE, font=HAND_FONT, outline=6, alpha=ease(prog(t, 1.5, 2.2)))


def sh_bedroom(ctx, t, D, cue):
    t_clean = cue("I was cleaning")
    t_okay = cue("Okay, I was pretending")
    t_under = cue("And under my bed")
    ctx.save()
    if t < t_under:
        cam(ctx, 960, 540, lerp(1.0, 1.05, ease(prog(t, 0, t_under))))
    else:
        cam(ctx, lerp(960, 760, ease(prog(t, t_under, t_under + 1))), lerp(540, 700, ease(prog(t, t_under, t_under + 1))),
            lerp(1.05, 1.6, ease(prog(t, t_under, t_under + 1))))
    bedroom_bg(ctx, t, glow_under=ease(prog(t, t_under + 2.0, t_under + 3.0)))
    if t < t_okay:
        # "cleaning": sweeping with a broom
        sw = math.sin(t * 6) * 0.25
        hands = guy(ctx, 1350, 520, 0.7, t, expr="smile", face=-0.4, larm=(0.9 + sw, -0.5), rarm=(-0.9 + sw, 0.5))
        line(ctx, 1300 + sw * 60, 600, 1240 + sw * 140, 900, 10, hexc("#8a5a2b"))
        poly(ctx, [(1200 + sw * 140, 880), (1290 + sw * 140, 880), (1300 + sw * 140, 940), (1190 + sw * 140, 940)])
        fs(ctx, hexc("#e8c84a"), lw=5)
        if t > t_clean:
            pop_text(ctx, "*cleaning*", 1350, 260, 60, t - t_clean, WHITE, font=HAND_FONT, outline=6)
    elif t < t_under:
        # actually lying on the bed with a phone
        ctx.save()
        ctx.translate(700, 520)
        ctx.rotate(-math.pi / 2)
        doodle(ctx, 0, 0, 0.6, expr="happy", face=0.0, larm=(2.6, 0.6), rarm=(-2.4, -0.4),
               blink=doodle_auto_blink(t))
        ctx.restore()
        rrect(ctx, 760, 380, 50, 80, 8)
        fs(ctx, hexc("#2a2a33"), lw=4)
        pop_text(ctx, "(not cleaning)", 960, 260, 64, t - t_okay, WHITE, font=HAND_FONT, outline=6)
    else:
        # lying on the floor, peeking under the bed
        ctx.save()
        ctx.translate(1120, 860)
        ctx.rotate(-math.pi / 2)
        doodle(ctx, 0, 0, 0.55, expr="o" if t < t_under + 2.0 else "shock", face=0.0, look=(0, 1),
               larm=(0.6, 0.2), rarm=(-0.6, -0.2), blink=doodle_auto_blink(t))
        ctx.restore()
        k = ease_out(prog(t, t_under + 0.6, t_under + 1.4))
        pizza_box(ctx, lerp(760, 920, k), 870, 0.8, rot=0.05)
        if t > t_under + 1.4:
            for i in range(3):
                ph = (t * 0.6 + i / 3) % 1
                text(ctx, "~", 1000 + i * 30, 820 - ph * 80, 40, hexc("#7a9a3a"), outline=0, shadow=False, alpha=1 - ph)
        if t > t_under + 2.2:
            sparkle(ctx, 760, 820, 40, t)
            pop_text(ctx, "?!", 1250, 640, 90, t - t_under - 2.2, GOLD)
    ctx.restore()
    vignette(ctx, 0.3)


def sh_box(ctx, t, D, cue):
    t_pics = cue("Covered in strange")
    t_birds = cue("Birds, eyes")
    t_button = cue("And right in the middle")
    t_sensible = cue("Now, any sensible")
    t_press = cue("So obviously")
    bg_fill(ctx, hexc("#2a2440"))
    warm_glow(ctx, 960, 540, 900, 0.35)
    z = lerp(1.0, 1.15, ease(prog(t, 0, t_button)))
    if t > t_button:
        z = lerp(1.15, 1.7, ease(prog(t, t_button, t_button + 1.2)))
    cy = 560 if t < t_button else lerp(560, 430, ease(prog(t, t_button, t_button + 1.2)))
    ctx.save()
    cam(ctx, 960, cy, z)
    pressed = ease(prog(t, D - 1.4, D - 1.2))
    golden_box(ctx, 960, 560, 1.25, t, glow=0.5 + 0.5 * math.sin(t * 3) * 0.3 + (0.5 if t > t_button else 0),
               pressed=pressed)
    if t > t_birds:
        for i, k in enumerate(("bird", "eye", "snake", "dog")):
            tt = t - t_birds - i * 0.6
            if tt > 0:
                a = back_out(clamp(tt / 0.3))
                circle(ctx, 680 + i * 190, 360, 50 * a)
                fs(ctx, WHITE, lw=5)
                glyph(ctx, k, 680 + i * 190, 360, 1.2 * a, INK)
    # the hero's finger/hand reaching in from the right
    if t > t_sensible:
        reach = ease(prog(t, t_press, D - 1.3))
        hx = lerp(1700, 980, reach)
        hy = lerp(330, 405, reach)
        line(ctx, 2200, 200, hx + 40, hy - 10, 18)
        circle(ctx, hx, hy, 26)
        fs(ctx, WHITE, lw=7)
    ctx.restore()
    if t > t_sensible and t < t_press:
        pop_text(ctx, "DON'T PRESS IT.", 960, 1010, 80, t - t_sensible, WHITE)
    if t > t_press + 0.8:
        pop_text(ctx, "PRESSED IT.", 960, 1010, 90, t - t_press - 0.8, RED, rot=-0.03)
    if t > D - 1.2:
        burst(ctx, 1450, 260, 120, t - D + 1.2, "CLICK!", size=56)
    vignette(ctx, 0.4)


def sh_portal(ctx, t, D, cue):
    t_whoosh = cue("Whoosh")
    t_tunnel = cue("My bedroom turned")
    t_socks = cue("My socks")
    t_years = cue("About four thousand")
    if t < t_tunnel:
        # bedroom being sucked into a portal
        k = ease_in(prog(t, t_whoosh, t_tunnel))
        ctx.save()
        cam(ctx, 960, 540, 1.0 + k * 0.6, rot=k * 1.5)
        bedroom_bg(ctx, t)
        guy(ctx, 1100, 520, 0.7, t, expr="shock", face=0, larm=(2.2, 0.4), rarm=(-2.2, -0.4),
            tilt=math.sin(t * 20) * 0.05)
        golden_box(ctx, 1240, 640, 0.35, t, glow=1.0, pressed=1.0, buzz=1.0)
        ctx.restore()
        r = 80 + 1400 * k
        warm_glow(ctx, 960, 540, r, 0.8 * clamp(t / 0.6), (0.6, 0.85, 1.0))
        circle(ctx, 960, 540, r * 0.35)
        setc(ctx, (1, 0.95, 0.7), 0.9 * clamp(t / 0.6))
        ctx.fill()
        if t < cue("Hum"):
            pop_text(ctx, "click.", 600, 220, 70, t, WHITE, font=HAND_FONT, outline=6)
        elif t < t_whoosh:
            pop_text(ctx, "hmmmmm...", 1300, 220, 70, t - cue("Hum"), WHITE, font=HAND_FONT, outline=6)
        else:
            burst(ctx, 960, 200, 160, t - t_whoosh, "WHOOSH!", size=64, color=(0.6, 0.85, 1.0), tcolor=LAPIS)
        return
    vortex(ctx, t, (0.15, 0.3, 0.8), (1.0, 0.82, 0.3), speed=2.2)
    rnd = random.Random(5)
    for i in range(14):
        ph = (t * 0.35 + i / 14) % 1
        a = rnd.random() * 6.28 + t * 0.3
        r = 60 + ph ** 2 * 1300
        px, py = W / 2 + math.cos(a) * r, H / 2 + math.sin(a) * r * 0.7
        sc = 0.2 + ph * 1.2
        kind = i % 4
        if kind == 0:     # sock
            ctx.save()
            ctx.translate(px, py)
            ctx.rotate(t * 3 + i)
            ctx.move_to(0, -30 * sc)
            ctx.line_to(0, 30 * sc)
            ctx.line_to(30 * sc, 30 * sc)
            setc(ctx, INK)
            ctx.set_line_width(20 * sc + 4)
            ctx.stroke_preserve()
            setc(ctx, WHITE)
            ctx.set_line_width(14 * sc + 2)
            ctx.stroke()
            ctx.restore()
        elif kind == 1:   # comic book
            ctx.save()
            ctx.translate(px, py)
            ctx.rotate(t * 2 + i)
            rrect(ctx, -40 * sc, -55 * sc, 80 * sc, 110 * sc, 4)
            fs(ctx, [hexc("#ff4a4a"), hexc("#ffd36a"), hexc("#4aa0ff")][i % 3], lw=3)
            text(ctx, "POW", 0, 0, 26 * sc + 4, WHITE, outline=3, shadow=False)
            ctx.restore()
        elif kind == 2:
            glyph(ctx, ["bird", "eye", "ankh", "sun"][i % 4], px, py, sc * 1.5, GOLD)
        else:
            clock_icon(ctx, px, py, 10 + ph * 60, t, back=True, rot=t + i)
    ctx.save()
    ctx.translate(W / 2 + 260 * math.sin(t * 0.9), H / 2 + 120 * math.cos(t * 1.3) - 60)
    ctx.rotate(t * 2.5)
    guy(ctx, 0, -150, 0.6, t, expr="shock", face=0, larm=(2.4, 0.5), rarm=(-2.4, -0.5), legs=(0.5, -0.5))
    ctx.restore()
    if t > t_socks:
        bc_counter(ctx, t - t_socks, D - t_socks, 2026, -2500)
    if t > t_years + 0.5:
        pop_text(ctx, "4,500 YEARS BACK!", 960, 980, 80, t - t_years - 0.5, GOLD)
    vignette(ctx, 0.6)


def sh_desert(ctx, t, D, cue):
    t_up = cue("When I looked up")
    t_pyr = cue("Pyramids!")
    t_shiny = cue("Shiny and new")
    t_fact = cue("Fun fact")
    t_rough = cue("The rough stones")
    if t < t_fact:
        if t < t_up:
            cx, cy, z = 560, 760, 1.6
        else:
            k = ease(prog(t, t_up, t_pyr + 1.0))
            cx, cy, z = lerp(560, 1000, k), lerp(760, 520, k), lerp(1.6, 0.95, k)
        ctx.save()
        cam(ctx, cx, cy, z)
        desert_bg(ctx, t)
        if t < t_up:
            # face first in the sand, legs kicking
            ctx.save()
            ctx.translate(560, 860)
            ctx.rotate(math.pi)
            doodle(ctx, 0, -40, 0.5, expr="flat", show_body=True, larm=(0.4, 0.2), rarm=(-0.4, -0.2),
                   legs=(math.sin(t * 12) * 0.5, -math.sin(t * 12) * 0.5), cap=True)
            ctx.restore()
            ctx.rectangle(380, 850, 360, 160)
            setc(ctx, SAND)
            ctx.fill()
            ellipse(ctx, 560, 850, 120, 30)
            fs(ctx, SAND_D, lw=5)
            for k in range(6):
                ph = (t * 2 + k / 6) % 1
                circle(ctx, 500 + k * 25, 840 - ph * 80, 6 * (1 - ph))
                setc(ctx, SAND_D, 0.8)
                ctx.fill()
        else:
            amazed = t > t_pyr
            guy(ctx, 560, 600, 0.55, t, expr="shock" if amazed else "o", face=0.6, look=(1, -0.6),
                larm=(2.5, 0.3) if amazed else (0.3, 0.2), rarm=(-2.5, -0.3) if amazed else (-0.3, -0.2))
            for k in range(4):
                circle(ctx, 520 + k * 30, 650 + (k % 2) * 20, 5)
                fs(ctx, SAND_D, lw=0)
        ctx.restore()
        if t > t_pyr:
            pop_text(ctx, "PYRAMIDS!", 960, 140, 120, t - t_pyr, GOLD, hold=t_shiny - t_pyr + 0.5)
        if t > t_shiny + 0.5:
            pop_text(ctx, "SHINY WHITE LIMESTONE", 1200, 140, 74, t - t_shiny - 0.5, WHITE)
        caption(ctx, "GIZA, EGYPT", "c. 2500 BC", t - t_up - 0.4, dur=4.5)
    else:
        tt = t - t_fact
        paper_lesson(ctx, "FUN FACT", tt, LAPIS)
        for i, (lab, cased, col) in enumerate((("THEN", True, hexc("#2f7a3a")), ("NOW", False, RED))):
            x = 560 + i * 800
            a = ease_out(prog(tt, 0.4 + i * 0.8, 0.9 + i * 0.8))
            if a <= 0:
                continue
            ctx.save()
            ctx.translate(x, 600)
            ctx.scale(a, a)
            rrect(ctx, -330, -360, 660, 560, 16)
            fs(ctx, hexc("#bfe6fa") if cased else hexc("#d8eef8"), lw=7)
            ctx.rectangle(-330, 110, 660, 90)
            fs(ctx, SAND, lw=0)
            pyramid(ctx, 0, 140, 480, 320, cased, sparkle_t=t if cased else None)
            ctx.restore()
            pop_text(ctx, lab, x, 330, 80, tt - 0.6 - i * 0.8, col, outline=0)
        if t > t_rough:
            text(ctx, "the smooth casing stones were later taken away to build Cairo", 960, 940, 46, INK,
                 font=HAND_FONT, outline=0, shadow=False, alpha=ease(prog(t, t_rough, t_rough + 0.4)))
    vignette(ctx, 0.3)


def sh_guards(ctx, t, D, cue):
    t_spears = cue("Spears.")
    t_two = cue("Two guards")
    t_peace = cue("I come in peace")
    t_under = cue("They did not understand")
    t_carry = cue("So they picked")
    ctx.save()
    if t < t_carry:
        cam(ctx, 900, 560, lerp(1.25, 1.35, ease(prog(t, 0, t_carry))))
    else:
        cam(ctx, lerp(900, 1300, ease(prog(t, t_carry, D))), 560, 1.2)
    desert_bg(ctx, t)
    if t < t_carry:
        # selfie
        scared = t > t_spears
        hands = guy(ctx, 860, 600, 0.6, t, expr="grin" if not scared else ("shock" if t < t_peace else "smile"),
                    face=0.9 if not scared else -0.8, look=(1, -0.3) if not scared else (-1, 0),
                    larm=(0.3, 0.2), rarm=(-2.3, 0.2) if not scared else (-2.6, 0.0),
                    brows="worried" if scared else None)
        if not scared:
            rx, ry = hands["r"]
            rrect(ctx, rx - 18, ry - 50, 36, 60, 6)
            fs(ctx, hexc("#2a2a33"), lw=4)
            if (t % 1.5) < 0.12:
                setc(ctx, WHITE, 0.6)
                ctx.paint()
        # spears poking in, then guards
        if t > t_spears - 0.2:
            k = ease_out(prog(t, t_spears - 0.2, t_two + 0.4))
            fade = 1 - prog(t, t_two + 0.2, t_two + 0.6)
            if fade > 0:
                ctx.push_group()
                for i in range(5):
                    spear(ctx, lerp(300, 520, k) - i * 40, 520 + i * 10, 1.0, rot=0.9)
                ctx.pop_group_to_source()
                ctx.paint_with_alpha(fade)
        if t > t_two - 0.3:
            k = ease_out(prog(t, t_two - 0.3, t_two + 0.4))
            for i, gxp in enumerate((560, 400)):
                gx = lerp(-200, gxp, k)
                egyptian(ctx, gx, 580, 0.62, t, role="guard", seed=i, face=0.9, expr="frown", brows="angry",
                         larm=(0.3, 0.2), rarm=(-1.6, 0.3))
                spear(ctx, gx + 120, 650, 1.1, rot=1.2)
        ctx.restore()
        if t > t_peace:
            speech(ctx, 1250, 260, 520, 120, "Hi! I come in peace!", 56, tail=(-160, 90),
                   alpha=ease(prog(t, t_peace, t_peace + 0.2)) * (1 - prog(t, t_under, t_under + 0.3)))
        if t > t_under:
            ctx.save()
            ctx.translate(520, 230)
            speech(ctx, 0, 0, 340, 120, "", tail=(0, 90), alpha=ease(prog(t, t_under, t_under + 0.2)))
            for i, k in enumerate(("bird", "eye", "snake", "dog")):
                glyph(ctx, k, -110 + i * 72, 0, 0.9, INK)
            ctx.restore()
            pop_text(ctx, "???", 860, 340, 90, t - t_under - 0.5, RED)
    else:
        tt = t - t_carry
        walk = t * 1.6
        bx = lerp(700, 1700, ease(prog(tt, 0, D - t_carry)))
        for i, off in enumerate((-110, 110)):
            egyptian(ctx, bx + off, 580, 0.62, t, role="guard", seed=i, face=0.9, walk=walk + i * 0.5,
                     expr="flat", larm=(2.8, -0.2), rarm=(2.8, 0.2))
        ctx.save()
        ctx.translate(bx, 470)
        ctx.rotate(-math.pi / 2)
        doodle(ctx, 0, 0, 0.55, expr="flat", face=0.0, larm=(0.3, 0.2), rarm=(-0.3, -0.2),
               legs=(math.sin(t * 9) * 0.4, -math.sin(t * 9) * 0.4), blink=doodle_auto_blink(t))
        ctx.restore()
        ctx.restore()
        pop_text(ctx, "like a sack of potatoes", 960, 980, 64, t - cue("Like a sack"), WHITE, font=HAND_FONT,
                 outline=6)
    vignette(ctx, 0.3)


def sh_palace(ctx, t, D, cue):
    t_cols = cue("Huge columns")
    t_empty = cue("And it was empty")
    t_trip = cue("The Pharaoh had gone")
    ctx.save()
    if t < t_empty:
        cam(ctx, lerp(300, 960, ease(prog(t, 0, t_empty))), 500, lerp(1.2, 0.95, ease(prog(t, 0, t_empty))))
    elif t < t_trip:
        cam(ctx, 960, 470, lerp(0.95, 1.4, ease(prog(t, t_empty, t_empty + 1.2))))
    else:
        cam(ctx, lerp(960, 1580, ease(prog(t, t_trip, t_trip + 1.0))), lerp(470, 410, ease(prog(t, t_trip, t_trip + 1.0))),
            lerp(1.4, 2.2, ease(prog(t, t_trip, t_trip + 1.0))))
    palace_bg(ctx, t, window_boat=prog(t, t_trip, D))
    for i, x in enumerate((420, 1130)):
        egyptian(ctx, x, 520, 0.6, t, role="guard", seed=i, face=0.0, expr="flat", larm=(0.3, 0.2),
                 rarm=(-0.3, -0.2))
        spear(ctx, x + 70, 620, 1.0)
    if t > t_empty:
        # spotlight on the empty throne + cobweb gag
        warm_glow(ctx, 960, 440, 300, 0.4)
        if t > t_empty + 1.2:
            text(ctx, "*crickets*", 960, 300, 44, INK, font=HAND_FONT, outline=0, shadow=False,
                 alpha=ease(prog(t, t_empty + 1.2, t_empty + 1.5)))
    ctx.restore()
    if t > t_empty + 0.8:
        pop_text(ctx, "EMPTY THRONE!", 960, 980, 90, t - t_empty - 0.8, GOLD, hold=t_trip - t_empty - 0.6)
    if t > t_trip + 0.8:
        pop_text(ctx, "\"GONE UP THE NILE\"", 960, 980, 80, t - t_trip - 0.8, WHITE)
    vignette(ctx, 0.35)


def sh_crowned(ctx, t, D, cue):
    t_cap = cue("My red cap")
    t_gasp = cue("He gasped")
    t_turns = cue("Turns out")
    t_eyes = cue("In their eyes")
    t_five = cue("Within five minutes")
    t_phar = cue("I was the Pharaoh")
    if t < t_turns:
        ctx.save()
        cam(ctx, 900, 520, lerp(1.3, 1.5, ease(prog(t, 0, t_turns))))
        palace_bg(ctx, t)
        guy(ctx, 760, 560, 0.62, t, expr="o" if t < t_gasp else "worried", face=0.6, look=(1, 0),
            larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        pointing = t > t_gasp
        egyptian(ctx, 1120, 560, 0.62, t, role="priest", face=-0.8,
                 expr="flat" if t < t_cap else "shock", brows="up" if t > t_cap else None,
                 larm=(0.3, 0.2) if not pointing else (-2.8, 0.1), rarm=(-0.3, -0.2) if not pointing else (2.6, 0.3))
        if t > t_cap:
            circle(ctx, 770, 470, 120 + 6 * math.sin(t * 8))
            ctx.save()
            setc(ctx, GOLD)
            ctx.set_line_width(8)
            ctx.set_dash([24, 14])
            ctx.stroke()
            ctx.restore()
        ctx.restore()
        if t > t_gasp:
            burst(ctx, 1400, 230, 150, t - t_gasp, "GASP!", size=64, color=(1, 0.85, 0.3))
    elif t < t_five:
        tt = t - t_turns
        paper_lesson(ctx, "THE RED CROWN (DESHRET)", tt, RED)
        a = ease_out(prog(tt, 0.4, 1.0))
        # Deshret crown drawing
        ctx.save()
        ctx.translate(560, 560)
        ctx.scale(max(a, 1e-3), max(a, 1e-3))
        poly(ctx, [(-150, 120), (-150, -40), (60, -40), (60, -260), (130, -260), (130, 120)])
        fs(ctx, hexc("#c8282d"), lw=8)
        ctx.move_to(60, -60)
        ctx.curve_to(-40, -140, -120, -100, -90, -40)
        setc(ctx, GOLD)
        ctx.set_line_width(12)
        ctx.stroke()
        ctx.restore()
        text(ctx, "crown of Lower Egypt", 560, 760, 50, INK, font=HAND_FONT, outline=0, shadow=False, alpha=a)
        b = ease_out(prog(tt, 1.6, 2.2))
        text(ctx, "≈", 960, 520, 160, INK, font="DejaVu Sans", outline=0, shadow=False, alpha=b)
        ctx.save()
        ctx.translate(1380, 600)
        ctx.scale(max(b, 1e-3), max(b, 1e-3))
        cap_alone(ctx, 0, 0, 1.4)
        ctx.restore()
        text(ctx, "my cap", 1380, 760, 50, INK, font=HAND_FONT, outline=0, shadow=False, alpha=b)
        if t > t_eyes:
            pop_text(ctx, "\"SENT FROM THE SKY!\"", 960, 940, 74, t - t_eyes - 0.5, LAPIS, outline=0)
    else:
        tt = t - t_five
        ctx.save()
        cam(ctx, 960, 470, lerp(1.4, 1.0, ease(prog(tt, 0, 2.0))))
        palace_bg(ctx, t)
        # bowing court
        for i, x in enumerate((360, 520, 1400, 1560)):
            bow = ease(prog(tt, 1.0 + i * 0.15, 1.6 + i * 0.15))
            egyptian(ctx, x, 560, 0.55, t, role=["priest", "servant", "architect", "guard"][i], seed=i,
                     face=0.8 if x < 960 else -0.8, tilt=(0.4 if x < 960 else -0.4) * bow, expr="happy",
                     larm=(2.6, 0.2) if bow > 0.5 else (0.3, 0.2), rarm=(-2.6, -0.2) if bow > 0.5 else (-0.3, -0.2))
        hands = guy(ctx, 960, 400, 0.6, t, crown=ease_out(prog(tt, 0.3, 1.0)), expr="o" if t < t_phar else "grin",
                    face=0.0, larm=(1.0, -1.4), rarm=(-1.0, 1.4), show_legs=True, legs=(-0.3, 0.3))
        crook(ctx, hands["l"][0], hands["l"][1] - 10, 0.6, rot=-0.3)
        flail(ctx, hands["r"][0], hands["r"][1] - 10, 0.6, rot=0.3, t=t)
        ctx.restore()
        if t > t_phar:
            confetti(ctx, t - t_phar)
            pop_text(ctx, "PHARAOH?!", 960, 980, 120, t - t_phar, GOLD, rot=-0.03)
    vignette(ctx, 0.35)


def sh_perks(ctx, t, D, cue):
    t_fan = cue("Servants fanning")
    t_grapes = cue("Grapes.")
    t_cakes = cue("Honey cakes")
    t_cat = cue("A pet cat")
    t_sacred = cue("The ancient Egyptians loved cats")
    ctx.save()
    cam(ctx, 960, 470, 1.25)
    palace_bg(ctx, t)
    for i, x in enumerate((720, 1200)):
        rot = (0.35 if i == 0 else -0.35) + math.sin(t * 3 + i) * 0.25
        egyptian(ctx, x, 520, 0.55, t, role="servant", seed=i, face=0.8 if i == 0 else -0.8, expr="smile",
                 larm=(0.3, 0.2), rarm=(-1.4, 0.4) if i == 0 else (-0.3, -0.2))
        if t > t_fan - 0.3:
            feather_fan(ctx, x + (40 if i == 0 else -40), 560, 0.9, rot)
    hands = guy(ctx, 960, 400, 0.6, t, crown=1.0, expr="happy", face=0.0,
                larm=(1.0, -1.4), rarm=(-1.6, 0.4) if t > t_grapes else (-1.0, 1.4), legs=(-0.3, 0.3))
    if t > t_grapes:
        grapes(ctx, hands["r"][0], hands["r"][1] - 20, 0.9)
    if t > t_cakes:
        for k in range(3):
            honey_cake(ctx, 820 + k * 60, 640, 0.9)
    if t > t_cat:
        k = ease_out(prog(t, t_cat, t_cat + 0.6))
        cat(ctx, lerp(1300, 1040, k), 560, 0.7, t, look=-1)
    ctx.restore()
    if t > t_fan:
        pop_text(ctx, "BEING PHARAOH = AWESOME", 960, 120, 70, t - 0.3, GOLD, hold=t_sacred - 0.5)
    if t > t_sacred:
        pop_text(ctx, "CATS WERE SACRED", 960, 120, 80, t - t_sacred, WHITE)
        text(ctx, "(the cat goddess Bastet)", 960, 980, 50, WHITE, font=HAND_FONT, outline=5,
             alpha=ease(prog(t, t_sacred + 1, t_sacred + 1.4)))
    vignette(ctx, 0.35)


def blueprint(ctx, x, y, w, h, t, slide=0.0):
    ctx.save()
    ctx.translate(x, y)
    rrect(ctx, -w / 2, -h / 2, w, h, 10)
    fs(ctx, hexc("#efe0b8"), lw=7)
    for k in range(-int(w / 2) + 40, int(w / 2), 50):
        line(ctx, k, -h / 2 + 10, k, h / 2 - 10, 1.5, (0.6, 0.5, 0.35), 0.5)
    for k in range(-int(h / 2) + 40, int(h / 2), 50):
        line(ctx, -w / 2 + 10, k, w / 2 - 10, k, 1.5, (0.6, 0.5, 0.35), 0.5)
    poly(ctx, [(0, -h * 0.38), (-w * 0.32, h * 0.32), (w * 0.32, h * 0.32)])
    fs(ctx, None, lw=6, stroke=hexc("#2a3a7a"))
    line(ctx, 0, -h * 0.38, 0, h * 0.32, 3, hexc("#2a3a7a"))
    text(ctx, "146 cubits", w * 0.38, 0, 26, hexc("#2a3a7a"), font=HAND_FONT, outline=0, shadow=False)
    glyph_column(ctx, -w * 0.42, -h * 0.3, 4, 0.6, hexc("#2a3a7a"), seed=5)
    if slide > 0:
        pts = []
        for i in range(41):
            u = i / 40
            px, py = lerp2((0, -h * 0.36), (w * 0.32, h * 0.32), u)
            off = math.sin(u * math.pi * 3) * 30
            pts.append((px + off, py - abs(off) * 0.3))
        pts += [(w * 0.38, h * 0.33), (w * 0.44, h * 0.26)]
        polyline_part(ctx, pts, slide, 9, RED)
    ctx.restore()


def sh_meeting(ctx, t, D, cue):
    t_plans = cue("My architects")
    t_serious = cue("It was very serious")
    t_boring = cue("And very boring")
    t_pen = cue("They handed me")
    t_improve = cue("So I made")
    t_drew = cue("I drew a slide")
    t_giant = cue("A giant slide")
    if t < t_pen:
        ctx.save()
        cam(ctx, 960, 500, 1.15)
        palace_bg(ctx, t, throne=False)
        ctx.rectangle(560, 640, 800, 40)
        fs(ctx, hexc("#8a5a2b"), lw=6)
        for sx in (600, 1320):
            line(ctx, sx, 680, sx, 800, 14, hexc("#6b4428"))
        k = ease_out(prog(t, t_plans, t_plans + 0.8))
        ctx.save()
        ctx.translate(960, 640)
        ctx.scale(1, 0.35)
        blueprint(ctx, 0, -40, 700 * max(k, 0.05), 360, t)
        ctx.restore()
        for i, x in enumerate((470, 1450)):
            egyptian(ctx, x, 440, 0.62, t, role="architect", seed=i, face=0.8 if x < 960 else -0.8,
                     expr="flat", brows=None, larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        bored = t > t_boring
        guy(ctx, 960, 380, 0.55, t, crown=1.0, expr="flat" if bored else "o", face=0.0, look=(0, 1),
            blink=0.9 if bored and (t % 2) < 1.4 else doodle_auto_blink(t), larm=(0.3, 0.2), rarm=(-0.3, -0.2),
            show_legs=False)
        ctx.restore()
        for i, w in enumerate(("SERIOUS.", "PRECISE.", "BORING.")):
            tw = [t_serious, cue("Very precise"), t_boring][i]
            if t > tw:
                pop_text(ctx, w, 480 + i * 480, 980, 76, t - tw, WHITE, hold=t_pen - tw - 0.2)
        if bored:
            text(ctx, "zzz", 1100, 220, 60, WHITE, font=HAND_FONT, outline=5, alpha=0.5 + 0.5 * math.sin(t * 4))
    else:
        tt = t - t_pen
        bg_fill(ctx, hexc("#6b4428"))
        for k in range(0, H, 60):
            line(ctx, 0, k, W, k + 30, 3, hexc("#5a3a1a"))
        blueprint(ctx, 960, 540, 1300, 860, t, slide=ease(prog(t, t_drew, t_giant + 2.0)))
        # reed pen following the slide
        if t > t_improve:
            k = ease(prog(t, t_drew, t_giant + 2.0))
            px = 960 + lerp(0, 1300 * 0.4, k)
            py = 540 + lerp(-860 * 0.36, 860 * 0.3, k) + math.sin(k * math.pi * 3) * 20
            line(ctx, px, py, px + 220, py - 260, 12, hexc("#c9a46a"))
            line(ctx, px, py, px + 30, py - 36, 6, INK)
        if t > t_improve:
            pop_text(ctx, "ONE SMALL IMPROVEMENT", 960, 70, 64, t - t_improve, RED, outline=6)
        if t > t_giant + 1.6:
            for i, x in enumerate((280, 1640)):
                egyptian(ctx, x, 760, 0.5, t, role="architect", seed=i, face=0.8 if x < 960 else -0.8,
                         expr="shock", brows="up", larm=(2.4, 0.4), rarm=(-2.4, -0.4))
    vignette(ctx, 0.35)


def sh_build(ctx, t, D, cue):
    t_no = cue("Nobody tells you no")
    t_week = cue("Within a week")
    t_slaves = cue("And by the way")
    t_village = cue("Archaeologists found")
    t_paid = cue("They were skilled")
    if t < t_slaves:
        ctx.save()
        cam(ctx, 1150, 500, 0.85)
        desert_bg(ctx, t, pyramids=False)
        pts = slide_path(1150, 820, 900, 640)
        pyramid(ctx, 1150, 820, 900, 640)
        draw_slide(ctx, pts, ease(prog(t, t_week, t_slaves + 0.2)), t)
        for i in range(10):
            ph = (t * 0.05 + i / 10) % 1
            x = lerp(-200, 800, ph)
            wy = 800 - i % 3 * 10
            egyptian(ctx, x, wy, 0.35, t, role="worker", seed=i, face=0.9, walk=t * 1.5 + i,
                     expr="smile", larm=(2.7, 0.2), rarm=(-2.7, -0.2))
            ctx.rectangle(x - 45, wy - 120, 90, 50)
            fs(ctx, LIME_D, lw=4)
        guy(ctx, 260, 620, 0.5, t, crown=1.0, expr="grin" if t > t_no else "smile", face=0.6,
            larm=(0.3, 0.2), rarm=(-2.2, 0.5) if t > t_week else (-0.3, -0.2))
        ctx.restore()
        if t > t_no:
            pop_text(ctx, "NOBODY SAYS NO.", 960, 120, 84, t - t_no, GOLD, hold=t_week - t_no + 0.8)
    else:
        tt = t - t_slaves
        paper_lesson(ctx, "MYTH: SLAVES BUILT THE PYRAMIDS", tt, RED)
        if tt > 0.4 and t < t_village + 0.5:
            a = back_out(prog(tt, 0.4, 0.8), 2) * (1 - prog(t, t_village, t_village + 0.5))
            ctx.save()
            ctx.translate(960, 420)
            ctx.scale(max(a, 1e-3), max(a, 1e-3))
            text(ctx, "SLAVES?", 0, 0, 150, INK, outline=0, shadow=False)
            line(ctx, -320, 60, 320, -60, 22, RED)
            line(ctx, -320, -60, 320, 60, 22, RED)
            ctx.restore()
        if t > t_village:
            for k in range(4):
                mud_house(ctx, 300 + k * 180, 560, 0.8)
            text(ctx, "workers' village at Giza", 560, 640, 48, INK, font=HAND_FONT, outline=0, shadow=False,
                 alpha=ease(prog(t, t_village, t_village + 0.4)))
        if t > t_paid:
            items = [("BREAD", "bread"), ("BEER", "beer"), ("DOCTORS", "doc")]
            for i, (lab, kind) in enumerate(items):
                tc = t_paid + 0.5 + i * 0.6
                if t < tc:
                    continue
                x = 1180 + i * 230
                a = back_out(clamp((t - tc) / 0.3))
                ctx.save()
                ctx.translate(x, 470)
                ctx.scale(a, a)
                if kind == "bread":
                    ellipse(ctx, 0, 0, 70, 40)
                    fs(ctx, hexc("#d9a24a"), lw=6)
                elif kind == "beer":
                    ctx.move_to(-40, -60); ctx.curve_to(-70, 0, -40, 70, 0, 70); ctx.curve_to(40, 70, 70, 0, 40, -60)
                    ctx.close_path()
                    fs(ctx, hexc("#b8763f"), lw=6)
                else:
                    ctx.rectangle(-18, -60, 36, 120)
                    ctx.rectangle(-60, -18, 120, 36)
                    fs(ctx, RED, lw=5)
                ctx.restore()
                text(ctx, lab, x, 580, 44, INK, outline=0, shadow=False, alpha=a)
            ctx.save()
            ctx.translate(960, 820)
            ctx.rotate(-0.05)
            rrect(ctx, -380, -70, 760, 140, 14)
            fs(ctx, None, lw=10, stroke=hexc("#2f7a3a"))
            text(ctx, "PAID, SKILLED WORKERS", 0, 0, 64, hexc("#2f7a3a"), outline=0, shadow=False)
            ctx.restore()
    vignette(ctx, 0.3)


def slide_world(ctx, t, rider_frac=None, crowd_cheer=0.0, hero_kw=None):
    desert_bg(ctx, t, pyramids=False)
    pts = slide_path(1150, 820, 900, 640)
    pyramid(ctx, 1150, 820, 900, 640)
    draw_slide(ctx, pts, 1.0, t)
    for i in range(20):
        x = 1500 + (i % 10) * 70
        y = 860 + (i // 10) * 70
        jump = abs(math.sin(t * 6 + i)) * 20 * crowd_cheer
        egyptian(ctx, x, y - jump, 0.24, t, role="worker", seed=i, face=-0.5, expr="laugh" if crowd_cheer else "smile",
                 larm=(2.6, 0.2) if crowd_cheer else (0.3, 0.2), rarm=(-2.6, -0.2) if crowd_cheer else (-0.3, -0.2),
                 show_legs=False)
    return pts


def sh_slide(ctx, t, D, cue):
    t_city = cue("The whole city")
    t_climb = cue("I climbed")
    t_slip = cue("It turns out")
    t_f1 = cue("Faster.")
    t_F = cue("FASTER!")
    if t < t_slip:
        ctx.save()
        k = ease(prog(t, t_climb, t_slip))
        cam(ctx, lerp(1300, 1150, k), lerp(600, 240, k), lerp(0.75, 1.5, k))
        slide_world(ctx, t, crowd_cheer=1.0 if t > t_city else 0.0)
        apex = (1150, 180)
        if t < t_climb:
            guy(ctx, 1500, 640, 0.36, t, crown=1.0, expr="grin", face=-0.5, larm=(0.3, 0.2), rarm=(-2.4, 0.3))
        else:
            # climbing the steps up the face
            u = ease(prog(t, t_climb, t_climb + 3.0))
            gx, gy = lerp(1500, apex[0] + 30, u), lerp(640, apex[1] - 40, u)
            sitting = u >= 1
            guy(ctx, gx, gy, 0.36, t, crown=1.0, expr="grin" if sitting else "worried", face=0.6,
                larm=(0.3, 0.2) if not sitting else (2.6, 0.3), rarm=(-0.3, -0.2) if not sitting else (-2.6, -0.3),
                legs=(-1.3, -1.1) if sitting else (math.sin(t * 9) * 0.5, -math.sin(t * 9) * 0.5))
        ctx.restore()
        if t > t_climb + 3.0:
            speech(ctx, 1250, 200, 380, 110, "Here we go!", 56, tail=(-60, 80),
                   alpha=ease(prog(t, t_climb + 3.0, t_climb + 3.2)))
    else:
        u = ease_in(prog(t, t_slip, D)) * 0.97
        ctx.save()
        pts = slide_path(1150, 820, 900, 640)
        px, py, ang = point_on(pts, u)
        cam(ctx, px, py - 60, 1.6, rot=-ang * 0.15, shake=3 + 10 * u, t=t)
        slide_world(ctx, t, crowd_cheer=1.0)
        ctx.save()
        ctx.translate(px, py - 34)
        ctx.rotate(ang * 0.6)
        guy(ctx, 0, -120, 0.36, t, crown=1.0, expr="laugh" if u < 0.4 else "shock", face=0.6, larm=(2.6, 0.4),
            rarm=(-2.6, -0.4), legs=(-1.4, -1.2), cap_off=0.0)
        ctx.restore()
        for k in range(6):
            line(ctx, px - 60 - k * 30, py - 150 + k * 22, px - 260 - k * 40, py - 190 + k * 22, 5, WHITE, 0.7)
        ctx.restore()
        # speedometer
        ctx.save()
        ctx.translate(1700, 900)
        circle(ctx, 0, 0, 120)
        fs(ctx, (0.05, 0.05, 0.08, 0.8), lw=6, stroke=GOLD)
        a = math.pi * (0.8 + 1.4 * u)
        line(ctx, 0, 0, math.cos(a) * 90, math.sin(a) * 90, 9, RED)
        text(ctx, f"{int(10 + 90 * u)} km/h", 0, 60, 30, WHITE, outline=0, shadow=False)
        ctx.restore()
        for i, (tc, lab, size) in enumerate(((t_f1, "Faster.", 70), (cue("Faster.") + 0.9, "FASTER!", 90),
                                             (t_F, "FASTER!!!", 120))):
            pass
        if t > t_f1:
            pop_text(ctx, "faster.", 400, 200, 70, t - t_f1, WHITE, font=HAND_FONT, outline=6, hold=0.8)
        if t > t_f1 + 0.9:
            pop_text(ctx, "Faster!", 500, 300, 90, t - t_f1 - 0.9, GOLD, hold=0.8)
        if t > t_F:
            pop_text(ctx, "FASTER!!!", 960, 160, 140, t - t_F, RED, rot=-0.05)
    vignette(ctx, 0.35)


def sh_crash(ctx, t, D, cue):
    t_horses = cue("The horses panicked")
    t_driver = cue("The driver screamed")
    t_gallop = cue("And we went galloping")
    t_land = 2.2
    if t < t_land:
        # flying over the crowd
        u = prog(t, 0, t_land)
        ctx.save()
        cam(ctx, lerp(1300, 2200, u), 560, 0.9)
        desert_bg(ctx, t, pyramids=False)
        pyramid(ctx, 1150, 820, 900, 640)
        draw_slide(ctx, slide_path(1150, 820, 900, 640), 1.0, t)
        for i in range(14):
            egyptian(ctx, 1500 + i * 70, 860, 0.24, t, role="worker", seed=i, face=0.0, expr="shock",
                     look=(0, -1), larm=(2.6, 0.2), rarm=(-2.6, -0.2), show_legs=False)
        gx = lerp(1680, 2450, u)
        gy = 700 - math.sin(u * math.pi) * 380 + u * 100
        guy(ctx, gx, gy, 0.4, t, crown=1.0, expr="shock", face=0.0, tilt=t * 5, larm=(2.4, 0.5), rarm=(-2.4, -0.5))
        chariot(ctx, 2400, 960, 0.6, t, moving=False)
        ctx.restore()
        pop_text(ctx, "WHEEEE!", 960, 140, 100, t - 0.2, WHITE)
        return
    tt = t - t_land
    # galloping chariot, background scrolling: desert -> market -> camel -> river
    scroll = tt * 900
    ctx.save()
    cam(ctx, 960, 560, 1.0, shake=6, t=t)
    egypt_sky(ctx, t)
    ctx.save()
    ctx.translate(-scroll * 0.2, 0)
    for k in range(-1, 8):
        pyramid(ctx, 400 + k * 900, 720, 600, 380)
    ctx.restore()
    ctx.rectangle(-500, 720, 3000, 800)
    fs(ctx, SAND, lw=6)
    ctx.save()
    ctx.translate(-scroll, 0)
    for k in range(4):
        market_stall(ctx, 2600 + k * 380, 900, 1.0, [RED, LAPIS, hexc("#2bb36b"), GOLD][k])
    camel(ctx, 4700, 850, 1.1, t)
    for k in range(10):
        palm(ctx, 800 + k * 700, 880, 260, t)
    ctx.restore()
    if tt > D - t_land - 2.5:
        k = prog(tt, D - t_land - 2.5, D - t_land)
        ctx.rectangle(lerp(1950, 1150, k), 720, 2000, 800)
        fs(ctx, NILE, lw=6)

    def rider(c):
        guy(c, -95, -300, 0.36, t, crown=1.0, expr="shock", face=0.9, tilt=math.sin(t * 14) * 0.1,
            larm=(2.6, 0.3), rarm=(-2.6, -0.3), show_legs=False)
    chariot(ctx, 560, 990, 0.95, t, moving=True, rider=rider)
    for k in range(8):
        ph = (t * 1.5 + k / 8) % 1
        circle(ctx, 400 - ph * 500, 960 - ph * 60, 30 + ph * 60)
        setc(ctx, SAND_L, 0.7 * (1 - ph))
        ctx.fill()
    ctx.restore()
    if t > t_horses:
        pop_text(ctx, "NEEEIGH!", 1500, 220, 90, t - t_horses, GOLD, hold=t_driver - t_horses)
    if t > t_driver:
        pop_text(ctx, "AAAAH!", 1450, 220, 110, t - t_driver, RED, hold=t_gallop - t_driver)
    if t > t_gallop + 1.0:
        pop_text(ctx, "MARKET!", 1500, 200, 70, t - t_gallop - 1.0, WHITE, hold=1.0)
    if t > t_gallop + 2.6:
        pop_text(ctx, "CAMEL!", 1500, 200, 80, t - t_gallop - 2.6, WHITE, hold=1.0)
    vignette(ctx, 0.35)


def sh_nile(ctx, t, D, cue):
    t_terrible = cue("something terrible")
    t_rising = cue("The river was rising")
    level = ease(prog(t, t_rising, D))
    ctx.save()
    cam(ctx, lerp(700, 860, ease(prog(t, 0, D))), lerp(620, 600, ease(prog(t, 0, D))), lerp(1.4, 1.15, ease(prog(t, 0, D))))
    nile_bg(ctx, t, level=level * 0.8)
    chariot(ctx, 1150, 860, 0.5, t, moving=False, driver=True)
    guy(ctx, 960, 690, 0.42, t, crown=1.0, expr="smile" if t < t_terrible else "shock", face=-0.8, look=(-1, 0.3),
        larm=(0.3, 0.2), rarm=(-0.3, -0.2) if t < t_terrible else (2.4, 0.3), brows="worried" if t > t_terrible else None)
    ctx.restore()
    if t > t_rising:
        # water level gauge
        ctx.save()
        ctx.translate(1700, 540)
        rrect(ctx, -40, -300, 80, 600, 20)
        fs(ctx, (1, 1, 1, 0.85), lw=6)
        h = 560 * (0.25 + 0.7 * level)
        rrect(ctx, -30, 290 - h, 60, h, 14)
        fs(ctx, NILE, lw=0)
        line(ctx, -60, -170, 60, -170, 6, RED)
        ctx.restore()
        pop_text(ctx, "TOO FAST!", 960, 140, 110, t - cue("Way too fast"), RED)
    vignette(ctx, 0.35)


def sh_nilefact(ctx, t, D, cue):
    t_inund = cue("The Egyptians called it")
    t_mud = cue("The water left behind")
    t_big = cue("But this year")
    t_farms = cue("It was heading")
    t_food = cue("Everyone's food")
    if t < t_big:
        paper_lesson(ctx, "THE NILE FLOOD", t, LAPIS)
        # yearly cycle: river swells, leaves black mud, wheat grows
        k1 = ease(prog(t, 0.5, 2.5))
        ctx.rectangle(200, 600, 1520, 300)
        fs(ctx, SAND, lw=5)
        ctx.rectangle(200, 600, 300 + 500 * k1 * (1 - ease(prog(t, t_mud, t_mud + 1.5))), 300)
        fs(ctx, NILE, lw=5)
        if t > t_mud:
            km = ease(prog(t, t_mud, t_mud + 1.5))
            ctx.rectangle(500, 600, 500 * km, 300)
            fs(ctx, MUD, lw=5)
            for k in range(int(12 * ease(prog(t, t_mud + 1.5, t_mud + 3.0)))):
                x = 520 + k * 40
                line(ctx, x, 600, x, 520, 5, FIELD_D)
                ellipse(ctx, x, 512, 6, 14)
                setc(ctx, hexc("#d9a020"))
                ctx.fill()
        if t > t_inund:
            pop_text(ctx, "\"THE INUNDATION\"", 960, 260, 80, t - t_inund, LAPIS, outline=0)
            text(ctx, "every summer, a GOOD thing", 960, 350, 50, INK, font=HAND_FONT, outline=0, shadow=False,
                 alpha=ease(prog(t, t_inund + 1, t_inund + 1.4)))
        if t > t_mud + 1.5:
            text(ctx, "black mud = perfect for wheat", 1300, 980, 50, INK, font=HAND_FONT, outline=0, shadow=False,
                 alpha=ease(prog(t, t_mud + 1.5, t_mud + 1.9)))
    else:
        tt = t - t_big
        ctx.save()
        cam(ctx, 1300, 720, 0.85)
        nile_bg(ctx, t, level=1.0, flood_reach=ease(prog(tt, 0.5, D - t_big)))
        for k in range(3):
            ph = (t * 1.2 + k / 3) % 1
            x = lerp(1000, 1900, ph)
            poly(ctx, [(x, 990), (x + 60, 1020), (x, 1050)])
            fs(ctx, RED, lw=0, alpha=1 - ph)
        for i in range(5):
            egyptian(ctx, 1950 + i * 110, 600, 0.3, t, role="worker", seed=i, face=-0.8, expr="shock",
                     larm=(2.6, 0.2), rarm=(-2.6, -0.2))
        ctx.restore()
        pop_text(ctx, "WAY TOO BIG!", 960, 120, 110, tt - 0.2, RED, hold=t_farms - t_big)
        if t > t_farms:
            pop_text(ctx, "FARMS + VILLAGE IN DANGER", 960, 120, 76, t - t_farms, WHITE)
        if t > t_food:
            pop_text(ctx, "A WHOLE YEAR OF FOOD!", 960, 980, 84, t - t_food, GOLD)
    vignette(ctx, 0.35)


def sh_idea(ctx, t, D, cue):
    t_slide = cue("My slide!")
    t_if = cue("If water can slide")
    t_what = cue("What if we built")
    t_chan = cue("Channels!")
    t_carry = cue("To carry the water")
    if t < t_if:
        ctx.save()
        cam(ctx, 960, 600, 1.5)
        nile_bg(ctx, t, level=1.0)
        guy(ctx, 960, 690, 0.42, t, crown=1.0, expr="flat" if t < t_slide else "grin", face=-0.6, look=(-1, 0.3),
            larm=(0.3, 0.2), rarm=(-0.3, -0.2) if t < t_slide else (-2.7, 0.0))
        ctx.restore()
        k = ease_out(prog(t, t_slide - 0.4, t_slide))
        if k > 0:
            ctx.save()
            ctx.translate(1000, 230)
            ctx.scale(k, k)
            warm_glow(ctx, 0, 0, 200, 0.7)
            circle(ctx, 0, -10, 60)
            fs(ctx, (1, 0.92, 0.4), lw=6)
            ctx.rectangle(-26, 45, 52, 40)
            fs(ctx, hexc("#9aa0a8"), lw=5)
            ctx.restore()
            pop_text(ctx, "MY SLIDE!", 960, 980, 110, t - t_slide, GOLD)
    else:
        tt = t - t_if
        paper_lesson(ctx, "THE BIG IDEA", tt, hexc("#2f7a3a"))
        # left: water down a pyramid slide; right: channels on flat ground
        pyramid(ctx, 500, 820, 520, 380)
        pts = slide_path(500, 820, 520, 380, n=40)
        draw_slide(ctx, pts, 1.0, t)
        polyline_part(ctx, pts, (tt * 0.6) % 1.2, 16, NILE)
        if t > t_what:
            ka = ease(prog(t, t_what, t_what + 0.6))
            line(ctx, 860, 600, 860 + 120 * ka, 600, 12, INK)
            poly(ctx, [(980, 580), (1010, 600), (980, 620)])
            fs(ctx, INK, lw=0, alpha=ka)
            # river + channels into fields
            ctx.rectangle(1080, 380, 120, 520)
            fs(ctx, NILE, lw=5)
            for r in range(3):
                for c in range(3):
                    ctx.rectangle(1300 + c * 170, 400 + r * 170, 150, 150)
                    fs(ctx, lerpc(hexc("#d8c070"), FIELD, ease(prog(t, t_carry + 0.5 + c * 0.4, t_carry + 1.5 + c * 0.4))), lw=4)
            for r in range(3):
                path = [(1200, 470 + r * 170), (1810, 470 + r * 170)]
                polyline_part(ctx, path, 1.0, 22, MUD)
                polyline_part(ctx, path, ease(prog(t, t_chan, t_carry + 2.0)), 14, NILE)
        if t > t_chan:
            pop_text(ctx, "CHANNELS!", 1500, 280, 90, t - t_chan, LAPIS, outline=0)
    vignette(ctx, 0.3)


def sh_rescue(ctx, t, D, cue):
    t_dig = cue("Dig!")
    t_every = cue("Farmers, workers")
    t_night = cue("We dug all night")
    if t < t_night:
        ctx.save()
        cam(ctx, 1200, 640, 1.0)
        nile_bg(ctx, t, level=1.0, sunset=ease(prog(t, 0, t_night)), channels=0.0)
        # channels being dug
        for path in channel_paths():
            polyline_part(ctx, path, ease(prog(t, t_every, t_night + 1)), 34, MUD)
        guy(ctx, 860, 520, 0.4, t, crown=1.0, expr="grin", face=0.6, larm=(0.3, 0.2), rarm=(-2.7, 0.0))
        if t > t_every - 0.5:
            roles = ["worker", "worker", "guard", "priest", "worker", "architect", "worker", "worker"]
            for i, role in enumerate(roles):
                x = 1000 + i * 120
                dig = math.sin(t * 6 + i)
                egyptian(ctx, x, 560 + (i % 3) * 110, 0.32, t, role=role, seed=i, face=-0.4, expr="grin",
                         larm=(0.6 + 0.4 * dig, 0.8), rarm=(-0.2 + 0.4 * dig, 0.8))
                line(ctx, x - 20, 640 + (i % 3) * 110 + dig * 10, x - 70, 690 + (i % 3) * 110, 6, hexc("#8a5a2b"))
        ctx.restore()
        if t > t_dig:
            pop_text(ctx, "DIG!", 600, 200, 130, t - t_dig, GOLD, hold=t_every - t_dig + 1.2)
        if t > cue("Everybody dig"):
            pop_text(ctx, "EVERYBODY DIG!", 1200, 200, 100, t - cue("Everybody dig"), WHITE, hold=t_night - t_every)
    else:
        tt = t - t_night
        ctx.save()
        cam(ctx, 1000, 600, 1.2)
        nile_bg(ctx, t, level=1.0, night=1.0)
        for i in range(5):
            torch(ctx, 400 + i * 300, 600, t + i, rot=0.1, s=0.9)
        shaduf(ctx, 900, 720, 1.0, t)
        dig = math.sin(t * 6)
        guy(ctx, 1500, 560, 0.38, t, crown=1.0, expr="grin", face=-0.4, larm=(0.6 + 0.4 * dig, 0.8),
            rarm=(-0.2 + 0.4 * dig, 0.8))
        line(ctx, 1480, 640 + dig * 10, 1430, 700, 6, hexc("#8a5a2b"))
        egyptian(ctx, 1010, 560, 0.42, t, role="worker", seed=1, face=-0.8, expr="grin",
                 larm=(2.4 + 0.3 * math.sin(t * 2), 0.2), rarm=(-2.4, -0.2))
        for i in range(6):
            dig = math.sin(t * 6 + i)
            x = 1150 + i * 110
            egyptian(ctx, x, 600 + (i % 2) * 80, 0.32, t, role="worker", seed=i, face=-0.4, expr="grin",
                     larm=(0.6 + 0.4 * dig, 0.8), rarm=(-0.2 + 0.4 * dig, 0.8))
        ctx.restore()
        pop_text(ctx, "THE SHADUF", 960, 120, 90, tt - 2.0, GOLD)
        text(ctx, "a counterweighted lever for lifting water (a real Egyptian tool)", 960, 990, 44, WHITE,
             font=HAND_FONT, outline=5, alpha=ease(prog(tt, 2.8, 3.2)))
    vignette(ctx, 0.4)


def sh_saved(ctx, t, D, cue):
    t_turn = cue("It turned")
    t_spread = cue("It spread out")
    t_wild = cue("The crowd went wild")
    t_lift = cue("They lifted me")
    t_best = cue("Best day")
    if t < t_wild:
        ctx.save()
        cam(ctx, 1300, 720, 0.85)
        nile_bg(ctx, t, level=1.0, sunset=1 - ease(prog(t, 0, 3)), channels=ease(prog(t, 0.5, t_spread + 1.0)),
                fields_wet=ease(prog(t, t_spread, t_wild)))
        ctx.restore()
        if t > t_turn:
            pop_text(ctx, "IT WORKS!", 960, 120, 110, t - t_turn, GOLD)
        if t > t_spread + 1.0:
            pop_text(ctx, "VILLAGE: SAFE", 1400, 980, 80, t - t_spread - 1.0, hexc("#2f7a3a"), outline=8)
    else:
        tt = t - t_wild
        ctx.save()
        cam(ctx, 960, 560, 1.1)
        nile_bg(ctx, t, level=0.9, channels=1.0, fields_wet=1.0)
        lift = ease_out(prog(t, t_lift, t_lift + 0.6))
        for i in range(7):
            x = 660 + i * 100
            jump = abs(math.sin(t * 6 + i)) * 20
            egyptian(ctx, x, 620 - jump, 0.36, t, role=["worker", "guard", "worker", "priest", "worker", "architect",
                                                          "worker"][i], seed=i, face=0.0, expr="laugh",
                     larm=(2.8, 0.1), rarm=(-2.8, -0.1))
        bob = math.sin(t * 6) * 15
        guy(ctx, 960, lerp(560, 330, lift) + bob * lift, 0.42, t, crown=1.0, expr="laugh", face=0.0,
            larm=(2.6, 0.3), rarm=(-2.6, -0.3))
        ctx.restore()
        confetti(ctx, tt)
        pop_text(ctx, "HOORAY!", 960, 130, 120, tt - 0.2, GOLD, hold=t_best - t_wild)
        if t > t_best:
            pop_text(ctx, "BEST. DAY. EVER.", 960, 980, 100, t - t_best, WHITE)
    vignette(ctx, 0.3)


def throne_hero(ctx, t, crown=1.0, **kw):
    kw.setdefault("larm", (1.0, -1.4))
    kw.setdefault("rarm", (-1.0, 1.4))
    return guy(ctx, 960, 400, 0.6, t, crown=crown, legs=(-0.3, 0.3), **kw)


def sh_pharaoh(ctx, t, D, cue):
    t_walk = cue("He walked into")
    t_silent = cue("The room went silent")
    t_cake = cue("Somebody dropped")
    ctx.save()
    if t < t_walk:
        cam(ctx, 1500, 520, 1.3)
    elif t < t_silent:
        cam(ctx, lerp(1500, 1150, ease(prog(t, t_walk, t_silent))), 500, lerp(1.3, 1.05, ease(prog(t, t_walk, t_silent))))
    else:
        cam(ctx, 1150, 500, 1.05)
    palace_bg(ctx, t)
    hands = throne_hero(ctx, t, expr="happy" if t < t_walk + 2 else "shock", face=0.6 if t > t_walk else 0.0,
                        rarm=(-1.6, 0.4), look=(1, 0) if t > t_walk + 2 else (0, 0))
    grapes(ctx, hands["r"][0], hands["r"][1] - 20, 0.9)
    k = ease(prog(t, 0.3, t_walk + 2.5))
    px = lerp(2300, 1450, k)
    egyptian(ctx, px, 520, 0.68, t, role="pharaoh", face=-0.8, walk=t * 1.3 if k < 1 else None,
             expr="flat" if t < t_walk + 2 else "frown", brows="angry" if t > t_walk + 2 else None,
             larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    servant_x = 1700
    egyptian(ctx, servant_x, 540, 0.55, t, role="servant", seed=3, face=-0.8,
             expr="smile" if t < t_silent else "shock", larm=(0.3, 0.2), rarm=(-1.5, 0.4) if t < t_cake else (-0.3, -0.2))
    if t < t_cake:
        honey_cake(ctx, servant_x - 100, 640, 1.0)
    else:
        fall = ease_in(prog(t, t_cake, t_cake + 0.5))
        honey_cake(ctx, servant_x - 100, lerp(640, 760, fall), 1.0)
    ctx.restore()
    if t > 0.3:
        pop_text(ctx, "THE REAL PHARAOH", 1400, 130, 80, t - 0.5, GOLD, hold=t_walk + 1.0)
    if t > t_silent:
        text(ctx, "...", 960, 160, 120, WHITE, outline=8, alpha=ease(prog(t, t_silent, t_silent + 0.3)) * (1 - prog(t, t_cake, t_cake + 0.2)))
    if t > t_cake + 0.4:
        pop_text(ctx, "*plop*", 1500, 900, 80, t - t_cake - 0.4, WHITE, font=HAND_FONT, outline=6)
    vignette(ctx, 0.4)


def sh_judgement(ctx, t, D, cue):
    t_adv = cue("But then his advisers")
    t_list = cue("The slide, the chariot")
    t_look = cue("The Pharaoh looked")
    t_smile = cue("And then, he smiled")
    ctx.save()
    if t < t_look:
        cam(ctx, 1150, 500, 1.05)
    else:
        cam(ctx, lerp(1150, 1440, ease(prog(t, t_look, t_look + 1.5))), lerp(500, 470, ease(prog(t, t_look, t_look + 1.5))),
            lerp(1.05, 2.4, ease(prog(t, t_look, t_smile))))
    palace_bg(ctx, t)
    throne_hero(ctx, t, expr="worried", face=0.6, look=(1, 0), brows="worried")
    sweat(ctx, 1010, 290, 0.8, t)
    smiled = t > t_smile
    egyptian(ctx, 1450, 520, 0.68, t, role="pharaoh", face=-0.8, expr="grin" if smiled else "frown",
             brows=None if smiled else "angry", larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    if t > t_adv - 0.5:
        k = ease_out(prog(t, t_adv - 0.5, t_adv + 0.3))
        egyptian(ctx, lerp(2200, 1750, k), 540, 0.55, t, role="priest", face=-0.8, expr="grin",
                 larm=(-1.8, 0.2), rarm=(-0.3, -0.2))
    ctx.restore()
    if t_list < t < t_look + 0.5:
        # scroll with the story told in pictures
        ka = ease_out(prog(t, t_list, t_list + 0.4))
        ctx.save()
        ctx.translate(960, 900)
        ctx.scale(1, max(ka, 1e-3))
        rrect(ctx, -620, -110, 1240, 220, 16)
        fs(ctx, hexc("#f2e2b8"), lw=6)
        icons = ["slide", "chariot", "flood", "channels"]
        for i, ic in enumerate(icons):
            x = -460 + i * 310
            a = ease(prog(t, t_list + 0.4 + i * 0.6, t_list + 0.7 + i * 0.6))
            if a <= 0:
                continue
            if ic == "slide":
                pyramid(ctx, x, 60, 160, 110)
                line(ctx, x, -50, x + 90, 50, 10, hexc("#ff9a2e"))
            elif ic == "chariot":
                circle(ctx, x - 20, 40, 34)
                fs(ctx, hexc("#8a5a2b"), lw=5)
                rrect(ctx, x - 50, -20, 90, 40, 6)
                fs(ctx, GOLD, lw=5)
            elif ic == "flood":
                for k in range(3):
                    glyph(ctx, "water", x, -20 + k * 30, 1.4, NILE)
            else:
                for k in range(3):
                    line(ctx, x - 70, -30 + k * 30, x + 70, -30 + k * 30, 12, NILE)
                ctx.rectangle(x - 70, -50, 140, 100)
                fs(ctx, None, lw=4, stroke=FIELD_D)
            if i < 3:
                text(ctx, "→", x + 155, 0, 60, INK, font="DejaVu Sans", outline=0, shadow=False, alpha=a)
        ctx.restore()
    if t > t_look + 2.0 and not smiled:
        text(ctx, "...", 960, 160, 120, WHITE, outline=8)
    if smiled:
        pop_text(ctx, "HE SMILED!", 960, 110, 110, t - t_smile, GOLD)
    vignette(ctx, 0.4)


def sh_reward(ctx, t, D, cue):
    t_back = cue("Then he took")
    t_fair = cue("Which was fair")
    ctx.save()
    cam(ctx, 1150, 470, 1.25)
    palace_bg(ctx, t)
    crown_k = 1.0 - ease(prog(t, t_back, t_back + 1.0))
    guy(ctx, 1000, 560, 0.6, t, crown=crown_k if crown_k > 0.02 else 0.0, expr="happy" if t < t_back else "flat",
        face=0.6, larm=(0.3, 0.2), rarm=(-0.3, -0.2), blush=t < t_back)
    # golden collar on the hero
    a = ease_out(prog(t, 0.6, 1.4))
    if a > 0:
        ctx.save()
        ctx.translate(1000, lerp(380, 560, a))
        ctx.scale(0.6, 0.6)
        gold_collar(ctx, "body")
        ctx.restore()
    egyptian(ctx, 1450, 520, 0.68, t, role="pharaoh", face=-0.8, expr="grin",
             larm=(-1.6, 0.4) if t < 1.6 or t_back < t < t_back + 1.2 else (0.3, 0.2), rarm=(-0.3, -0.2))
    if t_back < t < t_back + 1.2:
        u = ease(prog(t, t_back, t_back + 1.0))
        hero_crown(ctx, lerp(1000, 1450, u), lerp(560, 520, u) - math.sin(u * math.pi) * 100, 0.6, t, 1.0 - 0.0 * u)
    ctx.restore()
    if t > 1.2:
        pop_text(ctx, "ROYAL INVENTOR OF EGYPT", 960, 120, 84, t - 1.2, GOLD, hold=t_back - 1.4)
    if t > t_fair:
        pop_text(ctx, "fair.", 960, 980, 90, t - t_fair, WHITE, font=HAND_FONT, outline=7)
    vignette(ctx, 0.35)


def sh_return(ctx, t, D, cue):
    t_glow = cue("The red button was glowing")
    t_wave = cue("I waved goodbye")
    t_back = cue("I was back in my bedroom")
    if t < t_back:
        ctx.save()
        cam(ctx, 1150, 470, 1.25)
        palace_bg(ctx, t)
        hands = guy(ctx, 1000, 560, 0.6, t, expr="o" if t < t_wave else "smile", face=0.6 if t < t_wave else 0.0,
                    larm=(0.3, 0.2) if t < t_wave else (2.6 + 0.3 * math.sin(t * 10), 0.3),
                    rarm=(-1.2, -0.6))
        ctx.save()
        ctx.translate(1000, 560)
        ctx.scale(0.6, 0.6)
        gold_collar(ctx, "body")
        ctx.restore()
        golden_box(ctx, hands["r"][0] + 10, hands["r"][1] - 10, 0.28, t, glow=1.0 if t > t_glow else 0.4,
                   buzz=1.0, pressed=1.0 if t > t_wave + 2.0 else 0.0)
        egyptian(ctx, 1450, 520, 0.68, t, role="pharaoh", face=-0.8, expr="smile", larm=(0.3, 0.2),
                 rarm=(-2.4 + 0.3 * math.sin(t * 9), 0.3) if t > t_wave else (-0.3, -0.2))
        cat(ctx, 1250, 720, 0.5, t, look=-1)
        ctx.restore()
        if t > t_wave + 2.0:
            k = ease_in(prog(t, t_wave + 2.0, t_back))
            warm_glow(ctx, 960, 540, 100 + 1600 * k, 0.9, (0.7, 0.9, 1.0))
            setc(ctx, WHITE, k)
            ctx.paint()
        pop_text(ctx, "BZZZ!", 1300, 250, 80, t - 0.3, RED, hold=t_wave - 0.5)
    else:
        tt = t - t_back
        ctx.save()
        cam(ctx, 960, 560, 1.0)
        bedroom_bg(ctx, t)
        pizza_box(ctx, 1010, 870, 0.8, rot=0.05)
        land = ease_out(prog(tt, 0, 0.4))
        sq = -0.15 * math.exp(-max(0, tt - 0.4) * 6) if tt > 0.4 else 0
        guy(ctx, 1350, lerp(-300, 520, land), 0.7, t, expr="o", face=-0.4, squash=sq, larm=(0.3, 0.2),
            rarm=(-0.3, -0.2))
        ctx.save()
        ctx.translate(1350, lerp(-300, 520, land))
        ctx.scale(0.7, 0.7)
        gold_collar(ctx, "body")
        ctx.restore()
        ctx.restore()
        setc(ctx, WHITE, 1 - clamp(tt / 0.5))
        ctx.paint()
        if t > cue("Like nothing"):
            pop_text(ctx, "...or did it?", 960, 980, 80, t - cue("Like nothing") - 0.8, GOLD, font=HAND_FONT, outline=7)
    vignette(ctx, 0.3)


def classroom_desk(ctx, t):
    vgrad(ctx, 0, 0, W, H, hexc("#a6cfe6"), hexc("#8ab8d8"))
    rrect(ctx, 200, 60, 1520, 320, 10)
    fs(ctx, hexc("#2a4a3a"), lw=10, stroke=hexc("#8a5a2b"))
    text(ctx, "HISTORY: ANCIENT EGYPT", 960, 150, 60, WHITE, font=HAND_FONT, outline=0, shadow=False)
    pyramid(ctx, 560, 340, 200, 140, cased=False)
    text(ctx, "c. 2500 BC", 1300, 260, 46, WHITE, font=HAND_FONT, outline=0, shadow=False)
    ctx.rectangle(0, 600, W, 480)
    fs(ctx, hexc("#c9925a"), lw=6)


def sh_book(ctx, t, D, cue):
    t_photo = cue("There was a photo")
    t_workers = cue("Workers digging")
    t_water = cue("Water flowing")
    t_middle = cue("And in the middle")
    if t < t_photo:
        classroom_desk(ctx, t)
        k = ease_out(prog(t, 0.5, 1.5))
        guy(ctx, 960, lerp(1400, 460, k), 0.7, t, expr="flat", face=0.0, look=(0, 1), larm=(1.0, -1.4), rarm=(-1.0, 1.4),
            show_legs=False)
        ctx.save()
        ctx.translate(960, 780)
        poly(ctx, [(-420, -120), (0, -90), (420, -120), (440, 160), (0, 190), (-440, 160)])
        fs(ctx, WHITE, lw=7)
        line(ctx, 0, -90, 0, 190, 5)
        ctx.restore()
        caption(ctx, "MONDAY", "HISTORY CLASS", t - 0.3, dur=3.5)
    else:
        z = 1.0 if t < t_middle else lerp(1.0, 3.6, ease(prog(t, t_middle, t_middle + 3.0)))
        fx, fy = 210 + 1500 * 0.495, 160 + 900 * 0.44
        ctx.save()
        cam(ctx, lerp(960, fx, ease(prog(t, t_middle, t_middle + 3.0))), lerp(560, fy, ease(prog(t, t_middle, t_middle + 3.0))), z)
        bg_fill(ctx, WHITE)
        for k in range(30):
            line(ctx, 60, 120 + k * 32, 160, 120 + k * 32, 3, (0.7, 0.7, 0.7))
        text(ctx, "Tomb painting, Thebes (c. 1400 BC)", 960, 1095, 34, INK, font=HAND_FONT, outline=0, shadow=False)
        tomb_painting(ctx, 210, 160, 1500, 900, t)
        rrect(ctx, 210, 160, 1500, 900, 4)
        fs(ctx, None, lw=6)
        if t > t_workers:
            for i, (hx, hy) in enumerate(((210 + 1500 * 0.17, 160 + 900 * 0.6), (210 + 1500 * 0.5, 160 + 900 * 0.83))):
                tc = [t_workers, t_water][i]
                if t > tc and t < t_middle + 0.5:
                    circle(ctx, hx, hy, 120 + 6 * math.sin(t * 8))
                    ctx.save()
                    setc(ctx, RED)
                    ctx.set_line_width(7)
                    ctx.set_dash([20, 12])
                    ctx.stroke()
                    ctx.restore()
        if t > t_middle + 3.0:
            circle(ctx, fx, fy, 34 + math.sin(t * 8) * 2)
            ctx.save()
            setc(ctx, GOLD)
            ctx.set_line_width(4)
            ctx.set_dash([8, 5])
            ctx.stroke()
            ctx.restore()
        ctx.restore()
        if t > t_middle + 3.2:
            pop_text(ctx, "THAT'S ME!", 960, 980, 130, t - t_middle - 3.2, RED, rot=-0.03)
    vignette(ctx, 0.3)


def sh_outro(ctx, t, D, cue):
    t_next = cue("Because next time")
    spiral_bg(ctx, t, speed=0.2)
    k = ease_out(prog(t, 0, 0.5))
    pizza = t > t_next + 1.8
    hands = guy(ctx, 960, lerp(1400, 400, k), 1.15, t, expr="grin" if not pizza else "laugh", face=0.0, look=(0, 0),
                larm=(0.3, 0.2), rarm=(-2.6 + 0.25 * math.sin(t * 7), 0.4) if t < t_next else (-1.5, 0.6))
    if t > t_next + 1.0:
        a = back_out(prog(t, t_next + 1.0, t_next + 1.5), 2)
        ctx.save()
        ctx.translate(hands["r"][0] + 30, hands["r"][1] - 40)
        ctx.scale(max(a, 1e-3), max(a, 1e-3))
        poly(ctx, [(0, 0), (-70, -150), (70, -150)])
        fs(ctx, hexc("#ffd36a"), lw=6)
        ctx.rectangle(-75, -170, 150, 26)
        fs(ctx, hexc("#d9a24a"), lw=5)
        for (px, py) in ((-25, -110), (20, -120), (0, -60)):
            circle(ctx, px, py, 14)
            fs(ctx, RED, lw=3)
        ctx.restore()
        pop_text(ctx, "PIZZA? IN ROME?", 1500, 300, 70, t - t_next - 1.0, GOLD, rot=0.05)
    pop_text(ctx, "SUBSCRIBE TO HISTORY WORLD!", 960, 110, 80, t - 1.0, WHITE, hold=t_next + 0.5)
    vignette(ctx, 0.45)


def sh_endcard(ctx, t, D, cue):
    vgrad(ctx, 0, 0, W, H, hexc("#ffb84a"), hexc("#ff6a8a"))
    ctx.save()
    ctx.translate(W / 2, H / 2)
    ctx.rotate(t * 0.3)
    cols = [hexc("#ffd36a"), hexc("#ff8a4a"), hexc("#ff6aa8"), hexc("#6ad0ff")]
    for k in range(24):
        ctx.move_to(0, 0)
        ctx.arc(0, 0, 1600, k * math.pi / 12, k * math.pi / 12 + math.pi / 12)
        ctx.close_path()
        setc(ctx, cols[k % 4], 0.35)
        ctx.fill()
    ctx.restore()
    pyramid(ctx, 260, 1080, 560, 340)
    pyramid(ctx, 1680, 1080, 520, 320)
    confetti(ctx, t, n=80)
    k = ease_out(prog(t, 0.0, 0.6))
    guy(ctx, 380, lerp(1400, 560, k), 0.85, t, expr="grin", face=0.4, larm=(0.3, 0.2),
        rarm=(-2.6 + 0.3 * math.sin(t * 7), 0.5))
    a = back_out(prog(t, 0.3, 0.8), 2) * (1 + 0.04 * math.sin(t * 5))
    ctx.save()
    ctx.translate(1140, 400)
    ctx.scale(max(a, 1e-3), max(a, 1e-3))
    ctx.rotate(-0.03)
    text(ctx, "SUBSCRIBE TO", 0, -90, 110, WHITE, outline=14)
    text(ctx, "HISTORY WORLD!", 0, 70, 140, GOLD_L, outline=16)
    ctx.restore()
    tb = t - 1.0
    if tb > 0:
        kk = back_out(clamp(tb / 0.4), 2) * (1 + 0.05 * math.sin(t * 6))
        ctx.save()
        ctx.translate(1140, 720)
        ctx.scale(max(kk, 1e-3), max(kk, 1e-3))
        rrect(ctx, -300, -80, 600, 160, 40)
        fs(ctx, hexc("#ff2a2a"), lw=8)
        poly(ctx, [(-220, -40), (-220, 40), (-160, 0)])
        fs(ctx, WHITE, lw=0)
        text(ctx, "SUBSCRIBE", 40, 0, 80, WHITE, outline=6)
        ctx.restore()
        # bell
        ctx.save()
        ctx.translate(1530, 720)
        ctx.rotate(0.3 * math.sin(t * 10) * kk)
        ctx.move_to(-40, 30)
        ctx.curve_to(-40, -60, 40, -60, 40, 30)
        ctx.close_path()
        fs(ctx, GOLD, lw=6)
        circle(ctx, 0, 40, 10)
        fs(ctx, GOLD, lw=4)
        ctx.restore()
    if t > 1.8:
        text(ctx, "Next time: I accidentally invent pizza in Ancient Rome!", 1140, 900, 46, WHITE, font=HAND_FONT,
             outline=5, alpha=ease(prog(t, 1.8, 2.4)))
    fade = prog(t, D - 0.8, D)
    if fade > 0:
        setc(ctx, (0, 0, 0), fade)
        ctx.paint()


SHOT_FUNCS = {
    "hook": sh_hook, "rewind": sh_rewind, "title": sh_title, "bedroom": sh_bedroom, "box": sh_box,
    "portal": sh_portal, "desert": sh_desert, "guards": sh_guards, "palace": sh_palace, "crowned": sh_crowned,
    "perks": sh_perks, "meeting": sh_meeting, "build": sh_build, "slide": sh_slide, "crash": sh_crash,
    "nile": sh_nile, "nilefact": sh_nilefact, "idea": sh_idea, "rescue": sh_rescue, "saved": sh_saved,
    "pharaoh": sh_pharaoh, "judgement": sh_judgement, "reward": sh_reward, "return": sh_return, "book": sh_book,
    "outro": sh_outro, "endcard": sh_endcard,
}
