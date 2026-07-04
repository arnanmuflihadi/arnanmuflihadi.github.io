/* ============================================================
   Portfolio interactions — vanilla JS, no dependencies
   ============================================================ */
(function () {
  "use strict";

  /* ---------- Theme (light/dark, persisted) ---------- */
  var root = document.documentElement;
  var stored = localStorage.getItem("theme");
  if (stored) {
    root.setAttribute("data-theme", stored);
  } else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    root.setAttribute("data-theme", "dark");
  }
  function toggleTheme() {
    var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  }
  document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", toggleTheme);
  });

  /* ---------- Navbar: scrolled state + mobile menu ---------- */
  var nav = document.querySelector(".nav");
  if (nav) {
    var navSolid = document.body.classList.contains("nav-solid");
    var onScroll = function () { nav.classList.toggle("scrolled", navSolid || window.scrollY > 24); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    var burger = nav.querySelector(".nav__burger");
    if (burger) burger.addEventListener("click", function () { nav.classList.toggle("open"); });
    nav.querySelectorAll(".nav__links a").forEach(function (a) {
      a.addEventListener("click", function () { nav.classList.remove("open"); });
    });
  }

  /* ---------- Current year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (e) {
    e.textContent = new Date().getFullYear();
  });

  /* ---------- Scroll reveal ---------- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Lightbox for figures ---------- */
  var lb = document.createElement("div");
  lb.className = "lb";
  lb.innerHTML =
    '<button class="lb__close" aria-label="Close"><span class="ms">close</span></button>' +
    '<img alt="">' +
    '<div class="lb__cap"></div>';
  document.body.appendChild(lb);
  var lbImg = lb.querySelector("img");
  var lbCap = lb.querySelector(".lb__cap");

  var lbTrigger = null;
  function openLB(src, cap) {
    lbImg.src = src;
    lbImg.alt = cap || "";
    lbCap.textContent = cap || "";
    lb.classList.add("open");
    document.body.style.overflow = "hidden";
    lb.querySelector(".lb__close").focus();
  }
  function closeLB() {
    lb.classList.remove("open");
    document.body.style.overflow = "";
    if (lbTrigger) { lbTrigger.focus(); lbTrigger = null; }
  }

  document.querySelectorAll("[data-zoom]").forEach(function (frame) {
    var img = frame.querySelector("img");
    if (!img) return;
    var cap = frame.getAttribute("data-cap") || img.getAttribute("alt") || "";
    frame.setAttribute("tabindex", "0");
    frame.setAttribute("role", "button");
    frame.setAttribute("aria-label", "Enlarge figure: " + cap);
    function trigger() {
      lbTrigger = frame;
      openLB(img.currentSrc || img.src, cap);
    }
    frame.addEventListener("click", trigger);
    frame.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); trigger(); }
    });
  });
  lb.addEventListener("click", function (e) {
    if (e.target === lb || e.target.classList.contains("lb__close")) closeLB();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && lb.classList.contains("open")) closeLB();
  });

  /* ---------- Stacked-card depth (Selected Work) ---------- */
  var lists = Array.prototype.slice.call(document.querySelectorAll(".work__list"));
  if (lists.length && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var mqDesk = window.matchMedia("(min-width: 760px)");
    var groups = lists.map(function (l) { return Array.prototype.slice.call(l.querySelectorAll(".card")); });
    var ticking = false;

    function clear() {
      groups.forEach(function (cards) {
        cards.forEach(function (c) { c.style.removeProperty("--cs"); c.style.removeProperty("--co"); });
      });
    }
    function apply() {
      ticking = false;
      if (!mqDesk.matches) { clear(); return; }
      groups.forEach(function (cards) {
        // which cards are currently pinned (stacked)?
        var pinned = cards.map(function (c) {
          var top = parseFloat(getComputedStyle(c).top) || 0;
          return c.getBoundingClientRect().top <= top + 1.5;
        });
        cards.forEach(function (c, i) {
          var depth = 0;
          for (var j = i + 1; j < cards.length; j++) { if (pinned[j]) depth++; }
          c.style.setProperty("--cs", (Math.max(0.88, 1 - depth * 0.04)).toFixed(3));
          c.style.setProperty("--co", (Math.max(0.5, 1 - depth * 0.16)).toFixed(3));
        });
      });
    }
    function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(apply); } }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    if (mqDesk.addEventListener) mqDesk.addEventListener("change", apply);
    apply();
  }

  /* ---------- Scrollytelling (pinned stat panel + stepped findings) ---------- */
  document.querySelectorAll("[data-scrolly]").forEach(function (root) {
    var visual = root.querySelector("[data-scrolly-visual]");
    var numEl = visual.querySelector(".scrolly__num");
    var labelEl = visual.querySelector(".scrolly__label");
    var steps = Array.prototype.slice.call(root.querySelectorAll(".scrolly__step"));
    if (!visual || !numEl || !labelEl || !steps.length) return;

    var progress = document.createElement("div");
    progress.className = "scrolly__progress";
    steps.forEach(function () { progress.appendChild(document.createElement("span")); });
    visual.appendChild(progress);
    var dots = Array.prototype.slice.call(progress.children);
    if (dots[0]) dots[0].classList.add("is-active");

    var current = 0;
    function activate(index) {
      if (index === current || index < 0) return;
      current = index;
      steps.forEach(function (s, i) { s.classList.toggle("is-active", i === index); });
      dots.forEach(function (d, i) { d.classList.toggle("is-active", i === index); });
      visual.classList.add("is-swapping");
      window.setTimeout(function () {
        numEl.textContent = steps[index].getAttribute("data-num");
        labelEl.textContent = steps[index].getAttribute("data-label");
        visual.classList.remove("is-swapping");
      }, 160);
    }

    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (en) {
            if (en.isIntersecting) activate(steps.indexOf(en.target));
          });
        },
        { threshold: 0, rootMargin: "-35% 0px -35% 0px" }
      );
      steps.forEach(function (s) { io.observe(s); });
    }
  });
})();
