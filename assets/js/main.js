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

  var editorialCards = Array.prototype.slice.call(document.querySelectorAll(".editorial-portfolio .card"));
  editorialCards.forEach(function (card) {
    var num = card.querySelector(".num");
    var body = card.querySelector(".card__body");
    var title = card.querySelector("h3");
    if (num && body) body.setAttribute("data-index", num.textContent.trim());
    if (num && !card.hasAttribute("data-stack-order")) card.setAttribute("data-stack-order", num.textContent.trim());
    if (title && !card.hasAttribute("data-stack-title")) card.setAttribute("data-stack-title", title.textContent.trim());
  });
  if (editorialCards.length && "IntersectionObserver" in window) {
    var editorialObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          editorialObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    editorialCards.forEach(function (card) { editorialObserver.observe(card); });
  } else {
    editorialCards.forEach(function (card) { card.classList.add("in-view"); });
  }

  var parallaxMedia = document.querySelector("[data-parallax-media]");
  var reduceEditorialMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (editorialCards.length && !reduceEditorialMotion && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    var viewCursor = document.createElement("div");
    viewCursor.className = "card-view-cursor";
    viewCursor.setAttribute("aria-hidden", "true");
    viewCursor.innerHTML = "<span>View</span>";
    document.body.appendChild(viewCursor);
    document.body.classList.add("card-cursor-ready");

    var cursorX = -120;
    var cursorY = -120;
    var targetCursorX = -120;
    var targetCursorY = -120;
    var cursorFrame = 0;
    function animateViewCursor() {
      cursorX += (targetCursorX - cursorX) * .2;
      cursorY += (targetCursorY - cursorY) * .2;
      viewCursor.style.setProperty("--cursor-x", cursorX.toFixed(2) + "px");
      viewCursor.style.setProperty("--cursor-y", cursorY.toFixed(2) + "px");
      if (viewCursor.classList.contains("is-active") || Math.abs(targetCursorX - cursorX) > .2 || Math.abs(targetCursorY - cursorY) > .2) {
        cursorFrame = window.requestAnimationFrame(animateViewCursor);
      } else {
        cursorFrame = 0;
      }
    }
    function requestViewCursor() {
      if (!cursorFrame) cursorFrame = window.requestAnimationFrame(animateViewCursor);
    }

    editorialCards.forEach(function (card) {
      var media = card.querySelector(".card__media");
      if (!media) return;
      media.addEventListener("pointerenter", function (event) {
        targetCursorX = event.clientX;
        targetCursorY = event.clientY;
        viewCursor.classList.add("is-active");
        requestViewCursor();
      });
      media.addEventListener("pointermove", function (event) {
        targetCursorX = event.clientX;
        targetCursorY = event.clientY;
        var rect = media.getBoundingClientRect();
        var x = Math.max(-1, Math.min(1, ((event.clientX - rect.left) / rect.width - .5) * 2));
        var y = Math.max(-1, Math.min(1, ((event.clientY - rect.top) / rect.height - .5) * 2));
        card.style.setProperty("--card-media-x", (x * -12).toFixed(2) + "px");
        card.style.setProperty("--card-media-y", (y * -9).toFixed(2) + "px");
        requestViewCursor();
      });
      media.addEventListener("pointerleave", function () {
        viewCursor.classList.remove("is-active", "is-pressed");
        card.classList.remove("is-pointer-down");
        card.style.setProperty("--card-media-x", "0px");
        card.style.setProperty("--card-media-y", "0px");
      });
      media.addEventListener("pointerdown", function () {
        viewCursor.classList.add("is-pressed");
        card.classList.add("is-pointer-down");
      });
      media.addEventListener("pointerup", function () {
        viewCursor.classList.remove("is-pressed");
        card.classList.remove("is-pointer-down");
      });
    });
  }

  if (parallaxMedia && !reduceEditorialMotion) {
    var editorialTicking = false;
    var mediaX = 0;
    function updateEditorialMedia() {
      editorialTicking = false;
      var progress = Math.min(1, Math.max(0, window.scrollY / Math.max(1, window.innerHeight)));
      parallaxMedia.style.setProperty("--media-y", (-4 + progress * 8).toFixed(2) + "%");
      parallaxMedia.style.setProperty("--media-x", mediaX.toFixed(2) + "px");
    }
    function requestEditorialMedia() {
      if (!editorialTicking) {
        editorialTicking = true;
        window.requestAnimationFrame(updateEditorialMedia);
      }
    }
    parallaxMedia.addEventListener("pointermove", function (event) {
      var rect = parallaxMedia.getBoundingClientRect();
      mediaX = ((event.clientX - rect.left) / rect.width - .5) * 12;
      requestEditorialMedia();
    });
    parallaxMedia.addEventListener("pointerleave", function () {
      mediaX = 0;
      requestEditorialMedia();
    });
    window.addEventListener("scroll", requestEditorialMedia, { passive: true });
    window.addEventListener("resize", requestEditorialMedia);
    updateEditorialMedia();
  }

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

  /* ---------- Navbar: scrolled state + mobile menu ---------- */
  var nav = document.querySelector(".nav");
  if (nav) {
    var navSolid = document.body.classList.contains("nav-solid");
    var onScroll = function () { nav.classList.toggle("scrolled", navSolid || window.scrollY > 24); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    var burger = nav.querySelector(".nav__burger");
    if (burger) {
      burger.addEventListener("click", function () {
        var open = nav.classList.toggle("open");
        burger.setAttribute("aria-expanded", open ? "true" : "false");
      });
    }
    nav.querySelectorAll(".nav__links a").forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("open");
        if (burger) burger.setAttribute("aria-expanded", "false");
      });
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
    var mqDesk = window.matchMedia("(min-width: 1000px)");
    var groups = document.body.classList.contains("editorial-portfolio")
      ? [editorialCards]
      : lists.map(function (l) { return Array.prototype.slice.call(l.querySelectorAll(".card")); });
    var ticking = false;

    function clear() {
      groups.forEach(function (cards) {
        cards.forEach(function (c) {
          c.style.removeProperty("--stack-dim");
          c.classList.remove("is-stacked");
        });
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
          c.style.setProperty("--stack-dim", (Math.min(0.34, depth * 0.12)).toFixed(3));
          c.classList.toggle("is-stacked", depth > 0);
        });
      });
    }
    function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(apply); } }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    window.addEventListener("load", onScroll, { once: true });
    window.addEventListener("pageshow", onScroll);
    if (mqDesk.addEventListener) mqDesk.addEventListener("change", apply);
    apply();
    window.requestAnimationFrame(apply);
    window.setTimeout(onScroll, 180);
  }

  /* ---------- Contact form (AJAX submit with loading/success/error states) ---------- */
  var contactForm = document.querySelector("[data-contact-form]");
  if (contactForm) {
    var submitBtn = contactForm.querySelector(".contact__submit");
    var status = contactForm.querySelector("[data-contact-status]");
    var submitLabel = submitBtn ? submitBtn.innerHTML : "";
    contactForm.addEventListener("submit", function (e) {
      e.preventDefault();
      if (status) { status.textContent = ""; status.removeAttribute("data-state"); }
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "Sending…"; }
      fetch(contactForm.action, {
        method: "POST",
        body: new FormData(contactForm),
        headers: { Accept: "application/json" }
      }).then(function (res) {
        if (res.ok) {
          if (status) { status.textContent = "Message sent — thanks! I'll reply by email soon."; status.setAttribute("data-state", "success"); }
          contactForm.reset();
        } else {
          throw new Error("Form endpoint returned " + res.status);
        }
      }).catch(function (err) {
        console.error("Contact form submit failed", err);
        if (status) {
          status.innerHTML = "Something went wrong sending this. Please email me directly at <a href=\"mailto:arnanmuflihadi@gmail.com\">arnanmuflihadi@gmail.com</a> instead.";
          status.setAttribute("data-state", "error");
        }
      }).finally(function () {
        if (submitBtn) { submitBtn.disabled = false; submitBtn.innerHTML = submitLabel; }
      });
    });
  }

  /* ---------- Embedded map fallback (blank iframe -> visible message + direct link) ---------- */
  document.querySelectorAll("iframe[data-map-fallback]").forEach(function (frame) {
    var loaded = false;
    var timer = null;
    frame.addEventListener("load", function () { loaded = true; if (timer) window.clearTimeout(timer); });
    frame.addEventListener("error", showFallback);

    function armTimer() {
      // loading="lazy" iframes may sit unloaded off-screen for a while — only
      // start the "taking a while" clock once the iframe is actually in view.
      if (loaded || timer) return;
      timer = window.setTimeout(showFallback, 8000);
    }
    function showFallback() {
      if (loaded || frame.dataset.fallbackShown) return;
      frame.dataset.fallbackShown = "true";
      var note = document.createElement("div");
      note.className = "iframe-fallback";
      note.innerHTML = 'This map is taking a while to load. <a href="' + frame.src + '" target="_blank" rel="noopener">Open it directly ↗</a>';
      frame.insertAdjacentElement("afterend", note);
    }

    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) { armTimer(); io.disconnect(); }
        });
      }, { rootMargin: "200px 0px" });
      io.observe(frame);
    } else {
      armTimer();
    }
  });

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
