import { useState, useEffect, useRef } from 'react';
import { flushSync } from 'react-dom';

const collageImages = [
  { src: "images/Collage/Firefly_GeminiFlash_Close up of the 4 of them together, all smiling. Professional photo shoot wearing hip 169102.jpg", alt: "Band moment" },
  { src: "images/Collage/Firefly_GeminiFlash_Professional pop group portrait of all 7 of them in a unique setting and in different 181489.png", alt: "Band portrait" },
  { src: "images/Collage/Firefly_GeminiFlash_The 3 of them together, all smiling and goofing around. Professional photo shoot wear 501103.png", alt: "Band fun" },
  { src: "images/Collage/Firefly_GeminiFlash_The 3 of them together, all smiling and goofing around. Professional photo shoot wear 591272.png", alt: "Band fun" },
  { src: "images/Collage/Firefly_GeminiFlash_The 3 of them together, all smiling and goofing around. Professional photo shoot wear 790781.png", alt: "Band fun" },
  { src: "images/Collage/Firefly_GeminiFlash_The 4 of them together, all smiling and goofing around. Professional photo shoot wear 263443.png", alt: "Band fun" },
  { src: "images/Collage/Firefly_GeminiFlash_They are all having fun horseback riding in the Colorado mountains.. 816982.png", alt: "Horseback riding" },
  { src: "images/Collage/Firefly_GeminiFlash_They are all having fun horseback riding in the Colorado mountains.. 984380.jpg", alt: "Horseback riding" },
  { src: "images/Collage/Firefly_GeminiFlash_They are on an adventure together. 985742.jpg", alt: "Band adventure" },
];
const N = collageImages.length;
const COPIES = 7;
const tiledImages = Array.from({ length: COPIES }, () => collageImages).flat();
const START = Math.floor(COPIES / 2) * N; // center of 7 copies = 3*N

export default function FavoriteMoments() {
  const [collageIndex, setCollageIndex] = useState(START);
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const trackRef = useRef(null);
  const indexRef = useRef(START);
  const lastInteractionRef = useRef(0);
  const touchStartXRef = useRef(null);
  const lightboxOpenRef = useRef(false);
  const lightboxTouchStartXRef = useRef(null);

  // Preload all collage images into browser cache on mount
  useEffect(() => {
    collageImages.forEach(({ src }) => {
      const img = new Image();
      img.src = src;
    });
  }, []);

  const advanceCarousel = (dir, e) => {
    if (e) e.currentTarget.blur();
    lastInteractionRef.current = Date.now();
    const next = indexRef.current + dir;
    indexRef.current = next;
    setCollageIndex(next);
  };

  // Auto-scroll every 4.5s, pauses for 5s after any user interaction
  useEffect(() => {
    const timer = setInterval(() => {
      if (!lightboxOpenRef.current && Date.now() - lastInteractionRef.current > 5000) {
        const next = indexRef.current + 1;
        indexRef.current = next;
        setCollageIndex(next);
      }
    }, 4500);
    return () => clearInterval(timer);
  }, []);

  const handleTouchStart = (e) => {
    touchStartXRef.current = e.touches[0].clientX;
  };

  const handleTouchEnd = (e) => {
    if (touchStartXRef.current === null) return;
    const diff = touchStartXRef.current - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 30) {
      advanceCarousel(diff > 0 ? 1 : -1);
    }
    touchStartXRef.current = null;
  };

  const handleLightboxTouchStart = (e) => {
    lightboxTouchStartXRef.current = e.touches[0].clientX;
  };

  const handleLightboxTouchEnd = (e) => {
    if (lightboxTouchStartXRef.current === null) return;
    const diff = lightboxTouchStartXRef.current - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 30) {
      const dir = diff > 0 ? 1 : -1;
      const next = indexRef.current + dir;
      indexRef.current = next;
      setCollageIndex(next);
    }
    lightboxTouchStartXRef.current = null;
  };

  // After each slide animation ends, silently snap back to center zone.
  // Reading el.offsetWidth forces a synchronous reflow, committing the new
  // transform to the browser before transition is re-enabled — so the jump
  // is never painted and the user sees no backward movement.
  // IMPORTANT: child elements (.tray-slide, .tray-img) also have transitions
  // whose transitionend events bubble up here — ignore them.
  const handleTransitionEnd = (e) => {
    if (e.target !== trackRef.current) return;
    const ci = indexRef.current;
    const corrected = ((ci % N) + N) % N + START;
    if (corrected !== ci) {
      const el = trackRef.current;
      if (el) {
        el.style.transition = 'none';
        // flushSync re-assigns .center to a different DOM element, which would
        // trigger the slide scale transition and cause a visible pop.
        // Suppress all child slide transitions during the correction too.
        flushSync(() => { indexRef.current = corrected; setCollageIndex(corrected); });
        el.querySelectorAll('.tray-slide').forEach(s => { s.style.transition = 'none'; });
        void el.offsetWidth; // force reflow — commits track + slide state before animations re-enable
        el.style.transition = '';
        el.querySelectorAll('.tray-slide').forEach(s => { s.style.transition = ''; });
      }
    }
  };

  const current = tiledImages[Math.max(0, Math.min(tiledImages.length - 1, collageIndex))];

  return (
    <section className="gc-section collage-section" aria-labelledby="gc-moments-title">
      <div className="gc-section__head">
        <h2 id="gc-moments-title" className="gc-h2">Our Favorite Moments</h2>
      </div>
      <div className="tray-root" onTouchStart={handleTouchStart} onTouchEnd={handleTouchEnd}>
        <div className="tray-track" ref={trackRef} onTransitionEnd={handleTransitionEnd} style={{ transform: `translateX(calc(var(--side-w) - ${collageIndex} * var(--slide-w)))` }}>
          {tiledImages.map((img, i) => {
            const isCenter = i === collageIndex;
            const dist = Math.abs(i - collageIndex);
            const loadStrategy = dist <= 2 ? 'eager' : 'lazy';
            return (
              <div
                key={i}
                className={`tray-slide${isCenter ? ' center' : ''}`}
                onClick={isCenter ? () => { lightboxOpenRef.current = true; setLightboxOpen(true); } : undefined}
              >
                <img src={img.src} alt={img.alt} className="tray-img" loading={loadStrategy} />
              </div>
            );
          })}
        </div>
        <div className="tray-fade-left" />
        <div className="tray-fade-right" />
        <button type="button" className="tray-btn tray-btn-left" onClick={(e) => advanceCarousel(-1, e)} aria-label="Previous photo">&#8249;</button>
        <button type="button" className="tray-btn tray-btn-right" onClick={(e) => advanceCarousel(1, e)} aria-label="Next photo">&#8250;</button>
      </div>
      {lightboxOpen && (
        <div
          className="lightbox-overlay"
          onClick={() => { lightboxOpenRef.current = false; setLightboxOpen(false); }}
          onTouchStart={handleLightboxTouchStart}
          onTouchEnd={handleLightboxTouchEnd}
        >
          <button
            type="button"
            className="lightbox-close"
            onClick={(e) => { e.stopPropagation(); lightboxOpenRef.current = false; setLightboxOpen(false); }}
            aria-label="Close"
          >
            ✕
          </button>
          <img src={current.src} alt={current.alt} className="lightbox-img" onClick={(e) => e.stopPropagation()} />
        </div>
      )}
    </section>
  );
}
