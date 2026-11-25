"""One-off generator for the Contour Expeditions static HTML. Run: python3 build.py <site_dir>"""
import html
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from trips import TRIPS

SITE = sys.argv[1]
GUIDED = [t for t in TRIPS if t["type"] == "guided"]
UNGUIDED = [t for t in TRIPS if t["type"] == "unguided"]
YEAR = 2026
EMAIL = "info@contour-expeditions.com"
SUPPORT_EMAIL = "support@contour-expeditions.com"  # shown to visitors after a form is sent
PHONE = "+1 (970) 456-9659"  # also on WhatsApp
PHONE_TEL = "+19704569659"
# FormSubmit (formsubmit.co) delivers all three site forms to this inbox. After activation, swap the
# address for the random string FormSubmit emails you, so the address isn't exposed to bots.
FORM_TO = "f3d10a96e8d7729009c83224eed1bda3"  # FormSubmit alias for info@; works once the activation email has been confirmed
VER = 18
SITE_URL = "https://contour-expeditions.com/"
DEFAULT_OG = "assets/img/photos/home-hero.jpg"
SITEMAP = []


def abs_url(path):
    return SITE_URL + ("" if path == "index.html" else path[:-5] if path.endswith(".html") else path)


def clean_links(doc):
    """Drop .html from internal page links (GitHub Pages serves /about for about.html)."""
    import re
    doc = re.sub(r'href="((?:\.\./)*|/)?index\.html', lambda m: 'href="' + (m.group(1) or "./"), doc)
    return re.sub(r'href="(?!https?:|mailto:)([^"?#]*?)\.html(?=[?#"])', r'href="\1', doc)


def jsonld(data):
    return '\n  <script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/") + '</script>'


PROVIDER = {"@type": "TravelAgency", "@id": SITE_URL + "#organization", "name": "Contour Expeditions", "url": SITE_URL,
            "logo": SITE_URL + "assets/img/favicon-512.png"}

def img(t, root, size="full"):
    if t.get("image"):
        return f'{root}assets/img/photos/{t["image"] if size == "full" else t["thumb"]}'
    return f'{root}assets/img/placeholders/{t["slug"]}.svg'
e = html.escape

