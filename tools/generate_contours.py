#!/usr/bin/env python3
"""Generate a seamlessly tiling topographic contour SVG.

Builds a periodic height field from a sum of sine waves (integer
frequencies, so the left/right and top/bottom edges match), traces
iso-lines with marching squares, and writes them as SVG paths.

Usage: python3 tools/generate_contours.py [output.svg] [--seed N]
"""
import math
import random
import sys

SIZE = 900          # tile size in px
STEP = 6            # grid resolution in px
LEVELS = 22         # number of contour levels
INDEX_EVERY = 5     # every Nth line is a darker "index contour"
LINE = "#d4d8dc"
INDEX_LINE = "#bfc4c9"


def make_field(seed):
    rnd = random.Random(seed)
    waves = []
    for _ in range(14):
        kx = rnd.randint(-3, 3)
        ky = rnd.randint(-3, 3)
        if kx == 0 and ky == 0:
            continue
        amp = 1.0 / math.hypot(kx, ky) ** 1.3
        waves.append((kx, ky, amp, rnd.uniform(0, 2 * math.pi)))

    def h(x, y):
        return sum(a * math.sin(2 * math.pi * (kx * x + ky * y) / SIZE + p)
                   for kx, ky, a, p in waves)
    return h


def trace(h):
    n = SIZE // STEP
    grid = [[h(i * STEP, j * STEP) for i in range(n + 1)] for j in range(n + 1)]
    lo = min(map(min, grid))
    hi = max(map(max, grid))
    levels = [lo + (hi - lo) * (k + 0.5) / LEVELS for k in range(LEVELS)]

    def interp(p1, p2, v1, v2, t):
        f = (t - v1) / (v2 - v1)
        return (round(p1[0] + f * (p2[0] - p1[0]), 1),
                round(p1[1] + f * (p2[1] - p1[1]), 1))

    out = []
    for li, t in enumerate(levels):
        segs = []
        for j in range(n):
            for i in range(n):
                c = [(i * STEP, j * STEP), ((i + 1) * STEP, j * STEP),
                     ((i + 1) * STEP, (j + 1) * STEP), (i * STEP, (j + 1) * STEP)]
                v = [grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]]
                pts = []
                for e in range(4):
                    a, b = e, (e + 1) % 4
                    if (v[a] < t) != (v[b] < t):
                        pts.append(interp(c[a], c[b], v[a], v[b], t))
                if len(pts) == 2:
                    segs.append((pts[0], pts[1]))
                elif len(pts) == 4:  # saddle: pair by centre value
                    centre = sum(v) / 4
                    if (centre < t) == (v[0] < t):
                        segs += [(pts[0], pts[3]), (pts[1], pts[2])]
                    else:
                        segs += [(pts[0], pts[1]), (pts[2], pts[3])]
        out.append((li, join(segs)))
    return out


def join(segs):
    """Chain segments sharing endpoints into polylines."""
    ends = {}
    for idx, (a, b) in enumerate(segs):
        ends.setdefault(a, []).append(idx)
        ends.setdefault(b, []).append(idx)
    used = [False] * len(segs)
    lines = []
    for start in range(len(segs)):
        if used[start]:
            continue
        used[start] = True
        line = list(segs[start])
        for forward in (True, False):
            while True:
                tip = line[-1] if forward else line[0]
                nxt = next((k for k in ends.get(tip, []) if not used[k]), None)
                if nxt is None:
                    break
                used[nxt] = True
                a, b = segs[nxt]
                p = b if a == tip else a
                if forward:
                    line.append(p)
                else:
                    line.insert(0, p)
        lines.append(line)
    return lines


def to_svg(levels):
    paths = []
    for li, lines in levels:
        d = " ".join("M" + " ".join(f"{x:g},{y:g}" for x, y in ln) for ln in lines)
        index = li % INDEX_EVERY == 0
        paths.append(f'<path d="{d}" stroke="{INDEX_LINE if index else LINE}" '
                     f'stroke-width="{1.3 if index else 0.8}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" '
            f'viewBox="0 0 {SIZE} {SIZE}"><g fill="none" stroke-linecap="round" '
            f'stroke-linejoin="round">' + "".join(paths) + "</g></svg>\n")


if __name__ == "__main__":
    args = sys.argv[1:]
    seed = 7
    if "--seed" in args:
        i = args.index("--seed")
        seed = int(args[i + 1])
        del args[i:i + 2]
    dest = args[0] if args else "assets/img/contours.svg"
    with open(dest, "w") as f:
        f.write(to_svg(trace(make_field(seed))))
    print(f"wrote {dest}")
