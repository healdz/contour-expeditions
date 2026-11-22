/* Contour Expeditions — site behaviour
   - mobile nav toggle and dropdown menus
   - route maps (Leaflet + OpenTopoMap) on trip pages
   - placeholder booking links fall back to the contact form
   - forms show a notice until a Formspree ID is configured
*/
(function () {
  "use strict";

  /* ---------- Navigation ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("open", !open);
      document.body.classList.toggle("nav-open", !open);
    });
  }

  var dropdownToggles = document.querySelectorAll(".dropdown-toggle");

  function closeDropdowns(except) {
    dropdownToggles.forEach(function (btn) {
      if (btn === except) return;
      btn.setAttribute("aria-expanded", "false");
      document.getElementById(btn.getAttribute("aria-controls")).classList.remove("open");
    });
  }

  dropdownToggles.forEach(function (btn) {
    var menu = document.getElementById(btn.getAttribute("aria-controls"));
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = btn.getAttribute("aria-expanded") === "true";
      closeDropdowns(btn);
      btn.setAttribute("aria-expanded", String(!open));
      menu.classList.toggle("open", !open);
    });
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".has-dropdown")) closeDropdowns();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var openBtn = document.querySelector('.dropdown-toggle[aria-expanded="true"]');
    closeDropdowns();
    if (openBtn) openBtn.focus();
  });

  /* ---------- Booking links ----------
     Until a real booking URL is pasted into a "Reserve" / "Waitlist" link,
     send people to the contact form with the trip pre-filled. */
  document.querySelectorAll('a[data-todo="booking-link"]').forEach(function (a) {
    if (a.getAttribute("href") !== "#") return;
    var trip = a.getAttribute("data-trip") || "";
    var base = document.body.getAttribute("data-root") || "";
    a.setAttribute("href", base + "contact?trip=" + encodeURIComponent(trip) + "#contact-form");
  });

  /* Pre-fill the contact form's trip field from ?trip= */
  var params = new URLSearchParams(window.location.search);
  var tripField = document.getElementById("trip-interest");
  if (tripField && params.get("trip")) {
    var wanted = params.get("trip");
    var match = Array.prototype.find.call(tripField.options, function (o) { return o.value === wanted; });
    if (match) tripField.value = wanted;
  }

  /* ---------- Forms ---------- */
  document.querySelectorAll("form[data-formspree]").forEach(function (form) {
    var status = form.querySelector(".form-status");

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector('[name="_gotcha"]').value) return; // spam bot

      if (form.action.indexOf("YOUR_FORM_ID") !== -1) {
        show("This form isn't connected yet. Please email us directly in the meantime.");
        return;
      }

      var btn = form.querySelector('[type="submit"]');
      btn.disabled = true;
      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" }
      })
        .then(function (res) {
          if (!res.ok) throw new Error("Request failed");
          form.reset();
          show("Thanks — your message is on its way. We'll be in touch within two business days.");
        })
        .catch(function () {
          show("Something went wrong sending your message. Please try again or email us directly.");
        })
        .finally(function () { btn.disabled = false; });
    });

    function show(msg) {
      status.textContent = msg;
      status.hidden = false;
      status.focus();
    }
  });

  /* ---------- Photo gallery lightbox ---------- */
  var galleryItems = Array.prototype.slice.call(document.querySelectorAll(".gallery-item"));
  if (galleryItems.length) {
    var box = document.createElement("dialog");
    box.className = "lightbox";
    box.setAttribute("aria-label", "Photo viewer");
    box.innerHTML =
      '<figure><img alt=""><figcaption></figcaption></figure>' +
      '<button class="lb-prev" type="button" aria-label="Previous photo">&#8249;</button>' +
      '<button class="lb-next" type="button" aria-label="Next photo">&#8250;</button>' +
      '<button class="lb-close" type="button" aria-label="Close">&times;</button>';
    document.body.appendChild(box);
    var boxImg = box.querySelector("img");
    var boxCap = box.querySelector("figcaption");
    var current = 0;

    function showPhoto(i) {
      current = (i + galleryItems.length) % galleryItems.length;
      var thumb = galleryItems[current].querySelector("img");
      boxImg.src = galleryItems[current].getAttribute("data-full");
      boxImg.alt = thumb.alt;
      boxCap.textContent = thumb.alt;
    }

    galleryItems.forEach(function (item, i) {
      item.addEventListener("click", function () {
        showPhoto(i);
        box.showModal();
      });
    });
    box.querySelector(".lb-prev").addEventListener("click", function () { showPhoto(current - 1); });
    box.querySelector(".lb-next").addEventListener("click", function () { showPhoto(current + 1); });
    box.querySelector(".lb-close").addEventListener("click", function () { box.close(); });
    box.addEventListener("click", function (e) { if (e.target === box) box.close(); });
    box.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") showPhoto(current - 1);
      if (e.key === "ArrowRight") showPhoto(current + 1);
    });
    box.addEventListener("close", function () { galleryItems[current].focus(); });
  }

  /* ---------- Hut availability calendar ----------
     Data file: start date -> per hut on its night: free beds,
     null = not open for booking yet (counts as available), -1 = closed.
     Trip pages browse dates; the contact form (.hut-cal-picker) picks
     a start date or a window and writes it into hidden form fields. */
  document.querySelectorAll(".hut-cal").forEach(function (cal) {
    var picker = cal.classList.contains("hut-cal-picker");
    var trip = cal.getAttribute("data-trip");
    var summary = cal.querySelector(".hut-cal-summary");
    var grid = cal.querySelector(".hut-cal-grid");
    var monthLabel = cal.querySelector(".hut-cal-month");
    var detail = cal.querySelector(".hut-cal-detail");
    var selection = cal.querySelector(".hut-cal-selection");
    var sizeSelect = picker ? document.getElementById("f-group") : cal.querySelector("select");
    var base = document.body.getAttribute("data-root") || "";
    var data, months = [], monthIdx = 0, chosen = null, windowStart = null, windowEnd = null;
    var today = new Date(); today.setHours(0, 0, 0, 0);

    function iso(d) {
      return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
    }
    function parse(key) { return new Date(key + "T00:00:00"); }
    function fmt(d, opts) { return d.toLocaleDateString("en-GB", opts); }
    function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
    function groupSize() { return parseInt(sizeSelect.value, 10) || 9; }
    function people(n) { return n + (n === 1 ? " person" : " people"); }
    function mode() { var r = cal.querySelector('input[name="date_type"]:checked'); return r && r.value === "Window of dates" ? "window" : "date"; }

    function stateOf(key) {
      var counts = data.days[key];
      if (parse(key) < today) return "past";
      if (!counts || counts.indexOf(-1) !== -1) return "closed";
      var size = groupSize();
      return counts.every(function (n) { return n === null || n >= size; }) ? "available" : "full";
    }
    var labels = { available: "Available", full: "Fully booked", closed: "Closed", past: "Past" };

    function inWindow(key) { return windowStart && key >= windowStart && key <= (windowEnd || windowStart); }

    function render() {
      var m = months[monthIdx];
      monthLabel.textContent = fmt(m, { month: "long", year: "numeric" });
      cal.querySelector(".hut-cal-prev").disabled = monthIdx === 0;
      cal.querySelector(".hut-cal-next").disabled = monthIdx === months.length - 1;
      var html = ["M", "T", "W", "T", "F", "S", "S"].map(function (d) { return '<span class="dow">' + d + "</span>"; }).join("");
      var lead = (m.getDay() + 6) % 7;
      for (var i = 0; i < lead; i++) html += "<span></span>";
      for (var d = new Date(m); d.getMonth() === m.getMonth(); d = addDays(d, 1)) {
        var key = iso(d), st = stateOf(key);
        var cls = "day " + st + (key === chosen && !(picker && mode() === "window") ? " selected" : "") + (picker && mode() === "window" && inWindow(key) ? " in-window" : "");
        var title = fmt(d, { weekday: "long", day: "numeric", month: "long" }) + ": " + labels[st];
        var clickable = st === "available" || (picker && mode() === "window" && st !== "past" && st !== "closed") || (!picker && st === "full");
        html += clickable
          ? '<button type="button" class="' + cls + '" data-date="' + key + '" title="' + title + '" aria-label="' + title + '">' + d.getDate() + "</button>"
          : '<span class="' + cls + '" title="' + title + '">' + d.getDate() + "</span>";
      }
      grid.innerHTML = html;
      var count = Object.keys(data.days).filter(function (k) { return stateOf(k) === "available"; }).length;
      summary.textContent = count
        ? count + " start dates available for " + people(groupSize()) + "."
        : "No start dates are currently available for " + people(groupSize()) + ". Contact us and we'll check alternatives.";
    }

    function showDetail(key) {
      var start = parse(key), st = stateOf(key), counts = data.days[key];
      var rows = data.huts.map(function (hut, i) {
        var n = counts[i];
        var status = n === null ? "booking opens soon" : n === -1 ? "closed" : n === 0 ? "full" : n + " bed" + (n === 1 ? "" : "s") + " free";
        return "<li><strong>Night " + (i + 1) + " · " + fmt(addDays(start, i), { weekday: "short", day: "numeric", month: "short" }) +
          "</strong> " + hut.name + " — " + status + "</li>";
      }).join("");
      var href = base + "contact?trip=" + encodeURIComponent(trip) + "&start=" + key + "&group=" + groupSize() + "#contact-form";
      detail.innerHTML = "<h4>" + fmt(start, { weekday: "short", day: "numeric", month: "short", year: "numeric" }) + " — " + labels[st] + "</h4><ul>" + rows + "</ul>" +
        (st === "available" ? '<a class="btn btn-small" href="' + href + '">Reserve this start date →</a>' : "");
    }

    function writeSelection() {
      var f = function (k) { return fmt(parse(k), { weekday: "short", day: "numeric", month: "short", year: "numeric" }); };
      cal.querySelector('[name="start_date"]').value = mode() === "date" && chosen ? chosen : "";
      cal.querySelector('[name="window_start"]').value = mode() === "window" && windowStart ? windowStart : "";
      cal.querySelector('[name="window_end"]').value = mode() === "window" && windowStart ? (windowEnd || windowStart) : "";
      if (mode() === "date") {
        selection.textContent = chosen ? "Selected start date: " + f(chosen) + " (3 nights)." : "Choose an available start date.";
      } else if (!windowStart) {
        selection.textContent = "Choose the first and last start dates you could do.";
      } else if (!windowEnd) {
        selection.textContent = "Window starts " + f(windowStart) + ". Now choose the last start date.";
      } else {
        var n = Object.keys(data.days).filter(function (k) { return k >= windowStart && k <= windowEnd && stateOf(k) === "available"; }).length;
        selection.textContent = "Window: " + f(windowStart) + " – " + f(windowEnd) + " (" + n + " available start date" + (n === 1 ? "" : "s") + ").";
      }
    }

    grid.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-date]");
      if (!btn) return;
      var key = btn.getAttribute("data-date");
      if (!picker) { chosen = key; render(); showDetail(key); return; }
      if (mode() === "date") {
        chosen = key;
      } else if (!windowStart || windowEnd || key < windowStart) {
        windowStart = key; windowEnd = null;
      } else {
        windowEnd = key;
      }
      render(); writeSelection();
    });
    cal.querySelector(".hut-cal-prev").addEventListener("click", function () { monthIdx--; render(); });
    cal.querySelector(".hut-cal-next").addEventListener("click", function () { monthIdx++; render(); });
    sizeSelect.addEventListener("change", function () {
      if (chosen && stateOf(chosen) !== "available") chosen = null;
      if (detail) detail.innerHTML = "";
      if (data) { render(); if (picker) writeSelection(); }
    });
    cal.querySelectorAll('input[name="date_type"]').forEach(function (r) {
      r.addEventListener("change", function () { render(); writeSelection(); });
    });

    // On the contact form, show this calendar only while its trip is selected.
    var tripSelect = document.getElementById("trip-interest");
    function syncVisibility() {
      var show = tripSelect.value === trip;
      cal.hidden = !show;
      cal.querySelectorAll("input").forEach(function (i) { i.disabled = !show; });
    }
    if (picker && tripSelect) { tripSelect.addEventListener("change", syncVisibility); syncVisibility(); }

    fetch(cal.getAttribute("data-src"), { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (json) {
        data = json;
        var keys = Object.keys(data.days).filter(function (k) { return parse(k) >= today; }).sort();
        var seen = {};
        keys.forEach(function (k) {
          var ym = k.slice(0, 7);
          if (!seen[ym]) { seen[ym] = true; months.push(parse(ym + "-01")); }
        });
        var params = new URLSearchParams(window.location.search);
        if (picker && params.get("trip") === trip && params.get("group")) sizeSelect.value = params.get("group");
        var want = picker && params.get("trip") === trip && params.get("start");
        if (want && data.days[want]) chosen = want;
        var target = chosen || keys.filter(function (k) { return stateOf(k) === "available"; })[0] || keys[0];
        if (target) monthIdx = Math.max(0, months.findIndex(function (m) { return iso(m).slice(0, 7) === target.slice(0, 7); }));
        render();
        if (picker) writeSelection();
      })
      .catch(function () {
        cal.classList.add("hut-cal-error");
        summary.textContent = "Hut availability couldn't be loaded right now. Tell us your preferred dates in the message below and we'll check for you.";
      });
  });

  /* ---------- Route maps ---------- */
  var maps = document.querySelectorAll(".route-map[data-route]");
  if (maps.length && window.L) {
    maps.forEach(function (el) {
      var points = JSON.parse(el.getAttribute("data-route"));
      var latlngs = points.map(function (p) { return [p[0], p[1]]; });

      var map = L.map(el, { scrollWheelZoom: false });
      L.tileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", {
        maxZoom: 17,
        attribution:
          'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
          '<a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; ' +
          '<a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
      }).addTo(map);

      L.polyline(latlngs, { color: "#c8553d", weight: 4, opacity: 0.9, dashArray: "8 6" }).addTo(map);

      points.forEach(function (p, i) {
        var end = i === 0 || i === points.length - 1;
        L.circleMarker([p[0], p[1]], {
          radius: end ? 7 : 5,
          color: "#1f2326",
          weight: 2,
          fillColor: end ? "#c8553d" : "#ffffff",
          fillOpacity: 1
        })
          .addTo(map)
          .bindTooltip(p[2], { className: "route-label", direction: "top", offset: [0, -6] });
      });

      map.fitBounds(L.latLngBounds(latlngs), { padding: [40, 40] });
    });
  }
})();
