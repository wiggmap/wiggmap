# WiggMap — État des lieux du projet (snapshot factuel)

> **Date du snapshot** : 2026-06-13
> **Branche** : `main` (HEAD `7e3bf67`)
> **Méthode** : inspection directe du filesystem (ls, find, grep, lecture). Aucune valeur extraite de mémoire ou de documentation interne sans vérification.
> **Destinataires** : humain + LLM (Claude / Gemini / ChatGPT). Fichier autosuffisant : pas de référence externe nécessaire pour le comprendre.

---

## 1. Identité & stack

| Élément | Valeur |
|---|---|
| URL prod | `https://wiggmap.com` |
| Repo GitHub | `https://github.com/wiggmap/wiggmap` |
| Hébergement | **Netlify** (présence de `_redirects`, `_headers`, formulaire `data-netlify="true"`) |
| Type de site | **Site statique HTML/CSS/JS** — pas de framework JS, pas de build front-end |
| `package.json` | **Absent** |
| `node_modules/` | **Absent** |
| Outillage backend | Python (scripts de génération : `_gen_v3.py`, `scripts/*.py`) |
| Langues servies | **EN, FR, ES** (trois langues complètes pour countries + chronicles + LP + lead-magnet ; les pages racine sont sous `/en/`, `/fr/`, `/es/`) |
| Analytics | **GTM container `GTM-K4MMRD4R`** (consent mode v2 — denied par défaut, granted après opt-in cookie). Une page (`countries/country.html`) embarque en plus un gtag direct `G-36BWEJGCTB`. |
| Meta Pixel | **ID `867064843065581`** chargé via `data/header.js` après opt-in cookie. Présent sur toutes les pages qui injectent header.js (count : non audité — voir §5). |
| Newsletter | **Buttondown** — référencé dans `_headers` (CSP allowlist `buttondown.email` + `api.buttondown.email`) et utilisé dans `wiggmatch.html`. **Non détecté dans `en/index.html`, `fr/index.html`, `es/index.html`** (à confirmer : le footer.js peut l'injecter dynamiquement). |
| Formulaires Netlify | Déclarés dans `forms.html` : `newsletter` + `correction`. Présents aussi sur les 9 pages LP. |
| PWA | Oui : `manifest.webmanifest` (name "WiggMap", theme `#1a5430`) + Service Worker `sw.js` v3 (network-first sur HTML/JSON, cache-first sur assets). |
| Sécurité | **CSP actif (non Report-Only)** depuis PR #14, avec allowlist explicite : GTM, google-analytics, connect.facebook.net, unpkg, buttondown, *.supabase.co, cdn.jsdelivr.net. HSTS preload activé, X-Frame-Options DENY, etc. (cf. `_headers`). |
| Supabase | `https://tkctreoftezvbfejhbto.supabase.co` (clé publishable hardcodée dans `connect/widget.js`). Auth Google OAuth + email/password (cf. `SUPABASE_SETUP.sql`). |

---

## 2. Arborescence réelle

```
/                       ← racine repo == racine site servi par Netlify
├── index.html          (111 KB) ← HOME REDESIGN "tunnel" intégrée — voir §9
├── en/                 ← 14 pages racine traduites EN
├── fr/                 ← 14 pages racine traduites FR
├── es/                 ← 14 pages racine traduites ES
├── countries/
│   ├── country.html        ← template dynamique (≈ query string ?country=)
│   └── <slug>-{en|fr|es}.html  × 161 slugs × 3 = 483 pages statiques
├── chronicles/
│   ├── chronicle-*-{en|fr|es}.html  × 25 séries × 3 = 75 (thématique)
│   ├── villes/  ← 76 villes × 3 = 228 chroniques villes
│   └── 1966/    ← 4 pays × 3 = 12 chroniques "1966"
├── compare.html        (page dynamique legacy à la racine, encore servie)
├── compare/static/     ← 64 pages compare statiques pré-construites (paires de pays)
├── lp/                 ← 3 LP × 3 langues = 9 pages
├── lead-magnet/        ← 1 guide ("Top 25 visas 2026") × 3 langues = 3 pages
├── connect/            ← WiggMap Connect (8 fichiers, voir §8)
├── globe.html          ← carte 3D (globe.gl via unpkg)
├── wiggmatch.html      ← quiz dynamique trilingue (EN-source)
├── home-tunnel.html    ← prototype standalone (voir §9)
├── home-redesign-v2.html  ← autre prototype (voir §9)
├── data/
│   ├── countries.json / countries.fr.json / countries.es.json  (161 pays chacun)
│   ├── details/        ← 160 fichiers JSON (un par pays, EN)
│   ├── details-fr/     ← 160 fichiers JSON FR
│   ├── details-es/     ← 160 fichiers JSON ES
│   ├── _template.details.json
│   ├── geo-by-slug.json / timezones-by-slug.json / random.json
│   ├── header.js       ← injection navbar + Meta Pixel + lang detection
│   ├── footer.js       ← injection footer + cookie banner + newsletter
│   ├── share.js / correction-form.js
│   ├── map/            ← world.geojson + countries2.json + countries_index.json + build-index.html
│   └── i18n/{fr,es}/   ← (présents mais vides dans le snapshot)
├── assets/             ← wm-tokens.css + 161 paires hero-{slug}.{jpg,webp} + assets divers
├── assetscity/         ← images des chroniques villes
├── imgindex/           ← 5 PNG (centre, chronicles, globe, jeux, random) pour la home
├── ggg/                ← /wigggame/ prototype (questions.json, wigggame.html)
├── scripts/            ← scripts Python de build / migration / monitoring
├── _redirects          ← Netlify redirects (74 lignes)
├── _headers            ← Netlify headers (CSP + cache)
├── sw.js               ← Service Worker v3
├── manifest.webmanifest
├── robots.txt
├── sitemap.xml         ← sitemap-index
├── sitemap-roots.xml / sitemap-countries.xml / sitemap-chronicles.xml / sitemap-compare.xml
├── 404.html / about.html / privacy.html / terms.html / confirmation.html / forms.html / mon-compte.html / onboarding.html / indexchronicles.html
├── chronicles-{villes,dest,family,horizons,visas}.html  ← 5 hubs catégoriels racine (legacy, redirigés vers /fr/)
├── _gen_v3.py          ← générateur trilingue (voir §10)
├── template_chronicles.html
├── googleaee6c9fba1b1be46.html  ← verify Google Search Console
├── AUDIT.md / AUDIT_PREVIEW*.md / MIGRATION_PLAN.md / SPRINT_X/Y/Z_*_PLAN.md / SETUP_EMAIL_AND_PIXEL.md / SUPABASE_SETUP.sql
└── test/, .agents/, .codex/, .claude/, project-brain/  ← dossiers de scratch / docs internes
```

### Schéma d'URL multilingue réel (après migration "Sprint 2")

| Type | Convention | Exemples |
|---|---|---|
| Pages racine | Sous-dossier `/en/`, `/fr/`, `/es/` | `/en/about.html`, `/fr/compare.html`, `/es/wiggmatch.html` |
| Home | `/en/`, `/fr/`, `/es/` (et `/` redirigé) | `/fr/index.html` |
| Pays | Slug + suffixe langue à la racine `/countries/` | `/countries/argentina-fr.html` |
| Chroniques thématiques | Slug + suffixe langue à la racine `/chronicles/` | `/chronicles/chronicle-digital-nomad-visas-2026-en.html` |
| Chroniques villes | Sous-dossier `/chronicles/villes/` | `/chronicles/villes/chronicle-mexico-city-mexico-fr.html` |
| Chroniques 1966 | Sous-dossier `/chronicles/1966/` | `/chronicles/1966/chronicle-1966-france-fr.html` |
| Landing pages | `/lp/` slug-langue | `/lp/vivre-bali-budget-fr.html` |
| Lead magnets | `/lead-magnet/` slug-langue (noindex) | `/lead-magnet/visas-2026-fr.html` |
| Compare statique | `/compare/static/<pair>/index.html` | `/compare/static/france-vs-portugal/index.html` |

**Note importante : le repo conserve les anciennes pages racine** (`/about.html`, `/compare.html`, `/wiggmatch.html`, `/chronicles-*.html`, etc.). Les règles Netlify dans `_redirects` les redirigent en `301!` vers leur équivalent langue (par défaut `/en/`, sauf `chronicles-*` → `/fr/` et `wiggmatch.html` → `/fr/`). Le `301!` (bang) force la redirection même si le fichier existe. La racine `/` utilise Accept-Language : `Language=fr` → `/fr/` (302), `Language=es` → `/es/` (302), sinon `/en/` (301).

---

## 3. Inventaire contenu (comptes réels obtenus par commande)

### Pages racine
- **14 pages racine traduites par langue** (about, chronicles-dest, chronicles-family, chronicles-horizons, chronicles-villes, chronicles-visas, compare, confirmation, globe, index, indexchronicles, privacy, terms, wiggmatch).
- **TOTAL** : 14 × 3 = **42 pages racine** (vs. 14 fichiers legacy encore à la racine et redirigés).

### Pays
- **161 pays** (clés dans `data/countries.json`)
- **161 pages × 3 langues = 483 pages pays** + `country.html` (template dynamique legacy) = **484 fichiers `.html` dans `/countries/`**.
- Hero images : 161 paires `.jpg`/`.webp` dans `/assets/`.

### Chroniques
| Famille | Séries uniques | Pages totales |
|---|---|---|
| Thématiques racine `/chronicles/*.html` | 25 | 75 (25×3 langues) |
| Villes `/chronicles/villes/` | 76 | 228 (76×3) |
| Anniversaire 1966 `/chronicles/1966/` | 4 | 12 (4×3) |
| **TOTAL chroniques** | **105** | **315** |

→ confirmé par `sitemap-chronicles.xml` : 315 `<loc>`.

### Compare
- `compare.html` racine (page dynamique avec `?c=`) — encore présente, redirigée 301 vers `/en/compare.html`.
- `/en/compare.html`, `/fr/compare.html`, `/es/compare.html`.
- **64 pages compare statiques** dans `/compare/static/<pair>/index.html` (paires pays présélectionnées comme "France vs Portugal").

### Landing pages
- **3 LP × 3 langues = 9 pages** dans `/lp/` :
  - `erasmus-prague-budget-*`
  - `visa-mm2h-malaisie-*`
  - `vivre-bali-budget-*`

### Lead magnets / Ebook
- **1 lead magnet trilingue** : `/lead-magnet/visas-2026-{en,fr,es}.html` ("Les 25 meilleurs visas 2026").
- **Statut** : pages HTML standalone, conçues comme un guide complet en ligne (cover stylée + chapitres). **Pas de fichier PDF dans le repo** (recherche `*.pdf` : 0 résultat). À confirmer si un PDF est servi ailleurs (CDN, Buttondown) ou si l'ebook est uniquement la page HTML.

### Séries éditoriales identifiées (chronicles thématiques)
- **2056** : "Where will life be best in 30 years?" (3 langues)
- **Africa expat** : 4 parties × 3 langues
- **Amériques** : 3 parties × 3 langues
- **Asia / Asie expat** : 2 parties × 3 langues
- **Australia / Australie expat**
- **Digital nomads / Visas digital nomads / Crypto expats** (2026)
- **Retirement / Visas jubilacion / Visas retraite**
- **Study abroad / Estudiar / Étudier** : multi-parties (Europe Erasmus, Asia-Pacific, Americas-Africa, guide pratique)
- **Healthcare / Salud / Santé expats**
- **Forgotten countries / Países olvidados / Pays oubliés** d'expatriation
- **Property abroad / Propiedad extranjero / Immo étranger**
- **Raise children / Criar hijos / Élever enfants**
- **Expat work visas / Visas expatriacion / Visas expatriation durable**
- **Ready to leave / Listo para partir / Prêt à partir**
- **1966** (chronicle historique) : 4 pays (France, Angleterre, Iran, Japon) × 3 langues

### Sitemap (compté `<loc>`)
| Sitemap | URLs |
|---|---|
| `sitemap-roots.xml` | 61 |
| `sitemap-countries.xml` | 484 |
| `sitemap-chronicles.xml` | 315 |
| `sitemap-compare.xml` | 64 |
| **TOTAL** | **924** |

---

## 4. Données

### Fichiers sources principaux

| Fichier | Rôle | Notes |
|---|---|---|
| `data/countries.json` | Données canoniques 161 pays — champs `fields.{min_wage, avg_salary, doctor_salary, rent_studio, electricity, water, mobile, beer, coffee, dish, gas, vat, income_tax, smallbiz, iphone, samsung, immigration, happiness, sun, health, ...}` + `seo`, `hero`, `wigg`, `aliases` | Source pour compare/country pages |
| `data/countries.fr.json` / `countries.es.json` | Mêmes clés, descriptions traduites | Même nombre de lignes (21813) — schéma identique |
| `data/details/<slug>.json` × 160 | Détails enrichis (article éditorial markdown, expat score, snapshot, goDeeper) | EN |
| `data/details-fr/<slug>.json` × 160 | idem FR | |
| `data/details-es/<slug>.json` × 160 | idem ES | |
| `data/_template.details.json` | Schéma de référence du `details/<slug>.json` (meta, presentation, climate, housing, work, visa, health_lifestyle, transport, society, …) | |
| `data/map/countries2.json` | Variante "v2" du countries.json (utilisée par carte ?) — sample présent en tête | Schéma proche mais différent (subtitle différent) ; peut être un fork éditorial ou ancien fichier |
| `data/map/world.geojson` | Geometries pays pour la carte | |
| `data/map/countries_index.json` / `geo-by-slug.json` / `timezones-by-slug.json` | Index auxiliaires | |
| `data/i18n/{fr,es}/` | **Dossiers vides** dans ce snapshot (à confirmer si attendus ou rebut) | |

### Schéma type d'un `details/<slug>.json`
Clés racine : `country`, `name_note`, `expat_score`, `snapshot{capital, population, languages, driving_side}`, `article` (markdown enrichi avec emojis et placeholders `[[MAP]]`), `goDeeper{national_dish, lgbt_acceptance, top_sectors, things_to_know{personality, cards[]}}`.

### Doublons / bugs de données présents dans le repo

1. **6 fichiers stagés pour suppression (status `D`)** :
   - `data/details/dominican-republic (1).json` + `data/details/irland.json`
   - `data/details-fr/dominican-republic (1).json` + `data/details-fr/irland.json`
   - `data/details-es/dominican-republic (1).json` + `data/details-es/irland.json`
   - → fichiers supprimés sur disque mais suppression non encore commitée.
   - Le doublon "dominican-republic (1)" venait probablement d'un re-download ; `irland` est une faute de frappe (le bon est `ireland`).

2. **Incohérence countries.json vs details/** :
   - `countries.json` contient **161 clés** : la clé orpheline est **`santo-domingo`** (sans fichier dans `details/`).
   - `details/` n'a **aucun pays** que `countries.json` ignore.
   - → Soit `santo-domingo` est un alias éditorial qui devrait être merged dans `dominican-republic`, soit il manque un fichier `details/santo-domingo.json`.

3. **Fichier orphelin** : `data/details/afghanistan.html` (un .html dans un dossier de JSON) — probablement un rebut.

4. **Variantes d'images** : `/assets/` contient `hero-cote-d-ivoire.jpg` ET `hero-cote-divoire.jpg`, `hero-czech.jpg` ET `hero-czech-republic.jpg`, `hero-france.jpg` ET `Hero-france.jpg` (casse différente). Risque de collisions selon le système de fichiers.

---

## 5. Funnel & marketing

### Câblage actuel

| Outil | État | Détails |
|---|---|---|
| **Meta Pixel** | **Live** | ID `867064843065581` chargé via `data/header.js`. Respecte le consent : se déclenche après `localStorage.wigg_consent === 'accepted'` ou event `wigg_consent_granted`. Expose `window.wmTrackEvent(name, params)`. |
| **GTM / GA4** | **Live** | Container `GTM-K4MMRD4R` inline dans `<head>` de chaque page racine + page pays. Consent mode v2 (denied par défaut). |
| **Buttondown (newsletter)** | **Câblé** : CSP autorise `buttondown.email` + `api.buttondown.email`, et le formulaire est intégré dans `wiggmatch.html` (et probablement injecté par `data/footer.js`). **À confirmer** : pas trouvé dans les sources HTML statiques de `en/index.html`, `fr/index.html`, `es/index.html` (donc soit injecté à l'exécution, soit absent de la home — à vérifier en prod). |
| **Email de bienvenue** | À confirmer : le `SETUP_EMAIL_AND_PIXEL.md` (4358 octets) documente le setup mais n'a pas été lu dans ce snapshot. |
| **Formulaires Netlify** | **Live** : `newsletter` + `correction` déclarés dans `/forms.html` (cachée, `noindex`). Présents aussi sur 7+ pages (LP, wiggmatch). |
| **Sitemap** | **Live** : 924 URLs réparties en 4 sous-sitemaps via un sitemap-index. `lastmod` 2026-05-05. |
| **Pixel events tracking** | `window.wmTrackEvent(name, params)` exposé, mais on n'a pas audité quels events sont fire-and-forget. |

### Lead magnet funnel
- 3 pages LP (Bali, Erasmus Prague, MM2H Malaisie) servent de captures email avec form Netlify.
- 1 lead magnet "25 visas 2026" est en page HTML standalone `noindex` — à confirmer si délivré par lien direct, par email post-opt-in, ou downloadable.

---

## 6. SEO

### État du câblage

| Élément | État | Détails |
|---|---|---|
| **Canonical** | OK sur toutes les pages auditées (countries, chronicles, lp, lead-magnet, compare, home). | Sur la home `index.html` racine, `canonical` pointe vers `https://wiggmap.com/` (la home dans `/en/`, `/fr/`, `/es/` a son propre canonical vers `/en/`). |
| **Hreflang** | OK trilingue (en/fr/es + `x-default → en`) sur countries, chronicles, lp, lead-magnet, lang-roots. | À confirmer pour `globe.html`, `confirmation.html`, `mon-compte.html`, `forms.html`, `onboarding.html`. |
| **sitemap.xml** | Sitemap-index avec 4 sous-sitemaps. 924 URLs au total. | Voir §3. |
| **robots.txt** | Disallow `/data/`, `/template_chronicles.html`, `/mon-compte.html`, `/onboarding.html`, `/forms.html`, `index.html.bak/.old`. Allow explicite `/en/`, `/fr/`, `/es/`. Sitemap pointé. | |
| **Breadcrumbs JSON-LD** | OK sur countries (vérifié argentina-fr.html) et chronicles. | À confirmer sur about/wiggmatch/lp/lead-magnet. |
| **JSON-LD** | Présent partout : WebSite + Organization (home), Article (countries, chronicles), FAQPage (LP, chronicles villes), WebApplication (compare). | |
| **Schema BreadcrumbList** | Présent sur countries et compare. | |
| **og:image / og:title** | Présents sur toutes les pages auditées. | |
| **GSC verify** | Fichier `googleaee6c9fba1b1be46.html` présent à la racine. | |

### Trous SEO détectés

1. **`compare.html` racine** : `canonical` pointe vers `https://wiggmap.com/compare.html` — qui est redirigé 301 vers `/en/compare.html`. Canonical pointant vers une URL redirigée. À aligner. *(Ce comportement est masqué par la redirection forcée 301! côté Netlify.)*

2. **Home racine `index.html`** (111 KB, tunnel design) : ses `<link rel="alternate" hreflang>` pointent tous vers `https://wiggmap.com/` au lieu de `/en/`, `/fr/`, `/es/`. **Mais** ce fichier est sans doute mort en prod (voir §9) car `/` est redirigé via Accept-Language.

3. **`noindex,follow` sur `/fr/index.html` et `/es/index.html`** : encore présent dans le HTML alors que le commit `60f98ef` ("drop untranslated-banner") suggérait que la home FR/ES allait sortir de noindex. À reconfirmer si volontaire ou résidu.

4. **`countries.json` orphan** : `santo-domingo` n'a pas de fichier `details/`, donc pas de page pays statique → l'index pays doit gérer le cas.

5. **Doublons d'image hero** (`hero-cote-d-ivoire.jpg` vs `hero-cote-divoire.jpg`, etc.) — risque que les pages pointent vers des slugs différents en fonction de la langue/source.

6. **`google G-36BWEJGCTB`** présent uniquement sur `countries/country.html` (page dynamique) → on a un mélange GTM (sur 100% du site) + un gtag direct (sur cette seule page). À confirmer si intentionnel (double tracking ?).

---

## 7. Design system

### Tokens (`/assets/wm-tokens.css`, 147 lignes)

Source de vérité du design system, créée au Sprint Y.1 (commit `a1e26e2`). Documente les arbitrages :
- D1 cream : `#f5f0e8` + gradient `#f9f5ed → #f3ede3`
- D2 font UI : Inter canonical (Instrument Sans seulement sur wiggmatch — exception documentée)
- D3 : purge Poppins → Inter
- D4 CTA bright : `#22c55e` (Tailwind green-500)
- D5 compare : palette `compare/static` laissée off-charter (Sprint Y' à venir)
- D6 : Source Serif préservé pour le long-form chronicles
- D7 : script de regen `scripts/migrate_country_to_tokens.py` (idempotent)
- D8 : six PRs distincts Y.1…Y.6

### Variables principales
- **Brand** : `--green: #1a5430` (forest canonical), `--green-dark`, `--green-light`, `--green-tint`
- **CTA** : `--cta-bright: #22c55e`, `--cta-bright-hover: #16a34a`, `--ink-on-cta: #0a1f10`
- **Surfaces** : `--bg: #f5f0e8`, `--paper: #fffdf8`, `--paper-2`, `--rule`, `--line`
- **Ink** : `--ink: #171714`, `--ink-soft`, `--ink-muted`, `--ink-ghost`, `--ink-dark`
- **Fonts** : `--font-display` (Fraunces), `--font-ui` (Inter), `--font-brand-italic` (Cormorant Garamond), `--font-chronicle-body` (Source Serif)
- **Spacing** : `--space-1` à `--space-16` (T-shirt sizing 4–64 px)
- **Radii** : `--radius-xs` (2px) … `--radius-pill` (999px)
- **Shadows** : `--shadow-sm/md/lg/cta`
- **Z-index** : `--z-skip-link`, `--z-header`, `--z-modal`, `--z-toast`

### Système de couleurs par catégorie de chronique
Convention `<meta name="theme-color" content="#X" data-category-color="Y">` :
- `family` → `#d7731d` (orange chaleureux)
- `horizons` → `#7d55d8` (violet exploration)
- `villes` / `dest` / `visas` → `#1a5430` (forest)
- `city-*` (chroniques individuelles de villes) → **palette per-city** (chaque ville override `:root` localement — convention documentée en memory `city-chronicles-format.md`, NE PAS homogénéiser)

### `data/header.js` (rôle)
- Injecte la navbar (logo, links lang-aware, sociaux, burger menu).
- Détecte la langue : URL d'abord (`/en/`, `/fr/`, `/es/`, ou suffixe `-{en|fr|es}.html`), puis `localStorage.wigg_lang`, puis fallback `en`.
- Expose `window.WM_LANG`.
- Charge le **Meta Pixel** après opt-in cookie.
- Charge Supabase (référence dans le code) pour la pastille auth.

### `data/footer.js` (rôle)
- Injecte le footer (copyright + liens Terms/Privacy lang-aware + bouton "Cookies").
- Probablement injecte aussi le cookie banner et le formulaire newsletter (Buttondown), à confirmer (head des 60 premières lignes seules lues).

### Protocole de modif
- Le commit Sprint Y déclare que `header.js` et `footer.js` sont des **fichiers fragiles** (cf. `_headers` qui leur applique un cache court 1h pour tolérer les updates rapides).
- L'audit AUDIT.md mentionne explicitement comme contrainte : "data/header.js et data/footer.js non touchés".
- → **Convention** : ces fichiers doivent être modifiés avec précaution, idéalement isolément, car ils sont chargés par toutes les pages.

---

## 8. WiggMap Connect

### Fichiers présents (`/connect/`)

| Fichier | Lignes | Rôle |
|---|---|---|
| `index.html` | (~?) | Landing principale de Connect (FR par défaut, theme dark `#060d08`, accent vert `#1dd876`). |
| `feed.html` | 471 | Flux principal (feed/posts) |
| `swipe.html` | 399 | Vue swipe (probablement comme un Tinder pays/expats) |
| `group.html` | 630 | Vue groupe |
| `profile.html` | 966 | Vue profil utilisateur |
| `onboarding.html` | 1538 | Onboarding (probablement long parcours multi-étapes) |
| `widget.js` | 660 | **Widget commentaires** intégré dans les pages chroniques (auth Supabase Google OAuth + posts + votes "useful" + pinned). Multi-i18n EN/FR/ES. |
| `widget.css` | 78 | Styles widget |
| `assets/connect.css` / `connect.js` / `i18n.js` | — | Assets internes Connect |
| `assets/wiggmap-connect-logo.png` | — | Logo |

### Supabase (cf. `SUPABASE_SETUP.sql`)
- URL : `https://tkctreoftezvbfejhbto.supabase.co`
- Clé `sb_publishable_lAKWBnp2nbfgb2w5Uj55aQ_aD6fBWUb` hardcodée dans `connect/widget.js`.
- Tables (créées/migrées par le SQL) :
  - `profiles` : `id`, `username`, `avatar_url`, `country_origin`, `country_current`, `country_target`, `life_status`, `sector`, `languages` (jsonb), `onboarding_done` (bool), `created_at`
  - `posts` (référencée via la RPC `increment_useful(row_id uuid)` qui incrémente `useful_count`) — schéma exact non audité, mais widget.js implique `posts {slug, lang, type[temoignage|flash|question], text, useful_count, pinned_threshold=10, …}`.
- Auth : Google OAuth + email/password (trigger `handle_new_user` auto-crée le profil).
- RLS activé sur `profiles` (select all, insert/update only own).
- Mécanisme "pinned" : posts avec `useful_count >= 10` deviennent "Validé terrain".

### Codé vs prévu
- **Codé/présent** : pages UI, widget commentaires intégrable, SQL setup, traductions EN/FR/ES.
- **Statut prod** : à confirmer si Connect est branché et utilisé. Le widget commentaires est référencé dans la CSP (`*.supabase.co`, `wss://*.supabase.co`), mais pas vérifié s'il est effectivement injecté dans les pages chroniques actuellement servies.

---

## 9. Home — redesign en cours

### Trois fichiers "home" coexistent dans le repo

| Fichier | Taille | Statut | Servi en prod ? |
|---|---|---|---|
| `/index.html` (racine) | 111 KB | **Home tunnel intégrée** (nouveau design Fraunces + Instrument Sans + JetBrains Mono, scène `wm-tunnel-stage`, scrollSpacer, loader avec roulette de caractères, vignette, grain SVG, layers Z-positionnés). Inclut wm-tokens.css. Hérité des prototypes `home-tunnel.html` + `home-redesign-v2.html`. | **Probablement PAS** — voir ci-dessous. |
| `/en/index.html` | 48 KB | **Home legacy** (ancien design avec swap localStorage `wigg_lang`, sans tunnel). | **Oui** (servi pour visiteurs EN après redirection `/` → `/en/`). |
| `/fr/index.html` | 48 KB | idem legacy, traduit FR. `<meta name="robots" content="noindex,follow">` toujours présent. | **Oui** (servi via Accept-Language `Language=fr`). |
| `/es/index.html` | 48 KB | idem legacy, traduit ES. `noindex,follow` toujours présent. | **Oui** (servi via Accept-Language `Language=es`). |
| `/home-tunnel.html` | 36 KB | Prototype standalone "tunnel" (vanilla, sans Lenis/GSAP — choix volontaire après hiccup CDN qui avait laissé le loader bloqué sur écran noir). | **Non** (fichier isolé, non lié). |
| `/home-redesign-v2.html` | 48 KB | Autre prototype (utilise Lenis + GSAP + ScrollTrigger via cdn.jsdelivr). | **Non**. |
| `/test/wiggmap-home-v10.html` | — | Encore un prototype. | **Non**. |

### Diagnostic du "loader bloquant" (résolu)
- Le commit `71d0c11 fix(home-tunnel): vanilla tunnel — drop Lenis/GSAP, hard-fade loader` indique que **le tunnel chargeait Lenis et GSAP depuis cdn.jsdelivr** : un hiccup CDN ou un content-blocker laissait le tunnel non-initialisé → loader piégé sur écran noir.
- **Fix appliqué** : `home-tunnel.html` est passé en JS vanilla pur (loader force-fade après 1500 ms). Commits suivants `c8ecdef` (cascade photos + Z varié) et `c4cf48c` (hero dismissable, pas de scroll lock).
- **Statut du diagnostic** : terminé pour `home-tunnel.html`. Mais le code tunnel a aussi été intégré à la racine `/index.html` (commit `aae3118` ajoutait `home-tunnel.html`, puis les commits "update site" l'ont fusionné dans `index.html`). **Toutefois**, `/en/`, `/fr/`, `/es/index.html` n'ont PAS reçu ce nouveau design (vérifié : `grep wm-tunnel` retourne 0 occurrences).

### Quelle home est servie en prod aujourd'hui ?

```
Visiteur → https://wiggmap.com/
↓
Règle Netlify "/" :
  - si Accept-Language=fr  → 302 /fr/      → /fr/index.html  (LEGACY noindex,follow)
  - si Accept-Language=es  → 302 /es/      → /es/index.html  (LEGACY noindex,follow)
  - sinon                   → 301 /en/      → /en/index.html  (LEGACY)
```

**Conclusion** : la **home tunnel à la racine n'est jamais servie** — la redirection Netlify la court-circuite. Les visiteurs voient les anciennes homes legacy dans `/en/`, `/fr/`, `/es/`. C'est probablement **un travail en cours non encore propagé** : il faut soit dupliquer `index.html` vers `/en/`, `/fr/`, `/es/` (en localisant le contenu), soit supprimer le `index.html` racine s'il était un brouillon.

---

## 10. Scripts & outils

### Scripts Python (`/scripts/`)
| Script | Rôle | Exécution |
|---|---|---|
| `build_country_pages.py` | Génère les 161×3 pages pays statiques à partir de `data/countries*.json` + `data/details*/*.json`. | `python3 scripts/build_country_pages.py` (à confirmer) |
| `build_index_pages.py` | Génère les pages d'index. | idem |
| `build_wiggmatch_trilingual.py` | Sprint D1 : depuis le master FR, génère `/en/wiggmatch.html` et `/es/wiggmatch.html` et sync `/fr/`. | idem |
| `gen_sitemap.py` | Régénère les 4 sitemaps + sitemap-index. | idem |
| `inject_cities_section.py` | Sprint #13 : injecte une section "Cities in {country}" sur 51 pages pays. | one-shot |
| `migrate_chronicles_to_tokens.py` | Sprint Y.4 : migre 75 chroniques thématiques vers `wm-tokens.css`. | one-shot |
| `migrate_country_to_tokens.py` | Sprint Y.3 : migre 484 pages pays. Marqué idempotent. | one-shot ou re-runnable |
| `migrate_hero_to_picture.py` | Sprint Y.5 : remplace `<img hero>` par `<picture>` SSR. | one-shot |
| `migrate_to_lang_dirs.py` | Sprint 2 : migre pages racine vers `/en/`, `/fr/`, `/es/`. | one-shot |
| `migrate_villes_to_tokens.py` | Sprint Y.6 : migre 228 chroniques villes. | one-shot |
| `monitor_post_merge.py` | Sondage post-merge : ~50 URLs critiques (200 OK, redirects 301, canonical/hreflang corrects, SW v3, etc.) | `python3 scripts/monitor_post_merge.py` (CI-friendly : exit 1 si fail). Permet `--base` pour tester un deploy-preview. |
| `optimize-images.sh` | Re-encodage des assets en WebP. | shell |

### Outils racine
| Script | Rôle |
|---|---|
| `_gen_v3.py` (79 KB) | **Générateur trilingue de paragraphes de contexte + enrichissement details/** pour 26 pays "hot" (Thailand, Vietnam, Portugal, …). Construit des dictionnaires `NAME_FR`, `NAME_ES` et produit du texte naturel à partir des champs structurés. |
| `template_chronicles.html` | Template de chronique vide (référence pour copier-coller). |

---

## 11. Git

### Branche & remote
- Branche courante : **`main`** (HEAD `7e3bf67`, "update site")
- Remote : `https://github.com/wiggmap/wiggmap.git`

### Workflow PR / Netlify utilisé
- Workflow : branche sprint → deploy preview Netlify → PR vers main → squash merge → monitor `python3 scripts/monitor_post_merge.py` post-merge.
- 15 PRs mergées au total (#1 à #15).

### Branches ouvertes (non mergées dans main)
- **`sprint-home-redesign`** (HEAD `8546e2b`, 2026-05-05) — "immersive editorial redesign — single-page sprint"
- **`sprint-home-redesign-prototypes`** (HEAD `8f5c803`, 2026-05-05) — "fix(home protos): convert absolute paths to relative"
- **`sprint-home-tunnel`** (HEAD `aae3118`, 2026-05-06) — "feat(home): add 3D tunnel home prototype" *(commits suivants sur main : `71d0c11`, `c8ecdef`, `c4cf48c`, `60f98ef`, `0cdaea5`, `48e08f6`, `7e3bf67` — la branche tunnel a été partiellement reportée sur main directement, sans PR récente)*

### Derniers commits sur `main` (les 20 plus récents, condensés)
```
7e3bf67 update site
48e08f6 update site
0cdaea5 update site
60f98ef chore(i18n): drop untranslated-banner from /fr/ and /es/ home
c4cf48c polish(home-tunnel): kill the trap — dismissable hero, no scroll lock
c8ecdef fix(home-tunnel): photo cascade, hero entrance, varied Z rhythm
71d0c11 fix(home-tunnel): vanilla tunnel — drop Lenis/GSAP, hard-fade loader
aae3118 feat(home): add 3D tunnel home prototype (sprint-home-tunnel)
7261ce1 fix(redirects): route / based on Accept-Language (FR → /fr/, ES → /es/, else /en/)
40505e4 fix(monitor): handle sitemap-index format (#15)
22320c6 sec: enforce CSP (#14)
4942d07 feat(countries): "Cities in {country}" section on 51 pages (#13)
ae3e5ea seo: split sitemap by section + image sitemap (#12)
5a12362 tools(monitor): Y.5 perf + compare-paths regression gates (#11)
eda6f75 chore: cleanup repo (#10)
9fdfb9b hotfix: compare.html relative paths breaking on /en/, /fr/, /es/
c4f0b19 feat(chronicles-villes): adopt tokens.css (Y.6) (#9)
7d1816e perf(images): <picture> SSR + opt-out runtime swap (Y.5) (#8)
b1ef935 feat(chronicles): adopt tokens.css thematic × 75 (Y.4) (#7)
1c791a2 feat(countries): adopt tokens.css × 484 (Y.3) (#6)
```

### État de travail non-commit (uncommitted)
```
M  compare.html               ← ajout d'un script noindex,follow pour URL sans params
M  countries/country.html     ← ajout du même script + refonte du bloc "Related Chronicles" (CHRONICLES._index)
D  data/details/dominican-republic (1).json
D  data/details/irland.json
D  data/details-fr/dominican-republic (1).json
D  data/details-fr/irland.json
D  data/details-es/dominican-republic (1).json
D  data/details-es/irland.json
```

→ Les 6 suppressions sont du nettoyage de doublons / fautes de frappe (cf. §4). Les 2 modifications semblent être des hotfix SEO (anti-indexation des pages sans paramètre `?country=` ou `?c=`).

---

## 12. Bugs & pièges connus (à savoir avant de toucher au repo)

### Conventions strictes à respecter

1. **`data/header.js` et `data/footer.js` sont des fichiers chargés par TOUTES les pages**. Toute modif casse tout le site → tester localement avant push. Les SPRINT_*.md et AUDIT.md les marquent explicitement comme "non touchés" durant les audits.

2. **`scripts/migrate_*.py` ne sont PAS tous idempotents** : seul `migrate_country_to_tokens.py` est marqué idempotent. Les autres sont des one-shots → ne pas re-lancer après un sprint terminé.

3. **`compare.html` racine** : la PR #11 (hotfix `9fdfb9b`) a corrigé un bug où les chemins relatifs cassaient quand `compare.html` était servi depuis `/en/`, `/fr/`, `/es/`. **Toujours utiliser des chemins absolus `/assets/...` dans `compare.html`**, et une gate de monitor existe (`monitor_post_merge.py` valide les chemins absolus).

4. **Service Worker** : `sw.js` est en v3 (`CACHE_NAME = "wiggmap-v3"`). Toute migration de structure d'URL exige de **bumper la version** + purger les anciens caches. Le SW est en network-first pour HTML/JSON (donc pas de cache fantôme) mais le manifest doit toujours être à jour.

5. **Service Worker cache-busting** : commit explicite "bumped v2 → v3 to invalidate caches that hold the legacy non-trilingual root structure". → après une migration majeure, ne pas oublier le bump.

6. **`countries/country.html`** : page dynamique avec `?country=` qui doit rediriger / noindex si vide. Le script anti-indexation des params vides est en cours d'ajout (vu dans `git diff`).

7. **Images hero** : variantes orthographiques (`hero-cote-d-ivoire.jpg` vs `hero-cote-divoire.jpg`, etc.) → bien vérifier le slug exact attendu par le HTML.

8. **`countries.json` orphan `santo-domingo`** : si on génère les pages pays, cette clé n'a pas de fichier `details/` → casse potentielle du builder.

9. **CSP enforcée (pas Report-Only)** depuis PR #14 : toute nouvelle origine externe (CDN, API, font) doit être ajoutée dans `_headers` Content-Security-Policy ou la page sera bloquée.

10. **Memory "chronicles language switching" (voir `MEMORY.md` index)** : il existe un bug récurrent où le switcher de langue ne fonctionne pas sur certaines pages chroniques → vérifier sur **toutes** les pages chronicles après tout changement de header.js / footer.js / nav.

11. **Chroniques villes per-city palettes** : chaque chronique de ville a sa propre `:root` scoped palette. **Ne PAS uniformiser** — c'est intentionnel pour donner une identité par ville (cf. memory `city-chronicles-format.md`).

12. **Branche "sprint-home-tunnel"** : sa work s'est répandue directement sur main (commits `71d0c11` → `7e3bf67`) sans PR. La branche elle-même est "en retard" sur main. Risque de conflits si on rebase ; clarifier le statut avant de toucher.

### Corruptions / hotfixes du passé
- PR #11 `9fdfb9b` : "compare.html relative paths breaking on /en/, /fr/, /es/" — hotfix d'urgence.
- PR #15 `40505e4` : "fix(monitor): handle sitemap-index format" — PR #12 avait converti `sitemap.xml` en sitemap-index, ce qui cassait le monitor.
- Doublons `irland.json` (faute) + `dominican-republic (1).json` (re-download) : nettoyage en cours.

---

## 13. État réel vs roadmap

### Grands chantiers

| Chantier | Statut | Notes |
|---|---|---|
| Trilinguisme racine (`/en/`, `/fr/`, `/es/`) — pages racine | ✅ Fait (Sprint 2, PR #1) | 14 pages × 3 langues. Anciennes pages racine encore présentes pour les `301!`. |
| Trilinguisme `/wiggmatch.html` | ✅ Fait (Sprint D1, PR #2) | Build script + monitor coverage. |
| Trilinguisme LP + lead-magnet | ✅ Fait (Sprint X, PR #3) | 9 LP + 3 lead-magnets. |
| Design tokens canonical (`wm-tokens.css`) | ✅ Fait (Sprint Y.1, PR #4) | |
| Migration root pages → tokens | ✅ Fait (Sprint Y.2, PR #5) | 54 pages root. |
| Migration country pages → tokens | ✅ Fait (Sprint Y.3, PR #6) | 484 pages. |
| Migration chronicles thématiques → tokens | ✅ Fait (Sprint Y.4, PR #7) | 75 chroniques. |
| `<picture>` SSR + WebP runtime opt-out | ✅ Fait (Sprint Y.5, PR #8) | Country pages. |
| Migration chronicles villes → tokens | ✅ Fait (Sprint Y.6, PR #9) | 228 villes. |
| Section "Cities in {country}" injectée | ✅ Fait (PR #13) | 51 pays. |
| Sitemap éclaté + image sitemap | ✅ Fait (PR #12) | 4 sitemaps + index. |
| CSP enforced (was Report-Only) | ✅ Fait (PR #14) | |
| Monitor post-merge | ✅ Fait | ~50 URLs auditées CI-friendly. |
| Cleanup repo (backups, pycache, branches obsolètes, .gitignore) | ✅ Fait (PR #10) | |
| Routing langue à `/` via Accept-Language | ✅ Fait (commit `7261ce1`) | 302 conditionnels + 301 default. |
| **Home tunnel "redesign"** | 🔶 En cours | Intégrée dans `index.html` racine (jamais servi en prod). **PAS encore propagée vers `/en/`, `/fr/`, `/es/`**. |
| Home "untranslated banner" sur `/fr/` et `/es/` | ✅ Retiré (commit `60f98ef`) | Mais `noindex,follow` toujours présent. |
| Dédup `dominican-republic (1)` + faute `irland` | 🔶 En cours | Stagé pour suppression, non commité. |
| Anti-indexation `compare.html?` / `country.html?` vides | 🔶 En cours | Script injecté en modif locale, non commité. |
| Refonte design `compare.html` | 🔲 Prévu (item Sprint Y' du AUDIT.md) | Palette compare/static laissée off-charter. |
| Sprint Z (cf. SPRINT_Z_PLAN.md + SPRINT_Z_REDUCED_PLAN.md) | 🔲 État indéterminé | Documents présents, contenu non audité. |
| **WiggMap Connect** | 🔶 Codé, statut prod à confirmer | Pages UI + widget + Supabase setup présents ; pas vérifié si Connect est branché en prod. |
| Newsletter Buttondown sur home | ❓ À confirmer | Allowlist CSP + form sur wiggmatch.html, mais pas trouvé dans `en|fr|es/index.html` statique (peut être injecté par footer.js). |
| Page Ebook PDF téléchargeable | ❓ À confirmer | Lead-magnet est HTML uniquement dans le repo, pas de PDF. |
| Sprint X, Y, Z documentation détaillée | ✅ Présent | `SPRINT_X_PLAN.md`, `SPRINT_Y_PLAN.md`, `SPRINT_Z_PLAN.md`, `SPRINT_Z_REDUCED_PLAN.md` (non lus dans ce snapshot). |

### Ce qui débloque le plus de valeur maintenant (recommandations top-down)

1. **Trancher la home tunnel** — soit la propager à `/en/`, `/fr/`, `/es/` (et générer des variantes traduites), soit la retirer du `index.html` racine. Actuellement, du code mort à la racine + du travail récent invisible pour les visiteurs.

2. **Lever le `noindex,follow` sur `/fr/index.html` et `/es/index.html`** — depuis le commit "drop untranslated-banner", ces homes ne sont plus en EN brut, elles sont traduites. Le `noindex` les empêche d'apparaître sur Google FR et Google ES → perte directe de SEO local. (Vérifier que c'est bien le moment.)

3. **Commiter le nettoyage data** (`dominican-republic (1)` + `irland`) et résoudre **`santo-domingo`** (alias éditorial ou fichier manquant). Sinon le builder de pages pays peut casser silencieusement.

4. **Finaliser le hotfix d'anti-indexation `compare.html` / `country.html`** (déjà en modif locale) et le commiter. Évite que les pages "vides" (sans param) se retrouvent dans l'index Google.

5. **Statut Connect : décider si on déploie ou si on parke**. C'est ~5000 lignes de code (incluant Supabase + widget commentaires) qui dormiraient sans monitoring. Si on garde, brancher le widget sur les chroniques (au moins une série) et tester un cycle complet auth → post → vote.

---

## 14. Questions ouvertes / décisions en attente

1. **Home tunnel** : doit-elle remplacer la home legacy dans les 3 langues, ou rester un prototype ? Si oui, qui prend en charge la traduction du contenu hero (FR, ES) ?

2. **`noindex,follow` sur `/fr/` et `/es/` home** : décision marketing à prendre — soit on les laisse en `noindex` tant que le redesign n'est pas validé, soit on les indexe maintenant pour capter du trafic FR/ES rapidement.

3. **`santo-domingo` vs `dominican-republic`** : alias éditorial à fusionner, ou pays séparé à compléter avec ses propres `details/`?

4. **`compare.html` legacy à la racine** : à supprimer ou garder ? Le `_redirects` (`301!`) la masque, mais elle reste sur disque et consomme un slot SEO en doublure.

5. **Compare design refonte (Sprint Y')** : prioritaire ? Le AUDIT.md y faisait référence comme dette structurelle.

6. **WiggMap Connect** : MVP à lancer publiquement ou pas ? Quel est le funnel ? Quelle relation avec wiggmatch (qui est aussi un "matching" pays) ?

7. **`countries/country.html` (page dynamique)** : encore utilisée ? Les pages statiques `countries/<slug>-{lang}.html` couvrent les 161 pays. La dynamique semble redondante.

8. **`_gen_v3.py`** : statut ? Il ne couvre que 26 pays hot — est-ce un fichier de R&D ou de prod ?

9. **Ebook PDF** : doit-on produire un vrai PDF pour `lead-magnet/visas-2026`, ou est-ce que la version HTML suffit ?

10. **Memory "chronicles language switching" récurrent** : la racine du bug a-t-elle été identifiée ou est-on en mode "à surveiller manuellement à chaque sprint" ?

11. **Sprint Z / Sprint Z Reduced** : quel est le scope actif, et est-il toujours d'actualité ?

12. **Double tracking** sur `countries/country.html` (GTM + gtag `G-36BWEJGCTB` direct) : intentionnel ou résidu ?

13. **`data/i18n/{fr,es}/` vides** : à supprimer, ou destinés à un futur système d'i18n key/value ?

14. **Branches `sprint-home-redesign` + `sprint-home-redesign-prototypes`** : à fusionner, à archiver ou à supprimer ?
