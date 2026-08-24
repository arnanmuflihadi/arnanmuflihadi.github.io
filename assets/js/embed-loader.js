(() => {
  const selector = '[data-explicit-embed]';
  const local = href => {
    try { return new URL(href, window.location.href).origin === window.location.origin; }
    catch (_) { return false; }
  };

  document.querySelectorAll(selector).forEach(shell => {
    const frame = shell.querySelector('[data-embed-frame]');
    const load = shell.querySelector('[data-embed-load]');
    const status = shell.querySelector('[data-embed-status]');
    if (!frame || !load || !frame.dataset.src || !local(frame.dataset.src)) return;

    shell.dataset.embedReady = 'true';
    const setStatus = message => { if (status) status.textContent = message; };
    load.addEventListener('click', () => {
      if (shell.dataset.embedState === 'loaded' || shell.dataset.embedState === 'loading') return;
      shell.dataset.embedState = 'loading';
      load.disabled = true;
      load.textContent = 'Loading interactive map…';
      setStatus('Loading interactive map…');

      const timeout = window.setTimeout(() => {
        if (shell.dataset.embedState === 'loading') {
          setStatus('This map is taking longer than expected. You can open it in a new tab.');
        }
      }, 12000);

      frame.addEventListener('load', () => {
        window.clearTimeout(timeout);
        shell.dataset.embedState = 'loaded';
        load.hidden = true;
        setStatus('Interactive map loaded.');
      }, { once: true });
      frame.src = frame.dataset.src;
    });
  });
})();
