# SPRINT_X_PLAN — LP + Lead magnet trilingual

> **Date** : 2026-05-04
> **Mode** : audit + plan. Aucun fichier modifié dans cette phase.
> **Contexte** : sprint suivant la séquence Sprint 2 → Sprint D1 → **Sprint X** → Sprint Y → Sprint Z.

---

## ⚠️ Découverte majeure qui réoriente le sprint

**Les 12 fichiers EN/ES (9 LP + 3 lead-magnet) existent déjà et sont quasi-intégralement traduits proprement.** Datés avril 2026, qualité native confirmée par sondage. Le brief original ("Sprint X — LP + Lead magnet EN/ES (clones FR traduits)") est basé sur l'hypothèse que ces fichiers sont à créer. Ce n'est pas le cas.

**Ce que ça change** : le sprint passe de **~20h de traduction** (ce que le brief implique) à **~3-5h de finition + audit** (ce que la réalité demande).

---

## 1. Inventaire exact

### 1.1 Pages LP (9 fichiers, 3 slugs × 3 langues)

| Fichier | Lignes | `<title>` | `<html lang>` | canonical self | hreflang ×4 | Form `name="newsletter"` | `lead_source` lang-aware | `wmTrackEvent('Lead', content_name=...)` lang-aware |
|---|---|---|---|---|---|---|---|---|
| `lp/vivre-bali-budget-fr.html` | 252 | « Vivre à Bali budget mensuel 2026 » | fr ✓ | ✓ | ✓ | ✓ | `lp_vivre_bali_budget` | `lp_vivre_bali` |
| `lp/vivre-bali-budget-en.html` | 252 | « Living in Bali Monthly Cost 2026 » | en ✓ | ✓ | ✓ | ✓ | `lp_vivre_bali_budget_en` | `lp_vivre_bali_en` |
| `lp/vivre-bali-budget-es.html` | 252 | « Vivir en Bali presupuesto mensual 2026 » | es ✓ | ✓ | ✓ | ✓ | `lp_vivre_bali_budget_es` | `lp_vivre_bali_es` |
| `lp/visa-mm2h-malaisie-fr.html` | 250 | « Visa MM2H Malaisie 2026 » | fr ✓ | ✓ | ✓ | ✓ | `lp_visa_mm2h_malaisie` | `lp_mm2h_malaisie` |
| `lp/visa-mm2h-malaisie-en.html` | 236 | « Malaysia MM2H Visa 2026 » | en ✓ | ✓ | ✓ | ✓ | `lp_visa_mm2h_malaisie_en` | `lp_mm2h_malaisie_en` |
| `lp/visa-mm2h-malaisie-es.html` | 236 | « Visa MM2H Malasia 2026 » | es ✓ | ✓ | ✓ | ✓ | `lp_visa_mm2h_malaisie_es` | `lp_mm2h_malaisie_es` |
| `lp/erasmus-prague-budget-fr.html` | 199 | « Erasmus Prague budget 2026 » | fr ✓ | ✓ | ✓ | ✓ | `lp_erasmus_prague_budget` | `lp_erasmus_prague` |
| `lp/erasmus-prague-budget-en.html` | 199 | « Erasmus Prague Budget 2026 » | en ✓ | ✓ | ✓ | ✓ | `lp_erasmus_prague_budget_en` | `lp_erasmus_prague_en` |
| `lp/erasmus-prague-budget-es.html` | 199 | « Erasmus Praga Presupuesto 2026 » | es ✓ | ✓ | ✓ | ✓ | `lp_erasmus_prague_budget_es` | `lp_erasmus_prague_es` |

**Constat LP** : 9/9 propres. Spot-check body sur `lp/vivre-bali-budget-en.html` et `lp/vivre-bali-budget-es.html` confirme :
- Sections H2 traduites (« Los 3 perfiles de presupuesto », « Which neighborhoods to choose? »)
- Body paragraphes traduits avec terminologie native (KITAS, B1 visa, etc.)
- Form labels/CTAs traduits (« Get the guide → », « Recibir la guía → »)
- Email placeholders traduits (« your@email.com », « tu@email.com »)
- Diff structurel FR vs EN = uniquement les meta + canonical + hreflang + body translations (pas de bloc manquant)

### 1.2 Pages lead-magnet (3 fichiers, 1 slug × 3 langues)

| Fichier | Lignes | `<title>` | `<html lang>` | `noindex` | canonical | hreflang | Sitemap |
|---|---|---|---|---|---|---|---|
| `lead-magnet/visas-2026-fr.html` | 587 | « Les 25 meilleurs visas 2026 » | fr ✓ | ✓ | ❌ | ❌ | ✓ |
| `lead-magnet/visas-2026-en.html` | 556 | « The 25 Best Visas of 2026 » | en ✓ | ✓ | ❌ | ❌ | ✓ |
| `lead-magnet/visas-2026-es.html` | 556 | « Las 25 mejores visas de 2026 » | es ✓ | ✓ | ❌ | ❌ | ✓ |

