# SPRINT_Y_PLAN — Design system unifié

> **Date** : 2026-05-04
> **Mode** : audit + plan. Aucun fichier modifié dans cette phase.
> **Roadmap** : Sprint Y suit Sprint X et précède Sprint Z (Connect T2).
> **Audit ref** : AUDIT.md item 2.0 + 2.1 + 2.2 + 2.3 + 2.4 + 2.5.

---

## 0. TL;DR

Le design system actuel a dérivé sur **toutes les dimensions** : 12+ verts en circulation (top : `#1a5430` × 1407, `#15803d` × 1079, `#1d7f48` × 999, `#16a34a` × 254, `#22c55e` × 189), 7+ fonts (Fraunces 4046, Inter 1422, **Poppins 1375 hors charte**, Playfair Display 252, DM Serif/Sans 456, Source Serif 168, Cormorant Garamond 21, **Instrument Sans charter quasi inexistant à 3 occurrences**), 14+ creams (top : `#fffdf8` 551, `#f9f5ed` 513, `#f3ede3` 513, `#ece6d2` charter à seulement 12), et un `theme-color` éclaté sur 33+ valeurs distinctes.

**Constat brutal** : **Sprint 1 Lot 5 a déposé `#1a5430` sur 15 pages racine seulement**. Les 484 country pages + 75 chronicles thématiques + 228 chronicles villes + 64 compare/static **restent drift complet**.

Sprint Y est **trop gros pour 1 PR** (estimé 30-50h dev). Je propose un découpage en **6 lots Y.1 → Y.6** avec validation entre Y.2 (preview racine) et Y.3 (régénération massive — point de non-retour qui touche 800+ fichiers). Décisions critiques à arbitrer en §4 avant exécution.

---

## 1. Audit exhaustif de l'état réel

### 1.1 Verts (12+ valeurs, 4193 occurrences au total sur 6 plus fréquentes)

| Hex | Occurrences | Source / Usage | Verdict |
|---|---|---|---|
| **`#1a5430`** | **1407** | Charter forest. Sprint 1+2+D1+X. | ✓ **CANONICAL** |
| `#15803d` | 1079 | Tailwind green-700 — utilisé dans `art-tag` backgrounds des country pages, sections "Overview/Food note" via `style=...;color:#15803d`. **Drift systémique sur les 484 country pages** (probable origine `_gen_v3.py` ou `build_country_pages.py`). | ❌ **À purger** → `#1a5430` |
| `#1d7f48` | 999 | Forest variant — `theme-color` sur 484 country pages (drift Sprint 2 oubli) + JSON-LD + canonicals héritées | ❌ **À purger** → `#1a5430` |
| `#16a34a` | 254 | Tailwind green-600 — `wm-nl-btn:hover`, footer newsletter, wiggmatch CTA hover | ⚠️ **À garder ponctuellement** (hover état CTA cohérent avec décision Sprint 1 F4) — à officialiser comme `--cta-bright-hover` |
| `#22c55e` | 189 | Tailwind green-500 — `wm-nl-btn`, `wiggmatch btn-start`, manifest `theme_color`, 155 chronicles+lp+lead-magnet `theme-color` | ⚠️ **À garder ponctuellement** (CTA principal) — à officialiser comme `--cta-bright` |
| `#155f36` | 80 | Forest darker — `wm-footer-cookies-btn` hover, `green-dk` country pages | ⚠️ **À garder** comme `--green-dark` (`:hover` du forest principal) |
| `#0d9488` | 21 | Teal Bali — chronicle ville, **palette per-city intentionnelle** | ✓ **À conserver** sous `data-category-color` |
| `#2ecc71` + `#18a957` | 5 + 4 | Compare.html palette off-charter | ❌ **À purger** dans Y.6 ou différer Sprint Y' |
| `#1a7a45` | 4 | about.html (avant Sprint 1 — peut-être déjà nettoyé) | ❌ **Vérifier + purger** |
| `#1c7c46` | 5+ (Sprint 2 history) | Forest variant — déjà nettoyé en Sprint 2 mais peut subsister sur countries non régénérées | ❌ **À purger** |
| `#0a1f10` | 1 | `wm-nl-btn color` — texte foncé sur CTA bright | ✓ **À garder** comme `--ink-on-cta` |
| `#065f46`, `#059669` | 9 + 78 | Compare/static palette + chronicle ville Bali | ❌ **À purger** (compare) / **conserver** (Bali category-color) |

