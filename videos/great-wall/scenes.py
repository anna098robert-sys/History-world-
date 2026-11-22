"""Shots for 'How I Accidentally Did NOT Destroy the Great Wall of China'.
Each shot: fn(ctx, t, D, cue). cue(text) -> start time of the sentence containing text."""
import math, random
import cairo
from gfx import *

CJK = "Noto Serif CJK SC"
TIMELINE = {}          # filled by render.Renderer: id -> (shot, cue)

GOLD = (1, 0.85, 0.3)
MARBLE = hexc("#f4efe4")
MARBLE_D = hexc("#d8cfbd")
BRICK = hexc("#9a958c")
BRICK_D = hexc("#7d786f")
BRICK_L = hexc("#b3aea4")
CHINA_RED = hexc("#c8282d")


# ====================================================================== helpers
def cam(ctx, cx, cy, z=1.0, rot=0.0, shake=0.0, t=0.0):
    sx = shake * (math.sin(t * 47) + math.sin(t * 31)) * 0.5
    sy = shake * (math.cos(t * 53) + math.sin(t * 37)) * 0.5
    ctx.translate(W / 2 + sx, H / 2 + sy)
    ctx.rotate(rot)
    ctx.scale(z, z)
    ctx.translate(-cx, -cy)


def caption(ctx, place, year, t, dur=4.0, cn=None):
    if t < 0 or t > dur + 0.6:
        return
    k = ease_out(prog(t, 0, 0.5)) - ease_in(prog(t, dur, dur + 0.5))
    x = lerp(-960, 70, k)
    rrect(ctx, x, 850, 860, 150, 18)
    fs(ctx, (0.08, 0.07, 0.1, 0.82), lw=0)
    ctx.rectangle(x, 850, 14, 150)
    setc(ctx, CHINA_RED)
    ctx.fill()
    text(ctx, place, x + 40, 898, 46, WHITE, align="left", outline=0, shadow=False)
    text(ctx, year, x + 40, 958, 52, GOLD, align="left", outline=0, shadow=False)
    if cn:
        text(ctx, cn, x + 820, 925, 64, (1, 1, 1, 0.9), font=CJK, align="right", outline=0, shadow=False)


def year_counter(ctx, t, D, y0, y1):
    k = ease(prog(t, 0.3, D - 0.4))
    y = int(round(lerp(y0, y1, k)))
    rrect(ctx, W / 2 - 230, 60, 460, 130, 30)
    fs(ctx, (0.05, 0.03, 0.1, 0.75), lw=5, stroke=GOLD)
    text(ctx, str(y), W / 2, 125, 96, GOLD, outline=0, shadow=False)


def paper_bg(ctx, c=hexc("#f3e9d2")):
    bg_fill(ctx, c)
    for i in range(0, W, 60):
        line(ctx, i, 0, i, H, 1.5, (0.8, 0.72, 0.6), 0.45)
    for j in range(0, H, 60):
        line(ctx, 0, j, W, j, 1.5, (0.8, 0.72, 0.6), 0.45)


# ====================================================================== hats & characters
def hat_straw(c):
    poly(c, [(-150, -40), (0, -150), (150, -40)])
    fs(c, hexc("#e2c27a"), lw=LW)
    for k in (-60, 0, 60):
        line(c, k * 0.4, -140, k * 2.0, -46, 3, hexc("#b8964e"))


def hat_helmet(c):
    c.move_to(-104, -10)
    c.curve_to(-110, -150, 110, -150, 104, -10)
    c.curve_to(60, -40, -60, -40, -104, -10)
    fs(c, hexc("#5a5f66"), lw=LW)
    line(c, 0, -118, 0, -160, 8)
    c.move_to(0, -158)
    c.curve_to(-30, -200, 30, -210, 10, -230)
    c.curve_to(40, -200, 30, -160, 0, -158)
    fs(c, CHINA_RED, lw=4)
    c.move_to(-104, -10)
    c.curve_to(-60, -40, 60, -40, 104, -10)
    c.set_line_width(14)
    setc(c, hexc("#b8902e"))
    c.stroke()


def hat_official(c):
    rrect(c, -78, -150, 156, 110, 30)
    fs(c, hexc("#1c1c22"), lw=LW)
    for sx in (-1, 1):
        ellipse(c, sx * 130, -100, 55, 14)
        fs(c, hexc("#1c1c22"), lw=5)


def hat_cook(c):
    c.move_to(-100, -20)
    c.curve_to(-120, -140, 120, -140, 100, -20)
    c.close_path()
    fs(c, hexc("#f2f2ea"), lw=LW)
    line(c, -95, -30, 95, -30, 6, hexc("#c9b48a"))


def hat_fur(c):
    ellipse(c, 0, -70, 112, 70)
    fs(c, hexc("#4a3424"), lw=LW)
    c.rectangle(-118, -40, 236, 40)
    fs(c, hexc("#a07850"), lw=LW)


def mustache(fx=0.0, beard=False):
    def f(c):
        mx = 8 + fx * 34
        if beard:
            c.move_to(mx - 50, 30)
            c.curve_to(mx - 40, 120, mx + 40, 130, mx + 55, 30)
            c.curve_to(mx + 20, 55, mx - 20, 55, mx - 50, 30)
            fs(c, hexc("#2a2420"), lw=4)
        c.move_to(mx, 0)
        c.curve_to(mx - 20, -8, mx - 40, 2, mx - 48, 24)
        c.curve_to(mx - 30, 8, mx - 14, 8, mx, 8)
        c.curve_to(mx + 14, 8, mx + 30, 8, mx + 48, 24)
        c.curve_to(mx + 40, 2, mx + 20, -8, mx, 0)
        fs(c, hexc("#2a2420"), lw=3)
    return f


def combo(*fs_):
    def f(c):
        for g in fs_:
            g(c)
    return f


def guy(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t))
    return doodle(ctx, x, y, s, **kw)


def worker(ctx, x, y, s, t, seed=0, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, seed))
    kw.setdefault("body", [hexc("#5d7a96"), hexc("#7a6a52"), hexc("#6d7f5a")][seed % 3])
    return doodle(ctx, x, y, s, hair=hat_straw, cap=False, **kw)


def soldier(ctx, x, y, s, t, seed=0, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, seed + 1))
    kw.setdefault("body", hexc("#a3322c"))
    return doodle(ctx, x, y, s, hair=hat_helmet, cap=False, **kw)


def foreman(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 3))
    kw.setdefault("body", hexc("#2f4f7a"))
    fx = kw.get("face", 0.9)
    return doodle(ctx, x, y, s, hair=combo(hat_official, mustache(fx)), cap=False, **kw)


def general(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 5))
    kw.setdefault("body", hexc("#7a2a22"))
    fx = kw.get("face", 0.9)
    return doodle(ctx, x, y, s, hair=combo(hat_helmet, mustache(fx, beard=True)), cap=False, **kw)


def cook(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 6))
    kw.setdefault("body", hexc("#e8e0cc"))
    return doodle(ctx, x, y, s, hair=hat_cook, cap=False, **kw)


def raider(ctx, x, y, s, t, seed=0, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, seed + 7))
    kw.setdefault("body", hexc("#5a4632"))
    return doodle(ctx, x, y, s, hair=hat_fur, cap=False, **kw)


# ====================================================================== landscape
def ridge(x, base, amp, seed):
    r = random.Random(seed)
    p1, p2, p3 = r.random() * 6, r.random() * 6, r.random() * 6
    return base - amp * (0.55 + 0.45 * math.sin(x * 0.0021 + p1)) - amp * 0.35 * math.sin(x * 0.0057 + p2) \
        - amp * 0.12 * math.sin(x * 0.017 + p3)


WALL_BASE, WALL_AMP, WALL_SEED = 700, 230, 4


def wall_y(x):
    return ridge(x, WALL_BASE, WALL_AMP, WALL_SEED)


TOWERS = [-420, 80, 560, 1020, 1480, 1960, 2450, 2900]


def sky(ctx, night, t):
    if night:
        vgrad(ctx, -1200, -800, 4400, 2200, hexc("#070b1e"), hexc("#26305a"))
        rnd = random.Random(3)
        for i in range(180):
            x, y = rnd.random() * 4400 - 1200, rnd.random() * 1000 - 600
            circle(ctx, x, y, 1.5 + rnd.random() * 2.2)
            setc(ctx, WHITE, 0.35 + 0.35 * math.sin(t * 2 + i))
            ctx.fill()
        g = cairo.RadialGradient(1500, -40, 30, 1500, -40, 260)
        g.add_color_stop_rgba(0, 1, 1, 0.9, 0.5)
        g.add_color_stop_rgba(1, 1, 1, 0.9, 0)
        ctx.set_source(g)
        circle(ctx, 1500, -40, 260)
        ctx.fill()
        circle(ctx, 1500, -40, 70)
        fs(ctx, hexc("#f4f0d8"), lw=4)
    else:
        vgrad(ctx, -1200, -800, 4400, 2200, hexc("#7fb6dc"), hexc("#f6e2c0"))
        g = cairo.RadialGradient(300, 60, 40, 300, 60, 320)
        g.add_color_stop_rgba(0, 1, 0.95, 0.7, 0.8)
        g.add_color_stop_rgba(1, 1, 0.95, 0.7, 0)
        ctx.set_source(g)
        circle(ctx, 300, 60, 320)
        ctx.fill()
        circle(ctx, 300, 60, 80)
        fs(ctx, (1, 0.9, 0.55), lw=5)


def mountain_layer(ctx, base, amp, seed, c, mist=None, x0=-1300, x1=3300):
    ctx.move_to(x0, 2000)
    for x in range(x0, x1 + 1, 40):
        ctx.line_to(x, ridge(x, base, amp, seed))
    ctx.line_to(x1, 2000)
    ctx.close_path()
    fs(ctx, c, lw=5)
    if mist:
        vgrad(ctx, x0, base - 10, x1 - x0, 140, mist + (0.0,), mist + (0.55,))


def draw_wall(ctx, night=False, fires=None, t=0.0, glue_glow=0.0, towers=True, x0=-1300, x1=3300, s=1.0):
    """the Great Wall following the ridge, with watchtowers. fires: dict tower_index -> intensity 0..1"""
    th = 46 * s
    pts = [(x, wall_y(x)) for x in range(x0, x1 + 1, 20)]
    face = hexc("#8d877c") if not night else hexc("#3d4058")
    top = hexc("#b5ae9f") if not night else hexc("#565a78")
    # wall body
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(p[0], p[1])
    for p in reversed(pts):
        ctx.line_to(p[0], p[1] + th * 1.6)
    ctx.close_path()
    fs(ctx, face, lw=5)
    # crenellations
    for i in range(0, len(pts) - 1, 2):
        x, y = pts[i]
        ctx.rectangle(x - 5 * s, y - 16 * s, 12 * s, 16 * s)
    setc(ctx, top)
    ctx.fill()
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    setc(ctx, INK)
    ctx.set_line_width(4)
    ctx.stroke()
    if glue_glow > 0:
        ctx.save()
        ctx.move_to(*pts[0])
        sel = [p for p in pts if 900 < p[0] < 1160]
        ctx.move_to(*sel[0])
        for p in sel[1:]:
            ctx.line_to(p[0], p[1] + 10)
        setc(ctx, (1, 0.95, 0.6), 0.85 * glue_glow)
        ctx.set_line_width(26)
        ctx.stroke()
        ctx.restore()
    if towers:
        for i, tx in enumerate(TOWERS):
            if not (x0 - 100 < tx < x1 + 100):
                continue
            ty = wall_y(tx)
            watchtower(ctx, tx, ty + 10, 0.6 * s, night)
            if fires and fires.get(i, 0) > 0:
                fire(ctx, tx, ty - 110 * s, 70 * s * fires[i], t + i)
                smoke(ctx, tx, ty - 150 * s, t + i, 0.7 * fires[i] * s, night)


def watchtower(ctx, x, y, s=1.0, night=False):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    body = hexc("#a69f91") if not night else hexc("#474a66")
    dark = hexc("#2a2a33") if not night else hexc("#16182a")
    ctx.rectangle(-90, -170, 180, 170)
    fs(ctx, body, lw=6)
    for k in (-50, 0, 50):
        rrect(ctx, k - 16, -130, 32, 50, 16)
        fs(ctx, dark, lw=4)
    rrect(ctx, -22, -60, 44, 60, 22)
    fs(ctx, dark, lw=4)
    for k in range(-90, 91, 30):
        ctx.rectangle(k - 9, -196, 18, 26)
    setc(ctx, body)
    ctx.fill_preserve()
    setc(ctx, INK)
    ctx.set_line_width(4)
    ctx.stroke()
    ctx.rectangle(-98, -176, 196, 12)
    fs(ctx, hexc("#7d776b") if not night else hexc("#30334a"), lw=4)
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


