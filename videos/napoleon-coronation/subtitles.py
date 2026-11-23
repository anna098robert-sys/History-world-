"""Write English .srt subtitles from the narration timing. Usage: python3 subtitles.py <vo_dir> <out.srt>"""
import sys
from render import build_timeline


def ts(x):
    h, r = divmod(x, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"


shots, _ = build_timeline(sys.argv[1])
lines, n = [], 1
for sh in shots:
    for a, b, text in sh["sents"]:
        lines.append(f"{n}\n{ts(sh['start'] + a)} --> {ts(sh['start'] + b)}\n{text}\n")
        n += 1
open(sys.argv[2], "w").write("\n".join(lines))
print(n - 1, "subtitles")
