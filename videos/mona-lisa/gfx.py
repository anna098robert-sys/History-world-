"""Drawing primitives + the doodle characters (pycairo)."""
import math, random
import cairo

W, H = 1920, 1080
INK = (0.07, 0.07, 0.08)
WHITE = (1, 1, 1)
SHADE = (0.83, 0.86, 0.90)
RED = (0.93, 0.20, 0.22)
RED_D = (0.78, 0.10, 0.13)
RED_L = (0.97, 0.33, 0.33)
LW = 7.0
TITLE_FONT = "Luckiest Guy"
HAND_FONT = "Patrick Hand"


# ---------------------------------------------------------------- math helpers
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def lerpc(c1, c2, t):
    return tuple(lerp(a, b, t) for a, b in zip(c1, c2))


def prog(t, t0, t1):
    """0..1 progress of t between t0 and t1."""
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    return clamp((t - t0) / (t1 - t0))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in(x):
    x = clamp(x)
    return x ** 3


def back_out(x, s=1.70158):
    x = clamp(x) - 1
    return x * x * ((s + 1) * x + s) + 1


def elastic(x):
    x = clamp(x)
    if x in (0, 1):
        return x
    return 2 ** (-10 * x) * math.sin((x * 10 - 0.75) * (2 * math.pi) / 3) + 1


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


# ---------------------------------------------------------------- primitives
def setc(ctx, c, a=1.0):
    if len(c) == 4:
        ctx.set_source_rgba(*c)
    else:
        ctx.set_source_rgba(c[0], c[1], c[2], a)


def fs(ctx, fill, lw=LW, stroke=INK, alpha=1.0):
    """fill + stroke the current path."""
    if fill is not None:
        setc(ctx, fill, alpha)
        if lw:
            ctx.fill_preserve()
        else:
            ctx.fill()
    if lw:
        setc(ctx, stroke, alpha)
        ctx.set_line_width(lw)
        ctx.stroke()
    else:
        ctx.new_path()


def circle(ctx, x, y, r):
    ctx.new_sub_path()
    ctx.arc(x, y, max(r, 0.01), 0, 2 * math.pi)


def ellipse(ctx, x, y, rx, ry):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(max(rx, 0.01), max(ry, 0.01))
    ctx.new_sub_path()
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


def poly(ctx, pts, close=True):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    if close:
        ctx.close_path()


def line(ctx, x1, y1, x2, y2, lw=LW, c=INK, a=1.0):
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    setc(ctx, c, a)
    ctx.set_line_width(lw)
    ctx.stroke()


def bg_fill(ctx, c):
    setc(ctx, c)
    ctx.rectangle(-4000, -4000, 12000, 12000)
    ctx.fill()


def vgrad(ctx, x, y, w, h, c1, c2):
    g = cairo.LinearGradient(0, y, 0, y + h)
    g.add_color_stop_rgb(0, *c1[:3])
    g.add_color_stop_rgb(1, *c2[:3])
    ctx.rectangle(x, y, w, h)
    ctx.set_source(g)
    ctx.fill()


def new_ctx(surface):
    ctx = cairo.Context(surface)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    return ctx


# ---------------------------------------------------------------- text
def text(ctx, s, x, y, size, color=WHITE, font=TITLE_FONT, align="center",
         outline=10, ocolor=INK, alpha=1.0, rot=0.0, shadow=True):
    if alpha <= 0.001 or not s:
        return
    ctx.save()
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ext = ctx.text_extents(s)
    ctx.translate(x, y)
    ctx.rotate(rot)
    if align == "center":
        ox = -ext.x_advance / 2
    elif align == "right":
        ox = -ext.x_advance
    else:
        ox = 0
    oy = size * 0.36
    if shadow and outline:
        ctx.move_to(ox + size * 0.05, oy + size * 0.07)
        ctx.text_path(s)
        setc(ctx, (0, 0, 0), 0.35 * alpha)
        ctx.set_line_width(outline * 2)
        ctx.stroke_preserve()
        ctx.fill()
    ctx.move_to(ox, oy)
    ctx.text_path(s)
    if outline:
        setc(ctx, ocolor, alpha)
        ctx.set_line_width(outline * 2)
        ctx.stroke_preserve()
    setc(ctx, color, alpha)
    ctx.fill()
    ctx.restore()


def text_width(ctx, s, size, font=TITLE_FONT):
    ctx.save()
    ctx.select_font_face(font)
    ctx.set_font_size(size)
    w = ctx.text_extents(s).x_advance
    ctx.restore()
    return w


