# MIGRATION_PLAN — Trilingue racine (`/fr/`, `/en/`, `/es/`)

> **Sprint cible** : Sprint 2 du AUDIT.md, item 1.1 (impact 10, effort 6, ratio 1.67) — résolution du trou noir SEO racine.
> **Mode** : audit + plan. Aucun fichier modifié dans cette phase.
> **Date** : 2026-05-03.

---

## 0. TL;DR

Aujourd'hui les pages racine (`/index.html`, `/about.html`, etc.) sont servies sur une URL unique avec contenu swappé en JS via `localStorage.wigg_lang`. Conséquence : Google n'indexe qu'une seule version par URL → trafic FR + ES quasi nul depuis la racine.

**Cible** : 3 dossiers `/en/`, `/fr/`, `/es/` qui hébergent les variantes statiques des pages racine. `/` redirige 301 vers `/en/` (default langue de référence). Les pages déjà trilingues par filename (`countries/*-{lang}.html`, `chronicles/*-{lang}.html`, `lp/*-{lang}.html`, `lead-magnet/*-{lang}.html`, `compare/static/*`) **restent inchangées** — leur slug porte déjà la langue.

**Estimation** : ~14 commits, 18–24 h dev cumulé. Exécution sur branche dédiée + Netlify deploy preview obligatoire avant merge sur main. Sprint étalé sur ~2 semaines avec validation lot par lot.

---

## 1. Inventaire exact

### 1.1 Pages racine concernées par la migration (15 pages × 3 langues = 45 nouveaux fichiers cibles)

| Fichier actuel | URL actuelle | URL cibles | Statut migration | Notes |
|---|---|---|---|---|
| `index.html` | `/` | `/en/`, `/fr/`, `/es/` | **MIGRE** | Page maîtresse. Le `/` racine deviendra une 301 vers `/en/`. |
| `about.html` | `/about.html` | `/en/about.html`, `/fr/about.html`, `/es/about.html` | **MIGRE** | Contenu actuel EN. Variantes FR/ES à traduire. |
| `compare.html` | `/compare.html` | `/en/compare.html`, `/fr/compare.html`, `/es/compare.html` | **MIGRE** | Préserver `?c=...`. Refonte design en backlog (item 2.6) reste séparée. |
| `globe.html` | `/globe.html` | `/en/globe.html`, `/fr/globe.html`, `/es/globe.html` | **MIGRE** | Charge `unpkg.com/globe.gl`. UI EN. Variantes FR/ES à i18n-iser. |
| `indexchronicles.html` | `/indexchronicles.html` | `/en/indexchronicles.html`, `/fr/indexchronicles.html`, `/es/indexchronicles.html` | **MIGRE** | Index hub des 303 chroniques. Catégories internes déjà i18n via JS. |
| `chronicles-villes.html` | `/chronicles-villes.html` | `/en/chronicles-villes.html`, `/fr/`, `/es/` | **MIGRE** | Cat ville. Lang actuel FR. |
| `chronicles-dest.html` | `/chronicles-dest.html` | idem | **MIGRE** | Cat destination. |
| `chronicles-family.html` | `/chronicles-family.html` | idem | **MIGRE** | Cat famille. theme-color éditorial `#d7731d` à conserver. |
| `chronicles-horizons.html` | `/chronicles-horizons.html` | idem | **MIGRE** | Cat horizons. theme-color éditorial `#7d55d8` à conserver. |
| `chronicles-visas.html` | `/chronicles-visas.html` | idem | **MIGRE** | Cat visas. |
| `terms.html` | `/terms.html` | `/en/terms.html`, `/fr/terms.html`, `/es/terms.html` | **MIGRE** | Légal. Traduction par juriste recommandée — sinon disclaimer en haut "EN canonical". |
| `privacy.html` | `/privacy.html` | idem | **MIGRE** | Légal — même remarque. |
| `wiggmatch.html` | `/wiggmatch.html` | `/fr/wiggmatch.html` (+ `/en/`, `/es/` plus tard) | **CAS SPÉCIAL** | Aujourd'hui FR uniquement. Sprint dédié "wiggmatch trilingue" attendu. **Décision à valider** : (a) bloquer la migration de wiggmatch jusqu'au sprint trilingue OU (b) servir la version FR sur les 3 chemins `/en/wiggmatch.html` + `/es/wiggmatch.html` + `/fr/wiggmatch.html` avec banner "EN/ES coming soon" et `noindex` sur EN/ES temporairement. |
| `404.html` | `/404.html` | Servi par Netlify pour toute 404 | **MIGRE** mais cas spécial | Une seule version 404 servie globalement. Recommandation : 1 fichier multilingue (text via JS depuis localStorage) OU 3 fichiers `/en/404.html` etc. + config Netlify pour servir le bon selon la URL d'origine. |
| `confirmation.html` | `/confirmation.html` | `/en/confirmation.html`, etc. | **MIGRE** mais noindex | Page de remerciement post-form. |

### 1.2 Pages racine HORS scope migration (parcours auth / formulaires / templates)

| Fichier | Raison de l'exclusion |
|---|---|
| `mon-compte.html` | Parcours auth Supabase, `noindex,nofollow`, contenu généré par JS depuis le profil utilisateur. Inutile de trilingualiser l'URL — l'i18n côté JS via localStorage suffit. **Reste sur `/mon-compte.html`**. |
| `onboarding.html` | Parcours auth, `noindex,nofollow`, idem. **Reste sur `/onboarding.html`**. |
| `forms.html` | Test/staging, `noindex,nofollow`. **Reste sur `/forms.html`** ou supprimer. |
| `template_chronicles.html` | Bloqué via `robots.txt`. À supprimer du repo. |
| `index.html.bak`, `index.html.old`, `data/header.js.bak` | Backups. À supprimer. |

### 1.3 Pages déjà trilingues par filename — INCHANGÉES

