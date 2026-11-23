"""Shots for 'How I Accidentally Ruined Napoleon's Coronation'.
Each shot: fn(ctx, t, D, cue). cue(text) -> start time of the sentence containing text."""
import math, random
import cairo
from gfx import *

TIMELINE = {}          # filled by render.Renderer: id -> (shot, cue)

GOLD = (1, 0.84, 0.3)
GOLD_D = hexc("#b8892a")
GOLD_L = hexc("#ffe28a")
CRIMSON = hexc("#9a1b2b")
VELVET = hexc("#7a0f1e")
FR_BLUE = hexc("#22417a")
MARBLE = hexc("#f4efe4")
MARBLE_D = hexc("#d8cfbd")
STONE = hexc("#cfc4ae")
STONE_D = hexc("#a89c84")


# ====================================================================== helpers
def cam(ctx, cx, cy, z=1.0, rot=0.0, shake=0.0, t=0.0):
    sx = shake * (math.sin(t * 47) + math.sin(t * 31)) * 0.5
    sy = shake * (math.cos(t * 53) + math.sin(t * 37)) * 0.5
    ctx.translate(W / 2 + sx, H / 2 + sy)
    ctx.rotate(rot)
    ctx.scale(z, z)
    ctx.translate(-cx, -cy)


def caption(ctx, place, year, t, dur=4.0):
    if t < 0 or t > dur + 0.6:
        return
    k = ease_out(prog(t, 0, 0.5)) - ease_in(prog(t, dur, dur + 0.5))
    x = lerp(-900, 70, k)
    rrect(ctx, x, 850, 800, 150, 18)
    fs(ctx, (0.08, 0.07, 0.1, 0.82), lw=0)
    for i, c in enumerate((FR_BLUE, WHITE, RED)):
        ctx.rectangle(x + i * 6, 850, 6, 150)
        setc(ctx, c)
        ctx.fill()
    text(ctx, place, x + 44, 898, 46, WHITE, align="left", outline=0, shadow=False)
    text(ctx, year, x + 44, 958, 52, GOLD, align="left", outline=0, shadow=False)


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


# ====================================================================== props
def leaf(ctx, x, y, s=1.0, rot=0.0, glint=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ctx.move_to(0, -40)
    ctx.curve_to(22, -22, 22, 22, 0, 40)
    ctx.curve_to(-22, 22, -22, -22, 0, -40)
    g = cairo.LinearGradient(-20, -40, 20, 40)
    g.add_color_stop_rgb(0, *GOLD_L)
    g.add_color_stop_rgb(0.5, *GOLD)
    g.add_color_stop_rgb(1, *GOLD_D)
    ctx.set_source(g)
    ctx.fill_preserve()
    setc(ctx, hexc("#6a4a10"))
    ctx.set_line_width(4 / max(s, 0.2) * 0.5 + 2)
    ctx.stroke()
    line(ctx, 0, -34, 0, 34, 2.5, hexc("#8a6a20"))
    ctx.restore()
    if glint > 0:
        sparkle(ctx, x + 10 * s, y - 15 * s, 22 * s * glint, glint * 10)


def laurel(ctx, x, y, s=1.0, missing=0, t=0.0, rot=0.0):
    """golden laurel wreath seen slightly from above: two branches meeting at the back, open at the front-top."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ellipse(ctx, 0, 0, 130, 70)
    setc(ctx, GOLD_D)
    ctx.set_line_width(8)
    ctx.stroke()
    n = 10
    for side in (-1, 1):
        for i in range(n):
            if side == 1 and i >= n - missing:
                continue
            a = math.pi / 2 + side * (0.15 + i * 0.27)
            lx, ly = math.cos(a) * 130, math.sin(a) * 70
            tang = math.atan2(math.cos(a) * 70, -math.sin(a) * 130) * side
            for off in (-0.55, 0.55):
                leaf(ctx, lx, ly, 0.42, rot=tang + off + (math.pi / 2 if side < 0 else -math.pi / 2) * 0)
    ctx.restore()


def imperial_crown(ctx, x, y, s=1.0, rot=0.0, glow=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    if glow > 0:
        warm_glow(ctx, 0, -40, 260, 0.5 * glow, (1, 0.9, 0.5))
    # velvet cap
    ctx.move_to(-95, 20)
    ctx.curve_to(-110, -110, 110, -110, 95, 20)
    ctx.close_path()
    fs(ctx, VELVET, lw=6)
    # arches
    for k in (-1, 0, 1):
        ctx.move_to(-95 + 95 * (k + 1) * 0.0, 0)
        ctx.move_to(k * 90, 10)
        ctx.curve_to(k * 90, -90, k * 30, -130, 0, -132)
        setc(ctx, GOLD)
        ctx.set_line_width(16)
        ctx.stroke_preserve()
        setc(ctx, hexc("#6a4a10"))
        ctx.set_line_width(3)
        ctx.stroke()
    # band
    rrect(ctx, -110, -10, 220, 60, 10)
    g = cairo.LinearGradient(0, -10, 0, 50)
    g.add_color_stop_rgb(0, *GOLD_L)
    g.add_color_stop_rgb(1, *GOLD_D)
    ctx.set_source(g)
    ctx.fill_preserve()
    setc(ctx, hexc("#6a4a10"))
    ctx.set_line_width(5)
    ctx.stroke()
    for i, c in enumerate((hexc("#2b6bd6"), hexc("#d62b3a"), hexc("#2bb36b"), hexc("#d62b3a"), hexc("#2b6bd6"))):
        ellipse(ctx, -80 + i * 40, 20, 12, 15)
        fs(ctx, c, lw=3)
    # orb + cross
    circle(ctx, 0, -146, 18)
    fs(ctx, GOLD, lw=4)
    ctx.rectangle(-5, -190, 10, 34)
    fs(ctx, GOLD, lw=3)
    ctx.rectangle(-16, -180, 32, 9)
    fs(ctx, GOLD, lw=3)
    # shine
    ctx.move_to(-90, 0)
    ctx.line_to(-70, 0)
    ctx.line_to(-40, 45)
    ctx.line_to(-60, 45)
    setc(ctx, WHITE, 0.35)
    ctx.fill()
    ctx.restore()


def small_crown(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    poly(ctx, [(-60, 20), (-60, -20), (-40, 0), (-20, -35), (0, -5), (20, -35), (40, 0), (60, -20), (60, 20)])
    fs(ctx, GOLD, lw=5)
    for i in range(3):
        circle(ctx, -30 + i * 30, 6, 7)
        fs(ctx, hexc("#d62b3a") if i != 1 else hexc("#2b6bd6"), lw=2)
    ctx.restore()


def cushion(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(-110, 0)
    ctx.curve_to(-120, -30, 120, -30, 110, 0)
    ctx.curve_to(120, 30, -120, 30, -110, 0)
    fs(ctx, CRIMSON, lw=5)
    for sx in (-1, 1):
        line(ctx, sx * 112, 0, sx * 120, 30, 4, GOLD)
        circle(ctx, sx * 120, 36, 8)
        fs(ctx, GOLD, lw=3)
    ctx.restore()


def flag_fr(ctx, x, y, s, t, ph=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    line(ctx, 0, 0, 0, 260, 7, hexc("#6b4428"))
    for i, c in enumerate((FR_BLUE, WHITE, RED)):
        ctx.move_to(i * 50, 0)
        for k in range(11):
            xx = i * 50 + k * 5
            ctx.line_to(xx, math.sin(t * 4 + ph + xx * 0.04) * 6)
        for k in range(10, -1, -1):
            xx = i * 50 + k * 5
            ctx.line_to(xx, 100 + math.sin(t * 4 + ph + xx * 0.04) * 6)
        ctx.close_path()
        fs(ctx, c, lw=3)
    ctx.restore()


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


def carriage(ctx, x, y, s, t, moving=True, horses=True, rider=None):
    """golden coronation coach; (x,y) = ground under the coach centre."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if horses:
        for k in range(4):
            hx = 380 + k * 230
            horse(ctx, hx + 25, -125, 1.0, t, ph=k * 0.7, moving=moving)
            horse(ctx, hx, -110, 1.05, t, ph=k * 0.7 + 1.5, moving=moving)
        line(ctx, 150, -110, 380, -110, 6, hexc("#6b4428"))
    for wx, r in ((-150, 85), (130, 70)):
        ctx.save()
        ctx.translate(wx, -r)
        circle(ctx, 0, 0, r)
        fs(ctx, GOLD, lw=6)
        circle(ctx, 0, 0, r * 0.75)
        fs(ctx, None, lw=4)
        rot = t * 6 if moving else 0
        for k in range(8):
            a = rot + k * math.pi / 4
            line(ctx, 0, 0, math.cos(a) * r * 0.75, math.sin(a) * r * 0.75, 4)
        circle(ctx, 0, 0, 12)
        fs(ctx, GOLD_D, lw=3)
        ctx.restore()
    # body
    ctx.move_to(-230, -150)
    ctx.curve_to(-240, -330, -150, -380, 0, -380)
    ctx.curve_to(150, -380, 240, -330, 220, -150)
    ctx.curve_to(150, -110, -150, -110, -230, -150)
    g = cairo.LinearGradient(0, -380, 0, -110)
    g.add_color_stop_rgb(0, *GOLD_L)
    g.add_color_stop_rgb(1, *GOLD_D)
    ctx.set_source(g)
    ctx.fill_preserve()
    setc(ctx, INK)
    ctx.set_line_width(7)
    ctx.stroke()
    rrect(ctx, -130, -330, 170, 140, 30)
    fs(ctx, hexc("#9fc4dc"), lw=5)
    if rider:
        ctx.save()
        rrect(ctx, -130, -330, 170, 140, 30)
        ctx.clip()
        rider(ctx)
        ctx.restore()
        rrect(ctx, -130, -330, 170, 140, 30)
        fs(ctx, None, lw=5)
    ctx.move_to(-130, -330)
    ctx.line_to(-100, -330)
    ctx.line_to(-130, -250)
    setc(ctx, WHITE, 0.4)
    ctx.fill()
    imperial_crown(ctx, 0, -400, 0.4)
    for k in (-1, 1):
        circle(ctx, k * 170, -250, 18)
        fs(ctx, CRIMSON, lw=4)
    ctx.restore()


# ====================================================================== characters
def hair_short(color):
    def f(c):
        c.move_to(-98, -30)
        c.curve_to(-100, -140, 100, -146, 99, -34)
        c.curve_to(70, -70, 40, -50, 30, -80)
        c.curve_to(10, -50, -30, -60, -50, -70)
        c.curve_to(-60, -40, -80, -50, -98, -30)
        fs(c, color, lw=LW)
    return f


def hat_bicorne(sideways=True):
    def f(c):
        if sideways:
            c.move_to(-190, -60)
            c.curve_to(-120, -60, -100, -200, 0, -205)
            c.curve_to(100, -200, 120, -60, 190, -60)
            c.curve_to(100, -110, -100, -110, -190, -60)
            fs(c, hexc("#141418"), lw=LW)
            circle(c, 30, -130, 22)
            fs(c, FR_BLUE, lw=3)
            circle(c, 30, -130, 14)
            fs(c, WHITE, lw=0)
            circle(c, 30, -130, 7)
            fs(c, RED, lw=0)
        else:
            c.move_to(-90, -60)
            c.curve_to(-100, -210, 100, -210, 90, -60)
            c.close_path()
            fs(c, hexc("#141418"), lw=LW)
    return f


def hat_bearskin(c):
    c.move_to(-100, -20)
    c.curve_to(-120, -280, 120, -280, 100, -20)
    c.close_path()
    fs(c, hexc("#1a1a1e"), lw=LW)
    rnd = random.Random(1)
    for i in range(14):
        x = rnd.uniform(-80, 80)
        y = rnd.uniform(-220, -40)
        line(c, x, y, x + 6, y + 18, 3, hexc("#3a3a40"))
    c.move_to(80, -180)
    c.curve_to(110, -230, 90, -260, 60, -270)
    setc(c, RED)
    c.set_line_width(12)
    c.stroke()


def laurel_hair(c):
    hair_short(hexc("#3a2a1c"))(c)
    for side in (-1, 1):
        for i in range(5):
            a = -math.pi / 2 + side * (0.5 + i * 0.32)
            leaf(c, math.cos(a) * 100, math.sin(a) * 70 - 20, 0.5, rot=a + side * 1.2)


def crown_hair(c):
    hair_short(hexc("#3a2a1c"))(c)
    imperial_crown(c, 0, -80, 0.55)


def josephine_hair(diadem=True, crown=False):
    def f(c):
        c.move_to(-102, -10)
        c.curve_to(-120, -150, 120, -150, 102, -10)
        c.curve_to(80, -70, -80, -70, -102, -10)
        fs(c, hexc("#2a1a12"), lw=LW)
        for dx in (-90, -60, 60, 90):
            circle(c, dx, -10, 22)
            fs(c, hexc("#2a1a12"), lw=4)
        circle(c, 0, -125, 40)
        fs(c, hexc("#2a1a12"), lw=LW)
        if crown:
            small_crown(c, 0, -110, 0.9)
        elif diadem:
            c.move_to(-70, -80)
            c.curve_to(-30, -112, 30, -112, 70, -80)
            setc(c, GOLD)
            c.set_line_width(10)
            c.stroke()
            circle(c, 0, -104, 9)
            fs(c, hexc("#2b6bd6"), lw=3)
    return f


def sister_hair(color):
    def f(c):
        c.move_to(-102, -10)
        c.curve_to(-120, -150, 120, -150, 102, -10)
        c.curve_to(80, -70, -80, -70, -102, -10)
        fs(c, color, lw=LW)
        circle(c, 30, -128, 36)
        fs(c, color, lw=LW)
        line(c, -40, -96, 50, -104, 6, hexc("#f0d8e0"))
    return f


def mitre(color=WHITE, trim=GOLD):
    def f(c):
        c.move_to(-80, -60)
        c.line_to(-70, -170)
        c.line_to(0, -250)
        c.line_to(70, -170)
        c.line_to(80, -60)
        c.close_path()
        fs(c, color, lw=LW)
        line(c, 0, -240, 0, -64, 14, trim)
        line(c, -78, -80, 78, -80, 14, trim)
    return f


def painter_hair(c):
    c.move_to(-104, 0)
    for k in range(9):
        a = math.pi + k * math.pi / 8
        c.line_to(math.cos(a) * 118, math.sin(a) * 110 - 20)
    c.line_to(104, 0)
    c.curve_to(70, -70, -70, -70, -104, 0)
    fs(c, hexc("#8a8a90"), lw=LW)


def bald(c):
    for sx in (-1, 1):
        ellipse(c, sx * 96, -10, 16, 34)
        fs(c, hexc("#9a8a7a"), lw=4)


def top_hat(c):
    c.rectangle(-70, -230, 140, 170)
    fs(c, hexc("#222228"), lw=LW)
    ellipse(c, 0, -62, 130, 22)
    fs(c, hexc("#222228"), lw=LW)


def bonnet(color):
    def f(c):
        c.move_to(-120, 20)
        c.curve_to(-140, -170, 140, -170, 120, 20)
        c.curve_to(80, -70, -80, -70, -120, 20)
        fs(c, color, lw=LW)
    return f


def combo(*fs_):
    def f(c):
        for g in fs_:
            g(c)
    return f


def ermine(c, part, *a):
    if part == "body":
        c.move_to(-60, 70)
        c.curve_to(-70, 150, 70, 150, 60, 70)
        c.close_path()
        fs(c, WHITE, lw=5)
        rnd = random.Random(2)
        for i in range(10):
            x, y = rnd.uniform(-50, 50), rnd.uniform(85, 135)
            ellipse(c, x, y, 3, 7)
            fs(c, INK, lw=0)
        for i in range(6):
            circle(c, -30 + (i % 3) * 30, 190 + (i // 3) * 50, 9)
            fs(c, GOLD, lw=2)


def guy(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t))
    return doodle(ctx, x, y, s, **kw)


def napoleon(ctx, x, y, s, t, head="laurel", **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 1))
    kw.setdefault("body", CRIMSON)
    h = {"laurel": laurel_hair, "crown": crown_hair, "bicorne": combo(hair_short(hexc("#3a2a1c")), hat_bicorne()),
         "bare": hair_short(hexc("#3a2a1c"))}[head]
    return doodle(ctx, x, y, s, hair=h, cap=False, extra=ermine, **kw)


def josephine(ctx, x, y, s, t, crown=False, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 2))
    kw.setdefault("body", hexc("#f6f0e4"))

    def dress(c, part, *a):
        if part == "body":
            line(c, -60, 120, 60, 120, 10, GOLD)
            line(c, -66, 300, 66, 300, 10, GOLD)
    return doodle(ctx, x, y, s, hair=josephine_hair(crown=crown), cap=False, extra=dress, blush=True, **kw)


