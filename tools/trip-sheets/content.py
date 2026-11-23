"""Via Alpina trip sheet content. Rendered to .docx and to PDF from the same blocks."""
PLACEHOLDER = "[PLACEHOLDER]"
DOC = "/tmp/ce-doc"
COVER = "/Users/zheald/contour-expeditions/assets/img/photos/swiss-via-alpina.jpg"

GLANCE = [
    ("Trip style", "Self-guided hut-to-hut trek"),
    ("Duration", "4 days / 3 nights"),
    ("Start / finish", "Lauterbrunnen → Kandersteg (both by train from Interlaken)"),
    ("Distance", "Approx. 39 km (24 miles)"),
    ("Total ascent / descent", "Approx. 3,500 m up / 3,100 m down"),
    ("Highest point", "Blüemlisalphütte, 2,840 m (Hohtürli pass 2,778 m)"),
    ("Difficulty", "Challenging (4 of 5): marked mountain trails with steep sections, built steps and fixed cables"),
    ("Season", "The huts are open June through September; best conditions from early July"),
    ("Accommodation", "3 Swiss mountain huts in shared dormitories, half board (dinner and breakfast)"),
    ("Group size", "2–6 people recommended"),
]

OVERVIEW_ROWS = [
    ("1", "Lauterbrunnen → Mürren → Rotstockhütte", "13 km", "+1,500 / −250 m", "5–6 h\n(2.5–3 h using lifts)", "Rotstockhütte\n2,039 m"),
    ("2", "Rotstockhütte → Sefinenfurgge → Gspaltenhornhütte", "6.5 km", "+850 / −450 m", "4–5 h", "Gspaltenhornhütte\n2,455 m"),
    ("3", "Gspaltenhornhütte → Hohtürli → Blüemlisalphütte", "7.5 km", "+1,000 / −600 m", "5–6 h", "Blüemlisalphütte\n2,840 m"),
    ("4", "Blüemlisalphütte → Oeschinensee → Kandersteg", "12 km", "+150 / −1,800 m", "4–5 h\n(3 h using gondola)", "—"),
    ("", "Total", "Approx. 39 km", "+3,500 / −3,100 m", "", "3 nights"),
]

