import { useEffect, useMemo } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { getSpotlight, holidayGallery, holidayImages } from '../data/catalog.js';
import SiteNav from './SiteNav.jsx';
import SiteFooter from './SiteFooter.jsx';
import PlatformPicker from './PlatformPicker.jsx';
import SpotifyPreview from './SpotifyPreview.jsx';
import ReleaseHero from './ReleaseHero.jsx';
import { releaseKind } from '../utils/releaseKind.js';
import CatalogShelf from './CatalogShelf.jsx';
import AboutSection from './AboutSection.jsx';
import FavoriteMoments from './FavoriteMoments.jsx';

function heroEyebrow(release) {
  const kind = releaseKind(release).toLowerCase();
  return release.holiday ? `New Christmas ${kind} · ${release.year}` : `Latest ${kind} · ${release.year}`;
}

function HolidayHero({ release }) {
  return (
    <section className="gc-hero gc-hero--photo" aria-labelledby="gc-hero-title">
      <div className="gc-hero__media">
        <img src={holidayImages.banner} alt={holidayImages.bannerAlt} width="2400" height="595" fetchPriority="high" />
      </div>
      <div className="gc-hero__body gc-hero__body--photo">
        <div className="gc-hero__copy">
          <p className="gc-eyebrow">{heroEyebrow(release)}</p>
          <h1 id="gc-hero-title" className="gc-display">{release.title}</h1>
          <p className="gc-hero__blurb">{release.blurb}</p>
          <PlatformPicker release={release} />
          <Link to={`/album/${release.slug}`} className="gc-textlink">
            Track list and details <span aria-hidden="true">→</span>
          </Link>
        </div>
        <div className="gc-hero__aside">
          <SpotifyPreview release={release} />
        </div>
      </div>
    </section>
  );
}

function Companions({ releases, holiday }) {
  return (
    <section className="gc-section gc-companions" aria-labelledby="gc-companions-title">
      <h2 id="gc-companions-title" className="gc-eyebrow gc-companions__title">
        {holiday ? 'Also this Christmas' : 'Also recently'}
      </h2>
      <ul className="gc-companions__list">
        {releases.map((release) => (
          <li key={release.slug}>
            <Link to={`/album/${release.slug}`} className="gc-companion">
              <img src={release.cover} alt="" width="600" height="600" loading="lazy" />
              <span className="gc-companion__text">
                <span className="gc-companion__meta">{releaseKind(release)} · {release.year}</span>
                <span className="gc-companion__title">{release.title}</span>
                <span className="gc-companion__blurb">{release.blurb}</span>
                <span className="gc-companion__cta">Listen <span aria-hidden="true">→</span></span>
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

function HolidayGallery() {
  return (
    <>
      <section className="gc-section gc-gallery" aria-labelledby="gc-gallery-title">
        <div className="gc-section__head">
          <h2 id="gc-gallery-title" className="gc-h2">Christmas with Gracechase</h2>
        </div>
        <ul className="gc-gallery__grid">
          {holidayGallery.map((photo) => (
            <li key={photo.src}>
              <img src={photo.src} alt={photo.alt} width="1600" height="1195" loading="lazy" />
            </li>
          ))}
        </ul>
      </section>
      <div className="gc-window">
        <div className="gc-window__pane">
          <img src={holidayImages.fireside} alt={holidayImages.firesideAlt} width="2400" height="595" loading="lazy" />
          <span className="gc-window__frost" aria-hidden="true" />
        </div>
      </div>
    </>
  );
}

export default function HomePage() {
  const location = useLocation();
  const spotlight = useMemo(() => getSpotlight(), []);
  const { holiday, hero, also } = spotlight;

  useEffect(() => {
    const target = location.state?.scrollTo;
    if (!target) return;
    const frame = requestAnimationFrame(() => {
      if (target === 'top') {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return;
      }
      document.getElementById(target)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    return () => cancelAnimationFrame(frame);
  }, [location.key, location.state]);

  return (
    <div className={`gc gc-home ${holiday ? 'gc--holiday' : 'gc--offseason'}`}>
      <SiteNav overlay />
      <main>
        {holiday ? (
          <HolidayHero release={hero} />
        ) : (
          <ReleaseHero release={hero} eyebrow={heroEyebrow(hero)} showDetailsLink />
        )}

        <Companions releases={also} holiday={holiday} />

        {holiday ? <HolidayGallery /> : <FavoriteMoments />}

        <section className="gc-section gc-music" id="music" aria-labelledby="gc-music-title">
          <div className="gc-section__head">
            <h2 id="gc-music-title" className="gc-h2">All music</h2>
            <p className="gc-section__sub">Tap a cover to listen.</p>
          </div>
          <CatalogShelf holiday={holiday} />
        </section>

        <AboutSection />
      </main>
      <SiteFooter />
    </div>
  );
}