def sister(ctx, x, y, s, t, seed=0, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 3 + seed))
    kw.setdefault("body", [hexc("#e8b8c8"), hexc("#b8cce8"), hexc("#d8e0b0")][seed % 3])
    return doodle(ctx, x, y, s, hair=sister_hair([hexc("#5a3a22"), hexc("#c9a04a"), hexc("#3a2a1c")][seed % 3]),
                  cap=False, **kw)


def pope(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 5))
    kw.setdefault("body", hexc("#f4f2ea"))

    def stole(c, part, *a):
        if part == "body":
            line(c, -24, 80, -30, 320, 18, GOLD)
            line(c, 24, 80, 30, 320, 18, GOLD)
    return doodle(ctx, x, y, s, hair=mitre(), cap=False, extra=stole, **kw)


def bishop(ctx, x, y, s, t, seed=0, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 6 + seed))
    kw.setdefault("body", hexc("#6a2a6a"))
    return doodle(ctx, x, y, s, hair=mitre(WHITE, hexc("#c9a040")), cap=False, **kw)


def david(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 7))
    kw.setdefault("body", hexc("#2a2a3a"))
    return doodle(ctx, x, y, s, hair=painter_hair, cap=False, **kw)


def goldsmith(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 8))
    kw.setdefault("body", hexc("#8a6a4a"))

    def apron(c, part, *a):
        if part == "body":
            rrect(c, -50, 140, 100, 180, 14)
            fs(c, hexc("#5a4030"), lw=4)
    return doodle(ctx, x, y, s, hair=bald, cap=False, extra=apron, **kw)


def grenadier(ctx, x, y, s, t, seed=0, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, seed))
    kw.setdefault("body", FR_BLUE)

    def belts(c, part, *a):
        if part == "body":
            line(c, -50, 90, 50, 260, 10, WHITE)
            line(c, 50, 90, -50, 260, 10, WHITE)
    return doodle(ctx, x, y, s, hair=hat_bearskin, cap=False, extra=belts, **kw)


def citizen(ctx, x, y, s, t, seed=0, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, seed))
    rnd = random.Random(seed)
    kw.setdefault("body", [hexc("#5a6a8a"), hexc("#8a5a4a"), hexc("#6a7a5a"), hexc("#a08a6a")][seed % 4])
    h = [top_hat, bonnet(hexc("#e8d8b8")), hat_bicorne(False), bonnet(hexc("#c8a8d8"))][seed % 4]
    return doodle(ctx, x, y, s, hair=h, cap=False, **kw)


# ====================================================================== backgrounds
def cathedral_bg(ctx, t, dim=0.0, crack=0.0):
    """inside Notre-Dame, nave facing the altar."""
    vgrad(ctx, -1000, -800, 4000, 2400, hexc("#3a3048"), hexc("#6a5a5a"))
    # rose window
    rx, ry = 960, 180
    warm_glow(ctx, rx, ry, 420, 0.4, (1, 0.7, 0.9))
    circle(ctx, rx, ry, 190)
    fs(ctx, hexc("#2a2244"), lw=8)
    for k in range(16):
        a = k * math.pi / 8 + t * 0.02
        c = [hexc("#3a6ad6"), hexc("#d63a5a"), hexc("#e8b83a"), hexc("#3ab86a")][k % 4]
        ctx.move_to(rx, ry)
        ctx.arc(rx, ry, 175, a, a + math.pi / 8 - 0.04)
        ctx.close_path()
        setc(ctx, c, 0.85)
        ctx.fill()
    circle(ctx, rx, ry, 60)
    fs(ctx, hexc("#e8b83a"), lw=5)
    for k in range(16):
        a = k * math.pi / 8
        line(ctx, rx + math.cos(a) * 60, ry + math.sin(a) * 60, rx + math.cos(a) * 185, ry + math.sin(a) * 185, 5)
    # gothic columns + arches
    for i, cx in enumerate((-300, 120, 520, 1400, 1800, 2220)):
        ctx.rectangle(cx - 60, 0, 120, 1100)
        fs(ctx, STONE, lw=6)
        for k in (-30, 0, 30):
            line(ctx, cx + k, 10, cx + k, 1080, 3, STONE_D)
    for a0, a1 in ((-300, 120), (120, 520), (1400, 1800), (1800, 2220)):
        ctx.move_to(a0 + 60, 450)
        ctx.curve_to(a0 + 60, 150, (a0 + a1) / 2, 60, (a0 + a1) / 2, 40)
        ctx.curve_to((a0 + a1) / 2, 60, a1 - 60, 150, a1 - 60, 450)
        setc(ctx, STONE)
        ctx.set_line_width(40)
        ctx.stroke_preserve()
        setc(ctx, INK)
        ctx.set_line_width(4)
        ctx.stroke()
    # banners with N and bees
    for bx in (320, 1600):
        poly(ctx, [(bx - 90, 260), (bx + 90, 260), (bx + 90, 620), (bx, 680), (bx - 90, 620)])
        fs(ctx, hexc("#1f5a3a"), lw=6)
        text(ctx, "N", bx, 400, 120, GOLD, outline=4)
        for k in range(3):
            bee(ctx, bx - 50 + k * 50, 560, 0.5)
    # painted canvas decoration panel (with a crack behind)
    if crack > 0:
        ctx.save()
        ctx.rectangle(1120, 520, 200, 260)
        fs(ctx, hexc("#e8dcc0"), lw=4)
        ctx.rectangle(1120, 520, 200, 260)
        fs(ctx, STONE_D, lw=4)
        ctx.move_to(1150, 520)
        ctx.line_to(1200, 620)
        ctx.line_to(1160, 690)
        ctx.line_to(1230, 780)
        setc(ctx, INK)
        ctx.set_line_width(9)
        ctx.stroke()
        ctx.move_to(1200, 620)
        ctx.line_to(1260, 650)
        ctx.stroke()
        for k in range(4):
            stone_x, stone_y = 1140 + k * 45, 760 - (k % 2) * 10
            ellipse(ctx, stone_x, stone_y, 16, 10)
            fs(ctx, hexc("#8a7e68"), lw=3)
        ctx.restore()
    # altar + steps
    ctx.rectangle(-1000, 760, 4000, 600)
    fs(ctx, hexc("#7a6a5a"), lw=6)
    for k in range(3):
        ctx.rectangle(700 - k * 60, 700 + k * 30, 520 + k * 120, 30)
        fs(ctx, MARBLE_D, lw=4)
    ctx.rectangle(820, 600, 280, 100)
    fs(ctx, MARBLE, lw=6)
    ctx.rectangle(820, 600, 280, 26)
    fs(ctx, GOLD, lw=4)
    for k in range(4):
        cxp = 840 + k * 80
        line(ctx, cxp, 600, cxp, 540, 8, GOLD)
        ellipse(ctx, cxp, 530, 7, 14)
        setc(ctx, (1, 0.85, 0.4))
        ctx.fill()
        warm_glow(ctx, cxp, 525, 60, 0.4)
    # red carpet aisle
    poly(ctx, [(880, 760), (1040, 760), (1400, 1100), (520, 1100)])
    fs(ctx, CRIMSON, lw=5)
    line(ctx, 880, 760, 520, 1100, 8, GOLD)
    line(ctx, 1040, 760, 1400, 1100, 8, GOLD)
    if dim > 0:
        setc(ctx, (0.05, 0.03, 0.08), dim)
        ctx.paint()


