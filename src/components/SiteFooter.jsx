import { Link } from 'react-router-dom';

export default function SiteFooter() {
  return (
    <footer className="gc-footer">
      <p>
        &copy; {new Date().getFullYear()} Gracechase. All rights reserved.
      </p>
      <ul className="gc-footer__links">
        <li><Link to="/privacy">Privacy Policy</Link></li>
        <li><Link to="/contact">Contact</Link></li>
      </ul>
    </footer>
  );
}