| Dossier | Pattern | Volume | Décision |
|---|---|---|---|
| `countries/` | `{slug}-{en\|fr\|es}.html` | 484 fichiers (161 pays × 3) | **Inchangé.** La langue est dans le slug, hreflang correct. |
| `chronicles/` | `chronicle-{slug}-{en\|fr\|es}.html` | 75 thématiques | **Inchangé.** Idem. |
| `chronicles/villes/` | `chronicle-{ville}-{pays}-{en\|fr\|es}.html` | 228 (76 × 3) | **Inchangé.** Idem. |
| `lp/` | `{slug}-{en\|fr\|es}.html` | 9 (3 × 3) | **Inchangé.** Trilingue par filename, hreflang OK. |
| `lead-magnet/` | `visas-2026-{en\|fr\|es}.html` | 3 | **Inchangé.** noindex, parcours email. |
| `compare/static/` | `{a}-vs-{b}/index.html` | 64 paires | **Inchangé en V1.** Lang switching DOM-swap interne (data-i18n). Migration trilingue par dossier reportée à V2. |
| `connect/` | App-like (`feed`, `profile`, `swipe`...) | 6 | **Inchangé.** Application Supabase, parcours connecté, i18n via JS. Pas indexé. |
| `ggg/wigggame.html` | Quiz | 1 | **Inchangé.** Lang via JS interne. |

### 1.4 Verdict global volumes

- **Pages source à dupliquer** : 13 (les 15 du tableau 1.1 moins wiggmatch en sursis et 404 si solution Netlify multilingue)
- **Fichiers à créer** : 13 × 3 = **39 fichiers** dans `/en/`, `/fr/`, `/es/`
- **Fichiers à supprimer** (post-migration, après vérif 301) : les 13 fichiers racine devenus redondants — OU les conserver et faire des 301 internes (recommandé pour rollback rapide).
- **Fichiers à régénérer** : `sitemap.xml`, `robots.txt`, `_redirects`, `data/header.js` (lang switcher + prefix logic).
- **Fichiers à laisser tels quels** : 484 + 303 + 9 + 3 + 64 + 6 + 1 = **870 fichiers** non touchés.

---

## 2. Stratégie URL cible

### 2.1 Schéma final

```
/                          → 301 vers /en/                  (root canonical = EN)
/en/                       → page d'accueil EN
/fr/                       → page d'accueil FR
/es/                       → page d'accueil ES
/en/about.html
/fr/about.html
/es/about.html
... etc pour chaque page racine

/countries/portugal-en.html     ← INCHANGÉ
/chronicles/chronicle-bali-indonesia-en.html  ← INCHANGÉ
/lp/vivre-bali-budget-fr.html   ← INCHANGÉ
/lead-magnet/visas-2026-en.html ← INCHANGÉ
/compare/static/portugal-vs-spain/  ← INCHANGÉ
/mon-compte.html, /onboarding.html, /forms.html, /404.html  ← INCHANGÉ (noindex/app)
```

### 2.2 Décision pour `/` racine

**Recommandation : 301 vers `/en/`** plutôt qu'Accept-Language detection.

