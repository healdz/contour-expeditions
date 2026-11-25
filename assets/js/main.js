/* Contour Expeditions — site behaviour
   - mobile nav toggle and dropdown menus
   - route maps (Leaflet + OpenTopoMap) on trip pages
   - placeholder booking links fall back to the contact form
   - forms submit to FormSubmit (formsubmit.co)
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
    a.setAttribute("href", base + "reserve?trip=" + encodeURIComponent(trip) + "#booking-form");
  });

  /* Pre-fill the contact form's trip field from ?trip= */
  var params = new URLSearchParams(window.location.search);
  var tripField = document.getElementById("trip-interest");
  if (tripField && params.get("trip")) {
    var wanted = params.get("trip");
    var match = Array.prototype.find.call(tripField.options, function (o) { return o.value === wanted; });
    if (match) tripField.value = wanted;
  }

  /* ---------- Forms ----------
     All three forms (contact, reserve, customize) are emailed by FormSubmit (formsubmit.co),
     sent in the background through its AJAX endpoint. */
  document.querySelectorAll("form[data-formsubmit]").forEach(function (form) {
    var status = form.querySelector(".form-status");
    var email = form.getAttribute("data-email");
    var failed = "Something went wrong sending your message. Please try again or email us at " + email + ".";

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector('[name="_honey"]').value) return; // spam bot

      // Readable email: trip names instead of slugs, and ticked checkboxes joined into one line
      var fd = new FormData();
      new FormData(form).forEach(function (value, key) {
        fd.has(key) ? fd.set(key, fd.get(key) + ", " + value) : fd.append(key, value);
      });
      form.querySelectorAll("select").forEach(function (sel) {
        if (sel.value && !sel.disabled) fd.set(sel.name, sel.options[sel.selectedIndex].text);
      });

      // FormSubmit can take many seconds to answer, so confirm straight away. The answers stay in
      // the (hidden) form, and if the send fails the confirmation is removed and the form comes back.
      status.hidden = true;
      var panel = done();
      fetch(form.action.replace("formsubmit.co/", "formsubmit.co/ajax/"), {
        method: "POST",
        body: fd,
        headers: { Accept: "application/json" },
        keepalive: true // lets the send finish even if the visitor clicks away
      })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (String(data.success) !== "true") throw new Error(data.message || "Request failed");
          form.reset();
        })
        .catch(function (err) {
          console.error("FormSubmit:", err);
          panel.remove();
          form.hidden = false;
          show(failed);
        });
    });

    function show(msg) {
      status.textContent = msg;
      status.hidden = false;
      status.focus();
    }

    // Replace the form with a confirmation and links to keep browsing
    function done() {
      var base = document.body.getAttribute("data-root") || "";
      var panel = document.createElement("div");
      panel.className = "form-success";
      panel.setAttribute("role", "status");
      panel.tabIndex = -1;
      var h = document.createElement("h2");
      h.textContent = form.getAttribute("data-done-title");
      var p = document.createElement("p");
      p.textContent = form.getAttribute("data-done-text") + " Questions in the meantime? Email us at ";
      var mail = document.createElement("a");
      mail.href = "mailto:" + email;
      mail.textContent = email;
      p.appendChild(mail);
      p.appendChild(document.createTextNode("."));
      var links = document.createElement("div");
      links.className = "form-success-links";
      [["Browse Guided Expeditions", "guided-trips", ""], ["Browse Unguided Adventures", "unguided-trips", " btn-outline"]].forEach(function (l) {
        var a = document.createElement("a");
        a.className = "btn" + l[2];
        a.href = base + l[1];
        a.textContent = l[0] + " →";
        links.appendChild(a);
      });
      panel.appendChild(h);
      panel.appendChild(p);
      panel.appendChild(links);
      form.hidden = true;
      form.parentNode.insertBefore(panel, form.nextSibling);
      panel.scrollIntoView({ behavior: "smooth", block: "center" });
      panel.focus({ preventScroll: true });
      return panel;
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
     Trip pages: browse dates and see each hut's status.
     Reservation form: a pop-up ("Available Dates") fills the start/end
     date fields and writes a suggested message. */
  var fmtLong = { weekday: "long", day: "numeric", month: "long", year: "numeric" };

  document.querySelectorAll(".hut-cal").forEach(function (cal) {
    var picker = cal.classList.contains("hut-cal-picker");
    var trip = cal.getAttribute("data-trip");
    var nights = parseInt(cal.getAttribute("data-nights"), 10) || 1;
    var summary = cal.querySelector(".hut-cal-summary");
    var grid = cal.querySelector(".hut-cal-grid");
    var monthLabel = cal.querySelector(".hut-cal-month");
    var detail = cal.querySelector(".hut-cal-detail");
    var sizeSelect = picker ? document.getElementById("f-group") : cal.querySelector("select");
    var base = document.body.getAttribute("data-root") || "";
    var data, months = [], monthIdx = 0, chosen = null;
    var today = new Date(); today.setHours(0, 0, 0, 0);

    function iso(d) {
      return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
    }
    function parse(key) { return new Date(key + "T00:00:00"); }
    function fmt(d, opts) { return d.toLocaleDateString("en-GB", opts); }
    function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
    function groupSize() { return parseInt(sizeSelect.value, 10) || 9; }
    function people(n) { return n + (n === 1 ? " person" : " people"); }
    function endOf(key) { return iso(addDays(parse(key), nights)); }

    function stateOf(key) {
      var counts = data.days[key];
      if (parse(key) < today) return "past";
      if (!counts || counts.indexOf(-1) !== -1) return "closed";
      var size = groupSize();
      return counts.every(function (n) { return n === null || n >= size; }) ? "available" : "full";
    }
    var labels = { available: "Available", full: "Fully booked", closed: "Closed", past: "Past" };

    function showMonthOf(key) {
      var i = months.findIndex(function (m) { return iso(m).slice(0, 7) === key.slice(0, 7); });
      if (i >= 0) monthIdx = i;
    }

    function render() {
      if (!data) return;
      var m = months[monthIdx];
      monthLabel.textContent = fmt(m, { month: "long", year: "numeric" });
      cal.querySelector(".hut-cal-prev").disabled = monthIdx === 0;
      cal.querySelector(".hut-cal-next").disabled = monthIdx === months.length - 1;
      var html = ["M", "T", "W", "T", "F", "S", "S"].map(function (d) { return '<span class="dow">' + d + "</span>"; }).join("");
      var lead = (m.getDay() + 6) % 7;
      for (var i = 0; i < lead; i++) html += "<span></span>";
      for (var d = new Date(m); d.getMonth() === m.getMonth(); d = addDays(d, 1)) {
        var key = iso(d), st = stateOf(key);
        var inTrip = picker && chosen && key > chosen && key <= endOf(chosen);
        var cls = "day " + st + (key === chosen ? " selected" : "") + (inTrip ? " in-trip" : "");
        var title = fmt(d, { weekday: "long", day: "numeric", month: "long" }) + ": " + labels[st];
        var clickable = st === "available" || (!picker && st === "full");
        html += clickable
          ? '<button type="button" class="' + cls + '" data-date="' + key + '" title="' + title + '" aria-label="' + title + '">' + d.getDate() + "</button>"
          : '<span class="' + cls + '" title="' + title + '">' + d.getDate() + "</span>";
      }
      grid.innerHTML = html;
      var count = Object.keys(data.days).filter(function (k) { return stateOf(k) === "available"; }).length;
      summary.textContent = count
        ? count + " start dates available for " + people(groupSize()) + "."
        : "No start dates are currently available for " + people(groupSize()) + ". Contact us and we'll check alternatives.";
      if (picker) {
        cal.querySelector(".hut-cal-selection").textContent = chosen
          ? fmt(parse(chosen), { weekday: "short", day: "numeric", month: "short" }) + " → " +
            fmt(parse(endOf(chosen)), { weekday: "short", day: "numeric", month: "short", year: "numeric" }) + " (" + nights + " nights)"
          : "Choose an available start date.";
        cal.querySelector(".date-apply").disabled = !chosen;
      }
    }

    function showDetail(key) {
      var start = parse(key), st = stateOf(key), counts = data.days[key];
      var rows = data.huts.map(function (hut, i) {
        var n = counts[i];
        var status = n === null ? "booking opens soon" : n === -1 ? "closed" : n === 0 ? "full" : n + " bed" + (n === 1 ? "" : "s") + " free";
        return "<li><strong>Night " + (i + 1) + " · " + fmt(addDays(start, i), { weekday: "short", day: "numeric", month: "short" }) +
          "</strong> " + hut.name + " — " + status + "</li>";
      }).join("");
      var href = base + "reserve?trip=" + encodeURIComponent(trip) + "&start=" + key + "&group=" + groupSize() + "#booking-form";
      detail.innerHTML = "<h4>" + fmt(start, { weekday: "short", day: "numeric", month: "short", year: "numeric" }) + " — " + labels[st] + "</h4><ul>" + rows + "</ul>" +
        (st === "available" ? '<a class="btn btn-small" href="' + href + '">Reserve this start date →</a>' : "");
    }

    grid.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-date]");
      if (!btn) return;
      chosen = btn.getAttribute("data-date");
      render();
      if (!picker) showDetail(chosen);
    });
    cal.querySelector(".hut-cal-prev").addEventListener("click", function () { monthIdx--; render(); });
    cal.querySelector(".hut-cal-next").addEventListener("click", function () { monthIdx++; render(); });

    /* ----- Reservation form: date fields, pop-up, and suggested message ----- */
    var fields, dialog, startInput, endInput, msg, tripSelect, committed = null, autoText = "";
    if (picker) {
      fields = cal.closest(".date-fields");
      dialog = cal.closest("dialog");
      startInput = fields.querySelector('[name="start date"]');
      endInput = fields.querySelector('[name="end date"]');
      msg = document.getElementById("f-msg");
      tripSelect = document.getElementById("trip-interest");
      var short = fields.getAttribute("data-trip-short");

      var writeMessage = function () {
        if (!msg || (msg.value && msg.value !== autoText)) return; // respect the visitor's own words
        autoText = "Hi, I'd like to reserve " + short + " for " + people(groupSize()) +
          " starting on " + (committed ? fmt(parse(committed), fmtLong) : "___") + ".";
        msg.value = autoText;
      };
      var clearMessage = function () {
        if (msg && msg.value === autoText) msg.value = "";
        autoText = "";
      };
      var commit = function (key) {
        committed = key;
        startInput.value = key ? fmt(parse(key), fmtLong) : "";
        endInput.value = key ? fmt(parse(endOf(key)), fmtLong) : "";
        writeMessage();
      };
      var open = function () {
        chosen = committed;
        if (data) { showMonthOf(chosen || Object.keys(data.days).filter(function (k) { return stateOf(k) === "available"; })[0] || ""); render(); }
        dialog.showModal();
      };
      [startInput, endInput].forEach(function (input) {
        input.addEventListener("click", open);
        input.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " " || e.key === "ArrowDown") { e.preventDefault(); open(); }
        });
      });
      cal.querySelector(".date-apply").addEventListener("click", function () { commit(chosen); dialog.close(); startInput.focus(); });
      cal.querySelector(".date-cancel").addEventListener("click", function () { dialog.close(); });
      cal.querySelector(".date-dialog-close").addEventListener("click", function () { dialog.close(); });
      dialog.addEventListener("click", function (e) { if (e.target === dialog) dialog.close(); });

      sizeSelect.addEventListener("change", function () {
        if (fields.hidden) return;
        writeMessage();
        render();
      });

      var syncVisibility = function () {
        var show = tripSelect.value === trip;
        fields.hidden = !show;
        startInput.disabled = endInput.disabled = !show;
        if (show) writeMessage(); else clearMessage();
      };
      tripSelect.addEventListener("change", syncVisibility);
      syncVisibility();
    } else {
      sizeSelect.addEventListener("change", function () {
        if (chosen && stateOf(chosen) !== "available") chosen = null;
        detail.innerHTML = "";
        render();
      });
    }

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
        showMonthOf(keys.filter(function (k) { return stateOf(k) === "available"; })[0] || keys[0] || "");
        if (picker) {
          var params = new URLSearchParams(window.location.search);
          if (params.get("trip") === trip) {
            if (params.get("group")) sizeSelect.value = params.get("group");
            var want = params.get("start");
            if (want && data.days[want]) commit(want); else writeMessage();
          }
        }
        render();
      })
      .catch(function () {
        cal.classList.add("hut-cal-error");
        summary.textContent = picker
          ? "Hut availability couldn't be loaded right now. Tell us your preferred dates in the message below."
          : "Hut availability couldn't be loaded right now. Contact us for dates.";
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
