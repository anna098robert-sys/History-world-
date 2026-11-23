"""Backgrounds and every shot of the film. Each shot: fn(ctx, t, D, cue)
t = local time (s), D = shot duration, cue(text) = time the sentence containing `text` starts
(cue(text, 'end') = when it ends; cue(text, frac=0.5) = part-way through it)."""
import math, random
import cairo
from gfx import *

SKY = hexc("#8fd3f4")
SKY2 = hexc("#d9f1fb")
GRASS = hexc("#7cc36b")
GRASS_D = hexc("#5ea64f")
MARBLE = hexc("#f4efe4")
MARBLE_D = hexc("#d8cfbd")


# ====================================================================== camera
def cam(ctx, cx, cy, z=1.0, rot=0.0, shake=0.0, t=0.0):
    sx = shake * (math.sin(t * 47) + math.sin(t * 31)) * 0.5
    sy = shake * (math.cos(t * 53) + math.sin(t * 37)) * 0.5
    ctx.translate(W / 2 + sx, H / 2 + sy)
    ctx.rotate(rot)
    ctx.scale(max(z, 1e-3), max(z, 1e-3))
    ctx.translate(-cx, -cy)


def caption(ctx, place, year, t, dur=4.0):
    """location card in the lower-left: slides in, holds, slides out."""
    if t < 0 or t > dur + 0.6:
        return
    k = ease_out(prog(t, 0, 0.5)) - ease_in(prog(t, dur, dur + 0.5))
    x = lerp(-700, 70, k)
    ctx.save()
    rrect(ctx, x, 860, 640, 140, 18)
    fs(ctx, (0.08, 0.07, 0.1, 0.82), lw=0)
    ctx.rectangle(x, 860, 14, 140)
    setc(ctx, RED)
    ctx.fill()
    text(ctx, place, x + 40, 905, 46, WHITE, align="left", outline=0, shadow=False)
    text(ctx, year, x + 40, 962, 52, (1, 0.82, 0.3), align="left", outline=0, shadow=False)
    ctx.restore()


def year_counter(ctx, t, D, y0, y1):
    k = ease(prog(t, 0.3, D - 0.4))
    y = int(round(lerp(y0, y1, k)))
    rrect(ctx, W / 2 - 230, 60, 460, 130, 30)
    fs(ctx, (0.05, 0.03, 0.1, 0.75), lw=5, stroke=(1, 0.85, 0.4))
    text(ctx, str(y), W / 2, 125, 96, (1, 0.88, 0.4), outline=0, shadow=False)


# ====================================================================== backgrounds
def museum_bg(ctx, t, rain=True, light=1.0, paintings="plain"):
    vgrad(ctx, -600, -300, 3200, 1100, hexc("#efe2c8"), hexc("#e2d0ae"))
    # wainscot + floor
    vgrad(ctx, -600, 760, 3200, 500, hexc("#9b6b43"), hexc("#7a5132"))
    for i in range(-6, 40):
        line(ctx, i * 120 - 600, 780, i * 160 - 900, 1500, 3, hexc("#6a4428"), 0.6)
    line(ctx, -600, 780, 2600, 780, 6)
    ctx.rectangle(-600, 690, 3200, 90)
    fs(ctx, hexc("#d8c39c"), lw=5)
    # columns
    for cx in (-300, 2200, 2900):
        ctx.rectangle(cx - 55, -100, 110, 790)
        fs(ctx, MARBLE, lw=6)
        for k in (-28, 0, 28):
            line(ctx, cx + k, -80, cx + k, 670, 3, MARBLE_D)
        ctx.rectangle(cx - 75, 640, 150, 50)
        fs(ctx, MARBLE_D, lw=6)
        ctx.rectangle(cx - 75, -110, 150, 50)
        fs(ctx, MARBLE_D, lw=6)
    # tall window with rain
    wx, wy, ww, wh = 100, 90, 420, 520
    ctx.save()
    rrect(ctx, wx, wy, ww, wh, 200)
    ctx.clip()
    vgrad(ctx, wx, wy, ww, wh, hexc("#55697d"), hexc("#8a9aa8"))
    if rain:
        rnd = random.Random(7)
        for i in range(70):
            rx = wx + rnd.random() * ww
            ry = wy + ((rnd.random() * wh + t * 900 * (0.8 + rnd.random() * 0.4)) % wh)
            line(ctx, rx, ry, rx - 8, ry + 34, 2.5, (0.85, 0.9, 1.0), 0.7)
    ctx.restore()
    rrect(ctx, wx, wy, ww, wh, 200)
    fs(ctx, None, lw=10)
    line(ctx, wx + ww / 2, wy, wx + ww / 2, wy + wh, 8)
    line(ctx, wx, wy + wh * 0.55, wx + ww, wy + wh * 0.55, 8)
    # paintings
    if paintings == "plain":
        frame_box(ctx, 900, 180, 300, 220, fill=hexc("#7fa3b8"))
        ctx.move_to(900, 330); ctx.curve_to(980, 270, 1060, 300, 1200, 260); ctx.line_to(1200, 400); ctx.line_to(900, 400)
        fs(ctx, hexc("#6d8f4e"), lw=0)
        circle(ctx, 1130, 230, 28); fs(ctx, (1, 0.9, 0.5), lw=0)
        frame_box(ctx, 1320, 200, 220, 280, fill=hexc("#3b2f2a"))
        circle(ctx, 1430, 310, 60); fs(ctx, hexc("#e9d3b4"), lw=3)
        ctx.rectangle(1360, 380, 140, 100); fs(ctx, hexc("#5a3c2a"), lw=0)


def ac_vent(ctx, x, y, t, on=True):
    rrect(ctx, x - 130, y - 40, 260, 80, 12)
    fs(ctx, hexc("#d9dde2"), lw=6)
    for i in range(5):
        line(ctx, x - 110, y - 26 + i * 13, x + 110, y - 26 + i * 13, 3, hexc("#8a9099"))
    if on:
        for i in range(4):
            ph = (t * 1.3 + i * 0.25) % 1
            yy = y + 60 + ph * 220
            ctx.move_to(x - 90 + i * 55, yy)
            ctx.curve_to(x - 70 + i * 55, yy + 30, x - 110 + i * 55, yy + 60, x - 90 + i * 55, yy + 90)
            setc(ctx, (0.6, 0.85, 1.0), 0.8 * (1 - ph))
            ctx.set_line_width(5)
            ctx.stroke()


def glass_case(ctx, x, y, t, glow=0.5, spin=0.0, sign=True, open_=0.0):
    # pedestal
    ctx.rectangle(x - 150, y + 60, 300, 340)
    fs(ctx, MARBLE, lw=6)
    ctx.rectangle(x - 175, y + 50, 350, 40)
    fs(ctx, MARBLE_D, lw=6)
    ctx.rectangle(x - 175, y + 380, 350, 40)
    fs(ctx, MARBLE_D, lw=6)
    # velvet cushion + watch
    ellipse(ctx, x, y + 40, 120, 26)
    fs(ctx, hexc("#7a1e3a"), lw=5)
    pocket_watch(ctx, x + 10, y - 40, 62, t, glow=glow, spin=spin)
    # glass box
    ctx.save()
    ctx.translate(0, -open_ * 420)
    ctx.rectangle(x - 160, y - 220, 320, 270)
    setc(ctx, (0.8, 0.95, 1.0), 0.18)
    ctx.fill_preserve()
    setc(ctx, (0.35, 0.5, 0.6), 0.9)
    ctx.set_line_width(5)
    ctx.stroke()
    poly(ctx, [(x - 120, y - 200), (x - 60, y - 200), (x - 140, y + 20), (x - 155, y + 20)])
    setc(ctx, WHITE, 0.35)
    ctx.fill()
    ctx.restore()
    if sign:
        ctx.save()
        ctx.translate(x + 230, y + 150)
        ctx.rotate(0.04)
        rrect(ctx, -110, -70, 220, 140, 10)
        fs(ctx, hexc("#fffaf0"), lw=5)
        text(ctx, "DO NOT", 0, -36, 34, RED, outline=0, shadow=False)
        text(ctx, "TOUCH", 0, 2, 38, RED, outline=0, shadow=False)
        text(ctx, "origin unknown", 0, 42, 30, INK, font=HAND_FONT, outline=0, shadow=False)
        line(ctx, 0, 70, 0, 230, 8)
        ctx.restore()


def sky_bg(ctx, t, top=SKY, bot=SKY2, sun=(1650, 170), clouds=True, cl_y=(150, 260, 120)):
    vgrad(ctx, -800, -600, 3600, 1500, top, bot)
    if sun:
        g = cairo.RadialGradient(sun[0], sun[1], 40, sun[0], sun[1], 260)
        g.add_color_stop_rgba(0, 1, 0.95, 0.6, 0.8)
        g.add_color_stop_rgba(1, 1, 0.95, 0.6, 0)
        ctx.set_source(g)
        circle(ctx, sun[0], sun[1], 260)
        ctx.fill()
        circle(ctx, sun[0], sun[1], 80)
        fs(ctx, (1, 0.87, 0.35), lw=6)
    if clouds:
        for i, cy in enumerate(cl_y):
            cx = ((i * 700 + t * (18 + i * 6)) % 3200) - 700
            cloud(ctx, cx, cy, 1.0 - i * 0.15)


def cloud(ctx, x, y, s=1.0, c=WHITE):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(max(s, 1e-3), max(s, 1e-3))
    for dx, dy, r in ((-80, 10, 50), (-20, -20, 70), (60, 0, 55), (110, 20, 38)):
        circle(ctx, dx, dy, r)
    ctx.rectangle(-130, 10, 270, 48)
    setc(ctx, c, 0.95)
    ctx.fill()
    ctx.restore()


def hills(ctx, y, c1, c2, t=0.0, seed=1, amp=60):
    rnd = random.Random(seed)
    ph = rnd.random() * 6
    ctx.move_to(-900, 1500)
    for i in range(0, 41):
        x = -900 + i * 100
        ctx.line_to(x, y - amp * (0.5 + 0.5 * math.sin(i * 0.45 + ph)) - 20 * math.sin(i * 1.3 + ph))
    ctx.line_to(3300, 1500)
    ctx.close_path()
    fs(ctx, c1, lw=5)


def cypress(ctx, x, y, h):
    ellipse(ctx, x, y - h / 2, h * 0.14, h / 2)
    fs(ctx, hexc("#3e6e3a"), lw=5)


