(function () {
  "use strict";

  var CATEGORY_ICONS = {
    food: "🍴",
    experience: "⭐",
    sport: "⚽",
    other: "📍"
  };

  var CATEGORY_LABELS = {
    it: { food: "Cibo", experience: "Esperienza", sport: "Sport", other: "Altro" },
    en: { food: "Food", experience: "Experience", sport: "Sport", other: "Other" }
  };

  function escapeHtml(str) {
    return String(str == null ? "" : str).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function makeIcon(category) {
    var emoji = CATEGORY_ICONS[category] || CATEGORY_ICONS.other;
    return L.divIcon({
      className: "united-map-pin",
      html: "<span>" + emoji + "</span>",
      iconSize: [30, 30],
      iconAnchor: [15, 15],
      popupAnchor: [0, -18]
    });
  }

  function init() {
    var places = window.UNITED_PLACES || [];
    var lang = document.documentElement.getAttribute("lang") || "it";
    var labels = CATEGORY_LABELS[lang] || CATEGORY_LABELS.it;

    var grid = document.getElementById("mapPlacesGrid");
    if (grid) {
      grid.innerHTML = places.map(function (place, i) {
        var media = place.image
          ? '<img class="map-place-photo" src="' + escapeHtml(place.image) + '" alt="' + escapeHtml(place.name) + '" loading="lazy">'
          : '<div class="map-place-icon">' + (CATEGORY_ICONS[place.category] || CATEGORY_ICONS.other) + "</div>";
        return (
          '<div class="map-place-card" data-index="' + i + '" tabindex="0" role="button" aria-label="' + escapeHtml(place.name) + '">' +
          media +
          '<div class="map-place-body">' +
          '<span class="map-place-category">' + escapeHtml(labels[place.category] || labels.other) + "</span>" +
          '<h3 class="map-place-name">' + escapeHtml(place.name) + "</h3>" +
          (place.description ? '<p class="map-place-desc">' + escapeHtml(place.description) + "</p>" : "") +
          "</div></div>"
        );
      }).join("");
    }

    var map = null;
    var markers = [];
    var mapEl = document.getElementById("unitedMap");

    if (mapEl && typeof L !== "undefined") {
      map = L.map(mapEl, { scrollWheelZoom: false }).setView([45.6669, 12.2431], 13);

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors'
      }).addTo(map);

      mapEl.addEventListener("mouseenter", function () { map.scrollWheelZoom.enable(); });
      mapEl.addEventListener("mouseleave", function () { map.scrollWheelZoom.disable(); });

      markers = places.map(function (place) {
        var marker = L.marker([place.lat, place.lng], { icon: makeIcon(place.category) });
        marker.bindPopup(
          "<strong>" + escapeHtml(place.name) + "</strong>" +
          (place.description ? "<br>" + escapeHtml(place.description) : "")
        );
        marker.addTo(map);
        return marker;
      });
    }

    if (grid) {
      grid.querySelectorAll(".map-place-card").forEach(function (card) {
        function focusPlace() {
          var i = Number(card.getAttribute("data-index"));
          var place = places[i];
          if (!map || !markers[i]) return;
          map.flyTo([place.lat, place.lng], 16);
          markers[i].openPopup();
        }
        card.addEventListener("click", focusPlace);
        card.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); focusPlace(); }
        });
      });
    }

    var searchInput = document.getElementById("mapSearchInput");

    function applyFilters() {
      var activeBtn = document.querySelector(".map-filter.is-active");
      var category = activeBtn ? activeBtn.getAttribute("data-category") : "all";
      var query = (searchInput && searchInput.value || "").trim().toLowerCase();

      places.forEach(function (place, i) {
        var visible = (category === "all" || place.category === category) &&
          (!query || place.name.toLowerCase().indexOf(query) !== -1);

        if (map && markers[i]) {
          if (visible && !map.hasLayer(markers[i])) markers[i].addTo(map);
          if (!visible && map.hasLayer(markers[i])) map.removeLayer(markers[i]);
        }

        var card = grid && grid.querySelector('.map-place-card[data-index="' + i + '"]');
        if (card) card.style.display = visible ? "" : "none";
      });
    }

    if (searchInput) searchInput.addEventListener("input", applyFilters);

    document.querySelectorAll(".map-filter").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".map-filter").forEach(function (b) { b.classList.remove("is-active"); });
        btn.classList.add("is-active");
        applyFilters();
      });
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();
