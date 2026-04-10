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
            <a href="#" id="wmCookieReset">Cookies</a>
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
      .wm-footer a{
        color: rgba(0,0,0,.62);
        text-decoration: none;
        font-weight: 700;
      }
      .wm-footer a:hover{
        text-decoration: underline;
      }
      .wm-footer__sep{
        opacity: .55;
        font-weight: 900;
      }
    </style>
  `;

  document.body.insertAdjacentHTML("beforeend", footerHTML);

  // Cookie preferences reset link
  var cookieLink = document.getElementById('wmCookieReset');
  if (cookieLink) {
    cookieLink.addEventListener('click', function(e) {
      e.preventDefault();
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
