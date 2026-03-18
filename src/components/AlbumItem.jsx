import './AlbumItem.css'; 

const AlbumItem = ({ spotifyLink, youtubeMusicLink, appleMusicLink, amazonMusicLink }) => {
  const getAlbumId = (link) => {
    if (!link) return null;
    const match = link.match(/album\/([a-zA-Z0-9]+)/);
    return match ? match[1] : null;
  };

  const albumId = getAlbumId(spotifyLink);

  return (
      <div className="album-container"> 
        {albumId && (
          <iframe data-testid="embed-iframe" className="spotify-embed" style={{borderRadius: '12px'}} src={`https://open.spotify.com/embed/album/${albumId}?utm_source=generator`} width="100%" height="352" frameBorder="0" allowFullScreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        )}
        <div className="streaming-links">
          {spotifyLink && (
            <a href={spotifyLink} target="_blank" rel="noopener noreferrer" aria-label="Listen on Spotify" onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
              service: 'spotify',
              page_path: window.location.pathname,
              page_title: document.title,
              element_position: 'album_card_link_1',
              content_type: 'album_card'
            })}>
              <img src="images/link-icons/Alt Streaming Service Icons/Spotify_Primary_Logo_RGB_Green.png?v=2" alt="Spotify" />
            </a>
          )}
          {youtubeMusicLink && (
            <a href={youtubeMusicLink} target="_blank" rel="noopener noreferrer" aria-label="Listen on YouTube music" onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
              service: 'youtube_music',
              page_path: window.location.pathname,
              page_title: document.title,
              element_position: 'album_card_link_2',
              content_type: 'album_card'
            })}>
              <img src="images/link-icons/YT_music_logo.png" alt="YouTube Music" />
            </a>
          )}
          {appleMusicLink && (
            <a href={appleMusicLink} target="_blank" rel="noopener noreferrer" aria-label="Listen on Apple Music" onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
              service: 'apple_music',
              page_path: window.location.pathname,
              page_title: document.title,
              element_position: 'album_card_link_3',
              content_type: 'album_card'
            })}>
              <img src="images/link-icons/Alt Streaming Service Icons/music.cce3eb3f.svg" alt="Apple Music" />
            </a>
          )}
          {amazonMusicLink && (
            <a href={amazonMusicLink} target="_blank" rel="noopener noreferrer" aria-label="Listen on Amazon Music" onClick={() => window.gtag && window.gtag('event', 'music_service_click', { 
              service: 'amazon_music',
              page_path: window.location.pathname,
              page_title: document.title,
              element_position: 'album_card_link_4',
              content_type: 'album_card'
            })}>
              <img src="images/link-icons/amazon_music_logo.png" alt="Amazon Music" />
            </a>
          )}
        </div>
      </div>
  );
};

export default AlbumItem;