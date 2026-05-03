# AUDIT_PREVIEW_D1 — Sprint D1 wiggmatch trilingual

> **Date** : 2026-05-04
> **Branche** : `sprint-D1-wiggmatch-trilingual`
> **PR** : #2 (https://github.com/wiggmap/wiggmap/pull/2)
> **Deploy preview** : https://deploy-preview-2--phenomenal-zabaione-d26a6d.netlify.app
> **Méthode** : audit cURL + Python parsing sur 12 URLs distinctes du preview.

---

## TL;DR

| Check | État |
|---|---|
| 1. Status 200 sur les 3 wiggmatch URLs | ✅ OK |
| 2. JSON-LD parse (3 blocs × 3 fichiers = 9 blocs) | ✅ OK |
| 3. Hreflang triplet + x-default → /en/ | ✅ OK |
| 4. Sitemap (924 URLs, wiggmatch trio présent, legacy absent) | ✅ OK |
| 5. Sprint 1 non-régressé (skip-link, theme-color, lang attr) | ✅ OK |

**Bilan : 5/5 checks OK.** Aucun blocker détecté côté technique. Le merge sur `main` peut être autorisé après ta validation manuelle (lancer le quiz dans chaque langue + vérifier que le scoring renvoie la même top-ville pour les mêmes réponses sur les 3 langues + tester l'email gate).

---

## CHECK 1 — Status 200 sur les 3 wiggmatch URLs

| URL preview | Status | Body length | OK |
|---|---|---|---|
| `/en/wiggmatch.html` | 200 | ~152 KB | ✅ |
| `/fr/wiggmatch.html` | 200 | ~152 KB | ✅ |
| `/es/wiggmatch.html` | 200 | ~152 KB | ✅ |

Les 3 fichiers générés par `scripts/build_wiggmatch_trilingual.py` (commit D1.3) sont correctement servis par Netlify.

---

## CHECK 2 — JSON-LD parse (9 blocs au total)

Pour chaque variante, 3 blocs `<script type="application/ld+json">` détectés, tous parsent valides :

| URL | @type[0] | @type[1] | @type[2] | inLanguage |
|---|---|---|---|---|
| `/en/wiggmatch.html` | `WebApplication` | `Quiz` | `BreadcrumbList` | `en` (sur 1 et 2) |
| `/fr/wiggmatch.html` | `WebApplication` | `Quiz` | `BreadcrumbList` | `fr` (sur 1 et 2) |
| `/es/wiggmatch.html` | `WebApplication` | `Quiz` | `BreadcrumbList` | `es` (sur 1 et 2) |

`inLanguage` correctement aligné sur la lang du fichier (string, plus l'array `["en","fr","es"]` qui était présent en Sprint 2 et n'était pas sémantiquement correct).

---

## CHECK 3 — Hreflang triplet + x-default

Pour chaque variante, 4 `<link rel="alternate" hreflang="...">` détectés :

| URL | Hreflangs | x-default | OK |
|---|---|---|---|
| `/en/wiggmatch.html` | `en`, `fr`, `es`, `x-default` | `https://wiggmap.com/en/wiggmatch.html` | ✅ |
| `/fr/wiggmatch.html` | `en`, `fr`, `es`, `x-default` | `https://wiggmap.com/en/wiggmatch.html` | ✅ |
| `/es/wiggmatch.html` | `en`, `fr`, `es`, `x-default` | `https://wiggmap.com/en/wiggmatch.html` | ✅ |

- x-default → `/en/wiggmatch.html` cohérent avec D4 (EN-source pour wiggmatch).
- Toutes les hreflang URLs sont absolues (`https://...`), aucune relative.

---

## CHECK 4 — Sitemap

```
GET /sitemap.xml → 200 OK
URL count: 924 (attendu 924) ✓

Wiggmatch URLs présentes:
  ✓ https://wiggmap.com/en/wiggmatch.html  (4 hreflang dans sitemap)
  ✓ https://wiggmap.com/fr/wiggmatch.html  (4 hreflang dans sitemap)
  ✓ https://wiggmap.com/es/wiggmatch.html  (4 hreflang dans sitemap)

Legacy /wiggmatch.html: ABSENT ✓ (exclu via MIGRATED_TO_LANG_DIRS)
Google verify file: ABSENT ✓ (exclu via regex google[a-f0-9]{16,}\.html$)
```

---

## CHECK 5 — Sprint 1 non régressé

| URL | skip-link | theme-color | html lang | canonical (self) | title keyword | OK |
|---|---|---|---|---|---|---|
| `/en/wiggmatch.html` | ✓ wm-skip + #wm-main | `#1a5430` | `en` | self ✓ | "Find your" ✓ | ✅ |
| `/fr/wiggmatch.html` | ✓ wm-skip + #wm-main | `#1a5430` | `fr` | self ✓ | "Trouve ta" ✓ | ✅ |
| `/es/wiggmatch.html` | ✓ wm-skip + #wm-main | `#1a5430` | `es` | self ✓ | "Encuentra tu" ✓ | ✅ |

WM_I18N + WM_DYN dictionnaires présents et `wmDetectLang()` (D1.1) préservé sur les 3 fichiers.

---

## À valider manuellement avant merge sur main

L'audit auto valide la *forme* (HTML, JSON-LD, hreflang, sitemap, non-régression Sprint 1). La *fonction* (le quiz fonctionne, l'email gate déclenche, le scoring est cohérent) requiert un test manuel sur le preview :

