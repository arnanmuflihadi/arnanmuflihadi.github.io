/* ============================================================
   Portfolio interactions — vanilla JS, no dependencies
   ============================================================ */
(function () {
  "use strict";

  /* ---------- Editorial entrance + motion system ---------- */
  window.requestAnimationFrame(function () {
    window.requestAnimationFrame(function () {
      document.documentElement.classList.add("is-ready");
    });
  });

  /* ---------- Theme (light/dark, persisted) ---------- */
  /* data-theme itself is already set pre-paint by theme-init.js; this just
     wires up the toggle button and its aria state. */
  var root = document.documentElement;
  function toggleTheme() {
    var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
    syncThemeControls();
  }
  function syncThemeControls() {
    var dark = root.getAttribute("data-theme") === "dark";
    document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
      button.setAttribute("aria-pressed", dark ? "true" : "false");
      button.setAttribute("aria-label", dark ? "Use light mode" : "Use dark mode");
      button.setAttribute("title", dark ? "Use light mode" : "Use dark mode");
    });
  }
  document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", toggleTheme);
  });
  syncThemeControls();

  /* ---------- Current year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (e) {
    e.textContent = new Date().getFullYear();
  });

  /* ---------- Page-local ambient motion preference ---------- */
  var ambientToggle = document.querySelector("[data-ambient-toggle]");
  if (ambientToggle && window.matchMedia) {
    var ambientQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    var ambientEnabled = !ambientQuery.matches;
    function renderAmbientToggle() {
      var effective = ambientEnabled && !ambientQuery.matches;
      ambientToggle.disabled = ambientQuery.matches;
      ambientToggle.setAttribute("aria-pressed", effective ? "true" : "false");
      ambientToggle.innerHTML = "Ambient motion <span>" + (ambientQuery.matches ? "Reduced" : (ambientEnabled ? "On" : "Paused")) + "</span>";
      ambientToggle.dispatchEvent(new CustomEvent("ambient:change", {
        bubbles: true,
        detail: { enabled: effective }
      }));
    }
    ambientToggle.addEventListener("click", function () {
      if (ambientQuery.matches) return;
      ambientEnabled = !ambientEnabled;
      renderAmbientToggle();
    });
    if (ambientQuery.addEventListener) ambientQuery.addEventListener("change", renderAmbientToggle);
    else if (ambientQuery.addListener) ambientQuery.addListener(renderAmbientToggle);
    renderAmbientToggle();
  }

  /* ---------- Accessible lightbox for figures ---------- */
  var zoomFrames = Array.prototype.slice.call(document.querySelectorAll("[data-zoom]")).filter(function (frame) {
    return !!frame.querySelector("img");
  });
  if (zoomFrames.length) {
    var lb = document.createElement("div");
    lb.className = "lb";
    lb.hidden = true;
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-labelledby", "lb-title");
    lb.innerHTML =
      '<h2 class="lb__title" id="lb-title">Figure preview</h2>' +
      '<button class="lb__close" type="button" aria-label="Close figure preview"><span class="ms" aria-hidden="true">close</span></button>' +
      '<img alt="">' +
      '<div class="lb__cap"></div>';
    document.body.appendChild(lb);
    var lbImg = lb.querySelector("img");
    var lbCap = lb.querySelector(".lb__cap");
    var lbClose = lb.querySelector(".lb__close");
    var lbTrigger = null;
    var bodyOverflow = "";
    var closeTimer = null;

    function openLB(src, cap, trigger) {
      if (closeTimer) { window.clearTimeout(closeTimer); closeTimer = null; }
      lbTrigger = trigger;
      lbImg.src = src;
      lbImg.alt = cap || "";
      lbCap.textContent = cap || "";
      lb.hidden = false;
      lb.removeAttribute("aria-hidden");
      bodyOverflow = document.body.style.overflow;
      document.body.style.overflow = "hidden";
      trigger.setAttribute("aria-expanded", "true");
      window.requestAnimationFrame(function () {
        lb.classList.add("open");
        lbClose.focus();
      });
    }

    function closeLB() {
      if (lb.hidden) return;
      var returnTo = lbTrigger;
      lb.classList.remove("open");
      lb.setAttribute("aria-hidden", "true");
      document.body.style.overflow = bodyOverflow;
      if (returnTo) {
        returnTo.setAttribute("aria-expanded", "false");
        if (returnTo.isConnected) returnTo.focus();
      }
      lbTrigger = null;
      closeTimer = window.setTimeout(function () {
        if (!lb.classList.contains("open")) {
          lb.hidden = true;
          lbImg.removeAttribute("src");
          lbImg.alt = "";
        }
      }, 400);
    }

    zoomFrames.forEach(function (frame) {
      var img = frame.querySelector("img");
      var cap = frame.getAttribute("data-cap") || img.getAttribute("alt") || "";
      frame.setAttribute("tabindex", "0");
      frame.setAttribute("role", "button");
      frame.setAttribute("aria-haspopup", "dialog");
      frame.setAttribute("aria-expanded", "false");
      frame.setAttribute("aria-label", "Enlarge figure: " + cap);
      function trigger() { openLB(img.currentSrc || img.src, cap, frame); }
      frame.addEventListener("click", trigger);
      frame.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); trigger(); }
      });
    });

    lb.addEventListener("click", function (e) {
      if (e.target === lb || e.target.closest(".lb__close")) closeLB();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && lb.classList.contains("open")) { e.preventDefault(); closeLB(); }
      if (e.key === "Tab" && lb.classList.contains("open")) {
        e.preventDefault();
        lbClose.focus();
      }
    });
  }

})();
