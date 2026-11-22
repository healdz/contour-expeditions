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
  var msgField = document.getElementById("f-msg");
  if (msgField && params.get("start") && !msgField.value) {
    var startDate = new Date(params.get("start") + "T00:00:00");
    var tripName = tripField && tripField.selectedIndex > 0 ? tripField.options[tripField.selectedIndex].text.replace(/ \(.*\)$/, "") : "the trip";
    var group = parseInt(params.get("group"), 10);
    msgField.value = "I'd like to start " + tripName + " on " +
      startDate.toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long", year: "numeric" }) +
      (group ? " with " + group + (group === 1 ? " person" : " people") : "") + ".";
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
     Data file: start date -> free beds per hut on its night
     (number of beds, null = reservations not open yet, -1 = closed). */
  document.querySelectorAll(".hut-cal").forEach(function (cal) {
    var summary = cal.querySelector(".hut-cal-summary");
    var grid = cal.querySelector(".hut-cal-grid");
    var monthLabel = cal.querySelector(".hut-cal-month");
    var detail = cal.querySelector(".hut-cal-detail");
    var sizeSelect = cal.querySelector("select");
    var base = document.body.getAttribute("data-root") || "";
    var data, months = [], monthIdx = 0;
    var today = new Date(); today.setHours(0, 0, 0, 0);

    function iso(d) {
      return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
    }
    function fmt(d, opts) { return d.toLocaleDateString("en-GB", opts); }
    function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }

    function stateOf(key) {
      var counts = data.days[key];
      if (new Date(key + "T00:00:00") < today) return "past";
      if (!counts || counts.indexOf(-1) !== -1) return "closed";
      if (counts.indexOf(null) !== -1) return "pending";
      return Math.min.apply(null, counts) >= +sizeSelect.value ? "available" : "full";
    }
    var labels = { available: "Available", full: "Fully booked", pending: "Not yet bookable", closed: "Closed or not yet scheduled", past: "Past" };

    function render() {
      var m = months[monthIdx];
      monthLabel.textContent = fmt(m, { month: "long", year: "numeric" });
      cal.querySelector(".hut-cal-prev").disabled = monthIdx === 0;
      cal.querySelector(".hut-cal-next").disabled = monthIdx === months.length - 1;
      var html = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"].map(function (d) { return '<span class="dow">' + d + "</span>"; }).join("");
      var lead = (m.getDay() + 6) % 7;
      for (var i = 0; i < lead; i++) html += "<span></span>";
      for (var d = new Date(m); d.getMonth() === m.getMonth(); d = addDays(d, 1)) {
        var key = iso(d), st = stateOf(key);
        var title = fmt(d, { weekday: "long", day: "numeric", month: "long" }) + ": " + labels[st];
        html += st === "past" || st === "closed"
          ? '<span class="day ' + st + '" title="' + title + '">' + d.getDate() + "</span>"
          : '<button type="button" class="day ' + st + '" data-date="' + key + '" title="' + title + '" aria-label="' + title + '">' + d.getDate() + "</button>";
      }
      grid.innerHTML = html;
      var count = Object.keys(data.days).filter(function (k) { return stateOf(k) === "available"; }).length;
      summary.textContent = count
        ? count + " start date" + (count === 1 ? "" : "s") + " available for " + sizeSelect.value + (sizeSelect.value === "1" ? " person" : " people") + ". Choose a date to see the huts and request it."
        : "No start dates are bookable online for " + sizeSelect.value + (sizeSelect.value === "1" ? " person" : " people") + " yet. The huts open reservations for each summer season at different times. Contact us and we'll book your preferred dates as soon as they do.";
    }

    function showDetail(key) {
      var start = new Date(key + "T00:00:00"), st = stateOf(key), counts = data.days[key];
      var rows = data.huts.map(function (hut, i) {
        var n = counts[i];
        var status = n === null ? "not bookable yet" : n === -1 ? "closed" : n === 0 ? "full" : n + " bed" + (n === 1 ? "" : "s") + " free";
        return "<li><strong>Night " + (i + 1) + " · " + fmt(addDays(start, i), { weekday: "short", day: "numeric", month: "short" }) +
          '</strong> <a href="' + hut.url + '" target="_blank" rel="noopener">' + hut.name + "</a> — " + status + "</li>";
      }).join("");
      var href = base + "contact?trip=" + encodeURIComponent(cal.getAttribute("data-trip")) + "&start=" + key + "&group=" + sizeSelect.value + "#contact-form";
      detail.innerHTML = "<h4>Start " + fmt(start, { weekday: "long", day: "numeric", month: "long", year: "numeric" }) + " — " + labels[st] + "</h4><ul>" + rows + "</ul>" +
        '<a class="btn btn-small' + (st === "available" ? "" : " btn-outline") + '" href="' + href + '">' +
        (st === "available" ? "Request this start date →" : "Ask us about this date →") + "</a>";
    }

    grid.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-date]");
      if (!btn) return;
      grid.querySelectorAll(".selected").forEach(function (b) { b.classList.remove("selected"); });
      btn.classList.add("selected");
      showDetail(btn.getAttribute("data-date"));
    });
    cal.querySelector(".hut-cal-prev").addEventListener("click", function () { monthIdx--; render(); });
    cal.querySelector(".hut-cal-next").addEventListener("click", function () { monthIdx++; render(); });
    sizeSelect.addEventListener("change", function () { detail.innerHTML = ""; render(); });

    fetch(cal.getAttribute("data-src"), { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (json) {
        data = json;
        var keys = Object.keys(data.days).filter(function (k) { return data.days[k].some(function (c) { return c !== -1; }); }).sort();
        var first = new Date(keys[0] + "T00:00:00"), last = new Date(keys[keys.length - 1] + "T00:00:00");
        if (first < today) first = today;
        for (var m = new Date(first.getFullYear(), first.getMonth(), 1); m <= last; m = new Date(m.getFullYear(), m.getMonth() + 1, 1)) months.push(m);
        var firstOpen = keys.filter(function (k) { return stateOf(k) === "available"; })[0] ||
                        keys.filter(function (k) { return stateOf(k) === "pending" || stateOf(k) === "full"; })[0];
        if (firstOpen) {
          var fo = new Date(firstOpen + "T00:00:00");
          monthIdx = Math.max(0, months.findIndex(function (m) { return m.getFullYear() === fo.getFullYear() && m.getMonth() === fo.getMonth(); }));
        }
        cal.querySelector(".hut-cal-updated").textContent = "Hut data last updated " +
          new Date(data.updated).toLocaleString("en-GB", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" }) + ".";
        render();
      })
      .catch(function () {
        cal.classList.add("hut-cal-error");
        summary.innerHTML = 'Live hut availability couldn\'t be loaded right now. <a href="' + base + "contact?trip=" + cal.getAttribute("data-trip") + '#contact-form">Contact us</a> for dates.';
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
