"""Render a looping 16:9 flat doodle animation: round white head, red cap, red background.

Usage: python3 animations/cap_character.py [output.mp4]
Requires Pillow, numpy and ffmpeg on PATH.
"""
import math, subprocess, sys
from PIL import Image, ImageDraw

W, H, FPS, SECONDS = 1920, 1080, 30, 6
SS = 2                       # supersampling factor for smooth edges
BG = (226, 45, 38)           # solid red background
CAP = (178, 22, 20)          # deeper red so the cap reads against the background
SHADOW = (196, 34, 30)       # flat, slightly darker ellipse under the character
INK, WHITE = (17, 17, 17), (255, 255, 255)
R = 250                      # head radius (1x)
LINE = 15                    # outline thickness (1x)

def ease(x):                 # smooth 0..1..0 pulse helper
    return 0.5 - 0.5 * math.cos(2 * math.pi * x)

def blink_amount(t):
    for start in (1.7, 4.4, 4.75):
        d = t - start
        if 0 <= d < 0.18:
            return math.sin(math.pi * d / 0.18)
    return 0.0

def draw_character(t):
    s = SS
    size = int(R * 4.2 * s)
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx = cy = size / 2
    r, lw = R * s, LINE * s

    # head
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE, outline=INK, width=lw)

    # face: eyes drift slightly left/right, smile
    look = math.sin(2 * math.pi * t / SECONDS) * 0.07 * r
    ey, er = cy + 0.12 * r, 0.085 * r
    squeeze = 1 - 0.88 * blink_amount(t)
    for ex in (cx - 0.32 * r + look, cx + 0.32 * r + look):
        d.ellipse((ex - er, ey - er * squeeze, ex + er, ey + er * squeeze), fill=INK)
    d.arc((cx - 0.26 * r + look, cy + 0.12 * r, cx + 0.26 * r + look, cy + 0.52 * r),
          start=25, end=155, fill=INK, width=int(lw * 0.8))

    # cap brim (sticks out to the right)
    d.rounded_rectangle((cx + 0.25 * r, cy - 0.40 * r, cx + 1.45 * r, cy - 0.18 * r),
                        radius=0.11 * r, fill=CAP, outline=INK, width=lw)
    # cap dome: upper half of an ellipse sitting on the head
    dcx, dcy, drx, dry = cx - 0.02 * r, cy - 0.28 * r, 1.04 * r, 0.92 * r
    d.pieslice((dcx - drx, dcy - dry, dcx + drx, dcy + dry), 180, 360,
               fill=CAP, outline=INK, width=lw)
    # panel seam and top button
    d.arc((dcx - 0.35 * drx, dcy - dry, dcx + 0.35 * drx, dcy + dry), 270, 360,
          fill=INK, width=int(lw * 0.6))
    br = 0.09 * r
    d.ellipse((dcx - br, dcy - dry - br * 1.1, dcx + br, dcy - dry + br * 0.9),
              fill=CAP, outline=INK, width=int(lw * 0.8))
    return layer

def frame(i):
    t = i / FPS
    phase = (t % 1.5) / 1.5                     # 4 hops per 6 s loop
    hop = math.sin(math.pi * phase)             # 0 at ground, 1 at top
    lift = hop * 70
    # squash on landing, stretch while rising
    land = max(0.0, 1 - phase / 0.12) + max(0.0, (phase - 0.88) / 0.12)
    sx = 1 + 0.07 * land - 0.03 * hop
    sy = 1 - 0.07 * land + 0.03 * hop
    tilt = math.sin(2 * math.pi * t / 3.0) * 6

    img = Image.new("RGB", (W * SS, H * SS), BG)
    d = ImageDraw.Draw(img)
    ground = (H / 2 + R + 40) * SS
    sw = (R * 0.95 - hop * 55) * SS
    sh = (34 - hop * 10) * SS
    d.ellipse((W * SS / 2 - sw, ground - sh, W * SS / 2 + sw, ground + sh), fill=SHADOW)

    ch = draw_character(t).rotate(tilt, resample=Image.BICUBIC)
    nw, nh = int(ch.width * sx), int(ch.height * sy)
    ch = ch.resize((nw, nh), Image.BICUBIC)
    # keep the head's bottom planted on the ground line when squashing
    head_bottom = (H / 2 + 30 - lift) * SS + R * SS * sy
    x = int(W * SS / 2 - nw / 2)
    y = int(head_bottom - nh / 2 - R * SS * sy)
    img.paste(ch, (x, y), ch)
    return img.resize((W, H), Image.LANCZOS)

def main(out):
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                          "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(FPS * SECONDS):
        p.stdin.write(frame(i).tobytes())
    p.stdin.close()
    p.wait()

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "cap_character.mp4")