### 1.2 Cream / paper (14 valeurs, 2520 occurrences)

| Hex | Occurrences | Notes | Verdict |
|---|---|---|---|
| `#fffdf8` | 551 | Paper canonical (utilisé partout) | ✓ **CANONICAL `--paper`** |
| `#f9f5ed` + `#f3ede3` | 513 + 513 | Gradient body country pages (`linear-gradient(180deg,#f9f5ed,#f3ede3)`) | ✓ **À officialiser** comme `--bg-grad-start` / `--bg-grad-end` |
| `#fbf7ee` | 486 | Paper-2 country pages | ⚠️ **À fusionner** avec `--paper` (proche de `#fffdf8`) ou garder comme `--paper-2` |
| `#fef9e7` | 483 | Cream-warm — surfaces `bg-gold-tint` country | ⚠️ **À officialiser** ou supprimer (proche de banner orange `#fff7e6`) |
| `#fafaf8` | 228 | wiggmatch + chronicles paper | ⚠️ **À fusionner** avec `--paper` |
| `#f6f1e8` | 28 | indexchronicles bg | ❌ **À purger** → `--bg-grad-start` |
| **`#f5f0e8`** | 22 | **Index.html, lp/, sprint 1 token candidate** | ✓ **À officialiser comme `--bg`** (background body) |
| `#f7f5f0` | 18 | Sprint 1 some chronicles | ⚠️ **À fusionner** avec `--bg` |
| `#fef9c3` | 16 | Yellow background pour `art-tag.warn` | ✓ **À officialiser** comme `--warn-bg` |
| `#f6f8f7` | 13 | compare.html background — off-charter | ❌ **À purger** |
| **`#ece6d2`** | **12** | **Mémoire user dit charter, mais quasi inexistant dans le code** | ⚠️ **DÉCISION À ARBITRER** (D1) |
| `#f4f2ef` | 4 | about.html legacy — Sprint 1 normalement nettoyé | ❌ **À purger** |
| `#f8f4ea` | 2 | header.js drawer bg | ⚠️ **Conserver** ou aligner |

**Constat sur cream charter** : la mémoire user déclare `#ece6d2`, mais 12 occurrences seulement. La réalité dominante : **`#f5f0e8`** (utilisé sur les pages migrées Sprint 1/2 comme `--bg` officieux). **D1 critique** : confirmer `#f5f0e8` (réalité) ou `#ece6d2` (mémoire) ?

### 1.3 Fonts (8+ familles, 7541 occurrences)

| Famille | Occurrences | Usage | Verdict |
|---|---|---|---|
| **Fraunces** | **4046** | Display canonical (titres, brand) | ✓ **CANONICAL `--font-display`** |
| **Inter** | **1422** | UI canonical (body, nav, forms) | ✓ **CANONICAL `--font-ui`** (de facto) |
| Poppins | 1375 | **Drift** — header.js a Poppins en footer + chronicles éditorial.md déclare Poppins pour homepage. La charte user dit **Instrument Sans**. Quasi-aucune page n'utilise Instrument Sans. | ❌ **À arbitrer (D2)** : purger Poppins → Inter (recommandé), ou tout migrer vers Instrument Sans (gros chantier) |
| Playfair Display | 252 | compare.html + Bali chronicle (off-charter — Bali utilise palette city-specific) | ❌ **Compare** → Fraunces ; **Bali** → conserver (intentionnel) |
| DM Serif Display | 228 | Bali chronicle (city-specific) | ⚠️ **Conserver** sous `data-category-font` ? |
| DM Sans | 228 | Bali idem | ⚠️ **Idem** |
| Source Serif 4 | 168 | Chronicles éditorial.md déclare comme corps de texte chronicles | ⚠️ **Décision** : conserver pour chronicles ou unifier sur Inter ? |
| Cormorant Garamond | 21 | Header wordmark italique (intentionnel, signature de marque) | ✓ **À garder** comme `--font-brand-italic` (usage limité au wordmark) |
| Instrument Sans | 3 | Wiggmatch uniquement (charter user) | ⚠️ **D2** — promouvoir ou purger |

### 1.4 theme-color (33+ valeurs distinctes)

