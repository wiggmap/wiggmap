// /data/footer.js
(function () {
  // prevent duplicates
  if (document.getElementById("wmSiteFooter")) return;

  const year = new Date().getFullYear();

  const footerHTML = `
    <footer id="wmSiteFooter" class="wm-footer" role="contentinfo">
      <div class="wm-footer__inner">
        <div class="wm-footer__row">
          <div class="wm-footer__copy">© ${year} WiggMap. All rights reserved.</div>

          <nav class="wm-footer__links" aria-label="Legal">
            <a href="/terms.html">Terms</a>
            <span class="wm-footer__sep">•</span>
            <a href="/privacy.html">Privacy</a>
            <span class="wm-footer__sep">•</span>
            <button type="button" id="wmCookieReset" class="wm-footer-cookies-btn">Cookies</button>
          </nav>
        </div>
      </div>
    </footer>

    <style>
      .wm-footer{
        margin-top: 18px;
        padding: 18px 14px 22px;
        text-align: center;
        font-family: "Poppins", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        color: rgba(0,0,0,.62);
      }
      .wm-footer__inner{
        max-width: 1100px;
        margin: 0 auto;
        border-top: 1px solid rgba(0,0,0,.10);
        padding-top: 12px;
      }
      .wm-footer__row{
        display:flex;
        align-items:center;
        justify-content:center;
        gap: 12px;
        flex-wrap: wrap;
      }
      .wm-footer__copy{
        font-size: 13px;
        opacity: .9;
      }
      .wm-footer__links{
        display:flex;
        align-items:center;
        gap: 10px;
        flex-wrap: wrap;
        justify-content:center;
        font-size: 13px;
      }
      .wm-footer a,
      .wm-footer .wm-footer-cookies-btn{
        color: rgba(0,0,0,.62);
        text-decoration: none;
        font-weight: 700;
      }
      .wm-footer a:hover,
      .wm-footer .wm-footer-cookies-btn:hover{
        text-decoration: underline;
      }
      .wm-footer .wm-footer-cookies-btn{
        background: transparent;
        border: 0;
        padding: 0;
        font: inherit;
        cursor: pointer;
        line-height: inherit;
      }
      .wm-footer .wm-footer-cookies-btn:focus-visible{
        outline: 2px solid #1a5430;
        outline-offset: 2px;
        border-radius: 2px;
      }
      .wm-footer__sep{
        opacity: .55;
        font-weight: 900;
      }
    </style>
  `;

  document.body.insertAdjacentHTML("beforeend", footerHTML);

  // Cookie preferences reset trigger (now a <button>, no preventDefault needed)
  var cookieBtn = document.getElementById('wmCookieReset');
  if (cookieBtn) {
    cookieBtn.addEventListener('click', function() {
      localStorage.removeItem('wigg_consent');
      window.location.reload();
    });
  }
})();

