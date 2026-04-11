// data/header.js

// ═════════════════════════════════════════════════════════════════
// META PIXEL — Facebook/Instagram retargeting & conversion tracking
// ═════════════════════════════════════════════════════════════════
// Replace 'YOUR_PIXEL_ID' below with the actual pixel ID once created at
// https://business.facebook.com/events_manager/ → "Connect data sources" → Web → Pixel
// The pixel respects the cookie consent — it only fires after user opts in.
(function () {
  var META_PIXEL_ID = '867064843065581'; // ← REPLACE WITH REAL ID
  if (META_PIXEL_ID === 'YOUR_PIXEL_ID') return; // skip until configured
  function loadPixel() {
    if (window.fbq) return;
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
    document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', META_PIXEL_ID);
    fbq('track', 'PageView');
    // Expose globally for custom event tracking (e.g. fbq('track','Lead') on signup)
    window.wmTrackEvent = function(name, params) { if (window.fbq) fbq('track', name, params || {}); };
  }
  // Respect cookie consent: only load pixel if user accepted
  if (localStorage.getItem('wigg_consent') === 'accepted') {
    loadPixel();
  } else {
    // Wait for opt-in via the cookie banner (custom event from footer.js)
    window.addEventListener('wigg_consent_granted', loadPixel);
  }
})();

