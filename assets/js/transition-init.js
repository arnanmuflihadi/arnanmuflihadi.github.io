(function () {
  'use strict';
  if (window.__portfolioTransitionInit) return;
  window.__portfolioTransitionInit = true;
  var root = document.documentElement;
  var curtain = document.querySelector('.page-curtain');
  var label = curtain && curtain.querySelector('[data-route-label]');
  var key = 'portfolio:route-transition';
  var cleanupTimer = null;

  root.classList.add('js');

  function clear() {
    if (cleanupTimer) window.clearTimeout(cleanupTimer);
    cleanupTimer = null;
    root.removeAttribute('data-route-entry');
    root.removeAttribute('data-route-exit');
    if (curtain) {
      curtain.style.removeProperty('transform');
      curtain.style.removeProperty('pointer-events');
    }
    try { sessionStorage.removeItem(key); } catch (_) {}
  }

  window.PortfolioRouteTransition = { clear: clear };

  if (!curtain || matchMedia('(prefers-reduced-motion: reduce)').matches) {
    clear();
  } else {
    var candidate = null;
    try { candidate = JSON.parse(sessionStorage.getItem(key) || 'null'); } catch (_) {}
    try { sessionStorage.removeItem(key); } catch (_) {}
    var age = candidate && Number(candidate.createdAt);
    var labelText = candidate && typeof candidate.destinationLabel === 'string'
      ? Array.from(candidate.destinationLabel.replace(/\s+/g, ' ').trim()).slice(0, 80).join('')
      : '';
    var valid = candidate && candidate.targetPath === location.pathname &&
      Number.isFinite(age) && age >= 0 && (Date.now() - age) >= 0 && (Date.now() - age) <= 2000 &&
      Boolean(labelText);
    if (valid) {
      if (label) label.textContent = labelText;
      root.setAttribute('data-route-entry', 'true');
      // Failsafe only -- site-shell.js's GSAP timeline normally calls
      // clear() itself via onComplete. Worst case for the 8-column
      // reversed-stagger reveal is ~0.89s (7 * 38ms stagger + .52s reveal,
      // plus the label pre-fade offset), so this must clear comfortably
      // after that or it can yank the curtain mid-animation.
      cleanupTimer = window.setTimeout(clear, 1400);
    } else {
      clear();
    }
  }

  // A normal pageshow belongs to this newly loaded route and must preserve the
  // entry curtain until its 800 ms cleanup timer finishes. Only a bfcache
  // restoration can retain stale transition state, so clear in that case.
  window.addEventListener('pageshow', function (event) {
    if (event.persisted) clear();
  });
}());