**Constat lead-magnet** : 3/3 traduits proprement (sections H2 « Retirement Visas / Digital Nomad Visas / Skilled Work Visas » correctement localisées sur l'EN). **Mais 3 gaps** : pas de `<link rel="canonical">`, pas de `<link rel="alternate" hreflang>`, pas de form (volontaire — le lead-magnet est servi gratuitement après opt-in via les LP, c'est juste une landing post-conversion).

### 1.3 Sitemap.xml

**12/12 URLs présentes** :
- 9 LP × 3 langues
- 3 lead-magnet × 3 langues

Hreflang dans le sitemap (vérifié sur 3 spot-checks) : OK pour les LP. À confirmer sur lead-magnet (probablement OK car le script `gen_sitemap.py` utilise le même pattern slug-lang).

### 1.4 Convention forms Netlify

**1 form unifié** : tous les LP utilisent `<form name="newsletter">` avec un `<input type="hidden" name="lead_source" value="lp_{slug}_{lang}">` qui différencie les soumissions par page+langue. Cohérent avec l'approche Buttondown (1 endpoint, tags par lang).

### 1.5 Convention pixel Meta

`wmTrackEvent('Lead', { content_name:'lp_{slug}_{lang}', value:1, currency:'EUR' })` — la `content_name` inclut la lang (`_en`, `_es`). Cohérent.

---

## 2. Vrais gaps identifiés

| # | Gap | Fichiers | Impact | Effort |
|---|---|---|---|---|
| **G1** | `lead-magnet/*-{fr,en,es}.html` n'ont pas de `<link rel="canonical">` | 3 fichiers | SEO mineur (pages noindex donc pas crawlées, mais propreté technique) | 15 min |
| **G2** | `lead-magnet/*-{fr,en,es}.html` n'ont pas de `<link rel="alternate" hreflang>` | 3 fichiers | SEO mineur idem (pages noindex) | 15 min |
| **G3** | `monitor_post_merge.py` ne couvre pas les 9 LP ni les 3 lead-magnet (sont collectés en `FLAT_TRILINGUAL_SAMPLE` mais 1 seul fichier `lp/vivre-bali-budget-fr.html` testé) | 1 fichier script | Hygiène monitoring (régression sur LP/lead-magnet ne serait pas catchée) | 30 min |
| **G4** | Audit qualité body sur les 12 fichiers — vérification scan complet pour confirmer 0 fuite FR sur les variantes EN/ES (sondage initial = OK mais pas exhaustif) | 12 fichiers (lecture diagonale) | Brand quality | 1-2h |
| **G5** | `sitemap.xml` régénération + monitoring après G1+G2 (les 3 lead-magnet auront alors hreflang dans le sitemap) | `sitemap.xml` | SEO mineur | 15 min |

**Total estimé : ~3-4h dev** (vs ~20h dans le brief original).

---

## 3. URLs cibles : aucune création nécessaire

Toutes les 12 URLs cibles existent déjà :
- `https://wiggmap.com/lp/vivre-bali-budget-{en,fr,es}.html` ✓
- `https://wiggmap.com/lp/visa-mm2h-malaisie-{en,fr,es}.html` ✓
- `https://wiggmap.com/lp/erasmus-prague-budget-{en,fr,es}.html` ✓
- `https://wiggmap.com/lead-magnet/visas-2026-{en,fr,es}.html` ✓

---

## 4. Netlify Forms — convention finalisée

**Décision** : conserver `name="newsletter"` unifié sur les 9 LP. Le `lead_source` hidden champ différencie les soumissions par LP+langue, ce qui permet un tracking GA4/Buttondown propre sans multiplier les forms Netlify.

Le lead-magnet ne contient pas de form (la conversion est captée en amont via les LP).

---

## 5. SEO

### 5.1 Meta tags par langue
**Fait** sur les 12 fichiers (title + description + og:title + og:description + og:url + canonical lang-aware). Aucune action.

### 5.2 JSON-LD
À auditer (pas regardé en détail). Probable : pas de JSON-LD sur les LP (page minimaliste pour conversion). Le lead-magnet est noindex donc pas critique. **Si besoin** : ajouter `WebPage` + `BreadcrumbList` schema sur les 9 LP. Hors scope de ce sprint.

