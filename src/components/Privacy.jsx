import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Privacy.css';

// Simple helper to read a cookie value by name
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return undefined;
}

const Privacy = () => {
  const [gaOptedOut, setGaOptedOut] = useState(false);

  useEffect(() => {
    const gaId = import.meta.env.VITE_GA_MEASUREMENT_ID;
    if (!gaId) return; // no GA configured
    const cookieVal = getCookie(`ga-disable-${gaId}`);
    setGaOptedOut(!!cookieVal);
  }, []);

  // Ensure the page starts at the very top when this component mounts
  useEffect(() => {
    try {
      window.scrollTo({ top: 0, left: 0 });
      // extra reset for edge cases
      document.documentElement.scrollTop = 0;
      document.body.scrollTop = 0;
    } catch (err) {
      // ignore in non-browser environments
    }
  }, []);

  const handleGAOptOut = () => {
    const gaId = import.meta.env.VITE_GA_MEASUREMENT_ID;
    if (!gaId) return;
    // Set a 1-year cookie to disable GA on this browser for this site
    document.cookie = `ga-disable-${gaId}=true; path=/; max-age=31536000; SameSite=Lax`;
    setGaOptedOut(true);
    alert('You have opted out of Google Analytics on this browser.');
  };

  return (
    <div className="privacy-page">
      <div className="privacy-content-wrapper">
        <Link to="/" className="home-link">← Back to Home</Link>
        <header className="privacy-header">
          <h1>Privacy Policy</h1>
          <p>Last updated: November 9, 2025</p>
        </header>
        <section className="privacy-content">
          <div className="privacy-section">
            <h2>Who We Are</h2>
            <p>
              Gracechase shares music, news, and updates. This policy explains our data practices and your options.
            </p>
          </div>

          <div className="privacy-section">
            <h2>What We Collect</h2>
            <ul>
              <li>
                Site analytics: We use Google Analytics 4 (GA4) to measure visits, pages, and general usage. GA4 collects device/browser information, approximate location (based on IP), and event data like page views, clicks, button interactions, and navigation paths. We track which links and buttons you click to understand how you use the site and which content is most engaging. GA4 is configured to minimize unnecessary identifiers for this site.
              </li>
              <li>
                Advertising and conversion signals: We use the Twitter/X pixel and Meta (Facebook) pixel to measure ad performance and conversions (e.g., newsletter signups). These may allow Twitter and Meta to link visits to logged-in users for ad personalization according to their settings.
              </li>
              <li>
                Newsletter data: If you subscribe, we store your email and interests (categories you pick) securely in our database. We use this only for managing your subscription.
              </li>
              <li>
                Contact messages: If you contact us, we receive what you send, along with basic metadata like your IP address and timestamp, to help deliver and respond to your message.
              </li>
            </ul>
          </div>

          <div className="privacy-section">
            <h2>How We Use Data</h2>
            <ul>
              <li>Operate and improve the site and content.</li>
              <li>Measure reach and effectiveness of pages, links, campaigns, and individual buttons/features.</li>
              <li>Understand user behavior and preferences to improve user experience.</li>
              <li>Send newsletters or updates you requested.</li>
              <li>Detect and prevent abuse or errors.</li>
            </ul>
          </div>

          <div className="privacy-section">
            <h2>Cookies and Similar Technologies</h2>
            <p>
              GA4, Twitter/X pixel, and Meta (Facebook) pixel use cookies or similar storage to work. We show a consent banner for non-essential cookies (analytics and ads). You can block or delete cookies in your browser. We do not store your email in cookies or localStorage. We minimize cookies and only use them for analytics/ads and your GA opt-out preference.
            </p>
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {gaOptedOut ? (
                <button disabled style={{ padding: '0.5rem 1rem', backgroundColor: '#cccccc', color: '#666', border: 'none', borderRadius: 4 }}>
                  Google Analytics is disabled
                </button>
              ) : (
                <button onClick={handleGAOptOut} style={{ padding: '0.5rem 1rem', backgroundColor: '#D4AF37', color: '#000', border: 'none', borderRadius: 4, cursor: 'pointer' }}>
                  Opt out of Google Analytics
                </button>
              )}
              <a
                href="https://myadcenter.google.com/"
                target="_blank"
                rel="noopener noreferrer"
                style={{ padding: '0.5rem 1rem', border: '1px solid #D4AF37', borderRadius: 4, color: '#D4AF37', textDecoration: 'none' }}
              >
                Google ad controls
              </a>
              <a
                href="https://help.twitter.com/en/safety-and-security/privacy-controls-for-tailored-ads"
                target="_blank"
                rel="noopener noreferrer"
                style={{ padding: '0.5rem 1rem', border: '1px solid #D4AF37', borderRadius: 4, color: '#D4AF37', textDecoration: 'none' }}
              >
                Twitter/X ad settings
              </a>
              <a
                href="https://www.facebook.com/privacy/policy/"
                target="_blank"
                rel="noopener noreferrer"
                style={{ padding: '0.5rem 1rem', border: '1px solid #D4AF37', borderRadius: 4, color: '#D4AF37', textDecoration: 'none' }}
              >
                Meta privacy policy
              </a>
            </div>
          </div>

          <div className="privacy-section">
            <h2>Newsletter and Unsubscribe</h2>
            <p>
              When you subscribe, we store your email and interests securely in our database. If you unsubscribe, we delete your record(s) associated with that email within 24 hours and send a confirmation email. You can unsubscribe anytime on the <Link to="/unsubscribe">Unsubscribe</Link> page. We do not sell your email.
            </p>
            <p>
              <strong>Questions about how we use your newsletter data?</strong> You can contact us at any time via our <Link to="/contact">contact form</Link> or email contact.gracechase@gmail.com and we will respond to your inquiry.
            </p>
          </div>

          <div className="privacy-section">
            <h2>Sharing</h2>
            <p>
              We share limited data with service providers who help us run the site:
            </p>
            <ul>
              <li>Google Analytics (Google LLC) for usage analytics.</li>
              <li>Twitter/X for conversion tracking and ad attribution.</li>
              <li>Meta (Facebook) for conversion tracking and ad attribution.</li>
              <li>AWS (Amazon Web Services, Inc.) to host and store newsletter data and site services.</li>
            </ul>
            <p>
              These providers process data under their own privacy terms. We do not sell personal information.
            </p>
          </div>

          <div className="privacy-section">
            <h2>Legal Bases and Your Rights</h2>
            <p>
              Depending on where you live, you may have rights under laws like GDPR (EEA/UK) and CCPA/CPRA (California). Our typical legal bases are consent (for analytics/ads cookies) and legitimate interests (for basic site security), and contract/consent for sending newsletters you request.
            </p>
            <ul>
              <li>Access, correct, or delete personal data we hold about you.</li>
              <li>Object to or restrict certain processing (e.g., analytics/ads).</li>
              <li>Withdraw consent at any time (e.g., use the GA opt-out button above).</li>
            </ul>
            <p>
              To exercise rights, contact us and we’ll respond as required by law. If you’re in the EEA/UK, you may also lodge a complaint with your local data protection authority.
            </p>
          </div>

          <div className="privacy-section">
            <h2>Data Retention</h2>
            <p>
              Newsletter data: kept until you unsubscribe. If you interact with our emails or links, we may extend retention to keep your subscription active. Analytics data: up to 14 months (GA4 default). Contact data: up to 30 days after responding.
            </p>
          </div>

          <div className="privacy-section">
            <h2>Security</h2>
            <p>
              We use AWS encryption for data at rest and in transit, along with IAM roles to control access to our database and services.
            </p>
          </div>

          <div className="privacy-section">
            <h2>Children</h2>
            <p>
              This site is not directed to children under 13, and we do not knowingly collect personal information from them.
            </p>
          </div>

          <div className="privacy-section">
            <h2>International Transfers</h2>
            <p>
              Data may be processed in the United States and other countries where our providers operate. For EEA/UK users, we use Standard Contractual Clauses to protect your data during transfers.
            </p>
          </div>

          <div className="privacy-section">
            <h2>Changes to This Policy</h2>
            <p>
              We may update this policy to reflect changes to our practices or for legal reasons. We’ll update the “Last updated” date above. For significant changes, we’ll notify you via email (if subscribed) or a banner on the site.
            </p>
          </div>

          <div className="privacy-section">
            <h2>Contact</h2>
            <p>
              Questions or requests about privacy? <Link to="/contact">Send us a message</Link> or email contact.gracechase@gmail.com.
            </p>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Privacy;