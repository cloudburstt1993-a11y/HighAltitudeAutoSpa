// High Altitude Auto Spa: site script. Vanilla, defer-loaded on every page.

// GA4 Measurement ID (G-XXXXXXXXXX). Analytics stays off until this is filled in.
const GA4_ID = '[GA4_ID]';

function track(name, params) {
  if (typeof window.gtag === 'function') window.gtag('event', name, params);
}

if (/^G-[A-Z0-9]+$/.test(GA4_ID)) {
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () {
    window.dataLayer.push(arguments);
  };
  window.gtag('js', new Date());
  window.gtag('config', GA4_ID);
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA4_ID;
  document.head.append(s);
}

// A tap on the phone number is a conversion. data-call says which link it was (hero, header, mobile-bar...).
document.addEventListener('click', (e) => {
  const link = e.target.closest('a[href^="tel:"]');
  if (link) track('click_to_call', { link_location: link.dataset.call || 'other' });
});

// Mobile menu
const toggle = document.querySelector('[data-nav-toggle]');
const nav = document.querySelector('[data-nav]');
if (toggle && nav) {
  const setOpen = (open) => {
    toggle.setAttribute('aria-expanded', String(open));
    nav.toggleAttribute('data-open', open);
  };
  toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', (e) => {
    if (e.target.closest('a')) setOpen(false);
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      toggle.focus();
    }
  });
}

document.querySelectorAll('[data-year]').forEach((el) => {
  el.textContent = new Date().getFullYear();
});

// Quote form → Formspree, with an in-page confirmation instead of a trip to formspree.io.
// Without JS the form still posts normally and Formspree shows its own thank-you page.
const form = document.querySelector('[data-quote-form]');
if (form) {
  const success = document.querySelector('[data-form-success]');
  const error = form.querySelector('[data-form-error]');
  const button = form.querySelector('[type="submit"]');
  const label = button.textContent;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    error.hidden = true;
    button.disabled = true;
    button.textContent = 'Sending…';
    try {
      const res = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' },
      });
      if (!res.ok) throw new Error('Formspree responded ' + res.status);
      track('generate_lead', { form_name: 'quote', service: form.elements.service.value });
      form.hidden = true;
      success.hidden = false;
      success.focus();
    } catch {
      error.hidden = false;
      button.disabled = false;
      button.textContent = label;
    }
  });
}
