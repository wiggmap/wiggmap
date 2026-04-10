// ═══════════════════════════════════════════════════════════
// WiggMap Connect Widget — Chronicle Cities (Phase 0)
// Vanilla JS · No dependencies · localStorage only
// ═══════════════════════════════════════════════════════════

(function () {
  'use strict';

  // ── Detect page & extract slug (universal) ───────────────
  const path = window.location.pathname;
  if (!path.includes('/chronicles/') || !path.includes('chronicle-')) return;

  let citySlug, cityName, isCity = false;

  if (path.includes('/villes/')) {
    // City chronicle: chronicle-bangkok-thailand-fr.html → "bangkok"
    const cm = path.match(/chronicle-([a-z0-9-]+?)-[a-z]+-(?:en|fr|es)\.html$/);
    if (!cm) return;
    citySlug = cm[1];
    isCity = true;
  } else {
    // Thematic chronicle: chronicle-visa-nomade-digital-fr.html → "visa-nomade-digital"
    const tm = path.match(/chronicle-(.+)-(?:en|fr|es)\.html$/);
    if (!tm) return;
    citySlug = tm[1];
    // Remove trailing -2026 if present
    citySlug = citySlug.replace(/-2026$/, '');
  }

  cityName = citySlug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');

  // ── i18n ─────────────────────────────────────────────────
  const langM = path.match(/-(en|fr|es)\.html$/);
  const lang = langM ? langM[1] : 'fr';

  const T = {
    fr: {
      title: 'La communauté',
      save: 'Sauvegarder',
      saved: 'sauvegardée ✓',
      pinned: 'Épinglé par la communauté',
      recent: 'Discussions récentes',
      useful: '✦ Utile',
      validated: '✦ Validé terrain',
      votes: 'votes',
      loginQ: 'Tu vis à {city} ou tu prépares ton départ ?',
      loginCta: 'Rejoindre Connect →',
      yourXp: 'Ton expérience',
      placeholder: 'Partage ce que les articles ne disent pas…',
      types: { temoignage: 'Témoignage', flash: 'Flash', question: 'Question' },
      publish: 'Publier',
      publishMsg: 'Crée ton profil Connect pour publier →',
    },
    en: {
      title: 'The community',
      save: 'Save',
      saved: 'saved ✓',
      pinned: 'Pinned by the community',
      recent: 'Recent discussions',
      useful: '✦ Useful',
      validated: '✦ Field-validated',
      votes: 'votes',
      loginQ: 'Do you live in {city} or are you preparing your move?',
      loginCta: 'Join Connect →',
      yourXp: 'Your experience',
      placeholder: 'Share what the articles don\'t tell you…',
      types: { temoignage: 'Testimony', flash: 'Flash', question: 'Question' },
      publish: 'Publish',
      publishMsg: 'Create your Connect profile to publish →',
    },
    es: {
      title: 'La comunidad',
      save: 'Guardar',
      saved: 'guardada ✓',
      pinned: 'Fijado por la comunidad',
      recent: 'Discusiones recientes',
      useful: '✦ Útil',
      validated: '✦ Validado en terreno',
      votes: 'votos',
      loginQ: '¿Vives en {city} o preparas tu mudanza?',
      loginCta: 'Unirse a Connect →',
      yourXp: 'Tu experiencia',
      placeholder: 'Comparte lo que los artículos no cuentan…',
      types: { temoignage: 'Testimonio', flash: 'Flash', question: 'Pregunta' },
      publish: 'Publicar',
      publishMsg: 'Crea tu perfil Connect para publicar →',
    }
  };
  const t = T[lang] || T.fr;

  // ── Demo posts ───────────────────────────────────────────
  const DEMO_POSTS = [
    {
      id: 'demo-1',
      type: 'temoignage',
      author: 'Wigg Team',
      route: '🌍 WiggMap',
      text: lang === 'fr'
        ? 'Sois le premier à partager ton expérience ici. Les meilleurs posts sont épinglés par la communauté.'
        : lang === 'es'
        ? 'Sé el primero en compartir tu experiencia aquí. Los mejores posts son fijados por la comunidad.'
        : 'Be the first to share your experience here. The best posts are pinned by the community.',
      useful_count: 0,
      pinned: false,
    }
  ];

  // ── localStorage helpers ─────────────────────────────────
  function getVoted(postId) {
    return localStorage.getItem('wigg_useful_' + citySlug + '_' + postId) === '1';
  }
  function setVoted(postId) {
    localStorage.setItem('wigg_useful_' + citySlug + '_' + postId, '1');
  }
  function getSaved() {
    try { return JSON.parse(localStorage.getItem('wigg_saved_cities') || '[]'); } catch (e) { return []; }
  }
  function setSaved(arr) {
    localStorage.setItem('wigg_saved_cities', JSON.stringify(arr));
  }
  function isSaved() {
    return getSaved().includes(citySlug);
  }

  // ── Post counts from localStorage (phase 0) ─────────────
  function getLocalCount(postId) {
    return parseInt(localStorage.getItem('wigg_count_' + citySlug + '_' + postId) || '0', 10);
  }
  function setLocalCount(postId, n) {
    localStorage.setItem('wigg_count_' + citySlug + '_' + postId, String(n));
  }

  // ── Build HTML ───────────────────────────────────────────
  function buildPostHTML(post) {
    const count = Math.max(post.useful_count, getLocalCount(post.id));
    const isPinned = post.pinned || count >= 10;
    const isVoted = getVoted(post.id);
    const pct = Math.min(count / 10 * 100, 100);
    const typeLabel = t.types[post.type] || post.type;

    return `
      <div class="wcc-post ${isPinned ? 'pinned' : ''}" data-post-id="${post.id}">
        ${isPinned ? '<div class="wcc-validated">' + t.validated + '</div>' : ''}
        <span class="wcc-type-tag ${post.type}">${typeLabel}</span>
        <div class="wcc-post-author">${esc(post.author)}</div>
        <div class="wcc-post-route">${esc(post.route)}</div>
        <div class="wcc-post-text">${esc(post.text)}</div>
        <div class="wcc-useful-row">
          <button class="wcc-useful-btn ${isVoted ? 'voted' : ''}" data-post-id="${post.id}">
            ${isPinned ? t.validated : t.useful}
          </button>
          ${!isPinned ? `
          <div class="wcc-progress"><div class="wcc-progress-fill" style="width:${pct}%"></div></div>
          <span class="wcc-useful-count">${count}/10 ${t.votes}</span>
          ` : ''}
        </div>
      </div>`;
  }

  function esc(s) {
    const d = document.createElement('div');
    d.textContent = s || '';
    return d.innerHTML;
  }

  function buildWidget() {
    const posts = DEMO_POSTS;
    const pinned = posts.filter(p => p.pinned || getLocalCount(p.id) >= 10);
    const recent = posts.filter(p => !p.pinned && getLocalCount(p.id) < 10);
    const savedState = isSaved();

    return `
    <div class="wcc-widget">
      <div class="wcc-header">
        <div class="wcc-title">${t.title} ${esc(cityName)}</div>
        <button class="wcc-save-btn ${savedState ? 'saved' : ''}" id="wccSaveBtn">
          ${savedState ? esc(cityName) + ' ' + t.saved : t.save + ' ' + esc(cityName)}
        </button>
      </div>

      ${pinned.length ? `
      <div class="wcc-sep">${t.pinned}</div>
      ${pinned.map(buildPostHTML).join('')}
      ` : ''}

      <div class="wcc-sep">${t.recent}</div>
      ${recent.length ? recent.map(buildPostHTML).join('') : ''}

      <div class="wcc-login-banner">
        <span class="wcc-login-text">${t.loginQ.replace('{city}', esc(cityName))}</span>
        <a href="/connect/" class="wcc-login-link">${t.loginCta}</a>
      </div>

      <div class="wcc-sep">${t.yourXp}</div>
      <div class="wcc-compose">
        <textarea class="wcc-textarea" placeholder="${t.placeholder}"></textarea>
        <div class="wcc-type-pills">
          <span class="wcc-type-pill temoignage active" data-type="temoignage">${t.types.temoignage}</span>
          <span class="wcc-type-pill flash" data-type="flash">${t.types.flash}</span>
          <span class="wcc-type-pill question" data-type="question">${t.types.question}</span>
        </div>
        <button class="wcc-publish-btn" id="wccPublishBtn">${t.publish}</button>
      </div>
    </div>`;
  }

  // ── Init ──────────────────────────────────────────────────
  function initWidget() {
    // Save button
    const saveBtn = document.getElementById('wccSaveBtn');
    if (saveBtn) {
      saveBtn.addEventListener('click', function () {
        const saved = getSaved();
        if (saved.includes(citySlug)) {
          saved.splice(saved.indexOf(citySlug), 1);
          setSaved(saved);
          saveBtn.classList.remove('saved');
          saveBtn.textContent = t.save + ' ' + cityName;
        } else {
          saved.push(citySlug);
          setSaved(saved);
          saveBtn.classList.add('saved');
          saveBtn.textContent = cityName + ' ' + t.saved;
        }
      });
    }

    // Vote buttons
    document.querySelectorAll('.wcc-useful-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const postId = btn.dataset.postId;
        if (getVoted(postId)) return;
        setVoted(postId);
        let count = getLocalCount(postId) + 1;
        setLocalCount(postId, count);

        btn.classList.add('voted');
        const row = btn.closest('.wcc-useful-row');
        const fill = row.querySelector('.wcc-progress-fill');
        const countEl = row.querySelector('.wcc-useful-count');
        if (fill) fill.style.width = Math.min(count / 10 * 100, 100) + '%';
        if (countEl) countEl.textContent = count + '/10 ' + t.votes;

        if (count >= 10) {
          const post = btn.closest('.wcc-post');
          post.classList.add('pinned');
          btn.textContent = t.validated;
          // Add validated badge
          if (!post.querySelector('.wcc-validated')) {
            const badge = document.createElement('div');
            badge.className = 'wcc-validated';
            badge.textContent = t.validated;
            post.prepend(badge);
          }
          // Remove progress bar
          const progress = row.querySelector('.wcc-progress');
          if (progress) progress.remove();
          if (countEl) countEl.remove();
        }
      });
    });

    // Type pills
    document.querySelectorAll('.wcc-type-pill').forEach(function (pill) {
      pill.addEventListener('click', function () {
        document.querySelectorAll('.wcc-type-pill').forEach(function (p) { p.classList.remove('active'); });
        pill.classList.add('active');
      });
    });

    // Publish button (Phase 0 — no backend)
    const pubBtn = document.getElementById('wccPublishBtn');
    if (pubBtn) {
      pubBtn.addEventListener('click', function () {
        alert(t.publishMsg);
        window.location.href = '/connect/';
      });
    }
  }

  // ── Auto-injection ───────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    // Find insertion point: before siteFooter, or before footer.js, or end of body
    const target = document.getElementById('siteFooter')
      || document.querySelector('script[src*="footer.js"]')
      || document.body.lastElementChild;

    if (!target) return;

    const container = document.createElement('div');
    container.id = 'wigg-connect-widget';
    container.innerHTML = buildWidget();
    target.parentNode.insertBefore(container, target);
    initWidget();
  });

})();
