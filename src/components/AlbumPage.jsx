import { useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getRelease, isHolidaySeason } from '../data/catalog.js';
import SiteNav from './SiteNav.jsx';
import SiteFooter from './SiteFooter.jsx';
import ReleaseHero from './ReleaseHero.jsx';
import { releaseKind } from '../utils/releaseKind.js';
import CatalogShelf from './CatalogShelf.jsx';

export default function AlbumPage({ slug: fixedSlug }) {
  const params = useParams();
  const slug = fixedSlug || params.slug;
  const release = getRelease(slug);

  useEffect(() => {
    document.title = release ? `${release.title} | Gracechase` : 'Not found | Gracechase';
    return () => {
      document.title = 'Gracechase';
    };
  }, [release]);

  if (!release) {
    return (
      <div className="gc gc-album">
        <SiteNav />
        <main className="gc-notfound">
          <h1 className="gc-h2">We couldn't find that release.</h1>
          <p>The link may be old or mistyped.</p>
          <Link to="/" className="gc-textlink">Go to the Gracechase home page <span aria-hidden="true">→</span></Link>
        </main>
        <SiteFooter />
      </div>
    );
  }

  const songs = `${release.trackCount} ${release.trackCount === 1 ? 'song' : 'songs'}`;

  return (
    <div className="gc gc-album">
      <SiteNav />
      <main>
        <ReleaseHero release={release} eyebrow={`${releaseKind(release)} · ${release.year} · ${songs}`} />

        {release.tracks.length > 1 && (
          <section className="gc-section gc-tracks" aria-labelledby="gc-tracks-title">
            <h2 id="gc-tracks-title" className="gc-eyebrow">Track list</h2>
            <ol className="gc-tracks__list">
              {release.tracks.map((track) => (
                <li key={track}>{track}</li>
              ))}
            </ol>
          </section>
        )}

        <section className="gc-section gc-music" aria-labelledby="gc-more-title">
          <div className="gc-section__head">
            <h2 id="gc-more-title" className="gc-h2">More from Gracechase</h2>
            <Link to="/" state={{ scrollTo: 'music' }} className="gc-textlink">
              Back to all music <span aria-hidden="true">→</span>
            </Link>
          </div>
          <CatalogShelf holiday={isHolidaySeason()} currentSlug={release.slug} />
        </section>
      </main>
      <SiteFooter />
    </div>
  );
}
