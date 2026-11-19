"""Doodle guy stands proud, laurel wreath pops, giant wooden horse slides in.

Renders a 1920x1080, 30 fps, 6 s MP4 using Pillow + ffmpeg.
Usage: python3 proud_trojan_horse.py [output.mp4]
"""
import math, os, subprocess, sys
from PIL import Image, ImageDraw

W, H, FPS, DUR = 1920, 1080, 30, 6.0
SS = 2                      # supersampling factor for anti-aliasing
OL = 9                      # outline thickness (in 1080p px)
BG = (226, 45, 40)
SHADOW = (196, 32, 30)
CAP = (176, 18, 22)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GOLD = (247, 196, 46)
GOLD_D = (214, 158, 20)
WOOD = (176, 112, 58)
WOOD_D = (136, 82, 40)
WOOD_L = (205, 146, 86)
HS = 0.74                   # horse scale


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def ease_in_out(t):
    return t * t * (3 - 2 * t)


def ease_out_back(t, s=2.2):
    t -= 1
    return t * t * ((s + 1) * t + s) + 1


class Pen:
    """Drawing helper working in 1080p units, scaled by SS."""

    def __init__(self, img):
        self.d = ImageDraw.Draw(img)

    def P(self, pts):
        return [(x * SS, y * SS) for x, y in pts]

    def poly(self, pts, fill, ol=OL):
        pts = self.P(pts)
        self.d.polygon(pts, fill=fill)
        if ol:
            self.d.line(pts + [pts[0], pts[1]], fill=BLACK, width=int(ol * SS), joint="curve")
            r = ol * SS / 2
            for x, y in pts:
                self.d.ellipse([x - r, y - r, x + r, y + r], fill=BLACK)

    def ellipse(self, cx, cy, rx, ry, fill, ol=OL):
        b = [(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS]
        if ol:
            o = ol * SS / 2
            self.d.ellipse([b[0] - o, b[1] - o, b[2] + o, b[3] + o], fill=BLACK)
        self.d.ellipse(b, fill=fill)

    def line(self, pts, w=OL, fill=BLACK):
        pts = self.P(pts)
        self.d.line(pts, fill=fill, width=int(w * SS), joint="curve")
        r = w * SS / 2
        for x, y in (pts[0], pts[-1]):
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=fill)

    def arc(self, cx, cy, rx, ry, a0, a1, w=OL, fill=BLACK):
        b = [(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS]
        self.d.arc(b, a0, a1, fill=fill, width=int(w * SS))


def rot_ellipse_pts(cx, cy, rx, ry, ang, n=28):
    ca, sa = math.cos(ang), math.sin(ang)
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return out


def rounded_rect_pts(x0, y0, x1, y1, r, n=8):
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------- character
def draw_character(p, t):
    cx, ground = 640, 900
    # proud breathing + little hop when the wreath lands
    breathe = math.sin(t * 2 * math.pi / 1.6) * 4
    hop_t = clamp((t - 0.55) / 0.35)
    hop = -math.sin(hop_t * math.pi) * 18
    lift = breathe * 0.5 + hop
    chest = 1 + 0.03 * (1 + math.sin(t * 2 * math.pi / 1.6)) / 2

    p.ellipse(cx, ground + 6, 120, 18, SHADOW, ol=0)

    hip_y = 720 + lift
    neck_y = 520 + lift
    # legs
    p.line([(cx - 10, hip_y), (cx - 55, ground)], w=OL * 1.4)
    p.line([(cx + 10, hip_y), (cx + 55, ground)], w=OL * 1.4)
    p.line([(cx - 55, ground), (cx - 90, ground)], w=OL * 1.4)
    p.line([(cx + 55, ground), (cx + 90, ground)], w=OL * 1.4)
    # torso (white shirt, chest puffed)
    tw = 62 * chest
    p.poly([(cx - tw, neck_y + 20), (cx + tw, neck_y + 20), (cx + 48, hip_y + 10), (cx - 48, hip_y + 10)], WHITE)
    # arms: hands on hips, elbows out
    sh_y = neck_y + 40
    for s in (-1, 1):
        sh = (cx + s * tw * 0.85, sh_y)
        el = (cx + s * 150, sh_y + 85)
        hand = (cx + s * 52, hip_y - 10)
        p.line([sh, el, hand], w=OL * 1.4)
        p.ellipse(hand[0], hand[1], 14, 14, WHITE, ol=OL * 0.8)

    # head
    hx, hy, hr = cx, neck_y - 105, 120
    p.ellipse(hx, hy, hr, hr, WHITE)
    # eyes (blink at ~2.6s and ~5.1s)
    blink = any(abs(t - b) < 0.06 for b in (2.6, 5.1))
    for s in (-1, 1):
        ex, ey = hx + s * 40, hy + 5
        if blink:
            p.line([(ex - 12, ey), (ex + 12, ey)], w=OL * 0.9)
        else:
            p.ellipse(ex, ey, 11, 13, BLACK, ol=0)
    # small proud smile
    p.arc(hx, hy + 30, 32, 22, 20, 160, w=OL * 0.9)
    # red baseball cap
    cap_y = hy - 40
    dome = []
    for i in range(21):
        a = math.radians(180 + 180 * i / 20)
        dome.append((hx + 118 * math.cos(a), cap_y + 95 * math.sin(a)))
    p.poly([(hx + 40, cap_y - 12), (hx + 168, cap_y - 8), (hx + 192, cap_y - 1),
            (hx + 196, cap_y + 9), (hx + 172, cap_y + 18), (hx + 40, cap_y + 18)], CAP)
    p.poly(dome + [(hx + 118, cap_y + 6), (hx - 118, cap_y + 6)], CAP)
    p.ellipse(hx, cap_y - 93, 12, 9, CAP, ol=OL * 0.8)
    return hx, hy - hr


# ---------------------------------------------------------------- wreath
def draw_wreath(p, t, top):
    hx, top_y = top
    pt = clamp((t - 0.35) / 0.55)
    if pt <= 0:
        return
    sc = max(0.0, ease_out_back(pt))
    if sc < 0.02:
        return
    bob = math.sin((t - 0.9) * 2 * math.pi / 1.6) * 6 if t > 0.9 else 0
    cx, cy = hx, top_y - 125 + bob
    R, ky = 105 * sc, 0.75
    a0, a1, steps = 100.0, 240.0, 7      # angles for the LEFT branch (y down)

    def pt_at(a, s_):
        r = math.radians(a)
        x = cx + R * math.cos(r)
        return (x if s_ < 0 else 2 * cx - x), cy + R * ky * math.sin(r)

    for s_ in (-1, 1):
        # stem
        stem = [pt_at(a0 + (a1 - a0) * i / 16, s_) for i in range(17)]
        p.line(stem, w=OL * 0.6, fill=GOLD_D)
        for i in range(steps):
            f = (i + 0.5) / steps
            j = f * 16
            k = min(int(j), 15)
            (x0, y0), (x1, y1) = stem[k], stem[k + 1]
            px, py = x0 + (x1 - x0) * (j - k), y0 + (y1 - y0) * (j - k)
            tang = math.atan2(y1 - y0, x1 - x0)
            nx, ny = math.cos(tang + math.pi / 2), math.sin(tang + math.pi / 2)
            sz = sc * (1.0 - 0.3 * f)
            for side, col in ((1, GOLD_D), (-1, GOLD)):
                off = 17 * sz
                lx, ly = px + nx * off * side, py + ny * off * side
                p.poly(rot_ellipse_pts(lx, ly, 25 * sz, 10 * sz, tang - side * 0.7 * -s_, n=20), col, ol=OL * 0.55)
        # top leaf
        (x0, y0), (x1, y1) = stem[-2], stem[-1]
        tang = math.atan2(y1 - y0, x1 - x0)
        p.poly(rot_ellipse_pts(x1 + 18 * sc * math.cos(tang), y1 + 18 * sc * math.sin(tang),
                               24 * sc * 0.7, 10 * sc * 0.7, tang, n=20), GOLD, ol=OL * 0.55)
    # tie at bottom
    p.ellipse(cx, cy + R * ky, 13 * sc, 10 * sc, GOLD_D, ol=OL * 0.6)
    # pop burst lines
    bt = clamp((t - 0.6) / 0.45)
    if 0 < bt < 1:
        for k in range(8):
            a = -math.pi / 2 + (k - 3.5) * 0.38
            r0, r1 = R * 1.1 + 60 * bt, R * 1.1 + 60 * bt + 40 * (1 - bt)
            p.line([(cx + r0 * math.cos(a) * 1.3, cy + r0 * math.sin(a)),
                    (cx + r1 * math.cos(a) * 1.3, cy + r1 * math.sin(a))], w=OL * 0.8 * (1 - bt) + 2, fill=GOLD)


# ---------------------------------------------------------------- horse
def draw_horse(p, t):
    st = clamp((t - 1.3) / 2.6)
    final_x, start_x = 1330, W + 450
    x = start_x + (final_x - start_x) * ease_out_cubic(st)
    # settle rock after stopping
    rock = 0.0
    if t > 3.6:
        k = t - 3.6
        rock = math.sin(k * 9) * math.exp(-k * 3.5) * 0.035
    ground = 900
    dist = start_x - x
    if x > W + 500:
        return

    def T(pts, ox=x, oy=ground):
        # rotate about the front-bottom of the platform for the rock
        ca, sa = math.cos(rock), math.sin(rock)
        out = []
        for px, py in pts:
            px, py = px * HS, py * HS
            out.append((ox + px * ca - py * sa, oy + px * sa + py * ca))
        return out

    p.ellipse(x + 40 * HS, ground + 6, 420 * HS, 20, SHADOW, ol=0)

    wr = 46
    # platform
    p.poly(T([(-330, -70), (390, -70), (390, -30), (-330, -30)]), WOOD_D)
    # wheels with turning spokes
    ang = dist / (wr * HS)
    for wx in (-260, -40, 170, 320):
        (cx, cy), = T([(wx, -30 + wr * 0.35)])
        p.ellipse(cx, cy, wr * HS, wr * HS, WOOD_L)
        for k in range(3):
            a = ang + k * math.pi / 3
            p.line([(cx - wr * HS * 0.8 * math.cos(a), cy - wr * HS * 0.8 * math.sin(a)),
                    (cx + wr * HS * 0.8 * math.cos(a), cy + wr * HS * 0.8 * math.sin(a))], w=OL * 0.7)
        p.ellipse(cx, cy, 10, 10, WOOD_D, ol=OL * 0.6)
    # legs
    for lx in (-230, -120, 150, 260):
        p.poly(T([(lx - 30, -360), (lx + 30, -360), (lx + 26, -70), (lx - 26, -70)]), WOOD_D if lx in (-120, 150) else WOOD)
    # tail
    p.poly(T([(330, -520), (380, -540), (420, -420), (430, -300), (395, -310), (385, -420)]), WOOD_D)
    # body (barrel)
    body = T(rounded_rect_pts(-300, -620, 370, -330, 120))
    p.poly(body, WOOD)
    for py in (-560, -490, -420):
        p.line(T([(-280, py), (350, py)]), w=OL * 0.6)
    for px in (-100, 160):
        p.line(T([(px, -600), (px, -350)]), w=OL * 0.5)
    # hatch door
    p.poly(T([(20, -560), (110, -560), (110, -420), (20, -420)]), WOOD_D, ol=OL * 0.8)
    p.ellipse(*T([(95, -490)])[0], 7, 7, GOLD, ol=OL * 0.4)
    # neck
    p.poly(T([(-300, -560), (-180, -600), (-280, -900), (-400, -860)]), WOOD)
    # mane zigzag
    mane = [(-180, -610)]
    for i in range(7):
        f = (i + 1) / 7
        bx, by = -180 + (-280 + 180) * f, -600 + (-900 + 600) * f
        mane.append((bx + 38, by + 10) if i % 2 == 0 else (bx + 4, by))
    mane += [(-280, -900), (-180, -600)]
    p.poly(T(mane), WOOD_D, ol=OL * 0.8)
    # head
    p.poly(T([(-270, -930), (-410, -960), (-560, -860), (-560, -790), (-420, -790), (-330, -840)]), WOOD)
    # ear
    p.poly(T([(-300, -925), (-270, -1010), (-345, -945)]), WOOD_D)
    # eye + nostril
    p.ellipse(*T([(-380, -880)])[0], 13, 15, BLACK, ol=0)
    p.ellipse(*T([(-530, -825)])[0], 7, 7, BLACK, ol=0)
    p.line(T([(-560, -805), (-480, -805)]), w=OL * 0.6)


# ---------------------------------------------------------------- frames
def render(t):
    img = Image.new("RGB", (W * SS, H * SS), BG)
    p = Pen(img)
    top = draw_character(p, t)
    draw_wreath(p, t, top)
    draw_horse(p, t)
    # slow camera zoom-in (1.00 -> 1.14), toward the space between the two
    z = 1 + 0.14 * ease_in_out(clamp(t / DUR))
    fx, fy = 960 * SS, 600 * SS
    cw, ch = W * SS / z, H * SS / z
    x0 = fx - (fx / (W * SS)) * cw
    y0 = fy - (fy / (H * SS)) * ch
    img = img.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch)))
    return img.resize((W, H), Image.LANCZOS)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "proud_trojan_horse.mp4"
    n = int(FPS * DUR)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                           "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
                           "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(n):
        ff.stdin.write(render(i / FPS).tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", out)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--still":
        render(float(sys.argv[2])).save(sys.argv[3])
    else:
        main()