def pisa_tower(ctx, x, y, t, floors=3, lean=0.0, scaffold=True, s=1.0, dot=False):
    """tower base centre at (x,y). lean in degrees (positive = to the right)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(math.radians(lean))
    ctx.scale(max(s, 1e-3), max(s, 1e-3))
    fw, fh = 300, 112
    # base storey taller
    for i in range(floors):
        top = -fh * (i + 1) - 40
        h = fh + (40 if i == 0 else 0)
        yy = top
        ctx.rectangle(-fw / 2, yy, fw, h if i else fh + 40)
        fs(ctx, MARBLE, lw=6)
        # gallery arches
        n = 6
        for j in range(n):
            ax = -fw / 2 + 14 + j * (fw - 28) / n
            aw = (fw - 28) / n - 10
            ctx.new_sub_path()
            ctx.move_to(ax, yy + h - 10)
            ctx.line_to(ax, yy + 34)
            ctx.arc(ax + aw / 2, yy + 34, aw / 2, math.pi, 0)
            ctx.line_to(ax + aw, yy + h - 10)
            ctx.close_path()
            fs(ctx, hexc("#9b9282"), lw=4)
            line(ctx, ax + aw + 5, yy + 20, ax + aw + 5, yy + h - 8, 4, MARBLE_D)
        ctx.rectangle(-fw / 2 - 12, yy - 8, fw + 24, 16)
        fs(ctx, MARBLE_D, lw=5)
    if floors >= 8:
        # bell chamber
        yy = -fh * floors - 40 - 90
        ctx.rectangle(-fw * 0.36, yy, fw * 0.72, 90)
        fs(ctx, MARBLE, lw=6)
        for j in range(4):
            ax = -fw * 0.32 + j * fw * 0.17
            rrect(ctx, ax, yy + 18, fw * 0.1, 60, 18)
            fs(ctx, hexc("#9b9282"), lw=4)
        if dot:
            circle(ctx, 0, yy - 22, 16)
            fs(ctx, RED, lw=4)
    if scaffold and floors < 8:
        top = -fh * floors - 40
        for sx in (-fw / 2 - 40, fw / 2 + 40):
            line(ctx, sx, 0, sx, top - 80, 9, hexc("#8a5a2b"))
            for k in range(0, floors + 1):
                line(ctx, sx - 30, -k * fh - 20, sx + 30, -k * fh - 20, 7, hexc("#8a5a2b"))
        line(ctx, -fw / 2 - 40, top - 60, fw / 2 + 40, top - 60, 7, hexc("#8a5a2b"))
    ctx.restore()


def pisa_bg(ctx, t, ground_y=820):
    sky_bg(ctx, t)
    hills(ctx, 640, hexc("#a9c98a"), None, seed=2, amp=80)
    for x in (-200, 60, 250, 1400, 1750, 2100):
        cypress(ctx, x, 700, 200)
    # city wall + houses
    for i, hx in enumerate(range(-500, 2600, 230)):
        hh = 140 + (i * 37) % 80
        ctx.rectangle(hx, ground_y - hh, 200, hh)
        fs(ctx, [hexc("#e8b98a"), hexc("#f0cf9c"), hexc("#d99b6c")][i % 3], lw=5)
        poly(ctx, [(hx - 12, ground_y - hh), (hx + 100, ground_y - hh - 60), (hx + 212, ground_y - hh)])
        fs(ctx, hexc("#b8553a"), lw=5)
        rrect(ctx, hx + 80, ground_y - hh + 40, 40, 56, 18)
        fs(ctx, hexc("#5a3a2a"), lw=4)
    ctx.rectangle(-900, ground_y, 3800, 600)
    fs(ctx, hexc("#d8c08a"), lw=6)
    ctx.rectangle(-900, ground_y + 70, 3800, 600)
    fs(ctx, hexc("#9fc77e"), lw=0)


def england_bg(ctx, t, ground_y=850):
    sky_bg(ctx, t, top=hexc("#9cc9e6"), bot=hexc("#e4f1f7"), sun=(300, 160))
    hills(ctx, 640, hexc("#8fc27a"), None, seed=5, amp=90)
    hills(ctx, 760, hexc("#74b062"), None, seed=8, amp=60)
    # manor house
    hx, hy = 1250, ground_y
    ctx.rectangle(hx, hy - 260, 460, 260)
    fs(ctx, hexc("#cfc3a8"), lw=6)
    for k, gx in enumerate((hx, hx + 230)):
        poly(ctx, [(gx - 10, hy - 260), (gx + 115, hy - 380), (gx + 240, hy - 260)])
        fs(ctx, hexc("#cfc3a8"), lw=6)
        rrect(ctx, gx + 85, hy - 330, 60, 50, 6)
        fs(ctx, hexc("#3c4a5a"), lw=5)
    for k in range(4):
        ctx.rectangle(hx + 30 + k * 110, hy - 200, 60, 80)
        fs(ctx, hexc("#3c4a5a"), lw=5)
        line(ctx, hx + 60 + k * 110, hy - 200, hx + 60 + k * 110, hy - 120, 3)
    rrect(ctx, hx + 200, hy - 110, 70, 110, 30)
    fs(ctx, hexc("#6b4428"), lw=5)
    ctx.rectangle(hx + 400, hy - 440, 40, 90)
    fs(ctx, hexc("#a89a80"), lw=5)
    for k in range(3):
        ph = (t * 0.4 + k / 3) % 1
        circle(ctx, hx + 420 + ph * 60, hy - 460 - ph * 160, 20 + ph * 25)
        setc(ctx, (0.9, 0.9, 0.9), 0.6 * (1 - ph))
        ctx.fill()
    ctx.rectangle(-900, ground_y, 3800, 600)
    fs(ctx, hexc("#6fb05c"), lw=6)
    # fence
    for fxp in range(-600, 1200, 90):
        line(ctx, fxp, ground_y - 70, fxp, ground_y + 5, 7, hexc("#8a5a2b"))
    line(ctx, -600, ground_y - 55, 1200, ground_y - 55, 6, hexc("#8a5a2b"))
    line(ctx, -600, ground_y - 25, 1200, ground_y - 25, 6, hexc("#8a5a2b"))


def sheep(ctx, x, y, t, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(max(s, 1e-3), max(s, 1e-3))
    for dx in (-30, 30):
        line(ctx, dx, 20, dx, 60, 8)
    for dx, dy, r in ((-40, 0, 35), (0, -15, 40), (40, 0, 35), (0, 15, 38)):
        circle(ctx, dx, dy, r)
    setc(ctx, WHITE)
    ctx.fill()
    for dx, dy, r in ((-40, 0, 35), (0, -15, 40), (40, 0, 35), (0, 15, 38)):
        circle(ctx, dx, dy, r)
        fs(ctx, None, lw=5)
    for dx, dy, r in ((-40, 0, 33), (0, -15, 38), (40, 0, 33), (0, 15, 36)):
        circle(ctx, dx, dy, r)
    setc(ctx, WHITE)
    ctx.fill()
    ellipse(ctx, 80, -10 + math.sin(t * 2) * 4, 26, 20)
    fs(ctx, INK, lw=0)
    circle(ctx, 88, -14 + math.sin(t * 2) * 4, 4)
    fs(ctx, WHITE, lw=0)
    ctx.restore()


def apple_tree(ctx, x, y, t, apples=True, top_apple=True, branch_snap=0.0, s=1.0):
    """trunk base at (x,y). returns world pos of top apple."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(max(s, 1e-3), max(s, 1e-3))
    ctx.move_to(-45, 0)
    ctx.curve_to(-30, -150, -40, -300, -20, -420)
    ctx.line_to(30, -420)
    ctx.curve_to(40, -300, 30, -150, 50, 0)
    ctx.close_path()
    fs(ctx, hexc("#7a5130"), lw=6)
    line(ctx, -10, -330, -150, -470, 18, hexc("#7a5130"))
    line(ctx, 15, -350, 170, -480, 18, hexc("#7a5130"))
    sway = math.sin(t * 1.2) * 4
    for dx, dy, r in ((-180, -520, 140), (180, -530, 140), (0, -640, 170), (-90, -760, 120),
                      (110, -760, 120), (0, -470, 130)):
        circle(ctx, dx + sway, dy, r)
    setc(ctx, hexc("#4f9a45"))
    ctx.fill()
    for dx, dy, r in ((-180, -520, 140), (180, -530, 140), (0, -640, 170), (-90, -760, 120),
                      (110, -760, 120)):
        circle(ctx, dx + sway, dy, r)
        fs(ctx, None, lw=6)
    for dx, dy, r in ((-180, -520, 136), (180, -530, 136), (0, -640, 166), (-90, -760, 116),
                      (110, -760, 116), (0, -470, 126)):
        circle(ctx, dx + sway, dy, r)
    setc(ctx, hexc("#5aab4f"))
    ctx.fill()
    for dx, dy, r in ((-60, -700, 60), (120, -560, 50), (-170, -560, 45)):
        circle(ctx, dx + sway, dy, r)
        setc(ctx, hexc("#6dbd5e"))
        ctx.fill()
    if apples:
        for ax, ay in ((-200, -480), (-90, -560), (150, -500), (220, -600), (-150, -680), (60, -700), (30, -540)):
            apple(ctx, ax + sway, ay, 18)
    tp = (40 + sway, -880)
    if top_apple:
        # thin branch to top apple
        line(ctx, 10, -760, 40 + sway, -860, 8, hexc("#7a5130"))
        apple(ctx, tp[0], tp[1], 26)
    ctx.restore()
    return (x + tp[0] * s, y + tp[1] * s)


def london_window(ctx, x, y, w, h, t):
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    vgrad(ctx, x, y, w, h, hexc("#b7c4cc"), hexc("#e3e6df"))
    # skyline
    base = y + h
    for i, (bx, bw, bh) in enumerate(((0, 120, 160), (110, 90, 220), (190, 140, 140), (320, 100, 260), (420, 160, 180))):
        ctx.rectangle(x + bx * w / 560, base - bh * h / 420, bw * w / 560, bh * h / 420)
        setc(ctx, hexc("#7d8790"))
        ctx.fill()
    # Big Ben
    bx = x + w * 0.7
    ctx.rectangle(bx - 22, base - h * 0.85, 44, h * 0.85)
    setc(ctx, hexc("#5f6870"))
    ctx.fill()
    poly(ctx, [(bx - 26, base - h * 0.85), (bx, base - h * 1.0), (bx + 26, base - h * 0.85)])
    ctx.fill()
    circle(ctx, bx, base - h * 0.74, 14)
    setc(ctx, hexc("#e8e2c8"))
    ctx.fill()
    for k in range(4):
        ph = (t * 0.25 + k / 4) % 1
        circle(ctx, x + w * 0.2 + k * 60, base - 150 - ph * 160, 20 + ph * 30)
        setc(ctx, (0.6, 0.6, 0.6), 0.5 * (1 - ph))
        ctx.fill()
    ctx.restore()
    ctx.rectangle(x, y, w, h)
    fs(ctx, None, lw=12, stroke=hexc("#5a3a22"))
    line(ctx, x + w / 2, y, x + w / 2, y + h, 8, hexc("#5a3a22"))
    line(ctx, x, y + h / 2, x + w, y + h / 2, 8, hexc("#5a3a22"))


def lab_bg(ctx, t, dishes=True, cap_on_hook=False, window_open=True):
    vgrad(ctx, -600, -300, 3200, 1400, hexc("#cfd8c4"), hexc("#b8c4ae"))
    ctx.rectangle(-600, 820, 3200, 600)
    fs(ctx, hexc("#6d5a48"), lw=6)
    for i in range(-5, 30):
        line(ctx, i * 140 - 600, 820, i * 140 - 600, 1400, 3, hexc("#56463a"))
    london_window(ctx, 1240, 130, 520, 400, t)
    # shelves with bottles
    for sy in (180, 340):
        ctx.rectangle(80, sy, 700, 22)
        fs(ctx, hexc("#8a5a2b"), lw=5)
        for k in range(7):
            bx = 110 + k * 95
            c = [hexc("#7fb7d6"), hexc("#e2a24c"), hexc("#9ad08a"), hexc("#d27878")][k % 4]
            hh = 70 + (k * 17) % 40
            rrect(ctx, bx, sy - hh, 50, hh, 8)
            fs(ctx, c, lw=4)
            ctx.rectangle(bx + 14, sy - hh - 20, 22, 22)
            fs(ctx, hexc("#e8e2d0"), lw=4)
    # door with coat hook (right)
    ctx.rectangle(1850, 220, 300, 600)
    fs(ctx, hexc("#7a5a3a"), lw=6)
    rrect(ctx, 1890, 280, 220, 220, 8)
    fs(ctx, hexc("#9fb6c4"), lw=5)
    text(ctx, "LAB", 2000, 390, 40, INK, font=HAND_FONT, outline=0, shadow=False)
    circle(ctx, 1880, 560, 10)
    fs(ctx, hexc("#d8b04a"), lw=4)
    line(ctx, 1810, 330, 1830, 330, 8)
    if cap_on_hook:
        cap_alone(ctx, 1810, 400, 0.45, rot=0.25)
    # bench
    ctx.rectangle(-100, 640, 1500, 50)
    fs(ctx, hexc("#3f3a36"), lw=6)
    ctx.rectangle(-60, 690, 1420, 140)
    fs(ctx, hexc("#7a5a3a"), lw=6)
    for k in range(4):
        rrect(ctx, 0 + k * 350, 710, 300, 100, 8)
        fs(ctx, hexc("#8d6a46"), lw=4)
        circle(ctx, 150 + k * 350, 760, 9)
        fs(ctx, hexc("#d8b04a"), lw=3)
    microscope(ctx, 1100, 640)
    if dishes:
        for k, (dx, dy) in enumerate(((300, 625), (420, 618), (540, 625), (360, 600), (480, 596))):
            ellipse(ctx, dx, dy, 55, 14)
            fs(ctx, (0.9, 0.95, 0.97), lw=4)
            ellipse(ctx, dx, dy - 2, 44, 9)
            setc(ctx, (0.98, 0.85, 0.5))
            ctx.fill()


def microscope(ctx, x, y):
    ellipse(ctx, x, y - 10, 90, 18)
    fs(ctx, hexc("#2d3038"), lw=5)
    ctx.move_to(x + 30, y - 20)
    ctx.curve_to(x + 90, y - 120, x + 60, y - 220, x + 10, y - 240)
    setc(ctx, INK)
    ctx.set_line_width(26)
    ctx.stroke()
    ctx.move_to(x + 30, y - 20)
    ctx.curve_to(x + 90, y - 120, x + 60, y - 220, x + 10, y - 240)
    setc(ctx, hexc("#3b404a"))
    ctx.set_line_width(16)
    ctx.stroke()
    ctx.save()
    ctx.translate(x - 10, y - 220)
    ctx.rotate(-0.4)
    rrect(ctx, -22, -90, 44, 170, 10)
    fs(ctx, hexc("#c9ccd2"), lw=5)
    ctx.rectangle(-28, -110, 56, 26)
    fs(ctx, hexc("#3b404a"), lw=5)
    ctx.restore()
    ctx.rectangle(x - 70, y - 90, 120, 16)
    fs(ctx, hexc("#3b404a"), lw=5)


def spores(ctx, t, x0, y0, x1, y1, n=30, a=1.0, seed=11):
    rnd = random.Random(seed)
    for i in range(n):
        ph = (t * (0.15 + rnd.random() * 0.12) + rnd.random()) % 1
        x = lerp(x0, x1, ph) + math.sin(t * 2 + i) * 40
        y = lerp(y0, y1, ph) + math.cos(t * 1.7 + i * 2) * 50
        r = 7 + rnd.random() * 8
        circle(ctx, x, y, r)
        setc(ctx, (0.35, 0.65, 0.55), 0.8 * a * math.sin(ph * math.pi))
        ctx.fill()
        for k in range(5):
            ang = k * 1.256 + t
            line(ctx, x, y, x + math.cos(ang) * r * 1.6, y + math.sin(ang) * r * 1.6, 2,
                 (0.35, 0.65, 0.55), 0.6 * a * math.sin(ph * math.pi))


def card(ctx, x, y, w, h, t, rot, drawer, appear=0.0):
    """a polaroid-style card that flies in at time `appear`."""
    k = back_out(prog(t, appear, appear + 0.5), 1.6)
    if k <= 0:
        return
    ctx.save()
    ctx.translate(lerp(x, x, k), lerp(y + 900, y, k))
    ctx.rotate(rot * k)
    rrect(ctx, -w / 2 - 22, -h / 2 - 22, w + 44, h + 90, 8)
    fs(ctx, hexc("#fbf8f0"), lw=6)
    ctx.save()
    ctx.rectangle(-w / 2, -h / 2, w, h)
    ctx.clip()
    drawer(ctx, w, h)
    ctx.restore()
    ctx.rectangle(-w / 2, -h / 2, w, h)
    fs(ctx, None, lw=4)
    ctx.restore()


