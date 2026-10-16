import { Link } from 'react-router-dom';
import { releases } from '../data/catalog.js';
import { releaseKind } from '../utils/releaseKind.js';

export default function CatalogShelf({ holiday, currentSlug }) {
  const items = currentSlug ? releases.filter((r) => r.slug !== currentSlug) : releases;

  return (
    <ul className="gc-shelf">
      {items.map((release) => (
        <li key={release.slug}>
          <Link to={`/album/${release.slug}`} className="gc-shelf__item">
            <span className="gc-shelf__art">
              <img src={release.cover} alt="" loading="lazy" width="600" height="600" />
              {holiday && release.holiday && <span className="gc-tag" aria-hidden="true">Holiday</span>}
            </span>
            <span className="gc-shelf__title">{release.title}</span>
            <span className="gc-shelf__meta">
              {release.year} · {releaseKind(release)}
              {holiday && release.holiday && <span className="gc-sr-only"> · Holiday</span>}
            </span>
          </Link>
        </li>
      ))}
    </ul>
  );
}
