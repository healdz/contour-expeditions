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