// ── Cookie consent banner ──
(function(){
  if (localStorage.getItem('wigg_consent')) return; // already answered

  var lang = (localStorage.getItem('wigg_lang') || 'en').toLowerCase();
  var T = {
    en: { msg:'We use cookies for analytics to improve your experience.', accept:'Accept', reject:'Refuse', settings:'Settings', essential:'Essential (always on)', analytics:'Analytics (Google)', save:'Save preferences', privacy:'Privacy policy' },
    fr: { msg:'Nous utilisons des cookies analytiques pour améliorer votre expérience.', accept:'Accepter', reject:'Refuser', settings:'Paramétrer', essential:'Essentiels (toujours actifs)', analytics:'Analytiques (Google)', save:'Enregistrer', privacy:'Politique de confidentialité' },
    es: { msg:'Usamos cookies analíticas para mejorar tu experiencia.', accept:'Aceptar', reject:'Rechazar', settings:'Configurar', essential:'Esenciales (siempre activos)', analytics:'Analíticas (Google)', save:'Guardar', privacy:'Política de privacidad' }
  };
  var t = T[lang] || T.en;

  var banner = document.createElement('div');
  banner.id = 'wiggConsent';
  banner.innerHTML =
    '<div class="wc-inner">' +
      '<p class="wc-msg">' + t.msg + ' <a href="/privacy.html" class="wc-link">' + t.privacy + '</a></p>' +
      '<div class="wc-btns" id="wcBtns">' +
        '<button class="wc-btn wc-accept" id="wcAccept">' + t.accept + '</button>' +
        '<button class="wc-btn wc-reject" id="wcReject">' + t.reject + '</button>' +
        '<button class="wc-btn wc-settings" id="wcSettings">' + t.settings + '</button>' +
      '</div>' +
      '<div class="wc-detail" id="wcDetail" style="display:none">' +
        '<label class="wc-toggle"><input type="checkbox" checked disabled><span>' + t.essential + '</span></label>' +
        '<label class="wc-toggle"><input type="checkbox" id="wcAnalytics" checked><span>' + t.analytics + '</span></label>' +
        '<button class="wc-btn wc-accept" id="wcSave">' + t.save + '</button>' +
      '</div>' +
    '</div>';

  var style = document.createElement('style');
  style.textContent =
    '#wiggConsent{position:fixed;bottom:0;left:0;right:0;z-index:99999;background:#1c1710;border-top:1px solid rgba(255,255,255,.08);padding:16px 20px;font-family:Inter,system-ui,sans-serif;animation:wcSlide .35s ease}' +
    '@keyframes wcSlide{from{transform:translateY(100%)}to{transform:translateY(0)}}' +
    '.wc-inner{max-width:960px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px}' +
    '.wc-msg{flex:1 1 300px;font-size:13px;color:rgba(255,255,255,.7);line-height:1.5;margin:0}' +
    '.wc-link{color:#22c55e;text-decoration:underline;font-weight:600}' +
    '.wc-btns{display:flex;gap:8px;flex-wrap:wrap}' +
    '.wc-btn{padding:8px 18px;border-radius:2px;font-family:Inter,sans-serif;font-size:12px;font-weight:600;cursor:pointer;border:none;transition:opacity .15s}' +
    '.wc-accept{background:#1a5430;color:#fff}.wc-accept:hover{opacity:.85}' +
    '.wc-reject{background:transparent;color:rgba(255,255,255,.5);border:1px solid rgba(255,255,255,.15)}.wc-reject:hover{border-color:rgba(255,255,255,.35)}' +
    '.wc-settings{background:transparent;color:rgba(255,255,255,.5);border:1px solid rgba(255,255,255,.15);font-size:11px}.wc-settings:hover{border-color:rgba(255,255,255,.35)}' +
    '.wc-detail{flex-basis:100%;display:flex;flex-wrap:wrap;gap:12px;align-items:center;padding-top:10px;border-top:1px solid rgba(255,255,255,.08);margin-top:4px}' +
    '.wc-toggle{display:flex;align-items:center;gap:6px;font-size:12px;color:rgba(255,255,255,.55);cursor:pointer}' +
    '.wc-toggle input{accent-color:#1a5430;width:16px;height:16px}' +
    '@media(max-width:600px){.wc-inner{flex-direction:column;align-items:stretch;text-align:center}.wc-btns{justify-content:center}}';
  document.head.appendChild(style);
  document.body.appendChild(banner);

  function grant() {
    localStorage.setItem('wigg_consent', 'accepted');
    if (window.gtag) gtag('consent', 'update', { analytics_storage: 'granted' });
    // Notify other scripts (Meta Pixel, etc.) that consent was granted
    window.dispatchEvent(new Event('wigg_consent_granted'));
    banner.remove();
  }
  function deny() {
    localStorage.setItem('wigg_consent', 'refused');
    banner.remove();
  }

  document.getElementById('wcAccept').onclick = grant;
  document.getElementById('wcReject').onclick = deny;
  document.getElementById('wcSettings').onclick = function() {
    document.getElementById('wcDetail').style.display = 'flex';
    document.getElementById('wcBtns').style.display = 'none';
  };
  document.getElementById('wcSave').onclick = function() {
    if (document.getElementById('wcAnalytics').checked) grant(); else deny();
  };
})();