def landscape(ctx, t, night=False, fires=None, glue_glow=0.0, wall=True):
    sky(ctx, night, t)
    if night:
        mountain_layer(ctx, 470, 200, 1, hexc("#1d2444"), mist=(0.15, 0.18, 0.32))
        mountain_layer(ctx, 600, 230, 2, hexc("#1a2038"), mist=(0.12, 0.14, 0.26))
        mountain_layer(ctx, WALL_BASE + 20, WALL_AMP, WALL_SEED, hexc("#151a2e"))
    else:
        mountain_layer(ctx, 470, 200, 1, hexc("#9fb3c4"), mist=(0.93, 0.9, 0.85))
        mountain_layer(ctx, 600, 230, 2, hexc("#7f9c8c"), mist=(0.9, 0.9, 0.84))
        mountain_layer(ctx, WALL_BASE + 20, WALL_AMP, WALL_SEED, hexc("#5f8a5a"))
        # pines on the slopes
        rnd = random.Random(8)
        for i in range(40):
            x = rnd.random() * 4400 - 1200
            y = wall_y(x) + 120 + rnd.random() * 500
            pine(ctx, x, y, 40 + rnd.random() * 30)
    if wall:
        draw_wall(ctx, night, fires, t, glue_glow)
    if night:
        mountain_layer(ctx, 1150, 120, 9, hexc("#0e1222"))
    else:
        mountain_layer(ctx, 1150, 120, 9, hexc("#4c7448"))


def pine(ctx, x, y, h):
    line(ctx, x, y, x, y - h * 0.3, 5, hexc("#5a3a22"))
    for k in range(3):
        w = h * (0.5 - k * 0.12)
        yy = y - h * 0.25 - k * h * 0.28
        poly(ctx, [(x - w, yy), (x, yy - h * 0.45), (x + w, yy)])
        fs(ctx, hexc("#2f5a3a"), lw=3)


def walkway(ctx, t, night=False, tower_x=None, flicker=0.0):
    """side view standing on top of the wall. floor at y=760."""
    sky(ctx, night, t)
    if night:
        mountain_layer(ctx, 520, 200, 1, hexc("#1d2444"), mist=(0.15, 0.18, 0.32))
        mountain_layer(ctx, 640, 160, 3, hexc("#151a2e"))
    else:
        mountain_layer(ctx, 520, 200, 1, hexc("#9fb3c4"), mist=(0.93, 0.9, 0.85))
        mountain_layer(ctx, 640, 160, 3, hexc("#6f957a"), mist=(0.9, 0.9, 0.84))
    if tower_x is not None:
        watchtower(ctx, tower_x, 640, 2.0, night)
    # back parapet (crenellations)
    pc = hexc("#9b958a") if not night else hexc("#454a68")
    ctx.rectangle(-1200, 560, 4400, 90)
    fs(ctx, pc, lw=6)
    for k in range(-1200, 3200, 140):
        ctx.rectangle(k, 500, 80, 62)
        fs(ctx, pc, lw=6)
    bricks_texture(ctx, -1200, 560, 4400, 90, night, seed=1)
    # floor
    ctx.rectangle(-1200, 650, 4400, 120)
    fs(ctx, hexc("#c1b9a6") if not night else hexc("#5d6180"), lw=6)
    for k in range(-1200, 3200, 110):
        line(ctx, k, 650, k - 60, 770, 3, hexc("#9d9583") if not night else hexc("#45486a"))
    # front wall face
    ctx.rectangle(-1200, 770, 4400, 600)
    fs(ctx, hexc("#8d877c") if not night else hexc("#3a3e5a"), lw=6)
    bricks_texture(ctx, -1200, 770, 4400, 600, night, seed=2)
    if flicker > 0:
        setc(ctx, (1, 0.5, 0.1), 0.08 * flicker * (1 + 0.3 * math.sin(t * 20)))
        ctx.paint()


def bricks_texture(ctx, x, y, w, h, night=False, seed=0, bw=110, bh=40):
    c = hexc("#6f6a60") if not night else hexc("#2c2f46")
    rows = int(h / bh) + 1
    for r in range(rows):
        yy = y + r * bh
        if yy > y + h:
            break
        line(ctx, x, yy, x + w, yy, 2.5, c, 0.8)
        off = (bw / 2) * (r % 2)
        for k in range(int(w / bw) + 2):
            xx = x + off + k * bw
            line(ctx, xx, yy, xx, min(yy + bh, y + h), 2.5, c, 0.8)


def brick(ctx, x, y, w, h, t=0.0, stamp=True, cap_mark=0.0, crack=0.0, rot=0.0, glow=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, w * 0.2, 0, 0, w * 1.1)
        g.add_color_stop_rgba(0, 1, 0.85, 0.4, 0.7 * glow)
        g.add_color_stop_rgba(1, 1, 0.85, 0.4, 0)
        ctx.set_source(g)
        circle(ctx, 0, 0, w * 1.1)
        ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, h * 0.06)
    fs(ctx, BRICK, lw=max(3, w * 0.012))
    rnd = random.Random(5)
    for i in range(40):
        circle(ctx, -w / 2 + rnd.random() * w, -h / 2 + rnd.random() * h, w * 0.006 + rnd.random() * w * 0.006)
        setc(ctx, BRICK_D, 0.6)
        ctx.fill()
    if stamp:
        sw, sh = w * 0.42, h * 0.62
        rrect(ctx, -sw / 2 - w * 0.12, -sh / 2, sw, sh, 4)
        setc(ctx, BRICK_D)
        ctx.fill_preserve()
        setc(ctx, (0.35, 0.33, 0.3))
        ctx.set_line_width(max(2, w * 0.008))
        ctx.stroke()
        text(ctx, "隆慶四年", -w * 0.12, -sh * 0.12, sh * 0.30, (0.25, 0.23, 0.2), font=CJK, outline=0, shadow=False)
        text(ctx, "造", -w * 0.12, sh * 0.27, sh * 0.26, (0.25, 0.23, 0.2), font=CJK, outline=0, shadow=False)
    if cap_mark > 0:
        ctx.save()
        ctx.translate(w * 0.24, h * 0.12)
        ctx.scale(w * 0.00085 * cap_mark, w * 0.00085 * cap_mark)
        ctx.push_group()
        draw_cap(ctx, (0.45, 0.42, 0.38))
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(0.9)
        ctx.restore()
    if crack > 0:
        pts = [(-w * 0.05, -h / 2), (w * 0.02, -h * 0.2), (-w * 0.04, 0), (w * 0.05, h * 0.25), (0, h / 2)]
        n = max(2, int(len(pts) * crack))
        ctx.move_to(*pts[0])
        for p in pts[1:n]:
            ctx.line_to(*p)
        setc(ctx, INK)
        ctx.set_line_width(max(3, w * 0.012))
        ctx.stroke()
    ctx.restore()


def museum_bg(ctx, t):
    vgrad(ctx, -800, -400, 3600, 1600, hexc("#efe2c8"), hexc("#e2d0ae"))
    vgrad(ctx, -800, 760, 3600, 600, hexc("#9b6b43"), hexc("#7a5132"))
    for i in range(-6, 40):
        line(ctx, i * 120 - 600, 780, i * 160 - 900, 1500, 3, hexc("#6a4428"), 0.6)
    line(ctx, -800, 780, 2800, 780, 6)
    ctx.rectangle(-800, 690, 3600, 90)
    fs(ctx, hexc("#d8c39c"), lw=5)
    # exhibition banner
    rrect(ctx, 440, 40, 1220, 120, 10)
    fs(ctx, CHINA_RED, lw=6)
    text(ctx, "TREASURES OF THE MING DYNASTY", 1050, 100, 54, GOLD, outline=0, shadow=False)
    text(ctx, "明", 500, 100, 70, GOLD, font=CJK, outline=0, shadow=False)
    text(ctx, "明", 1600, 100, 70, GOLD, font=CJK, outline=0, shadow=False)
    # hanging scroll painting
    ctx.rectangle(120, 200, 260, 460)
    fs(ctx, hexc("#f2e8cf"), lw=5)
    ctx.rectangle(100, 190, 300, 18)
    fs(ctx, hexc("#5a3a22"), lw=4)
    ctx.rectangle(100, 652, 300, 18)
    fs(ctx, hexc("#5a3a22"), lw=4)
    ctx.move_to(130, 560)
    for x in range(130, 371, 20):
        ctx.line_to(x, 520 - 60 * abs(math.sin(x * 0.03)))
    ctx.line_to(370, 640)
    ctx.line_to(130, 640)
    fs(ctx, hexc("#9aa59a"), lw=3)
    text(ctx, "山水", 330, 280, 40, CHINA_RED, font=CJK, outline=0, shadow=False)
    # porcelain vase on pedestal
    ctx.rectangle(2060, 520, 220, 260)
    fs(ctx, MARBLE, lw=6)
    ctx.save()
    ctx.translate(2170, 420)
    ctx.move_to(-30, -100)
    ctx.line_to(30, -100)
    ctx.curve_to(30, -60, 90, -40, 90, 20)
    ctx.curve_to(90, 80, 40, 100, 30, 100)
    ctx.line_to(-30, 100)
    ctx.curve_to(-40, 100, -90, 80, -90, 20)
    ctx.curve_to(-90, -40, -30, -60, -30, -100)
    fs(ctx, hexc("#f6f6f2"), lw=6)
    ctx.move_to(-80, 0)
    ctx.curve_to(-40, -40, 0, 40, 40, 0)
    ctx.curve_to(60, -20, 80, 10, 84, 20)
    setc(ctx, hexc("#2b4f9a"))
    ctx.set_line_width(8)
    ctx.stroke()
    ellipse(ctx, 0, 50, 50, 16)
    fs(ctx, None, lw=5, stroke=hexc("#2b4f9a"))
    ctx.restore()
    # lanterns
    for lx in (330, 1790):
        line(ctx, lx, 0, lx, 230, 4)
        ellipse(ctx, lx, 290, 55, 66)
        fs(ctx, CHINA_RED, lw=5)
        line(ctx, lx - 30, 240, lx + 30, 240, 6, GOLD)
        line(ctx, lx - 30, 340, lx + 30, 340, 6, GOLD)
        line(ctx, lx, 356, lx, 400, 4, GOLD)


def brick_case(ctx, x, y, t, glow=0.3, open_=0.0, sign=True, cap_mark=0.0):
    ctx.rectangle(x - 150, y + 60, 300, 340)
    fs(ctx, MARBLE, lw=6)
    ctx.rectangle(x - 175, y + 50, 350, 40)
    fs(ctx, MARBLE_D, lw=6)
    ctx.rectangle(x - 175, y + 380, 350, 40)
    fs(ctx, MARBLE_D, lw=6)
    ellipse(ctx, x, y + 40, 130, 24)
    fs(ctx, hexc("#7a1e3a"), lw=5)
    brick(ctx, x, y - 10, 220, 100, t, cap_mark=cap_mark, glow=glow)
    ctx.save()
    ctx.translate(0, -open_ * 420)
    ctx.rectangle(x - 160, y - 200, 320, 250)
    setc(ctx, (0.8, 0.95, 1.0), 0.18)
    ctx.fill_preserve()
    setc(ctx, (0.35, 0.5, 0.6), 0.9)
    ctx.set_line_width(5)
    ctx.stroke()
    poly(ctx, [(x - 120, y - 180), (x - 60, y - 180), (x - 140, y + 20), (x - 155, y + 20)])
    setc(ctx, WHITE, 0.35)
    ctx.fill()
    ctx.restore()
    if sign:
        ctx.save()
        ctx.translate(x + 240, y + 150)
        ctx.rotate(0.04)
        rrect(ctx, -115, -75, 230, 150, 10)
        fs(ctx, hexc("#fffaf0"), lw=5)
        text(ctx, "DO NOT", 0, -40, 34, RED, outline=0, shadow=False)
        text(ctx, "TOUCH", 0, -2, 38, RED, outline=0, shadow=False)
        text(ctx, "Ming brick, 1570", 0, 40, 30, INK, font=HAND_FONT, outline=0, shadow=False)
        line(ctx, 0, 75, 0, 230, 8)
        ctx.restore()


