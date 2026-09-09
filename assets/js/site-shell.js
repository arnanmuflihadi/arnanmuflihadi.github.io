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
    document.querySelector('.cs-pager'),
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

  // The same destination must carry the same title whether reached from
  // the menu, a project card, or a contextual CTA.
  const routeLabels = Object.freeze({
    'index.html': 'Home',
    'portfolio.html': 'Work',
    'about.html': 'About',
    'news.html': 'News',
    'contact.html': 'Contact',
    'project-transit.html': 'Transit access',
    'project-pangan.html': 'Food networks',
    'project-alphaearth-food.html': 'Earth observation',
    'project-mbr.html': 'Urban morphology',
    'project-cbd.html': 'Business centres'
  });

  const classifyClick = (event, link) => {
    if (!link || !event || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return null;
    if (link.target || link.hasAttribute('download')) return null;
    const href = link.getAttribute('href');
    if (!href || href.charAt(0) === '#') return null;
    let url;
    try { url = new URL(link.href, location.href); } catch (_) { return null; }
    if (url.origin !== location.origin || url.hash || !/\.html$/i.test(url.pathname)) return null;
    if (url.pathname === location.pathname || /\/maps\//.test(url.pathname)) return null;
    const pageName = url.pathname.split('/').pop();
    return { url, label: routeLabels[pageName] || normalizeLabel(link.getAttribute('aria-label') || link.querySelector('h2, h3')?.textContent || link.textContent) };
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
    // The burger follows the nav in the document. Preserve that order so
    // native Tab traversal and the wrap-around guard use the same sequence.
    return (toggle ? controls.concat(toggle) : controls).filter((control) => control.getClientRects().length > 0);
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

  // Timing measured off pleurat.com/work's own curtain (--cover:.48s,
  // --reveal:.52s, --stagger:38ms over 8 columns); scaled down for small/
  // slow devices the same way this file already scaled the old single-wipe
  // curtain, so a full 8-column stagger doesn't feel sluggish on mobile.
  const curtainTiming = () => {
    const compact = innerWidth < 700;
    return {
      compact,
      stagger: compact ? 0.022 : 0.038,
      cover: compact ? 0.32 : 0.48,
      reveal: compact ? 0.34 : 0.52,
      labelFade: compact ? 0.22 : 0.3
    };
  };

  const clearRouteEntry = () => {
    const root = document.documentElement;
    const curtain = document.querySelector('.page-curtain');
    root.removeAttribute('data-route-entry');
    root.removeAttribute('data-route-exit');
    if (curtain) {
      curtain.style.removeProperty('pointer-events');
      curtain.querySelectorAll(':scope > span').forEach((span) => span.style.removeProperty('transform'));
      const labelWrap = curtain.querySelector('b');
      if (labelWrap) {
        labelWrap.style.removeProperty('opacity');
        labelWrap.style.removeProperty('visibility');
      }
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
    const spans = curtain.querySelectorAll(':scope > span');
    // GSAP's autoAlpha sets visibility:inherit (not visible) at alpha 1, so
    // it has to animate the visibility:hidden element itself -- the <b>
    // wrapper -- not the text-only inner span, or it just inherits hidden
    // right back from its own parent.
    const labelWrap = curtain.querySelector('b');
    const t = curtainTiming();
    window.gsap.set(curtain, { pointerEvents: 'auto' });
    window.gsap.set(spans, { yPercent: 0 });
    if (labelWrap) window.gsap.set(labelWrap, { autoAlpha: 1 });
    const revealTimeline = window.gsap.timeline({ onComplete: clearRouteEntry });
    if (labelWrap) revealTimeline.to(labelWrap, { autoAlpha: 0, duration: t.labelFade * 0.7, ease: 'power2.in' }, 0);
    // Reversed stagger (from: 'end') so the curtain opens from the edge
    // opposite the one it closed from, instead of just rewinding itself.
    revealTimeline.to(spans, {
      yPercent: -101,
      duration: t.reveal,
      ease: 'power4.inOut',
      stagger: { each: t.stagger, from: 'end' }
    }, t.labelFade * 0.35);
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

    const spans = curtain.querySelectorAll(':scope > span');
    const labelText = curtain.querySelector('[data-route-label]');
    const labelWrap = curtain.querySelector('b');
    if (labelText) labelText.textContent = transition.label;
    document.documentElement.dataset.routeExit = 'true';
    window.gsap.killTweensOf(spans);
    if (labelWrap) window.gsap.killTweensOf(labelWrap);
    window.gsap.set(curtain, { pointerEvents: 'auto' });
    window.gsap.set(spans, { yPercent: -101 });
    if (labelWrap) window.gsap.set(labelWrap, { autoAlpha: 0 });

    const t = curtainTiming();
    const wipeSpan = (spans.length - 1) * t.stagger + t.cover;
    const settleDuration = t.compact ? 0.1 : 0.16;
    const go = () => location.assign(transition.url.href);
    // A brief closed-and-settled beat before navigating -- so the
    // destination name has a moment to actually be read, rather than the
    // curtain closing and the browser leaving in the same instant.
    navigationTimer = window.setTimeout(go, (wipeSpan + settleDuration) * 1000 + 260);
    const exitTimeline = window.gsap.timeline({
      onComplete: () => {
        clearTimeout(navigationTimer);
        go();
      }
    }).to(spans, {
      yPercent: 0,
      duration: t.cover,
      ease: 'power4.inOut',
      stagger: { each: t.stagger, from: 'start' }
    }, 0);
    if (labelWrap) exitTimeline.to(labelWrap, { autoAlpha: 1, duration: t.labelFade, ease: 'power2.out' }, t.cover * 0.55);
    exitTimeline.to({}, { duration: settleDuration });
  }, true);
})();