def bee(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for sx in (-1, 1):
        ellipse(ctx, sx * 18, -14, 16, 10)
        fs(ctx, GOLD_L, lw=3)
    ellipse(ctx, 0, 0, 12, 22)
    fs(ctx, GOLD, lw=3)
    ctx.restore()


def crowd_stands(ctx, t, y0=520, gasp=0.0, seed=1, n=16, x0=-200, x1=2100, s=0.32):
    rnd = random.Random(seed)
    for row in range(2):
        for i in range(n):
            x = x0 + (i + 0.5 * row) * (x1 - x0) / n
            y = y0 + row * 110
            expr = "o" if gasp > 0.5 else ["smile", "flat", "smile"][(i + row) % 3]
            bob = math.sin(t * 2 + i) * 3
            citizen(ctx, x, y + bob, s, t, seed=i + row * 7 + seed, face=rnd.uniform(-0.3, 0.3),
                    expr=expr, look=(0, -1) if gasp > 0.5 else (0, 0), larm=(0.3, 0.2),
                    rarm=(-0.3, -0.2) if gasp < 0.5 else (-2.6, 0.4), show_legs=False)


def paris_bg(ctx, t, night=False):
    vgrad(ctx, -1000, -800, 4000, 2000, hexc("#9fb2c4"), hexc("#e2e4e0"))
    # Notre-Dame facade in the distance
    nd_facade(ctx, 1380, 640, 0.55)
    # Parisian houses
    for i, hx in enumerate(range(-700, 2700, 260)):
        if 1050 < hx < 1650:
            continue
        hh = 380 + (i * 53) % 140
        ctx.rectangle(hx, 820 - hh, 240, hh)
        fs(ctx, [hexc("#e8dcc4"), hexc("#d8c8a8"), hexc("#efe4cf")][i % 3], lw=6)
        poly(ctx, [(hx - 10, 820 - hh), (hx + 20, 820 - hh - 70), (hx + 220, 820 - hh - 70), (hx + 250, 820 - hh)])
        fs(ctx, hexc("#5a6a7a"), lw=6)
        for r in range(int(hh / 110)):
            for c in range(3):
                rrect(ctx, hx + 25 + c * 72, 820 - hh + 30 + r * 105, 46, 70, 6)
                fs(ctx, hexc("#4a5a6a"), lw=4)
                line(ctx, hx + 20 + c * 72, 820 - hh + 104 + r * 105, hx + 76 + c * 72, 820 - hh + 104 + r * 105,
                     4, hexc("#2a2a30"))
        ctx.rectangle(hx + 200, 820 - hh - 110, 26, 50)
        fs(ctx, hexc("#9a6a5a"), lw=4)
    ctx.rectangle(-1000, 820, 4000, 600)
    fs(ctx, hexc("#9a948a"), lw=6)
    for k in range(-1000, 3000, 70):
        line(ctx, k, 820, k - 40, 1100, 2, hexc("#7a7468"))


def nd_facade(ctx, x, y, s):
    """Notre-Dame west facade, base centre at (x, y)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    c = hexc("#d8ccb2")
    for tx in (-260, 260):
        ctx.rectangle(tx - 150, -900, 300, 900)
        fs(ctx, c, lw=7)
        for k in range(2):
            rrect(ctx, tx - 100 + k * 120, -840, 80, 230, 40)
            fs(ctx, hexc("#4a4a5a"), lw=5)
        ctx.rectangle(tx - 160, -920, 320, 30)
        fs(ctx, c, lw=6)
    ctx.rectangle(-110, -700, 220, 700)
    fs(ctx, c, lw=7)
    circle(ctx, 0, -560, 90)
    fs(ctx, hexc("#6a4a7a"), lw=6)
    for k in range(12):
        a = k * math.pi / 6
        line(ctx, math.cos(a) * 25, -560 + math.sin(a) * 25, math.cos(a) * 85, -560 + math.sin(a) * 85, 4)
    ctx.rectangle(-410, -380, 820, 40)
    fs(ctx, hexc("#c8bca2"), lw=5)
    for k, px in enumerate((-260, 0, 260)):
        ctx.new_sub_path()
        ctx.move_to(px - 80, 0)
        ctx.line_to(px - 80, -170)
        ctx.curve_to(px - 80, -260, px, -290, px, -290)
        ctx.curve_to(px, -290, px + 80, -260, px + 80, -170)
        ctx.line_to(px + 80, 0)
        ctx.close_path()
        fs(ctx, hexc("#5a4a3a"), lw=6)
    ctx.restore()


def museum_bg(ctx, t, painting_cap=0.0):
    vgrad(ctx, -800, -400, 3600, 1600, hexc("#2f2a3a"), hexc("#4a3f4f"))
    vgrad(ctx, -800, 760, 3600, 600, hexc("#7a5132"), hexc("#5a3a22"))
    for i in range(-6, 40):
        line(ctx, i * 120 - 600, 780, i * 160 - 900, 1500, 3, hexc("#4a3020"), 0.6)
    line(ctx, -800, 780, 2800, 780, 6)
    # spotlights
    for sx in (700, 1450):
        g = cairo.LinearGradient(sx, 0, sx, 760)
        g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.18)
        g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0.0)
        poly(ctx, [(sx - 40, 0), (sx + 40, 0), (sx + 300, 760), (sx - 300, 760)])
        ctx.set_source(g)
        ctx.fill()
    # the big painting
    david_painting(ctx, 160, 80, 1080, 640, t, cap=painting_cap)
    rrect(ctx, 560, 735, 280, 34, 6)
    fs(ctx, hexc("#e8dcb4"), lw=3)
    text(ctx, "J.-L. DAVID · 1805-07", 700, 752, 22, INK, outline=0, shadow=False)
    # banner
    rrect(ctx, 1380, 60, 420, 110, 10)
    fs(ctx, FR_BLUE, lw=6)
    text(ctx, "NAPOLEON", 1590, 105, 64, GOLD, outline=0, shadow=False)
    text(ctx, "the exhibition", 1590, 150, 30, WHITE, font=HAND_FONT, outline=0, shadow=False)


def leaf_case(ctx, x, y, t, glow=0.3, open_=0.0, sign=True):
    ctx.rectangle(x - 130, y + 60, 260, 340)
    fs(ctx, MARBLE, lw=6)
    ctx.rectangle(x - 150, y + 50, 300, 40)
    fs(ctx, MARBLE_D, lw=6)
    ellipse(ctx, x, y + 40, 110, 22)
    fs(ctx, hexc("#1f2a5a"), lw=5)
    if glow > 0:
        warm_glow(ctx, x, y - 20, 200, 0.6 * glow)
    leaf(ctx, x, y - 10, 1.2, rot=0.9, glint=glow)
    ctx.save()
    ctx.translate(0, -open_ * 420)
    ctx.rectangle(x - 140, y - 170, 280, 220)
    setc(ctx, (0.8, 0.95, 1.0), 0.15)
    ctx.fill_preserve()
    setc(ctx, (0.6, 0.7, 0.8), 0.9)
    ctx.set_line_width(5)
    ctx.stroke()
    poly(ctx, [(x - 110, y - 150), (x - 60, y - 150), (x - 120, y + 20), (x - 135, y + 20)])
    setc(ctx, WHITE, 0.3)
    ctx.fill()
    ctx.restore()
    if sign:
        ctx.save()
        ctx.translate(x + 220, y + 160)
        ctx.rotate(0.04)
        rrect(ctx, -115, -75, 230, 150, 10)
        fs(ctx, hexc("#fffaf0"), lw=5)
        text(ctx, "DO NOT", 0, -40, 34, RED, outline=0, shadow=False)
        text(ctx, "TOUCH", 0, -2, 38, RED, outline=0, shadow=False)
        text(ctx, "leaf from the crown", 0, 40, 28, INK, font=HAND_FONT, outline=0, shadow=False)
        line(ctx, 0, 75, 0, 230, 8)
        ctx.restore()


def david_painting(ctx, x, y, w, h, t, cap=0.0, frame=True, mother=True):
    """stylised version of David's 'Coronation of Napoleon' inside a gilt frame."""
    if frame:
        frame_box(ctx, x, y, w, h, fill=hexc("#3a2e24"), border=hexc("#c9a040"), bw=30)
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    ctx.translate(x, y)
    ctx.scale(w / 1000, h / 600)
    vgrad(ctx, 0, 0, 1000, 600, hexc("#5a4a3a"), hexc("#2a2018"))
    # architecture
    for cx in (80, 260, 740, 920):
        ctx.rectangle(cx - 30, 0, 60, 420)
        setc(ctx, hexc("#8a7a62"))
        ctx.fill()
    ctx.move_to(260, 200)
    ctx.curve_to(260, 60, 740, 60, 740, 200)
    setc(ctx, hexc("#7a6a52"))
    ctx.set_line_width(30)
    ctx.stroke()
    # gallery box with Madame Mère
    ctx.rectangle(380, 150, 240, 90)
    setc(ctx, hexc("#4a3a2a"))
    ctx.fill()
    if mother:
        for k in range(5):
            circle(ctx, 410 + k * 45, 185, 14)
            setc(ctx, hexc("#e8d0b0") if k != 2 else hexc("#f2dcc0"))
            ctx.fill()
            ctx.rectangle(400 + k * 45, 200, 22, 34)
            setc(ctx, hexc("#3a2a2a") if k != 2 else hexc("#6a2a3a"))
            ctx.fill()
    # floor + carpet
    ctx.rectangle(0, 420, 1000, 180)
    setc(ctx, hexc("#4a3426"))
    ctx.fill()
    # crowd of dignitaries on the left
    rnd = random.Random(3)
    for k in range(14):
        px = 30 + k * 26 + rnd.uniform(-5, 5)
        py = 330 + (k % 3) * 18
        circle(ctx, px, py, 11)
        setc(ctx, hexc("#e2c8a8"))
        ctx.fill()
        ctx.rectangle(px - 11, py + 10, 22, 70)
        setc(ctx, [hexc("#7a1a1a"), hexc("#1a1a2a"), hexc("#d8c8a8"), hexc("#3a2a4a")][k % 4])
        ctx.fill()
    # pope + bishops on the right
    for k, (px, col) in enumerate(((800, hexc("#f2ede0")), (860, hexc("#e8e0d0")), (910, hexc("#d8c8a8")))):
        circle(ctx, px, 300 + k * 6, 13)
        setc(ctx, hexc("#e2c8a8"))
        ctx.fill()
        poly(ctx, [(px - 10, 290 + k * 6), (px, 262 + k * 6), (px + 10, 290 + k * 6)])
        setc(ctx, WHITE)
        ctx.fill()
        ctx.rectangle(px - 16, 312 + k * 6, 32, 100)
        setc(ctx, col)
        ctx.fill()
    # the red-cap guy peeking out between the bishops
    if cap > 0:
        ctx.save()
        ctx.translate(885, 300)
        ctx.scale(0.13, 0.13)
        circle(ctx, 0, 0, 100)
        setc(ctx, hexc("#f2f0ea"))
        ctx.fill()
        for ex in (-25, 35):
            circle(ctx, ex, -15, 12)
            setc(ctx, INK)
            ctx.fill()
        draw_cap(ctx)
        ctx.restore()
    # Napoleon standing, raising the crown
    circle(ctx, 640, 300, 16)
    setc(ctx, hexc("#e2c8a8"))
    ctx.fill()
    ctx.move_to(615, 320)
    ctx.line_to(665, 320)
    ctx.line_to(700, 470)
    ctx.line_to(580, 470)
    ctx.close_path()
    setc(ctx, CRIMSON)
    ctx.fill()
    ctx.move_to(625, 320)
    ctx.curve_to(600, 360, 560, 420, 520, 470)
    setc(ctx, hexc("#f2ede0"))
    ctx.set_line_width(14)
    ctx.stroke()
    line(ctx, 655, 330, 690, 270, 9, CRIMSON)
    circle(ctx, 694, 262, 9)
    setc(ctx, GOLD)
    ctx.fill()
    # Josephine kneeling
    circle(ctx, 560, 380, 14)
    setc(ctx, hexc("#e8d0b0"))
    ctx.fill()
    ctx.move_to(540, 395)
    ctx.line_to(580, 395)
    ctx.line_to(600, 460)
    ctx.line_to(520, 460)
    ctx.close_path()
    setc(ctx, hexc("#f2ede0"))
    ctx.fill()
    ctx.move_to(520, 450)
    ctx.curve_to(450, 470, 380, 490, 300, 500)
    setc(ctx, CRIMSON)
    ctx.set_line_width(26)
    ctx.stroke()
    # varnish glow
    g = cairo.RadialGradient(620, 330, 40, 620, 330, 500)
    g.add_color_stop_rgba(0, 1, 0.9, 0.6, 0.25)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.3)
    ctx.set_source(g)
    ctx.rectangle(0, 0, 1000, 600)
    ctx.fill()
    ctx.restore()


def oil_paint_overlay(ctx, k):
    """turns the current frame into a warm, varnished canvas look (k=0..1)."""
    if k <= 0:
        return
    setc(ctx, (0.55, 0.4, 0.2), 0.35 * k)
    ctx.paint()
    rnd = random.Random(4)
    for i in range(220):
        x, y = rnd.random() * W, rnd.random() * H
        a = rnd.random() * math.pi
        line(ctx, x, y, x + math.cos(a) * 30, y + math.sin(a) * 30, 3, (0.2, 0.12, 0.05), 0.12 * k)
    for y in range(0, H, 9):
        line(ctx, 0, y, W, y, 1, (0, 0, 0), 0.05 * k)


# ====================================================================== SHOTS
def hook_scene(ctx, t, D, cue, freeze_at=None):
    t_nd = cue("Notre Dame Cathedral")
    t_thou = cue("Thousands")
    t_crown = cue("That golden crown")
    t_supp = cue("It's supposed")
    t_hands = cue("In my hands")
    t_angry = cue("And the angry")
    t_nap = cue("That's Napoleon")
    t_story = cue("This is the story")
    tt = t if freeze_at is None else min(t, freeze_at)
    # crown position: slow-motion arc
    cx_c, cy_c = lerp(900, 1060, ease(prog(tt, 0, D))), lerp(330, 300, ease(prog(tt, 0, D)))
    crot = 0.15 * math.sin(tt * 0.6) + tt * 0.08
    # camera beats
    if tt < t_nd:
        cx, cy, z = cx_c, cy_c, lerp(3.4, 2.6, ease(prog(tt, 0, t_nd)))
    elif tt < t_supp:
        k = ease(prog(tt, t_nd, t_nd + 2.2))
        cx, cy, z = lerp(cx_c, 960, k), lerp(cy_c, 520, k), lerp(2.6, 0.95, k)
    elif tt < t_angry:
        k = ease(prog(tt, t_supp, t_supp + 0.8))
        cx, cy, z = lerp(960, 760, k), lerp(520, 640, k), lerp(0.95, 1.9, k)
    elif tt < t_story:
        k = ease(prog(tt, t_angry, t_angry + 0.8))
        cx, cy, z = lerp(760, 1180, k), lerp(640, 520, k), lerp(1.9, 1.6, k)
    else:
        k = ease(prog(tt, t_story, t_story + 1.5))
        cx, cy, z = lerp(1180, 960, k), lerp(520, 520, k), lerp(1.6, 1.0, k)
    ctx.save()
    cam(ctx, cx, cy, z, shake=2 if tt < 1.0 else 0, t=tt)
    cathedral_bg(ctx, tt, dim=0.25)
    crowd_stands(ctx, tt, y0=560, gasp=1.0 if tt > t_thou else 0.0, x0=-300, x1=780, n=8, s=0.3)
    crowd_stands(ctx, tt, y0=560, gasp=1.0 if tt > t_thou else 0.0, x0=1180, x1=2300, n=8, s=0.3, seed=5)
    pope(ctx, 1320, 540, 0.42, tt, face=-0.7, expr="shock", larm=(0.3, 0.2), rarm=(-1.6, 0.6))
    reach = ease(prog(tt, t_angry - 1, t_angry + 0.6))
    napoleon(ctx, 1110, 520, 0.6, tt, head="laurel", face=-0.3, look=(-0.3, -1), expr="frown",
             brows="angry", larm=(0.3, 0.2), rarm=(lerp(-0.4, -2.75, reach), lerp(0, -0.2, reach)))
    guy(ctx, 760, 600, 0.55, tt, expr="shock", face=0.4, look=(0.5, -1), brows="worried",
        larm=(1.3, -0.4), rarm=(-1.3, 0.4))
    cushion(ctx, 760, 700, 0.6)
    if tt > t_supp and tt < t_angry:
        a = ease(prog(tt, t_supp, t_supp + 0.3))
        ctx.save()
        ellipse(ctx, 760, 690, 90, 34)
        setc(ctx, GOLD, a)
        ctx.set_line_width(6)
        ctx.set_dash([18, 10])
        ctx.stroke()
        ctx.restore()
    # the crown, slow motion, with trail
    for k in range(5):
        ctx.save()
        ctx.push_group()
        imperial_crown(ctx, cx_c - (k + 1) * 6, cy_c + (k + 1) * 14, 0.5, rot=crot - (k + 1) * 0.03)
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(0.08 * (5 - k))
        ctx.restore()
    imperial_crown(ctx, cx_c, cy_c, 0.5, rot=crot, glow=1.0)
    for k in range(5):
        sparkle(ctx, cx_c + math.cos(k * 1.3 + tt) * 120, cy_c - 40 + math.sin(k * 1.7 + tt) * 80, 18, tt * 2 + k)
    ctx.restore()
    vignette(ctx, 0.55)


