"""Elevation profile per day: one series, shared y and x scales so days compare at a glance."""
import json, math
route = json.load(open("/tmp/ce-doc/route.json"))
W, H = 1200, 330
L, R, T, B = 70, 24, 76, 46
YMIN, YMAX, XMAX = 750, 3000, 14.5
INK, SLATE, MUTED, GRID, ACCENT = "#1f2326", "#4a535b", "#7b858e", "#e3e6e8", "#c8553d"
marks = {1: [(0, "Lauterbrunnen"), (None, "Mürren"), (-1, "Rotstockhütte")],
         2: [(0, "Rotstockhütte"), (None, "Sefinenfurgge"), (-1, "Gspaltenhornhütte")],
         3: [(0, "Gspaltenhornhütte"), (None, "Hohtürli"), (-1, "Blüemlisalphütte")],
         4: [(0, "Blüemlisalphütte"), (None, "Oeschinensee"), (-1, "Kandersteg")]}
OFFICIAL = {"Lauterbrunnen": 797, "Mürren": 1639, "Rotstockhütte": 2039, "Sefinenfurgge": 2612, "Gspaltenhornhütte": 2455, "Hohtürli": 2778, "Blüemlisalphütte": 2840, "Oeschinensee": 1578, "Kandersteg": 1176}
mid_pts = {"Mürren": (46.56369, 7.89712), "Sefinenfurgge": (46.53156, 7.81293), "Hohtürli": (46.51113, 7.77018), "Oeschinensee": (46.5000, 7.7150)}

def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))

for d in route:
    pts = [c for c in d["coords"] if c[2] is not None]
    dist = [0.0]
    for a, b in zip(pts, pts[1:]):
        dist.append(dist[-1] + hav(a, b))
    # light smoothing of DEM noise (5-point moving average)
    ele = [c[2] for c in pts]
    sm = [sum(ele[max(0, i - 2):i + 3]) / len(ele[max(0, i - 2):i + 3]) for i in range(len(ele))]
    x = lambda km: L + km / XMAX * (W - L - R)
    y = lambda m: T + (YMAX - m) / (YMAX - YMIN) * (H - T - B)
    line = " ".join(f"{x(k):.1f},{y(e):.1f}" for k, e in zip(dist, sm))
    area = f"M{x(0):.1f},{y(YMIN):.1f} L" + line.replace(" ", " L") + f" L{x(dist[-1]):.1f},{y(YMIN):.1f} Z"
    g = []
    for m in range(1000, 3001, 500):
        g.append(f'<line x1="{L}" x2="{W-R}" y1="{y(m):.1f}" y2="{y(m):.1f}" stroke="{GRID}" stroke-width="1"/>'
                 f'<text x="{L-10}" y="{y(m)+4:.1f}" text-anchor="end" font-size="14" fill="{MUTED}">{m:,} m</text>')
    for k in range(0, 15, 2):
        g.append(f'<text x="{x(k):.1f}" y="{H-B+22}" text-anchor="middle" font-size="14" fill="{MUTED}">{k} km</text>')
    labels, placed = [], []
    for idx, name in marks[d["day"]]:
        if idx is None:
            p = mid_pts[name]
            idx = min(range(len(pts)), key=lambda i: hav(pts[i], p))
        i = idx if idx >= 0 else len(pts) - 1
        px, py = x(dist[i]), y(sm[i])
        text = f"{name} · {OFFICIAL[name]:,} m"
        w = len(text) * 8.3
        anchor = "start" if i == 0 else "end" if i == len(pts) - 1 else "middle"
        x0 = px if anchor == "start" else px - w if anchor == "end" else px - w / 2
        if anchor == "middle" and placed and x0 < max(e for r, s0, e in placed if r == 0) + 12:
            pass
        row = 0
        while any(r == row and not (x0 + w + 12 < s0 or x0 > e + 12) for r, s0, e in placed):
            row += 1
        placed.append((row, x0, x0 + w))
        ty = 22 + row * 24
        labels.append(f'<line x1="{px:.1f}" x2="{px:.1f}" y1="{ty+6}" y2="{py-6:.1f}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="2 3"/>'
                      f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#fff" stroke="{INK}" stroke-width="2"/>'
                      f'<text x="{px:.1f}" y="{ty}" text-anchor="{anchor}" font-size="15" fill="{SLATE}"><tspan font-weight="600" fill="{INK}">{name}</tspan> · {OFFICIAL[name]:,} m</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter, Helvetica, Arial, sans-serif">
<rect width="{W}" height="{H}" fill="#fff"/>{"".join(g)}
<line x1="{L}" x2="{W-R}" y1="{y(YMIN):.1f}" y2="{y(YMIN):.1f}" stroke="{MUTED}" stroke-width="1"/>
<path d="{area}" fill="{ACCENT}" fill-opacity="0.12"/>
<polyline points="{line}" fill="none" stroke="{ACCENT}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
{"".join(labels)}
</svg>'''
    open(f"/tmp/ce-doc/profile-{d['day']}.html", "w").write(
        '<!DOCTYPE html><html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap"></head>'
        f'<body style="margin:0">{svg}</body></html>')
print("profiles written")
