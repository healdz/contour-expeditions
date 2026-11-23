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
html = open("/tmp/ce-doc/map_template.html").read().replace("__LINES__", json.dumps(lines)).replace("__PTS__", json.dumps(pts, ensure_ascii=False))
open("/tmp/ce-doc/map.html", "w").write(html)
print("map.html written")
