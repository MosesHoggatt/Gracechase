import { Link, useLocation } from 'react-router-dom';

export default function SiteNav({ overlay = false }) {
  const { pathname } = useLocation();
  const onHome = pathname === '/';

  return (
    <header className={`gc-nav${overlay ? ' gc-nav--overlay' : ''}`}>
      <nav className="gc-nav__inner" aria-label="Main">
        <Link to="/" className="gc-nav__brand" replace={onHome} state={onHome ? { scrollTo: 'top' } : undefined}>
          <img className="gc-nav__logo" src="images/brand/gracechase-logo.png" alt="Gracechase" />
        </Link>
        <ul className="gc-nav__links">
          <li>
            <Link to="/" state={{ scrollTo: 'music' }} replace={onHome}>Music</Link>
          </li>
          <li>
            <Link to="/" state={{ scrollTo: 'about' }} replace={onHome}>About</Link>
          </li>
          <li>
            <Link to="/newsletter" className="gc-nav__cta">Stay in touch</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
}