# ----------------------------------------------------------------- placeholders
def placeholder(name, label, sky, mist, ground, seed, w=1600, h=1000):
    rnd = random.Random(seed)
    layers = []
    for i, (base, amp, col, op) in enumerate([(0.42, 0.22, ground, 0.45), (0.55, 0.18, ground, 0.7), (0.7, 0.14, ground, 1)]):
        pts, x = [], 0
        y = base * h
        while x <= w:
            pts.append(f"{x},{y:.0f}")
            x += rnd.randint(60, 160)
            y = max(h * 0.15, min(h * 0.92, y + rnd.uniform(-amp, amp) * h * 0.6))
        pts.append(f"{w},{y:.0f}")
        layers.append(f'<polygon points="0,{h} {" ".join(pts)} {w},{h}" fill="{col}" fill-opacity="{op}"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky}"/><stop offset="1" stop-color="{mist}"/></linearGradient></defs>
<rect width="{w}" height="{h}" fill="url(#g)"/>
<circle cx="{rnd.randint(int(w*0.55), int(w*0.85))}" cy="{int(h*0.22)}" r="{int(h*0.07)}" fill="#fff" fill-opacity="0.55"/>
{"".join(layers)}
<text x="{w-40}" y="{h-36}" text-anchor="end" font-family="Arial, sans-serif" font-size="22" letter-spacing="4" fill="#fff" fill-opacity="0.7">PHOTO PLACEHOLDER · {e(label.upper())}</text>
</svg>
'''
    with open(os.path.join(SITE, "assets/img/placeholders", name), "w") as f:
        f.write(svg)

def make_placeholders():
    for i, t in enumerate(TRIPS):
        if "colors" not in t: continue
        placeholder(f"{t['slug']}.svg", t["name"], *t["colors"], seed=i + 1)
    extra = [
        ("home-hero.svg", "Expedition hero", ("#4f5d6a", "#d6dde3", "#222a31")),
        ("guided.svg", "Guided trips", ("#6a5d58", "#e8ddd6", "#2e2522")),
        ("unguided.svg", "Unguided trips", ("#58706a", "#dbe6e2", "#22302c")),
        ("customize.svg", "Custom expedition", ("#6c6a85", "#e2e0ec", "#2b2a3a")),
        ("about.svg", "Our team in the field", ("#7a6f5c", "#ece6da", "#332d22")),
        ("team-1.svg", "Founder", ("#8b97a1", "#e6eaed", "#3b444b")),
        ("team-2.svg", "Expedition lead", ("#8f9a8a", "#e8ece5", "#3c4537")),
        ("team-3.svg", "Trip designer", ("#9c8f86", "#efe9e4", "#463c35")),
    ]
    for i, (n, lbl, cols) in enumerate(extra):
        placeholder(n, lbl, *cols, seed=100 + i, h=1000 if "team" not in n else 1600)

# ------------------------------------------------------------------- partials
import re as _re
_IDX = open(os.path.join(SITE, "index.html")).read()
LOGO_H, LOGO_F = _re.findall(r'<svg viewBox="0 0 40 40" aria-hidden="true"><defs><clipPath id="logo-hex-[hf]">.*?</svg>', _IDX)[:2]
LOGO_OLD = '''<svg viewBox="0 0 40 40" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.6"><path d="M20 3c9 0 17 6 17 16s-7 18-17 18S3 30 3 20 11 3 20 3z"/><path d="M20 9c6 0 11 4 11 10s-5 12-11 12S9 26 9 20s5-11 11-11z" opacity=".75"/><path d="M21 15c3 0 5 2 5 5s-3 6-6 6-5-3-5-6 3-5 6-5z" opacity=".55"/></g><circle cx="21" cy="20.5" r="2" fill="#c8553d"/></svg>'''
CHEV = '<svg class="chev" width="10" height="10" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
ICON_IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor"/></svg>'
ICON_FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4h-3c-2.8 0-4.5 1.8-4.5 4.6V11H7v4h2.5v6h4v-6H17l.5-4h-4V8.8c0-.5.3-.8.5-.8z" fill="currentColor"/></svg>'
ICON_STRAVA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 2 4 14h4l2-4 2 4h4L10 2zm5 12-2 4-2-4H9l4 8 4-8h-2z" fill="currentColor"/></svg>'

def nav(root, active):
    def dd(key, title, trips, all_href, all_label):
        cur = ' class="has-dropdown is-current"' if active == key else ' class="has-dropdown"'
        items = "".join(f'<li><a href="{root}trips/{t["slug"]}.html">{e(t["nav"])}<span>{e(t["navsub"])}</span></a></li>' for t in trips)
        return f'''<li{cur}>
          <button class="dropdown-toggle" aria-expanded="false" aria-controls="dd-{key}">{title} {CHEV}</button>
          <ul class="dropdown" id="dd-{key}">
            {items}
            <li class="dropdown-all"><a href="{root}{all_href}">{all_label} →</a></li>
          </ul>
        </li>'''
    def link(key, href, label, extra=""):
        cur = ' aria-current="page"' if active == key else ""
        return f'<li{extra}><a href="{root}{href}"{cur}>{label}</a></li>'
    return f'''<a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="{root}index.html" aria-label="Contour Expeditions home">
        {LOGO_H}
        <span class="brand-name">Contour<small>Expeditions</small></span>
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Menu">
        <svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><path d="M2 6h18M2 11h18M2 16h18" stroke="currentColor" stroke-width="1.8"/></svg>
      </button>
      <nav class="primary-nav" id="primary-nav" aria-label="Main">
        <ul>
          {dd("guided", "Guided Expeditions", GUIDED, "guided-trips.html", "All guided trips")}
          {dd("unguided", "Unguided Adventures", UNGUIDED, "unguided-trips.html", "All unguided trips")}
          {link("customize", "customize.html", "Customize Your Adventure")}
          {link("about", "about.html", "About")}
          {link("contact", "contact.html", "Contact", ' class="nav-cta"')}
        </ul>
      </nav>
    </div>
  </header>'''

def footer(root):
    tiles = "".join(f'<a href="{root}trips/{t["slug"]}.html"><img src="{img(t, root, "thumb")}" alt="" loading="lazy"><span>{e(t["name"])}</span></a>' for t in TRIPS)
    g = "".join(f'<li><a href="{root}trips/{t["slug"]}.html">{e(t["name"])}</a></li>' for t in GUIDED)
    u = "".join(f'<li><a href="{root}trips/{t["slug"]}.html">{e(t["name"])}</a></li>' for t in UNGUIDED)
    return f'''<footer class="site-footer">
    <div class="container">
      <div class="footer-index" aria-label="Expedition index">{tiles}</div>
      <div class="footer-grid">
        <div>
          <a class="brand" href="{root}index.html">{LOGO_F}<span class="brand-name">Contour<small>Expeditions</small></span></a>
          <p class="footer-tagline">Guided expeditions, self-guided adventures, and custom trips for people who read maps for fun.</p>
          <div class="socials">
            <a href="#" data-todo="social-link" aria-label="Instagram">{ICON_IG}</a>
            <a href="#" data-todo="social-link" aria-label="Facebook">{ICON_FB}</a>
            <a href="#" data-todo="social-link" aria-label="Strava">{ICON_STRAVA}</a>
          </div>
        </div>
        <div>
          <h4>Guided</h4>
          <ul>{g}</ul>
        </div>
        <div>
          <h4>Unguided</h4>
          <ul>{u}</ul>
        </div>
        <div>
          <h4>Explore</h4>
          <ul>
            <li><a href="{root}customize.html">Customize Your Adventure</a></li>
            <li><a href="{root}about.html">About</a></li>
            <li><a href="{root}contact.html">Contact</a></li>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© {YEAR} Contour Expeditions • All rights reserved</span>
        <span class="scale-bar" aria-hidden="true"><span class="bar"><i></i><i></i><i></i><i></i></span> 0 — 10 KM · N ↑</span>
      </div>
    </div>
  </footer>'''

def page(path, title, desc, active, body, head_extra="", scripts_extra="", root=None, og_image=DEFAULT_OG, ld=None, index=True):
    depth = path.count("/")
    root = root if root is not None else "../" * depth
    full_title = f"{title} | Contour Expeditions" if title else "Contour Expeditions | Guided & Self-Guided Adventure Travel"
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(full_title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta property="og:title" content="{e(full_title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Contour Expeditions">
  <meta property="og:url" content="{abs_url(path)}">
  <meta property="og:image" content="{SITE_URL + og_image}">
  <meta property="og:image:alt" content="{e(full_title)}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="{abs_url(path)}">{"" if index else chr(10) + '  <meta name="robots" content="noindex">'}{jsonld(ld) if ld else ""}
  <meta name="robots" content="max-image-preview:large">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" href="/assets/img/favicon-96.png" type="image/png" sizes="96x96">
  <link rel="icon" href="/assets/img/favicon-192.png" type="image/png" sizes="192x192">
  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Oswald:wght@400;500;600&amp;display=swap">{head_extra}
  <link rel="stylesheet" href="{root}assets/css/styles.css?v={VER}">
</head>
<body data-root="{root}">
  {nav(root, active)}

  <main id="main">
{body}
  </main>

  {footer(root)}
{scripts_extra}
  <script src="{root}assets/js/main.js?v={VER}"></script>
</body>
</html>
'''
    doc = clean_links(doc)
    if index:
        SITEMAP.append(path)
    out = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(out) or SITE, exist_ok=True)
    with open(out, "w") as f:
        f.write(doc)

# ------------------------------------------------------------------- components
def difficulty(n):
    rings = "".join(f'<circle cx="{6 + i*13}" cy="9" r="5" fill="{"#c8553d" if i < n else "none"}" stroke="{"#c8553d" if i < n else "#b9c0c6"}" stroke-width="1.5"/>' for i in range(5))
    names = {1: "Easy", 2: "Moderate", 3: "Moderate–Challenging", 4: "Challenging", 5: "Strenuous"}
    return f'<span class="difficulty"><svg viewBox="0 0 64 18" role="img" aria-label="Difficulty {n} of 5">{rings}</svg>{names[n]}</span>'

def badge(t):
    return f'<span class="badge badge-{t["type"]}">{"Guided" if t["type"] == "guided" else "Self-guided"}</span>'

def trip_card(t, root):
    return f'''<a class="trip-card" href="{root}trips/{t["slug"]}.html">
            <div class="media"><img src="{img(t, root, "thumb")}" alt="{e(t["name"])}" loading="lazy">{badge(t)}</div>
            <div class="body">
              <span class="coords">{t["coords"]} · {t["max_elev"]}</span>
              <h3>{e(t["name"])}</h3>
              <p>{e(t["card"])}</p>
              <div class="facts"><span>{t["duration"]}</span><span>Difficulty {t["difficulty"]}/5</span></div>
              <div class="price"><strong>From {t["price"]}</strong><span>View trip →</span></div>
            </div>
          </a>'''

def cta(title_html, text, btn_href, btn_label):
    return f'''    <section class="section cta-band">
      <div class="container">
        <h2>{title_html}</h2>
        <p>{e(text)}</p>
        <a class="btn" href="{btn_href}">{btn_label} →</a>
      </div>
    </section>'''

# ------------------------------------------------------------------- pages
def photo(t, root, key, size="sm"):
    name = t["slug"] + (f"-{key}" if key else "")
    if not key:
        return f"{root}assets/img/photos/{t['image']}"
    return f"{root}assets/img/photos/{name}{'-sm' if size == 'sm' else ''}.jpg"


def side_photo(t, root, section):
    key, alt = t["photos"][section]
    return f'<figure class="side-photo"><img src="{photo(t, root, key)}" alt="{e(alt)}" loading="lazy"></figure>'


def gallery(t, root):
    items = "\n".join(f'''          <button class="gallery-item" type="button" data-full="{photo(t, root, k, "full")}" aria-label="View larger: {e(alt)}">
            <img src="{photo(t, root, k) if k else photo(t, root, "", "full")}" alt="{e(alt)}" loading="lazy">
          </button>''' for k, alt in t["gallery"])
    return f'''    <section class="section" id="gallery" aria-labelledby="gallery-h">
      <div class="container">
        <div class="section-head"><span class="label">From the Trail</span><h2 id="gallery-h">Photo <em>Gallery</em></h2></div>
        <div class="gallery">
{items}
        </div>
      </div>
    </section>

'''


def cal_body():
    return '''
          <p class="hut-cal-summary" aria-live="polite">Loading hut availability…</p>
          <div class="hut-cal-nav">
            <button type="button" class="hut-cal-prev" aria-label="Previous month">‹</button>
            <span class="hut-cal-month"></span>
            <button type="button" class="hut-cal-next" aria-label="Next month">›</button>
          </div>
          <div class="hut-cal-grid"></div>
          <ul class="hut-cal-legend">
            <li><i class="available"></i>Available</li>
            <li><i class="full"></i>Fully booked</li>
            <li><i class="closed"></i>Closed</li>
          </ul>'''


def hut_calendar(t):
    """Browsable availability calendar for a trip page."""
    av = t["availability"]
    sizes = "".join(f'<option value="{n}"{" selected" if n == 2 else ""}>{n} {"person" if n == 1 else "people"}</option>' for n in range(1, 9))
    return f'''
        <div class="hut-cal" data-src="{av["data"]}" data-trip="{t["slug"]}" data-nights="{av["nights"]}">
          <div class="hut-cal-head">
            <h3>Check Hut <em>Availability</em></h3><label class="hut-cal-size">Group size <select>{sizes}</select></label>
          </div>
          <p class="hut-cal-note">The huts on this route are open from <strong>June through September</strong>. A start date is available when each hut has beds for your group on consecutive nights.</p>{cal_body()}
          <div class="hut-cal-detail" aria-live="polite"></div>
          <noscript><p>Turn on JavaScript to see hut availability.</p></noscript>
        </div>'''


def date_fields(t):
    """Start/end date fields for the reservation form, with a pop-up availability calendar."""
    av = t["availability"]
    days = av["nights"] + 1
    return f'''
            <div class="date-fields" data-trip="{t["slug"]}" data-trip-short="{e(av["short"])}" hidden>
              <div class="form-row">
                <div class="field"><label for="f-start-{t["slug"]}">Start date</label>
                  <input class="date-input" id="f-start-{t["slug"]}" name="start date" placeholder="Select start date" readonly aria-haspopup="dialog"></div>
                <div class="field"><label for="f-end-{t["slug"]}">End date</label>
                  <input class="date-input" id="f-end-{t["slug"]}" name="end date" placeholder="Select end date" readonly aria-haspopup="dialog"></div>
              </div>
              <p class="date-fields-note">Huts are open June through September. This trip is {days} days / {av["nights"]} nights, so the end date is set from your start date.</p>
              <dialog class="date-dialog" aria-labelledby="dd-title-{t["slug"]}">
                <div class="hut-cal hut-cal-picker" data-src="{av["data"]}" data-trip="{t["slug"]}" data-nights="{av["nights"]}">
                  <div class="hut-cal-head">
                    <h3 id="dd-title-{t["slug"]}">Available <em>Dates</em></h3>
                    <button type="button" class="date-dialog-close" aria-label="Close">×</button>
                  </div>{cal_body()}
                  <p class="hut-cal-selection" aria-live="polite">Choose an available start date.</p>
                  <div class="date-dialog-actions">
                    <button type="button" class="btn btn-outline btn-small date-cancel">Cancel</button>
                    <button type="button" class="btn btn-small date-apply" disabled>Select Dates</button>
                  </div>
                </div>
              </dialog>
            </div>'''


def build_trip(t):
    root = "../"
    photos = t.get("photos", {})
    guided = t["type"] == "guided"
    itin = "\n".join(f'''          <details>
            <summary><span class="day">Day {i}</span><span class="title">{e(title)}</span>{f'<span class="meta">{e(meta)}</span>' if meta else ""}</summary>
            <div class="content"><p>{e(text)}</p></div>
          </details>''' for i, (title, meta, text) in enumerate(t["itinerary"], 1))
    inc = "".join(f"<li>{e(x)}</li>" for x in t["included"])
    exc = "".join(f"<li>{e(x)}</li>" for x in t["excluded"])
    why = "".join(f'<div class="item"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in t["why"])
    status_label = {"available": "Available", "limited": "Limited", "waitlist": "Waitlist"}
    rows = "".join(f'''
              <tr>
                <td>{e(d)}</td>
                <td>{e(p)}</td>
                <td><span class="status status-{s}">{status_label[s]}</span></td>
                <td><a class="btn btn-small {"btn-outline" if s == "waitlist" else ""}" href="#" data-todo="booking-link" data-trip="{t["slug"]}">{"Waitlist" if s == "waitlist" else "Reserve"} →</a></td>
              </tr>''' for d, p, s in t["dates"])
    faqs = [
        ("How fit do I need to be?", t["fitness"]),
        ("Can I join solo?" if guided else "Can I do this trip solo?",
         "Absolutely — most of our guests travel solo. We pair solo travellers into shared rooms or tents, or you can add a single supplement." if guided
         else "Yes, though we recommend at least two people for safety and cost. Solo travellers pay a single supplement for accommodation, and we schedule an extra check-in call each day."),
        ("What's included in the trip?", "See the full list under What's Included above. In short: " + "; ".join(x[0].lower() + x[1:] for x in t["included"][:3]) + ". Flights and travel insurance are not included."),
    ]
    if not guided:
        faqs.append(("What support do I get on the trip?", "You'll have a pre-trip video briefing, GPX tracks and route notes, and a 24/7 support line that connects to our team. We can rebook accommodation, arrange transfers, or coordinate with local rescue services if anything changes."))
    faqs += [
        ("What happens after I book?", "You'll receive a welcome pack with packing list, travel logistics, and recommended training within 48 hours, followed by a planning call with your trip lead about 8 weeks before departure."),
        ("What's your cancellation policy?", "Deposits are refundable up to 90 days before departure. Within 90 days, payments can be transferred to a future trip. Full terms are provided when you book."),
    ]
    faq_html = "\n".join(f'''          <details>
            <summary><span class="title">{e(q)}</span></summary>
            <div class="content"><p>{e(a)}</p></div>
          </details>''' for q, a in faqs)
    route_json = e(json.dumps(t["route"], ensure_ascii=False))
    kind = "Guided Expedition" if guided else "Self-Guided Adventure"
    body = f'''    <section class="hero">
      <img src="{img(t, root)}" alt="{e(t.get("alt", t["name"] + " landscape"))}">
      <div class="container">
        <span class="label">{kind}</span>
        <h1>{e(t["name"])}</h1>
        <p class="subtitle">{e(t["subtitle"])}</p>
        <div class="hero-meta coords"><span>{t["coords"]}</span><span>Max elev. {t["max_elev"]}</span><span>{t["duration"]}</span></div>
        <div class="hero-actions">
          <a class="btn" href="#dates-prices">Dates &amp; Prices</a>
          <a class="btn btn-light" href="#itinerary">View Itinerary</a>
        </div>
      </div>
    </section>

    <section class="section section-panel">
      <div class="container{" media-split" if "overview" in photos else ""}">
        <div>
          <span class="label">Overview</span>
          <p class="overview">{e(t["overview"])}</p>
        </div>{side_photo(t, root, "overview") if "overview" in photos else ""}
      </div>
    </section>

    <hr class="route-divider">

    <section class="section" aria-labelledby="glance-h">
      <div class="container">
        <h2 id="glance-h">At a <em>Glance</em></h2>
        <div class="glance">
          <div class="legend">
            <dl>
              <div><dt>Trip Style</dt><dd>{badge(t)}</dd></div>
              <div><dt>Duration</dt><dd>{t["duration"]}</dd></div>
              <div><dt>Group Size</dt><dd>{e(t["group"])}</dd></div>
              <div><dt>Difficulty</dt><dd>{difficulty(t["difficulty"])}</dd></div>
              <div><dt>Max Elevation</dt><dd>{t["max_elev"]}</dd></div>
              <div><dt>Start / End</dt><dd>{e(t["start_end"])}</dd></div>
              <div><dt>Accommodation</dt><dd>{e(t["accommodation"])}</dd></div>
              <div><dt>Activities</dt><dd>{e(t["activities"])}</dd></div>
            </dl>
          </div>
          <aside class="price-box">
            <!-- TODO: confirm pricing -->
            <div class="from">From <span class="todo">Sample</span></div>
            <div class="amount">{t["price"]} <small style="font-size:.4em">USD</small></div>
            <div class="terms">{t["deposit"]} deposit • Flexible payments{" • per person" if not guided else ""}</div>
            <a class="btn" href="#dates-prices">Dates &amp; Prices</a>
            <a class="btn btn-light" href="{root}contact.html?trip={t["slug"]}#contact-form">Ask a Question</a>
          </aside>
        </div>
      </div>
    </section>

    <section class="section section-panel" aria-labelledby="map-h">
      <div class="container">
        <span class="label">The Route</span>
        <h2 id="map-h">Route <em>Map</em></h2>
        <div class="route-map" data-route="{route_json}" role="img" aria-label="Map of the {e(t["name"])} route"></div>
        <p class="map-note">Route shown is approximate and for illustration only.<!-- TODO: replace waypoints with the real route or a GPX trace --></p>
      </div>
    </section>

    <section class="section" id="itinerary" aria-labelledby="itin-h">
      <div class="container">
        <span class="label">Day by Day</span>
        <h2 id="itin-h">Trip <em>Itinerary</em></h2>
        <div class="{"media-split media-split-wide" if "itinerary" in photos else ""}">
        <div class="accordion itinerary">
{itin}
        </div>{side_photo(t, root, "itinerary") if "itinerary" in photos else ""}
        </div>
      </div>
    </section>

    <section class="section section-panel" aria-labelledby="inc-h">
      <div class="container">
        <h2 id="inc-h">What's <em>Included</em></h2>
        <div class="{"media-split media-split-reverse" if "included" in photos else ""}">{side_photo(t, root, "included") if "included" in photos else ""}
        <div class="grid grid-2">
          <div><h3>Included</h3><ul class="checklist">{inc}</ul></div>
          <div><h3>Not Included</h3><ul class="checklist excluded">{exc}</ul></div>
        </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="why-h">
      <div class="container">
        <span class="label">Why Go</span>
        <h2 id="why-h">Why You'll Love <em>This Trip</em></h2>
        <div class="grid grid-3 numbered">{why}</div>
      </div>
    </section>

    <section class="section section-wash" id="dates-prices" aria-labelledby="dates-h">
      <div class="container">
        <h2 id="dates-h">Dates &amp; <em>Prices</em>{"" if t.get("price_confirmed") else ' <span class="todo">Sample dates</span>'}</h2>
        <!-- TODO: replace sample dates/prices; paste booking URLs into the Reserve/Waitlist href="#" links -->
        <div class="{"dates-layout" if t.get("availability") else ""}">
        <div>
        <div class="table-wrap">
          <table class="dates-table">
            <thead><tr><th scope="col">Dates</th><th scope="col">Price</th><th scope="col">Availability</th><th scope="col"><span class="visually-hidden">Book</span></th></tr></thead>
            <tbody>{rows}
            </tbody>
          </table>
        </div>
        <div class="dates-foot">
          <span>From <strong>{t["price"]} USD</strong> · {t["deposit"]} deposit • Flexible payments</span>
          <a class="text-link" href="{root}contact.html?trip={t["slug"]}#contact-form">Not ready to book? Ask a question →</a>
        </div>
        </div>{hut_calendar(t) if t.get("availability") else ""}
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="faq-h">
      <div class="container narrow">
        <h2 id="faq-h">Common <em>Questions</em></h2>
        <div class="accordion">
{faq_html}
        </div>
      </div>
    </section>

{gallery(t, root) if t.get("gallery") else ""}{cta("Ready for Your Next <em>Expedition</em>?", "Spots are limited — reserve yours or reach out with questions.", "#dates-prices", "Reserve My Spot")}'''
    leaflet_css = '\n  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">'
    leaflet_js = '  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>'
    url = abs_url(f"trips/{t['slug']}.html")
    seen, stops = set(), []
    for lat, lng, label in t["route"]:
        if label not in seen:
            seen.add(label); stops.append(label)
    ld = {
        "@context": "https://schema.org",
        "@type": "TouristTrip",
        "name": f"{t['name']}: {t['subtitle']}" if ":" not in t["name"] else t["name"],
        "description": t["overview"],
        "url": url,
        "touristType": [a.strip() for a in t["activities"].split("•")],
        "itinerary": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i, "item": {"@type": "Place", "name": n}} for i, n in enumerate(stops, 1)]},
        "provider": PROVIDER,
    }
    ld["image"] = SITE_URL + ("assets/img/photos/" + t["image"] if t.get("image") else DEFAULT_OG)
    if t.get("price_confirmed"):
        ld["offers"] = {"@type": "Offer", "price": t["price"].strip("$").replace(",", ""), "priceCurrency": "USD",
                        "availability": "https://schema.org/InStock", "url": url}
    title = f"{t['name']} – {t['subtitle']}" if ":" in t["name"] else f"{t['name']}: {t['subtitle']}"
    og = "assets/img/photos/" + t["image"] if t.get("image") else DEFAULT_OG
    page(f"trips/{t['slug']}.html", title, t["card"], t["type"], body, leaflet_css, leaflet_js, og_image=og, ld=ld)


def build_home():
    root = ""
    featured = "".join(trip_card(t, root) for t in TRIPS)
    body = f'''    <section class="hero">
      <img style="object-position: 50% 15%" src="assets/img/photos/home-hero.jpg?v=2" alt="Frosted scree slopes below a sheer, snow-capped Andean peak" fetchpriority="high">
      <div class="container">
        <span class="label">Contour Expeditions</span>
        <p class="hero-title">Follow the <em>Lines</em></p>
        <h1 class="subtitle">Guided &amp; self-guided adventure trips in Peru, Ecuador, the Alps &amp; beyond</h1>
        <div class="hero-actions">
          <a class="btn" href="#ways">Explore Expeditions →</a>
          <a class="btn btn-light" href="customize.html">Plan a Custom Trip</a>
        </div>
      </div>
    </section>

    <section class="section" id="ways" aria-labelledby="ways-h">
      <div class="container">
        <div class="section-head center">
          <span class="label">Choose Your Route</span>
          <h2 id="ways-h">Three Ways to <em>Explore</em></h2>
          <p class="lead">Travel with our guides, go it alone with our planning behind you, or design an expedition from a blank map.</p>
        </div>
        <div class="grid grid-3">
          <a class="path-card" href="guided-trips.html">
            <img style="object-position: 60% 50%" src="assets/img/photos/home-guided.jpg" alt="View from a tent door across a trekking camp to snowy Andean peaks" loading="lazy">
            <span class="num">01 · GUIDED</span>
            <h3>Guided Expeditions</h3>
            <p>Small groups led by certified mountain guides. Permits, logistics, and safety handled.</p>
            <span class="text-link">View guided trips →</span>
          </a>
          <a class="path-card" href="unguided-trips.html">
            <img src="assets/img/photos/home-unguided.jpg" alt="Two hikers resting on an alpine meadow facing Dolomite peaks" loading="lazy">
            <span class="num">02 · UNGUIDED</span>
            <h3>Unguided Adventures</h3>
            <p>Our tested routes, bookings, and GPX tracks, with 24/7 support. You set the pace.</p>
            <span class="text-link">View unguided trips →</span>
          </a>
          <a class="path-card" href="customize.html">
            <img style="object-position: 45% 40%" src="assets/img/photos/home-customize-peak.jpg" alt="Fluted ice face of a glaciated Andean summit under breaking cloud" loading="lazy">
            <span class="num">03 · CUSTOM</span>
            <h3>Customize Your Own Adventure</h3>
            <p>Have a line on the map in mind? We'll help plan it and connect you with guides worldwide.</p>
            <span class="text-link">Start planning →</span>
          </a>
        </div>
      </div>
    </section>

    <hr class="route-divider">

    <section class="section section-panel" aria-labelledby="feat-h">
      <div class="container">
        <div class="section-head">
          <span class="label">Upcoming Expeditions</span>
          <h2 id="feat-h">Signature <em>Routes</em></h2>
        </div>
        <div class="grid grid-4">
          {featured}
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="approach-h">
      <div class="container">
        <div class="section-head">
          <span class="label">Our Approach</span>
          <h2 id="approach-h">Less Logistics. <em>More Altitude.</em></h2>
        </div>
        <div class="grid grid-3 numbered">
          <div class="item"><h3>Routes We Know</h3><p>Every trip is scouted and refined on the ground, with local partners who live in the mountains we visit.</p></div>
          <div class="item"><h3>Safety Built In</h3><p>Certified guides, acclimatization schedules, satellite communication, and a 24/7 support line on every trip.</p></div>
          <div class="item"><h3>Small Footprint</h3><p>Small groups, locally owned lodging, and fair wages for the arrieros, guides, and hosts who make it possible.</p></div>
        </div>
      </div>
    </section>

    <section class="section section-wash">
      <div class="container">
        <div class="testimonial">
          <!-- TODO: replace with a real guest testimonial -->
          <span class="label">Field Notes</span>
          <blockquote>“Every detail was handled, so all we had to think about was the next pass. The Huayhuash ruined every other trek for me — in the best way.”</blockquote>
          <cite>— Guest name, Huayhuash 2026 <span class="todo">Placeholder</span></cite>
          <div class="stats">
            <div><strong>{len(TRIPS)}</strong><span>Signature Routes</span></div>
            <div><strong>7</strong><span>Countries</span></div>
            <div><strong>6,263 m</strong><span>Highest Summit</span></div>
          </div>
        </div>
      </div>
    </section>

{cta("Ready to Go Somewhere <em>Wild</em>?", "Pick a route, or tell us where you've always wanted to go.", "guided-trips.html", "Explore Trips")}'''
    home_ld = {
        "@type": "TravelAgency",
        "@id": SITE_URL + "#organization",
        "name": "Contour Expeditions",
        "url": SITE_URL,
        "logo": SITE_URL + "assets/img/favicon-512.png",
        "image": SITE_URL + DEFAULT_OG,
        "email": EMAIL,
        "telephone": PHONE_TEL,
        "description": "Guided expeditions, self-guided adventures, and custom trips in Peru, Ecuador, the Alps, Morocco, and the Balkans.",
        "areaServed": ["Peru", "Ecuador", "Italy", "Switzerland", "Morocco", "Bosnia and Herzegovina", "Montenegro"],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "TouristTrip", "name": t["name"], "url": abs_url(f"trips/{t['slug']}.html")}} for t in TRIPS],
    }
    home_ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": SITE_URL + "#website", "name": "Contour Expeditions", "alternateName": "contour-expeditions.com",
         "url": SITE_URL, "publisher": {"@id": SITE_URL + "#organization"}},
        home_ld]}
    page("index.html", "", "Contour Expeditions: guided expeditions, self-guided adventures, and custom trips in Peru, Ecuador, the Dolomites, Morocco, and the Balkans.", "home", body, ld=home_ld)


def build_listing(kind):
    trips = GUIDED if kind == "guided" else UNGUIDED
    if kind == "guided":
        title, h1, intro = "Guided Trips", "Guided <em>Trips</em>", "Join a small group led by certified mountain guides and local experts. We handle permits, lodging, meals, transport, and safety, so you can focus on the mountains."
        points = [("Certified Guides", "IFMGA / UIAGM and nationally certified mountain guides lead every technical day."),
                  ("Small Groups", "Never more than 10 guests, and tighter ratios on summit days."),
                  ("All-Inclusive Logistics", "From the airport to the high camp, everything is arranged for you.")]
        other = ("unguided-trips.html", "Prefer to go independently? See our unguided trips →")
    else:
        title, h1, intro = "Unguided Trips", "Unguided <em>Trips</em>", "Our self-guided adventures give you the freedom to travel at your own pace, with all the hard planning done. We book accommodation, provide tested GPX routes and notes, and stay on call 24/7 while you're out there."
        points = [("Tested Routes", "Every route has been travelled and refined by our team, with GPX tracks and detailed daily notes."),
                  ("Bookings Handled", "Huts, guesthouses, rentals, and transfers are booked before you leave home."),
                  ("24/7 Support", "A real person on the end of the line if plans change or something goes wrong.")]
        other = ("guided-trips.html", "Want a guide by your side? See our guided trips →")
    cards = "".join(trip_card(t, "") for t in trips)
    pts = "".join(f'<div class="item"><h3>{h}</h3><p>{p}</p></div>' for h, p in points)
    body = f'''    <section class="hero hero-small">
      <img src="assets/img/placeholders/{kind}.svg" alt="">
      <div class="container">
        <span class="label">{"Expeditions" if kind == "guided" else "Self-Guided"}</span>
        <h1>{h1}</h1>
        <p class="subtitle">{"Expert-led. Small groups. Big mountains." if kind == "guided" else "Your pace. Our planning."}</p>
      </div>
    </section>

    <section class="section section-panel">
      <div class="container">
        <div class="section-head"><p class="lead">{intro}</p></div>
        <div class="grid {"grid-4" if len(trips) == 4 else "grid-3"}">
          {cards}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head"><span class="label">How It Works</span><h2>What to <em>Expect</em></h2></div>
        <div class="grid grid-3 numbered">{pts}</div>
        <p style="margin-top:2rem"><a class="text-link" href="{other[0]}">{other[1]}</a></p>
      </div>
    </section>

{cta("Don't See Your <em>Route</em>?", "We'll help you design a custom expedition anywhere in the world.", "customize.html", "Customize Your Adventure")}'''
    page(f"{kind}-trips.html", title, intro, kind, body)


def form_open(fid, subject, done_title, done_text):
    return f'''<form class="form" id="{fid}" action="https://formsubmit.co/{FORM_TO}" method="POST" data-formsubmit data-email="{SUPPORT_EMAIL}" data-done-title="{done_title}" data-done-text="{done_text}">
          <input type="hidden" name="_subject" value="{subject}">
          <input type="hidden" name="_template" value="table">
          <label class="hp" aria-hidden="true">Leave blank <input type="text" name="_honey" tabindex="-1" autocomplete="off"></label>'''


def build_customize():
    body = f'''    <section class="hero hero-small">
      <img src="assets/img/placeholders/customize.svg" alt="">
      <div class="container">
        <span class="label">Custom Expeditions</span>
        <h1>Customize Your <em>Adventure</em></h1>
        <p class="subtitle">Bring the idea. We'll help you draw the map.</p>
        <div class="hero-actions"><a class="btn" href="#custom-form">Start Planning →</a></div>
      </div>
    </section>

    <section class="section section-panel">
      <div class="container split">
        <div>
          <span class="label">Built Around You</span>
          <h2>Your Expedition, <em>Your Way</em></h2>
          <p class="lead">Dreaming of a ski traverse in Georgia's Caucasus, a first 6,000-metre peak in Bolivia, or a packrafting route through Patagonia? We help independent adventurers, clubs, and private groups plan expeditions anywhere in the world.</p>
          <p>We'll work with you on route planning, timing, permits, and logistics, then connect you with vetted international guiding organizations and local outfitters where you want them. You can have us plan every detail, or just the parts you'd rather not untangle yourself.</p>
        </div>
        <img src="assets/img/placeholders/about.svg" alt="Map spread out with route planning notes">
      </div>
    </section>

    <section class="section" aria-labelledby="how-h">
      <div class="container">
        <div class="section-head center"><span class="label">The Process</span><h2 id="how-h">How It <em>Works</em></h2></div>
        <ol class="steps">
          <li><span class="pin">1</span><div><h3>Tell Us Your Idea</h3><p>Share where, when, and what kind of adventure using the form below.</p></div></li>
          <li><span class="pin">2</span><div><h3>Planning Call</h3><p>A free 30-minute call to discuss goals, experience, and budget.</p></div></li>
          <li><span class="pin">3</span><div><h3>Route &amp; Guide Matching</h3><p>We draft an itinerary and introduce you to trusted guides and outfitters.</p></div></li>
          <li><span class="pin">4</span><div><h3>You Go</h3><p>Bookings confirmed, GPX and notes delivered, and 24/7 support while you're out.</p></div></li>
        </ol>
      </div>
    </section>

    <section class="section section-panel" aria-labelledby="svc-h">
      <div class="container">
        <div class="section-head"><span class="label">Services</span><h2 id="svc-h">How We Can <em>Help</em></h2></div>
        <div class="grid grid-4 numbered">
          <div class="item"><h3>Route Planning</h3><p>Objectives, daily stages, acclimatization, and bail-out options mapped in detail.</p></div>
          <div class="item"><h3>Guide Connections</h3><p>Introductions to certified guiding organizations and outfitters we trust around the world.</p></div>
          <div class="item"><h3>Permits &amp; Logistics</h3><p>Permits, park fees, transfers, accommodation, and gear rental, sorted.</p></div>
          <div class="item"><h3>On-Trip Support</h3><p>Weather and conditions briefings plus a 24/7 support line while you travel.</p></div>
        </div>
      </div>
    </section>

    <section class="section" id="custom-form" aria-labelledby="form-h">
      <div class="container narrow">
        <div class="section-head"><span class="label">Get Started</span><h2 id="form-h">Tell Us About Your <em>Expedition</em></h2>
          <p>We reply to every enquiry within two business days.</p></div>
        {form_open("custom-expedition-form", "Custom expedition enquiry", "Enquiry received", "Thanks for sharing your idea. We've received your custom expedition enquiry and will be in touch shortly, within two business days, to set up a planning call.")}
          <div class="form-row">
            <div class="field"><label for="c-name">Name <span class="req">*</span></label><input id="c-name" name="name" required autocomplete="name"></div>
            <div class="field"><label for="c-email">Email <span class="req">*</span></label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
          </div>
          <div class="field"><label for="c-dest">Destination or region <span class="req">*</span></label><input id="c-dest" name="destination" required placeholder="e.g. Cordillera Real, Bolivia"></div>
          <fieldset class="field">
            <legend>Activities</legend>
            <div class="checks">
              {"".join(f'<label><input type="checkbox" name="activities" value="{a}"> {a}</label>' for a in ["Trekking", "Mountaineering", "Ski touring", "Climbing", "Bikepacking", "Surf", "Paddling", "Other"])}
            </div>
          </fieldset>
          <div class="form-row">
            <div class="field"><label for="c-dates">Dates or season</label><input id="c-dates" name="dates" placeholder="e.g. July 2027, flexible"></div>
            <div class="field"><label for="c-size">Group size</label><input id="c-size" name="group size" type="number" min="1" max="50"></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="c-exp">Experience level</label>
              <select id="c-exp" name="experience"><option value="">Select…</option><option>New to this activity</option><option>Some experience</option><option>Experienced</option><option>Expert / professional</option></select></div>
            <div class="field"><label for="c-style">Guiding preference</label>
              <select id="c-style" name="guiding"><option value="">Select…</option><option>Fully guided</option><option>Guided on key days</option><option>Self-supported with planning help</option><option>Not sure yet</option></select></div>
          </div>
          <div class="field"><label for="c-budget">Budget per person (USD)</label>
            <select id="c-budget" name="budget"><option value="">Select…</option><option>Under $2,000</option><option>$2,000 – $4,000</option><option>$4,000 – $7,000</option><option>$7,000+</option></select></div>
          <div class="field"><label for="c-details">Tell us more <span class="req">*</span></label><textarea id="c-details" name="details" required placeholder="Your idea, objectives, any constraints…"></textarea></div>
          <div class="form-status" role="status" tabindex="-1" hidden></div>
          <div><button class="btn" type="submit">Send Enquiry →</button></div>
        </form>
      </div>
    </section>'''
    page("customize.html", "Customize Your Adventure", "Plan a custom expedition with Contour Expeditions: route planning, permits, logistics, and connections to international guiding organizations.", "customize", body)


def build_about():
    team = [("team-1", "Your Name", "Founder", "Placeholder bio: background, favourite mountains, and why you started Contour Expeditions."),
            ("team-2", "Team Member", "Expedition Lead", "Placeholder bio: certifications, expeditions led, and specialities."),
            ("team-3", "Team Member", "Trip Designer", "Placeholder bio: regions of expertise and the routes they've scouted.")]
    cards = "".join(f'<div class="team-card"><img src="assets/img/placeholders/{img}.svg" alt="Portrait of {n}" loading="lazy"><h3>{n}</h3><div class="role">{r}</div><p>{b}</p></div>' for img, n, r, b in team)
    body = f'''    <section class="hero hero-small">
      <img src="assets/img/placeholders/about.svg" alt="">
      <div class="container">
        <span class="label">About</span>
        <h1>Read the <em>Terrain</em></h1>
        <p class="subtitle">Map people, mountain people.</p>
      </div>
    </section>

    <section class="section section-panel">
      <div class="container split">
        <div>
          <span class="label">Our Story</span> <span class="todo">Placeholder</span>
          <h2>Why <em>Contour</em></h2>
          <p class="lead">Contour lines show you the shape of the land before you ever set foot on it. That's how we approach every trip: understand the terrain, plan with care, then go and experience it fully.</p>
          <p>Contour Expeditions was founded by guides and lifelong adventurers who spent years planning trips for friends: high passes in the Andes, hut-to-hut routes in the Alps, and bikepacking loops through the Balkans. Today we lead small guided expeditions, design self-guided adventures with full support, and help travellers build their own expeditions with trusted partners around the world.</p>
        </div>
        <img src="assets/img/placeholders/home-hero.svg" alt="Team on a mountain ridge" loading="lazy">
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head"><span class="label">Values</span><h2>What We <em>Stand For</em></h2></div>
        <div class="grid grid-3 numbered">
          <div class="item"><h3>Safety First</h3><p>Certified guides, conservative decisions, proper acclimatization, and emergency plans on every trip.</p></div>
          <div class="item"><h3>Local Partners</h3><p>We work with local guides, arrieros, hut keepers, and hosts, and pay fairly.</p></div>
          <div class="item"><h3>Low Impact</h3><p>Small groups, Leave No Trace practices, and locally owned lodging wherever possible.</p></div>
        </div>
      </div>
    </section>

    <section class="section section-panel">
      <div class="container">
        <div class="section-head"><span class="label">The Team</span> <span class="todo">Placeholder</span><h2>Who You'll <em>Travel With</em></h2></div>
        <div class="grid grid-3">{cards}</div>
      </div>
    </section>

{cta("Let's Plan Something <em>Big</em>", "Join a guided expedition, head out on your own, or build something new.", "contact.html", "Get in Touch")}'''
    page("about.html", "About", "About Contour Expeditions: guides and planners for adventure travel in the mountains and beyond.", "about", body)


def build_contact(kind="contact"):
    """kind="contact": Get in Touch (questions). kind="reserve": Book Your Adventure (reservations)."""
    booking = kind == "reserve"
    opts = "".join(f'<option value="{t["slug"]}">{e(t["name"])} ({"Guided" if t["type"] == "guided" else "Unguided"})</option>' for t in TRIPS)
    groups = "".join(f'<option value="{n}"{" selected" if n == 2 else ""}>{n} {"person" if n == 1 else "people"}</option>' for n in range(1, 9))
    if booking:
        intro = ("Reservations", "Book Your <em>Adventure</em>",
                 "Tell us which trip you'd like to book, how many people are coming, and your preferred dates. "
                 "We'll confirm availability and send your booking and payment details within two business days.")
        trip_field = f'''<div class="field"><label for="trip-interest">Trip <span class="req">*</span></label>
              <select id="trip-interest" name="trip" required><option value="">Select a trip</option>{opts}</select></div>
            <div class="field"><label for="f-group">Group size</label>
              <select id="f-group" name="group size">{groups}<option value="9+">9 or more</option></select></div>
            {"".join(date_fields(t) for t in TRIPS if t.get("availability"))}'''
        form_id, subject, submit = "booking-form", "Reservation request", "Request Reservation →"
        done = ("Reservation request received", "We've received your reservation request and will confirm the details shortly, within two business days.")
        side = f'''<h2>How Booking <em>Works</em></h2>
          <ol class="steps steps-compact">
            <li><span class="pin">1</span><div><h3>Send Your Request</h3><p>Choose your trip, group size, and dates.</p></div></li>
            <li><span class="pin">2</span><div><h3>We Confirm</h3><p>We check availability and reply within two business days.</p></div></li>
            <li><span class="pin">3</span><div><h3>Secure Your Spot</h3><p>Pay the deposit to lock in your dates.</p></div></li>
          </ol>
          <p>Have a question first? <a class="text-link" href="contact.html">Get in touch →</a></p>'''
    else:
        intro = ("Contact", "Get in <em>Touch</em>",
                 "Questions about a trip, a custom expedition, or anything else? Send us a message and we'll get back to you within two business days.")
        trip_field = f'''<div class="field"><label for="trip-interest">Trip of interest</label>
              <select id="trip-interest" name="trip"><option value="">General enquiry</option>{opts}<option value="custom">Custom expedition</option></select></div>'''
        form_id, subject, submit = "contact-form", "Website enquiry", "Send Message →"
        done = ("Message received", "Thanks for reaching out. We've received your message and will get back to you shortly, within two business days.")
        side = f'''<h2>Reach <em>Us</em></h2>
          <ul class="contact-list">
            <li><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><strong>Phone / WhatsApp</strong><span><a href="tel:{PHONE_TEL}">{PHONE}</a> · <a href="https://wa.me/{PHONE_TEL[1:]}">WhatsApp</a></span></li>
            <li><strong>Based in</strong><span>City, State <span class="todo">Placeholder</span></span></li>
            <li><strong>Response time</strong><span>Within two business days</span></li>
          </ul>
          <p>Ready to book? <a class="text-link" href="reserve.html">Book your adventure →</a></p>
          <p>Planning something bigger? See <a class="text-link" href="customize.html">Customize Your Adventure →</a></p>'''
    body = f'''    <section class="page-intro">
      <div class="container">
        <span class="label">{intro[0]}</span>
        <h1>{intro[1]}</h1>
        <p class="lead">{intro[2]}</p>
      </div>
    </section>

    <section class="section section-panel" style="padding-top:3rem">
      <div class="container split" style="align-items:start">
        <div id="{form_id}">
          {form_open(form_id + "-el", subject, *done)}
            <div class="form-row">
              <div class="field"><label for="f-name">Name <span class="req">*</span></label><input id="f-name" name="name" required autocomplete="name"></div>
              <div class="field"><label for="f-email">Email <span class="req">*</span></label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
            </div>
            {trip_field}
            <div class="field"><label for="f-msg">Message <span class="req">*</span></label><textarea id="f-msg" name="message" required></textarea></div>
            <div class="form-status" role="status" tabindex="-1" hidden></div>
            <div><button class="btn" type="submit">{submit}</button></div>
          </form>
        </div>
        <div>
          {side}
        </div>
      </div>
    </section>'''
    if booking:
        page("reserve.html", "Book Your Adventure", "Book a guided or self-guided trip with Contour Expeditions: choose your trip, group size, and dates.", "reserve", body)
    else:
        page("contact.html", "Contact", "Contact Contour Expeditions about guided trips, self-guided adventures, or a custom expedition.", "contact", body)


def build_404():
    body = '''    <section class="page-intro" style="min-height:50vh">
      <div class="container narrow">
        <span class="label">404 · Off Route</span>
        <h1>You've Wandered <em>Off the Map</em></h1>
        <p class="lead">The page you're looking for doesn't exist or has moved.</p>
        <a class="btn" href="/index.html">Back to Base Camp →</a>
      </div>
    </section>'''
    page("404.html", "Page Not Found", "Page not found.", "", body, root="/", index=False)


def build_favicon():
    with open(os.path.join(SITE, "assets/img/favicon.svg"), "w") as f:
        f.write(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"').replace("currentColor", "#1f2326") + "\n")


if __name__ == "__main__":
    os.makedirs(os.path.join(SITE, "assets/img/placeholders"), exist_ok=True)
    make_placeholders()
    for t in TRIPS:
        build_trip(t)
    SITEMAP.sort(key=lambda p: (p != "index.html", p.startswith("trips/"), p))
    build_home()
    build_listing("guided")
    build_listing("unguided")
    build_customize()
    build_about()
    build_contact()
    build_contact("reserve")
    build_404()
    import datetime
    today = datetime.date.today().isoformat()
    urls = "".join(f"  <url><loc>{abs_url(p)}</loc><lastmod>{today}</lastmod></url>\n" for p in sorted(SITEMAP, key=lambda p: (p != "index.html", p.startswith("trips/"), p)))
    with open(os.path.join(SITE, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    with open(os.path.join(SITE, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: " + SITE_URL + "sitemap.xml\n")
    print("built")
