"""Vertical (1080x1920) shots for the Short 'I Accidentally Destroyed Troy!'.
Each shot: fn(ctx, t, D, cue)."""
import math, random
import cairo
from gfx import *
from helpers import cam, cloud, warm_glow, vhs
from egypt_lib import guy, confetti

TIMELINE = {}

WOOD = hexc("#b9824a")
WOOD_D = hexc("#8f5f33")
WOOD_L = hexc("#d6a066")
SEA = hexc("#2f8fd0")
SEA_D = hexc("#1f6fa8")
SAND = hexc("#f2d38a")
SAND_D = hexc("#d9b064")
WALL = hexc("#e6cf9c")
WALL_D = hexc("#c8ad74")
BRONZE = hexc("#d9a23a")
BRONZE_D = hexc("#a8761f")
CREST = hexc("#e0302e")
NIGHT_T = hexc("#0b1230")
NIGHT_B = hexc("#2a3466")
GROUND = 1500


# ====================================================================== props
def trojan_horse(ctx, x, y, s, t, door=0.0, shake=0.0, bow=0.0, roll=0.0, night=False):
    """(x, y) = ground under the platform centre. ~1300*s tall."""
    ctx.save()
    sx = math.sin(t * 40) * 8 * shake
    ctx.translate(x + sx, y)
    ctx.scale(s, s)
    ctx.rotate(math.sin(t * 33) * 0.01 * shake)
    dim = 0.45 if night else 0.0
    W_, WD, WL = (lerpc(c, NIGHT_T, dim) for c in (WOOD, WOOD_D, WOOD_L))
    # platform + wheels
    ctx.rectangle(-430, -150, 860, 70)
    fs(ctx, WD, lw=8)
    for wx in (-330, -110, 110, 330):
        ctx.save()
        ctx.translate(wx, -70)
        circle(ctx, 0, 0, 70)
        fs(ctx, WD, lw=8)
        for k in range(4):
            a = roll + k * math.pi / 4
            line(ctx, -math.cos(a) * 62, -math.sin(a) * 62, math.cos(a) * 62, math.sin(a) * 62, 7, INK)
        circle(ctx, 0, 0, 14)
        fs(ctx, INK, lw=0)
        ctx.restore()
    # legs
    for lx, lean in ((-290, -0.06), (-170, 0.04), (170, -0.04), (290, 0.06)):
        ctx.save()
        ctx.translate(lx, -150)
        ctx.rotate(lean)
        ctx.rectangle(-42, -480, 84, 480)
        fs(ctx, W_, lw=8)
        for k in range(5):
            line(ctx, -42, -60 - k * 90, 42, -60 - k * 90, 4, WD)
        ctx.restore()
    # body barrel
    rrect(ctx, -400, -900, 800, 360, 170)
    fs(ctx, W_, lw=9)
    ctx.save()
    rrect(ctx, -400, -900, 800, 360, 170)
    ctx.clip()
    for k in range(9):
        line(ctx, -400, -880 + k * 42, 400, -880 + k * 42, 5, WD)
    for k in range(8):
        circle(ctx, -350 + k * 100, -720 + (k % 2) * 40, 7)
        fs(ctx, INK, lw=0)
    ctx.rectangle(-400, -900, 800, 70)
    setc(ctx, WL, 0.5)
    ctx.fill()
    ctx.restore()
    rrect(ctx, -400, -900, 800, 360, 170)
    fs(ctx, None, lw=9)
    # tail
    ctx.move_to(-390, -820)
    ctx.curve_to(-520, -800, -540, -640, -480, -520)
    setc(ctx, hexc("#7a4a24"))
    ctx.set_line_width(40)
    ctx.stroke()
    # neck + head
    ctx.move_to(220, -860)
    ctx.line_to(330, -1250)
    ctx.line_to(470, -1220)
    ctx.line_to(400, -800)
    ctx.close_path()
    fs(ctx, W_, lw=9)
    for k in range(5):
        line(ctx, 260 + k * 22, -900 - k * 70, 400 + k * 14, -880 - k * 70, 4, WD)
    ctx.save()
    ctx.translate(420, -1260)
    ctx.rotate(0.25)
    rrect(ctx, -60, -70, 280, 140, 60)
    fs(ctx, W_, lw=9)
    circle(ctx, 30, -10, 18)
    fs(ctx, WHITE, lw=5)
    circle(ctx, 36, -8, 8)
    fs(ctx, INK, lw=0)
    circle(ctx, 190, 20, 10)
    fs(ctx, INK, lw=0)
    poly(ctx, [(-40, -60), (-10, -150), (20, -60)])
    fs(ctx, W_, lw=7)
    ctx.restore()
    # mane
    for k in range(6):
        ctx.move_to(300 + k * 18, -1240 + k * 70)
        ctx.curve_to(240 + k * 18, -1230 + k * 70, 230 + k * 18, -1190 + k * 70, 270 + k * 18, -1170 + k * 70)
        setc(ctx, hexc("#5a3418"))
        ctx.set_line_width(26)
        ctx.stroke()
    # trapdoor in the belly
    ctx.save()
    ctx.translate(-40, -560)
    ctx.rectangle(-60, -10, 120, 90)
    setc(ctx, hexc("#120a06"))
    ctx.fill()
    ctx.rotate(-door * 1.6)
    ctx.rectangle(-60, 0, 120, 14)
    ctx.rectangle(-60, -10, 120, 90 * (1 - door) + 14)
    fs(ctx, WD, lw=6)
    circle(ctx, 40, 40 * (1 - door), 7)
    fs(ctx, BRONZE, lw=3)
    ctx.restore()
    if bow > 0:
        ctx.save()
        ctx.translate(0, -900)
        ctx.scale(bow, bow)
        line(ctx, -400, 160, 400, 160, 34, RED)
        line(ctx, 0, -10, 0, 360, 34, RED)
        for sxx in (-1, 1):
            ctx.move_to(0, -20)
            ctx.curve_to(sxx * 160, -180, sxx * 220, 40, 0, -20)
            fs(ctx, RED, lw=7)
        circle(ctx, 0, -20, 34)
        fs(ctx, hexc("#ff5a5a"), lw=7)
        ctx.restore()
        rrect(ctx, 120, -540, 230, 110, 10)
        fs(ctx, WHITE, lw=6)
        text(ctx, "GIFT!", 235, -485, 60, RED, outline=0, shadow=False)
    ctx.restore()


