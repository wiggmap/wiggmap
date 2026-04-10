// ═══════════════════════════════════════════════════════════
// WiggMap Connect Widget — Supabase Auth + Real Posts
// Vanilla JS · Supabase CDN · No framework
// ═══════════════════════════════════════════════════════════

(function () {
  'use strict';

  // ╔═══════════════════════════════════════════════════════╗
  // ║  REMPLACE CES 2 LIGNES PAR TES VRAIES VALEURS        ║
  // ║  Supabase Dashboard → Settings → API                  ║
  // ╚═══════════════════════════════════════════════════════╝
  const SUPABASE_URL  = 'https://tkctreoftezvbfejhbto.supabase.co';
  const SUPABASE_KEY  = 'sb_publishable_lAKWBnp2nbfgb2w5Uj55aQ_aD6fBWUb';

  // ── Detect page & extract slug ───────────────────────────
  const path = window.location.pathname;
  if (!path.includes('/chronicles/') || !path.includes('chronicle-')) return;

  let citySlug, cityName, isCity = false;
  if (path.includes('/villes/')) {
    const cm = path.match(/chronicle-([a-z0-9-]+?)-[a-z]+-(?:en|fr|es)\.html$/);
    if (!cm) return;
    citySlug = cm[1];
    isCity = true;
  } else {
    const tm = path.match(/chronicle-(.+)-(?:en|fr|es)\.html$/);
    if (!tm) return;
    citySlug = tm[1].replace(/-2026$/, '');
  }
  cityName = citySlug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');

  const langM = path.match(/-(en|fr|es)\.html$/);
  const lang = langM ? langM[1] : 'fr';

  // ── i18n ─────────────────────────────────────────────────
  const T = {
    fr: {
      title: 'La communauté', save: 'Sauvegarder', saved: 'sauvegardée ✓',
      pinned: 'Épinglé par la communauté', recent: 'Discussions récentes',
      useful: '✦ Utile', validated: '✦ Validé terrain', votes: 'votes',
      loginQ: 'Tu vis à {city} ou tu prépares ton départ ?',
      loginCta: 'Rejoindre Connect →',
      yourXp: 'Ton expérience',
      placeholder: 'Partage ce que les articles ne disent pas…',
      types: { temoignage: 'Témoignage', flash: 'Flash', question: 'Question' },
      publish: 'Publier',
      authTitle: 'Connecte-toi pour publier',
      authSub: 'Ton compte te permet aussi de sauvegarder des villes et suivre tes contributions.',
      authGoogle: 'Continuer avec Google',
      
      authLegal: 'En continuant, tu acceptes les <a href="/terms.html">CGU</a> de WiggMap.',
      authClose: 'Fermer',
      noPostsYet: 'Sois le premier à partager ton expérience ici.',
      myAccount: 'Mon compte',
      logout: 'Déconnexion',
      posting: 'Publication…',
      posted: 'Publié ✓',
      loginFirst: 'Connecte-toi d\'abord',
    },
    en: {
      title: 'The community', save: 'Save', saved: 'saved ✓',
      pinned: 'Pinned by the community', recent: 'Recent discussions',
      useful: '✦ Useful', validated: '✦ Field-validated', votes: 'votes',
      loginQ: 'Do you live in {city} or are you preparing your move?',
      loginCta: 'Join Connect →',
      yourXp: 'Your experience',
      placeholder: 'Share what the articles don\'t tell you…',
      types: { temoignage: 'Testimony', flash: 'Flash', question: 'Question' },
      publish: 'Publish',
      authTitle: 'Sign in to publish',
      authSub: 'Your account also lets you save cities and track your contributions.',
      authGoogle: 'Continue with Google',
      
      authLegal: 'By continuing, you accept WiggMap\'s <a href="/terms.html">Terms</a>.',
      authClose: 'Close',
      noPostsYet: 'Be the first to share your experience here.',
      myAccount: 'My account',
      logout: 'Sign out',
      posting: 'Publishing…',
      posted: 'Published ✓',
      loginFirst: 'Sign in first',
    },
    es: {
      title: 'La comunidad', save: 'Guardar', saved: 'guardada ✓',
      pinned: 'Fijado por la comunidad', recent: 'Discusiones recientes',
      useful: '✦ Útil', validated: '✦ Validado en terreno', votes: 'votos',
      loginQ: '¿Vives en {city} o preparas tu mudanza?',
      loginCta: 'Unirse a Connect →',
      yourXp: 'Tu experiencia',
      placeholder: 'Comparte lo que los artículos no cuentan…',
      types: { temoignage: 'Testimonio', flash: 'Flash', question: 'Pregunta' },
      publish: 'Publicar',
      authTitle: 'Inicia sesión para publicar',
      authSub: 'Tu cuenta también te permite guardar ciudades y seguir tus aportes.',
      authGoogle: 'Continuar con Google',
      
      authLegal: 'Al continuar, aceptas los <a href="/terms.html">Términos</a> de WiggMap.',
      authClose: 'Cerrar',
      noPostsYet: 'Sé el primero en compartir tu experiencia aquí.',
      myAccount: 'Mi cuenta',
      logout: 'Cerrar sesión',
      posting: 'Publicando…',
      posted: 'Publicado ✓',
      loginFirst: 'Inicia sesión primero',
    }
  };
  const t = T[lang] || T.fr;

  // ── Supabase client (lazy-loaded) ────────────────────────
  let sb = null;
  let currentUser = null;

  function loadSupabase() {
    return new Promise(resolve => {
      if (window.supabase) {
        sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
        return resolve(sb);
      }
      const s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js';
      s.onload = () => {
        sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
        resolve(sb);
      };
      document.head.appendChild(s);
    });
  }

  async function getSession() {
    if (!sb) await loadSupabase();
    const { data } = await sb.auth.getSession();
    currentUser = data?.session?.user || null;
    return currentUser;
  }

  // ── localStorage helpers (fallback for guests) ───────────
  function getSaved() {
    try { return JSON.parse(localStorage.getItem('wigg_saved_cities') || '[]'); } catch (e) { return []; }
  }
  function setSaved(arr) { localStorage.setItem('wigg_saved_cities', JSON.stringify(arr)); }
  function isSaved() { return getSaved().includes(citySlug); }
  function getVoted(postId) { return localStorage.getItem('wigg_useful_' + citySlug + '_' + postId) === '1'; }
  function setVotedLocal(postId) { localStorage.setItem('wigg_useful_' + citySlug + '_' + postId, '1'); }
  function getLocalCount(postId) { return parseInt(localStorage.getItem('wigg_count_' + citySlug + '_' + postId) || '0', 10); }
  function setLocalCount(postId, n) { localStorage.setItem('wigg_count_' + citySlug + '_' + postId, String(n)); }

  // ── Esc HTML ─────────────────────────────────────────────
  function esc(s) { const d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; }

  // ── Build post HTML ──────────────────────────────────────
  function buildPostHTML(post) {
    const count = Math.max(post.useful_count || 0, getLocalCount(post.id));
    const isPinned = post.is_pinned || count >= 10;
    const isVoted = getVoted(post.id);
    const pct = Math.min(count / 10 * 100, 100);
    const typeLabel = t.types[post.post_type || post.type] || post.post_type || 'post';
    const author = post.profiles?.username || post.author || 'Anonyme';
    const avatar = post.profiles?.avatar_url || '';
    const initials = author.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

    return `
      <div class="wcc-post ${isPinned ? 'pinned' : ''}" data-post-id="${post.id}">
        ${isPinned ? '<div class="wcc-validated">' + t.validated + '</div>' : ''}
        <span class="wcc-type-tag ${post.post_type || post.type || ''}">${esc(typeLabel)}</span>
        <div class="wcc-post-meta">
          <div class="wcc-avatar-sm" ${avatar ? 'style="background-image:url(' + esc(avatar) + ');background-size:cover"' : ''}>${avatar ? '' : esc(initials)}</div>
          <span class="wcc-post-author">${esc(author)}</span>
        </div>
        <div class="wcc-post-text">${esc(post.content || post.text || '')}</div>
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

  // ── Build widget ─────────────────────────────────────────
  function buildWidget(posts, user) {
    const allPosts = posts || [];
    const pinned = allPosts.filter(p => p.is_pinned || (p.useful_count || 0) >= 10);
    const recent = allPosts.filter(p => !p.is_pinned && (p.useful_count || 0) < 10);
    const savedState = isSaved();
    const isAuth = !!user;
    const userName = user?.user_metadata?.full_name || user?.email?.split('@')[0] || '';
    const userAvatar = user?.user_metadata?.avatar_url || '';
    const userInitials = userName.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

    return `
    <div class="wcc-widget">
      <div class="wcc-header">
        <div class="wcc-title">${t.title} ${esc(cityName)}</div>
        <div class="wcc-header-right">
          ${isAuth ? `
            <a href="/mon-compte.html" class="wcc-user-badge">
              <div class="wcc-avatar" ${userAvatar ? 'style="background-image:url(' + esc(userAvatar) + ');background-size:cover"' : ''}>${userAvatar ? '' : esc(userInitials)}</div>
              <span>${esc(userName.split(' ')[0])}</span>
            </a>
          ` : ''}
          <button class="wcc-save-btn ${savedState ? 'saved' : ''}" id="wccSaveBtn">
            ${savedState ? esc(cityName) + ' ' + t.saved : t.save + ' ' + esc(cityName)}
          </button>
        </div>
      </div>

      ${pinned.length ? `
      <div class="wcc-sep">${t.pinned}</div>
      ${pinned.map(buildPostHTML).join('')}
      ` : ''}

      <div class="wcc-sep">${t.recent}</div>
      ${recent.length ? recent.map(buildPostHTML).join('')
        : `<p class="wcc-empty">${t.noPostsYet}</p>`}

      ${!isAuth ? `
      <div class="wcc-login-banner">
        <span class="wcc-login-text">${t.loginQ.replace('{city}', esc(cityName))}</span>
        <button class="wcc-login-link" id="wccShowAuth">${t.loginCta}</button>
      </div>
      ` : ''}

      <div class="wcc-sep">${t.yourXp}</div>
      <div class="wcc-compose">
        <textarea class="wcc-textarea" id="wccTextarea" placeholder="${t.placeholder}" ${!isAuth ? 'disabled' : ''}></textarea>
        <div class="wcc-compose-row">
          <div class="wcc-type-pills">
            <span class="wcc-type-pill temoignage active" data-type="temoignage">${t.types.temoignage}</span>
            <span class="wcc-type-pill flash" data-type="flash">${t.types.flash}</span>
            <span class="wcc-type-pill question" data-type="question">${t.types.question}</span>
          </div>
          <button class="wcc-publish-btn ${isAuth ? 'active' : ''}" id="wccPublishBtn">${t.publish}</button>
        </div>
      </div>

      <!-- Auth modal (hidden by default) -->
      <div class="wcc-auth-overlay" id="wccAuthOverlay" style="display:none">
        <div class="wcc-auth-modal">
          <button class="wcc-auth-close" id="wccAuthClose">&times;</button>
          <p class="wcc-auth-title">${t.authTitle}</p>
          <p class="wcc-auth-sub">${t.authSub}</p>
          <button class="wcc-auth-btn wcc-auth-google" id="wccLoginGoogle">
            <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
            ${t.authGoogle}
          </button>
          <p class="wcc-auth-legal">${t.authLegal}</p>
        </div>
      </div>
    </div>`;
  }

  // ── Fetch posts from Supabase ────────────────────────────
  async function fetchPosts() {
    if (!sb) await loadSupabase();
    try {
      const { data, error } = await sb
        .from('posts')
        .select('*, profiles(username, avatar_url)')
        .eq('city_slug', citySlug)
        .order('is_pinned', { ascending: false })
        .order('created_at', { ascending: false })
        .limit(20);
      if (error) throw error;
      return data || [];
    } catch (e) {
      console.warn('WCC: Could not fetch posts', e);
      return [];
    }
  }

  // ── Auth functions ───────────────────────────────────────
  async function loginGoogle() {
    if (!sb) await loadSupabase();
    await sb.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: window.location.href }
    });
  }

  async function migrateLocalStorage(userId) {
    const saved = getSaved();
    for (const slug of saved) {
      await sb.from('saved_cities').upsert(
        { user_id: userId, city_slug: slug },
        { onConflict: 'user_id,city_slug' }
      ).catch(() => {});
    }
  }

  // ── Publish post ─────────────────────────────────────────
  async function publishPost(content, postType) {
    if (!currentUser || !sb) return;
    // Upsert profile
    await sb.from('profiles').upsert({
      id: currentUser.id,
      username: currentUser.user_metadata?.full_name || currentUser.email?.split('@')[0] || 'User',
      avatar_url: currentUser.user_metadata?.avatar_url || null,
    }, { onConflict: 'id' }).catch(() => {});

    const { data, error } = await sb.from('posts').insert({
      author_id: currentUser.id,
      city_slug: citySlug,
      post_type: postType,
      content: content,
      useful_count: 0,
      is_pinned: false,
    }).select('*, profiles(username, avatar_url)').single();

    if (error) { console.error('WCC publish error', error); return null; }
    return data;
  }

  // ── Vote ─────────────────────────────────────────────────
  async function voteUseful(postId) {
    if (getVoted(postId)) return;
    setVotedLocal(postId);
    let count = getLocalCount(postId) + 1;
    setLocalCount(postId, count);

    // If logged in, also write to Supabase
    if (currentUser && sb) {
      await sb.from('useful_votes').insert({
        post_id: postId, user_id: currentUser.id
      }).catch(() => {});
      await sb.rpc('increment_useful', { post_uuid: postId }).catch(() => {
        // Fallback if RPC doesn't exist: direct update
        sb.from('posts').update({ useful_count: count }).eq('id', postId).catch(() => {});
      });
    }
    return count;
  }

  // ── Init widget ──────────────────────────────────────────
  function attachListeners() {
    // Save button
    const saveBtn = document.getElementById('wccSaveBtn');
    if (saveBtn) {
      saveBtn.addEventListener('click', async () => {
        const saved = getSaved();
        if (saved.includes(citySlug)) {
          saved.splice(saved.indexOf(citySlug), 1);
          setSaved(saved);
          saveBtn.classList.remove('saved');
          saveBtn.textContent = t.save + ' ' + cityName;
          if (currentUser && sb) await sb.from('saved_cities').delete().eq('user_id', currentUser.id).eq('city_slug', citySlug).catch(() => {});
        } else {
          saved.push(citySlug);
          setSaved(saved);
          saveBtn.classList.add('saved');
          saveBtn.textContent = cityName + ' ' + t.saved;
          if (currentUser && sb) await sb.from('saved_cities').upsert({ user_id: currentUser.id, city_slug: citySlug }, { onConflict: 'user_id,city_slug' }).catch(() => {});
        }
      });
    }

    // Auth modal
    const showAuth = document.getElementById('wccShowAuth');
    const overlay = document.getElementById('wccAuthOverlay');
    const closeAuth = document.getElementById('wccAuthClose');
    if (showAuth) showAuth.addEventListener('click', () => overlay.style.display = 'flex');
    if (closeAuth) closeAuth.addEventListener('click', () => overlay.style.display = 'none');
    if (overlay) overlay.addEventListener('click', e => { if (e.target === overlay) overlay.style.display = 'none'; });

    // Google login
    const gBtn = document.getElementById('wccLoginGoogle');
    if (gBtn) gBtn.addEventListener('click', loginGoogle);
    

    // Vote buttons
    document.querySelectorAll('.wcc-useful-btn').forEach(btn => {
      btn.addEventListener('click', async () => {
        const postId = btn.dataset.postId;
        const count = await voteUseful(postId);
        if (count === undefined) return;
        btn.classList.add('voted');
        const row = btn.closest('.wcc-useful-row');
        const fill = row?.querySelector('.wcc-progress-fill');
        const countEl = row?.querySelector('.wcc-useful-count');
        if (fill) fill.style.width = Math.min(count / 10 * 100, 100) + '%';
        if (countEl) countEl.textContent = count + '/10 ' + t.votes;
        if (count >= 10) {
          const post = btn.closest('.wcc-post');
          post.classList.add('pinned');
          btn.textContent = t.validated;
          if (!post.querySelector('.wcc-validated')) {
            const badge = document.createElement('div');
            badge.className = 'wcc-validated';
            badge.textContent = t.validated;
            post.prepend(badge);
          }
          row?.querySelector('.wcc-progress')?.remove();
          countEl?.remove();
        }
      });
    });

    // Type pills
    document.querySelectorAll('.wcc-type-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        document.querySelectorAll('.wcc-type-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
      });
    });

    // Publish button
    const pubBtn = document.getElementById('wccPublishBtn');
    const textarea = document.getElementById('wccTextarea');
    if (pubBtn) {
      pubBtn.addEventListener('click', async () => {
        if (!currentUser) {
          // Show auth modal
          if (overlay) overlay.style.display = 'flex';
          return;
        }
        const content = textarea?.value?.trim();
        if (!content) return;
        const activeType = document.querySelector('.wcc-type-pill.active')?.dataset?.type || 'temoignage';

        pubBtn.textContent = t.posting;
        pubBtn.disabled = true;
        const post = await publishPost(content, activeType);
        if (post) {
          // Prepend to recent list
          const recentSep = [...document.querySelectorAll('.wcc-sep')].find(s => s.textContent === t.recent);
          if (recentSep) {
            const div = document.createElement('div');
            div.innerHTML = buildPostHTML(post);
            recentSep.after(div.firstElementChild);
          }
          textarea.value = '';
          pubBtn.textContent = t.posted;
          setTimeout(() => { pubBtn.textContent = t.publish; pubBtn.disabled = false; }, 2000);
        } else {
          pubBtn.textContent = t.publish;
          pubBtn.disabled = false;
        }
      });
    }

    // Textarea click when not logged in
    if (textarea && !currentUser) {
      textarea.addEventListener('focus', () => {
        if (!currentUser && overlay) {
          textarea.blur();
          overlay.style.display = 'flex';
        }
      });
    }
  }

  // ── Auto-injection ───────────────────────────────────────
  document.addEventListener('DOMContentLoaded', async () => {
    const target = document.getElementById('siteFooter')
      || document.querySelector('script[src*="footer.js"]')
      || document.body.lastElementChild;
    if (!target) return;

    // Load Supabase + check session
    await loadSupabase();
    const user = await getSession();
    if (user) await migrateLocalStorage(user.id);

    // Fetch real posts (or empty array if no backend yet)
    const posts = await fetchPosts();

    // Build + inject
    const container = document.createElement('div');
    container.id = 'wigg-connect-widget';
    container.innerHTML = buildWidget(posts, user);
    target.parentNode.insertBefore(container, target);
    attachListeners();
  });

})();
