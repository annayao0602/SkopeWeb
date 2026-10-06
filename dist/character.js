(() => {
  const canvas = document.getElementById('skope-character');
  const fallback = document.getElementById('character-fallback');
  if (!canvas || !window.rive) return;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let ready = false;
  let visible = true;
  const restoreImage = () => {
    ready = false;
    canvas.hidden = true;
    fallback.hidden = false;
  };
  rive.RuntimeLoader.setWasmUrl('assets/rive/rive.wasm');
  let character;
  const syncPlayback = () => {
    if (!ready) return;
    if (visible && !document.hidden && !reducedMotion.matches) character.play();
    else character.pause();
  };
  try {
    character = new rive.Rive({
      src: 'assets/idle.riv',
      canvas,
      autoplay: !reducedMotion.matches,
      autoBind: true,
      stateMachines: 'State Machine 1',
      layout: new rive.Layout({fit: rive.Fit.Contain, alignment: rive.Alignment.Center}),
      onLoad: () => {
        canvas.hidden = false;
        fallback.hidden = true;
        ready = true;
        character.resizeDrawingSurfaceToCanvas();
        syncPlayback();
      },
      onLoadError: restoreImage,
    });
    new ResizeObserver(() => {
      if (ready) character.resizeDrawingSurfaceToCanvas();
    }).observe(canvas.parentElement);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => {
        visible = entries[0].isIntersecting;
        syncPlayback();
      }).observe(canvas);
    }
    document.addEventListener('visibilitychange', syncPlayback);
    reducedMotion.addEventListener('change', syncPlayback);
  } catch (error) {
    restoreImage();
  }
})();
