/* Shared shell: accessible mobile navigation and guarded document transitions. */
(() => {
  'use strict';

  const header = document.querySelector('[data-site-header]');
  const toggle = document.querySelector('[data-nav-toggle]');
  const close = document.querySelector('[data-nav-close]');
  const nav = document.querySelector('[data-site-nav]');
  const mobileQuery = matchMedia('(max-width: 699px)');
  const reducedQuery = matchMedia('(prefers-reduced-motion: reduce)');
  const background = [
    document.querySelector('.skip-link'),
    document.querySelector('.site-brand'),
    document.querySelector('main'),
    document.querySelector('.site-footer')
  ].filter(Boolean);
  const inertState = new Map();
  let menuOpen = false;
  let scrollLock = null;
  let navigationTimer = null;

  const normalizeLabel = (value) => {
    const label = String(value || '').replace(/\s+/g, ' ').trim();
    return Array.from(label).slice(0, 80).join('') || 'View page';
  };

  const classifyClick = (event, link) => {
    if (!link || !event || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return null;
    if (link.target || link.hasAttribute('download')) return null;
    const href = link.getAttribute('href');
    if (!href || href.charAt(0) === '#') return null;
    let url;
    try { url = new URL(link.href, location.href); } catch (_) { return null; }
    if (url.origin !== location.origin || url.hash || !/\.html$/i.test(url.pathname)) return null;
    if (url.pathname === location.pathname || /\/maps\//.test(url.pathname)) return null;
    return { url, label: normalizeLabel(link.getAttribute('aria-label') || link.textContent) };
  };

  window.SiteNavigationPolicy = Object.freeze({ classifyClick, normalizeLabel });

  const setInert = (element, value) => {
    if (!element) return;
    if (value) {
      if (!inertState.has(element)) inertState.set(element, {
        inert: Boolean(element.inert),
        ariaHidden: element.getAttribute('aria-hidden')
      });
      element.inert = true;
      element.setAttribute('aria-hidden', 'true');
      return;
    }
    const previous = inertState.get(element);
    if (previous) {
      element.inert = previous.inert;
      if (previous.ariaHidden == null) element.removeAttribute('aria-hidden');
      else element.setAttribute('aria-hidden', previous.ariaHidden);
      inertState.delete(element);
    } else {
      element.inert = false;
      element.removeAttribute('aria-hidden');
    }
  };

  const lockScroll = () => {
    if (scrollLock) return;
    const body = document.body;
    const root = document.documentElement;
    scrollLock = {
      y: window.scrollY,
      rootOverflow: root.style.overflow,
      bodyOverflow: body.style.overflow,
      bodyPosition: body.style.position,
      bodyTop: body.style.top,
      bodyLeft: body.style.left,
      bodyRight: body.style.right,
      bodyWidth: body.style.width,
      bodyOverscroll: body.style.overscrollBehavior
    };
    root.dataset.menuLocked = 'true';
    root.style.overflow = 'hidden';
    body.style.overflow = 'hidden';
    body.style.position = 'fixed';
    body.style.top = `-${scrollLock.y}px`;
    body.style.left = '0';
    body.style.right = '0';
    body.style.width = '100%';
    body.style.overscrollBehavior = 'none';
  };

  const unlockScroll = () => {
    if (!scrollLock) return;
    const body = document.body;
    const root = document.documentElement;
    const state = scrollLock;
    scrollLock = null;
    root.removeAttribute('data-menu-locked');
    root.style.overflow = state.rootOverflow;
    body.style.overflow = state.bodyOverflow;
    body.style.position = state.bodyPosition;
    body.style.top = state.bodyTop;
    body.style.left = state.bodyLeft;
    body.style.right = state.bodyRight;
    body.style.width = state.bodyWidth;
    body.style.overscrollBehavior = state.bodyOverscroll;
    window.scrollTo(0, state.y);
  };

  const menuFocusable = () => {
    if (!nav) return toggle ? [toggle] : [];
    const controls = Array.from(nav.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'));
    return toggle ? [toggle].concat(controls) : controls;
  };

  const applyMenuState = (open, options = {}) => {
    const isMobile = mobileQuery.matches;
    menuOpen = Boolean(open && isMobile && nav && header && toggle);
    if (!header || !toggle || !nav) return;
    header.dataset.menuOpen = String(menuOpen);
    toggle.setAttribute('aria-expanded', String(menuOpen));
    toggle.setAttribute('aria-label', menuOpen ? 'Close menu' : 'Open menu');

    if (!isMobile) {
      nav.inert = false;
      background.forEach((element) => setInert(element, false));
      unlockScroll();
      return;
    }

    nav.inert = !menuOpen;
    background.forEach((element) => setInert(element, menuOpen));
    if (menuOpen) {
      lockScroll();
      if (options.focus !== false) {
        requestAnimationFrame(() => nav.querySelector('a[href], button:not([disabled])')?.focus({ preventScroll: true }));
      }
    } else {
      unlockScroll();
      if (options.restoreFocus) toggle.focus({ preventScroll: true });
    }
  };

  const closeMenu = (options = {}) => applyMenuState(false, { restoreFocus: options.restoreFocus !== false, focus: false });
  const openMenu = () => applyMenuState(true);

  toggle?.addEventListener('click', () => menuOpen ? closeMenu() : openMenu());
  close?.addEventListener('click', () => closeMenu());
  nav?.addEventListener('click', (event) => {
    if (event.target === nav) {
      closeMenu();
      return;
    }
    const link = event.target.closest('a');
    if (!link || !menuOpen) return;
    const transition = classifyClick(event, link);
    closeMenu({ restoreFocus: !transition });
  }, true);

  document.addEventListener('keydown', (event) => {
    if (!menuOpen) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      closeMenu();
      return;
    }
    if (event.key !== 'Tab') return;
    const controls = menuFocusable();
    if (!controls.length) return;
    const active = document.activeElement;
    const index = controls.indexOf(active);
    if (event.shiftKey && (index <= 0 || active === document.body)) {
      event.preventDefault();
      controls[controls.length - 1].focus();
    } else if (!event.shiftKey && (index === -1 || index === controls.length - 1)) {
      event.preventDefault();
      controls[0].focus();
    }
  });

  const onViewportChange = () => applyMenuState(false, { restoreFocus: false, focus: false });
  if (mobileQuery.addEventListener) mobileQuery.addEventListener('change', onViewportChange);
  else mobileQuery.addListener(onViewportChange);
  addEventListener('pagehide', () => closeMenu({ restoreFocus: false }));
  addEventListener('pageshow', () => closeMenu({ restoreFocus: false }));
  applyMenuState(false, { restoreFocus: false, focus: false });

  const clearRouteEntry = () => {
    const root = document.documentElement;
    const curtain = document.querySelector('.page-curtain');
    root.removeAttribute('data-route-entry');
    root.removeAttribute('data-route-exit');
    if (curtain) {
      curtain.style.removeProperty('transform');
      curtain.style.removeProperty('pointer-events');
    }
    window.PortfolioRouteTransition?.clear?.();
  };

  const revealRouteEntry = () => {
    if (!document.documentElement.hasAttribute('data-route-entry')) return;
    const curtain = document.querySelector('.page-curtain');
    if (!curtain) return clearRouteEntry();
    if (reducedQuery.matches || !window.gsap) {
      requestAnimationFrame(clearRouteEntry);
      return;
    }
    window.gsap.set(curtain, { yPercent: 0, pointerEvents: 'auto' });
    window.gsap.to(curtain, {
      yPercent: -101,
      duration: innerWidth < 700 ? 0.14 : 0.2,
      ease: 'power2.out',
      onComplete: clearRouteEntry
    });
  };

  revealRouteEntry();

  document.addEventListener('click', (event) => {
    const link = event.target.closest('a');
    const transition = classifyClick(event, link);
    if (!transition || reducedQuery.matches || !window.gsap) return;
    const curtain = document.querySelector('.page-curtain');
    if (!curtain || document.documentElement.hasAttribute('data-route-exit')) return;

    event.preventDefault();
    closeMenu({ restoreFocus: false });
    try {
      sessionStorage.setItem('portfolio:route-transition', JSON.stringify({
        targetPath: transition.url.pathname,
        createdAt: Date.now(),
        destinationLabel: transition.label
      }));
    } catch (_) {
      location.assign(transition.url.href);
      return;
    }

    const label = curtain.querySelector('[data-route-label]');
    if (label) label.textContent = transition.label;
    document.documentElement.dataset.routeExit = 'true';
    window.gsap.killTweensOf(curtain);
    if (label) window.gsap.killTweensOf(label);
    window.gsap.set(curtain, { yPercent: -101, pointerEvents: 'auto' });
    if (label) window.gsap.set(label, { autoAlpha: 0 });
    const compact = innerWidth < 700;
    const closeDuration = compact ? 0.18 : 0.3;
    const labelDuration = compact ? 0.16 : 0.22;
    const settleDuration = compact ? 0.08 : 0.12;
    const go = () => location.assign(transition.url.href);
    // A brief closed-and-settled beat before navigating -- so the
    // destination name has a moment to actually be read, rather than the
    // curtain closing and the browser leaving in the same instant.
    navigationTimer = window.setTimeout(go, (closeDuration + labelDuration + settleDuration) * 1000 + 260);
    const exitTimeline = window.gsap.timeline({
      onComplete: () => {
        clearTimeout(navigationTimer);
        go();
      }
    }).to(curtain, { yPercent: 0, duration: closeDuration, ease: 'power2.inOut' });
    if (label) exitTimeline.to(label, { autoAlpha: 1, duration: labelDuration, ease: 'power2.out' });
    exitTimeline.to({}, { duration: settleDuration });
  }, true);
})();