| Option | Pour | Contre | Décision |
|---|---|---|---|
| **A. 301 statique → /en/** | Crawlable par Google sans ambiguïté. Cache CDN-friendly. Comportement déterministe. Compatible avec `<link rel="canonical">` clair. | Un user FR arrivant via lien direct sur `/` voit 1 fois EN avant de pouvoir switch. | **RECOMMANDÉE** ✓ |
| B. Accept-Language → /fr/ ou /en/ | UX FR meilleure au premier visit. | Casse la canonisation Google (Vary: Accept-Language est mal géré). Cacheable seulement avec Vary header complexe. Comportement non-déterministe pour les bots. | Rejet. |
| C. JS detect localStorage + `location.replace()` après load | Souple. | Flicker FOUC, mauvais pour FCP. Bloque le crawler partiellement. | Rejet. |

**Bénéfice user** : header.js peut, *en plus* du 301, détecter `localStorage.wigg_lang === 'fr'` et faire un `location.replace('/fr/')` sur les pages `/en/` si l'utilisateur a déjà choisi FR (UX silencieuse). À implémenter au Lot 6 du sprint. Garantir que ce soft-redirect se fait UNIQUEMENT si lang utilisateur ≠ lang URL courante, pour éviter les boucles.

### 2.3 Default langue = EN — justification

- `<title>WiggMap — Where is the grass actually greener?` (EN) déjà en place sur `/`.
- Trafic anticipé EN > FR > ES (marché anglophone = 5× le francophone).
- Cohérence avec `hreflang="x-default"` qui pointe déjà vers EN sur les pages countries.
- Plus simple à expliquer aux growth/marketing : "par défaut on est anglophone".

### 2.4 Pages déjà profondes — CONFIRMATION : restent à plat

Tu avais demandé : *"countries et chronicles restent inchangées car le slug-lang dans le nom de fichier porte déjà l'info ; vérifie si je me trompe"*.

**Confirmation** : tu as raison. Trois raisons :

1. **Slug-lang autosuffisant.** `/countries/portugal-en.html` encode déjà la langue. Les hreflang sont corrects (vérifié Sprint 1 audit).
2. **Volume.** Migrer 484+303+9+3 = 799 fichiers vers /en/, /fr/, /es/ doublerait ce volume sans bénéfice SEO (Google les indexe déjà correctement par variante de filename).
3. **PageRank stable.** Toutes les références internes pointent vers `/countries/portugal-en.html`. Casser ces URLs serait un coût massif en redirects et risque temporaire de perte ranking.

**Cohérence visuelle** : oui, c'est asymétrique (`/en/about.html` mais `/countries/portugal-en.html`). Mais le pattern est compréhensible : **les pages racine deviennent par-dossier ; les pages générées en masse restent par filename.** Documenter ce choix dans `project-brain/architecture.md`.

---

## 3. Plan de redirections 301 (Netlify `_redirects`)

### 3.1 Règles à ajouter

Le fichier `_redirects` actuel (1 règle pour `/countries/country.html?country=...`) doit recevoir ces nouvelles règles :

```
# ───── ROOT ─────
# Default lang
/                                /en/                        301!

# ───── ROOT PAGES (preserve query strings via :splat) ─────
# 13 pages × redirection vers /en/ par défaut
/index.html                      /en/                        301!
/about.html                      /en/about.html              301!
/compare.html                    /en/compare.html            301!
/compare.html *                  /en/compare.html?:splat     301!
/globe.html                      /en/globe.html              301!
/indexchronicles.html            /en/indexchronicles.html    301!
/chronicles-villes.html          /en/chronicles-villes.html  301!
/chronicles-dest.html            /en/chronicles-dest.html    301!
/chronicles-family.html          /en/chronicles-family.html  301!
/chronicles-horizons.html        /en/chronicles-horizons.html 301!
/chronicles-visas.html           /en/chronicles-visas.html   301!
/terms.html                      /en/terms.html              301!
/privacy.html                    /en/privacy.html            301!
/confirmation.html               /en/confirmation.html       301!

# wiggmatch — décision pending (voir §1.1) — placeholder default = 301 vers /fr/
/wiggmatch.html                  /fr/wiggmatch.html          301!

# ───── EXISTING (préservée) ─────
/countries/country.html country=:slug  /countries/:slug-en.html  301!

# ───── 404 catch-all ─────
# Pas de règle ici — Netlify sert /404.html par défaut.
```

### 3.2 Détail sur les query strings

Netlify `_redirects` supporte la conservation des query strings via `:splat` ou `*`. Trois cas critiques :

| URL d'origine | URL cible | Règle |
|---|---|---|
| `/compare.html?c=fr,jp,br` | `/en/compare.html?c=fr,jp,br` | `/compare.html *  /en/compare.html?:splat  301!` |
| `/countries/country.html?country=portugal` | `/countries/portugal-en.html` | (déjà existant) |
| `/index.html?utm_source=...` | `/en/?utm_source=...` | Netlify préserve query par défaut. ✓ |

### 3.3 Validation

- `curl -I https://wiggmap.com/about.html` → doit retourner `HTTP/1.1 301` + `Location: /en/about.html`.
- Aucune URL existante ne doit retourner 404.
- Lien `/compare.html?c=thailand,indonesia,portugal` (utilisé dans `index.html` ligne 506 + header.js) → doit aboutir à `/en/compare.html?c=thailand,indonesia,portugal`. **Mais** on aura migré index.html → liens internes à mettre à jour pour pointer directement vers `/en/compare.html?...` et éviter le 301 inutile.

---

## 4. Impact sur `header.js` / `footer.js`

### 4.1 `header.js` — 4 zones impactées

#### 4.1.1 Logique `prefix` (lignes 34-40)

**Code actuel** :
```js
const isSubPage = path.includes("/countries/") || path.includes("/chronicles/")
                 || path.includes("/lp/") || path.includes("/lead-magnet/");
const isDeepPage2 = path.includes("/chronicles/villes/");
const isDeepPage3 = path.includes("/compare/static/");
const prefix = isDeepPage3 ? "../../../" : (isDeepPage2 ? "../../" : (isSubPage ? "../" : ""));
```

**Impact** : avec `/en/about.html`, `path = "/en/about.html"` → ne matche aucun pattern → `prefix = ""`. **Bonne nouvelle : pas de régression**, car les liens injectés par header.js sont **tous absolus** (commencent par `/`). La variable `prefix` était utilisée pour des chemins relatifs assets, mais l'audit montre qu'elle ne sert plus qu'à `homeLink` qui est déjà absolu (`/`). À auditer ligne par ligne.

**Action recommandée** : ajouter `const isLangRoot = /^\/(en|fr|es)(\/|$)/.test(path);` et utiliser ce flag pour faire pointer `homeLink` vers `/en/`, `/fr/`, ou `/es/` selon la langue active (au lieu de `/`). Le burger logo doit ramener à la home dans la langue courante.

#### 4.1.2 Détection langue actuelle (currentLang)

**Code actuel (ligne 336)** :
```js
const currentLang = localStorage.getItem("wigg_lang") || "en";
```

**Problème** : la source de vérité doit devenir l'**URL** sur les pages migrées, pas localStorage. Sinon : un user lang FR clique sur `/en/about.html` depuis un lien externe → header.js voit `wigg_lang=fr` localStorage → affiche pill FR active mais URL est /en/. Incohérence.

**Action recommandée** :
```js
// Déterminer langue depuis URL d'abord, fallback localStorage, fallback 'en'
function detectLang(path) {
  var m = path.match(/^\/(en|fr|es)(\/|$)/);
  if (m) return m[1];
  // Pour les pages avec slug-lang (countries, chronicles, lp...) :
  var slugLang = path.match(/-([a-z]{2})\.html$/);
  if (slugLang && ['en','fr','es'].indexOf(slugLang[1]) !== -1) return slugLang[1];
  // Fallback localStorage (pages non migrées : mon-compte, onboarding, etc.)
  return (localStorage.getItem("wigg_lang") || "en").toLowerCase();
}
const currentLang = detectLang(window.location.pathname);
// Synchroniser localStorage pour cohérence
localStorage.setItem("wigg_lang", currentLang);
```

#### 4.1.3 Lang pill switcher (lignes 398-401, 441-444 + handler)

**Code actuel** : clic sur `[data-lang]` → `localStorage.setItem('wigg_lang', code)` + `location.reload()`.

**Cible** : clic sur `[data-lang]` → calculer URL équivalente dans la nouvelle langue → `location.assign(newUrl)`.

**Pseudo-code** :
```js
function langSwitch(targetLang) {
  var path = window.location.pathname;
  // 1. Pages slug-lang (countries, chronicles, lp, lead-magnet, compare/static)
  var slugMatch = path.match(/^(.*?)-([a-z]{2})\.html$/);
  if (slugMatch && ['en','fr','es'].indexOf(slugMatch[2]) !== -1) {
    // Cas spécial chronicles : utiliser CHRONICLE_LANGS (existant ligne 689)
    if (CHRONICLE_LANGS[path]) return location.assign(CHRONICLE_LANGS[path][targetLang]);
    // Sinon swap simple
    return location.assign(slugMatch[1] + '-' + targetLang + '.html' + window.location.search);
  }
  // 2. Pages root migrées (/en/foo, /fr/foo, /es/foo)
  var rootMatch = path.match(/^\/(en|fr|es)(\/.*)?$/);
  if (rootMatch) {
    var rest = rootMatch[2] || '/';
    return location.assign('/' + targetLang + rest + window.location.search);
  }
  // 3. Pages non migrées (mon-compte, onboarding, forms, 404, connect/) :
  //    fallback historique = localStorage + reload
  localStorage.setItem('wigg_lang', targetLang);
  location.reload();
}
```

**Risque** : si `CHRONICLE_LANGS` ne contient pas une chronicle (ajout récent oublié), le fallback "swap simple" peut produire une URL 404. Garde-fou : `fetch(newUrl, {method:'HEAD'})` async avant `location.assign`, fallback sur reload localStorage si 404. Coût : 1 ping par switch.

#### 4.1.4 `CHRONICLE_LANGS` (ligne 689)

**Statut** : objet existant qui mappe `path actuel → {en, fr, es}` pour les chroniques (déjà documenté dans `project-brain/CLAUDE.md`).

**Impact migration** : **aucun** — les chroniques restent à plat (`/chronicles/...-{lang}.html`). Le switcher utilise déjà ce mapping pour les chroniques. Garder tel quel.

**Action recommandée** : étendre la **documentation interne** pour y ajouter une note "Pour les pages root migrées (/en/, /fr/, /es/), pas besoin de mapping : la regex `/^\/(en|fr|es)(\/.*)?$/` suffit car l'URL contient déjà la langue."

### 4.2 `footer.js` — 2 zones impactées

#### 4.2.1 Liens hardcodés `/terms.html`, `/privacy.html` (lignes 15, 17, 102)

Ces liens deviennent : `/{currentLang}/terms.html`, `/{currentLang}/privacy.html`. Donc le footer doit lire `currentLang` (via le même `detectLang()` exposé par header.js, OU recalculer).

**Action recommandée** : header.js expose `window.WM_LANG = currentLang;` après détection. footer.js lit `window.WM_LANG || 'en'` pour générer les liens. Couplage faible, robuste.

#### 4.2.2 Cookie banner privacy link (ligne 102)

`<a href="/privacy.html" class="wc-link">` → `<a href="/{lang}/privacy.html" class="wc-link">`. Idem.

#### 4.2.3 Newsletter signup endpoint (ligne 540)

Inchangé : `fetch('/', { method:'POST', ... })` poste un Netlify Form sur la racine. Le formulaire est captured par Netlify quel que soit le path — pas de changement requis. **Vérifier toutefois** qu'après migration `/` (qui est devenu un 301) accepte toujours les POST Netlify Forms — Netlify gère normalement les formulaires indépendamment du contenu HTML servi sur la route.

### 4.3 Autres scripts de header.js/footer.js — sans impact

- IIFE webp swap (`footer.js:160`) : indépendant des URLs.
- Related chronicles déterministe (`footer.js:296+`) : utilise `window.location.pathname.includes('/chronicles/')` — chroniques restent à plat, OK.
- Breadcrumbs (`footer.js:228+`) : injecte uniquement sur `/chronicles/` — OK.
- Connect widget (`footer.js:213-226`) : charge sur `/chronicles/` uniquement — OK.

---

## 5. Impact sur le code existant

### 5.1 Liens internes hardcodés à mettre à jour

#### 5.1.1 Dans `index.html` (et clones FR/ES à créer)

Tous les liens `/about.html`, `/compare.html?c=...`, `/globe.html`, `/wiggmatch.html`, `/indexchronicles.html`, `/ggg/wigggame.html` (15+ occurrences via grep) doivent devenir `/en/about.html`, etc. dans la version EN, `/fr/about.html` dans la version FR, `/es/about.html` dans la version ES.

**Outil** : script Python `scripts/migrate_root_links.py` qui prend en entrée le HTML source + lang cible, applique les substitutions via regex, et émet le HTML migré. Idempotent (re-run produit même output).

#### 5.1.2 Dans header.js (déjà couvert §4.1)

`href="/wiggmatch.html"`, `href="/indexchronicles.html"`, `href="/onboarding.html"` (auth — non migré, reste tel quel), `href="/mon-compte.html"` (auth — non migré). Les 3 premiers doivent devenir lang-aware.

#### 5.1.3 Dans footer.js (déjà couvert §4.2)

`href="/terms.html"`, `href="/privacy.html"` → lang-aware.

#### 5.1.4 Dans les pages countries / chronicles (référence aux pages racine)

Les pages countries+chronicles peuvent référencer `/about.html`, `/compare.html`, etc. dans leur contenu. **À auditer via grep**.

```bash
grep -lE 'href="/(about|compare|globe|wiggmatch|indexchronicles|chronicles-)[a-z\-]*\.html' \
  countries/*.html chronicles/*.html chronicles/villes/*.html
```

Si occurrences trouvées → soit (a) régénérer ces 800 fichiers via `_gen_v3.py` après mise à jour des templates, soit (b) laisser les liens en racine et compter sur les 301 (acceptable mais coûte 1 round-trip par clic).

**Recommandation** : (a) régénération propre via script, dans un commit dédié, après que la migration des pages racine soit validée et stable.

### 5.2 `sitemap.xml`

**Régénération obligatoire** via `scripts/gen_sitemap.py`. Changements :

- Supprimer les 14 anciennes URLs racine (`/about.html`, `/compare.html`, `/indexchronicles.html`, etc.).
- Ajouter les 42 nouvelles URLs (14 pages × 3 langues).
- Ajouter `/`, `/en/`, `/fr/`, `/es/` au sitemap (redirect-only mais utile pour découvrabilité).
- Hreflang tuples : pour chaque trio `/en/about.html` ↔ `/fr/about.html` ↔ `/es/about.html`, émettre les `<xhtml:link rel="alternate" hreflang="...">` correctement.
- Conserver les 870 URLs déjà sitemapées non-racine.

**Volume final estimé** : 894 URLs actuelles − 14 + 42 + 4 = **926 URLs**.

### 5.3 `canonical` URLs

Chaque page migrée doit déclarer son canonical exact :

- `/en/about.html` → `<link rel="canonical" href="https://wiggmap.com/en/about.html">`
- `/fr/about.html` → `<link rel="canonical" href="https://wiggmap.com/fr/about.html">`
- `/es/about.html` → `<link rel="canonical" href="https://wiggmap.com/es/about.html">`

**Pour chaque trio**, ajouter les `hreflang` complets (en, fr, es, x-default) en `<head>`.

### 5.4 Service Worker (`sw.js`)

**Cache name à bump** : `wiggmap-v2` → `wiggmap-v3`. Sinon les utilisateurs avec SW actif servent l'ancien `/` cached et n'atteignent jamais le 301. Attention : bump SW = invalidation cache totale → légère perte temporaire de perf perçue, acceptable.

`CORE_ASSETS` à mettre à jour :
```js
const CORE_ASSETS = ["/", "/en/", "/manifest.webmanifest"];
// "/" reste car le SW gère le 301 transparent côté navigateur
```

### 5.5 `robots.txt`

Aucun changement strict requis (les `Disallow` actuels restent valides). Recommandation : ajouter `Allow: /en/`, `Allow: /fr/`, `Allow: /es/` pour explicitation (Google les crawlerait de toute façon, mais c'est un signal propre).

### 5.6 `_headers` Netlify (créé Sprint 1)

Aucun changement requis. La CSP couvre tous les domaines, les règles `cache-control` s'appliquent aux dossiers `/assets/`, `/data/`, etc. Les nouvelles URLs `/en/...` héritent du bloc `/*` global. ✓

### 5.7 Skip-link `#wm-main` (créé Sprint 1)

Présent sur les 15 pages racine actuelles. **Doit être propagé** sur les 39 nouvelles pages `/en/`, `/fr/`, `/es/`. Le script de duplication (§6.2) doit préserver le pattern.

### 5.8 GTM / GA4 / Meta Pixel

Aucun impact technique. Toutefois :

- Les URLs vues dans GA4 vont changer du jour au lendemain → ajouter des **annotations** dans GA4 et Search Console à la date de la mise en prod pour expliquer les ruptures de courbes.
- Vérifier que GTM continue à se déclencher sur `/en/`, `/fr/`, `/es/` (les triggers `Page View` `Page URL contains` doivent inclure les nouvelles routes — auditer GTM workspace avant déploiement).

### 5.9 Buttondown / Lead magnet

- Buttondown reçoit l'email + un tag `wiggmap_newsletter_{lang}`. Le tag est dérivé de `localStorage.wigg_lang` (footer.js ligne 549 environ). Avec la migration, `currentLang` viendra de l'URL → tag devient correct. ✓
- Lead magnet `/lead-magnet/visas-2026-{lang}.html` : URLs inchangées, parcours intact.

### 5.10 Auth Supabase

- `mon-compte.html`, `onboarding.html` non migrés → URLs inchangées.
- `connect/` non migré → URLs inchangées.
- Aucun impact sur le flow OAuth Google ou les cookies Supabase.

---

## 6. Ordre d'exécution sécurisé

### 6.0 Branche dédiée + deploy preview Netlify

**Obligatoire.** Tout le travail se fait sur `git checkout -b sprint-2-trilingual-roots`. Après chaque commit, push sur la branche → Netlify génère un deploy preview URL (ex : `deploy-preview-23--wiggmap.netlify.app`). Tests visuels sur le preview, **jamais sur main directement** jusqu'à validation finale.

### 6.1 Étapes ordonnées avec point de rollback

| # | Étape | Commits | Rollback | Validation requise |
|---|---|---|---|---|
| 1 | Créer la branche, ajouter `MIGRATION_PLAN.md` (ce fichier) au repo | 1 | `git branch -D` | Plan validé par toi |
| 2 | Créer dossiers `/en/`, `/fr/`, `/es/`. Dupliquer chaque page racine en 3 versions via script. EN = copie 1:1 du fichier existant. FR = traduction (existante si déjà en FR, sinon `[TRANSLATE-FR]` placeholder). ES = traduction. | 1 par page = 13 commits, OU 1 commit batch | `git revert SHA` ou `rm -rf en/ fr/ es/` | Build local sans erreur. Diff visuel `/en/about.html` vs `/about.html` = identique sauf canonical/hreflang |
| 3 | Mettre à jour `_redirects` avec toutes les règles 301 du §3 | 1 | `git revert SHA` | `curl -I` sur 5 URLs anciennes → 301 corrects |
| 4 | Mettre à jour `header.js` : `detectLang()`, `langSwitch()`, lang-aware `homeLink` | 1 | `git revert SHA` | Test 5 pages-types Sprint 1, lang switch fonctionne, no console error |
| 5 | Mettre à jour `footer.js` : liens privacy/terms lang-aware via `window.WM_LANG` | 1 | `git revert SHA` | Test 5 pages-types, footer links pointent vers bon `/lang/` |
| 6 | Mettre à jour `index.html` (les 3 versions /en/, /fr/, /es/) : tous les liens internes hardcodés deviennent lang-aware | 1 | `git revert SHA` | Click-through sur chaque CTA de la home |
| 7 | Régénérer `sitemap.xml` via `scripts/gen_sitemap.py` mis à jour | 1 | `git revert SHA` | XML valide, 926 URLs, hreflang tuples corrects |
| 8 | Bump `sw.js` cache name → `wiggmap-v3`, ajouter `/en/` à CORE_ASSETS | 1 | `git revert SHA` | DevTools Application → SW unregister + re-register, vérifier nouvelle version |
| 9 | Mettre à jour `robots.txt` (Allow explicite) | 1 | `git revert SHA` | `curl /robots.txt` propre |
| 10 | Audit grep links internes dans countries/, chronicles/ → si occurrences `/about.html` etc. → script de réécriture + commit régénération | 1 (régénération) ou 0 (pas trouvé) | `git revert SHA` | Aucun lien interne pointe vers ancienne racine |
| 11 | Documentation : update `project-brain/architecture.md` avec nouveau schéma URLs + `data/header.js` doc CHRONICLE_LANGS | 1 | `git revert SHA` | Doc cohérente |

**Total commits** : ~11 (lots batch) à ~14 (lots fins).

### 6.2 Stratégie de duplication pages racine (étape 2 détaillée)

Script `scripts/migrate_to_lang_dirs.py` :

```python
# Pseudo-code
SOURCE_PAGES = ['index.html', 'about.html', 'compare.html', 'globe.html',
                'indexchronicles.html', 'chronicles-villes.html', 'chronicles-dest.html',
                'chronicles-family.html', 'chronicles-horizons.html', 'chronicles-visas.html',
                'terms.html', 'privacy.html', 'confirmation.html']
LANGS = ['en', 'fr', 'es']

for page in SOURCE_PAGES:
    src = open(page).read()
    for lang in LANGS:
        dst = src
        # 1. Update <html lang="...">
        dst = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', dst, count=1)
        # 2. Update canonical
        dst = re.sub(r'<link rel="canonical" href="[^"]*"',
                     f'<link rel="canonical" href="https://wiggmap.com/{lang}/{page if page != "index.html" else ""}"',
                     dst, count=1)
        # 3. Inject hreflang block (replace existing if any)
        dst = inject_hreflang(dst, page, lang)
        # 4. Update internal links: /about.html -> /{lang}/about.html (etc.)
        for src_page in SOURCE_PAGES:
            target = src_page if src_page != 'index.html' else ''
            dst = dst.replace(f'href="/{src_page}"', f'href="/{lang}/{target}"')
            dst = re.sub(rf'href="/{re.escape(src_page)}\?', f'href="/{lang}/{target}?', dst)
        # 5. Write
        os.makedirs(lang, exist_ok=True)
        out_name = 'index.html' if page == 'index.html' else page
        open(f'{lang}/{out_name}', 'w').write(dst)
```

**Garantie idempotence** : re-run du script produit byte-identique output. Tests unitaires Python sur les substitutions.

### 6.3 Stratégie traductions FR / ES (cas où contenu actuel n'est pas dans la langue cible)

**Pages où contenu source = EN** : `index.html` (tit/desc EN, JS swap au runtime), `about.html`, `globe.html`, `terms.html`, `privacy.html`, `404.html`.

**Pages où contenu source = FR** : `wiggmatch.html` (cas spécial), `chronicles-villes/dest/family/horizons/visas.html` (lang="fr" actuel).

**Approche** :

1. Pour les pages où la traduction n'existe pas en dur → créer le fichier `/fr/about.html` avec le contenu EN + un balisage `<!-- TODO-i18n FR -->` au début. Lancer un workflow de traduction humaine (ou IA validée) en parallèle de la migration technique.
2. **Pas de blocage** : les pages avec contenu non-traduit peuvent être servies temporairement sur `/fr/about.html` avec contenu EN + bannière "Cette page n'est pas encore traduite. [Lire en anglais →](https://wiggmap.com/en/about.html)". Mieux que pas de page du tout pour le SEO.
3. Pages chroniques index (`chronicles-villes.html` etc.) → contenu source FR → variantes EN/ES à créer.

### 6.4 Migration data : aucun script de migration DB requis

Pas de DB côté front. Aucun migration de données. ✓

---

## 7. Critères de succès — checklist concrète

### 7.1 Pré-merge (sur deploy preview Netlify)

- [ ] **Build Netlify OK** : zéro warning, zéro 404 dans le build log.
- [ ] **Lighthouse mobile** sur `/en/`, `/fr/`, `/es/` : Performance ≥ 85, SEO = 100, A11y ≥ 95.
- [ ] **Hreflang validator** ([https://technicalseo.com/tools/hreflang/](https://technicalseo.com/tools/hreflang/)) : 0 erreur sur les 14 trios root.
- [ ] **Schema.org validator** : tous les JSON-LD parsent sur `/en/about.html`, `/fr/about.html`, `/es/about.html`.
- [ ] **Manuel** sur 10 URLs aléatoires anciennes (`/about.html`, `/compare.html?c=...`, `/wiggmatch.html`, etc.) : `curl -I` retourne 301 vers la bonne cible.
- [ ] **Lang switcher** : sur `/en/about.html`, click pill FR → `/fr/about.html` (pas reload de la même URL). Test sur les 14 pages.
- [ ] **CHRONICLE_LANGS** : sur `/chronicles/chronicle-bali-indonesia-en.html`, click pill FR → `/chronicles/chronicle-bali-indonesia-fr.html`. Pas régressé.
- [ ] **Service Worker** : DevTools → Application → unregister ancien SW + re-register → `wiggmap-v3` actif → reload pages, pas de stale `/` cached.
- [ ] **Newsletter form** : POST sur `/en/about.html` → succès Netlify Form.
- [ ] **Auth Supabase** : login depuis `/en/` → callback fonctionne, redirige vers `/onboarding.html` puis `/mon-compte.html`.
- [ ] **GTM** : firing sur les 3 nouvelles routes confirmé via GTM Debug.
- [ ] **Skip-link** : Tab depuis top de chaque page → focus visible, jump vers `#wm-main`.
- [ ] **5 pages-types** Sprint 1 (index, country/france-en, chronicle/villes/bali-en, chronicle/digital-nomad-visas, compare) : visuel + console + responsive OK.
- [ ] **Aucune erreur console** sur deploy preview.

### 7.2 Post-merge (production, 1ʳᵉ semaine)

- [ ] **Search Console** : soumettre les 3 nouvelles versions du sitemap. Vérifier crawl rate.
- [ ] **Search Console > Pages > Indexed** : suivre la transition. Les anciennes URLs doivent passer en "Page with redirect", les nouvelles en "Indexed".
- [ ] **GA4 > Reports > Engagement > Pages and screens** : annoter la date de migration. Comparer trafic J-7 vs J+7 par langue.
- [ ] **Backlinks tools** (Ahrefs / Semrush) : vérifier que les liens externes pointant vers les anciennes URLs sont absorbés par les 301.
- [ ] **Aucun lien interne brisé** : audit Screaming Frog complet, 0 link 404.

### 7.3 Post-merge (mois 1-3)

- [ ] **Trafic organique FR + ES** : doit augmenter (objectif +50% à 3 mois sur les requêtes `where to live`, `coût de la vie`, `costo de vida` etc.).
- [ ] **CTR Search Console** : par langue, suivre l'évolution.
- [ ] **Aucune chute de ranking sur EN** : si chute > 15 % sur les 30 premiers KW, audit + rollback partiel possible.

---

## 8. Risques identifiés

### 8.1 Drop SEO temporaire

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| **Google met 2-4 semaines à recrawler les nouvelles URLs** | Élevée | Perte ranking 1-3 semaines | (a) Sitemap soumis dès J+0. (b) `Indexing API` (Google Search Console) pour 50 URLs prioritaires. (c) 301 propres pour transmission PageRank. (d) Timing : éviter de migrer en pleine campagne marketing. |
| **301 chains** (`/about.html` → `/en/about.html` → autre 301) | Modérée | Perte de jus SEO + perf | Audit Screaming Frog après mise à jour des liens internes. Aucune chain > 1 hop tolérée. |
| **Variantes FR/ES non traduites** | Élevée si pas de workflow trad | Pages `<title>` et `<meta>` EN sur des URLs FR → mauvais signal | Bannière + canonical vers `/en/` sur les pages non-traduites. Bloquer du sitemap FR/ES tant que pas traduites. |
| **Hreflang mal formé** | Modérée | Google ignore les variantes, indexe une seule | Validateur automatique en pre-commit. Audit hreflang dans étape 7. |

### 8.2 Liens externes existants

Backlinks vers `/about.html`, `/compare.html`, `/indexchronicles.html` : couverts par les 301 du §3. **Risque résiduel** : sites qui pointent vers `/wiggmatch.html` (FR-only) → 301 vers `/fr/wiggmatch.html`. Si user EN clique sur ce lien → arrive sur page FR. Acceptable temporairement, à corriger dès le sprint wiggmatch trilingue.

### 8.3 Cache navigateur / SW

| Couche | Risque | Mitigation |
|---|---|---|
| Cache HTTP navigateur | User avec ancienne version cachée de `/about.html` continue à voir l'ancien contenu pendant max-age. | `_headers` actuel sur `/data/*.json` = 3600s, sur HTML pas spécifié → Netlify default ~10min. Pour la migration, ajouter temporairement `Cache-Control: no-cache` sur `/*.html` (sauf `/{en,fr,es}/*` qui restent en max-age long). |
| Service Worker | User avec SW v2 cached sert l'ancien `/index.html`. | Bump cache name `v2 → v3` (étape 8). SW skipWaiting + clients.claim au activate (déjà en place). |
| CDN Netlify | Pages cachées CDN servent l'ancien contenu. | Netlify purge auto au deploy. ✓ |

### 8.4 Cas particuliers query strings

| URL | Query critique | Risque | Mitigation |
|---|---|---|---|
| `/compare.html?c=...` | Liste de pays comparés | Si query perdue dans le 301 → user voit comparateur vide | Règle `/compare.html *  /en/compare.html?:splat  301!` couvre. À tester avec `curl -I "https://wiggmap.com/compare.html?c=fr,jp,br"`. |
| `/countries/country.html?country=portugal` | Slug du pays | Déjà géré (règle existante). | Inchangé. |
| `/wiggmatch.html?ref=...` | UTM marketing | Si `?ref=...` perdu → tracking faussé | Règle splat préservée. ✓ |

### 8.5 Auth Supabase

`mon-compte.html` et `onboarding.html` non migrés → URLs inchangées. Le callback OAuth Google est configuré sur `https://wiggmap.com/onboarding.html` (à vérifier dans console Supabase). Pas d'impact.

### 8.6 Connect widget (Supabase chronicles)

Widget chargé sur `/chronicles/*` (inchangé). Pas d'impact.

### 8.7 Sécurité et CSP

CSP `_headers` actuelle (Report-Only) couvre tous les domaines. Les nouvelles URLs `/en/`, `/fr/`, `/es/` héritent du bloc `/*`. Aucune nouvelle origine externe à allowlister. ✓

---

## 9. Estimation temps + commits

### 9.1 Découpage en lots (14 commits)

| # | Lot | Description | Effort (h) | Risque |
|---|---|---|---|---|
| 1 | Plan + branche | Commit MIGRATION_PLAN.md + `git checkout -b sprint-2-trilingual-roots` | 0 (fait) | — |
| 2 | Script migration | `scripts/migrate_to_lang_dirs.py` + tests unitaires | 4 | Faible |
| 3 | Duplication pages | Run script, génère 39 fichiers dans /en/ /fr/ /es/ | 1 | Faible |
| 4 | Traductions FR/ES placeholders | Bannières "non traduite", canonical vers /en/ | 2 | Faible |
| 5 | `_redirects` | 14 règles 301 + splat | 0.5 | Faible |
| 6 | `header.js` lang-aware | detectLang, langSwitch, homeLink | 3 | Moyen |
| 7 | `footer.js` lang-aware | privacy/terms via window.WM_LANG | 1 | Faible |
| 8 | `index.html` × 3 langues | Liens internes lang-aware via re-run script | 1 | Faible |
| 9 | `sitemap.xml` régénéré | `scripts/gen_sitemap.py` updated | 2 | Faible |
| 10 | `sw.js` cache bump | v2 → v3, CORE_ASSETS update | 0.5 | Très faible |
| 11 | `robots.txt` | Allow explicite | 0.25 | Très faible |
| 12 | Audit liens internes countries/chronicles | grep + script si occurrences | 2-4 | Faible |
| 13 | Doc | `project-brain/architecture.md` mis à jour | 1 | Très faible |
| 14 | Tests + ajustements | Lighthouse, hreflang validator, fix mineurs | 3 | Variable |

**Total dev** : ~21 h (range 18-24 h selon la qualité des traductions disponibles).

### 9.2 Calendrier suggéré

- **Semaine 1** : lots 1-7 (infrastructure technique). Deploy preview review.
- **Semaine 2** : lots 8-14 (intégration + tests). Ajustements basés sur preview.
- **J+15** : merge sur main + push prod + monitoring intensif.
- **J+15 à J+45** : monitoring SEO Search Console + GA4. Ajustements éventuels.

### 9.3 Dépendances externes (qui ne sont pas du dev)

- **Traductions FR/ES** : si pas déjà disponibles, 4-8 h de traducteur humain ou de revue IA. À démarrer en parallèle dès le lot 1.
- **Budget GSC Indexing API** : 200 requêtes/jour gratuit, suffit largement pour 42 nouvelles URLs.
- **Annotations GA4 / Search Console** : 30 min admin.

### 9.4 Ne PAS sous-estimer

- **Édition de wiggmatch.html** = SPRINT SÉPARÉ (cf. §1.1). Ne pas tenter de l'inclure dans ce sprint, le scope explose.
- **Refonte design compare.html** (backlog 2.6) = SPRINT SÉPARÉ.
- **Pillar pages "Best for X 2026"** (backlog 5.1) = SPRINT SÉPARÉ.

---

## 10. Décisions à valider avant exécution

1. **(D1) Cas wiggmatch.html** : (a) bloquer migration jusqu'au sprint trilingue dédié et garder l'URL `/wiggmatch.html` actuelle non migrée OU (b) servir la version FR sur `/en/` + `/es/` avec banner "EN/ES coming soon" + `noindex` temporaire ?
   - **Recommandation** : (a). Plus simple, zéro risque SEO. La règle 301 du §3 est `/wiggmatch.html → /fr/wiggmatch.html`, et on ne crée pas `/en/wiggmatch.html` ni `/es/wiggmatch.html` tant que le sprint trilingue n'est pas livré.

2. **(D2) `/` racine** : confirmer **301 → /en/** (vs autre option) ?
   - **Recommandation** : confirmer (raisons §2.2).

3. **(D3) Pages `noindex` (`mon-compte`, `onboarding`, `forms`, `404`, `confirmation`)** :
   - `mon-compte` + `onboarding` + `forms` : confirmer **non migrées** (restent à plat).
   - `404.html` : (a) 1 fichier multilingue avec switch JS OU (b) 3 fichiers `/en/404.html` etc. avec config Netlify ?
     - **Recommandation** : (a). Plus simple, Netlify ne supporte pas nativement de servir un 404 par langue.
   - `confirmation.html` : (a) 1 fichier multilingue OU (b) 3 fichiers ?
     - **Recommandation** : (b) si on veut tracker conversion par langue dans GA4 ; (a) sinon.

4. **(D4) Traductions manquantes** : workflow choisi ?
   - (a) Traduction humaine pré-launch (bloquant)
   - (b) IA validée pré-launch
   - (c) Bannière "non traduite" + canonical vers /en/ + traduction post-launch (non bloquant)
   - **Recommandation** : (c). Permet de shipper la migration technique vite, traductions en parallèle sans bloquer.

5. **(D5) Pages `chronicles-*.html` index** : leur contenu actuel est en FR (`lang="fr"`). EN/ES à traduire. Même question que D4.
   - **Recommandation** : (c) idem. Bannière + canonical FR.

6. **(D6) Régénération country/chronicle pages pour mettre à jour les liens internes** (étape 10 / lot 12) : faire dans **ce sprint** (cohérence totale, +4h dev) OU **sprint séparé** (laisser les liens internes pointer vers ancienne racine, 301 fait le travail) ?
   - **Recommandation** : sprint séparé. Le 301 absorbe correctement, et régénérer 800 fichiers dans le même sprint augmente le scope risque. Faire un sprint **post-validation** dédié à la propreté du graphe interne.

7. **(D7) Gestion `wm_consent` cookie** : le cookie `wigg_consent` (localStorage) survit au changement d'URL ? Test à valider — normalement oui, localStorage est par origin pas par path.
   - **Validation** : 1 test manuel sur deploy preview suffira.

8. **(D8) Branche git** : nom proposé `sprint-2-trilingual-roots`. OK ?

9. **(D9) Indexing API GSC** : utilisation pour push immédiat des 42 nouvelles URLs ? Nécessite credentials Google Cloud Service Account + adapter `scripts/`.
   - **Recommandation** : utile mais non bloquant. À faire en J+1 après merge.

10. **(D10) Date de mise en prod** : éviter merge sur main pendant :
    - les pics de trafic naturels (lundi matin EU)
    - les lancements marketing
    - les vacances scolaires (équipe peu réactive si rollback urgent)
    - **Recommandation** : merge un mardi ou mercredi matin, équipe au complet, monitoring actif sur 4h.

---

## Annexe A — Liste exhaustive des URLs à migrer (référence)

```
SOURCE                              → TARGET (×3 langs)
/                                   → /en/ (canonical), /fr/, /es/
/index.html                         → /en/, /fr/, /es/             (alias de la home)
/about.html                         → /{lang}/about.html
/compare.html                       → /{lang}/compare.html         (préserve ?c=...)
/globe.html                         → /{lang}/globe.html
/indexchronicles.html               → /{lang}/indexchronicles.html
/chronicles-villes.html             → /{lang}/chronicles-villes.html
/chronicles-dest.html               → /{lang}/chronicles-dest.html
/chronicles-family.html             → /{lang}/chronicles-family.html
/chronicles-horizons.html           → /{lang}/chronicles-horizons.html
/chronicles-visas.html              → /{lang}/chronicles-visas.html
/terms.html                         → /{lang}/terms.html
/privacy.html                       → /{lang}/privacy.html
/confirmation.html                  → /{lang}/confirmation.html
/wiggmatch.html                     → /fr/wiggmatch.html SEUL (sprint séparé pour EN/ES)
```

URLs **inchangées** :

```
/countries/{slug}-{lang}.html       (484 fichiers)
/chronicles/chronicle-{slug}-{lang}.html  (75 thématiques)
/chronicles/villes/chronicle-{ville}-{pays}-{lang}.html  (228)
/lp/{slug}-{lang}.html              (9)
/lead-magnet/visas-2026-{lang}.html (3)
/compare/static/{a}-vs-{b}/         (64)
/connect/*.html                     (6, app interne)
/ggg/wigggame.html                  (1)
/mon-compte.html                    (auth, noindex)
/onboarding.html                    (auth, noindex)
/forms.html                         (test, noindex)
/404.html                           (catch-all, multilingue JS)
```

---

## Annexe B — Diff prévu sur `_redirects`

**Avant** (4 lignes) :
```
# Netlify redirects

# Old dynamic country URL → new static page (default to English)
/countries/country.html  country=:slug  /countries/:slug-en.html  301!
```

**Après** (~25 lignes) :
```
# Netlify redirects — Sprint 2 trilingual roots

# ───── ROOT ─────
/                                /en/                        301!
/index.html                      /en/                        301!

# ───── ROOT PAGES (preserve query strings) ─────
/about.html                      /en/about.html              301!
/compare.html *                  /en/compare.html?:splat     301!
/globe.html                      /en/globe.html              301!
/indexchronicles.html            /en/indexchronicles.html    301!
/chronicles-villes.html          /en/chronicles-villes.html  301!
/chronicles-dest.html            /en/chronicles-dest.html    301!
/chronicles-family.html          /en/chronicles-family.html  301!
/chronicles-horizons.html        /en/chronicles-horizons.html 301!
/chronicles-visas.html           /en/chronicles-visas.html   301!
/terms.html                      /en/terms.html              301!
/privacy.html                    /en/privacy.html            301!
/confirmation.html               /en/confirmation.html       301!
/wiggmatch.html                  /fr/wiggmatch.html          301!

# ───── EXISTING ─────
/countries/country.html  country=:slug  /countries/:slug-en.html  301!
```

---

## Annexe C — Pseudo-code détaillé de `langSwitch()` pour header.js

```js
function langSwitch(targetLang) {
  if (!['en','fr','es'].includes(targetLang)) return;
  var path = window.location.pathname;
  var search = window.location.search;
  var hash = window.location.hash;

  // 1. Pages chroniques (mappées explicitement dans CHRONICLE_LANGS)
  if (CHRONICLE_LANGS[path]) {
    var dest = CHRONICLE_LANGS[path][targetLang];
    if (dest) return location.assign(dest + search + hash);
  }

  // 2. Pages slug-lang générique (countries, lp, lead-magnet, compare/static)
  var slugMatch = path.match(/^(.*?)-([a-z]{2})\.html$/);
  if (slugMatch && ['en','fr','es'].includes(slugMatch[2])) {
    var newPath = slugMatch[1] + '-' + targetLang + '.html';
    return location.assign(newPath + search + hash);
  }

  // 3. Pages root migrées (/en/, /fr/, /es/)
  var rootMatch = path.match(/^\/(en|fr|es)(\/.*)?$/);
  if (rootMatch) {
    var rest = rootMatch[2] || '/';
    return location.assign('/' + targetLang + rest + search + hash);
  }

  // 4. Fallback : pages non migrées (mon-compte, onboarding, forms, 404, connect/, ggg/)
  // Utilise localStorage + reload comme avant
  localStorage.setItem('wigg_lang', targetLang);
  location.reload();
}
```

---

*Plan rédigé le 2026-05-03. Aucun fichier source modifié dans cette phase. En attente validation des points D1-D10 pour démarrer l'exécution.*
