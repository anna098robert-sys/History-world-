"""Shots for 'I Accidentally Stole the Mona Lisa!'.
Each shot: fn(ctx, t, D, cue). cue(text) -> start time (s) of the sentence containing text."""
import math, random
import cairo
from gfx import *
from helpers import *
from egypt_lib import (guy, bedroom_bg, caption, confetti, paper_lesson, bc_counter, polyline_part, lerp2)

TIMELINE = {}          # filled by render.Renderer: id -> (shot, cue)

STONE = hexc("#efe3c8")       # Paris limestone
STONE_D = hexc("#d6c49e")
ROOF = hexc("#6d7a8c")        # zinc mansard roofs
ROOF_D = hexc("#556172")
COBBLE = hexc("#9a8f80")
COBBLE_D = hexc("#7d7366")
SKY_T = hexc("#8fc8ee")
SKY_B = hexc("#e8f4fb")
NAVY = hexc("#1f2c4a")
GUARD_G = hexc("#2f4a3a")
WALL_RED = hexc("#8a2a2a")
PARQUET = hexc("#b07a45")
PARQUET_D = hexc("#8f5f33")
CLOTH = hexc("#d9c7a0")
COAT = hexc("#dfe6ee")
BREAD = hexc("#e0a24f")
BREAD_D = hexc("#b87a2c")
NIGHT_T = hexc("#0d1430")
NIGHT_B = hexc("#2c3a66")


# ====================================================================== little helpers
def run_kw(t, sp=3.0, face=0.9):
    """keyword args for a running doodle."""
    sw = math.sin(t * sp * 2 * math.pi)
    return dict(walk=t * sp, face=face, larm=(0.9 * sw, 0.9), rarm=(0.9 * sw, -0.9))


def whistle_marks(ctx, x, y, t, s=1.0):
    for k in range(3):
        ph = (t * 3 + k / 3) % 1
        a = -0.6 + k * 0.6
        r = 30 + ph * 60
        line(ctx, x + math.cos(a) * r * s, y + math.sin(a) * r * s, x + math.cos(a) * (r + 25) * s,
             y + math.sin(a) * (r + 25) * s, 5, INK, 1 - ph)


def dust_puffs(ctx, x, y, t, n=5, c=(0.85, 0.82, 0.75)):
    for k in range(n):
        ph = (t * 2 + k / n) % 1
        circle(ctx, x - ph * 120 - k * 10, y - ph * 30, 14 + ph * 26)
        setc(ctx, c, 0.6 * (1 - ph))
        ctx.fill()


def speed_lines(ctx, x, y, n=6, length=260, a=0.7, c=INK, seed=1):
    rnd = random.Random(seed)
    for k in range(n):
        yy = y - 120 + k * 45 + rnd.uniform(-8, 8)
        xx = x - rnd.uniform(0, 60)
        line(ctx, xx, yy, xx - length * rnd.uniform(0.6, 1), yy, 5, c, a)


# ====================================================================== props
def mona(ctx, x, y, w, h, frame=True):
    """cartoon Mona Lisa panel centred at (x, y)."""
    ctx.save()
    ctx.translate(x - w / 2, y - h / 2)
    if frame:
        rrect(ctx, -10, -10, w + 20, h + 20, 4)
        fs(ctx, hexc("#5a3a1a"), lw=5)
    ctx.save()
    ctx.rectangle(0, 0, w, h)
    ctx.clip()
    g = cairo.LinearGradient(0, 0, 0, h)
    g.add_color_stop_rgb(0, *hexc("#9fb08a"))
    g.add_color_stop_rgb(0.45, *hexc("#6f7f5a"))
    g.add_color_stop_rgb(1, *hexc("#3a3a22"))
    ctx.set_source(g)
    ctx.paint()
    # winding path and hills
    ctx.move_to(0, h * 0.38)
    ctx.curve_to(w * 0.2, h * 0.3, w * 0.3, h * 0.45, w * 0.15, h * 0.5)
    setc(ctx, hexc("#b89a6a"))
    ctx.set_line_width(w * 0.03)
    ctx.stroke()
    ctx.move_to(w, h * 0.33)
    ctx.curve_to(w * 0.85, h * 0.4, w * 0.95, h * 0.48, w * 0.8, h * 0.52)
    ctx.stroke()
    # body (dark dress) + hands
    ctx.move_to(w * 0.18, h)
    ctx.curve_to(w * 0.2, h * 0.62, w * 0.3, h * 0.5, w * 0.5, h * 0.5)
    ctx.curve_to(w * 0.7, h * 0.5, w * 0.8, h * 0.62, w * 0.82, h)
    ctx.close_path()
    setc(ctx, hexc("#2e2a1e"))
    ctx.fill()
    ctx.move_to(w * 0.4, h * 0.53)
    ctx.curve_to(w * 0.45, h * 0.62, w * 0.55, h * 0.62, w * 0.6, h * 0.53)
    setc(ctx, hexc("#e2bd84"))
    ctx.fill()
    ellipse(ctx, w * 0.47, h * 0.86, w * 0.12, h * 0.045)
    setc(ctx, hexc("#e2bd84"))
    ctx.fill()
    # hair + veil
    ellipse(ctx, w * 0.5, h * 0.32, w * 0.2, h * 0.21)
    setc(ctx, hexc("#2a1e14"))
    ctx.fill()
    # face
    ellipse(ctx, w * 0.5, h * 0.31, w * 0.13, h * 0.15)
    setc(ctx, hexc("#e8c48a"))
    ctx.fill()
    for ex in (0.45, 0.55):
        circle(ctx, w * ex, h * 0.29, max(1.5, w * 0.012))
        setc(ctx, hexc("#2a1e14"))
        ctx.fill()
    ctx.move_to(w * 0.46, h * 0.37)
    ctx.curve_to(w * 0.49, h * 0.385, w * 0.52, h * 0.385, w * 0.545, h * 0.365)
    setc(ctx, hexc("#7a4a2a"))
    ctx.set_line_width(max(1.5, w * 0.008))
    ctx.stroke()
    # varnish
    g = cairo.RadialGradient(w / 2, h * 0.4, w * 0.1, w / 2, h / 2, w * 0.8)
    g.add_color_stop_rgba(0, 1, 0.9, 0.5, 0.12)
    g.add_color_stop_rgba(1, 0.2, 0.12, 0, 0.35)
    ctx.set_source(g)
    ctx.paint()
    ctx.restore()
    ctx.restore()


def bundle(ctx, x, y, s=1.0, rot=0.0, peek=0.0, t=0.0):
    """the Mona Lisa wrapped in cloth. peek 0..1 pulls the cloth back."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    w, h = 140, 200
    if peek > 0:
        mona(ctx, 0, 0, w, h, frame=False)
        rrect(ctx, -w / 2, -h / 2, w, h, 6)
        fs(ctx, None, lw=6)
    top = -h / 2 + h * peek * 0.95
    ctx.move_to(-w / 2 - 6, top)
    ctx.curve_to(-w / 4, top + 10 * math.sin(t * 3), w / 4, top - 10, w / 2 + 6, top)
    ctx.line_to(w / 2 + 6, h / 2 + 6)
    ctx.line_to(-w / 2 - 6, h / 2 + 6)
    ctx.close_path()
    fs(ctx, CLOTH, lw=6)
    if peek < 0.5:
        line(ctx, -w / 2, 10, w / 2, 10, 5, hexc("#8a6a3a"))
        line(ctx, 0, top + 4, 0, h / 2, 5, hexc("#8a6a3a"))
    for k in range(3):
        line(ctx, -w / 2 + 20 + k * 40, top + 30, -w / 2 + 30 + k * 40, h / 2 - 20, 2, hexc("#b8a27a"))
    ctx.restore()


def ticket(ctx, x, y, s=1.0, rot=0.0, glow=0.0, t=0.0, text_mode="louvre"):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    if glow > 0:
        warm_glow(ctx, 0, 0, 520, 0.75 * glow, (1, 0.85, 0.4))
        for k in range(10):
            a = k * 0.63 + t * 0.8
            line(ctx, math.cos(a) * 260, math.sin(a) * 160, math.cos(a) * (330 + 40 * glow), math.sin(a) * (200 + 30 * glow),
                 6, (1, 0.9, 0.5), 0.5 * glow)
    rrect(ctx, -260, -140, 520, 280, 12)
    fs(ctx, hexc("#f1dfa8"), lw=7)
    rrect(ctx, -240, -120, 480, 240, 8)
    fs(ctx, None, lw=3, stroke=hexc("#8a6a3a"))
    line(ctx, 130, -120, 130, 120, 3, hexc("#8a6a3a"))
    for k in range(9):
        circle(ctx, 130, -110 + k * 27, 4)
        setc(ctx, hexc("#c9b17a"))
        ctx.fill()
    if text_mode == "louvre":
        text(ctx, "MUSÉE DU LOUVRE", -55, -78, 40, hexc("#5a2a1a"), outline=0, shadow=False)
        text(ctx, "PARIS", -55, -32, 30, hexc("#5a2a1a"), font=HAND_FONT, outline=0, shadow=False)
        text(ctx, "21 AOÛT 1911", -55, 22, 48, RED, outline=0, shadow=False)
        text(ctx, "ENTRÉE · 1 PERSONNE", -55, 78, 26, hexc("#5a2a1a"), font=HAND_FONT, outline=0, shadow=False)
        text(ctx, "N° 0821", 190, 0, 26, hexc("#5a2a1a"), font=HAND_FONT, outline=0, shadow=False, rot=-math.pi / 2)
    else:
        text(ctx, "NEXT DESTINATION:", -55, -80, 32, hexc("#5a2a1a"), outline=0, shadow=False)
        text(ctx, "TITANIC", -55, -20, 64, hexc("#1f3a7a"), outline=0, shadow=False)
        text(ctx, "1912", -55, 50, 60, RED, outline=0, shadow=False)
        # little ship
        ctx.save()
        ctx.translate(190, 30)
        ctx.scale(0.5, 0.5)
        poly(ctx, [(-80, 0), (80, 0), (60, 40), (-70, 40)])
        fs(ctx, INK, lw=0)
        for k in range(4):
            ctx.rectangle(-55 + k * 32, -40, 18, 40)
            fs(ctx, hexc("#e8a23a"), lw=3)
        ctx.restore()
    ctx.restore()


def baguette(ctx, x, y, s=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -70, -12, 140, 24, 12)
    fs(ctx, BREAD, lw=4)
    for k in range(4):
        line(ctx, -45 + k * 28, -8, -32 + k * 28, 8, 3, BREAD_D)
    ctx.restore()


def bread_cart(ctx, x, y, s, t, crashed=0.0, seed=3):
    """wooden baker's cart; crashed>0 sends baguettes flying."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    tilt = -0.25 * clamp(crashed * 3)
    ctx.save()
    ctx.rotate(tilt)
    line(ctx, -230, -150, -330, -200, 10, hexc("#6b4428"))
    ctx.rectangle(-220, -230, 440, 120)
    fs(ctx, hexc("#a06a3a"), lw=7)
    for k in range(5):
        line(ctx, -220 + k * 110, -230, -220 + k * 110, -110, 4, hexc("#7a4a24"))
    text(ctx, "BOULANGERIE", 0, -170, 34, WHITE, outline=4, shadow=False)
    if crashed < 0.05:
        rnd = random.Random(seed)
        for k in range(16):
            baguette(ctx, rnd.uniform(-160, 160), -240 - rnd.uniform(0, 70), 0.9, rot=rnd.uniform(-0.5, 0.5))
    ctx.restore()
    for wx in (-140, 140):
        circle(ctx, wx, -60, 60)
        fs(ctx, hexc("#6b4428"), lw=6)
        circle(ctx, wx, -60, 12)
        fs(ctx, INK, lw=0)
    ctx.restore()
    if crashed > 0:
        rnd = random.Random(seed)
        for k in range(22):
            vx, vy = rnd.uniform(-500, 500), rnd.uniform(-900, -400)
            tt = crashed * 1.4
            bx = x + vx * tt * s
            by = y - 260 * s + (vy * tt + 900 * tt * tt) * s
            by = min(by, y + 20)
            baguette(ctx, bx, by, 0.9 * s, rot=rnd.uniform(-3, 3) + tt * rnd.uniform(-8, 8))


def gas_lamp(ctx, x, y, h=420, lit=0.0):
    line(ctx, x, y, x, y - h, 12, hexc("#2a3a32"))
    ctx.rectangle(x - 26, y - 30, 52, 30)
    fs(ctx, hexc("#2a3a32"), lw=4)
    poly(ctx, [(x - 34, y - h), (x + 34, y - h), (x + 24, y - h - 70), (x - 24, y - h - 70)])
    fs(ctx, hexc("#f6e2a0") if lit else hexc("#dfe6ee"), lw=5)
    poly(ctx, [(x - 40, y - h - 70), (x + 40, y - h - 70), (x, y - h - 100)])
    fs(ctx, hexc("#2a3a32"), lw=4)
    if lit:
        warm_glow(ctx, x, y - h - 35, 260, 0.55 * lit)


def eiffel(ctx, x, y, h, c=hexc("#8a6a4a")):
    w = h * 0.55
    ctx.move_to(x - w / 2, y)
    ctx.curve_to(x - w * 0.2, y - h * 0.3, x - w * 0.06, y - h * 0.65, x - w * 0.02, y - h)
    ctx.line_to(x + w * 0.02, y - h)
    ctx.curve_to(x + w * 0.06, y - h * 0.65, x + w * 0.2, y - h * 0.3, x + w / 2, y)
    ctx.line_to(x + w * 0.3, y)
    ctx.curve_to(x + w * 0.15, y - h * 0.18, x - w * 0.15, y - h * 0.18, x - w * 0.3, y)
    ctx.close_path()
    setc(ctx, c)
    ctx.fill()
    for k, yy in enumerate((0.3, 0.6)):
        ww = w * (0.32 - k * 0.16)
        ctx.rectangle(x - ww, y - h * yy, ww * 2, h * 0.025)
        ctx.fill()
    line(ctx, x, y - h, x, y - h * 1.07, 3, c)


def haussmann(ctx, x, base, w, floors, seed=0, night=False, lit=None):
    """Parisian apartment building with mansard roof and balconies."""
    rnd = random.Random(seed)
    fh = 110
    h = floors * fh + 60
    body = lerpc(STONE, NIGHT_B, 0.6) if night else [STONE, hexc("#f2e8d2"), hexc("#e9d9b8")][seed % 3]
    ctx.rectangle(x, base - h, w, h)
    fs(ctx, body, lw=6)
    # ground floor shop
    shop = [hexc("#2f5a3a"), hexc("#7a2a2a"), hexc("#2a3f6a"), hexc("#6a4a2a")][seed % 4]
    ctx.rectangle(x + 14, base - 110, w - 28, 110)
    fs(ctx, lerpc(shop, NIGHT_T, 0.5) if night else shop, lw=5)
    ctx.rectangle(x + 30, base - 90, w - 60, 70)
    fs(ctx, hexc("#f6d98a") if night else hexc("#cfe3ee"), lw=4)
    # awning
    if not night:
        for k in range(int((w - 28) / 40)):
            poly(ctx, [(x + 14 + k * 40, base - 130), (x + 54 + k * 40, base - 130), (x + 54 + k * 40, base - 100),
                       (x + 14 + k * 40, base - 100)])
            fs(ctx, [RED, WHITE][k % 2], lw=3)
    # windows
    cols = int(w / 90)
    for f in range(1, floors):
        y0 = base - 110 - f * fh + 20
        for c in range(cols):
            wx = x + (w - cols * 90) / 2 + c * 90 + 20
            on = night and lit is not None and lit.get((seed, f, c), False)
            rrect(ctx, wx, y0, 50, 76, 6)
            fs(ctx, (hexc("#f6d98a") if on else hexc("#3a4a6a")) if night else hexc("#4a6a8a"), lw=4)
            if f == 1 or f == floors - 1:
                ctx.rectangle(wx - 8, y0 + 64, 66, 14)
                fs(ctx, None, lw=3)
                for k in range(5):
                    line(ctx, wx - 4 + k * 14, y0 + 64, wx - 4 + k * 14, y0 + 78, 2)
    # cornice + mansard
    top = base - h
    ctx.rectangle(x - 10, top - 14, w + 20, 18)
    fs(ctx, STONE_D if not night else lerpc(STONE_D, NIGHT_B, 0.6), lw=5)
    poly(ctx, [(x - 6, top - 14), (x + 30, top - 120), (x + w - 30, top - 120), (x + w + 6, top - 14)])
    fs(ctx, ROOF if not night else ROOF_D, lw=6)
    for c in range(cols):
        dx = x + (w - cols * 90) / 2 + c * 90 + 22
        rrect(ctx, dx, top - 100, 46, 60, 18)
        fs(ctx, STONE if not night else lerpc(STONE, NIGHT_B, 0.6), lw=4)
    for k in range(2):
        ctx.rectangle(x + 40 + k * (w - 110), top - 160, 30, 50)
        fs(ctx, hexc("#b8704a"), lw=4)


