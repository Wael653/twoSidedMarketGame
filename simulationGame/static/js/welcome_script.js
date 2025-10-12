
  const { animate, text, stagger,svg } = anime;

  setTimeout(() => {
  const { chars } = text.split('.willkommen-title', { 
    words: false, 
    chars: true 
  });

  animate(chars, {
    y: [
      { to: '-1.5rem', ease: 'outExpo', duration: 600 },
      { to: 0,          ease: 'outBounce', duration: 800 }
    ],
    delay: stagger(50),
    ease: 'inOutCirc',
    loopDelay: 900,
    loop: true,
  });
}, 1000);


