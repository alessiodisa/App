(function () {
  "use strict";

  var CATEGORIES = ["food", "experience", "sport", "other"];

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

  var SECTION_LABELS = {
    it: { food: "Cibo", experience: "Esperienze", sport: "Sport", other: "Altro" },
    en: { food: "Food", experience: "Experiences", sport: "Sport", other: "Other" }
  };

  var SORT_LABELS = {
    it: { featured: "In evidenza", latest: "Ultime", popular: "Più gettonate" },
    en: { featured: "Featured", latest: "Latest", popular: "Most popular" }
  };

  var SORT_MODES = ["featured", "latest", "popular"];

  var NO_RESULTS_TEXT = {
    it: "Nessun risultato in questa categoria.",
    en: "No results in this category."
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

  function sortItems(items, mode) {
    var arr = items.slice();
    if (mode === "featured") {
      var featured = arr.filter(function (p) { return !!p.featured; });
      arr = featured.length ? featured : arr;
      arr.sort(function (a, b) { return (b.popularity || 0) - (a.popularity || 0); });
    } else if (mode === "latest") {
      arr.sort(function (a, b) { return new Date(b.addedAt || 0) - new Date(a.addedAt || 0); });
    } else {
      arr.sort(function (a, b) { return (b.popularity || 0) - (a.popularity || 0); });
    }
    return arr;
  }

  function init() {
    var places = window.UNITED_PLACES || [];
    var lang = document.documentElement.getAttribute("lang") || "it";
    var cardLabels = CATEGORY_LABELS[lang] || CATEGORY_LABELS.it;
    var sectionLabels = SECTION_LABELS[lang] || SECTION_LABELS.it;
    var sortLabels = SORT_LABELS[lang] || SORT_LABELS.it;
    var locale = lang === "en" ? "en-GB" : "it-IT";

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

    function focusPlace(place) {
      var i = places.indexOf(place);
      if (!map || i === -1 || !markers[i]) return;
      map.flyTo([place.lat, place.lng], 16);
      markers[i].openPopup();
    }

    function cardHtml(place) {
      var media = place.image
        ? '<img class="map-place-photo" src="' + escapeHtml(place.image) + '" alt="' + escapeHtml(place.name) + '" loading="lazy">'
        : '<div class="map-place-icon">' + (CATEGORY_ICONS[place.category] || CATEGORY_ICONS.other) + "</div>";
      var dateStr = "";
      if (place.addedAt) {
        var d = new Date(place.addedAt);
        if (!isNaN(d)) dateStr = d.toLocaleDateString(locale, { day: "2-digit", month: "short" });
      }
      var meta = (dateStr || place.popularity != null)
        ? '<div class="map-place-meta">' +
          "<span>" + escapeHtml(dateStr) + "</span>" +
          (place.popularity != null ? "<span>♥ " + escapeHtml(place.popularity) + "</span>" : "") +
          "</div>"
        : "";
      return (
        '<div class="map-place-card" data-place="' + places.indexOf(place) + '" tabindex="0" role="button" aria-label="' + escapeHtml(place.name) + '">' +
        media +
        '<div class="map-place-body">' +
        '<span class="map-place-category">' + escapeHtml(cardLabels[place.category] || cardLabels.other) + "</span>" +
        '<h3 class="map-place-name">' + escapeHtml(place.name) + "</h3>" +
        (place.description ? '<p class="map-place-desc">' + escapeHtml(place.description) + "</p>" : "") +
        meta +
        "</div></div>"
      );
    }

    function wireCards(container) {
      container.querySelectorAll(".map-place-card").forEach(function (card) {
        var place = places[Number(card.getAttribute("data-place"))];
        if (!place) return;
        card.addEventListener("click", function () { focusPlace(place); });
        card.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); focusPlace(place); }
        });
      });
    }

    var sectionsRoot = document.getElementById("mapCategorySections");
    var sectionState = {};

    function renderSectionGrid(category) {
      var section = sectionsRoot.querySelector('.map-category[data-category="' + category + '"]');
      if (!section) return;
      var grid = section.querySelector(".map-places-grid");
      var items = places.filter(function (p) { return p.category === category; });
      var sorted = sortItems(items, sectionState[category]);
      grid.innerHTML = sorted.map(cardHtml).join("");
      wireCards(grid);
    }

    if (sectionsRoot) {
      var html = "";
      CATEGORIES.forEach(function (category) {
        var items = places.filter(function (p) { return p.category === category; });
        if (!items.length) return;
        sectionState[category] = "featured";

        var sortButtons = SORT_MODES.map(function (mode) {
          return '<button type="button" data-mode="' + mode + '" class="' + (mode === "featured" ? "is-active" : "") + '">' +
            escapeHtml(sortLabels[mode]) + "</button>";
        }).join("");

        html +=
          '<div class="map-category" data-category="' + category + '">' +
          '<div class="map-category-header">' +
          "<h2>" + escapeHtml(sectionLabels[category]) + "</h2>" +
          '<div class="map-sort" data-category="' + category + '">' + sortButtons + "</div>" +
          "</div>" +
          '<div class="map-places-grid"></div>' +
          '<p class="map-category-empty" hidden>' + escapeHtml(NO_RESULTS_TEXT[lang] || NO_RESULTS_TEXT.it) + "</p>" +
          "</div>";
      });
      sectionsRoot.innerHTML = html;

      CATEGORIES.forEach(function (category) {
        if (sectionState[category]) renderSectionGrid(category);
      });

      sectionsRoot.querySelectorAll(".map-sort").forEach(function (group) {
        var category = group.getAttribute("data-category");
        group.querySelectorAll("button").forEach(function (btn) {
          btn.addEventListener("click", function () {
            group.querySelectorAll("button").forEach(function (b) { b.classList.remove("is-active"); });
            btn.classList.add("is-active");
            sectionState[category] = btn.getAttribute("data-mode");
            renderSectionGrid(category);
          });
        });
      });
    }

    var searchInput = document.getElementById("mapSearchInput");

    function applyFilters() {
      var activeBtn = document.querySelector(".map-filter.is-active");
      var activeCategory = activeBtn ? activeBtn.getAttribute("data-category") : "all";
      var query = (searchInput && searchInput.value || "").trim().toLowerCase();

      places.forEach(function (place, i) {
        var matches = (activeCategory === "all" || place.category === activeCategory) &&
          (!query || place.name.toLowerCase().indexOf(query) !== -1);

        if (map && markers[i]) {
          if (matches && !map.hasLayer(markers[i])) markers[i].addTo(map);
          if (!matches && map.hasLayer(markers[i])) map.removeLayer(markers[i]);
        }
      });

      if (sectionsRoot) {
        sectionsRoot.querySelectorAll(".map-category").forEach(function (section) {
          var category = section.getAttribute("data-category");
          var categoryMatches = activeCategory === "all" || activeCategory === category;
          section.style.display = categoryMatches ? "" : "none";

          var visibleCount = 0;
          section.querySelectorAll(".map-place-card").forEach(function (card) {
            var place = places[Number(card.getAttribute("data-place"))];
            var visible = !query || (place && place.name.toLowerCase().indexOf(query) !== -1);
            card.style.display = visible ? "" : "none";
            if (visible) visibleCount++;
          });

          var emptyMsg = section.querySelector(".map-category-empty");
          if (emptyMsg) emptyMsg.hidden = visibleCount !== 0;
        });
      }
    }

    if (searchInput) searchInput.addEventListener("input", applyFilters);

    document.querySelectorAll(".map-filters .map-filter").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".map-filters .map-filter").forEach(function (b) { b.classList.remove("is-active"); });
        btn.classList.add("is-active");
        applyFilters();
      });
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();
