import sys, html
sys.path.insert(0, "/tmp/ce-doc")
from content import *
e = html.escape
def lbl(t): return f'<div class="label">[ {e(t)} ]</div>'
def ph(t): return e(t).replace(e(PLACEHOLDER), '<span class="ph">PLACEHOLDER</span>')
def kv_table(rows): return '<table class="kv">' + "".join(f"<tr><th>{e(k)}</th><td>{ph(v)}</td></tr>" for k, v in rows) + "</table>"

parts = []
parts.append(f'''<section class="page cover">
{lbl("Self-Guided Trip Sheet")}
<h1 class="title">Swiss Alps: Via Alpina</h1>
<p class="sub">Hut to Hut Beneath the Jungfrau · Lauterbrunnen → Kandersteg</p>
<img class="hero" src="file://{COVER}">
<h2>At a Glance</h2>{kv_table(GLANCE)}
<p class="note">This trip sheet covers everything you need for the trek: the route, each day in detail, how to get to the start and home from the finish, what to pack, and ideas for before and after. Your GPX route file and booking confirmations are sent separately.</p>
</section>''')
rows = "".join("<tr" + (' class="total"' if i == len(OVERVIEW_ROWS) - 1 else "") + ">" + "".join(f"<td>{e(v).replace(chr(10), '<br>')}</td>" for v in r) + "</tr>" for i, r in enumerate(OVERVIEW_ROWS))
summ = "".join(f'<li><strong>Day {d["n"]}: {e(d["title"])}.</strong> {e(d["sections"][0][1][0].split(". ")[0])}.</li>' for d in DAYS)
parts.append(f'''<section class="page">
{lbl("Overview")}<h1>High-Level Itinerary</h1>
<p class="lead">Four days crossing two high passes through the Bernese Oberland, with each night in a staffed Swiss mountain hut.</p>
<table class="grid"><thead><tr><th>Day</th><th>Route</th><th>Distance</th><th>Ascent / descent</th><th>Walking time</th><th>Overnight</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Route Summary</h2><ul>{summ}</ul>
<p class="disclaimer">{e(DISCLAIMER)}</p>
</section>''')
parts.append(f'''<section class="page map">
<h2 style="margin-top:0">Route Map</h2>
<img class="mapimg" src="file://{DOC}/map.jpg">
<p class="caption">Red line: the route on marked trails. Red dots: overnight huts. White dots: passes and waypoints. Black dots: start and finish. Map © OpenStreetMap contributors, SRTM; map style © OpenTopoMap (CC-BY-SA). Use the GPX file on your phone for navigation.</p>
</section>''')
for d in DAYS:
    stats = "".join(f"<div><span>{e(k)}</span><strong>{e(v)}</strong></div>" for k, v in d["stats"])
    secs = "".join(f"<h3>{e(h)}</h3>" + "".join(f"<p>{e(t)}</p>" for t in ps) for h, ps in d["sections"])
    parts.append(f'''<section class="page">
{lbl("Day " + str(d["n"]))}<h1>{e(d["title"])}</h1>
<div class="stats">{stats}</div>
<img class="daymap" src="file://{DOC}/daymap-{d["n"]}.jpg"><p class="caption">Today's route is the red dashed line, with arrows showing the direction of travel; the rest of the trek is dashed grey. Map © OpenStreetMap contributors, SRTM; map style © OpenTopoMap (CC-BY-SA).</p>
<img class="profile" src="file://{DOC}/profile-{d["n"]}.png"><p class="caption">Elevation profile. All four days use the same scale.</p>
{secs}</section>''')
parts.append('<section class="page">' + lbl("Travel") + "<h1>Getting There and Back</h1>" +
             "".join(f"<h3>{e(h)}</h3>" + "".join(f"<p>{e(t)}</p>" for t in ps) for h, ps in GETTING) + "</section>")
