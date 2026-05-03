# WiggMap — Audit complet (2026-05-03)

> **Mode** : audit non-destructif. Aucun fichier modifié.
> **Contraintes respectées** : `data/header.js` et `data/footer.js` non touchés.
> **Périmètre lu** : `index.html`, `indexchronicles.html`, `wiggmatch.html`, `compare.html`, `globe.html`, `about.html`, échantillon `countries/*`, `chronicles/*`, `chronicles/villes/*`, `lp/*`, `lead-magnet/*`, `data/header.js` (extraits), `data/footer.js`, `sitemap.xml` (résumé), `robots.txt`, `manifest.webmanifest`, `sw.js`, `_redirects`, `connect/widget.js`, `project-brain/*`.
> **Volumétrie** : 484 pages pays (3 langues × 161), 228 chroniques villes (3 × 76), 75 chroniques thématiques, 64 pages compare statiques, 9 LP, 894 URLs au sitemap (506 KB).

---

## Synthèse exécutive

WiggMap a une base technique solide (PWA, sitemap exhaustif, hreflang correct sur les pages pays et chroniques, FAQPage schema sur 100 % des chroniques, Article schema partout, GTM + consent mode v2 conformes). **Les trois leviers majeurs non exploités** sont : (1) la **homepage est servie sur une seule URL pour les 3 langues**, ce qui sabote l'indexation trilingue racine ; (2) le **design system a divergé** en 6+ verts, 6+ fonts display, 5+ valeurs cream — dilution de marque ; (3) les **hero JPG pays pèsent 2–3 MB** alors que les `.webp` existent — LCP mobile catastrophique sur les 484 pages pays.

Les corrections à plus fort levier sont concentrées dans une dizaine d'opportunités à ratio > 3 listées ci-dessous. Les vraies dettes structurelles (tokens CSS partagés, refonte compare.html, pillar content, hubs SEO) sont plus chères mais conditionnent la trajectoire à 6 mois.

---

## Légende

- **Impact** (1–10) : combinaison user × SEO × revenu, attribution explicitée par opportunité.
- **Effort** (heures, converti en score 1–10 : 1 = ≤2 h, 3 = ½ journée, 5 = 1 jour, 8 = 1 semaine, 10 = >2 semaines).
- **Ratio** = Impact ÷ Effort (score). Plus le ratio est élevé, plus le levier est actionnable.

---

## Top 12 quick wins (ratio ≥ 3)

| # | Opportunité | Impact | Effort | Ratio |
|---|---|---|---|---|
| 1 | Hero `bc.webp` (278 KB) au preload au lieu de `bc.png` (2.9 MB) | 8 | 1 | **8.0** |
| 2 | JSON-LD manquants sur `about.html`, `wiggmatch.html`, `compare.html` | 6 | 1 | **6.0** |
| 3 | `lang` attribute HTML statique aligné sur le contenu réel | 5 | 1 | **5.0** |
| 4 | Canonical normalisé sur `compare.html` (paramètre `?c=` qui multiplie les URLs) | 5 | 1 | **5.0** |
| 5 | `<link rel=preload as=image fetchpriority=high>` du hero LCP par page pays | 7 | 2 | **3.5** |
| 6 | `content-visibility:auto` sur `.country-grid`, `.city-grid`, `.chron-grid` | 4 | 1 | **4.0** |
| 7 | Skip-to-main-content link injecté dans le DOM avant `#siteHeader` | 4 | 1 | **4.0** |
| 8 | Compare.html : passer en chemins absolus `/assets/`, `/css/main.css` | 4 | 1 | **4.0** |
| 9 | Hreflang complet sur `wiggmatch.html` / `compare.html` / `about.html` / `globe.html` | 6 | 2 | **3.0** |
| 10 | `_headers` Netlify avec CSP, X-Frame-Options, Referrer-Policy, Permissions-Policy | 6 | 2 | **3.0** |
| 11 | `theme-color` unifié `#1a5430` partout (HTML + manifest) | 3 | 1 | **3.0** |
| 12 | Cron mensuel `optimize-images.sh` étendu à `assetscity/` (170 fichiers, 4 PNG > 3 MB) | 6 | 2 | **3.0** |

> Les 12 premiers tiennent en **~2 jours de dev cumulés** et adressent : LCP, indexation tri-langue, sécurité, conformité accessibilité de base.

---

## Détail par axe

### 1. SEO technique

