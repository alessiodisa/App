(function () {
  "use strict";

  var LANG_KEY = "united-lang";

  function applyLang(lang) {
    var dict = I18N[lang] || I18N.it;
    document.documentElement.setAttribute("lang", lang);

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (dict[key] != null) el.textContent = dict[key];
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-placeholder");
      if (dict[key] != null) el.setAttribute("placeholder", dict[key]);
    });

    document.querySelectorAll(".lang-switch button").forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-lang") === lang);
    });
  }

  function initLang() {
    var saved = localStorage.getItem(LANG_KEY);
    var browser = (navigator.language || "it").slice(0, 2);
    var lang = saved || (I18N[browser] ? browser : "it");
    applyLang(lang);

    document.querySelectorAll(".lang-switch button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var lang = btn.getAttribute("data-lang");
        localStorage.setItem(LANG_KEY, lang);
        applyLang(lang);
      });
    });
  }

  function initNavScroll() {
    var nav = document.getElementById("siteNav");
    if (!nav) return;
    function onScroll() {
      nav.classList.toggle("is-scrolled", window.scrollY > 8);
    }
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  function initMobileNav() {
    var nav = document.getElementById("siteNav");
    var toggle = document.getElementById("navToggle");
    if (!nav || !toggle) return;
    toggle.addEventListener("click", function () {
      nav.classList.toggle("is-open");
    });
    nav.querySelectorAll(".mobile-nav a").forEach(function (a) {
      a.addEventListener("click", function () { nav.classList.remove("is-open"); });
    });
  }

  function initReveal() {
    var els = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window) || !els.length) {
      els.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    els.forEach(function (el) { observer.observe(el); });
  }

  function initJoinForm() {
    var form = document.getElementById("joinForm");
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var lang = document.documentElement.getAttribute("lang") || "it";
      var note = form.parentElement.querySelector(".join-note");
      if (note) note.textContent = I18N[lang]["join.thanks"];
      form.reset();
    });
  }

  // Infinite horizontal auto-scroll: clones the group markup enough times to
  // always keep at least two screens' worth of content queued ahead, then
  // drives the CSS animation off the exact measured pixel distance so the
  // loop never gaps or pops (used by both the partners bar and the
  // Instagram carousel).
  function initAutoScroll(track, groupSelector, cssVarName, defaultGap) {
    if (!track) return;
    var base = track.querySelector(groupSelector);
    if (!base) return;

    function fillAndMeasure() {
      track.querySelectorAll(groupSelector + "[data-clone]").forEach(function (el) {
        el.remove();
      });

      var groupWidth = base.getBoundingClientRect().width;
      var gap = parseFloat(getComputedStyle(track).columnGap) || defaultGap;
      var step = groupWidth + gap;
      if (!step || step <= gap) return;

      var viewportWidth = track.parentElement.getBoundingClientRect().width;
      var groupsNeeded = Math.ceil((viewportWidth * 2) / step) + 1;
      var current = track.querySelectorAll(groupSelector).length;

      for (var i = current; i < groupsNeeded; i++) {
        var clone = base.cloneNode(true);
        clone.setAttribute("data-clone", "");
        clone.setAttribute("aria-hidden", "true");
        track.appendChild(clone);
      }

      track.style.setProperty(cssVarName, step + "px");
      track.classList.add("mq-ready");
    }

    fillAndMeasure();
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(fillAndMeasure);
    }
    window.addEventListener("resize", fillAndMeasure);
  }

  // Tries to load the real Instagram posts from the Netlify function. If it
  // is not configured yet (no token) or unreachable (e.g. local file preview,
  // or the site isn't deployed to Netlify), the static placeholder tiles
  // already in the HTML stay untouched.
  function initInstagramFeed() {
    var track = document.getElementById("igTrack");
    if (!track) return;

    fetch("/.netlify/functions/instagram-feed")
      .then(function (res) {
        if (!res.ok) throw new Error("feed unavailable");
        return res.json();
      })
      .then(function (data) {
        if (!data.posts || !data.posts.length) return;

        track.querySelectorAll(".ig-group").forEach(function (el) {
          el.remove();
        });
        track.classList.remove("mq-ready");
        track.style.removeProperty("--ig-w");

        var group = document.createElement("div");
        group.className = "ig-group";
        data.posts.forEach(function (post) {
          var tile = document.createElement("a");
          tile.className = "ig-tile ig-real";
          tile.href = post.permalink;
          tile.target = "_blank";
          tile.rel = "noopener";
          tile.style.backgroundImage = "url('" + post.image + "')";

          var label = document.createElement("span");
          label.className = "ig-label";
          label.textContent = post.caption || "@unitedcultureee";
          tile.appendChild(label);

          group.appendChild(tile);
        });
        track.appendChild(group);

        initAutoScroll(track, ".ig-group", "--ig-w", 20);
      })
      .catch(function () {
        // Keep the existing placeholder tiles.
      });
  }

  // On real devices (especially over cellular) the video often isn't
  // buffered enough to play the instant the page loads — play() is called
  // too early, silently fails, and nothing retries it until the browser's
  // own autoplay-unlock gesture (scroll/tap) fires our retry below. To get
  // it playing the moment it's actually ready — with zero interaction —
  // this also retries on every buffering milestone (loadeddata/canplay/
  // canplaythrough) and once more when it's fully downloaded.
  function initVideoAutoplay() {
    var videos = document.querySelectorAll("video[autoplay]");
    if (!videos.length) return;

    function tryPlay(video) {
      var p = video.play();
      if (p && p.catch) p.catch(function () {});
    }

    videos.forEach(function (video) {
      tryPlay(video);
      ["loadeddata", "canplay", "canplaythrough", "progress"].forEach(function (evt) {
        video.addEventListener(evt, function () { tryPlay(video); });
      });
      if (video.readyState >= 2) tryPlay(video);
    });

    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) tryPlay(entry.target);
        });
      }, { threshold: 0.1 });
      videos.forEach(function (v) { io.observe(v); });
    }

    var retry = function () { videos.forEach(tryPlay); };
    ["touchstart", "scroll", "click"].forEach(function (evt) {
      document.addEventListener(evt, retry, { once: true, passive: true });
    });
  }

  // Renders the Treviso United standings/roster/staff/fixtures block from
  // assets/data/treviso-united.json, which a scheduled GitHub Action
  // (.github/workflows/update-classifica.yml) keeps in sync with
  // calciotto.tv every few hours. Cache-busted on every load so visitors
  // always see the latest committed data, not a stale cached copy.
  function escapeHtml(str) {
    return String(str == null ? "" : str).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function initTrevisoData() {
    var root = document.getElementById("campionato");
    if (!root) return;

    fetch("assets/data/treviso-united.json?t=" + Date.now())
      .then(function (res) {
        if (!res.ok) throw new Error("data unavailable");
        return res.json();
      })
      .then(renderTrevisoData)
      .catch(function () {
        var lang = document.documentElement.getAttribute("lang") || "it";
        var msg = escapeHtml(I18N[lang]["campionato.error"]);
        ["campionatoMatches", "campionatoStaff"].forEach(function (id) {
          var el = document.getElementById(id);
          if (el) el.innerHTML = "<li>" + msg + "</li>";
        });
        var table = document.getElementById("campionatoTable");
        if (table) table.innerHTML = "";
        var roster = document.getElementById("campionatoRoster");
        if (roster) roster.innerHTML = "<p>" + msg + "</p>";
      });
  }

  function renderTrevisoData(data) {
    var lang = document.documentElement.getAttribute("lang") || "it";
    var locale = lang === "en" ? "en-GB" : "it-IT";

    var table = document.getElementById("campionatoTable");
    if (table && data.standings && data.standings.length) {
      var rows = data.standings.map(function (r) {
        var cls = r.is_treviso_united ? ' class="is-united"' : "";
        return "<tr" + cls + "><td>" + escapeHtml(r.pos) + "</td><td>" + escapeHtml(r.name) + "</td><td>" +
          escapeHtml(r.pts) + "</td><td>" + escapeHtml(r.played) + "</td><td>" + escapeHtml(r.wins) + "</td><td>" +
          escapeHtml(r.draws) + "</td><td>" + escapeHtml(r.losses) + "</td><td>" + escapeHtml(r.gd) + "</td></tr>";
      }).join("");
      table.innerHTML = "<thead><tr><th>#</th><th>Squadra</th><th>Pt</th><th>G</th><th>V</th><th>N</th><th>P</th><th>DR</th></tr></thead><tbody>" + rows + "</tbody>";
    }

    var roster = document.getElementById("campionatoRoster");
    if (roster) {
      if (data.players && data.players.length) {
        roster.innerHTML = data.players.map(function (p) {
          var stats = p.stats || {};
          var statLine = (stats.appearances || 0) + "PG · " + (stats.goals || 0) + "G";
          return '<div class="campionato-player"><span class="campionato-num">' + escapeHtml(p.number || "-") +
            '</span><span class="campionato-info"><span class="campionato-name">' + escapeHtml(p.name) +
            '</span><span class="campionato-pos">' + escapeHtml(p.position_label || "") +
            '</span></span><span class="campionato-stats">' + escapeHtml(statLine) + "</span></div>";
        }).join("");
      } else {
        roster.innerHTML = "";
      }
    }

    var staffList = document.getElementById("campionatoStaff");
    if (staffList) {
      var lang2 = document.documentElement.getAttribute("lang") || "it";
      if (data.staff && data.staff.length) {
        staffList.innerHTML = data.staff.map(function (s) {
          return "<li><span>" + escapeHtml(s.name) + '</span><span class="campionato-role">' + escapeHtml(s.role_label || "") + "</span></li>";
        }).join("");
      } else {
        staffList.innerHTML = "<li>" + escapeHtml(I18N[lang2]["campionato.staff.empty"]) + "</li>";
      }
    }

    var matches = document.getElementById("campionatoMatches");
    if (matches) {
      var lang3 = document.documentElement.getAttribute("lang") || "it";
      if (data.upcoming_matches && data.upcoming_matches.length) {
        matches.innerHTML = data.upcoming_matches.map(function (m) {
          var d = new Date(m.date);
          var dateStr = isNaN(d) ? "" : d.toLocaleDateString(locale, { day: "2-digit", month: "short" });
          return '<li><span>' + escapeHtml(m.opponent) + '</span><span class="campionato-date">' + escapeHtml(dateStr) + "</span></li>";
        }).join("");
      } else {
        matches.innerHTML = "<li>" + escapeHtml(I18N[lang3]["campionato.matches.empty"]) + "</li>";
      }
    }

    var updated = document.getElementById("campionatoUpdated");
    if (updated && data.generated_at) {
      var gd = new Date(data.generated_at);
      if (!isNaN(gd)) {
        updated.textContent = gd.toLocaleString(locale, { day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit" });
      }
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    initLang();
    initNavScroll();
    initMobileNav();
    initReveal();
    initJoinForm();
    initAutoScroll(document.getElementById("marqueeTrack"), ".marquee-group", "--mq-w", 76);
    initAutoScroll(document.getElementById("igTrack"), ".ig-group", "--ig-w", 20);
    initInstagramFeed();
    initVideoAutoplay();
    initTrevisoData();
  });
})();