def helmet(color=BRONZE, crest=CREST, plume_wob=0.0):
    def f(c):
        c.move_to(-108, 40)
        c.curve_to(-120, -150, 120, -150, 108, 40)
        c.line_to(60, 40)
        c.line_to(50, -10)
        c.line_to(-50, -10)
        c.line_to(-60, 40)
        c.close_path()
        fs(c, color, lw=LW)
        line(c, 0, -10, 0, 60, 14, color)
        c.move_to(-90, -110)
        c.curve_to(-40, -230 + plume_wob * 20, 60, -240, 120, -150)
        c.curve_to(60, -170, -20, -170, -90, -110)
        fs(c, crest, lw=6)
    return f


def soldier(ctx, x, y, s, t, seed=0, shield=True, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, seed + 3))
    kw.setdefault("body", hexc("#c8302c"))

    def ex(c, part, *a):
        if part == "body":
            line(c, -60, 150, 60, 150, 10, BRONZE)
            for k in range(5):
                line(c, -50 + k * 25, 230, -50 + k * 25, 320, 7, BRONZE_D)
        if part == "hands" and shield:
            hl = a[0]
            circle(c, hl[0] - 10, hl[1], 80)
            fs(c, BRONZE, lw=6)
            circle(c, hl[0] - 10, hl[1], 30)
            fs(c, CREST, lw=4)
    return doodle(ctx, x, y, s, hair=helmet(plume_wob=math.sin(t * 8 + seed)), cap=False, extra=ex, **kw)


def trojan(ctx, x, y, s, t, seed=0, pajamas=False, **kw):
    kw.setdefault("blink", doodle_auto_blink(t, seed + 7))
    cols = [hexc("#6a5acd"), hexc("#2bb3a0"), hexc("#f2a33a"), hexc("#e86a9a"), hexc("#7ac25a")]
    kw.setdefault("body", hexc("#dfe8ff") if pajamas else cols[seed % 5])

    def band(c):
        if pajamas:
            c.move_to(-100, -20)
            c.curve_to(-90, -160, 120, -170, 170, -60)
            c.curve_to(120, -110, 40, -60, 100, -30)
            c.close_path()
            fs(c, hexc("#b8c8f0"), lw=LW)
            circle(c, 175, -55, 20)
            fs(c, WHITE, lw=4)
        else:
            c.move_to(-102, -40)
            c.curve_to(-60, -82, 60, -82, 102, -40)
            setc(c, [GOLD_C, WHITE, hexc("#ffd36a")][seed % 3])
            c.set_line_width(14)
            c.stroke()
            for k in range(5):
                a = math.pi + 0.35 + k * 0.6
                ellipse(c, math.cos(a) * 96, math.sin(a) * 70 - 30, 18, 10)
                fs(c, hexc("#5aa84a"), lw=3)
    return doodle(ctx, x, y, s, hair=band, cap=False, **kw)


GOLD_C = (1, 0.84, 0.3)


def column(ctx, x, base, h, w=70):
    ctx.rectangle(x - w / 2, base - h, w, h)
    fs(ctx, hexc("#f4efe4"), lw=6)
    for k in (-18, 0, 18):
        line(ctx, x + k, base - h + 20, x + k, base - 20, 3, hexc("#d8cfbd"))
    ctx.rectangle(x - w / 2 - 14, base - h - 24, w + 28, 26)
    fs(ctx, hexc("#e4dccb"), lw=5)


def sky(ctx, t, night=False, dusk=0.0):
    if night:
        vgrad(ctx, -2000, -2500, 6000, 5000, NIGHT_T, NIGHT_B)
        rnd = random.Random(2)
        for i in range(160):
            circle(ctx, rnd.uniform(-1500, 2600), rnd.uniform(-1800, 1100), 1.5 + rnd.random() * 2.5)
            setc(ctx, WHITE, 0.4 + 0.4 * math.sin(t * 2 + i))
            ctx.fill()
        warm_glow(ctx, 760, 260, 300, 0.35, (1, 1, 0.9))
        circle(ctx, 760, 260, 90)
        fs(ctx, hexc("#f6f0d8"), lw=5)
    else:
        top = lerpc(hexc("#4fb3f0"), hexc("#ff8a5a"), dusk)
        bot = lerpc(hexc("#d6f0fb"), hexc("#ffd9a0"), dusk)
        vgrad(ctx, -2000, -2500, 6000, 5000, top, bot)
        warm_glow(ctx, 820, 260, 320, 0.6, (1, 0.95, 0.6))
        circle(ctx, 820, 260, 90)
        fs(ctx, (1, 0.88, 0.35), lw=6)
        for i in range(4):
            cloud(ctx, ((i * 700 + t * 30) % 3200) - 900, 420 + i * 110, 1.2, a=0.8)