def pop_text(ctx, s, x, y, size, t, color=WHITE, rot=0.0, font=TITLE_FONT, outline=10,
             dur=0.35, hold=99, out=0.25):
    """text that pops in with a springy scale at t=0, fades after hold."""
    if t < 0:
        return
    k = back_out(t / dur, 2.6) if t < dur else 1.0
    a = 1.0 if t < hold else 1 - prog(t, hold, hold + out)
    if a <= 0:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(max(k, 0.01), max(k, 0.01))
    text(ctx, s, 0, 0, size, color, font=font, rot=rot, outline=outline, alpha=a)
    ctx.restore()


def burst(ctx, x, y, r, t, label, color=(1, 0.85, 0.2), tcolor=RED, size=None, spikes=14, seed=1):
    """comic-book explosion bubble with a word inside."""
    if t < 0:
        return
    k = back_out(t / 0.25, 2.2) if t < 0.25 else 1 + 0.03 * math.sin(t * 20)
    rnd = random.Random(seed)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(max(k, 1e-3), max(k, 1e-3))
    ctx.rotate(0.08 * math.sin(t * 6))
    pts = []
    for i in range(spikes * 2):
        a = i * math.pi / spikes
        rr = r * (1.0 if i % 2 == 0 else 0.68 + rnd.random() * 0.08)
        pts.append((math.cos(a) * rr * 1.25, math.sin(a) * rr))
    poly(ctx, pts)
    fs(ctx, color, lw=8)
    text(ctx, label, 0, 0, size or r * 0.55, tcolor, outline=7, rot=-0.08)
    ctx.restore()


def speech(ctx, x, y, w, h, s, size=48, tail=(-40, 60), alpha=1.0, think=False, font=HAND_FONT,
           tcolor=INK):
    """speech/thought bubble centred at x,y."""
    if alpha <= 0:
        return
    ctx.save()
    ctx.push_group()
    if think:
        ellipse(ctx, x, y, w / 2, h / 2)
        fs(ctx, WHITE, lw=6)
        tx, ty = tail
        for i, rr in enumerate((18, 12, 8)):
            f = (i + 1) / 3.5
            circle(ctx, x + tx * f * 1.6, y + h / 2 * 0.8 + ty * f, rr)
            fs(ctx, WHITE, lw=5)
    else:
        tx, ty = tail
        ctx.move_to(x - 30, y + h / 2 - 12)
        ctx.line_to(x + tx, y + h / 2 + ty)
        ctx.line_to(x + 25, y + h / 2 - 12)
        fs(ctx, WHITE, lw=6)
        rrect(ctx, x - w / 2, y - h / 2, w, h, min(h / 2, 40))
        fs(ctx, WHITE, lw=6)
        ctx.move_to(x - 28, y + h / 2 - 3)
        ctx.line_to(x + tx * 0.95, y + h / 2 + ty * 0.95)
        ctx.line_to(x + 23, y + h / 2 - 3)
        setc(ctx, WHITE)
        ctx.fill()
    if s:
        text(ctx, s, x, y, size, tcolor, font=font, outline=0, shadow=False)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(alpha)
    ctx.restore()


# ---------------------------------------------------------------- effects
def sweat(ctx, x, y, s=1.0, t=0.0):
    yy = y + (t * 60) % 40
    ctx.save()
    ctx.translate(x, yy)
    ctx.scale(s, s)
    ctx.move_to(0, -22)
    ctx.curve_to(10, -6, 14, 4, 0, 12)
    ctx.curve_to(-14, 4, -10, -6, 0, -22)
    fs(ctx, (0.55, 0.8, 1.0), lw=4)
    ctx.restore()


def stars_ring(ctx, x, y, r, t, n=4):
    for i in range(n):
        a = t * 3 + i * 2 * math.pi / n
        star(ctx, x + math.cos(a) * r, y + math.sin(a) * r * 0.35, 16, (1, 0.85, 0.2))


def star(ctx, x, y, r, c, rot=0.0, lw=4):
    pts = []
    for i in range(10):
        a = rot - math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    poly(ctx, pts)
    fs(ctx, c, lw=lw)


def sparkle(ctx, x, y, r, t, c=(1, 1, 0.8)):
    k = 0.5 + 0.5 * math.sin(t * 9)
    rr = r * (0.6 + 0.4 * k)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(t * 1.5)
    ctx.move_to(0, -rr)
    ctx.curve_to(rr * 0.12, -rr * 0.12, rr * 0.12, -rr * 0.12, rr, 0)
    ctx.curve_to(rr * 0.12, rr * 0.12, rr * 0.12, rr * 0.12, 0, rr)
    ctx.curve_to(-rr * 0.12, rr * 0.12, -rr * 0.12, rr * 0.12, -rr, 0)
    ctx.curve_to(-rr * 0.12, -rr * 0.12, -rr * 0.12, -rr * 0.12, 0, -rr)
    setc(ctx, c, 0.95)
    ctx.fill()
    ctx.restore()


