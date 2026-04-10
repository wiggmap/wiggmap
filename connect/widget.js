// WiggMap Connect — Chronicle Comment Widget
(function () {
  'use strict';

  /* ── Config ── */
  var SUPABASE_URL = 'https://tkctreoftezvbfejhbto.supabase.co';
  var SUPABASE_KEY = 'sb_publishable_lAKWBnp2nbfgb2w5Uj55aQ_aD6fBWUb';
  var PINNED_THRESHOLD = 10;

  /* ── Slug detection ── */
  function getSlug() {
    var file = window.location.pathname.split('/').pop().replace('.html', '');
    var slug = file.replace(/^chronicle-/, '');
    slug = slug.replace(/-(en|fr|es)$/, '');
    return slug;
  }

  /* ── Lang detection ── */
  function getLang() {
    var file = window.location.pathname.split('/').pop();
    if (file.endsWith('-fr.html')) return 'fr';
    if (file.endsWith('-es.html')) return 'es';
    return 'en';
  }

  var SLUG = getSlug();
  var LANG = getLang();

  var I18N = {
    en: {
      title: 'Community',
      save: 'Save this page',
      saved: 'Saved',
      login: 'Continue with Google',
      logout: 'Sign out',
      placeholder: 'Share your experience, tip or question\u2026',
      submit: 'Post',
      useful: 'Useful',
      pinned: 'Validated on the ground',
      empty: 'No posts yet \u2014 be the first to share.',
      temoignage: 'Testimony',
      flash: 'Flash infos',
      question: 'Question',
      loginFirst: 'Sign in to post'
    },
    fr: {
      title: 'Communaut\u00e9',
      save: 'Sauvegarder cette page',
      saved: 'Sauvegard\u00e9e',
      login: 'Continuer avec Google',
      logout: 'Se d\u00e9connecter',
      placeholder: 'Partage ton exp\u00e9rience, conseil ou question\u2026',
      submit: 'Publier',
      useful: 'Utile',
      pinned: 'Valid\u00e9 terrain',
      empty: 'Aucun post pour le moment \u2014 sois le premier.',
      temoignage: 'T\u00e9moignage',
      flash: 'Flash infos',
      question: 'Question',
      loginFirst: 'Connecte-toi pour poster'
    },
    es: {
      title: 'Comunidad',
      save: 'Guardar esta p\u00e1gina',
      saved: 'Guardada',
      login: 'Continuar con Google',
      logout: 'Cerrar sesi\u00f3n',
      placeholder: 'Comparte tu experiencia, consejo o pregunta\u2026',
      submit: 'Publicar',
      useful: '\u00datil',
      pinned: 'Validado en terreno',
      empty: 'Sin publicaciones a\u00fan \u2014 s\u00e9 el primero.',
      temoignage: 'Testimonio',
      flash: 'Flash infos',
      question: 'Pregunta',
      loginFirst: 'Inicia sesi\u00f3n para publicar'
    }
  };

  var t = I18N[LANG] || I18N.en;

  /* ── Supabase init ── */
  var sb = null;
  var currentUser = null;

  function initSupabase(cb) {
    function create() {
      sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY, {
        auth: {
          detectSessionInUrl: true,
          persistSession: true,
          autoRefreshToken: true
        }
      });
      console.log('[wcc] Supabase client created');
      cb();
    }
    if (window.supabase) return create();
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js';
    s.onload = create;
    document.head.appendChild(s);
  }

  /* ── Helpers ── */
  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html) e.innerHTML = html;
    return e;
  }

  /* ── Translate Supabase error messages to user-friendly text ── */
  function friendlyError(err) {
    if (!err) return '';
    var msg = (err.message || err.code || '').toLowerCase();
    var ERR = {
      en: {
        invalid_credentials: 'Wrong email or password.',
        email_not_confirmed: 'Confirm your email first — check your inbox.',
        user_already_registered: 'This email is already registered. Sign in instead.',
        weak_password: 'Password too weak — use at least 6 characters.',
        rate_limit: 'Too many attempts — try again in a minute.',
        network: 'Network error — check your connection.',
        generic: 'Something went wrong. Please try again.'
      },
      fr: {
        invalid_credentials: 'Email ou mot de passe incorrect.',
        email_not_confirmed: 'Confirme ton email d\u2019abord \u2014 v\u00e9rifie ta bo\u00eete mail.',
        user_already_registered: 'Email d\u00e9j\u00e0 utilis\u00e9. Connecte-toi plut\u00f4t.',
        weak_password: 'Mot de passe trop faible \u2014 6 caract\u00e8res minimum.',
        rate_limit: 'Trop de tentatives \u2014 r\u00e9essaye dans une minute.',
        network: 'Erreur r\u00e9seau \u2014 v\u00e9rifie ta connexion.',
        generic: 'Une erreur est survenue. R\u00e9essaye.'
      },
      es: {
        invalid_credentials: 'Email o contrase\u00f1a incorrectos.',
        email_not_confirmed: 'Confirma tu email primero \u2014 revisa tu bandeja.',
        user_already_registered: 'Este email ya est\u00e1 registrado. Inicia sesi\u00f3n.',
        weak_password: 'Contrase\u00f1a muy d\u00e9bil \u2014 6 caracteres m\u00ednimo.',
        rate_limit: 'Demasiados intentos \u2014 espera un minuto.',
        network: 'Error de red \u2014 revisa tu conexi\u00f3n.',
        generic: 'Algo sali\u00f3 mal. Int\u00e9ntalo de nuevo.'
      }
    };
    var L = ERR[LANG] || ERR.en;
    if (msg.indexOf('invalid login credentials') !== -1 || msg.indexOf('invalid_credentials') !== -1) return L.invalid_credentials;
    if (msg.indexOf('email not confirmed') !== -1) return L.email_not_confirmed;
    if (msg.indexOf('already registered') !== -1 || msg.indexOf('already exists') !== -1 || msg.indexOf('user_already_exists') !== -1) return L.user_already_registered;
    if (msg.indexOf('weak password') !== -1 || msg.indexOf('password should') !== -1) return L.weak_password;
    if (msg.indexOf('rate') !== -1 || msg.indexOf('too many') !== -1) return L.rate_limit;
    if (msg.indexOf('network') !== -1 || msg.indexOf('failed to fetch') !== -1) return L.network;
    return err.message || L.generic;
  }

  function timeAgo(dateStr) {
    var diff = (Date.now() - new Date(dateStr).getTime()) / 1000;
    if (diff < 60) return '<1 min';
    if (diff < 3600) return Math.floor(diff / 60) + ' min';
    if (diff < 86400) return Math.floor(diff / 3600) + 'h';
    if (diff < 2592000) return Math.floor(diff / 86400) + 'd';
    return new Date(dateStr).toLocaleDateString();
  }

  var GOOGLE_SVG = '<svg viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>';

  /* ── Build widget ── */
  var root, authEl, composeEl, postsEl, saveBtn;
  var selectedType = 'temoignage';

  function buildWidget() {
    root = el('div', 'wcc-root');

    /* Header */
    var header = el('div', 'wcc-header');
    header.appendChild(el('h3', 'wcc-title', '\u2726 ' + t.title));
    saveBtn = el('button', 'wcc-save-btn', '\u2661 ' + t.save);
    saveBtn.onclick = toggleSave;
    header.appendChild(saveBtn);
    root.appendChild(header);

    /* Auth */
    authEl = el('div', 'wcc-auth');
    root.appendChild(authEl);

    /* Compose */
    composeEl = el('div', 'wcc-compose');
    var typeBar = el('div', 'wcc-type-bar');
    ['temoignage', 'flash', 'question'].forEach(function (typ) {
      var btn = el('button', 'wcc-type-btn' + (typ === selectedType ? ' wcc-active' : ''), t[typ]);
      btn.dataset.type = typ;
      btn.onclick = function () {
        selectedType = typ;
        typeBar.querySelectorAll('.wcc-type-btn').forEach(function (b) { b.classList.remove('wcc-active'); });
        btn.classList.add('wcc-active');
      };
      typeBar.appendChild(btn);
    });
    composeEl.appendChild(typeBar);

    var textarea = el('textarea', 'wcc-textarea');
    textarea.placeholder = t.placeholder;
    textarea.disabled = true;
    composeEl.appendChild(textarea);

    var footer = el('div', 'wcc-compose-footer');
    var submitBtn = el('button', 'wcc-submit-btn', t.submit);
    submitBtn.disabled = true;
    submitBtn.onclick = function () { submitPost(textarea, submitBtn); };
    footer.appendChild(submitBtn);
    composeEl.appendChild(footer);
    root.appendChild(composeEl);

    /* Posts */
    postsEl = el('div', 'wcc-posts');
    postsEl.appendChild(el('div', 'wcc-loading', '\u2026'));
    root.appendChild(postsEl);

    /* Inject before footer */
    var siteFooter = document.getElementById('siteFooter');
    if (siteFooter) {
      siteFooter.parentNode.insertBefore(root, siteFooter);
    } else {
      document.body.appendChild(root);
    }
  }

  /* ── Auth UI ── */
  function renderAuth() {
    authEl.innerHTML = '';
    if (currentUser) {
      var row = el('div', 'wcc-user-row');
      var av = document.createElement('img');
      av.className = 'wcc-avatar';
      av.src = currentUser.avatar_url || '';
      av.alt = '';
      av.onerror = function(){ this.style.display='none'; };
      row.appendChild(av);
      row.appendChild(el('span', 'wcc-user-name', currentUser.username || currentUser.email));
      var out = el('button', 'wcc-logout-btn', t.logout);
      out.onclick = doLogout;
      row.appendChild(out);
      authEl.appendChild(row);

      var ta = composeEl.querySelector('.wcc-textarea');
      var sb2 = composeEl.querySelector('.wcc-submit-btn');
      ta.disabled = false;
      ta.placeholder = t.placeholder;
      sb2.disabled = false;
    } else {
      authEl.appendChild(buildAuthPanel());

      var ta2 = composeEl.querySelector('.wcc-textarea');
      var sb3 = composeEl.querySelector('.wcc-submit-btn');
      ta2.disabled = true;
      ta2.placeholder = t.loginFirst;
      sb3.disabled = true;
    }
  }

  /* ── Auth panel (Google + email) ── */
  var authMode = 'login'; // 'login' or 'signup'

  function buildAuthPanel() {
    var panel = el('div', 'wcc-auth-panel');

    // Google button
    var gBtn = el('button', 'wcc-google-btn', GOOGLE_SVG + ' ' + t.login);
    gBtn.onclick = doLoginGoogle;
    panel.appendChild(gBtn);

    // Separator
    var sep = el('div', 'wcc-auth-sep');
    sep.innerHTML = '<span>' + (LANG === 'fr' ? 'ou' : LANG === 'es' ? 'o' : 'or') + '</span>';
    panel.appendChild(sep);

    // Email form
    var form = el('div', 'wcc-auth-form');
    var emailInput = document.createElement('input');
    emailInput.type = 'email';
    emailInput.className = 'wcc-input';
    emailInput.placeholder = 'Email';
    emailInput.autocomplete = 'email';
    form.appendChild(emailInput);

    var pwInput = document.createElement('input');
    pwInput.type = 'password';
    pwInput.className = 'wcc-input';
    pwInput.placeholder = LANG === 'fr' ? 'Mot de passe' : LANG === 'es' ? 'Contraseña' : 'Password';
    pwInput.autocomplete = 'current-password';
    form.appendChild(pwInput);

    var errEl = el('div', 'wcc-auth-error');
    form.appendChild(errEl);

    var submitRow = el('div', 'wcc-auth-submit-row');
    var submitLabel = authMode === 'signup'
      ? (LANG === 'fr' ? 'Créer un compte' : LANG === 'es' ? 'Crear cuenta' : 'Create account')
      : (LANG === 'fr' ? 'Connexion' : LANG === 'es' ? 'Iniciar sesión' : 'Sign in');
    var submitBtn = el('button', 'wcc-submit-btn', submitLabel);
    submitBtn.onclick = function () {
      var email = emailInput.value.trim();
      var pw = pwInput.value;
      errEl.textContent = '';
      if (!email || !pw) { errEl.textContent = LANG === 'fr' ? 'Remplis tous les champs' : 'Fill all fields'; return; }
      if (pw.length < 6) { errEl.textContent = LANG === 'fr' ? '6 caractères minimum' : 'Min 6 characters'; return; }
      submitBtn.disabled = true;
      submitBtn.textContent = '…';
      if (authMode === 'signup') {
        doSignupEmail(email, pw, errEl, submitBtn);
      } else {
        doLoginEmail(email, pw, errEl, submitBtn);
      }
    };
    submitRow.appendChild(submitBtn);
    form.appendChild(submitRow);

    // Toggle link
    var toggleRow = el('div', 'wcc-auth-toggle');
    if (authMode === 'login') {
      toggleRow.innerHTML = (LANG === 'fr' ? 'Pas encore de compte ? ' : LANG === 'es' ? '¿Sin cuenta? ' : 'No account? ');
      var toggleLink = el('a', 'wcc-auth-toggle-link', LANG === 'fr' ? 'Créer un compte' : LANG === 'es' ? 'Crear cuenta' : 'Create account');
      toggleLink.href = '#';
      toggleLink.onclick = function (e) { e.preventDefault(); authMode = 'signup'; renderAuth(); };
      toggleRow.appendChild(toggleLink);
    } else {
      toggleRow.innerHTML = (LANG === 'fr' ? 'Déjà un compte ? ' : LANG === 'es' ? '¿Ya tienes cuenta? ' : 'Already have an account? ');
      var toggleLink2 = el('a', 'wcc-auth-toggle-link', LANG === 'fr' ? 'Se connecter' : LANG === 'es' ? 'Iniciar sesión' : 'Sign in');
      toggleLink2.href = '#';
      toggleLink2.onclick = function (e) { e.preventDefault(); authMode = 'login'; renderAuth(); };
      toggleRow.appendChild(toggleLink2);
    }
    form.appendChild(toggleRow);

    panel.appendChild(form);
    return panel;
  }

  function doLoginGoogle() {
    sb.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: window.location.href }
    });
  }

  function doLoginEmail(email, pw, errEl, btn) {
    sb.auth.signInWithPassword({ email: email, password: pw }).then(function (res) {
      btn.disabled = false;
      btn.textContent = LANG === 'fr' ? 'Connexion' : LANG === 'es' ? 'Iniciar sesión' : 'Sign in';
      if (res.error) {
        errEl.textContent = friendlyError(res.error);
        return;
      }
      // Session set by onAuthStateChange
    });
  }

  function doSignupEmail(email, pw, errEl, btn) {
    sb.auth.signUp({
      email: email,
      password: pw,
      options: { emailRedirectTo: window.location.origin + '/onboarding.html' }
    }).then(function (res) {
      btn.disabled = false;
      btn.textContent = LANG === 'fr' ? 'Créer un compte' : LANG === 'es' ? 'Crear cuenta' : 'Create account';
      if (res.error) {
        errEl.textContent = friendlyError(res.error);
        return;
      }
      // Check if email confirmation is required (no identities = already exists)
      if (res.data.user && res.data.user.identities && res.data.user.identities.length === 0) {
        errEl.textContent = LANG === 'fr' ? 'Email d\u00e9j\u00e0 utilis\u00e9. Connecte-toi plut\u00f4t.' : LANG === 'es' ? 'Email ya registrado. Inicia sesi\u00f3n.' : 'Email already registered. Sign in instead.';
        return;
      }
      // If session exists (no email confirm), redirect to onboarding
      if (res.data.session) {
        window.location.href = '/onboarding.html?from=' + encodeURIComponent(window.location.href);
      } else {
        errEl.style.color = '#1a5430';
        errEl.textContent = LANG === 'fr' ? '\u2713 V\u00e9rifie ta bo\u00eete mail pour confirmer ton compte.' : LANG === 'es' ? '\u2713 Revisa tu bandeja para confirmar tu cuenta.' : '\u2713 Check your inbox to confirm your account.';
      }
    });
  }

  function doLogout() {
    sb.auth.signOut().then(function () {
      currentUser = null;
      renderAuth();
    });
  }

  /* ── Save page ── */
  function checkSaved() {
    if (!currentUser) {
      var local = JSON.parse(localStorage.getItem('wcc_saved') || '[]');
      if (local.indexOf(SLUG) !== -1) {
        saveBtn.classList.add('wcc-saved');
        saveBtn.innerHTML = '\u2665 ' + t.saved;
      }
      return;
    }
    sb.from('saved_cities').select('id').eq('user_id', currentUser.id).eq('slug', SLUG).then(function (res) {
      if (res.data && res.data.length > 0) {
        saveBtn.classList.add('wcc-saved');
        saveBtn.innerHTML = '\u2665 ' + t.saved;
        saveBtn.dataset.savedId = res.data[0].id;
      }
    });
  }

  function toggleSave() {
    if (!currentUser) {
      var local = JSON.parse(localStorage.getItem('wcc_saved') || '[]');
      var idx = local.indexOf(SLUG);
      if (idx === -1) {
        local.push(SLUG);
        saveBtn.classList.add('wcc-saved');
        saveBtn.innerHTML = '\u2665 ' + t.saved;
      } else {
        local.splice(idx, 1);
        saveBtn.classList.remove('wcc-saved');
        saveBtn.innerHTML = '\u2661 ' + t.save;
      }
      localStorage.setItem('wcc_saved', JSON.stringify(local));
      return;
    }

    if (saveBtn.classList.contains('wcc-saved')) {
      var sid = saveBtn.dataset.savedId;
      if (sid) sb.from('saved_cities').delete().eq('id', sid).then(function () {});
      saveBtn.classList.remove('wcc-saved');
      saveBtn.innerHTML = '\u2661 ' + t.save;
      delete saveBtn.dataset.savedId;
    } else {
      sb.from('saved_cities').insert({ user_id: currentUser.id, slug: SLUG }).select().then(function (res) {
        saveBtn.classList.add('wcc-saved');
        saveBtn.innerHTML = '\u2665 ' + t.saved;
        if (res.data && res.data[0]) saveBtn.dataset.savedId = res.data[0].id;
      });
    }
  }

  /* ── Load posts ── */
  function loadPosts() {
    postsEl.innerHTML = '<div class="wcc-loading">\u2026</div>';
    console.log('[wcc] loading posts for slug:', SLUG);
    sb.from('posts')
      .select('*, profiles(username, avatar_url)')
      .eq('slug', SLUG)
      .order('useful_count', { ascending: false })
      .order('created_at', { ascending: false })
      .then(function (res) {
        console.log('[wcc] posts result:', res.error || (res.data ? res.data.length + ' posts' : 'null'));
        postsEl.innerHTML = '';
        if (res.error) {
          console.error('[wcc] loadPosts error', res.error);
          postsEl.appendChild(el('div', 'wcc-empty', 'Error loading posts'));
          return;
        }
        if (!res.data || res.data.length === 0) {
          postsEl.appendChild(el('div', 'wcc-empty', t.empty));
          return;
        }
        // Load user votes if logged in
        if (currentUser) {
          var postIds = res.data.map(function (p) { return p.id; });
          sb.from('useful_votes').select('post_id').eq('user_id', currentUser.id).in('post_id', postIds)
            .then(function (vRes) {
              var voted = {};
              if (vRes.data) vRes.data.forEach(function (v) { voted[v.post_id] = true; });
              res.data.forEach(function (post) { renderPost(post, voted[post.id]); });
            });
        } else {
          res.data.forEach(function (post) { renderPost(post, false); });
        }
      });
  }

  function renderPost(post, hasVoted) {
    var isPinned = (post.useful_count || 0) >= PINNED_THRESHOLD;
    var card = el('div', 'wcc-post' + (isPinned ? ' wcc-pinned' : ''));

    var head = el('div', 'wcc-post-head');
    var profile = post.profiles || {};
    var av = document.createElement('img');
    av.className = 'wcc-post-avatar';
    av.src = profile.avatar_url || '';
    av.alt = '';
    head.appendChild(av);
    head.appendChild(el('span', 'wcc-post-author', profile.username || 'Anon'));
    var badge = el('span', 'wcc-post-type', t[post.type] || post.type);
    badge.dataset.type = post.type;
    head.appendChild(badge);
    if (isPinned) {
      head.appendChild(el('span', 'wcc-post-pinned-badge', '\u2726 ' + t.pinned));
    }
    head.appendChild(el('span', 'wcc-post-date', timeAgo(post.created_at)));
    card.appendChild(head);

    card.appendChild(el('div', 'wcc-post-body', escapeHtml(post.content)));

    var foot = el('div', 'wcc-post-foot');
    var voteBtn = el('button', 'wcc-vote-btn' + (hasVoted ? ' wcc-voted' : ''), '\u2726 ' + t.useful + ' <strong>' + (post.useful_count || 0) + '</strong>');
    if (!currentUser) voteBtn.disabled = true;
    if (hasVoted) voteBtn.disabled = true;
    voteBtn.onclick = function () { doVote(post.id, voteBtn); };
    foot.appendChild(voteBtn);
    card.appendChild(foot);

    postsEl.appendChild(card);
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>');
  }

  /* ── Vote ── */
  function doVote(postId, btn) {
    if (!currentUser) return;
    btn.disabled = true;
    sb.from('useful_votes').insert({ post_id: postId, user_id: currentUser.id }).then(function (res) {
      if (res.error) return;
      btn.classList.add('wcc-voted');
      // Increment count in posts table
      sb.rpc('increment_useful', { row_id: postId }).then(function () {
        loadPosts();
      });
    });
  }

  /* ── Submit post ── */
  function submitPost(textarea, submitBtn) {
    console.log('[wcc] submitPost called', { body: textarea.value.trim(), user: currentUser, slug: SLUG, type: selectedType });
    var body = textarea.value.trim();
    if (!body) { console.warn('[wcc] empty body'); return; }
    if (!currentUser) { console.warn('[wcc] no user session'); return; }
    submitBtn.disabled = true;
    submitBtn.textContent = '…';

    var payload = {
      slug: SLUG,
      user_id: currentUser.id,
      type: selectedType,
      content: body,
      useful_count: 0
    };
    console.log('[wcc] inserting post', payload);

    sb.from('posts').insert(payload).then(function (res) {
      console.log('[wcc] insert result', res);
      submitBtn.disabled = false;
      submitBtn.textContent = t.submit;
      if (res.error) {
        console.error('[wcc] post error', res.error);
        // Inline error feedback
        var existingErr = composeEl.querySelector('.wcc-post-error');
        if (existingErr) existingErr.remove();
        var errBox = el('div', 'wcc-post-error');
        errBox.style.cssText = 'padding:8px 12px;margin:0 12px 8px;font-size:12px;color:#c0392b;background:#fef2f2;border:1px solid #fecaca;border-radius:2px';
        errBox.textContent = friendlyError(res.error);
        composeEl.querySelector('.wcc-compose-footer').parentNode.insertBefore(errBox, composeEl.querySelector('.wcc-compose-footer'));
        setTimeout(function(){ if (errBox.parentNode) errBox.remove(); }, 5000);
        return;
      }
      textarea.value = '';
      loadPosts();
    });
  }

  /* ── Upsert profile (only if not exists — don't overwrite onboarding data) ── */
  function upsertProfile(user) {
    var meta = user.user_metadata || {};
    var uid = user.id;
    // Check if profile already exists
    sb.from('profiles').select('id').eq('id', uid).then(function (res) {
      if (res.data && res.data.length > 0) return; // profile exists, don't overwrite
      // First login — create minimal profile
      sb.from('profiles').insert({
        id: uid,
        username: meta.full_name || meta.name || user.email.split('@')[0],
        avatar_url: meta.avatar_url || meta.picture || '',
        onboarding_done: false
      }).then(function (r) {
        if (r.error && r.error.code !== '23505') { // ignore duplicate key
          console.error('[wcc] profile insert error', r.error);
        }
      });
    });
  }

  /* ── Set user from session (loads username/avatar from profiles table) ── */
  function setUser(session, onReady) {
    if (session && session.user) {
      var u = session.user;
      var meta = u.user_metadata || {};
      // Optimistic — use auth metadata first
      currentUser = {
        id: u.id,
        email: u.email,
        username: meta.full_name || meta.name || u.email.split('@')[0],
        avatar_url: meta.avatar_url || meta.picture || ''
      };
      console.log('[wcc] user set (optimistic):', currentUser.username, currentUser.id);
      // Then load from profiles table to get the canonical username
      sb.from('profiles').select('username,avatar_url').eq('id', u.id).maybeSingle().then(function (res) {
        if (res.data) {
          if (res.data.username) currentUser.username = res.data.username;
          if (res.data.avatar_url) currentUser.avatar_url = res.data.avatar_url;
          console.log('[wcc] user upgraded from profile:', currentUser.username);
        } else {
          // Profile doesn't exist — create it
          upsertProfile(u);
        }
        if (onReady) onReady();
      });
    } else {
      currentUser = null;
      console.log('[wcc] no session');
      if (onReady) onReady();
    }
  }

  /* ── Boot ── */
  function boot() {
    buildWidget();

    initSupabase(function () {
      var hasOAuthHash = window.location.hash && window.location.hash.includes('access_token');

      sb.auth.getSession().then(function (res) {
        console.log('[wcc] getSession result:', res.data.session ? 'active' : 'none');
        setUser(res.data.session, function () {
          renderAuth();
          checkSaved();
          loadPosts();
          if (hasOAuthHash && res.data.session) {
            history.replaceState(null, '', window.location.pathname + window.location.search);
          }
        });
      });

      sb.auth.onAuthStateChange(function (event, session) {
        console.log('[wcc] auth state changed:', event);
        setUser(session, function () {
          renderAuth();
          checkSaved();
          loadPosts();
        });
      });
    });
  }

  /* ── Wait for DOM ── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