DAYS = [
  {
    "n": 1, "title": "Lauterbrunnen to Rotstockhütte",
    "stats": [("Distance", "13 km"), ("Ascent", "+1,500 m"), ("Descent", "−250 m"), ("Walking time", "5–6 h"), ("Overnight", "Rotstockhütte, 2,039 m")],
    "sections": [
      ("The route", [
        "Start at Lauterbrunnen station (797 m), at the foot of one of the deepest valleys in the Alps. The trail climbs steeply through forest on the west side of the valley, with waterfalls pouring off the cliffs opposite, to reach the car-free village of Mürren (1,639 m) after approx. 2.5–3 hours.",
        "From Mürren, the path continues on gentler alpine pasture tracks above Gimmelwald and past Spielbodenalp, with the Eiger, Mönch and Jungfrau filling the skyline behind you. A final climb brings you to the Rotstockhütte (2,039 m), tucked beneath the Schilthorn.",
      ]),
      ("Save your legs", ["To skip the steep first climb (approx. 850 m of ascent), take the cable car from Lauterbrunnen to Grütschalp and the mountain railway on to Mürren (approx. 25 minutes in total). From Mürren it is 2.5–3 hours to the hut."]),
      ("Terrain", ["Good, well-signed paths throughout. The forest climb to Mürren is steep but not exposed."]),
      ("Food and water", ["Lauterbrunnen and Mürren are your last shops and cash machines. Fill your water in Mürren; the farm restaurant at Spielbodenalp is a good lunch stop when open."]),
    ],
  },
  {
    "n": 2, "title": "Rotstockhütte to Gspaltenhornhütte",
    "stats": [("Distance", "6.5 km"), ("Ascent", "+850 m"), ("Descent", "−450 m"), ("Walking time", "4–5 h"), ("Overnight", "Gspaltenhornhütte, 2,455 m")],
    "sections": [
      ("The route", [
        "A short day in distance but a big one in scenery. From the hut, a marked mountain trail climbs steadily over pasture and then scree to the Sefinenfurgge (2,612 m), a narrow notch on the ridge with views back to the Jungfrau massif. The last section to the pass is steep, with built steps.",
        "Rather than dropping into the Kiental valley, the route traverses across the high slopes beneath the Gspaltenhorn to the Gspaltenhornhütte (2,455 m). Arrive early and enjoy an afternoon in one of the most dramatic hut settings on the trip, facing the Gspaltenhorn and its glaciers.",
      ]),
      ("Terrain", ["Steep, loose scree on both sides of the Sefinenfurgge. Trekking poles help. Snow can linger near the pass into July; we will tell you before departure whether microspikes are needed."]),
      ("Bail-out option", ["In poor weather, descend west from the Sefinenfurgge to Griesalp, where a PostBus runs down the valley to Reichenbach for trains to Interlaken or Kandersteg."]),
      ("Food and water", ["There is no reliable water between the huts. Carry 1.5–2 litres and a packed lunch (order it at the Rotstockhütte the evening before)."]),
    ],
  },
  {
    "n": 3, "title": "Gspaltenhornhütte to Blüemlisalphütte",
    "stats": [("Distance", "7.5 km"), ("Ascent", "+1,000 m"), ("Descent", "−600 m"), ("Walking time", "5–6 h"), ("Overnight", "Blüemlisalphütte, 2,840 m")],
    "sections": [
      ("The route", [
        "The crux of the trek. Descend approx. 500 m from the hut into the upper Gamchi valley and cross the glacial stream. From the valley floor (around 1,950 m), the trail climbs past the pastures of Bundalp and then up the long, relentless ascent to the Hohtürli (2,778 m), the highest pass on the Via Alpina.",
        "The upper part of the climb follows steep moraine with long staircases and fixed cables. From the pass it is a final ten minutes to the Blüemlisalphütte (2,840 m), perched on the ridge above the Blüemlisalp glacier. Sunset and sunrise here are unforgettable.",
      ]),
      ("Terrain", ["Steep, loose and exposed in places on the upper Hohtürli. Take your time, keep a hand on the cables where fitted, and avoid the climb in wet or icy conditions. Plan to be over the pass by early afternoon, before thunderstorms build."]),
      ("Food and water", ["Top up water in the Gamchi valley or at Bundalp (a seasonal mountain inn; check opening). Bring a packed lunch from the Gspaltenhornhütte."]),
      ("Tonight", ["The Blüemlisalphütte is high and can be cold even in summer. Have your warm jacket, hat and gloves ready."]),
    ],
  },
  {
    "n": 4, "title": "Blüemlisalphütte to Kandersteg via Oeschinensee",
    "stats": [("Distance", "12 km"), ("Ascent", "+150 m"), ("Descent", "−1,800 m"), ("Walking time", "4–5 h"), ("Finish", "Kandersteg, 1,176 m")],
    "sections": [
      ("The route", [
        "A long descent with a spectacular reward. Leave the hut on the west side of the Hohtürli and descend past the alp of Oberbärgli to the turquoise Oeschinensee (1,578 m), one of the most beautiful lakes in the Alps. Stop for a swim, a rowing boat or a long lunch at the lakeside restaurants.",
        "From the lake, either walk approx. 20 minutes to the top station of the Oeschinensee gondola and ride down to Kandersteg, or continue on foot (approx. 1–1.25 hours) to Kandersteg village and the station (1,176 m).",
      ]),
      ("Terrain", ["The descent to the lake is steep in places and long overall, so knees will feel it. Poles are strongly recommended."]),
      ("Finishing up", ["Trains leave Kandersteg at least hourly. See Getting There and Back for onward connections."]),
    ],
  },
]

GETTING = [
  ("Arriving in Switzerland", [
    "Fly into Zurich (ZRH) or Geneva (GVA). Both airports have train stations with direct or easy connections to the Bernese Oberland. Basel (BSL) also works.",
  ]),
  ("To the start: Lauterbrunnen", [
    "Take the train to Interlaken Ost (approx. 2 hours from Zurich Airport, approx. 3 hours from Geneva Airport, usually changing in Bern).",
    "From Interlaken Ost, the Berner Oberland Bahn runs to Lauterbrunnen in approx. 20 minutes, at least every 30–60 minutes.",
    "We recommend spending the night before in Lauterbrunnen, Wengen or Mürren so you can start fresh in the morning.",
  ]),
  ("From the finish: Kandersteg", [
    "Kandersteg is on the main Lötschberg line. Trains run at least hourly to Spiez (approx. 25 minutes), with connections to Interlaken Ost (approx. 20 minutes further), Bern (approx. 1 hour from Kandersteg) and Zurich Airport (approx. 2–2.5 hours).",
  ]),
  ("Luggage", [
    "Carry only what you need on the trail. Send the rest ahead from Interlaken Ost or Lauterbrunnen to Kandersteg using the Swiss railways' station-to-station luggage service (check current availability and cut-off times), or leave it at your Interlaken hotel and collect it on the way home.",
  ]),
  ("Tickets and passes", [
    "Buy tickets in the SBB Mobile app or at the station. If you are travelling for several days in Switzerland, a Swiss Travel Pass or Half Fare Card usually pays for itself and includes discounts on many mountain lifts.",
    "All times are approximate. Check current timetables before you travel.",
  ]),
]

