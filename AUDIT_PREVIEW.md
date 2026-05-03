# AUDIT_PREVIEW — Sprint 2 Lot 11

> **Date** : 2026-05-03
> **Branche** : `sprint-2-trilingual-roots`
> **Deploy preview** : https://deploy-preview-1--phenomenal-zabaione-d26a6d.netlify.app
> **Méthode** : audit automatisé via cURL + parser Python sur 50+ URLs distinctes du preview.

---

## TL;DR

| Check | État | Notes |
|---|---|---|
| 1. HTTP / canonical / lang / robots / banner | ⚠️ KO **(faux positif)** | 2 lignes en KO uniquement à cause d'un bug dans le test. Le site est correct. |
| 2. Hreflang sur 5 pages échantillon | ✅ OK | x-default correct (EN ou FR selon D4/D5), 4 alternates par page, URLs absolues. |
| 3. Sitemap | ✅ OK | 922 URLs, hreflang correct, legacy absentes. |
| 4. robots.txt | ✅ OK | Allow lang-dirs + Disallow tighten + Sitemap declaration présents. |
| 5. JSON-LD on /{en,fr,es}/about.html | ✅ OK | AboutPage + Organization + BreadcrumbList parsent sur les 3 variantes. |
| 6. _redirects sur legacy URLs | ❌ KO **(vrai bug)** | 1 règle (`/compare.html *`) ne match pas l'URL nue, et la query string n'est pas préservée → fix proposé. |
| 7. Service Worker | ✅ OK | `wiggmap-v3` actif, 5 core assets dont les 3 lang homes. |
| 8. Sprint 1 non régressé | ✅ OK | bc.webp preload, skip-link, theme-color #1a5430 tous présents sur /en/. |

**Bilan** : 6/8 OK + 1 faux positif + **1 vrai bug bloquant** (Check 6, `/compare.html` sans query). **STOP avant Lot 12** comme convenu, ping pour décision.

---

## CHECK 1 — Réponse HTTP par URL (39 URLs migrées + 3 legacy)

### Résultats résumés

- **39 URLs `/en/*`, `/fr/*`, `/es/*`** : toutes retournent **HTTP 200** ✓
- **`<html lang>` cohérent** : 39/39 corrects
- **`<meta robots noindex,follow>`** : présent uniquement sur les variantes non-source-of-truth (24/39 attendus → 24/39 trouvés ✓)
- **Bannière `.wm-untranslated-banner`** : présente partout où attendue ✓
- **Canonicals** : 37/39 corrects, 2 lignes en KO **mais c'est un bug de mon test, pas du site**.

### KO détail — faux positifs (test corrige nécessaire, site OK)

| URL preview | Canonical retourné | Mon test attendait | Vraie attente per D4/D5 |
|---|---|---|---|
| `/fr/` | `https://wiggmap.com/en/` | `https://wiggmap.com/fr/` (faux) | `https://wiggmap.com/en/` ✓ |
| `/es/` | `https://wiggmap.com/en/` | `https://wiggmap.com/es/` (faux) | `https://wiggmap.com/en/` ✓ |

**Diagnostic** : `index.html` est EN-source per D4/D5. Donc `/fr/` (variante non-traduite) doit pointer son canonical vers `/en/` (la version source). C'est exactement ce que le site fait. Mon test avait un bug : `expected_canon = f"{PROD}/{lg}/" if page == 'index.html' else ...` — le ternaire devrait dépendre de `lg == src_lang`, pas de `page == 'index.html'`. Le `page == 'index.html'` ne vérifie pas la cohérence source-of-truth.

**Action** : pas de fix sur le site nécessaire. Si je devais re-runner l'audit, je corrigerais juste la condition du test.

### Spot checks sur 3 URLs legacy

| URL | Status réel | Location réelle | Comportement |
|---|---|---|---|
| `/` | 301 | `/en/` | ✓ redirige vers EN |
| `/index.html` | 301 | `/en/` | ✓ redirige vers EN |
| `/about.html` | 301 | `/en/about.html` | ✓ redirige (Sprint 2 Lot 4 actif) |

> **Important** : contrairement à mon hypothèse Lot S4 ("staged inactive jusqu'à suppression des fichiers"), Netlify applique les `301!` **immédiatement** (le `!` force le redirect même si le fichier source existe). Les 301 sont donc déjà actifs en preview. Le Lot 12 (suppression fichiers source) reste utile pour le ménage du repo, mais n'est PAS le déclencheur SEO comme initialement prévu — les 301 sont déjà actifs ici.

---

## CHECK 2 — Hreflang sur 5 pages échantillon