def beach_bg(ctx, t):
    sky(ctx, t)
    ctx.rectangle(-2000, 980, 6000, 400)
    fs(ctx, SEA, lw=5)
    for k in range(14):
        ph = (t * 0.3 + k / 14) % 1
        line(ctx, -600 + k * 230 + ph * 60, 1040 + (k % 3) * 60, -520 + k * 230 + ph * 60, 1040 + (k % 3) * 60, 5, WHITE, 0.6)
    # distant Greek ships
    for k, sx in enumerate((-300, 1300, 1750)):
        bx = sx + math.sin(t * 0.7 + k) * 10
        ctx.move_to(bx - 90, 990)
        ctx.curve_to(bx - 60, 1030, bx + 60, 1030, bx + 90, 990)
        ctx.close_path()
        fs(ctx, hexc("#4a2e1a"), lw=4)
        line(ctx, bx, 990, bx, 870, 5)
        poly(ctx, [(bx - 50, 880), (bx + 50, 880), (bx + 46, 970), (bx - 46, 970)])
        fs(ctx, WHITE, lw=4)
    ctx.move_to(-2000, 1230)
    for x in range(-2000, 4001, 80):
        ctx.line_to(x, 1230 + 24 * math.sin(x * 0.01 + t * 2))
    ctx.line_to(4000, 3000)
    ctx.line_to(-2000, 3000)
    ctx.close_path()
    fs(ctx, SAND, lw=6)
    rnd = random.Random(5)
    for i in range(40):
        circle(ctx, rnd.uniform(-1500, 2600), rnd.uniform(1300, 2400), 4)
        setc(ctx, SAND_D)
        ctx.fill()
    # olive tree
    line(ctx, 60, GROUND - 40, 40, 1080, 26, hexc("#6b4428"))
    for dx, dy in ((-60, 1050), (60, 1020), (0, 980), (110, 1070)):
        ellipse(ctx, 40 + dx, dy, 110, 60)
        fs(ctx, hexc("#7a9a4a"), lw=5)


def troy_walls(ctx, t, base=GROUND, night=False, gate_open=0.0, crumble=0.0):
    dim = 0.55 if night else 0.0
    wc = lerpc(WALL, NIGHT_T, dim)
    wd = lerpc(WALL_D, NIGHT_T, dim)
    ctx.rectangle(-2000, base - 900, 6000, 900)
    fs(ctx, wc, lw=8)
    for r in range(10):
        for k in range(-30, 60):
            ctx.rectangle(k * 140 + (70 if r % 2 else 0), base - 900 + r * 90, 140, 90)
    setc(ctx, wd)
    ctx.set_line_width(3)
    ctx.stroke()
    for k in range(-20, 40):
        ctx.rectangle(k * 120, base - 960, 70, 62)
        fs(ctx, wc, lw=6)
    # towers
    for tx in (-200, 1280):
        tilt = crumble * (0.25 if tx > 0 else -0.2)
        ctx.save()
        ctx.translate(tx, base)
        ctx.rotate(tilt)
        ctx.rectangle(-170, -1250, 340, 1250)
        fs(ctx, lerpc(hexc("#ead8aa"), NIGHT_T, dim), lw=8)
        for k in range(4):
            ctx.rectangle(-170 + k * 95, -1310, 60, 62)
            fs(ctx, lerpc(hexc("#ead8aa"), NIGHT_T, dim), lw=6)
        rrect(ctx, -30, -1100, 60, 110, 30)
        fs(ctx, hexc("#3a2a1e"), lw=5)
        # banner
        poly(ctx, [(0, -1310), (0, -1460), (110, -1430 + 10 * math.sin(t * 4)), (0, -1400)])
        fs(ctx, lerpc(hexc("#7a3ab8"), NIGHT_T, dim), lw=4)
        line(ctx, 0, -1310, 0, -1470, 5)
        ctx.restore()
    # gate
    gx = 540
    ctx.move_to(gx - 230, base)
    ctx.line_to(gx - 230, base - 480)
    ctx.curve_to(gx - 230, base - 640, gx + 230, base - 640, gx + 230, base - 480)
    ctx.line_to(gx + 230, base)
    ctx.close_path()
    fs(ctx, hexc("#2a1a10") if not night else hexc("#0a0610"), lw=8)
    for side in (-1, 1):
        ctx.save()
        ctx.translate(gx + side * 230, base)
        ctx.scale(1 - gate_open * 0.85, 1)
        ctx.rectangle(-side * 230 if side > 0 else 0, -560, 230, 560)
        fs(ctx, lerpc(hexc("#8a5a2b"), NIGHT_T, dim), lw=6)
        ctx.restore()
    text(ctx, "TROY", gx, base - 760, 110, lerpc(hexc("#7a3a1a"), NIGHT_T, dim * 0.5), outline=0, shadow=False)


def city_square(ctx, t, night=False, lanterns=True):
    sky(ctx, t, night=night)
    dim = 0.55 if night else 0.0
    cols = [hexc("#f2a3a3"), hexc("#a3d0f2"), hexc("#f2e2a3"), hexc("#b8e2a3"), hexc("#e2b8f2"), hexc("#f2c8a3")]
    rnd = random.Random(3)
    x = -1500
    i = 0
    while x < 2700:
        w = rnd.choice((260, 320, 380))
        h = rnd.choice((520, 620, 720))
        c = lerpc(cols[i % 6], NIGHT_T, dim)
        ctx.rectangle(x, GROUND - 250 - h, w, h)
        fs(ctx, c, lw=7)
        for r in range(int(h / 180)):
            for k in range(int(w / 110)):
                wx = x + 30 + k * 110
                wy = GROUND - 250 - h + 50 + r * 180
                rrect(ctx, wx, wy, 60, 90, 30)
                lit = night and rnd.random() < 0.35
                fs(ctx, hexc("#f6d98a") if lit else lerpc(hexc("#3a4a6a"), NIGHT_T, dim * 0.5), lw=4)
        poly(ctx, [(x - 20, GROUND - 250 - h), (x + w / 2, GROUND - 250 - h - 90), (x + w + 20, GROUND - 250 - h)])
        fs(ctx, lerpc(hexc("#c8553a"), NIGHT_T, dim), lw=6)
        x += w + 10
        i += 1
    # temple with columns in the back
    for k in range(6):
        column(ctx, -100 + k * 140, GROUND - 260, 420)
    ctx.rectangle(-2000, GROUND - 260, 6000, 2000)
    fs(ctx, lerpc(hexc("#e2c896"), NIGHT_T, dim), lw=6)
    for k in range(-20, 40):
        line(ctx, k * 140, GROUND - 260, k * 200 - 600, 3000, 3, lerpc(hexc("#c8ac74"), NIGHT_T, dim), 0.7)
    if lanterns:
        ctx.move_to(-600, GROUND - 900)
        ctx.curve_to(0, GROUND - 780, 1000, GROUND - 780, 1700, GROUND - 900)
        setc(ctx, INK)
        ctx.set_line_width(3)
        ctx.stroke()
        for k in range(9):
            lx = -400 + k * 250
            ly = GROUND - 860 + 70 * math.sin((k + 0.5) / 9 * math.pi)
            if night:
                warm_glow(ctx, lx, ly, 90, 0.4)
            ellipse(ctx, lx, ly, 24, 32)
            fs(ctx, [RED, GOLD_C, hexc("#ff8ad8"), hexc("#6ad0ff")][k % 4], lw=4)