| Hex | Occurrences | Source | Verdict |
|---|---|---|---|
| `#1d7f48` | **484** | TOUS les country pages (drift Sprint 2 oubli) | ❌ **À purger** → `#1a5430` |
| `#22c55e` | 155 | 90 chronicles thématiques + lp + lead-magnet (post-Sprint X partiellement nettoyé) | ❌ **À purger** → `#1a5430` |
| `#1a5430` | 59 | Sprint 1+2+D1+X pages migrées | ✓ **CANONICAL** |
| `#dc2626` (rouge), `#7c3aed` (violet), `#0891b2` (teal), `#16a34a` (vert), `#d97706` (orange), `#f59e0b` (jaune), `#b45309`, `#f97316`, `#0d9488`, `#065f46`, `#0369a1`, `#2563eb`, `#1d4ed8`, `#0284c7`, `#ec4899`, `#ea580c`, `#e11d48`, `#db2777`, `#ca8a04`, `#c2410c`, `#b91c1c`, `#4f46e5`, `#475569`, `#4338ca`, `#3b82f6`, `#0f766e`, `#0ea5e9`, `#06b6d4` | total ≈ 228 | **Chronicles villes** (76 villes × 3 langues = 228 fichiers, palette per-city intentionnelle per memory) | ✓ **À conserver** sous `data-category-color="city-{slug}"` |
| `#d7731d` (orange) + `#7d55d8` (violet) | 4 + 4 | chronicles-family + chronicles-horizons (Sprint 1 a749c8e, intentionnel catégoriel) | ✓ **À officialiser** sous `data-category-color="family|horizons"` |

### 1.5 Hero JPG / WebP état

| | |
|---|---|
| Hero JPG country pages | **169** fichiers, **jusqu'à 3.5 MB** chacun (tajikistan, andorra, gabon, etc.) |
| WebP country pages | **169** fichiers (1:1 correspondence) — **existent mais non servis** par défaut |
| Hero PNG country pages | 0 |
| `assetscity/` images | 170 fichiers, plusieurs **PNG >3MB sans webp** (hambourg.png 3.5MB, mendoza.png 3.5MB, athenes.png 3.4MB, munich.png 3.3MB, cologne.png 3.3MB) |
| Runtime webp swap | Actif sur tous les `<img>` JPG (footer.js IIFE) — coût ~33 fetches "test" par page |
| Flag `__WM_DISABLE_WEBP_SWAP` | Présent dans footer.js (Sprint 1 D1.8), **utilisé nulle part** = personne n'a opté out | 

### 1.6 Compare/static palette off-charter

```
:root{
  --green:#059669;       /* off-charter — Tailwind emerald-600 */
  --green-light:rgba(5,150,105,.09);
  --bg:#f6f8f7;          /* off-charter — pas dans la liste cream */
  --font:'Inter',...;
}
```

64 pages compare/static partagent cette palette. **Drift complet**, mais isolé (un seul cluster). À refondre dans un sous-sprint Y.6 ou différer.

### 1.7 Pages déjà propres (Sprint 1+2+D1+X acquis — à NE PAS toucher)

- 14 pages racine `/en/`, `/fr/`, `/es/` (Sprint 2)
- 3 wiggmatch lang variants (Sprint D1)
- 3 lead-magnet lang variants (Sprint X)
- 9 LP lang variants (déjà propre depuis avril)
- skip-link `wm-skip` partout (Sprint 1 Lot 5)
- 2 pages éditorial catégoriel (`chronicles-family`, `chronicles-horizons`)

Sprint Y doit **préserver intégralement ces acquis** (vérifs auto dans monitor).

---

## 2. tokens.css — proposition de structure

### 2.1 Création de `/assets/wm-tokens.css` (nouveau fichier, ~3 KB minifié)

