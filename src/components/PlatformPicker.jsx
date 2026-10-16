import { useState } from 'react';
import { PLATFORM_STORAGE_KEY, availablePlatforms } from '../data/catalog.js';

function readRemembered() {
  try {
    return window.localStorage.getItem(PLATFORM_STORAGE_KEY);
  } catch {
    return null;
  }
}

function remember(id) {
  try {
    window.localStorage.setItem(PLATFORM_STORAGE_KEY, id);
  } catch {
    // Private mode or storage disabled: the choice just won't persist.
  }
}

function trackClick(service, slug) {
  if (typeof window.gtag === 'function') {
    window.gtag('event', 'music_service_click', {
      service,
      release: slug,
      page_path: window.location.pathname,
    });
  }
}

export default function PlatformPicker({ release }) {
  const options = availablePlatforms(release);
  const [rememberedId, setRememberedId] = useState(readRemembered);
  const [choosing, setChoosing] = useState(false);

  if (options.length === 0) return null;

  const remembered = options.find((p) => p.id === rememberedId);

  const handleClick = (platform) => {
    remember(platform.id);
    setRememberedId(platform.id);
    setChoosing(false);
    trackClick(platform.id, release.slug);
  };

  if (remembered && !choosing) {
    return (
      <div className="gc-picker gc-picker--remembered">
        <a
          className="gc-play"
          href={release.links[remembered.id]}
          target="_blank"
          rel="noopener noreferrer"
          onClick={() => handleClick(remembered)}
        >
          <span className="gc-play__logo">
            <img src={remembered.icon} alt="" width="28" height="28" />
          </span>
          <span className="gc-play__label">
            Play on {remembered.label}<span className="gc-sr-only">: {release.title} (opens in a new tab)</span>
          </span>
        </a>
        {options.length > 1 && (
          <button type="button" className="gc-picker__change" onClick={() => setChoosing(true)}>
            Listen on another app
          </button>
        )}
      </div>
    );
  }

  return (
    <div className="gc-picker">
      <p className="gc-picker__prompt" id={`gc-picker-${release.slug}`}>
        Listen on your app
      </p>
      <ul className="gc-picker__grid" aria-labelledby={`gc-picker-${release.slug}`}>
        {options.map((platform) => (
          <li key={platform.id}>
            <a
              className="gc-service"
              href={release.links[platform.id]}
              target="_blank"
              rel="noopener noreferrer"
              onClick={() => handleClick(platform)}
            >
              <img className="gc-service__logo" src={platform.icon} alt="" width="32" height="32" />
              <span className="gc-service__label">
                {platform.label}<span className="gc-sr-only">: listen to {release.title} (opens in a new tab)</span>
              </span>
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
