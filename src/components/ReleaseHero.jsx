import { Link } from 'react-router-dom';
import PlatformPicker from './PlatformPicker.jsx';
import SpotifyPreview from './SpotifyPreview.jsx';

export default function ReleaseHero({ release, eyebrow, showDetailsLink = false }) {
  return (
    <section className="gc-hero gc-hero--cover" aria-labelledby="gc-hero-title">
      <div
        className="gc-hero__ambient"
        style={{ backgroundImage: `url("${release.cover}")` }}
        aria-hidden="true"
      />
      <div className="gc-hero__body gc-hero__body--cover">
        <img
          className="gc-hero__cover"
          src={release.cover}
          alt={`${release.title} cover art`}
          width="600"
          height="600"
          fetchPriority="high"
        />
        <div className="gc-hero__copy">
          <p className="gc-eyebrow">{eyebrow}</p>
          <h1 id="gc-hero-title" className="gc-display">{release.title}</h1>
          <p className="gc-hero__blurb">{release.blurb}</p>
          <PlatformPicker key={release.slug} release={release} />
          <SpotifyPreview release={release} />
          {showDetailsLink && (
            <Link to={`/album/${release.slug}`} className="gc-textlink">
              Track list and details <span aria-hidden="true">→</span>
            </Link>
          )}
        </div>
      </div>
    </section>
  );
}