| URL | Hreflangs | Langues | x-default | Attendu | OK |
|---|---|---|---|---|---|
| `/en/about.html` | 4 | en, fr, es, x-default | `https://wiggmap.com/en/about.html` | EN-source → /en/ | ✅ |
| `/fr/about.html` | 4 | en, fr, es, x-default | `https://wiggmap.com/en/about.html` | EN-source → /en/ | ✅ |
| `/en/chronicles-villes.html` | 4 | en, fr, es, x-default | `https://wiggmap.com/fr/chronicles-villes.html` | FR-source → /fr/ | ✅ |
| `/fr/chronicles-villes.html` | 4 | en, fr, es, x-default | `https://wiggmap.com/fr/chronicles-villes.html` | FR-source → /fr/ | ✅ |
| `/en/` | 4 | en, fr, es, x-default | `https://wiggmap.com/en/` | EN-source → /en/ | ✅ |

Toutes les hreflang URLs sont absolues (commencent par `https://`) ✓.
Tous les x-default cohérents avec D4/D5 ✓.

---

## CHECK 3 — Sitemap

```
GET /sitemap.xml → 200 OK
URL count: 922 (attendu 922) ✓
Hreflang sur /en/about.html: 4 xhtml:link (attendu 4) ✓
Lang-dir URLs présentes: 39/39 (attendu 39) ✓
Legacy URLs en doublon: 0 (testé /about.html, /compare.html, /globe.html,
  /chronicles-villes.html, /terms.html — toutes absentes du sitemap) ✓
```

---

## CHECK 4 — robots.txt

```
GET /robots.txt → 200 OK
✓ Allow: /en/
✓ Allow: /fr/
✓ Allow: /es/
✓ Disallow: /onboarding.html
✓ Disallow: /forms.html
✓ Disallow: /index.html.bak
✓ Disallow: /index.html.old
✓ Sitemap: https://wiggmap.com/sitemap.xml
```

8/8 attendus présents.

---

## CHECK 5 — JSON-LD sur /{en,fr,es}/about.html

| Variante | Blocs trouvés | @type listés | Validation |
|---|---|---|---|
| `/en/about.html` | 3 | AboutPage, Organization, BreadcrumbList | ✅ tous parsent |
| `/fr/about.html` | 3 | AboutPage, Organization, BreadcrumbList | ✅ tous parsent |
| `/es/about.html` | 3 | AboutPage, Organization, BreadcrumbList | ✅ tous parsent |

Aucune régression vs Sprint 1 (les schémas créés en commit `c4be2c7` sont préservés tels quels par `migrate_to_lang_dirs.py`).

---

## CHECK 6 — _redirects active behavior — ❌ KO

### Résumé

| URL legacy | Status | Location | Attendu | OK |
|---|---|---|---|---|
| `/about.html` | 301 | `/en/about.html` | 301 → /en/about.html | ✅ |
| **`/compare.html`** | **200** | (pas de Location) | 301 → /en/compare.html | ❌ |
| `/globe.html` | 301 | `/en/globe.html` | 301 → /en/globe.html | ✅ |
| `/chronicles-villes.html` | 301 | `/fr/chronicles-villes.html` | 301 → /fr/chronicles-villes.html | ✅ |
| `/chronicles-family.html` | 301 | `/fr/chronicles-family.html` | 301 → /fr/chronicles-family.html | ✅ |
| `/terms.html` | 301 | `/en/terms.html` | 301 → /en/terms.html | ✅ |
| `/wiggmatch.html` | 301 | `/fr/wiggmatch.html` | 301 → /fr/wiggmatch.html | ✅ |
| `/` | 301 | `/en/` | 301 → /en/ | ✅ |
| `/index.html` | 301 | `/en/` | 301 → /en/ | ✅ |
| **`/compare.html?c=fr,jp,br`** | **200** | (pas de Location) | 301 → /en/compare.html?c=fr,jp,br | ❌ |

8/10 OK. **2 KO concernent uniquement `/compare.html`** (avec et sans query string).

### Diagnostic du bug

Règle actuelle dans `_redirects` :
```
/compare.html *                  /en/compare.html?:splat           301!
```

Le `*` en suffixe est un splat Netlify qui exige **au moins un caractère** après `/compare.html`. Conséquences :

1. `/compare.html` (URL nue) **ne match pas** la règle → Netlify tombe sur le fichier source `/compare.html` qui existe → status 200.
2. `/compare.html?c=fr,jp,br` ne match pas non plus, parce que **la query string n'est pas comptée comme partie du path** par le splat Netlify (le splat capture le path, pas la query). Même résultat : 200, fichier source servi.

Toutes les autres règles (`/about.html`, `/globe.html`, etc.) sont des règles **sans splat** → elles matchent exactement et fonctionnent.

### Fix proposé (à appliquer en commit séparé après ton go)

Remplacer la ligne 32 de `_redirects` :
```
# AVANT
/compare.html *                  /en/compare.html?:splat           301!

# APRÈS (2 lignes : nue + splat)
/compare.html                    /en/compare.html                  301!
/compare.html *                  /en/compare.html?:splat           301!
```