1. **Lancer le quiz dans chaque langue** :
   - `https://deploy-preview-2--phenomenal-zabaione-d26a6d.netlify.app/en/wiggmatch.html`
   - `https://deploy-preview-2--phenomenal-zabaione-d26a6d.netlify.app/fr/wiggmatch.html`
   - `https://deploy-preview-2--phenomenal-zabaione-d26a6d.netlify.app/es/wiggmatch.html`
   → Vérifier : 8 questions affichées, options traduites, navigation Continue/Continuer/Continuar fonctionne.

2. **Test de cohérence du scoring** (le plus important) :
   Répondre aux **mêmes 8 réponses** sur les 3 langues → la **même top-ville** doit être recommandée. Le scoring engine est lang-independent (lignes 1602-1696 du fichier), donc en cas d'écart c'est qu'on a cassé quelque chose.

3. **Email gate** :
   Cliquer sur le bouton "Reveal the 2 cities" / "Découvrir les 2 villes" / "Descubrir las 2 ciudades" → modal email s'affiche, soumission test avec un email réel → vérifier dans Netlify Forms dashboard que la soumission apparaît dans le formulaire `wiggmatch-leads`.

4. **Lang switcher** :
   - Sur `/en/wiggmatch.html`, cliquer le drapeau FR → arrive sur `/fr/wiggmatch.html` (PAS `/fr/`).
   - Cliquer le drapeau EN sur la même page → no-op (déjà sur EN, pas de reload, état du quiz préservé).
   - Refaire : commencer le quiz EN à la Q3, switcher à FR → arrive sur `/fr/wiggmatch.html` à la Q1 (état perdu, normal).

5. **Aucune bannière "untranslated"** sur les 3 (chaque variante = source per D4).

6. **Console DevTools** : zéro erreur JS sur les 3 versions au chargement et pendant le quiz.

---

## Recommandation post-validation

Si les 6 tests manuels ci-dessus passent → tu peux merger la PR via GitHub UI (squash ou merge commit). Le hotfix `a0d4149` (déjà sur main) reste.

Après merge, lancer en local :
```bash
git pull origin main
python3 scripts/monitor_post_merge.py --quiet
```

Le monitoring devrait passer **74/74 OK** (les 2 KO actuels `/en/wiggmatch.html` et `/es/wiggmatch.html` deviennent verts).

---

*Audit produit le 2026-05-04. AUDIT_PREVIEW_D1.md commité immédiatement après cette rédaction (D1.6).*