```css
/* WiggMap Design Tokens — Sprint Y, source de vérité unique */

:root {
  /* ─── BRAND COLORS ──────────────────────────────────────────── */
  --green: #1a5430;            /* Forest charter — couleur brand canonical */
  --green-dark: #155f36;       /* Forest hover / actif */
  --green-light: #d4e8d0;      /* Forest 20% — backgrounds tints */
  --green-tint: rgba(26, 84, 48, 0.08);  /* Forest 8% — pseudo-décoratif */

  /* CTA bright (officialise #22c55e Tailwind comme couleur de marque) */
  --cta-bright: #22c55e;       /* Vert vif — CTA principaux (newsletter, quiz start) */
  --cta-bright-hover: #16a34a; /* Hover du CTA bright */
  --ink-on-cta: #0a1f10;       /* Texte sur fond CTA bright */

  /* Status semantic */
  --warn: #d97706;
  --warn-bg: #fef9e7;
  --warn-border: rgba(217, 119, 6, 0.25);
  --error: #dc2626;
  --success: var(--green);

  /* ─── SURFACES (paper / cream) ──────────────────────────────── */
  --bg: #f5f0e8;               /* Cream body canonical (D1 décision) */
  --bg-grad-start: #f9f5ed;    /* Country pages gradient start */
  --bg-grad-end: #f3ede3;      /* Country pages gradient end */
  --paper: #fffdf8;            /* Cards, surfaces level 1 */
  --paper-2: #fbf7ee;          /* Cards, surfaces level 2 */
  --rule: #c8bfaa;             /* Borders / dividers neutral */
  --rule-soft: rgba(23, 23, 20, 0.08);
  --line: rgba(23, 23, 20, 0.10);

  /* ─── INK (text colors) ─────────────────────────────────────── */
  --ink: #171714;              /* Primary text */
  --ink-soft: #54554e;         /* Secondary text */
  --ink-muted: #8a7f6a;        /* Tertiary text / hints */
  --ink-ghost: #b0a898;        /* Disabled / placeholders */
  --ink-dark: #0f1117;         /* Dark backgrounds (chronicle hero, wiggmatch) */
  --ink-darker: #1c1710;       /* Newsletter footer dark */

  /* ─── FONTS ─────────────────────────────────────────────────── */
  --font-display: 'Fraunces', Georgia, serif;
  --font-ui: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
  --font-brand-italic: 'Cormorant Garamond', 'Playfair Display', Georgia, serif;
  /* Per-category font overrides (city chronicles intentional variation) */

  /* ─── SPACING (T-shirt scale) ───────────────────────────────── */
  --space-1: 4px;   --space-2: 8px;   --space-3: 12px;  --space-4: 16px;
  --space-5: 20px;  --space-6: 24px;  --space-8: 32px;  --space-10: 40px;
  --space-12: 48px; --space-16: 64px;

  /* ─── RADII ─────────────────────────────────────────────────── */
  --radius-xs: 2px;            /* Boutons + cards Sprint 1 style */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-pill: 999px;

  /* ─── SHADOWS ───────────────────────────────────────────────── */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 6px 24px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 12px 34px rgba(25, 20, 12, 0.06);
  --shadow-cta: 0 2px 8px rgba(34, 197, 94, 0.35);

  /* ─── Z-INDEX ───────────────────────────────────────────────── */
  --z-skip-link: 100000;
  --z-header: 9999;
  --z-modal: 10001;
  --z-toast: 11000;
}

/* ─── Category-color convention (Sprint 1 a749c8e + Sprint Y) ───
   Chronicles index pages and city chronicles use signature colors.
   Pages declare them via <meta name="theme-color" content="#X" data-category-color="Y">.
   No CSS variable is generated automatically — pages with their own
   accent palette continue to use locally-scoped vars (city chronicles
   pattern preserved per memory:city-chronicles-format.md). */

/* ─── Fallback for old browsers without var support ─────────────
   Sites that import this file should still display correctly if a
   browser lacks CSS custom properties. Modern Netlify traffic = 99%+
   support so we don't pollute with fallbacks here, but DO repeat
   critical hex inline on the body background for FOUC safety. */
```

### 2.2 Convention `data-category-color` officialisée

Documenter dans `tokens.css` (commentaire) :

| Catégorie | Couleur | Usage |
|---|---|---|
| `family` | `#d7731d` (orange) | `chronicles-family.html` index — convention Sprint 1 a749c8e |
| `horizons` | `#7d55d8` (violet) | `chronicles-horizons.html` index — convention Sprint 1 a749c8e |
| `villes` (générique) | `#1a5430` (forest) | `chronicles-villes.html` index |
| `dest` | `#1a5430` | `chronicles-dest.html` index |
| `visas` | `#1a5430` | `chronicles-visas.html` index |
| `city-{slug}` | variable per city | 76 villes × leurs accents propriétaires |

### 2.3 Impact estimé sur les 700+ fichiers HTML

