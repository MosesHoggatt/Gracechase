import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import './EvenBetterChristmas.css';

const EvenBetterChristmas = () => {
  const albumData = {
    spotifyLink: 'https://open.spotify.com/album/0FDPRyIXg50LXOdgH8g65b',
    amazonMusicLink: 'https://music.amazon.com/albums/B0FWZ9VRCF',
    appleMusicLink: 'https://music.apple.com/us/album/even-better-christmas/1847634777',
    youtubeMusicLink: 'https://music.youtube.com/playlist?list=OLAK5uy_n_fdOT3WVxXeKfjr-h2arrYbk623z3VRU',
  };

  useEffect(() => {
    window.scrollTo({ top: 0, left: 0 });
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
  }, []);

  return (
    <div className="even-better-christmas-page">
      {/* Header */}
      <div className="ebc-header">
        <nav className="ebc-navbar">
          <p><Link to="/" className="ebc-nav-link" onClick={(e) => {
            e.preventDefault();
            window.location.href = '/#/';
            setTimeout(() => {
              window.scrollTo({
                top: 0,
                behavior: 'smooth'
              });
            }, 100);
          }}>Home</Link></p>
          <p><Link to="/" className="ebc-nav-link" onClick={(e) => {
            e.preventDefault();
            window.location.href = '/#/';
            setTimeout(() => {
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
            }, 100);
          }}>About</Link></p>
          <p><Link to="/" className="ebc-nav-link" onClick={(e) => {
            e.preventDefault();
            window.location.href = '/#/';
            setTimeout(() => {
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
            }, 100);
          }}>Releases</Link></p>
          <p><Link to="/newsletter" className="ebc-nav-link">Stay in touch</Link></p>
          {/* <p><Link to="/blog" className="ebc-nav-link">Blog</Link></p> */}
        </nav>
      </div>

      <div className="ebc-content-wrapper">
        <p className="ebc-hero-text">Your new favorite Christmas album</p>
        
        <div className="ebc-hero">
          <img 
            src="images/album-covers/Even Better Christmas Cover 1000px.jpg" 
            alt="Even Better Christmas Album Cover" 
            className="ebc-cover"
          />
        </div>

        <div className="ebc-player-section">
          <iframe 
            className="ebc-spotify-embed" 
            style={{borderRadius: '16px'}} 
            src="https://open.spotify.com/embed/album/0FDPRyIXg50LXOdgH8g65b?utm_source=generator" 
            width="100%" 
            height="975" 
            frameBorder="0" 
            allowFullScreen="" 
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
            loading="lazy"
          ></iframe>

          <p className="ebc-platform-text">Listen on your favorite platform:</p>

          <div className="ebc-streaming-links">
            {albumData.spotifyLink && (
              <a
                href={albumData.spotifyLink}
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Listen on Spotify"
                onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
                  service: 'spotify', 
                  album: 'even_better_christmas',
                  page_path: '/even-better-christmas',
                  page_title: 'Even Better Christmas - Gracechase',
                  element_position: 'streaming_link_1',
                  content_type: 'album_page'
                })}
              >
                <img src="images/link-icons/Alt Streaming Service Icons/Spotify_Primary_Logo_RGB_Green.png?v=2" alt="Spotify" />
              </a>
            )}
            {albumData.youtubeMusicLink && (
              <a
                href={albumData.youtubeMusicLink}
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Listen on YouTube Music"
                onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
                  service: 'youtube_music', 
                  album: 'even_better_christmas',
                  page_path: '/even-better-christmas',
                  page_title: 'Even Better Christmas - Gracechase',
                  element_position: 'streaming_link_2',
                  content_type: 'album_page'
                })}
              >
                <img src="images/link-icons/YT_music_logo.png" alt="YouTube Music" />
              </a>
            )}
            {albumData.appleMusicLink && (
              <a
                href={albumData.appleMusicLink}
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Listen on Apple Music"
                onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
                  service: 'apple_music', 
                  album: 'even_better_christmas',
                  page_path: '/even-better-christmas',
                  page_title: 'Even Better Christmas - Gracechase',
                  element_position: 'streaming_link_3',
                  content_type: 'album_page'
                })}
              >
                <img src="images/link-icons/Alt Streaming Service Icons/music.cce3eb3f.svg" alt="Apple Music" />
              </a>
            )}
            {albumData.amazonMusicLink && (
              <a
                href={albumData.amazonMusicLink}
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Listen on Amazon Music"
                onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
                  service: 'amazon_music', 
                  album: 'even_better_christmas',
                  page_path: '/even-better-christmas',
                  page_title: 'Even Better Christmas - Gracechase',
                  element_position: 'streaming_link_4',
                  content_type: 'album_page'
                })}
              >
                <img src="images/link-icons/amazon_music_logo.png" alt="Amazon Music" />
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EvenBetterChristmas;
