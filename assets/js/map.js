(function () {
  "use strict";

  var CATEGORY_ICONS = {
    food: "🍴",
    experience: "⭐",
    sport: "⚽",
    other: "📍"
  };

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

  function initMap() {
    var el = document.getElementById("unitedMap");
    if (!el || typeof L === "undefined") return;

    var map = L.map(el, { scrollWheelZoom: false }).setView([45.6669, 12.2431], 13);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors'
    }).addTo(map);

    el.addEventListener("mouseenter", function () { map.scrollWheelZoom.enable(); });
    el.addEventListener("mouseleave", function () { map.scrollWheelZoom.disable(); });

    var places = window.UNITED_PLACES || [];
    places.forEach(function (place) {
      L.marker([place.lat, place.lng], { icon: makeIcon(place.category) })
        .addTo(map)
        .bindPopup(
          "<strong>" + place.name + "</strong>" +
          (place.description ? "<br>" + place.description : "")
        );
    });
  }

  document.addEventListener("DOMContentLoaded", initMap);
})();
