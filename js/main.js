/* EnerFab — site interactions and motion.
   Motion uses GSAP + ScrollTrigger + SplitText and Lenis smooth scrolling
   (self-hosted in /js/vendor). Everything degrades to a static, fully
   readable page if those fail to load or the visitor prefers reduced motion. */
(function () {
  'use strict';
  var root = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(pointer: fine)').matches;
  var hasGsap = !!(window.gsap && window.ScrollTrigger);
  if (!hasGsap || reduce) root.classList.remove('motion');
  var motion = root.classList.contains('motion');

  /* ---------- header: solid after scroll, hides on scroll down ---------- */
  var header = document.querySelector('.site-header');
  var nav = document.getElementById('nav');
  var lastY = 0;
  function onScroll(y) {
    if (!header) return;
    header.classList.toggle('is-scrolled', y > 20);
    var hide = y > 400 && y > lastY + 4 && !(nav && nav.classList.contains('is-open'));
    if (y < lastY - 4 || y < 400) hide = false;
    if (Math.abs(y - lastY) > 4) {
      header.classList.toggle('is-hidden', hide);
      root.classList.toggle('header-hidden', hide);
      lastY = y;
    }
  }

  /* ---------- mobile menu ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var lenis = null;
  function setMenu(open) {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.style.overflow = open ? 'hidden' : '';
    if (lenis) open ? lenis.stop() : lenis.start();
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () { setMenu(!nav.classList.contains('is-open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a') && nav.classList.contains('is-open')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('is-open')) { setMenu(false); toggle.focus(); } });
  }
  document.querySelectorAll('.nav__drop > button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var open = btn.parentElement.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(open));
    });
  });
  document.addEventListener('click', function (e) {
    document.querySelectorAll('.nav__drop.is-open').forEach(function (d) {
      if (!d.contains(e.target) && window.innerWidth > 1080) { d.classList.remove('is-open'); d.querySelector('button').setAttribute('aria-expanded', 'false'); }
    });
  });

  /* ---------- YouTube facade: nothing loads from YouTube until play ---------- */
  document.querySelectorAll('.video[data-yt]').forEach(function (v) {
    var btn = v.querySelector('button');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(v.dataset.yt) + '?autoplay=1&rel=0';
      f.title = v.dataset.title || 'EnerFab video';
      f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
      f.allowFullscreen = true;
      v.innerHTML = '';
      v.appendChild(f);
    });
  });

  /* ---------- lightboxes ---------- */
  var dlg = document.querySelector('.lightbox[data-gallery]');
  if (dlg && dlg.showModal) {
    var dImg = dlg.querySelector('img'), dCap = dlg.querySelector('p');
    document.querySelectorAll('.gallery button').forEach(function (b) {
      b.addEventListener('click', function () {
        var img = b.querySelector('img');
        dImg.src = img.currentSrc || img.src; dImg.alt = img.alt; dCap.textContent = img.alt;
        dlg.showModal();
      });
    });
  }
  document.querySelectorAll('[data-open]').forEach(function (b) {
    var d = document.getElementById(b.dataset.open);
    if (d && d.showModal) b.addEventListener('click', function () { d.showModal(); });
  });
  document.querySelectorAll('.lightbox').forEach(function (d) {
    d.addEventListener('click', function (e) { if (e.target === d || e.target.closest('.lightbox__close')) d.close(); });
  });

  /* ---------- before / after sliders ---------- */
  document.querySelectorAll('.ba').forEach(function (ba) {
    var r = ba.querySelector('input');
    var set = function () { ba.style.setProperty('--pos', r.value + '%'); };
    r.addEventListener('input', function () { ba.dataset.touched = '1'; set(); });
    set();
  });

  /* ---------- solutions sub-nav highlighting ---------- */
  var sublinks = document.querySelectorAll('.subnav a[href^="#"]');
  if (sublinks.length && 'IntersectionObserver' in window) {
    var map = {};
    sublinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        sublinks.forEach(function (a) { a.classList.remove('is-active'); });
        var a = map[en.target.id];
        if (a) { a.classList.add('is-active'); a.scrollIntoView({ block: 'nearest', inline: 'nearest' }); }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) { var s = document.getElementById(id); if (s) so.observe(s); });
  }

  /* ---------- inquiry form (posts to /api/inquiry, a Cloudflare Pages Function) ---------- */
  document.querySelectorAll('form.js-inquiry').forEach(function (form) {
    var status = form.querySelector('.form__status');
    var submit = form.querySelector('[type="submit"]');
    var want = new URLSearchParams(window.location.search).get('interest');
    var sel = form.querySelector('select[name="interest"]');
    if (want && sel) Array.prototype.forEach.call(sel.options, function (o) { if (o.text.toLowerCase() === want.toLowerCase()) sel.value = o.value || o.text; });
    var show = function (msg) { if (status) { status.textContent = msg; status.classList.add('is-visible'); } };
    var qs = new URLSearchParams(window.location.search);
    if (qs.get('sent')) show('Thank you. Your inquiry has been sent and our engineers will be in touch.');
    if (qs.get('error')) show('Your inquiry could not be sent. Please email info@enerfab.lk or call +94 11 288 8821.');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var d = new FormData(form);
      if (window.turnstile && !d.get('cf-turnstile-response')) { show('Please complete the security check above the button, then send again.'); return; }
      submit.disabled = true;
      show('Sending…');
      fetch(form.action, { method: 'POST', body: d, headers: { Accept: 'application/json' }, credentials: 'same-origin' })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || !j.ok) throw new Error(j.error || 'failed'); }); })
        .then(function () { form.reset(); show('Thank you. Your inquiry has been sent and our engineers will be in touch.'); if (window.turnstile) window.turnstile.reset(); })
        .catch(function (err) {
          show((err && err.message && err.message !== 'failed' ? err.message + ' ' : '') + 'If it keeps failing, email info@enerfab.lk or call +94 11 288 8821.');
          if (window.turnstile) window.turnstile.reset();
        })
        .then(function () { submit.disabled = false; });
    });
  });

  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ======================= MOTION ======================= */
  if (!motion) {
    window.addEventListener('scroll', function () { onScroll(window.scrollY); }, { passive: true });
    onScroll(window.scrollY);
    document.querySelectorAll('.hrail').forEach(function (h) { h.classList.add('hrail--native'); });
    return;
  }

  // Wait for web fonts (max 1.5 s) so split lines match the final layout.
  var fontsReady = document.fonts && document.fonts.ready ? Promise.race([document.fonts.ready, new Promise(function (r) { setTimeout(r, 1500); })]) : Promise.resolve();
  fontsReady.then(startMotion);
  function startMotion() {
  var gsap = window.gsap, ST = window.ScrollTrigger;
  gsap.registerPlugin(ST);
  if (window.SplitText) gsap.registerPlugin(window.SplitText);

  // Smooth scrolling on mouse/trackpad devices; native scrolling on touch.
  if (window.Lenis && finePointer) {
    lenis = new window.Lenis({ duration: 1.15, smoothWheel: true });
    lenis.on('scroll', function (e) { ST.update(); onScroll(e.scroll); });
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    document.querySelectorAll('a[href*="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var url = new URL(a.href, location.href);
        if (url.pathname !== location.pathname || !url.hash) return;
        var t = document.getElementById(url.hash.slice(1));
        if (!t) return;
        e.preventDefault();
        lenis.scrollTo(t, { offset: -100 });
        history.replaceState(null, '', url.hash);
      });
    });
  } else {
    window.addEventListener('scroll', function () { onScroll(window.scrollY); }, { passive: true });
  }
  onScroll(window.scrollY);

  var ease = 'expo.out';

  // Headlines: lines rise out of a mask. [data-split="load"] plays immediately.
  function splitLines(el) {
    if (!window.SplitText) return null;
    return window.SplitText.create(el, { type: 'lines', mask: 'lines', linesClass: 'line' });
  }
  document.querySelectorAll('[data-split]').forEach(function (el) {
    var s = splitLines(el);
    el.style.visibility = 'visible';
    if (!s) return;
    var tween = { yPercent: 110, duration: 1.3, ease: ease, stagger: 0.1 };
    if (el.dataset.split === 'load') gsap.from(s.lines, Object.assign(tween, { delay: 0.15 }));
    else gsap.from(s.lines, Object.assign(tween, { scrollTrigger: { trigger: el, start: 'top 88%' } }));
  });

  // Fade-up blocks, batched so groups stagger together.
  ST.batch('[data-reveal]', {
    start: 'top 90%',
    onEnter: function (els) { gsap.to(els, { opacity: 1, y: 0, duration: 1.1, ease: ease, stagger: 0.08, overwrite: true }); }
  });

  // Image mask reveals.
  gsap.utils.toArray('[data-mask]').forEach(function (el) {
    gsap.to(el, { clipPath: 'inset(0% 0% 0% 0% round 22px)', duration: 1.5, ease: ease, scrollTrigger: { trigger: el, start: 'top 85%' } });
    var img = el.querySelector('img');
    if (img) gsap.from(img, { scale: 1.25, duration: 1.8, ease: ease, scrollTrigger: { trigger: el, start: 'top 85%' } });
  });

  // Parallax.
  gsap.utils.toArray('[data-parallax]').forEach(function (el) {
    var amt = parseFloat(el.dataset.parallax) || 10;
    gsap.fromTo(el, { yPercent: -amt }, { yPercent: amt, ease: 'none', scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  // Statement: words light up as you scroll.
  document.querySelectorAll('.statement').forEach(function (el) {
    if (!window.SplitText) { el.classList.add('is-static'); return; }
    var s = window.SplitText.create(el, { type: 'words', wordsClass: 'w' });
    gsap.to(s.words, { opacity: 1, ease: 'none', stagger: 0.1, scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 45%', scrub: true } });
  });

  // Counters.
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var end = parseFloat(el.dataset.count), obj = { v: el.dataset.from ? parseFloat(el.dataset.from) : 0 };
    var fmt = function (n) { return el.dataset.plain ? String(Math.round(n)) : Math.round(n).toLocaleString('en-US'); };
    el.textContent = fmt(obj.v);
    gsap.to(obj, { v: end, duration: 2.2, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 90%' }, onUpdate: function () { el.textContent = fmt(obj.v); } });
  });

  // Timeline line fills as you read.
  document.querySelectorAll('.timeline__fill').forEach(function (f) {
    gsap.to(f, { scaleY: 1, ease: 'none', scrollTrigger: { trigger: f.parentElement, start: 'top 70%', end: 'bottom 60%', scrub: true } });
  });

  // Tour: step cards ease in, and the progress rail follows.
  var dots = document.querySelectorAll('.tour__progress i');
  gsap.utils.toArray('.tour .step').forEach(function (step, i) {
    var card = step.querySelector('.step__card');
    if (i > 0 && card) gsap.from(card.children, { y: 50, opacity: 0, duration: 1.1, ease: ease, stagger: 0.08, scrollTrigger: { trigger: step, start: 'top 65%' } });
    ST.create({ trigger: step, start: 'top center', end: 'bottom center', onToggle: function (self) { if (self.isActive) dots.forEach(function (d, j) { d.classList.toggle('is-on', j === i); }); } });
  });

  // Horizontal solutions rail: pinned on desktop, native swipe on touch.
  var mm = gsap.matchMedia();
  document.querySelectorAll('.hrail').forEach(function (rail) {
    var track = rail.querySelector('.hrail__track');
    mm.add('(min-width: 1081px) and (pointer: fine)', function () {
      var dist = function () { return Math.max(0, track.scrollWidth - window.innerWidth); };
      gsap.to(track, { x: function () { return -dist(); }, ease: 'none', scrollTrigger: { trigger: rail, start: 'center center', end: function () { return '+=' + dist(); }, pin: true, scrub: 0.6, invalidateOnRefresh: true, anticipatePin: 1 } });
    });
    mm.add('(max-width: 1080px), (pointer: coarse)', function () {
      rail.classList.add('hrail--native');
      return function () { rail.classList.remove('hrail--native'); };
    });
  });

  // Before/after slider sweeps once as it scrolls into view (until touched).
  document.querySelectorAll('.ba[data-sweep]').forEach(function (ba) {
    var r = ba.querySelector('input'), o = { v: 8 };
    gsap.to(o, { v: 72, ease: 'none', scrollTrigger: { trigger: ba, start: 'top 85%', end: 'bottom 35%', scrub: true }, onUpdate: function () { if (ba.dataset.touched) return; r.value = o.v; ba.style.setProperty('--pos', o.v + '%'); } });
  });

  // Page-hero background drifts slower than the page.
  var phbg = document.querySelector('.page-hero__bg');
  if (phbg) gsap.to(phbg, { yPercent: 14, ease: 'none', scrollTrigger: { trigger: '.page-hero', start: 'top top', end: 'bottom top', scrub: true } });

  // Footer wordmark slides in.
  var fw = document.querySelector('.footer-word');
  if (fw) gsap.from(fw, { yPercent: 40, opacity: 0, ease: 'none', scrollTrigger: { trigger: fw, start: 'top bottom', end: 'bottom 85%', scrub: true } });

  // Magnetic buttons (mouse only).
  if (finePointer) document.querySelectorAll('[data-magnetic]').forEach(function (b) {
    var xTo = gsap.quickTo(b, 'x', { duration: 0.6, ease: 'elastic.out(1, .4)' }), yTo = gsap.quickTo(b, 'y', { duration: 0.6, ease: 'elastic.out(1, .4)' });
    b.addEventListener('pointermove', function (e) { var r = b.getBoundingClientRect(); xTo((e.clientX - r.left - r.width / 2) * 0.3); yTo((e.clientY - r.top - r.height / 2) * 0.4); });
    b.addEventListener('pointerleave', function () { xTo(0); yTo(0); });
  });

  if (document.readyState === 'complete') ST.refresh(); else window.addEventListener('load', function () { ST.refresh(); });
  }
})();