# ====================================================================== the doodle guy shorthand
def guy(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t))
    return doodle(ctx, x, y, s, **kw)


def worker(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 2))
    return doodle(ctx, x, y, s, hair="worker", cap=False, body=hexc("#9c7a50"), **kw)


def newton(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 1))
    kw.setdefault("body", hexc("#4b3b5c"))

    def collar(c, part, *a):
        if part == "body":
            poly(c, [(-30, 78), (0, 120), (30, 78)])
            fs(c, WHITE, lw=4)
    return doodle(ctx, x, y, s, hair="newton", cap=False, extra=collar, **kw)


def fleming(ctx, x, y, s, t, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, 4))

    def coat(c, part, *a):
        if part == "body":
            poly(c, [(-44, 80), (-8, 190), (-30, 80)], close=True)
            fs(c, hexc("#e9edf0"), lw=4)
            poly(c, [(44, 80), (8, 190), (30, 80)], close=True)
            fs(c, hexc("#e9edf0"), lw=4)
            line(c, 0, 190, 0, 330, 4)
            for yy in (220, 270):
                circle(c, 12, yy, 5)
                fs(c, INK, lw=0)
    return doodle(ctx, x, y, s, hair="fleming", cap=False, glasses=True, bowtie=hexc("#2f4f8f"),
                  extra=coat, **kw)


# ====================================================================== SHOTS
def sh_hook(ctx, t, D, cue):
    spiral_bg(ctx, t, (0.12, 0.08, 0.14), (0.17, 0.11, 0.2), speed=0.15)
    z = 1 + t * 0.012
    ctx.save()
    cam(ctx, W / 2, H / 2, z)
    t1, t2, t3 = cue("tower"), cue("apple"), cue("mould")
    t_my = cue("My accidents")

    def tower_pic(c, w, h):
        vgrad(c, -w / 2, -h / 2, w, h, SKY, SKY2)
        c.rectangle(-w / 2, h * 0.3, w, h)
        fs(c, GRASS, lw=0)
        pisa_tower(c, 0, h * 0.32, t, floors=8, lean=4 * ease(prog(t, t1 + 0.3, t1 + 1.5)), scaffold=False, s=0.32)

    def apple_pic(c, w, h):
        vgrad(c, -w / 2, -h / 2, w, h, hexc("#bfe3c0"), hexc("#e8f5e0"))
        yy = lerp(-h * 0.35, h * 0.2, ease_in(prog(t, t2 + 0.3, t2 + 1.0)))
        apple(c, 0, yy, 50)
        if prog(t, t2 + 0.3, t2 + 1.0) < 1:
            motion_lines(c, -40, yy - 140, 80, 100, 3, vertical=True)

    def dish_pic(c, w, h):
        vgrad(c, -w / 2, -h / 2, w, h, hexc("#d8e4ee"), hexc("#f4f7fa"))
        petri(c, 0, 0, 125, t, mould=ease(prog(t, t3, t3 + 1.5)), halo=ease(prog(t, t3 + 0.5, t3 + 2.2)))

    k_shrink = ease(prog(t, t_my - 0.3, t_my + 0.4))
    sx = lerp(1, 0.8, k_shrink)
    for (cx, cy, rot, dr, ap) in ((420, 470, -0.08, tower_pic, t1), (960, 450, 0.05, apple_pic, t2),
                                   (1500, 470, -0.04, dish_pic, t3)):
        ctx.save()
        spread = {420: -140, 960: 0, 1500: 140}[cx]
        fly = -1100 * ease_in(k_shrink) if cx == 960 else 0
        ctx.translate(cx + spread * k_shrink, cy + fly)
        ctx.scale(max(sx, 1e-3), max(sx, 1e-3))
        ctx.translate(-cx, -cy + lerp(0, -60, k_shrink))
        card(ctx, cx, cy, 380, 380, t, rot, dr, appear=ap)
        ctx.restore()
    # caption words under cards
    for cx, word, ap in ((420, "LEANS", t1), (960, "FALLS", t2), (1500, "SAVES", t3)):
        pop_text(ctx, word, cx, 790, 60, t - ap - 0.4, (1, 0.85, 0.3), hold=t_my - ap - 0.6)
    if t > t_my - 0.4:
        k = back_out(prog(t, t_my - 0.4, t_my + 0.2), 1.8)
        guy(ctx, 960, lerp(1500, 690, k), 0.95, t, expr="sly", face=0.2, look=(0.4, 0),
            larm=(0.3, 0.2), rarm=(-2.3, 0.9))
        pop_text(ctx, "MY ACCIDENTS.", 960, 180, 110, t - t_my - 0.5, RED, rot=-0.04)
    ctx.restore()


def sh_title(ctx, t, D, cue):
    spiral_bg(ctx, t, speed=0.35)
    for i in range(8):
        a = i * 0.785 + t * 0.4
        r = 620 + 40 * math.sin(t + i)
        clock_icon(ctx, W / 2 + math.cos(a) * r, H / 2 + math.sin(a) * r * 0.62, 50, t + i, rot=a)
    words = [("I", RED), ("ACCIDENTALLY", WHITE)]
    w2 = [("CHANGED", WHITE), ("HISTORY", (1, 0.82, 0.25))]
    def row(ws, y, size, t0):
        total = sum(text_width(ctx, w, size) for w, _ in ws) + 40 * (len(ws) - 1)
        x = W / 2 - total / 2
        for i, (w, c) in enumerate(ws):
            ww = text_width(ctx, w, size)
            tt = t - t0 - i * 0.18
            if tt > 0:
                k = back_out(tt / 0.45, 2.4) if tt < 0.45 else 1
                ctx.save()
                ctx.translate(x + ww / 2, y)
                ctx.scale(max(k, 1e-3), max(k, 1e-3))
                ctx.rotate(-0.03 + 0.01 * math.sin(t * 3 + i))
                text(ctx, w, 0, 0, size, c, outline=14)
                ctx.restore()
            x += ww + 40
    row(words, 420, 150, 0.2)
    row(w2, 600, 170, 0.6)
    k = ease_out(prog(t, 1.2, 1.8))
    if k > 0:
        guy(ctx, 1650, lerp(1500, 820, k), 0.75, t, expr="grin", face=-0.3, larm=(2.6, -0.3), rarm=(-0.3, 0))
        cap_alone  # noqa
    text(ctx, "HISTORY WORLD", W / 2, 930, 48, WHITE, font=HAND_FONT, outline=6, alpha=ease(prog(t, 1.5, 2.2)))


def sh_cap(ctx, t, D, cue):
    spiral_bg(ctx, t)
    t_red = cue("Red."),
    t_red = cue("Red.")
    t_big = cue("Slightly")
    t_rem = cue("Remember")
    z = lerp(1.0, 1.25, ease(prog(t, 0, D)))
    ctx.save()
    cam(ctx, 960, 560, z)
    cd = 0.0
    if t > t_big:
        cd = ease_out(prog(t, t_big + 0.2, t_big + 0.5)) - ease(prog(t, t_big + 1.4, t_big + 1.9))
    push = t_big + 1.3 < t < t_big + 2.0
    guy(ctx, 960, 560, 1.7, t, expr="smile" if not push else "flat", face=0.85, cap_down=cd,
        larm=(0.15, 0.05), rarm=(-0.15 if not push else -2.6, -0.05 if not push else 1.1),
        look=(0, -0.5) if cd > 0.5 else (0, 0))
    ctx.restore()
    if t > t_red:
        # arrow + label
        k = ease_out(prog(t, t_red, t_red + 0.4))
        ctx.save()
        setc(ctx, (1, 0.9, 0.3))
        ctx.set_line_width(10)
        ctx.move_to(1500, 230)
        ctx.curve_to(1450, 180, 1350, 200, lerp(1500, 1250, k), lerp(230, 280, k))
        ctx.stroke()
        ctx.restore()
        pop_text(ctx, "RED.", 1580, 210, 110, t - t_red, RED, rot=0.08)
    if t > t_big:
        pop_text(ctx, "slightly too big", 1550, 340, 64, t - t_big, WHITE, font=HAND_FONT, outline=6)
    if t > t_rem:
        k = (t - t_rem)
        a = 0.5 + 0.5 * math.sin(k * 8)
        ctx.save()
        ellipse(ctx, 1020, 330, 380 + 10 * a, 200 + 8 * a)
        setc(ctx, (1, 0.9, 0.3), 0.9)
        ctx.set_line_width(12)
        ctx.set_dash([40, 22])
        ctx.stroke()
        ctx.restore()
        pop_text(ctx, "REMEMBER IT!", 960, 980, 90, k, (1, 0.85, 0.25), rot=-0.03)