def motion_lines(ctx, x, y, w, h, n=5, c=INK, a=0.6, vertical=False, seed=3):
    rnd = random.Random(seed)
    for i in range(n):
        if vertical:
            xx = x + (i + 0.5) * w / n
            yy = y + rnd.random() * h * 0.3
            line(ctx, xx, yy, xx, yy + h * (0.5 + rnd.random() * 0.4), 4, c, a)
        else:
            yy = y + (i + 0.5) * h / n
            xx = x + rnd.random() * w * 0.3
            line(ctx, xx, yy, xx + w * (0.5 + rnd.random() * 0.4), yy, 4, c, a)


def vignette(ctx, strength=0.55):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 1.05)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, strength)
    ctx.set_source(g)
    ctx.paint()


def spiral_bg(ctx, t, c1=(0.72, 0.13, 0.15), c2=(0.80, 0.18, 0.19), cx=W / 2, cy=H / 2, speed=0.25,
              arms=1):
    """swirly painted background like the character reference image."""
    bg_fill(ctx, c1)
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(t * speed)
    for k in range(arms):
        ctx.save()
        ctx.rotate(k * 2 * math.pi / arms)
        ctx.move_to(0, 0)
        for i in range(0, 900):
            a = i * 0.035
            r = 6 + a * 52
            ctx.line_to(math.cos(a) * r, math.sin(a) * r)
        setc(ctx, c2)
        ctx.set_line_width(60)
        ctx.stroke()
        ctx.restore()
    ctx.restore()


def vortex(ctx, t, hue=(0.55, 0.15, 0.75), hue2=(0.95, 0.45, 0.15), speed=2.0):
    """time-travel tunnel: concentric rotating rings + rays."""
    bg_fill(ctx, (0.05, 0.03, 0.12))
    ctx.save()
    ctx.translate(W / 2, H / 2)
    for i in range(26, 0, -1):
        r = (i * 90 + (t * 260) % 90) * 1.0
        f = clamp(r / 2400)
        c = lerpc(hue2, hue, (i % 2) * 0.7 + f * 0.3)
        ctx.save()
        ctx.rotate(t * speed * (1 if i % 2 else -0.6) + i * 0.3)
        ctx.scale(1.0, 0.82)
        n = 12
        for j in range(n):
            a0 = j * 2 * math.pi / n
            ctx.move_to(0, 0)
            ctx.arc(0, 0, r, a0, a0 + math.pi / n)
            ctx.close_path()
        setc(ctx, c, 0.55 * (1 - f * 0.4))
        ctx.fill()
        ctx.restore()
    g = cairo.RadialGradient(0, 0, 0, 0, 0, 380)
    g.add_color_stop_rgba(0, 1, 1, 0.95, 1)
    g.add_color_stop_rgba(0.25, 1, 0.95, 0.7, 0.8)
    g.add_color_stop_rgba(1, 1, 0.8, 0.5, 0)
    ctx.set_source(g)
    circle(ctx, 0, 0, 380)
    ctx.fill()
    ctx.restore()


