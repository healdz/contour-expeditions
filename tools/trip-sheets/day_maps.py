import json
route = json.load(open("/tmp/ce-doc/route.json"))
lines = [[[round(c[0], 5), round(c[1], 5)] for c in d["coords"]] for d in route]
pts = [
  ["Lauterbrunnen", 46.59836, 7.90804, "start", "797 m · Start"], ["Mürren", 46.56369, 7.89712, "town", "1,639 m"],
  ["Rotstockhütte", 46.54516, 7.83832, "hut", "2,039 m · Night 1"], ["Sefinenfurgge", 46.53156, 7.81293, "pass", "2,612 m"],
  ["Gspaltenhornhütte", 46.51269, 7.81026, "hut", "2,455 m · Night 2"], ["Hohtürli", 46.51113, 7.77018, "pass", "2,778 m"],
  ["Blüemlisalphütte", 46.51016, 7.77164, "hut", "2,840 m · Night 3"], ["Oeschinensee", 46.5000, 7.7150, "town", "1,578 m · lakeside"],
  ["Kandersteg", 46.49556, 7.67151, "start", "1,176 m · Finish"],
]
days = [
  (1, "Day 1 · Lauterbrunnen → Rotstockhütte", "Approx. 13 km · +1,500 m / −250 m", ["Lauterbrunnen", "Mürren", "Rotstockhütte"],
   {"Lauterbrunnen": "right", "Mürren": "right", "Rotstockhütte": "left"}),
  (2, "Day 2 · Rotstockhütte → Gspaltenhornhütte", "Approx. 6.5 km · +850 m / −450 m", ["Rotstockhütte", "Sefinenfurgge", "Gspaltenhornhütte"],
   {"Rotstockhütte": "right", "Sefinenfurgge": "left", "Gspaltenhornhütte": "right"}),
  (3, "Day 3 · Gspaltenhornhütte → Blüemlisalphütte", "Approx. 7.5 km · +1,000 m / −600 m", ["Gspaltenhornhütte", "Hohtürli", "Blüemlisalphütte"],
   {"Gspaltenhornhütte": "right", "Hohtürli": "left", "Blüemlisalphütte": "right"}),
  (4, "Day 4 · Blüemlisalphütte → Kandersteg", "Approx. 12 km · +150 m / −1,800 m", ["Blüemlisalphütte", "Oeschinensee", "Kandersteg"],
   {"Blüemlisalphütte": "left", "Oeschinensee": "bottom", "Kandersteg": "right"}),
]
tpl = open("/tmp/ce-doc/day_template.html").read()
for n, title, sub, names, dirs in days:
    h = (tpl.replace("__LINES__", json.dumps(lines)).replace("__PTS__", json.dumps(pts, ensure_ascii=False))
            .replace("__DAY__", str(n)).replace("__TITLE__", title).replace("__SUB__", sub + " · red dashed line = today's trail")
            .replace("__NAMES__", json.dumps(names, ensure_ascii=False)).replace("__DIRS__", json.dumps(dirs, ensure_ascii=False)))
    open(f"/tmp/ce-doc/daymap-{n}.html", "w").write(h)
print("ok")
