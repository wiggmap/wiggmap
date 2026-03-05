// data/header.js
(function () {
  const isCountryPage = document.location.pathname.includes("/countries/");
  const prefix = isCountryPage ? "../" : "";
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
    { href: X_URL,        label: "X (Twitter)",  svg: `<svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M18.9 2H22l-6.6 7.6L23.5 22h-6.7l-5.2-6.8L5.6 22H2.5l7.1-8.2L.5 2h6.8l4.7 6.1L18.9 2Zm-1.2 18h1.8L6.2 3.9H4.3L17.7 20Z"/></svg>` },
    { href: IG_URL,       label: "Instagram",    svg: `<svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M7.8 2h8.4A5.8 5.8 0 0 1 22 7.8v8.4A5.8 5.8 0 0 1 16.2 22H7.8A5.8 5.8 0 0 1 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2Zm0 2A3.8 3.8 0 0 0 4 7.8v8.4A3.8 3.8 0 0 0 7.8 20h8.4a3.8 3.8 0 0 0 3.8-3.8V7.8A3.8 3.8 0 0 0 16.2 4H7.8Z"/><path fill="currentColor" d="M12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z"/><circle fill="currentColor" cx="17.5" cy="6.5" r="1.1"/></svg>` },
    { href: TELEGRAM_URL, label: "Telegram",     svg: `<svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M21.9 4.6c.2-.8-.5-1.5-1.3-1.2L2.7 10.4c-.9.4-.9 1.7.1 2l4.6 1.5 1.8 5.6c.3 1 1.6 1.1 2.1.3l2.6-3.7 4.9 3.6c.7.5 1.7.1 1.9-.8l1.2-14.3ZM8.3 13.2l9.9-6.1-7.6 7.4-.3 3.9-1.7-5.1-2.5-.8Z"/></svg>` },
  ];

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
      .wmh-ico--tg{ background:rgba(0,136,204,.12); border-color:rgba(0,136,204,.22); }
      .wmh-ico--tg:hover{ background:rgba(0,136,204,.20); }

      /* Nav buttons */
      .wmh-nav{ display:flex; align-items:center; gap:8px; flex-wrap:nowrap !important; }
      .wmh-btn{
        font-weight:900; font-size:13px; color:#5b6b62;
        padding:7px 11px; border-radius:999px;
        border:1px solid rgba(0,0,0,.10);
        background:rgba(255,255,255,.80);
        display:inline-flex; align-items:center; gap:6px;
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

      /* Mobile */
      @media (max-width: 640px){
        .wmh-inner{ padding:8px 12px; gap:8px; flex-wrap:wrap; }
        .wmh-brand img{ height:44px; }
        .wmh-social{ display:none !important; }
        .wmh-right .wmh-nav{ display:none !important; }
        .wmh-right{ flex:1 1 auto; justify-content:flex-end; gap:7px; }
        .wmh-nav-mobile{
          display:grid !important;
          grid-template-columns:repeat(3,1fr);
          gap:5px; width:100%; flex-basis:100%;
        }
        .wmh-btn{ justify-content:center; padding:8px 6px; font-size:12px; }
        .wmh-drop-trigger{ font-size:14px; padding:6px 9px; }
      }
      .wmh-btn--game{
        border-color:rgba(29,216,118,0.4) !important;
        background:rgba(29,216,118,0.10) !important;
        padding:5px 10px !important;
      }
      .wmh-btn--game:hover{
        background:rgba(29,216,118,0.22) !important;
        border-color:rgba(29,216,118,0.7) !important;
      }
      .wmh-nav-mobile{ display:none; }
    `;
    document.head.appendChild(st);
  }

  const currentLang = localStorage.getItem("wigg_lang") || "en";
  const currentLangData = LANGS[currentLang] || LANGS.en;

  const socialItems = SOCIALS.map(s =>
    `<a class="wmh-drop-item" href="${s.href}" target="_blank" rel="noopener noreferrer">${s.svg} ${s.label}</a>`
  ).join("");

  const langItems = Object.entries(LANGS).map(([code, d]) =>
    `<div class="wmh-drop-item ${code === currentLang ? 'active' : ''}" data-lang="${code}"><span>${d.flag}</span> ${d.label}</div>`
  ).join("");

  const svgShare = `<svg viewBox="0 0 24 24" width="17" height="17"><path fill="currentColor" d="M18 16c-.8 0-1.4.3-1.9.8L8.9 12.7c.1-.2.1-.5.1-.7s0-.5-.1-.7l7.1-4.1c.5.5 1.2.8 2 .8 1.7 0 3-1.3 3-3s-1.3-3-3-3-3 1.3-3 3c0 .2 0 .5.1.7L7.9 9.8C7.4 9.3 6.7 9 6 9c-1.7 0-3 1.3-3 3s1.3 3 3 3c.7 0 1.4-.3 1.9-.8l7.2 4.1c-.1.2-.1.4-.1.7 0 1.6 1.3 2.9 2.9 2.9s2.9-1.3 2.9-2.9S19.6 16 18 16z"/></svg>`;

  const headerHTML = `
    <header class="wmh-bar">
      <div class="wmh-inner">
        <div class="wmh-left">
          <a class="wmh-brand" href="${homeLink}" aria-label="WiggMap home">
            <img src="${prefix}assets/logo.png" alt="WiggMap logo">
          </a>
        </div>
        <div class="wmh-right">

          <!-- Icônes sociales — desktop uniquement -->
          <div class="wmh-social">
            <a class="wmh-ico" href="${X_URL}" target="_blank" rel="noopener noreferrer" title="X">
              <svg viewBox="0 0 24 24" width="17" height="17"><path fill="currentColor" d="M18.9 2H22l-6.6 7.6L23.5 22h-6.7l-5.2-6.8L5.6 22H2.5l7.1-8.2L.5 2h6.8l4.7 6.1L18.9 2Zm-1.2 18h1.8L6.2 3.9H4.3L17.7 20Z"/></svg>
            </a>
            <a class="wmh-ico" href="${IG_URL}" target="_blank" rel="noopener noreferrer" title="Instagram">
              <svg viewBox="0 0 24 24" width="17" height="17"><path fill="currentColor" d="M7.8 2h8.4A5.8 5.8 0 0 1 22 7.8v8.4A5.8 5.8 0 0 1 16.2 22H7.8A5.8 5.8 0 0 1 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2Zm0 2A3.8 3.8 0 0 0 4 7.8v8.4A3.8 3.8 0 0 0 7.8 20h8.4a3.8 3.8 0 0 0 3.8-3.8V7.8A3.8 3.8 0 0 0 16.2 4H7.8Z"/><path fill="currentColor" d="M12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z"/><circle fill="currentColor" cx="17.5" cy="6.5" r="1.1"/></svg>
            </a>
            <a class="wmh-ico wmh-ico--tg" href="${TELEGRAM_URL}" target="_blank" rel="noopener noreferrer" title="Telegram">
              <svg viewBox="0 0 24 24" width="17" height="17"><path fill="currentColor" d="M21.9 4.6c.2-.8-.5-1.5-1.3-1.2L2.7 10.4c-.9.4-.9 1.7.1 2l4.6 1.5 1.8 5.6c.3 1 1.6 1.1 2.1.3l2.6-3.7 4.9 3.6c.7.5 1.7.1 1.9-.8l1.2-14.3ZM8.3 13.2l9.9-6.1-7.6 7.4-.3 3.9-1.7-5.1-2.5-.8Z"/></svg>
            </a>
          </div>

          <!-- Dropdown réseaux — mobile uniquement, caché par défaut -->
          <div class="wmh-dropdown" id="wmhSocialDropdown" style="display:none;">
            <div class="wmh-drop-trigger" id="wmhSocialTrigger">
              ${svgShare}<span class="arrow">▾</span>
            </div>
            <div class="wmh-drop-menu">${socialItems}</div>
          </div>

          <!-- Dropdown langue — partout -->
          <div class="wmh-dropdown" id="wmhLangDropdown">
            <div class="wmh-drop-trigger" id="wmhLangTrigger">
              <span>${currentLangData.flag}</span><span class="arrow">▾</span>
            </div>
            <div class="wmh-drop-menu">${langItems}</div>
          </div>

          <nav class="wmh-nav">
            <a class="wmh-btn" href="${globeLink}" target="_blank" rel="noopener noreferrer">🌍 Globe</a>
            <a class="wmh-btn" href="#" id="btnRandom">🎲 Random</a>
            <a class="wmh-btn wmh-btn--game" href="${prefix}ggg/wigggame.html"><img src="${prefix}assets/wigggame2.png" alt="WiggGame" style="height:22px;width:auto;display:block;"></a>
          </nav>
        </div>

        <nav class="wmh-nav-mobile">
          <a class="wmh-btn" href="${globeLink}" target="_blank" rel="noopener noreferrer">🌍 Globe</a>
          <a class="wmh-btn" href="#" id="btnRandomMobile">🎲 Random</a>
          <a class="wmh-btn wmh-btn--game" href="${prefix}ggg/wigggame.html"><img src="${prefix}assets/wigggame2.png" alt="WiggGame" style="height:20px;width:auto;display:block;"></a>
        </nav>
      </div>
    </header>
  `;

  const mount = document.getElementById("siteHeader");
  if (!mount) return console.warn("siteHeader not found");
  mount.innerHTML = headerHTML;

  // Social dropdown visible sur mobile seulement
  function updateSocialVisibility(){
    const el = document.getElementById("wmhSocialDropdown");
    if(el) el.style.display = window.innerWidth <= 640 ? "block" : "none";
  }
  updateSocialVisibility();
  window.addEventListener("resize", updateSocialVisibility);

  // Dropdown toggle
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

  // Lang selection
  document.querySelectorAll("[data-lang]").forEach(item => {
    item.addEventListener("click", () => {
      localStorage.setItem("wigg_lang", item.dataset.lang);
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
      window.location.href = "/countries/country.html?country=" + encodeURIComponent(slug);
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

})();