def rice_pot(ctx, x, y, s, t, fire_on=True):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if fire_on:
        for k in range(3):
            stone_(ctx, -110 + k * 110, 150)
        fire(ctx, 0, 110, 70, t)
    ctx.move_to(-200, -60)
    ctx.curve_to(-210, 120, -120, 160, 0, 160)
    ctx.curve_to(120, 160, 210, 120, 200, -60)
    ctx.close_path()
    fs(ctx, hexc("#3a3a40"), lw=7)
    ellipse(ctx, 0, -60, 200, 40)
    fs(ctx, hexc("#2a2a30"), lw=7)
    ellipse(ctx, 0, -56, 180, 30)
    fs(ctx, hexc("#f4f0e2"), lw=0)
    rnd = random.Random(2)
    for i in range(50):
        ellipse(ctx, -160 + rnd.random() * 320, -70 + rnd.random() * 26, 7, 4)
        setc(ctx, WHITE)
        ctx.fill()
    for k in range(4):
        ph = (t * 0.5 + k / 4) % 1
        xx = -120 + k * 80
        ctx.move_to(xx, -90 - ph * 200)
        ctx.curve_to(xx + 30, -120 - ph * 200, xx - 30, -150 - ph * 200, xx, -180 - ph * 200)
        setc(ctx, WHITE, 0.7 * (1 - ph))
        ctx.set_line_width(10)
        ctx.stroke()
    ctx.restore()


def stone_(ctx, x, y):
    ellipse(ctx, x, y, 50, 28)
    fs(ctx, hexc("#8a857c"), lw=5)