// ── Runtime image format swap (.jpg → .webp if available) ──
// Looks at all <img src=".jpg/.png"> and tries the .webp version first.
// Falls back gracefully to the original on 404.
//
// Pages that already serve <picture><source srcset=".webp"> SSR can opt out
// by setting `window.__WM_DISABLE_WEBP_SWAP = true;` BEFORE this script runs
// (or before DOMContentLoaded). The flag must be set on the global object;
// any truthy value disables the runtime swap and the MutationObserver below.
(function() {
  if (window.__WM_DISABLE_WEBP_SWAP) return;
  // Check WebP support once
  var webpSupported = (function() {
    try {
      var c = document.createElement('canvas');
      return c.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    } catch (e) { return false; }
  })();
  if (!webpSupported) return;

  function tryWebp(img) {
    if (img.dataset.wmWebpDone) return;
    img.dataset.wmWebpDone = '1';
    var src = img.getAttribute('src') || '';
    if (!/\.(jpg|jpeg|png)$/i.test(src)) return;
    if (/data:|blob:/.test(src)) return;
    var webp = src.replace(/\.(jpg|jpeg|png)$/i, '.webp');
    // Test if webp exists by attempting to load it on a hidden image
    var test = new Image();
    test.onload = function() { img.src = webp; };
    test.onerror = function() {}; // keep original
    test.src = webp;
  }

  function scanImages() {
    document.querySelectorAll('img').forEach(tryWebp);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scanImages);
  } else {
    scanImages();
  }

  // Also watch for newly added images (e.g. dynamic content)
  if (window.MutationObserver) {
    new MutationObserver(function(muts) {
      muts.forEach(function(m) {
        m.addedNodes.forEach(function(n) {
          if (n.nodeType !== 1) return;
          if (n.tagName === 'IMG') tryWebp(n);
          else if (n.querySelectorAll) n.querySelectorAll('img').forEach(tryWebp);
        });
      });
    }).observe(document.body, { childList: true, subtree: true });
  }
})();

// ── PWA back-button viewport fix ──
window.addEventListener('pageshow', function(e) {
  if (e.persisted) window.scrollTo(0, 0);
});

// WiggMap Connect Widget — chargement automatique sur les chronicles
(function() {
  const path = window.location.pathname;
  if (!path.includes('/chronicles/')) return;

  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = '/connect/widget.css';
  document.head.appendChild(link);

  const script = document.createElement('script');
  script.src = '/connect/widget.js';
  document.body.appendChild(script);
})();