PACKING = [
  ("Hut essentials", [
    "Sleeping bag liner (silk or cotton) — required in the huts; blankets and pillows are provided. If you'd rather not bring one, liners can be rented at each hut for €10 per night",
    "Earplugs and eye mask — the huts have shared dormitories, so expect snoring and early risers",
    "Headlamp",
    "Small quick-dry towel and minimal toiletries (most huts have no showers)",
    "Swiss francs in cash — not every hut takes cards",
    "Hut shoes — slippers aren't provided, so bring flip-flops, light slippers or a spare pair of shoes; boots stay at the entrance",
  ]),
  ("Clothing", [
    "Waterproof jacket with hood", "Waterproof overtrousers", "Insulated jacket (down or synthetic)", "Fleece or midlayer",
    "2 hiking tops (merino or synthetic)", "Hiking trousers or shorts, plus leggings", "Warm hat and sun hat", "Light gloves",
    "2–3 pairs of hiking socks", "Underwear", "Light change of clothes for evenings in the hut",
  ]),
  ("Footwear", [
    "Broken-in hiking boots with good grip (ankle support recommended)",
    "Gaiters (early season or after fresh snow)",
  ]),
  ("Gear", [
    "Backpack, 30–40 litres, with a rain cover or liner", "Trekking poles", "Microspikes (June to early July or after fresh snow — we'll advise)",
    "Water bottles or bladder, 2 litres total", "Sunglasses (category 3–4)", "Sunscreen (SPF 50) and lip balm",
    "Phone with offline maps and the GPX route loaded, plus a paper hiking map as backup",
  ]),
  ("Health and safety", [
    "First aid kit: blister care, painkillers, personal medication", "Emergency blanket and whistle", "Fully charged phone and a power bank",
    "Travel insurance details, including mountain rescue cover",
  ]),
  ("Food", [
    "Trail snacks for 4 days (bars, nuts, chocolate)",
    "Packed lunches can be ordered at each hut the evening before",
  ]),
  ("Documents and money", [
    "Passport or ID", "Booking confirmations (we'll send these)", "Train tickets or travel pass", "Credit card and Swiss francs",
  ]),
  ("Optional", [
    "Swimsuit for the Oeschinensee", "Light sandals for the lake", "Camera", "A book or cards for evenings in the hut",
  ]),
]

BEFORE = [
  ("Settle into the Lauterbrunnen valley", "Spend a night in Lauterbrunnen, Wengen or Mürren. Walk to Staubbach Falls in Lauterbrunnen village, and take the short bus ride to Trümmelbach Falls, where glacier meltwater thunders through caves inside the mountain."),
  ("Ride up the Schilthorn", "From Mürren, the cable car to the Schilthorn (Piz Gloria) gives a 360° panorama over the peaks you'll walk beneath on Day 1."),
  ("Visit the Jungfraujoch", "The 'Top of Europe' railway from Wengen and Kleine Scheidegg makes a spectacular (if pricey) day out. Book ahead in summer."),
  ("Train for it", "In the weeks before you travel, build up to back-to-back days of 5–6 hours' hiking with 1,000 m or more of ascent, carrying your loaded pack."),
]
AFTER = [
  ("Linger in Kandersteg", "Stay a night and return to the Oeschinensee by gondola without a pack: row across the lake, or ride the summer toboggan run at the top station."),
  ("Blausee", "A small, intensely blue lake in the forest a short bus ride down the valley from Kandersteg."),
  ("Bern", "Switzerland's capital is approx. 1 hour away by train. Wander the arcaded, UNESCO-listed old town and the view from the Rose Garden."),
  ("Lake Thun", "Take a boat from Spiez past the castles of Spiez, Oberhofen and Thun."),
  ("Soak tired legs", "The thermal baths of Leukerbad are approx. 1.5 hours away through the Lötschberg tunnel in the Valais."),
  ("Keep exploring", "Zermatt and the Matterhorn are approx. 2–2.5 hours from Kandersteg by train."),
  ("Eat like a local", "Rösti, Älplermagronen (alpine macaroni with potatoes and apple sauce), raclette and fondue — you've earned them."),
]

SAFETY = [
  ("Emergency numbers", "Rega air rescue 1414 · European emergency 112 · Ambulance 144 · Police 117. Contour Expeditions 24/7 support line: " + PLACEHOLDER + "."),
  ("Weather", "Check the MeteoSwiss forecast each morning. Summer thunderstorms often build in the afternoon, so start early and aim to be over each pass by early afternoon."),
  ("Snow", "Snow can linger on the Sefinenfurgge and Hohtürli into July. We check conditions before you depart and will tell you whether microspikes are needed."),
  ("Hut etiquette", "Arrive by approx. 5 pm. Boots off at the door; change into your own hut shoes (slippers aren't provided). Sleeping is in shared dormitories, so keep noise and headlamp use to a minimum after lights out. Dinner is usually served around 6–6:30 pm, quiet hours are 10 pm–6 am, and breakfast is early. Carry out all your rubbish, and let the warden know where you're heading next."),
  ("Trail markings", "The whole route follows white-red-white mountain trail markings. Stay on the marked path, especially on scree and near the passes."),
]

CONTACT = [("Email", "hello@contour-expeditions.com"), ("Phone / WhatsApp", PLACEHOLDER), ("Website", "contour-expeditions.com")]
DISCLAIMER = "Distances, heights and walking times are approximate and assume fit hikers without long breaks. Conditions in the mountains change; always check the weather and trail conditions and follow local signage."