(function () {
  const isSubPage = document.location.pathname.includes("/countries/")
                 || document.location.pathname.includes("/chronicles/");
  const isDeepPage2 = document.location.pathname.includes("/chronicles/villes/");
  const isDeepPage3 = document.location.pathname.includes("/compare/static/");
  const prefix = isDeepPage3 ? "../../../" : (isDeepPage2 ? "../../" : (isSubPage ? "../" : ""));
  const homeLink = prefix + "index.html";
  const globeLink = prefix + "globe.html";
  const aboutLink = prefix + "about.html";

  const TELEGRAM_URL = "https://t.me/wiggmap";
  const X_URL = "https://x.com/wiggmap70349";
  const IG_URL = "https://www.instagram.com/wiggmap?igsh=MWQ4eWowd3Q3MmRhMg==";

  const LANGS = {
    en: { flag: "🇬🇧", label: "English" },
    fr: { flag: "🇫🇷", label: "Français" },
    es: { flag: "🇪🇸", label: "Español" }
  };

  const SOCIALS = [
    { href: X_URL,        label: "X (Twitter)",  svg: `<svg viewBox="0 0 24 24" width="16" height="16"><path fill="#000000" d="M18.9 2H22l-6.6 7.6L23.5 22h-6.7l-5.2-6.8L5.6 22H2.5l7.1-8.2L.5 2h6.8l4.7 6.1L18.9 2Zm-1.2 18h1.8L6.2 3.9H4.3L17.7 20Z"/></svg>` },
    { href: IG_URL,       label: "Instagram",    svg: `<svg viewBox="0 0 24 24" width="16" height="16"><defs><linearGradient id="ig_wmh2" x1="0%" y1="100%" x2="100%" y2="0%"><stop offset="0%" stop-color="#FCAF45"/><stop offset="35%" stop-color="#FD1D1D"/><stop offset="65%" stop-color="#C13584"/><stop offset="100%" stop-color="#405DE6"/></linearGradient></defs><path fill="url(#ig_wmh2)" d="M7.8 2h8.4A5.8 5.8 0 0 1 22 7.8v8.4A5.8 5.8 0 0 1 16.2 22H7.8A5.8 5.8 0 0 1 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2Zm0 2A3.8 3.8 0 0 0 4 7.8v8.4A3.8 3.8 0 0 0 7.8 20h8.4a3.8 3.8 0 0 0 3.8-3.8V7.8A3.8 3.8 0 0 0 16.2 4H7.8Z"/><path fill="url(#ig_wmh2)" d="M12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z"/><circle fill="url(#ig_wmh2)" cx="17.5" cy="6.5" r="1.1"/></svg>` },
    { href: TELEGRAM_URL, label: "Telegram",     svg: `<svg viewBox="0 0 24 24" width="16" height="16"><path fill="#29B6F6" d="M21.9 4.6c.2-.8-.5-1.5-1.3-1.2L2.7 10.4c-.9.4-.9 1.7.1 2l4.6 1.5 1.8 5.6c.3 1 1.6 1.1 2.1.3l2.6-3.7 4.9 3.6c.7.5 1.7.1 1.9-.8l1.2-14.3ZM8.3 13.2l9.9-6.1-7.6 7.4-.3 3.9-1.7-5.1-2.5-.8Z"/></svg>` },
  ];

  const NAV_I18N = {
    en: { search: "Search", chronicles: "Chronicles", compare: "Compare", globe: "Globe", match: "WiggMatch" },
    fr: { search: "Recherche", chronicles: "Chroniques", compare: "Comparer", globe: "Globe", match: "WiggMatch" },
    es: { search: "Buscar", chronicles: "Crónicas", compare: "Comparar", globe: "Globo", match: "WiggMatch" },
  };

  const svgSearch = `<svg viewBox="0 0 24 24" width="16" height="16"><path fill="#6366F1" d="M15.5 14h-.79l-.28-.27A6.47 6.47 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>`;

  const svgBurger = `<svg viewBox="0 0 24 24" width="17" height="17"><rect fill="currentColor" x="3" y="5" width="18" height="2" rx="1"/><rect fill="currentColor" x="3" y="11" width="18" height="2" rx="1"/><rect fill="currentColor" x="3" y="17" width="18" height="2" rx="1"/></svg>`;

  const svgGame = `<svg viewBox="0 0 24 24" width="18" height="18"><path fill="#8B5CF6" d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-10 7H8v3H6v-3H3v-2h3V8h2v3h3v2zm4.5 2c-.83 0-1.5-.67-1.5-1.5S14.67 12 15.5 12s1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4-3c-.83 0-1.5-.67-1.5-1.5S18.67 9 19.5 9s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>`;

  const svgMatch = `<svg viewBox="0 0 24 24" width="17" height="17"><path fill="#16A34A" d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>`;

  const svgChronicles = `<svg viewBox="0 0 24 24" width="17" height="17"><path fill="#D97706" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>`;

  const svgCompare = `<svg viewBox="0 0 24 24" width="17" height="17"><path fill="#3B82F6" d="M9.01 14H2v2h7.01v3L13 15l-3.99-4v3zm5.98-1v-3H22V8h-7.01V5L11 9l3.99 4z"/></svg>`;

  const svgGlobe = `<svg viewBox="0 0 24 24" width="17" height="17"><path fill="#22C55E" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>`;

  if (!document.getElementById("wmhStyle")) {
    const st = document.createElement("style");
    st.id = "wmhStyle";
    st.textContent = `
      .wmh-bar{
        position:sticky; top:0; z-index:9999;
        background:rgba(246,248,247,.95);
        backdrop-filter:blur(10px);
        border-bottom:1px solid rgba(0,0,0,.08);
      }
      .wmh-bar, .wmh-bar *{ box-sizing:border-box !important; font-family:Arial,Helvetica,sans-serif !important; }
      .wmh-bar a{ text-decoration:none !important; }
      .wmh-bar svg{ display:block !important; }

      .wmh-inner{
        max-width:1100px; margin:0 auto;
        padding:10px 14px;
        display:flex; align-items:center; justify-content:space-between;
        gap:10px;
      }

      .wmh-left{ display:flex; align-items:center; }
      .wmh-brand img{ height:54px; width:auto; display:block; }

      .wmh-right{
        display:flex; align-items:center; justify-content:flex-end;
        gap:10px; flex-wrap:nowrap !important;
      }

      /* Social icons desktop */
      .wmh-social{ display:flex; align-items:center; gap:6px; }
      .wmh-ico{
        width:36px; height:36px;
        display:inline-flex; align-items:center; justify-content:center;
        border:1px solid rgba(0,0,0,.10);
        background:rgba(255,255,255,.80);
        border-radius:10px; color:#18201c;
        transition:background .15s;
      }
      .wmh-ico:hover{ background:#fff; }
      .wmh-ico--x{ background:rgba(0,0,0,.05); border-color:rgba(0,0,0,.18); }
      .wmh-ico--x:hover{ background:rgba(0,0,0,.10); }
      .wmh-ico--ig{ background:rgba(193,53,132,.07); border-color:rgba(193,53,132,.22); }
      .wmh-ico--ig:hover{ background:rgba(193,53,132,.14); }
      .wmh-ico--tg{ background:rgba(41,182,246,.12); border-color:rgba(41,182,246,.30); }
      .wmh-ico--tg:hover{ background:rgba(41,182,246,.22); }

      /* Nav buttons */
      .wmh-nav{ display:flex; align-items:center; gap:8px; flex-wrap:nowrap !important; }
      .wmh-btn{
        font-weight:900; font-size:13px; color:#5b6b62;
        padding:7px 11px; border-radius:999px;
        border:1px solid rgba(0,0,0,.10);
        background:rgba(255,255,255,.80);
        display:inline-flex; align-items:center; gap:6px;
        cursor:pointer;
        transition:background .15s, color .15s;
      }
      .wmh-btn:hover{ background:#fff; color:#18201c; }

      /* Dropdown base */
      .wmh-dropdown{ position:relative; }
      .wmh-drop-trigger{
        display:inline-flex; align-items:center; gap:5px;
        padding:6px 10px; border-radius:999px;
        border:1px solid rgba(0,0,0,.10);
        background:rgba(255,255,255,.80);
        cursor:pointer; font-size:15px; font-weight:800;
        color:#18201c; transition:background .15s;
        user-select:none; white-space:nowrap;
      }
      .wmh-drop-trigger:hover{ background:#fff; }
      .wmh-drop-trigger .arrow{
        font-size:9px; color:#999;
        transition:transform .2s; display:inline-block;
      }
      .wmh-dropdown.open .arrow{ transform:rotate(180deg); }

      .wmh-drop-menu{
        display:none;
        position:absolute; top:calc(100% + 7px); right:0;
        background:#fff;
        border:1px solid rgba(0,0,0,.10);
        border-radius:12px;
        box-shadow:0 8px 28px rgba(0,0,0,.13);
        min-width:150px; overflow:hidden;
        z-index:10000;
      }
      .wmh-dropdown.open .wmh-drop-menu{ display:block; }
      .wmh-drop-left{ left:0 !important; right:auto !important; }

      .wmh-drop-item{
        display:flex; align-items:center; gap:9px;
        padding:10px 15px;
        font-size:13px; font-weight:800; color:#18201c;
        cursor:pointer; transition:background .12s;
        white-space:nowrap; text-decoration:none !important;
      }
      .wmh-drop-item:hover{ background:rgba(0,0,0,.05); }
      .wmh-drop-item.active{ background:rgba(0,0,0,.07); }
      .wmh-drop-item + .wmh-drop-item{ border-top:1px solid rgba(0,0,0,.05); }

      /* Search panel */
      .wmh-search-panel{ min-width:300px; padding:10px 10px 8px; }
      .wmh-search-panel input{
        width:100%; padding:8px 12px; font-size:14px;
        border:1px solid rgba(0,0,0,.15); border-radius:8px;
        background:#fff; color:#18201c; outline:none;
        font-family:Arial,Helvetica,sans-serif !important;
      }
      .wmh-search-panel input:focus{ border-color:#22c55e; box-shadow:0 0 0 2px rgba(34,197,94,.15); }
      .wmh-search-results{ max-height:230px; overflow-y:auto; margin-top:6px; }
      .wmh-search-results .wmh-drop-item{ padding:8px 10px; font-size:13px; white-space:normal; }
      .wmh-search-empty{ padding:10px 12px; font-size:13px; color:#999; text-align:center; }

      /* Mobile hamburger (top row) — caché sur desktop */
      .wmh-menu-top-m{ display:none; }

      /* Mobile */
      @media (max-width: 768px){
        .wmh-inner{ padding:6px 12px !important; gap:6px; flex-wrap:wrap; }
        .wmh-brand img{ height:40px !important; }
        .wmh-social{ display:none !important; }
        .wmh-right .wmh-nav{ display:none !important; }
        .wmh-right .wmh-lang-wrap{ display:none !important; }
        .wmh-right{ flex:1 1 auto; justify-content:flex-end; align-items:center; gap:6px; }

        /* Hamburger top row — inline-flex pour ne pas casser le layout du trigger */
        .wmh-menu-top-m{ display:inline-flex !important; padding:5px 9px !important; }
        /* Masquer la flèche ▾ dans le hamburger mobile (redondant avec l'icône ☰) */
        #wmhMenuTopM .arrow{ display:none !important; }

        /* Grille 2 colonnes égales pour Recherche + Random */
        .wmh-nav-mobile{
          display:grid !important;
          grid-template-columns:1fr 1fr;
          gap:6px; width:100%; flex-basis:100%;
          margin-top:2px;
        }
        /* Le dropdown search prend toute la cellule */
        .wmh-nav-mobile .wmh-dropdown{ width:100%; display:block; }
        /* Boutons : pleine largeur, bien centrés, hauteur uniforme */
        .wmh-nav-mobile .wmh-btn,
        .wmh-nav-mobile .wmh-dropdown .wmh-btn{
          box-sizing:border-box;
          width:100%; height:34px !important;
          display:inline-flex; align-items:center; justify-content:center;
          padding:0 8px !important; margin:0;
          font-size:12px !important; font-weight:700; line-height:1;
          border:1px solid rgba(0,0,0,.10);
          background:rgba(255,255,255,.80);
          font-family:inherit;
        }
        /* Panneau de recherche plein écran */
        .wmh-search-panel{ min-width:calc(100vw - 28px); }
        /* Positionnement des menus déroulants dans la grille */
        .wmh-nav-mobile .wmh-dropdown:first-child .wmh-drop-menu{ left:0; right:auto; }
        .wmh-nav-mobile .wmh-dropdown:last-child .wmh-drop-menu{ right:0; left:auto; }
      }

      /* Petits écrans réels — encore plus compact */
      @media (max-width: 480px){
        .wmh-inner{ padding:5px 10px !important; gap:5px; }
        .wmh-brand img{ height:36px !important; }
        .wmh-menu-top-m{ padding:4px 8px !important; }
        .wmh-nav-mobile{ gap:5px; margin-top:1px; }
        .wmh-nav-mobile .wmh-btn,
        .wmh-nav-mobile .wmh-dropdown .wmh-btn{
          height:32px !important;
          font-size:11.5px !important;
          padding:0 6px !important;
        }
      }

      .wmh-nav-mobile{ display:none; }
    `;
    document.head.appendChild(st);
  }

  const currentLang = localStorage.getItem("wigg_lang") || "en";
  const currentLangData = LANGS[currentLang] || LANGS.en;
  const ni = NAV_I18N[currentLang] || NAV_I18N.en;

  const socialItems = SOCIALS.map(s =>
    `<a class="wmh-drop-item" href="${s.href}" target="_blank" rel="noopener noreferrer">${s.svg} ${s.label}</a>`
  ).join("");

  const langItems = Object.entries(LANGS).map(([code, d]) =>
    `<div class="wmh-drop-item ${code === currentLang ? 'active' : ''}" data-lang="${code}"><span>${d.flag}</span> ${d.label}</div>`
  ).join("");

  const svgShare = `<svg viewBox="0 0 24 24" width="17" height="17"><path fill="currentColor" d="M18 16c-.8 0-1.4.3-1.9.8L8.9 12.7c.1-.2.1-.5.1-.7s0-.5-.1-.7l7.1-4.1c.5.5 1.2.8 2 .8 1.7 0 3-1.3 3-3s-1.3-3-3-3-3 1.3-3 3c0 .2 0 .5.1.7L7.9 9.8C7.4 9.3 6.7 9 6 9c-1.7 0-3 1.3-3 3s1.3 3 3 3c.7 0 1.4-.3 1.9-.8l7.2 4.1c-.1.2-.1.4-.1.7 0 1.6 1.3 2.9 2.9 2.9s2.9-1.3 2.9-2.9S19.6 16 18 16z"/></svg>`;

  const menuItemsHTML = `
    <a class="wmh-drop-item" href="${prefix}indexchronicles.html">${svgChronicles} ${ni.chronicles}</a>
    <a class="wmh-drop-item" href="${prefix}compare.html?c=thailand,indonesia,portugal">${svgCompare} ${ni.compare}</a>
    <a class="wmh-drop-item" href="${globeLink}" target="_blank" rel="noopener noreferrer">${svgGlobe} ${ni.globe}</a>
    <a class="wmh-drop-item" href="${prefix}wiggmatch.html">${svgMatch} ${ni.match}</a>
    <a class="wmh-drop-item" href="${prefix}ggg/wigggame.html">${svgGame} Quiz</a>
  `;

  const searchDropHTML = (id, inputId, resultsId, icon) => `
    <div class="wmh-dropdown" id="${id}">
      <button class="wmh-btn" id="${id}Trig">${icon} ${ni.search}</button>
      <div class="wmh-drop-menu wmh-search-panel wmh-drop-left" id="${id}Panel">
        <input type="text" id="${inputId}" autocomplete="off" placeholder="${ni.search}…">
        <div class="wmh-search-results" id="${resultsId}"></div>
      </div>
    </div>`;

  const burgerDropHTML = (id, trigClass) => `
    <div class="wmh-dropdown" id="${id}">
      <div class="${trigClass}" id="${id}Trig">${svgBurger}<span class="arrow">▾</span></div>
      <div class="wmh-drop-menu">${menuItemsHTML}</div>
    </div>`;

  const headerHTML = `
    <header class="wmh-bar">
      <div class="wmh-inner">
        <div class="wmh-left">
          <a class="wmh-brand" href="${homeLink}" aria-label="WiggMap home">
            <img src="/assets/logo.png" alt="WiggMap logo">
          </a>
        </div>
        <div class="wmh-right">

          <!-- Icônes sociales — desktop uniquement -->
          <div class="wmh-social">
            <a class="wmh-ico wmh-ico--x" href="${X_URL}" target="_blank" rel="noopener noreferrer" title="X">
              <svg viewBox="0 0 24 24" width="17" height="17"><path fill="#000000" d="M18.9 2H22l-6.6 7.6L23.5 22h-6.7l-5.2-6.8L5.6 22H2.5l7.1-8.2L.5 2h6.8l4.7 6.1L18.9 2Zm-1.2 18h1.8L6.2 3.9H4.3L17.7 20Z"/></svg>
            </a>
            <a class="wmh-ico wmh-ico--ig" href="${IG_URL}" target="_blank" rel="noopener noreferrer" title="Instagram">
              <svg viewBox="0 0 24 24" width="17" height="17">
                <defs><linearGradient id="ig_wmh" x1="0%" y1="100%" x2="100%" y2="0%"><stop offset="0%" stop-color="#FCAF45"/><stop offset="35%" stop-color="#FD1D1D"/><stop offset="65%" stop-color="#C13584"/><stop offset="100%" stop-color="#405DE6"/></linearGradient></defs>
                <path fill="url(#ig_wmh)" d="M7.8 2h8.4A5.8 5.8 0 0 1 22 7.8v8.4A5.8 5.8 0 0 1 16.2 22H7.8A5.8 5.8 0 0 1 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2Zm0 2A3.8 3.8 0 0 0 4 7.8v8.4A3.8 3.8 0 0 0 7.8 20h8.4a3.8 3.8 0 0 0 3.8-3.8V7.8A3.8 3.8 0 0 0 16.2 4H7.8Z"/>
                <path fill="url(#ig_wmh)" d="M12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z"/>
                <circle fill="url(#ig_wmh)" cx="17.5" cy="6.5" r="1.1"/>
              </svg>
            </a>
            <a class="wmh-ico wmh-ico--tg" href="${TELEGRAM_URL}" target="_blank" rel="noopener noreferrer" title="Telegram">
              <svg viewBox="0 0 24 24" width="17" height="17"><path fill="#29B6F6" d="M21.9 4.6c.2-.8-.5-1.5-1.3-1.2L2.7 10.4c-.9.4-.9 1.7.1 2l4.6 1.5 1.8 5.6c.3 1 1.6 1.1 2.1.3l2.6-3.7 4.9 3.6c.7.5 1.7.1 1.9-.8l1.2-14.3ZM8.3 13.2l9.9-6.1-7.6 7.4-.3 3.9-1.7-5.1-2.5-.8Z"/></svg>
            </a>
          </div>

          <!-- Dropdown réseaux — mobile uniquement, caché par défaut -->
          <div class="wmh-dropdown" id="wmhSocialDropdown" style="display:none;">
            <div class="wmh-drop-trigger" id="wmhSocialTrigger">
              ${svgShare}<span class="arrow">▾</span>
            </div>
            <div class="wmh-drop-menu">${socialItems}</div>
          </div>

          <!-- Hamburger — mobile top row (entre réseaux et langue) -->
          ${burgerDropHTML("wmhMenuTopM", "wmh-drop-trigger wmh-menu-top-m")}

          <!-- Nav desktop : Search + Random + Hamburger -->
          <nav class="wmh-nav">
            ${searchDropHTML("wmhSearchDrop", "wmhSearchInput", "wmhSearchResults", svgSearch)}
            <a class="wmh-btn" href="#" id="btnRandom">🎲 Random</a>
            ${burgerDropHTML("wmhMenuDrop", "wmh-drop-trigger")}
          </nav>

          <!-- Auth button -->
          <div id="wigg-auth-btn" style="display:flex;align-items:center;"></div>

          <!-- Dropdown langue — desktop : tout à droite -->
          <div class="wmh-dropdown wmh-lang-wrap" id="wmhLangDropdown">
            <div class="wmh-drop-trigger" id="wmhLangTrigger">
              <span>${currentLangData.flag}</span><span class="arrow">▾</span>
            </div>
            <div class="wmh-drop-menu">${langItems}</div>
          </div>
        </div>

        <!-- Mobile grid : Search + Random seulement (2 colonnes) -->
        <nav class="wmh-nav-mobile">
          ${searchDropHTML("wmhSearchDropM", "wmhSearchInputM", "wmhSearchResultsM", "🔍")}
          <a class="wmh-btn" href="#" id="btnRandomMobile">🎲 Random</a>
        </nav>
      </div>
    </header>
  `;

  const mount = document.getElementById("siteHeader");
  if (!mount) return console.warn("siteHeader not found");
  mount.innerHTML = headerHTML;

  function updateMobileVisibility(){
    const isMobile = window.innerWidth <= 768;
    const social = document.getElementById("wmhSocialDropdown");
    if(social) social.style.display = isMobile ? "block" : "none";
    const langWrap = document.getElementById("wmhLangDropdown");
    if(langWrap){
      if(isMobile){ langWrap.style.display = "block"; langWrap.classList.remove("wmh-lang-wrap"); }
      else { langWrap.style.display = ""; langWrap.classList.add("wmh-lang-wrap"); }
    }
  }
  updateMobileVisibility();
  window.addEventListener("resize", updateMobileVisibility);

  function initDropdown(triggerId, dropdownId){
    const trigger = document.getElementById(triggerId);
    const dropdown = document.getElementById(dropdownId);
    if(!trigger || !dropdown) return;
    trigger.addEventListener("click", e => {
      e.stopPropagation();
      const wasOpen = dropdown.classList.contains("open");
      document.querySelectorAll(".wmh-dropdown.open").forEach(d => d.classList.remove("open"));
      if(!wasOpen) dropdown.classList.add("open");
    });
  }
  document.addEventListener("click", () => {
    document.querySelectorAll(".wmh-dropdown.open").forEach(d => d.classList.remove("open"));
  });

  initDropdown("wmhLangTrigger", "wmhLangDropdown");
  initDropdown("wmhSocialTrigger", "wmhSocialDropdown");
  initDropdown("wmhMenuDropTrig", "wmhMenuDrop");
  initDropdown("wmhMenuTopMTrig", "wmhMenuTopM");

  // Search logic
  let countriesCache = null;
  async function loadCountries(){
    if(countriesCache) return countriesCache;
    const f = currentLang === "fr" ? "/data/countries.fr.json" :
              currentLang === "es" ? "/data/countries.es.json" : "/data/countries.json";
    try{
      const r = await fetch(f + "?nc=" + Date.now(), { cache:"no-store" });
      countriesCache = await r.json();
    }catch(e){ countriesCache = {}; }
    return countriesCache;
  }

  function slugToName(slug){
    return slug.split("-").map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
  }

  const SEARCH_EXTRAS=[{n:"Abu Dhabi",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-abu-dhabi-emirats-{lang}.html"},
    {n:"Ankara",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-ankara-turquie-{lang}.html"},
    {n:"Antalya",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-antalya-turquie-{lang}.html"},
    {n:"Athens",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-athenes-grece-{lang}.html"},
    {n:"Austin",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-austin-usa-{lang}.html"},
    {n:"Bali",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-bali-indonesia-{lang}.html"},
    {n:"Bangkok",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-bangkok-thailand-{lang}.html"},
    {n:"Barcelona",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-barcelone-espagne-{lang}.html"},
    {n:"Bariloche",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-bariloche-argentine-{lang}.html"},
    {n:"Berlin",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-berlin-allemagne-{lang}.html"},
    {n:"Bogotá",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-bogota-colombie-{lang}.html"},
    {n:"Buenos Aires",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-buenos-aires-argentine-{lang}.html"},
    {n:"Cairns",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-cairns-australia-{lang}.html"},
    {n:"Calgary",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-calgary-canada-{lang}.html"},
    {n:"Cali",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-cali-colombie-{lang}.html"},
    {n:"Cancún",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-cancun-mexico-{lang}.html"},
    {n:"Cartagena",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-cartagena-colombie-{lang}.html"},
    {n:"Chiang Mai",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-chiang-mai-thailand-{lang}.html"},
    {n:"Cologne",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-cologne-allemagne-{lang}.html"},
    {n:"Córdoba",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-cordoba-argentine-{lang}.html"},
    {n:"Da Nang",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-da-nang-vietnam-{lang}.html"},
    {n:"Dubai",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-dubai-emirats-{lang}.html"},
    {n:"Faro",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-faro-portugal-{lang}.html"},
    {n:"Florianópolis",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-florianopolis-bresil-{lang}.html"},
    {n:"Fukuoka",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-fukuoka-japan-{lang}.html"},
    {n:"Funchal",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-funchal-portugal-{lang}.html"},
    {n:"George Town",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-george-town-malaisie-{lang}.html"},
    {n:"Guadalajara",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-guadalajara-mexico-{lang}.html"},
    {n:"Hamburg",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-hambourg-allemagne-{lang}.html"},
    {n:"Hanoi",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-hanoi-vietnam-{lang}.html"},
    {n:"Heraklion",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-heraklion-grece-{lang}.html"},
    {n:"Ho Chi Minh City",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-ho-chi-minh-vietnam-{lang}.html"},
    {n:"Hội An",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-hoi-an-vietnam-{lang}.html"},
    {n:"Hua Hin",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-hua-hin-thailand-{lang}.html"},
    {n:"Istanbul",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-istanbul-turquie-{lang}.html"},
    {n:"Izmir",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-izmir-turquie-{lang}.html"},
    {n:"Jakarta",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-jakarta-indonesia-{lang}.html"},
    {n:"Johor Bahru",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-johor-bahru-malaisie-{lang}.html"},
    {n:"Kota Kinabalu",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-kota-kinabalu-malaisie-{lang}.html"},
    {n:"Kuala Lumpur",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-kuala-lumpur-malaisie-{lang}.html"},
    {n:"Kyoto",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-kyoto-japan-{lang}.html"},
    {n:"Chania",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-la-canee-grece-{lang}.html"},
    {n:"Lisbon",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-lisbonne-portugal-{lang}.html"},
    {n:"Los Angeles",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-los-angeles-usa-{lang}.html"},
    {n:"Lyon",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-lyon-france-{lang}.html"},
    {n:"Madrid",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-madrid-espagne-{lang}.html"},
    {n:"Málaga",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-malaga-espagne-{lang}.html"},
    {n:"Marseille",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-marseille-france-{lang}.html"},
    {n:"Medellín",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-medellin-colombie-{lang}.html"},
    {n:"Melbourne",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-melbourne-australia-{lang}.html"},
    {n:"Mendoza",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-mendoza-argentine-{lang}.html"},
    {n:"Mexico City",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-mexico-city-mexico-{lang}.html"},
    {n:"Miami",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-miami-usa-{lang}.html"},
    {n:"Monterrey",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-monterrey-mexico-{lang}.html"},
    {n:"Montreal",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-montreal-canada-{lang}.html"},
    {n:"Munich",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-munich-allemagne-{lang}.html"},
    {n:"New York",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-new-york-usa-{lang}.html"},
    {n:"Nice",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-nice-france-{lang}.html"},
    {n:"Osaka",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-osaka-japan-{lang}.html"},
    {n:"Paris",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-paris-france-{lang}.html"},
    {n:"Perth",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-perth-australia-{lang}.html"},
    {n:"Phuket",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-phuket-thailand-{lang}.html"},
    {n:"Porto",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-porto-portugal-{lang}.html"},
    {n:"Ras Al Khaimah",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-ras-al-khaimah-emirats-{lang}.html"},
    {n:"Rio de Janeiro",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-rio-bresil-{lang}.html"},
    {n:"Salvador de Bahia",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-salvador-bresil-{lang}.html"},
    {n:"São Paulo",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-sao-paulo-bresil-{lang}.html"},
    {n:"Sharjah",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-sharjah-emirats-{lang}.html"},
    {n:"Surabaya",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-surabaya-indonesia-{lang}.html"},
    {n:"Sydney",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-sydney-australia-{lang}.html"},
    {n:"Thessaloniki",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-thessalonique-grece-{lang}.html"},
    {n:"Tokyo",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-tokyo-japan-{lang}.html"},
    {n:"Toronto",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-toronto-canada-{lang}.html"},
    {n:"Valencia",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-valence-espagne-{lang}.html"},
    {n:"Vancouver",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-vancouver-canada-{lang}.html"},
    {n:"Yogyakarta",i:"🏙️",t:"city",u:"/chronicles/villes/chronicle-yogyakarta-indonesia-{lang}.html"},
    {n:"2056: Where Will Life Be Best in 30 Years? The Prospective G",i:"📖",t:"chronicle",u:"/chronicles/chronicle-2056-best-countries-30-years-en.html"},
    {n:"Expat in Africa 2026: The Complete Guide (18 Countries)",i:"📖",t:"chronicle",u:"/chronicles/chronicle-africa-expat-p1-en.html"},
    {n:"Living in North Africa &amp; Islands 2026: Morocco, Tunisia,",i:"📖",t:"chronicle",u:"/chronicles/chronicle-africa-expat-p2-en.html"},
    {n:"Living in East &amp; Southern Africa 2026: Kenya, Rwanda, Ta",i:"📖",t:"chronicle",u:"/chronicles/chronicle-africa-expat-p3-en.html"},
    {n:"Living in West Africa 2026: Senegal, Ghana, Ivory Coast + Fi",i:"📖",t:"chronicle",u:"/chronicles/chronicle-africa-expat-p4-en.html"},
    {n:"Expat Life Under the American Sun — Panama, Costa Rica, Puer",i:"📖",t:"chronicle",u:"/chronicles/chronicle-ameriques-partie1-en.html"},
    {n:"Expat Life Under the American Sun — St Kitts, Bahamas, Antig",i:"📖",t:"chronicle",u:"/chronicles/chronicle-ameriques-partie2-en.html"},
    {n:"Expat Life Under the American Sun — Anguilla, BVI, Sint Maar",i:"📖",t:"chronicle",u:"/chronicles/chronicle-ameriques-partie3-en.html"},
    {n:"Moving to Southeast Asia in 2026: Thailand, Vietnam, Bali, P",i:"📖",t:"chronicle",u:"/chronicles/chronicle-asia-expat-guide-part1-2026-en.html"},
    {n:"Moving to Asia in 2026: Japan, Laos, China, Cambodia — Visas",i:"📖",t:"chronicle",u:"/chronicles/chronicle-asia-expat-guide-part2-2026-en.html"},
    {n:"Australia 2026: Visas, Salaries, Quality of Life &amp; Regio",i:"📖",t:"chronicle",u:"/chronicles/chronicle-australia-expat-guide-2026-en.html"},
    {n:"The 25 Best Digital Nomad Visas in 2026",i:"📖",t:"chronicle",u:"/chronicles/chronicle-digital-nomad-visas-2026-en.html"},
    {n:"Expat Work Visas in 2026: the 25 Best Countries to Relocate ",i:"📖",t:"chronicle",u:"/chronicles/chronicle-expat-work-visas-2026-en.html"},
    {n:"6 Countries Nobody Thinks of for Expats in 2026",i:"📖",t:"chronicle",u:"/chronicles/chronicle-forgotten-expat-countries-2026-en.html"},
    {n:"The 25 Best Healthcare Systems for Expats in 2026",i:"📖",t:"chronicle",u:"/chronicles/chronicle-healthcare-expats-2026-en.html"},
    {n:"Buying Property Abroad: What Foreigners Actually Own in 15 C",i:"📖",t:"chronicle",u:"/chronicles/chronicle-property-abroad-2026-en.html"},
    {n:"Best Countries to Raise Children in 2026 — Education, Safety",i:"📖",t:"chronicle",u:"/chronicles/chronicle-raise-children-2026-en.html"},
    {n:"Am I really ready to move abroad in 2026?",i:"📖",t:"chronicle",u:"/chronicles/chronicle-ready-to-leave-en.html"},
    {n:"Retirement Visas in 2026: the 25 Best Options to Retire Abro",i:"📖",t:"chronicle",u:"/chronicles/chronicle-retirement-visas-2026-en.html"},
    {n:"Study Abroad 2026: Argentina, Canada, Mexico, Georgia, Moroc",i:"📖",t:"chronicle",u:"/chronicles/chronicle-study-abroad-americas-africa-2026-en.html"},
    {n:"Studying in Asia & Pacific 2026: Taiwan, South Korea, Malays",i:"📖",t:"chronicle",u:"/chronicles/chronicle-study-abroad-asia-pacific-2026-en.html"},
    {n:"Best Erasmus Destinations 2026: 8 European Cities for Studen",i:"📖",t:"chronicle",u:"/chronicles/chronicle-study-abroad-europe-erasmus-2026-en.html"},
    {n:"Practical guide: studying abroad in 2026 — fund, prepare, go",i:"📖",t:"chronicle",u:"/chronicles/chronicle-study-abroad-practical-guide-2026-en.html"},
    {n:"WiggMatch",i:"💚",t:"tool",u:"/wiggmatch.html"},
    {n:"Quiz",i:"🎮",t:"tool",u:"/ggg/wigggame.html"},
    {n:"Compare",i:"⚖️",t:"tool",u:"/compare.html"},
    {n:"Globe 3D",i:"🌍",t:"tool",u:"/globe.html"}];

  function renderResults(query, data, resultsEl){
    const q = query.toLowerCase().trim();
    if(!q){ resultsEl.innerHTML = ""; return; }
    const lg = (localStorage.getItem("wigg_lang") || "en").toLowerCase();
    const ul = ["en","fr","es"].includes(lg) ? lg : "en";
    const results = [];

    // Search countries
    const entries = Object.entries(data || {});
    entries.forEach(([slug, info]) => {
      const name = (info && (info.name || info.country || info.pays || info.pais) || slugToName(slug)).toLowerCase();
      if(name.includes(q) || slug.replace(/-/g," ").includes(q)){
        const display = (info && (info.name || info.country || info.pays || info.pais)) || slugToName(slug);
        const flag = (info && info.flag) ? info.flag + " " : "";
        results.push({html:`<a class="wmh-drop-item" href="/countries/${encodeURIComponent(slug)}-${ul}.html">${flag}${display}</a>`, priority:0});
      }
    });

    // Search extras (cities, chronicles, tools)
    if(typeof SEARCH_EXTRAS !== "undefined"){
      SEARCH_EXTRAS.forEach(ex => {
        if(ex.n.toLowerCase().includes(q)){
          const url = ex.u.replace("{lang}", ul);
          const label = ex.i + " " + ex.n;
          const cat = ex.t === "city" ? "ville" : ex.t === "chronicle" ? "article" : "";
          const tag = cat ? ` <span style="font-size:10px;color:#999;margin-left:4px">${cat}</span>` : "";
          results.push({html:`<a class="wmh-drop-item" href="${url}">${label}${tag}</a>`, priority: ex.t === "tool" ? -1 : 1});
        }
      });
    }

    if(!results.length){
      resultsEl.innerHTML = `<div class="wmh-search-empty">—</div>`;
      return;
    }
    // Sort: tools first, then countries, then extras
    results.sort((a,b) => a.priority - b.priority);
    resultsEl.innerHTML = results.slice(0, 10).map(r => r.html).join("");
  }

  function initSearch(dropId, inputId, resultsId){
    const drop = document.getElementById(dropId);
    const trigBtn = document.getElementById(dropId + "Trig");
    const input = document.getElementById(inputId);
    const resultsEl = document.getElementById(resultsId);
    if(!drop || !trigBtn || !input || !resultsEl) return;

    trigBtn.addEventListener("click", e => {
      e.stopPropagation();
      const wasOpen = drop.classList.contains("open");
      document.querySelectorAll(".wmh-dropdown.open").forEach(d => d.classList.remove("open"));
      if(!wasOpen){
        drop.classList.add("open");
        setTimeout(() => input.focus(), 50);
        loadCountries();
      }
    });

    input.addEventListener("click", e => e.stopPropagation());

    input.addEventListener("input", async () => {
      const data = await loadCountries();
      renderResults(input.value, data, resultsEl);
    });

    input.addEventListener("keydown", e => {
      if(e.key === "Escape"){ drop.classList.remove("open"); input.value = ""; resultsEl.innerHTML = ""; }
    });
  }

  initSearch("wmhSearchDrop", "wmhSearchInput", "wmhSearchResults");
  initSearch("wmhSearchDropM", "wmhSearchInputM", "wmhSearchResultsM");

  // Chronicle URL mapping — for language switching on article pages
  const CHRONICLE_LANGS = {
    "/chronicles/chronicle-2056-best-countries-30-years-en.html": { en: "/chronicles/chronicle-2056-best-countries-30-years-en.html", fr: "/chronicles/chronicle-2056-ou-vivra-t-on-le-mieux-fr.html",       es: "/chronicles/chronicle-2056-mejores-paises-30-anos-es.html" },
    "/chronicles/chronicle-2056-ou-vivra-t-on-le-mieux-fr.html":  { en: "/chronicles/chronicle-2056-best-countries-30-years-en.html", fr: "/chronicles/chronicle-2056-ou-vivra-t-on-le-mieux-fr.html",       es: "/chronicles/chronicle-2056-mejores-paises-30-anos-es.html" },
    "/chronicles/chronicle-2056-mejores-paises-30-anos-es.html":  { en: "/chronicles/chronicle-2056-best-countries-30-years-en.html", fr: "/chronicles/chronicle-2056-ou-vivra-t-on-le-mieux-fr.html",       es: "/chronicles/chronicle-2056-mejores-paises-30-anos-es.html" },

    "/chronicles/digital-nomads-2026-en.html": { en: "/chronicles/digital-nomads-2026-en.html", fr: "/chronicles/digital-nomads-2026-fr.html", es: "/chronicles/digital-nomads-2026-es.html" },
    "/chronicles/digital-nomads-2026-fr.html": { en: "/chronicles/digital-nomads-2026-en.html", fr: "/chronicles/digital-nomads-2026-fr.html", es: "/chronicles/digital-nomads-2026-es.html" },
    "/chronicles/digital-nomads-2026-es.html": { en: "/chronicles/digital-nomads-2026-en.html", fr: "/chronicles/digital-nomads-2026-fr.html", es: "/chronicles/digital-nomads-2026-es.html" },

    "/chronicles/expats-nomads-crypto-2026-en.html":      { en: "/chronicles/expats-nomads-crypto-2026-en.html",      fr: "/chronicles/expatries-nomades-crypto-2026-fr.html",    es: "/chronicles/expatriados-nomadas-crypto-2026-es.html" },
    "/chronicles/expatries-nomades-crypto-2026-fr.html":  { en: "/chronicles/expats-nomads-crypto-2026-en.html",      fr: "/chronicles/expatries-nomades-crypto-2026-fr.html",    es: "/chronicles/expatriados-nomadas-crypto-2026-es.html" },
    "/chronicles/expatriados-nomadas-crypto-2026-es.html":{ en: "/chronicles/expats-nomads-crypto-2026-en.html",      fr: "/chronicles/expatries-nomades-crypto-2026-fr.html",    es: "/chronicles/expatriados-nomadas-crypto-2026-es.html" },

    "/chronicles/chronicle-ameriques-partie1-en.html": { en: "/chronicles/chronicle-ameriques-partie1-en.html", fr: "/chronicles/chronicle-ameriques-partie1-fr.html", es: "/chronicles/chronicle-ameriques-partie1-es.html" },
    "/chronicles/chronicle-ameriques-partie1-fr.html": { en: "/chronicles/chronicle-ameriques-partie1-en.html", fr: "/chronicles/chronicle-ameriques-partie1-fr.html", es: "/chronicles/chronicle-ameriques-partie1-es.html" },
    "/chronicles/chronicle-ameriques-partie1-es.html": { en: "/chronicles/chronicle-ameriques-partie1-en.html", fr: "/chronicles/chronicle-ameriques-partie1-fr.html", es: "/chronicles/chronicle-ameriques-partie1-es.html" },

    "/chronicles/chronicle-raise-children-2026-en.html": { en: "/chronicles/chronicle-raise-children-2026-en.html", fr: "/chronicles/chronicle-elever-enfants-2026-fr.html", es: "/chronicles/chronicle-criar-hijos-2026-es.html" },
    "/chronicles/chronicle-elever-enfants-2026-fr.html": { en: "/chronicles/chronicle-raise-children-2026-en.html", fr: "/chronicles/chronicle-elever-enfants-2026-fr.html", es: "/chronicles/chronicle-criar-hijos-2026-es.html" },
    "/chronicles/chronicle-criar-hijos-2026-es.html":    { en: "/chronicles/chronicle-raise-children-2026-en.html", fr: "/chronicles/chronicle-elever-enfants-2026-fr.html", es: "/chronicles/chronicle-criar-hijos-2026-es.html" },

    "/chronicles/chronicle-ameriques-partie2-en.html": { en: "/chronicles/chronicle-ameriques-partie2-en.html", fr: "/chronicles/chronicle-ameriques-partie2-fr.html", es: "/chronicles/chronicle-ameriques-partie2-es.html" },
    "/chronicles/chronicle-ameriques-partie2-fr.html": { en: "/chronicles/chronicle-ameriques-partie2-en.html", fr: "/chronicles/chronicle-ameriques-partie2-fr.html", es: "/chronicles/chronicle-ameriques-partie2-es.html" },
    "/chronicles/chronicle-ameriques-partie2-es.html": { en: "/chronicles/chronicle-ameriques-partie2-en.html", fr: "/chronicles/chronicle-ameriques-partie2-fr.html", es: "/chronicles/chronicle-ameriques-partie2-es.html" },

    "/chronicles/chronicle-ameriques-partie3-en.html": { en: "/chronicles/chronicle-ameriques-partie3-en.html", fr: "/chronicles/chronicle-ameriques-partie3-fr.html", es: "/chronicles/chronicle-ameriques-partie3-es.html" },
    "/chronicles/chronicle-ameriques-partie3-fr.html": { en: "/chronicles/chronicle-ameriques-partie3-en.html", fr: "/chronicles/chronicle-ameriques-partie3-fr.html", es: "/chronicles/chronicle-ameriques-partie3-es.html" },
    "/chronicles/chronicle-ameriques-partie3-es.html": { en: "/chronicles/chronicle-ameriques-partie3-en.html", fr: "/chronicles/chronicle-ameriques-partie3-fr.html", es: "/chronicles/chronicle-ameriques-partie3-es.html" },

    "/chronicles/chronicle-australia-expat-guide-2026-en.html":    { en: "/chronicles/chronicle-australia-expat-guide-2026-en.html", fr: "/chronicles/chronicle-australie-expatriation-2026-fr.html", es: "/chronicles/chronicle-australia-guia-expatriados-2026-es.html" },
    "/chronicles/chronicle-australie-expatriation-2026-fr.html":   { en: "/chronicles/chronicle-australia-expat-guide-2026-en.html", fr: "/chronicles/chronicle-australie-expatriation-2026-fr.html", es: "/chronicles/chronicle-australia-guia-expatriados-2026-es.html" },
    "/chronicles/chronicle-australia-guia-expatriados-2026-es.html": { en: "/chronicles/chronicle-australia-expat-guide-2026-en.html", fr: "/chronicles/chronicle-australie-expatriation-2026-fr.html", es: "/chronicles/chronicle-australia-guia-expatriados-2026-es.html" },

    "/chronicles/chronicle-retirement-visas-2026-en.html":           { en: "/chronicles/chronicle-retirement-visas-2026-en.html",           fr: "/chronicles/chronicle-visas-retraite-2026-fr.html",              es: "/chronicles/chronicle-visas-jubilacion-2026-es.html" },
    "/chronicles/chronicle-visas-retraite-2026-fr.html":             { en: "/chronicles/chronicle-retirement-visas-2026-en.html",           fr: "/chronicles/chronicle-visas-retraite-2026-fr.html",              es: "/chronicles/chronicle-visas-jubilacion-2026-es.html" },
    "/chronicles/chronicle-visas-jubilacion-2026-es.html":           { en: "/chronicles/chronicle-retirement-visas-2026-en.html",           fr: "/chronicles/chronicle-visas-retraite-2026-fr.html",              es: "/chronicles/chronicle-visas-jubilacion-2026-es.html" },

    "/chronicles/chronicle-digital-nomad-visas-2026-en.html":        { en: "/chronicles/chronicle-digital-nomad-visas-2026-en.html",        fr: "/chronicles/chronicle-visas-digital-nomads-2026-fr.html",        es: "/chronicles/chronicle-visas-nomadas-digitales-2026-es.html" },
    "/chronicles/chronicle-visas-digital-nomads-2026-fr.html":       { en: "/chronicles/chronicle-digital-nomad-visas-2026-en.html",        fr: "/chronicles/chronicle-visas-digital-nomads-2026-fr.html",        es: "/chronicles/chronicle-visas-nomadas-digitales-2026-es.html" },
    "/chronicles/chronicle-visas-nomadas-digitales-2026-es.html":    { en: "/chronicles/chronicle-digital-nomad-visas-2026-en.html",        fr: "/chronicles/chronicle-visas-digital-nomads-2026-fr.html",        es: "/chronicles/chronicle-visas-nomadas-digitales-2026-es.html" },

    "/chronicles/chronicle-expat-work-visas-2026-en.html":           { en: "/chronicles/chronicle-expat-work-visas-2026-en.html",           fr: "/chronicles/chronicle-visas-expatriation-durable-2026-fr.html", es: "/chronicles/chronicle-visas-expatriacion-2026-es.html" },
    "/chronicles/chronicle-visas-expatriation-durable-2026-fr.html": { en: "/chronicles/chronicle-expat-work-visas-2026-en.html",           fr: "/chronicles/chronicle-visas-expatriation-durable-2026-fr.html", es: "/chronicles/chronicle-visas-expatriacion-2026-es.html" },
    "/chronicles/chronicle-visas-expatriacion-2026-es.html":         { en: "/chronicles/chronicle-expat-work-visas-2026-en.html",           fr: "/chronicles/chronicle-visas-expatriation-durable-2026-fr.html", es: "/chronicles/chronicle-visas-expatriacion-2026-es.html" },

    "/chronicles/chronicle-healthcare-expats-2026-en.html":  { en: "/chronicles/chronicle-healthcare-expats-2026-en.html",  fr: "/chronicles/chronicle-sante-expats-2026-fr.html",  es: "/chronicles/chronicle-salud-expats-2026-es.html" },
    "/chronicles/chronicle-sante-expats-2026-fr.html":       { en: "/chronicles/chronicle-healthcare-expats-2026-en.html",  fr: "/chronicles/chronicle-sante-expats-2026-fr.html",  es: "/chronicles/chronicle-salud-expats-2026-es.html" },
    "/chronicles/chronicle-salud-expats-2026-es.html":       { en: "/chronicles/chronicle-healthcare-expats-2026-en.html",  fr: "/chronicles/chronicle-sante-expats-2026-fr.html",  es: "/chronicles/chronicle-salud-expats-2026-es.html" },

    "/chronicles/chronicle-forgotten-expat-countries-2026-en.html":       { en: "/chronicles/chronicle-forgotten-expat-countries-2026-en.html",       fr: "/chronicles/chronicle-pays-oublies-expatriation-2026-fr.html",       es: "/chronicles/chronicle-paises-olvidados-expatriacion-2026-es.html" },
    "/chronicles/chronicle-pays-oublies-expatriation-2026-fr.html":      { en: "/chronicles/chronicle-forgotten-expat-countries-2026-en.html",       fr: "/chronicles/chronicle-pays-oublies-expatriation-2026-fr.html",       es: "/chronicles/chronicle-paises-olvidados-expatriacion-2026-es.html" },
    "/chronicles/chronicle-paises-olvidados-expatriacion-2026-es.html":  { en: "/chronicles/chronicle-forgotten-expat-countries-2026-en.html",       fr: "/chronicles/chronicle-pays-oublies-expatriation-2026-fr.html",       es: "/chronicles/chronicle-paises-olvidados-expatriacion-2026-es.html" },

    "/chronicles/chronicle-asia-expat-guide-part1-2026-en.html":         { en: "/chronicles/chronicle-asia-expat-guide-part1-2026-en.html",         fr: "/chronicles/chronicle-asie-expatriation-partie1-2026-fr.html",       es: "/chronicles/chronicle-asia-guia-expatriados-parte1-2026-es.html" },
    "/chronicles/chronicle-asie-expatriation-partie1-2026-fr.html":      { en: "/chronicles/chronicle-asia-expat-guide-part1-2026-en.html",         fr: "/chronicles/chronicle-asie-expatriation-partie1-2026-fr.html",       es: "/chronicles/chronicle-asia-guia-expatriados-parte1-2026-es.html" },
    "/chronicles/chronicle-asia-guia-expatriados-parte1-2026-es.html":   { en: "/chronicles/chronicle-asia-expat-guide-part1-2026-en.html",         fr: "/chronicles/chronicle-asie-expatriation-partie1-2026-fr.html",       es: "/chronicles/chronicle-asia-guia-expatriados-parte1-2026-es.html" },

    "/chronicles/chronicle-asia-expat-guide-part2-2026-en.html":         { en: "/chronicles/chronicle-asia-expat-guide-part2-2026-en.html",         fr: "/chronicles/chronicle-asie-expatriation-partie2-2026-fr.html",       es: "/chronicles/chronicle-asia-guia-expatriados-parte2-2026-es.html" },
    "/chronicles/chronicle-asie-expatriation-partie2-2026-fr.html":      { en: "/chronicles/chronicle-asia-expat-guide-part2-2026-en.html",         fr: "/chronicles/chronicle-asie-expatriation-partie2-2026-fr.html",       es: "/chronicles/chronicle-asia-guia-expatriados-parte2-2026-es.html" },
    "/chronicles/chronicle-asia-guia-expatriados-parte2-2026-es.html":   { en: "/chronicles/chronicle-asia-expat-guide-part2-2026-en.html",         fr: "/chronicles/chronicle-asie-expatriation-partie2-2026-fr.html",       es: "/chronicles/chronicle-asia-guia-expatriados-parte2-2026-es.html" },

    "/chronicles/villes/chronicle-nice-france-en.html": { en: "/chronicles/villes/chronicle-nice-france-en.html", fr: "/chronicles/villes/chronicle-nice-france-fr.html", es: "/chronicles/villes/chronicle-nice-france-es.html" },
    "/chronicles/villes/chronicle-nice-france-fr.html": { en: "/chronicles/villes/chronicle-nice-france-en.html", fr: "/chronicles/villes/chronicle-nice-france-fr.html", es: "/chronicles/villes/chronicle-nice-france-es.html" },
    "/chronicles/villes/chronicle-nice-france-es.html": { en: "/chronicles/villes/chronicle-nice-france-en.html", fr: "/chronicles/villes/chronicle-nice-france-fr.html", es: "/chronicles/villes/chronicle-nice-france-es.html" },

    "/chronicles/villes/chronicle-lyon-france-en.html": { en: "/chronicles/villes/chronicle-lyon-france-en.html", fr: "/chronicles/villes/chronicle-lyon-france-fr.html", es: "/chronicles/villes/chronicle-lyon-france-es.html" },
    "/chronicles/villes/chronicle-lyon-france-fr.html": { en: "/chronicles/villes/chronicle-lyon-france-en.html", fr: "/chronicles/villes/chronicle-lyon-france-fr.html", es: "/chronicles/villes/chronicle-lyon-france-es.html" },
    "/chronicles/villes/chronicle-lyon-france-es.html": { en: "/chronicles/villes/chronicle-lyon-france-en.html", fr: "/chronicles/villes/chronicle-lyon-france-fr.html", es: "/chronicles/villes/chronicle-lyon-france-es.html" },

    "/chronicles/villes/chronicle-marseille-france-en.html": { en: "/chronicles/villes/chronicle-marseille-france-en.html", fr: "/chronicles/villes/chronicle-marseille-france-fr.html", es: "/chronicles/villes/chronicle-marseille-france-es.html" },
    "/chronicles/villes/chronicle-marseille-france-fr.html": { en: "/chronicles/villes/chronicle-marseille-france-en.html", fr: "/chronicles/villes/chronicle-marseille-france-fr.html", es: "/chronicles/villes/chronicle-marseille-france-es.html" },
    "/chronicles/villes/chronicle-marseille-france-es.html": { en: "/chronicles/villes/chronicle-marseille-france-en.html", fr: "/chronicles/villes/chronicle-marseille-france-fr.html", es: "/chronicles/villes/chronicle-marseille-france-es.html" },

    "/chronicles/villes/chronicle-paris-france-en.html": { en: "/chronicles/villes/chronicle-paris-france-en.html", fr: "/chronicles/villes/chronicle-paris-france-fr.html", es: "/chronicles/villes/chronicle-paris-france-es.html" },
    "/chronicles/villes/chronicle-paris-france-fr.html": { en: "/chronicles/villes/chronicle-paris-france-en.html", fr: "/chronicles/villes/chronicle-paris-france-fr.html", es: "/chronicles/villes/chronicle-paris-france-es.html" },
    "/chronicles/villes/chronicle-paris-france-es.html": { en: "/chronicles/villes/chronicle-paris-france-en.html", fr: "/chronicles/villes/chronicle-paris-france-fr.html", es: "/chronicles/villes/chronicle-paris-france-es.html" },

    "/chronicles/villes/chronicle-bangkok-thailand-en.html": { en: "/chronicles/villes/chronicle-bangkok-thailand-en.html", fr: "/chronicles/villes/chronicle-bangkok-thailand-fr.html", es: "/chronicles/villes/chronicle-bangkok-thailand-es.html" },
    "/chronicles/villes/chronicle-bangkok-thailand-fr.html": { en: "/chronicles/villes/chronicle-bangkok-thailand-en.html", fr: "/chronicles/villes/chronicle-bangkok-thailand-fr.html", es: "/chronicles/villes/chronicle-bangkok-thailand-es.html" },
    "/chronicles/villes/chronicle-bangkok-thailand-es.html": { en: "/chronicles/villes/chronicle-bangkok-thailand-en.html", fr: "/chronicles/villes/chronicle-bangkok-thailand-fr.html", es: "/chronicles/villes/chronicle-bangkok-thailand-es.html" },

    "/chronicles/villes/chronicle-barcelone-espagne-en.html": { en: "/chronicles/villes/chronicle-barcelone-espagne-en.html", fr: "/chronicles/villes/chronicle-barcelone-espagne-fr.html", es: "/chronicles/villes/chronicle-barcelone-espagne-es.html" },
    "/chronicles/villes/chronicle-barcelone-espagne-fr.html": { en: "/chronicles/villes/chronicle-barcelone-espagne-en.html", fr: "/chronicles/villes/chronicle-barcelone-espagne-fr.html", es: "/chronicles/villes/chronicle-barcelone-espagne-es.html" },
    "/chronicles/villes/chronicle-barcelone-espagne-es.html": { en: "/chronicles/villes/chronicle-barcelone-espagne-en.html", fr: "/chronicles/villes/chronicle-barcelone-espagne-fr.html", es: "/chronicles/villes/chronicle-barcelone-espagne-es.html" },

    "/chronicles/villes/chronicle-cairns-australia-en.html": { en: "/chronicles/villes/chronicle-cairns-australia-en.html", fr: "/chronicles/villes/chronicle-cairns-australia-fr.html", es: "/chronicles/villes/chronicle-cairns-australia-es.html" },
    "/chronicles/villes/chronicle-cairns-australia-fr.html": { en: "/chronicles/villes/chronicle-cairns-australia-en.html", fr: "/chronicles/villes/chronicle-cairns-australia-fr.html", es: "/chronicles/villes/chronicle-cairns-australia-es.html" },
    "/chronicles/villes/chronicle-cairns-australia-es.html": { en: "/chronicles/villes/chronicle-cairns-australia-en.html", fr: "/chronicles/villes/chronicle-cairns-australia-fr.html", es: "/chronicles/villes/chronicle-cairns-australia-es.html" },

    "/chronicles/villes/chronicle-calgary-canada-en.html": { en: "/chronicles/villes/chronicle-calgary-canada-en.html", fr: "/chronicles/villes/chronicle-calgary-canada-fr.html", es: "/chronicles/villes/chronicle-calgary-canada-es.html" },
    "/chronicles/villes/chronicle-calgary-canada-fr.html": { en: "/chronicles/villes/chronicle-calgary-canada-en.html", fr: "/chronicles/villes/chronicle-calgary-canada-fr.html", es: "/chronicles/villes/chronicle-calgary-canada-es.html" },
    "/chronicles/villes/chronicle-calgary-canada-es.html": { en: "/chronicles/villes/chronicle-calgary-canada-en.html", fr: "/chronicles/villes/chronicle-calgary-canada-fr.html", es: "/chronicles/villes/chronicle-calgary-canada-es.html" },

    "/chronicles/villes/chronicle-chiang-mai-thailand-en.html": { en: "/chronicles/villes/chronicle-chiang-mai-thailand-en.html", fr: "/chronicles/villes/chronicle-chiang-mai-thailand-fr.html", es: "/chronicles/villes/chronicle-chiang-mai-thailand-es.html" },
    "/chronicles/villes/chronicle-chiang-mai-thailand-fr.html": { en: "/chronicles/villes/chronicle-chiang-mai-thailand-en.html", fr: "/chronicles/villes/chronicle-chiang-mai-thailand-fr.html", es: "/chronicles/villes/chronicle-chiang-mai-thailand-es.html" },
    "/chronicles/villes/chronicle-chiang-mai-thailand-es.html": { en: "/chronicles/villes/chronicle-chiang-mai-thailand-en.html", fr: "/chronicles/villes/chronicle-chiang-mai-thailand-fr.html", es: "/chronicles/villes/chronicle-chiang-mai-thailand-es.html" },

    "/chronicles/villes/chronicle-hua-hin-thailand-en.html": { en: "/chronicles/villes/chronicle-hua-hin-thailand-en.html", fr: "/chronicles/villes/chronicle-hua-hin-thailand-fr.html", es: "/chronicles/villes/chronicle-hua-hin-thailand-es.html" },
    "/chronicles/villes/chronicle-hua-hin-thailand-fr.html": { en: "/chronicles/villes/chronicle-hua-hin-thailand-en.html", fr: "/chronicles/villes/chronicle-hua-hin-thailand-fr.html", es: "/chronicles/villes/chronicle-hua-hin-thailand-es.html" },
    "/chronicles/villes/chronicle-hua-hin-thailand-es.html": { en: "/chronicles/villes/chronicle-hua-hin-thailand-en.html", fr: "/chronicles/villes/chronicle-hua-hin-thailand-fr.html", es: "/chronicles/villes/chronicle-hua-hin-thailand-es.html" },

    "/chronicles/villes/chronicle-madrid-espagne-en.html": { en: "/chronicles/villes/chronicle-madrid-espagne-en.html", fr: "/chronicles/villes/chronicle-madrid-espagne-fr.html", es: "/chronicles/villes/chronicle-madrid-espagne-es.html" },
    "/chronicles/villes/chronicle-madrid-espagne-fr.html": { en: "/chronicles/villes/chronicle-madrid-espagne-en.html", fr: "/chronicles/villes/chronicle-madrid-espagne-fr.html", es: "/chronicles/villes/chronicle-madrid-espagne-es.html" },
    "/chronicles/villes/chronicle-madrid-espagne-es.html": { en: "/chronicles/villes/chronicle-madrid-espagne-en.html", fr: "/chronicles/villes/chronicle-madrid-espagne-fr.html", es: "/chronicles/villes/chronicle-madrid-espagne-es.html" },

    "/chronicles/villes/chronicle-malaga-espagne-en.html": { en: "/chronicles/villes/chronicle-malaga-espagne-en.html", fr: "/chronicles/villes/chronicle-malaga-espagne-fr.html", es: "/chronicles/villes/chronicle-malaga-espagne-es.html" },
    "/chronicles/villes/chronicle-malaga-espagne-fr.html": { en: "/chronicles/villes/chronicle-malaga-espagne-en.html", fr: "/chronicles/villes/chronicle-malaga-espagne-fr.html", es: "/chronicles/villes/chronicle-malaga-espagne-es.html" },
    "/chronicles/villes/chronicle-malaga-espagne-es.html": { en: "/chronicles/villes/chronicle-malaga-espagne-en.html", fr: "/chronicles/villes/chronicle-malaga-espagne-fr.html", es: "/chronicles/villes/chronicle-malaga-espagne-es.html" },

    "/chronicles/villes/chronicle-melbourne-australia-en.html": { en: "/chronicles/villes/chronicle-melbourne-australia-en.html", fr: "/chronicles/villes/chronicle-melbourne-australia-fr.html", es: "/chronicles/villes/chronicle-melbourne-australia-es.html" },
    "/chronicles/villes/chronicle-melbourne-australia-fr.html": { en: "/chronicles/villes/chronicle-melbourne-australia-en.html", fr: "/chronicles/villes/chronicle-melbourne-australia-fr.html", es: "/chronicles/villes/chronicle-melbourne-australia-es.html" },
    "/chronicles/villes/chronicle-melbourne-australia-es.html": { en: "/chronicles/villes/chronicle-melbourne-australia-en.html", fr: "/chronicles/villes/chronicle-melbourne-australia-fr.html", es: "/chronicles/villes/chronicle-melbourne-australia-es.html" },

    "/chronicles/villes/chronicle-montreal-canada-en.html": { en: "/chronicles/villes/chronicle-montreal-canada-en.html", fr: "/chronicles/villes/chronicle-montreal-canada-fr.html", es: "/chronicles/villes/chronicle-montreal-canada-es.html" },
    "/chronicles/villes/chronicle-montreal-canada-fr.html": { en: "/chronicles/villes/chronicle-montreal-canada-en.html", fr: "/chronicles/villes/chronicle-montreal-canada-fr.html", es: "/chronicles/villes/chronicle-montreal-canada-es.html" },
    "/chronicles/villes/chronicle-montreal-canada-es.html": { en: "/chronicles/villes/chronicle-montreal-canada-en.html", fr: "/chronicles/villes/chronicle-montreal-canada-fr.html", es: "/chronicles/villes/chronicle-montreal-canada-es.html" },

    "/chronicles/villes/chronicle-perth-australia-en.html": { en: "/chronicles/villes/chronicle-perth-australia-en.html", fr: "/chronicles/villes/chronicle-perth-australia-fr.html", es: "/chronicles/villes/chronicle-perth-australia-es.html" },
    "/chronicles/villes/chronicle-perth-australia-fr.html": { en: "/chronicles/villes/chronicle-perth-australia-en.html", fr: "/chronicles/villes/chronicle-perth-australia-fr.html", es: "/chronicles/villes/chronicle-perth-australia-es.html" },
    "/chronicles/villes/chronicle-perth-australia-es.html": { en: "/chronicles/villes/chronicle-perth-australia-en.html", fr: "/chronicles/villes/chronicle-perth-australia-fr.html", es: "/chronicles/villes/chronicle-perth-australia-es.html" },

    "/chronicles/villes/chronicle-phuket-thailand-en.html": { en: "/chronicles/villes/chronicle-phuket-thailand-en.html", fr: "/chronicles/villes/chronicle-phuket-thailand-fr.html", es: "/chronicles/villes/chronicle-phuket-thailand-es.html" },
    "/chronicles/villes/chronicle-phuket-thailand-fr.html": { en: "/chronicles/villes/chronicle-phuket-thailand-en.html", fr: "/chronicles/villes/chronicle-phuket-thailand-fr.html", es: "/chronicles/villes/chronicle-phuket-thailand-es.html" },
    "/chronicles/villes/chronicle-phuket-thailand-es.html": { en: "/chronicles/villes/chronicle-phuket-thailand-en.html", fr: "/chronicles/villes/chronicle-phuket-thailand-fr.html", es: "/chronicles/villes/chronicle-phuket-thailand-es.html" },

    "/chronicles/villes/chronicle-sydney-australia-en.html": { en: "/chronicles/villes/chronicle-sydney-australia-en.html", fr: "/chronicles/villes/chronicle-sydney-australia-fr.html", es: "/chronicles/villes/chronicle-sydney-australia-es.html" },
    "/chronicles/villes/chronicle-sydney-australia-fr.html": { en: "/chronicles/villes/chronicle-sydney-australia-en.html", fr: "/chronicles/villes/chronicle-sydney-australia-fr.html", es: "/chronicles/villes/chronicle-sydney-australia-es.html" },
    "/chronicles/villes/chronicle-sydney-australia-es.html": { en: "/chronicles/villes/chronicle-sydney-australia-en.html", fr: "/chronicles/villes/chronicle-sydney-australia-fr.html", es: "/chronicles/villes/chronicle-sydney-australia-es.html" },

    "/chronicles/villes/chronicle-toronto-canada-en.html": { en: "/chronicles/villes/chronicle-toronto-canada-en.html", fr: "/chronicles/villes/chronicle-toronto-canada-fr.html", es: "/chronicles/villes/chronicle-toronto-canada-es.html" },
    "/chronicles/villes/chronicle-toronto-canada-fr.html": { en: "/chronicles/villes/chronicle-toronto-canada-en.html", fr: "/chronicles/villes/chronicle-toronto-canada-fr.html", es: "/chronicles/villes/chronicle-toronto-canada-es.html" },
    "/chronicles/villes/chronicle-toronto-canada-es.html": { en: "/chronicles/villes/chronicle-toronto-canada-en.html", fr: "/chronicles/villes/chronicle-toronto-canada-fr.html", es: "/chronicles/villes/chronicle-toronto-canada-es.html" },

    "/chronicles/villes/chronicle-valence-espagne-en.html": { en: "/chronicles/villes/chronicle-valence-espagne-en.html", fr: "/chronicles/villes/chronicle-valence-espagne-fr.html", es: "/chronicles/villes/chronicle-valence-espagne-es.html" },
    "/chronicles/villes/chronicle-valence-espagne-fr.html": { en: "/chronicles/villes/chronicle-valence-espagne-en.html", fr: "/chronicles/villes/chronicle-valence-espagne-fr.html", es: "/chronicles/villes/chronicle-valence-espagne-es.html" },
    "/chronicles/villes/chronicle-valence-espagne-es.html": { en: "/chronicles/villes/chronicle-valence-espagne-en.html", fr: "/chronicles/villes/chronicle-valence-espagne-fr.html", es: "/chronicles/villes/chronicle-valence-espagne-es.html" },

    "/chronicles/villes/chronicle-vancouver-canada-en.html": { en: "/chronicles/villes/chronicle-vancouver-canada-en.html", fr: "/chronicles/villes/chronicle-vancouver-canada-fr.html", es: "/chronicles/villes/chronicle-vancouver-canada-es.html" },
    "/chronicles/villes/chronicle-vancouver-canada-fr.html": { en: "/chronicles/villes/chronicle-vancouver-canada-en.html", fr: "/chronicles/villes/chronicle-vancouver-canada-fr.html", es: "/chronicles/villes/chronicle-vancouver-canada-es.html" },
    "/chronicles/villes/chronicle-vancouver-canada-es.html": { en: "/chronicles/villes/chronicle-vancouver-canada-en.html", fr: "/chronicles/villes/chronicle-vancouver-canada-fr.html", es: "/chronicles/villes/chronicle-vancouver-canada-es.html" },

    "/chronicles/villes/chronicle-sao-paulo-bresil-en.html": { en: "/chronicles/villes/chronicle-sao-paulo-bresil-en.html", fr: "/chronicles/villes/chronicle-sao-paulo-bresil-fr.html", es: "/chronicles/villes/chronicle-sao-paulo-bresil-es.html" },
    "/chronicles/villes/chronicle-sao-paulo-bresil-fr.html": { en: "/chronicles/villes/chronicle-sao-paulo-bresil-en.html", fr: "/chronicles/villes/chronicle-sao-paulo-bresil-fr.html", es: "/chronicles/villes/chronicle-sao-paulo-bresil-es.html" },
    "/chronicles/villes/chronicle-sao-paulo-bresil-es.html": { en: "/chronicles/villes/chronicle-sao-paulo-bresil-en.html", fr: "/chronicles/villes/chronicle-sao-paulo-bresil-fr.html", es: "/chronicles/villes/chronicle-sao-paulo-bresil-es.html" },
    "/chronicles/villes/chronicle-rio-bresil-en.html": { en: "/chronicles/villes/chronicle-rio-bresil-en.html", fr: "/chronicles/villes/chronicle-rio-bresil-fr.html", es: "/chronicles/villes/chronicle-rio-bresil-es.html" },
    "/chronicles/villes/chronicle-rio-bresil-fr.html": { en: "/chronicles/villes/chronicle-rio-bresil-en.html", fr: "/chronicles/villes/chronicle-rio-bresil-fr.html", es: "/chronicles/villes/chronicle-rio-bresil-es.html" },
    "/chronicles/villes/chronicle-rio-bresil-es.html": { en: "/chronicles/villes/chronicle-rio-bresil-en.html", fr: "/chronicles/villes/chronicle-rio-bresil-fr.html", es: "/chronicles/villes/chronicle-rio-bresil-es.html" },
    "/chronicles/villes/chronicle-florianopolis-bresil-en.html": { en: "/chronicles/villes/chronicle-florianopolis-bresil-en.html", fr: "/chronicles/villes/chronicle-florianopolis-bresil-fr.html", es: "/chronicles/villes/chronicle-florianopolis-bresil-es.html" },
    "/chronicles/villes/chronicle-florianopolis-bresil-fr.html": { en: "/chronicles/villes/chronicle-florianopolis-bresil-en.html", fr: "/chronicles/villes/chronicle-florianopolis-bresil-fr.html", es: "/chronicles/villes/chronicle-florianopolis-bresil-es.html" },
    "/chronicles/villes/chronicle-florianopolis-bresil-es.html": { en: "/chronicles/villes/chronicle-florianopolis-bresil-en.html", fr: "/chronicles/villes/chronicle-florianopolis-bresil-fr.html", es: "/chronicles/villes/chronicle-florianopolis-bresil-es.html" },
    "/chronicles/villes/chronicle-salvador-bresil-en.html": { en: "/chronicles/villes/chronicle-salvador-bresil-en.html", fr: "/chronicles/villes/chronicle-salvador-bresil-fr.html", es: "/chronicles/villes/chronicle-salvador-bresil-es.html" },
    "/chronicles/villes/chronicle-salvador-bresil-fr.html": { en: "/chronicles/villes/chronicle-salvador-bresil-en.html", fr: "/chronicles/villes/chronicle-salvador-bresil-fr.html", es: "/chronicles/villes/chronicle-salvador-bresil-es.html" },
    "/chronicles/villes/chronicle-salvador-bresil-es.html": { en: "/chronicles/villes/chronicle-salvador-bresil-en.html", fr: "/chronicles/villes/chronicle-salvador-bresil-fr.html", es: "/chronicles/villes/chronicle-salvador-bresil-es.html" },
    "/chronicles/villes/chronicle-tokyo-japan-en.html": { en: "/chronicles/villes/chronicle-tokyo-japan-en.html", fr: "/chronicles/villes/chronicle-tokyo-japan-fr.html", es: "/chronicles/villes/chronicle-tokyo-japan-es.html" },
    "/chronicles/villes/chronicle-tokyo-japan-fr.html": { en: "/chronicles/villes/chronicle-tokyo-japan-en.html", fr: "/chronicles/villes/chronicle-tokyo-japan-fr.html", es: "/chronicles/villes/chronicle-tokyo-japan-es.html" },
    "/chronicles/villes/chronicle-tokyo-japan-es.html": { en: "/chronicles/villes/chronicle-tokyo-japan-en.html", fr: "/chronicles/villes/chronicle-tokyo-japan-fr.html", es: "/chronicles/villes/chronicle-tokyo-japan-es.html" },
    "/chronicles/villes/chronicle-osaka-japan-en.html": { en: "/chronicles/villes/chronicle-osaka-japan-en.html", fr: "/chronicles/villes/chronicle-osaka-japan-fr.html", es: "/chronicles/villes/chronicle-osaka-japan-es.html" },
    "/chronicles/villes/chronicle-osaka-japan-fr.html": { en: "/chronicles/villes/chronicle-osaka-japan-en.html", fr: "/chronicles/villes/chronicle-osaka-japan-fr.html", es: "/chronicles/villes/chronicle-osaka-japan-es.html" },
    "/chronicles/villes/chronicle-osaka-japan-es.html": { en: "/chronicles/villes/chronicle-osaka-japan-en.html", fr: "/chronicles/villes/chronicle-osaka-japan-fr.html", es: "/chronicles/villes/chronicle-osaka-japan-es.html" },
    "/chronicles/villes/chronicle-fukuoka-japan-en.html": { en: "/chronicles/villes/chronicle-fukuoka-japan-en.html", fr: "/chronicles/villes/chronicle-fukuoka-japan-fr.html", es: "/chronicles/villes/chronicle-fukuoka-japan-es.html" },
    "/chronicles/villes/chronicle-fukuoka-japan-fr.html": { en: "/chronicles/villes/chronicle-fukuoka-japan-en.html", fr: "/chronicles/villes/chronicle-fukuoka-japan-fr.html", es: "/chronicles/villes/chronicle-fukuoka-japan-es.html" },
    "/chronicles/villes/chronicle-fukuoka-japan-es.html": { en: "/chronicles/villes/chronicle-fukuoka-japan-en.html", fr: "/chronicles/villes/chronicle-fukuoka-japan-fr.html", es: "/chronicles/villes/chronicle-fukuoka-japan-es.html" },

    "/chronicles/villes/chronicle-kyoto-japan-en.html": { en: "/chronicles/villes/chronicle-kyoto-japan-en.html", fr: "/chronicles/villes/chronicle-kyoto-japan-fr.html", es: "/chronicles/villes/chronicle-kyoto-japan-es.html" },
    "/chronicles/villes/chronicle-kyoto-japan-fr.html": { en: "/chronicles/villes/chronicle-kyoto-japan-en.html", fr: "/chronicles/villes/chronicle-kyoto-japan-fr.html", es: "/chronicles/villes/chronicle-kyoto-japan-es.html" },
    "/chronicles/villes/chronicle-kyoto-japan-es.html": { en: "/chronicles/villes/chronicle-kyoto-japan-en.html", fr: "/chronicles/villes/chronicle-kyoto-japan-fr.html", es: "/chronicles/villes/chronicle-kyoto-japan-es.html" },

    "/chronicles/villes/chronicle-mexico-city-mexico-en.html": { en: "/chronicles/villes/chronicle-mexico-city-mexico-en.html", fr: "/chronicles/villes/chronicle-mexico-city-mexico-fr.html", es: "/chronicles/villes/chronicle-mexico-city-mexico-es.html" },
    "/chronicles/villes/chronicle-mexico-city-mexico-fr.html": { en: "/chronicles/villes/chronicle-mexico-city-mexico-en.html", fr: "/chronicles/villes/chronicle-mexico-city-mexico-fr.html", es: "/chronicles/villes/chronicle-mexico-city-mexico-es.html" },
    "/chronicles/villes/chronicle-mexico-city-mexico-es.html": { en: "/chronicles/villes/chronicle-mexico-city-mexico-en.html", fr: "/chronicles/villes/chronicle-mexico-city-mexico-fr.html", es: "/chronicles/villes/chronicle-mexico-city-mexico-es.html" },
    "/chronicles/villes/chronicle-guadalajara-mexico-en.html": { en: "/chronicles/villes/chronicle-guadalajara-mexico-en.html", fr: "/chronicles/villes/chronicle-guadalajara-mexico-fr.html", es: "/chronicles/villes/chronicle-guadalajara-mexico-es.html" },
    "/chronicles/villes/chronicle-guadalajara-mexico-fr.html": { en: "/chronicles/villes/chronicle-guadalajara-mexico-en.html", fr: "/chronicles/villes/chronicle-guadalajara-mexico-fr.html", es: "/chronicles/villes/chronicle-guadalajara-mexico-es.html" },
    "/chronicles/villes/chronicle-guadalajara-mexico-es.html": { en: "/chronicles/villes/chronicle-guadalajara-mexico-en.html", fr: "/chronicles/villes/chronicle-guadalajara-mexico-fr.html", es: "/chronicles/villes/chronicle-guadalajara-mexico-es.html" },
    "/chronicles/villes/chronicle-monterrey-mexico-en.html": { en: "/chronicles/villes/chronicle-monterrey-mexico-en.html", fr: "/chronicles/villes/chronicle-monterrey-mexico-fr.html", es: "/chronicles/villes/chronicle-monterrey-mexico-es.html" },
    "/chronicles/villes/chronicle-monterrey-mexico-fr.html": { en: "/chronicles/villes/chronicle-monterrey-mexico-en.html", fr: "/chronicles/villes/chronicle-monterrey-mexico-fr.html", es: "/chronicles/villes/chronicle-monterrey-mexico-es.html" },
    "/chronicles/villes/chronicle-monterrey-mexico-es.html": { en: "/chronicles/villes/chronicle-monterrey-mexico-en.html", fr: "/chronicles/villes/chronicle-monterrey-mexico-fr.html", es: "/chronicles/villes/chronicle-monterrey-mexico-es.html" },
    "/chronicles/villes/chronicle-cancun-mexico-en.html": { en: "/chronicles/villes/chronicle-cancun-mexico-en.html", fr: "/chronicles/villes/chronicle-cancun-mexico-fr.html", es: "/chronicles/villes/chronicle-cancun-mexico-es.html" },
    "/chronicles/villes/chronicle-cancun-mexico-fr.html": { en: "/chronicles/villes/chronicle-cancun-mexico-en.html", fr: "/chronicles/villes/chronicle-cancun-mexico-fr.html", es: "/chronicles/villes/chronicle-cancun-mexico-es.html" },
    "/chronicles/villes/chronicle-cancun-mexico-es.html": { en: "/chronicles/villes/chronicle-cancun-mexico-en.html", fr: "/chronicles/villes/chronicle-cancun-mexico-fr.html", es: "/chronicles/villes/chronicle-cancun-mexico-es.html" },
    "/chronicles/villes/chronicle-new-york-usa-en.html": { en: "/chronicles/villes/chronicle-new-york-usa-en.html", fr: "/chronicles/villes/chronicle-new-york-usa-fr.html", es: "/chronicles/villes/chronicle-new-york-usa-es.html" },
    "/chronicles/villes/chronicle-new-york-usa-fr.html": { en: "/chronicles/villes/chronicle-new-york-usa-en.html", fr: "/chronicles/villes/chronicle-new-york-usa-fr.html", es: "/chronicles/villes/chronicle-new-york-usa-es.html" },
    "/chronicles/villes/chronicle-new-york-usa-es.html": { en: "/chronicles/villes/chronicle-new-york-usa-en.html", fr: "/chronicles/villes/chronicle-new-york-usa-fr.html", es: "/chronicles/villes/chronicle-new-york-usa-es.html" },
    "/chronicles/villes/chronicle-los-angeles-usa-en.html": { en: "/chronicles/villes/chronicle-los-angeles-usa-en.html", fr: "/chronicles/villes/chronicle-los-angeles-usa-fr.html", es: "/chronicles/villes/chronicle-los-angeles-usa-es.html" },
    "/chronicles/villes/chronicle-los-angeles-usa-fr.html": { en: "/chronicles/villes/chronicle-los-angeles-usa-en.html", fr: "/chronicles/villes/chronicle-los-angeles-usa-fr.html", es: "/chronicles/villes/chronicle-los-angeles-usa-es.html" },
    "/chronicles/villes/chronicle-los-angeles-usa-es.html": { en: "/chronicles/villes/chronicle-los-angeles-usa-en.html", fr: "/chronicles/villes/chronicle-los-angeles-usa-fr.html", es: "/chronicles/villes/chronicle-los-angeles-usa-es.html" },
    "/chronicles/villes/chronicle-miami-usa-en.html": { en: "/chronicles/villes/chronicle-miami-usa-en.html", fr: "/chronicles/villes/chronicle-miami-usa-fr.html", es: "/chronicles/villes/chronicle-miami-usa-es.html" },
    "/chronicles/villes/chronicle-miami-usa-fr.html": { en: "/chronicles/villes/chronicle-miami-usa-en.html", fr: "/chronicles/villes/chronicle-miami-usa-fr.html", es: "/chronicles/villes/chronicle-miami-usa-es.html" },
    "/chronicles/villes/chronicle-miami-usa-es.html": { en: "/chronicles/villes/chronicle-miami-usa-en.html", fr: "/chronicles/villes/chronicle-miami-usa-fr.html", es: "/chronicles/villes/chronicle-miami-usa-es.html" },
    "/chronicles/villes/chronicle-austin-usa-en.html": { en: "/chronicles/villes/chronicle-austin-usa-en.html", fr: "/chronicles/villes/chronicle-austin-usa-fr.html", es: "/chronicles/villes/chronicle-austin-usa-es.html" },
    "/chronicles/villes/chronicle-austin-usa-fr.html": { en: "/chronicles/villes/chronicle-austin-usa-en.html", fr: "/chronicles/villes/chronicle-austin-usa-fr.html", es: "/chronicles/villes/chronicle-austin-usa-es.html" },
    "/chronicles/villes/chronicle-austin-usa-es.html": { en: "/chronicles/villes/chronicle-austin-usa-en.html", fr: "/chronicles/villes/chronicle-austin-usa-fr.html", es: "/chronicles/villes/chronicle-austin-usa-es.html" },

    "/chronicles/villes/chronicle-athenes-grece-en.html": { en: "/chronicles/villes/chronicle-athenes-grece-en.html", fr: "/chronicles/villes/chronicle-athenes-grece-fr.html", es: "/chronicles/villes/chronicle-athenes-grece-es.html" },
    "/chronicles/villes/chronicle-athenes-grece-fr.html": { en: "/chronicles/villes/chronicle-athenes-grece-en.html", fr: "/chronicles/villes/chronicle-athenes-grece-fr.html", es: "/chronicles/villes/chronicle-athenes-grece-es.html" },
    "/chronicles/villes/chronicle-athenes-grece-es.html": { en: "/chronicles/villes/chronicle-athenes-grece-en.html", fr: "/chronicles/villes/chronicle-athenes-grece-fr.html", es: "/chronicles/villes/chronicle-athenes-grece-es.html" },
    "/chronicles/villes/chronicle-thessalonique-grece-en.html": { en: "/chronicles/villes/chronicle-thessalonique-grece-en.html", fr: "/chronicles/villes/chronicle-thessalonique-grece-fr.html", es: "/chronicles/villes/chronicle-thessalonique-grece-es.html" },
    "/chronicles/villes/chronicle-thessalonique-grece-fr.html": { en: "/chronicles/villes/chronicle-thessalonique-grece-en.html", fr: "/chronicles/villes/chronicle-thessalonique-grece-fr.html", es: "/chronicles/villes/chronicle-thessalonique-grece-es.html" },
    "/chronicles/villes/chronicle-thessalonique-grece-es.html": { en: "/chronicles/villes/chronicle-thessalonique-grece-en.html", fr: "/chronicles/villes/chronicle-thessalonique-grece-fr.html", es: "/chronicles/villes/chronicle-thessalonique-grece-es.html" },
    "/chronicles/villes/chronicle-heraklion-grece-en.html": { en: "/chronicles/villes/chronicle-heraklion-grece-en.html", fr: "/chronicles/villes/chronicle-heraklion-grece-fr.html", es: "/chronicles/villes/chronicle-heraklion-grece-es.html" },
    "/chronicles/villes/chronicle-heraklion-grece-fr.html": { en: "/chronicles/villes/chronicle-heraklion-grece-en.html", fr: "/chronicles/villes/chronicle-heraklion-grece-fr.html", es: "/chronicles/villes/chronicle-heraklion-grece-es.html" },
    "/chronicles/villes/chronicle-heraklion-grece-es.html": { en: "/chronicles/villes/chronicle-heraklion-grece-en.html", fr: "/chronicles/villes/chronicle-heraklion-grece-fr.html", es: "/chronicles/villes/chronicle-heraklion-grece-es.html" },
    "/chronicles/villes/chronicle-la-canee-grece-en.html": { en: "/chronicles/villes/chronicle-la-canee-grece-en.html", fr: "/chronicles/villes/chronicle-la-canee-grece-fr.html", es: "/chronicles/villes/chronicle-la-canee-grece-es.html" },
    "/chronicles/villes/chronicle-la-canee-grece-fr.html": { en: "/chronicles/villes/chronicle-la-canee-grece-en.html", fr: "/chronicles/villes/chronicle-la-canee-grece-fr.html", es: "/chronicles/villes/chronicle-la-canee-grece-es.html" },
    "/chronicles/villes/chronicle-la-canee-grece-es.html": { en: "/chronicles/villes/chronicle-la-canee-grece-en.html", fr: "/chronicles/villes/chronicle-la-canee-grece-fr.html", es: "/chronicles/villes/chronicle-la-canee-grece-es.html" },

    "/chronicles/villes/chronicle-bali-indonesia-en.html": { en: "/chronicles/villes/chronicle-bali-indonesia-en.html", fr: "/chronicles/villes/chronicle-bali-indonesia-fr.html", es: "/chronicles/villes/chronicle-bali-indonesia-es.html" },
    "/chronicles/villes/chronicle-bali-indonesia-fr.html": { en: "/chronicles/villes/chronicle-bali-indonesia-en.html", fr: "/chronicles/villes/chronicle-bali-indonesia-fr.html", es: "/chronicles/villes/chronicle-bali-indonesia-es.html" },
    "/chronicles/villes/chronicle-bali-indonesia-es.html": { en: "/chronicles/villes/chronicle-bali-indonesia-en.html", fr: "/chronicles/villes/chronicle-bali-indonesia-fr.html", es: "/chronicles/villes/chronicle-bali-indonesia-es.html" },
    "/chronicles/villes/chronicle-jakarta-indonesia-en.html": { en: "/chronicles/villes/chronicle-jakarta-indonesia-en.html", fr: "/chronicles/villes/chronicle-jakarta-indonesia-fr.html", es: "/chronicles/villes/chronicle-jakarta-indonesia-es.html" },
    "/chronicles/villes/chronicle-jakarta-indonesia-fr.html": { en: "/chronicles/villes/chronicle-jakarta-indonesia-en.html", fr: "/chronicles/villes/chronicle-jakarta-indonesia-fr.html", es: "/chronicles/villes/chronicle-jakarta-indonesia-es.html" },
    "/chronicles/villes/chronicle-jakarta-indonesia-es.html": { en: "/chronicles/villes/chronicle-jakarta-indonesia-en.html", fr: "/chronicles/villes/chronicle-jakarta-indonesia-fr.html", es: "/chronicles/villes/chronicle-jakarta-indonesia-es.html" },
    "/chronicles/villes/chronicle-surabaya-indonesia-en.html": { en: "/chronicles/villes/chronicle-surabaya-indonesia-en.html", fr: "/chronicles/villes/chronicle-surabaya-indonesia-fr.html", es: "/chronicles/villes/chronicle-surabaya-indonesia-es.html" },
    "/chronicles/villes/chronicle-surabaya-indonesia-fr.html": { en: "/chronicles/villes/chronicle-surabaya-indonesia-en.html", fr: "/chronicles/villes/chronicle-surabaya-indonesia-fr.html", es: "/chronicles/villes/chronicle-surabaya-indonesia-es.html" },
    "/chronicles/villes/chronicle-surabaya-indonesia-es.html": { en: "/chronicles/villes/chronicle-surabaya-indonesia-en.html", fr: "/chronicles/villes/chronicle-surabaya-indonesia-fr.html", es: "/chronicles/villes/chronicle-surabaya-indonesia-es.html" },
    "/chronicles/villes/chronicle-yogyakarta-indonesia-en.html": { en: "/chronicles/villes/chronicle-yogyakarta-indonesia-en.html", fr: "/chronicles/villes/chronicle-yogyakarta-indonesia-fr.html", es: "/chronicles/villes/chronicle-yogyakarta-indonesia-es.html" },
    "/chronicles/villes/chronicle-yogyakarta-indonesia-fr.html": { en: "/chronicles/villes/chronicle-yogyakarta-indonesia-en.html", fr: "/chronicles/villes/chronicle-yogyakarta-indonesia-fr.html", es: "/chronicles/villes/chronicle-yogyakarta-indonesia-es.html" },
    "/chronicles/villes/chronicle-yogyakarta-indonesia-es.html": { en: "/chronicles/villes/chronicle-yogyakarta-indonesia-en.html", fr: "/chronicles/villes/chronicle-yogyakarta-indonesia-fr.html", es: "/chronicles/villes/chronicle-yogyakarta-indonesia-es.html" },

    "/chronicles/villes/chronicle-abu-dhabi-emirats-en.html": { en: "/chronicles/villes/chronicle-abu-dhabi-emirats-en.html", fr: "/chronicles/villes/chronicle-abu-dhabi-emirats-fr.html", es: "/chronicles/villes/chronicle-abu-dhabi-emirats-es.html" },
    "/chronicles/villes/chronicle-abu-dhabi-emirats-fr.html": { en: "/chronicles/villes/chronicle-abu-dhabi-emirats-en.html", fr: "/chronicles/villes/chronicle-abu-dhabi-emirats-fr.html", es: "/chronicles/villes/chronicle-abu-dhabi-emirats-es.html" },
    "/chronicles/villes/chronicle-abu-dhabi-emirats-es.html": { en: "/chronicles/villes/chronicle-abu-dhabi-emirats-en.html", fr: "/chronicles/villes/chronicle-abu-dhabi-emirats-fr.html", es: "/chronicles/villes/chronicle-abu-dhabi-emirats-es.html" },
    "/chronicles/villes/chronicle-dubai-emirats-en.html": { en: "/chronicles/villes/chronicle-dubai-emirats-en.html", fr: "/chronicles/villes/chronicle-dubai-emirats-fr.html", es: "/chronicles/villes/chronicle-dubai-emirats-es.html" },
    "/chronicles/villes/chronicle-dubai-emirats-fr.html": { en: "/chronicles/villes/chronicle-dubai-emirats-en.html", fr: "/chronicles/villes/chronicle-dubai-emirats-fr.html", es: "/chronicles/villes/chronicle-dubai-emirats-es.html" },
    "/chronicles/villes/chronicle-dubai-emirats-es.html": { en: "/chronicles/villes/chronicle-dubai-emirats-en.html", fr: "/chronicles/villes/chronicle-dubai-emirats-fr.html", es: "/chronicles/villes/chronicle-dubai-emirats-es.html" },
    "/chronicles/villes/chronicle-sharjah-emirats-en.html": { en: "/chronicles/villes/chronicle-sharjah-emirats-en.html", fr: "/chronicles/villes/chronicle-sharjah-emirats-fr.html", es: "/chronicles/villes/chronicle-sharjah-emirats-es.html" },
    "/chronicles/villes/chronicle-sharjah-emirats-fr.html": { en: "/chronicles/villes/chronicle-sharjah-emirats-en.html", fr: "/chronicles/villes/chronicle-sharjah-emirats-fr.html", es: "/chronicles/villes/chronicle-sharjah-emirats-es.html" },
    "/chronicles/villes/chronicle-sharjah-emirats-es.html": { en: "/chronicles/villes/chronicle-sharjah-emirats-en.html", fr: "/chronicles/villes/chronicle-sharjah-emirats-fr.html", es: "/chronicles/villes/chronicle-sharjah-emirats-es.html" },
    "/chronicles/villes/chronicle-ras-al-khaimah-emirats-en.html": { en: "/chronicles/villes/chronicle-ras-al-khaimah-emirats-en.html", fr: "/chronicles/villes/chronicle-ras-al-khaimah-emirats-fr.html", es: "/chronicles/villes/chronicle-ras-al-khaimah-emirats-es.html" },
    "/chronicles/villes/chronicle-ras-al-khaimah-emirats-fr.html": { en: "/chronicles/villes/chronicle-ras-al-khaimah-emirats-en.html", fr: "/chronicles/villes/chronicle-ras-al-khaimah-emirats-fr.html", es: "/chronicles/villes/chronicle-ras-al-khaimah-emirats-es.html" },
    "/chronicles/villes/chronicle-ras-al-khaimah-emirats-es.html": { en: "/chronicles/villes/chronicle-ras-al-khaimah-emirats-en.html", fr: "/chronicles/villes/chronicle-ras-al-khaimah-emirats-fr.html", es: "/chronicles/villes/chronicle-ras-al-khaimah-emirats-es.html" },
    "/chronicles/villes/chronicle-istanbul-turquie-en.html": { en: "/chronicles/villes/chronicle-istanbul-turquie-en.html", fr: "/chronicles/villes/chronicle-istanbul-turquie-fr.html", es: "/chronicles/villes/chronicle-istanbul-turquie-es.html" },
    "/chronicles/villes/chronicle-istanbul-turquie-fr.html": { en: "/chronicles/villes/chronicle-istanbul-turquie-en.html", fr: "/chronicles/villes/chronicle-istanbul-turquie-fr.html", es: "/chronicles/villes/chronicle-istanbul-turquie-es.html" },
    "/chronicles/villes/chronicle-istanbul-turquie-es.html": { en: "/chronicles/villes/chronicle-istanbul-turquie-en.html", fr: "/chronicles/villes/chronicle-istanbul-turquie-fr.html", es: "/chronicles/villes/chronicle-istanbul-turquie-es.html" },
    "/chronicles/villes/chronicle-ankara-turquie-en.html": { en: "/chronicles/villes/chronicle-ankara-turquie-en.html", fr: "/chronicles/villes/chronicle-ankara-turquie-fr.html", es: "/chronicles/villes/chronicle-ankara-turquie-es.html" },
    "/chronicles/villes/chronicle-ankara-turquie-fr.html": { en: "/chronicles/villes/chronicle-ankara-turquie-en.html", fr: "/chronicles/villes/chronicle-ankara-turquie-fr.html", es: "/chronicles/villes/chronicle-ankara-turquie-es.html" },
    "/chronicles/villes/chronicle-ankara-turquie-es.html": { en: "/chronicles/villes/chronicle-ankara-turquie-en.html", fr: "/chronicles/villes/chronicle-ankara-turquie-fr.html", es: "/chronicles/villes/chronicle-ankara-turquie-es.html" },
    "/chronicles/villes/chronicle-izmir-turquie-en.html": { en: "/chronicles/villes/chronicle-izmir-turquie-en.html", fr: "/chronicles/villes/chronicle-izmir-turquie-fr.html", es: "/chronicles/villes/chronicle-izmir-turquie-es.html" },
    "/chronicles/villes/chronicle-izmir-turquie-fr.html": { en: "/chronicles/villes/chronicle-izmir-turquie-en.html", fr: "/chronicles/villes/chronicle-izmir-turquie-fr.html", es: "/chronicles/villes/chronicle-izmir-turquie-es.html" },
    "/chronicles/villes/chronicle-izmir-turquie-es.html": { en: "/chronicles/villes/chronicle-izmir-turquie-en.html", fr: "/chronicles/villes/chronicle-izmir-turquie-fr.html", es: "/chronicles/villes/chronicle-izmir-turquie-es.html" },
    "/chronicles/villes/chronicle-antalya-turquie-en.html": { en: "/chronicles/villes/chronicle-antalya-turquie-en.html", fr: "/chronicles/villes/chronicle-antalya-turquie-fr.html", es: "/chronicles/villes/chronicle-antalya-turquie-es.html" },
    "/chronicles/villes/chronicle-antalya-turquie-fr.html": { en: "/chronicles/villes/chronicle-antalya-turquie-en.html", fr: "/chronicles/villes/chronicle-antalya-turquie-fr.html", es: "/chronicles/villes/chronicle-antalya-turquie-es.html" },
    "/chronicles/villes/chronicle-antalya-turquie-es.html": { en: "/chronicles/villes/chronicle-antalya-turquie-en.html", fr: "/chronicles/villes/chronicle-antalya-turquie-fr.html", es: "/chronicles/villes/chronicle-antalya-turquie-es.html" },
    "/chronicles/villes/chronicle-buenos-aires-argentine-en.html": { en: "/chronicles/villes/chronicle-buenos-aires-argentine-en.html", fr: "/chronicles/villes/chronicle-buenos-aires-argentine-fr.html", es: "/chronicles/villes/chronicle-buenos-aires-argentine-es.html" },
    "/chronicles/villes/chronicle-buenos-aires-argentine-fr.html": { en: "/chronicles/villes/chronicle-buenos-aires-argentine-en.html", fr: "/chronicles/villes/chronicle-buenos-aires-argentine-fr.html", es: "/chronicles/villes/chronicle-buenos-aires-argentine-es.html" },
    "/chronicles/villes/chronicle-buenos-aires-argentine-es.html": { en: "/chronicles/villes/chronicle-buenos-aires-argentine-en.html", fr: "/chronicles/villes/chronicle-buenos-aires-argentine-fr.html", es: "/chronicles/villes/chronicle-buenos-aires-argentine-es.html" },
    "/chronicles/villes/chronicle-cordoba-argentine-en.html": { en: "/chronicles/villes/chronicle-cordoba-argentine-en.html", fr: "/chronicles/villes/chronicle-cordoba-argentine-fr.html", es: "/chronicles/villes/chronicle-cordoba-argentine-es.html" },
    "/chronicles/villes/chronicle-cordoba-argentine-fr.html": { en: "/chronicles/villes/chronicle-cordoba-argentine-en.html", fr: "/chronicles/villes/chronicle-cordoba-argentine-fr.html", es: "/chronicles/villes/chronicle-cordoba-argentine-es.html" },
    "/chronicles/villes/chronicle-cordoba-argentine-es.html": { en: "/chronicles/villes/chronicle-cordoba-argentine-en.html", fr: "/chronicles/villes/chronicle-cordoba-argentine-fr.html", es: "/chronicles/villes/chronicle-cordoba-argentine-es.html" },
    "/chronicles/villes/chronicle-mendoza-argentine-en.html": { en: "/chronicles/villes/chronicle-mendoza-argentine-en.html", fr: "/chronicles/villes/chronicle-mendoza-argentine-fr.html", es: "/chronicles/villes/chronicle-mendoza-argentine-es.html" },
    "/chronicles/villes/chronicle-mendoza-argentine-fr.html": { en: "/chronicles/villes/chronicle-mendoza-argentine-en.html", fr: "/chronicles/villes/chronicle-mendoza-argentine-fr.html", es: "/chronicles/villes/chronicle-mendoza-argentine-es.html" },
    "/chronicles/villes/chronicle-mendoza-argentine-es.html": { en: "/chronicles/villes/chronicle-mendoza-argentine-en.html", fr: "/chronicles/villes/chronicle-mendoza-argentine-fr.html", es: "/chronicles/villes/chronicle-mendoza-argentine-es.html" },
    "/chronicles/villes/chronicle-bariloche-argentine-en.html": { en: "/chronicles/villes/chronicle-bariloche-argentine-en.html", fr: "/chronicles/villes/chronicle-bariloche-argentine-fr.html", es: "/chronicles/villes/chronicle-bariloche-argentine-es.html" },
    "/chronicles/villes/chronicle-bariloche-argentine-fr.html": { en: "/chronicles/villes/chronicle-bariloche-argentine-en.html", fr: "/chronicles/villes/chronicle-bariloche-argentine-fr.html", es: "/chronicles/villes/chronicle-bariloche-argentine-es.html" },
    "/chronicles/villes/chronicle-bariloche-argentine-es.html": { en: "/chronicles/villes/chronicle-bariloche-argentine-en.html", fr: "/chronicles/villes/chronicle-bariloche-argentine-fr.html", es: "/chronicles/villes/chronicle-bariloche-argentine-es.html" },
    "/chronicles/villes/chronicle-berlin-allemagne-en.html": { en: "/chronicles/villes/chronicle-berlin-allemagne-en.html", fr: "/chronicles/villes/chronicle-berlin-allemagne-fr.html", es: "/chronicles/villes/chronicle-berlin-allemagne-es.html" },
    "/chronicles/villes/chronicle-berlin-allemagne-fr.html": { en: "/chronicles/villes/chronicle-berlin-allemagne-en.html", fr: "/chronicles/villes/chronicle-berlin-allemagne-fr.html", es: "/chronicles/villes/chronicle-berlin-allemagne-es.html" },
    "/chronicles/villes/chronicle-berlin-allemagne-es.html": { en: "/chronicles/villes/chronicle-berlin-allemagne-en.html", fr: "/chronicles/villes/chronicle-berlin-allemagne-fr.html", es: "/chronicles/villes/chronicle-berlin-allemagne-es.html" },
    "/chronicles/villes/chronicle-munich-allemagne-en.html": { en: "/chronicles/villes/chronicle-munich-allemagne-en.html", fr: "/chronicles/villes/chronicle-munich-allemagne-fr.html", es: "/chronicles/villes/chronicle-munich-allemagne-es.html" },
    "/chronicles/villes/chronicle-munich-allemagne-fr.html": { en: "/chronicles/villes/chronicle-munich-allemagne-en.html", fr: "/chronicles/villes/chronicle-munich-allemagne-fr.html", es: "/chronicles/villes/chronicle-munich-allemagne-es.html" },
    "/chronicles/villes/chronicle-munich-allemagne-es.html": { en: "/chronicles/villes/chronicle-munich-allemagne-en.html", fr: "/chronicles/villes/chronicle-munich-allemagne-fr.html", es: "/chronicles/villes/chronicle-munich-allemagne-es.html" },
    "/chronicles/villes/chronicle-hambourg-allemagne-en.html": { en: "/chronicles/villes/chronicle-hambourg-allemagne-en.html", fr: "/chronicles/villes/chronicle-hambourg-allemagne-fr.html", es: "/chronicles/villes/chronicle-hambourg-allemagne-es.html" },
    "/chronicles/villes/chronicle-hambourg-allemagne-fr.html": { en: "/chronicles/villes/chronicle-hambourg-allemagne-en.html", fr: "/chronicles/villes/chronicle-hambourg-allemagne-fr.html", es: "/chronicles/villes/chronicle-hambourg-allemagne-es.html" },
    "/chronicles/villes/chronicle-hambourg-allemagne-es.html": { en: "/chronicles/villes/chronicle-hambourg-allemagne-en.html", fr: "/chronicles/villes/chronicle-hambourg-allemagne-fr.html", es: "/chronicles/villes/chronicle-hambourg-allemagne-es.html" },
    "/chronicles/villes/chronicle-cologne-allemagne-en.html": { en: "/chronicles/villes/chronicle-cologne-allemagne-en.html", fr: "/chronicles/villes/chronicle-cologne-allemagne-fr.html", es: "/chronicles/villes/chronicle-cologne-allemagne-es.html" },
    "/chronicles/villes/chronicle-cologne-allemagne-fr.html": { en: "/chronicles/villes/chronicle-cologne-allemagne-en.html", fr: "/chronicles/villes/chronicle-cologne-allemagne-fr.html", es: "/chronicles/villes/chronicle-cologne-allemagne-es.html" },
    "/chronicles/villes/chronicle-cologne-allemagne-es.html": { en: "/chronicles/villes/chronicle-cologne-allemagne-en.html", fr: "/chronicles/villes/chronicle-cologne-allemagne-fr.html", es: "/chronicles/villes/chronicle-cologne-allemagne-es.html" },
    "/chronicles/villes/chronicle-bogota-colombie-en.html": { en: "/chronicles/villes/chronicle-bogota-colombie-en.html", fr: "/chronicles/villes/chronicle-bogota-colombie-fr.html", es: "/chronicles/villes/chronicle-bogota-colombie-es.html" },
    "/chronicles/villes/chronicle-bogota-colombie-fr.html": { en: "/chronicles/villes/chronicle-bogota-colombie-en.html", fr: "/chronicles/villes/chronicle-bogota-colombie-fr.html", es: "/chronicles/villes/chronicle-bogota-colombie-es.html" },
    "/chronicles/villes/chronicle-bogota-colombie-es.html": { en: "/chronicles/villes/chronicle-bogota-colombie-en.html", fr: "/chronicles/villes/chronicle-bogota-colombie-fr.html", es: "/chronicles/villes/chronicle-bogota-colombie-es.html" },
    "/chronicles/villes/chronicle-medellin-colombie-en.html": { en: "/chronicles/villes/chronicle-medellin-colombie-en.html", fr: "/chronicles/villes/chronicle-medellin-colombie-fr.html", es: "/chronicles/villes/chronicle-medellin-colombie-es.html" },
    "/chronicles/villes/chronicle-medellin-colombie-fr.html": { en: "/chronicles/villes/chronicle-medellin-colombie-en.html", fr: "/chronicles/villes/chronicle-medellin-colombie-fr.html", es: "/chronicles/villes/chronicle-medellin-colombie-es.html" },
    "/chronicles/villes/chronicle-medellin-colombie-es.html": { en: "/chronicles/villes/chronicle-medellin-colombie-en.html", fr: "/chronicles/villes/chronicle-medellin-colombie-fr.html", es: "/chronicles/villes/chronicle-medellin-colombie-es.html" },
    "/chronicles/villes/chronicle-cali-colombie-en.html": { en: "/chronicles/villes/chronicle-cali-colombie-en.html", fr: "/chronicles/villes/chronicle-cali-colombie-fr.html", es: "/chronicles/villes/chronicle-cali-colombie-es.html" },
    "/chronicles/villes/chronicle-cali-colombie-fr.html": { en: "/chronicles/villes/chronicle-cali-colombie-en.html", fr: "/chronicles/villes/chronicle-cali-colombie-fr.html", es: "/chronicles/villes/chronicle-cali-colombie-es.html" },
    "/chronicles/villes/chronicle-cali-colombie-es.html": { en: "/chronicles/villes/chronicle-cali-colombie-en.html", fr: "/chronicles/villes/chronicle-cali-colombie-fr.html", es: "/chronicles/villes/chronicle-cali-colombie-es.html" },
    "/chronicles/villes/chronicle-cartagena-colombie-en.html": { en: "/chronicles/villes/chronicle-cartagena-colombie-en.html", fr: "/chronicles/villes/chronicle-cartagena-colombie-fr.html", es: "/chronicles/villes/chronicle-cartagena-colombie-es.html" },
    "/chronicles/villes/chronicle-cartagena-colombie-fr.html": { en: "/chronicles/villes/chronicle-cartagena-colombie-en.html", fr: "/chronicles/villes/chronicle-cartagena-colombie-fr.html", es: "/chronicles/villes/chronicle-cartagena-colombie-es.html" },
    "/chronicles/villes/chronicle-cartagena-colombie-es.html": { en: "/chronicles/villes/chronicle-cartagena-colombie-en.html", fr: "/chronicles/villes/chronicle-cartagena-colombie-fr.html", es: "/chronicles/villes/chronicle-cartagena-colombie-es.html" },
    "/chronicles/villes/chronicle-hanoi-vietnam-en.html": { en: "/chronicles/villes/chronicle-hanoi-vietnam-en.html", fr: "/chronicles/villes/chronicle-hanoi-vietnam-fr.html", es: "/chronicles/villes/chronicle-hanoi-vietnam-es.html" },
    "/chronicles/villes/chronicle-hanoi-vietnam-fr.html": { en: "/chronicles/villes/chronicle-hanoi-vietnam-en.html", fr: "/chronicles/villes/chronicle-hanoi-vietnam-fr.html", es: "/chronicles/villes/chronicle-hanoi-vietnam-es.html" },
    "/chronicles/villes/chronicle-hanoi-vietnam-es.html": { en: "/chronicles/villes/chronicle-hanoi-vietnam-en.html", fr: "/chronicles/villes/chronicle-hanoi-vietnam-fr.html", es: "/chronicles/villes/chronicle-hanoi-vietnam-es.html" },
    "/chronicles/villes/chronicle-ho-chi-minh-vietnam-en.html": { en: "/chronicles/villes/chronicle-ho-chi-minh-vietnam-en.html", fr: "/chronicles/villes/chronicle-ho-chi-minh-vietnam-fr.html", es: "/chronicles/villes/chronicle-ho-chi-minh-vietnam-es.html" },
    "/chronicles/villes/chronicle-ho-chi-minh-vietnam-fr.html": { en: "/chronicles/villes/chronicle-ho-chi-minh-vietnam-en.html", fr: "/chronicles/villes/chronicle-ho-chi-minh-vietnam-fr.html", es: "/chronicles/villes/chronicle-ho-chi-minh-vietnam-es.html" },
    "/chronicles/villes/chronicle-ho-chi-minh-vietnam-es.html": { en: "/chronicles/villes/chronicle-ho-chi-minh-vietnam-en.html", fr: "/chronicles/villes/chronicle-ho-chi-minh-vietnam-fr.html", es: "/chronicles/villes/chronicle-ho-chi-minh-vietnam-es.html" },
    "/chronicles/villes/chronicle-da-nang-vietnam-en.html": { en: "/chronicles/villes/chronicle-da-nang-vietnam-en.html", fr: "/chronicles/villes/chronicle-da-nang-vietnam-fr.html", es: "/chronicles/villes/chronicle-da-nang-vietnam-es.html" },
    "/chronicles/villes/chronicle-da-nang-vietnam-fr.html": { en: "/chronicles/villes/chronicle-da-nang-vietnam-en.html", fr: "/chronicles/villes/chronicle-da-nang-vietnam-fr.html", es: "/chronicles/villes/chronicle-da-nang-vietnam-es.html" },
    "/chronicles/villes/chronicle-da-nang-vietnam-es.html": { en: "/chronicles/villes/chronicle-da-nang-vietnam-en.html", fr: "/chronicles/villes/chronicle-da-nang-vietnam-fr.html", es: "/chronicles/villes/chronicle-da-nang-vietnam-es.html" },
    "/chronicles/villes/chronicle-hoi-an-vietnam-en.html": { en: "/chronicles/villes/chronicle-hoi-an-vietnam-en.html", fr: "/chronicles/villes/chronicle-hoi-an-vietnam-fr.html", es: "/chronicles/villes/chronicle-hoi-an-vietnam-es.html" },
    "/chronicles/villes/chronicle-hoi-an-vietnam-fr.html": { en: "/chronicles/villes/chronicle-hoi-an-vietnam-en.html", fr: "/chronicles/villes/chronicle-hoi-an-vietnam-fr.html", es: "/chronicles/villes/chronicle-hoi-an-vietnam-es.html" },
    "/chronicles/villes/chronicle-hoi-an-vietnam-es.html": { en: "/chronicles/villes/chronicle-hoi-an-vietnam-en.html", fr: "/chronicles/villes/chronicle-hoi-an-vietnam-fr.html", es: "/chronicles/villes/chronicle-hoi-an-vietnam-es.html" },
    "/chronicles/villes/chronicle-kuala-lumpur-malaisie-en.html": { en: "/chronicles/villes/chronicle-kuala-lumpur-malaisie-en.html", fr: "/chronicles/villes/chronicle-kuala-lumpur-malaisie-fr.html", es: "/chronicles/villes/chronicle-kuala-lumpur-malaisie-es.html" },
    "/chronicles/villes/chronicle-kuala-lumpur-malaisie-fr.html": { en: "/chronicles/villes/chronicle-kuala-lumpur-malaisie-en.html", fr: "/chronicles/villes/chronicle-kuala-lumpur-malaisie-fr.html", es: "/chronicles/villes/chronicle-kuala-lumpur-malaisie-es.html" },
    "/chronicles/villes/chronicle-kuala-lumpur-malaisie-es.html": { en: "/chronicles/villes/chronicle-kuala-lumpur-malaisie-en.html", fr: "/chronicles/villes/chronicle-kuala-lumpur-malaisie-fr.html", es: "/chronicles/villes/chronicle-kuala-lumpur-malaisie-es.html" },
    "/chronicles/villes/chronicle-george-town-malaisie-en.html": { en: "/chronicles/villes/chronicle-george-town-malaisie-en.html", fr: "/chronicles/villes/chronicle-george-town-malaisie-fr.html", es: "/chronicles/villes/chronicle-george-town-malaisie-es.html" },
    "/chronicles/villes/chronicle-george-town-malaisie-fr.html": { en: "/chronicles/villes/chronicle-george-town-malaisie-en.html", fr: "/chronicles/villes/chronicle-george-town-malaisie-fr.html", es: "/chronicles/villes/chronicle-george-town-malaisie-es.html" },
    "/chronicles/villes/chronicle-george-town-malaisie-es.html": { en: "/chronicles/villes/chronicle-george-town-malaisie-en.html", fr: "/chronicles/villes/chronicle-george-town-malaisie-fr.html", es: "/chronicles/villes/chronicle-george-town-malaisie-es.html" },
    "/chronicles/villes/chronicle-johor-bahru-malaisie-en.html": { en: "/chronicles/villes/chronicle-johor-bahru-malaisie-en.html", fr: "/chronicles/villes/chronicle-johor-bahru-malaisie-fr.html", es: "/chronicles/villes/chronicle-johor-bahru-malaisie-es.html" },
    "/chronicles/villes/chronicle-johor-bahru-malaisie-fr.html": { en: "/chronicles/villes/chronicle-johor-bahru-malaisie-en.html", fr: "/chronicles/villes/chronicle-johor-bahru-malaisie-fr.html", es: "/chronicles/villes/chronicle-johor-bahru-malaisie-es.html" },
    "/chronicles/villes/chronicle-johor-bahru-malaisie-es.html": { en: "/chronicles/villes/chronicle-johor-bahru-malaisie-en.html", fr: "/chronicles/villes/chronicle-johor-bahru-malaisie-fr.html", es: "/chronicles/villes/chronicle-johor-bahru-malaisie-es.html" },
    "/chronicles/villes/chronicle-kota-kinabalu-malaisie-en.html": { en: "/chronicles/villes/chronicle-kota-kinabalu-malaisie-en.html", fr: "/chronicles/villes/chronicle-kota-kinabalu-malaisie-fr.html", es: "/chronicles/villes/chronicle-kota-kinabalu-malaisie-es.html" },
    "/chronicles/villes/chronicle-kota-kinabalu-malaisie-fr.html": { en: "/chronicles/villes/chronicle-kota-kinabalu-malaisie-en.html", fr: "/chronicles/villes/chronicle-kota-kinabalu-malaisie-fr.html", es: "/chronicles/villes/chronicle-kota-kinabalu-malaisie-es.html" },
    "/chronicles/villes/chronicle-kota-kinabalu-malaisie-es.html": { en: "/chronicles/villes/chronicle-kota-kinabalu-malaisie-en.html", fr: "/chronicles/villes/chronicle-kota-kinabalu-malaisie-fr.html", es: "/chronicles/villes/chronicle-kota-kinabalu-malaisie-es.html" },

    "/chronicles/chronicle-africa-expat-p1-en.html":        { en: "/chronicles/chronicle-africa-expat-p1-en.html",        fr: "/chronicles/chronicle-afrique-expatrier-p1-fr.html",    es: "/chronicles/chronicle-africa-expatriarse-p1-es.html" },
    "/chronicles/chronicle-afrique-expatrier-p1-fr.html":   { en: "/chronicles/chronicle-africa-expat-p1-en.html",        fr: "/chronicles/chronicle-afrique-expatrier-p1-fr.html",    es: "/chronicles/chronicle-africa-expatriarse-p1-es.html" },
    "/chronicles/chronicle-africa-expatriarse-p1-es.html":  { en: "/chronicles/chronicle-africa-expat-p1-en.html",        fr: "/chronicles/chronicle-afrique-expatrier-p1-fr.html",    es: "/chronicles/chronicle-africa-expatriarse-p1-es.html" },

    "/chronicles/chronicle-africa-expat-p2-en.html":        { en: "/chronicles/chronicle-africa-expat-p2-en.html",        fr: "/chronicles/chronicle-afrique-expatrier-p2-fr.html",    es: "/chronicles/chronicle-africa-expatriarse-p2-es.html" },
    "/chronicles/chronicle-afrique-expatrier-p2-fr.html":   { en: "/chronicles/chronicle-africa-expat-p2-en.html",        fr: "/chronicles/chronicle-afrique-expatrier-p2-fr.html",    es: "/chronicles/chronicle-africa-expatriarse-p2-es.html" },
    "/chronicles/chronicle-africa-expatriarse-p2-es.html":  { en: "/chronicles/chronicle-africa-expat-p2-en.html",        fr: "/chronicles/chronicle-afrique-expatrier-p2-fr.html",    es: "/chronicles/chronicle-africa-expatriarse-p2-es.html" },

    "/chronicles/chronicle-africa-expat-p3-en.html":        { en: "/chronicles/chronicle-africa-expat-p3-en.html",        fr: "/chronicles/chronicle-afrique-expatrier-p3-fr.html",    es: "/chronicles/chronicle-africa-expatriarse-p3-es.html" },
    "/chronicles/chronicle-afrique-expatrier-p3-fr.html":   { en: "/chronicles/chronicle-africa-expat-p3-en.html",        fr: "/chronicles/chronicle-afrique-expatrier-p3-fr.html",    es: "/chronicles/chronicle-africa-expatriarse-p3-es.html" },
    "/chronicles/chronicle-africa-expatriarse-p3-es.html":  { en: "/chronicles/chronicle-africa-expat-p3-en.html",        fr: "/chronicles/chronicle-afrique-expatrier-p3-fr.html",    es: "/chronicles/chronicle-africa-expatriarse-p3-es.html" },

    "/chronicles/chronicle-africa-expat-p4-en.html":        { en: "/chronicles/chronicle-africa-expat-p4-en.html",        fr: "/chronicles/chronicle-afrique-expatrier-p4-fr.html",    es: "/chronicles/chronicle-africa-expatriarse-p4-es.html" },
    "/chronicles/chronicle-afrique-expatrier-p4-fr.html":   { en: "/chronicles/chronicle-africa-expat-p4-en.html",        fr: "/chronicles/chronicle-afrique-expatrier-p4-fr.html",    es: "/chronicles/chronicle-africa-expatriarse-p4-es.html" },
    "/chronicles/chronicle-africa-expatriarse-p4-es.html":  { en: "/chronicles/chronicle-africa-expat-p4-en.html",        fr: "/chronicles/chronicle-afrique-expatrier-p4-fr.html",    es: "/chronicles/chronicle-africa-expatriarse-p4-es.html" },

    "/chronicles/villes/chronicle-lisbonne-portugal-en.html": { en: "/chronicles/villes/chronicle-lisbonne-portugal-en.html", fr: "/chronicles/villes/chronicle-lisbonne-portugal-fr.html", es: "/chronicles/villes/chronicle-lisbonne-portugal-es.html" },
    "/chronicles/villes/chronicle-lisbonne-portugal-fr.html": { en: "/chronicles/villes/chronicle-lisbonne-portugal-en.html", fr: "/chronicles/villes/chronicle-lisbonne-portugal-fr.html", es: "/chronicles/villes/chronicle-lisbonne-portugal-es.html" },
    "/chronicles/villes/chronicle-lisbonne-portugal-es.html": { en: "/chronicles/villes/chronicle-lisbonne-portugal-en.html", fr: "/chronicles/villes/chronicle-lisbonne-portugal-fr.html", es: "/chronicles/villes/chronicle-lisbonne-portugal-es.html" },
    "/chronicles/villes/chronicle-porto-portugal-en.html": { en: "/chronicles/villes/chronicle-porto-portugal-en.html", fr: "/chronicles/villes/chronicle-porto-portugal-fr.html", es: "/chronicles/villes/chronicle-porto-portugal-es.html" },
    "/chronicles/villes/chronicle-porto-portugal-fr.html": { en: "/chronicles/villes/chronicle-porto-portugal-en.html", fr: "/chronicles/villes/chronicle-porto-portugal-fr.html", es: "/chronicles/villes/chronicle-porto-portugal-es.html" },
    "/chronicles/villes/chronicle-porto-portugal-es.html": { en: "/chronicles/villes/chronicle-porto-portugal-en.html", fr: "/chronicles/villes/chronicle-porto-portugal-fr.html", es: "/chronicles/villes/chronicle-porto-portugal-es.html" },
    "/chronicles/villes/chronicle-faro-portugal-en.html": { en: "/chronicles/villes/chronicle-faro-portugal-en.html", fr: "/chronicles/villes/chronicle-faro-portugal-fr.html", es: "/chronicles/villes/chronicle-faro-portugal-es.html" },
    "/chronicles/villes/chronicle-faro-portugal-fr.html": { en: "/chronicles/villes/chronicle-faro-portugal-en.html", fr: "/chronicles/villes/chronicle-faro-portugal-fr.html", es: "/chronicles/villes/chronicle-faro-portugal-es.html" },
    "/chronicles/villes/chronicle-faro-portugal-es.html": { en: "/chronicles/villes/chronicle-faro-portugal-en.html", fr: "/chronicles/villes/chronicle-faro-portugal-fr.html", es: "/chronicles/villes/chronicle-faro-portugal-es.html" },
    "/chronicles/villes/chronicle-funchal-portugal-en.html": { en: "/chronicles/villes/chronicle-funchal-portugal-en.html", fr: "/chronicles/villes/chronicle-funchal-portugal-fr.html", es: "/chronicles/villes/chronicle-funchal-portugal-es.html" },
    "/chronicles/villes/chronicle-funchal-portugal-fr.html": { en: "/chronicles/villes/chronicle-funchal-portugal-en.html", fr: "/chronicles/villes/chronicle-funchal-portugal-fr.html", es: "/chronicles/villes/chronicle-funchal-portugal-es.html" },
    "/chronicles/villes/chronicle-funchal-portugal-es.html": { en: "/chronicles/villes/chronicle-funchal-portugal-en.html", fr: "/chronicles/villes/chronicle-funchal-portugal-fr.html", es: "/chronicles/villes/chronicle-funchal-portugal-es.html" },

    "/chronicles/chronicle-study-abroad-europe-erasmus-2026-en.html":  { en: "/chronicles/chronicle-study-abroad-europe-erasmus-2026-en.html",  fr: "/chronicles/chronicle-etudier-europe-erasmus-2026-fr.html",           es: "/chronicles/chronicle-estudiar-europa-erasmus-2026-es.html" },
    "/chronicles/chronicle-etudier-europe-erasmus-2026-fr.html":       { en: "/chronicles/chronicle-study-abroad-europe-erasmus-2026-en.html",  fr: "/chronicles/chronicle-etudier-europe-erasmus-2026-fr.html",           es: "/chronicles/chronicle-estudiar-europa-erasmus-2026-es.html" },
    "/chronicles/chronicle-estudiar-europa-erasmus-2026-es.html":      { en: "/chronicles/chronicle-study-abroad-europe-erasmus-2026-en.html",  fr: "/chronicles/chronicle-etudier-europe-erasmus-2026-fr.html",           es: "/chronicles/chronicle-estudiar-europa-erasmus-2026-es.html" },

    "/chronicles/chronicle-study-abroad-americas-africa-2026-en.html": { en: "/chronicles/chronicle-study-abroad-americas-africa-2026-en.html", fr: "/chronicles/chronicle-etudier-ameriques-afrique-2026-fr.html",        es: "/chronicles/chronicle-estudiar-americas-africa-2026-es.html" },
    "/chronicles/chronicle-etudier-ameriques-afrique-2026-fr.html":    { en: "/chronicles/chronicle-study-abroad-americas-africa-2026-en.html", fr: "/chronicles/chronicle-etudier-ameriques-afrique-2026-fr.html",        es: "/chronicles/chronicle-estudiar-americas-africa-2026-es.html" },
    "/chronicles/chronicle-estudiar-americas-africa-2026-es.html":     { en: "/chronicles/chronicle-study-abroad-americas-africa-2026-en.html", fr: "/chronicles/chronicle-etudier-ameriques-afrique-2026-fr.html",        es: "/chronicles/chronicle-estudiar-americas-africa-2026-es.html" },

    "/chronicles/chronicle-study-abroad-asia-pacific-2026-en.html":    { en: "/chronicles/chronicle-study-abroad-asia-pacific-2026-en.html",    fr: "/chronicles/chronicle-etudier-asie-pacifique-2026-fr.html",          es: "/chronicles/chronicle-estudiar-asia-pacifico-2026-es.html" },
    "/chronicles/chronicle-etudier-asie-pacifique-2026-fr.html":       { en: "/chronicles/chronicle-study-abroad-asia-pacific-2026-en.html",    fr: "/chronicles/chronicle-etudier-asie-pacifique-2026-fr.html",          es: "/chronicles/chronicle-estudiar-asia-pacifico-2026-es.html" },
    "/chronicles/chronicle-estudiar-asia-pacifico-2026-es.html":       { en: "/chronicles/chronicle-study-abroad-asia-pacific-2026-en.html",    fr: "/chronicles/chronicle-etudier-asie-pacifique-2026-fr.html",          es: "/chronicles/chronicle-estudiar-asia-pacifico-2026-es.html" },

    "/chronicles/chronicle-study-abroad-practical-guide-2026-en.html":    { en: "/chronicles/chronicle-study-abroad-practical-guide-2026-en.html",    fr: "/chronicles/chronicle-etudier-etranger-guide-pratique-2026-fr.html", es: "/chronicles/chronicle-estudiar-extranjero-guia-practica-2026-es.html" },
    "/chronicles/chronicle-etudier-etranger-guide-pratique-2026-fr.html": { en: "/chronicles/chronicle-study-abroad-practical-guide-2026-en.html",    fr: "/chronicles/chronicle-etudier-etranger-guide-pratique-2026-fr.html", es: "/chronicles/chronicle-estudiar-extranjero-guia-practica-2026-es.html" },
    "/chronicles/chronicle-estudiar-extranjero-guia-practica-2026-es.html": { en: "/chronicles/chronicle-study-abroad-practical-guide-2026-en.html",  fr: "/chronicles/chronicle-etudier-etranger-guide-pratique-2026-fr.html", es: "/chronicles/chronicle-estudiar-extranjero-guia-practica-2026-es.html" },

    "/chronicles/chronicle-ready-to-leave-en.html":       { en: "/chronicles/chronicle-ready-to-leave-en.html",       fr: "/chronicles/chronicle-pret-partir-fr.html",           es: "/chronicles/chronicle-listo-para-partir-es.html" },
    "/chronicles/chronicle-pret-partir-fr.html":           { en: "/chronicles/chronicle-ready-to-leave-en.html",       fr: "/chronicles/chronicle-pret-partir-fr.html",           es: "/chronicles/chronicle-listo-para-partir-es.html" },
    "/chronicles/chronicle-listo-para-partir-es.html":     { en: "/chronicles/chronicle-ready-to-leave-en.html",       fr: "/chronicles/chronicle-pret-partir-fr.html",           es: "/chronicles/chronicle-listo-para-partir-es.html" },

    "/chronicles/chronicle-property-abroad-2026-en.html":        { en: "/chronicles/chronicle-property-abroad-2026-en.html",        fr: "/chronicles/chronicle-immo-etranger-2026-fr.html",            es: "/chronicles/chronicle-propiedad-extranjero-2026-es.html" },
    "/chronicles/chronicle-immo-etranger-2026-fr.html":          { en: "/chronicles/chronicle-property-abroad-2026-en.html",        fr: "/chronicles/chronicle-immo-etranger-2026-fr.html",            es: "/chronicles/chronicle-propiedad-extranjero-2026-es.html" },
    "/chronicles/chronicle-propiedad-extranjero-2026-es.html":   { en: "/chronicles/chronicle-property-abroad-2026-en.html",        fr: "/chronicles/chronicle-immo-etranger-2026-fr.html",            es: "/chronicles/chronicle-propiedad-extranjero-2026-es.html" },
  };

  // Lang selection
  // Dynamic fallback for static country pages: /countries/{slug}-{lang}.html
  function dynamicCountryLangSwap(pathname, newLang){
    const m = pathname.match(/^\/countries\/([a-z0-9-]+)-(en|fr|es)\.html$/);
    if (!m) return null;
    return `/countries/${m[1]}-${newLang}.html`;
  }

  document.querySelectorAll("[data-lang]").forEach(item => {
    item.addEventListener("click", () => {
      const newLang = item.dataset.lang;
      localStorage.setItem("wigg_lang", newLang);
      const path = document.location.pathname;
      const mapping = CHRONICLE_LANGS[path];
      if (mapping && mapping[newLang]) {
        window.location.href = mapping[newLang];
        return;
      }
      const dyn = dynamicCountryLangSwap(path, newLang);
      if (dyn) {
        window.location.href = dyn;
        return;
      }
      location.reload();
    });
  });

  // Random
  async function goRandomCountry(){
    try{
      const res = await fetch("/data/countries.json?nocache=" + Date.now(), { cache:"no-store" });
      if(!res.ok) throw new Error("HTTP " + res.status);
      const data = await res.json();
      const keys = Object.keys(data || {});
      if(!keys.length) throw new Error("No keys");
      const slug = keys[Math.floor(Math.random() * keys.length)];
      const lang = (localStorage.getItem("wigg_lang") || "en").toLowerCase();
      const useLang = ["en","fr","es"].includes(lang) ? lang : "en";
      window.location.href = "/countries/" + encodeURIComponent(slug) + "-" + useLang + ".html";
    }catch(e){
      console.error("Random error:", e);
      alert("Random failed.");
    }
  }
  function bindRandom(id){
    const btn = document.getElementById(id);
    if(btn) btn.addEventListener("click", e => { e.preventDefault(); goRandomCountry(); });
  }
  bindRandom("btnRandom");
  bindRandom("btnRandomMobile");

  // ── Auth state in header (centralized — works on every page) ──
  (function(){
    var SB_URL='https://tkctreoftezvbfejhbto.supabase.co';
    var SB_KEY='sb_publishable_lAKWBnp2nbfgb2w5Uj55aQ_aD6fBWUb';
    var lang=(localStorage.getItem('wigg_lang')||'en').toLowerCase();
    var T={
      en:{login:'Sign in',account:'My account'},
      fr:{login:'Connexion',account:'Mon compte'},
      es:{login:'Iniciar sesión',account:'Mi cuenta'}
    };
    var t=T[lang]||T.en;

    function renderLoading(authEl){
      authEl.innerHTML='<div style="width:30px;height:30px;border-radius:50%;background:rgba(26,84,48,.08);animation:wmhPulse 1.2s ease-in-out infinite"></div>';
      if(!document.getElementById('wmhPulseStyle')){
        var st=document.createElement('style');
        st.id='wmhPulseStyle';
        st.textContent='@keyframes wmhPulse{0%,100%{opacity:.4}50%{opacity:.8}}';
        document.head.appendChild(st);
      }
    }

    function renderLoggedOut(authEl){
      authEl.innerHTML='<a href="/onboarding.html" style="padding:6px 14px;border:1.5px solid #1a5430;border-radius:2px;color:#1a5430;font-family:Inter,sans-serif;font-size:12px;font-weight:600;text-decoration:none;white-space:nowrap">'+t.login+'</a>';
    }

    function renderLoggedIn(authEl,name,avatar){
      var displayName=name||t.account;
      var initial=displayName[0]?displayName[0].toUpperCase():'?';
      var avatarHtml=avatar
        ? '<img src="'+avatar+'" style="width:30px;height:30px;border-radius:50%;object-fit:cover;border:1.5px solid #c8bfaa" onerror="this.outerHTML=\'<div style=&quot;width:30px;height:30px;border-radius:50%;background:#1a5430;color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700&quot;>'+initial+'</div>\'" />'
        : '<div style="width:30px;height:30px;border-radius:50%;background:#1a5430;color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;">'+initial+'</div>';
      authEl.innerHTML='<a href="/mon-compte.html" style="display:flex;align-items:center;gap:7px;text-decoration:none;color:#1a5430;font-family:Inter,sans-serif;font-size:13px;font-weight:500;" title="'+displayName+'">'+avatarHtml+'<span class="wmh-auth-name" style="max-width:80px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+displayName+'</span></a>';
    }

    // Ensure profile exists in DB (called for every authenticated user, on every page)
    function ensureProfile(sbClient,user,onProfileLoaded){
      var meta=user.user_metadata||{};
      sbClient.from('profiles').select('username,avatar_url').eq('id',user.id).maybeSingle().then(function(res){
        if(res.data){
          // Profile exists — return it
          if(onProfileLoaded) onProfileLoaded(res.data);
          return;
        }
        // Profile doesn't exist — create it (handles signup flow)
        var fullName=meta.full_name||meta.name||(user.email?user.email.split('@')[0]:'');
        sbClient.from('profiles').insert({
          id:user.id,
          username:fullName,
          avatar_url:meta.avatar_url||meta.picture||null,
          onboarding_done:false
        }).select('username,avatar_url').single().then(function(insertRes){
          if(insertRes.error&&insertRes.error.code!=='23505'){
            console.warn('[wmh] profile insert error',insertRes.error);
          }
          if(onProfileLoaded) onProfileLoaded(insertRes.data||{username:fullName,avatar_url:meta.avatar_url||meta.picture||''});
        });
      });
    }

    function refresh(sbClient){
      var authEl=document.getElementById('wigg-auth-btn');
      if(!authEl) return;
      sbClient.auth.getSession().then(function(res){
        var session=res.data.session;
        if(!session||!session.user){
          renderLoggedOut(authEl);
          return;
        }
        var u=session.user;
        var meta=u.user_metadata||{};
        // Show optimistic UI immediately from auth metadata
        var fallbackName=(meta.full_name||meta.name||(u.email?u.email.split('@')[0]:'')).split(' ')[0];
        var fallbackAvatar=meta.avatar_url||meta.picture||'';
        renderLoggedIn(authEl,fallbackName,fallbackAvatar);
        // Then upgrade with profile data from DB (username may differ)
        ensureProfile(sbClient,u,function(profile){
          var name=(profile.username||fallbackName||'').split(' ')[0];
          var avatar=profile.avatar_url||fallbackAvatar;
          renderLoggedIn(authEl,name,avatar);
        });
      });
    }

    function initHeaderAuth(sbClient){
      var authEl=document.getElementById('wigg-auth-btn');
      if(authEl) renderLoading(authEl);
      // Expose globally so other scripts can refresh the header (e.g. after onboarding)
      window.wmhAuthClient=sbClient;
      window.wmhRefreshAuth=function(){refresh(sbClient);};
      refresh(sbClient);
      sbClient.auth.onAuthStateChange(function(event,session){
        refresh(sbClient);
      });
    }

    function makeClient(){
      return window.supabase.createClient(SB_URL,SB_KEY,{auth:{detectSessionInUrl:true,persistSession:true,autoRefreshToken:true}});
    }
    if(window.supabase){
      initHeaderAuth(makeClient());
    }else{
      var s=document.createElement('script');
      s.src='https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js';
      s.onload=function(){initHeaderAuth(makeClient());};
      document.head.appendChild(s);
    }
  })();

})();
