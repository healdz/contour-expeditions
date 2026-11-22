#!/usr/bin/env python3
"""Build a start-date availability file for a hut-to-hut trip.

Downloads daily availability for each hut from hut-reservation.org and marks a
start date as bookable only when hut 1 has beds that night, hut 2 the next
night, and so on. Runs on a schedule via .github/workflows/hut-availability.yml.

Usage: python3 tools/hut_availability.py OUTPUT.json
"""
import datetime
import json
import sys
import time
import urllib.request

TRIP = "swiss-via-alpina"
HUTS = [  # in order of nights
    {"id": 69, "name": "Rotstockhütte"},
    {"id": 44, "name": "Gspaltenhornhütte"},
    {"id": 1, "name": "Blüemlisalphütte"},
]
API = "https://www.hut-reservation.org/api/v1/reservation/getHutAvailability?hutId={}"
BOOK = "https://www.hut-reservation.org/reservation/book-hut/{}/wizard"
UA = "contour-expeditions.com availability calendar (3 requests every 6 hours)"


def fetch(hut_id):
    req = urllib.request.Request(API.format(hut_id), headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        rows = json.load(r)
    beds = {}
    for row in rows:
        # number = free beds (0 = full); None = staffed season but reservations not open yet;
        # -1 = closed or unstaffed (winter room only)
        day = row["date"][:10]
        beds[day] = row.get("freeBeds") if row.get("hutStatus") == "SERVICED" else -1
    return beds


def main(out):
    per_hut = []
    for i, hut in enumerate(HUTS):
        if i:
            time.sleep(2)
        per_hut.append(fetch(hut["id"]))

    days = {}
    for start in sorted(per_hut[0]):
        d0 = datetime.date.fromisoformat(start)
        nights = [(d0 + datetime.timedelta(days=n)).isoformat() for n in range(len(HUTS))]
        if not all(night in beds for night, beds in zip(nights, per_hut)):
            continue
        counts = [beds[night] for night, beds in zip(nights, per_hut)]
        if any(c != -1 for c in counts):  # skip dates where every hut is closed, to keep the file small
            days[start] = counts

    data = {
        "trip": TRIP,
        "updated": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
        "huts": [{"name": h["name"], "url": BOOK.format(h["id"])} for h in HUTS],
        "days": days,  # start date -> per hut on its night: free beds, null = not bookable yet, -1 = closed
    }
    with open(out, "w") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    bookable = sum(1 for c in days.values() if all(isinstance(n, int) and n > 0 for n in c))
    print(f"wrote {out}: {len(days)} dates with any hut open, {bookable} bookable start dates")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else f"{TRIP}.json")