def sh_hook(ctx, t, D, cue):
    t_dec = cue("December")
    t_nd = cue("Notre Dame Cathedral")
    t_thou = cue("Thousands")
    t_crown = cue("That golden crown")
    t_hands = cue("In my hands")
    t_angry = cue("And the angry")
    t_nap = cue("That's Napoleon")
    t_story = cue("This is the story")
    frozen = t > t_nap + 0.3
    hook_scene(ctx, t, D, cue, freeze_at=t_nap + 0.3 if frozen else None)
    if frozen:
        setc(ctx, (0.1, 0.05, 0.1), 0.25)
        ctx.paint()
    # slow-motion badge
    if t < t_nap:
        a = 0.6 + 0.4 * math.sin(t * 4)
        circle(ctx, 1790, 70, 12)
        setc(ctx, RED, a)
        ctx.fill()
        text(ctx, "SLOW MOTION", 1600, 72, 34, WHITE, align="left", outline=0, shadow=False, alpha=0.85)
        text(ctx, "x0.05", 1600, 112, 28, WHITE, font=HAND_FONT, align="left", outline=0, shadow=False, alpha=0.7)
    if t > t_dec:
        pop_text(ctx, "PARIS · 2 DECEMBER 1804", 960, 960, 72, t - t_dec, GOLD, hold=t_thou - t_dec)
    if t > t_crown:
        pop_text(ctx, "THE CROWN", 1300, 160, 80, t - t_crown - 0.3, GOLD, hold=t_hands - t_crown - 0.6)
    if t > t_hands:
        pop_text(ctx, "(MY JOB.)", 760, 980, 80, t - t_hands, WHITE, hold=t_angry - t_hands)
    if t > t_nap:
        k = ease_out(prog(t, t_nap + 0.3, t_nap + 0.7))
        setc(ctx, GOLD)
        ctx.set_line_width(12)
        ctx.move_to(1560, 200)
        ctx.curve_to(1520, 300, 1450, 340, lerp(1560, 1330, k), lerp(200, 380, k))
        ctx.stroke()
        pop_text(ctx, "NAPOLEON BONAPARTE", 1460, 150, 80, t - t_nap - 0.3, WHITE, rot=0.04, hold=t_story - t_nap)
    if t > t_story:
        pop_text(ctx, "HOW I RUINED HIS CORONATION", 960, 980, 84, t - t_story - 0.4, RED)


