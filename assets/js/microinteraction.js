/*
  Shared micro-interactions
  -------------------------
  - Case-study reading progress bar and section dots.
  - Inline term definitions via data-term-definition.
  - Pointer-aware card highlight for the portfolio overview.
*/
(function () {
  "use strict";

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function slug(value, fallback) {
    var id = String(value || "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "");
    return id || fallback;
  }

  function initReadingProgress() {
    if (!document.querySelector(".cs-hero")) return;

    var bar = document.createElement("div");
    bar.className = "read-progress";
    bar.setAttribute("aria-hidden", "true");
    bar.innerHTML = "<span></span>";
    document.body.appendChild(bar);

    var fill = bar.querySelector("span");
    var ticking = false;

    function update() {
      ticking = false;
      var max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
      var pct = Math.min(1, Math.max(0, window.scrollY / max));
      fill.style.transform = "scaleX(" + pct.toFixed(4) + ")";
    }

    function requestUpdate() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }

    update();
    window.addEventListener("scroll", requestUpdate, { passive: true });
    window.addEventListener("resize", requestUpdate);
  }

  function initSectionRail() {
    var sections = Array.prototype.slice.call(document.querySelectorAll("main .cs-section"));
    if (sections.length < 3) return;

    var nav = document.createElement("nav");
    nav.className = "case-progress";
    nav.setAttribute("aria-label", "Case study sections");

    sections.forEach(function (section, index) {
      var heading = section.querySelector("h2");
      var idx = section.querySelector(".idx");
      var title = heading ? heading.textContent.trim() : "Section " + (index + 1);
      if (!section.id) section.id = slug(title, "case-section-" + (index + 1));

      var link = document.createElement("a");
      link.href = "#" + section.id;
      link.innerHTML = '<span aria-hidden="true"></span><em>' + title + "</em>";
      link.setAttribute("aria-label", "Jump to " + (idx ? idx.textContent.trim() + ": " : "") + title);
      nav.appendChild(link);
    });

    document.body.appendChild(nav);
    var links = Array.prototype.slice.call(nav.querySelectorAll("a"));

    function activate(section) {
      links.forEach(function (link) {
        var active = link.getAttribute("href") === "#" + section.id;
        link.classList.toggle("is-active", active);
        if (active) link.setAttribute("aria-current", "step");
        else link.removeAttribute("aria-current");
      });
    }

    activate(sections[0]);

    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) activate(entry.target);
        });
      }, { threshold: 0.01, rootMargin: "-42% 0px -48% 0px" });
      sections.forEach(function (section) { observer.observe(section); });
    }
  }

  function initTermTooltips() {
    var terms = Array.prototype.slice.call(document.querySelectorAll("[data-term-definition]"));
    if (!terms.length) return;

    var tip = document.createElement("div");
    tip.className = "term-popover";
    tip.setAttribute("role", "tooltip");
    tip.hidden = true;
    document.body.appendChild(tip);

    var active = null;
    var closeTimer = null;

    function positionTerm(term) {
      var rect = term.getBoundingClientRect();
      var pad = 14;
      var width = Math.min(320, window.innerWidth - pad * 2);
      tip.style.maxWidth = width + "px";
      tip.hidden = false;
      var tipRect = tip.getBoundingClientRect();
      var left = Math.min(window.innerWidth - tipRect.width - pad, Math.max(pad, rect.left + rect.width / 2 - tipRect.width / 2));
      var top = rect.top - tipRect.height - 12;
      if (top < pad) top = rect.bottom + 12;
      tip.style.left = left + "px";
      tip.style.top = top + "px";
    }

    function show(term) {
      window.clearTimeout(closeTimer);
      if (active && active !== term) active.setAttribute("aria-expanded", "false");
      active = term;
      tip.textContent = "";
      var title = document.createElement("strong");
      title.textContent = term.getAttribute("data-term") || term.textContent.trim();
      var body = document.createElement("span");
      body.textContent = term.getAttribute("data-term-definition") || "";
      tip.appendChild(title);
      tip.appendChild(document.createTextNode(" "));
      tip.appendChild(body);
      tip.setAttribute("aria-label", title.textContent + ". " + body.textContent);
      term.setAttribute("aria-expanded", "true");
      positionTerm(term);
    }

    function hideSoon(delay) {
      window.clearTimeout(closeTimer);
      closeTimer = window.setTimeout(function () {
        if (active) active.setAttribute("aria-expanded", "false");
        active = null;
        tip.hidden = true;
      }, delay == null ? 90 : delay);
    }

    terms.forEach(function (term, index) {
      if (!term.id) term.id = "term-tip-" + index;
      term.classList.add("term-tip");
      term.setAttribute("role", "button");
      term.setAttribute("tabindex", "0");
      term.setAttribute("aria-expanded", "false");

      term.addEventListener("mouseenter", function () { show(term); });
      term.addEventListener("mouseleave", function () { hideSoon(110); });
      term.addEventListener("focus", function () { show(term); });
      term.addEventListener("blur", function () { hideSoon(70); });
      term.addEventListener("click", function (event) {
        event.preventDefault();
        if (active === term && !tip.hidden) hideSoon(0);
        else show(term);
      });
      term.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          show(term);
        }
      });
    });

    tip.addEventListener("mouseenter", function () { window.clearTimeout(closeTimer); });
    tip.addEventListener("mouseleave", function () { hideSoon(80); });
    window.addEventListener("scroll", function () {
      if (active && !tip.hidden) positionTerm(active);
    }, { passive: true });
    window.addEventListener("resize", function () {
      if (active && !tip.hidden) positionTerm(active);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && active) hideSoon(0);
    });
  }

  function initCardHighlights() {
    if (reduceMotion) return;
    document.querySelectorAll(".card").forEach(function (card) {
      card.addEventListener("pointermove", function (event) {
        var rect = card.getBoundingClientRect();
        card.style.setProperty("--mx", (((event.clientX - rect.left) / rect.width) * 100).toFixed(2) + "%");
        card.style.setProperty("--my", (((event.clientY - rect.top) / rect.height) * 100).toFixed(2) + "%");
      });
      card.addEventListener("pointerleave", function () {
        card.style.removeProperty("--mx");
        card.style.removeProperty("--my");
      });
    });
  }

  function init() {
    initReadingProgress();
    initSectionRail();
    initTermTooltips();
    initCardHighlights();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
