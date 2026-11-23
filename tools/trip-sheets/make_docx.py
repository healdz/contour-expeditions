import sys
sys.path.insert(0, "/tmp/ce-doc")
from content import *
from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

INK, SLATE, MUTED, ACCENT, WASH = RGBColor(0x1F, 0x23, 0x26), RGBColor(0x4A, 0x53, 0x5B), RGBColor(0x7B, 0x85, 0x8E), RGBColor(0xC8, 0x55, 0x3D), "F3F5F6"
HEAD, BODY = "Oswald", "Inter"

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for side in ("left_margin", "right_margin"): setattr(sec, side, Inches(0.75))
sec.top_margin, sec.bottom_margin = Inches(0.7), Inches(0.7)

st = doc.styles["Normal"]; st.font.name = BODY; st.font.size = Pt(10.5); st.font.color.rgb = INK
st.element.rPr.rFonts.set(qn("w:eastAsia"), BODY)
st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 1.2
for name, size, color in (("Heading 1", 22, INK), ("Heading 2", 14, INK), ("Heading 3", 11, ACCENT)):
    h = doc.styles[name]; h.font.name = HEAD; h.font.size = Pt(size); h.font.bold = False; h.font.color.rgb = color
    h.font.all_caps = True; h.element.rPr.rFonts.set(qn("w:asciiTheme"), "") if False else None
    rf = h.element.rPr.find(qn("w:rFonts"))
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"): rf.set(qn(a), HEAD)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]
    h.paragraph_format.space_before = Pt(14 if name != "Heading 3" else 10); h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexcolor); tcPr.append(shd)

def borders(table, color="D4D8DC"):
    tblPr = table._tbl.tblPr; b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}"); e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), color); b.append(e)
    tblPr.append(b)

def cell_text(cell, text, bold=False, color=None, size=None, font=None, caps=False):
    cell.text = ""; p = cell.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
    for i, line in enumerate(str(text).split("\n")):
        if i: p.add_run().add_break()
        r = p.add_run(line); r.bold = bold; r.font.all_caps = caps
        if color: r.font.color.rgb = color
        if size: r.font.size = Pt(size)
        if font: r.font.name = font

def para(text, color=None, size=None, italic=False, bold=False, align=None, after=None):
    p = doc.add_paragraph(); r = p.add_run(text); r.italic = italic; r.bold = bold
    if color: r.font.color.rgb = color
    if size: r.font.size = Pt(size)
    if align: p.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    return p

def label(text):
    p = doc.add_paragraph(); r = p.add_run(f"[ {text} ]"); r.font.name = HEAD; r.font.size = Pt(9); r.font.color.rgb = ACCENT
    p.paragraph_format.space_after = Pt(2); return p

def field(paragraph, instr):
    r = paragraph.add_run(); f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin"); r._r.append(f1)
    r2 = paragraph.add_run(); it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = instr; r2._r.append(it)
    r3 = paragraph.add_run(); f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end"); r3._r.append(f2)

def header_footer(section):
    section.header.is_linked_to_previous = False; section.footer.is_linked_to_previous = False
    hp = section.header.paragraphs[0]; hp.text = ""
    r = hp.add_run("CONTOUR EXPEDITIONS  ·  SWISS ALPS: VIA ALPINA TRIP SHEET"); r.font.name = HEAD; r.font.size = Pt(8); r.font.color.rgb = MUTED
    fp = section.footer.paragraphs[0]; fp.text = ""; fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = fp.add_run("contour-expeditions.com  ·  Page "); r.font.size = Pt(8); r.font.color.rgb = MUTED
    field(fp, "PAGE")
    for run in fp.runs: run.font.size = Pt(8); run.font.color.rgb = MUTED

header_footer(sec)

# ---------- Cover ----------
label("Self-Guided Trip Sheet")
t = doc.add_paragraph(); r = t.add_run("Swiss Alps: Via Alpina"); r.font.name = HEAD; r.font.size = Pt(32); r.font.all_caps = True; r.font.color.rgb = INK
t.paragraph_format.space_after = Pt(0)
para("Hut to Hut Beneath the Jungfrau  ·  Lauterbrunnen → Kandersteg", SLATE, 12, italic=True, after=10)
doc.add_picture(COVER, width=Inches(7))
doc.add_heading("At a Glance", level=2)
tb = doc.add_table(rows=0, cols=2); borders(tb); tb.alignment = WD_TABLE_ALIGNMENT.CENTER
for k, v in GLANCE:
    row = tb.add_row().cells; cell_text(row[0], k, color=SLATE, size=8.5, font=HEAD, caps=True); shade(row[0], WASH); cell_text(row[1], v, size=10)
for row in tb.rows: row.cells[0].width, row.cells[1].width = Inches(1.9), Inches(5.1)
para("This trip sheet covers everything you need for the trek: the route, each day in detail, how to get to the start and home from the finish, what to pack, and ideas for before and after. Your GPX route file and booking confirmations are sent separately.", SLATE, 9.5, after=0).paragraph_format.space_before = Pt(8)

# ---------- High-level itinerary ----------
doc.add_page_break()
label("Overview")
doc.add_heading("High-Level Itinerary", level=1)
para("Four days crossing two high passes through the Bernese Oberland, with each night in a staffed Swiss mountain hut.", SLATE)
tb = doc.add_table(rows=1, cols=6); borders(tb)
for c, h in zip(tb.rows[0].cells, ("Day", "Route", "Distance", "Ascent / descent", "Walking time", "Overnight")):
    cell_text(c, h, color=RGBColor(0xFF, 0xFF, 0xFF), size=8.5, font=HEAD, caps=True); shade(c, "1F2326")
