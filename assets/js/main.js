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
  });
})();
