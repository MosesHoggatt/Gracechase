// Simple GA4 outbound link tracking
export function initOutboundLinkTracking() {
  if (typeof window === 'undefined') return;
  if (window.__outboundTrackingInit) return;
  window.__outboundTrackingInit = true;

  const handler = (event) => {
    try {
      const anchor = event.target && event.target.closest ? event.target.closest('a') : null;
      if (!anchor) return;

      const href = anchor.getAttribute('href');
      if (!href) return;

      // Resolve absolute URL and check if external
      const url = new URL(href, window.location.href);
      const isExternal = /^https?:/i.test(url.href) && url.host !== window.location.host;
      if (!isExternal) return;

      const label =
        anchor.getAttribute('aria-label')?.trim() ||
        (anchor.textContent || '').trim() ||
        (anchor.querySelector('img')?.getAttribute('alt') || '').trim();

      if (window.gtag) {
        window.gtag('event', 'outbound_click', {
          link_url: url.href,
          link_domain: url.hostname,
          link_text: label,
          transport_type: 'beacon',
        });
      }
    } catch (e) {
      // swallow errors to avoid interrupting navigation
    }
  };

  document.addEventListener('click', handler, true);
}
