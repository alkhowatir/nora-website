/* Nora AlSaud — site behaviour. No dependencies. Progressive: the site is fully readable without JS. */
(() => {
  'use strict';
  const d = document, root = d.documentElement;
  const $ = (s, c = d) => c.querySelector(s);
  const $$ = (s, c = d) => [...c.querySelectorAll(s)];
  const rtl = root.dir === 'rtl';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let L = {};
  try { L = JSON.parse($('#i18n').textContent); } catch (e) { /* defaults below */ }
  const raf = (fn) => { let t = false; return (...a) => { if (t) return; t = true; requestAnimationFrame(() => { t = false; fn(...a); }); }; };

  /* ---- Theme (initial value is set by the inline <head> script → no flash) ---- */
  const KEY = 'nora-theme';
  const tbtn = $('.theme-toggle');
  const metaTheme = $('meta[name="theme-color"]');
  const syncTheme = () => {
    const dark = root.dataset.theme === 'dark';
    if (tbtn) tbtn.setAttribute('aria-checked', String(dark));
    if (metaTheme) metaTheme.setAttribute('content', dark ? '#0a0c0e' : '#e9e5dc');
  };
  if (tbtn) {
    tbtn.addEventListener('click', () => {
      const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
      root.classList.add('theme-anim');
      root.dataset.theme = next;
      try { localStorage.setItem(KEY, next); } catch (e) { /* storage may be blocked */ }
      syncTheme();
      clearTimeout(tbtn._t);
      tbtn._t = setTimeout(() => root.classList.remove('theme-anim'), 650);
    });
  }

  // keep theme in sync across tabs
  addEventListener('storage', (e) => {
    if (e.key === KEY && (e.newValue === 'dark' || e.newValue === 'light')) { root.dataset.theme = e.newValue; syncTheme(); }
  });
  syncTheme();

  /* ---- Header state + mobile menu ---- */
  const hdr = $('.hdr');
  const mnav = $('.mnav');
  const mbtn = $('.menu-btn');
  const onScrollHdr = raf(() => hdr && hdr.classList.toggle('scrolled', scrollY > 24));
  addEventListener('scroll', onScrollHdr, { passive: true });
  onScrollHdr();
  const setMenu = (open) => {
    if (!mnav || !mbtn) return;
    mnav.classList.toggle('open', open);
    mnav.inert = !open;
    mbtn.setAttribute('aria-expanded', String(open));
    d.body.classList.toggle('menu-open', open);
  };
  if (mnav && mbtn) {
    mnav.inert = true;
    mbtn.addEventListener('click', () => setMenu(mbtn.getAttribute('aria-expanded') !== 'true'));
    mnav.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
    addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });
    matchMedia('(min-width: 980px)').addEventListener('change', (e) => { if (e.matches) setMenu(false); });
  }

  /* ---- Reveal on scroll ---- */
  const rv = $$('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rv.forEach((el) => io.observe(el));
  } else { rv.forEach((el) => el.classList.add('in')); }

  /* ---- Hero parallax (subtle) ---- */
  const par = $$('[data-parallax]');
  if (par.length && !reduce) {
    const run = raf(() => { const y = Math.min(scrollY, innerHeight * 1.2) * 0.06; par.forEach((el) => { el.style.transform = `translate3d(0,${-y}px,0)`; }); });
    addEventListener('scroll', run, { passive: true }); run();
  }

  /* ---- Pointer light on service rows ---- */
  $$('.svc').forEach((el) => el.addEventListener('pointermove', (e) => {
    const r = el.getBoundingClientRect();
    el.style.setProperty('--mx', `${e.clientX - r.left}px`);
    el.style.setProperty('--my', `${e.clientY - r.top}px`);
  }));

  /* ---- Back to top ---- */
  const btt = $('.btt');
  if (btt) {
    const pg = $('.pg', btt);
    btt.inert = true;
    const upd = raf(() => {
      const max = root.scrollHeight - innerHeight;
      const on = scrollY > Math.max(520, innerHeight * 0.7);
      btt.classList.toggle('on', on);
      btt.inert = !on;
      if (pg) btt.style.setProperty('--p', max > 0 ? Math.min(100, (scrollY / max) * 100).toFixed(1) : 0);
    });
    addEventListener('scroll', upd, { passive: true });
    addEventListener('resize', upd);
    upd();
    btt.addEventListener('click', () => {
      scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
      const s = $('.skip'); if (s) s.focus({ preventScroll: true });
    });
  }

  /* ---- Work rail navigation controls ---- */
  const rail = $('.rail');
  if (rail) {
    const track = $('.rail-track', rail);
    const prev = $('.rbtn.prev'), next = $('.rbtn.next');
    if (track && (prev || next)) {
      let nudge = 0;
      const step = 440;
      // In RTL (Arabic), previous moves right (+), next moves left (-)
      // In LTR (English), previous moves left (-), next moves right (+)
      const isRtl = () => (document.documentElement.dir === 'rtl' || document.documentElement.lang === 'ar');

      const applyNudge = (delta) => {
        if (reduce) {
          rail.scrollBy({ left: delta, behavior: 'smooth' });
        } else {
          nudge += delta;
          track.style.transform = `translate3d(${nudge}px, 0, 0)`;
        }
      };

      if (prev) {
        prev.disabled = false;
        prev.addEventListener('click', () => {
          applyNudge(isRtl() ? step : -step);
        });
      }

      if (next) {
        next.disabled = false;
        next.addEventListener('click', () => {
          applyNudge(isRtl() ? -step : step);
        });
      }
    }
  }

  /* ---- Project filters + lightbox ---- */
  const grid = $('.pgrid');
  if (grid) {
    const items = $$('.pitem', grid);
    const fbtns = $$('.filters button');
    const live = $('#filter-live');
    const apply = (f, push) => {
      items.forEach((it) => { it.hidden = !(f === 'all' || it.dataset.cat === f); });
      fbtns.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.filter === f)));
      if (live) live.textContent = (L.showing || '') + ' ' + items.filter((i) => !i.hidden).length;
      if (push) history.replaceState(null, '', f === 'all' ? location.pathname : '#' + f);
    };
    fbtns.forEach((b) => b.addEventListener('click', () => apply(b.dataset.filter, true)));
    const h = location.hash.slice(1);
    if (h === 'residential' || h === 'commercial') apply(h, false);

    const lb = $('.lb');
    if (lb && typeof lb.showModal === 'function') {
      const img = $('img', lb), capT = $('.lb-t', lb), capN = $('.lb-n', lb);
      let idx = 0, list = [];
      const show = (i) => {
        idx = (i + list.length) % list.length;
        const b = list[idx];
        img.src = b.dataset.full; img.alt = b.dataset.alt;
        capT.textContent = b.dataset.cap; capN.textContent = `${idx + 1} / ${list.length}`;
        const n = new Image(); n.src = list[(idx + 1) % list.length].dataset.full;
      };
      items.forEach((it) => $('button', it).addEventListener('click', (e) => {
        list = items.filter((x) => !x.hidden).map((x) => $('button', x));
        show(list.indexOf(e.currentTarget)); lb.showModal();
      }));
      $('.lb-close', lb).addEventListener('click', () => lb.close());
      $('.lb-prev', lb).addEventListener('click', () => show(idx - 1));
      $('.lb-next', lb).addEventListener('click', () => show(idx + 1));
      lb.addEventListener('click', (e) => { if (e.target === lb) lb.close(); });
      lb.addEventListener('keydown', (e) => {
        const fwd = rtl ? 'ArrowLeft' : 'ArrowRight', back = rtl ? 'ArrowRight' : 'ArrowLeft';
        if (e.key === fwd) show(idx + 1); else if (e.key === back) show(idx - 1);
      });
    }
  }

  /* ---- Film ---- */
  const film = $('.film-frame');
  if (film) {
    const v = $('video', film), p = $('.play', film);
    p.addEventListener('click', () => { film.classList.add('playing'); v.controls = true; v.play().catch(() => {}); v.focus(); });
    v.addEventListener('ended', () => { film.classList.remove('playing'); v.controls = false; });
  }

  /* ---- Forms (front-end only; server endpoint is injected via data-endpoint) ---- */
  $$('form[data-form]').forEach((f) => {
    const st = $('.form-status', f);
    const say = (cls, msg) => { st.className = 'form-status show ' + cls; st.textContent = msg; };
    const file = $('input[type="file"]', f);
    if (file) file.addEventListener('change', () => {
      const x = file.files[0]; file.setCustomValidity('');
      if (x && x.size > 5 * 1024 * 1024) { file.setCustomValidity(L.fileBig || 'File too large'); file.reportValidity(); }
    });
    f.addEventListener('submit', async (e) => {
      e.preventDefault();
      f.classList.add('was-validated');
      if (!f.checkValidity()) {
        const bad = $(':invalid', f); if (bad) bad.focus();
        say('err', L.fix || 'Please complete the required fields.');
        return;
      }
      const hp = $('.hp input', f); if (hp && hp.value) return; // honeypot
      const ep = f.dataset.endpoint;
      if (!ep) { say('ok', L.demo); return; } // no backend wired in the sample
      try {
        const r = await fetch(ep, { method: 'POST', body: new FormData(f) });
        if (!r.ok) throw new Error(r.status);
        say('ok', L.sent); f.reset(); f.classList.remove('was-validated');
      } catch (err) { say('err', L.failed); }
    });
  });
})();