def phone(ctx, x, y, s, t, typed=1.0, stars=1):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rrect(ctx, -330, -620, 660, 1240, 70)
    fs(ctx, hexc("#1c1c22"), lw=10)
    rrect(ctx, -300, -580, 600, 1160, 46)
    fs(ctx, hexc("#f6f7fb"), lw=0)
    rrect(ctx, -70, -560, 140, 30, 15)
    fs(ctx, hexc("#1c1c22"), lw=0)
    text(ctx, "AncientReviews", 0, -470, 50, hexc("#1a4ab8"), outline=0, shadow=False)
    rrect(ctx, -260, -410, 520, 300, 20)
    fs(ctx, hexc("#e8d8b8"), lw=4)
    ctx.save()
    ctx.translate(0, -120)
    ctx.scale(0.23, 0.23)
    trojan_horse(ctx, 0, 0, 1.0, t)
    ctx.restore()
    text(ctx, "Giant Wooden Horse", 0, -60, 46, INK, outline=0, shadow=False)
    text(ctx, "(free gift)", 0, -10, 38, hexc("#6a6a7a"), font=HAND_FONT, outline=0, shadow=False)
    for k in range(5):
        on = k < stars
        star(ctx, -200 + k * 100, 90, 42, (1, 0.8, 0.1) if on else (0.85, 0.85, 0.88), lw=4)
    msg = "Unexpected army included."
    n = int(len(msg) * clamp(typed))
    rrect(ctx, -270, 170, 540, 260, 20)
    fs(ctx, WHITE, lw=4)
    text(ctx, "1/5", -240, 220, 46, RED, align="left", outline=0, shadow=False)
    lines_ = ["Unexpected army", "included."]
    shown = msg[:n]
    l1, l2 = shown[:15], shown[16:]
    text(ctx, l1, -240, 290, 42, INK, font=HAND_FONT, align="left", outline=0, shadow=False)
    text(ctx, l2, -240, 350, 42, INK, font=HAND_FONT, align="left", outline=0, shadow=False)
    if typed >= 1:
        rrect(ctx, -170, 470, 340, 80, 40)
        fs(ctx, hexc("#1a4ab8"), lw=0)
        text(ctx, "POST", 0, 510, 44, WHITE, outline=0, shadow=False)
    ctx.restore()


def portal(ctx, x, y, r, t, a=1.0):
    if r <= 2:
        return
    warm_glow(ctx, x, y, r * 1.8, 0.6 * a, (0.6, 0.85, 1.0))
    for k in range(6):
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(t * (3 + k) * (1 if k % 2 else -1))
        ctx.scale(1, 1.25)
        ctx.arc(0, 0, r * (1 - k * 0.13), 0, math.pi * 1.5)
        setc(ctx, [hexc("#6ad0ff"), GOLD_C, hexc("#b88aff")][k % 3], a)
        ctx.set_line_width(18 - k * 2)
        ctx.stroke()
        ctx.restore()
    ellipse(ctx, x, y, r * 0.35, r * 0.45)
    setc(ctx, WHITE, 0.9 * a)
    ctx.fill()


def hero(ctx, x, y, s, t, **kw):
    return guy(ctx, x, y, s, t, **kw)


def disclaimer(ctx, a=1.0):
    if a <= 0:
        return
    rrect(ctx, 140, 1800, 800, 56, 28)
    fs(ctx, (0, 0, 0, 0.45 * a), lw=0)
    text(ctx, "Fictional comedy inspired by the legend of the Trojan Horse", 540, 1828, 30, WHITE, font=HAND_FONT,
         outline=0, shadow=False, alpha=a)


# ====================================================================== SHOTS
def chaos_scene(ctx, t, freeze=None):
    """the burning-free cartoon chaos of Troy: soldiers everywhere, citizens running in pajamas."""
    city_square(ctx, t, night=True)
    trojan_horse(ctx, 900, GROUND + 60, 0.75, t, door=1.0, night=True)
    rnd = random.Random(1)
    for i in range(7):
        sp = 260 + rnd.random() * 200
        d = 1 if i % 2 else -1
        x = ((rnd.random() * 2400 + d * t * sp) % 2600) - 800
        y = GROUND - 120 + (i % 3) * 140
        if i % 2:
            soldier(ctx, x, y - 290, 0.5, t, seed=i, face=0.9 * d, walk=t * 3 + i, expr="grin",
                    larm=(0.3, 0.2), rarm=(-2.4, 0.3))
        else:
            trojan(ctx, x, y - 290, 0.5, t, seed=i, pajamas=True, face=0.9 * d, walk=t * 3 + i, expr="scared",
                   larm=(2.6, 0.3), rarm=(-2.6, -0.3))
    for i in range(6):
        ph = (t * 0.6 + i / 6) % 1
        circle(ctx, 200 + i * 150, GROUND - 100 - ph * 500, 50 + ph * 80)
        setc(ctx, (0.8, 0.75, 0.7), 0.35 * (1 - ph))
        ctx.fill()