| Section | Fichiers | Action requise | Effort |
|---|---|---|---|
| Pages racine `/en/`, `/fr/`, `/es/` | 14 | Inject `<link rel="stylesheet" href="/assets/wm-tokens.css">` + remplacer `:root{...}` inline par usage des vars | 2-3h |
| Wiggmatch × 3 | 3 | idem (via `build_wiggmatch_trilingual.py`) | 30 min |
| LP × 9 + lead-magnet × 3 | 12 | idem | 1h |
| Country pages | 484 | Régénération via `_gen_v3.py` ou `scripts/build_country_pages.py` (existant) | 2-4h |
| Chronicles thématiques | 75 | Régénération via script (à créer ?) ou manuel | 4-6h |
| Chronicles villes | 228 | **Préserver palette per-city** + injecter tokens.css base | 2-3h |
| Compare.html + compare/static | 65 | Refonte palette → off-charter à purger | 4-6h |
| Connect/* | 6 | Idem (auth pages) | 1h |

**Total estimé** : **15-25h dev**.

---

## 3. Stratégie d'exécution

### 3.1 Découpage en 6 lots

| Lot | Périmètre | Effort | Risque |
|---|---|---|---|
| **Y.1** | Créer `/assets/wm-tokens.css` + valider décisions D1-D6 + mettre à jour AUDIT.md item 2 | 2h | Très faible |
| **Y.2** | Migration des 14 pages racine `/en/`, `/fr/`, `/es/` (load tokens.css + purge couleurs/fonts inline drift) | 3h | Faible |
| **Y.3** | Régénération scripted des 484 country pages (`scripts/build_country_pages.py` ou nouveau script) | 4-6h | Modéré (point de non-retour) |
| **Y.4** | Régénération scripted des 75 chronicles thématiques | 4h | Modéré |
| **Y.5** | Hero JPG country pages → `<picture>` SSR (active enfin `window.__WM_DISABLE_WEBP_SWAP=true` sur ces pages) + compression assetscity/ batch | 3-4h | Faible (déjà préparé Sprint D1) |
| **Y.6** | Chronicles villes (228) — base tokens + palette per-city préservée + Compare/static refonte (différable) | 4-5h | Modéré-élevé (volume) |

**Total : ~20-24h**, étalé sur 1-2 semaines avec validation entre Y.2 et Y.3.

### 3.2 Pages racine d'abord (Y.2) ou tout d'un coup ?

**Recommandation : pages racine d'abord, validation, puis régénération massive.**

**Pourquoi** :
- Y.2 touche 14 fichiers — dégât maximal en cas de bug = 14 pages.
- Y.3 touche 484 country pages d'un coup — dégât maximal = TOUT le SEO long-tail country.
- Validation visuelle entre Y.2 et Y.3 = garde-fou critique.
- Si Y.2 révèle un problème dans tokens.css, on corrige avant que ça contamine 484 pages.

### 3.3 Scripted vs manuel

| Section | Méthode | Justification |
|---|---|---|
| Pages racine (14) | **Manuel** (Edit ciblé) | Diversité de structure, peu de fichiers |
| Wiggmatch × 3 | **Re-run** `build_wiggmatch_trilingual.py` | Déjà idempotent |
| LP + lead-magnet | **Manuel** ou script ad-hoc | 12 fichiers, peu de structure répétée |
| Country pages 484 | **Script obligatoire** (`scripts/build_country_pages.py` existant ou nouveau) | Volume + cohérence |
| Chronicles thématiques 75 | **Script** (à créer) ou **manuel par lot de 5** | Volume |
| Chronicles villes 228 | **Script** (créer `build_chronicle_villes.py`) | Volume + préservation per-city palette |
| Compare/static 64 | **Script** ou **différer Sprint Y'** | Volume + isolation |

### 3.4 Hero JPG <picture> SSR (Y.5)

L'idée : sur chaque country page régénérée en Y.3, remplacer
```html
<img src="/assets/hero-portugal.jpg" alt="Portugal" loading="lazy" onerror="this.style.display='none'">
```
par
```html
<picture>
  <source srcset="/assets/hero-portugal.webp" type="image/webp">
  <img src="/assets/hero-portugal.jpg" alt="Portugal" loading="lazy">
</picture>
```

Et ajouter au `<head>` :
```html
<script>window.__WM_DISABLE_WEBP_SWAP=true;</script>
```

→ Le runtime swap de `footer.js` ne s'exécute plus → -33 fetches "test" par page → **gain LCP majeur** sur 484 pages.

Pour `assetscity/`, **compression batch** avec `optimize-images.sh` étendu (même pattern que Sprint 1 backlog 3.5).

---

## 4. Décisions à arbitrer

### D1 — Cream officiel

- **(a)** `#f5f0e8` (réalité du code, 22 occurrences + tous les acquis Sprint 1+2+D1+X)
- **(b)** `#ece6d2` (mémoire user, 12 occurrences seulement, peu utilisé)
- **(c)** Aligner sur le trio `#f5f0e8` (bg) + `#f9f5ed`/`#f3ede3` (gradient)

**Recommandation : (c)**. Reflète la réalité multi-surface du repo.

### D2 — Font UI officielle

- **(a)** **Inter** (réalité — 1422 occurrences, dominant après Fraunces)
- **(b)** **Instrument Sans** (charter mémoire user — 3 occurrences, gros chantier de migration)
- **(c)** **Inter** comme UI canonical, **Instrument Sans** réservé à `wiggmatch` (status quo + officialisation de l'exception)

**Recommandation : (c)**. Évite un re-roll massif sur 1422 occurrences pour un gain brand marginal. À reconsidérer en Sprint Y' si volonté éditoriale.

### D3 — Poppins purge

- 1375 occurrences réparties entre `header.js`/`footer.js` (interdiction Sprint 1 levée Sprint D1) et chronicles selon `editorial.md`.
- **(a)** Purger Poppins partout → Inter (recommandé pour cohérence)
- **(b)** Garder Poppins dans `editorial.md` chronicles convention
- **(c)** Documenter Poppins comme exception éditoriale (chronicles only)

**Recommandation : (a)**. Inter couvre déjà tous les usages UI ; Poppins n'apporte pas de différenciation visuelle significative.

### D4 — `#22c55e` officialisation

- **(a)** Garder `#22c55e` Tailwind comme `--cta-bright` officiel (status quo, pragmatique)
- **(b)** Choisir un vert vif WiggMap dédié (ex : `#1ea049` ou `#2bb56a`)

**Recommandation : (a)**. Les utilisateurs sont habitués au vert Tailwind, et `#22c55e` est réutilisable hors marketing (palette accessible + reconnu). À officialiser avec une note "couleur sémantique CTA, pas brand".

### D5 — Compare/static refonte

- 64 pages avec palette `#059669/#22c55e/Playfair Display` off-charter.
- **(a)** Inclure dans Sprint Y (lot Y.6) — +4-6h dev
- **(b)** Différer en **Sprint Y'** dédié — pas dans ce sprint
- **(c)** Quick fix Sprint Y : juste theme-color + canonical (15 min) ; refonte plus tard

**Recommandation : (b)**. Le compare/static est un sous-cluster avec sa logique propre (DOM swap i18n) et doit être traité avec attention. Le différer évite de gonfler ce sprint déjà gros.

### D6 — Source Serif 4 (chronicles éditorial)

`editorial.md` déclare Source Serif 4 comme "corps de texte chronicles". 168 occurrences.
- **(a)** Garder (convention éditoriale documentée)
- **(b)** Purger → Inter
- **(c)** Garder + documenter comme `--font-chronicle-body` dans tokens.css

**Recommandation : (c)**. Préserve le choix éditorial existant (ligne éditoriale longue forme) + l'officialise.

### D7 — Régénération massive (Y.3) : protocole

Les 484 country pages doivent être régénérées en bulk. **Mode** :
- **(a)** Run `_gen_v3.py` (script existant, à adapter)
- **(b)** Run `scripts/build_country_pages.py` (script existant)
- **(c)** Créer `scripts/migrate_country_to_tokens.py` dédié (idempotent)

**Recommandation : (c)**. Permet idempotence + dry-run + self-test (pattern Sprint 2/D1 reproduit).

### D8 — Sprint Y dans une seule PR ou plusieurs ?

- **(a)** Tout dans une PR `sprint-Y-design-system` → review massive
- **(b)** Plusieurs PRs : `sprint-Y1-tokens`, `sprint-Y2-roots`, `sprint-Y3-countries`, `sprint-Y4-chronicles`, `sprint-Y5-images`, etc.

**Recommandation : (b)**. Découpage = rollback chirurgical. Une régression sur Y.3 ne doit pas bloquer Y.5.

---

## 5. Ordre d'exécution sécurisé en lots

### Lot Y.1 — `tokens.css` + arbitrages
**Périmètre** : créer `/assets/wm-tokens.css`, mettre à jour `AUDIT.md` item 2, créer `SPRINT_Y_PLAN.md` (ce fichier).
**Effort** : 2h
**Garde-fous** : validation manuelle des arbitrages D1-D8 par toi.
**Commit** : `feat(tokens): canonical design system in /assets/wm-tokens.css`
**PR** : `sprint-Y1-tokens` → merger après ton OK.

### Lot Y.2 — Pages racine
**Périmètre** : 14 fichiers `/en/`, `/fr/`, `/es/` (Sprint 2 acquis) + 9 LP + 3 lead-magnet + 3 wiggmatch.
**Action** : injecter `<link rel="stylesheet" href="/assets/wm-tokens.css">` dans `<head>` + supprimer/remplacer les `:root{...}` inline qui drift.
**Effort** : 3h
**Garde-fous** : `node --check` sur header/footer si touchés (probable pas), monitor preview, audit auto 3 langs.
**Commit** : `feat(roots): adopt /assets/wm-tokens.css on Sprint 1+2+D1+X pages`
**PR** : `sprint-Y2-roots` → preview + monitor + ton OK avant merge.

### Lot Y.3 — Country pages × 484 (point de non-retour)
**Périmètre** : 484 fichiers `countries/*-{en,fr,es}.html`.
**Action** : créer `scripts/migrate_country_to_tokens.py` (idempotent + dry-run + self-test). Run script. Vérifs auto.
**Effort** : 4-6h
**Garde-fous** : dry-run obligatoire avant execution. Validation HTML + JSON-LD + canonical + hreflang sur 100% des fichiers post-script.
**Commit** : `feat(countries): adopt tokens.css + purge color drift on 484 pages`
**PR** : `sprint-Y3-countries` → preview + sample manual review + ton OK avant merge.

### Lot Y.4 — Chronicles thématiques × 75
**Périmètre** : 75 fichiers `chronicles/*.html` (hors villes).
**Action** : script `migrate_chronicles_to_tokens.py` ou édition lot par lot.
**Effort** : 4h
**Garde-fous** : préserver JSON-LD (FAQPage déjà sur 100%) + hreflang + skip-link.
**Commit** : `feat(chronicles): adopt tokens.css on 75 thematic chronicles`
**PR** : `sprint-Y4-chronicles-thematic`.

### Lot Y.5 — Hero JPG `<picture>` SSR + assetscity/ compression
**Périmètre** : pendant Y.3 (countries), substituer `<img>` par `<picture>` SSR + activer flag `__WM_DISABLE_WEBP_SWAP=true` sur les country pages migrées. Compression `assetscity/*.png` via `optimize-images.sh` étendu.
**Effort** : 3-4h
**Garde-fous** : flag sw.js cache bump v3→v4 (force purge), monitor LCP via Lighthouse spot-check.
**Commit** : `perf(images): <picture> SSR on countries + compress assetscity (-15MB total)`
**PR** : `sprint-Y5-images` (peut être séparée ou couplée avec Y.3).

### Lot Y.6 — Chronicles villes × 228
**Périmètre** : 228 fichiers `chronicles/villes/*.html`.
**Action** : script qui injecte tokens.css mais préserve la palette per-city (locally scoped vars).
**Effort** : 4-5h
**Garde-fous** : grep verifier que les `--g`, `--gd`, `--gp` per-city restent inchangés post-script.
**Commit** : `feat(chronicles-villes): adopt tokens.css base, preserve per-city palette`
**PR** : `sprint-Y6-chronicles-villes`.

### Lots différés (Sprint Y' suggéré)

- Compare.html + compare/static × 64 (D5)
- Refonte JSON-LD chronicles thématiques (item 1.9 AUDIT.md)
- Migration vers Instrument Sans (D2 (b))

---

## 6. Préservation des acquis Sprint 1+2+D1+X

À chaque lot, monitor `monitor_post_merge.py` doit retourner exit 0 sur preview. Items contrôlés :

| Acquis | Méthode de preservation |
|---|---|
| Skip-link `<a class="wm-skip">` partout | Vérif grep post-script (regex match obligatoire) |
| `theme-color #1a5430` sur 14 pages racine | Vérif grep + monitor `check5_no_regression` |
| `data-category-color` sur chronicles-family/horizons | Whitelist dans le script (ne pas écraser) |
| `<link rel="canonical">` per-page | Idempotent — tokens migration ne touche pas ces tags |
| Hreflang quartet | Idem |
| JSON-LD FAQPage / Article / WebApplication / Quiz | Idem |
| Sprint D1 wiggmatch trilingual | Re-run `build_wiggmatch_trilingual.py` après tokens.css créé pour propager le `<link>` |
| Sprint X lead-magnet canonical+hreflang | Idem |
| Monitor `monitor_post_merge.py` | Doit retourner 85+/85+ OK après chaque lot |

---

## 7. Risques majeurs

### R1 — Régénération massive Y.3 = point de non-retour SEO

484 country pages d'un coup. Si bug dans le script → SEO 404 sur toute la longue traîne pays. **Mitigation** :
- Dry-run obligatoire
- Spot-check 5 country pages random après run
- Monitor T+0 après merge (84 pages + redirect-target check)
- Rollback prêt : `git revert` + force-push si régression critique en T+5min

### R2 — Cohérence vs créativité (chronicles villes)

228 chroniques villes ont chacune une palette d'accent propre (#0d9488 Bali teal, #f59e0b Bangkok orange, etc.). Le sprint **doit préserver** cette diversité tout en injectant les tokens base.

**Mitigation** : tokens.css fournit `--green` (charter) + un commentaire qui dit "city chronicles override locally via :root scoped vars". Le script Y.6 ne touche QUE les vars de base, pas les vars per-city.

### R3 — Cache navigateur

Bumper `sw.js` cache `v3 → v4` au début du sprint (Y.1) pour forcer la purge. Sinon, utilisateurs avec SW v3 servent l'ancienne version stylée drift.

### R4 — Compare/static palette refusée → différé

Si D5 = (b), Sprint Y laisse compare.html + 64 sous-pages off-charter. **Acceptable** vu la complexité, à documenter dans `AUDIT.md` comme dette technique.

### R5 — Performances tokens.css

`/assets/wm-tokens.css` chargé sur 700+ fichiers HTML. Si le fichier est mal optimisé → impact LCP. **Mitigation** : minifier (~3KB), `Cache-Control: public, max-age=31536000, immutable` (déjà via Sprint 1 `_headers`), preload sur les pages critiques.

### R6 — JSON-LD préservation

Les 303 chronicles ont déjà FAQPage schema. Le script Y.4 ne doit JAMAIS toucher les blocs JSON-LD existants. **Mitigation** : grep `"FAQPage"` count avant/après.

---

## 8. Estimation totale

| Lot | Effort | Risque | Recommandation |
|---|---|---|---|
| Y.1 (tokens.css) | 2h | Très faible | À faire en premier |
| Y.2 (roots) | 3h | Faible | Validation entre Y.2 et Y.3 |
| Y.3 (countries) | 4-6h | Modéré (PNR) | Dry-run obligatoire |
| Y.4 (chronicles thématiques) | 4h | Modéré | Idempotent |
| Y.5 (images) | 3-4h | Faible | Lié à Y.3 |
| Y.6 (chronicles villes) | 4-5h | Modéré-élevé (volume) | Préserver per-city |

**Total : ~20-24h dev**, **6 PRs distinctes** (D8 (b)), étalé sur **1-2 semaines** avec validations entre chaque lot.

---

## 9. Décisions à valider

Réponds-moi sur D1 → D8 :

```
D1 (cream): a | b | c       — recommandé: c
D2 (font UI): a | b | c     — recommandé: c
D3 (Poppins purge): a | b | c — recommandé: a
D4 (#22c55e CTA): a | b     — recommandé: a
D5 (compare refonte): a | b | c — recommandé: b
D6 (Source Serif): a | b | c — recommandé: c
D7 (regen script): a | b | c — recommandé: c
D8 (1 PR vs N PRs): a | b   — recommandé: b
```

Avec tes 8 réponses, je démarre Y.1 immédiatement.

---

*Plan rédigé le 2026-05-04. Aucun fichier source modifié dans cette phase. En attente arbitrage D1-D8.*
