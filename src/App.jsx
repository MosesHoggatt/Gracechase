import { useEffect } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import Blog from './components/Blog.jsx';
import BlogPost from './components/BlogPost.jsx';
import Privacy from './components/Privacy.jsx';
import Contact from './components/Contact.jsx';
import NewsletterSignup from './components/NewsletterSignup.jsx';
import Unsubscribe from './components/Unsubscribe.jsx';
import LetMyHeartFindChristmas from './components/LetMyHeartFindChristmas.jsx';
import HomePage from './components/HomePage.jsx';
import AlbumPage from './components/AlbumPage.jsx';
import SiteNav from './components/SiteNav.jsx';
import SiteFooter from './components/SiteFooter.jsx';
import './App.css';

function Subpage({ children }) {
  return (
    <div className="gc-subpage">
      <SiteNav />
      {children}
      <SiteFooter />
    </div>
  );
}

function App() {
  const location = useLocation();

  useEffect(() => {
    if (!location.state?.scrollTo) {
      window.scrollTo(0, 0);
    }
  }, [location.pathname, location.state]);

  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/album/:slug" element={<AlbumPage />} />
      <Route path="/even-better-christmas" element={<AlbumPage slug="even-better-christmas" />} />
      <Route path="/let-my-heart-find-christmas" element={<LetMyHeartFindChristmas />} />
      <Route path="/blog" element={<Subpage><Blog /></Subpage>} />
      <Route path="/blog/:id" element={<Subpage><BlogPost /></Subpage>} />
      <Route path="/privacy" element={<Subpage><Privacy /></Subpage>} />
      <Route path="/contact" element={<Subpage><Contact /></Subpage>} />
      <Route path="/newsletter" element={<Subpage><NewsletterSignup /></Subpage>} />
      <Route path="/unsubscribe" element={<Subpage><Unsubscribe /></Subpage>} />
    </Routes>
  );
}

export default App;