for i, rowdata in enumerate(OVERVIEW_ROWS):
    row = tb.add_row().cells; last = i == len(OVERVIEW_ROWS) - 1
    for c, v in zip(row, rowdata): cell_text(c, v, bold=last, size=9.5)
    if last:
        for c in row: shade(c, WASH)
widths = (0.45, 2.2, 0.75, 1.2, 1.15, 1.25)
for row in tb.rows:
    for c, w in zip(row.cells, widths): c.width = Inches(w)
doc.add_heading("Route Summary", level=2)
for d in DAYS:
    p = doc.add_paragraph(style="List Bullet"); r = p.add_run(f"Day {d['n']}: {d['title']}. "); r.bold = True
    p.add_run(d["sections"][0][1][0].split(". ")[0] + ".")
p = para(DISCLAIMER, MUTED, 8.5, italic=True); p.paragraph_format.space_before = Pt(10)

# ---------- Map (landscape page) ----------
ms = doc.add_section(WD_SECTION.NEW_PAGE); ms.orientation = WD_ORIENT.LANDSCAPE
ms.page_width, ms.page_height = Inches(11), Inches(8.5)
for side in ("left_margin", "right_margin"): setattr(ms, side, Inches(0.5))
ms.top_margin, ms.bottom_margin = Inches(0.55), Inches(0.5)
header_footer(ms)
h = doc.add_heading("Route Map", level=2); h.paragraph_format.space_before = Pt(0)
doc.add_picture(f"{DOC}/map.jpg", width=Inches(10))
para("Red line: the route on marked trails. Red dots: overnight huts. White dots: passes and waypoints. Black dots: start and finish. "
     "Map © OpenStreetMap contributors, SRTM; map style © OpenTopoMap (CC-BY-SA). Use the GPX file on your phone for navigation.", MUTED, 8, after=0)

# ---------- Days ----------
ds = doc.add_section(WD_SECTION.NEW_PAGE); ds.orientation = WD_ORIENT.PORTRAIT
ds.page_width, ds.page_height = Inches(8.5), Inches(11)
for side in ("left_margin", "right_margin"): setattr(ds, side, Inches(0.75))
ds.top_margin, ds.bottom_margin = Inches(0.7), Inches(0.7)
header_footer(ds)
for i, d in enumerate(DAYS):
    if i: doc.add_page_break()
    label(f"Day {d['n']}")
    doc.add_heading(d["title"], level=1)
    tb = doc.add_table(rows=2, cols=len(d["stats"])); borders(tb)
    for j, (k, v) in enumerate(d["stats"]):
        cell_text(tb.rows[0].cells[j], k, color=SLATE, size=8, font=HEAD, caps=True); shade(tb.rows[0].cells[j], WASH)
        cell_text(tb.rows[1].cells[j], v, bold=True, size=10)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    doc.add_picture(f"{DOC}/daymap-{d['n']}.jpg", width=Inches(7))
    para("Today's route is the red dashed line, with arrows showing the direction of travel; the rest of the trek is dashed grey. Map © OpenStreetMap contributors, SRTM; map style © OpenTopoMap (CC-BY-SA).", MUTED, 8, after=6)
    doc.add_picture(f"{DOC}/profile-{d['n']}.png", width=Inches(7))
    para("Elevation profile. All four days use the same scale.", MUTED, 8, after=4)
    for heading, paras in d["sections"]:
        doc.add_heading(heading, level=3)
        for t in paras: para(t)

# ---------- Getting there ----------
doc.add_page_break(); label("Travel"); doc.add_heading("Getting There and Back", level=1)
for heading, paras in GETTING:
    doc.add_heading(heading, level=3)
    for t in paras: para(t)

# ---------- Packing ----------
doc.add_page_break(); label("Gear"); doc.add_heading("Packing List", level=1)
para("Aim for a pack weight of 7–9 kg without water. Everything below fits in a 30–40 litre backpack.", SLATE)
for heading, items in PACKING:
    doc.add_heading(heading, level=3)
    for it in items:
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(1); p.paragraph_format.left_indent = Inches(0.1)
        r = p.add_run("☐  "); r.font.color.rgb = ACCENT; p.add_run(it)

# ---------- Before & after ----------
doc.add_page_break(); label("Make the Most of It"); doc.add_heading("Before and After Your Trek", level=1)
doc.add_heading("Before: Lauterbrunnen and Interlaken", level=2)
for k, v in BEFORE:
    p = doc.add_paragraph(style="List Bullet"); r = p.add_run(k + ". "); r.bold = True; p.add_run(v)
doc.add_heading("After: Kandersteg and Beyond", level=2)
for k, v in AFTER:
    p = doc.add_paragraph(style="List Bullet"); r = p.add_run(k + ". "); r.bold = True; p.add_run(v)

# ---------- Safety ----------
doc.add_page_break(); label("On the Trail"); doc.add_heading("Safety and Hut Life", level=1)
for k, v in SAFETY:
    doc.add_heading(k, level=3); para(v)
doc.add_heading("Contact Contour Expeditions", level=2)
tb = doc.add_table(rows=0, cols=2); borders(tb)
for k, v in CONTACT:
    row = tb.add_row().cells; cell_text(row[0], k, color=SLATE, size=8.5, font=HEAD, caps=True); shade(row[0], WASH); cell_text(row[1], v, size=10)
for row in tb.rows: row.cells[0].width, row.cells[1].width = Inches(1.9), Inches(5.1)
p = para(DISCLAIMER, MUTED, 8.5, italic=True); p.paragraph_format.space_before = Pt(12)

out = sys.argv[1]
doc.save(out); print("saved", out)
