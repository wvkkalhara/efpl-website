/* EnerFab — site interactions */
(function () {
  document.documentElement.classList.remove('no-js');

  // Sticky header shadow
  var header = document.querySelector('.site-header');
  var onScroll = function () { if (header) header.classList.toggle('is-scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a') && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
  }

  // Solutions dropdown (click for touch + keyboard)
  document.querySelectorAll('.nav__drop > button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var drop = btn.parentElement;
      var open = drop.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open);
    });
  });
  document.addEventListener('click', function (e) {
    document.querySelectorAll('.nav__drop.is-open').forEach(function (d) {
      if (!d.contains(e.target) && window.innerWidth > 960) { d.classList.remove('is-open'); d.querySelector('button').setAttribute('aria-expanded', 'false'); }
    });
  });

  // Reveal on scroll
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  // Click-to-load YouTube (no third-party load until requested)
  document.querySelectorAll('.video[data-yt]').forEach(function (v) {
    var btn = v.querySelector('button');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + v.dataset.yt + '?autoplay=1&rel=0';
      f.title = v.dataset.title || 'EnerFab video';
      f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
      f.allowFullscreen = true;
      v.innerHTML = '';
      v.appendChild(f);
    });
  });

  // Gallery lightbox
  var dlg = document.querySelector('.lightbox');
  if (dlg && dlg.showModal) {
    var dImg = dlg.querySelector('img');
    var dCap = dlg.querySelector('p');
    document.querySelectorAll('.gallery button').forEach(function (b) {
      b.addEventListener('click', function () {
        var img = b.querySelector('img');
        dImg.src = b.dataset.full || img.src;
        dImg.alt = img.alt;
        dCap.textContent = img.alt;
        dlg.showModal();
      });
    });
    dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.closest('.lightbox__close')) dlg.close(); });
  }

  // Solutions sub-nav active state
  var sublinks = document.querySelectorAll('.subnav a');
  if (sublinks.length && 'IntersectionObserver' in window) {
    var map = {};
    sublinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          sublinks.forEach(function (a) { a.classList.remove('is-active'); });
          var a = map[en.target.id];
          if (a) { a.classList.add('is-active'); a.scrollIntoView({ block: 'nearest', inline: 'nearest' }); }
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) { var s = document.getElementById(id); if (s) so.observe(s); });
  }

  // Inquiry form: opens the visitor's email app with the message pre-filled.
  // To receive submissions directly, set data-endpoint on the form (e.g. a Formspree URL).
  document.querySelectorAll('form.js-inquiry').forEach(function (form) {
    var status = form.querySelector('.form__status');
    var want = new URLSearchParams(window.location.search).get('interest');
    var sel = form.querySelector('select[name="interest"]');
    if (want && sel) {
      Array.prototype.forEach.call(sel.options, function (o) { if (o.text.toLowerCase() === want.toLowerCase()) sel.value = o.value || o.text; });
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var d = new FormData(form);
      var endpoint = form.dataset.endpoint;
      var show = function (msg) { if (status) { status.textContent = msg; status.classList.add('is-visible'); } };
      if (endpoint) {
        fetch(endpoint, { method: 'POST', body: d, headers: { Accept: 'application/json' } })
          .then(function (r) { if (!r.ok) throw new Error(); form.reset(); show('Thank you — your inquiry has been sent. We will be in touch shortly.'); })
          .catch(function () { show('Sorry, something went wrong. Please email info@efpl.org or call +94 11 288 8821.'); });
        return;
      }
      var subject = 'Website inquiry' + (d.get('interest') ? ' — ' + d.get('interest') : '') + ' from ' + d.get('name');
      var body = [
        'Name: ' + d.get('name'),
        'Email: ' + d.get('email'),
        'Phone: ' + (d.get('phone') || '-'),
        d.get('company') ? 'Company: ' + d.get('company') : null,
        d.get('interest') ? 'Interested in: ' + d.get('interest') : null,
        '',
        d.get('message')
      ].filter(function (x) { return x !== null; }).join('\n');
      window.location.href = 'mailto:info@efpl.org?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      show('Your email app should open with the message ready to send. If it does not, write to info@efpl.org.');
    });
  });

  // Footer year
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
