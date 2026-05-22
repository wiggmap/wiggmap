# SPRINT_Z_REDUCED_PLAN — Connect T1 finalisation (Z.0 + Z.1 only)

> **Date** : 2026-05-05
> **Mode** : audit + plan. Aucun fichier modifié dans cette phase.
> **Scope confirmé** : seulement Z.0 (Supabase schema extension + Storage) + Z.1 (brancher /connect/* sur Supabase). Z.2 (feed read), Z.3 (post-create), Z.4 (groups) reportés à un sprint ultérieur "quand 20-50 users réels".

---

## 0. TL;DR

**Bonne nouvelle** : tout l'infra Supabase existe déjà.
- `SUPABASE_SETUP.sql` à la racine = table `profiles` + trigger auto-create + RLS policies
- `/onboarding.html` racine + `/mon-compte.html` = pattern auth complet wired sur Supabase
- `connect/widget.js` = pattern lazy-load Supabase + auth state listener

**Ce qu'il manque (Z.0)** : extension schema pour les champs spécifiques Connect (bio, member_type, country_targets array, display_name, city, langues avec niveau) + Storage bucket avatars.

**Ce qu'il manque (Z.1)** : brancher 3 fichiers `/connect/onboarding.html`, `/connect/profile.html`, `/connect/index.html` en remplaçant le `localStorage.wigg_connect_profile` par UPSERT/SELECT Supabase, en réutilisant les patterns existants.

**Estimation totale** : ~10-13h dev + ~30 min Flo (apply SQL + créer Storage bucket).

---

## 1. État réel des assets Supabase

### 1.1 Supabase déjà configuré

| Composant | État | Source |
|---|---|---|
| Project URL | `https://tkctreoftezvbfejhbto.supabase.co` | dur dans 4+ fichiers |
| Public anon key | `sb_publishable_lAKWBnp2nbfgb2w5Uj55aQ_aD6fBWUb` | dur dans 4+ fichiers |
| Table `profiles` | ✅ existe (10 colonnes) | SUPABASE_SETUP.sql |
| Trigger `handle_new_user` | ✅ auto-create profile à signup | idem |
| Backfill orphan profiles | ✅ INSERT pour auth.users sans profile | idem |
| RLS sur profiles | ✅ select all + insert own + update own | idem |
| Auth Google OAuth | ✅ wired sur /onboarding.html racine + /mon-compte.html + connect/widget.js | code |
| Auth email/password | ✅ idem | idem |
| Table `posts` | ✅ existe (utilisée par connect/widget.js chronicles comments) | inferred from `increment_useful` RPC + widget.js queries |
| Storage bucket | ⚠️ à confirmer (pas vu de référence dans le code racine) | inconnu |

### 1.2 Schema actuel `profiles`

```sql
profiles (
  id              UUID         -- references auth.users
  username        TEXT
  avatar_url      TEXT
  country_origin  TEXT         -- slug WiggMap (singular)
  country_current TEXT         -- slug WiggMap
  country_target  TEXT         -- ⚠️ SINGULAR — needs to become array for Connect
  life_status     TEXT
  sector          TEXT
  languages       JSONB        -- format actuel = []
  onboarding_done BOOLEAN
  created_at      TIMESTAMPTZ
)
```

### 1.3 Schema cible (per vision §171 + Connect onboarding mockup)

Extensions requises :
- `display_name TEXT` — séparé de `username` (username = handle unique, display_name = nom affiché)
- `bio TEXT` — max 200 chars (vision §99 dit "max 200 chars" mais Connect mockup dit "160 car.")
- `member_type TEXT` — `individu` / `commerce` / `association`
- `country_targets TEXT[]` — array de slugs (vision §94 "1 à 3"). Garder `country_target` singular pour back-compat avec /onboarding.html legacy.
- `city_origin TEXT`, `city_current TEXT`, `city_target TEXT` — Connect mockup demande ville + pays
- `quarter TEXT` — "départ prévu" (e.g. "Q3 2026")
- `duration TEXT` — "depuis combien de temps" (e.g. "6 mois")
- `languages JSONB` — déjà existe, format à préciser : `[{lang:'fr', level:5}, ...]` (vision §97 dit niveau 1-5)

### 1.4 Pages /connect/ à brancher

| Fichier | État actuel | Z.1 action |
|---|---|---|
| `connect/index.html` (588 lignes) | Landing avec liens vers `/connect/onboarding.html` | Ajouter check session → redirect intelligent (auth + onboarding_done → /connect/profile.html, sinon → /connect/onboarding.html) |
| `connect/onboarding.html` (1538 lignes) | Mockup, persiste tout dans `localStorage.wigg_connect_profile` | Brancher Auth Google/email + UPSERT profile en Supabase. Garder localStorage comme cache rapide. |
| `connect/profile.html` (966 lignes) | Render depuis `localStorage.wigg_profile` | SELECT profile WHERE id=auth.uid() OR username=$param. Si pas auth → redirect onboarding. Garder localStorage fallback offline. |
| `connect/feed.html`, `group.html`, `swipe.html` | Mockups + prototypes — **HORS SCOPE Z.1** | reportés Z.2-Z.4 |

---

## 2. Plan d'exécution

### Lot Z.0 — Schema extension SQL + Storage + doc (~3h dev + Flo apply)

#### Z.0.1 — Étendre `SUPABASE_SETUP.sql`

Ajouter au fichier existant (ALTER TABLE IF NOT EXISTS pattern, idempotent) :

```sql
-- Sprint Z.0 additions for Connect T1 finalization

ALTER TABLE profiles ADD COLUMN IF NOT EXISTS display_name   TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS bio            TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS member_type    TEXT DEFAULT 'individu';
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS country_targets TEXT[] DEFAULT ARRAY[]::TEXT[];
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS city_origin    TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS city_current   TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS city_target    TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS quarter        TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS duration       TEXT;

-- Constraint: bio max 200 chars (vision §99)
ALTER TABLE profiles DROP CONSTRAINT IF EXISTS profiles_bio_length;
ALTER TABLE profiles ADD CONSTRAINT profiles_bio_length CHECK (bio IS NULL OR length(bio) <= 200);

-- Constraint: member_type whitelist
ALTER TABLE profiles DROP CONSTRAINT IF EXISTS profiles_member_type_chk;
ALTER TABLE profiles ADD CONSTRAINT profiles_member_type_chk
  CHECK (member_type IN ('individu', 'commerce', 'association'));

-- Constraint: country_targets max 3 entries (vision §94)
ALTER TABLE profiles DROP CONSTRAINT IF EXISTS profiles_country_targets_max3;
ALTER TABLE profiles ADD CONSTRAINT profiles_country_targets_max3
  CHECK (array_length(country_targets, 1) IS NULL OR array_length(country_targets, 1) <= 3);

-- Index for public profile fetch by username
CREATE UNIQUE INDEX IF NOT EXISTS profiles_username_uniq ON profiles (username) WHERE username IS NOT NULL;

-- Backfill: copy country_target → country_targets array for existing rows
UPDATE profiles
SET country_targets = ARRAY[country_target]
WHERE country_target IS NOT NULL AND (country_targets IS NULL OR array_length(country_targets, 1) IS NULL);
```

#### Z.0.2 — Storage bucket `avatars`

```sql
-- Storage bucket (run in Supabase dashboard → Storage → create bucket)
-- name: avatars
-- public: true (read access via public URL)

-- RLS policies (Supabase dashboard → Storage → Policies):
-- 1. SELECT: anyone can read (public)
-- 2. INSERT: authenticated user can upload to /{user_id}/* path
-- 3. UPDATE: authenticated user can replace own /{user_id}/* objects
-- 4. DELETE: authenticated user can delete own /{user_id}/* objects

-- (Storage bucket creation + policies must be applied via Supabase dashboard
-- UI, not SQL — Storage is a separate concern from the auth schema.)
```

Documenté dans `project-brain/connect-supabase-schema.md` (à créer en Z.0.3).

#### Z.0.3 — Documentation `project-brain/connect-supabase-schema.md`

Spec complète : tables, colonnes, RLS, Storage, queries types pour Z.1+ (UPSERT profile, SELECT by id, SELECT by username, upload avatar, etc.).

#### Z.0.4 — Pas de touche prod par moi

Flo applique :
- `SUPABASE_SETUP.sql` mis à jour dans Supabase SQL Editor (idempotent — IF NOT EXISTS partout)
- Crée le bucket `avatars` via Supabase dashboard Storage
- Configure les 4 policies RLS via Supabase dashboard

**Validation Z.0** :
- Schema check : Flo run `\d profiles` dans psql ou Supabase SQL editor pour confirmer les colonnes
- RLS check : depuis JS console sur prod, `await sb.from('profiles').select('*').limit(1)` doit retourner data si logged-in, [] si anonyme
- Storage check : Flo upload manuel d'une image test puis `select('avatar_url').eq('id', user_id)` confirme la URL

### Lot Z.1 — Brancher /connect/onboarding/profile/index sur Supabase (~7-10h dev)

#### Z.1.1 — Centralisation `data/connect-config.js` (~1h)

Nouveau fichier à créer :

```js
// data/connect-config.js — single source for Supabase config + lazy client.
// Loaded by /onboarding.html, /mon-compte.html, /connect/{onboarding,profile,index}.html.
// Replaces 4+ hardcoded SUPABASE_URL/KEY duplications.
(function () {
  if (window.WMC) return; // idempotent

  const SUPABASE_URL = 'https://tkctreoftezvbfejhbto.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_lAKWBnp2nbfgb2w5Uj55aQ_aD6fBWUb';

  let _sb = null;
  let _loadingPromise = null;

  function loadSupabase() {
    if (window.supabase) return Promise.resolve();
    if (_loadingPromise) return _loadingPromise;
    _loadingPromise = new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js';
      s.onload = resolve;
      s.onerror = () => reject(new Error('Supabase JS failed to load'));
      document.head.appendChild(s);
    });
    return _loadingPromise;
  }

  async function getSb() {
    if (_sb) return _sb;
    await loadSupabase();
    _sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY, {
      auth: { detectSessionInUrl: true, persistSession: true },
    });
    return _sb;
  }

  async function getSession() {
    const sb = await getSb();
    const { data: { session } } = await sb.auth.getSession();
    return session;
  }

  async function getProfile(opts) {
    // opts: { id?, username? } — fetch by id (default = current auth user) or username
    const sb = await getSb();
    let userId = opts && opts.id;
    if (!userId && !(opts && opts.username)) {
      const session = await getSession();
      userId = session && session.user.id;
      if (!userId) return null;
    }
    let q = sb.from('profiles').select('*');
    if (opts && opts.username) q = q.eq('username', opts.username);
    else q = q.eq('id', userId);
    const { data, error } = await q.maybeSingle();
    if (error) { console.error('[wmc] getProfile', error); return null; }
    return data;
  }

  async function upsertProfile(patch) {
    const sb = await getSb();
    const session = await getSession();
    if (!session) throw new Error('Not authenticated');
    const row = { id: session.user.id, ...patch, updated_at: new Date().toISOString() };
    const { data, error } = await sb.from('profiles').upsert(row).select().single();
    if (error) throw error;
    return data;
  }

  async function uploadAvatar(file) {
    const sb = await getSb();
    const session = await getSession();
    if (!session) throw new Error('Not authenticated');
    const ext = (file.name || 'png').split('.').pop().toLowerCase();
    const path = `${session.user.id}/avatar.${ext}`;
    const { error } = await sb.storage.from('avatars').upload(path, file, { upsert: true, cacheControl: '3600' });
    if (error) throw error;
    const { data: { publicUrl } } = sb.storage.from('avatars').getPublicUrl(path);
    return publicUrl;
  }

  async function signOut() {
    const sb = await getSb();
    await sb.auth.signOut();
  }

  // Public API
  window.WMC = {
    getSb, getSession, getProfile, upsertProfile, uploadAvatar, signOut,
    SUPABASE_URL, SUPABASE_KEY,
  };
})();
```

#### Z.1.2 — Patch `connect/index.html` (~30 min)

Ajouter au `<head>` (avant `</head>`) :
```html
<script src="/data/connect-config.js"></script>
```

Ajouter au bas du `<body>` :
```html
<script>
(async function() {
  const session = await WMC.getSession();
  if (!session) return; // not auth → stay on landing
  const profile = await WMC.getProfile();
  if (profile && profile.onboarding_done) {
    window.location.replace('/connect/profile.html');
  } else {
    window.location.replace('/connect/onboarding.html');
  }
})();
</script>
```

→ Les 2 CTAs "Create profile" / "Login" pointent déjà vers `/connect/onboarding.html` qui gère les deux cas. Pas de changement nécessaire sur le HTML existant.

#### Z.1.3 — Patch `connect/onboarding.html` (~3-4h)

Plus gros changement. Strategy : **garder le mockup HTML existant** (toute l'UX, les 5 steps, le multi-language), **ajouter** la couche auth + persistence Supabase :

1. Ajouter `<script src="/data/connect-config.js">` en `<head>`
2. Au load : `await WMC.getSession()`. Si pas auth → afficher écran "login required" (réutiliser pattern de /onboarding.html racine ligne ~250 — Google OAuth + email/password tabs).
3. Si auth + profile.onboarding_done → redirect `/connect/profile.html`.
4. Si auth + pas onboarding_done → load any partial localStorage cache, fill the form fields, let user complete.
5. Sur "submit" final : `await WMC.upsertProfile({ display_name, bio, member_type, country_origin, city_origin, country_current, city_current, country_targets, city_target, quarter, duration, life_status, sector, languages, avatar_url, onboarding_done: true })`.
6. Sur upload avatar : `await WMC.uploadAvatar(file)` → save returned URL en `avatar_url`.
7. Garder le `localStorage.setItem('wigg_connect_profile', JSON.stringify(...))` comme cache offline (résilience si Supabase down).
8. Sur succès final → redirect `/connect/profile.html`.

Validations client (à faire avant UPSERT) :
- bio.length <= 200
- country_targets.length <= 3
- member_type in ['individu', 'commerce', 'association']
- username unique check (avant submit, query `select id from profiles where username = X`)

#### Z.1.4 — Patch `connect/profile.html` (~2h)

1. Ajouter `<script src="/data/connect-config.js">`
2. Au load :
   - Lire `?username=X` du URL (ou `?id=Y`)
   - Si paramètre → `WMC.getProfile({ username: X })` (autre profil, public)
   - Sinon → `WMC.getProfile()` (own profile via session)
3. Si pas de profile → redirect `/connect/onboarding.html`
4. Render avec les vraies données Supabase (au lieu de `localStorage.wigg_profile`)
5. Garder le localStorage en cache rapide : on lit d'abord du cache, on render, puis on fetch Supabase et on update silencieusement.
6. Bouton "Edit profile" → redirige `/connect/onboarding.html` (qui détectera profile existant et pré-remplira).
7. Bouton "Sign out" → `await WMC.signOut()` puis redirect `/connect/`.

#### Z.1.5 — Quick wins en passant (sans dérive)

- **Centralisation clés Supabase** : `/onboarding.html` racine, `/mon-compte.html`, `connect/widget.js`, `data/header.js` continuent d'avoir leurs clés en dur. Documenter qu'on pourrait les migrer vers `connect-config.js` mais ne PAS le faire dans ce PR (touche 4 fichiers déjà prod-stables, risque pour zéro gain immédiat).
- **`connect/assets/connect.js` `WC.getProfile/saveProfile`** : actuellement localStorage-only. Le marquer `@deprecated — use window.WMC.* instead` en commentaire.
- **Nothing else** — strict scope limit.

#### Z.1.6 — Tests Flo

Manuel sur preview Netlify (PR à créer) :
1. Visiter `/connect/` → voir landing
2. Cliquer "Create profile" → arrive sur `/connect/onboarding.html`
3. Login Google → continue onboarding
4. Compléter les 5 steps → submit
5. Arrive sur `/connect/profile.html` avec son profil
6. Sign out → revient à `/connect/`
7. Re-login → arrive direct sur `/connect/profile.html` (skip onboarding car onboarding_done=true)
8. Edit profile → modifie bio → re-submit → bio persisté
9. Visiter `/connect/profile.html?username=floob` (autre user) → voir ce profil public
10. Sur Supabase dashboard → confirm la row dans `profiles` avec tous les champs

---

## 3. Risques (réduits vu le scope)

### R1 — Schema migration sur prod Supabase

Z.0 = ALTER TABLE sur table prod. Si une colonne déjà existe avec un type différent → migration échoue. Mitigation : `IF NOT EXISTS` partout (idempotent), tester en Supabase SQL Editor avant.

### R2 — Backfill `country_targets`

L'UPDATE qui copie `country_target` → `country_targets` array touche les rows existantes. Mitigation : la query est WHERE-bounded (`WHERE country_target IS NOT NULL AND country_targets IS NULL OR empty`), donc idempotente. Mais à monitorer après run.

### R3 — Storage bucket public read

Bucket `avatars` public means tous les avatars sont publiquement accessibles via URL stable. **Voulu** (per vision §61, profils publics). Pas de risque RGPD spécifique tant qu'on ne stocke que des avatars (pas de docs perso).

### R4 — Connect onboarding bug = casse soft launch

Si Z.1 introduit un bug dans `/connect/onboarding.html`, tous les nouveaux signups sur Connect sont bloqués. **Mitigation** : tests Flo serrés (Z.1.6 checklist 10 points) sur preview Netlify avant merge sur main.

### R5 — Conflit avec `/onboarding.html` racine

Le legacy `/onboarding.html` racine reste actif et écrit dans la même table `profiles`. Si un user crée un profile via legacy puis visite Connect → données partielles (display_name, bio, etc. à null). Pas de conflit data-wise (juste UI feature gap). Acceptable pendant soft launch.

---

## 4. Décisions résiduelles

Toutes les décisions D1-D7 sont arbitrées. Quelques sous-points fins à confirmer pendant exec si pas évidents :

- **Bio max length** : vision §99 dit 200 chars, Connect mockup dit "160 car." — j'utilise **200** (plus permissif, peut toujours réduire en UI). Confirme ?
- **Member type "commerce" / "association"** : vision §100 inclut ces 2 types en plus de "individu". Connect mockup montre "Individu" + "Commerce" + "Association" cards. → garde les 3, default "individu".
- **Avatar fallback** : si user n'upload pas, utilise sa Google `picture` (déjà géré par trigger `handle_new_user`). Connect onboarding peut écraser via upload manual.
- **Username uniqueness check** : `before submit, query` pour voir si username déjà pris. Si oui → error message "username taken". Acceptable ?

---

## 5. Estimation totale Sprint Z (réduit)

| Lot | Description | Effort dev | Effort Flo |
|---|---|---|---|
| Z.0.1 | SQL migration extension | 1h | 5 min apply |
| Z.0.2 | Storage bucket + RLS doc | 30 min | 10 min apply (UI) |
| Z.0.3 | `project-brain/connect-supabase-schema.md` | 30 min | 0 |
| Z.1.1 | `data/connect-config.js` | 1h | 0 |
| Z.1.2 | Patch `connect/index.html` | 30 min | 0 |
| Z.1.3 | Patch `connect/onboarding.html` (gros) | 3-4h | 0 |
| Z.1.4 | Patch `connect/profile.html` | 2h | 0 |
| Z.1.5 | Comments + doc deprecated | 15 min | 0 |
| Z.1.6 | Tests preview manuel | 0 | 30 min |
| **Total** | **2 PRs** (Z.0 + Z.1) | **~9-12h dev** | **~45 min Flo** |

---

## 6. Plan d'exécution

### PR #16 — Z.0 (sprint-Z0-supabase-schema)
1. Étendre `SUPABASE_SETUP.sql` (Z.0.1)
2. Créer `project-brain/connect-supabase-schema.md` (Z.0.2 + Z.0.3 doc)
3. Push branche, ouvrir PR
4. **STOP** — j'attends Flo apply le SQL + crée le bucket Storage + confirme via console JS que ça marche

### PR #17 — Z.1 (sprint-Z1-connect-supabase) — démarre après validation Z.0 par Flo
1. Créer `data/connect-config.js` (Z.1.1)
2. Patch `connect/index.html` (Z.1.2)
3. Patch `connect/onboarding.html` (Z.1.3)
4. Patch `connect/profile.html` (Z.1.4)
5. Push branche, ouvrir PR, deploy preview
6. **STOP** — Flo teste les 10 points checklist Z.1.6 sur preview
7. Si tout OK → merge sur main
8. Monitor T+0 prod (vérifier que `/connect/onboarding.html` retourne 200 avec script connect-config.js chargé)

---

## 7. Confirmation avant exec

Réponds-moi (1-2 lignes) sur :

1. **Bio max length** : 200 (vision) ou 160 (Connect mockup) ?
2. **Username unique check** : OK pour query before submit ?
3. **Storage bucket name** : `avatars` (proposé) ou autre ?
4. **OK pour démarrer Z.0 maintenant + STOP avant Z.1** (en attendant ton apply SQL Supabase) ?

Si "go défauts" → je démarre Z.0 immédiatement avec : bio 200 chars, username unique check, bucket "avatars", STOP après Z.0 pour ton apply.

---

*Plan rédigé le 2026-05-05. Aucun fichier source modifié dans cette phase.*