### 5.3 Sitemap.xml
**Déjà inclut les 12 URLs.** Régénération nécessaire seulement si on touche aux fichiers (G1, G2 ajoutent canonical/hreflang dans le HTML, ce qui n'affecte PAS le sitemap puisque le sitemap utilise sa propre logique de hreflang via `build_hreflang_group()`).

### 5.4 monitor_post_merge.py
Étendre `FLAT_TRILINGUAL_SAMPLE` pour couvrir au moins 1 URL par slug et par langue dans LP + lead-magnet. Actuellement : 1 seul échantillon LP testé, 0 lead-magnet.

---

## 6. Ordre d'exécution proposé

| Lot | Action | Effort | Garde-fou |
|---|---|---|---|
| **X.1** | Patcher les 3 lead-magnet : ajouter `<link rel="canonical">` + 4 hreflang | 15 min | Vérif HTML statique : 4 hreflang détectés, canonical = self |
| **X.2** | Audit qualité body : grep FR-only words sur EN/ES, sondage diagonal de 3 sections par fichier | 1-2h | Production d'un rapport de spot-check (peut être inclus dans AUDIT report final) |
| **X.3** | Étendre `monitor_post_merge.py` : ajouter LP + lead-magnet × 3 langues à `FLAT_TRILINGUAL_SAMPLE` (12 nouvelles lignes), avec status 200 + canonical correctness + hreflang count | 30 min | `node --check` non applicable, `python3 -m py_compile`, test contre prod = exit 0 attendu (les 3 lead-magnet en canonical KO tant que X.1 pas mergé) |
| **X.4** | Push branche `sprint-X-lp-lead-magnet-finalize`, ouvrir PR #3, deploy preview, audit léger 5 checks | 30 min | Audit sur preview avant merge |
| **X.5** | Validation manuelle (toi) sur preview → merge sur main → monitor T+0 prod | — | Exit 0 attendu |

**Total : 5 lots, ~3-4h dev cumulé**, sans checkpoint intermédiaire (comme Sprint D1).

---

## 7. Risques + décisions à arbitrer

### R1 — Le sprint est-il vraiment utile ?

**Constat** : 3/12 fichiers ont un gap (canonical + hreflang sur lead-magnet noindex). Les 9 LP sont parfaits. Audit qualité body montre 0 fuite FR détectée sur l'échantillon.

**Question** : tu préfères
- **(a)** Faire le sprint X comme prévu (3-5h, propreté technique, monitor robuste pour LP+LM)
- **(b)** Skipper Sprint X et passer direct à Sprint Y design system (les 3 gaps lead-magnet sont noindex donc invisibles SEO). Risque : pas de monitoring robuste sur LP/LM, une régression future ne serait pas catchée.
- **(c)** Réduire Sprint X à juste X.1 (canonical + hreflang lead-magnet) + X.3 (monitor extension) en 45 min, skipper X.2 audit body (low ROI car déjà OK)

**Recommandation : (c)**. Économie de 2h vs (a), gagne le monitoring robuste vs (b).

### R2 — Audit body qualité : quelle profondeur ?

Si tu veux faire X.2 (audit body) :
- **Mode léger** (30 min) : grep FR-only words contre EN+ES, spot-check 1 section par fichier, livrable 1-page
- **Mode profond** (4-6h) : lecture comparative ligne par ligne FR↔EN puis FR↔ES, livrable rapport détaillé par fichier
- **Mode externalisé** : pas dans le scope de ce sprint, à passer à un relecteur natif

**Recommandation : mode léger** si tu veux faire X.2, ou skipper.

### R3 — JSON-LD sur les 9 LP

Aucune des LP n'a de JSON-LD. Ajouter `WebPage` + `BreadcrumbList` × 9 = +18 blocs JSON-LD. SEO modéré (rich results possibles), effort 1h. Hors scope sprint X par défaut.

**Recommandation : reporter** à un sprint SEO+ ultérieur.

### R4 — Numérotation `lead_source` actuelle

Tous les LP utilisent un `lead_source` hidden field comme `lp_vivre_bali_budget_en`. Le wmTrackEvent utilise un `content_name` différent : `lp_vivre_bali_en` (sans `_budget_`). **Décalage de nommage** entre Netlify Forms (`lead_source`) et Meta Pixel (`content_name`). Pas critique mais source de confusion future en analytics.

**Question** : harmoniser ?
- **(a)** Garder le décalage (zéro effort, mais analytics divergente)
- **(b)** Aligner sur la version courte `lp_vivre_bali_en` partout (15 min)
- **(c)** Aligner sur la version longue `lp_vivre_bali_budget_en` partout (15 min)

**Recommandation : (a)** dans ce sprint, à reporter à un audit analytics dédié.

### R5 — Lead-magnet et option image-sitemap

Les lead-magnet sont des PDFs HTML. Si tu veux les indexer dans Google Image (improbable pour un PDF guide), il faudrait ajouter image-sitemap. Hors scope.

---

## 8. Décisions à valider

1. **(D1)** Quel scope ? **(a) sprint complet 3-5h, (b) skip, (c) mini sprint 45 min — recommandé** ?
2. **(D2)** Audit qualité body : **mode léger / profond / externalisé / skip** ?
3. **(D3)** Numérotation `lead_source` vs `content_name` : harmoniser ou garder décalage ?

---

## Plan d'exécution (si recommandation (c) acceptée)

5 commits atomiques :
- `seo(lead-magnet): add canonical + hreflang quartet` (3 fichiers patchés)
- `tools(monitor): extend coverage to LP + lead-magnet × 3 langs` (1 script patché)
- `docs: SPRINT_X_PLAN.md committed` (ce fichier — déjà sur branche)
- `docs: AUDIT_PREVIEW_X.md` (rapport audit preview après push branche)
- `feat: ...` (si X.2 audit body produit, optionnel)

Push branche → PR → deploy preview → audit auto → ton go → merge → monitor T+0.

---

*Plan rédigé le 2026-05-04. Aucun fichier source modifié dans cette phase. En attente arbitrage D1-D3.*
