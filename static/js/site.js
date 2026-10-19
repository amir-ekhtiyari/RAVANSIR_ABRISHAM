/* Ravan Seir Abrisham – progressive enhancement only. The site works without JavaScript. */
(function () {
  'use strict';

  var doc = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function storage(key, value) {
    try {
      if (value === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, value);
    } catch (e) { return null; }
  }

  /* ---------- Theme ---------- */
  function syncThemeButtons() {
    var dark = doc.getAttribute('data-theme') === 'dark';
    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
    });
  }
  function setTheme(theme, persist) {
    doc.classList.add('theme-switching');
    doc.setAttribute('data-theme', theme);
    if (persist) storage('theme', theme);
    syncThemeButtons();
    window.setTimeout(function () { doc.classList.remove('theme-switching'); }, 350);
  }
  document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      setTheme(doc.getAttribute('data-theme') === 'dark' ? 'light' : 'dark', true);
    });
  });
  // Follow the system setting until the visitor makes a choice.
  var systemDark = window.matchMedia('(prefers-color-scheme: dark)');
  var onSystemChange = function (e) { if (!storage('theme')) setTheme(e.matches ? 'dark' : 'light', false); };
  if (systemDark.addEventListener) systemDark.addEventListener('change', onSystemChange);
  syncThemeButtons();

  /* ---------- Language switch keeps the current section ---------- */
  document.querySelectorAll('.lang-switch a').forEach(function (a) {
    a.addEventListener('click', function () {
      if (location.hash && a.href.indexOf('#') === -1) a.href += location.hash;
    });
  });

  /* ---------- Header: compact + solid after scrolling ---------- */
  var header = document.querySelector('[data-header]');
  if (header && !header.classList.contains('site-header--solid')) {
    var onScroll = function () { header.classList.toggle('is-solid', window.scrollY > 24); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Hero: word-by-word title, cursor glow, scroll parallax ---------- */
  var hero = document.querySelector('[data-hero]');
  if (hero) {
    var title = hero.querySelector('h1[data-split]');
    if (title) {
      var wordIndex = 0;
      var splitNode = function (node) {
        Array.prototype.slice.call(node.childNodes).forEach(function (child) {
          if (child.nodeType === 3) {
            var parts = child.textContent.split(/(\s+)/);
            var frag = document.createDocumentFragment();
            parts.forEach(function (part) {
              if (!part) return;
              if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
              var w = document.createElement('span');
              w.className = 'w';
              w.style.setProperty('--i', wordIndex++);
              w.textContent = part;
              frag.appendChild(w);
            });
            child.parentNode.replaceChild(frag, child);
          } else if (child.nodeType === 1) {
            splitNode(child);
          }
        });
      };
      splitNode(title);
      title.classList.add('is-split');
    }

    if (!reduceMotion.matches) {
      var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
      if (finePointer) {
        var glowFrame = 0;
        hero.addEventListener('pointermove', function (e) {
          if (glowFrame) return;
          glowFrame = requestAnimationFrame(function () {
            glowFrame = 0;
            var r = hero.getBoundingClientRect();
            hero.style.setProperty('--mx', (e.clientX - r.left) + 'px');
            hero.style.setProperty('--my', (e.clientY - r.top) + 'px');
            hero.style.setProperty('--tx', ((e.clientX - r.left) / r.width * 2 - 1).toFixed(3));
            hero.style.setProperty('--ty', ((e.clientY - r.top) / r.height * 2 - 1).toFixed(3));
          });
        });
        hero.addEventListener('pointerenter', function () { hero.classList.add('is-hover'); });
        hero.addEventListener('pointerleave', function () {
          hero.classList.remove('is-hover');
          hero.style.setProperty('--tx', 0);
          hero.style.setProperty('--ty', 0);
        });
      }

      var parallaxFrame = 0;
      var updateParallax = function () {
        parallaxFrame = 0;
        var h = hero.offsetHeight;
        var y = Math.min(Math.max(window.scrollY, 0), h);
        hero.style.setProperty('--hero-py', (y * 0.35).toFixed(1) + 'px');
        hero.style.setProperty('--hero-cy', (y * -0.12).toFixed(1) + 'px');
        hero.style.setProperty('--hero-co', Math.max(0, 1 - y / (h * 0.85)).toFixed(3));
      };
      window.addEventListener('scroll', function () {
        if (!parallaxFrame) parallaxFrame = requestAnimationFrame(updateParallax);
      }, { passive: true });
      updateParallax();
    }
  }

  /* ---------- QR codes: page link + digital business card (library loaded on demand) ---------- */
  var qrDialog = document.getElementById('qr-dialog');
  var qrLibPromise = null;
  var loadQrLib = function () {
    if (window.qrcode) return Promise.resolve(window.qrcode);
    if (!qrLibPromise) {
      qrLibPromise = new Promise(function (resolve, reject) {
        var src = qrDialog && qrDialog.getAttribute('data-qr-lib');
        if (!src) { reject(new Error('QR library path missing')); return; }
        var tag = document.createElement('script');
        tag.src = src;
        tag.onload = function () { resolve(window.qrcode); };
        tag.onerror = reject;
        document.head.appendChild(tag);
      });
    }
    return qrLibPromise;
  };
  var pageUrl = function () { return window.location.href.split('#')[0]; };
  var qrText = function (box) {
    if (box.hasAttribute('data-qr-page')) return pageUrl();
    var holder = box.parentNode.querySelector('template[data-qr-text]');
    return holder ? (holder.content ? holder.content.textContent : holder.textContent) : '';
  };
  var buildQr = function (qrcode, text, ecc) {
    qrcode.stringToBytes = qrcode.stringToBytesFuncs['UTF-8'];
    var qr = qrcode(0, ecc || 'M');
    qr.addData(text, 'Byte');
    qr.make();
    return qr;
  };
  var renderQr = function (box) {
    var text = qrText(box);
    if (!text) return Promise.resolve();
    return loadQrLib().then(function (qrcode) {
      var qr = buildQr(qrcode, text, box.getAttribute('data-qr-ecc'));
      box._qr = qr;
      box.innerHTML = qr.createSvgTag({ cellSize: 4, margin: 0, scalable: true });
      var svg = box.querySelector('svg');
      if (svg) { svg.setAttribute('aria-hidden', 'true'); svg.setAttribute('focusable', 'false'); }
      var logo = box.getAttribute('data-qr-logo');
      if (logo && !box.querySelector('.qr-logo')) {
        var badge = document.createElement('span');
        badge.className = 'qr-logo';
        badge.innerHTML = '<img src="' + logo + '" alt="">';
        box.appendChild(badge);
      }
      box.classList.add('is-ready');
    });
  };
  // A crisp PNG (with a white quiet zone and the logo for the page code) for printing or sharing.
  var downloadQr = function (box, filename) {
    var qr = box && box._qr;
    if (!qr) return;
    var count = qr.getModuleCount();
    var scale = Math.max(8, Math.ceil(1024 / count));
    var quiet = 4 * scale;
    var size = count * scale + quiet * 2;
    var canvas = document.createElement('canvas');
    canvas.width = canvas.height = size;
    var ctx = canvas.getContext('2d');
    ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, size, size);
    ctx.fillStyle = '#0b1424';
    for (var r = 0; r < count; r++) {
      for (var c = 0; c < count; c++) {
        if (qr.isDark(r, c)) ctx.fillRect(quiet + c * scale, quiet + r * scale, scale, scale);
      }
    }
    var finish = function () {
      var link = document.createElement('a');
      link.download = filename;
      link.href = canvas.toDataURL('image/png');
      document.body.appendChild(link); link.click(); link.remove();
    };
    var logo = box.getAttribute('data-qr-logo');
    if (!logo) { finish(); return; }
    var img = new Image();
    img.onload = function () {
      var s = size * 0.22, x = (size - s) / 2, pad = s * 0.12;
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      if (ctx.roundRect) ctx.roundRect(x - pad, x - pad, s + pad * 2, s + pad * 2, s * 0.2); else ctx.rect(x - pad, x - pad, s + pad * 2, s + pad * 2);
      ctx.fill();
      ctx.drawImage(img, x, x, s, s);
      finish();
    };
    img.onerror = finish;
    img.src = logo;
  };

  // Business-card QR in the contact section: render when it comes into view.
  var inlineQr = document.querySelectorAll('.qr-card [data-qr-render], .footer-qr-mini [data-qr-render]');
  if (inlineQr.length) {
    if ('IntersectionObserver' in window) {
      var qrObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) { qrObserver.unobserve(entry.target); renderQr(entry.target); }
        });
      }, { rootMargin: '200px' });
      inlineQr.forEach(function (el) { qrObserver.observe(el); });
    } else {
      inlineQr.forEach(renderQr);
    }
  }

  if (qrDialog && typeof qrDialog.showModal === 'function') {
    var qrLastFocus = null;
    var selectTab = function (name) {
      qrDialog.querySelectorAll('[data-qr-tab]').forEach(function (tab) {
        var on = tab.getAttribute('data-qr-tab') === name;
        tab.setAttribute('aria-selected', on ? 'true' : 'false');
        tab.tabIndex = on ? 0 : -1;
      });
      qrDialog.querySelectorAll('[data-qr-panel]').forEach(function (panel) {
        panel.hidden = panel.getAttribute('data-qr-panel') !== name;
        if (!panel.hidden) panel.querySelectorAll('[data-qr-render]').forEach(function (box) { if (!box._qr) renderQr(box); });
      });
    };
    var openQr = function (trigger) {
      qrLastFocus = trigger || document.activeElement;
      var urlLabel = qrDialog.querySelector('[data-qr-url]');
      if (urlLabel) urlLabel.textContent = decodeURI(pageUrl());
      qrDialog.querySelectorAll('[data-qr-page]').forEach(function (box) { box._qr = null; });
      selectTab('page');
      if (typeof closeDrawer === 'function' && drawer && drawer.classList.contains('is-open')) closeDrawer();
      qrDialog.showModal();
      document.body.classList.add('no-scroll');
    };
    document.addEventListener('click', function (e) {
      var opener = e.target.closest('[data-qr-open]');
      if (opener) { e.preventDefault(); openQr(opener); }
    });
    qrDialog.addEventListener('close', function () {
      document.body.classList.remove('no-scroll');
      if (qrLastFocus && qrLastFocus.focus) qrLastFocus.focus();
    });
    qrDialog.addEventListener('click', function (e) {
      if (e.target === qrDialog || e.target.closest('[data-qr-close]')) qrDialog.close();
      var tab = e.target.closest('[data-qr-tab]');
      if (tab) selectTab(tab.getAttribute('data-qr-tab'));
      var dl = e.target.closest('[data-qr-download]');
      if (dl) {
        var which = dl.getAttribute('data-qr-download');
        downloadQr(qrDialog.querySelector('[data-qr-panel="' + which + '"] [data-qr-render]'),
          which === 'page' ? 'ravan-seir-abrisham-qr.png' : 'ravan-seir-abrisham-contact-qr.png');
      }
      var copy = e.target.closest('[data-qr-copy]');
      if (copy && navigator.clipboard) {
        navigator.clipboard.writeText(pageUrl()).then(function () {
          var label = copy.querySelector('[data-qr-copy-label]');
          if (!label) return;
          var original = label.getAttribute('data-original') || label.textContent;
          label.setAttribute('data-original', original);
          label.textContent = '✓';
          setTimeout(function () { label.textContent = original; }, 1600);
        });
      }
    });
    qrDialog.addEventListener('keydown', function (e) {
      var tab = e.target.closest('[data-qr-tab]');
      if (!tab || (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight')) return;
      var next = tab.getAttribute('data-qr-tab') === 'page' ? 'card' : 'page';
      selectTab(next);
      qrDialog.querySelector('[data-qr-tab="' + next + '"]').focus();
    });
  } else {
    document.querySelectorAll('[data-qr-open]').forEach(function (btn) { btn.hidden = true; });
  }

  /* ---------- Back to top (with scroll-progress ring) ---------- */
  var toTop = document.querySelector('[data-to-top]');
  if (toTop) {
    var bar = toTop.querySelector('.ring .bar');
    var LEN = 169.6;
    var ticking = false;
    var update = function () {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(1, window.scrollY / max) : 0;
      if (bar) bar.style.strokeDashoffset = String(LEN * (1 - p));
      toTop.classList.toggle('is-shown', window.scrollY > window.innerHeight * 0.6);
      ticking = false;
    };
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
    toTop.addEventListener('click', function () {
      toTop.classList.add('is-launching');
      window.scrollTo({ top: 0, behavior: reduceMotion.matches ? 'auto' : 'smooth' });
      var skip = document.querySelector('#main');
      window.setTimeout(function () { toTop.classList.remove('is-launching'); if (skip) skip.focus({ preventScroll: true }); }, 800);
    });
  }

  /* ---------- Mobile drawer (focus trap, Esc, backdrop) ---------- */
  var drawer = document.querySelector('[data-drawer]');
  var opener = document.querySelector('[data-drawer-open]');
  var lastFocus = null;
  function focusables() {
    return Array.prototype.filter.call(
      drawer.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])'),
      function (el) { return el.offsetParent !== null; });
  }
  function openDrawer() {
    lastFocus = document.activeElement;
    drawer.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    opener.setAttribute('aria-expanded', 'true');
    document.body.classList.add('no-scroll');
    var items = focusables();
    if (items.length) window.setTimeout(function () { items[0].focus(); }, 50);
  }
  function closeDrawer() {
    drawer.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
    opener.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('no-scroll');
    if (lastFocus) lastFocus.focus();
  }
  if (drawer && opener) {
    opener.addEventListener('click', openDrawer);
    drawer.querySelectorAll('[data-drawer-close]').forEach(function (el) { el.addEventListener('click', closeDrawer); });
    drawer.querySelectorAll('.drawer-nav a, .drawer-foot .btn').forEach(function (a) { a.addEventListener('click', closeDrawer); });
    drawer.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { closeDrawer(); return; }
      if (e.key !== 'Tab') return;
      var items = focusables();
      if (!items.length) return;
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 1080 && drawer.classList.contains('is-open')) closeDrawer(); });
  }

  /* ---------- Scroll reveal & process animation ---------- */
  var revealTargets = document.querySelectorAll('.reveal, [data-process]');
  if ('IntersectionObserver' in window && !reduceMotion.matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-visible'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    revealTargets.forEach(function (el) { io.observe(el); });
  } else {
    revealTargets.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- SVG (SMIL) animations: stop when reduced motion is requested ---------- */
  function applyMotionPreference() {
    document.querySelectorAll('svg').forEach(function (svg) {
      if (!svg.pauseAnimations) return;
      if (reduceMotion.matches) svg.pauseAnimations(); else svg.unpauseAnimations();
    });
  }
  applyMotionPreference();
  if (reduceMotion.addEventListener) reduceMotion.addEventListener('change', applyMotionPreference);

  /* ---------- Route map: highlight a route from its card ---------- */
  var map = document.querySelector('[data-route-map]');
  if (map) {
    document.querySelectorAll('[data-route]').forEach(function (card) {
      var key = card.getAttribute('data-route');
      var on = function () {
        map.classList.add('has-focus');
        map.querySelectorAll('[data-route-line]').forEach(function (l) {
          l.classList.toggle('is-focus', l.getAttribute('data-route-line') === key);
        });
      };
      var off = function () { map.classList.remove('has-focus'); };
      card.addEventListener('mouseenter', on);
      card.addEventListener('focus', on);
      card.addEventListener('mouseleave', off);
      card.addEventListener('blur', off);
    });
  }

  /* ---------- Toasts ---------- */
  var toastBox = document.getElementById('toasts');
  function dismiss(toast) {
    toast.classList.add('is-leaving');
    window.setTimeout(function () { toast.remove(); }, 260);
  }
  function wireToast(toast) {
    var btn = toast.querySelector('[data-toast-close]');
    if (btn) btn.addEventListener('click', function () { dismiss(toast); });
    window.setTimeout(function () { if (toast.isConnected) dismiss(toast); }, 7000);
  }
  function icon(name) {
    return '<svg class="icon" width="20" height="20" aria-hidden="true"><use href="#i-' + name + '"></use></svg>';
  }
  function showToast(message, isError) {
    if (!toastBox) return;
    var t = document.createElement('div');
    t.className = 'toast' + (isError ? ' toast--error' : '');
    t.setAttribute('role', isError ? 'alert' : 'status');
    t.innerHTML = icon(isError ? 'circle-alert' : 'circle-check') + '<p></p>' +
      '<button type="button" data-toast-close aria-label="' + ({fa: 'بستن', tr: 'Kapat'}[doc.lang] || 'Close') + '">' + icon('x') + '</button>';
    t.querySelector('p').textContent = message;
    toastBox.appendChild(t);
    wireToast(t);
  }
  if (toastBox) toastBox.querySelectorAll('.toast').forEach(wireToast);

  /* ---------- Contact form: AJAX submit with server-side validation ---------- */
  var form = document.querySelector('[data-contact-form]');
  if (form && window.fetch && window.FormData) {
    var status = form.parentElement.querySelector('[data-form-status]');
    var button = form.querySelector('button[type="submit"]');

    var clearErrors = function () {
      form.querySelectorAll('.field').forEach(function (f) {
        f.classList.remove('has-error');
        var input = f.querySelector('input, textarea');
        if (input) input.removeAttribute('aria-invalid');
        var err = f.querySelector('.error');
        if (err) err.textContent = '';
      });
      if (status) status.innerHTML = '';
    };
    form.querySelectorAll('input, textarea').forEach(function (input) {
      input.addEventListener('input', function () {
        var f = input.closest('.field');
        if (f && f.classList.contains('has-error')) {
          f.classList.remove('has-error');
          input.removeAttribute('aria-invalid');
          var err = f.querySelector('.error');
          if (err) err.textContent = '';
        }
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      clearErrors();
      button.classList.add('is-loading');
      button.setAttribute('aria-busy', 'true');
      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
        credentials: 'same-origin'
      }).then(function (res) {
        return res.json().catch(function () { return { ok: false }; });
      }).then(function (data) {
        if (data.ok) {
          if (toastBox) toastBox.querySelectorAll('.toast--error').forEach(dismiss);
          var card = form.closest('.form-card');
          card.innerHTML = '<div class="form-success" tabindex="-1"><div class="badge">' +
            '<svg class="icon" width="34" height="34" aria-hidden="true"><use href="#i-circle-check"></use></svg></div>' +
            '<h3></h3><p></p></div>';
          card.querySelector('h3').textContent = form.getAttribute('data-success-title') || '';
          card.querySelector('p').textContent = data.message;
          card.querySelector('.form-success').focus();
          showToast(data.message, false);
          return;
        }
        var first = null;
        Object.keys(data.errors || {}).forEach(function (name) {
          var f = form.querySelector('[data-field="' + name + '"]');
          if (!f) return;
          f.classList.add('has-error');
          var input = f.querySelector('input, textarea');
          if (input) { input.setAttribute('aria-invalid', 'true'); if (!first) first = input; }
          var err = f.querySelector('.error');
          if (err) err.innerHTML = icon('circle-alert').replace('width="20" height="20"', 'width="15" height="15"') + '<span></span>';
          if (err) err.querySelector('span').textContent = data.errors[name].join(' ');
        });
        var msg = data.message || form.getAttribute('data-error-text');
        if (status) {
          status.innerHTML = '<div class="form-alert form-alert--error">' + icon('circle-alert') + '<div></div></div>';
          status.querySelector('div div').textContent = msg;
        }
        showToast(msg, true);
        if (first) first.focus();
      }).catch(function () {
        // Network problem: fall back to a normal form post.
        form.submit();
      }).finally(function () {
        button.classList.remove('is-loading');
        button.removeAttribute('aria-busy');
      });
    });
  }
})();