pack = "".join(f'<div class="pgroup"><h3>{e(h)}</h3><ul class="check">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul></div>" for h, items in PACKING)
parts.append(f'<section class="page">{lbl("Gear")}<h1>Packing List</h1><p class="lead">Aim for a pack weight of 7–9 kg without water. Everything below fits in a 30–40 litre backpack.</p><div class="pack">{pack}</div></section>')
bl = lambda rows: "<ul>" + "".join(f"<li><strong>{e(k)}.</strong> {e(v)}</li>" for k, v in rows) + "</ul>"
parts.append(f'<section class="page">{lbl("Make the Most of It")}<h1>Before and After Your Trek</h1><h2>Before: Lauterbrunnen and Interlaken</h2>{bl(BEFORE)}<h2>After: Kandersteg and Beyond</h2>{bl(AFTER)}</section>')
saf = "".join(f"<h3>{e(k)}</h3><p>{ph(v)}</p>" for k, v in SAFETY)
parts.append(f'<section class="page">{lbl("On the Trail")}<h1>Safety and Hut Life</h1>{saf}<h2>Contact Contour Expeditions</h2>{kv_table(CONTACT)}<p class="disclaimer">{e(DISCLAIMER)}</p></section>')

css = """
@page { size: letter; margin: 0.65in 0.75in 0.7in;
  @top-left { content: "CONTOUR EXPEDITIONS  ·  SWISS ALPS: VIA ALPINA TRIP SHEET"; font: 500 7.5pt Oswald, sans-serif; letter-spacing: .12em; color: #7b858e; }
  @bottom-right { content: "contour-expeditions.com  ·  Page " counter(page); font: 7.5pt Inter, sans-serif; color: #7b858e; } }
@page mappage { size: letter landscape; margin: 0.45in 0.5in; }
body { font: 10pt/1.5 Inter, sans-serif; color: #1f2326; margin: 0; }
.page { break-after: page; }
.page:last-child { break-after: auto; }
.map { page: mappage; }
h1, h2, h3, .title { font-family: Oswald, sans-serif; font-weight: 500; text-transform: uppercase; letter-spacing: .03em; margin: 0; }
h1 { font-size: 22pt; margin-bottom: 10px; } h2 { font-size: 14pt; margin: 18px 0 8px; } h3 { font-size: 10.5pt; color: #c8553d; margin: 14px 0 4px; letter-spacing: .08em; }
.title { font-size: 32pt; line-height: 1.05; }
.label { font: 500 8.5pt Oswald, sans-serif; letter-spacing: .2em; text-transform: uppercase; color: #c8553d; margin-bottom: 4px; }
.sub { font: italic 500 12pt Oswald, sans-serif; color: #4a535b; margin: 4px 0 12px; }
.hero { width: 100%; height: 3.4in; object-fit: cover; border-radius: 4px; }
p { margin: 0 0 7px; } .lead { color: #4a535b; font-size: 10.5pt; }
table { border-collapse: collapse; width: 100%; }
.kv th { width: 1.9in; text-align: left; vertical-align: top; background: #f3f5f6; font: 500 8pt Oswald, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #4a535b; }
.kv th, .kv td { border: 1px solid #d4d8dc; padding: 5px 9px; }
.grid th { background: #1f2326; color: #fff; font: 500 8pt Oswald, sans-serif; letter-spacing: .12em; text-transform: uppercase; text-align: left; padding: 7px 8px; }
.grid td { border-bottom: 1px solid #d4d8dc; padding: 8px; vertical-align: top; font-size: 9.5pt; }
.grid tr.total td { background: #f3f5f6; font-weight: 600; }
ul { padding-left: 18px; margin: 0 0 8px; } li { margin-bottom: 5px; }
.note, .caption, .disclaimer { color: #7b858e; font-size: 8.5pt; } .note { margin-top: 10px; } .disclaimer { font-style: italic; margin-top: 16px; }
.mapimg { width: 100%; border: 1.5px solid #1f2326; border-radius: 3px; }
.stats { display: flex; border: 1px solid #d4d8dc; margin: 4px 0 10px; }
.stats div { flex: 1; padding: 6px 9px; border-right: 1px solid #d4d8dc; } .stats div:last-child { border-right: 0; }
.stats span { display: block; font: 500 7.5pt Oswald, sans-serif; letter-spacing: .14em; text-transform: uppercase; color: #4a535b; }
.stats strong { font-size: 10pt; }
.profile { width: 100%; }
.daymap { width: 100%; border: 1.5px solid #1f2326; border-radius: 3px; display: block; }
h3 { break-after: avoid; }
.pack { columns: 2; column-gap: 28px; } .pgroup { break-inside: avoid; }
.check { list-style: none; padding: 0; } .check li { padding-left: 20px; position: relative; margin-bottom: 3px; font-size: 9.5pt; }
.check li::before { content: ""; position: absolute; left: 0; top: 3px; width: 10px; height: 10px; border: 1.5px solid #c8553d; border-radius: 2px; }
.ph { background: #fbeae6; color: #a8432e; font: 500 8pt Oswald, sans-serif; letter-spacing: .1em; padding: 1px 5px; }
"""
doc = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Via Alpina Trip Sheet</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,600;1,400&family=Oswald:wght@500&display=swap">
<style>{css}</style></head><body>{"".join(parts)}</body></html>'''
open("/tmp/ce-doc/tripsheet.html", "w").write(doc); print("html ok")
