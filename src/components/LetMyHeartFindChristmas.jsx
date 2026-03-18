import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import './LetMyHeartFindChristmas.css';

const LetMyHeartFindChristmas = () => {
  const songData = {
    spotifyLink: 'https://open.spotify.com/track/3oHzD0CBikEYjepCw0jSUR',
    amazonMusicLink: 'https://music.amazon.com/albums/B0FWZ9VRCF?marketplaceId=ATVPDKIKX0DER&musicTerritory=US&ref=dm_sh_YPp9Dcmls7KUynKPxZfcrZA6G&trackAsin=B0FWZD4RXG',
    appleMusicLink: 'https://music.apple.com/us/song/let-my-heart-find-christmas/1847634790',
    youtubeMusicLink: 'https://music.youtube.com/watch?v=ZU_5UIlvofo',
    youtubeVideoId: 'Z-NfhHJEkPY',
  };

  const albumData = {
    spotifyAlbumId: '0FDPRyIXg50LXOdgH8g65b',
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
    <div className="lmhfc-page">
      <div className="lmhfc-content-wrapper">

        {/* 2. Hero Video */}
        <div className="lmhfc-video-container">
          <iframe
            className="lmhfc-video"
            src={`https://www.youtube.com/embed/${songData.youtubeVideoId}?autoplay=1&mute=1&rel=0`}
            title="Let My Heart Find Christmas - Music Video"
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowFullScreen
          ></iframe>
        </div>

        {/* 3. Primary CTA */}
        <div className="lmhfc-primary-cta">
          <h2 className="lmhfc-cta-headline">SAVE/STREAM THIS SONG NOW</h2>
          
          <div className="lmhfc-streaming-buttons">
            {/* Spotify - largest/most prominent */}
            {songData.spotifyLink && (
              <a
                href={songData.spotifyLink}
                target="_blank"
                rel="noopener noreferrer"
                className="lmhfc-btn lmhfc-btn-spotify"
                onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
                  service: 'spotify', 
                  song: 'let_my_heart_find_christmas',
                  context: 'primary_cta',
                  page_path: '/let-my-heart-find-christmas',
                  page_title: 'Let My Heart Find Christmas - Gracechase',
                  element_position: 'button_1',
                  campaign_source: 'ad_campaign_lmhfc',
                  content_type: 'landing_page'
                })}
              >
                <div className="lmhfc-btn-icon">
                  <img src="images/link-icons/Alt Streaming Service Icons/Spotify_Primary_Logo_RGB_Green.png?v=2" alt="" />
                </div>
                <div className="lmhfc-btn-text">Listen on Spotify</div>
              </a>
            )}

            {/* Apple Music */}
            {songData.appleMusicLink && (
              <a
                href={songData.appleMusicLink}
                target="_blank"
                rel="noopener noreferrer"
                className="lmhfc-btn lmhfc-btn-apple"
                onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
                  service: 'apple_music', 
                  song: 'let_my_heart_find_christmas',
                  context: 'primary_cta',
                  page_path: '/let-my-heart-find-christmas',
                  page_title: 'Let My Heart Find Christmas - Gracechase',
                  element_position: 'button_2',
                  campaign_source: 'ad_campaign_lmhfc',
                  content_type: 'landing_page'
                })}
              >
                <div className="lmhfc-btn-icon">
                  <img src="images/link-icons/Alt Streaming Service Icons/music.cce3eb3f.svg" alt="" />
                </div>
                <div className="lmhfc-btn-text">Listen on Apple Music</div>
              </a>
            )}

            {/* Amazon Music */}
            {songData.amazonMusicLink && (
              <a
                href={songData.amazonMusicLink}
                target="_blank"
                rel="noopener noreferrer"
                className="lmhfc-btn lmhfc-btn-amazon"
                onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
                  service: 'amazon_music', 
                  song: 'let_my_heart_find_christmas',
                  context: 'primary_cta',
                  page_path: '/let-my-heart-find-christmas',
                  page_title: 'Let My Heart Find Christmas - Gracechase',
                  element_position: 'button_3',
                  campaign_source: 'ad_campaign_lmhfc',
                  content_type: 'landing_page'
                })}
              >
                <div className="lmhfc-btn-icon">
                  <img src="images/link-icons/amazon_music_logo.png" alt="" />
                </div>
                <div className="lmhfc-btn-text">Listen on Amazon Music</div>
              </a>
            )}
            
            {/* YouTube Music */}
            {songData.youtubeMusicLink && (
              <a
                href={songData.youtubeMusicLink}
                target="_blank"
                rel="noopener noreferrer"
                className="lmhfc-btn lmhfc-btn-youtube"
                onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
                  service: 'youtube_music', 
                  song: 'let_my_heart_find_christmas',
                  context: 'primary_cta',
                  page_path: '/let-my-heart-find-christmas',
                  page_title: 'Let My Heart Find Christmas - Gracechase',
                  element_position: 'button_4',
                  campaign_source: 'ad_campaign_lmhfc',
                  content_type: 'landing_page'
                })}
              >
                <div className="lmhfc-btn-icon">
                  <img src="images/link-icons/YT_music_logo.png" alt="" />
                </div>
                <div className="lmhfc-btn-text">Listen on YouTube Music</div>
              </a>
            )}
          </div>
        </div>

        {/* 4. Secondary Album Offer */}
        <div className="lmhfc-album-section">
          <h2 className="lmhfc-album-heading">EXPLORE THE FULL ALBUM</h2>
          
          <div className="lmhfc-album-content">
            <iframe
              className="lmhfc-album-embed"
              style={{borderRadius: '12px'}}
              src={`https://open.spotify.com/embed/album/${albumData.spotifyAlbumId}?utm_source=generator`}
              width="100%"
              height="975.333"
              frameBorder="0"
              allowFullScreen=""
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
              loading="lazy"
            ></iframe>
          </div>

          <div className="lmhfc-album-links">
            {albumData.spotifyLink && (
              <a
                href={albumData.spotifyLink}
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Stream album on Spotify"
                onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
                  service: 'spotify', 
                  album: 'even_better_christmas',
                  context: 'secondary_album_offer',
                  page_path: '/let-my-heart-find-christmas',
                  page_title: 'Let My Heart Find Christmas - Gracechase',
                  element_position: 'album_link_1',
                  campaign_source: 'ad_campaign_lmhfc',
                  content_type: 'landing_page'
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
                aria-label="Stream album on YouTube Music"
                onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
                  service: 'youtube_music', 
                  album: 'even_better_christmas',
                  context: 'secondary_album_offer',
                  page_path: '/let-my-heart-find-christmas',
                  page_title: 'Let My Heart Find Christmas - Gracechase',
                  element_position: 'album_link_2',
                  campaign_source: 'ad_campaign_lmhfc',
                  content_type: 'landing_page'
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
                aria-label="Stream album on Apple Music"
                onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
                  service: 'apple_music', 
                  album: 'even_better_christmas',
                  context: 'secondary_album_offer',
                  page_path: '/let-my-heart-find-christmas',
                  page_title: 'Let My Heart Find Christmas - Gracechase',
                  element_position: 'album_link_3',
                  campaign_source: 'ad_campaign_lmhfc',
                  content_type: 'landing_page'
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
                aria-label="Stream album on Amazon Music"
                onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
                  service: 'amazon_music', 
                  album: 'even_better_christmas',
                  context: 'secondary_album_offer',
                  page_path: '/let-my-heart-find-christmas',
                  page_title: 'Let My Heart Find Christmas - Gracechase',
                  element_position: 'album_link_4',
                  campaign_source: 'ad_campaign_lmhfc',
                  content_type: 'landing_page'
                })}
              >
                <img src="images/link-icons/amazon_music_logo.png" alt="Amazon Music" />
              </a>
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="lmhfc-footer">
          <div className="lmhfc-footer-content">
            <p>&copy; 2025 Gracechase. All rights reserved. |
              {' '}
              <Link to="/privacy">Privacy Policy</Link>
              {' '}|
              {' '}
              <Link to="/contact">Contact</Link>
              {' '}|
              {' '}
              <Link to="/">Home</Link>
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default LetMyHeartFindChristmas;