def paris_street(ctx, t, x0=-1200, x1=4200, base=800, night=False, eiffel_x=2100, seed=0, lamps_lit=0.0, lit=None):
    if night:
        vgrad(ctx, x0 - 400, -900, x1 - x0 + 800, 2000, NIGHT_T, NIGHT_B)
        rnd = random.Random(9)
        for i in range(120):
            circle(ctx, rnd.uniform(x0, x1), rnd.uniform(-800, 300), 1.5 + rnd.random() * 2)
            setc(ctx, WHITE, 0.4 + 0.4 * math.sin(t * 2 + i))
            ctx.fill()
        circle(ctx, x0 + 1500, -100, 70)
        fs(ctx, hexc("#f4f0d8"), lw=4)
    else:
        vgrad(ctx, x0 - 400, -900, x1 - x0 + 800, 2000, SKY_T, SKY_B)
        for i in range(5):
            cloud(ctx, ((i * 900 + t * 18) % (x1 - x0)) + x0, -60 + (i % 2) * 90, 1.1, a=0.85)
    if eiffel_x is not None:
        eiffel(ctx, eiffel_x, base - 200, 1050, c=hexc("#4a4a6a") if night else hexc("#9a7a5a"))
    rnd = random.Random(seed)
    x = x0
    i = 0
    while x < x1:
        w = rnd.choice((300, 360, 420))
        floors = rnd.choice((4, 5, 5, 6))
        haussmann(ctx, x, base, w, floors, seed=seed + i, night=night, lit=lit)
        x += w + 4
        i += 1
    # pavement + cobbles
    ctx.rectangle(x0 - 400, base, x1 - x0 + 800, 40)
    fs(ctx, hexc("#b8ad9c") if not night else hexc("#4a4a5a"), lw=5)
    ctx.rectangle(x0 - 400, base + 40, x1 - x0 + 800, 900)
    fs(ctx, COBBLE if not night else hexc("#3a3a4a"), lw=5)
    for r in range(6):
        for k in range(int((x1 - x0) / 60) + 20):
            ellipse(ctx, x0 - 300 + k * 60 + (30 if r % 2 else 0), base + 70 + r * 42, 24, 12)
            setc(ctx, COBBLE_D if not night else hexc("#2e2e3c"))
            ctx.fill()
    for k in range(int((x1 - x0) / 700) + 1):
        gas_lamp(ctx, x0 + 200 + k * 700, base + 30, lit=lamps_lit)


# ====================================================================== characters
def kepi(color=NAVY, band=hexc("#c9a040")):
    def f(c):
        poly(c, [(-82, -40), (-70, -150), (70, -150), (82, -40)])
        fs(c, color, lw=LW)
        c.rectangle(-84, -66, 168, 24)
        fs(c, band, lw=5)
        c.move_to(20, -40)
        c.curve_to(70, -36, 120, -40, 140, -26)
        c.curve_to(110, -18, 60, -22, 20, -26)
        c.close_path()
        fs(c, INK, lw=4)
    return f


def moustache(fx=0.0, color=hexc("#2a2420"), big=False):
    def f(c):
        mx = 8 + fx * 34
        k = 1.4 if big else 1.0
        c.move_to(mx, 2)
        c.curve_to(mx - 20 * k, -6, mx - 44 * k, 4, mx - 52 * k, 28)
        c.curve_to(mx - 30 * k, 12, mx - 14, 12, mx, 12)
        c.curve_to(mx + 14, 12, mx + 30 * k, 12, mx + 52 * k, 28)
        c.curve_to(mx + 44 * k, 4, mx + 20 * k, -6, mx, 2)
        fs(c, color, lw=3)
    return f


def flat_cap(color=hexc("#4a4a52")):
    def f(c):
        c.move_to(-104, -20)
        c.curve_to(-110, -120, 80, -130, 104, -40)
        c.curve_to(130, -30, 150, -20, 130, -10)
        c.curve_to(40, -40, -60, -40, -104, -20)
        fs(c, color, lw=LW)
    return f


def top_hat(c):
    c.rectangle(-66, -240, 132, 170)
    fs(c, hexc("#1c1c22"), lw=LW)
    c.rectangle(-66, -110, 132, 20)
    fs(c, hexc("#6a2a2a"), lw=4)
    ellipse(c, 0, -72, 118, 20)
    fs(c, hexc("#1c1c22"), lw=LW)


def big_hat(color, flower=RED):
    def f(c):
        c.move_to(-100, 0)
        c.curve_to(-100, -110, 100, -110, 100, 0)
        fs(c, hexc("#5a3a22"), lw=LW)
        ellipse(c, 0, -70, 210, 40)
        fs(c, color, lw=LW)
        ellipse(c, 0, -100, 90, 50)
        fs(c, color, lw=LW)
        for k in range(3):
            circle(c, -60 + k * 40, -120, 18)
            fs(c, [flower, WHITE, hexc("#ff9ad0")][k], lw=3)
        c.move_to(80, -110)
        c.curve_to(160, -170, 200, -120, 220, -160)
        setc(c, WHITE)
        c.set_line_width(14)
        c.stroke()
    return f


def toque(c):
    c.move_to(-90, -40)
    for k in range(5):
        a0 = math.pi + k * math.pi / 5
        c.arc(math.cos(a0 + math.pi / 10) * 70, -130 + math.sin(a0 + math.pi / 10) * 30, 40, a0, a0 + math.pi)
    c.line_to(90, -40)
    c.close_path()
    fs(c, WHITE, lw=LW)
    c.rectangle(-90, -60, 180, 30)
    fs(c, WHITE, lw=LW)


def nightcap(c):
    c.move_to(-100, -20)
    c.curve_to(-90, -160, 120, -170, 170, -60)
    c.curve_to(120, -110, 40, -60, 100, -30)
    c.close_path()
    fs(c, hexc("#c8d8f0"), lw=LW)
    circle(c, 175, -55, 20)
    fs(c, WHITE, lw=4)


def combo(*fs_):
    def f(c):
        for g in fs_:
            g(c)
    return f


def coat_extra(c, part, *a):
    """the hero's borrowed white cleaner's coat (keeps his body silhouette)."""
    if part == "body":
        line(c, 0, 90, 0, 330, 4, hexc("#9aa6b2"))
        for yy in (150, 210, 270):
            circle(c, 10, yy, 6)
            fs(c, hexc("#9aa6b2"), lw=2)
        ctx_pocket = [(-52, 220), (-14, 220), (-16, 262), (-50, 262)]
        poly(c, ctx_pocket)
        fs(c, None, lw=4, stroke=hexc("#9aa6b2"))
        poly(c, [(-40, 78), (0, 120), (40, 78)])
        fs(c, None, lw=4, stroke=hexc("#9aa6b2"))


def hero(ctx, x, y, s, t, coat=False, **kw):
    if coat:
        kw.setdefault("body", COAT)
        kw.setdefault("extra", coat_extra)
    return guy(ctx, x, y, s, t, **kw)


def policeman(ctx, x, y, s, t, seed=0, whistle=False, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, seed + 3))
    kw.setdefault("body", NAVY)
    fx = kw.get("face", 0.0)

    def belt(c, part, *a):
        if part == "body":
            line(c, -62, 210, 62, 210, 12, INK)
            for yy in (130, 170):
                circle(c, 0, yy, 7)
                fs(c, hexc("#c9a040"), lw=2)
            if whistle:
                pass
    h = combo(kepi(), moustache(fx))
    hands = doodle(ctx, x, y, s, hair=h, cap=False, extra=belt, **kw)
    if whistle:
        mx = x + (8 + fx * 34) * s * (-1 if kw.get("flip") else 1)
        rrect(ctx, mx - 6 * s, y + 18 * s, 50 * s, 18 * s, 6 * s)
        fs(ctx, hexc("#c9ccd2"), lw=3)
        whistle_marks(ctx, mx + 60 * s, y + 20 * s, t, s * 1.2)
    return hands


def museum_guard(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 5))
    kw.setdefault("body", GUARD_G)
    fx = kw.get("face", 0.0)

    def trim(c, part, *a):
        if part == "body":
            line(c, -50, 90, -50, 320, 5, hexc("#c9a040"))
            line(c, 50, 90, 50, 320, 5, hexc("#c9a040"))
            text(c, "LOUVRE", 0, 160, 22, hexc("#c9a040"), outline=0, shadow=False)
    return doodle(ctx, x, y, s, hair=combo(kepi(GUARD_G), moustache(fx, big=True)), cap=False, extra=trim, **kw)


def thief(ctx, x, y, s, t, **kw):
    """the man in the white workman's smock (inspired by Vincenzo Peruggia)."""
    kw.setdefault("blink", doodle_auto_blink(t, 8))
    kw.setdefault("body", hexc("#f4f2ec"))
    fx = kw.get("face", 0.0)

    def smock(c, part, *a):
        if part == "body":
            for yy in (130, 180, 230):
                line(c, -60, yy, 60, yy + 6, 2, hexc("#c9c4b4"))
            ctx_ = c
            poly(ctx_, [(-30, 80), (0, 110), (30, 80)])
            fs(ctx_, None, lw=3, stroke=hexc("#c9c4b4"))
    return doodle(ctx, x, y, s, hair=combo(flat_cap(), moustache(fx)), cap=False, extra=smock, **kw)


def citizen(ctx, x, y, s, t, seed=0, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, seed))
    rnd = random.Random(seed)
    kind = seed % 4
    if kind == 0:
        kw.setdefault("body", hexc("#2a2a33"))
        h = top_hat
    elif kind == 1:
        kw.setdefault("body", [hexc("#d8a8c8"), hexc("#a8c8e0"), hexc("#e8d0a0")][seed % 3])
        h = big_hat([hexc("#f2e2c8"), hexc("#c8e0f2"), hexc("#f2c8d8")][seed % 3])
    elif kind == 2:
        kw.setdefault("body", hexc("#6a5a4a"))
        h = flat_cap(hexc("#7a6a4a"))
    else:
        kw.setdefault("body", hexc("#3a4a5a"))
        h = combo(top_hat, moustache(kw.get("face", 0.0), hexc("#8a8a8a")))
    return doodle(ctx, x, y, s, hair=h, cap=False, **kw)


def baker(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 11))
    kw.setdefault("body", WHITE)
    fx = kw.get("face", 0.0)
    return doodle(ctx, x, y, s, hair=combo(toque, moustache(fx, big=True)), cap=False, **kw)


def newsboy(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 12))
    kw.setdefault("body", hexc("#7a5a3a"))
    return doodle(ctx, x, y, s, hair=flat_cap(hexc("#5a4a3a")), cap=False, **kw)


def dog(ctx, x, y, s, t, run=True, happy=True, bread=False, face=1):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s * face, s)
    ph = t * 14 if run else 0
    bob = abs(math.sin(ph)) * 10 if run else 0
    ctx.translate(0, -bob)
    for k, lx in enumerate((-50, -25, 40, 65)):
        a = math.sin(ph + k * 1.6) * 0.6 if run else 0
        line(ctx, lx, 20, lx + math.sin(a) * 40, 20 + math.cos(a) * 40, 9)
    ctx.move_to(-70, 0)
    wag = math.sin(t * 20) * 0.5
    ctx.save()
    ctx.translate(-70, -10)
    ctx.rotate(-0.8 + wag)
    line(ctx, 0, 0, 0, -50, 9)
    ctx.restore()
    ellipse(ctx, 0, 0, 80, 36)
    fs(ctx, WHITE, lw=6)
    ellipse(ctx, -20, -10, 26, 18)
    setc(ctx, hexc("#b8763f"))
    ctx.fill()
    circle(ctx, 78, -36, 36)
    fs(ctx, WHITE, lw=6)
    ellipse(ctx, 60, -60, 14, 26)
    fs(ctx, hexc("#b8763f"), lw=4)
    circle(ctx, 88, -44, 5)
    fs(ctx, INK, lw=0)
    circle(ctx, 112, -30, 7)
    fs(ctx, INK, lw=0)
    if happy:
        ctx.move_to(86, -22)
        ctx.curve_to(96, -8, 108, -8, 112, -20)
        setc(ctx, INK)
        ctx.set_line_width(4)
        ctx.stroke()
        ellipse(ctx, 100, -10, 8, 12)
        fs(ctx, hexc("#ff7a8a"), lw=2)
    if bread:
        baguette(ctx, 110, -24, 0.9, rot=0.1)
    ctx.restore()


def fiacre(ctx, x, y, s, t, moving=True, face=1):
    """horse-drawn cab, facing right (face=-1 flips)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s * face, s)
    horse(ctx, 320, -120, 1.0, t * 1.4 if moving else 0, moving=moving)
    line(ctx, 130, -110, 250, -110, 7, hexc("#6b4428"))
    rrect(ctx, -170, -330, 300, 210, 30)
    fs(ctx, hexc("#2a2a33"), lw=7)
    rrect(ctx, -120, -300, 120, 100, 14)
    fs(ctx, hexc("#9fc4dc"), lw=5)
    ctx.rectangle(-190, -350, 340, 26)
    fs(ctx, hexc("#1c1c22"), lw=5)
    for wx, r in ((-110, 80), (100, 60)):
        ctx.save()
        ctx.translate(wx, -r)
        circle(ctx, 0, 0, r)
        fs(ctx, hexc("#b8302a"), lw=6)
        circle(ctx, 0, 0, r * 0.75)
        fs(ctx, None, lw=3)
        rot = t * 6 if moving else 0
        for k in range(8):
            a = rot + k * math.pi / 4
            line(ctx, 0, 0, math.cos(a) * r * 0.75, math.sin(a) * r * 0.75, 3)
        ctx.restore()
    # driver
    doodle(ctx, 110, -430, 0.3, hair=top_hat, cap=False, body=hexc("#3a2a2a"), face=0.9,
           expr="shock" if moving else "flat", larm=(0.3, 0.2), rarm=(-1.4, 0.3), show_legs=False,
           blink=doodle_auto_blink(t, 13))
    ctx.restore()


def statue(ctx, x, y, s, kind=0, t=0.0):
    """white marble statue on a plinth; (x, y) = floor."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rectangle(-90, -160, 180, 160)
    fs(ctx, hexc("#e8e2d6"), lw=6)
    ctx.rectangle(-104, -176, 208, 20)
    fs(ctx, hexc("#d8d0c0"), lw=5)
    M = hexc("#f4f0e8")
    if kind == 0:   # Roman bust
        ctx.move_to(-80, -176)
        ctx.curve_to(-80, -260, 80, -260, 80, -176)
        fs(ctx, M, lw=6)
        circle(ctx, 0, -320, 70)
        fs(ctx, M, lw=6)
        for k in range(6):
            circle(ctx, -50 + k * 20, -380, 16)
            fs(ctx, M, lw=4)
        line(ctx, -20, -320, -8, -320, 4)
        line(ctx, 14, -320, 26, -320, 4)
    elif kind == 1:  # Greek figure with toga
        ctx.move_to(-60, -176)
        ctx.line_to(-40, -460)
        ctx.line_to(40, -460)
        ctx.line_to(60, -176)
        ctx.close_path()
        fs(ctx, M, lw=6)
        for k in range(5):
            line(ctx, -40 + k * 20, -440, -50 + k * 25, -190, 3, hexc("#d8d0c0"))
        circle(ctx, 0, -510, 50)
        fs(ctx, M, lw=6)
        line(ctx, 40, -430, 110, -520, 18, INK)
        line(ctx, 40, -430, 110, -520, 10, M)
    elif kind == 2:  # suit of armour
        ctx.rectangle(-50, -420, 100, 240)
        fs(ctx, hexc("#b8bec8"), lw=6)
        for k in range(4):
            line(ctx, -50, -380 + k * 50, 50, -380 + k * 50, 3, hexc("#8a909a"))
        rrect(ctx, -44, -520, 88, 100, 30)
        fs(ctx, hexc("#c8ced8"), lw=6)
        for k in range(3):
            line(ctx, -30, -480 + k * 14, 30, -480 + k * 14, 4, INK)
        line(ctx, 60, -180, 60, -560, 8, hexc("#6b4428"))
        poly(ctx, [(50, -560), (60, -600), (70, -560)])
        fs(ctx, hexc("#c9ccd2"), lw=3)
    ctx.restore()


def winged_victory(ctx, x, y, s):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    M = hexc("#ece6da")
    # ship prow plinth
    poly(ctx, [(-160, 0), (160, 0), (200, -120), (-120, -140)])
    fs(ctx, hexc("#9a948a"), lw=6)
    # body
    ctx.move_to(-60, -140)
    ctx.curve_to(-80, -260, -40, -380, 0, -420)
    ctx.curve_to(40, -380, 70, -260, 60, -140)
    ctx.close_path()
    fs(ctx, M, lw=6)
    for k in range(5):
        line(ctx, -40 + k * 20, -380, -50 + k * 26, -150, 3, hexc("#c8c0b0"))
    # wings
    for sx in (-1, 1):
        ctx.move_to(0, -380)
        ctx.curve_to(sx * 80, -480, sx * 220, -520, sx * 260, -600)
        ctx.curve_to(sx * 200, -500, sx * 140, -440, sx * 40, -330)
        ctx.close_path()
        fs(ctx, M, lw=6)
        for k in range(4):
            line(ctx, sx * (60 + k * 45), -420 - k * 30, sx * (90 + k * 40), -470 - k * 30, 3, hexc("#c8c0b0"))
    ctx.restore()