def sack(ctx, x, y, s=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ctx.move_to(-60, -70)
    ctx.curve_to(-90, 0, -80, 80, 0, 80)
    ctx.curve_to(80, 80, 90, 0, 60, -70)
    ctx.curve_to(30, -90, -30, -90, -60, -70)
    fs(ctx, hexc("#d9c08a"), lw=6)
    line(ctx, -40, -78, 40, -78, 8, hexc("#8a6235"))
    text(ctx, "米", 0, 10, 60, hexc("#8a6235"), font=CJK, outline=0, shadow=False)
    ctx.restore()


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


def straw_pile(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-130, 0)
    ctx.curve_to(-100, -110, 100, -110, 130, 0)
    ctx.close_path()
    fs(ctx, hexc("#d8b45a"), lw=6)
    rnd = random.Random(4)
    for i in range(30):
        x0 = -110 + rnd.random() * 220
        y0 = -rnd.random() * 70
        line(ctx, x0, y0, x0 + rnd.uniform(-30, 30), y0 - 20, 3, hexc("#a8843a"))
    for k in range(3):
        line(ctx, -90 + k * 70, -10, -40 + k * 70, -60, 12, hexc("#6b4428"))
    ctx.restore()


def ladder(ctx, x1, y1, x2, y2, w=50):
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * w / 2, dx / n * w / 2
    line(ctx, x1 + nx, y1 + ny, x2 + nx, y2 + ny, 8, hexc("#6b4428"))
    line(ctx, x1 - nx, y1 - ny, x2 - nx, y2 - ny, 8, hexc("#6b4428"))
    for k in range(1, int(n / 50)):
        f = k * 50 / n
        line(ctx, x1 + dx * f + nx, y1 + dy * f + ny, x1 + dx * f - nx, y1 + dy * f - ny, 6, hexc("#6b4428"))


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


def fire_chain(t, t0, step=0.5, n=8, start=4, max_i=None):
    """which towers burn: ignite from `start` outward."""
    fires = {}
    order = sorted(range(n), key=lambda i: abs(i - start))
    for k, i in enumerate(order):
        tt_ = t - t0 - k * step
        if tt_ > 0:
            fires[i] = clamp(tt_ / 0.4)
    return fires


# ====================================================================== SHOTS
def sh_hook(ctx, t, D, cue):
    t_year = cue("The year")
    t_every = cue("Every fire")
    t_enemy = cue("Enemies")
    t_me = cue("That's me")
    t_none = cue("And there was no enemy")
    t_least = cue("At least")
    # camera: start tight on the hero + flaring fire, pull out to reveal the burning chain, then snap back
    hx = TOWERS[4] + 75
    hy = wall_y(TOWERS[4]) - 204
    if t < t_me:
        k = ease(prog(t, 0.6, 4.2))
        cx, cy, z = lerp(hx - 20, 1100, k), lerp(hy + 40, 380, k), lerp(2.6, 0.62, k)
    elif t < t_least:
        k = ease_out(prog(t, t_me, t_me + 0.5))
        cx, cy, z = lerp(1100, hx - 10, k), lerp(380, hy + 40, k), lerp(0.62, 2.4, k)
    else:
        k = ease(prog(t, t_least, t_least + 1.2))
        cx, cy, z = lerp(hx - 10, 1260, k), lerp(hy + 40, 640, k), lerp(2.4, 1.2, k)
    shake = 6 * (1 - prog(t, 0, 1.2)) + (3 if t_enemy < t < t_me else 0)
    ctx.save()
    cam(ctx, cx, cy, z, shake=shake, t=t)
    fires = fire_chain(t, 0.15, step=0.45, start=4)
    landscape(ctx, t, night=True, fires=fires)
    # soldiers running along the wall with torches
    if t > t_enemy - 0.5:
        for i in range(6):
            sx = 600 + ((t - t_enemy) * 120 + i * 150) % 1200
            sy = wall_y(sx) - 50
            soldier(ctx, sx, sy, 0.16, t, seed=i, face=0.9, walk=t * 2 + i * 0.3, larm=(0.3, 0.2), rarm=(-2.4, 0.3))
    # hero on the central tower holding a torch
    frozen = t_me + 0.5 < t < t_none
    tt = t_me + 0.5 if frozen else t
    expr = "shock" if t < t_me else ("grin" if t < t_none else "worried")
    guy(ctx, hx, hy, 0.25, tt, expr=expr, face=0.3, larm=(0.3, 0.2), rarm=(-2.5, 0.2), brows="worried" if t > t_none else None)
    torch(ctx, hx + 52, hy - 12, tt, rot=0.1, s=0.34)
    # foreshadowing: eyes glinting in the dark valley
    if t > t_least:
        a = ease(prog(t, t_least + 0.4, t_least + 1.0))
        for ex in (1180, 1250, 1330):
            for d in (-7, 7):
                circle(ctx, ex + d, 820 + (ex % 3) * 10, 3.5)
                setc(ctx, (1, 0.9, 0.3), a)
                ctx.fill()
    ctx.restore()
    if frozen:
        setc(ctx, (0.1, 0.1, 0.2), 0.25)
        ctx.paint()
    if t > t_year:
        pop_text(ctx, "1570", 960, 140, 130, t - t_year, GOLD, hold=t_every - t_year + 1.6)
    if t > t_enemy:
        pop_text(ctx, "ENEMIES ARE COMING!", 960, 980, 84, t - t_enemy, RED, hold=t_me - t_enemy - 0.1)
    if t > t_me:
        k = ease_out(prog(t, t_me + 0.3, t_me + 0.7))
        setc(ctx, GOLD)
        ctx.set_line_width(12)
        ctx.move_to(1500, 230)
        ctx.curve_to(1450, 330, 1350, 360, lerp(1500, 1230, k), lerp(230, 380, k))
        ctx.stroke()
        pop_text(ctx, "THAT'S ME.", 1560, 190, 100, t - t_me - 0.3, WHITE, rot=0.05, hold=t_none - t_me)
    if t > t_none:
        pop_text(ctx, "NO ENEMY...?", 960, 960, 90, t - t_none, WHITE, hold=t_least - t_none)
    if t > t_least + 0.6:
        pop_text(ctx, "...OR WAS THERE?", 960, 960, 90, t - t_least - 0.6, GOLD)
    vignette(ctx, 0.55)


def sh_rewind(ctx, t, D, cue):
    hs, hc = TIMELINE["hook"]
    th = hs["D"] * (1 - ease_in(prog(t, 0, D))) ** 1.0
    sh_hook(ctx, max(0.0, th), hs["D"], hc)
    setc(ctx, (0.1, 0.1, 0.3), 0.25)
    ctx.paint()
    vhs(ctx, t)
    rewind_icon(ctx, 220, 120, 1.0, 0.9)
    text(ctx, "REWIND", 330, 122, 70, WHITE, align="left", outline=0, shadow=False)


def sh_title(ctx, t, D, cue):
    spiral_bg(ctx, t, speed=0.35)
    # small wall silhouette at the bottom
    ctx.save()
    ctx.translate(0, 380)
    ctx.scale(1, 0.6)
    for x in range(-100, 2100, 140):
        y = 900 + 60 * math.sin(x * 0.004)
        ctx.rectangle(x, y, 120, 400)
        ctx.rectangle(x + 10, y - 40, 40, 40)
        ctx.rectangle(x + 70, y - 40, 40, 40)
    setc(ctx, (0.5, 0.08, 0.1))
    ctx.fill()
    ctx.restore()

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
    row([("HOW", WHITE), ("I", WHITE), ("ACCIDENTALLY", WHITE)], 250, 110, 0.15)
    row([("DID", WHITE), ("NOT", GOLD), ("DESTROY", WHITE)], 420, 150, 0.5)
    row([("THE", WHITE), ("GREAT", GOLD), ("WALL", GOLD)], 600, 150, 0.9)
    k = ease_out(prog(t, 1.2, 1.8))
    if k > 0:
        guy(ctx, 1700, lerp(1500, 820, k), 0.7, t, expr="grin", face=-0.3, larm=(2.6, -0.3), rarm=(-0.3, 0))
    text(ctx, "HISTORY WORLD", W / 2, 1000, 48, WHITE, font=HAND_FONT, outline=6, alpha=ease(prog(t, 1.5, 2.2)))


def sh_intro(ctx, t, D, cue):
    t_last = cue("Last time")
    t_prom = cue("So I made")
    t_no = cue("No more")
    spiral_bg(ctx, t, speed=0.15)
    k = ease_out(prog(t, 0, 0.5))
    promising = t > t_prom
    guy(ctx, 560, lerp(1300, 470, k), 1.05, t, expr="smile" if t < t_last else ("worried" if t < t_prom else "flat"),
        face=0.4, larm=(0.3, 0.2), rarm=(-2.6 + 0.3 * math.sin(t * 7), 0.5) if t < t_last else
        ((-2.9, 0.0) if promising else (-0.3, -0.2)), brows="worried" if t_last < t < t_prom else None)
    if t < t_last:
        pop_text(ctx, "HI!", 900, 260, 110, t - 0.3, GOLD, hold=t_last - 0.6)
    elif t < t_prom:
        tt = t - t_last
        kb = ease_out(prog(tt, 0, 0.4))
        ctx.save()
        ctx.translate(1300, 450)
        ctx.scale(max(kb, 1e-3), max(kb, 1e-3))
        speech(ctx, 0, 0, 760, 520, "", think=True, tail=(-300, 140))
        pocket_watch(ctx, -220, -40, 80, t, glow=0.5, spin=t)
        # three tiny icons of last episode
        ctx.save()
        ctx.translate(20, 40)
        ctx.rotate(math.radians(6))
        ctx.rectangle(-30, -150, 60, 170)
        fs(ctx, MARBLE, lw=5)
        for j in range(4):
            line(ctx, -30, -150 + j * 42, 30, -150 + j * 42, 3)
        ctx.restore()
        apple(ctx, 160, -30, 40)
        circle(ctx, 280, 30, 55)
        fs(ctx, (0.98, 0.9, 0.62), lw=5)
        circle(ctx, 280, 30, 22)
        fs(ctx, (0.35, 0.65, 0.55), lw=0)
        ctx.restore()
        pop_text(ctx, "3 CENTURIES. OOPS.", 1300, 860, 72, tt - 1.6, WHITE)
    else:
        tt = t - t_prom
        ctx.save()
        ctx.translate(1300, 470)
        kb = back_out(prog(tt, 0, 0.5), 1.6)
        ctx.scale(max(kb, 1e-3), max(kb, 1e-3))
        ctx.rotate(-0.03)
        rrect(ctx, -420, -260, 840, 520, 16)
        fs(ctx, hexc("#fffaf0"), lw=8)
        text(ctx, "MY PROMISE", 0, -180, 70, CHINA_RED, outline=0, shadow=False)
        rrect(ctx, -360, -60, 80, 80, 10)
        fs(ctx, WHITE, lw=6)
        if t > t_no + 0.8:
            kc = ease_out(prog(t, t_no + 0.8, t_no + 1.1))
            ctx.move_to(-350, -20)
            ctx.line_to(-330, 0)
            ctx.line_to(lerp(-330, -270, kc), lerp(0, -80, kc))
            setc(ctx, (0.2, 0.65, 0.3))
            ctx.set_line_width(14)
            ctx.stroke()
        text(ctx, "No more touching", -240, -40, 56, INK, font=HAND_FONT, align="left", outline=0, shadow=False)
        text(ctx, "museum stuff.", -240, 30, 56, INK, font=HAND_FONT, align="left", outline=0, shadow=False)
        text(ctx, "signed: red cap guy", 120, 180, 44, hexc("#2b4f9a"), font=HAND_FONT, outline=0, shadow=False)
        ctx.restore()
    vignette(ctx, 0.45)


def sh_museum(ctx, t, D, cue):
    t_new = cue("New exhibit")
    t_mid = cue("And in the middle")
    t_old = cue("Old.")
    t_sign = cue("The sign")
    pan = ease(prog(t, t_mid - 0.5, t_mid + 1.5))
    cx = lerp(900, 1300, pan)
    z = lerp(1.0, 1.25, ease(prog(t, t_sign - 0.4, t_sign + 0.8)))
    cy = lerp(500, 470, ease(prog(t, t_sign - 0.4, t_sign + 0.8)))
    ctx.save()
    cam(ctx, cx, cy, z)
    museum_bg(ctx, t)
    brick_case(ctx, 1400, 430, t, glow=0.25 + 0.15 * math.sin(t * 3))
    if t < t_mid:
        gx = lerp(-200, 760, ease_out(prog(t, 0, t_mid - 0.3)))
        walking = gx < 750
        guy(ctx, gx, 470, 0.85, t, expr="smile" if t < t_new else "o", face=0.9 if t < t_new else 0.2,
            look=(0, -1) if t > t_new else (1, 0), walk=t * 1.6 if walking else None,
            larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        if t > t_new:
            pop_text(ctx, "ooh!", 900, 250, 60, t - t_new - 0.3, WHITE, font=HAND_FONT, outline=5)
    else:
        tt = t - t_mid
        gx = lerp(760, 1060, ease(prog(tt, 0.2, 1.8)))
        bored = t > t_old
        guy(ctx, gx, 470, 0.85, t, expr="flat" if bored else "smile", face=0.9, look=(1, 0.2),
            walk=t * 1.6 if 0.2 < tt < 1.8 else None, larm=(0.3, 0.2), rarm=(-0.3, -0.2),
            brows=None)
    ctx.restore()
    for i, w in enumerate(("OLD.", "GREY.", "BORING.")):
        tw = cue(w.title().rstrip(".") + ".")
        if t > tw:
            pop_text(ctx, w, 500 + i * 300, 900, 70, t - tw, WHITE, rot=-0.05 + i * 0.04, hold=t_sign - tw + 0.5)
    vignette(ctx, 0.35)


def sh_touch(ctx, t, D, cue):
    ctx.save()
    z = lerp(1.7, 2.1, ease(prog(t, 0, D)))
    cam(ctx, 1300, 420, z)
    museum_bg(ctx, t)
    brick_case(ctx, 1400, 430, t, glow=0.3 + 0.7 * ease(prog(t, D * 0.6, D)), open_=ease(prog(t, 0.1, 0.6)))
    reach = ease(prog(t, D * 0.3, D * 0.75))
    shake = math.sin(t * 60) * 0.05 * (1 - reach)
    guy(ctx, 1180, 400, 1.0, t, expr="worried" if t < D * 0.5 else "grin", face=0.9, look=(1, 0.5),
        larm=(0.3, 0.2), rarm=(lerp(-0.3, -2.1, reach) + shake, lerp(-0.2, 0.0, reach)),
        brows="worried" if t < D * 0.5 else None)
    if t > D * 0.75:
        sparkle(ctx, 1380, 420, 70, t, (1, 1, 0.7))
    ctx.restore()
    # stopwatch
    ctx.save()
    ctx.translate(1600, 200)
    circle(ctx, 0, 0, 110)
    fs(ctx, WHITE, lw=8)
    ctx.rectangle(-18, -150, 36, 40)
    fs(ctx, GOLD, lw=6)
    secs = min(4.0, t / max(0.1, D * 0.8) * 4)
    a = secs / 60 * 2 * math.pi * 15 / 4
    line(ctx, 0, 0, math.sin(a) * 80, -math.cos(a) * 80, 8, RED)
    text(ctx, f"00:0{int(secs)}", 0, 50, 46, INK, outline=0, shadow=False)
    ctx.restore()
    vignette(ctx, 0.45)


def sh_tunnel(y0, y1, hue=(0.75, 0.12, 0.15), hue2=(1.0, 0.8, 0.3)):
    def f(ctx, t, D, cue):
        vortex(ctx, t, hue, hue2, speed=2.0)
        rnd = random.Random(5)
        for i in range(10):
            ph = (t * 0.35 + i / 10) % 1
            a = rnd.random() * 6.28 + t * 0.3
            r = 60 + ph ** 2 * 1300
            if i % 2:
                brick(ctx, W / 2 + math.cos(a) * r, H / 2 + math.sin(a) * r * 0.7, 30 + ph * 140, 14 + ph * 64,
                      stamp=False, rot=t + i)
            else:
                clock_icon(ctx, W / 2 + math.cos(a) * r, H / 2 + math.sin(a) * r * 0.7, 10 + ph * 70, t,
                           back=y1 < y0, rot=t + i)
        ctx.save()
        ctx.translate(W / 2 + 260 * math.sin(t * 0.9), H / 2 + 120 * math.cos(t * 1.3) - 60)
        ctx.rotate(t * 2.5)
        doodle(ctx, 0, -150, 0.6, expr="shock", face=0, larm=(2.4, 0.5), rarm=(-2.4, -0.5), legs=(0.5, -0.5))
        ctx.restore()
        year_counter(ctx, t, D, y0, y1)
        vignette(ctx, 0.6)
    return f


def sh_arrive(ctx, t, D, cue):
    t_front = cue("And in front")
    land = ease_in(prog(t, 0.1, 0.7))
    pan = ease(prog(t, t_front - 0.3, D))
    ctx.save()
    cam(ctx, lerp(500, 1300, pan), lerp(560, 480, pan), lerp(1.25, 0.72, pan))
    landscape(ctx, t)
    gx, gy = 380, lerp(-300, 760, land)
    sq = -0.18 * math.exp(-max(0, t - 0.7) * 6) if t > 0.7 else 0
    awed = t > t_front
    guy(ctx, gx, gy, 0.5, t, expr="o" if not awed else "shock", face=0.8, squash=sq, look=(1, -0.4),
        larm=(0.3, 0.2), rarm=(-0.3, -0.2) if not awed else (-1.2, 0.4))
    ctx.restore()
    if t > t_front + 1.5:
        pop_text(ctx, "WHOA.", 300, 200, 90, t - t_front - 1.5, WHITE)
    caption(ctx, "JINSHANLING, CHINA", "1570 AD · MING DYNASTY", t - 0.8, dur=6, cn="金山岭")
    vignette(ctx, 0.3)


DYN = [("QIN", "221 BC", hexc("#c94a3a")), ("HAN", "206 BC", hexc("#d9903a")), ("N. WEI", "400s", hexc("#8a6ab0")),
       ("SUI", "600s", hexc("#3a8ac9")), ("JIN", "1100s", hexc("#4aa06a")), ("MING", "1368-1644", hexc("#e0b52a"))]


def sh_wallfact(ctx, t, D, cue):
    t_many = cue("It's many walls")
    t_put = cue("Put all")
    t_half = cue("That's about")
    paper_bg(ctx)
    if t < t_put:
        pop_text(ctx, "NOT ONE WALL...", 960, 120, 90, t - 0.2, INK, outline=0)
        if t > t_many:
            pop_text(ctx, "MANY WALLS", 960, 220, 90, t - t_many, CHINA_RED, outline=0, rot=-0.02)
        for i, (name, yr, c) in enumerate(DYN):
            tt = t - t_many - 0.6 - i * 0.55
            if tt <= 0:
                continue
            k = ease(clamp(tt / 0.8))
            y = 360 + i * 105
            xs = [200 + j * 40 for j in range(int(30 * k) + 1)]
            ctx.move_to(xs[0], y + 30 * math.sin(xs[0] * 0.01 + i))
            for x in xs[1:]:
                ctx.line_to(x, y + 30 * math.sin(x * 0.01 + i))
            setc(ctx, c)
            ctx.set_line_width(22)
            ctx.stroke()
            text(ctx, name, 1460, y, 56, c, align="left", outline=5)
            text(ctx, yr, 1720, y, 40, INK, font=HAND_FONT, align="left", outline=0, shadow=False)
    else:
        tt = t - t_put
        n = int(21196 * ease(prog(tt, 0.2, 2.2)))
        pop_text(ctx, f"{n:,} km".replace(",", ","), 960, 200, 140, tt, CHINA_RED)
        text(ctx, "total length of all the walls (2012 survey)", 960, 300, 44, INK, font=HAND_FONT, outline=0,
             shadow=False, alpha=ease(prog(tt, 0.8, 1.2)))
        # Earth with a wall wrapping half around
        ex, ey, r = 960, 700, 260
        circle(ctx, ex, ey, r)
        fs(ctx, hexc("#4a8fd6"), lw=7)
        for dx, dy, rr in ((-90, -60, 100), (80, 70, 80), (130, -120, 60)):
            circle(ctx, ex + dx, ey + dy, rr)
            setc(ctx, hexc("#5fb85a"))
            ctx.fill()
        circle(ctx, ex, ey, r)
        fs(ctx, None, lw=7)
        if t > t_half - 0.3:
            k = ease(prog(t, t_half - 0.3, t_half + 1.5))
            ctx.save()
            ctx.arc(ex, ey, r + 30, math.pi, math.pi + math.pi * k)
            setc(ctx, hexc("#8d877c"))
            ctx.set_line_width(26)
            ctx.stroke()
            ctx.restore()
            pop_text(ctx, "~ HALFWAY AROUND THE EARTH", 960, 1020, 64, t - t_half - 0.8, INK, outline=0)
    vignette(ctx, 0.3)


def sh_ming(ctx, t, D, cue):
    t_ming = cue("The Ming dynasty")
    t_qi = cue("And a famous")
    hollow = cue("And a famous", frac=0.6)
    if t < hollow:
        ctx.save()
        cam(ctx, lerp(900, 1000, ease(prog(t, 0, hollow))), 470, 1.1)
        walkway(ctx, t, tower_x=1500)
        # scaffolding on the tower
        for sx in (1250, 1750):
            line(ctx, sx, 640, sx, 220, 9, hexc("#8a5a2b"))
        for yy in (560, 440, 320):
            line(ctx, 1230, yy, 1770, yy, 7, hexc("#8a5a2b"))
        for i in range(3):
            wx = 300 + i * 170 + 30 * math.sin(t + i)
            worker(ctx, wx, 470, 0.5, t, seed=i, face=0.8, walk=t * 1.2 + i, larm=(0.9, -1.3), rarm=(-0.9, 1.3))
            for b in range(2):
                brick(ctx, wx + 5, 560 - b * 28, 80, 26, stamp=False)
        if t > t_qi:
            k = ease_out(prog(t, t_qi - 0.3, t_qi + 0.4))
            general(ctx, lerp(2000, 1050, k), 450, 0.62, t, face=-0.6 if k < 1 else 0.7, walk=t * 1.5 if k < 1 else None,
                    larm=(0.3, 0.2), rarm=(-2.0, 0.3) if k >= 1 else (-0.3, -0.2), expr="smile")
        guy(ctx, 160, 470, 0.55, t, expr="o", face=0.9, larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        ctx.restore()
        if t > t_ming:
            pop_text(ctx, "STONE + BRICK", 960, 120, 80, t - t_ming, WHITE, hold=t_qi - t_ming - 0.2)
        if t > t_qi + 0.6:
            pop_text(ctx, "GENERAL QI JIGUANG", 960, 120, 84, t - t_qi - 0.6, GOLD)
            text(ctx, "戚继光", 960, 220, 64, WHITE, font=CJK, outline=6, alpha=ease(prog(t, t_qi + 1, t_qi + 1.4)))
    else:
        tt = t - hollow
        paper_bg(ctx)
        # cutaway of a hollow watchtower
        ctx.save()
        ctx.translate(960, 560)
        k = ease_out(prog(tt, 0, 0.6))
        ctx.scale(max(k, 1e-3), max(k, 1e-3))
        ctx.rectangle(-420, -380, 840, 700)
        fs(ctx, hexc("#a69f91"), lw=8)
        ctx.rectangle(-360, -320, 720, 580)
        fs(ctx, hexc("#e8dcc0"), lw=6)
        line(ctx, -360, -30, 360, -30, 10, hexc("#7d776b"))
        for k2 in range(-420, 421, 70):
            ctx.rectangle(k2 - 22, -430, 44, 52)
            fs(ctx, hexc("#a69f91"), lw=5)
        # beds, pots, soldiers
        ctx.rectangle(-330, 170, 260, 40)
        fs(ctx, hexc("#8a5a2b"), lw=5)
        soldier(ctx, -200, 140, 0.32, t, expr="sleep", blink=1.0, face=0.3, larm=(0.3, 0.2), rarm=(-0.3, -0.2),
                tilt=-1.5)
        soldier(ctx, 150, 60, 0.42, t, seed=2, face=-0.5, expr="smile", larm=(0.6, 1.4), rarm=(-0.3, -0.2))
        rice_pot(ctx, 270, 200, 0.35, t, fire_on=False)
        for k2 in range(3):
            line(ctx, -300 + k2 * 40, -290, -300 + k2 * 40, -60, 6, hexc("#6b4428"))
            poly(ctx, [(-310 + k2 * 40, -290), (-290 + k2 * 40, -290), (-300 + k2 * 40, -320)])
            fs(ctx, hexc("#9aa0a8"), lw=3)
        soldier(ctx, 100, -200, 0.32, t, seed=3, face=0.8, expr="flat", larm=(0.3, 0.2), rarm=(-1.4, 0.2))
        ctx.restore()
        pop_text(ctx, "HOLLOW WATCHTOWER", 960, 80, 80, tt - 0.3, CHINA_RED)
        text(ctx, "soldiers lived, slept and cooked inside", 960, 1030, 46, INK, font=HAND_FONT, outline=0,
             shadow=False, alpha=ease(prog(tt, 1.0, 1.4)))
    vignette(ctx, 0.3)


def sh_bricks(ctx, t, D, cue):
    t_sold = cue("Soldiers, farmers")
    t_stamp = cue("And many bricks")
    t_blame = cue("If a brick")
    if t < t_stamp:
        ctx.save()
        cam(ctx, 960, 560, 1.0)
        sky(ctx, False, t)
        mountain_layer(ctx, 470, 200, 1, hexc("#9fb3c4"), mist=(0.93, 0.9, 0.85))
        # a steep mountain path going up-right
        ctx.move_to(-100, 1200)
        ctx.line_to(-100, 980)
        ctx.line_to(2100, 300)
        ctx.line_to(2100, 1200)
        ctx.close_path()
        fs(ctx, hexc("#6f957a"), lw=6)
        ctx.move_to(-100, 990)
        ctx.line_to(2100, 310)
        setc(ctx, hexc("#c9b48a"))
        ctx.set_line_width(40)
        ctx.stroke()
        labels = ["SOLDIER", "FARMER", "PRISONER"]
        for i in range(7):
            ph = (t * 0.06 + i / 7) % 1
            x = lerp(-50, 2050, ph)
            y = lerp(975, 295, ph) - 240 * 0.5
            if i % 3 == 0:
                soldier(ctx, x, y, 0.42, t, seed=i, face=0.9, walk=t * 1.5 + i, larm=(0.9, -1.3), rarm=(-0.9, 1.3))
            else:
                worker(ctx, x, y, 0.42, t, seed=i, face=0.9, walk=t * 1.5 + i, larm=(0.9, -1.3), rarm=(-0.9, 1.3))
            for b in range(3):
                brick(ctx, x + 10, y + 110 - b * 22, 70, 22, stamp=False)
            if t > t_sold and i in (1, 2, 3):
                lab = labels[(i - 1) % 3]
                text(ctx, lab, x, y - 110, 34, WHITE, outline=5, alpha=ease(prog(t, t_sold + (i - 1) * 0.6,
                                                                                   t_sold + (i - 1) * 0.6 + 0.3)))
        ctx.restore()
        pop_text(ctx, "THOUSANDS OF WORKERS", 960, 110, 84, t - 0.4, WHITE)
    else:
        tt = t - t_stamp
        bg_fill(ctx, hexc("#2a2622"))
        z = lerp(1.0, 1.1, ease(prog(tt, 0, D - t_stamp)))
        ctx.save()
        cam(ctx, 960, 540, z)
        crack = ease(prog(t, t_blame + 0.3, t_blame + 1.0))
        brick(ctx, 960, 520, 1100, 480, t, crack=crack)
        ctx.restore()
        pop_text(ctx, "MAKER'S MARK", 960, 110, 80, tt - 0.3, GOLD, hold=t_blame - t_stamp)
        text(ctx, "\"made in the 4th year of Longqing\" (1570)", 960, 940, 48, WHITE, font=HAND_FONT, outline=5,
             alpha=ease(prog(tt, 1.0, 1.4)) * (1 - prog(t, t_blame, t_blame + 0.3)))
        if t > t_blame + 1.0:
            burst(ctx, 1500, 860, 150, t - t_blame - 1.0, "BLAME!", size=60, color=(1, 0.5, 0.4), tcolor=WHITE)
    vignette(ctx, 0.35)


def sh_stamp(ctx, t, D, cue):
    t_your = cue("Your mark")
    t_cant = cue("I can't write")
    t_drew = cue("So I drew")
    t_cap = cue("A tiny cap")
    t_rem = cue("Remember")
    if t < t_cap:
        ctx.save()
        cam(ctx, 900, 480, 1.3)
        walkway(ctx, t)
        foreman(ctx, 1200, 470, 0.7, t, face=-0.8, expr="flat", larm=(-1.2, 0.3) if t < t_your + 1 else (0.3, 0.2),
                rarm=(-0.3, -0.2))
        holding = t > 1.0
        guy(ctx, 700, 470, 0.7, t, expr="o" if t < t_cant else ("worried" if t < t_drew else "sly"), face=0.8,
            larm=(0.3, 0.2), rarm=(-1.2, -0.3) if holding else (-0.3, -0.2), brows="worried" if t_cant < t < t_drew else None)
        # brick on a table
        ctx.rectangle(760, 600, 300, 30)
        fs(ctx, hexc("#8a5a2b"), lw=5)
        brick(ctx, 910, 575, 200, 52, stamp=False)
        if t_cant < t < t_drew + 0.5:
            for i, ch in enumerate("長城磚造"):
                ph = (t * 0.6 + i / 4) % 1
                text(ctx, ch, 600 + i * 70, 320 - ph * 80, 60, INK, font=CJK, outline=0, shadow=False, alpha=1 - ph)
            text(ctx, "???", 700, 230, 70, CHINA_RED, outline=0, shadow=False)
        ctx.restore()
        if t > t_your:
            speech(ctx, 1450, 230, 420, 120, "Your mark.", 60, tail=(-120, 70),
                   alpha=ease(prog(t, t_your, t_your + 0.2)) * (1 - prog(t, t_cant, t_cant + 0.3)))
    else:
        tt = t - t_cap
        bg_fill(ctx, hexc("#2a2622"))
        brick(ctx, 960, 520, 1100, 480, t, cap_mark=back_out(prog(tt, 0.2, 0.6), 2))
        if tt < 0.4:
            ctx.save()
            ctx.translate(1290, lerp(200, 520, ease_in(prog(tt, 0, 0.25))))
            rrect(ctx, -80, -160, 160, 120, 14)
            fs(ctx, hexc("#7a4a2a"), lw=6)
            ctx.rectangle(-30, -260, 60, 100)
            fs(ctx, hexc("#7a4a2a"), lw=6)
            ctx.restore()
        if t > t_rem:
            a = 0.5 + 0.5 * math.sin((t - t_rem) * 8)
            ctx.save()
            circle(ctx, 1225, 560, 130 + 8 * a)
            setc(ctx, GOLD)
            ctx.set_line_width(12)
            ctx.set_dash([40, 22])
            ctx.stroke()
            ctx.restore()
            pop_text(ctx, "REMEMBER THAT BRICK!", 960, 950, 90, t - t_rem, GOLD, rot=-0.03)
    vignette(ctx, 0.35)


def sh_rice(ctx, t, D, cue):
    t_pot = cue("A giant pot")
    t_starv = cue("I was starving")
    t_grab = cue("I grabbed")
    t_glue = cue("It was glue")
    t_scream = cue("I grabbed", frac=0.7)
    ctx.save()
    cam(ctx, 960, 520, 1.2, shake=8 * (prog(t, t_scream, t_scream + 0.1) - prog(t, t_scream + 0.6, t_scream + 1)), t=t)
    walkway(ctx, t)
    rice_pot(ctx, 1150, 600, 0.9, t)
    cook(ctx, 1500, 470, 0.7, t, face=-0.8, expr="shock" if t > t_scream else "smile",
         larm=(-2.4, 0.4) if t > t_scream else (0.3, 0.2), rarm=(2.4, -0.4) if t > t_scream else (-0.3, -0.2),
         brows="angry" if t > t_scream else None)
    sniff = t_pot < t < t_grab
    gx = lerp(400, 720, ease(prog(t, t_pot, t_starv)))
    guy(ctx, gx, 470, 0.7, t, expr="happy" if sniff else ("grin" if t < t_scream else "shock"), face=0.8,
        tilt=0.15 if sniff else 0, look=(1, 0), larm=(0.3, 0.2),
        rarm=(-1.3, -0.3) if t > t_grab else (-0.3, -0.2))
    if t > t_grab:
        ellipse(ctx, gx + 140, 560, 40, 16)
        fs(ctx, hexc("#e9e2cc"), lw=4)
    if sniff:
        for k in range(3):
            ph = (t * 0.8 + k / 3) % 1
            xx = lerp(1050, gx + 60, ph)
            ctx.move_to(xx, 420 + math.sin(ph * 12 + k) * 20)
            ctx.line_to(xx + 40, 420 + math.sin(ph * 12 + k + 1) * 20)
            setc(ctx, WHITE, 0.8)
            ctx.set_line_width(8)
            ctx.stroke()
    ctx.restore()
    if t > t_starv:
        burst(ctx, 380, 260, 120, t - t_starv, "GRRRBL", size=46, color=(1, 0.75, 0.3))
    if t > t_scream:
        burst(ctx, 1500, 200, 160, t - t_scream, "STOP!!", size=70, color=(1, 0.4, 0.35), tcolor=WHITE)
    if t > t_glue:
        pop_text(ctx, "IT'S GLUE.", 960, 960, 110, t - t_glue, WHITE)
    vignette(ctx, 0.35)


def sh_ricefact(ctx, t, D, cue):
    t_sci = cue("Scientists")
    t_still = cue("Some of those")
    paper_bg(ctx)
    k1 = back_out(prog(t, 0.2, 0.6), 1.8)
    k2 = back_out(prog(t, 1.2, 1.6), 1.8)
    k3 = back_out(prog(t, 2.4, 2.8), 1.8)
    ctx.save()
    ctx.translate(350, 380)
    ctx.scale(max(k1, 1e-3), max(k1, 1e-3))
    ellipse(ctx, 0, 40, 170, 70)
    fs(ctx, hexc("#3a3a40"), lw=7)
    ellipse(ctx, 0, 25, 150, 45)
    fs(ctx, hexc("#f4f0e2"), lw=4)
    rnd = random.Random(1)
    for i in range(30):
        ellipse(ctx, rnd.uniform(-120, 120), 25 + rnd.uniform(-25, 25), 8, 4)
        setc(ctx, WHITE)
        ctx.fill()
    for k in range(3):
        ph = (t * 0.6 + k / 3) % 1
        ctx.move_to(-60 + k * 60, -20 - ph * 120)
        ctx.curve_to(-40 + k * 60, -50 - ph * 120, -80 + k * 60, -80 - ph * 120, -60 + k * 60, -110 - ph * 120)
        setc(ctx, (0.6, 0.6, 0.6), 0.7 * (1 - ph))
        ctx.set_line_width(8)
        ctx.stroke()
    text(ctx, "STICKY RICE SOUP", 0, 170, 40, INK, outline=0, shadow=False)
    ctx.restore()
    text(ctx, "+", 680, 420, 120, INK, outline=0, shadow=False, alpha=clamp(k2))
    ctx.save()
    ctx.translate(960, 380)
    ctx.scale(max(k2, 1e-3), max(k2, 1e-3))
    ctx.move_to(-110, -10)
    ctx.curve_to(-60, -120, 60, -120, 110, -10)
    ctx.close_path()
    fs(ctx, hexc("#f2f2ee"), lw=6)
    ctx.move_to(-130, -10)
    ctx.line_to(130, -10)
    ctx.line_to(105, 90)
    ctx.line_to(-105, 90)
    ctx.close_path()
    fs(ctx, hexc("#8a5a2b"), lw=6)
    text(ctx, "石灰", 0, 40, 50, hexc("#f2e6c4"), font=CJK, outline=0, shadow=False)
    ctx.restore()
    text(ctx, "LIME", 960, 550, 40, INK, outline=0, shadow=False, alpha=clamp(k2))
    text(ctx, "=", 1240, 420, 120, INK, outline=0, shadow=False, alpha=clamp(k3))
    ctx.save()
    ctx.translate(1560, 400)
    ctx.scale(max(k3, 1e-3), max(k3, 1e-3))
    for r in range(3):
        for c in range(2):
            brick(ctx, -110 + c * 220 + (110 if r % 2 else 0) - 55, -90 + r * 90, 200, 70, stamp=False)
    text(ctx, "SUPER MORTAR", 0, 190, 40, INK, outline=0, shadow=False)
    ctx.restore()
    if t > t_sci:
        for i, w in enumerate(("STRONGER", "WATER RESISTANT")):
            pop_text(ctx, w, 640 + i * 640, 760, 66, t - t_sci - 0.8 - i * 0.6, hexc("#2f7a3a"), outline=0)
        text(ctx, "(the secret ingredient: amylopectin, a starch in sticky rice)", 960, 850, 40, INK,
             font=HAND_FONT, outline=0, shadow=False, alpha=ease(prog(t, t_sci + 2, t_sci + 2.4)))
    if t > t_still:
        pop_text(ctx, "STILL STANDING AFTER ~500 YEARS", 960, 980, 70, t - t_still, CHINA_RED)
    vignette(ctx, 0.3)


def sh_spill(ctx, t, D, cue):
    t_trip = cue("And I, of course")
    t_sack = cue("A whole sack")
    t_double = cue("Double sticky")
    t_red = cue("The foreman's face")
    t_shrug = cue("Then he shrugged")
    ctx.save()
    cam(ctx, 960, 500, 1.15)
    walkway(ctx, t)
    # mortar trough
    ctx.rectangle(880, 610, 420, 70)
    fs(ctx, hexc("#6b4428"), lw=6)
    ctx.rectangle(895, 615, 390, 30)
    fs(ctx, hexc("#e6e0d0"), lw=0)
    trip = prog(t, t_trip + 0.3, t_trip + 1.2)
    if t < t_trip + 0.3:
        gx = lerp(300, 700, ease(prog(t, 0, t_trip + 0.3)))
        guy(ctx, gx, 470, 0.7, t, expr="smile", face=0.9, walk=t * 1.6, larm=(0.9, -1.3), rarm=(-0.9, 1.3))
        sack(ctx, gx + 50, 560, 0.8)
    else:
        rot = lerp(0, 1.3, ease_in(trip))
        gy = 470 + 120 * ease_in(trip)
        guy(ctx, 760, gy, 0.7, t, expr="shock", face=0.9, tilt=rot, larm=(2.0, 0.2), rarm=(-2.4, 0.2))
        sx = lerp(820, 1080, ease(trip))
        sy = lerp(560, 560, trip) - math.sin(trip * math.pi) * 200
        sack(ctx, sx, sy, 0.8, rot=trip * 3)
        if t > t_sack:
            # rice pouring
            rnd = random.Random(3)
            for i in range(40):
                ph = (t * 1.5 + rnd.random()) % 1
                circle(ctx, 1080 + rnd.uniform(-40, 40), 560 + ph * 70, 6)
                setc(ctx, WHITE)
                ctx.fill()
    redness = ease(prog(t, t_red, t_red + 0.6)) * (1 - ease(prog(t, t_shrug, t_shrug + 0.4)))
    shrug = t > t_shrug
    fm_body = lerpc(hexc("#2f4f7a"), hexc("#2f4f7a"), 0)
    foreman(ctx, 1500, 470, 0.7, t, face=-0.8, expr="frown" if not shrug else "flat",
            brows="angry" if redness > 0.2 else None,
            larm=(1.4, -0.6) if shrug and t < t_shrug + 1.2 else (0.3, 0.2),
            rarm=(-1.4, 0.6) if shrug and t < t_shrug + 1.2 else ((-1.5, -0.3) if t > t_shrug + 1.2 else (-0.3, -0.2)))
    if redness > 0:
        circle(ctx, 1500, 470, 70)
        setc(ctx, (1, 0.15, 0.1), 0.45 * redness)
        ctx.fill()
    if t > t_shrug + 1.2:
        # slapping mortar between bricks
        for b in range(3):
            brick(ctx, 1250 + b * 110, 520 - (b % 2) * 2, 100, 34, stamp=False)
        ph = (t * 2) % 1
        ellipse(ctx, 1300 + ph * 220, 500, 30, 10)
        fs(ctx, hexc("#e6e0d0"), lw=3)
    ctx.restore()
    if t > t_double:
        burst(ctx, 1000, 220, 160, t - t_double, "DOUBLE STICKY", size=46, color=(1, 0.95, 0.75), tcolor=CHINA_RED)
    if t > t_shrug + 0.2:
        pop_text(ctx, "*shrug*", 1560, 940, 70, t - t_shrug - 0.2, WHITE, font=HAND_FONT, outline=6)
    vignette(ctx, 0.35)


def sh_night(ctx, t, D, cue):
    t_wind = cue("The wind")
    t_hid = cue("I hid")
    t_found = cue("and found", frac=0.0) if False else cue("I hid", frac=0.55)
    t_torch = cue("And a torch")
    t_camp = cue("A campfire")
    if t < t_hid:
        ctx.save()
        cam(ctx, 1100, 450, lerp(0.9, 1.1, ease(prog(t, 0, t_hid))))
        landscape(ctx, t, night=True)
        ctx.restore()
        if t > t_wind:
            for i in range(12):
                ph = (t * 1.4 + i / 12) % 1
                y = 200 + (i * 73) % 700
                line(ctx, W * (1 - ph) - 200, y, W * (1 - ph), y + 10, 4, WHITE, 0.4 * math.sin(ph * math.pi))
            pop_text(ctx, "BRRRR...", 960, 900, 90, t - t_wind, (0.7, 0.9, 1.0))
    else:
        ctx.save()
        cam(ctx, 960, 520, 1.15)
        # inside the beacon tower: dark stone room
        bg_fill(ctx, hexc("#1b1c2a"))
        bricks_texture(ctx, -200, -100, 2400, 1300, night=True, seed=3)
        ctx.rectangle(-200, 760, 2400, 400)
        fs(ctx, hexc("#2a2c40"), lw=6)
        rrect(ctx, 200, 150, 220, 300, 110)
        fs(ctx, hexc("#0a0c1a"), lw=6)
        circle(ctx, 330, 230, 30)
        fs(ctx, hexc("#f4f0d8"), lw=3)
        straw_pile(ctx, 1150, 770, 1.4)
        if t < t_torch:
            torch(ctx, 1500, 520, t, rot=0.2, s=0.8)
        found = t > t_found
        has_torch = t > t_torch
        guy(ctx, 750, 470, 0.75, t, expr="worried" if not found else ("grin" if has_torch else "o"), face=0.8,
            tilt=0.03 * math.sin(t * 30) if not found else 0, look=(1, 0.3),
            larm=(-0.9, 1.9) if not found else (0.3, 0.2), rarm=(0.9, -1.9) if not found else
            ((-2.4, 0.2) if has_torch else (-0.3, -0.2)))
        if has_torch:
            torch(ctx, 860, 340, t, rot=0.15, s=0.8)
        ctx.restore()
        if t > t_camp:
            speech(ctx, 1400, 240, 460, 130, "Campfire time!", 60, think=True, tail=(-200, 80),
                   alpha=ease(prog(t, t_camp, t_camp + 0.3)))
    vignette(ctx, 0.5)


def sh_beacon(ctx, t, D, cue):
    t_alarm = cue("That was the alarm")
    t_moment = cue("The moment")
    t_next = cue("Then the next")
    t_chain = cue("A chain of fire")
    if t < t_moment + 0.6:
        ctx.save()
        cam(ctx, 960, 520, 1.15, shake=4 * prog(t, t_alarm, t_alarm + 0.3), t=t)
        bg_fill(ctx, hexc("#1b1c2a"))
        bricks_texture(ctx, -200, -100, 2400, 1300, night=True, seed=3)
        ctx.rectangle(-200, 760, 2400, 400)
        fs(ctx, hexc("#2a2c40"), lw=6)
        straw_pile(ctx, 1150, 770, 1.4)
        k = ease(prog(t, 0.2, 1.4))
        fire(ctx, 1150, 650, 40 + 160 * k, t)
        guy(ctx, 750, 470, 0.75, t, expr="grin" if t < t_alarm else "shock", face=0.8, look=(1, 0),
            larm=(2.2, -0.4) if t < t_alarm else (2.5, 0.3), rarm=(-2.4, 0.2))
        torch(ctx, 860, 340, t, rot=0.15, s=0.8)
        ctx.restore()
        setc(ctx, (1, 0.5, 0.1), 0.15 * k)
        ctx.paint()
        if t > t_alarm:
            pop_text(ctx, "NOT A CAMPFIRE.", 960, 140, 100, t - t_alarm, RED)
    else:
        tt = t - t_moment - 0.6
        z = lerp(1.6, 0.62, ease(prog(tt, 0, 3.5)))
        ctx.save()
        cam(ctx, lerp(1480, 1100, ease(prog(tt, 0, 3.5))), lerp(320, 360, ease(prog(tt, 0, 3.5))), z)
        fires = {}
        ignite = [5, 6, 7, 4, 3, 2, 1, 0]
        for k, i in enumerate(ignite):
            v = tt - k * 0.9
            if v > 0:
                fires[i] = clamp(v / 0.4)
        landscape(ctx, t, night=True, fires=fires)
        ctx.restore()
        if t > t_chain:
            # race bar: fire vs horse
            kk = prog(t, t_chain, D)
            rrect(ctx, 260, 900, 1400, 130, 20)
            fs(ctx, (0.05, 0.05, 0.1, 0.75), lw=0)
            text(ctx, "FIRE", 300, 935, 40, GOLD, align="left", outline=0, shadow=False)
            text(ctx, "HORSE", 300, 995, 40, WHITE, align="left", outline=0, shadow=False)
            line(ctx, 460, 935, 460 + 1150 * ease_out(kk), 935, 18, (1, 0.6, 0.2))
            line(ctx, 460, 995, 460 + 1150 * kk * 0.3, 995, 18, (0.8, 0.8, 0.85))
    vignette(ctx, 0.5)


def sh_beaconfact(ctx, t, D, cue):
    t_one = cue("One fire")
    t_two = cue("Two fires")
    t_three = cue("Three fires")
    t_wind = cue("Thanks to the wind")
    if t < t_wind:
        bg_fill(ctx, hexc("#151827"))
        pop_text(ctx, "THE MING ALARM CODE", 960, 110, 84, t - 0.2, GOLD)
        rows = [(t_one, 1, "~100 RAIDERS"), (t_two, 2, "~500 RAIDERS"), (t_three, 3, "1,000+ RAIDERS")]
        for r, (tc, n, lab) in enumerate(rows):
            if t < tc:
                continue
            y = 330 + r * 230
            a = ease(prog(t, tc, tc + 0.3))
            for k in range(n):
                fire(ctx, 300 + k * 120, y, 42 * a, t + k)
            for k in range(n):
                circle(ctx, 800 + k * 90, y, 26 * a)
                fs(ctx, hexc("#3b404a"), lw=4)
                line(ctx, 800 + k * 90, y, 840 + k * 90, y - 20, 10, hexc("#3b404a"))
            text(ctx, "+", 640, y, 70, WHITE, outline=0, shadow=False, alpha=a)
            text(ctx, "=", 1130, y, 70, WHITE, outline=0, shadow=False, alpha=a)
            pop_text(ctx, lab, 1500, y, 66, t - tc - 0.2, [WHITE, (1, 0.7, 0.3), RED][r])
        text(ctx, "fires (or smoke by day) + cannon shots", 960, 1020, 40, WHITE, font=HAND_FONT, outline=0,
             shadow=False, alpha=ease(prog(t, t_one + 1, t_one + 1.4)))
    else:
        tt = t - t_wind
        ctx.save()
        cam(ctx, 960, 520, 1.1)
        bg_fill(ctx, hexc("#1b1c2a"))
        bricks_texture(ctx, -200, -100, 2400, 1300, night=True, seed=3)
        ctx.rectangle(-200, 760, 2400, 400)
        fs(ctx, hexc("#2a2c40"), lw=6)
        for k in range(3):
            straw_pile(ctx, 700 + k * 380, 770, 1.0)
            a = ease(prog(tt, k * 0.5, k * 0.5 + 0.5))
            fire(ctx, 700 + k * 380, 680, 120 * a, t + k)
        for i in range(10):
            ph = (t * 1.6 + i / 10) % 1
            y = 200 + (i * 61) % 400
            line(ctx, 200 + ph * 1600, y, 400 + ph * 1600, y, 5, WHITE, 0.35 * math.sin(ph * math.pi))
        ctx.restore()
        setc(ctx, (1, 0.45, 0.1), 0.18)
        ctx.paint()
        pop_text(ctx, "3 FIRES = 1,000+ RAIDERS!", 960, 140, 90, tt - 1.0, RED)
    vignette(ctx, 0.5)


def night_walkway(ctx, t, fire_big=True):
    walkway(ctx, t, night=True, flicker=1.0)
    if fire_big:
        straw_pile(ctx, 1450, 650, 1.0)
        fire(ctx, 1450, 520, 150, t)


def sh_panic(ctx, t, D, cue):
    t_sold = cue("Soldiers pouring")
    t_me = cue("And me")
    t_trouble = cue("I was going")
    ctx.save()
    cam(ctx, 1000, 470, 1.05, shake=3, t=t)
    night_walkway(ctx, t)
    for i in range(7):
        sx = -300 + ((t - t_sold) * 260 + i * 260) % 1900 if t > t_sold else -400
        soldier(ctx, sx, 480, 0.6, t, seed=i, face=0.9, walk=t * 2.2 + i * 0.3, expr="shock",
                larm=(0.3, 0.2), rarm=(-2.5, 0.2))
        line(ctx, sx + 50, 420, sx + 60, 200, 7, hexc("#6b4428"))
        poly(ctx, [(sx + 52, 205), (sx + 68, 205), (sx + 62, 160)])
        fs(ctx, hexc("#c9ccd2"), lw=3)
    guy(ctx, 1200, 470, 0.72, t, expr="shock" if t < t_trouble else "worried", face=0.0, look=(-1, 0),
        larm=(0.3, 0.2), rarm=(-2.4, 0.2), brows="worried")
    torch(ctx, 1310, 340, t, rot=0.15, s=0.8)
    if t > t_trouble:
        sweat(ctx, 1290, 360, 1.3, t)
    ctx.restore()
    for i, w in enumerate(("BOOM!", "BOOM!")):
        pop_text(ctx, w, 300 + i * 260, 200 + i * 60, 70, t - 0.2 - i * 0.6, (1, 0.7, 0.3), rot=-0.1 + i * 0.15,
                 hold=1.2)
    if t > cue("Horns"):
        pop_text(ctx, "HOOOONK!", 1500, 150, 80, t - cue("Horns"), (1, 0.85, 0.4), hold=1.4)
    if t > t_trouble:
        pop_text(ctx, "SO MUCH TROUBLE.", 960, 980, 100, t - t_trouble, RED)
    vignette(ctx, 0.55)


def sh_twist(ctx, t, D, cue):
    t_down = cue("Down below")
    t_right = cue("Right under")
    if t < t_down:
        ctx.save()
        cam(ctx, 1000, 470, 1.2)
        night_walkway(ctx, t)
        soldier(ctx, 800, 470, 0.7, t, face=-0.9, expr="shock", larm=(-1.9, 0.0), rarm=(-0.3, -0.2))
        guy(ctx, 1150, 470, 0.72, t, expr="o", face=-0.9, look=(-1, 0.5), larm=(0.3, 0.2), rarm=(-2.4, 0.2))
        ctx.restore()
        pop_text(ctx, "LOOK!", 560, 230, 90, t - 0.6, WHITE)
    else:
        tt = t - t_down
        ctx.save()
        cam(ctx, 1040, lerp(600, 760, ease(prog(tt, 0, 2))), lerp(1.4, 1.7, ease(prog(tt, 0, D - t_down))))
        landscape(ctx, t, night=True, fires={3: 1, 4: 1, 5: 1}, glue_glow=ease(prog(t, t_right, t_right + 0.6)))
        # raiders frozen in the firelight
        g = cairo.RadialGradient(1040, 880, 30, 1040, 880, 420)
        g.add_color_stop_rgba(0, 1, 0.6, 0.2, 0.35)
        g.add_color_stop_rgba(1, 1, 0.6, 0.2, 0)
        ctx.set_source(g)
        circle(ctx, 1040, 880, 420)
        ctx.fill()
        for i in range(6):
            rx = 880 + i * 60
            raider(ctx, rx, 860 + (i % 2) * 20, 0.17, t, seed=i, face=0.5, expr="shock", look=(0.5, -1),
                   larm=(0.3, 0.2), rarm=(-0.6, -0.8))
        ladder(ctx, 860, 930, 960, 760, 30)
        ladder(ctx, 1150, 940, 1100, 770, 30)
        ctx.restore()
        pop_text(ctx, "RAIDERS!", 960, 140, 110, tt - 0.5, RED)
        if t > t_right:
            pop_text(ctx, "THE DOUBLE-RICE SECTION", 960, 980, 70, t - t_right - 0.4, GOLD)
    vignette(ctx, 0.5)


def sh_battle(ctx, t, D, cue):
    t_push = cue("They pushed")
    t_move = cue("But that section")
    t_not = cue("Not one brick")
    t_looked = cue("The raiders looked")
    t_home = cue("and decided", frac=0.0) if False else cue("The raiders looked", frac=0.8)
    ctx.save()
    cam(ctx, 960, 560, 1.0, shake=4 * (prog(t, t_push, t_push + 0.2) - prog(t, t_move, t_move + 0.3)), t=t)
    # front view: big wall face, soldiers on top, raiders below
    sky(ctx, True, t)
    mountain_layer(ctx, 450, 160, 1, hexc("#1d2444"))
    ctx.rectangle(-200, 260, 2400, 560)
    fs(ctx, hexc("#3a3e5a"), lw=6)
    bricks_texture(ctx, -200, 260, 2400, 560, night=True, seed=5, bw=150, bh=56)
    for k in range(-200, 2200, 160):
        ctx.rectangle(k, 190, 100, 72)
        fs(ctx, hexc("#3a3e5a"), lw=6)
    gg = ease(prog(t, t_move, t_move + 0.5))
    if gg > 0:
        rrect(ctx, 600, 270, 720, 540, 20)
        setc(ctx, (1, 0.95, 0.6), 0.12 * gg)
        ctx.fill()
        rrect(ctx, 600, 270, 720, 540, 20)
        ctx.save()
        ctx.set_dash([30, 18])
        setc(ctx, (1, 0.95, 0.6), 0.8 * gg)
        ctx.set_line_width(8)
        ctx.stroke()
        ctx.restore()
    for i in range(6):
        sx = 250 + i * 290
        soldier(ctx, sx, 125, 0.42, t, seed=i, face=0.0, expr="flat" if t < t_looked else "grin",
                larm=(0.3, 0.2), rarm=(-2.6, 0.3))
    fire(ctx, 1750, 120, 70, t)
    ctx.rectangle(-200, 820, 2400, 400)
    fs(ctx, hexc("#151a2e"), lw=6)
    leaving = t > t_home
    for i in range(5):
        rx = 520 + i * 230
        if leaving:
            rx += (t - t_home) * 220 * (1 if i % 2 else -1)
        tug = math.sin(t * 9 + i) * 0.4 if t_push < t < t_looked else 0
        raider(ctx, rx, 760, 0.5, t, seed=i, face=0.0 if not leaving else (0.9 if i % 2 else -0.9),
               expr=("worried" if t > t_not else "flat") if t < t_looked else "frown", look=(0, -1) if t > t_looked else (0, 0),
               walk=t * 2 if leaving else None, larm=(2.6 + tug, 0.2), rarm=(-2.6 - tug, -0.2),
               flip=False)
        if not leaving:
            line(ctx, rx - 40, 640, rx - 60 + tug * 60, 300, 4, hexc("#8a6a42"))
            circle(ctx, rx - 60 + tug * 60, 300, 12)
            fs(ctx, hexc("#9aa0a8"), lw=4)
    if not leaving:
        ladder(ctx, 400, 820, 470, 260, 60)
        ladder(ctx, 1500, 820, 1440, 260, 60)
    ctx.restore()
    if t > t_push:
        pop_text(ctx, "PUSH!", 300, 900, 70, t - t_push, (1, 0.7, 0.3), hold=t_move - t_push)
        pop_text(ctx, "PULL!", 1600, 900, 70, t - t_push - 0.5, (1, 0.7, 0.3), hold=t_move - t_push)
    if t > t_not:
        pop_text(ctx, "NOT ONE BRICK.", 960, 980, 100, t - t_not, GOLD, hold=t_looked - t_not + 0.5)
    if t > t_home + 0.3:
        speech(ctx, 960, 960, 520, 110, "...let's go home.", 56, tail=(0, -100), alpha=ease(prog(t, t_home + 0.3, t_home + 0.6)))
    vignette(ctx, 0.5)


def sh_hero(ctx, t, D, cue):
    t_off = cue("The officers")
    t_nobody = cue("Nobody asked")
    t_vol = cue("I didn't volunteer")
    ctx.save()
    cam(ctx, 960, 480, 1.1)
    walkway(ctx, t)
    setc(ctx, (1, 0.6, 0.3), 0.15)
    ctx.paint()
    for i in range(5):
        jump = abs(math.sin(t * 5 + i)) * 40
        soldier(ctx, 250 + i * 190, 470 - jump, 0.55, t, seed=i, face=0.3, expr="laugh",
                larm=(2.6, 0.2), rarm=(-2.6, -0.2))
    if t > t_off - 0.3:
        foreman(ctx, 1350, 470, 0.68, t, face=-0.4, expr="grin", larm=(0.3, 0.2), rarm=(-2.0, 0.2))
    whistle = t > t_nobody
    guy(ctx, 1650, 470, 0.68, t, expr="o" if whistle else "smile", face=0.9 if whistle else -0.5,
        look=(1, -1) if whistle else (0, 0), larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    ctx.restore()
    pop_text(ctx, "HOORAY!", 600, 160, 100, t - 0.3, GOLD, hold=t_nobody - 0.5)
    if t > t_off:
        speech(ctx, 1300, 230, 560, 120, "Who raised the alarm?", 52, tail=(40, 80),
               alpha=ease(prog(t, t_off + 0.5, t_off + 0.8)) * (1 - prog(t, t_nobody, t_nobody + 0.3)))
    if t > t_nobody:
        for k in range(3):
            ph = (t * 0.7 + k / 3) % 1
            text(ctx, "♪", 1820 + ph * 60, 250 - ph * 120, 60, WHITE, font="DejaVu Sans", outline=4, alpha=1 - ph)
    if t > t_vol:
        pop_text(ctx, "*whistles innocently*", 1360, 980, 70, t - t_vol, WHITE, font=HAND_FONT, outline=6)
    vignette(ctx, 0.35)


def sh_peace(ctx, t, D, cue):
    t_think = cue("I'd like")
    t_didnt = cue("I definitely")
    paper_bg(ctx, hexc("#e9dcbc"))
    k = ease_out(prog(t, 0.2, 1.2))
    # scroll unrolling
    w = 1400 * k
    ctx.rectangle(960 - w / 2, 220, w, 560)
    fs(ctx, hexc("#f6ecd2"), lw=6)
    for sx in (960 - w / 2, 960 + w / 2):
        rrect(ctx, sx - 22, 190, 44, 620, 18)
        fs(ctx, hexc("#7a4a2a"), lw=6)
    if k > 0.9:
        a = ease(prog(t, 1.2, 1.6))
        text(ctx, "1571", 960, 300, 90, CHINA_RED, outline=0, shadow=False, alpha=a)
        text(ctx, "PEACE WITH ALTAN KHAN", 960, 390, 62, INK, outline=0, shadow=False, alpha=a)
        text(ctx, "和", 1500, 330, 120, CHINA_RED, font=CJK, outline=0, shadow=False, alpha=a)
        foreman(ctx, 880, 530, 0.45, t, face=0.8, expr="smile", larm=(0.3, 0.2), rarm=(-1.5, 0.2))
        raider(ctx, 1040, 530, 0.45, t, face=-0.8, expr="smile", larm=(1.5, -0.2), rarm=(-0.3, -0.2))
        text(ctx, "border markets open · calmer for decades", 960, 740, 44, INK, font=HAND_FONT, outline=0,
             shadow=False, alpha=ease(prog(t, 2.5, 3.0)))
    if t > t_think:
        kk = ease_out(prog(t, t_think, t_think + 0.4))
        guy(ctx, 1700, lerp(1300, 760, kk), 0.6, t, expr="sly" if t < t_didnt else "flat", face=-0.6,
            larm=(2.2, -0.4) if t < t_didnt else (1.4, -0.6), rarm=(-0.3, -0.2) if t < t_didnt else (-1.4, 0.6))
    if t > t_didnt:
        pop_text(ctx, "(I DIDN'T.)", 960, 960, 80, t - t_didnt, CHINA_RED)
    vignette(ctx, 0.3)


def sh_myth(ctx, t, D, cue):
    t_heard = cue("You've probably heard")
    t_isnt = cue("It isn't")
    t_yang = cue("In two thousand")
    bg_fill(ctx, hexc("#03050d"))
    rnd = random.Random(9)
    for i in range(200):
        circle(ctx, rnd.random() * W, rnd.random() * H, 1 + rnd.random() * 2)
        setc(ctx, WHITE, 0.3 + 0.5 * rnd.random())
        ctx.fill()
    # Earth limb
    z = lerp(1.0, 1.08, ease(prog(t, 0, D)))
    ctx.save()
    cam(ctx, W / 2, H / 2, z)
    g = cairo.RadialGradient(960, 2200, 1300, 960, 2200, 1500)
    g.add_color_stop_rgba(0, 0.4, 0.7, 1, 0.9)
    g.add_color_stop_rgba(1, 0.4, 0.7, 1, 0)
    ctx.set_source(g)
    circle(ctx, 960, 2200, 1500)
    ctx.fill()
    circle(ctx, 960, 2200, 1350)
    setc(ctx, hexc("#3a7fc6"))
    ctx.fill()
    ctx.save()
    circle(ctx, 960, 2200, 1350)
    ctx.clip()
    for dx, dy, r in ((-400, -1150, 260), (200, -1250, 200), (600, -1080, 220)):
        circle(ctx, 960 + dx, 2200 + dy, r)
        setc(ctx, hexc("#6aa860"))
        ctx.fill()
    for i in range(5):
        cloud(ctx, 400 + i * 300 + t * 10, 1000 + (i % 2) * 40, 0.8)
    ctx.restore()
    circle(ctx, 960, 2200, 1350)
    fs(ctx, None, lw=6)
    ctx.restore()
    if t < t_yang:
        pop_text(ctx, "VISIBLE FROM SPACE?", 960, 150, 100, t - t_heard, WHITE)
        if t > t_isnt:
            k = back_out(prog(t, t_isnt, t_isnt + 0.3), 2)
            ctx.save()
            ctx.translate(960, 480)
            ctx.scale(max(k, 1e-3), max(k, 1e-3))
            ctx.rotate(-0.1)
            rrect(ctx, -260, -90, 520, 180, 20)
            fs(ctx, None, lw=14, stroke=RED)
            text(ctx, "MYTH", 0, 0, 130, RED, outline=0, shadow=False)
            ctx.restore()
            text(ctx, "not with the naked eye: the wall is long, but narrow", 960, 680, 46, WHITE,
                 font=HAND_FONT, outline=0, shadow=False, alpha=ease(prog(t, t_isnt + 1.5, t_isnt + 1.9)))
    else:
        tt = t - t_yang
        # capsule with astronaut at the window
        k = ease_out(prog(tt, 0, 1.0))
        ctx.save()
        ctx.translate(lerp(2300, 1250, k), 430)
        ctx.rotate(-0.15)
        ctx.move_to(-260, -170)
        ctx.line_to(200, -110)
        ctx.line_to(200, 110)
        ctx.line_to(-260, 170)
        ctx.close_path()
        fs(ctx, hexc("#d9dde2"), lw=7)
        ctx.rectangle(200, -80, 160, 160)
        fs(ctx, hexc("#b8bec6"), lw=6)
        for sx in (-1, 1):
            ctx.rectangle(240, sx * 90 - (90 if sx < 0 else 0) + (0 if sx < 0 else 0), 380, 90 * sx)
            fs(ctx, hexc("#2b4f8a"), lw=5)
        circle(ctx, -60, 0, 95)
        fs(ctx, hexc("#0e1a33"), lw=7)
        ctx.save()
        circle(ctx, -60, 0, 90)
        ctx.clip()
        circle(ctx, -60, 20, 60)
        fs(ctx, WHITE, lw=5)
        ellipse(ctx, -60, 15, 42, 30)
        fs(ctx, hexc("#e8b84a"), lw=4)
        ctx.restore()
        ctx.restore()
        pop_text(ctx, "YANG LIWEI · SHENZHOU 5 · 2003", 960, 140, 70, tt - 0.8, GOLD)
        text(ctx, "China's first astronaut", 960, 230, 48, WHITE, font=HAND_FONT, outline=0, shadow=False,
             alpha=ease(prog(tt, 1.4, 1.8)))
        if t > cue("and couldn't"):
            speech(ctx, 600, 520, 480, 120, "I can't see it!", 58, tail=(260, 40),
                   alpha=ease(prog(t, cue("and couldn't"), cue("and couldn't") + 0.3)))
    vignette(ctx, 0.5)


def sh_return(ctx, t, D, cue):
    t_closer = cue("But this time")
    t_corner = cue("In the corner")
    if t < t_closer:
        ctx.save()
        cam(ctx, 1150, 500, 1.0)
        museum_bg(ctx, t)
        brick_case(ctx, 1400, 430, t, glow=0.15)
        land = ease_out(prog(t, 0, 0.5))
        sq = -0.15 * math.exp(-max(0, t - 0.5) * 6) if t > 0.5 else 0
        guy(ctx, 1050, lerp(-300, 470, land), 0.85, t, expr="smile", squash=sq, face=0.9, look=(1, 0),
            larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        ctx.restore()
    else:
        tt = t - t_closer
        bg_fill(ctx, hexc("#2a2622"))
        z = lerp(1.0, 1.9, ease(prog(t, t_corner, t_corner + 1.6)))
        ctx.save()
        cam(ctx, lerp(960, 1225, ease(prog(t, t_corner, t_corner + 1.6))), 550, z)
        brick(ctx, 960, 520, 1100, 480, t, cap_mark=1.0)
        if t > t_corner + 1.6:
            ctx.save()
            circle(ctx, 1225, 560, 130 + 6 * math.sin(t * 8))
            setc(ctx, GOLD)
            ctx.set_line_width(8)
            ctx.set_dash([30, 18])
            ctx.stroke()
            ctx.restore()
        ctx.restore()
        if t > t_corner + 1.8:
            pop_text(ctx, "MY CAP!", 960, 950, 120, t - t_corner - 1.8, RED, rot=-0.03)
    vignette(ctx, 0.45)


def sh_ending(ctx, t, D, cue):
    t_set = cue("I set it on fire")
    t_still = cue("But it's still")
    t_welcome = cue("You're welcome")
    if t < t_still:
        spiral_bg(ctx, t, speed=0.2)
        guy(ctx, 420, 470, 0.95, t, expr="smile" if t < t_set else "worried", face=0.5,
            larm=(0.3, 0.2), rarm=(-1.6, 0.4), brows="worried" if t > t_set else None)
        items = [("SET IT ON FIRE", "fire"), ("FILLED IT WITH RICE", "rice"), ("ALMOST STARTED A WAR", "war")]
        for i, (lab, kind) in enumerate(items):
            tc = cue("I set it on fire", frac=[0.0, 0.33, 0.66][i]) if i < 2 else cue("and almost")
            if t < tc:
                continue
            y = 260 + i * 240
            a = ease(prog(t, tc, tc + 0.3))
            if kind == "fire":
                fire(ctx, 860, y + 20, 60 * a, t)
            elif kind == "rice":
                ellipse(ctx, 860, y + 10, 70 * a, 30 * a)
                fs(ctx, hexc("#f4f0e2"), lw=5)
            else:
                line(ctx, 810, y - 50, 910, y + 50, 12 * a, hexc("#9aa0a8"))
                line(ctx, 910, y - 50, 810, y + 50, 12 * a, hexc("#9aa0a8"))
            pop_text(ctx, lab, 1350, y, 64, t - tc, WHITE, font=TITLE_FONT)
            # checkmark
            ctx.save()
            ctx.translate(1350 + text_width(ctx, lab, 64) / 2 + 70, y)
            ctx.move_to(-20, 0)
            ctx.line_to(0, 22)
            ctx.line_to(36, -30)
            setc(ctx, (0.4, 0.9, 0.4), a)
            ctx.set_line_width(12)
            ctx.stroke()
            ctx.restore()
    else:
        ctx.save()
        cam(ctx, lerp(900, 1300, ease(prog(t, t_still, D))), 450, 0.62)
        landscape(ctx, t)
        ctx.restore()
        pop_text(ctx, "STILL STANDING.", 960, 160, 110, t - t_still, WHITE)
        if t > t_welcome:
            k = ease_out(prog(t, t_welcome - 0.2, t_welcome + 0.3))
            guy(ctx, 1600, lerp(1400, 760, k), 0.8, t, expr="sly", face=-0.4, larm=(0.3, 0.2), rarm=(-2.2, 0.8))
            pop_text(ctx, "YOU'RE WELCOME.", 960, 960, 110, t - t_welcome, GOLD, rot=-0.03)
    vignette(ctx, 0.45)


def sh_outro(ctx, t, D, cue):
    t_prob = cue("Probably")
    # living room: sofa + TV advertising the next exhibit
    vgrad(ctx, 0, 0, W, 800, hexc("#d9c7a8"), hexc("#c9b490"))
    ctx.rectangle(0, 780, W, 300)
    fs(ctx, hexc("#8a6a4a"), lw=6)
    rrect(ctx, 260, 560, 760, 260, 40)
    fs(ctx, hexc("#4a6a8a"), lw=7)
    rrect(ctx, 220, 500, 120, 300, 40)
    fs(ctx, hexc("#3f5c7a"), lw=7)
    rrect(ctx, 940, 500, 120, 300, 40)
    fs(ctx, hexc("#3f5c7a"), lw=7)
    guy(ctx, 640, 470, 0.72, t, expr="smile" if t < t_prob else "sly", face=0.9, look=(1, 0),
        larm=(0.3, 0.2), rarm=(-1.2, 0.5), legs=(-1.2, -1.2), show_legs=True)
    # TV
    ctx.rectangle(1300, 700, 400, 120)
    fs(ctx, hexc("#5a3a22"), lw=6)
    rrect(ctx, 1220, 300, 560, 400, 20)
    fs(ctx, hexc("#1a1a1f"), lw=8)
    ctx.save()
    rrect(ctx, 1250, 330, 500, 340, 10)
    ctx.clip()
    vgrad(ctx, 1250, 330, 500, 340, hexc("#f4c870"), hexc("#e89a40"))
    poly(ctx, [(1340, 620), (1460, 430), (1580, 620)])
    fs(ctx, hexc("#d9a050"), lw=5)
    poly(ctx, [(1520, 620), (1620, 480), (1720, 620)])
    fs(ctx, hexc("#c99040"), lw=5)
    text(ctx, "NEW EXHIBIT:", 1500, 370, 36, INK, outline=0, shadow=False)
    text(ctx, "ANCIENT EGYPT", 1500, 410, 40, CHINA_RED, outline=0, shadow=False)
    ctx.restore()
    if t > t_prob:
        pop_text(ctx, "...probably.", 960, 160, 100, t - t_prob, GOLD, font=HAND_FONT, outline=8)
    vignette(ctx, 0.4)


def sh_endcard(ctx, t, D, cue):
    spiral_bg(ctx, t, speed=0.3)
    k = ease_out(prog(t, 0.0, 0.6))
    guy(ctx, 560, lerp(1400, 470, k), 1.05, t, expr="grin", face=0.4,
        larm=(0.3, 0.2), rarm=(-2.6 + 0.3 * math.sin(t * 7), 0.5))
    pop_text(ctx, "HISTORY WORLD", 1300, 260, 120, t - 0.4, WHITE)
    tb = t - 1.0
    if tb > 0:
        kk = back_out(clamp(tb / 0.4), 2) * (1 + 0.04 * math.sin(t * 5))
        ctx.save()
        ctx.translate(1300, 520)
        ctx.scale(max(kk, 1e-3), max(kk, 1e-3))
        rrect(ctx, -300, -80, 600, 160, 40)
        fs(ctx, hexc("#ff2a2a"), lw=8)
        text(ctx, "SUBSCRIBE", 0, 0, 84, WHITE, outline=6)
        ctx.restore()
    if t > 1.8:
        text(ctx, "Next time: Ancient Egypt. What could go wrong?", 1300, 760, 46, WHITE, font=HAND_FONT,
             outline=5, alpha=ease(prog(t, 1.8, 2.4)))
    if t > 2.4:
        kb = ease_in(prog(t, 2.4, 3.0))
        brick(ctx, 1300, lerp(-200, 900, kb), 200, 90, stamp=True, cap_mark=1.0, rot=(1 - kb) * 4)
    fade = prog(t, D - 1.0, D)
    if fade > 0:
        setc(ctx, (0, 0, 0), fade)
        ctx.paint()


SHOT_FUNCS = {
    "hook": sh_hook, "rewind": sh_rewind, "title": sh_title, "intro": sh_intro, "museum": sh_museum,
    "touch": sh_touch, "tunnel1": sh_tunnel(2026, 1570), "arrive": sh_arrive, "wallfact": sh_wallfact,
    "ming": sh_ming, "bricks": sh_bricks, "stamp": sh_stamp, "rice": sh_rice, "ricefact": sh_ricefact,
    "spill": sh_spill, "night": sh_night, "beacon": sh_beacon, "beaconfact": sh_beaconfact, "panic": sh_panic,
    "twist": sh_twist, "battle": sh_battle, "hero": sh_hero, "peace": sh_peace, "myth": sh_myth,
    "tunnel2": sh_tunnel(1570, 2026, hue=(0.2, 0.25, 0.7), hue2=(0.9, 0.75, 0.3)),
    "return": sh_return, "ending": sh_ending, "outro": sh_outro, "endcard": sh_endcard,
}


def cloud(ctx, x, y, s=1.0, c=WHITE):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for dx, dy, r in ((-80, 10, 50), (-20, -20, 70), (60, 0, 55), (110, 20, 38)):
        circle(ctx, dx, dy, r)
    ctx.rectangle(-130, 10, 270, 48)
    setc(ctx, c, 0.95)
    ctx.fill()
    ctx.restore()