Note : sur Netlify, les query strings sont **par défaut** préservées sur un redirect simple. Il est probable que la 2ᵉ règle (splat) soit même superflue — le test dira. Si la règle nue suffit à préserver `?c=...`, on peut supprimer la règle splat. Test à faire après le fix.

### Impact si Lot 12 lancé sans fix

- `/compare.html` continue de servir l'ancien fichier (200) tant qu'il existe.
- Si Lot 12 supprime `compare.html` du repo → la règle splat ne match toujours pas l'URL nue → **404 sur `/compare.html`** au lieu d'un 301 vers `/en/compare.html`.
- **Régression SEO** : tous les backlinks vers `/compare.html` cassent.
- **Régression user** : le CTA "Compare" depuis le header (qui pointe encore peut-être vers `/compare.html?c=...` selon où la JS a été mise à jour) tombe en 404.

→ **Lot 12 absolument bloqué tant que ce fix n'est pas appliqué.**

---

## CHECK 7 — Service Worker

```
GET /sw.js → 200 OK
✓ CACHE_NAME = "wiggmap-v3"
✓ Core assets: "/", "/en/", "/fr/", "/es/", "/manifest.webmanifest"
```

Tous attendus présents.

---

## CHECK 8 — Sprint 1 non régressé sur /en/

```
GET /en/ → 200 OK
✓ <link rel="preload" as="image" href="/assets/bc.webp" type="image/webp" fetchpriority="high">
✓ <a class="wm-skip" href="#wm-main">Skip to content</a>
✓ <a id="wm-main" tabindex="-1"></a>
✓ <meta name="theme-color" content="#1a5430">
```

4/4 sprintage 1 préservé sur la nouvelle structure ✓.

---

## Décisions / actions requises

### Bug bloquant (Lot 12 verrouillé)

**B1** — Corriger `_redirects` ligne `/compare.html *` :
- Ajouter une règle nue `/compare.html  /en/compare.html  301!` AVANT la règle splat.
- Tester si la règle nue suffit à préserver les query strings (Netlify le fait par défaut).
- Si oui, supprimer la règle splat redondante.
- Re-runner Lot 11 (curl test sur `/compare.html` et `/compare.html?c=fr,jp,br`) pour confirmer 301 dans les deux cas.

**Estimation fix B1** : 5 min écriture + 1 commit + ~30s pour re-tester via cURL.

### Faux positifs (pas d'action site)

**FP1** — Mon script de test avait un bug d'attente sur les canonicals `/fr/` et `/es/`. Le site est correct. Pour ré-audit propre, corriger la condition `expected_canon = f"{PROD}/{src_lang}/"` quand `lg != src_lang` pour les pages index.html. Pas critique — le constat manuel sur le preview confirme que le site fait bien la bonne chose.

### Observations factuelles à documenter

**O1** — Les `301!` sont déjà actifs malgré la présence des fichiers source dans le repo. Mon hypothèse "staged inactive" du Lot S4 était fausse. Conséquence positive : les 301 SEO sont déjà fonctionnels en preview, on peut valider leur effet sans attendre Lot 12. Le Lot 12 reste utile pour le **nettoyage du repo** (supprimer les 13 fichiers source devenus redondants), mais ce n'est plus le **point de bascule SEO** comme prévu — le bascule a déjà eu lieu via les `301!` du Lot S4.

**O2** — En conséquence : Lot 12 perd un peu de sa criticité. Le risque réel résiduel est que la suppression des fichiers source casserait la règle splat `/compare.html *` (qui ne match déjà pas correctement) → **fix B1 obligatoire avant Lot 12**.

---

## Récap final

- **6 checks OK** sur 8 (Checks 2, 3, 4, 5, 7, 8 verts).
- **1 faux positif** (Check 1, 2 lignes liées à un bug de mon test, site OK confirmé manuellement).
- **1 vrai bug** (Check 6, règle `/compare.html *` ne match ni l'URL nue ni l'URL avec query string) → **fix B1 requis avant Lot 12**.

**STOP, ping pour décision** :

1. Veux-tu que j'applique le fix B1 (modif `_redirects` ligne 32) en commit dédié sur la même branche, puis re-runne Lot 11 partiel sur `/compare.html` uniquement pour confirmer le passage à 301 ?
2. Une fois B1 corrigé et re-vérifié, Lot 12 redevient envisageable. Mais comme observé en O1/O2, son enjeu SEO est désormais limité au nettoyage. Tu peux choisir de le reporter à un sprint "repo cleanup" séparé si tu préfères ne pas casser l'option de rollback rapide (revert _redirects → fichiers source servis instantanément).

Lot 12 reste verrouillé jusqu'à ton go explicite.

---

*Audit produit le 2026-05-03. AUDIT_PREVIEW.md sera commité immédiatement après la rédaction (sans aucune autre modification de fichier).*
