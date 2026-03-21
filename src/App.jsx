import { useState, useEffect, useRef } from 'react';
import { flushSync } from 'react-dom';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import AlbumItem from './components/AlbumItem.jsx';
import Blog from './components/Blog.jsx';
import BlogPost from './components/BlogPost.jsx';
import Privacy from './components/Privacy.jsx';
import Contact from './components/Contact.jsx';
import NewsletterSignup from './components/NewsletterSignup.jsx';
import Unsubscribe from './components/Unsubscribe.jsx';
import EvenBetterChristmas from './components/EvenBetterChristmas.jsx';
import LetMyHeartFindChristmas from './components/LetMyHeartFindChristmas.jsx';
import './App.css';

function App() {
  const location = useLocation();
  // Toggle a class on <html> only for specific subpages where we want a dark root background
  useEffect(() => {
    const htmlEl = document.documentElement;
    const darkRoutes = ['/contact', '/privacy', '/newsletter'];
    const isDarkSubpage = darkRoutes.includes(location.pathname);
    if (isDarkSubpage) {
      htmlEl.classList.add('subpage');
    } else {
      htmlEl.classList.remove('subpage');
    }
  }, [location.pathname]);
  // Sample album data (replace with API data in a real MERN app)
  const newAlbum = {
    id: 'new',
    spotifyLink: 'https://open.spotify.com/album/0FDPRyIXg50LXOdgH8g65b',
    amazonMusicLink: 'https://music.amazon.com/albums/B0FWZ9VRCF',
    appleMusicLink: 'https://music.apple.com/us/album/even-better-christmas/1847634777',
    youtubeMusicLink: 'https://music.youtube.com/playlist?list=OLAK5uy_n_fdOT3WVxXeKfjr-h2arrYbk623z3VRU',
  };

  const albums = [
    {
      id: 1,
      spotifyEmbedIframe: '<iframe data-testid="embed-iframe" className="spotify-embed" style={{borderRadius: "12px"}} src={`https://open.spotify.com/embed/album/${albumId}?utm_source=generator`} width="100%" height="352" frameBorder="0" allowFullScreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>',
      spotifyLink: 'https://open.spotify.com/album/0eRcQ32hkwgvSvfPPPOOhu',
      amazonMusicLink: 'https://music.amazon.com/albums/B0FRYSGZ4C',
      youtubeLink: 'https://www.youtube.com/watch?v=EDaC7_Ek8eM&list=OLAK5uy_lUIwPFRjiX3R6qIWC3VFwBNw4LLNCupHc',
      appleMusicLink: 'https://music.apple.com/us/album/your-majesty/1841459632',
      youtubeMusicLink: 'https://music.youtube.com/playlist?list=OLAK5uy_kVbhrim-szUB-OAs0nCayOWOijpXukKCA',
    },
    {
      id: 2,
      spotifyEmbedIframe: '<iframe data-testid="embed-iframe" className="spotify-embed" style={{borderRadius: "12px"}} src={`https://open.spotify.com/embed/album/5Tt1sGIoAnpzRHY3abDqz4?utm_source=generator`} width="100%" height="352" frameBorder="0" allowFullScreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>',
      spotifyLink: 'https://open.spotify.com/album/5Tt1sGIoAnpzRHY3abDqz4',
      amazonMusicLink: 'https://music.amazon.com/albums/B0FNLZ7CJ4',
      youtubeLink: 'https://youtu.be/QoaeKUHDJM8',
      appleMusicLink: 'https://music.apple.com/us/album/im-still-your-love-single/1835662171',
      youtubeMusicLink: 'https://music.youtube.com/watch?v=QoaeKUHDJM8',
    },
  ];

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

  return (
    <Routes>
      <Route path="/" element={
        <div className="main-page">
          {/* Navbar */}
          <div className="header">
            <nav className="navbar">
              <p><Link to="/" className="nav-link" onClick={(e) => {
                e.preventDefault();
                const element = document.getElementById('about');
                if (element) {
                  const offset = 100;
                  const rect = element.getBoundingClientRect();
                  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                  const elementTop = rect.top + scrollTop;
                  window.scrollTo({
                    top: elementTop - offset,
                    behavior: 'smooth'
                  });
                }
              }}>About</Link></p>
              <p><Link to="/" className="nav-link" onClick={(e) => {
                e.preventDefault();
                const element = document.getElementById('releases');
                if (element) {
                  const offset = 100;
                  const rect = element.getBoundingClientRect();
                  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                  const elementTop = rect.top + scrollTop;
                  window.scrollTo({
                    top: elementTop - offset,
                    behavior: 'smooth'
                  });
                }
              }}>Releases</Link></p>
              <p><Link to="/newsletter" className="nav-link">Stay in touch</Link></p>
              {/* <p><Link to="/blog" className="nav-link">Blog</Link></p> */}
            </nav>
          </div>

          {/* Logo and Band Hero Shot */}
          <header className="hero-section">
            <img
              className="hero-image"
              src="images/site-banners/GC Studio Banner YT.jpg"
              alt="Gracechase studio banner"
            />
          </header>

          {/* Releases Section */}
          <section className="releases-section" id="releases">
            <h2>Releases</h2>
            <div className="embeds-grid">
              <div className="embed-cell embed-smf">
                <iframe
                  data-testid="embed-iframe"
                  style={{ borderRadius: '12px' }}
                  src="https://open.spotify.com/embed/album/17n7rXpMd7OqsIkfjQQDDR?utm_source=generator"
                  width="100%"
                  height="352"
                  frameBorder="0"
                  allowFullScreen=""
                  allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                  loading="lazy"
                />
                <div className="streaming-links">
                  <a href="https://open.spotify.com/album/17n7rXpMd7OqsIkfjQQDDR" target="_blank" rel="noopener noreferrer" aria-label="Listen on Spotify">
                    <img src="images/link-icons/Alt Streaming Service Icons/Spotify_Primary_Logo_RGB_Green.png?v=2" alt="Spotify" />
                  </a>
                  <a href="https://music.youtube.com/playlist?list=OLAK5uy_kO4ztJC1BtAXZTzuvXEh44m22aGglsgKo" target="_blank" rel="noopener noreferrer" aria-label="Listen on YouTube Music">
                    <img src="images/link-icons/YT_music_logo.png" alt="YouTube Music" />
                  </a>
                  <a href="https://music.apple.com/us/album/set-me-free/1878887745" target="_blank" rel="noopener noreferrer" aria-label="Listen on Apple Music">
                    <img src="images/link-icons/Alt Streaming Service Icons/music.cce3eb3f.svg" alt="Apple Music" />
                  </a>
                  <a href="https://music.amazon.com/albums/B0GNPDJP9H" target="_blank" rel="noopener noreferrer" aria-label="Listen on Amazon Music">
                    <img src="images/link-icons/amazon_music_logo.png" alt="Amazon Music" />
                  </a>
                </div>
              </div>
              <div className="embed-cell embed-ebc">
                <iframe
                  data-testid="embed-iframe"
                  style={{ borderRadius: '12px' }}
                  src="https://open.spotify.com/embed/album/0FDPRyIXg50LXOdgH8g65b?utm_source=generator"
                  width="100%"
                  height="352"
                  frameBorder="0"
                  allowFullScreen=""
                  allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                  loading="lazy"
                />
                <div className="streaming-links">
                  <a href="https://open.spotify.com/album/0FDPRyIXg50LXOdgH8g65b" target="_blank" rel="noopener noreferrer" aria-label="Listen on Spotify">
                    <img src="images/link-icons/Alt Streaming Service Icons/Spotify_Primary_Logo_RGB_Green.png?v=2" alt="Spotify" />
                  </a>
                  <a href="https://music.youtube.com/playlist?list=OLAK5uy_n_fdOT3WVxXeKfjr-h2arrYbk623z3VRU" target="_blank" rel="noopener noreferrer" aria-label="Listen on YouTube Music">
                    <img src="images/link-icons/YT_music_logo.png" alt="YouTube Music" />
                  </a>
                  <a href="https://music.apple.com/us/album/even-better-christmas/1847634777" target="_blank" rel="noopener noreferrer" aria-label="Listen on Apple Music">
                    <img src="images/link-icons/Alt Streaming Service Icons/music.cce3eb3f.svg" alt="Apple Music" />
                  </a>
                  <a href="https://music.amazon.com/albums/B0FWZ9VRCF" target="_blank" rel="noopener noreferrer" aria-label="Listen on Amazon Music">
                    <img src="images/link-icons/amazon_music_logo.png" alt="Amazon Music" />
                  </a>
                </div>
              </div>
              {albums.map((album) => (
                <div className={`embed-cell ${album.id === 1 ? 'embed-ymj' : 'embed-isyl'}`} key={album.id}>
                  <AlbumItem
                    spotifyLink={album.spotifyLink}
                    youtubeMusicLink={album.youtubeMusicLink}
                    youtubeLink={album.youtubeLink}
                    appleMusicLink={album.appleMusicLink}
                    amazonMusicLink={album.amazonMusicLink}
                  />
                </div>
              ))}
            </div>
          </section>

          {/* Our Favorite Moments Carousel */}
          <section className="collage-section">
            <h2>Our Favorite Moments</h2>
            <div className="tray-root" onTouchStart={handleTouchStart} onTouchEnd={handleTouchEnd}>
              <div className="tray-track" ref={trackRef} onTransitionEnd={handleTransitionEnd} style={{ transform: `translateX(calc(var(--side-w) - ${collageIndex} * var(--slide-w)))` }}>
                {tiledImages.map((img, i) => {
                  const isCenter = i === collageIndex;
                  const dist = Math.abs(i - collageIndex);
                  const loadStrategy = dist <= 2 ? 'eager' : 'lazy';
                  // Clamp to prevent undefined access if index drifts out of bounds
                  const safeImg = tiledImages[Math.max(0, Math.min(tiledImages.length - 1, i))];
                  return (
                    <div
                      key={i}
                      className={`tray-slide${isCenter ? ' center' : ''}`}
                      onClick={isCenter ? () => { lightboxOpenRef.current = true; setLightboxOpen(true); } : undefined}
                    >
                      <img src={safeImg.src} alt={safeImg.alt} className="tray-img" loading={loadStrategy} />
                    </div>
                  );
                })}
              </div>
              <div className="tray-fade-left" />
              <div className="tray-fade-right" />
              <button className="tray-btn tray-btn-left" onClick={(e) => advanceCarousel(-1, e)} aria-label="Previous photo">&#8249;</button>
              <button className="tray-btn tray-btn-right" onClick={(e) => advanceCarousel(1, e)} aria-label="Next photo">&#8250;</button>
            </div>
            {lightboxOpen && (
              <div className="lightbox-overlay" onClick={() => setLightboxOpen(false)} onTouchStart={handleLightboxTouchStart} onTouchEnd={handleLightboxTouchEnd}>
                <button className="lightbox-close" onClick={(e) => { e.stopPropagation(); setLightboxOpen(false); }} aria-label="Close">✕</button>
                <img
                  src={tiledImages[Math.max(0, Math.min(tiledImages.length - 1, collageIndex))].src}
                  alt={tiledImages[Math.max(0, Math.min(tiledImages.length - 1, collageIndex))].alt}
                  className="lightbox-img"
                  onClick={(e) => e.stopPropagation()}
                />
              </div>
            )}
          </section>

          {/* About Section */}
          <section className="about-section" id="about">
            <h2>About Gracechase</h2>
            <p>Grace has been chasing you. Maybe it's time to stop running.</p>
            <div className="about-content">
              <div className="about-subsection">
                <h3>Our Story</h3>
                <p>
                  Hey there! We are Gracechase. We're an innovative music group that combines our musical creativity with cutting edge AI technology to create songs that are beautiful and exciting, and aim to point the listener back to our Creator.
                </p>
              </div>
              <div className="about-subsection">
                <h3>What inspires us</h3>
                <p>
                  We are deeply moved by the Grace of our Lord Jesus, and we want to remind our listeners of His unending love and mercy through our music. We love to write, and to share our stories, and we hope that we can inspire our listeners to the awe and wonder of creation, and of the One who made it all.
                </p>
              </div>
              {/* <div className="about-subsection">
                 <h3>Meet the Crew</h3>
                <p>Gracechase is brought to life by a team of AI "characters" and human collaborators:</p>
                <ul>
                  <li><strong>Grace:</strong> The lead AI composer, inspired by classical elegance.</li>
                  <li><strong>Chase:</strong> The rhythm generator, driven by dynamic energy.</li>
                  <li><strong>Harmony:</strong> The human arranger, adding emotional depth.</li>
                  <li><strong>Echo:</strong> The sound designer, crafting immersive audio experiences.</li>
                </ul>
              </div> */}
            </div>
          </section>

          <section className='footer'>
            <div className='footer-content'>
              <p>&copy; 2025 Gracechase. All rights reserved. |
                {' '}
                <Link to="/privacy">Privacy Policy</Link>
                {' '}|
                {' '}
                <Link to="/contact">Contact</Link>
              </p>
            </div>
          </section>
        </div>
      } />
      <Route path="/blog" element={<Blog />} />
      <Route path="/blog/:id" element={<BlogPost />} />
      <Route path="/privacy" element={<Privacy />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="/newsletter" element={<NewsletterSignup />} />
      <Route path="/unsubscribe" element={<Unsubscribe />} />
      <Route path="/even-better-christmas" element={<EvenBetterChristmas />} />
      <Route path="/let-my-heart-find-christmas" element={<LetMyHeartFindChristmas />} />
    </Routes>
  );
}

export default App;