def sh_hook(ctx, t, D, cue):
    t_because = cue("because")
    # beats: 0 face close-up -> 0.9 whip pull-back to reveal horse & chaos -> 2.3 push to face -> freeze at end
    hx, hy = 420, GROUND - 330
    if t < 0.9:
        cx, cy, z = hx + 20, hy - 20, lerp(2.4, 2.1, t / 0.9)
    elif t < t_because:
        k = ease_out(prog(t, 0.9, 1.6))
        cx, cy, z = lerp(hx + 20, 640, k), lerp(hy - 20, 980, k), lerp(2.1, 0.75, k)
    else:
        k = ease(prog(t, t_because, t_because + 0.6))
        cx, cy, z = lerp(640, hx + 160, k), lerp(980, hy - 60, k), lerp(0.75, 1.35, k)
    frozen = t > D - 0.35
    tt = min(t, D - 0.35)
    ctx.save()
    cam(ctx, cx, cy, z, shake=6 if 0.9 < t < 2.0 else 2, t=tt)
    chaos_scene(ctx, tt)
    hero(ctx, hx, hy, 0.62, tt, expr="scared", face=0.0, look=(0, 0), brows="worried",
         larm=(2.6, 0.4), rarm=(-2.6, -0.4), tilt=0.05 * math.sin(tt * 18))
    sweat(ctx, hx + 70, hy - 60, 1.0, tt)
    sweat(ctx, hx - 80, hy - 40, 0.8, tt + 0.3)
    ctx.restore()
    if frozen:
        setc(ctx, (0.15, 0.1, 0.05), 0.3)
        ctx.paint()
    pop_text(ctx, "I ACCIDENTALLY", 540, 250, 78, t - 0.1, WHITE, rot=-0.04)
    pop_text(ctx, "DESTROYED TROY!", 540, 350, 100, t - 0.3, (1, 0.85, 0.2), rot=-0.04)
    disclaimer(ctx, 1 - prog(t, D - 0.6, D))
    vignette(ctx, 0.45)