def sh_backup(ctx, t, D, cue):
    hs, hc = TIMELINE["hook"]
    k_paint = ease(prog(t, 0, 0.5))
    k = ease(prog(t, 0.3, D - 0.2))
    museum_bg(ctx, t)
    guy(ctx, 1500, lerp(1400, 560, k), 0.7, t, expr="o", face=-0.6, look=(-1, -1),
        larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    # the frozen cold-open frame shrinks exactly into David's painting on the wall
    zx, zy = lerp(1.0, 1080 / W, k), lerp(1.0, 640 / H, k)
    ctx.save()
    ctx.translate(lerp(0, 160, k), lerp(0, 80, k))
    ctx.scale(zx, zy)
    ctx.rectangle(0, 0, W, H)
    ctx.clip()
    ctx.push_group()
    hook_scene(ctx, hs["D"], hs["D"], hc, freeze_at=hc("That's Napoleon") + 0.3)
    oil_paint_overlay(ctx, k_paint)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(1 - 0.85 * ease(prog(t, D - 0.6, D)))
    ctx.restore()
    pop_text(ctx, "LET ME BACK UP...", 960, 980, 80, t - 0.3, WHITE)


def sh_title(ctx, t, D, cue):
    # imperial blue background with gold bees
    vgrad(ctx, 0, 0, W, H, hexc("#1a2a5a"), hexc("#0e1636"))
    for i in range(40):
        rnd = random.Random(i)
        x = (rnd.random() * W + t * 20 * (0.5 + rnd.random())) % W
        y = rnd.random() * H
        bee(ctx, x, y, 0.5 + rnd.random() * 0.5)
    spiral_bg  # noqa

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
    row([("HOW", WHITE), ("I", WHITE), ("ACCIDENTALLY", WHITE)], 280, 110, 0.15)
    row([("RUINED", RED), ("NAPOLEON'S", GOLD)], 450, 150, 0.5)
    row([("CORONATION", GOLD)], 630, 170, 0.9)
    k = ease_out(prog(t, 1.2, 1.8))
    if k > 0:
        guy(ctx, 1700, lerp(1500, 820, k), 0.7, t, expr="grin", face=-0.3, larm=(2.6, -0.3), rarm=(-0.3, 0))
        imperial_crown(ctx, 1640, lerp(1200, 640, k), 0.25, rot=-0.3)
    text(ctx, "HISTORY WORLD", W / 2, 1000, 48, WHITE, font=HAND_FONT, outline=6, alpha=ease(prog(t, 1.5, 2.2)))


def sh_museum(ctx, t, D, cue):
    t_real = cue("The real one")
    t_next = cue("And next to it")
    t_sign = cue("The sign")
    if t < t_next:
        z = lerp(0.95, 1.1, ease(prog(t, 0, t_next)))
        ctx.save()
        cam(ctx, 760, 430, z)
        museum_bg(ctx, t)
        leaf_case(ctx, 1500, 430, t, glow=0.3)
        guy(ctx, 900, 560, 0.7, t, expr="o", face=-0.6, look=(-1, -1), larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        ctx.restore()
        if t > t_real:
            pop_text(ctx, "REAL ONE: ~6 x 10 METRES", 960, 980, 70, t - t_real - 0.3, GOLD)
            text(ctx, "(Louvre, Paris)", 960, 1045, 40, WHITE, font=HAND_FONT, outline=5,
                 alpha=ease(prog(t, t_real + 1, t_real + 1.4)))
    else:
        tt = t - t_next
        ctx.save()
        cam(ctx, lerp(1300, 1480, ease(prog(tt, 0, 2))), lerp(480, 440, ease(prog(tt, 0, 2))),
            lerp(1.1, 1.6, ease(prog(t, t_sign - 0.3, t_sign + 1))))
        museum_bg(ctx, t)
        leaf_case(ctx, 1500, 430, t, glow=0.4 + 0.3 * math.sin(t * 3))
        guy(ctx, 1220, 560, 0.7, t, expr="smile" if t < t_sign else "sly", face=0.9, look=(1, -0.3),
            larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        ctx.restore()
    vignette(ctx, 0.4)


def sh_touch(ctx, t, D, cue):
    ctx.save()
    cam(ctx, 1420, 430, lerp(1.7, 2.1, ease(prog(t, 0, D))))
    museum_bg(ctx, t)
    leaf_case(ctx, 1500, 430, t, glow=0.4 + 0.6 * ease(prog(t, D * 0.6, D)), open_=ease(prog(t, 0.1, 0.6)))
    reach = ease(prog(t, D * 0.3, D * 0.75))
    guy(ctx, 1300, 400, 1.0, t, expr="sly" if t < D * 0.5 else "grin", face=0.9, look=(1, 0.5),
        larm=(0.3, 0.2), rarm=(lerp(-0.3, -2.1, reach), lerp(-0.2, 0.0, reach)))
    ctx.restore()
    vignette(ctx, 0.45)


def sh_tunnel(y0, y1, hue=(0.15, 0.2, 0.6), hue2=(1.0, 0.85, 0.35)):
    def f(ctx, t, D, cue):
        vortex(ctx, t, hue, hue2, speed=2.0)
        rnd = random.Random(5)
        for i in range(12):
            ph = (t * 0.35 + i / 12) % 1
            a = rnd.random() * 6.28 + t * 0.3
            r = 60 + ph ** 2 * 1300
            px, py = W / 2 + math.cos(a) * r, H / 2 + math.sin(a) * r * 0.7
            if i % 3 == 0:
                leaf(ctx, px, py, 0.3 + ph * 1.5, rot=t * 2 + i)
            elif i % 3 == 1:
                bee(ctx, px, py, 0.5 + ph * 2)
            else:
                clock_icon(ctx, px, py, 10 + ph * 70, t, back=y1 < y0, rot=t + i)
        ctx.save()
        ctx.translate(W / 2 + 260 * math.sin(t * 0.9), H / 2 + 120 * math.cos(t * 1.3) - 60)
        ctx.rotate(t * 2.5)
        doodle(ctx, 0, -150, 0.6, expr="shock", face=0, larm=(2.4, 0.5), rarm=(-2.4, -0.5), legs=(0.5, -0.5))
        ctx.restore()
        year_counter(ctx, t, D, y0, y1)
        vignette(ctx, 0.6)
    return f


def sh_arrive(ctx, t, D, cue):
    t_sold = cue("Soldiers.")
    t_vive = cue("Everyone was shouting")
    land = ease_in(prog(t, 0.1, 0.7))
    ctx.save()
    cam(ctx, lerp(700, 960, ease(prog(t, 0, D))), 520, lerp(1.2, 1.0, ease(prog(t, 0, D))))
    paris_bg(ctx, t)
    for i in range(5):
        flag_fr(ctx, 120 + i * 420, 330 + (i % 2) * 40, 0.8, t, ph=i)
    # crowd + soldiers
    for i in range(10):
        citizen(ctx, -200 + i * 230, 700, 0.42, t, seed=i, face=0.2, expr="grin" if t > t_vive else "smile",
                larm=(0.3, 0.2), rarm=(-2.6 + 0.3 * math.sin(t * 6 + i), 0.3) if t > t_vive else (-0.3, -0.2),
                show_legs=False)
    if t > t_sold - 0.3:
        for i in range(4):
            gx = lerp(2200, 1100, ease(prog(t, t_sold - 0.3, t_sold + 2))) + i * 170
            grenadier(ctx, gx, 600, 0.5, t, seed=i, face=-0.9, walk=t * 1.6 + i * 0.25, expr="flat",
                      larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    gx, gy = 980, lerp(-300, 620, land)
    sq = -0.18 * math.exp(-max(0, t - 0.7) * 6) if t > 0.7 else 0
    guy(ctx, gx, gy, 0.6, t, expr="shock" if t < t_sold else "o", face=0.6, squash=sq,
        larm=(-0.9, 1.9), rarm=(0.9, -1.9), tilt=0.03 * math.sin(t * 30))
    ctx.restore()
    snow(ctx, t)
    if t > t_vive:
        pop_text(ctx, "VIVE L'EMPEREUR!", 960, 160, 110, t - t_vive, GOLD, rot=-0.03)
    caption(ctx, "PARIS, FRANCE", "2 DECEMBER 1804", t - 0.8, dur=5)
    vignette(ctx, 0.35)


def sh_context(ctx, t, D, cue):
    t_rev = cue("A few years")
    t_now = cue("Now a young")
    t_pope = cue("Even the Pope")
    paper_bg(ctx)
    pop_text(ctx, "QUICK HISTORY LESSON", 960, 90, 70, t - 0.2, INK, outline=0)
    if t < t_now:
        # the revolution: a king's crown tumbling, 1789
        k = ease(prog(t, t_rev + 0.8, t_rev + 2.5))
        ctx.save()
        ctx.translate(960, lerp(380, 820, ease_in(k)))
        ctx.rotate(k * 2.4)
        imperial_crown(ctx, 0, 0, 0.8)
        ctx.restore()
        pop_text(ctx, "1789: REVOLUTION", 960, 260, 90, t - t_rev, RED, outline=8)
        text(ctx, "France gets rid of its king", 960, 960, 50, INK, font=HAND_FONT, outline=0, shadow=False,
             alpha=ease(prog(t, t_rev + 1.2, t_rev + 1.6)))
    else:
        tt = t - t_now
        k = ease_out(prog(tt, 0, 0.6))
        napoleon(ctx, 620, lerp(1400, 470, k), 0.85, t, head="bicorne", body=FR_BLUE, face=0.6, expr="smile",
                 larm=(0.3, 0.2), rarm=(-1.3, 1.6))
        pop_text(ctx, "NAPOLEON BONAPARTE", 1250, 300, 72, tt - 0.4, FR_BLUE, outline=6)
        text(ctx, "general from Corsica · age 35", 1250, 380, 48, INK, font=HAND_FONT, outline=0, shadow=False,
             alpha=ease(prog(tt, 1.0, 1.4)))
        if t > cue("Now a young", frac=0.7):
            pop_text(ctx, "EMPEROR OF THE FRENCH", 1250, 520, 70, t - cue("Now a young", frac=0.7), GOLD)
        if t > t_pope:
            kk = ease_out(prog(t, t_pope, t_pope + 0.5))
            pope(ctx, lerp(2200, 1500, kk), 760, 0.5, t, face=-0.8, expr="smile", walk=t * 1.4 if kk < 1 else None,
                 larm=(0.3, 0.2), rarm=(-0.3, -0.2))
            text(ctx, "Pope Pius VII", 1500, 1030, 44, INK, font=HAND_FONT, outline=0, shadow=False, alpha=kk)
            # route Rome -> Paris
            ctx.save()
            ctx.set_dash([18, 12])
            line(ctx, 1150, 900, lerp(1150, 1300, kk), lerp(900, 700, kk), 6, RED)
            ctx.restore()
            text(ctx, "Rome", 1150, 940, 40, INK, font=HAND_FONT, outline=0, shadow=False, alpha=kk)
            text(ctx, "Paris", 1300, 670, 40, INK, font=HAND_FONT, outline=0, shadow=False, alpha=kk)
    vignette(ctx, 0.3)


def workshop_bg(ctx, t):
    vgrad(ctx, -800, -400, 3600, 1600, hexc("#5a4632"), hexc("#3a2a1c"))
    ctx.rectangle(-800, 760, 3600, 600)
    fs(ctx, hexc("#4a3424"), lw=6)
    ctx.rectangle(-200, 600, 2400, 40)
    fs(ctx, hexc("#7a5a3a"), lw=6)
    ctx.rectangle(-200, 640, 2400, 140)
    fs(ctx, hexc("#6a4a2a"), lw=6)
    for k in range(6):
        line(ctx, 100 + k * 300, 380, 100 + k * 300, 600, 6, hexc("#2a1a10"))
    rrect(ctx, 1500, 160, 360, 260, 10)
    fs(ctx, hexc("#9fb6c4"), lw=8)
    line(ctx, 1680, 160, 1680, 420, 6)
    snow_win = random.Random(1)
    warm_glow(ctx, 400, 580, 300, 0.4)


def sh_goldsmith(ctx, t, D, cue):
    t_mb = cue("Martin Biennais")
    t_help = cue("Help me")
    t_wreath = cue("It was a wreath")
    ctx.save()
    cam(ctx, 960, 500, lerp(1.1, 1.25, ease(prog(t, 0, D))))
    paris_bg(ctx, t)
    grab = t > 0.5
    goldsmith(ctx, lerp(1700, 1150, ease_out(prog(t, 0, 0.6))), 560, 0.62, t, face=-0.8,
              expr="worried", brows="worried", larm=(-1.5, 0.3) if grab else (0.3, 0.2), rarm=(-0.3, -0.2))
    guy(ctx, 800, 560, 0.62, t, expr="shock" if t < t_help else "o", face=0.8,
        larm=(0.3, 0.2), rarm=(-1.4, 0.2) if t > t_wreath else (-0.3, -0.2))
    if t > t_wreath - 0.3:
        k = back_out(prog(t, t_wreath - 0.3, t_wreath + 0.2), 1.8)
        ctx.save()
        ctx.translate(980, 600)
        ctx.scale(max(k, 1e-3), max(k, 1e-3))
        warm_glow(ctx, 0, 0, 220, 0.5)
        laurel(ctx, 0, 0, 0.9, t=t)
        ctx.restore()
    ctx.restore()
    snow(ctx, t, n=50)
    if t > t_mb:
        pop_text(ctx, "MARTIN-GUILLAUME BIENNAIS", 960, 120, 70, t - t_mb - 0.3, GOLD, hold=t_wreath - t_mb)
        text(ctx, "the Emperor's goldsmith", 960, 200, 46, WHITE, font=HAND_FONT, outline=5,
             alpha=ease(prog(t, t_mb + 0.8, t_mb + 1.2)) * (1 - prog(t, t_wreath, t_wreath + 0.3)))
    if t > t_help:
        speech(ctx, 1400, 300, 420, 120, "Help me carry this!", 52, tail=(-80, 80),
               alpha=ease(prog(t, t_help, t_help + 0.2)) * (1 - prog(t, t_wreath, t_wreath + 0.3)))
    if t > t_wreath + 1.0:
        pop_text(ctx, "GOLDEN LAUREL WREATH", 960, 980, 80, t - t_wreath - 1.0, GOLD)
    vignette(ctx, 0.35)


def sh_leaves(ctx, t, D, cue):
    t_trip = cue("I tripped")
    t_two = cue("Two golden leaves")
    t_hist = cue("History says")
    t_only = cue("I only broke two")
    if t < t_hist:
        ctx.save()
        cam(ctx, 960, 540, 1.2)
        paris_bg(ctx, t)
        trip = prog(t, t_trip, t_trip + 0.8)
        heavy = t < t_trip
        guy(ctx, lerp(600, 900, ease(prog(t, 0, t_trip))), 560 + 120 * ease_in(trip), 0.62, t,
            expr="worried" if heavy else "shock", face=0.8, tilt=lerp(0.05 * math.sin(t * 8), 1.3, ease_in(trip)),
            walk=t * 1.2 if heavy else None, larm=(1.2, -1.4), rarm=(-1.2, 1.4), brows="worried")
        wx = lerp(lerp(700, 1000, ease(prog(t, 0, t_trip))), 1150, ease(trip))
        wy = 660 - math.sin(trip * math.pi) * 200 + 100 * ease_in(trip)
        laurel(ctx, wx, wy, 0.6, missing=2 if t > t_two else 0, t=t, rot=trip * 2)
        if t > t_two:
            for k in range(2):
                tt = t - t_two
                lx = wx + 40 + k * 30 + tt * 80
                ly = min(wy + tt * 300, 720)
                if ly < 720:
                    leaf(ctx, lx, ly, 0.6, rot=tt * 8 + k)
            pop_text(ctx, "*plink* *plink*", 1300, 360, 60, tt, GOLD, font=HAND_FONT, outline=6, hold=2.0)
        if heavy:
            for k in range(3):
                sweat(ctx, 640 + k * 40, 430, 0.8, t + k)
            pop_text(ctx, "HEAVY!", 900, 250, 80, t - 1.3, WHITE, hold=t_trip - 1.4)
        ctx.restore()
        snow(ctx, t, n=50)
    else:
        tt = t - t_hist
        paper_bg(ctx)
        laurel(ctx, 960, 520, 1.6, missing=int(clamp(tt / 0.4) * 6) if tt < 3 else 6, t=t)
        n = min(6, int(tt / 0.35))
        for k in range(n):
            leaf(ctx, 1500 + (k % 3) * 90, 360 + (k // 3) * 140, 0.9, rot=0.6)
        pop_text(ctx, "6 LEAVES REMOVED", 960, 140, 90, tt - 0.4, RED)
        text(ctx, "the wreath was too heavy", 960, 230, 48, INK, font=HAND_FONT, outline=0, shadow=False,
             alpha=ease(prog(tt, 1.0, 1.4)))
        if t > t_only:
            # 2 mine, 4 not mine
            for k in range(6):
                lx, ly = 1500 + (k % 3) * 90, 360 + (k // 3) * 140
                c = (0.2, 0.7, 0.3) if k < 2 else (0.85, 0.2, 0.2)
                circle(ctx, lx, ly, 50)
                setc(ctx, c, 0.9)
                ctx.set_line_width(6)
                ctx.stroke()
            pop_text(ctx, "2 = ME", 1590, 680, 60, t - t_only, hexc("#2f7a3a"), outline=0)
            pop_text(ctx, "4 = NOT ME!", 1590, 760, 60, t - cue("I'm not taking"), RED, outline=0)
    vignette(ctx, 0.35)


def sh_auction(ctx, t, D, cue):
    t_sold = cue("For six hundred")
    t_one = cue("For one leaf")
    bg_fill(ctx, hexc("#2a1e1a"))
    warm_glow(ctx, 960, 440, 600, 0.35)
    # podium + leaf on a stand
    ctx.rectangle(760, 560, 400, 400)
    fs(ctx, hexc("#5a3a22"), lw=7)
    ctx.rectangle(740, 540, 440, 40)
    fs(ctx, hexc("#7a5a3a"), lw=6)
    leaf(ctx, 960, 420, 2.2, rot=0.7, glint=0.8)
    pop_text(ctx, "AUCTION · 2017", 960, 110, 80, t - 0.3, GOLD)
    # bidders' paddles
    for k in range(4):
        x = 200 + k * 160 if k < 2 else 1500 + (k - 2) * 160
        up = math.sin(t * 3 + k) > 0.2 and t < t_sold
        line(ctx, x, 1000, x, 880 - (60 if up else 0), 8, hexc("#6b4428"))
        circle(ctx, x, 850 - (60 if up else 0), 40)
        fs(ctx, WHITE, lw=5)
        text(ctx, str(12 + k * 7), x, 850 - (60 if up else 0), 36, INK, outline=0, shadow=False)
    # price ticker
    price = int(lerp(50000, 625000, ease(prog(t, 1.5, t_sold + 1.0))))
    rrect(ctx, 610, 620, 700, 140, 20)
    fs(ctx, (0.05, 0.05, 0.08, 0.85), lw=5, stroke=GOLD)
    text(ctx, f"€{price:,}", 960, 690, 90, GOLD, outline=0, shadow=False)
    if t > t_sold + 1.2:
        # gavel
        k = prog(t, t_sold + 1.2, t_sold + 1.4)
        ctx.save()
        ctx.translate(1350, 520)
        ctx.rotate(lerp(-0.8, 0.2, ease_in(k)))
        line(ctx, 0, 0, -160, -40, 14, hexc("#6b4428"))
        rrect(ctx, -220, -80, 80, 80, 10)
        fs(ctx, hexc("#7a4a2a"), lw=6)
        ctx.restore()
        burst(ctx, 960, 900, 140, t - t_sold - 1.35, "SOLD!", size=70, color=(1, 0.85, 0.3))
    if t > t_one:
        pop_text(ctx, "FOR ONE LEAF.", 960, 250, 90, t - t_one, WHITE, rot=-0.03)
    vignette(ctx, 0.45)


def sh_carriage(ctx, t, D, cue):
    t_way = cue("Nobody told me")
    t_short = cue("So I told")
    ctx.save()
    roll = t * 140
    cam(ctx, 1030, 640, 1.1)
    ctx.save()
    ctx.translate(-roll % 260 - 260, 0)
    paris_bg(ctx, t)
    ctx.restore()
    for i in range(6):
        flag_fr(ctx, ((i * 380 - roll * 0.6) % 2600) - 400, 300, 0.7, t, ph=i)

    def rider(c):
        napoleon(c, -45, -250, 0.42, t, head="bare", face=0.4, expr="flat", larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    carriage(ctx, 760, 900, 0.95, t, moving=True, rider=rider)
    # the guy riding on the back as a footman, then whispering to the driver
    pointing = t > t_short
    # coachman sitting at the front of the roof, the guy behind him
    citizen(ctx, 880, 430, 0.36, t, seed=2, face=0.9, expr="flat" if not pointing else "o",
            larm=(1.0, -1.2), rarm=(-1.0, 1.2), show_legs=False)
    guy(ctx, 650 if not pointing else 780, 415, 0.36, t,
        expr="o" if t < t_short else "sly", face=0.8, larm=(0.3, 0.2),
        rarm=(-1.6, 0.0) if pointing else (-2.2, 0.4), show_legs=False)
    ctx.restore()
    pop_text(ctx, "8 HORSES", 1500, 160, 80, t - 1.0, GOLD, hold=t_way - 1.2)
    if t > t_short:
        speech(ctx, 1450, 230, 520, 130, "I know a shortcut!", 58, tail=(-160, 100),
               alpha=ease(prog(t, t_short, t_short + 0.2)))
    vignette(ctx, 0.35)


def sh_late(ctx, t, D, cue):
    t_lost = cue("We got lost")
    t_inside = cue("And inside Notre Dame")
    if t < t_inside:
        # map with a looping route
        paper_bg(ctx, hexc("#efe2c2"))
        # Seine
        ctx.move_to(-50, 640)
        ctx.curve_to(400, 520, 800, 760, 1200, 600)
        ctx.curve_to(1500, 480, 1800, 620, 1980, 560)
        setc(ctx, hexc("#7fb2d6"))
        ctx.set_line_width(70)
        ctx.stroke()
        ellipse(ctx, 1060, 640, 140, 50)
        fs(ctx, hexc("#d8c8a0"), lw=5)
        text(ctx, "NOTRE-DAME", 1060, 540, 40, INK, outline=0, shadow=False)
        star(ctx, 1060, 640, 22, GOLD)
        text(ctx, "TUILERIES", 300, 380, 40, INK, outline=0, shadow=False)
        k = ease(prog(t, 0.3, t_inside - 0.2))
        pts = []
        for i in range(int(200 * k) + 2):
            u = i / 200
            x = 300 + u * 760 + 260 * math.sin(u * 17)
            y = 420 + 220 * math.sin(u * 11) + u * 200
            pts.append((x, y))
        ctx.save()
        ctx.set_dash([16, 10])
        poly(ctx, pts, close=False)
        setc(ctx, RED)
        ctx.set_line_width(7)
        ctx.stroke()
        ctx.restore()
        px, py = pts[-1]
        circle(ctx, px, py, 18)
        fs(ctx, GOLD, lw=5)
        if t > t_lost:
            pop_text(ctx, "WRONG WAY!", 960, 140, 100, t - t_lost, RED)
            for k2 in range(3):
                text(ctx, "?", 1500 + k2 * 90, 300 + 30 * math.sin(t * 4 + k2), 110, RED, outline=0, shadow=False)
    else:
        tt = t - t_inside
        ctx.save()
        cam(ctx, 1150, 520, lerp(1.4, 1.7, ease(prog(tt, 0, D - t_inside))))
        cathedral_bg(ctx, t, dim=0.15)
        pope(ctx, 1150, 520, 0.6, t, face=-0.2, expr="flat", blink=1.0 if (t % 3) < 1.5 else 0.0,
             larm=(0.6, 1.8), rarm=(-0.6, -1.8), tilt=-0.05)
        for k in range(3):
            ph = (t * 0.5 + k / 3) % 1
            circle(ctx, 1220 + ph * 40, 430 - ph * 60, 8 + ph * 10)
            setc(ctx, WHITE, 0.5 * (1 - ph))
            ctx.fill()
        ctx.restore()
        clock_icon(ctx, 1650, 220, 110, tt * 2, back=False)
        pop_text(ctx, "~1 HOUR LATER...", 960, 980, 80, tt - 0.8, WHITE)
        text(ctx, "brrr", 600, 300, 60, (0.7, 0.85, 1.0), font=HAND_FONT, outline=5, alpha=ease(prog(tt, 2, 2.4)))
    vignette(ctx, 0.4)


def sh_cathedral(ctx, t, D, cue):
    t_well = cue("Well, mostly")
    t_rev = cue("The Revolution")
    if t < t_rev:
        ctx.save()
        cam(ctx, 960, lerp(600, 480, ease(prog(t, 0, t_rev))), lerp(0.9, 1.0, ease(prog(t, 0, t_rev))))
        paris_bg(ctx, t)
        nd_facade(ctx, 960, 820, 0.85)
        # temporary neo-gothic porch
        ctx.rectangle(660, 640, 600, 180)
        fs(ctx, hexc("#e8dcc0"), lw=6)
        for k in range(4):
            line(ctx, 700 + k * 170, 640, 700 + k * 170, 820, 8, GOLD)
        text(ctx, "N", 960, 700, 70, GOLD, outline=4)
        carriage(ctx, 1500, 960, 0.5, t, moving=t < 1.0)
        ctx.restore()
        pop_text(ctx, "NOTRE-DAME", 960, 120, 100, t - 0.4, GOLD, hold=t_well - 0.4)
        if t > t_well:
            pop_text(ctx, "...MOSTLY.", 960, 980, 90, t - t_well, WHITE)
    else:
        tt = t - t_rev
        ctx.save()
        cam(ctx, 1220, 640, lerp(1.6, 2.0, ease(prog(tt, 0, D - t_rev))))
        cathedral_bg(ctx, t, crack=1.0)
        # a painted canvas panel peels back to reveal the crack
        peel = ease(prog(t, cue("so the organisers") - 0.5, cue("so the organisers") + 1.0))
        ctx.save()
        ctx.translate(1120 + 200 * peel * 0.75, 520)
        pw = 200 * (1 - peel * 0.75)
        ctx.rectangle(0, 0, pw, 260)
        fs(ctx, hexc("#f2ead6"), lw=4)
        for k in range(3):
            line(ctx, 15, 40 + k * 80, max(16, pw - 15), 40 + k * 80, 6, GOLD)
        ctx.restore()
        guy(ctx, 1000, 640, 0.42, t, expr="o", face=0.9, look=(1, -0.5), larm=(0.3, 0.2), rarm=(-1.6, 0.3))
        ctx.restore()
        pop_text(ctx, "PAINTED CANVAS & CARDBOARD", 960, 120, 74, tt - 0.5, GOLD)
        text(ctx, "hiding the damage left by the Revolution", 960, 1000, 46, WHITE, font=HAND_FONT, outline=5,
             alpha=ease(prog(tt, 1.5, 1.9)))
    vignette(ctx, 0.4)


def train_shape(ctx, x0, y0, x1, y1, w=120, sag=0.0):
    ctx.move_to(x0, y0 - 20)
    ctx.curve_to(lerp(x0, x1, 0.4), y0 + sag, lerp(x0, x1, 0.7), y1 - w * 0.4, x1, y1 - w / 2)
    ctx.line_to(x1, y1 + w / 2)
    ctx.curve_to(lerp(x0, x1, 0.7), y1 + w * 0.4, lerp(x0, x1, 0.4), y0 + 40 + sag, x0, y0 + 30)
    ctx.close_path()
    fs(ctx, CRIMSON, lw=6)
    rnd = random.Random(3)
    for i in range(14):
        u = rnd.random()
        bx = lerp(x0, x1, u)
        by = lerp(y0, y1, u) + rnd.uniform(-20, 20)
        bee(ctx, bx, by, 0.45)
    ctx.move_to(x1, y1 - w / 2)
    ctx.line_to(x1, y1 + w / 2)
    setc(ctx, WHITE)
    ctx.set_line_width(18)
    ctx.stroke()


def aisle_bg(ctx, t, dim=0.1):
    """side view of the nave: columns, crowd behind, red carpet floor."""
    vgrad(ctx, -1000, -800, 4000, 2400, hexc("#3a3048"), hexc("#6a5a5a"))
    for cx in range(-400, 2600, 340):
        ctx.rectangle(cx - 50, -100, 100, 900)
        fs(ctx, STONE, lw=6)
        ctx.move_to(cx + 50, 300)
        ctx.curve_to(cx + 50, 120, cx + 170, 60, cx + 170, 40)
        ctx.curve_to(cx + 170, 60, cx + 290, 120, cx + 290, 300)
        setc(ctx, STONE)
        ctx.set_line_width(30)
        ctx.stroke()
    for k in range(6):
        warm_glow(ctx, 100 + k * 360, 320, 160, 0.3)
    crowd_stands(ctx, t, y0=520, n=14, x0=-300, x1=2300, s=0.3)
    setc(ctx, (0.08, 0.05, 0.12), 0.45)
    ctx.paint()
    ctx.rectangle(-1000, 760, 4000, 600)
    fs(ctx, hexc("#6a5a4a"), lw=6)
    ctx.rectangle(-1000, 790, 4000, 160)
    fs(ctx, CRIMSON, lw=5)
    setc(ctx, (0.05, 0.03, 0.08), dim)
    ctx.paint()


def sh_train(ctx, t, D, cue):
    t_sis = cue("The other train bearers")
    t_like = cue("And they really")
    ctx.save()
    cam(ctx, 900, 600, 1.3)
    aisle_bg(ctx, t)
    walk = t * 0.6
    jx = 1400 + math.sin(t * 0.5) * 10
    train_shape(ctx, jx - 20, 640, 260, 860, w=150)
    josephine(ctx, jx, 520, 0.6, t, face=0.6, expr="smile", walk=walk, larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    looks = t > t_like
    for i, sx in enumerate((900, 600)):
        sister(ctx, sx, 560, 0.52, t, seed=i, face=0.8 if not looks else 0.0, walk=walk + i * 0.3,
               expr="flat" if not looks else "frown", brows="angry" if looks else None,
               look=(1, 0) if not looks else (0, 0), larm=(0.8, -1.2), rarm=(-0.8, 1.2))
    guy(ctx, 360, 560, 0.52, t, expr="smile", face=0.8, walk=walk + 0.6, larm=(0.8, -1.2), rarm=(-0.8, 1.2))
    ctx.restore()
    pop_text(ctx, "EMPRESS JOSEPHINE", 1400, 150, 74, t - 1.2, GOLD, hold=t_sis - 1.4)
    if t > t_sis:
        pop_text(ctx, "NAPOLEON'S SISTERS", 760, 150, 74, t - t_sis - 0.3, WHITE, hold=t_like - t_sis)
    if t > t_like + 0.4:
        for i, sx in enumerate((900, 600)):
            text(ctx, "hmph!", sx, 330, 50, RED, font=HAND_FONT, outline=5, alpha=ease(prog(t, t_like + 0.4 + i * 0.4,
                                                                                         t_like + 0.7 + i * 0.4)))
    vignette(ctx, 0.4)


def sh_yank(ctx, t, D, cue):
    t_go = cue("All at once")
    t_land = cue("The whole train")
    t_step = cue("I stepped on it")
    ctx.save()
    jolt = prog(t, t_step + 0.8, t_step + 1.2) - prog(t, t_step + 1.6, t_step + 2.4)
    cam(ctx, 900, 600, 1.3, shake=10 * (prog(t, t_step + 0.8, t_step + 0.9) - prog(t, t_step + 1.4, t_step + 1.6)), t=t)
    aisle_bg(ctx, t)
    jx = 1400 - 60 * jolt
    dropped = t > t_go
    sag = 140 * ease(prog(t, t_go, t_go + 0.4)) if dropped else 0
    train_shape(ctx, jx - 20, 640, 300 if not dropped else 420, 860 + sag * 0.3, w=150, sag=sag)
    josephine(ctx, jx, 520, 0.6, t, face=0.6 if jolt < 0.3 else -0.2, expr="smile" if jolt < 0.3 else "shock",
              tilt=-0.35 * jolt, larm=(0.3, 0.2) if jolt < 0.3 else (2.4, 0.3),
              rarm=(-0.3, -0.2) if jolt < 0.3 else (-2.4, -0.3))
    for i, sx in enumerate((900, 620)):
        sister(ctx, sx - (120 if dropped else 0), 560, 0.52, t, seed=i, face=0.0, expr="grin" if dropped else "frown",
               larm=(0.8, -1.2) if not dropped else (0.3, 0.2), rarm=(-0.8, 1.2) if not dropped else (-0.3, -0.2))
    under = t > t_land
    if under:
        # the guy buried under the velvet, feet sticking out
        ctx.save()
        ctx.translate(560, 840)
        ctx.rotate(-math.pi / 2)
        doodle(ctx, 0, 0, 0.45, expr="shock", face=0, larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        ctx.restore()
        ellipse(ctx, 560, 820, 200, 80)
        fs(ctx, CRIMSON, lw=6)
        for k in range(4):
            bee(ctx, 480 + k * 50, 810, 0.5)
        kick = math.sin(t * 9) * 12
        for k in range(2):
            line(ctx, 370, 830 + k * 18, 290, 815 + k * 30 + kick * (1 if k else -1), 9)
            ellipse(ctx, 282, 815 + k * 30 + kick * (1 if k else -1), 18, 10)
            fs(ctx, INK, lw=0)
        cap_alone(ctx, 760, 790, 0.35, rot=0.5)
    else:
        guy(ctx, 380, 560, 0.52, t, expr="o", face=0.8, larm=(0.8, -1.2), rarm=(-0.8, 1.2))
    ctx.restore()
    if t > t_go:
        pop_text(ctx, "LET GO!", 760, 200, 90, t - t_go, RED, hold=t_land - t_go + 0.5)
    if t > t_step + 0.8:
        burst(ctx, 1450, 220, 150, t - t_step - 0.8, "YANK!", size=70, color=(1, 0.85, 0.3))
    if t > t_step + 2.0:
        pop_text(ctx, "like a fish on a line", 960, 980, 64, t - t_step - 2.0, WHITE, font=HAND_FONT, outline=6)
    vignette(ctx, 0.4)


def altar_scene(ctx, t, nap_kw=None, crown_pos=None, guy_kw=None, pope_kw=None, cushion_crown=True, dim=0.1):
    cathedral_bg(ctx, t, dim=dim)
    crowd_stands(ctx, t, y0=560, x0=-300, x1=700, n=6, s=0.3, gasp=(nap_kw or {}).get("_gasp", 0))
    crowd_stands(ctx, t, y0=560, x0=1300, x1=2300, n=6, s=0.3, seed=5, gasp=(nap_kw or {}).get("_gasp", 0))
    pk = dict(face=-0.7, expr="smile", larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    pk.update(pope_kw or {})
    pope(ctx, 1280, 540, 0.5, t, **pk)
    nk = dict(head="laurel", face=-0.4, expr="flat", larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    nk.update({k: v for k, v in (nap_kw or {}).items() if not k.startswith("_")})
    napoleon(ctx, 1060, 540, 0.58, t, **nk)
    gk = dict(expr="smile", face=0.6, larm=(1.3, -0.4), rarm=(-1.3, 0.4))
    gk.update(guy_kw or {})
    guy(ctx, 780, 600, 0.55, t, **gk)
    cushion(ctx, 780, 700, 0.6)
    if cushion_crown:
        imperial_crown(ctx, 780, 670, 0.32, glow=0.4)
    if crown_pos:
        x, y, rot = crown_pos
        imperial_crown(ctx, x, y, 0.45, rot=rot, glow=1.0)


def sh_crown(ctx, t, D, cue):
    t_cush = cue("I was holding")
    t_bless = cue("The Pope raised")
    t_sneeze = cue("And I sneezed")
    t_big = cue("A dusty")
    ctx.save()
    if t < t_sneeze:
        cam(ctx, lerp(1000, 900, ease(prog(t, 0, t_sneeze))), 560, lerp(1.0, 1.5, ease(prog(t, 0, t_sneeze))))
    else:
        cam(ctx, 780, 600, 2.3, shake=12 * (prog(t, t_sneeze + 0.6, t_sneeze + 0.7) -
                                            prog(t, t_sneeze + 1.0, t_sneeze + 1.3)), t=t)
    sn = prog(t, t_sneeze - 0.1, t_sneeze + 0.6)
    tilt = -0.25 * ease(sn) if t < t_sneeze + 0.6 else 0.35 * math.exp(-(t - t_sneeze - 0.6) * 4)
    altar_scene(ctx, t, pope_kw=dict(rarm=(-2.2, 0.4)) if t > t_bless else None,
                guy_kw=dict(expr="o" if t_sneeze < t < t_sneeze + 0.6 else ("shock" if t > t_sneeze + 0.6 else "smile"),
                            tilt=tilt, face=0.3 if t > t_sneeze else 0.6),
                cushion_crown=True)
    if t > t_sneeze + 0.6:
        rnd = random.Random(2)
        for i in range(30):
            ph = clamp((t - t_sneeze - 0.6) * 1.2)
            a = rnd.uniform(-1.2, 0.2)
            r = ph * rnd.uniform(80, 300)
            circle(ctx, 830 + math.cos(a) * r, 560 + math.sin(a) * r, 4)
            setc(ctx, (0.85, 0.95, 1.0), 0.8 * (1 - ph))
            ctx.fill()
    ctx.restore()
    if t > t_cush:
        pop_text(ctx, "THE CROWN", 600, 160, 80, t - t_cush - 0.4, GOLD, hold=t_bless - t_cush)
    if t > t_bless + 0.5:
        pop_text(ctx, "*blessing*", 1400, 200, 64, t - t_bless - 0.5, WHITE, font=HAND_FONT, outline=6,
                 hold=t_sneeze - t_bless - 0.6)
    if t > t_sneeze - 0.1 and t < t_sneeze + 0.6:
        pop_text(ctx, "ah... ah...", 960, 200, 80, t - t_sneeze + 0.1, WHITE, font=HAND_FONT, outline=6)
    if t > t_sneeze + 0.6:
        burst(ctx, 1300, 300, 220, t - t_sneeze - 0.6, "AH-CHOOO!", size=84, color=(0.75, 0.9, 1.0),
              tcolor=hexc("#2a4a7a"))
    vignette(ctx, 0.4)


def sh_fly(ctx, t, D, cue):
    t_gasp = cue("The whole cathedral")
    t_snatch = cue("And Napoleon")
    t_catch = cue("And Napoleon", frac=0.62)
    t_head = cue("And Napoleon", frac=0.85)
    ctx.save()
    cam(ctx, lerp(880, 1000, ease(prog(t, 0, D))), lerp(500, 470, ease(prog(t, 0, D))), lerp(1.3, 1.15, ease(prog(t, 0, D))))
    # crown flight: from cushion up in an arc to Napoleon's hand, then to his head
    if t < t_catch:
        u = ease_out(prog(t, 0, t_catch))
        cx = lerp(780, 1110, u)
        cy = 670 - math.sin(u * math.pi) * 300 + (u * -40)
        rot = t * 3
        pos = (cx, cy, rot)
        nap_r = (lerp(-0.4, -2.75, ease(prog(t, t_snatch, t_catch))), 0.0)
        head = "laurel"
    elif t < t_head:
        u = ease(prog(t, t_catch, t_head))
        pos = (lerp(1110, 1072, u), lerp(310, 440, u), lerp(0.4, 0, u))
        nap_r = (lerp(-2.75, -2.9, u), lerp(0, 0.9, u))
        head = "laurel"
    else:
        pos = None
        nap_r = (-0.3, -0.2)
        head = "crown"
    altar_scene(ctx, t, nap_kw=dict(head=head, rarm=nap_r, expr="flat" if t < t_head else "smile",
                                    look=(0.2, -1) if t < t_head else (0, 0), _gasp=1 if t > t_gasp else 0,
                                    brows="angry" if t < t_head else None),
                crown_pos=pos, cushion_crown=False,
                guy_kw=dict(expr="shock", face=0.3, look=(1, -1)), pope_kw=dict(expr="shock"))
    if pos and t < t_catch:
        for k in range(4):
            sparkle(ctx, pos[0] - 40 + k * 25, pos[1] + 50, 16, t * 3 + k)
    ctx.restore()
    if t > t_gasp:
        pop_text(ctx, "GASP!", 400, 200, 100, t - t_gasp, WHITE, hold=t_snatch - t_gasp)
    if t > t_catch:
        burst(ctx, 1500, 260, 140, t - t_catch, "CATCH!", size=60, color=(1, 0.85, 0.3))
    if t > t_head + 0.3:
        pop_text(ctx, "SELF-CROWNED.", 960, 980, 100, t - t_head - 0.3, GOLD)
    vignette(ctx, 0.4)


def sh_crownfact(ctx, t, D, cue):
    t_right = cue("And they're right")
    t_plan = cue("He did plan it")
    t_catch = cue("He just didn't")
    paper_bg(ctx)
    # hierarchy diagram: Napoleon above the Pope
    k = ease(prog(t, 0.8, 2.0))
    napoleon(ctx, 760, lerp(560, 360, k), 0.6, t, head="crown", face=0.3, expr="smile",
             larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    pope(ctx, 1160, lerp(360, 560, k), 0.6, t, face=-0.3, expr="flat", larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    if k > 0.9:
        poly(ctx, [(960, 280), (930, 340), (990, 340)])
        fs(ctx, hexc("#2f7a3a"), lw=0)
        text(ctx, "NO ONE ABOVE HIM", 960, 880, 70, INK, outline=0, shadow=False)
    pop_text(ctx, "PLANNED ALL ALONG", 960, 110, 90, t - 0.3, FR_BLUE)
    if t > t_plan:
        ctx.save()
        ctx.translate(360, 700)
        ctx.rotate(-0.12)
        rrect(ctx, -220, -70, 440, 140, 14)
        fs(ctx, None, lw=10, stroke=hexc("#2f7a3a"))
        text(ctx, "TRUE", 0, 0, 90, hexc("#2f7a3a"), outline=0, shadow=False)
        ctx.restore()
    if t > t_catch:
        ctx.save()
        ctx.translate(1580, 700)
        ctx.rotate(0.12)
        rrect(ctx, -260, -70, 520, 140, 14)
        fs(ctx, None, lw=10, stroke=RED)
        text(ctx, "THE CATCH?", 0, 0, 80, RED, outline=0, shadow=False)
        ctx.restore()
    vignette(ctx, 0.3)


def sh_josephine(ctx, t, D, cue):
    t_knelt = cue("She knelt")
    t_perfect = cue("The one moment")
    t_far = cue("Mostly because")
    if t < t_far:
        ctx.save()
        cam(ctx, 1000, 560, lerp(1.4, 1.7, ease(prog(t, 0, t_far))))
        cathedral_bg(ctx, t, dim=0.1)
        warm_glow(ctx, 1000, 500, 500, 0.3)
        lower = ease(prog(t, t_knelt + 1.0, t_knelt + 3.0))
        napoleon(ctx, 1120, 520, 0.6, t, head="crown", face=-0.6, expr="smile",
                 larm=(lerp(1.6, 1.2, lower), -0.6), rarm=(-0.3, -0.2))
        josephine(ctx, 900, lerp(600, 640, ease(prog(t, 0, t_knelt + 0.5))), 0.55, t, face=0.5,
                  crown=t > t_knelt + 3.0, expr="happy" if t > t_knelt + 3.0 else "smile",
                  larm=(0.6, -1.8), rarm=(-0.6, 1.8), show_legs=False)
        if t < t_knelt + 3.0:
            small_crown(ctx, lerp(1010, 905, lower), lerp(470, 560, lower), 0.5)
        if t > t_perfect:
            for k in range(6):
                sparkle(ctx, 800 + k * 80, 400 + 40 * math.sin(k + t), 24, t + k)
        ctx.restore()
        if t > t_perfect:
            pop_text(ctx, "PERFECT.", 960, 980, 100, t - t_perfect, GOLD)
    else:
        tt = t - t_far
        ctx.save()
        cam(ctx, 960, 560, lerp(1.6, 0.6, ease(prog(tt, 0, 1.5))))
        cathedral_bg(ctx, t, dim=0.1)
        napoleon(ctx, 1120, 520, 0.6, t, head="crown", face=-0.6, expr="smile", larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        josephine(ctx, 900, 640, 0.55, t, face=0.5, crown=True, expr="happy", show_legs=False,
                  larm=(0.6, -1.8), rarm=(-0.6, 1.8))
        guy(ctx, 2300, 600, 0.55, t, expr="grin", face=-0.6, larm=(0.3, 0.2), rarm=(-2.4, 0.4))
        ctx.restore()
        pop_text(ctx, "(me, far, far away)", 1500, 980, 64, tt - 1.2, WHITE, font=HAND_FONT, outline=6)
    vignette(ctx, 0.4)


def sh_height(ctx, t, D, cue):
    t_not = cue("Napoleon wasn't")
    t_169 = cue("He was about")
    t_myth = cue("The myth came")
    t_brit = cue("The myth came", frac=0.6)
    paper_bg(ctx)
    pop_text(ctx, "\"LITTLE\" NAPOLEON?", 960, 100, 90, t - 0.2, INK, outline=0)
    if t < t_myth:
        # height chart
        for k in range(6):
            y = 900 - k * 100
            line(ctx, 500, y, 1500, y, 2, (0.6, 0.55, 0.45))
            text(ctx, f"{k * 0.4:.1f} m", 450, y, 32, INK, font=HAND_FONT, outline=0, shadow=False, align="right")
        k = ease_out(prog(t, t_not, t_not + 0.8))
        # 250 px per metre; doodle spans 556*s from head top to feet
        sn = 1.69 * 250 / 556
        napoleon(ctx, 800, lerp(1400, 900 - 456 * sn, k), sn, t, head="bare", body=FR_BLUE,
                 face=0.3, expr="flat", larm=(0.3, 0.2), rarm=(-1.3, 1.6))
        sg = 1.62 * 250 / 556
        guy(ctx, 1320, lerp(1400, 900 - 456 * sg, k), sg, t, expr="o", face=-0.4, look=(-1, 0),
            larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        if t > t_169:
            yl = 900 - 1.69 * 250
            line(ctx, 640, yl, 960, yl, 6, RED)
            pop_text(ctx, "~1.69 m", 800, yl - 60, 70, t - t_169, RED, outline=0)
            pop_text(ctx, "AVERAGE FOR HIS TIME", 960, 1010, 64, t - t_169 - 0.8, hexc("#2f7a3a"), outline=0)
    else:
        tt = t - t_myth
        # two rulers: French inch vs English inch
        for r, (lab, unit, col) in enumerate((("FRENCH INCH", 2.707, FR_BLUE), ("ENGLISH INCH", 2.54, RED))):
            y = 330 + r * 170
            rrect(ctx, 260, y, 1000, 90, 10)
            fs(ctx, hexc("#f6e6b0"), lw=5)
            step = unit * 80
            k = 0
            while 280 + k * step < 1250:
                line(ctx, 280 + k * step, y, 280 + k * step, y + 40, 4)
                k += 1
            text(ctx, lab, 1300, y + 45, 46, col, align="left", outline=0, shadow=False)
        text(ctx, "5 ft 2 in (French) = about 5 ft 7 in (English)", 960, 720, 52, INK, font=HAND_FONT, outline=0,
             shadow=False, alpha=ease(prog(tt, 0.8, 1.2)))
        if t > t_brit:
            # British caricature print
            kk = back_out(prog(t, t_brit, t_brit + 0.5), 1.6)
            ctx.save()
            ctx.translate(960, 900)
            ctx.scale(max(kk, 1e-3), max(kk, 1e-3))
            ctx.rotate(-0.05)
            rrect(ctx, -330, -140, 660, 220, 6)
            fs(ctx, hexc("#efe2c2"), lw=6)
            napoleon(ctx, -150, -40, 0.18, t, head="bicorne", body=FR_BLUE, face=0.3, expr="frown", brows="angry",
                     larm=(2.4, 0.3), rarm=(-2.4, -0.3))
            text(ctx, "\"LITTLE BONEY\"", 110, -60, 46, INK, outline=0, shadow=False)
            text(ctx, "British cartoon, c. 1803", 110, 0, 34, INK, font=HAND_FONT, outline=0, shadow=False)
            ctx.restore()
    vignette(ctx, 0.3)


def sh_painting(ctx, t, D, cue):
    t_years = cue("He spent")
    t_mother = cue("Like Napoleon's mother")
    t_wasnt = cue("She wasn't")
    t_rome = cue("She had stayed")
    if t < t_years:
        ctx.save()
        cam(ctx, 900, 520, 1.25)
        cathedral_bg(ctx, t, dim=0.15)
        crowd_stands(ctx, t, y0=560, x0=-300, x1=700, n=6, s=0.3)
        # David in a box, sketching
        ctx.rectangle(560, 500, 380, 160)
        fs(ctx, hexc("#5a3a22"), lw=6)
        david(ctx, 750, 420, 0.5, t, face=0.6, expr="flat", look=(1, 0.3), larm=(0.9, -1.4), rarm=(-1.0, 1.2 + 0.2 * math.sin(t * 12)))
        rrect(ctx, 780, 470, 120, 90, 6)
        fs(ctx, hexc("#f4ecd8"), lw=4)
        for k in range(3):
            line(ctx, 795, 490 + k * 22, 795 + 90 * ((t * 1.3 + k * 0.3) % 1), 490 + k * 22, 3)
        ctx.restore()
        pop_text(ctx, "JACQUES-LOUIS DAVID", 960, 120, 84, t - 0.6, GOLD)
        text(ctx, "official painter", 960, 200, 48, WHITE, font=HAND_FONT, outline=5, alpha=ease(prog(t, 1.4, 1.8)))
    else:
        tt = t - t_years
        bg_fill(ctx, hexc("#1e1a24"))
        z = 1.0 if t < t_mother else lerp(1.0, 2.6, ease(prog(t, t_mother, t_mother + 1.5)))
        ctx.save()
        cam(ctx, 960, 540 if t < t_mother else lerp(540, 419, ease(prog(t, t_mother, t_mother + 1.5))), z)
        david_painting(ctx, 260, 160, 1400, 840, t)
        ctx.restore()
        pop_text(ctx, "1805 - 1807", 960, 90, 80, tt - 0.4, GOLD, hold=t_mother - t_years - 0.3)
        if t > t_mother + 1.0:
            ctx.save()
            circle(ctx, 960, 560, 120 + 6 * math.sin(t * 8))
            setc(ctx, GOLD)
            ctx.set_line_width(8)
            ctx.set_dash([24, 14])
            ctx.stroke()
            ctx.restore()
            pop_text(ctx, "MADAME MÈRE", 960, 90, 80, t - t_mother - 1.0, WHITE, hold=t_wasnt - t_mother - 0.6)
        if t > t_wasnt:
            pop_text(ctx, "WASN'T THERE!", 960, 90, 90, t - t_wasnt, RED)
        if t > t_rome:
            pop_text(ctx, "(she stayed in Rome)", 960, 990, 64, t - t_rome, WHITE, font=HAND_FONT, outline=6)
    vignette(ctx, 0.4)


def sh_spotted(ctx, t, D, cue):
    look = ease(prog(t, 1.2, 1.8))
    zoom_eye = ease(prog(t, 3.0, 4.0))
    ctx.save()
    if t < 4.6:
        cam(ctx, lerp(900, 760, zoom_eye), lerp(500, 420, zoom_eye), lerp(1.2, 2.6, zoom_eye))
        cathedral_bg(ctx, t, dim=0.2)
        ctx.rectangle(560, 500, 380, 160)
        fs(ctx, hexc("#5a3a22"), lw=6)
        david(ctx, 750, 420, 0.5, t, face=lerp(0.6, -0.9, look), expr="o" if look > 0.5 else "flat",
              look=(lerp(1, -1, look), 0.3), brows="up" if look > 0.5 else None,
              larm=(0.9, -1.4), rarm=(-1.0, 1.2))
        rrect(ctx, 780, 470, 120, 90, 6)
        fs(ctx, hexc("#f4ecd8"), lw=4)
    else:
        cam(ctx, 600, 600, 2.0)
        cathedral_bg(ctx, t, dim=0.2)
        guy(ctx, 600, 600, 0.55, t, expr="shock", face=0.3, look=(1, -0.6), brows="worried",
            tilt=0.2 * math.sin(t * 10), larm=(1.3, -0.4), rarm=(-1.3, 0.4))
        pop_text(ctx, "*sniff*", 760, 400, 60, t - 4.8, WHITE, font=HAND_FONT, outline=5)
    ctx.restore()
    if t < 4.6 and t > 2.0:
        # dramatic zoom lines
        for k in range(24):
            a = k * math.pi / 12
            line(ctx, W / 2 + math.cos(a) * 600, H / 2 + math.sin(a) * 600, W / 2 + math.cos(a) * 1400,
                 H / 2 + math.sin(a) * 1400, 8, WHITE, 0.25 * zoom_eye)
    if t > 4.6:
        pop_text(ctx, "UH-OH.", 960, 980, 110, t - 4.6, RED)
    vignette(ctx, 0.45)


def sh_return(ctx, t, D, cue):
    t_closer = cue("I stepped closer")
    t_there = cue("And there")
    if t < t_closer:
        ctx.save()
        cam(ctx, 900, 480, 1.0)
        museum_bg(ctx, t, painting_cap=1.0)
        leaf_case(ctx, 1500, 430, t, glow=0.15)
        land = ease_out(prog(t, 0, 0.5))
        sq = -0.15 * math.exp(-max(0, t - 0.5) * 6) if t > 0.5 else 0
        guy(ctx, 1100, lerp(-300, 560, land), 0.7, t, expr="smile", squash=sq, face=-0.6, look=(-1, -0.6),
            larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        ctx.restore()
    else:
        z = lerp(1.0, 4.2, ease(prog(t, t_closer, t_there + 1.8)))
        cxp = lerp(700, 160 + 1080 * 0.885, ease(prog(t, t_closer, t_there + 1.8)))
        cyp = lerp(400, 80 + 640 * 0.5, ease(prog(t, t_closer, t_there + 1.8)))
        ctx.save()
        cam(ctx, cxp, cyp, z)
        museum_bg(ctx, t, painting_cap=1.0)
        if t > t_there + 1.8:
            circle(ctx, 160 + 1080 * 0.885, 80 + 640 * 0.5 - 2, 20 + math.sin(t * 8))
            setc(ctx, GOLD)
            ctx.set_line_width(3)
            ctx.set_dash([8, 5])
            ctx.stroke()
        ctx.restore()
        if t > t_there + 2.0:
            pop_text(ctx, "MY CAP!", 960, 960, 120, t - t_there - 2.0, RED, rot=-0.03)
    vignette(ctx, 0.45)


def sh_pocket(ctx, t, D, cue):
    t_cold = cue("Then I put")
    t_two = cue("Two leaves")
    t_each = cue("At six hundred")
    t_back = cue("I should probably")
    ctx.save()
    cam(ctx, 1000, 500, 1.3)
    museum_bg(ctx, t, painting_cap=1.0)
    leaf_case(ctx, 1500, 430, t, glow=0.15)
    out = t > t_two
    guy(ctx, 1150, 560, 0.7, t, expr="o" if t < t_two else ("shock" if t < t_back else "grin"), face=0.0,
        larm=(0.3, 0.2), rarm=(-2.0, 0.4) if out else (0.1, 0.3), brows="worried" if t > t_back else None)
    if out:
        k = ease_out(prog(t, t_two, t_two + 0.4))
        hx, hy = 1150 + 135, 560 - 30
        warm_glow(ctx, hx, hy, 160, 0.5 * k)
        for i in range(2):
            leaf(ctx, hx - 10 + i * 45, lerp(hy + 120, hy, k) - i * 12, 1.1 * k + 0.01, rot=0.5 + i * 0.4,
                 glint=0.8)
    if t > t_back:
        sweat(ctx, 1240, 420, 1.2, t)
    ctx.restore()
    if t > t_each:
        pop_text(ctx, "€600,000+ EACH?!", 960, 150, 100, t - t_each, GOLD)
    vignette(ctx, 0.45)


def sh_ending(ctx, t, D, cue):
    t_yes = cue("I made the Emperor")
    t_still = cue("And he still")
    t_help = cue("I think I helped")
    if t < t_still:
        vgrad(ctx, 0, 0, W, H, hexc("#1a2a5a"), hexc("#0e1636"))
        for i in range(30):
            rnd = random.Random(i)
            bee(ctx, (rnd.random() * W + t * 15) % W, rnd.random() * H, 0.5)
        guy(ctx, 420, 470, 0.95, t, expr="worried", face=0.5, brows="worried", larm=(0.3, 0.2), rarm=(-1.6, 0.4))
        items = [("MADE THE EMPEROR LATE", 0.0), ("TRIPPED THE EMPRESS", 0.33), ("THREW A CROWN AT HIM", 0.66)]
        for i, (lab, fr) in enumerate(items):
            tc = cue("I made the Emperor", frac=fr)
            if t < tc:
                continue
            y = 280 + i * 220
            pop_text(ctx, lab, 1250, y, 64, t - tc, WHITE)
            a = ease(prog(t, tc, tc + 0.3))
            ctx.save()
            ctx.translate(1250 + text_width(ctx, lab, 64) / 2 + 70, y)
            ctx.move_to(-20, 0)
            ctx.line_to(0, 22)
            ctx.line_to(36, -30)
            setc(ctx, (0.4, 0.9, 0.4), a)
            ctx.set_line_width(12)
            ctx.stroke()
            ctx.restore()
    else:
        tt = t - t_still
        bg_fill(ctx, hexc("#1e1a24"))
        ctx.save()
        cam(ctx, 960, 540, lerp(1.0, 1.06, ease(prog(tt, 0, D - t_still))))
        david_painting(ctx, 260, 140, 1400, 840, t, cap=1.0)
        ctx.restore()
        pop_text(ctx, "EMPEROR ANYWAY.", 960, 90, 100, tt - 0.2, GOLD)
        if t > t_help:
            k = ease_out(prog(t, t_help - 0.2, t_help + 0.3))
            guy(ctx, 1700, lerp(1400, 760, k), 0.8, t, expr="sly", face=-0.4, larm=(0.3, 0.2), rarm=(-2.2, 0.8))
            pop_text(ctx, "I HELPED.", 960, 990, 110, t - t_help, WHITE, rot=-0.03)
    vignette(ctx, 0.45)


def sh_outro(ctx, t, D, cue):
    t_mean = cue("I mean it")
    vgrad(ctx, 0, 0, W, 800, hexc("#d9c7a8"), hexc("#c9b490"))
    ctx.rectangle(0, 780, W, 300)
    fs(ctx, hexc("#8a6a4a"), lw=6)
    rrect(ctx, 260, 560, 760, 260, 40)
    fs(ctx, hexc("#4a6a8a"), lw=7)
    rrect(ctx, 220, 500, 120, 300, 40)
    fs(ctx, hexc("#3f5c7a"), lw=7)
    rrect(ctx, 940, 500, 120, 300, 40)
    fs(ctx, hexc("#3f5c7a"), lw=7)
    guy(ctx, 640, 470, 0.72, t, expr="smile" if t < t_mean else "flat", face=0.9 if t < t_mean else 0.0,
        look=(1, 0), larm=(0.3, 0.2), rarm=(-1.2, 0.5), legs=(-1.2, -1.2))
    # the two leaves on the coffee table, a letter "RETURN TO MUSEUM"
    ctx.rectangle(1150, 700, 420, 30)
    fs(ctx, hexc("#5a3a22"), lw=5)
    leaf(ctx, 1260, 680, 0.5, rot=1.2, glint=0.6)
    leaf(ctx, 1320, 684, 0.5, rot=1.5, glint=0.6)
    rrect(ctx, 1380, 640, 160, 60, 4)
    fs(ctx, WHITE, lw=4)
    text(ctx, "to: museum", 1460, 670, 26, INK, font=HAND_FONT, outline=0, shadow=False)
    # window: a Viking ship sails past? keep it simple: a mysterious glowing envelope
    if t > t_mean + 0.6:
        pop_text(ctx, "...I mean it.", 960, 160, 100, t - t_mean - 0.6, GOLD, font=HAND_FONT, outline=8)
    vignette(ctx, 0.4)


def sh_endcard(ctx, t, D, cue):
    vgrad(ctx, 0, 0, W, H, hexc("#1a2a5a"), hexc("#0e1636"))
    for i in range(30):
        rnd = random.Random(i)
        bee(ctx, (rnd.random() * W + t * 15) % W, rnd.random() * H, 0.5)
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
        text(ctx, "More history I definitely didn't ruin, coming soon.", 1300, 760, 46, WHITE, font=HAND_FONT,
             outline=5, alpha=ease(prog(t, 1.8, 2.4)))
    if t > 2.4:
        kb = ease_in(prog(t, 2.4, 3.0))
        imperial_crown(ctx, 560, lerp(-300, 330, kb), 0.32, rot=(1 - kb) * 6)
    fade = prog(t, D - 1.0, D)
    if fade > 0:
        setc(ctx, (0, 0, 0), fade)
        ctx.paint()


SHOT_FUNCS = {
    "hook": sh_hook, "backup": sh_backup, "title": sh_title, "museum": sh_museum, "touch": sh_touch,
    "tunnel1": sh_tunnel(2026, 1804), "arrive": sh_arrive, "context": sh_context, "goldsmith": sh_goldsmith,
    "leaves": sh_leaves, "auction": sh_auction, "carriage": sh_carriage, "late": sh_late,
    "cathedral": sh_cathedral, "train": sh_train, "yank": sh_yank, "crown": sh_crown, "fly": sh_fly,
    "crownfact": sh_crownfact, "josephine": sh_josephine, "height": sh_height, "painting": sh_painting,
    "spotted": sh_spotted, "tunnel2": sh_tunnel(1804, 2026, hue=(0.5, 0.1, 0.2), hue2=(1.0, 0.85, 0.4)),
    "return": sh_return, "pocket": sh_pocket, "ending": sh_ending, "outro": sh_outro, "endcard": sh_endcard,
}
