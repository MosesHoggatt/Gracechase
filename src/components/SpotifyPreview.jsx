import { spotifyAlbumId } from '../data/catalog.js';

export default function SpotifyPreview({ release }) {
  const albumId = spotifyAlbumId(release);
  if (!albumId) return null;

  return (
    <figure className="gc-preview">
      <figcaption className="gc-preview__label">Preview on Spotify</figcaption>
      <iframe
        title={`Spotify preview: ${release.title}`}
        src={`https://open.spotify.com/embed/album/${albumId}?utm_source=generator`}
        width="100%"
        height="152"
        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
        loading="lazy"
      />
    </figure>
  );
}