#### 1.1 Homepage trilingue inexistante (URL unique)
**Description.** `index.html` sert les 3 langues sur la même URL `https://wiggmap.com/`. Les 3 `<link rel="alternate" hreflang>` pointent tous vers `/`. Le `<html lang="fr">` est codé en dur, le `<title>` initial est anglais, et le contenu visible est traduit côté JS depuis `localStorage`. Conséquences : Google n'indexe qu'une seule version (langue selon premier crawl), ne distingue pas les 3 marchés, et passe à côté du linguistic targeting Search Console. Le problème est aggravé par le fait que toutes les pages internes (countries, chronicles) **ont** des URLs par langue : la racine est un trou noir SEO au sommet de l'arborescence.
**Fichiers.** `/index.html` (lignes 2, 4, 8, 11–13, 24, 696, 698) ; nouveau : `/index-fr.html`, `/index-es.html` ou redirect `/?lang=fr → /fr/`.
**Impact.** SEO **+** (le plus gros levier d'acquisition organique non exploité, racine du graph) ; user neutre (le switcher continue à fonctionner) ; revenu indirect via trafic.
**Score impact** : 10 — **effort** : 6 (rebrancher le routing, créer 3 pages variantes, mettre à jour `_redirects`, sitemap, hreflang) — **ratio 1.67**.

#### 1.2 Hreflang manquants sur pages produits & légales
**Description.** `wiggmatch.html`, `compare.html`, `globe.html`, `about.html`, `terms.html`, `privacy.html`, `confirmation.html`, `mon-compte.html`, `onboarding.html`, `chronicles-villes.html`, `chronicles-dest.html`, `chronicles-family.html`, `chronicles-horizons.html`, `chronicles-visas.html` n'ont aucun `<link rel="alternate" hreflang>`. `indexchronicles.html` n'a que `x-default`.
**Fichiers.** Liste ci-dessus. Si les variantes par langue n'existent pas (cas wiggmatch/compare), au minimum déclarer `hreflang="x-default"` self-référent + `hreflang="en|fr|es"` pointant vers la même URL pour rendre le ciblage explicite.
**Impact.** SEO + (pages-clés du parcours : un utilisateur qui Google "compare countries cost of living" arrive sur compare.html qui est mono-langue). User neutre.
**Score impact** : 6 — **effort** : 2 — **ratio 3.0**.

#### 1.3 Canonical paramétrée sur compare.html
**Description.** `compare.html` a `<link rel="canonical" href="https://wiggmap.com/compare.html">` (ligne 9), mais l'URL réellement visitée inclut `?c=thailand,indonesia,portugal` (homepage CTA, header CTA). Combinaisons → URLs distinctes pour Google → duplication. Le canonical statique est correct, mais il faut **aussi** un `<meta name="robots" content="noindex">` conditionnel quand les paramètres sont présents OU traiter les combinaisons populaires comme pages /compare/static/{a}-vs-{b}/ (déjà 64 existantes — bon réflexe à étendre).
**Fichiers.** `/compare.html`. Optionnel : générer ~50 paires SEO additionnelles dans `/compare/static/` via `_gen_v3.py`.
**Impact.** SEO + (consolidation crawl budget). User neutre.
**Score impact** : 5 — **effort** : 1 — **ratio 5.0**.

#### 1.4 JSON-LD absent sur 4 pages-clés
**Description.** Aucun `<script type="application/ld+json">` sur `about.html`, `wiggmatch.html`, `compare.html`, `terms.html`, `privacy.html`. Or about.html est la 2ᵉ page la plus prioritaire au sitemap (`<priority>0.9</priority>`). Manquent : `Organization` ou `AboutPage` sur about, `WebApplication` ou `Quiz` sur wiggmatch, `WebApplication` sur compare.
**Fichiers.** `/about.html`, `/wiggmatch.html`, `/compare.html`.
**Impact.** SEO + (rich results, knowledge graph) ; revenu indirect.
**Score impact** : 6 — **effort** : 1 — **ratio 6.0**.

#### 1.5 Image sitemap absent
**Description.** 484 images héro pays + 170 images héro villes (≈ 650 images uniques) ne figurent pas dans `sitemap.xml`. Google Image est un canal d'acquisition non négligeable pour des requêtes "Bali skyline", "Lisbon view".
**Fichiers.** `/sitemap.xml` (étendre via `/scripts/gen_sitemap.py`). Ajouter `xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"` et un `<image:image>` par URL country/chronicle ville.
**Impact.** SEO + (trafic Google Images, surtout pour les villes).
**Score impact** : 5 — **effort** : 2 — **ratio 2.5**.

#### 1.6 Sitemap monolithique 506 KB
**Description.** `/sitemap.xml` contient les 894 URLs en un seul fichier. La spec recommande < 50 MB / 50 000 URLs (largement OK), mais la lecture est plus rapide pour Googlebot quand le sitemap est split par section (`sitemap-countries.xml`, `sitemap-chronicles.xml`, `sitemap-cities.xml`, `sitemap-compare.xml`) avec un `sitemap-index.xml` racine. Permet aussi de monitorer les sections séparément dans Search Console.
**Fichiers.** `/sitemap.xml` → `/sitemap-index.xml` + 4–5 fichiers enfants. `/scripts/gen_sitemap.py` à refactor.
**Impact.** SEO + (analytics granulaire, crawl efficiency). 
**Score impact** : 3 — **effort** : 2 — **ratio 1.5**.

#### 1.7 Lang attribute HTML incohérent
**Description.** `<html lang="fr">` sur `index.html` (titre EN), `globe.html` (titre EN), `mon-compte.html`, `onboarding.html` ; `<html lang="en">` sur `wiggmatch.html` (titre FR : "Trouve ta ville idéale"). Google utilise cet attribut comme signal langue. Sur les chronicles villes c'est correct (`-fr.html` → `lang="fr"` ✓), c'est sur les pages racine que ça déraille.
**Fichiers.** `/index.html:2`, `/globe.html:2`, `/wiggmatch.html:2`, `/mon-compte.html:2`, `/onboarding.html:2`.
**Impact.** SEO + (signal langue) ; a11y + (lecteurs d'écran).
**Score impact** : 5 — **effort** : 1 — **ratio 5.0**.

#### 1.8 Maillage interne pays↔chroniques côté JS uniquement
**Description.** Sur les pages pays, les sections "Related chronicles" et "Compare pairs" sont injectées par `country.html` JS depuis `CHRONICLES._index` / `CHRONICLES.countries` / `COMPARE_PAIRS`. Idem pour `wmRelated` (chronicles voisines, footer.js). Googlebot exécute le JS mais avec un délai, et le random shuffle dans `pickThree()` (footer.js:388) crée du contenu **non déterministe** entre crawls — les liens ne stabilisent jamais. Le PageRank interne est dilué.
**Fichiers.** `data/footer.js:388` (random shuffle des related — à transformer en hash déterministe basé sur le slug courant), `countries/country.html` (script bloc related/compare → idéalement rendu côté serveur via `_gen_v3.py` au build).
**Impact.** SEO ++ (consolidation PageRank interne sur un graph stable) ; user + (cohérence parcours).
**Score impact** : 7 — **effort** : 5 — **ratio 1.4**.

#### 1.9 Article schema : auteur incohérent + datePublished partiel
**Description.** Bali chronicle utilise `"author":{"@type":"Person","name":"Wigg"}` ✓ (cohérent avec persona éditorial). France country page utilise `"author":{"@type":"Organization","name":"WiggMap"}`. La charte éditoriale (`project-brain/editorial.md:11`) impose "Wigg" comme auteur unique. Aussi : country pages n'ont pas de `datePublished` ni `dateModified`.
**Fichiers.** Templates générateurs : `/scripts/build_country_pages.py`, `/_gen_v3.py`. Éviter de toucher les 484 fichiers à la main.
**Impact.** SEO + (E-E-A-T, signal d'autorité) ; brand + (auteur unique, ligne éditoriale).
**Score impact** : 4 — **effort** : 1 — **ratio 4.0**.

#### 1.10 Robots.txt minimal
**Description.** Bloque `/data/`, `/template_chronicles.html`, `/mon-compte.html`. Manquent : `/index.html.bak`, `/index.html.old`, `/data/header.js.bak`, `/lead-magnet/` (déjà `noindex` sur la page mais pas dans robots), explicit `Allow: /sitemap.xml`. Ajouter aussi `Crawl-delay: 1` pour bots agressifs (Bingbot a tendance à hammer).
**Fichiers.** `/robots.txt`.
**Impact.** SEO + (économie crawl budget, hygiène).
**Score impact** : 2 — **effort** : 1 — **ratio 2.0**.

---

### 2. Design system & identité éditoriale

> **Constat structurel** : la charte WiggMap stipule cream `#ece6d2`, forest `#1a5430`, Fraunces display, Instrument Sans UI. La réalité du code : **6 verts** (`#1a5430`, `#1d7f48`, `#1a7a45`, `#16a34a`, `#22c55e`, `#2ecc71`, `#18a957`, `#1c7c46`, `#0d9488` teal sur Bali), **6 fonts** (Inter, Fraunces, Cormorant Garamond, Playfair Display, DM Sans, DM Serif Display, Poppins, Source Serif 4), **5+ creams** (`#f4f2ef`, `#f5f0e8`, `#f6f1e8`, `#f6f8f7`, `#fafaf8`). Chaque fichier réinvente sa palette.

#### 2.0 [SPRINT DESIGN SYSTEM UNIFIÉ] Conventions à formaliser dans `tokens.css`
**Notes ajoutées en cours de Sprint 1 — à traiter ensemble dans un sprint dédié au design system :**

- **`data-category-color` officiel.** Les pages d'index chroniques `chronicles-family.html` (orange `#d7731d`) et `chronicles-horizons.html` (violet `#7d55d8`) portent un `theme-color` éditorial **intentionnel** par catégorie (restauré dans le commit `fix: restore intentional category theme-colors`). Définir dans `tokens.css` une convention `data-category-color="<famille|horizons|villes|dest|visas>"` avec les couleurs officielles de chaque catégorie (4–5 couleurs documentées), pour que ce ne soit plus traité comme du drift par les futurs audits. Les autres catégories (`villes`, `dest`, `visas`) étaient sur `#1c7c46` générique pré-Lot 5 — à statuer : leur attribuer une signature catégorielle ou les garder sur le forest charter ?
- **Couleur CTA officielle.** Le `#22c55e` utilisé sur le bouton newsletter footer + plusieurs CTAs (`btn-reveal`, `tool-badge`, etc.) est un **fallback Tailwind**, pas une couleur de marque WiggMap. Définir un token `--cta-bright` (ou équivalent nommé) dans `tokens.css` avec une valeur officielle validée — soit conserver `#22c55e` en l'officialisant, soit choisir un vert vif plus distinctif. Ne pas continuer à hardcoder `#22c55e` partout.

#### 2.1 Tokens CSS centralisés (variables.css partagé)
**Description.** Créer `/assets/wm-tokens.css` chargé sur toutes les pages : variables de couleurs, fonts, espacements, radii, shadows. Aujourd'hui chaque HTML duplique 50+ lignes de `:root{...}` inline avec dérive systématique. Une fois centralisé, il devient possible de muter la marque en un seul commit.
**Fichiers.** Nouveau `/assets/wm-tokens.css`. Pages racine à amender : `index.html`, `about.html`, `wiggmatch.html`, `compare.html`, `globe.html`, `indexchronicles.html`, `404.html`, `confirmation.html`, `chronicles-*.html` (5 fichiers). Country pages et chronicles pages : laisser la duplication temporaire (484 + 303 fichiers — chantier séparé) mais documenter les tokens canoniques.
**Impact.** Brand ++ ; maintenabilité ++ ; SEO neutre.
**Score impact** : 7 — **effort** : 4 — **ratio 1.75**.

#### 2.2 Aligner tous les verts sur `#1a5430`
**Description.** Remplacer `#1d7f48`, `#1a7a45`, `#16a34a`, `#22c55e`, `#2ecc71`, `#18a957`, `#1c7c46` par `#1a5430` partout sauf : (a) sur les chronicles villes où la couleur d'accent est volontairement variable (cf. `memory/city-chronicles-format.md:170`), (b) sur le `green-bright #22c55e` qui sert de couleur d'accent CTA (à conserver mais à documenter). Risque principal : la palette `#16a34a` (Tailwind green) est utilisée par `wiggmatch.html` et le widget consent — ces dérivés "vert bright" doivent rester car contraste hover/CTA.
**Fichiers.** `about.html:21`, `countries/*` (template), `indexchronicles.html:25`, `compare.html:35`, `wiggmatch.html:23`, `globe.html`, `data/footer.js:124,510` (note : intervention footer.js exclue par la contrainte — flagguer pour validation utilisateur).
**Impact.** Brand ++ ; cohérence visuelle ++.
**Score impact** : 6 — **effort** : 3 — **ratio 2.0**.

#### 2.3 Aligner les fonts sur Fraunces (display) + Instrument Sans (UI)
**Description.** Charter user : Fraunces + Instrument Sans. Réalité : Inter omniprésent (UI), Cormorant Garamond pour le wordmark header (légitime — italique distinctif), Fraunces display (✓), mais aussi Playfair Display (compare.html, Bali chronicle), DM Sans + DM Serif Display (Bali), Poppins (footer + per editorial.md homepage). Le footer (Poppins déclaré sans charger la font → fallback système silencieux) est dans header/footer non-modifiables ; documenter et flagguer. Pour les pages modifiables, basculer sur Inter → Instrument Sans, retirer Playfair/DM/Poppins.
**Fichiers.** `compare.html:21`, `chronicles/villes/chronicle-bali-*.html` (et autres villes utilisant Playfair/DM), `lp/*` (Cormorant Garamond utilisé en italique titre — à conserver, c'est un choix éditorial). `data/footer.js:30,510` (Poppins) — exclu par contrainte.
**Impact.** Brand ++ ; perf + (moins de fonts → moins de requêtes Google Fonts) ; CLS + (font-display:swap déjà en place).
**Score impact** : 6 — **effort** : 4 — **ratio 1.5**.

#### 2.4 Cream unifié
**Description.** Charter `#ece6d2`. Aucune page ne l'utilise. Les valeurs vivantes : `#f5f0e8` (index, lp), `#f4f2ef` (about), `#f6f1e8` (indexchronicles), `#f6f8f7` (compare), `#fafaf8` (Bali). Choisir UNE référence (suggestion : `#f5f0e8` qui est la plus utilisée OU `#ece6d2` charter si plus contrasté avec paper `#fffdf8`). Vérifier le contraste WCAG du texte sur ce fond.
**Fichiers.** Mêmes que 2.1 (tokens centralisés résout d'un coup).
**Impact.** Brand + ; a11y + si le contraste est validé.
**Score impact** : 4 — **effort** : 2 — **ratio 2.0**.

#### 2.5 `theme-color` cohérent
**Description.** Différents per page : `#1a1a1a` (index), `#1c7c46` (indexchronicles), `#1d7f48` (france), `#16a34a` (wiggmatch), `#0d9488` (Bali — teal !), `#22c55e` (manifest), `#1a5430` (lp). Aligner sur `#1a5430` (sauf chronicles villes où l'accent varie). Le manifest a `theme_color: #22c55e` qui crée un flash incohérent au lancement PWA.
**Fichiers.** `manifest.webmanifest`, `index.html:7`, toutes pages racine.
**Impact.** Brand + (cohérence onglets navigateur, splash PWA).
**Score impact** : 3 — **effort** : 1 — **ratio 3.0**.

#### 2.6 Refonte visuelle compare.html
**Description.** Page off-charte la plus criante : palette `#2ecc71`/`#18a957`, fond `#f6f8f7`, font Playfair Display + Inter, charge `css/main.css` externe (chemins relatifs `assets/favicon.ico` qui cassent en sous-page). 1 169 lignes. C'est un atterrissage SERP majeur ("compare countries cost of living") et le plus low-end visuellement.
**Fichiers.** `compare.html`, `compare/static/*` (héritent du même look).
**Impact.** Brand + ; conversion + (page de fonction-clé) ; SEO neutre.
**Score impact** : 6 — **effort** : 5 — **ratio 1.2**.

---

### 3. Performance (Core Web Vitals)

#### 3.1 Hero JPG pays 2–3 MB → WebP < 300 KB
**Description.** `/assets/hero-tajikistan.jpg` = 3.49 MB. Médiane des 161 héros pays ≈ 2.5 MB. Les `.webp` existent (181 fichiers vs 172 JPG) mais le HTML pointe sur `.jpg` et compte sur le runtime swap de footer.js qui échoue silencieusement si webp manquant ET fait double fetch. Sur mobile 4G, LCP attendu : >5 s. Cible : <2.5 s.
**Fichiers.** Templates `countries/country.html` JS (réécrire `<img src="hero.jpg">` en `<picture><source srcset="webp">`), `_gen_v3.py` (régénérer 484 pages). Étendre `scripts/optimize-images.sh` aux assets manquants.
**Impact.** Perf ++ (LCP) ; SEO + (Web Vitals = ranking factor) ; user ++.
**Score impact** : 9 — **effort** : 4 — **ratio 2.25**.

#### 3.2 Préload `bc.webp` au lieu de `bc.png`
**Description.** `index.html:23` : `<link rel="preload" as="image" href="/assets/bc.png">`. `bc.png` = 2.9 MB. `bc.webp` = 278 KB (10× plus petit). Le preload sert l'image utilisée comme `body{background-image: url('/assets/bc.png')}` (ligne 49). Mobile iOS reçoit en plus le `body::before` workaround (ligne 60). Switch direct sur webp = -2.6 MB sur le first paint.
**Fichiers.** `index.html:23,49,62`. Ajouter détection webp via `image-set()` CSS pour le fallback rare.
**Impact.** Perf ++ (LCP/FCP) ; SEO + ; bandwidth +.
**Score impact** : 8 — **effort** : 1 — **ratio 8.0**.

#### 3.3 Remplacer le runtime WebP swap par `<picture>` SSR
**Description.** `data/footer.js:160-206` scanne tous les `<img>` au DOMContentLoaded, fait un `new Image()` test, puis swap si succès. Sur la home : 12 country cards + 12 city cards + 3 chron thumbs + 6 hero placeholders = 33 fetches "test" supplémentaires. Aggrave INP, allonge le main thread, crée des layout shifts (CLS) car la nouvelle image se charge après celle d'origine. Solution : générer le HTML au build avec `<picture><source srcset="...webp" type="image/webp"><img src="...jpg"></picture>`. **Contrainte** : `footer.js` non modifiable → désactiver le scanner via un flag global `window.__WM_DISABLE_WEBP_SWAP=true` et construire le HTML correctement par défaut. Demander validation user pour assouplir la contrainte sur footer.js.
**Fichiers.** Templates générateurs ; `index.html` markup dynamique (lignes 908–1015). Pas de modification footer.js sans validation.
**Impact.** Perf ++ (INP, CLS, économie bande passante) ; SEO + (Vitals).
**Score impact** : 7 — **effort** : 5 — **ratio 1.4**.

#### 3.4 Preload du hero LCP par page pays + `fetchpriority=high`
**Description.** Sur `/countries/france-en.html`, le LCP visible est `/assets/hero-france.jpg` mais aucun preload. Ajouter `<link rel="preload" as="image" fetchpriority="high" href="/assets/hero-{slug}.webp">`. Globe.html le fait déjà (✓ ligne 17).
**Fichiers.** Template country pages, `_gen_v3.py`.
**Impact.** Perf ++ (LCP).
**Score impact** : 7 — **effort** : 2 — **ratio 3.5**.

#### 3.5 Optimize-images.sh étendu à `assetscity/`
**Description.** 4 fichiers > 3 MB dans `assetscity/` (hambourg.png 3.47 MB, mendoza.png 3.47 MB, athenes.png 3.40 MB, munich.png 3.35 MB). Ces images sont les héros des chroniques villes — directement le LCP des 228 pages chroniques villes. Le script existe mais ne semble pas couvrir ce répertoire.
**Fichiers.** `scripts/optimize-images.sh`. Ajouter une boucle `assetscity/`.
**Impact.** Perf ++ (LCP chronicles villes) ; SEO + ; bande passante.
**Score impact** : 6 — **effort** : 2 — **ratio 3.0**.

#### 3.6 Service Worker : précacher header.js + footer.js
**Description.** `sw.js:3` ne précache que `/`, `/index.html`, `/manifest.webmanifest`. Or `header.js` (124 KB) et `footer.js` (28 KB) sont chargés sur **toutes** les pages. Stratégie cache-first sur ces 2 fichiers + bump du `CACHE_NAME = wiggmap-v3` à chaque modif. Attention : si les fichiers sont mis à jour côté serveur sans bump, version stale → bug langue silencieux. Préférer stratégie stale-while-revalidate.
**Fichiers.** `sw.js`.
**Impact.** Perf + (-150 KB transferred sur 2ᵉ visite, navigation interne instantanée).
**Score impact** : 6 — **effort** : 2 — **ratio 3.0**.

#### 3.7 `content-visibility:auto` sur les grilles longues
**Description.** Les `.country-grid`, `.chron-grid`, `.city-grid` (homepage), `.scroll-row` (indexchronicles) sont rendues même hors viewport. `content-visibility:auto; contain-intrinsic-size:300px` sur les grilles → skip rendering hors viewport. Gain mesuré généralement 100–300 ms sur le first render.
**Fichiers.** `index.html` (CSS lignes 268–304, 358–399, 401–419), `indexchronicles.html`.
**Impact.** Perf + (TBT, FCP).
**Score impact** : 4 — **effort** : 1 — **ratio 4.0**.

#### 3.8 Suppression des backups (1.1 MB sur le repo, potentiellement servis)
**Description.** `index.html.bak` (513 KB), `index.html.old` (513 KB), `data/header.js.bak` (120 KB) sont versionnés et servis par Netlify. Risques : (1) accessible publiquement (peut révéler du HTML déprécié), (2) crawl budget gâché. Bloqués indirectement par robots si ajoutés.
**Fichiers.** Supprimer (`git rm`). Ou ajouter à `.gitignore` + `_redirects` 410 Gone.
**Impact.** Sec + ; perf marginal.
**Score impact** : 2 — **effort** : 1 — **ratio 2.0**.

#### 3.9 Globe.html : SRI + lazy load globe.gl
**Description.** `globe.html:19` : `<script src="https://unpkg.com/globe.gl"></script>` sans `integrity` ni `crossorigin`. Risque supply-chain CDN. Et le script est synchrone avant `<body>` → bloque parsing. Solutions : (1) ajouter `integrity` SHA hash, (2) `defer` + skeleton HUD pendant chargement, (3) self-host la version pinnée dans `/assets/`.
**Fichiers.** `globe.html:19,24`.
**Impact.** Sec + ; perf + (FCP).
**Score impact** : 5 — **effort** : 2 — **ratio 2.5**.

---

### 4. UX & conversion

#### 4.1 Cards hero : taille tactile + zone cliquable
**Description.** Les `.country-card` et `.city-card` (home) ont une zone cliquable correcte (toute la card est `<a>`) mais le `font-size:11px` du `.cc-fact` et `font-size:10px` du `.city-country` sont sous le seuil de lisibilité mobile (Apple HIG : 11pt min, Material 12sp). Augmenter à 12px et garder le contraste blanc/.75 alpha.
**Fichiers.** `index.html:298-304, 419`.
**Impact.** UX + ; a11y +.
**Score impact** : 3 — **effort** : 1 — **ratio 3.0**.

#### 4.2 Lead-magnet visibility from chronicles
**Description.** Les 3 LP `lead-magnet/visas-2026-{lang}.html` ont un `noindex` (volontaire — page gatée). Mais aucun CTA visible sur les chroniques visa pour pousser l'opt-in. Lead magnet = canal email. La newsletter footer existe ✓ mais "1 chronicle a week" est moins concret qu'un PDF gratuit.
**Fichiers.** Templates chronicles visas (`chronicle-visas-*-2026-*.html` × 3 langues × 4 sujets visa = 12 fichiers).
**Impact.** Conversion ++ (revenu via cohorte email) ; SEO neutre.
**Score impact** : 6 — **effort** : 2 — **ratio 3.0**.

#### 4.3 Country page : CTA "Compare with…" proéminent
**Description.** Pages pays montrent un carrousel `.rc-row` (compare pairs) en sidebar mais l'invitation à initier sa propre comparaison n'est pas mise en avant. Ajouter un CTA bandeau full-width "Compare {country} with another country →" qui ouvre un modal avec input search.
**Fichiers.** Template country pages.
**Impact.** Conversion + (rétention sur le funnel compare → wiggmatch) ; engagement +.
**Score impact** : 5 — **effort** : 2 — **ratio 2.5**.

#### 4.4 WiggMatch : persistence + reprise + share
**Description.** Le quiz fait 8 questions (≈ 3 min). Si l'utilisateur quitte, perte totale. Sauvegarder l'état dans `localStorage` (clé `wm-match-progress`), CTA "Resume" sur retour. Ajouter à la fin un share button (résultat → URL stable `/wiggmatch.html?r=<hash>` qui re-rend les top 3 villes).
**Fichiers.** `wiggmatch.html`.
**Impact.** Conversion + (taux de complétion) ; viralité + (share) ; user +.
**Score impact** : 5 — **effort** : 4 — **ratio 1.25**.

#### 4.5 Newsletter signup : feedback d'erreur Buttondown
**Description.** `data/footer.js:551` poste à Buttondown en `mode:'no-cors'` → l'utilisateur voit "✓ Thanks!" même si l'inscription a échoué côté Buttondown. Risque : faux positif, churn silencieux. Ajouter ping `/api/check-subscriber` (Netlify Function) ou retomber sur Buttondown form publique avec redirect post.
**Fichiers.** `data/footer.js:530-565` — exclu par contrainte. À discuter avec user.
**Impact.** Trust + ; revenu + (vrais subs comptés).
**Score impact** : 4 — **effort** : 3 — **ratio 1.33**.

#### 4.6 Sticky newsletter dismissible sur chronicles longues
**Description.** Sur les chronicles 15-25 min, l'utilisateur scroll longtemps avant d'arriver au CTA newsletter en pied. Ajouter un mini-CTA sticky bottom-right dismissible après 30 % de scroll.
**Fichiers.** Nouveau snippet conditionnel chargé sur `/chronicles/*` (similaire au pattern `widget.js` actuel).
**Impact.** Conversion + ; user neutre si dismissible.
**Score impact** : 5 — **effort** : 3 — **ratio 1.67**.

---

### 5. Contenu & SEO éditorial

#### 5.1 Pillar / hub pages "Best countries for X 2026"
**Description.** WiggMap couvre 161 pays, 76 villes, 75 thématiques mais n'a pas de **pages-hubs** type "Best countries for digital nomads 2026" (pillar) qui agrégeraient les chroniques + un classement WiggMap propriétaire + CTAs vers compare. Ces pages sont les plus recherchées sur Google ("best country for retirement", "best country to raise kids", "best digital nomad visa"). Concurrence (Nomad List, InternationalLiving) verrouille ces SERPs avec ce format.
**Fichiers.** Nouveau : `/best/digital-nomads-2026-{lang}.html`, `/best/retirement-2026-{lang}.html`, `/best/families-2026-{lang}.html`, `/best/lowest-cost-2026-{lang}.html`. 4 hubs × 3 langues = 12 fichiers.
**Impact.** SEO ++ (mots-clés haute intention) ; revenu + (acquisition).
**Score impact** : 8 — **effort** : 8 — **ratio 1.0**.

#### 5.2 Country page : section "Cities in {country}"
**Description.** Les pages pays ne listent pas systématiquement les chroniques villes du pays. Ex : `/countries/thailand-en.html` devrait contenir un H2 "Cities in Thailand" listant Bangkok, Chiang Mai, Phuket, etc., avec lien vers chaque chronicle. Améliore PageRank vers les villes + UX exploration.
**Fichiers.** Templates country pages, mapping country→cities à dériver des slugs `chronicles/villes/chronicle-{city}-{country-slug}-*`.
**Impact.** SEO ++ (maillage) ; user ++ (exploration intuitive).
**Score impact** : 7 — **effort** : 4 — **ratio 1.75**.

#### 5.3 FAQ schema sur chronicles thématiques
**Description.** Excellente nouvelle : 303/303 chroniques ont déjà `FAQPage` schema (vérifié grep). C'est conforme aux attentes. **Aucune action requise**, gardée ici pour traçabilité. Vérifier juste que les nouveaux contenus respectent ce pattern.
**Fichiers.** Aucun.
**Impact.** —
**Score impact** : 0 — **effort** : 0 — **ratio n/a**.

#### 5.4 Calendar éditorial : couvrir les zones blanches
**Description.** Couverture chronicles : Asie SE++, Amériques++, Afrique +, Europe +, Australie +. Quasi-absents : **Asie centrale** (Kazakhstan, Ouzbékistan, Kirghizistan — émergent comme nomad destinations), **Afrique de l'Est** (Kenya, Rwanda, Ouganda — Tech hubs), **Caucase au-delà de Géorgie** (Arménie). Plan : 1 chronicle par mois sur ces zones × 3 langues = 36 articles/an.
**Fichiers.** Nouveaux chronicles thématiques + villes (Almaty, Tachkent, Bichkek, Tbilissi, Erevan, Nairobi, Kigali, Kampala).
**Impact.** SEO + (conquérir des SERPs sous-couverts) ; brand + (exhaustivité).
**Score impact** : 5 — **effort** : 8 — **ratio 0.6**.

---

### 6. Accessibilité

#### 6.1 Skip-to-main-content link
**Description.** Aucun lien "Aller au contenu" pour utilisateurs clavier / lecteur d'écran. Sur chronicles, le burger header + langue + auth = 5+ tab stops avant le contenu. Standard a11y depuis 20 ans.
**Fichiers.** Injection avant `#siteHeader` sur templates racine. Ou via header.js (exclu).
**Impact.** A11y ++ ; SEO + (signal d'accessibilité).
**Score impact** : 4 — **effort** : 1 — **ratio 4.0**.

#### 6.2 `:focus-visible` styles uniformes
**Description.** Aucune règle `:focus-visible` ni `:focus` détectée dans `index.html`, `header.js`, `footer.js`. Les utilisateurs clavier voient le focus-ring par défaut du navigateur (variable, parfois invisible sur fond clair). Définir `:focus-visible{outline:2px solid #1a5430; outline-offset:2px}` global.
**Fichiers.** `/assets/wm-tokens.css` (lié à 2.1).
**Impact.** A11y ++ (WCAG 2.4.7).
**Score impact** : 5 — **effort** : 2 — **ratio 2.5**.

#### 6.3 Contraste sur texte hero (sub/desc rgba alpha bas)
**Description.** Sur Wiggmatch hero : `.hero-desc{color:rgba(255,255,255,0.55)}` sur fond `var(--ink)#0f1117` = ratio ≈ 4.4:1 (limite AA pour texte normal, KO pour AAA). `.hero-stat-lbl` rgba(.3) ≈ 2.8:1 — **fail AA**. Idem `.hero-quick a{color:#fff}` sur fond glassmorphic semi-transparent qui peut tomber sous 3:1 selon l'image. Auditer + remonter alpha à .65 minimum.
**Fichiers.** `wiggmatch.html:43,50` ; `index.html:108-115` ; chronicles dark heros.
**Impact.** A11y + (WCAG 1.4.3) ; user +.
**Score impact** : 5 — **effort** : 2 — **ratio 2.5**.

#### 6.4 Bouton cookies en `<a href="#">` au lieu de `<button>`
**Description.** `data/footer.js:19` : `<a href="#" id="wmCookieReset">Cookies</a>` — c'est un déclencheur d'action, pas un lien. A11y + sémantique. Exclu par contrainte (footer.js).
**Fichiers.** `data/footer.js:19` (à valider avec user).
**Impact.** A11y + ; SEO neutre.
**Score impact** : 3 — **effort** : 1 — **ratio 3.0**.

#### 6.5 Alt text vide vs informatif
**Description.** Vérification : la majorité des `<img>` ont des `alt` (bon). `data/footer.js:414` génère cards related avec `background-image` (pas d'alt possible). Pour les `<img>` dynamiques générés home (lignes 910, 1009), l'alt vaut le nom de pays ✓. Sur les country pages, `.hero-img` a un alt mais reste générique. Rendre les alt descriptifs (ex : "Lisbon old town view at sunset" plutôt que "Portugal").
**Fichiers.** Templates country pages, JSON details (`data/details/{slug}.json` → `hero.alt`).
**Impact.** A11y + ; SEO image +.
**Score impact** : 4 — **effort** : 3 — **ratio 1.33**.

---

### 7. Architecture code & maintenabilité

#### 7.1 `_headers` Netlify : sécurité + caching
**Description.** Aucun fichier `_headers`. Manquent : `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`, `X-Frame-Options: DENY` (ou CSP frame-ancestors), CSP minimale autorisant GTM, Buttondown, fonts.googleapis, unpkg, Supabase. Aussi : `Cache-Control: public, max-age=31536000, immutable` sur `/assets/*`, et `max-age=300` sur HTML pour permettre updates rapides.
**Fichiers.** Nouveau `/_headers`.
**Impact.** Sec ++ ; perf + (caching agressif assets) ; SEO + (HTTPS + CSP signal qualité).
**Score impact** : 6 — **effort** : 2 — **ratio 3.0**.

#### 7.2 Compare.html : chemins absolus
**Description.** `compare.html:15-16` : `<link rel="icon" href="assets/favicon.ico">` et `<link rel="stylesheet" href="css/main.css">` — chemins **relatifs**. Tous les autres fichiers du projet utilisent `/assets/`. Si compare.html est jamais déplacé en sous-dossier (ex : `/compare/index.html`), ça casse. Et `css/main.css` n'existe à la racine, ça veut dire qu'il y a soit un fichier non audité, soit un 404 silencieux.
**Fichiers.** `compare.html:15,16`. Vérifier l'existence de `/css/main.css`.
**Impact.** Maintenabilité ++ ; perf + si 404 résolu.
**Score impact** : 4 — **effort** : 1 — **ratio 4.0**.

#### 7.3 Connect widget : éviter double chargement
**Description.** `data/footer.js:215-226` injecte CSS+JS du widget connect sur chaque page chronicle. CSS = 6.3 KB, JS = 25.6 KB. Charger via `<link rel="preload">` au début + `defer` script + cache busting sur version. Considérer aussi un check `if (window.__wmConnectLoaded)` pour éviter les doubles inserts si le DOM mute.
**Fichiers.** `data/footer.js:215-226` (exclu par contrainte) + `connect/widget.js`.
**Impact.** Perf + (chronicles).
**Score impact** : 3 — **effort** : 1 — **ratio 3.0**.

#### 7.4 Service worker stratégie : stale-while-revalidate
**Description.** Actuellement network-first sur HTML/JSON, cache-first sur le reste. Network-first ralentit les retours utilisateurs sur des pages déjà visitées. Switch à `stale-while-revalidate` sur HTML : sert immédiatement la version cachée, fetch en background pour la prochaine visite. Améliore perçu + 30 %.
**Fichiers.** `sw.js`.
**Impact.** Perf + (perçu navigation interne).
**Score impact** : 5 — **effort** : 2 — **ratio 2.5**.

#### 7.5 Random pour related chronicles → déterministe
**Description.** `data/footer.js:388-394` (Fisher-Yates shuffle) sélectionne 3 related chronicles aléatoirement. Conséquence : Googlebot voit des liens internes différents à chaque crawl → graph instable. Remplacer par `pickThree(pool, currentSlug)` qui hash le slug courant et choisit déterministiquement (ex : `hash(slug) % len(pool)`). User-side, l'utilisateur revoit les mêmes related — pas grave, c'est même mieux pour l'attendu (consistence).
**Fichiers.** `data/footer.js:388` (exclu par contrainte — flagguer).
**Impact.** SEO + (PageRank stable) ; user neutre.
**Score impact** : 4 — **effort** : 1 — **ratio 4.0**.

#### 7.6 Manifest : icônes maskable + thème aligné
**Description.** `manifest.webmanifest` : 2 icônes (192, 512), pas de `purpose: "maskable"` (PWA Android écrase l'icône en safe area). `theme_color: #22c55e` ne matche pas la marque. Ajouter `icons: [...{purpose:"maskable"}, {purpose:"any"}]`, fixer `theme_color: "#1a5430"`, `background_color: "#f5f0e8"` (cream).
**Fichiers.** `manifest.webmanifest`. Générer les variantes maskable depuis `/assets/icons/`.
**Impact.** PWA + (UX install) ; brand +.
**Score impact** : 3 — **effort** : 2 — **ratio 1.5**.

#### 7.7 Build script idempotence
**Description.** `_gen_v3.py` (79 KB) régénère les pages — confirmer qu'il est idempotent (re-run produit byte-identique output) sinon dérive silencieuse via les hash diffs commit-by-commit. À long terme, migrer vers `scripts/build_country_pages.py` + `scripts/build_index_pages.py` qui semblent plus modulaires.
**Fichiers.** `_gen_v3.py`, `scripts/*`.
**Impact.** Maintenabilité + ; SEO + (consistence outputs).
**Score impact** : 4 — **effort** : 6 — **ratio 0.67**.

---

## Backlog priorisé global (ratio impact/effort décroissant)

| Rang | Axe | Opportunité | Impact | Effort (h) | Effort score | Ratio |
|---|---|---|---|---|---|---|
| 1 | Perf | 3.2 Préload `bc.webp` au lieu de `bc.png` | 8 | 1 | 1 | **8.0** |
| 2 | SEO | 1.4 JSON-LD sur about / wiggmatch / compare | 6 | 1 | 1 | **6.0** |
| 3 | SEO | 1.3 Canonical compare.html (?c=) | 5 | 1 | 1 | **5.0** |
| 4 | SEO | 1.7 `lang` HTML cohérent | 5 | 1 | 1 | **5.0** |
| 5 | Perf | 3.7 `content-visibility:auto` grilles | 4 | 1 | 1 | **4.0** |
| 6 | A11y | 6.1 Skip-to-main-content link | 4 | 1 | 1 | **4.0** |
| 7 | Code | 7.2 Compare.html : chemins absolus | 4 | 1 | 1 | **4.0** |
| 8 | SEO | 1.9 Article schema : auteur Wigg + datePublished | 4 | 1 | 1 | **4.0** |
| 9 | Code | 7.5 Related chronicles déterministes | 4 | 1 | 1 | **4.0** |
| 10 | Perf | 3.4 Preload hero pays + fetchpriority | 7 | 2 | 2 | **3.5** |
| 11 | SEO | 1.2 Hreflang sur wiggmatch / compare / about / globe | 6 | 2 | 2 | **3.0** |
| 12 | Code | 7.1 `_headers` Netlify (CSP, sec) | 6 | 2 | 2 | **3.0** |
| 13 | Perf | 3.5 Optimize-images.sh étendre à assetscity/ | 6 | 2 | 2 | **3.0** |
| 14 | Perf | 3.6 SW précache header.js + footer.js | 6 | 2 | 2 | **3.0** |
| 15 | UX | 4.2 Lead magnet visibility chronicles | 6 | 2 | 2 | **3.0** |
| 16 | Design | 2.5 `theme-color` unifié | 3 | 1 | 1 | **3.0** |
| 17 | UX | 4.1 Tailles tactiles cards | 3 | 1 | 1 | **3.0** |
| 18 | A11y | 6.4 Cookies `<a>` → `<button>` | 3 | 1 | 1 | **3.0** |
| 19 | Code | 7.3 Connect widget double load | 3 | 1 | 1 | **3.0** |
| 20 | A11y | 6.2 `:focus-visible` styles | 5 | 2 | 2 | **2.5** |
| 21 | A11y | 6.3 Contraste hero subs | 5 | 2 | 2 | **2.5** |
| 22 | UX | 4.3 Country page : CTA Compare with… | 5 | 2 | 2 | **2.5** |
| 23 | Perf | 3.9 Globe.html SRI + lazy | 5 | 2 | 2 | **2.5** |
| 24 | SEO | 1.5 Image sitemap | 5 | 2 | 2 | **2.5** |
| 25 | Code | 7.4 SW stale-while-revalidate | 5 | 2 | 2 | **2.5** |
| 26 | Perf | 3.1 Hero JPG pays → WebP < 300 KB | 9 | 4 | 4 | **2.25** |
| 27 | Design | 2.2 Aligner verts sur #1a5430 | 6 | 3 | 3 | **2.0** |
| 28 | Design | 2.4 Cream unifié | 4 | 2 | 2 | **2.0** |
| 29 | Perf | 3.8 Suppression backups | 2 | 1 | 1 | **2.0** |
| 30 | SEO | 1.10 Robots.txt enrichi | 2 | 1 | 1 | **2.0** |
| 31 | Design | 2.1 Tokens CSS centralisés | 7 | 4 | 4 | **1.75** |
| 32 | Contenu | 5.2 Country : section "Cities in" | 7 | 4 | 4 | **1.75** |
| 33 | UX | 4.6 Sticky newsletter chronicles | 5 | 3 | 3 | **1.67** |
| 34 | SEO | 1.1 Homepage trilingue (3 URLs) | 10 | 6 | 6 | **1.67** |
| 35 | SEO | 1.6 Sitemap split | 3 | 2 | 2 | **1.5** |
| 36 | Code | 7.6 Manifest maskable + theme | 3 | 2 | 2 | **1.5** |
| 37 | Design | 2.3 Aligner fonts Fraunces+Instrument | 6 | 4 | 4 | **1.5** |
| 38 | SEO | 1.8 Maillage country↔chronicles SSR | 7 | 5 | 5 | **1.4** |
| 39 | Perf | 3.3 `<picture>` SSR au lieu runtime swap | 7 | 5 | 5 | **1.4** |
| 40 | UX | 4.5 Newsletter feedback Buttondown | 4 | 3 | 3 | **1.33** |
| 41 | A11y | 6.5 Alt text descriptifs | 4 | 3 | 3 | **1.33** |
| 42 | Design | 2.6 Refonte visuelle compare.html | 6 | 5 | 5 | **1.2** |
| 43 | UX | 4.4 WiggMatch persistence + share | 5 | 4 | 4 | **1.25** |
| 44 | Contenu | 5.1 Pillar pages "Best for X 2026" | 8 | 8 | 8 | **1.0** |
| 45 | Code | 7.7 Build scripts idempotence | 4 | 6 | 6 | **0.67** |
| 46 | Contenu | 5.4 Couverture Asie centrale + Afrique Est | 5 | 8 | 8 | **0.6** |

---

## Plan d'action recommandé (3 sprints)

**Sprint 1 — Quick wins (2 jours)** : items #1 → #19. Adresse perf LCP (#1, #10, #13), conformité SEO (#2, #3, #4, #8, #11), sécurité de base (#12), a11y minimum (#6, #18). Aucun changement structurel.

**Sprint 2 — Cohérence visuelle + maillage (1 semaine)** : items #20 → #33. Tokens CSS, alignement couleurs/fonts, contraste a11y, country↔cities, newsletter chronicles. Pose les fondations pour scale.

**Sprint 3 — Levée de constraintes & contenu (2–4 semaines)** : items #34 → #46. Homepage trilingue (négocier la complexité avec user), refonte compare.html, pillar pages, couverture éditoriale. Ces items modifient des hypothèses produit et nécessitent validation explicite.

---

## Items à valider avec l'utilisateur avant exécution

Plusieurs opportunités haute valeur **touchent à `data/header.js` ou `data/footer.js`** — exclus par la contrainte. Lever cette exclusion débloquerait :
- **#3.3** `<picture>` SSR (suppression du runtime webp swap dans footer.js).
- **#2.2 / #2.5** Alignement vert/`theme-color` (footer.js déclare encore `#22c55e`, `#16a34a`).
- **#7.5** Related chronicles déterministes (footer.js:388).
- **#4.5** Feedback Buttondown (footer.js:551).
- **#6.4** Cookies `<a>` → `<button>` (footer.js:19).

Demander confirmation : ces 5 changements peuvent-ils intervenir dans un commit dédié `header/footer` après validation préalable ?

---

*Audit produit le 2026-05-03. Aucun fichier source modifié.*