def clock_icon(ctx, x, y, r, t, back=True, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    circle(ctx, 0, 0, r)
    fs(ctx, (0.98, 0.93, 0.78), lw=max(3, r * 0.12))
    circle(ctx, 0, 0, r * 0.82)
    fs(ctx, None, lw=max(1.5, r * 0.04))
    for i in range(12):
        a = i * math.pi / 6
        line(ctx, math.cos(a) * r * 0.68, math.sin(a) * r * 0.68, math.cos(a) * r * 0.78,
             math.sin(a) * r * 0.78, max(1.5, r * 0.05))
    d = -1 if back else 1
    a1 = d * t * 8
    a2 = d * t * 0.7
    line(ctx, 0, 0, math.sin(a1) * r * 0.7, -math.cos(a1) * r * 0.7, max(2, r * 0.06))
    line(ctx, 0, 0, math.sin(a2) * r * 0.45, -math.cos(a2) * r * 0.45, max(2, r * 0.09))
    ctx.restore()


def pocket_watch(ctx, x, y, r, t, glow=0.0, spin=0.0):
    if glow > 0:
        g = cairo.RadialGradient(x, y, r * 0.5, x, y, r * 3)
        g.add_color_stop_rgba(0, 1, 0.9, 0.5, 0.7 * glow)
        g.add_color_stop_rgba(1, 1, 0.8, 0.3, 0)
        ctx.set_source(g)
        circle(ctx, x, y, r * 3)
        ctx.fill()
    # chain
    ctx.save()
    ctx.move_to(x, y - r * 1.15)
    ctx.curve_to(x - r * 1.4, y - r * 2.2, x - r * 2.4, y - r * 0.2, x - r * 1.9, y + r * 0.9)
    setc(ctx, (0.75, 0.6, 0.2))
    ctx.set_line_width(r * 0.1)
    ctx.set_dash([r * 0.12, r * 0.08])
    ctx.stroke()
    ctx.restore()
    circle(ctx, x, y - r * 1.12, r * 0.16)
    fs(ctx, (0.85, 0.68, 0.25), lw=4)
    circle(ctx, x, y, r)
    fs(ctx, (0.85, 0.68, 0.25), lw=6)
    circle(ctx, x, y, r * 0.84)
    fs(ctx, (0.99, 0.96, 0.86), lw=4)
    for i in range(12):
        a = i * math.pi / 6
        line(ctx, x + math.cos(a) * r * 0.66, y + math.sin(a) * r * 0.66, x + math.cos(a) * r * 0.76,
             y + math.sin(a) * r * 0.76, max(2, r * 0.05))
    a1 = -spin * 9 + 0.6
    a2 = -spin * 0.8 + 2.2
    line(ctx, x, y, x + math.sin(a1) * r * 0.66, y - math.cos(a1) * r * 0.66, max(2, r * 0.05))
    line(ctx, x, y, x + math.sin(a2) * r * 0.42, y - math.cos(a2) * r * 0.42, max(3, r * 0.08))
    circle(ctx, x, y, r * 0.06)
    fs(ctx, INK, lw=0)
    # glint
    ctx.save()
    circle(ctx, x, y, r * 0.84)
    ctx.clip()
    ctx.move_to(x - r, y - r * 0.2)
    ctx.line_to(x - r * 0.2, y - r)
    ctx.line_to(x + r * 0.05, y - r)
    ctx.line_to(x - r, y + r * 0.05)
    setc(ctx, WHITE, 0.35)
    ctx.fill()
    ctx.restore()


# ---------------------------------------------------------------- characters
def _arm(ctx, sx, sy, ang, bend, l1=80, l2=78, lw=8, hand=True):
    """arm from shoulder; ang = angle from straight down (rad, +out to the right)."""
    ex = sx + math.sin(ang) * l1
    ey = sy + math.cos(ang) * l1
    a2 = ang + bend
    hx = ex + math.sin(a2) * l2
    hy = ey + math.cos(a2) * l2
    ctx.move_to(sx, sy)
    ctx.line_to(ex, ey)
    ctx.line_to(hx, hy)
    setc(ctx, INK)
    ctx.set_line_width(lw)
    ctx.stroke()
    if hand:
        circle(ctx, hx, hy, 11)
        fs(ctx, WHITE, lw=5)
    return hx, hy


def doodle(ctx, x, y, s=1.0, face=0.9, expr="smile", look=(0, 0), blink=0.0,
           larm=(0.25, 0.1), rarm=(-0.25, -0.1), legs=(0.0, 0.0), walk=None,
           cap=True, cap_off=0.0, cap_color=RED, body=WHITE, tilt=0.0, squash=0.0,
           hair=None, extra=None, brows=None, flip=False, show_legs=True, show_body=True,
           blush=False, glasses=False, bowtie=None, cap_down=0.0):
    """The red-cap doodle guy (and, with hair/extra, every other character).
    (x, y) = head centre. Head radius = 100*s. Returns dict of hand positions in world coords.
    face: horizontal offset of facial features (-1 left .. 1 right).
    larm/rarm: (angle_from_down, elbow_bend); positive angle swings toward +x.
    legs: (left_angle, right_angle) or walk phase for automatic stride."""
    hands = {}
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if flip:
        ctx.scale(-1, 1)
    ctx.rotate(tilt)
    sq = 1 + squash
    ctx.scale(1 / sq ** 0.5, sq)

    if walk is not None:
        sw = math.sin(walk * 2 * math.pi)
        legs = (sw * 0.45, -sw * 0.45)
        bob = abs(math.cos(walk * 2 * math.pi)) * 6
        ctx.translate(0, -bob)

    # legs
    if show_legs and show_body:
        for side, a in ((-1, legs[0]), (1, legs[1])):
            hx, hy = side * 30, 318
            fx = hx + math.sin(a) * 120
            fy = hy + math.cos(a) * 120
            line(ctx, hx, hy, fx, fy, 9)
            ellipse(ctx, fx + 10, fy + 4, 22, 11)
            fs(ctx, INK, lw=0)

    # body
    if show_body:
        ctx.move_to(-48, 70)
        ctx.curve_to(-58, 170, -70, 260, -66, 300)
        ctx.curve_to(-64, 332, -40, 336, 0, 336)
        ctx.curve_to(40, 336, 64, 332, 66, 300)
        ctx.curve_to(70, 260, 58, 170, 48, 70)
        ctx.close_path()
        fs(ctx, body, lw=LW)
        if body == WHITE:
            ctx.save()
            ctx.move_to(-48, 90)
            ctx.curve_to(-58, 170, -70, 260, -66, 300)
            ctx.curve_to(-52, 250, -44, 170, -38, 95)
            setc(ctx, SHADE)
            ctx.fill()
            ctx.restore()
        if bowtie:
            poly(ctx, [(0, 102), (-26, 88), (-26, 118)])
            fs(ctx, bowtie, lw=4)
            poly(ctx, [(0, 102), (26, 88), (26, 118)])
            fs(ctx, bowtie, lw=4)
            circle(ctx, 0, 102, 7)
            fs(ctx, bowtie, lw=4)
        if extra:
            extra(ctx, "body")

    # arms (drawn over body)
    if show_body:
        m = -1 if flip else 1
        hl = _arm(ctx, -46, 120, -larm[0] * 1 - 0.0, -larm[1])
        hr = _arm(ctx, 46, 120, -rarm[0], -rarm[1])
        # store local positions -> approximate world positions (ignores tilt/squash)
        hands["l"] = (x + m * hl[0] * s, y + hl[1] * s)
        hands["r"] = (x + m * hr[0] * s, y + hr[1] * s)
        if extra:
            extra(ctx, "hands", hl, hr)

    # hair behind head
    if hair == "newton":
        ctx.move_to(-104, -30)
        ctx.curve_to(-140, 60, -130, 150, -95, 175)
        ctx.curve_to(-60, 190, -40, 150, -30, 120)
        ctx.line_to(30, 120)
        ctx.curve_to(40, 150, 70, 190, 100, 172)
        ctx.curve_to(135, 140, 140, 60, 104, -30)
        ctx.close_path()
        fs(ctx, hexc("#6b4428"), lw=LW)

    # head
    R = 100
    circle(ctx, 0, 0, R)
    setc(ctx, WHITE)
    ctx.fill()
    ctx.save()
    circle(ctx, 0, 0, R)
    ctx.clip()
    circle(ctx, 0, 0, R)
    setc(ctx, SHADE)
    ctx.fill()
    circle(ctx, 16, -6, R * 0.97)
    setc(ctx, WHITE)
    ctx.fill()
    ctx.restore()
    circle(ctx, 0, 0, R)
    fs(ctx, None, lw=LW)

    # face
    fx = face * 34
    lx, ly = look[0] * 8, look[1] * 7
    ey = -22
    eyes = [(-30 + fx + lx, ey + ly), (32 + fx + lx, ey - 3 + ly)]
    if blush:
        for ex_, ey_ in eyes:
            ellipse(ctx, ex_ + (-6 if ex_ < fx else 8), ey_ + 30, 16, 8)
            setc(ctx, (1, 0.5, 0.5), 0.5)
            ctx.fill()
    if expr in ("shock", "scared"):
        for ex_, ey_ in eyes:
            ellipse(ctx, ex_, ey_, 15, 18)
            fs(ctx, WHITE, lw=4.5)
            circle(ctx, ex_ + lx * 0.6, ey_ + ly * 0.6, 6)
            fs(ctx, INK, lw=0)
    elif expr in ("happy", "laugh") or blink >= 0.98:
        for ex_, ey_ in eyes:
            if blink >= 0.98 and expr not in ("happy", "laugh"):
                line(ctx, ex_ - 10, ey_, ex_ + 10, ey_, 5)
            else:
                ctx.move_to(ex_ - 11, ey_ + 4)
                ctx.curve_to(ex_ - 6, ey_ - 9, ex_ + 6, ey_ - 9, ex_ + 11, ey_ + 4)
                setc(ctx, INK)
                ctx.set_line_width(5)
                ctx.stroke()
    elif expr == "sly":
        for ex_, ey_ in eyes:
            ellipse(ctx, ex_, ey_ + 2, 10, 5)
            fs(ctx, INK, lw=0)
            line(ctx, ex_ - 13, ey_ - 5, ex_ + 13, ey_ - 3, 4.5)
    else:
        for ex_, ey_ in eyes:
            ellipse(ctx, ex_, ey_, 9.5, 10.5 * (1 - blink * 0.9))
            fs(ctx, INK, lw=0)
    if glasses:
        for ex_, ey_ in eyes:
            circle(ctx, ex_, ey_, 21)
            fs(ctx, None, lw=4.5)
        line(ctx, eyes[0][0] + 21, eyes[0][1], eyes[1][0] - 21, eyes[1][1], 4.5)
    if brows:
        for i, (ex_, ey_) in enumerate(eyes):
            sgn = -1 if i == 0 else 1
            if brows == "worried":
                line(ctx, ex_ - 12, ey_ - 22 - sgn * 6 * -1, ex_ + 12, ey_ - 22 + sgn * 6 * -1, 5)
            elif brows == "angry":
                line(ctx, ex_ - 12, ey_ - 26 + sgn * 6, ex_ + 12, ey_ - 26 - sgn * 6, 5)
            elif brows == "up":
                ctx.move_to(ex_ - 12, ey_ - 26)
                ctx.curve_to(ex_ - 4, ey_ - 34, ex_ + 4, ey_ - 34, ex_ + 12, ey_ - 26)
                setc(ctx, INK)
                ctx.set_line_width(5)
                ctx.stroke()
    mx, my = 8 + fx + lx * 0.6, 14 + ly * 0.6
    ctx.set_line_width(5.5)
    setc(ctx, INK)
    if expr == "smile" or expr == "happy":
        ctx.move_to(mx - 17, my - 3)
        ctx.curve_to(mx - 9, my + 11, mx + 9, my + 11, mx + 17, my - 3)
        ctx.stroke()
    elif expr in ("grin", "laugh"):
        ctx.move_to(mx - 24, my - 4)
        ctx.curve_to(mx - 18, my + 30, mx + 18, my + 30, mx + 24, my - 4)
        ctx.close_path()
        fs(ctx, (0.25, 0.05, 0.08), lw=5)
        ellipse(ctx, mx, my + 13, 10, 5)
        setc(ctx, (0.95, 0.4, 0.45))
        ctx.fill()
    elif expr in ("shock", "scared"):
        ellipse(ctx, mx, my + 8, 13, 18)
        fs(ctx, (0.25, 0.05, 0.08), lw=5)
    elif expr == "worried":
        ctx.move_to(mx - 20, my + 6)
        ctx.curve_to(mx - 10, my - 4, mx - 4, my + 12, mx + 4, my + 4)
        ctx.curve_to(mx + 10, my - 4, mx + 14, my + 8, mx + 20, my + 2)
        ctx.stroke()
    elif expr == "sly":
        ctx.move_to(mx - 16, my + 4)
        ctx.curve_to(mx - 2, my + 10, mx + 12, my + 6, mx + 20, my - 6)
        ctx.stroke()
    elif expr == "flat" or expr == "sleep":
        line(ctx, mx - 14, my + 4, mx + 14, my + 4, 5.5)
    elif expr == "o":
        ellipse(ctx, mx, my + 4, 7, 9)
        fs(ctx, (0.25, 0.05, 0.08), lw=4.5)
    elif expr == "frown":
        ctx.move_to(mx - 17, my + 10)
        ctx.curve_to(mx - 9, my - 2, mx + 9, my - 2, mx + 17, my + 10)
        ctx.stroke()

    # hair / hats on top
    if hair == "newton":
        ctx.move_to(-100, -20)
        ctx.curve_to(-104, -142, 104, -150, 102, -20)
        ctx.curve_to(70, -70, 10, -78, -20, -60)
        ctx.curve_to(-50, -70, -80, -60, -100, -20)
        fs(ctx, hexc("#7a4f2e"), lw=LW)
    elif hair == "fleming":
        ctx.move_to(-98, -28)
        ctx.curve_to(-100, -140, 98, -146, 99, -30)
        ctx.curve_to(60, -66, 10, -70, -30, -52)
        ctx.curve_to(-60, -62, -86, -46, -98, -28)
        fs(ctx, hexc("#9aa0a8"), lw=LW)
    elif hair == "worker":
        # medieval coif / hood + beard
        ctx.move_to(-104, 10)
        ctx.curve_to(-112, -150, 112, -150, 104, 10)
        ctx.curve_to(80, -50, -80, -50, -104, 10)
        fs(ctx, hexc("#8a6a42"), lw=LW)
        ctx.move_to(-62 + fx * 0.5, 44)
        ctx.curve_to(-50 + fx * 0.5, 115, 70 + fx * 0.5, 115, 82 + fx * 0.5, 36)
        ctx.curve_to(50 + fx * 0.5, 64, -30 + fx * 0.5, 66, -62 + fx * 0.5, 44)
        fs(ctx, hexc("#5a3a22"), lw=5)
    elif hair == "bald":
        pass
    elif callable(hair):
        hair(ctx)

    if cap:
        ctx.save()
        ctx.translate(0, -cap_off * 260 + cap_down * 34)
        ctx.rotate(-cap_off * 0.9)
        draw_cap(ctx, cap_color)
        ctx.restore()
    ctx.restore()
    return hands


def draw_cap(ctx, color=RED, alone=False):
    dark = tuple(c * 0.82 for c in color)
    light = tuple(min(1, c * 1.06 + 0.04) for c in color)
    # dome
    ctx.move_to(-104, 8)
    ctx.curve_to(-122, -95, -40, -150, 20, -138)
    ctx.curve_to(80, -128, 112, -86, 108, -52)
    ctx.curve_to(60, -60, -30, -42, -104, 8)
    ctx.close_path()
    fs(ctx, color, lw=LW)
    # dark side panel
    ctx.save()
    ctx.move_to(-104, 8)
    ctx.curve_to(-122, -95, -40, -150, 20, -138)
    ctx.curve_to(-50, -120, -84, -60, -88, -2)
    ctx.close_path()
    setc(ctx, dark)
    ctx.fill()
    # highlight stripe
    ctx.move_to(-20, -60)
    ctx.curve_to(-10, -110, 30, -134, 50, -132)
    ctx.curve_to(10, -118, -2, -90, -6, -60)
    setc(ctx, light)
    ctx.fill()
    ctx.restore()
    # redraw outline of dome
    ctx.move_to(-104, 8)
    ctx.curve_to(-122, -95, -40, -150, 20, -138)
    ctx.curve_to(80, -128, 112, -86, 108, -52)
    ctx.curve_to(60, -60, -30, -42, -104, 8)
    fs(ctx, None, lw=LW)
    # button
    ellipse(ctx, 10, -144, 12, 9)
    fs(ctx, color, lw=5)
    # brim
    ctx.move_to(40, -66)
    ctx.curve_to(90, -92, 150, -100, 172, -84)
    ctx.curve_to(186, -72, 170, -46, 140, -38)
    ctx.curve_to(120, -34, 108, -44, 104, -50)
    ctx.curve_to(84, -58, 60, -62, 40, -66)
    ctx.close_path()
    fs(ctx, dark, lw=LW)


def cap_alone(ctx, x, y, s, rot=0.0, color=RED):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    # inner shadow of the opening
    ellipse(ctx, -2, -10, 100, 22)
    fs(ctx, (0.45, 0.06, 0.08), lw=5)
    draw_cap(ctx, color)
    ctx.restore()


def doodle_auto_blink(t, seed=0):
    """natural blink amount for time t."""
    period = 3.1 + (seed % 3) * 0.7
    ph = (t + seed * 0.77) % period
    return 1.0 if ph < 0.12 else 0.0


# ---------------------------------------------------------------- props
def stone(ctx, x, y, r, seed=0, c=(0.78, 0.76, 0.72)):
    rnd = random.Random(seed)
    pts = []
    for i in range(8):
        a = i * math.pi / 4 + rnd.random() * 0.3
        rr = r * (0.8 + rnd.random() * 0.3)
        pts.append((x + math.cos(a) * rr * 1.2, y + math.sin(a) * rr * 0.85))
    poly(ctx, pts)
    fs(ctx, c, lw=4)


def basket(ctx, x, y, s=1.0, stones=5):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for i in range(stones):
        stone(ctx, -45 + (i % 4) * 30, -30 - (i // 4) * 22, 22, seed=i)
    ctx.move_to(-75, -30)
    ctx.line_to(75, -30)
    ctx.line_to(55, 40)
    ctx.line_to(-55, 40)
    ctx.close_path()
    fs(ctx, hexc("#c99a5b"), lw=6)
    for i in range(1, 4):
        line(ctx, -75 + i * 5, -30 + i * 17, 75 - i * 5, -30 + i * 17, 3, hexc("#8a6235"))
    ctx.restore()


def apple(ctx, x, y, r, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.move_to(0, -r * 0.7)
    ctx.curve_to(r * 0.9, -r * 1.2, r * 1.35, -r * 0.1, r * 0.9, r * 0.7)
    ctx.curve_to(r * 0.6, r * 1.15, r * 0.15, r * 1.0, 0, r * 0.9)
    ctx.curve_to(-r * 0.15, r * 1.0, -r * 0.6, r * 1.15, -r * 0.9, r * 0.7)
    ctx.curve_to(-r * 1.35, -r * 0.1, -r * 0.9, -r * 1.2, 0, -r * 0.7)
    fs(ctx, (0.88, 0.12, 0.15), lw=max(3, r * 0.14))
    ellipse(ctx, -r * 0.45, -r * 0.2, r * 0.18, r * 0.3)
    setc(ctx, WHITE, 0.6)
    ctx.fill()
    line(ctx, 0, -r * 0.7, r * 0.15, -r * 1.25, max(3, r * 0.12), hexc("#5a3a1a"))
    ctx.move_to(r * 0.12, -r * 1.0)
    ctx.curve_to(r * 0.5, -r * 1.4, r * 0.9, -r * 1.2, r * 0.95, -r * 1.05)
    ctx.curve_to(r * 0.6, -r * 0.85, r * 0.3, -r * 0.9, r * 0.12, -r * 1.0)
    fs(ctx, (0.35, 0.7, 0.25), lw=max(2, r * 0.08))
    ctx.restore()


def petri(ctx, x, y, r, t=0.0, germs=1.0, mould=0.0, halo=0.0, lid=0.0, seed=4, germ_faces=True):
    """petri dish seen from above with bacteria colonies and optional mould."""
    ctx.save()
    ctx.translate(x, y)
    circle(ctx, 0, 0, r)
    fs(ctx, (0.93, 0.96, 0.97), lw=max(4, r * 0.03))
    circle(ctx, 0, 0, r * 0.93)
    fs(ctx, (0.98, 0.90, 0.62), lw=max(2, r * 0.012))
    rnd = random.Random(seed)
    hr = r * 0.62 * halo
    for i in range(70):
        a = rnd.random() * 2 * math.pi
        d = math.sqrt(rnd.random()) * r * 0.82
        gx, gy = math.cos(a) * d, math.sin(a) * d
        gr = r * (0.035 + rnd.random() * 0.035)
        dist = math.hypot(gx - r * 0.05, gy + r * 0.05)
        vis = germs
        dead = False
        if halo > 0 and dist < hr:
            dead = True
            vis *= clamp(1 - (hr - dist) / (r * 0.12))
        if vis <= 0.02:
            continue
        wob = math.sin(t * 6 + i) * gr * 0.15
        ctx.save()
        ctx.translate(gx, gy + wob)
        circle(ctx, 0, 0, gr * vis)
        fs(ctx, (0.95, 0.75, 0.15) if not dead else (0.8, 0.7, 0.4), lw=max(1.5, gr * 0.18))
        if germ_faces and gr * vis > 9:
            k = gr * vis
            if dead:
                for sx in (-1, 1):
                    line(ctx, sx * k * 0.35 - k * 0.12, -k * 0.25, sx * k * 0.35 + k * 0.12, -k * 0.05, max(1.5, k * 0.1))
                    line(ctx, sx * k * 0.35 - k * 0.12, -k * 0.05, sx * k * 0.35 + k * 0.12, -k * 0.25, max(1.5, k * 0.1))
            else:
                line(ctx, -k * 0.5, -k * 0.35, -k * 0.15, -k * 0.2, max(1.5, k * 0.1))
                line(ctx, k * 0.5, -k * 0.35, k * 0.15, -k * 0.2, max(1.5, k * 0.1))
                circle(ctx, -k * 0.3, -k * 0.05, k * 0.09)
                circle(ctx, k * 0.3, -k * 0.05, k * 0.09)
                setc(ctx, INK)
                ctx.fill()
                ctx.move_to(-k * 0.3, k * 0.35)
                ctx.curve_to(-k * 0.1, k * 0.2, k * 0.1, k * 0.2, k * 0.3, k * 0.35)
                setc(ctx, INK)
                ctx.set_line_width(max(1.5, k * 0.09))
                ctx.stroke()
        ctx.restore()
    if mould > 0:
        mr = r * 0.32 * mould
        rnd2 = random.Random(9)
        for i in range(40):
            a = rnd2.random() * 2 * math.pi
            d = rnd2.random() * mr * 0.8
            circle(ctx, r * 0.05 + math.cos(a) * d, -r * 0.05 + math.sin(a) * d, mr * (0.25 + rnd2.random() * 0.25))
            setc(ctx, lerpc((0.25, 0.6, 0.55), (0.55, 0.8, 0.6), rnd2.random()), 0.85)
            ctx.fill()
        for i in range(24):
            a = i * 2 * math.pi / 24 + t * 0.3
            ctx.move_to(r * 0.05 + math.cos(a) * mr * 0.8, -r * 0.05 + math.sin(a) * mr * 0.8)
            ctx.line_to(r * 0.05 + math.cos(a) * mr * 1.1, -r * 0.05 + math.sin(a) * mr * 1.1)
        setc(ctx, (0.85, 0.95, 0.9), 0.8)
        ctx.set_line_width(max(2, r * 0.012))
        ctx.stroke()
    if lid > 0:
        circle(ctx, lid * r * 0.25, -lid * r * 0.1, r * 1.03)
        setc(ctx, (0.85, 0.95, 1.0), 0.28)
        ctx.fill_preserve()
        setc(ctx, (0.5, 0.65, 0.75), 0.6)
        ctx.set_line_width(max(3, r * 0.02))
        ctx.stroke()
    ctx.restore()


def frame_box(ctx, x, y, w, h, fill=(0.95, 0.92, 0.85), border=hexc("#b8862e"), bw=26):
    rrect(ctx, x - bw, y - bw, w + 2 * bw, h + 2 * bw, 6)
    fs(ctx, border, lw=6)
    rrect(ctx, x - bw * 0.45, y - bw * 0.45, w + bw * 0.9, h + bw * 0.9, 4)
    fs(ctx, tuple(c * 0.85 for c in border), lw=3)
    ctx.rectangle(x, y, w, h)
    fs(ctx, fill, lw=5)