// ── Breadcrumbs (chronicles only — visual + JSON-LD) ──
(function() {
  var path = window.location.pathname;
  if (!path.includes('/chronicles/')) return;
  if (/\/chronicles-[a-z]+\.html$/i.test(path) || /\/indexchronicles\.html$/i.test(path)) return;

  var lang = (localStorage.getItem('wigg_lang') || 'en').toLowerCase();
  if (['en','fr','es'].indexOf(lang) === -1) lang = 'en';

  var T = {
    en: { home:'Home', chron:'Chronicles', cities:'Cities' },
    fr: { home:'Accueil', chron:'Chroniques', cities:'Villes' },
    es: { home:'Inicio', chron:'Crónicas', cities:'Ciudades' }
  };
  var t = T[lang];
  var isCity = path.includes('/chronicles/villes/');

  function inject() {
    if (document.getElementById('wmBreadcrumbs')) return;
    // Insert just below the bandeau (before the first content section)
    var bandeau = document.querySelector('.bandeau');
    if (!bandeau) return;

    var crumbs = [
      { label: t.home, href: '/' },
      { label: t.chron, href: '/indexchronicles.html' }
    ];
    if (isCity) crumbs.push({ label: t.cities, href: '/chronicles-villes.html' });

    var html = '<nav class="wm-breadcrumbs" id="wmBreadcrumbs" aria-label="Breadcrumb">' +
      '<ol class="wm-bc-list">' +
      crumbs.map(function(c, i) {
        return '<li class="wm-bc-item">' +
          (i < crumbs.length - 1
            ? '<a href="' + c.href + '" class="wm-bc-link">' + c.label + '</a><span class="wm-bc-sep">›</span>'
            : '<a href="' + c.href + '" class="wm-bc-link">' + c.label + '</a><span class="wm-bc-sep">›</span><span class="wm-bc-current">' + (document.title.split('·')[0] || '').trim() + '</span>')
        + '</li>';
      }).join('') +
      '</ol></nav>';

    var div = document.createElement('div');
    div.innerHTML = html;
    bandeau.parentNode.insertBefore(div.firstChild, bandeau.nextSibling);

    // Inject CSS once
    if (!document.getElementById('wmBcStyle')) {
      var st = document.createElement('style');
      st.id = 'wmBcStyle';
      st.textContent =
        '.wm-breadcrumbs{max-width:900px;margin:0 auto;padding:14px 28px 0;font-family:Inter,system-ui,sans-serif}' +
        '.wm-bc-list{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;align-items:center;gap:0;font-size:12px;color:#8a7f6a}' +
        '.wm-bc-item{display:inline-flex;align-items:center;font-weight:500}' +
        '.wm-bc-link{color:#1a5430;text-decoration:none;font-weight:600;transition:opacity .15s}' +
        '.wm-bc-link:hover{text-decoration:underline}' +
        '.wm-bc-sep{margin:0 8px;color:#c8bfaa;font-weight:400}' +
        '.wm-bc-current{color:#54554e;font-weight:500;max-width:50ch;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}' +
        '@media(max-width:720px){.wm-breadcrumbs{padding:10px 18px 0}.wm-bc-list{font-size:11px}.wm-bc-current{max-width:18ch}}';
      document.head.appendChild(st);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }
})();

// ── Related chronicles (chronicle pages only) ──
(function() {
  var path = window.location.pathname;
  if (!path.includes('/chronicles/')) return;
  if (/\/chronicles-[a-z]+\.html$/i.test(path) || /\/indexchronicles\.html$/i.test(path)) return;

  var lang = (localStorage.getItem('wigg_lang') || 'en').toLowerCase();
  if (['en','fr','es'].indexOf(lang) === -1) lang = 'en';

  var T = {
    en: { title:'Continue exploring' },
    fr: { title:'Continuer à explorer' },
    es: { title:'Sigue explorando' }
  };
  var t = T[lang];
  var isCity = path.includes('/chronicles/villes/');

  // Curated pool of related links per language (to avoid runtime fetch + indexing)
  // City chronicles → other cities. Regular chronicles → other regular chronicles.
  var POOL_CITY = {
    en: [
      { title:'Bangkok',      slug:'chronicle-bangkok-thailand-en',     img:'thailand'  },
      { title:'Lisbon',       slug:'chronicle-lisbonne-portugal-en',    img:'portugal'  },
      { title:'Tokyo',        slug:'chronicle-tokyo-japan-en',          img:'japan'     },
      { title:'Mexico City',  slug:'chronicle-mexico-city-mexico-en',   img:'mexico'    },
      { title:'Bali',         slug:'chronicle-bali-indonesia-en',       img:'indonesia' },
      { title:'Dubai',        slug:'chronicle-dubai-emirats-en',        img:'uae'       },
      { title:'Berlin',       slug:'chronicle-berlin-allemagne-en',     img:'germany'   },
      { title:'Medellín',     slug:'chronicle-medellin-colombie-en',    img:'colombia'  },
      { title:'Kuala Lumpur', slug:'chronicle-kuala-lumpur-malaisie-en',img:'malaysia'  },
      { title:'Porto',        slug:'chronicle-porto-portugal-en',       img:'portugal'  },
      { title:'Istanbul',     slug:'chronicle-istanbul-turquie-en',     img:'turkey'    },
      { title:'Buenos Aires', slug:'chronicle-buenos-aires-argentine-en', img:'argentina' }
    ],
    fr: [
      { title:'Bangkok',      slug:'chronicle-bangkok-thailand-fr',     img:'thailand'  },
      { title:'Lisbonne',     slug:'chronicle-lisbonne-portugal-fr',    img:'portugal'  },
      { title:'Tokyo',        slug:'chronicle-tokyo-japan-fr',          img:'japan'     },
      { title:'Mexico',       slug:'chronicle-mexico-city-mexico-fr',   img:'mexico'    },
      { title:'Bali',         slug:'chronicle-bali-indonesia-fr',       img:'indonesia' },
      { title:'Dubaï',        slug:'chronicle-dubai-emirats-fr',        img:'uae'       },
      { title:'Berlin',       slug:'chronicle-berlin-allemagne-fr',     img:'germany'   },
      { title:'Medellín',     slug:'chronicle-medellin-colombie-fr',    img:'colombia'  },
      { title:'Kuala Lumpur', slug:'chronicle-kuala-lumpur-malaisie-fr',img:'malaysia'  },
      { title:'Porto',        slug:'chronicle-porto-portugal-fr',       img:'portugal'  },
      { title:'Istanbul',     slug:'chronicle-istanbul-turquie-fr',     img:'turkey'    },
      { title:'Buenos Aires', slug:'chronicle-buenos-aires-argentine-fr', img:'argentina' }
    ],
    es: [
      { title:'Bangkok',      slug:'chronicle-bangkok-thailand-es',     img:'thailand'  },
      { title:'Lisboa',       slug:'chronicle-lisbonne-portugal-es',    img:'portugal'  },
      { title:'Tokio',        slug:'chronicle-tokyo-japan-es',          img:'japan'     },
      { title:'Ciudad de México', slug:'chronicle-mexico-city-mexico-es', img:'mexico' },
      { title:'Bali',         slug:'chronicle-bali-indonesia-es',       img:'indonesia' },
      { title:'Dubái',        slug:'chronicle-dubai-emirats-es',        img:'uae'       },
      { title:'Berlín',       slug:'chronicle-berlin-allemagne-es',     img:'germany'   },
      { title:'Medellín',     slug:'chronicle-medellin-colombie-es',    img:'colombia'  },
      { title:'Kuala Lumpur', slug:'chronicle-kuala-lumpur-malaisie-es',img:'malaysia'  },
      { title:'Oporto',       slug:'chronicle-porto-portugal-es',       img:'portugal'  },
      { title:'Estambul',     slug:'chronicle-istanbul-turquie-es',     img:'turkey'    },
      { title:'Buenos Aires', slug:'chronicle-buenos-aires-argentine-es', img:'argentina' }
    ]
  };

  var POOL_REGULAR = {
    en: [
      { title:'Best Digital Nomad Visas 2026',    slug:'chronicle-digital-nomad-visas-2026-en',     img:'portugal' },
      { title:'Asia Expat Guide 2026 — Part 1',   slug:'chronicle-asia-expat-guide-part1-2026-en',  img:'thailand' },
      { title:'2056: Where to live in 30 years',  slug:'chronicle-2056-best-countries-30-years-en', img:'norway'   },
      { title:'Australia Expat Guide 2026',       slug:'chronicle-australia-expat-guide-2026-en',   img:'australia'},
      { title:'Africa Expat Guide — Part 1',      slug:'chronicle-africa-expat-p1-en',              img:'morocco'  },
      { title:'Healthcare Systems for Expats',    slug:'chronicle-healthcare-expats-2026-en',       img:'germany'  }
    ],
    fr: [
      { title:'Meilleurs visas digital nomad 2026',  slug:'chronicle-visas-digital-nomads-2026-fr',     img:'portugal' },
      { title:'Asie 2026 — Partie 1',                slug:'chronicle-asie-expatriation-partie1-2026-fr',img:'thailand' },
      { title:'2056 : où vivra-t-on le mieux ?',     slug:'chronicle-2056-ou-vivra-t-on-le-mieux-fr',   img:'norway'   },
      { title:'Australie : guide expatriation 2026', slug:'chronicle-australie-expatriation-2026-fr',   img:'australia'},
      { title:'Afrique : partie 1',                  slug:'chronicle-afrique-expatrier-p1-fr',          img:'morocco'  },
      { title:'Systèmes de santé pour expats',       slug:'chronicle-sante-expats-2026-fr',             img:'germany'  }
    ],
    es: [
      { title:'Mejores visados nómada digital 2026', slug:'chronicle-visas-nomadas-digitales-2026-es',  img:'portugal' },
      { title:'Asia 2026 — Parte 1',                 slug:'chronicle-asia-guia-expatriados-parte1-2026-es', img:'thailand' },
      { title:'2056: ¿dónde vivir mejor?',           slug:'chronicle-2056-mejores-paises-30-anos-es',   img:'norway'   },
      { title:'Australia: guía expatriados 2026',    slug:'chronicle-australia-guia-expatriados-2026-es', img:'australia' },
      { title:'África: parte 1',                     slug:'chronicle-africa-expatriarse-p1-es',          img:'morocco'  },
      { title:'Sistemas de salud para expats',       slug:'chronicle-salud-expats-2026-es',              img:'germany'  }
    ]
  };

  // Pick 3 items deterministically from the pool, derived from currentSlug.
  // Pool is already pre-filtered by category (POOL_CITY for city pages,
  // POOL_REGULAR for regular chronicles), so a slug-seeded shuffle keeps
  // related links semantically coherent enough for V1 while stabilising the
  // internal link graph across crawls. V2 (planned): enrich pool items with
  // {region,tags} and prefer pool entries sharing a region/tag with currentSlug
  // before falling back to the seeded shuffle on the rest.
  function pickThree(pool, currentSlug) {
    var p = pool.filter(function(item) { return item.slug !== currentSlug; });
    // 32-bit djb2-ish hash of the slug, used as seed so the same page always
    // shows the same 3 related cards (stable for SEO + user familiarity).
    var seed = 5381;
    for (var s = 0; s < currentSlug.length; s++) {
      seed = ((seed << 5) + seed + currentSlug.charCodeAt(s)) | 0;
    }
    if (seed === 0) seed = 1; // guard against degenerate seed
    function rng() {
      // LCG (Numerical Recipes constants), 31-bit positive
      seed = (Math.imul(seed, 1103515245) + 12345) & 0x7fffffff;
      return seed / 0x7fffffff;
    }
    for (var i = p.length - 1; i > 0; i--) {
      var j = Math.floor(rng() * (i + 1));
      var x = p[i]; p[i] = p[j]; p[j] = x;
    }
    return p.slice(0, 3);
  }

  function inject() {
    if (document.getElementById('wmRelated')) return;
    var siteFooter = document.getElementById('siteFooter');
    if (!siteFooter) return;

    var currentFile = path.split('/').pop().replace('.html', '');
    var pool = isCity ? (POOL_CITY[lang] || POOL_CITY.en) : (POOL_REGULAR[lang] || POOL_REGULAR.en);
    var picks = pickThree(pool, currentFile);
    if (picks.length === 0) return;

    var basePath = isCity ? '/chronicles/villes/' : '/chronicles/';
    var html = '<section id="wmRelated" class="wm-rel" aria-label="Related articles">' +
      '<div class="wm-rel-inner">' +
        '<h3 class="wm-rel-title">' + t.title + '</h3>' +
        '<div class="wm-rel-grid">' +
          picks.map(function(item) {
            return '<a class="wm-rel-card" href="' + basePath + item.slug + '.html">' +
              '<div class="wm-rel-thumb" style="background-image:url(\'/assets/hero-' + item.img + '.jpg\')"></div>' +
              '<div class="wm-rel-body"><div class="wm-rel-name">' + item.title + '</div></div>' +
              '</a>';
          }).join('') +
        '</div>' +
      '</div>' +
    '</section>';

    siteFooter.parentNode.insertBefore(
      Object.assign(document.createElement('div'), { innerHTML: html }).firstChild,
      siteFooter
    );

    if (!document.getElementById('wmRelStyle')) {
      var st = document.createElement('style');
      st.id = 'wmRelStyle';
      st.textContent =
        '.wm-rel{padding:48px 24px 24px;background:#faf8f3;border-top:1px solid rgba(0,0,0,.06);font-family:Inter,system-ui,sans-serif}' +
        '.wm-rel-inner{max-width:900px;margin:0 auto}' +
        '.wm-rel-title{font-family:Fraunces,Georgia,serif;font-size:clamp(20px,2.6vw,26px);font-weight:700;letter-spacing:-.01em;text-align:center;margin:0 0 22px;color:#171714}' +
        '.wm-rel-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}' +
        '.wm-rel-card{position:relative;border-radius:2px;overflow:hidden;aspect-ratio:4/3;background:#1a1a1a;text-decoration:none;cursor:pointer;transition:transform .2s ease,box-shadow .25s;display:block}' +
        '.wm-rel-card:hover{transform:scale(1.02) translateY(-3px);box-shadow:0 10px 30px rgba(0,0,0,.15)}' +
        '.wm-rel-thumb{position:absolute;inset:0;background-size:cover;background-position:center;transition:transform .4s ease}' +
        '.wm-rel-card:hover .wm-rel-thumb{transform:scale(1.05)}' +
        '.wm-rel-card::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.85),rgba(0,0,0,.15) 50%,transparent)}' +
        '.wm-rel-body{position:absolute;left:0;right:0;bottom:0;padding:14px 16px;z-index:2;color:#fff}' +
        '.wm-rel-name{font-family:Fraunces,Georgia,serif;font-size:15px;font-weight:700;line-height:1.2;letter-spacing:-.01em}' +
        '@media(max-width:720px){.wm-rel{padding:36px 18px 20px}.wm-rel-grid{grid-template-columns:1fr 1fr;gap:10px}.wm-rel-name{font-size:13px}}' +
        '@media(max-width:420px){.wm-rel-grid{grid-template-columns:1fr 1fr}}';
      document.head.appendChild(st);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    setTimeout(inject, 50);
  }
})();

// ── Newsletter capture (footer area) ──
(function() {
  // Don't show on PWA install / private pages
  var path = window.location.pathname;
  if (/onboarding|mon-compte|404/.test(path)) return;

  var lang = (localStorage.getItem('wigg_lang') || 'en').toLowerCase();
  if (['en','fr','es'].indexOf(lang) === -1) lang = 'en';

  var T = {
    en: { title:'Get the best of WiggMap', sub:'1 chronicle a week. Visas, cost of living, expat life. No spam.', placeholder:'your@email.com', subscribe:'Subscribe', thanks:'✓ Thanks! Check your inbox.', error:'Please enter a valid email.' },
    fr: { title:'Recevez le meilleur de WiggMap', sub:'1 chronique par semaine. Visas, coût de la vie, expatriation. Sans spam.', placeholder:'ton@email.com', subscribe:'S\'abonner', thanks:'✓ Merci ! Vérifie ta boîte mail.', error:'Email invalide.' },
    es: { title:'Recibe lo mejor de WiggMap', sub:'1 crónica por semana. Visados, coste de vida, vida expat. Sin spam.', placeholder:'tu@email.com', subscribe:'Suscribirme', thanks:'✓ ¡Gracias! Revisa tu bandeja.', error:'Email no válido.' }
  };
  var t = T[lang];

  function inject() {
    if (document.getElementById('wmNewsletter')) return;
    var footer = document.getElementById('wmSiteFooter');
    if (!footer) return;

    var html =
      '<section id="wmNewsletter" class="wm-nl" aria-label="Newsletter signup">' +
        '<div class="wm-nl-inner">' +
          '<div class="wm-nl-text">' +
            '<h3 class="wm-nl-title">' + t.title + '</h3>' +
            '<p class="wm-nl-sub">' + t.sub + '</p>' +
          '</div>' +
          '<form class="wm-nl-form" id="wmNlForm" name="newsletter" method="POST" data-netlify="true">' +
            '<input type="hidden" name="form-name" value="newsletter">' +
            '<input class="wm-nl-input" id="wmNlEmail" type="email" name="email" placeholder="' + t.placeholder + '" required>' +
            '<button class="wm-nl-btn" type="submit">' + t.subscribe + '</button>' +
          '</form>' +
          '<div class="wm-nl-msg" id="wmNlMsg"></div>' +
        '</div>' +
      '</section>';

    footer.parentNode.insertBefore(
      Object.assign(document.createElement('div'), { innerHTML: html }).firstChild,
      footer
    );

    if (!document.getElementById('wmNlStyle')) {
      var st = document.createElement('style');
      st.id = 'wmNlStyle';
      st.textContent =
        '.wm-nl{background:#1c1710;padding:48px 24px;color:#fff;font-family:Inter,system-ui,sans-serif;border-top:1px solid rgba(255,255,255,.06)}' +
        '.wm-nl-inner{max-width:880px;margin:0 auto;display:flex;flex-direction:column;align-items:center;gap:18px;text-align:center}' +
        '.wm-nl-text{max-width:46ch}' +
        '.wm-nl-title{font-family:Fraunces,Georgia,serif;font-size:clamp(22px,3vw,30px);font-weight:700;letter-spacing:-.01em;line-height:1.15;margin:0 0 8px}' +
        '.wm-nl-sub{font-size:14px;color:rgba(255,255,255,.6);line-height:1.55;margin:0}' +
        '.wm-nl-form{display:flex;gap:8px;width:100%;max-width:480px;flex-wrap:wrap}' +
        '.wm-nl-input{flex:1;min-width:180px;padding:13px 18px;border:1px solid rgba(255,255,255,.15);border-radius:2px;background:rgba(255,255,255,.05);color:#fff;font-family:Inter,sans-serif;font-size:14px;outline:none;transition:border-color .15s,background .15s}' +
        '.wm-nl-input::placeholder{color:rgba(255,255,255,.4)}' +
        '.wm-nl-input:focus{border-color:#22c55e;background:rgba(255,255,255,.08)}' +
        '.wm-nl-btn{padding:13px 26px;background:#22c55e;color:#0a1f10;border:none;border-radius:2px;font-family:Inter,sans-serif;font-size:13px;font-weight:700;cursor:pointer;transition:background .15s,transform .15s;letter-spacing:.02em}' +
        '.wm-nl-btn:hover{background:#16a34a;transform:translateY(-1px)}' +
        '.wm-nl-msg{font-size:13px;font-weight:600;min-height:18px;color:#22c55e}' +
        '.wm-nl-msg.err{color:#f87171}' +
        '@media(max-width:520px){.wm-nl{padding:36px 18px}.wm-nl-form{flex-direction:column}.wm-nl-btn{width:100%}}';
      document.head.appendChild(st);
    }

    // ─────────────────────────────────────────────────────────────
    // EMAIL SERVICE CONFIG — change BUTTONDOWN_USERNAME to switch
    // ─────────────────────────────────────────────────────────────
    // Default: Netlify Forms (stores emails in your Netlify dashboard)
    // To also auto-add subscribers to Buttondown:
    //   1. Sign up at https://buttondown.email (free up to 100 subs)
    //   2. Set BUTTONDOWN_USERNAME below to your username
    //   3. Done — every signup is dual-posted to Netlify + Buttondown
    var BUTTONDOWN_USERNAME = 'wiggmap'; // ← e.g. 'wiggmap'

    var form = document.getElementById('wmNlForm');
    var msg = document.getElementById('wmNlMsg');
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var email = document.getElementById('wmNlEmail').value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        msg.className = 'wm-nl-msg err';
        msg.textContent = t.error;
        return;
      }
      // 1. Submit to Netlify Forms (always — primary storage)
      var fd = new FormData(form);
      var netlifyPromise = fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(fd).toString()
      });
      // 2. Optionally also send to Buttondown
      var buttondownPromise = Promise.resolve();
      if (BUTTONDOWN_USERNAME) {
        var bdData = new FormData();
        bdData.append('email', email);
        bdData.append('tag', 'wiggmap_newsletter_' + lang);
        buttondownPromise = fetch('https://buttondown.email/api/emails/embed-subscribe/' + BUTTONDOWN_USERNAME, {
          method: 'POST',
          mode: 'no-cors',
          body: bdData
        }).catch(function(){}); // best-effort
      }
      // 3. Track Meta conversion event
      if (window.wmTrackEvent) window.wmTrackEvent('Lead', { content_name: 'newsletter_signup', content_category: lang });
      // 4. UI feedback
      Promise.allSettled([netlifyPromise, buttondownPromise]).then(function() {
        msg.className = 'wm-nl-msg';
        msg.textContent = t.thanks;
        form.style.display = 'none';
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    setTimeout(inject, 100);
  }
})();