def broom(ctx, x, y, s=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    line(ctx, 0, -200, 0, 120, 10, hexc("#8a5a2b"))
    poly(ctx, [(-50, 110), (50, 110), (60, 190), (-60, 190)])
    fs(ctx, hexc("#e8c84a"), lw=5)
    for k in range(6):
        line(ctx, -45 + k * 18, 130, -50 + k * 20, 186, 2, hexc("#b8962a"))
    ctx.restore()


# ====================================================================== interiors
def gallery_bg(ctx, t, x0=-1200, x1=4200, base=780, wax=0.0, paintings=True, seed=1):
    """the Louvre's Grand Gallery, side view: red walls, gilt frames, skylit vault, waxed parquet."""
    vgrad(ctx, x0 - 400, -900, x1 - x0 + 800, 2000, hexc("#f2e2c2"), hexc("#e2cfa8"))
    # vault + skylight
    ctx.rectangle(x0 - 400, -900, x1 - x0 + 800, 700)
    fs(ctx, hexc("#e8d8b8"), lw=0)
    for k in range(int((x1 - x0) / 300) + 3):
        cx = x0 - 300 + k * 300
        ctx.move_to(cx, 60)
        ctx.curve_to(cx + 40, -120, cx + 260, -120, cx + 300, 60)
        setc(ctx, hexc("#c9a96a"))
        ctx.set_line_width(14)
        ctx.stroke()
        ctx.rectangle(cx + 60, -200, 180, 60)
        fs(ctx, hexc("#cfe6f2"), lw=5)
    warm_glow(ctx, (x0 + x1) / 2, -100, 1600, 0.25, (1, 1, 0.9))
    # wall
    ctx.rectangle(x0 - 400, 70, x1 - x0 + 800, base - 70)
    fs(ctx, WALL_RED, lw=6)
    ctx.rectangle(x0 - 400, 60, x1 - x0 + 800, 26)
    fs(ctx, hexc("#c9a040"), lw=5)
    # columns / pilasters
    for k in range(int((x1 - x0) / 600) + 2):
        cx = x0 + k * 600
        ctx.rectangle(cx - 40, 86, 80, base - 86)
        fs(ctx, hexc("#efe3c8"), lw=5)
        ctx.rectangle(cx - 52, 86, 104, 24)
        fs(ctx, hexc("#d8c49e"), lw=4)
    if paintings:
        rnd = random.Random(seed)
        for k in range(int((x1 - x0) / 300)):
            px = x0 + 80 + k * 300
            if (k % 2) == 0:
                w, h = rnd.choice(((160, 200), (200, 150), (140, 180)))
                frame_box(ctx, px + 20, 200 + rnd.uniform(0, 60), w, h, fill=rnd.choice(
                    (hexc("#5a6a4a"), hexc("#7a5a3a"), hexc("#4a5a7a"), hexc("#8a7a4a"))), border=hexc("#c9a040"), bw=16)
    # floor
    ctx.rectangle(x0 - 400, base, x1 - x0 + 800, 900)
    fs(ctx, PARQUET, lw=6)
    for k in range(int((x1 - x0) / 80) + 20):
        line(ctx, x0 - 300 + k * 80, base, x0 - 300 + k * 80 - 160, base + 600, 3, PARQUET_D)
    if wax > 0:
        for k in range(int((x1 - x0) / 400) + 2):
            ex = x0 + k * 400 + 100
            ellipse(ctx, ex, base + 80, 150, 16)
            setc(ctx, WHITE, 0.35 * wax)
            ctx.fill()
            sparkle(ctx, ex + 60, base + 70, 22 * wax, t * 2 + k)


def salon_wall(ctx, t, missing=True, hooks_glow=0.0):
    """Salon Carré wall: paintings hung frame to frame, with the Mona Lisa's spot."""
    vgrad(ctx, -1200, -800, 4400, 2000, hexc("#7a2424"), hexc("#5a1a1a"))
    ctx.rectangle(-1200, -800, 4400, 140)
    fs(ctx, hexc("#e8d8b8"), lw=0)
    ctx.rectangle(-1200, -670, 4400, 30)
    fs(ctx, hexc("#c9a040"), lw=5)
    rnd = random.Random(7)
    frames = [(-900, -560, 300, 220), (-560, -560, 220, 300), (-280, -560, 360, 240), (140, -560, 260, 300),
              (460, -560, 300, 220), (-900, -260, 240, 300), (-600, -220, 300, 220), (-240, -230, 220, 280),
              (420, -230, 300, 230), (780, -560, 280, 300), (800, -200, 260, 260), (-880, 120, 320, 220),
              (-500, 100, 260, 260), (380, 110, 300, 220), (740, 120, 280, 240)]
    cols = [hexc("#5a6a4a"), hexc("#7a5a3a"), hexc("#4a5a7a"), hexc("#8a7a4a"), hexc("#6a4a5a")]
    for i, (x, y, w, h) in enumerate(frames):
        frame_box(ctx, x, y, w, h, fill=cols[i % 5], border=hexc("#c9a040"), bw=18)
        ctx.save()
        ctx.rectangle(x, y, w, h)
        ctx.clip()
        circle(ctx, x + w * 0.5, y + h * 0.45, min(w, h) * 0.18)
        setc(ctx, hexc("#e2c08a"), 0.7)
        ctx.fill()
        ctx.restore()
    # the spot: x 60..300?  centre at (0, 160)
    cx, cy, w, h = 0, 170, 160, 230
    if missing:
        ctx.rectangle(cx - w / 2, cy - h / 2, w, h)
        setc(ctx, hexc("#6a1e1e"))
        ctx.fill()
        ctx.rectangle(cx - w / 2, cy - h / 2, w, h)
        ctx.save()
        ctx.set_dash([12, 10])
        fs(ctx, None, lw=3, stroke=hexc("#4a1010"))
        ctx.restore()
        for hx, hy in ((-60, -100), (60, -100), (-60, 100), (60, 100)):
            if hooks_glow > 0:
                warm_glow(ctx, cx + hx, cy + hy, 40, 0.8 * hooks_glow)
            line(ctx, cx + hx, cy + hy, cx + hx, cy + hy + 18, 7, hexc("#3a3a40"))
            ctx.move_to(cx + hx, cy + hy + 18)
            ctx.curve_to(cx + hx, cy + hy + 30, cx + hx + 14, cy + hy + 30, cx + hx + 14, cy + hy + 18)
            setc(ctx, hexc("#3a3a40"))
            ctx.set_line_width(6)
            ctx.stroke()
    else:
        frame_box(ctx, cx - w / 2, cy - h / 2, w, h, fill=WHITE, border=hexc("#c9a040"), bw=16)
        mona(ctx, cx, cy, w, h, frame=False)
    ctx.rectangle(-1200, 520, 4400, 600)
    fs(ctx, PARQUET, lw=6)
    for k in range(70):
        line(ctx, -1200 + k * 80, 520, -1360 + k * 80, 1100, 3, PARQUET_D)


def staircase_bg(ctx, t):
    """the Daru staircase seen from the side, with the Winged Victory at the top."""
    vgrad(ctx, -1500, -1500, 5000, 3200, hexc("#d8ccb4"), hexc("#b8a88c"))
    for k in range(6):
        ctx.rectangle(-1400 + k * 700, -1500, 60, 3000)
        fs(ctx, hexc("#c8b89c"), lw=4)
    # steps from top-left (0,-400) down to bottom-right (1600, 700)
    n = 22
    for i in range(n):
        x = -200 + i * 80
        y = -420 + i * 52
        ctx.rectangle(x, y, 2400, 52)
        fs(ctx, hexc("#efe6d4") if i % 2 else hexc("#e4d9c2"), lw=4)
    ctx.rectangle(-1500, -420, 1300 + 10, 2000)
    fs(ctx, hexc("#e4d9c2"), lw=5)
    ctx.rectangle(-200 + n * 80, -420 + n * 52, 3000, 2000)
    fs(ctx, hexc("#d8ccb4"), lw=5)
    # red carpet runner
    ctx.move_to(-200, -420)
    for i in range(n):
        ctx.line_to(-200 + (i + 1) * 80, -420 + i * 52)
        ctx.line_to(-200 + (i + 1) * 80, -420 + (i + 1) * 52)
    ctx.line_to(-200 + n * 80, -380 + n * 52)
    ctx.line_to(-200, -380)
    ctx.close_path()
    setc(ctx, hexc("#9a2a2a"), 0.0)
    ctx.fill()
    winged_victory(ctx, -650, -420, 0.9)


def stair_pos(u):
    """position on the staircase surface for 0..1."""
    n = 22
    x = -200 + u * n * 80
    y = -420 + u * n * 52
    return x, y


# ====================================================================== SHOTS
def chase_world(ctx, t, D, cue, base=820):
    """shared hook geometry: everyone runs right; returns hero world position."""
    run_speed = 520
    hx = 300 + t * run_speed
    paris_street(ctx, t, x0=-1200, x1=hx + 3200, base=base - 20, eiffel_x=1900 + t * run_speed * 0.6, seed=2)
    return hx


def sh_hook(ctx, t, D, cue):
    t_run = cue("I'm running")
    t_behind = cue("Behind me")
    t_front = cue("And in front")
    base = 820
    run_speed = 520
    hx = 300 + t * run_speed
    cart_x = 300 + D * run_speed + 520
    if t < 1.2:      # frame one: extreme close-up whip pan
        k = ease_out(prog(t, 0, 1.2))
        cx, cy, z = hx + 60, base - 330, lerp(3.0, 1.4, k)
    elif t < t_behind:
        cx, cy, z = hx + 150, base - 300, 1.15
    elif t < t_front:
        k = ease(prog(t, t_behind, t_behind + 1.2))
        cx, cy, z = lerp(hx + 150, hx - 520, k), base - 300, lerp(1.15, 0.8, k)
    else:
        k = ease(prog(t, t_front, t_front + 1.0))
        cx, cy, z = lerp(hx - 520, (hx + cart_x) / 2, k), base - 300, lerp(0.8, 0.75, k)
    ctx.save()
    cam(ctx, cx, cy, z, shake=4, t=t)
    paris_street(ctx, t, x0=hx - 3000, x1=hx + 3000, base=base - 20, eiffel_x=hx + 900 - t * 200, seed=2)
    bread_cart(ctx, cart_x, base + 40, 1.0, t)
    baker(ctx, cart_x + 260, base - 268, 0.6, t, face=-0.8, expr="o" if t > t_front else "smile",
          larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    # pursuers
    for i in range(3):
        px = hx - 520 - i * 230
        policeman(ctx, px, base - 268, 0.62, t, seed=i, whistle=(i == 0), expr="frown", brows="angry",
                  **run_kw(t + i * 0.2, 2.6))
    dog(ctx, hx - 330, base - 30, 0.8, t, run=True)
    hands = hero(ctx, hx, base - 282, 0.66, t, expr="shock" if t < t_front else "scared",
                 brows="worried", walk=t * 3.0, face=0.9, larm=(0.9 * math.sin(t * 18.8), 0.9), rarm=(-1.1, 1.6),
                 look=(1, 0) if t > t_front else (-0.6, 0))
    bundle(ctx, hands["r"][0] + 10, hands["r"][1] - 40, 0.55, rot=0.2, t=t)
    speed_lines(ctx, hx - 80, base - 250, seed=int(t * 8))
    dust_puffs(ctx, hx - 40, base + 40, t)
    sweat(ctx, hx - 50, base - 470, 0.9, t)
    ctx.restore()
    if t > 0.25:
        pop_text(ctx, "PARIS · 1911", 960, 120, 90, t - 0.25, GOLD, hold=t_behind - 0.6)
    if t > t_run + 2.5:
        pop_text(ctx, "THE MONA LISA!", 1450, 980, 76, t - t_run - 2.5, WHITE, hold=t_behind - t_run - 2.4)
    if t > t_behind:
        pop_text(ctx, "TWEEEET!", 420, 200, 90, t - t_behind - 1.0, WHITE, rot=-0.08, hold=t_front - t_behind - 1.2)
    if t > t_front + 0.8:
        pop_text(ctx, "UH-OH.", 960, 980, 110, t - t_front - 0.8, RED)
    vignette(ctx, 0.35)


def sh_crash(ctx, t, D, cue):
    t_how = cue("So how did")
    t_funny = cue("Funny story")
    t_save = cue("I was trying")
    hs, hc = TIMELINE["hook"]
    run_speed = 520
    base = 820
    cart_x = 300 + hs["D"] * run_speed + 520
    freeze = t > 0.9
    tt = min(t, 0.9)
    ctx.save()
    cam(ctx, cart_x, base - 320, lerp(0.95, 1.1, ease(prog(t, 0, D))), shake=18 * (1 - prog(t, 0, 0.5)), t=t)
    paris_street(ctx, tt, x0=cart_x - 3000, x1=cart_x + 3000, base=base - 20, eiffel_x=cart_x + 400, seed=2)
    bread_cart(ctx, cart_x, base + 40, 1.0, tt, crashed=0.05 + tt * 0.6)
    baker(ctx, cart_x + 260, base - 268, 0.6, tt, face=-0.8, expr="shock", brows="up", larm=(2.6, 0.3),
          rarm=(-2.6, -0.3))
    # hero flying head over heels above the cart, painting high above
    hx, hy = cart_x - 40 + tt * 200, base - 520 - tt * 120
    hero(ctx, hx, hy, 0.62, tt, expr="scared", tilt=2.6 + tt * 2, larm=(2.4, 0.4), rarm=(-2.4, -0.4))
    bundle(ctx, hx + 260, hy - 220, 0.6, rot=1.0 + tt * 3, t=tt)
    for i in range(2):
        policeman(ctx, cart_x - 600 - i * 220, base - 268, 0.62, tt, seed=i, expr="shock",
                  larm=(1.8, 0.2), rarm=(-1.8, -0.2), legs=(0.4, -0.4))
    ctx.restore()
    burst(ctx, 480, 250, 200, t, "CRUNCH!", size=80, color=(1, 0.85, 0.35))
    if freeze:
        setc(ctx, (0.15, 0.1, 0.05), 0.25)
        ctx.paint()
    if t > t_how:
        pop_text(ctx, "STEALING THE MONA LISA?!", 960, 980, 76, t - t_how, WHITE, hold=t_funny - t_how)
    if t > t_save:
        pop_text(ctx, "I WAS TRYING TO SAVE IT.", 960, 980, 80, t - t_save, GOLD, rot=-0.02)
    vignette(ctx, 0.4)


def sh_rewind(ctx, t, D, cue):
    hs, hc = TIMELINE["hook"]
    th = hs["D"] * (1 - ease_in(prog(t, 0, D)))
    sh_hook(ctx, max(0.0, th), hs["D"], hc)
    setc(ctx, (0.1, 0.1, 0.3), 0.25)
    ctx.paint()
    vhs(ctx, t)
    rewind_icon(ctx, 220, 120, 1.0, 0.9)
    text(ctx, "REWIND", 330, 122, 70, WHITE, align="left", outline=0, shadow=False)


def sh_title(ctx, t, D, cue):
    vgrad(ctx, 0, 0, W, H, hexc("#2a3f6a"), hexc("#141e38"))
    ctx.save()
    ctx.translate(W / 2, 1300)
    ctx.rotate(t * 0.12)
    for k in range(24):
        ctx.move_to(0, 0)
        ctx.arc(0, 0, 2400, k * math.pi / 12, k * math.pi / 12 + math.pi / 24)
        ctx.close_path()
        setc(ctx, GOLD, 0.08)
        ctx.fill()
    ctx.restore()
    eiffel(ctx, 1650, 1080, 700, c=hexc("#0e1428"))
    frame_box(ctx, 160, 330, 260, 360, fill=WHITE, border=hexc("#c9a040"), bw=24)
    mona(ctx, 290, 510, 260, 360, frame=False)

    def row(words, y, size, t0):
        total = sum(text_width(ctx, w, size) for w, _ in words) + 36 * (len(words) - 1)
        x = W / 2 + 100 - total / 2
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
    row([("I", WHITE), ("ACCIDENTALLY", WHITE)], 320, 120, 0.15)
    row([("STOLE", RED), ("THE", WHITE)], 490, 140, 0.5)
    row([("MONA", GOLD_L), ("LISA!", GOLD_L)], 680, 170, 0.85)
    k = ease_out(prog(t, 1.2, 1.8))
    if k > 0:
        hands = hero(ctx, 1640, lerp(1500, 760, k), 0.55, t, expr="worried", face=-0.3, brows="worried",
                     larm=(0.3, 0.2), rarm=(-1.1, 1.6))
        bundle(ctx, hands["r"][0], hands["r"][1] - 30, 0.4, rot=0.1, t=t)
    text(ctx, "HISTORY WORLD", W / 2, 1000, 48, WHITE, font=HAND_FONT, outline=6, alpha=ease(prog(t, 1.5, 2.2)))


def grandpa_box(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rectangle(-170, -120, 340, 120)
    fs(ctx, hexc("#c9925a"), lw=7)
    poly(ctx, [(-170, -120), (-210, -190), (-20, -150)])
    fs(ctx, hexc("#d9a26a"), lw=6)
    poly(ctx, [(170, -120), (210, -190), (20, -150)])
    fs(ctx, hexc("#d9a26a"), lw=6)
    text(ctx, "GRANDPA'S STUFF", 0, -60, 30, INK, font=HAND_FONT, outline=0, shadow=False)
    ctx.restore()


def sh_ticket(ctx, t, D, cue):
    t_box = cue("I was looking")
    t_bottom = cue("And at the very bottom")
    t_old = cue("An old, yellow")
    t_musee = cue("Musée du Louvre")
    t_weird = cue("Weird")
    t_thumb = cue("Then my thumb")
    if t < t_old:
        ctx.save()
        cam(ctx, lerp(960, 1000, ease(prog(t, 0, t_old))), lerp(540, 620, ease(prog(t, 0, t_old))),
            lerp(1.0, 1.35, ease(prog(t, 0, t_old))))
        bedroom_bg(ctx, t)
        grandpa_box(ctx, 1150, 880, 1.0)
        dig = t > t_box
        hero(ctx, 1000, 520, 0.7, t, expr="o" if t > t_bottom else "flat", face=0.6, look=(1, 1),
             tilt=0.25 if dig else 0, larm=(0.3, 0.2), rarm=(-1.0 + 0.4 * math.sin(t * 8), 0.6) if dig else (-0.3, -0.2))
        # junk flying out of the box
        if dig:
            rnd = random.Random(4)
            items = ["sock", "yoyo", "camera", "spoon", "sock", "yoyo"]
            for i in range(6):
                t0 = t_box + 0.3 + i * 0.55
                if t > t0:
                    u = prog(t, t0, t0 + 1.0)
                    ix = 1150 + lerp(0, rnd.uniform(-500, 500), u)
                    iy = 780 - math.sin(u * math.pi) * 320 + u * 120
                    kind = items[i]
                    ctx.save()
                    ctx.translate(ix, iy)
                    ctx.rotate(u * 6)
                    if kind == "sock":
                        line(ctx, 0, -30, 0, 20, 22)
                        line(ctx, 0, -30, 0, 20, 14, WHITE)
                    elif kind == "yoyo":
                        circle(ctx, 0, 0, 26)
                        fs(ctx, RED, lw=5)
                    elif kind == "camera":
                        rrect(ctx, -40, -26, 80, 52, 6)
                        fs(ctx, hexc("#3a3a40"), lw=5)
                        circle(ctx, 0, 0, 16)
                        fs(ctx, hexc("#9aa0a8"), lw=4)
                    else:
                        line(ctx, -30, 0, 30, 0, 8, hexc("#c9ccd2"))
                    ctx.restore()
        if t > t_bottom + 1.0:
            sparkle(ctx, 1150, 780, 40, t)
        ctx.restore()
        if t > t_box:
            pop_text(ctx, "*looking for my charger*", 960, 140, 56, t - t_box, WHITE, font=HAND_FONT, outline=6,
                     hold=t_bottom - t_box)
    else:
        bg_fill(ctx, hexc("#2a2440"))
        glow = ease(prog(t, t_thumb + 0.6, D))
        warm_glow(ctx, 960, 540, 900, 0.3 + 0.4 * glow)
        z = lerp(1.0, 1.1, ease(prog(t, t_old, D)))
        ctx.save()
        cam(ctx, 960, 540, z, shake=6 * glow, t=t)
        ticket(ctx, 960, 520, 1.6, rot=-0.04, glow=glow, t=t)
        # thumb
        if t > t_thumb:
            k = ease(prog(t, t_thumb, t_thumb + 0.6))
            tx, ty = lerp(1500, 920, k), lerp(900, 560, k)
            line(ctx, 2000, 1300, tx + 30, ty + 40, 60)
            line(ctx, 2000, 1300, tx + 30, ty + 40, 46, WHITE)
            ellipse(ctx, tx, ty, 46, 36)
            fs(ctx, WHITE, lw=7)
        ctx.restore()
        if t > t_weird:
            pop_text(ctx, "1911?!", 1550, 200, 90, t - t_weird, RED, hold=t_thumb - t_weird)
        if t > t_thumb + 0.8:
            pop_text(ctx, "GLOW?!", 960, 980, 90, t - t_thumb - 0.8, GOLD)
    vignette(ctx, 0.4)


def sh_portal(ctx, t, D, cue):
    t_tunnel = cue("My lamp")
    t_back = cue("Backwards")
    if t < 2.0:
        k = ease_in(prog(t, 0, 2.0))
        ctx.save()
        cam(ctx, 960, 540, 1.0 + k * 0.6, rot=k * 1.5)
        bedroom_bg(ctx, t)
        hands = hero(ctx, 1100, 520, 0.7, t, expr="shock", face=0, larm=(2.2, 0.4), rarm=(-1.4, 0.2),
                     tilt=math.sin(t * 20) * 0.05)
        ticket(ctx, hands["r"][0] + 30, hands["r"][1] - 10, 0.25, glow=1.0, t=t)
        ctx.restore()
        r = 80 + 1400 * k
        warm_glow(ctx, 960, 540, r, 0.8, (1, 0.9, 0.6))
        circle(ctx, 960, 540, r * 0.35)
        setc(ctx, (1, 0.95, 0.75), 0.9 * clamp(t / 0.6))
        ctx.fill()
        burst(ctx, 960, 200, 160, t - 0.2, "WHOOSH!", size=64, color=(1, 0.88, 0.5), tcolor=hexc("#2a3f6a"))
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
        ctx.save()
        ctx.translate(px, py)
        ctx.rotate(t * 2 + i)
        if kind == 0:      # sock
            line(ctx, 0, -30 * sc, 0, 30 * sc, 20 * sc + 4)
            line(ctx, 0, -30 * sc, 0, 30 * sc, 14 * sc + 2, WHITE)
        elif kind == 1:    # lamp
            poly(ctx, [(-30 * sc, 0), (30 * sc, 0), (18 * sc, -40 * sc), (-18 * sc, -40 * sc)])
            fs(ctx, hexc("#ffd36a"), lw=3)
            line(ctx, 0, 0, 0, 50 * sc, 5)
        elif kind == 2:    # mini painting frame
            rrect(ctx, -30 * sc, -40 * sc, 60 * sc, 80 * sc, 4)
            fs(ctx, hexc("#c9a040"), lw=3)
        else:
            ctx.restore()
            clock_icon(ctx, px, py, 10 + ph * 60, t, back=True, rot=t + i)
            continue
        ctx.restore()
    ctx.save()
    ctx.translate(W / 2 + 260 * math.sin(t * 0.9), H / 2 + 120 * math.cos(t * 1.3) - 60)
    ctx.rotate(t * 2.5)
    guy(ctx, 0, -150, 0.6, t, expr="shock", face=0, larm=(2.4, 0.5), rarm=(-2.4, -0.5), legs=(0.5, -0.5))
    ctx.restore()
    if t > t_tunnel:
        bc_counter(ctx, t - t_tunnel, D - t_tunnel, 2026, 1911)
    if t > t_back + 0.5:
        pop_text(ctx, "115 YEARS BACK!", 960, 980, 80, t - t_back - 0.5, GOLD)
    vignette(ctx, 0.6)


def sh_paris(ctx, t, D, cue):
    t_horses = cue("Horses.")
    t_carr = cue("Carriages")
    t_gents = cue("Gentlemen")
    t_ladies = cue("Ladies")
    t_eiffel = cue("And in the distance")
    t_only = cue("Only twenty")
    base = 820
    if t < t_horses:
        cx, cy, z = 700, base - 200, 1.6
    elif t < t_eiffel:
        k = ease(prog(t, t_horses, t_eiffel))
        cx, cy, z = lerp(700, 1300, k), lerp(base - 200, base - 320, k), lerp(1.6, 1.0, k)
    else:
        k = ease(prog(t, t_eiffel, t_eiffel + 1.5))
        cx, cy, z = lerp(1300, 1900, k), lerp(base - 320, base - 600, k), lerp(1.0, 0.7, k)
    ctx.save()
    cam(ctx, cx, cy, z)
    paris_street(ctx, t, x0=-1200, x1=4000, base=base - 20, eiffel_x=2200, seed=5)
    # passing carriages and people
    if t > t_horses - 0.5:
        fiacre(ctx, lerp(-400, 3200, prog(t, t_horses - 0.5, D + 3)), base + 150, 0.7, t)
    if t > t_gents - 0.5:
        for i in range(3):
            citizen(ctx, lerp(2400, 900, prog(t, t_gents - 0.5, D + 2)) + i * 160, base - 268, 0.6, t,
                    seed=i * 4, face=-0.8, walk=t * 1.2 + i, expr="smile", larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    if t > t_ladies - 0.5:
        for i in range(2):
            citizen(ctx, lerp(-200, 1500, prog(t, t_ladies - 0.5, D + 2)) - i * 200, base - 268, 0.6, t,
                    seed=1 + i * 4, face=0.8, walk=t * 1.1 + i, expr="smile", larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    # the hero lands
    land = ease_in(prog(t, 0.1, 0.7))
    sq = -0.18 * math.exp(-max(0, t - 0.7) * 6) if t > 0.7 else 0
    stunned = 0.7 < t < t_horses + 0.5
    hero(ctx, 700, lerp(-500, base - 282, land), 0.62, t, expr="worried" if stunned else "o", squash=sq,
         face=0.0 if stunned else 0.6, look=(1, -0.5) if t > t_eiffel else (0, 0),
         tilt=0.08 * math.sin(t * 5) if stunned else 0, larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    if stunned:
        stars_ring(ctx, 700, base - 470, 110, t)
    ctx.restore()
    if 0.7 < t < 2.5:
        burst(ctx, 500, 280, 120, t - 0.7, "BONK!", size=54)
    if t > t_only:
        pop_text(ctx, "EIFFEL TOWER (1889)", 1300, 150, 70, t - t_only, GOLD)
    caption(ctx, "PARIS, FRANCE", "1911", t - t_horses, dur=4.5)
    vignette(ctx, 0.3)


def newspaper(ctx, x, y, s, t, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -360, -440, 720, 880, 6)
    fs(ctx, hexc("#f2ecdc"), lw=7)
    text(ctx, "LA GAZETTE DE PARIS", 0, -370, 56, INK, outline=0, shadow=False)
    line(ctx, -320, -320, 320, -320, 4)
    text(ctx, "LUNDI 21 AOÛT 1911", 0, -290, 40, RED, outline=0, shadow=False)
    line(ctx, -320, -260, 320, -260, 4)
    text(ctx, "GRANDE CHALEUR À PARIS", 0, -200, 44, INK, outline=0, shadow=False)
    for k in range(14):
        line(ctx, -320, -140 + k * 30, -20, -140 + k * 30, 4, (0.6, 0.6, 0.6))
        line(ctx, 20, -140 + k * 30, 320, -140 + k * 30, 4, (0.6, 0.6, 0.6))
    rrect(ctx, 20, 300, 300, 110, 4)
    fs(ctx, hexc("#d8d0c0"), lw=3)
    eiffel(ctx, 170, 400, 90, c=INK)
    ctx.restore()


def sh_newspaper(ctx, t, D, cue):
    t_monday = cue("Monday, August")
    t_math = cue("My brain")
    t_day = cue("That was the day")
    t_two = cue("And it would take")
    if t < t_monday:
        ctx.save()
        cam(ctx, 1000, 520, 1.3)
        paris_street(ctx, t, x0=-600, x1=3000, base=800, eiffel_x=1900, seed=5)
        newsboy(ctx, 1240, 507, 0.62, t, face=-0.4, expr="laugh", larm=(0.3, 0.2), rarm=(2.6 if False else -2.7, 0.2))
        for k in range(3):
            ctx.rectangle(1190 + k * 6, 640 - k * 8, 110, 70)
            fs(ctx, hexc("#f2ecdc"), lw=4)
        grab = t > 2.0
        hands = hero(ctx, 900, 507, 0.62, t, expr="o", face=0.8, larm=(0.3, 0.2), rarm=(-1.5, 0.3) if grab else (-0.3, -0.2))
        if grab:
            ctx.rectangle(hands["r"][0] - 10, hands["r"][1] - 40, 90, 70)
            fs(ctx, hexc("#f2ecdc"), lw=4)
        ctx.restore()
        pop_text(ctx, "EXTRA! EXTRA!", 1300, 160, 80, t - 0.2, WHITE, hold=2.6)
    elif t < t_day:
        tt = t - t_monday
        bg_fill(ctx, hexc("#3a3040"))
        z = lerp(1.0, 1.3, ease(prog(t, t_monday, t_math)))
        ctx.save()
        cam(ctx, 960, lerp(540, 300, ease(prog(t, t_monday, t_math))), z)
        newspaper(ctx, 960, 560, 1.05, t, rot=0.02)
        if t > t_math:
            circle(ctx, 960, 270, 220 + 6 * math.sin(t * 8))
            ctx.save()
            setc(ctx, RED)
            ctx.set_line_width(10)
            ctx.set_dash([30, 16])
            ctx.stroke()
            ctx.restore()
        ctx.restore()
        if t > t_math:
            for k, w in enumerate(("21 AUGUST", "1911", "THE LOUVRE")):
                pop_text(ctx, w, 360 + k * 600, 980, 70, t - t_math - k * 0.6, GOLD)
    else:
        tt = t - t_day
        bg_fill(ctx, hexc("#1d1a2a"))
        k = back_out(prog(tt, 0.1, 0.6), 1.6)
        ctx.save()
        ctx.translate(760, 520)
        ctx.scale(max(k, 1e-3), max(k, 1e-3))
        frame_box(ctx, -150, -210, 300, 420, fill=WHITE, border=hexc("#c9a040"), bw=26)
        mona(ctx, 0, 0, 300, 420, frame=False)
        ctx.restore()
        if tt > 1.2:
            ka = back_out(prog(tt, 1.2, 1.5), 2)
            ctx.save()
            ctx.translate(760, 520)
            ctx.rotate(-0.25)
            ctx.scale(max(ka, 1e-3), max(ka, 1e-3))
            rrect(ctx, -250, -70, 500, 140, 14)
            fs(ctx, None, lw=14, stroke=RED)
            text(ctx, "STOLEN!", 0, 0, 110, RED, outline=0, shadow=False)
            ctx.restore()
        hero(ctx, 1450, 470, 0.7, t, expr="shock", face=-0.6, look=(-1, 0), larm=(2.5, 0.3), rarm=(-2.5, -0.3),
             brows="worried")
        if t > t_two:
            pop_text(ctx, "MISSING FOR 2 YEARS", 960, 980, 80, t - t_two, WHITE)
    vignette(ctx, 0.35)


def sh_plan(ctx, t, D, cue):
    t_too = cue("I panicked too")
    t_plan = cue("Then I made a plan")
    items = [("STOP THE THIEF", cue("Stop the thief")), ("SAVE THE PAINTING", cue("Save the painting")),
             ("HOME FOR DINNER", cue("Be home"))]
    if t < t_plan:
        ctx.save()
        cam(ctx, 960, 520, 1.2)
        paris_street(ctx, t, x0=-600, x1=3000, base=800, eiffel_x=1900, seed=5)
        # running in circles
        a = t * 5
        hx, hy = 960 + math.cos(a) * 220, 500 + math.sin(a) * 20
        hero(ctx, hx, hy, 0.6, t, expr="scared", face=-math.sin(a), walk=t * 3, larm=(2.6, 0.3), rarm=(-2.6, -0.3),
             brows="worried")
        sweat(ctx, hx + 50, hy - 60, 0.8, t)
        ctx.restore()
        pop_text(ctx, "PANIC!", 960, 140, 120, t - 0.3, RED, rot=-0.05)
    else:
        paper_lesson(ctx, "THE PLAN", t - t_plan, hexc("#2a3f6a"))
        hero(ctx, 330, 470, 0.7, t, expr="grin", face=0.6, larm=(0.3, 0.2), rarm=(-1.8, 0.2))
        for i, (lab, tc) in enumerate(items):
            if t < tc:
                continue
            y = 330 + i * 190
            a = ease(prog(t, tc, tc + 0.3))
            rrect(ctx, 700, y - 50, 90, 90, 12)
            fs(ctx, WHITE, lw=6)
            ctx.move_to(718, y)
            ctx.line_to(740, y + 24)
            ctx.line_to(lerp(740, 780, a), lerp(y + 24, y - 30, a))
            setc(ctx, hexc("#2f7a3a"))
            ctx.set_line_width(14)
            ctx.stroke()
            pop_text(ctx, lab, 830 + text_width(ctx, lab, 70) / 2, y, 70, t - tc, INK, outline=0)
        if t > cue("Easy"):
            pop_text(ctx, "EASY.", 1400, 980, 110, t - cue("Easy"), RED, rot=-0.05)
    vignette(ctx, 0.3)


def louvre_facade(ctx, t, base=820, sign=True):
    """the Louvre courtyard facade (no glass pyramid in 1911!)."""
    vgrad(ctx, -1200, -900, 4400, 2000, SKY_T, SKY_B)
    for i in range(4):
        cloud(ctx, ((i * 900 + t * 18) % 3600) - 700, -80 + (i % 2) * 90, 1.0, a=0.85)
    ctx.rectangle(-1200, 40, 4400, base - 40)
    fs(ctx, STONE, lw=6)
    # roof
    poly(ctx, [(-1200, 40), (-1200, -40), (3200, -40), (3200, 40)])
    fs(ctx, ROOF, lw=6)
    # central pavilion with dome
    ctx.rectangle(700, -160, 520, base + 160)
    fs(ctx, hexc("#f2e8d2"), lw=6)
    ctx.move_to(720, -160)
    ctx.curve_to(760, -380, 1160, -380, 1200, -160)
    ctx.close_path()
    fs(ctx, ROOF, lw=6)
    poly(ctx, [(760, -160), (960, -260), (1160, -160)])
    fs(ctx, STONE_D, lw=5)
    # columns + arched windows
    for k in range(-4, 18):
        x = k * 180 + 20
        if 690 < x < 1230:
            continue
        ctx.rectangle(x, 80, 26, base - 160)
        fs(ctx, STONE_D, lw=4)
        rrect(ctx, x + 50, 160, 80, 160, 40)
        fs(ctx, hexc("#4a6a8a"), lw=4)
        rrect(ctx, x + 50, 440, 80, 160, 40)
        fs(ctx, hexc("#4a6a8a"), lw=4)
    # big door
    rrect(ctx, 860, base - 330, 200, 330, 100)
    fs(ctx, hexc("#5a3a22"), lw=7)
    line(ctx, 960, base - 300, 960, base, 5)
    text(ctx, "MUSÉE DU LOUVRE", 960, -100, 46, INK, outline=0, shadow=False)
    if sign:
        ctx.save()
        ctx.translate(1180, base - 170)
        ctx.rotate(0.05)
        rrect(ctx, -110, -60, 220, 120, 8)
        fs(ctx, WHITE, lw=5)
        text(ctx, "FERMÉ", 0, -22, 40, RED, outline=0, shadow=False)
        text(ctx, "LE LUNDI", 0, 22, 34, INK, outline=0, shadow=False)
        ctx.restore()
    ctx.rectangle(-1200, base, 4400, 800)
    fs(ctx, hexc("#d8ccb0"), lw=6)
    for k in range(60):
        line(ctx, -1200 + k * 80, base, -1300 + k * 80, base + 400, 2, hexc("#c4b89c"))


def sh_disguise(ctx, t, D, cue):
    t_closed = cue("On Mondays")
    t_staff = cue("Staff only")
    t_coat = cue("So I borrowed")
    t_whistle = cue("I whistled")
    t_swept = cue("I swept")
    t_nod = cue("I nodded")
    t_back = cue("He nodded back")
    t_in = cue("I was in")
    base = 820
    coat_on = t > t_coat + 3.0
    ctx.save()
    if t < t_coat:
        cam(ctx, 960, 400, lerp(0.75, 1.0, ease(prog(t, 0, t_coat))))
    elif t < t_whistle:
        cam(ctx, lerp(960, 300, ease(prog(t, t_coat, t_coat + 1))), 520, 1.25)
    else:
        cam(ctx, lerp(300, 900, ease(prog(t, t_whistle, t_in))), 520, 1.15)
    louvre_facade(ctx, t, base)
    # laundry line on the left
    line(ctx, -200, 260, 500, 300, 4)
    for x in (-200, 500):
        line(ctx, x, 260 if x < 0 else 300, x, base, 9, hexc("#6b4428"))
    if not coat_on:
        k = prog(t, t_coat + 1.5, t_coat + 3.0)
        cx = lerp(180, 0, k)
        cy = lerp(290, 480, k)
        if k < 1:
            ctx.save()
            ctx.translate(cx, cy)
            ctx.rotate(0.05 * math.sin(t * 3))
            poly(ctx, [(-70, 0), (70, 0), (90, 220), (-90, 220)])
            fs(ctx, COAT, lw=6)
            line(ctx, 0, 0, 0, 220, 3, hexc("#9aa6b2"))
            ctx.restore()
    for k in range(3):
        rrect(ctx, 320 + k * 60, 295, 40, 70, 6)
        fs(ctx, [RED, hexc("#6a9ad8"), hexc("#f2d86a")][k], lw=4)
    # guard at the door
    nod_g = 0.15 * math.sin(prog(t, t_back, t_back + 0.6) * math.pi * 2) if t > t_back else 0
    museum_guard(ctx, 1110, base - 272, 0.62, t, face=-0.6 if t > t_whistle else 0.0, expr="flat",
                 tilt=nod_g, larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    # hero
    if t < t_coat:
        hx = 200
        hero(ctx, hx, base - 272, 0.62, t, expr="worried" if t > t_closed else "smile", face=0.6,
             look=(1, -0.3), larm=(0.3, 0.2), rarm=(-0.3, -0.2), brows="worried" if t > t_staff else None)
    elif not coat_on:
        hero(ctx, 80, base - 272, 0.62, t, expr="sly", face=-0.6, larm=(0.3, 0.2), rarm=(-2.4 if False else -0.3, -0.2),
             **{})
    else:
        hx = lerp(80, 860, ease(prog(t, t_coat + 3.0, t_nod)))
        sweep = math.sin(t * 7) * 0.3
        nod_h = 0.15 * math.sin(prog(t, t_nod, t_nod + 0.6) * math.pi * 2) if t > t_nod else 0
        hands = hero(ctx, hx, base - 272, 0.62, t, coat=True, expr="grin" if t > t_in else "happy", face=0.8,
                     walk=t * 1.3 if t < t_nod else None, tilt=nod_h, larm=(0.6 + sweep, -0.6), rarm=(-0.6 + sweep, 0.6))
        broom(ctx, hands["r"][0] + 10, hands["r"][1] + 60, 0.8, rot=-0.4 + sweep)
        if t > t_whistle and t < t_nod:
            for k in range(3):
                ph = (t * 0.8 + k / 3) % 1
                text(ctx, "♪", hx + 70 + ph * 60, base - 520 - ph * 100, 54, INK, font="DejaVu Sans", outline=0,
                     shadow=False, alpha=1 - ph)
        if t > t_swept:
            dust_puffs(ctx, hands["r"][0] + 60, base - 10, t, n=4)
    ctx.restore()
    if t > t_closed:
        pop_text(ctx, "CLOSED ON MONDAYS", 960, 120, 80, t - t_closed, RED, hold=t_coat - t_closed)
    if t > t_coat + 3.0:
        pop_text(ctx, "*very professional*", 960, 120, 60, t - t_coat - 3.0, WHITE, font=HAND_FONT, outline=6,
                 hold=t_in - t_coat - 3.2)
    if t > t_in:
        pop_text(ctx, "I'M IN!", 960, 980, 120, t - t_in, GOLD, rot=-0.04)
    vignette(ctx, 0.3)


def sh_louvre(ctx, t, D, cue):
    t_long = cue("Long golden")
    t_fact = cue("Fun fact")
    ctx.save()
    cx = lerp(-200, 2200, ease(prog(t, 0, D)))
    cam(ctx, cx, 400, lerp(0.6, 0.75, ease(prog(t, 0, D))))
    gallery_bg(ctx, t, x0=-1500, x1=3600, base=780)
    statue(ctx, 400, 780, 0.8, 1, t)
    statue(ctx, 1600, 780, 0.8, 0, t)
    statue(ctx, 2800, 780, 0.8, 1, t)
    sweep = math.sin(t * 7) * 0.3
    hx = cx - 200
    hands = hero(ctx, hx, 507, 0.62, t, coat=True, expr="o", face=0.6, look=(0.3, -1), walk=t * 1.1,
                 larm=(0.6 + sweep, -0.6), rarm=(-0.6 + sweep, 0.6))
    broom(ctx, hands["r"][0] + 10, hands["r"][1] + 60, 0.8, rot=-0.4 + sweep)
    ctx.restore()
    pop_text(ctx, "WOW.", 960, 140, 120, t - 0.3, GOLD, hold=t_fact - 0.5)
    if t > t_fact:
        rrect(ctx, 460, 860, 1000, 160, 20)
        fs(ctx, (0.05, 0.05, 0.1, 0.8), lw=0)
        text(ctx, "ROYAL PALACE", 700, 940, 56, GOLD, outline=0, shadow=False,
             alpha=ease(prog(t, t_fact + 0.6, t_fact + 1.0)))
        text(ctx, "→", 960, 940, 70, WHITE, font="DejaVu Sans", outline=0, shadow=False,
             alpha=ease(prog(t, t_fact + 1.0, t_fact + 1.4)))
        text(ctx, "MUSEUM (1793)", 1230, 940, 56, WHITE, outline=0, shadow=False,
             alpha=ease(prog(t, t_fact + 1.4, t_fact + 1.8)))
    vignette(ctx, 0.35)


def sh_empty(ctx, t, D, cue):
    t_froze = cue("And I froze")
    t_hooks = cue("On the wall")
    t_late = cue("I was too late")
    ctx.save()
    if t < t_froze:
        cam(ctx, lerp(-700, 0, ease(prog(t, 0, t_froze))), lerp(-200, 100, ease(prog(t, 0, t_froze))),
            lerp(0.55, 0.8, ease(prog(t, 0, t_froze))))
    elif t < t_late:
        cam(ctx, 0, lerp(100, 170, ease(prog(t, t_hooks, t_hooks + 1.0))),
            lerp(0.8, 2.2, ease(prog(t, t_hooks, t_hooks + 2.0))))
    else:
        cam(ctx, 0, lerp(170, 260, ease(prog(t, t_late, t_late + 0.5))), lerp(2.2, 0.85, ease_out(prog(t, t_late, t_late + 0.5))),
            shake=8 * (1 - prog(t, t_late, t_late + 1.0)), t=t)
    salon_wall(ctx, t, missing=True, hooks_glow=ease(prog(t, t_hooks + 1.0, t_hooks + 1.5)))
    froze = t > t_froze
    hx = lerp(-700, -330, ease(prog(t, 0, t_froze))) if t < t_froze else -330
    sweep = math.sin(t * 7) * 0.3 if not froze else 0
    dropped = t > t_froze + 0.4
    hands = hero(ctx, hx, 247, 0.62, t, coat=True, expr="smile" if not froze else ("shock" if t < t_late else "scared"),
                 face=0.8 if not froze else 0.3, look=(1, -0.5) if froze else (1, 0), walk=t * 1.1 if not froze else None,
                 larm=(0.6 + sweep, -0.6) if not dropped else (2.4, 0.3), rarm=(-0.6 + sweep, 0.6) if not dropped else (-2.4, -0.3),
                 brows="worried" if t > t_late else None)
    if not dropped:
        broom(ctx, hands["r"][0] + 10, hands["r"][1] + 60, 0.8, rot=-0.4 + sweep)
    else:
        fall = ease_in(prog(t, t_froze + 0.4, t_froze + 0.9))
        broom(ctx, hx + 90, 400 + 120 * fall, 0.8, rot=-0.4 + fall * 1.2)
    ctx.restore()
    caption(ctx, "THE LOUVRE · SALON CARRÉ", "21 AUGUST 1911", t - 0.6, dur=4)
    if t > t_hooks + 1.5 and t < t_late:
        pop_text(ctx, "4 IRON HOOKS", 960, 980, 80, t - t_hooks - 1.5, WHITE)
    if t > t_late:
        pop_text(ctx, "TOO LATE!", 960, 140, 140, t - t_late, RED, rot=-0.04)
    vignette(ctx, 0.4)


def sh_suspect(ctx, t, D, cue):
    t_him = cue("I saw him")
    t_man = cue("A man in")
    t_hmm = cue("Hmm")
    t_sus = cue("Suspicious")
    ctx.save()
    cam(ctx, lerp(600, 1500, ease(prog(t, 0, t_man + 2))), 420, lerp(0.85, 1.05, ease(prog(t, t_hmm, D))))
    gallery_bg(ctx, t, x0=-800, x1=3600, base=780, seed=3)
    statue(ctx, 1200, 780, 0.8, 0, t)
    hero(ctx, 600, 507, 0.62, t, coat=True, expr="o" if t < t_hmm else "sly", face=0.9, look=(1, 0),
         larm=(0.3, 0.2), rarm=(-1.1, 1.8) if t > t_hmm else (-0.3, -0.2))
    tx = lerp(2200, 2600, prog(t, t_him, D))
    hands = thief(ctx, tx, 507, 0.62, t, face=0.8, walk=t * 1.6, expr="flat", look=(1, 0),
                  larm=(0.3, 0.2), rarm=(-1.1, 1.6))
    bundle(ctx, hands["r"][0] + 10, hands["r"][1] - 40, 0.55, rot=0.15, t=t)
    if t > t_man + 2.5:
        circle(ctx, tx + 40, 470, 140 + 6 * math.sin(t * 8))
        ctx.save()
        setc(ctx, GOLD)
        ctx.set_line_width(8)
        ctx.set_dash([24, 14])
        ctx.stroke()
        ctx.restore()
    ctx.restore()
    if t > t_man:
        pop_text(ctx, "WHITE SMOCK", 1500, 140, 66, t - t_man - 0.6, WHITE, hold=1.8)
        pop_text(ctx, "WRAPPED... SOMETHING", 1500, 140, 66, t - t_man - 2.8, WHITE, hold=t_hmm - t_man - 2.9)
    if t > t_sus:
        pop_text(ctx, "SUSPICIOUS.", 960, 980, 110, t - t_sus, RED)
    vignette(ctx, 0.35)


def sh_chase(ctx, t, D, cue):
    t_roman = cue("I hid behind a Roman")
    t_greek = cue("Then behind a Greek")
    t_guard = cue("Then behind a guard")
    t_turn = cue("The man turned")
    t_art = cue("I froze")
    t_works = cue("It worked")
    t_runs = cue("Then he started running")
    t_so = cue("So did I")
    t_wax = cue("And that's when")
    xs = {"roman": 900, "greek": 1500, "guard": 2100}
    # hero position by phase
    if t < t_roman:
        hx, hide = lerp(300, 820, ease(prog(t, 0, t_roman))), None
    elif t < t_greek:
        hx, hide = lerp(820, xs["roman"] - 60, ease(prog(t, t_roman, t_roman + 0.5))), "roman"
    elif t < t_guard:
        hx, hide = lerp(xs["roman"] - 60, xs["greek"] - 70, ease(prog(t, t_greek, t_greek + 0.8))), "greek"
    elif t < t_turn:
        hx, hide = lerp(xs["greek"] - 70, xs["guard"] - 70, ease(prog(t, t_guard, t_guard + 0.8))), "guard"
    elif t < t_runs:
        hx, hide = xs["guard"] + 160, "art"
    else:
        hx, hide = xs["guard"] + 160 + (t - t_runs) * 520, None
    tx = 2700 + (t * 40 if t < t_runs else t_runs * 40 + (t - t_runs) * 560)
    ctx.save()
    cam(ctx, lerp(900, max(hx + 300, 900), ease(prog(t, 0, 1.0))), 420, 0.8)
    gallery_bg(ctx, t, x0=-800, x1=tx + 2200, base=780, wax=ease(prog(t, t_wax, t_wax + 0.5)), seed=5)
    statue(ctx, xs["roman"], 780, 0.8, 0, t)
    statue(ctx, xs["greek"], 780, 0.8, 1, t)
    museum_guard(ctx, xs["guard"], 507, 0.62, t, face=0.6 if t < t_guard + 1.0 else -0.6,
                 expr="flat" if t < t_guard + 1.0 else "o", larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    # hero
    sneaky = t < t_runs
    if hide == "art":
        ctx.rectangle(hx - 90, 620, 180, 160)
        fs(ctx, hexc("#e8e2d6"), lw=6)
        hero(ctx, hx, 337, 0.62, t, coat=True, expr="flat", face=0.0, blink=1.0 if t < t_works else 0.0,
             larm=(2.0, 0.6), rarm=(-1.2, 1.5), legs=(0.0, -0.3))
        rrect(ctx, hx - 80, 690, 160, 50, 4)
        fs(ctx, hexc("#c9a040"), lw=3)
        text(ctx, "\"BOY WITH CAP\"", hx, 715, 20, INK, outline=0, shadow=False)
    elif sneaky:
        ty = 507
        hero(ctx, hx, ty + 30, 0.62, t, coat=True, expr="sly", face=0.9, look=(1, 0), squash=-0.12,
             walk=t * 1.0 if hide is None else None, larm=(1.4, -1.6), rarm=(-1.4, 1.6))
        if hide == "roman":
            statue(ctx, xs["roman"], 780, 0.8, 0, t)
        elif hide == "greek":
            statue(ctx, xs["greek"], 780, 0.8, 1, t)
        elif hide == "guard":
            museum_guard(ctx, xs["guard"], 507, 0.62, t, face=0.6 if t < t_guard + 1.0 else -0.6,
                         expr="flat" if t < t_guard + 1.0 else "o", larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    else:
        slip = t > t_wax
        kw = run_kw(t, 3.0) if not slip else {"face": 0.9, "larm": (2.6, 0.4), "rarm": (-2.6, -0.4),
                                                "legs": (math.sin(t * 14) * 0.9, -math.sin(t * 14) * 0.9)}
        hero(ctx, hx, 507, 0.62, t, coat=True, expr="shock" if slip else "grin",
             tilt=0.5 * math.sin(t * 9) if slip else 0, **kw)
        speed_lines(ctx, hx - 80, 520, seed=int(t * 8))
    # the thief
    turn = t_turn < t < t_works + 0.3
    hands = thief(ctx, tx, 507, 0.62, t, face=-0.8 if turn else 0.8, walk=None if turn else t * (1.6 if t < t_runs else 3.0),
                  expr="sly" if turn else ("shock" if t > t_runs else "flat"), brows="angry" if turn else None,
                  larm=(0.3, 0.2), rarm=(-1.1, 1.6))
    bundle(ctx, hands["r"][0] + (-150 if turn else 10), hands["r"][1] - 40, 0.55, rot=0.15, t=t)
    ctx.restore()
    if t_turn < t < t_art + 0.5:
        pop_text(ctx, "?!", 1500, 200, 110, t - t_turn, WHITE)
    if t > t_works:
        pop_text(ctx, "IT WORKED!", 600, 140, 90, t - t_works, GOLD, hold=t_runs - t_works)
    if t > t_wax + 0.5:
        pop_text(ctx, "FRESHLY WAXED!", 960, 980, 90, t - t_wax - 0.5, WHITE, rot=-0.03)
    vignette(ctx, 0.35)


def sh_stairs(ctx, t, D, cue):
    t_armor = cue("I slid across", frac=0.55)
    t_down = cue("I slid across", frac=0.8)
    t_bumps = [cue("Bump.") + i * 0.0 for i in range(1)]
    t_victory = cue("Right past")
    t_land = cue("And I landed")
    bump_times = [cue("Bump.")]
    sents = TIMELINE["stairs"][0]["sents"]
    bump_times = [a for a, b, s in sents if s.startswith("Bump")]
    if t < t_down:
        # hockey-puck slide along the gallery, bonk off the armour
        u = prog(t, 0, t_armor)
        hx = lerp(0, 1700, u) if t < t_armor else lerp(1700, 1500, ease_out(prog(t, t_armor, t_armor + 0.4)))
        ctx.save()
        cam(ctx, hx + 200, 420, 0.85)
        gallery_bg(ctx, t, x0=-1500, x1=3600, base=780, wax=1.0, seed=8)
        statue(ctx, 1900, 780, 0.8, 2, t)
        spin = t * 10 if t < t_armor else t_armor * 10 + (t - t_armor) * 18
        ctx.save()
        ctx.translate(hx, 700)
        ctx.rotate(spin)
        ctx.translate(-hx, -700)
        hero(ctx, hx, 560, 0.45, t, coat=True, expr="shock", larm=(2.6, 0.4), rarm=(-2.6, -0.4), legs=(-1.4, 1.4))
        ctx.restore()
        if t < t_armor:
            speed_lines(ctx, hx - 120, 700, seed=int(t * 10), c=WHITE)
        ctx.restore()
        pop_text(ctx, "WHEEEE!", 600, 160, 100, t - 0.5, WHITE, hold=t_armor - 0.8)
        if t > t_armor:
            burst(ctx, 1300, 300, 150, t - t_armor, "CLANG!", size=64, color=(0.8, 0.85, 0.95), tcolor=INK)
    else:
        # tumble down the Daru staircase, past the Winged Victory
        u = ease_in_out = ease(prog(t, t_down, t_land))
        if bump_times:
            nb = sum(1 for b in bump_times if t > b)
        sx, sy = stair_pos(clamp(u))
        bounce = abs(math.sin(prog(t, t_down, t_land) * math.pi * 8)) * 60
        ctx.save()
        cam(ctx, lerp(-200, 1500, clamp(u)), lerp(-560, 500, clamp(u)), 0.62)
        staircase_bg(ctx, t)
        landed = t > t_land
        if not landed:
            ctx.save()
            ctx.translate(sx, sy - 90 - bounce)
            ctx.rotate(t * 7)
            hero(ctx, 0, -60, 0.45, t, coat=True, expr="shock", larm=(2.4, 0.5), rarm=(-2.4, -0.5), legs=(0.6, -0.6))
            ctx.restore()
        else:
            ex, ey = stair_pos(1.0)
            hero(ctx, ex + 100, ey - 330, 0.6, t, coat=True, expr="worried", face=0.8, look=(1, 0), squash=-0.15 * math.exp(-(t - t_land) * 5),
                 larm=(0.3, 0.2), rarm=(-0.3, -0.2))
            stars_ring(ctx, ex + 100, ey - 410, 100, t)
            th = thief(ctx, ex + 480, ey - 330, 0.6, t, face=-0.8, expr="shock", larm=(0.3, 0.2), rarm=(-1.1, 1.6))
            bundle(ctx, th["r"][0] - 100, th["r"][1] - 40, 0.55, rot=-0.15, t=t)
        ctx.restore()
        for i, b in enumerate(bump_times):
            if b < t < b + 0.8:
                pop_text(ctx, "BUMP!", 400 + i * 380, 220 + (i % 2) * 120, 90, t - b, WHITE, rot=-0.1 + i * 0.07)
        if t_victory < t < t_land:
            pop_text(ctx, "WINGED VICTORY OF SAMOTHRACE", 960, 980, 60, t - t_victory, GOLD)
            text(ctx, "(not helping)", 960, 1045, 40, WHITE, font=HAND_FONT, outline=5,
                 alpha=ease(prog(t, t_victory + 1.6, t_victory + 2.0)))
    vignette(ctx, 0.4)


def sh_catch(ctx, t, D, cue):
    t_crash = 0.0
    t_flew = cue("The painting flew")
    t_slow = cue("Time slowed")
    t_dove = cue("I dove")
    t_stretch = cue("I stretched")
    t_caught = cue("And I caught it")
    t_peek = cue("I peeked")
    t_her = cue("It was really her")
    t_fact = cue("Fun fact")
    t_tiny = cue("And she's tiny")
    base = 800
    if t < t_peek:
        slow = t > t_slow
        ctx.save()
        z = 1.0 if not slow else lerp(1.0, 1.3, ease(prog(t, t_slow, t_caught)))
        cam(ctx, 960, 500, z, shake=10 * (1 - prog(t, 0, 0.6)), t=t)
        gallery_bg(ctx, t, x0=-800, x1=3200, base=base, seed=9)
        # painting arc
        if t < t_caught:
            u = prog(t, t_flew, t_caught)
            px = lerp(1250, 880, u)
            py = 640 - math.sin(u * math.pi) * 380
            bundle(ctx, px, py, 0.6, rot=u * 6, t=t)
        tfall = prog(t, 0, 0.6)
        thief(ctx, 1300, 527 + 60 * tfall, 0.62, t, face=-0.5, expr="shock", tilt=0.6 * tfall, larm=(2.4, 0.4),
              rarm=(-2.4, -0.4))
        dive = ease(prog(t, t_dove, t_stretch + 0.5))
        hx = lerp(600, 720, dive)
        hy = lerp(527, 640, dive)
        hands = hero(ctx, hx, hy, 0.62, t, coat=True, expr="shock" if t < t_caught else "grin", face=0.6,
                     look=(1, -1), tilt=lerp(0, 1.25, dive), larm=(2.6, 0.2) if t > t_dove else (0.3, 0.2),
                     rarm=(-2.6, -0.2) if t > t_dove else (-0.3, -0.2))
        if t > t_caught:
            bundle(ctx, hands["r"][0] + 20, hands["r"][1] - 30, 0.6, rot=0.4, t=t)
        ctx.restore()
        burst(ctx, 1250, 280, 150, t, "POW!", size=70)
        if slow and t < t_caught:
            setc(ctx, (0.1, 0.15, 0.35), 0.18)
            ctx.paint()
            text(ctx, "SLOW MOTION", 1700, 72, 34, WHITE, align="right", outline=0, shadow=False, alpha=0.8)
        if t > t_caught:
            pop_text(ctx, "GOT IT!", 960, 140, 130, t - t_caught, GOLD, rot=-0.05)
    elif t < t_fact:
        bg_fill(ctx, hexc("#2a2440"))
        warm_glow(ctx, 960, 540, 800, 0.4)
        peek = ease(prog(t, t_peek, t_peek + 1.5))
        bundle(ctx, 960, 560, 2.3, peek=peek, t=t)
        if t > t_her:
            for k in range(6):
                sparkle(ctx, 960 + math.cos(k + t) * 380, 560 + math.sin(k * 1.7 + t) * 300, 30, t + k)
            pop_text(ctx, "IT'S REALLY HER!", 960, 110, 100, t - t_her, GOLD)
    else:
        paper_lesson(ctx, "FUN FACTS", t - t_fact, hexc("#2a3f6a"))
        # poplar panel cross-section
        ctx.save()
        ctx.translate(480, 560)
        ka = ease_out(prog(t, t_fact + 0.3, t_fact + 0.9))
        ctx.scale(max(ka, 1e-3), max(ka, 1e-3))
        rrect(ctx, -170, -230, 340, 460, 6)
        fs(ctx, hexc("#c9a46a"), lw=7)
        for k in range(9):
            ctx.move_to(-160, -200 + k * 50)
            ctx.curve_to(-60, -180 + k * 50, 60, -220 + k * 50, 160, -200 + k * 50)
            setc(ctx, hexc("#a8824a"))
            ctx.set_line_width(4)
            ctx.stroke()
        mona(ctx, 0, 0, 260, 380, frame=False)
        ctx.restore()
        text(ctx, "POPLAR WOOD", 480, 880, 56, INK, outline=0, shadow=False, alpha=ka)
        text(ctx, "not canvas!", 480, 940, 44, RED, font=HAND_FONT, outline=0, shadow=False, alpha=ka)
        if t > t_tiny:
            kb = ease_out(prog(t, t_tiny, t_tiny + 0.6))
            # size comparison with the hero: 77 x 53 cm
            sc = 0.75
            hero(ctx, 1380, 380, sc, t, expr="o", face=0.6, look=(1, 0), larm=(0.3, 0.2), rarm=(-0.3, -0.2))
            ph = 77 / 165 * 556 * sc      # hero ~1.65 m tall
            pw = 53 / 165 * 556 * sc
            ctx.save()
            ctx.translate(1600, 380 + 456 * sc - ph / 2 - 120 * kb)
            ctx.scale(max(kb, 1e-3), max(kb, 1e-3))
            frame_box(ctx, -pw / 2, -ph / 2, pw, ph, fill=WHITE, border=hexc("#c9a040"), bw=8)
            mona(ctx, 0, 0, pw, ph, frame=False)
            ctx.restore()
            pop_text(ctx, "77 × 53 cm", 1500, 940, 70, t - t_tiny - 0.4, RED, outline=0)
    vignette(ctx, 0.35)


def sh_guard(ctx, t, D, cue):
    t_me = cue("He looked at me")
    t_painting = cue("He looked at the painting")
    t_wall = cue("He looked at the empty")
    t_vanish = cue("The real thief")
    t_whistle = cue("And the guard blew")
    t_thief = cue("Thief!")
    look = 0
    ctx.save()
    if t < t_me:
        cam(ctx, 960, 480, 1.0)
    else:
        cam(ctx, 1100, 430, lerp(1.0, 1.25, ease(prog(t, t_me, t_vanish))), shake=6 if t > t_whistle else 0, t=t)
    staircase_bg(ctx, t) if False else gallery_bg(ctx, t, x0=-800, x1=3200, base=800, seed=9)
    hands = hero(ctx, 760, 527, 0.62, t, coat=True, expr="grin" if t < t_me else ("worried" if t < t_whistle else "shock"),
                 face=0.6 if t < t_me else 0.8, look=(0, -1) if t < t_me else (1, 0),
                 larm=(2.6, 0.2) if t < t_me else (0.3, 0.2), rarm=(-1.1, 1.6), brows="worried" if t > t_me else None)
    bundle(ctx, hands["r"][0] + 10, hands["r"][1] - 40, 0.55, rot=0.15, t=t)
    # thief sneaking away behind
    if t < t_vanish + 1.0:
        k = prog(t, 0, t_vanish + 1.0)
        thief(ctx, lerp(300, -300, k), 527, 0.62, t, face=-0.8, walk=t * 2.4, expr="sly", larm=(0.3, 0.2),
              rarm=(-0.3, -0.2))
    else:
        dust_puffs(ctx, -200, 760, t, n=4)
    gk = ease_out(prog(t, 0.6, 2.0))
    gx = lerp(1900, 1350, gk)
    if t < t_me:
        gface = -0.8
    elif t < t_painting:
        gface = -0.8
    elif t < t_wall:
        gface = -0.5
    else:
        gface = 0.9 if t < t_vanish else -0.8
    museum_guard(ctx, gx, 514, 0.65, t, face=gface, expr="o" if t < t_whistle else "frown",
                 brows="angry" if t > t_whistle else "up", look=(-1, 0.6) if t_painting < t < t_wall else (gface, 0),
                 larm=(0.3, 0.2), rarm=(-2.4, 0.3) if t > t_thief else (-0.3, -0.2))
    if t > t_whistle:
        mx = gx + (8 + gface * 34) * 0.65
        rrect(ctx, mx - 36, 514 + 12, 34, 12, 4)
        fs(ctx, hexc("#c9ccd2"), lw=3)
        ctx.save()
        ctx.translate(mx - 60, 532)
        ctx.scale(-1, 1)
        whistle_marks(ctx, 0, 0, t, 1.2)
        ctx.restore()
    ctx.restore()
    # inset: the empty wall
    if t_wall < t < t_vanish:
        ka = back_out(prog(t, t_wall, t_wall + 0.3), 1.6)
        ctx.save()
        ctx.translate(1550, 260)
        ctx.scale(max(ka, 1e-3), max(ka, 1e-3))
        rrect(ctx, -200, -150, 400, 300, 10)
        fs(ctx, WALL_RED, lw=8, stroke=WHITE)
        ctx.rectangle(-60, -90, 120, 180)
        ctx.save()
        ctx.set_dash([10, 8])
        fs(ctx, None, lw=4, stroke=hexc("#3a1010"))
        ctx.restore()
        ctx.restore()
    if t > t_vanish + 0.5:
        pop_text(ctx, "*poof*", 200, 760, 70, t - t_vanish - 0.5, WHITE, font=HAND_FONT, outline=6, hold=1.8)
    if t > t_whistle:
        pop_text(ctx, "TWEEEEET!", 960, 140, 100, t - t_whistle, WHITE, rot=0.06, hold=t_thief - t_whistle)
    if t > t_thief:
        burst(ctx, 1500, 260, 180, t - t_thief, "STOP, THIEF!", size=56, color=(1, 0.45, 0.4), tcolor=WHITE)
    vignette(ctx, 0.4)


def street_chase_frame(ctx, t, hx, base, seed, pursuers=True, dogx=None, hero_kw=None, bread=False, cart=None,
                       crashed=0.0, extras=None):
    paris_street(ctx, t, x0=hx - 2500, x1=hx + 3500, base=base - 20, eiffel_x=hx + 1100 - t * 150, seed=seed)
    if extras:
        extras(ctx)
    if cart is not None:
        bread_cart(ctx, cart, base + 40, 1.0, t, crashed=crashed)
    if pursuers:
        for i in range(3):
            px = hx - 620 - i * 220
            policeman(ctx, px, base - 268, 0.62, t, seed=i, whistle=(i == 0), expr="frown", brows="angry",
                      **run_kw(t + i * 0.2, 2.6))
    if dogx is not None:
        dog(ctx, dogx, base - 30, 0.8, t, run=True, bread=bread)


def sh_escape(ctx, t, D, cue):
    t_out = cue("So I ran")
    t_police = cue("Policemen blowing")
    t_driver = cue("A carriage driver")
    t_dog = cue("And a little dog")
    base = 820
    if t < t_police - 0.5:
        # out of the courtyard
        k = prog(t, 0, t_police - 0.5)
        hx = lerp(500, 2600, k)
        ctx.save()
        cam(ctx, hx, 500, 0.8)
        louvre_facade(ctx, t, base, sign=False)
        hands = hero(ctx, hx, base - 272, 0.62, t, coat=True, expr="shock", brows="worried",
                     walk=t * 3, face=0.9, larm=(0.9 * math.sin(t * 18.8), 0.9), rarm=(-1.1, 1.6))
        bundle(ctx, hands["r"][0] + 10, hands["r"][1] - 40, 0.55, rot=0.2, t=t)
        speed_lines(ctx, hx - 80, base - 250, seed=int(t * 8))
        museum_guard(ctx, hx - 700, base - 272, 0.62, t, expr="frown", brows="angry",
                     **run_kw(t, 2.6))
        ctx.restore()
        pop_text(ctx, "RUN!", 960, 140, 130, t - 0.3, RED)
    else:
        tt = t - t_police + 0.5
        hx = 500 + tt * 520
        ctx.save()
        cam(ctx, hx - 250, 520, 0.72, shake=3, t=t)

        def extras(c):
            if t > t_driver - 0.5:
                fiacre(c, hx + 700 - (t - t_driver) * 100, base + 160, 0.7, t, moving=False, face=-1)
        street_chase_frame(ctx, t, hx, base, seed=11, dogx=hx - 380 if t > t_dog - 0.3 else None, extras=extras)
        hands = hero(ctx, hx, base - 282, 0.62, t, coat=True, expr="scared", brows="worried", walk=t * 3.0, face=0.9,
                     larm=(0.9 * math.sin(t * 18.8), 0.9), rarm=(-1.1, 1.6))
        bundle(ctx, hands["r"][0] + 10, hands["r"][1] - 40, 0.55, rot=0.2, t=t)
        speed_lines(ctx, hx - 80, base - 250, seed=int(t * 8))
        if t > t_dog:
            for k in range(3):
                ph = (t * 0.8 + k / 3) % 1
                text(ctx, "♥", hx - 330 + k * 30, base - 140 - ph * 100, 40, RED, font="DejaVu Sans", outline=0,
                     shadow=False, alpha=1 - ph)
        ctx.restore()
        if t > t_police:
            pop_text(ctx, "TWEET! TWEET!", 500, 180, 80, t - t_police, WHITE, rot=-0.06, hold=t_driver - t_police)
        if t > t_driver:
            speech(ctx, 1450, 230, 420, 120, "Sacrebleu!", 64, tail=(80, 80),
                   alpha=ease(prog(t, t_driver, t_driver + 0.2)) * (1 - prog(t, t_dog, t_dog + 0.3)))
        if t > t_dog + 0.5:
            pop_text(ctx, "BEST. DAY. EVER.", 960, 980, 80, t - t_dog - 0.5, WHITE, font=HAND_FONT, outline=7)
    vignette(ctx, 0.35)


def flower_stand(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rectangle(-120, -100, 240, 100)
    fs(ctx, hexc("#3a6a3a"), lw=6)
    for k in range(10):
        circle(ctx, -100 + k * 22, -110 - (k % 3) * 14, 16)
        fs(ctx, [RED, hexc("#ffd36a"), hexc("#ff9ad0"), WHITE][k % 4], lw=3)
    ctx.restore()


def bicycle(ctx, x, y, s, t):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for wx in (-90, 90):
        circle(ctx, wx, -60, 60)
        fs(ctx, None, lw=6)
    line(ctx, -90, -60, 0, -60, 5)
    line(ctx, 0, -60, 90, -60, 5)
    line(ctx, 0, -60, -30, -150, 5)
    line(ctx, 90, -60, 70, -170, 5)
    citizen(ctx, -10, -330, 0.4, t, seed=8, face=-0.8, expr="shock", larm=(0.3, 0.2), rarm=(-1.2, 0.2), show_legs=False)
    ctx.restore()


def sh_streetchase(ctx, t, D, cue):
    t_jump = cue("I jumped over")
    t_corner = cue("Then I turned")
    t_cart = cue("The baguette cart")
    t_yes = cue("Yes.")
    t_crunch = cue("Crunch!")
    t_bread = cue("Bread everywhere")
    t_dog = cue("The dog was")
    t_baker = cue("The baker")
    base = 820
    speed = 520
    stop = t_crunch
    hx = 300 + min(t, stop) * speed
    jump_t, duck_t, dodge_t = t_jump + 0.3, t_jump + 1.9, t_jump + 3.4
    obstacles = [(300 + jump_t * speed, "flower"), (300 + duck_t * speed, "horse"), (300 + dodge_t * speed, "bike")]
    cart_x = 300 + stop * speed + 260
    crashed = prog(t, t_crunch, t_crunch + 1.2)
    ctx.save()
    cam(ctx, hx + (120 if t < t_cart else lerp(120, 200, ease(prog(t, t_cart, t_crunch)))), 520,
        0.72 if t < t_corner else lerp(0.72, 0.65, ease(prog(t, t_corner, t_cart))), shake=3 + 14 * (prog(t, t_crunch, t_crunch + 0.1) - prog(t, t_crunch + 0.5, t_crunch + 1)), t=t)

    def extras(c):
        for ox, kind in obstacles:
            if kind == "flower":
                flower_stand(c, ox, base + 40, 1.0)
            elif kind == "horse":
                fiacre(c, ox - 250, base + 160, 0.75, t, moving=False)
            else:
                bicycle(c, ox + 120 - (t - t_jump) * 160, base + 60, 0.9, t)
    street_chase_frame(ctx, t, hx, base, seed=14, pursuers=t < t_bread, dogx=hx - 380 if t < t_crunch else cart_x + 380,
                       bread=t > t_dog, cart=cart_x, crashed=crashed, extras=extras)
    if t < t_crunch:
        jumpy = 0
        for (ox, kind), tj in zip(obstacles, (jump_t, duck_t, dodge_t)):
            if kind == "flower":
                jumpy = max(jumpy, math.sin(clamp((t - tj + 0.5) / 1.0) * math.pi) * 260 if tj - 0.5 < t < tj + 0.5 else 0)
        duck = duck_t - 0.5 < t < duck_t + 0.5
        hands = hero(ctx, hx, base - 282 - jumpy + (80 if duck else 0), 0.62, t, coat=True,
                     expr="scared" if t < t_cart else "shock", brows="worried", walk=t * 3.0, face=0.9,
                     squash=-0.25 if duck else 0, larm=(0.9 * math.sin(t * 18.8), 0.9), rarm=(-1.1, 1.6))
        bundle(ctx, hands["r"][0] + 10, hands["r"][1] - 40, 0.55, rot=0.2, t=t)
        speed_lines(ctx, hx - 80, base - 250, seed=int(t * 8))
    else:
        u = prog(t, t_crunch, t_crunch + 1.0)
        hero(ctx, cart_x + u * 200, base - 500 - math.sin(u * math.pi) * 300 + u * 300, 0.62, t, coat=True,
             expr="scared", tilt=2.6 + t * 3 * (1 - u), larm=(2.4, 0.4), rarm=(-2.4, -0.4))
    baker(ctx, cart_x + 300, base - 268, 0.6, t, face=-0.8, expr="frown" if t > t_baker else ("shock" if t > t_crunch else "o"),
          brows="angry" if t > t_baker else None, larm=(0.3, 0.2) if t < t_baker else (2.2, 0.8),
          rarm=(-0.3, -0.2) if t < t_baker else (-2.2, -0.8))
    ctx.restore()
    for (lab, tc) in (("HOP!", jump_t - 0.3), ("DUCK!", duck_t - 0.3), ("DODGE!", dodge_t - 0.3)):
        if tc < t < tc + 1.0:
            pop_text(ctx, lab, 960, 160, 100, t - tc, GOLD)
    if t > t_cart and t < t_crunch:
        pop_text(ctx, "THAT BAGUETTE CART.", 960, 980, 80, t - t_cart, RED)
    if t > t_crunch:
        burst(ctx, 1300, 260, 200, t - t_crunch, "CRUNCH!", size=80, color=(1, 0.85, 0.35))
    vignette(ctx, 0.35)


def sh_hide(ctx, t, D, cue):
    t_pound = cue("My heart")
    t_holding = cue("I was holding")
    t_plan = cue("I needed")
    base = 820
    ctx.save()
    cam(ctx, 960, 560, lerp(1.0, 1.25, ease(prog(t, 0, D))))
    paris_street(ctx, t, x0=-800, x1=3000, base=base - 20, eiffel_x=1600, seed=14)
    # wanted poster
    if t > t_holding:
        ka = back_out(prog(t, t_holding + 1.5, t_holding + 2.0), 1.6)
        ctx.save()
        ctx.translate(1450, 420)
        ctx.rotate(0.04)
        ctx.scale(max(ka, 1e-3), max(ka, 1e-3))
        rrect(ctx, -150, -200, 300, 400, 6)
        fs(ctx, hexc("#f2e6c4"), lw=6)
        text(ctx, "RECHERCHÉ", 0, -150, 44, RED, outline=0, shadow=False)
        circle(ctx, 0, -20, 70)
        fs(ctx, WHITE, lw=5)
        ctx.save()
        ctx.translate(0, -20)
        ctx.scale(0.7, 0.7)
        draw_cap(ctx)
        ctx.restore()
        text(ctx, "petit · rapide", 0, 110, 32, INK, font=HAND_FONT, outline=0, shadow=False)
        text(ctx, "CASQUETTE ROUGE", 0, 155, 30, INK, outline=0, shadow=False)
        ctx.restore()
    # bread pile with eyes
    for k in range(18):
        rnd = random.Random(k)
        baguette(ctx, 700 + rnd.uniform(-180, 180), base + 20 - rnd.uniform(0, 150), 1.0, rot=rnd.uniform(-0.6, 0.6))
    peek = 0.5 + 0.5 * math.sin(t * 1.5)
    for ex in (-25, 25):
        circle(ctx, 700 + ex, base - 120 - 10 * peek, 18)
        fs(ctx, WHITE, lw=4)
        circle(ctx, 700 + ex + 6 * math.sin(t * 2), base - 120 - 10 * peek, 7)
        fs(ctx, INK, lw=0)
    ctx.save()
    ctx.translate(700, base - 180 - 10 * peek)
    ctx.scale(0.45, 0.45)
    draw_cap(ctx)
    ctx.restore()
    # policemen running past then gone
    k = prog(t, 0, t_pound + 1.0)
    if k < 1:
        for i in range(3):
            policeman(ctx, lerp(-300, 2600, k) - i * 220, base - 268, 0.62, t, seed=i, whistle=(i == 0), expr="frown",
                      brows="angry", **run_kw(t + i * 0.2, 2.6))
    # heartbeat
    if t > t_pound:
        beat = abs(math.sin(t * 7)) ** 6
        ctx.save()
        ctx.translate(820, base - 330)
        ctx.scale(0.6 + 0.3 * beat, 0.6 + 0.3 * beat)
        text(ctx, "♥", 0, 0, 120, RED, font="DejaVu Sans", outline=6, shadow=False)
        ctx.restore()
    ctx.restore()
    if t < t_pound:
        text(ctx, "tweet... tweet...", 1500, 200, 60, WHITE, font=HAND_FONT, outline=6, alpha=1 - prog(t, 0, t_pound))
    if t > t_plan:
        pop_text(ctx, "NEW PLAN NEEDED.", 960, 980, 90, t - t_plan, GOLD)
    vignette(ctx, 0.4)


def sh_note(ctx, t, D, cue):
    lines = [("Dear police,", cue("Dear police")),
             ("Here is the Mona Lisa.", cue("Here is the Mona Lisa")),
             ("I did not steal it.", cue("I did not steal it")),
             ("I found it.", cue("I found it")),
             ("Please give it back", cue("Please give it back")),
             ("to the Louvre.", cue("Please give it back", frac=0.5)),
             ("Sincerely, a friend", cue("Sincerely")),
             ("P.S. Sorry about the baguettes.", cue("P.S."))]
    bg_fill(ctx, hexc("#5a3a22"))
    for k in range(0, H, 50):
        line(ctx, 0, k, W, k + 20, 3, hexc("#4a2e1a"))
    ctx.save()
    z = lerp(1.0, 1.08, ease(prog(t, 0, D)))
    cam(ctx, 960, 540, z)
    ctx.save()
    ctx.translate(960, 540)
    ctx.rotate(-0.03)
    rrect(ctx, -520, -460, 1040, 920, 8)
    fs(ctx, hexc("#fbf6e8"), lw=6)
    for k in range(13):
        line(ctx, -480, -330 + k * 64, 480, -330 + k * 64, 2, hexc("#a8c4e0"))
    line(ctx, -400, -440, -400, 440, 2, hexc("#e0a0a0"))
    pen = None
    for i, (s, tc) in enumerate(lines):
        if t < tc:
            continue
        frac = clamp((t - tc) / max(0.6, len(s) * 0.06))
        shown = s[:int(len(s) * frac)]
        y = -350 + i * 96
        x0 = -360 + (60 if i in (1, 2, 3, 4, 5) else 0)
        col = RED if s.startswith("P.S.") else hexc("#1f2c4a")
        text(ctx, shown, x0, y, 58, col, font=HAND_FONT, align="left", outline=0, shadow=False)
        if frac < 1:
            pen = (x0 + text_width(ctx, shown, 58, HAND_FONT), y)
    if pen:
        line(ctx, pen[0], pen[1] + 10, pen[0] + 180, pen[1] - 200, 16, hexc("#e8c84a"))
        line(ctx, pen[0], pen[1] + 10, pen[0] + 24, pen[1] - 18, 8, INK)
    # little red-cap doodle signature
    if t > cue("Sincerely") + 1.0:
        ctx.save()
        ctx.translate(320, 250)
        ctx.scale(0.4, 0.4)
        circle(ctx, 0, 0, 100)
        fs(ctx, WHITE, lw=8)
        circle(ctx, -25, -10, 9)
        circle(ctx, 35, -12, 9)
        fs(ctx, INK, lw=0)
        draw_cap(ctx)
        ctx.restore()
    ctx.restore()
    ctx.restore()
    vignette(ctx, 0.4)


def police_station(ctx, t, base=820, lights=0.0):
    lit = {}
    rnd = random.Random(3)
    for s in range(3, 12):
        for f in range(1, 6):
            for c in range(5):
                lit[(s, f, c)] = rnd.random() < lights
    paris_street(ctx, t, x0=-800, x1=3000, base=base - 20, night=True, eiffel_x=1900, seed=3, lamps_lit=1.0, lit=lit)
    # station front
    ctx.rectangle(600, base - 520, 700, 500)
    fs(ctx, hexc("#4a4a5e"), lw=7)
    rrect(ctx, 650, base - 560, 600, 70, 6)
    fs(ctx, NAVY, lw=6)
    text(ctx, "COMMISSARIAT DE POLICE", 950, base - 525, 38, WHITE, outline=0, shadow=False)
    # blue lantern
    warm_glow(ctx, 1320, base - 420, 160, 0.6, (0.4, 0.6, 1.0))
    rrect(ctx, 1295, base - 460, 50, 80, 10)
    fs(ctx, hexc("#6a9af2"), lw=5)
    # door + steps
    for k in range(3):
        ctx.rectangle(780 - k * 30, base - 20 + k * 20 - 40, 340 + k * 60, 22)
        fs(ctx, hexc("#7a7a8a"), lw=4)
    rrect(ctx, 840, base - 330, 220, 270, 20)
    fs(ctx, hexc("#3a2a1e"), lw=7)
    circle(ctx, 1030, base - 190, 9)
    fs(ctx, GOLD, lw=3)
    # bell
    circle(ctx, 1110, base - 260, 14)
    fs(ctx, GOLD, lw=4)


def sh_station(ctx, t, D, cue):
    t_officer = cue("From behind")
    base = 820
    # beats inside the first sentence
    t_tiptoe_end = 2.4
    t_place = 3.0
    t_ring = 4.0
    t_ran = 4.8
    door = ease(prog(t, t_officer + 2.0, t_officer + 2.8))
    scream = t > t_officer + 4.6
    ctx.save()
    cam(ctx, lerp(700, 1000, ease(prog(t, 0, t_ran))), 520, 0.95, shake=6 if scream else 0, t=t)
    police_station(ctx, t, base, lights=ease(prog(t, t_officer + 4.8, t_officer + 6.5)))
    if t > t_place:
        bundle(ctx, 950, base - 150, 0.6, rot=0.0, t=t)
        # the note
        ctx.rectangle(1000, base - 120, 70, 50)
        fs(ctx, hexc("#fbf6e8"), lw=3)
    if door > 0:
        ctx.save()
        rrect(ctx, 840, base - 330, 220, 270, 20)
        setc(ctx, hexc("#ffd98a"))
        ctx.fill()
        ctx.restore()
        ctx.rectangle(840, base - 330, 220 * (1 - door * 0.8), 270)
        fs(ctx, hexc("#3a2a1e"), lw=5)
        policeman(ctx, 960, base - 302, 0.55, t, seed=5, face=0.0, expr="flat" if not scream else "scared",
                  look=(0, 1) if t > t_officer + 3.5 else (0, 0), blink=0.9 if not scream else 0.0,
                  larm=(0.3, 0.2) if not scream else (2.6, 0.3), rarm=(-0.3, -0.2) if not scream else (-2.6, -0.3),
                  body=hexc("#c8d8f0"), brows="up" if scream else None)
        ctx.save()
        ctx.translate(960, base - 302)
        ctx.scale(0.55, 0.55)
        nightcap(ctx)
        ctx.restore()
    # hero
    if t < t_ran:
        hx = lerp(200, 880, ease(prog(t, 0, t_tiptoe_end))) if t < t_place else 880
        hero(ctx, hx, base - 272, 0.55, t, expr="sly", face=0.8, look=(1, 0.3), squash=-0.08,
             walk=t * 0.8 if t < t_tiptoe_end else None, larm=(1.4, -1.6), rarm=(-1.6, 0.6) if t > t_ring else (-1.1, 1.6),
             blink=doodle_auto_blink(t))
        if t < t_place:
            bundle(ctx, hx + 70, base - 330, 0.5, rot=0.2, t=t)
    else:
        k = ease_out(prog(t, t_ran, t_ran + 0.8))
        hx = lerp(880, 260, k)
        hide = k >= 1
        hero(ctx, hx, base - 272, 0.55, t, expr="sly" if hide else "grin", face=0.6 if hide else -0.9, look=(1, 0),
             walk=None if hide else t * 3, larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    gas_lamp(ctx, 330, base + 30, lit=1.0) if t > t_ran else None
    ctx.restore()
    if t_ring < t < t_ring + 1.2:
        pop_text(ctx, "DING-DONG!", 1250, 180, 80, t - t_ring, GOLD)
    if scream:
        burst(ctx, 1300, 230, 180, t - t_officer - 4.6, "AAAAAH!", size=74, color=(1, 0.85, 0.3))
    vignette(ctx, 0.5)


def sh_history(ctx, t, D, cue):
    t_real = cue("In real history")
    t_peru = cue("The thief, a man named")
    t_crowds = cue("Meanwhile")
    t_famous = cue("That's how")
    paper_lesson(ctx, "WHAT REALLY HAPPENED", t, RED)
    # timeline
    k = ease(prog(t, t_real, t_real + 1.5))
    line(ctx, 200, 300, lerp(200, 1720, k), 300, 10)
    for i, (x, lab, sub) in enumerate(((240, "21 AUG 1911", "stolen"), (980, "1911 - 1913", "missing"),
                                       (1680, "DEC 1913", "found in Florence"))):
        tc = t_real + 0.5 + i * 0.6
        if t > tc:
            circle(ctx, x, 300, 18 * back_out(clamp((t - tc) / 0.3)))
            fs(ctx, RED, lw=5)
            text(ctx, lab, x, 240, 44, INK, outline=0, shadow=False, alpha=ease(clamp((t - tc) / 0.3)))
            text(ctx, sub, x, 360, 40, INK, font=HAND_FONT, outline=0, shadow=False, alpha=ease(clamp((t - tc) / 0.3)))
    if t_peru < t < t_crowds:
        # trunk in the small apartment
        ka = ease_out(prog(t, t_peru + 1.0, t_peru + 1.6))
        ctx.save()
        ctx.translate(560, 720)
        ctx.scale(max(ka, 1e-3), max(ka, 1e-3))
        rrect(ctx, -220, -130, 440, 230, 16)
        fs(ctx, hexc("#7a4a24"), lw=7)
        lid = ease(prog(t, t_peru + 2.5, t_peru + 3.3))
        ctx.save()
        ctx.translate(-220, -130)
        ctx.rotate(-1.0 * lid)
        rrect(ctx, 0, -70, 440, 70, 16)
        fs(ctx, hexc("#8a5a2b"), lw=7)
        ctx.restore()
        if lid > 0.3:
            ctx.save()
            ctx.translate(0, -60)
            ctx.rotate(-0.1)
            mona(ctx, 0, 0, 110, 160)
            ctx.restore()
        for k2 in (-150, 150):
            ctx.rectangle(k2 - 15, -130, 30, 230)
            fs(ctx, hexc("#c9a040"), lw=4)
        ctx.restore()
        thief(ctx, 1150, 540, 0.62, t, face=-0.6, expr="sly", larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        text(ctx, "VINCENZO PERUGGIA", 1150, 1000, 56, INK, outline=0, shadow=False,
             alpha=ease(prog(t, t_peru + 0.8, t_peru + 1.2)))
        if t > t_peru + 6.0:
            rrect(ctx, 1450, 520, 360, 130, 10)
            fs(ctx, hexc("#2a3f6a"), lw=5)
            text(ctx, "FLORENCE", 1630, 565, 44, WHITE, outline=0, shadow=False)
            text(ctx, "Dec 1913", 1630, 615, 36, GOLD, font=HAND_FONT, outline=0, shadow=False)
    elif t > t_crowds:
        # crowds staring at the empty wall
        ctx.rectangle(300, 450, 1320, 420)
        fs(ctx, WALL_RED, lw=6)
        ctx.rectangle(890, 520, 140, 200)
        ctx.save()
        ctx.set_dash([10, 8])
        fs(ctx, None, lw=4, stroke=hexc("#3a1010"))
        ctx.restore()
        for i in range(9):
            citizen(ctx, 380 + i * 140, 700, 0.36, t, seed=i, face=0.0, expr="o", look=(0, -1),
                    larm=(0.3, 0.2), rarm=(-0.3, -0.2), show_legs=False)
        if t > t_famous:
            pop_text(ctx, "MOST FAMOUS PAINTING ON EARTH", 960, 980, 70, t - t_famous, RED)
    vignette(ctx, 0.3)


def sh_glow(ctx, t, D, cue):
    t_early = cue("Two years early")
    t_glow = cue("Then my ticket")
    paper_lesson(ctx, "WHAT REALLY HAPPENED", D, RED)
    line(ctx, 200, 300, 1720, 300, 10)
    circle(ctx, 240, 300, 18)
    fs(ctx, RED, lw=5)
    text(ctx, "21 AUG 1911", 240, 240, 44, INK, outline=0, shadow=False)
    text(ctx, "DEC 1913", 1680, 240, 44, INK, outline=0, shadow=False)
    k = ease(prog(t, 0.3, 1.0))
    line(ctx, 1560, 200, lerp(1560, 1800, k), lerp(200, 280, k), 12, RED)
    line(ctx, 1800, 200, lerp(1800, 1560, k), lerp(200, 280, k), 12, RED)
    ka = back_out(prog(t, 1.0, 1.4), 2)
    ctx.save()
    ctx.translate(420, 420)
    ctx.rotate(-0.08)
    ctx.scale(max(ka, 1e-3), max(ka, 1e-3))
    rrect(ctx, -200, -50, 400, 100, 12)
    fs(ctx, GOLD, lw=6)
    text(ctx, "SAME NIGHT!", 0, 0, 60, INK, outline=0, shadow=False)
    ctx.restore()
    if t > t_early:
        pop_text(ctx, "2 YEARS EARLY", 1300, 520, 80, t - t_early, hexc("#2f7a3a"), outline=0)
    if t > t_glow:
        g = ease(prog(t, t_glow, D))
        setc(ctx, (1, 0.9, 0.5), 0.4 * g)
        ctx.paint()
        ticket(ctx, 960, 760, 0.8, rot=0.05 * math.sin(t * 20), glow=1.0, t=t)
    vignette(ctx, 0.3)


def laptop(ctx, x, y, s, t, typed="", results=0.0, cap=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -520, -340, 1040, 640, 24)
    fs(ctx, hexc("#2a2a33"), lw=8)
    rrect(ctx, -490, -310, 980, 580, 10)
    fs(ctx, WHITE, lw=0)
    # browser bar
    rrect(ctx, -460, -280, 920, 70, 35)
    fs(ctx, hexc("#eef0f4"), lw=4)
    text(ctx, typed + ("|" if (t * 2) % 2 < 1 else ""), -420, -245, 40, INK, font=HAND_FONT, align="left", outline=0,
         shadow=False)
    circle(ctx, 410, -245, 18)
    fs(ctx, None, lw=4)
    line(ctx, 423, -232, 438, -217, 5)
    if results > 0:
        a = ease(results)
        text(ctx, "Mona Lisa theft (1911)", -430, -160, 46, hexc("#1a4ab8"), align="left", outline=0, shadow=False, alpha=a)
        text(ctx, "Stolen from the Louvre on 21 August 1911.", -430, -95, 36, INK, font=HAND_FONT, align="left", outline=0,
             shadow=False, alpha=a)
        text(ctx, "Returned THE SAME NIGHT by an unknown hero,", -430, -45, 36, INK, font=HAND_FONT, align="left",
             outline=0, shadow=False, alpha=a)
        text(ctx, "described as short, very fast,", -430, 5, 36, INK, font=HAND_FONT, align="left", outline=0,
             shadow=False, alpha=a)
        text(ctx, "and wearing a strange RED CAP.", -430, 55, 36, RED, font=HAND_FONT, align="left", outline=0,
             shadow=False, alpha=a)
        rrect(ctx, 200, -150, 250, 300, 8)
        fs(ctx, hexc("#e8e0d0"), lw=4)
        if cap > 0:
            ctx.save()
            ctx.translate(325, 10)
            ctx.scale(0.55 * cap, 0.55 * cap)
            circle(ctx, 0, 0, 100)
            fs(ctx, hexc("#f2efe6"), lw=6)
            draw_cap(ctx)
            ctx.restore()
            text(ctx, "\"the red-cap hero\"", 325, 120, 26, INK, font=HAND_FONT, outline=0, shadow=False)
    ctx.restore()
    poly(ctx, [(x - 600 * s, y + 300 * s), (x + 600 * s, y + 300 * s), (x + 660 * s, y + 360 * s), (x - 660 * s, y + 360 * s)])
    fs(ctx, hexc("#3a3a44"), lw=6)


def sh_home(ctx, t, D, cue):
    t_bed = cue("Back in my bedroom")
    t_laptop = cue("I grabbed my laptop")
    t_jaw = cue("And my jaw")
    t_stolen = cue("Stolen August")
    t_ret = cue("Returned the very")
    if t < t_laptop:
        ctx.save()
        cam(ctx, 960, 540, 1.0)
        bedroom_bg(ctx, t)
        land = ease_out(prog(t, 0, 0.4))
        sq = -0.15 * math.exp(-max(0, t - 0.4) * 6) if t > 0.4 else 0
        hero(ctx, 1350, lerp(-300, 520, land), 0.7, t, coat=True, expr="o", face=-0.4, squash=sq,
             larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        ctx.restore()
        setc(ctx, WHITE, 1 - clamp(t / 0.5))
        ctx.paint()
        if t > cue("Still no charger"):
            pop_text(ctx, "(still no charger)", 960, 980, 64, t - cue("Still no charger"), WHITE, font=HAND_FONT, outline=6)
    else:
        bg_fill(ctx, hexc("#3a4a6a"))
        typed_full = "mona lisa theft"
        n = int(len(typed_full) * clamp((t - t_laptop - 1.0) / 1.6))
        res = prog(t, t_jaw - 0.3, t_jaw + 0.3)
        z = 1.0 if t < t_ret else lerp(1.0, 1.18, ease(prog(t, t_ret, t_ret + 2)))
        ctx.save()
        cam(ctx, 960 if t < t_ret else lerp(960, 1010, ease(prog(t, t_ret, t_ret + 2))), 500, z)
        laptop(ctx, 960, 520, 1.15, t, typed=typed_full[:n], results=res, cap=ease_out(prog(t, t_ret + 3.0, t_ret + 3.6)))
        ctx.restore()
        if t > t_jaw:
            hero(ctx, 180, lerp(1300, 760, ease_out(prog(t, t_jaw, t_jaw + 0.4))), 0.6, t, expr="shock", face=0.6,
                 look=(1, -0.5), larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    vignette(ctx, 0.35)


def sh_next(ctx, t, D, cue):
    t_famous = cue("I was famous")
    t_glow = cue("Then the ticket")
    t_dest = cue("Next destination")
    t_uh = cue("Uh oh")
    t_no = cue("No, no, no")
    t_refund = cue("Can I get")
    if t < t_glow:
        ctx.save()
        cam(ctx, 960, 540, 1.0)
        bedroom_bg(ctx, t)
        hero(ctx, 1000, 500 - abs(math.sin(t * 6)) * 40, 0.7, t, coat=True, expr="laugh", face=0.0,
             larm=(2.6, 0.3), rarm=(-2.6, -0.3))
        ctx.restore()
        confetti(ctx, t)
        pop_text(ctx, "FAMOUS!", 960, 140, 130, t - 0.2, GOLD)
        if t > cue("Kind of"):
            pop_text(ctx, "(kind of)", 960, 260, 60, t - cue("Kind of"), WHITE, font=HAND_FONT, outline=6)
    elif t < t_uh:
        bg_fill(ctx, hexc("#141a33"))
        g = ease(prog(t, t_glow, t_dest))
        ctx.save()
        cam(ctx, 960, 540, lerp(1.0, 1.15, g), shake=5 * g, t=t)
        ticket(ctx, 960, 520, 1.7, glow=g, t=t, text_mode="titanic" if t > t_dest - 0.2 else "louvre")
        ctx.restore()
        if t > t_dest - 0.3:
            setc(ctx, WHITE, 1 - clamp((t - t_dest + 0.3) / 0.4))
            ctx.paint()
    else:
        # panic
        ctx.save()
        cam(ctx, 960, 540, 1.0, shake=6, t=t)
        bedroom_bg(ctx, t)
        a = t * 6
        running = t > t_no
        hx = 960 + (math.cos(a) * 380 if running else 0)
        hy = 500 + (math.sin(a) * 40 if running else 0)
        hero(ctx, hx, hy, 0.7, t, coat=True, expr="scared", face=-math.sin(a) if running else 0.0, brows="worried",
             walk=t * 3 if running else None, larm=(2.6, 0.3), rarm=(-2.6, -0.3), cap_off=0.35 * abs(math.sin(t * 9)) if running else 0)
        sweat(ctx, hx + 60, hy - 90, 1.0, t)
        sweat(ctx, hx - 60, hy - 80, 0.8, t + 0.4)
        ticket(ctx, 400, 860, 0.35, rot=0.3, glow=0.6, t=t, text_mode="titanic")
        ctx.restore()
        if t < t_no:
            pop_text(ctx, "UH OH.", 960, 140, 130, t - t_uh, RED)
        else:
            pop_text(ctx, "NO NO NO NO!", 960, 140, 120, t - t_no, RED, rot=-0.05, hold=t_refund - t_no)
        if t > t_refund:
            pop_text(ctx, "REFUND???", 960, 980, 110, t - t_refund, GOLD, rot=0.04)
    vignette(ctx, 0.35)


def sh_outro(ctx, t, D, cue):
    t_jacket = cue("And maybe")
    spiral_bg(ctx, t, speed=0.2)
    k = ease_out(prog(t, 0, 0.5))
    hands = hero(ctx, 960, lerp(1400, 400, k), 1.15, t, expr="grin", face=0.0, look=(0, 0),
                 larm=(0.3, 0.2), rarm=(-2.6 + 0.25 * math.sin(t * 7), 0.4))
    if t > t_jacket:
        a = back_out(prog(t, t_jacket, t_jacket + 0.5), 2)
        # life jacket (life ring)
        ctx.save()
        ctx.translate(960, 400 + 230 * 1.15)
        ctx.scale(max(a, 1e-3), max(a, 1e-3))
        circle(ctx, 0, 0, 150)
        circle(ctx, 0, 0, 80)
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        setc(ctx, hexc("#ff7a2a"))
        ctx.fill_preserve()
        setc(ctx, INK)
        ctx.set_line_width(7)
        ctx.stroke()
        ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
        for k2 in range(4):
            aa = k2 * math.pi / 2 + 0.4
            ctx.move_to(math.cos(aa) * 82, math.sin(aa) * 82)
            ctx.arc(0, 0, 148, aa, aa + 0.5)
            ctx.arc_negative(0, 0, 82, aa + 0.5, aa)
            ctx.close_path()
            setc(ctx, WHITE)
            ctx.fill()
        ctx.restore()
        pop_text(ctx, "TITANIC, 1912", 1500, 300, 70, t - t_jacket, WHITE, rot=0.05)
    pop_text(ctx, "SUBSCRIBE TO HISTORY WORLD!", 960, 110, 80, t - 0.6, WHITE)
    vignette(ctx, 0.45)


def sh_endcard(ctx, t, D, cue):
    vgrad(ctx, 0, 0, W, H, hexc("#2a3f6a"), hexc("#ff6a8a"))
    ctx.save()
    ctx.translate(W / 2, H / 2)
    ctx.rotate(t * 0.3)
    cols = [hexc("#ffd36a"), hexc("#ff8a4a"), hexc("#ff6aa8"), hexc("#6ad0ff")]
    for k in range(24):
        ctx.move_to(0, 0)
        ctx.arc(0, 0, 1600, k * math.pi / 12, k * math.pi / 12 + math.pi / 12)
        ctx.close_path()
        setc(ctx, cols[k % 4], 0.3)
        ctx.fill()
    ctx.restore()
    eiffel(ctx, 1750, 1080, 520, c=hexc("#2a2440"))
    confetti(ctx, t, n=80)
    k = ease_out(prog(t, 0.0, 0.6))
    hands = hero(ctx, 380, lerp(1400, 560, k), 0.85, t, expr="grin", face=0.4, larm=(0.3, 0.2),
                 rarm=(-2.6 + 0.3 * math.sin(t * 7), 0.5))
    a = back_out(prog(t, 0.3, 0.8), 2) * (1 + 0.04 * math.sin(t * 5))
    ctx.save()
    ctx.translate(1100, 360)
    ctx.scale(max(a, 1e-3), max(a, 1e-3))
    ctx.rotate(-0.03)
    text(ctx, "HISTORY WORLD", 0, -40, 150, GOLD_L, outline=16)
    ctx.restore()
    tb = t - 1.0
    if tb > 0:
        kk = back_out(clamp(tb / 0.4), 2) * (1 + 0.05 * math.sin(t * 6))
        ctx.save()
        ctx.translate(1100, 620)
        ctx.scale(max(kk, 1e-3), max(kk, 1e-3))
        rrect(ctx, -300, -80, 600, 160, 40)
        fs(ctx, hexc("#ff2a2a"), lw=8)
        poly(ctx, [(-220, -40), (-220, 40), (-160, 0)])
        fs(ctx, WHITE, lw=0)
        text(ctx, "SUBSCRIBE", 40, 0, 80, WHITE, outline=6)
        ctx.restore()
        ctx.save()
        ctx.translate(1490, 620)
        ctx.rotate(0.3 * math.sin(t * 10) * kk)
        ctx.move_to(-40, 30)
        ctx.curve_to(-40, -60, 40, -60, 40, 30)
        ctx.close_path()
        fs(ctx, GOLD, lw=6)
        circle(ctx, 0, 40, 10)
        fs(ctx, GOLD, lw=4)
        ctx.restore()
        # click cursor
        if tb > 0.8:
            u = ease(prog(tb, 0.8, 1.4))
            cxp, cyp = lerp(1500, 1150, u), lerp(950, 640, u)
            poly(ctx, [(cxp, cyp), (cxp, cyp + 60), (cxp + 16, cyp + 46), (cxp + 30, cyp + 74), (cxp + 40, cyp + 68),
                       (cxp + 26, cyp + 42), (cxp + 46, cyp + 40)])
            fs(ctx, WHITE, lw=4)
            if tb > 1.4:
                pop_text(ctx, "SUBSCRIBED!", 1100, 760, 50, tb - 1.4, (0.4, 1, 0.5))
    if t > 1.8:
        text(ctx, "Next time: Titanic, 1912. What could go wrong?", 1100, 900, 46, WHITE, font=HAND_FONT,
             outline=5, alpha=ease(prog(t, 1.8, 2.4)))
    fade = prog(t, D - 0.8, D)
    if fade > 0:
        setc(ctx, (0, 0, 0), fade)
        ctx.paint()


SHOT_FUNCS = {
    "hook": sh_hook, "crash": sh_crash, "rewind": sh_rewind, "title": sh_title, "ticket": sh_ticket,
    "portal": sh_portal, "paris": sh_paris, "newspaper": sh_newspaper, "plan": sh_plan, "disguise": sh_disguise,
    "louvre": sh_louvre, "empty": sh_empty, "suspect": sh_suspect, "chase": sh_chase, "stairs": sh_stairs,
    "catch": sh_catch, "guard": sh_guard, "escape": sh_escape, "streetchase": sh_streetchase, "hide": sh_hide,
    "note": sh_note, "station": sh_station, "history": sh_history, "glow": sh_glow, "home": sh_home,
    "next": sh_next, "outro": sh_outro, "endcard": sh_endcard,
}