def sh_museum(ctx, t, D, cue):
    t_ac = cue("The air")
    t_saw = cue("Then I saw")
    t_sign = cue("The sign")
    # camera pans from entrance to the glass case
    pan = ease(prog(t, t_saw - 0.6, t_saw + 1.4))
    cx = lerp(820, 1500, pan)
    z = lerp(1.0, 1.15, ease(prog(t, t_sign - 0.5, t_sign + 1)))
    cy = lerp(540, 470, ease(prog(t, t_sign - 0.5, t_sign + 1)))
    ctx.save()
    cam(ctx, cx, cy, z)
    museum_bg(ctx, t)
    ac_vent(ctx, 700, 60, t, on=True)
    glass_case(ctx, 1750, 430, t, glow=0.4 + 0.3 * math.sin(t * 3))
    # guy walks in, stops under the vent, enjoys the AC, then walks to the case
    if t < t_ac:
        gx = lerp(-150, 700, ease_out(prog(t, 0, max(0.1, t_ac - 0.2))))
        walk = t * 1.6 if gx < 690 else None
        guy(ctx, gx, 470, 0.85, t, expr="smile", face=0.9, walk=walk, larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    elif t < t_saw:
        tt = t - t_ac
        guy(ctx, 700, 470, 0.85, t, expr="happy", face=0.0, look=(0, -1), larm=(2.5, 0.3), rarm=(-2.5, -0.3),
            tilt=0.05 * math.sin(tt * 2))
        pop_text(ctx, "ahhh...", 900, 260, 60, tt - 0.3, WHITE, font=HAND_FONT, outline=5)
    else:
        tt = t - t_saw
        gx = lerp(700, 1380, ease(prog(tt, 0.3, 2.3)))
        walking = 0.3 < tt < 2.3
        guy(ctx, gx, 470, 0.85, t, expr="o" if tt < 0.8 else "smile", face=0.9, look=(1, 0),
            walk=(t * 1.6 if walking else None), larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        if tt < 1.0:
            pop_text(ctx, "!", gx + 40, 280, 110, tt, (1, 0.85, 0.2))
    if t > t_saw + 1.0:
        sparkle(ctx, 1720, 360, 40, t)
        sparkle(ctx, 1810, 420, 26, t + 1)
    ctx.restore()
    vignette(ctx, 0.35)


def sh_touch(ctx, t, D, cue):
    ctx.save()
    z = lerp(1.6, 2.1, ease(prog(t, 0, D)))
    cam(ctx, 1640, 420, z)
    museum_bg(ctx, t)
    glass_case(ctx, 1750, 430, t, glow=0.5 + 0.5 * ease(prog(t, D * 0.6, D)), open_=ease(prog(t, 0.1, 0.8)),
               spin=0)
    reach = ease(prog(t, D * 0.35, D * 0.8))
    guy(ctx, 1560, 400, 1.0, t, expr="sly" if t < D * 0.5 else "grin", face=0.9, look=(1, 0.3),
        larm=(0.3, 0.2), rarm=(lerp(-0.3, -2.25, reach), lerp(-0.2, 0.15, reach)))
    if t > D * 0.78:
        sparkle(ctx, 1760, 390, 70, t, (1, 1, 0.7))
    ctx.restore()
    vignette(ctx, 0.45)


def sh_tunnel(y0, y1, hue=(0.55, 0.15, 0.75), hue2=(0.95, 0.45, 0.15), slow=False):
    def f(ctx, t, D, cue):
        sp = 2.0 * (1 - ease(prog(t, 0, D)) if slow else 1)
        vortex(ctx, t * (0.6 if slow else 1), hue, hue2, speed=sp + 0.05)
        rnd = random.Random(5)
        for i in range(10):
            ph = (t * 0.35 * (0.3 if slow else 1) + i / 10) % 1
            a = rnd.random() * 6.28 + t * 0.3
            r = 60 + ph ** 2 * 1300
            clock_icon(ctx, W / 2 + math.cos(a) * r, H / 2 + math.sin(a) * r * 0.7, 10 + ph * 70,
                       t * (0 if slow and t > D * 0.8 else 1), back=y1 < y0, rot=t + i)
        # guy tumbling through
        sc = 0.55 + 0.1 * math.sin(t * 2)
        rot = t * (2.5 if not slow else 2.5 * (1 - ease(prog(t, 0, D))))
        ctx.save()
        ctx.translate(W / 2 + 260 * math.sin(t * 0.9), H / 2 + 120 * math.cos(t * 1.3) - 60)
        ctx.rotate(rot)
        doodle(ctx, 0, -150, sc, expr="shock" if not slow else "worried", face=0, larm=(2.4, 0.5),
               rarm=(-2.4, -0.5), legs=(0.5, -0.5))
        ctx.restore()
        year_counter(ctx, t, D, y0, y1)
        vignette(ctx, 0.6)
    return f


def sh_pisa_arrive(ctx, t, D, cue):
    t_pisa = cue("Pisa.")
    t_work = cue("Workers")
    t_three = cue("Only three")
    t_straight = cue("Perfectly")
    tilt = 1 - ease(prog(t, 0, 3.0))
    cx = lerp(600, 1250, ease(prog(t, t_work - 0.5, t_work + 2)))
    z = lerp(0.95, 1.12, ease(prog(t, t_three, D)))
    ctx.save()
    cam(ctx, cx, lerp(200, 520, ease(prog(t, 0, 3.0))), z)
    pisa_bg(ctx, t)
    pisa_tower(ctx, 1450, 830, t, floors=3, lean=0)
    # workers moving stones around the base
    for i, (wx0, wx1, ph) in enumerate(((1150, 1300, 0.0), (1780, 1650, 0.4))):
        k = 0.5 + 0.5 * math.sin(t * 0.9 + ph * 6)
        wx = lerp(wx0, wx1, k)
        worker(ctx, wx, 560, 0.55, t, face=0.8 if wx1 > wx0 else -0.8, walk=t * 1.2 + ph,
               larm=(0.6, 1.4), rarm=(-0.6, -1.4))
        basket(ctx, wx + (40 if wx1 > wx0 else -40), 650, 0.5)
    # guy lands, dizzy
    land = ease_in(prog(t, 0.2, 0.9))
    gy = lerp(-300, 520, land)
    sq = -0.18 * math.exp(-max(0, t - 0.9) * 6) * (1 if t > 0.9 else 0)
    dizzy = 0.9 < t < t_pisa + 0.5
    guy(ctx, 620, gy, 0.75, t, expr="worried" if dizzy else "o", face=0.5 if not dizzy else 0,
        squash=sq, tilt=0.08 * math.sin(t * 5) if dizzy else 0, look=(1, -0.5) if not dizzy else (0, 0))
    if dizzy:
        stars_ring(ctx, 620, gy - 110, 110, t)
    if t > t_straight:
        # plumb line check
        k = ease(prog(t, t_straight, t_straight + 0.5))
        line(ctx, 1450, 400, 1450, lerp(400, 820, k), 4, RED)
        circle(ctx, 1450, lerp(400, 820, k), 10)
        fs(ctx, RED, lw=3)
        pop_text(ctx, "90°", 1600, 340, 70, t - t_straight - 0.4, (0.2, 0.75, 0.3), outline=8)
    ctx.restore()
    caption(ctx, "PISA, ITALY", "1178 AD", t - t_pisa, dur=5)
    vignette(ctx, 0.3)


def sh_pisa_basket(ctx, t, D, cue):
    t_new = cue("I think")
    t_arg = cue("I didn't")
    t_free = cue("Free lunch")
    ctx.save()
    cam(ctx, 900, 520, 1.25)
    pisa_bg(ctx, t)
    pisa_tower(ctx, 1450, 830, t, floors=3)
    hand = ease_out(prog(t, 0.6, 1.4))
    # worker walks in from the right with basket
    wx = lerp(1500, 1080, ease_out(prog(t, 0, 0.9)))
    worker(ctx, wx, 520, 0.75, t, face=-0.8, walk=t * 1.4 if t < 0.9 else None, expr="flat",
           brows="angry", larm=(lerp(0.9, 1.6, hand), 0.4), rarm=(-0.3, -0.2))
    has = t > 1.3
    stag = math.sin(t * 6) * 0.08 if has else 0
    guy(ctx, 720, 520 + (10 if has else 0), 0.75, t, expr="shock" if 1.3 < t < t_new else "smile" if t > t_arg else "o",
        face=0.8, tilt=stag, larm=(0.9, -1.3) if has else (0.3, 0.2), rarm=(-0.9, 1.3) if has else (-0.3, -0.2))
    bx = lerp(990, 790, hand) if t < 1.3 else 790
    basket(ctx, bx, 640 + (10 if has else 0) + (stag * 60), 0.8, stones=7)
    if t > t_new:
        speech(ctx, 1150, 270, 330, 110, "New guy. Go!", 52, tail=(-40, 50), alpha=ease(prog(t, t_new, t_new + 0.2)) * (1 - prog(t, t_arg, t_arg + 0.2)))
    if t > t_free:
        burst(ctx, 470, 230, 150, t - t_free, "FREE LUNCH!", size=46, color=(1, 0.88, 0.3))
    ctx.restore()
    vignette(ctx, 0.3)


def sh_pisa_soil(ctx, t, D, cue):
    t_soft = cue("The ground")
    t_clay = cue("Clay")
    t_fridge = cue("Building")
    bg_fill(ctx, hexc("#f6efe0"))
    # paper grid
    for i in range(0, W, 60):
        line(ctx, i, 0, i, H, 1.5, (0.8, 0.75, 0.65), 0.6)
    for j in range(0, H, 60):
        line(ctx, 0, j, W, j, 1.5, (0.8, 0.75, 0.65), 0.6)
    split = ease(prog(t, t_fridge - 0.3, t_fridge + 0.6))
    ctx.save()
    ctx.translate(lerp(0, -430, split), 0)
    # cross section
    gy = 520
    layers = [("CLAY", hexc("#b98a62"), 120), ("SAND", hexc("#e8cf8f"), 110), ("SHELLS", hexc("#d6c3a0"), 120),
              ("CLAY", hexc("#a87a55"), 200)]
    y = gy
    k_layers = ease(prog(t, t_soft - 0.3, t_soft + 0.8))
    ctx.rectangle(260, 0, 1400, gy)
    setc(ctx, SKY2)
    ctx.fill()
    for i, (name, c, h) in enumerate(layers):
        kk = ease(prog(t, t_clay + i * 0.7 - 0.2, t_clay + i * 0.7 + 0.3)) if i < 3 else 1
        ctx.rectangle(260, y, 1400, h)
        fs(ctx, c, lw=5)
        if name == "SHELLS":
            rnd = random.Random(2)
            for k in range(28):
                sx, sy = 280 + rnd.random() * 1360, y + 15 + rnd.random() * (h - 30)
                ctx.save()
                ctx.translate(sx, sy)
                ctx.rotate(rnd.random() * 6)
                ctx.move_to(-14, 6)
                ctx.curve_to(-14, -16, 14, -16, 14, 6)
                ctx.close_path()
                fs(ctx, hexc("#fff4e6"), lw=3)
                ctx.restore()
        if name == "SAND":
            rnd = random.Random(3)
            for k in range(160):
                circle(ctx, 270 + rnd.random() * 1380, y + 5 + rnd.random() * (h - 10), 2.5)
                setc(ctx, hexc("#b89a58"))
                ctx.fill()
        if i < 3 and kk > 0:
            ctx.save()
            ctx.translate(1500, y + h / 2)
            ctx.scale(max(kk, 1e-3), max(kk, 1e-3))
            text(ctx, name, 0, 0, 58, WHITE, outline=8)
            ctx.restore()
        y += h
    # tower sinking slightly
    sink = 30 * ease(prog(t, t_soft, t_soft + 3))
    ctx.save()
    ctx.rectangle(260, 0, 1400, gy + sink)
    ctx.clip()
    pisa_tower(ctx, 960, gy + sink, t, floors=3, scaffold=False, s=0.9, lean=1.2 * ease(prog(t, t_soft, t_soft + 3)))
    ctx.restore()
    for k in range(3):
        a = ease(prog(t, t_soft + 0.5 + k * 0.3, t_soft + 1 + k * 0.3))
        line(ctx, 960 - 120 + k * 120, gy + 30, 960 - 120 + k * 120, gy + 30 + 70 * a, 8, RED)
        poly(ctx, [(960 - 140 + k * 120, gy + 30 + 70 * a), (960 - 100 + k * 120, gy + 30 + 70 * a),
                   (960 - 120 + k * 120, gy + 60 + 70 * a)])
        fs(ctx, RED, lw=0)
    ctx.rectangle(260, 0, 1400, 1040)
    fs(ctx, None, lw=8)
    pop_text(ctx, "SOFT GROUND", 960, 90, 80, t - t_soft, RED, rot=-0.02)
    ctx.restore()
    if split > 0:
        # fridge on mattress inset
        ctx.save()
        ctx.translate(lerp(2200, 1480, split), 520)
        rrect(ctx, -380, -360, 760, 720, 30)
        fs(ctx, hexc("#fffaf0"), lw=8)
        sink2 = 50 * ease(prog(t, t_fridge + 0.8, t_fridge + 2.6))
        wob = math.sin(t * 7) * 3 * (1 - prog(t, t_fridge + 2.6, t_fridge + 3))
        # mattress
        ctx.move_to(-300, 160)
        ctx.curve_to(-140, 160 + sink2 * 0.3, -110, 120 + sink2, 0, 120 + sink2)
        ctx.curve_to(110, 120 + sink2, 140, 160 + sink2 * 0.3, 300, 160)
        ctx.line_to(300, 260)
        ctx.line_to(-300, 260)
        ctx.close_path()
        fs(ctx, hexc("#9ec9e8"), lw=6)
        for k in range(-2, 3):
            circle(ctx, k * 110, 210, 8)
            fs(ctx, hexc("#6a9cc0"), lw=3)
        # fridge
        ctx.save()
        ctx.translate(0, sink2 + 120)
        ctx.rotate(math.radians(6 * ease(prog(t, t_fridge + 0.8, t_fridge + 2.6))) + wob * 0.005)
        rrect(ctx, -90, -330, 180, 330, 16)
        fs(ctx, hexc("#eef2f5"), lw=6)
        line(ctx, -90, -220, 90, -220, 5)
        line(ctx, 60, -300, 60, -250, 8)
        line(ctx, 60, -190, 60, -110, 8)
        ctx.restore()
        text(ctx, "= TOWER ON PISA SOIL", 0, -290, 40, INK, font=HAND_FONT, outline=0, shadow=False)
        ctx.restore()


def sh_pisa_carry(ctx, t, D, cue):
    t_south = cue("Always")
    t_proud = cue("I was very proud")
    ctx.save()
    cam(ctx, 1450, 520, 1.0)
    pisa_bg(ctx, t)
    trips = int(max(0, t - 0.2) / 1.35)
    pile = min(trips, 9)
    lean = 0.25 * pile / 9
    pisa_tower(ctx, 1450, 830, t, floors=3, lean=lean)
    # stone pile on south (right) side
    rnd = random.Random(1)
    for i in range(pile * 3):
        stone(ctx, 1700 + (i % 6) * 34 - 30 + rnd.random() * 10, 800 - (i // 6) * 28, 22, seed=i)
    # guy trip loop
    ph = (max(0, t - 0.2) % 1.35) / 1.35
    if ph < 0.6:
        gx = lerp(1100, 1880, ph / 0.6)
        guy(ctx, gx, 470, 0.7, t, expr="smile", face=0.9, walk=t * 2.2, larm=(0.9, -1.3), rarm=(-0.9, 1.3))
        basket(ctx, gx + 30, 600, 0.6, stones=5)
    elif ph < 0.7:
        guy(ctx, 1880, 470, 0.7, t, expr="happy", face=0.9, larm=(1.6, 0.2), rarm=(-0.3, -0.2))
    else:
        gx = lerp(1880, 1100, (ph - 0.7) / 0.3)
        guy(ctx, gx, 470, 0.7, t, expr="smile", face=-0.9, walk=t * 2.6, larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        basket(ctx, gx - 60, 610, 0.45, stones=0)
    ctx.restore()
    # HUD: compass + trip counter
    rrect(ctx, 60, 60, 360, 120, 20)
    fs(ctx, (0.08, 0.07, 0.1, 0.8), lw=0)
    text(ctx, f"TRIPS: {trips}", 240, 122, 64, (1, 0.85, 0.3), outline=0, shadow=False)
    if t > t_south:
        ctx.save()
        ctx.translate(1760, 200)
        circle(ctx, 0, 0, 90)
        fs(ctx, hexc("#fffaf0"), lw=6)
        poly(ctx, [(0, -70), (14, 0), (0, 70), (-14, 0)])
        fs(ctx, RED, lw=3)
        text(ctx, "N", 0, -110, 40, INK, outline=0, shadow=False)
        ctx.restore()
        pop_text(ctx, "SOUTH SIDE ONLY", 1350, 140, 64, t - t_south, WHITE)
    if t > t_proud:
        burst(ctx, 400, 360, 140, t - t_proud, "GENIUS!", size=58, color=(0.5, 0.9, 0.5), tcolor=WHITE)


def sh_pisa_lean(ctx, t, D, cue):
    t_groan = 0.0
    t_tilt = cue("The whole tower")
    t_tower = cue("The workers stared")
    t_me = cue("Then they stared")
    lean = 4.0 * ease(prog(t, t_tilt, t_tilt + 2.6))
    shake = 9 * (prog(t, 0.2, 0.5) - prog(t, t_tilt + 2.4, t_tilt + 3.2))
    ctx.save()
    z = lerp(1.05, 1.0, ease(prog(t, 0, 2)))
    cam(ctx, 1300, 500, z, shake=shake, t=t)
    pisa_bg(ctx, t)
    rnd = random.Random(1)
    pisa_tower(ctx, 1450, 830, t, floors=3, lean=lean + 0.25)
    for i in range(27):
        stone(ctx, 1700 + (i % 6) * 34 - 30 + rnd.random() * 10, 800 - (i // 6) * 28, 22, seed=i)
    if shake > 0.5:
        for i in range(10):
            ph = (t * 0.8 + i * 0.1) % 1
            circle(ctx, 1250 + i * 50 + math.sin(i) * 40, 810 - ph * 120, 30 + ph * 40)
            setc(ctx, (0.85, 0.78, 0.6), 0.5 * (1 - ph))
            ctx.fill()
    # two workers look at tower, then at guy (left)
    look_me = t > t_me
    for i, wx in enumerate((980, 1150)):
        worker(ctx, wx, 520, 0.68, t, face=(-0.9 if look_me else 0.9), expr="shock" if t > t_tilt else "flat",
               look=(1, -0.6) if not look_me else (-1, 0), brows="angry" if look_me else None,
               larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    guy(ctx, 620, 520, 0.72, t, expr="worried" if not look_me else "grin", face=0.9 if not look_me else 0.2,
        look=(1, -0.5) if not look_me else (0, 0), brows="worried", larm=(0.3, 0.2),
        rarm=(-0.3, -0.2) if not look_me else (-2.2, 0.8))
    if look_me:
        sweat(ctx, 700, 400, 1.2, t)
        sweat(ctx, 540, 420, 0.9, t + 0.3)
    ctx.restore()
    if t < t_tilt + 2:
        pop_text(ctx, "CREEEAK...", 1350, 130, 90, t - 0.2, (1, 0.85, 0.3), rot=-0.04, hold=t_tilt + 1.6)
    if t > t_tilt + 1.2:
        pop_text(ctx, "JUST A LITTLE.", 1400, 1000, 60, t - t_tilt - 1.2, WHITE, hold=t_tower - t_tilt - 1.3)
    vignette(ctx, 0.35)


def sh_pisa_fact(ctx, t, D, cue):
    t_soil = cue("The soil")
    t_lean = cue("But the lean")
    t_today = cue("Today")
    t_eng = cue("Engineers")
    t_welcome = cue("You're welcome")
    if t < t_today:
        # timeline
        bg_fill(ctx, hexc("#f6efe0"))
        for i in range(0, W, 60):
            line(ctx, i, 0, i, H, 1.5, (0.8, 0.75, 0.65), 0.5)
        k = ease(prog(t, 0.2, 2.0))
        line(ctx, 200, 560, lerp(200, 1720, k), 560, 12)
        pts = [(260, "1173", "work begins"), (520, "1178", "3 floors · tilt starts"),
               (1000, "1272", "work resumes"), (1600, "1372", "tower finished")]
        for i, (x, yr, lab) in enumerate(pts):
            tt = t - 0.4 - i * 0.6
            if tt > 0:
                circle(ctx, x, 560, 22 * back_out(clamp(tt / 0.3)))
                fs(ctx, RED, lw=6)
                pop_text(ctx, yr, x, 470, 64, tt, INK, outline=0)
                text(ctx, lab, x, 650, 40, INK, font=HAND_FONT, outline=0, shadow=False, alpha=ease(clamp(tt / 0.3)))
        if t > 1.4:
            kk = ease(prog(t, 1.4, 2.2))
            ctx.save()
            ctx.rectangle(560, 520, 420 * kk, 80)
            setc(ctx, hexc("#8a6a6a"), 0.25)
            ctx.fill()
            ctx.restore()
            pop_text(ctx, "WAR PAUSE ~94 YEARS", 770, 760, 50, t - 1.6, RED, outline=6)
        if t > t_soil:
            pop_text(ctx, "the soil settles, so the tower survives", 960, 880, 54, t - t_soil, hexc("#2f7a3a"),
                     font=HAND_FONT, outline=0)
        if t > t_lean:
            pop_text(ctx, "BUT THE LEAN STAYED", 960, 230, 80, t - t_lean, RED, rot=-0.03)
    else:
        tt = t - t_today
        ctx.save()
        cam(ctx, 1300, 450, lerp(0.85, 0.95, ease(prog(tt, 0, 6))))
        pisa_bg(ctx, t)
        pisa_tower(ctx, 1400, 830, t, floors=8, lean=4.0, scaffold=False, s=0.82)
        # angle indicator
        a = ease(prog(tt, 0.3, 1.2))
        line(ctx, 1400, 830, 1400, 830 - 1050 * a, 5, (0.2, 0.5, 0.9))
        ctx.save()
        ctx.set_dash([20, 14])
        ln = 1050 * a
        line(ctx, 1400, 830, 1400 + math.sin(math.radians(4)) * ln, 830 - math.cos(math.radians(4)) * ln, 5, RED)
        ctx.restore()
        pop_text(ctx, "ABOUT 4°", 1000, 200, 90, tt - 0.8, RED)
        # tourists doing "the pose"
        if t > t_welcome - 0.4:
            k = ease_out(prog(t, t_welcome - 0.4, t_welcome))
            guy(ctx, 820, lerp(900, 520, k), 0.7, t, expr="grin", face=0.9, larm=(0.3, 0.2), rarm=(-2.0, 0.2))
            worker(ctx, 600, lerp(950, 560, k), 0.55, t, face=0.9, expr="grin", larm=(0.3, 0.2),
                   rarm=(-2.0, 0.2))
        ctx.restore()
        if t > t_eng:
            pop_text(ctx, "1990 - 2001: STABILISED", 960, 990, 56, t - t_eng, WHITE)
        if t > t_welcome:
            burst(ctx, 380, 260, 140, t - t_welcome, "GRAZIE!", size=56, color=(0.4, 0.8, 0.45), tcolor=WHITE)
    vignette(ctx, 0.3)


def sh_newton_arrive(ctx, t, D, cue):
    t_farm = cue("A farm")
    t_wool = cue("Woolsthorpe")
    t_plague = cue("A terrible plague")
    t_name = cue("His name")
    ctx.save()
    cx = lerp(700, 1200, ease(prog(t, 0, t_plague)))
    cam(ctx, cx, 520, lerp(1.05, 0.95, ease(prog(t, 0, D))))
    england_bg(ctx, t)
    sheep(ctx, 300, 900, t, 0.8)
    sheep(ctx, 560, 950, t + 1, 0.7)
    apple_tree(ctx, 900, 860, t, s=0.8)
    # Newton walks in carrying books, then sits
    if t < t_name:
        nx = lerp(1900, 1050, ease(prog(t, t_plague, t_name)))
        if t < t_plague:
            nx = 1900
        newton(ctx, nx, 560, 0.62, t, face=-0.8, walk=t * 1.3 if t_plague < t < t_name else None,
               larm=(0.8, 1.5), rarm=(-0.5, -0.3), expr="flat")
        for k in range(3):
            ctx.rectangle(nx - 95 + k * 3, 690 - k * 22, 70, 22)
            fs(ctx, [hexc("#8a3b2b"), hexc("#2b4b8a"), hexc("#3b6b3b")][k], lw=4)
    else:
        newton(ctx, 1050, 560, 0.62, t, face=-0.6, expr="smile", larm=(0.6, 1.5), rarm=(-0.5, -0.3))
        for k in range(3):
            ctx.rectangle(1110 + k * 3, 760 - k * 22, 70, 22)
            fs(ctx, [hexc("#8a3b2b"), hexc("#2b4b8a"), hexc("#3b6b3b")][k], lw=4)
    # guy pops out from behind the fence, shivering
    k = ease_out(prog(t, 0.3, 1.0))
    guy(ctx, 420, lerp(900, 640, k), 0.6, t, expr="worried", face=0.8, tilt=0.03 * math.sin(t * 30),
        larm=(-0.9, 1.9), rarm=(0.9, -1.9), legs=(0, 0))
    ctx.restore()
    caption(ctx, "WOOLSTHORPE MANOR, ENGLAND", "1666 AD", t - t_wool, dur=5)
    if t > t_plague:
        k = ease(prog(t, t_plague, t_plague + 0.4)) * (1 - ease(prog(t, t_name - 0.2, t_name + 0.2)))
        if k > 0:
            ctx.save()
            ctx.translate(1450, 330)
            ctx.rotate(0.05)
            ctx.scale(max(k, 1e-3), max(k, 1e-3))
            rrect(ctx, -260, -170, 520, 340, 8)
            fs(ctx, hexc("#f2e6c4"), lw=6)
            text(ctx, "NOTICE", 0, -110, 56, INK, outline=0, shadow=False)
            text(ctx, "Cambridge University", 0, -40, 40, INK, font=HAND_FONT, outline=0, shadow=False)
            text(ctx, "is CLOSED", 0, 10, 52, RED, outline=0, shadow=False)
            text(ctx, "due to the Great Plague", 0, 70, 38, INK, font=HAND_FONT, outline=0, shadow=False)
            text(ctx, "1665", 0, 125, 40, INK, font=HAND_FONT, outline=0, shadow=False)
            ctx.restore()
    if t > t_name:
        pop_text(ctx, "ISAAC NEWTON", 1100, 170, 100, t - t_name - 0.3, WHITE, rot=-0.03)
        text(ctx, "age 23", 1100, 260, 48, (1, 0.85, 0.3), font=HAND_FONT, outline=5,
             alpha=ease(prog(t, t_name + 0.8, t_name + 1.2)))
    vignette(ctx, 0.3)


def sh_newton_think(ctx, t, D, cue):
    t_why = cue("Why does")
    t_deep = cue("Deep stuff")
    t_hungry = cue("I was hungry")
    ctx.save()
    cam(ctx, 950, 500, 1.15)
    england_bg(ctx, t)
    apple_tree(ctx, 900, 860, t, s=0.8)
    newton(ctx, 1080, 600, 0.62, t, face=0.3, look=(0.3, -1), expr="o" if (t * 2) % 2 < 1 else "flat",
           larm=(0.4, 0.3), rarm=(-2.6, 1.9))
    peek = ease_out(prog(t, t_deep - 0.5, t_deep + 0.3))
    if peek > 0:
        guy(ctx, lerp(700, 760, peek), 600, 0.6, t, expr="flat" if t < t_hungry else "o", face=0.9,
            look=(1, 0) if t < t_hungry + 0.6 else (0.5, -1), larm=(0.3, 0.2), rarm=(-1.3, -0.4))
    ctx.restore()
    # thought bubble: Earth & Moon
    kb = ease_out(prog(t, 0.4, 1.0))
    if kb > 0:
        ctx.save()
        ctx.translate(1450, 300)
        ctx.scale(max(kb, 1e-3), max(kb, 1e-3))
        speech(ctx, 0, 0, 640, 440, "", think=True, tail=(-120, 120))
        circle(ctx, 0, 10, 60)
        fs(ctx, hexc("#4a8fd6"), lw=5)
        ctx.move_to(-30, -20); ctx.curve_to(0, -40, 20, 10, -10, 30); ctx.curve_to(-40, 20, -50, 0, -30, -20)
        fs(ctx, hexc("#5fb85a"), lw=3)
        ctx.save()
        ctx.scale(1, 0.55)
        circle(ctx, 0, 18, 200)
        ctx.set_dash([12, 10])
        setc(ctx, INK, 0.6)
        ctx.set_line_width(4)
        ctx.stroke()
        ctx.restore()
        a = t * 1.3
        mx, my = math.cos(a) * 200, 10 + math.sin(a) * 110
        circle(ctx, mx, my, 26)
        fs(ctx, hexc("#e2e2d8"), lw=4)
        if t > t_why:
            # "why not fly off?" tangent arrow
            k = ease(prog(t, t_why + 0.5, t_why + 1.2))
            tx, ty = -math.sin(a) * 200, math.cos(a) * 110
            n = math.hypot(tx, ty) or 1
            line(ctx, mx, my, mx + tx / n * 150 * k, my + ty / n * 150 * k, 5, RED)
            text(ctx, "?", mx + tx / n * 170, my + ty / n * 170, 70, RED, alpha=k)
        ctx.restore()
    if t > t_hungry:
        burst(ctx, 420, 280, 130, t - t_hungry, "GRRRBL", size=50, color=(1, 0.75, 0.3))
    vignette(ctx, 0.3)


def sh_newton_climb(ctx, t, D, cue):
    t_climb = cue("I climbed")
    t_reach = cue("I reached")
    t_snap = cue("And the branch")
    snap_t = cue("And the branch", frac=0.75)
    climb = ease(prog(t, t_climb, t_reach))
    cy = lerp(560, 260, ease(prog(t, 0.5, t_reach + 0.3)))
    ctx.save()
    cam(ctx, 960, cy, 1.0)
    england_bg(ctx, t)
    tp = apple_tree(ctx, 960, 860, t, s=1.0, top_apple=t < snap_t + 0.05)
    # the guy climbs up the trunk
    gy = lerp(560, 150, climb)
    stretch = ease(prog(t, t_reach, t_snap))
    side = math.sin(t * 8) * 0.4 * (1 if 0 < climb < 1 else 0)
    if t < snap_t:
        guy(ctx, 960 - 30 + stretch * 10, gy - stretch * 30, 0.55, t,
            expr="sly" if t < t_reach else "worried", face=0.5, look=(0.5, -1),
            larm=(2.6 + side, 0.2), rarm=(-2.6 + side + stretch * 0.3, -0.2), legs=(side, -side))
    else:
        tt = t - snap_t
        fall = ease_in(prog(tt, 0.15, 0.9))
        guy(ctx, 960 - 20, lerp(gy - 40, 600, fall), 0.55, t, expr="shock", face=0, tilt=tt * 3,
            larm=(2.4, 0.3), rarm=(-2.4, -0.3))
        # apple falls straight down
        ay = lerp(tp[1], 760, ease_in(prog(tt, 0.0, 1.1)))
        apple(ctx, tp[0], ay, 26)
        burst(ctx, tp[0] + 200, tp[1] + 60, 120, tt, "SNAP!", size=60)
    ctx.restore()
    vignette(ctx, 0.3)


def sh_newton_fall(ctx, t, D, cue):
    t_straight = cue("Straight down")
    t_down = cue("Down.")
    t_watch = cue("Newton watched")
    if t < t_watch:
        # slow motion apple on a white-ish speed background
        bg_fill(ctx, hexc("#eaf6e6"))
        for i in range(14):
            x = 200 + i * 120
            y = ((t * 900 + i * 173) % 1400) - 200
            line(ctx, x, y, x, y - 240, 5, (0.6, 0.8, 0.6), 0.6)
        ay = lerp(150, 760, ease(prog(t, 0, t_watch)))
        ctx.save()
        ctx.set_dash([18, 16])
        line(ctx, 960, 60, 960, 1020, 4, RED, 0.6)
        ctx.restore()
        apple(ctx, 960, ay, 90, rot=t * 0.4)
        if t > t_straight:
            pop_text(ctx, "NOT SIDEWAYS", 480, 380, 70, t - t_straight - 0.6, INK, outline=0, rot=-0.05,
                     hold=99)
            pop_text(ctx, "NOT UP", 1440, 380, 70, t - t_straight - 1.3, INK, outline=0, rot=0.05)
        if t > t_down:
            pop_text(ctx, "DOWN.", 960, 920, 150, t - t_down, RED)
    else:
        tt = t - t_watch
        z = lerp(1.6, 2.6, ease(prog(tt, 0, D - t_watch)))
        ctx.save()
        cam(ctx, 1080, 520, z)
        england_bg(ctx, t)
        apple_tree(ctx, 900, 860, t, s=0.8, top_apple=False)
        ay = lerp(400, 760, ease_in(prog(tt, 0, 1.0)))
        apple(ctx, 1000, ay, 22)
        newton(ctx, 1080, 600, 0.62, t, face=-0.4, look=(-0.6, 1 if tt > 0.6 else -0.5),
               expr="o" if tt < 1.5 else "shock", larm=(0.4, 0.3), rarm=(-0.4, -0.3), brows="up" if tt > 1.5 else None)
        ctx.restore()
        if tt > 1.6:
            for i in range(3):
                sparkle(ctx, 1050 + i * 180, 380 - i * 40, 40, t + i)
    vignette(ctx, 0.35)


def sh_newton_idea(ctx, t, D, cue):
    t_what = cue("What if")
    t_21 = cue("Twenty one")
    t_never = cue("He never")
    t_lying = cue("Lying")
    if t < t_21:
        # diagram: Earth, apple, Moon with matching arrows
        bg_fill(ctx, hexc("#0e1a33"))
        rnd = random.Random(4)
        for i in range(120):
            circle(ctx, rnd.random() * W, rnd.random() * H, 1.5 + rnd.random() * 2)
            setc(ctx, WHITE, 0.4 + 0.4 * math.sin(t * 2 + i))
            ctx.fill()
        ex, ey = 700, 620
        circle(ctx, ex, ey, 260)
        fs(ctx, hexc("#4a8fd6"), lw=7)
        for dx, dy, r in ((-80, -60, 90), (60, 80, 70), (120, -110, 50)):
            circle(ctx, ex + dx, ey + dy, r)
            setc(ctx, hexc("#5fb85a"))
            ctx.fill()
        circle(ctx, ex, ey, 260)
        fs(ctx, None, lw=7)
        # Newton lightbulb
        k = ease_out(prog(t, 0.2, 0.7))
        ctx.save()
        ctx.translate(560, 200)
        ctx.scale(max(k, 1e-3), max(k, 1e-3))
        g = cairo.RadialGradient(0, 0, 10, 0, 0, 160)
        g.add_color_stop_rgba(0, 1, 0.95, 0.5, 0.8)
        g.add_color_stop_rgba(1, 1, 0.95, 0.5, 0)
        ctx.set_source(g)
        circle(ctx, 0, 0, 160)
        ctx.fill()
        circle(ctx, 0, -10, 60)
        fs(ctx, (1, 0.92, 0.4), lw=6)
        ctx.rectangle(-26, 45, 52, 40)
        fs(ctx, hexc("#9aa0a8"), lw=5)
        ctx.restore()
        # apple near the surface
        apple(ctx, ex + 120, ey - 330, 30)
        ka = ease(prog(t, t_what, t_what + 0.8))
        line(ctx, ex + 120, ey - 290, ex + 120, ey - 290 + 30 * ka, 8, (1, 0.85, 0.3))
        # moon
        a = -0.5 + t * 0.12
        mx, my = ex + math.cos(a) * 900, ey + math.sin(a) * 520
        circle(ctx, mx, my, 80)
        fs(ctx, hexc("#e2e2d8"), lw=6)
        circle(ctx, mx - 20, my - 15, 16)
        fs(ctx, hexc("#c8c8bc"), lw=3)
        km = ease(prog(t, t_what + 1.2, t_what + 2.2))
        dx, dy = ex - mx, ey - my
        n = math.hypot(dx, dy)
        line(ctx, mx + dx / n * 95, my + dy / n * 95, mx + dx / n * (95 + 200 * km), my + dy / n * (95 + 200 * km), 8,
             (1, 0.85, 0.3))
        if km > 0.5:
            text(ctx, "SAME FORCE!", 1350, 160, 80, (1, 0.85, 0.3), alpha=ease(prog(km, 0.5, 1)))
        kf = ease(prog(t, t_what + 3.0, t_what + 3.6))
        if kf > 0:
            text(ctx, "F = G M m / r²", 1420, 900, 76, WHITE, font=HAND_FONT, outline=0, alpha=kf)
    else:
        tt = t - t_21
        ctx.save()
        z = 1.0 if t < t_never else lerp(1.0, 1.3, ease(prog(t, t_never, t_never + 2)))
        cam(ctx, 960 if t < t_never else 760, 540 if t < t_never else 650, z)
        england_bg(ctx, t)
        apple_tree(ctx, 900, 860, t, s=0.8, top_apple=False)
        # Newton walks off excitedly holding apple
        nx = lerp(1150, 1900, ease_in(prog(t, t_never - 0.5, t_never + 2.5)))
        newton(ctx, nx, 580, 0.62, t, face=0.8, expr="grin", walk=t * 2 if t > t_never - 0.5 else None,
               larm=(0.3, 0.2), rarm=(-2.5, 0.4))
        # guy lying in the grass with a branch on his face
        ctx.save()
        ctx.translate(640, 900)
        ctx.rotate(-math.pi / 2)
        doodle(ctx, 0, 0, 0.5, expr="flat", face=0, blink=1.0, larm=(0.6, 0.2), rarm=(-0.6, -0.2), cap=True)
        ctx.restore()
        ctx.save()
        ctx.translate(640, 890)
        ctx.rotate(0.3)
        line(ctx, -120, 0, 140, 0, 14, hexc("#7a5130"))
        for k in range(3):
            ellipse(ctx, -60 + k * 70, -20, 34, 16)
            fs(ctx, hexc("#5aab4f"), lw=4)
        ctx.restore()
        if t > t_lying + 0.8:
            text(ctx, "...ow.", 760, 780, 50, INK, font=HAND_FONT, outline=0, shadow=False,
                 alpha=ease(prog(t, t_lying + 0.8, t_lying + 1.1)))
        ctx.restore()
        # Principia book pop-up
        kb = back_out(prog(tt, 0.6, 1.2), 1.8) * (1 - ease(prog(t, t_never - 0.3, t_never + 0.2)))
        if kb > 0:
            ctx.save()
            ctx.translate(960, 460)
            ctx.scale(max(kb, 1e-3), max(kb, 1e-3))
            ctx.rotate(-0.04)
            rrect(ctx, -240, -300, 480, 600, 14)
            fs(ctx, hexc("#7a2b22"), lw=8)
            rrect(ctx, -200, -250, 400, 500, 8)
            fs(ctx, hexc("#f2e6c4"), lw=5)
            text(ctx, "PHILOSOPHIÆ", 0, -150, 44, INK, outline=0, shadow=False)
            text(ctx, "NATURALIS", 0, -95, 44, INK, outline=0, shadow=False)
            text(ctx, "PRINCIPIA", 0, -30, 58, RED, outline=0, shadow=False)
            text(ctx, "MATHEMATICA", 0, 30, 40, INK, outline=0, shadow=False)
            text(ctx, "Is. Newton", 0, 110, 44, INK, font=HAND_FONT, outline=0, shadow=False)
            text(ctx, "1687", 0, 180, 60, INK, outline=0, shadow=False)
            ctx.restore()
    vignette(ctx, 0.35)


def sh_fleming_arrive(ctx, t, D, cue):
    t_london = cue("London")
    t_lab = cue("A tiny")
    t_fl = cue("A Scottish")
    if t < t_lab:
        # exterior: London street 1928
        ctx.save()
        cam(ctx, lerp(800, 1100, ease(prog(t, 0, t_lab))), 540, 1.0)
        vgrad(ctx, -600, -300, 3200, 1400, hexc("#b9c3c8"), hexc("#e6e4dc"))
        for i in range(6):
            ph = (t * 0.2 + i / 6) % 1
            circle(ctx, 200 + i * 300, 500 - ph * 400, 60 + ph * 60)
            setc(ctx, (0.55, 0.55, 0.55), 0.35 * (1 - ph))
            ctx.fill()
        # Big Ben
        bx = 1500
        ctx.rectangle(bx - 70, 80, 140, 760)
        fs(ctx, hexc("#c9b48a"), lw=6)
        for k in range(10):
            line(ctx, bx - 70, 140 + k * 70, bx + 70, 140 + k * 70, 3, hexc("#9a8460"))
        ctx.rectangle(bx - 90, 160, 180, 180)
        fs(ctx, hexc("#c9b48a"), lw=6)
        clock_icon(ctx, bx, 250, 70, t * 0.05, back=False)
        poly(ctx, [(bx - 90, 160), (bx, -60), (bx + 90, 160)])
        fs(ctx, hexc("#4f5a52"), lw=6)
        # hospital building
        ctx.rectangle(-300, 260, 1250, 600)
        fs(ctx, hexc("#b5674a"), lw=6)
        for r in range(3):
            for c in range(7):
                rrect(ctx, -240 + c * 170, 320 + r * 170, 90, 120, 6)
                fs(ctx, hexc("#e8eef0"), lw=5)
        rrect(ctx, 50, 220, 600, 70, 8)
        fs(ctx, hexc("#2f3a44"), lw=5)
        text(ctx, "ST MARY'S HOSPITAL", 350, 256, 46, hexc("#f2e6c4"), outline=0, shadow=False)
        ctx.rectangle(-900, 860, 3800, 400)
        fs(ctx, hexc("#7a7a78"), lw=6)
        # old car driving by
        carx = lerp(-500, 2400, prog(t, 0.3, t_lab))
        ctx.save()
        ctx.translate(carx, 830)
        rrect(ctx, -170, -110, 340, 90, 20)
        fs(ctx, hexc("#2b2b33"), lw=6)
        rrect(ctx, -110, -190, 200, 90, 16)
        fs(ctx, hexc("#2b2b33"), lw=6)
        rrect(ctx, -90, -175, 70, 60, 8)
        fs(ctx, hexc("#9fb6c4"), lw=4)
        for wx in (-110, 110):
            circle(ctx, wx, -20, 42)
            fs(ctx, INK, lw=0)
            circle(ctx, wx, -20, 16)
            fs(ctx, hexc("#c9ccd2"), lw=4)
        ctx.restore()
        if t > 0.3:
            pop_text(ctx, "HONK!", carx + 60, 600, 60, t - 0.6, (1, 0.85, 0.3), hold=1.5)
        ctx.restore()
        caption(ctx, "LONDON, ENGLAND", "1928", t - t_london, dur=4.5)
    else:
        ctx.save()
        cam(ctx, lerp(900, 800, ease(prog(t, t_lab, D))), 520, lerp(1.0, 1.08, ease(prog(t, t_lab, D))))
        lab_bg(ctx, t)
        # Fleming packing suitcase
        fleming(ctx, 760, 530, 0.68, t, face=0.6, expr="smile", larm=(0.5, 1.5), rarm=(-0.8, -1.2),
                look=(0.2, 1))
        rrect(ctx, 820, 540, 230, 100, 10)
        fs(ctx, hexc("#7a4a2a"), lw=6)
        line(ctx, 900, 540, 900, 520, 6)
        line(ctx, 970, 540, 970, 520, 6)
        line(ctx, 900, 520, 970, 520, 6)
        # guy peeking from under the bench
        k = ease_out(prog(t, t_lab + 0.8, t_lab + 1.5))
        guy(ctx, 220, lerp(900, 570, k), 0.6, t, expr="o", face=0.9, look=(1, 0), larm=(0.3, 0.2), rarm=(-1.2, -0.6))
        ctx.restore()
        if t > t_fl:
            pop_text(ctx, "ALEXANDER FLEMING", 960, 120, 84, t - t_fl - 0.6, WHITE)
        if t > t_fl + 1.8:
            ctx.save()
            ctx.translate(1600, 860)
            ctx.rotate(0.05)
            speech(ctx, 0, 0, 380, 110, "Holiday time!", 54, tail=(-120, -120))
            ctx.restore()
    vignette(ctx, 0.35)


def sh_fleming_bact(ctx, t, D, cue):
    t_back = cue("Back then")
    t_none = cue("There was no cure")
    if t < t_back:
        bg_fill(ctx, hexc("#1c2a33"))
        z = lerp(1.0, 1.15, ease(prog(t, 0, t_back)))
        ctx.save()
        cam(ctx, W / 2, H / 2, z)
        petri(ctx, W / 2, H / 2, 420, t, germs=ease(prog(t, 0.2, 1.4)))
        ctx.restore()
        pop_text(ctx, "STAPHYLOCOCCUS", W / 2, 110, 80, t - 1.0, (1, 0.85, 0.3))
        text(ctx, "(the bacteria behind nasty infections)", W / 2, 990, 46, WHITE, font=HAND_FONT, outline=5,
             alpha=ease(prog(t, 1.6, 2.0)))
    else:
        tt = t - t_back
        bg_fill(ctx, hexc("#f6efe0"))
        for i in range(0, W, 60):
            line(ctx, i, 0, i, H, 1.5, (0.8, 0.75, 0.65), 0.5)
        # big hand with scratch
        ctx.save()
        ctx.translate(760, 560)
        rrect(ctx, -260, -120, 520, 280, 120)
        fs(ctx, WHITE, lw=8)
        for k in range(4):
            rrect(ctx, -230 + k * 120, -320, 100, 240, 50)
            fs(ctx, WHITE, lw=8)
        rrect(ctx, 220, -60, 220, 100, 50)
        fs(ctx, WHITE, lw=8)
        ks = ease(prog(tt, 0.3, 0.8))
        line(ctx, -120, 40, -120 + 220 * ks, -20, 8, RED)
        if tt > 0.8:
            for i in range(8):
                ph = (t * 0.7 + i / 8) % 1
                circle(ctx, -100 + i * 26, 30 - i * 7 + ph * 40, 6 * (1 - ph))
                setc(ctx, RED, 0.8)
                ctx.fill()
        ctx.restore()
        pop_text(ctx, "A SMALL SCRATCH...", 760, 140, 70, tt - 0.4, INK, outline=0)
        if t > t_back + 1.8:
            for i in range(5):
                tx = 1350 + (i % 3) * 120
                ty = 380 + (i // 3) * 160
                germ_t = t - t_back - 1.8 - i * 0.15
                if germ_t > 0:
                    k = back_out(clamp(germ_t / 0.3))
                    ctx.save()
                    ctx.translate(tx, ty)
                    ctx.scale(max(k, 1e-3), max(k, 1e-3))
                    circle(ctx, 0, 0, 50)
                    fs(ctx, (0.95, 0.75, 0.15), lw=6)
                    line(ctx, -24, -18, -8, -10, 5)
                    line(ctx, 24, -18, 8, -10, 5)
                    circle(ctx, -14, 0, 5); circle(ctx, 14, 0, 5)
                    fs(ctx, INK, lw=0)
                    ctx.move_to(-16, 22); ctx.curve_to(-6, 12, 6, 12, 16, 22)
                    fs(ctx, None, lw=5)
                    ctx.restore()
        if t > t_none:
            k = ease(prog(t, t_none, t_none + 0.4))
            ctx.save()
            rrect(ctx, 1220, 820, 560, 140, 20)
            fs(ctx, RED, lw=8, alpha=k)
            text(ctx, "NO CURE", 1500, 890, 96, WHITE, outline=8, alpha=k)
            ctx.restore()
    vignette(ctx, 0.35)


def sh_fleming_sneeze(ctx, t, D, cue):
    t_nosy = cue("And I was nosy")
    t_peek = cue("I lifted")
    t_breeze = cue("Just then")
    t_sneeze = cue("I sneezed")
    t_lids = cue("The lids")
    t_mostly = cue("Mostly")
    ctx.save()
    cam(ctx, 820, 520, 1.12)
    lab_bg(ctx, t, dishes=False)
    # Fleming exits right through door
    if t < t_nosy + 0.3:
        fx = lerp(800, 2050, ease_in(prog(t, 0.3, t_nosy + 0.3)))
        fleming(ctx, fx, 530, 0.68, t, face=0.9, walk=t * 2, expr="smile", larm=(0.3, 0.2), rarm=(-0.5, -1.4))
        rrect(ctx, fx + 40, 630, 200, 90, 10)
        fs(ctx, hexc("#7a4a2a"), lw=6)
    # dishes on bench (close-ish)
    lid = ease(prog(t, t_peek, t_peek + 0.6)) * (1 - ease(prog(t, t_sneeze + 0.15, t_sneeze + 0.35)))
    for k, dx in enumerate((300, 440, 580)):
        ellipse(ctx, dx, 625, 60, 15)
        fs(ctx, (0.9, 0.95, 0.97), lw=4)
        ellipse(ctx, dx, 623, 48, 10)
        setc(ctx, (0.98, 0.85, 0.5))
        ctx.fill()
        off = lid * 60 if k != 1 else lid * 60
        crooked = 0.0
        if t > t_sneeze + 0.3 and k == 1:
            crooked = 0.35
        ctx.save()
        ctx.translate(dx + (lid * 40) + crooked * 40, 612 - off)
        ctx.rotate(crooked)
        ellipse(ctx, 0, 0, 62, 15)
        setc(ctx, (0.85, 0.95, 1), 0.45)
        ctx.fill_preserve()
        setc(ctx, (0.4, 0.55, 0.65))
        ctx.set_line_width(4)
        ctx.stroke()
        ctx.restore()
    # guy
    if t > t_nosy - 0.3:
        gx = lerp(-100, 450, ease(prog(t, t_nosy - 0.3, t_nosy + 1.0)))
        sn = prog(t, t_sneeze - 0.6, t_sneeze)
        tilt = -0.25 * ease(sn) if t < t_sneeze else 0.35 * math.exp(-(t - t_sneeze) * 4)
        expr = "sly" if t < t_breeze else ("worried" if t < t_sneeze - 0.6 else ("o" if t < t_sneeze else "shock"))
        if t > t_mostly:
            expr = "grin"
        guy(ctx, gx, 500, 0.72, t, expr=expr, face=0.6, look=(0.3, 1), tilt=tilt,
            walk=t * 1.6 if t < t_nosy + 1.0 else None,
            larm=(0.3, 0.2), rarm=(-1.4, 0.6) if t_peek < t < t_sneeze + 0.3 else (-0.3, -0.2),
            brows="worried" if t > t_mostly else None)
        if t > t_mostly:
            sweat(ctx, gx + 80, 390, 1.0, t)
    # spores drift up from the floor vent
    if t > t_breeze:
        ctx.rectangle(820, 790, 220, 30)
        fs(ctx, hexc("#9aa0a8"), lw=5)
        for k in range(6):
            line(ctx, 830 + k * 35, 795, 830 + k * 35, 815, 3)
        a = ease(prog(t, t_breeze, t_breeze + 1))
        spores(ctx, t - t_breeze, 930, 800, 440, 560, n=26, a=a)
        text(ctx, "MOULD LAB ↓", 930, 870, 44, INK, font=HAND_FONT, outline=0, shadow=False, alpha=a)
    ctx.restore()
    if t > t_sneeze:
        burst(ctx, 1250, 300, 190, t - t_sneeze, "AH-CHOO!", size=70, color=(0.7, 0.95, 0.8), tcolor=hexc("#2b6b4a"))
    if t > t_mostly:
        pop_text(ctx, "mostly.", 1500, 820, 64, t - t_mostly, WHITE, font=HAND_FONT, outline=6)
        pop_text(ctx, "probably.", 1520, 900, 64, t - t_mostly - 0.7, WHITE, font=HAND_FONT, outline=6)
    vignette(ctx, 0.35)


def sh_fleming_return(ctx, t, D, cue):
    t_back = cue("Fleming was back")
    t_stop = cue("Then he stopped")
    t_mould = cue("One dish")
    t_gone = cue("And all around")
    if t < t_back:
        # calendar flip
        bg_fill(ctx, hexc("#2b2430"))
        n = int(t / 0.09)
        days = ["AUG 2", "AUG 9", "AUG 16", "AUG 23", "AUG 30", "SEPT 3"]
        idx = min(len(days) - 1, int(prog(t, 0.2, t_back - 0.6) * (len(days) - 1) + 0.0001))
        ctx.save()
        ctx.translate(W / 2, H / 2)
        rrect(ctx, -300, -330, 600, 660, 26)
        fs(ctx, WHITE, lw=10)
        ctx.rectangle(-300, -330, 600, 160)
        fs(ctx, RED, lw=10)
        text(ctx, "1928", 0, -250, 90, WHITE, outline=0, shadow=False)
        d = days[idx]
        text(ctx, d.split()[0], 0, -60, 110, INK, outline=0, shadow=False)
        text(ctx, d.split()[1], 0, 120, 220, RED if idx == len(days) - 1 else INK, outline=0, shadow=False)
        if idx < len(days) - 1:
            ph = (t * 6) % 1
            ctx.rectangle(-300, -170 - ph * 200, 600, 30)
            setc(ctx, WHITE, 0.6)
            ctx.fill()
        ctx.restore()
        clock_icon(ctx, 350, 300, 110, t * 4, back=False)
    elif t < t_mould:
        ctx.save()
        cam(ctx, 760, 520, lerp(1.1, 1.4, ease(prog(t, t_stop, t_mould))))
        lab_bg(ctx, t)
        stopped = t > t_stop
        fleming(ctx, 620, 530, 0.68, t, face=0.6, look=(0.3, 1), expr="flat" if not stopped else "o",
                larm=(0.6, 1.3) if not stopped else (0.3, 0.2),
                rarm=(-0.8 + 0.2 * math.sin(t * 5) * (0 if stopped else 1), -1.2), brows="up" if stopped else None)
        ctx.restore()
    else:
        tt = t - t_mould
        bg_fill(ctx, hexc("#1c2a33"))
        ctx.save()
        cam(ctx, W / 2, H / 2, lerp(1.0, 1.12, ease(prog(tt, 0, D - t_mould))))
        petri(ctx, W / 2, H / 2, 430, t, germs=1.0, mould=ease(prog(tt, 0.2, 1.6)),
              halo=ease(prog(t, t_gone, t_gone + 2.0)))
        ctx.restore()
        pop_text(ctx, "MOULD", 420, 220, 80, tt - 0.6, (0.6, 0.95, 0.75))
        if t > t_gone + 1.4:
            pop_text(ctx, "BACTERIA: GONE", 1440, 960, 72, t - t_gone - 1.4, (1, 0.85, 0.3))
    vignette(ctx, 0.35)


def sh_fleming_fact(ctx, t, D, cue):
    t_peni = cue("That mould was")
    t_anti = cue("And from it")
    t_nobel = cue("In nineteen")
    t_lives = cue("It has saved")
    if t < t_anti:
        ctx.save()
        cam(ctx, 760, 460, 1.5)
        lab_bg(ctx, t)
        fleming(ctx, 680, 530, 0.68, t, face=0.6, expr="smile", look=(0.3, 0.5), brows="up",
                larm=(0.3, 0.2), rarm=(-1.6, 0.6))
        petri(ctx, 850, 640, 52, t, mould=1, halo=1, germ_faces=False)
        ctx.restore()
        speech(ctx, 1380, 300, 520, 150, "That's funny...", 66, tail=(-180, 90),
               alpha=ease(prog(t, 0.3, 0.6)))
        if t > t_peni:
            pop_text(ctx, "PENICILLIUM", 1380, 900, 90, t - t_peni - 0.5, (0.6, 0.95, 0.75))
    elif t < t_nobel:
        tt = t - t_anti
        spiral_bg(ctx, t, (0.08, 0.2, 0.25), (0.1, 0.26, 0.3), speed=0.2)
        k = back_out(prog(tt, 0.2, 0.8), 1.6)
        ctx.save()
        ctx.translate(W / 2, 560)
        ctx.scale(max(k, 1e-3), max(k, 1e-3))
        g = cairo.RadialGradient(0, 0, 50, 0, 0, 420)
        g.add_color_stop_rgba(0, 1, 1, 0.8, 0.6)
        g.add_color_stop_rgba(1, 1, 1, 0.8, 0)
        ctx.set_source(g)
        circle(ctx, 0, 0, 420)
        ctx.fill()
        rrect(ctx, -140, -200, 280, 380, 40)
        fs(ctx, hexc("#d9eef2"), lw=8)
        ctx.rectangle(-60, -270, 120, 80)
        fs(ctx, hexc("#4a4a52"), lw=7)
        rrect(ctx, -120, -60, 240, 160, 12)
        fs(ctx, WHITE, lw=6)
        text(ctx, "PENICILLIN", 0, 20, 40, hexc("#2f4f8f"), outline=0, shadow=False)
        ctx.restore()
        for i in range(6):
            sparkle(ctx, W / 2 + math.cos(i + t) * 360, 560 + math.sin(i * 2 + t) * 260, 30, t + i)
        pop_text(ctx, "THE FIRST TRUE ANTIBIOTIC", W / 2, 140, 76, tt - 0.8, (1, 0.85, 0.3))
    elif t < t_lives:
        tt = t - t_nobel
        bg_fill(ctx, hexc("#1d1a2a"))
        k = back_out(prog(tt, 0.1, 0.7), 1.6)
        ctx.save()
        ctx.translate(W / 2, 470)
        ctx.scale(max(k, 1e-3), max(k, 1e-3))
        poly(ctx, [(-90, -330), (-30, -170), (30, -170), (90, -330)])
        fs(ctx, hexc("#2f4f8f"), lw=6)
        circle(ctx, 0, 0, 180)
        fs(ctx, hexc("#e2b23a"), lw=8)
        circle(ctx, 0, 0, 140)
        fs(ctx, hexc("#f0c64a"), lw=4)
        text(ctx, "NOBEL", 0, -20, 64, hexc("#7a5a10"), outline=0, shadow=False)
        text(ctx, "1945", 0, 50, 56, hexc("#7a5a10"), outline=0, shadow=False)
        ctx.restore()
        for i, (nm, x) in enumerate((("FLEMING", 480), ("FLOREY", 960), ("CHAIN", 1440))):
            pop_text(ctx, nm, x, 850, 72, tt - 0.8 - i * 0.4, WHITE)
        text(ctx, "Medicine for the world", W / 2, 960, 46, (1, 0.85, 0.3), font=HAND_FONT, outline=4,
             alpha=ease(prog(tt, 2.5, 3)))
    else:
        tt = t - t_lives
        bg_fill(ctx, hexc("#f6efe0"))
        cols, rows = 24, 11
        n = int(cols * rows * ease(prog(tt, 0.2, D - t_lives - 0.5)))
        for i in range(n):
            cx = 120 + (i % cols) * 73
            cy = 160 + (i // cols) * 78
            circle(ctx, cx, cy - 14, 14)
            fs(ctx, WHITE, lw=4)
            line(ctx, cx, cy, cx, cy + 22, 5)
            if i % 37 == 0:
                cap_alone(ctx, cx, cy - 22, 0.12)
        pop_text(ctx, "MILLIONS UPON MILLIONS OF LIVES", W / 2, 1010, 64, tt - 0.4, RED)
    vignette(ctx, 0.35)


def sh_return(ctx, t, D, cue):
    t_case = cue("The watch was back")
    t_touch = cue("Then I touched")
    t_gone = cue("My cap was gone")
    ctx.save()
    z = 1.0 if t < t_touch else lerp(1.0, 1.7, ease(prog(t, t_touch, t_touch + 1.0)))
    cam(ctx, lerp(1200, 1300, ease(prog(t, 0, t_touch))), lerp(540, 330, ease(prog(t, t_touch, t_touch + 1.0))), z)
    museum_bg(ctx, t)
    glass_case(ctx, 1750, 430, t, glow=0.2)
    land = ease_out(prog(t, 0.0, 0.5))
    sq = -0.15 * math.exp(-max(0, t - 0.5) * 6) if t > 0.5 else 0
    touching = t > t_touch
    expr = "smile" if t < t_touch else ("o" if t < t_gone else "shock")
    guy(ctx, 1250, lerp(-300, 470, land), 0.85, t, cap=False, expr=expr, squash=sq, face=0.5 if t < t_touch else 0,
        look=(0.3, -0.3) if not touching else (0, -1),
        rarm=(-2.7, 0.9) if touching else (-0.3, -0.2), larm=(2.7, -0.9) if t > t_gone else (0.3, 0.2),
        brows="worried" if t > t_gone else None)
    ctx.restore()
    if t > t_gone:
        pop_text(ctx, "MY CAP?!", 960, 150, 130, t - t_gone, RED, rot=-0.03)
        sweat(ctx, 1150, 300, 1.4, t)
    vignette(ctx, 0.4)


def painting_pisa(ctx, w, h, t):
    vgrad(ctx, 0, 0, w, h, hexc("#c9b98e"), hexc("#e8dcb4"))
    ctx.rectangle(0, h * 0.78, w, h)
    setc(ctx, hexc("#9a9a6a"))
    ctx.fill()
    pisa_tower(ctx, w / 2, h * 0.82, t, floors=8, lean=4, scaffold=False, s=0.25, dot=True)


def painting_newton(ctx, w, h, t):
    vgrad(ctx, 0, 0, w, h, hexc("#a9b98e"), hexc("#d8dcb4"))
    ctx.rectangle(0, h * 0.75, w, h)
    setc(ctx, hexc("#6a8a4a"))
    ctx.fill()
    apple_tree(ctx, w * 0.42, h * 0.8, t, s=0.26, top_apple=False)
    doodle(ctx, w * 0.62, h * 0.55, 0.22, hair="newton", body=hexc("#4b3b5c"), cap=True, expr="smile", face=-0.5)


def painting_lab(ctx, w, h, t):
    vgrad(ctx, 0, 0, w, h, hexc("#b9b49a"), hexc("#d4ceb4"))
    ctx.rectangle(w * 0.62, h * 0.15, w * 0.24, h * 0.7)
    fs(ctx, hexc("#6a4a2a"), lw=4)
    cap_alone(ctx, w * 0.56, h * 0.38, 0.22, rot=0.25)
    ctx.rectangle(0, h * 0.62, w * 0.55, h * 0.06)
    fs(ctx, hexc("#3f3a36"), lw=3)
    for k in range(3):
        ellipse(ctx, w * 0.12 + k * 50, h * 0.6, 20, 6)
        fs(ctx, (0.95, 0.95, 0.9), lw=2)
    doodle(ctx, w * 0.3, h * 0.42, 0.2, hair="fleming", glasses=True, cap=False, expr="smile",
           bowtie=hexc("#2f4f8f"))


def sh_gallery(ctx, t, D, cue):
    t_p1 = cue("A leaning")
    t_p2 = cue("A young man")
    t_p3 = cue("And a messy")
    frames = [(300, painting_pisa), (900, painting_newton), (1500, painting_lab)]
    # camera: wide, then each painting
    if t < t_p1:
        cx, cy, z = 900, 470, 0.9
    else:
        tgt = [(450, 1, t_p1), (1050, 1, t_p2), (1650, 1, t_p3)]
        idx = 0 if t < t_p2 else 1 if t < t_p3 else 2
        x0 = tgt[idx - 1][0] if idx > 0 else 900
        z0 = 1.9 if idx > 0 else 0.9
        k = ease(prog(t, tgt[idx][2] - 0.3, tgt[idx][2] + 0.7))
        cx = lerp(x0, tgt[idx][0], k)
        z = lerp(z0, 1.9, k)
        cy = lerp(470, 420, k)
    ctx.save()
    cam(ctx, cx, cy, z)
    vgrad(ctx, -800, -300, 3600, 1100, hexc("#7a2b33"), hexc("#5e1f27"))
    for i in range(-8, 40):
        line(ctx, i * 80 - 400, -300, i * 80 - 400, 800, 3, hexc("#6a242c"), 0.8)
    ctx.rectangle(-800, 760, 3600, 600)
    fs(ctx, hexc("#7a5132"), lw=6)
    for x, drawer in frames:
        y, w, h = 230, 300, 380
        frame_box(ctx, x, y, w, h, border=hexc("#c9a040"))
        ctx.save()
        ctx.rectangle(x, y, w, h)
        ctx.clip()
        ctx.translate(x, y)
        drawer(ctx, w, h, t)
        ctx.restore()
        ctx.rectangle(x + w / 2 - 70, y + h + 50, 140, 40)
        fs(ctx, hexc("#e8dcb4"), lw=3)
    # guy without cap looking at paintings
    gx = lerp(0, 1800, ease(prog(t, 0.5, D - 0.5)))
    guy(ctx, cx - 200 / z, 590, 0.6, t, cap=False, expr="shock" if t > t_p1 + 0.5 else "o",
        face=0.2, look=(0.2, -1), larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    # highlight circles
    for x, tt0, (hx, hy, hr) in ((300, t_p1, (466, 282, 34)), (900, t_p2, (1090, 405, 46)), (1500, t_p3, (1668, 375, 50))):
        if t > tt0 + 1.0:
            k = ease_out(prog(t, tt0 + 1.0, tt0 + 1.4))
            ctx.save()
            circle(ctx, hx, hy, hr * (1 + 0.1 * math.sin(t * 8)))
            setc(ctx, (1, 0.9, 0.3), k)
            ctx.set_line_width(5)
            ctx.set_dash([12, 8])
            ctx.stroke()
            ctx.restore()
    ctx.restore()
    vignette(ctx, 0.45)


def sh_ending(ctx, t, D, cue):
    t_photo = cue("in an old painting", frac=0.0)
    t_me = cue("that's me", frac=0.0)
    t_change = cue("Changing")
    t_acc = cue("By accident")
    spiral_bg(ctx, t, speed=0.2)
    # sepia photos sliding past
    rnd = random.Random(6)
    for i in range(6):
        ph = (t * 0.09 + i / 6) % 1
        x = lerp(2300, -400, ph)
        y = 260 + (i % 2) * 520
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(-0.08 + rnd.random() * 0.16)
        rrect(ctx, -170, -130, 340, 260, 6)
        fs(ctx, hexc("#f1e6cc"), lw=5)
        ctx.rectangle(-145, -105, 290, 190)
        fs(ctx, hexc("#b59a6a"), lw=3)
        # sepia scenery silhouettes
        for k in range(3):
            doodle(ctx, -80 + k * 80, -10, 0.16, body=hexc("#7a6040"), cap=False, expr="flat", face=0)
        cap_alone(ctx, -80 + (i % 3) * 80, -38, 0.14)
        ctx.restore()
    k = ease_out(prog(t, 0.2, 0.9))
    wink = t_acc < t < t_acc + 0.8
    guy(ctx, 960, lerp(1400, 470, k), 1.0, t, cap=False, expr="sly" if t > t_me else "smile", face=0,
        larm=(0.3, 0.2), rarm=(-2.2, 0.8) if t > t_me else (-0.3, -0.2), blink=1.0 if wink else None or doodle_auto_blink(t))
    if t > t_change:
        pop_text(ctx, "CHANGING HISTORY.", 960, 140, 100, t - t_change, WHITE)
    if t > t_acc:
        pop_text(ctx, "BY ACCIDENT.", 960, 960, 110, t - t_acc, (1, 0.85, 0.3), rot=-0.03)
    vignette(ctx, 0.5)


def sh_outro(ctx, t, D, cue):
    t_prob = cue("Probably")
    ctx.save()
    cam(ctx, 1500, 450, lerp(1.2, 1.35, ease(prog(t, 0, D))))
    museum_bg(ctx, t)
    # a new exhibit: an ancient-looking hourglass
    ctx.rectangle(1600, 490, 300, 340)
    fs(ctx, MARBLE, lw=6)
    ctx.save()
    ctx.translate(1750, 390)
    poly(ctx, [(-70, -100), (70, -100), (10, 0), (70, 100), (-70, 100), (-10, 0)])
    fs(ctx, (0.85, 0.95, 1.0, 0.6), lw=5)
    ctx.rectangle(-90, -120, 180, 22)
    fs(ctx, hexc("#8a5a2b"), lw=5)
    ctx.rectangle(-90, 98, 180, 22)
    fs(ctx, hexc("#8a5a2b"), lw=5)
    poly(ctx, [(-50, 96), (50, 96), (0, 50)])
    fs(ctx, hexc("#e8cf8f"), lw=0)
    ctx.restore()
    sparkle(ctx, 1810, 330, 30, t)
    reach = ease(prog(t, t_prob, t_prob + 0.6))
    guy(ctx, 1520, 470, 0.85, t, cap=False, expr="flat" if t < t_prob else "sly", face=0.9 if t > t_prob else 0,
        look=(1, 0) if t > t_prob else (0, 0),
        larm=(0.3, 0.2) if t < t_prob else (0.3, 0.2), rarm=(lerp(-0.3, -2.2, reach), lerp(-0.2, 0.1, reach)),
        brows="up" if t < t_prob else None)
    if t < t_prob:
        pop_text(ctx, "Not touching anything.", 1450, 180, 54, t - 0.2, WHITE, font=HAND_FONT, outline=6)
    ctx.restore()
    if t > t_prob:
        pop_text(ctx, "...probably.", 960, 940, 90, t - t_prob, (1, 0.85, 0.3), font=HAND_FONT, outline=8)
    vignette(ctx, 0.45)


def sh_endcard(ctx, t, D, cue):
    spiral_bg(ctx, t, speed=0.3)
    k = ease_out(prog(t, 0.0, 0.6))
    landed = t > 3.0
    guy(ctx, 560, lerp(1400, 470, k), 1.05, t, expr="grin" if landed or t < 2.2 else "o", face=0.4,
        cap=landed, look=(0, 0) if landed else (0, -1),
        larm=(0.3, 0.2), rarm=(-2.6 + 0.3 * math.sin(t * 7), 0.5))
    if 2.2 < t <= 3.0:
        kc = ease_in(prog(t, 2.2, 3.0))
        ctx.save()
        ctx.translate(560, lerp(-250, 470, kc))
        ctx.rotate(6.28 * 2 * (1 - kc))
        ctx.scale(1.05, 1.05)
        from gfx import draw_cap
        draw_cap(ctx)
        ctx.restore()
    if 3.0 < t < 3.6:
        pop_text(ctx, "FOUND IT!", 560, 200, 70, t - 3.0, (1, 0.85, 0.3), rot=-0.05)
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
        text(ctx, "Next time: more history I definitely didn't ruin.", 1300, 760, 46, WHITE, font=HAND_FONT,
             outline=5, alpha=ease(prog(t, 1.8, 2.4)))
    fade = prog(t, D - 1.0, D)
    if fade > 0:
        setc(ctx, (0, 0, 0), fade)
        ctx.paint()


SHOT_FUNCS = {
    "hook": sh_hook, "title": sh_title, "cap": sh_cap, "museum": sh_museum, "touch": sh_touch,
    "tunnel1": sh_tunnel(2026, 1178),
    "pisa_arrive": sh_pisa_arrive, "pisa_basket": sh_pisa_basket, "pisa_soil": sh_pisa_soil,
    "pisa_carry": sh_pisa_carry, "pisa_lean": sh_pisa_lean, "pisa_fact": sh_pisa_fact,
    "tunnel2": sh_tunnel(1178, 1666, hue=(0.15, 0.55, 0.35), hue2=(0.9, 0.85, 0.3)),
    "newton_arrive": sh_newton_arrive, "newton_think": sh_newton_think, "newton_climb": sh_newton_climb,
    "newton_fall": sh_newton_fall, "newton_idea": sh_newton_idea,
    "tunnel3": sh_tunnel(1666, 1928, hue=(0.15, 0.3, 0.75), hue2=(0.4, 0.85, 0.95)),
    "fleming_arrive": sh_fleming_arrive, "fleming_bact": sh_fleming_bact, "fleming_sneeze": sh_fleming_sneeze,
    "fleming_return": sh_fleming_return, "fleming_fact": sh_fleming_fact,
    "tunnel4": sh_tunnel(1928, 2026, hue=(0.75, 0.15, 0.2), hue2=(1.0, 0.75, 0.3), slow=True),
    "return": sh_return, "gallery": sh_gallery, "ending": sh_ending, "outro": sh_outro, "endcard": sh_endcard,
}
