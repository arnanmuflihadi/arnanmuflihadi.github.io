/* Shared motion lifecycle: GSAP/ScrollTrigger own presentational scroll state. */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  // Order is NOT the source filenames' numbering: these six frames are
  // independent illustration variants, not a rotoscoped cycle, so playing
  // them 01->06 jumps the stride width around non-monotonically (measured
  // silhouette widths: 390,340,197,314,413,213px) and reads as a leg twitch.
  // Sorted by measured stride width (narrowest/legs-crossed to widest/full
  // stride), the ping-pong below opens and closes the stride smoothly.
  const walkFrames = ['03', '06', '04', '02', '01', '05'];
  // Real strides pause briefly at full contact (weight transfer) and snap
  // quickly through the crossed-leg passing position -- holding every
  // frame for an equal beat is what makes a walk cycle read as mechanical.
  // 03 is the narrowest/passing pose, 05 the widest/contact pose (see
  // widths above), so the sequence's two ends get the beat weighted.
  const walkFrameBeats = { '03': 0.7, '06': 1, '04': 1, '02': 1, '01': 1, '05': 1.5 };
  const walkFrameSource = (frame) => `assets/img/redesign/analyst-walk-${frame}.webp`;
  const walkIdleSource = 'assets/img/redesign/analyst-walk-01-idle.webp';
  let ctx = null;
  let lenis = null;
  let ticker = null;
  let resizeTimer = null;
  let refreshTimer = null;
  let ambientEntries = [];
  let cleanup = [];
  let userAmbientEnabled = true;
  let welcomeTimeline = null;

  const desktop = () => innerWidth >= 1100 && matchMedia('(hover: hover) and (pointer: fine)').matches;
  const compact = () => innerWidth >= 700 && innerWidth < 1100;
  const eligible = () => !reduced.matches
    && !(navigator.connection && navigator.connection.saveData)
    && Boolean(window.gsap && window.ScrollTrigger);
  const on = (target, type, listener, options) => {
    target.addEventListener(type, listener, options);
    cleanup.push(() => target.removeEventListener(type, listener, options));
  };

  function createWelcomeIntro() {
    const root = document.documentElement;
    const intro = document.querySelector('[data-welcome-intro]');
    if (!intro || !root.classList.contains('welcome-intro-pending')) return;

    const finish = () => {
      root.classList.remove('welcome-intro-pending');
      intro.hidden = true;
      clearTimeout(window.__welcomeFailSafe);
      document.removeEventListener('keydown', onKeydown);
    };
    const onKeydown = (event) => {
      if (event.key !== 'Escape') return;
      welcomeTimeline?.progress(1);
      finish();
    };

    try { sessionStorage.setItem('portfolio:welcome-seen', 'true'); } catch (_) {}
    if (reduced.matches || !window.gsap) {
      finish();
      return;
    }

    const word = intro.querySelector('[data-welcome-word]');
    const note = intro.querySelector('[data-welcome-note]');
    const track = intro.querySelector('[data-welcome-track-fill]');
    const panels = Array.from(intro.querySelectorAll('.welcome-intro__panels span'));
    // Overlapped rather than chained: pleurat starts nearly everything on one
    // shared trigger with only a small intra-element stagger, and its result
    // reads faster than its own total duration would suggest. Running the
    // track fill alongside the note instead of after it, and pulling the
    // panel-lift earlier (0.5x instead of 0.62x), gets the same effect here.
    const duration = innerWidth < 700 ? 0.68 : 0.95;
    document.addEventListener('keydown', onKeydown);
    window.gsap.set(intro, { autoAlpha: 1 });
    window.gsap.set([word, note], { autoAlpha: 0, y: 16 });
    window.gsap.set(panels, { yPercent: 0 });
    if (track) window.gsap.set(track, { scaleX: 0 });
    welcomeTimeline = window.gsap.timeline({ defaults: { ease: 'power3.out' }, onComplete: finish })
      .to(word, { autoAlpha: 1, y: 0, duration: duration * 0.32 }, 0.05)
      .to(note, { autoAlpha: 1, y: 0, duration: duration * 0.24 }, duration * 0.16)
      .to(track, { scaleX: 1, duration: duration * 0.5, ease: 'power1.inOut' }, duration * 0.16)
      .to(panels, { yPercent: -104, duration: duration * 0.42, stagger: 0.06, ease: 'power2.inOut' }, duration * 0.5)
      .to(intro, { autoAlpha: 0, duration: 0.1, ease: 'none' }, duration * 0.92);
  }

  function resetHeroStatic() {
    const walker = document.querySelector('[data-hero-walker]');
    const sprite = document.querySelector('.analyst-sprite');
    if (!walker) return;
    walker.style.removeProperty('transform');
    walker.style.removeProperty('will-change');
    walker.style.removeProperty('left');
    if (sprite) {
      sprite.src = walkIdleSource;
      sprite.dataset.frame = walkFrames[0];
      sprite.style.removeProperty('transform');
      sprite.style.removeProperty('will-change');
    }
  }

  function resetAmbientToggle() {
    const button = document.querySelector('[data-ambient-toggle]');
    if (!button) return;
    if (reduced.matches) {
      button.disabled = true;
      button.setAttribute('aria-pressed', 'false');
      button.innerHTML = 'Ambient motion <span>Reduced</span>';
      return;
    }
    button.disabled = false;
    button.setAttribute('aria-pressed', userAmbientEnabled ? 'true' : 'false');
    button.innerHTML = `Ambient motion <span>${userAmbientEnabled ? 'On' : 'Paused'}</span>`;
  }

  function ambientAllowed() {
    return userAmbientEnabled && !reduced.matches && !document.hidden;
  }

  function updateAmbientPlayback() {
    ambientEntries.forEach((entry) => {
      const shouldPlay = ambientAllowed() && entry.inView;
      entry.items.forEach((item) => shouldPlay ? item.play() : item.pause());
    });
  }

  function registerAmbient(items, trigger, ScrollTrigger) {
    const entry = { items, inView: false };
    ambientEntries.push(entry);
    ScrollTrigger.create({
      trigger,
      start: 'top bottom',
      end: 'bottom top',
      onEnter: () => { entry.inView = true; updateAmbientPlayback(); },
      onEnterBack: () => { entry.inView = true; updateAmbientPlayback(); },
      onLeave: () => { entry.inView = false; updateAmbientPlayback(); },
      onLeaveBack: () => { entry.inView = false; updateAmbientPlayback(); }
    });
    const rect = trigger.getBoundingClientRect();
    entry.inView = rect.bottom > 0 && rect.top < innerHeight;
    return entry;
  }

  function createHeroMotion(gsap, ScrollTrigger, hero, media) {
    const walker = media.querySelector('[data-hero-walker]');
    const sprite = media.querySelector('.analyst-sprite');
    const route = media.querySelector('.hero-route__line');
    const routeProgress = media.querySelector('[data-hero-route-progress]');
    const stops = gsap.utils.toArray('[data-hero-route-stop]');
    const copy = hero.querySelector('.spatial-hero__copy');
    const skylineBack = media.querySelector('[data-parallax="back"]');
    const skylineMid = media.querySelector('[data-parallax="mid"]');
    const skylineFront = media.querySelector('[data-parallax="front"]');
    if (!walker || !sprite) return;

    const isDesktop = desktop();
    const isCompact = compact();
    const repeats = isDesktop ? -1 : 1;
    const journeyEnd = isDesktop ? '82%' : (isCompact ? '68%' : '52%');
    const journeyDuration = isDesktop ? 15 : (isCompact ? 11 : 8);
    const frameDuration = isDesktop ? 0.1 : 0.13;
    let travellingRight = true;
    const motions = [];

    // Travel belongs to the wrapper (positioned via CSS `left`, relative to
    // the full strip width); the illustrated sprite keeps a stable baseline
    // and only swaps frame / flips to face the actual yoyo direction.
    gsap.set(walker, { willChange: 'transform' });
    gsap.set(sprite, { scaleX: 1, transformOrigin: '50% 100%', willChange: 'transform' });
    gsap.set(stops, { scale: 1 });
    if (route) gsap.set(route, { autoAlpha: 0.3 });
    // SVG pathLength is unitless; use attributes instead of CSS pixel values
    // so the active route segment genuinely draws and reverses with travel.
    if (routeProgress) gsap.set(routeProgress, { attr: { 'stroke-dasharray': 1, 'stroke-dashoffset': 1 }, autoAlpha: 0.8 });

    // One-time arrival: the scene builds in layer by layer instead of
    // appearing fully formed, so the welcome curtain lifts on something
    // already coming to life rather than a static hero frame.
    const skylineLayers = [skylineBack, skylineMid, skylineFront].filter(Boolean);
    if (skylineLayers.length) {
      gsap.set(skylineLayers, { autoAlpha: 0, y: 14 });
      gsap.set(walker, { autoAlpha: 0 });
      gsap.timeline({ defaults: { ease: 'power3.out' }, delay: 0.15 })
        .to(skylineLayers, { autoAlpha: 1, y: 0, duration: 1.0, stagger: 0.1 }, 0)
        .to(walker, { autoAlpha: 1, duration: 0.55 }, 0.45);
    }

    // Walk cycle: the illustrated frame sequence, preloaded before it is
    // ever added to the ambient rotation so the first swap never pops in.
    // Ping-ponging (1->6 then 6->1, via yoyo) instead of hard-restarting at
    // frame 6 removes the jump-cut every loop -- the sequence always ends
    // exactly where it began, by construction, with no art dependency.
    // Frames swap at a fixed rate, and the walker's own travel below is
    // linear rather than eased for the same reason: an eased "slow down,
    // speed up" pace next to a constant leg cadence is what reads as feet
    // sliding on the ground instead of a real stride.
    const walk = gsap.timeline({ paused: true, repeat: -1, yoyo: true });
    walkFrames.forEach((frame) => {
      walk.call(() => {
        sprite.src = walkFrameSource(frame);
        sprite.dataset.frame = frame;
      }).to({}, { duration: frameDuration * (walkFrameBeats[frame] || 1) });
    });
    // A small per-step bob sells the weight of each stride without needing
    // more art frames -- two bounces per ping-pong lap, roughly one per foot.
    const bob = gsap.to(sprite, {
      y: -3,
      duration: frameDuration * 3,
      ease: 'sine.inOut',
      paused: true,
      repeat: -1,
      yoyo: true
    });

    const journey = gsap.timeline({
      paused: true,
      repeat: repeats,
      yoyo: true,
      onRepeat: () => {
        travellingRight = !travellingRight;
        gsap.set(sprite, { scaleX: travellingRight ? 1 : -1 });
      }
    });
    journey.to(walker, { left: journeyEnd, duration: journeyDuration, ease: 'none' }, 0);
    if (routeProgress) journey.to(routeProgress, { attr: { 'stroke-dashoffset': 0 }, duration: journeyDuration, ease: 'none' }, 0);
    if (stops.length) {
      journey.to(stops, {
        scale: 1.3,
        duration: 0.3,
        stagger: journeyDuration / stops.length,
        yoyo: true,
        repeat: 1,
        ease: 'sine.inOut'
      }, 0);
    }
    motions.push(journey);

    if (isDesktop && skylineBack && skylineMid && skylineFront) {
      motions.push(gsap.to(skylineBack, {
        x: -8, duration: 12, ease: 'sine.inOut', paused: true, repeat: -1, yoyo: true, willChange: 'transform'
      }));
      motions.push(gsap.to(skylineMid, {
        x: -4, duration: 9, ease: 'sine.inOut', paused: true, repeat: -1, yoyo: true, willChange: 'transform'
      }));
    }
    if (isDesktop) {
      if (copy) {
        gsap.to(copy, {
          y: '6vh',
          autoAlpha: 0.55,
          ease: 'none',
          scrollTrigger: { trigger: hero, start: 'top top', end: '35% top', scrub: true }
        });
      }
      gsap.fromTo(media, { scale: 1.015 }, {
        scale: 1,
        ease: 'none',
        scrollTrigger: { trigger: hero, start: 'top top', end: '35% top', scrub: true }
      });
      // Depth-of-field: the skyline layers drift past each other at
      // different rates as the hero scrolls out, echoing the walker's
      // own parallax and reinforcing that this is a built, layered scene.
      if (skylineBack) gsap.to(skylineBack, { y: -18, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: '35% top', scrub: true } });
      if (skylineMid) gsap.to(skylineMid, { y: -34, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: '35% top', scrub: true } });
      if (skylineFront) gsap.to(skylineFront, { y: -54, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: '35% top', scrub: true } });
    }
    const heroEntry = registerAmbient(motions, hero, ScrollTrigger);
    let walkCancelled = false;
    const walkTimer = window.setTimeout(() => {
      const preload = walkFrames.map((frame) => new Promise((resolve) => {
        const image = new Image();
        image.onload = resolve;
        image.onerror = resolve;
        image.src = walkFrameSource(frame);
      }));
      Promise.all(preload).then(() => {
        if (walkCancelled) return;
        heroEntry.items.push(walk, bob);
        updateAmbientPlayback();
      });
    }, 200);
    cleanup.push(() => {
      walkCancelled = true;
      clearTimeout(walkTimer);
    });
  }

  function createMarqueeMotion(gsap, ScrollTrigger) {
    const marquee = document.querySelector('.expertise-marquee__track');
    const stage = document.querySelector('.expertise-marquee');
    if (!marquee || !stage || !desktop()) return;
    const loop = gsap.to(marquee, {
      xPercent: -22,
      duration: 32,
      ease: 'none',
      repeat: -1,
      paused: true,
      willChange: 'transform'
    });
    registerAmbient([loop], stage, ScrollTrigger);
  }

  function createClosingRouteMotion(gsap, ScrollTrigger) {
    const motif = document.querySelector('[data-closing-route]');
    const path = motif?.querySelector('[data-closing-route-line]');
    if (!motif || !path || (!desktop() && !compact())) return;
    const nodes = Array.from(motif.querySelectorAll('circle'));
    const loop = gsap.timeline({ paused: true, repeat: desktop() ? -1 : 1, repeatDelay: 1.3 });
    gsap.set(path, { strokeDasharray: '0.72 0.28', strokeDashoffset: 0.9 });
    gsap.set(nodes, { transformOrigin: '50% 50%' });
    loop.to(path, { strokeDashoffset: 0, duration: 2.8, ease: 'sine.inOut' }, 0)
      .to(nodes, { scale: 1.34, duration: 0.26, stagger: 0.18, yoyo: true, repeat: 1, ease: 'sine.inOut' }, 0.3)
      .to(path, { strokeDashoffset: -0.22, duration: 1.8, ease: 'sine.inOut' }, 2.8);
    registerAmbient([loop], motif, ScrollTrigger);
  }

  function createEditorialRouteMotion(gsap, ScrollTrigger) {
    const hero = document.querySelector('.portfolio-page .portfolio-hero, .about-page .portfolio-hero');
    const motif = hero?.querySelector('[data-page-route]');
    const path = motif?.querySelector('[data-page-route-line]');
    if (!hero || !motif || !path || (!desktop() && !compact())) return;

    const nodes = Array.from(motif.querySelectorAll('circle'));
    const loop = gsap.timeline({ paused: true, repeat: desktop() ? -1 : 0, repeatDelay: 1.5 });
    gsap.set(path, { strokeDasharray: '0.74 0.26', strokeDashoffset: 0.82 });
    gsap.set(nodes, { transformOrigin: '50% 50%' });
    loop.to(path, { strokeDashoffset: 0, duration: 3.8, ease: 'sine.inOut' }, 0)
      .to(nodes, { scale: 1.26, duration: 0.24, stagger: 0.2, yoyo: true, repeat: 1, ease: 'sine.inOut' }, 0.45)
      .to(path, { strokeDashoffset: -0.18, duration: 1.7, ease: 'sine.inOut' }, 3.8);
    registerAmbient([loop], hero, ScrollTrigger);
  }

  function createAboutFlowMotion(gsap, ScrollTrigger) {
    const flow = document.querySelector('[data-about-flow]');
    const steps = flow ? Array.from(flow.querySelectorAll('.flow__step')) : [];
    if (!flow || !steps.length) return;

    // CSS keeps this content completely visible before motion is eligible. Only
    // this GSAP path applies a temporary start state, so no-JS and reduced
    // motion visitors never inherit a hidden legacy timeline.
    flow.classList.add('is-cohesion-flow');
    gsap.set(steps, { autoAlpha: 0, y: 18 });
    gsap.timeline({
      scrollTrigger: {
        trigger: flow,
        start: 'top 78%',
        once: true
      }
    })
      .call(() => flow.classList.add('is-flow-drawn'))
      .to(steps, {
        autoAlpha: 1,
        y: 0,
        duration: 0.58,
        ease: 'power2.out',
        stagger: 0.12,
        clearProps: 'opacity,visibility,transform'
      }, 0.08);
    cleanup.push(() => flow.classList.remove('is-cohesion-flow', 'is-flow-drawn'));
  }

  function createHomeSelectedMotion(gsap, ScrollTrigger) {
    const section = document.querySelector('[data-home-selected]');
    const projects = section ? Array.from(section.querySelectorAll('[data-home-project]')) : [];
    if (!section || !projects.length) return;

    gsap.set(projects, { autoAlpha: 0, y: 28 });
    ScrollTrigger.batch(projects, {
      start: 'top 82%',
      once: true,
      onEnter: (batch) => gsap.to(batch, {
        autoAlpha: 1,
        y: 0,
        duration: 0.76,
        ease: 'power2.out',
        stagger: 0.12,
        clearProps: 'opacity,visibility,transform'
      })
    });

    if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
    projects.forEach((project) => {
      const media = project.querySelector('[data-home-project-media]');
      if (!media) return;
      const settle = () => gsap.to(media, { scale: 1, duration: 0.42, ease: 'power2.out', overwrite: true });
      on(project, 'pointerenter', () => gsap.to(media, { scale: 1.018, duration: 0.55, ease: 'power2.out', overwrite: true }));
      on(project, 'pointerleave', settle);
      on(project, 'focusin', () => gsap.to(media, { scale: 1.018, duration: 0.35, ease: 'power2.out', overwrite: true }));
      on(project, 'focusout', settle);
    });
  }

  function createAboutBridgeMotion(gsap, ScrollTrigger) {
    const bridge = document.querySelector('[data-about-bridge]');
    const steps = bridge ? Array.from(bridge.querySelectorAll('[data-method-step]')) : [];
    if (!bridge || !steps.length) return;

    // The method list is complete, readable content without JS; this is
    // only a scroll-time stagger, never the owner of the content.
    gsap.set(steps, { autoAlpha: 0, y: 14 });
    gsap.timeline({
      scrollTrigger: { trigger: bridge, start: 'top 78%', once: true }
    }).to(steps, {
      autoAlpha: 1,
      y: 0,
      duration: 0.5,
      stagger: 0.09,
      ease: 'power2.out',
      clearProps: 'opacity,visibility,transform'
    });
  }

  function createJourneyRail(gsap, ScrollTrigger) {
    const rail = document.querySelector('[data-journey-rail]');
    const progress = rail?.querySelector('[data-journey-progress]');
    const stops = rail ? Array.from(rail.querySelectorAll('[data-journey-stop]')) : [];
    if (!rail || !stops.length) return;

    // Each stop names its own section via data-target, so the same rail
    // markup and script work on any page -- home, Work, About -- without
    // page-specific selector lists.
    const sections = stops.map((stop) => document.querySelector(stop.getAttribute('data-target')));

    gsap.set(progress, { height: '0%' });
    ScrollTrigger.create({
      trigger: document.body,
      start: 'top top',
      end: 'bottom bottom',
      onUpdate: (self) => gsap.set(progress, { height: `${Math.round(self.progress * 100)}%` })
    });

    sections.forEach((section, index) => {
      const stop = stops[index];
      if (!section || !stop) return;
      const activate = () => stops.forEach((item, itemIndex) => item.classList.toggle('is-active', itemIndex === index));
      ScrollTrigger.create({
        trigger: section,
        start: 'top 55%',
        end: 'bottom 45%',
        onEnter: activate,
        onEnterBack: activate
      });
    });
  }

  function createWorkRailMotion(gsap, ScrollTrigger) {
    const rail = document.querySelector('[data-work-rail]');
    const stage = rail?.querySelector('.work-rail__stage');
    const frames = stage?.querySelector('.work-rail__frames');
    const category = stage?.querySelector('[data-work-rail-category]');
    const title = stage?.querySelector('[data-work-rail-title]');
    const question = stage?.querySelector('[data-work-rail-question]');
    const rows = rail ? Array.from(rail.querySelectorAll('.atlas-row')) : [];
    if (!rail || !stage || !frames || !rows.length || !desktop()) return;

    const stageImage = document.createElement('img');
    stageImage.className = 'work-rail__frame is-work-active';
    stageImage.alt = '';
    stageImage.decoding = 'async';
    stageImage.setAttribute('aria-hidden', 'true');
    frames.appendChild(stageImage);
    // The stage is a decorative echo of whichever row is active -- the row
    // itself is already a full, properly-labelled keyboard-accessible link
    // to the same destination, so the stage stays out of the a11y tree and
    // just forwards clicks rather than duplicating the link semantics.
    const viewChip = document.createElement('span');
    viewChip.className = 'work-rail__view-chip';
    viewChip.setAttribute('aria-hidden', 'true');
    viewChip.textContent = 'View case study ↗';
    stage.appendChild(viewChip);
    on(stage, 'click', () => { if (rows[active]) rows[active].click(); });
    rail.classList.add('work-rail--enhanced');

    let active = -1;
    const activate = (index, instant = false) => {
      const row = rows[index];
      if (!row || active === index) return;
      active = index;
      const source = row.querySelector('picture img') || Array.from(row.children).find((child) => child.tagName === 'IMG');
      const categoryText = row.querySelector('.eyebrow')?.textContent.trim() || 'CASE STUDY';
      const titleText = row.querySelector('h2, h3')?.textContent.trim() || `Study ${index + 1}`;
      const questionText = row.querySelector('div > p:last-child')?.textContent.trim() || '';
      rows.forEach((item, itemIndex) => item.classList.toggle('is-work-active', itemIndex === index));
      if (category) category.textContent = `CURRENT STUDY / ${String(index + 1).padStart(2, '0')} · ${categoryText}`;
      if (title) title.textContent = titleText;
      if (question) question.textContent = questionText;
      if (source) stageImage.src = source.currentSrc || source.src;
      gsap.killTweensOf(stageImage);
      if (instant) {
        gsap.set(stageImage, { autoAlpha: 1, scale: 1 });
      } else {
        gsap.fromTo(stageImage, { autoAlpha: 0, scale: 1.025 }, {
          autoAlpha: 1,
          scale: 1,
          duration: 0.46,
          ease: 'power2.out',
          overwrite: true
        });
      }
    };

    activate(0, true);
    rows.forEach((row, index) => {
      on(row, 'focusin', () => activate(index));
      if (matchMedia('(hover: hover) and (pointer: fine)').matches) on(row, 'pointerenter', () => activate(index));
      ScrollTrigger.create({
        trigger: row,
        start: 'top 62%',
        end: 'bottom 38%',
        onEnter: () => activate(index),
        onEnterBack: () => activate(index)
      });
    });
    cleanup.push(() => {
      rail.classList.remove('work-rail--enhanced');
      rows.forEach((row) => row.classList.remove('is-work-active'));
      frames.replaceChildren();
      if (category) category.textContent = '';
      if (title) title.textContent = '';
      if (question) question.textContent = '';
    });
  }

  function requestRefresh(ScrollTrigger) {
    clearTimeout(refreshTimer);
    refreshTimer = setTimeout(() => ScrollTrigger.refresh(), 80);
  }

  function createCaseStoryMotion(ScrollTrigger) {
    const roots = Array.from(document.querySelectorAll('.project-story, [data-transit-scrolly]'));

    function attach(root) {
      if (!root || root.dataset.motionStoryBound === 'true') return;
      // data-static-story only skips the multi-MB live GeoJSON fetch (see
      // scrolly-stories.js/scrolly-transit-static.js) -- the empty map
      // layers it leaves behind are already hidden by .is-static-manual
      // CSS. controller.activate()/setActive() never touches that fetch,
      // it just toggles the (cheap, already-rendered) KPI card, kicker,
      // legend caption and progress bar, so scroll-driven sync is just as
      // safe here as on the fully dynamic case studies. Without this, the
      // step text keeps advancing on scroll while the whole visual panel
      // sits frozen on step one -- a static story that never seems to move.
      const controller = root.storyController || (root.matches('[data-transit-scrolly]') ? window.transitStory : null);
      const steps = Array.from(root.querySelectorAll('[data-scrolly-step], .story-step'));
      if (!controller || typeof controller.activate !== 'function' || !steps.length) return;
      root.dataset.motionStoryBound = 'true';
      // One trigger owns each story's state. It is anchored to the reading
      // column, whose geometry remains stable when an adjacent visual decodes;
      // per-step triggers can otherwise briefly replay stale measurements on
      // a large Lenis wheel delta and desynchronise the visual from its copy.
      const activateViewportStep = () => {
        const anchor = innerHeight * 0.58;
        let activeIndex = 0;
        let bestDistance = Infinity;
        steps.forEach((step, index) => {
          const rect = step.getBoundingClientRect();
          const edgeDistance = anchor < rect.top
            ? rect.top - anchor
            : (anchor > rect.bottom ? anchor - rect.bottom : 0);
          const midpointDistance = Math.abs(((rect.top + rect.bottom) / 2) - anchor);
          // A step that contains the reading anchor wins; midpoint distance
          // resolves the otherwise rare overlap/gap case deterministically.
          const distance = edgeDistance * 10000 + midpointDistance;
          if (distance < bestDistance) {
            bestDistance = distance;
            activeIndex = index;
          }
        });
        controller.activate(activeIndex);
      };
      const readingColumn = root.querySelector('.story-steps, .scrolly-static-steps');
      if (!readingColumn) return;
      let syncFrame = 0;
      const inReadingRange = () => {
        const rect = readingColumn.getBoundingClientRect();
        return rect.top <= innerHeight * 0.58 && rect.bottom >= innerHeight * 0.42;
      };
      const syncViewportStep = () => {
        syncFrame = 0;
        if (inReadingRange()) activateViewportStep();
      };
      const scheduleViewportSync = () => {
        if (!syncFrame) syncFrame = requestAnimationFrame(syncViewportStep);
      };
      // Lenis advances native scroll continuously, but ScrollTrigger's
      // container update can coalesce a fast wheel sequence. This listener is
      // a one-frame, geometry-gated state sync—not an animation loop—and
      // delegates the actual visual/content update to the existing controller.
      on(window, 'scroll', scheduleViewportSync, { passive: true });
      cleanup.push(() => {
        if (syncFrame) cancelAnimationFrame(syncFrame);
      });
      ScrollTrigger.create({
        trigger: readingColumn,
        start: 'top 58%',
        end: 'bottom 42%',
        invalidateOnRefresh: true,
        onEnter: scheduleViewportSync,
        onEnterBack: scheduleViewportSync,
        onRefresh: scheduleViewportSync
      });
      scheduleViewportSync();
      requestRefresh(ScrollTrigger);
    }

    roots.forEach(attach);
    on(document, 'story:ready', (event) => attach(event.target));
    on(document, 'story:layout', () => requestRefresh(ScrollTrigger));
    on(document, 'story:error', () => requestRefresh(ScrollTrigger));
  }

  function createCaseEvidenceMotion(gsap, ScrollTrigger) {
    const journeys = gsap.utils.toArray('[data-case-journey]');
    journeys.forEach((journey) => {
      const route = journey.querySelector('[data-case-journey-route]');
      const nodes = gsap.utils.toArray(journey.querySelectorAll('[data-case-journey-node]'));
      const steps = gsap.utils.toArray(journey.querySelectorAll('[data-case-journey-step]'));
      if (!route || !steps.length) return;

      gsap.set(route, { attr: { 'stroke-dasharray': 1, 'stroke-dashoffset': 1 } });
      gsap.set(nodes, { autoAlpha: 0, scale: 0.45, transformBox: 'fill-box', transformOrigin: '50% 50%' });
      gsap.set(steps, { autoAlpha: 0, y: 18 });

      const timeline = gsap.timeline({ paused: true, defaults: { ease: 'power2.out' } })
        .to(route, { attr: { 'stroke-dashoffset': 0 }, duration: 0.78, ease: 'power1.inOut' }, 0)
        .to(nodes, { autoAlpha: 1, scale: 1, duration: 0.28, stagger: 0.1, clearProps: 'transform,opacity,visibility' }, 0.28)
        .to(steps, { autoAlpha: 1, y: 0, duration: 0.52, stagger: 0.1, clearProps: 'transform,opacity,visibility' }, 0.18);

      ScrollTrigger.create({
        trigger: journey,
        start: 'top 82%',
        once: true,
        onEnter: () => timeline.play()
      });
    });
  }

  function createCaseMethodFlowMotion(gsap, ScrollTrigger) {
    const flows = gsap.utils.toArray('.case-study-page .dflow');
    flows.forEach((flow) => {
      const phases = gsap.utils.toArray(flow.querySelectorAll('.dflow__phase'));
      const links = gsap.utils.toArray(flow.querySelectorAll('.dflow__link'));
      if (!phases.length) return;

      // Each connector becomes a small drawn route segment (line + travelling
      // dot) instead of a static arrow glyph, so the pipeline reads as one
      // continuous route between phases rather than four separate cards.
      links.forEach((link) => {
        link.innerHTML = '<span class="dflow__link-line" aria-hidden="true"></span><span class="dflow__link-dot" aria-hidden="true"></span>';
      });
      const lines = gsap.utils.toArray(flow.querySelectorAll('.dflow__link-line'));
      const dots = gsap.utils.toArray(flow.querySelectorAll('.dflow__link-dot'));

      gsap.set(phases, { autoAlpha: 0, y: 16 });
      gsap.set(flow.querySelectorAll('.dflow__num'), { scale: 0.6, transformOrigin: '50% 50%' });
      gsap.set(lines, { scaleX: 0, transformOrigin: 'left center' });
      gsap.set(dots, { autoAlpha: 0, scale: 0 });
      const timeline = gsap.timeline({ paused: true, defaults: { ease: 'power2.out' } });
      phases.forEach((phase, index) => {
        const at = index * 0.22;
        const num = phase.querySelector('.dflow__num');
        timeline.to(phase, { autoAlpha: 1, y: 0, duration: 0.42, clearProps: 'opacity,visibility,transform' }, at);
        if (num) timeline.to(num, { scale: 1, duration: 0.3, ease: 'back.out(2.2)' }, at + 0.08);
        if (lines[index]) {
          timeline.to(lines[index], { scaleX: 1, duration: 0.3, ease: 'power1.inOut' }, at + 0.2)
            .to(dots[index], { autoAlpha: 1, scale: 1, duration: 0.18 }, at + 0.42)
            .to(dots[index], { autoAlpha: 0, duration: 0.14 }, at + 0.6);
        }
      });
      ScrollTrigger.create({
        trigger: flow,
        start: 'top 84%',
        once: true,
        onEnter: () => timeline.play()
      });
    });
  }

  function createCaseChartMotion(gsap, ScrollTrigger) {
    const chartSelector = '[data-mbr-chart], [data-cbd-bars], [data-alphaearth-chart], [data-pangan-chart]';

    function playChart(svg) {
      if (!svg || !svg.isConnected) return;
      const bars = gsap.utils.toArray(svg.querySelectorAll('.story-chart-bar, .alphaearth-chart__bar, .alphaearth-chart__range'));
      const lines = gsap.utils.toArray(svg.querySelectorAll('.story-chart-line, .alphaearth-chart__line'));
      const bands = gsap.utils.toArray(svg.querySelectorAll('.story-chart-band'));
      const points = gsap.utils.toArray(svg.querySelectorAll('.story-chart-point, .alphaearth-chart__point, .alphaearth-chart__median'));
      const values = gsap.utils.toArray(svg.querySelectorAll('.story-chart-value, .alphaearth-chart__end-label, .alphaearth-chart__range-label, .alphaearth-chart__value'));
      const cards = gsap.utils.toArray(svg.querySelectorAll('.mbr-chart__card, .mbr-chart__metric, .mbr-chart__label, .mbr-chart__note, .alphaearth-chart__scope-unit, .alphaearth-chart__scope-label, .alphaearth-chart__scope-note, .alphaearth-chart__pilot-card, .alphaearth-chart__pilot-value, .alphaearth-chart__pilot-label, .alphaearth-chart__aggregate-box, .alphaearth-chart__aggregate-label, .alphaearth-chart__gate-box, .alphaearth-chart__gate-title, .alphaearth-chart__gate-copy'));
      const targets = bars.concat(lines, bands, points, values, cards);
      if (!targets.length) return;

      svg.__caseChartTimeline?.kill();
      gsap.killTweensOf(targets);
      // GSAP logs a warning for an empty target list. A chart can legitimately
      // be bars-only, line-only, or a metric-card state, so initialise only
      // the primitive groups that are actually present.
      if (bars.length) gsap.set(bars, { autoAlpha: 0.18, scaleX: 0.02, transformBox: 'fill-box', transformOrigin: 'left center' });
      if (lines.length) gsap.set(lines, { autoAlpha: 0.24, attr: { 'stroke-dasharray': 1, 'stroke-dashoffset': 1 } });
      if (bands.length) gsap.set(bands, { autoAlpha: 0 });
      if (points.length) gsap.set(points, { autoAlpha: 0, scale: 0.55, transformBox: 'fill-box', transformOrigin: '50% 50%' });
      if (values.length) gsap.set(values, { autoAlpha: 0, y: 6 });
      if (cards.length) gsap.set(cards, { autoAlpha: 0, y: 10 });

      const timeline = gsap.timeline({ defaults: { ease: 'power2.out' } });
      if (cards.length) timeline.to(cards, { autoAlpha: 1, y: 0, duration: 0.38, stagger: 0.045, clearProps: 'transform,opacity,visibility' }, 0);
      if (bands.length) timeline.to(bands, { autoAlpha: 0.68, duration: 0.24 }, 0.06);
      if (bars.length) timeline.to(bars, { autoAlpha: 1, scaleX: 1, duration: 0.56, stagger: 0.045, clearProps: 'transform,opacity,visibility' }, 0.1);
      if (lines.length) timeline.to(lines, { autoAlpha: 1, attr: { 'stroke-dashoffset': 0 }, duration: 0.68, stagger: 0.08, clearProps: 'opacity,visibility' }, 0.12);
      if (points.length) timeline.to(points, { autoAlpha: 1, scale: 1, duration: 0.24, stagger: 0.04, clearProps: 'transform,opacity,visibility' }, 0.54);
      if (values.length) timeline.to(values, { autoAlpha: 1, y: 0, duration: 0.28, stagger: 0.025, clearProps: 'transform,opacity,visibility' }, 0.52);
      svg.__caseChartTimeline = timeline;
    }

    function animateChart(svg) {
      if (!svg || !svg.isConnected) return;
      svg.__caseChartTrigger?.kill();
      const rect = svg.getBoundingClientRect();
      const visible = rect.bottom > 0 && rect.top < innerHeight;
      if (visible) {
        playChart(svg);
        return;
      }
      svg.__caseChartTrigger = ScrollTrigger.create({
        trigger: svg,
        start: 'top 90%',
        once: true,
        onEnter: () => playChart(svg)
      });
    }

    const animateRoot = (root) => {
      if (!root || !root.querySelectorAll) return;
      root.querySelectorAll(chartSelector).forEach(animateChart);
    };

    document.querySelectorAll(chartSelector).forEach(animateChart);
    on(document, 'story:visual-change', (event) => animateRoot(event.target));
  }

  function createReveals(gsap, ScrollTrigger) {
    // Case heroes carry the page's LCP text. Keep them visible in the first
    // paint; the route curtain remains the entry transition while below-fold
    // evidence still receives the shared reveal treatment.
    const items = gsap.utils.toArray('.reveal').filter((item) => !item.closest('.cs-hero') && !item.matches('.dflow'));
    if (!items.length) return;
    document.documentElement.classList.remove('js-reveal');
    gsap.set(items, { autoAlpha: 0, y: 20 });
    ScrollTrigger.batch(items, {
      start: 'top 86%',
      once: true,
      onEnter: (batch) => gsap.to(batch, {
        autoAlpha: 1,
        y: 0,
        duration: 0.72,
        ease: 'power2.out',
        stagger: 0.06,
        overwrite: true,
        clearProps: 'transform,opacity,visibility'
      })
    });
  }

  function destroy() {
    cleanup.forEach((off) => off());
    cleanup = [];
    clearTimeout(refreshTimer);
    ctx?.revert();
    ctx = null;
    ambientEntries = [];
    if (ticker && window.gsap) window.gsap.ticker.remove(ticker);
    ticker = null;
    lenis?.destroy();
    lenis = null;
    document.documentElement.classList.remove('motion-ready');
    document.querySelectorAll('[data-motion-story-bound="true"]').forEach((root) => delete root.dataset.motionStoryBound);
  }

  function init() {
    destroy();
    resetHeroStatic();
    const button = document.querySelector('[data-ambient-toggle]');
    userAmbientEnabled = !button || button.getAttribute('aria-pressed') !== 'false';
    resetAmbientToggle();

    if (!eligible()) return;
    const { gsap, ScrollTrigger } = window;
    gsap.registerPlugin(ScrollTrigger);
    const hero = document.querySelector('[data-hero-stage]');
    const media = document.querySelector('.spatial-hero__strip');

    const routeAllowsLenis = Boolean(hero && media) || document.body.matches('[data-smooth-scroll="desktop"]');
    if (routeAllowsLenis && desktop() && window.Lenis) {
      lenis = new Lenis({ autoRaf: false, syncTouch: false });
      lenis.on('scroll', ScrollTrigger.update);
      ticker = (time) => lenis.raf(time * 1000);
      gsap.ticker.add(ticker);
      gsap.ticker.lagSmoothing(0);
    }

    ctx = gsap.context(() => {
      if (hero && media) createHeroMotion(gsap, ScrollTrigger, hero, media);
      createMarqueeMotion(gsap, ScrollTrigger);
      createClosingRouteMotion(gsap, ScrollTrigger);
      createEditorialRouteMotion(gsap, ScrollTrigger);
      createHomeSelectedMotion(gsap, ScrollTrigger);
      createAboutBridgeMotion(gsap, ScrollTrigger);
      createJourneyRail(gsap, ScrollTrigger);
      createWorkRailMotion(gsap, ScrollTrigger);
      createAboutFlowMotion(gsap, ScrollTrigger);
      createCaseStoryMotion(ScrollTrigger);
      createCaseEvidenceMotion(gsap, ScrollTrigger);
      createCaseMethodFlowMotion(gsap, ScrollTrigger);
      createCaseChartMotion(gsap, ScrollTrigger);
      createReveals(gsap, ScrollTrigger);
    }, document.body);

    if (button) {
      on(button, 'ambient:change', (event) => {
        userAmbientEnabled = Boolean(event.detail && event.detail.enabled);
        updateAmbientPlayback();
      });
    }
    on(document, 'visibilitychange', updateAmbientPlayback);
    updateAmbientPlayback();
    document.documentElement.classList.add('motion-ready');
    requestRefresh(ScrollTrigger);
  }

  function scheduleInit() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(init, 180);
  }

  if (document.readyState === 'loading') addEventListener('DOMContentLoaded', createWelcomeIntro, { once: true });
  else createWelcomeIntro();
  if (document.readyState === 'complete') init();
  else addEventListener('load', init, { once: true });
  if (reduced.addEventListener) reduced.addEventListener('change', init);
  else reduced.addListener(init);
  addEventListener('resize', scheduleInit);
  addEventListener('pagehide', destroy);
  addEventListener('pageshow', (event) => { if (event.persisted) scheduleInit(); });
})();