def sh_discovery(ctx, t, D, cue):
    t_found = cue("I was exploring", frac=0.55)
    t_nobody = cue("Nobody")
    t_take = cue("Nobody", frac=0.7)
    ctx.save()
    if t < 1.6:
        k = ease(prog(t, 0, 1.6))
        cam(ctx, lerp(200, 380, k), GROUND - 400, 1.15)
    elif t < t_nobody:
        k = ease(prog(t, 1.6, 2.6))
        cam(ctx, lerp(380, 820, k), lerp(GROUND - 400, GROUND - 820, k), lerp(1.15, 0.6, k))
    elif t < t_take:
        cam(ctx, 520, GROUND - 400, 1.25)
    else:
        cam(ctx, 700, GROUND - 600, lerp(1.0, 0.85, prog(t, t_take, D)))
    beach_bg(ctx, t)
    trojan_horse(ctx, 1000, GROUND + 30, 0.8, t)
    if t < 1.6:
        hx = lerp(-200, 440, ease_out(prog(t, 0, 1.4)))
        hero(ctx, hx, GROUND - 285, 0.62, t, expr="smile", face=0.9, walk=t * 1.8 if hx < 430 else None,
             larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    elif t < t_nobody:
        knock = math.sin(t * 14) * 0.3 if t > t_found + 0.6 else 0
        hero(ctx, 440, GROUND - 285, 0.62, t, expr="grin" if t > t_found else "shock", face=0.8, look=(1, -1),
             larm=(2.4, 0.3) if t < t_found + 0.6 else (0.3, 0.2), rarm=(-2.4, -0.3) if t < t_found + 0.6 else (-1.6 + knock, 0.3))
        if t > 2.0:
            for k in range(4):
                sparkle(ctx, 470 + (k - 1.5) * 60, GROUND - 420 + math.sin(t * 5 + k) * 20, 22, t + k)
        if t > t_found + 0.6:
            pop_text(ctx, "knock knock", 640, GROUND - 560, 46, t - t_found - 0.6, WHITE, font=HAND_FONT, outline=5, hold=1.0)
    elif t < t_take:
        # looks left, right... sly
        ph = prog(t, t_nobody, t_take)
        look = -1 if ph < 0.35 else (1 if ph < 0.7 else 0)
        hero(ctx, 440, GROUND - 285, 0.62, t, expr="sly" if ph > 0.7 else "flat", face=look * 0.9, look=(look, 0),
             larm=(0.3, 0.2), rarm=(-0.3, -0.2))
    else:
        pull = ease(prog(t, t_take + 0.4, D))
        hx = 440 - 220 * pull
        hero(ctx, hx, GROUND - 285, 0.62, t, expr="grin", face=-0.9, tilt=0.25, walk=t * 1.2, larm=(1.6, -0.5),
             rarm=(1.4, -0.3))
        ctx.move_to(hx + 70, GROUND - 200)
        ctx.curve_to(hx + 250, GROUND - 160, 520, GROUND - 260, 640, GROUND - 330)
        setc(ctx, hexc("#c9a46a"))
        ctx.set_line_width(10)
        ctx.stroke()
    ctx.restore()
    if t_found < t < t_nobody:
        pop_text(ctx, "!!!", 540, 520, 130, t - t_found, (1, 0.85, 0.2), hold=1.0)
    if t > t_take:
        pop_text(ctx, "MINE NOW.", 540, 520, 100, t - t_take, WHITE, rot=-0.05)
    vignette(ctx, 0.35)


def sh_gift(ctx, t, D, cue):
    t_loved = cue("They loved it")
    t_party = cue("They even threw")
    ctx.save()
    if t < t_loved:
        roll = t * 2
        hx = lerp(100, 330, prog(t, 0, t_loved))
        cam(ctx, lerp(300, 520, prog(t, 0, t_loved)), GROUND - 650, 0.72)
        sky(ctx, t)
        troy_walls(ctx, t, gate_open=ease(prog(t, t_loved - 1.0, t_loved)))
        trojan_horse(ctx, hx - 700 + 900, GROUND + 40, 0.55, t, roll=roll, bow=ease_out(prog(t, 1.2, 1.8)))
        hero(ctx, hx + 520, GROUND - 260, 0.55, t, expr="worried", brows="worried", face=0.9, tilt=0.35,
             walk=t * 1.4, larm=(-1.6, 0.5), rarm=(-1.4, 0.3))
        sweat(ctx, hx + 580, GROUND - 340, 0.8, t)
        line(ctx, hx + 470, GROUND - 200, hx + 330, GROUND - 280, 8, hexc("#c9a46a"))
        for k in range(3):
            trojan(ctx, 1000 + k * 120, GROUND - 260, 0.45, t, seed=k, face=-0.7,
                   expr="o" if t < t_loved - 1 else "grin", larm=(0.3, 0.2), rarm=(-0.3, -0.2))
        ctx.restore()
        pop_text(ctx, "\"IT'S A GIFT!\"", 540, 520, 80, t - 1.4, WHITE, hold=t_loved - 1.6)
    elif t < t_party:
        cam(ctx, 540, GROUND - 600, 0.95)
        sky(ctx, t)
        troy_walls(ctx, t, gate_open=1.0)
        for k in range(8):
            jump = abs(math.sin(t * 7 + k)) * 40
            trojan(ctx, 120 + k * 120, GROUND - 260 - jump + (k % 2) * 60, 0.45, t, seed=k, face=0.0, expr="laugh",
                   larm=(2.7, 0.2), rarm=(-2.7, -0.2))
        hero(ctx, 540, GROUND - 470 - abs(math.sin(t * 7)) * 30, 0.5, t, expr="happy", face=0.0, blush=True, larm=(2.6, 0.2), rarm=(-2.6, -0.2))
        ctx.restore()
        confetti(ctx, t)
        pop_text(ctx, "YAAAY!", 540, 520, 130, t - t_loved, (1, 0.85, 0.2), rot=-0.05)
    else:
        tt = t - t_party
        cam(ctx, lerp(560, 700, ease(prog(tt, 0, D - t_party))), GROUND - 650, lerp(0.7, 0.85, ease(prog(tt, 0, 3))))
        city_square(ctx, t)
        trojan_horse(ctx, 1100, GROUND + 60, 0.65, t, bow=1.0)
        for k in range(7):
            x = 100 + k * 150
            dance = math.sin(t * 8 + k)
            trojan(ctx, x, GROUND - 200 + (k % 2) * 90, 0.45, t, seed=k + 2, face=dance * 0.5, expr="laugh",
                   tilt=0.15 * dance, larm=(2.4 + 0.4 * dance, 0.3), rarm=(-2.4 + 0.4 * dance, -0.3),
                   legs=(0.3 * dance, -0.3 * dance))
        # crowd-surfing hero
        hx = 540 + math.sin(t * 2) * 120
        ctx.save()
        ctx.translate(hx, GROUND - 330)
        ctx.rotate(-1.3 + 0.1 * math.sin(t * 5))
        hero(ctx, 0, -120, 0.5, t, expr="laugh", face=0.0, larm=(2.6, 0.3), rarm=(-2.6, -0.3))
        ctx.restore()
        for k in range(3):
            ph = (t * 0.8 + k / 3) % 1
            text(ctx, "♪", 300 + k * 260 + ph * 40, 900 - ph * 200, 80, GOLD_C, font="DejaVu Sans", outline=5,
                 alpha=1 - ph)
        ctx.restore()
        confetti(ctx, t)
        pop_text(ctx, "PARTY FOR ME!", 540, 520, 100, tt - 0.6, WHITE, rot=0.04)
    vignette(ctx, 0.35)


def sh_night(ctx, t, D, cue):
    t_heard = cue("But that night")
    t_sneeze = cue("But that night", frac=0.78)
    t_wait = cue("Wait")
    t_dont = cue("wooden horses")
    jolt = prog(t, t_sneeze, t_sneeze + 0.1) - prog(t, t_sneeze + 0.6, t_sneeze + 1.0)
    ctx.save()
    if t < t_heard + 1.2:
        cam(ctx, lerp(300, 620, ease(prog(t, 0, t_heard + 1.2))), GROUND - 520, 0.85)
    elif t < t_wait:
        cam(ctx, 620, GROUND - 420, lerp(1.3, 1.6, ease(prog(t, t_heard + 1.2, t_sneeze))), shake=14 * jolt, t=t)
    else:
        cam(ctx, 560, GROUND - 360, lerp(2.0, 2.4, ease(prog(t, t_wait, D))), shake=3, t=t)
    city_square(ctx, t, night=True)
    trojan_horse(ctx, 1000, GROUND + 60, 0.75, t, night=True, shake=jolt)
    for k in range(3):
        ph = (t * 0.5 + k / 3) % 1
        text(ctx, "cri cri", 200 + k * 250, 1100 - ph * 60, 34, (0.7, 0.8, 1.0), font=HAND_FONT, outline=0,
             shadow=False, alpha=0.6 * (1 - ph) * (1 - prog(t, t_sneeze, t_sneeze + 0.2)))
    if t < t_heard + 1.2:
        # tiptoe toward the horse
        hx = lerp(80, 560, ease(prog(t, 0, t_heard + 1.2)))
        hero(ctx, hx, GROUND - 285, 0.62, t, expr="o", face=0.9, look=(1, 0), squash=-0.08,
             walk=t * 0.9, larm=(1.4, -1.6), rarm=(-1.4, 1.6), blink=0.0)
    elif t < t_wait:
        sn = t > t_sneeze
        hero(ctx, 560, GROUND - 285, 0.62, t, expr="flat" if not sn else "shock", face=0.9, look=(1, 0),
             tilt=0.18 if not sn else -0.1 - 0.1 * math.sin(t * 30) * (1 - prog(t, t_sneeze, t_sneeze + 0.6)),
             larm=(0.3, 0.2), rarm=(-2.2, 0.9), brows="up" if sn else None)
    else:
        hero(ctx, 560, GROUND - 285, 0.62, t, expr="scared" if t > t_dont else "shock", face=0.0, look=(0, 0),
             larm=(2.6, 0.3), rarm=(-2.6, -0.3), brows="worried")
        sweat(ctx, 640, GROUND - 360, 0.7, t)
    ctx.restore()
    if t_sneeze < t < t_sneeze + 1.7:
        burst(ctx, 720, 620, 190, t - t_sneeze, "ACHOO!", size=78, color=(1, 0.88, 0.3), tcolor=RED)
    if t > t_dont:
        pop_text(ctx, "?!", 540, 560, 160, t - t_dont, (1, 0.85, 0.2))
    vignette(ctx, 0.6)


def sh_twist(ctx, t, D, cue):
    t_door = cue("I opened", frac=0.25)
    t_out = cue("I opened", frac=0.55)
    t_app = cue("Apparently")
    ctx.save()
    if t < t_out:
        cam(ctx, 820, GROUND - 640, lerp(1.6, 1.9, ease(prog(t, 0, t_out))))
    elif t < t_app:
        k = ease_out(prog(t, t_out, t_out + 0.5))
        cam(ctx, lerp(820, 760, k), lerp(GROUND - 640, GROUND - 680, k), lerp(1.9, 0.8, k), shake=8, t=t)
    else:
        k = ease(prog(t, t_app, t_app + 1.0))
        cam(ctx, lerp(760, 600, k), lerp(GROUND - 680, GROUND - 560, k), lerp(0.8, 0.9, k), shake=5, t=t)
    city_square(ctx, t, night=True)
    door = ease_out(prog(t, t_door, t_door + 0.4))
    trojan_horse(ctx, 900, GROUND + 60, 0.75, t, night=True, door=door, shake=0.4 if t > t_out else 0)
    dx, dy = 900 - 30, GROUND + 60 - 0.75 * 560 + 60
    # soldiers dropping out of the hatch and running off in all directions
    if t > t_out:
        n = int(min(18, (t - t_out) / 0.18))
        for i in range(n):
            tt = t - t_out - i * 0.18
            u = clamp(tt / 0.4)
            d = -1 if i % 2 else 1
            x = dx + d * tt * (420 + (i % 5) * 60)
            y = lerp(dy - 120, GROUND - 280 + (i % 4) * 40, ease_in(u)) - math.sin(u * math.pi) * 80
            soldier(ctx, x, y, 0.42, t, seed=i, face=0.9 * d, walk=t * 3 + i if u >= 1 else None,
                    expr="grin" if i % 3 else "laugh", larm=(0.3, 0.2), rarm=(-2.5, 0.3), tilt=(1 - u) * 1.2 * d)
    # the hero: freezes, cap flies off and comes back
    cap_t = t_out + 0.3
    cap_off = 0.0
    if t > cap_t:
        u = prog(t, cap_t, cap_t + 2.6)
        cap_off = math.sin(u * math.pi) * 3.0 if u < 1 else 0.0
    frozen = t_out < t < t_app
    if t < t_app:
        hero(ctx, 560, GROUND - 285, 0.62, t, expr="smile" if t < t_door + 0.4 else "shock", face=0.6, look=(1, -0.3),
             larm=(0.3, 0.2), rarm=(-2.0, 0.6) if t < t_door + 0.4 else (-0.3, -0.2),
             cap_off=cap_off, squash=0.05 if frozen else 0, brows="up" if t > t_out else None)
    else:
        hx = 560 + math.sin((t - t_app) * 2.2) * 300
        hero(ctx, hx, GROUND - 285, 0.6, t, expr="scared", face=math.cos((t - t_app) * 2.2), walk=t * 3,
             larm=(2.6, 0.3), rarm=(-2.6, -0.3), cap_off=cap_off, brows="worried")
        # soldiers parading around, cheering
        for i in range(8):
            d = 1 if i % 2 else -1
            x = ((t - t_app) * (380 + i * 30) * d + i * 330) % 2000 - 400
            soldier(ctx, x, GROUND - 250 + (i % 3) * 70, 0.42, t, seed=i, face=0.9 * d, walk=t * 3 + i,
                    expr="laugh" if i % 2 else "grin", larm=(0.3, 0.2), rarm=(-2.6, 0.3))
        # citizens in pajamas fleeing
        for i in range(4):
            x = ((t - t_app) * 500 * (1 if i % 2 else -1) + i * 400) % 1800 - 300
            trojan(ctx, x, GROUND - 150 + (i % 2) * 60, 0.42, t, seed=i, pajamas=True, face=0.9 if i % 2 else -0.9,
                   walk=t * 3, expr="scared", larm=(2.6, 0.3), rarm=(-2.6, -0.3))
    ctx.restore()
    if t > t_door - 0.1 and t < t_out:
        pop_text(ctx, "*creak*", 540, 560, 70, t - t_door, WHITE, font=HAND_FONT, outline=6)
    if t_out < t < t_out + 2.2:
        burst(ctx, 540, 600, 200, t - t_out, "SURPRISE!", size=66, color=(1, 0.85, 0.3), tcolor=RED)
    if t > t_app + 1.0:
        ctx.save()
        ctx.translate(540, 640)
        ctx.rotate(-0.06)
        k = back_out(prog(t, t_app + 1.0, t_app + 1.4), 2)
        ctx.scale(max(k, 1e-3), max(k, 1e-3))
        rrect(ctx, -330, -70, 660, 140, 20)
        fs(ctx, GOLD_C, lw=8)
        text(ctx, "FREE ARMY INCLUDED", 0, 0, 56, RED, outline=0, shadow=False)
        ctx.restore()
    vignette(ctx, 0.5)


def sh_ending(ctx, t, D, cue):
    t_next = cue("Next time")
    t_phone = t_next - 0.9
    if t < t_phone:
        ctx.save()
        cam(ctx, lerp(540, 700, prog(t, 0, t_phone)), GROUND - 720, 0.72, shake=3, t=t)
        sky(ctx, t, dusk=0.6)
        troy_walls(ctx, t, crumble=ease(prog(t, 0.8, 2.6)))
        for i in range(5):
            ph = (t * 0.5 + i / 5) % 1
            circle(ctx, 100 + i * 240, GROUND - 1000 - ph * 400, 70 + ph * 90)
            setc(ctx, (0.8, 0.72, 0.62), 0.45 * (1 - ph))
            ctx.fill()
        hx = 300 + t * 160
        hero(ctx, hx, GROUND - 285, 0.62, t, expr="scared", face=0.9, walk=t * 3,
             larm=(2.6, 0.3), rarm=(-2.6, -0.3), brows="worried")
        sweat(ctx, hx - 70, GROUND - 340, 0.9, t)
        ctx.restore()
        if t > 1.6:
            burst(ctx, 540, 620, 160, t - 1.6, "BONK!", size=64)
    elif t < t_next + 0.6:
        ctx.save()
        cam(ctx, 540, GROUND - 400, 1.3)
        beach_bg(ctx, t)
        hands = hero(ctx, 520, GROUND - 285, 0.62, t, expr="flat", face=0.3, look=(0.5, 1), larm=(0.3, 0.2),
                     rarm=(-1.6, 1.2))
        rrect(ctx, hands["r"][0] - 25, hands["r"][1] - 70, 50, 90, 8)
        fs(ctx, hexc("#1c1c22"), lw=4)
        ctx.restore()
        pop_text(ctx, "*whips out phone*", 540, 560, 60, t - t_phone, WHITE, font=HAND_FONT, outline=6)
    else:
        tt = t - t_next - 0.6
        bg_fill(ctx, hexc("#2a3f6a"))
        confetti(ctx, t, n=30, a=0.5)
        k = ease_out(prog(tt, 0, 0.5))
        typed = prog(tt, 0.6, 2.8)
        stars = 1 if tt > 0.4 else 0
        phone(ctx, 540, lerp(1900, 900, k), 1.15, t, typed=typed, stars=stars)
        # the hero's thumb
        if tt < 3.0:
            line(ctx, 900, 1900, 760, 1260 + 20 * math.sin(t * 20), 60)
            line(ctx, 900, 1900, 760, 1260 + 20 * math.sin(t * 20), 46, WHITE)
        if tt > 3.0:
            ctx.save()
            ctx.translate(540, 230)
            ctx.rotate(-0.04)
            kk = back_out(prog(tt, 3.0, 3.4), 2)
            ctx.scale(max(kk, 1e-3), max(kk, 1e-3))
            rrect(ctx, -500, -80, 1000, 160, 24)
            fs(ctx, WHITE, lw=8)
            star(ctx, -400, 0, 50, (1, 0.8, 0.1), lw=5)
            text(ctx, "1/5 - Unexpected army included.", 40, 0, 50, INK, font=HAND_FONT, outline=0, shadow=False)
            ctx.restore()
    vignette(ctx, 0.35)


def sh_cta(ctx, t, D, cue):
    t_hist = cue("History isn't")
    spiral_bg(ctx, t, speed=0.25)
    k = ease_out(prog(t, 0.0, 0.4))
    jump = ease_in(prog(t, D - 1.4, D - 0.7))
    pr = 260 * ease_out(prog(t, t_hist - 0.6, t_hist)) * (1 - ease_in(prog(t, D - 0.6, D - 0.15)))
    portal(ctx, 820, 900, pr, t)
    if jump < 1:
        hx = lerp(420, 820, jump)
        hy = lerp(820, 900, jump) - math.sin(jump * math.pi) * 200
        sc = 0.95 * (1 - 0.8 * jump)
        ctx.save()
        ctx.translate(hx, hy)
        ctx.rotate(jump * 6)
        hero(ctx, 0, 0, sc, t, expr="grin" if t < t_hist else "worried", face=0.0, look=(0, 0), blush=True,
             brows="worried" if t > t_hist else None, larm=(0.3, 0.2),
             rarm=(-2.6 + 0.35 * math.sin(t * 9), 0.5))
        ctx.restore()
        sweat(ctx, hx + 90, hy - 70, 1.0, t)
    # subscribe button (above the subtitles)
    kk = back_out(prog(t, 0.2, 0.6), 2) * (1 + 0.04 * math.sin(t * 6))
    ctx.save()
    ctx.translate(540, 300)
    ctx.scale(max(kk, 1e-3), max(kk, 1e-3))
    rrect(ctx, -320, -90, 640, 180, 50)
    fs(ctx, hexc("#ff2a2a"), lw=9)
    poly(ctx, [(-230, -45), (-230, 45), (-160, 0)])
    fs(ctx, WHITE, lw=0)
    text(ctx, "SUBSCRIBE", 40, 0, 88, WHITE, outline=6)
    ctx.restore()
    text(ctx, "HISTORY WORLD", 540, 470, 80, (1, 0.85, 0.2), outline=9, alpha=ease(prog(t, 0.4, 0.8)))
    disclaimer(ctx, ease(prog(t, 0.5, 1.0)))
    fade = prog(t, D - 0.25, D)
    if fade > 0:
        setc(ctx, WHITE, fade)
        ctx.paint()


SHOT_FUNCS = {"hook": sh_hook, "discovery": sh_discovery, "gift": sh_gift, "night": sh_night, "twist": sh_twist,
              "ending": sh_ending, "cta": sh_cta}
