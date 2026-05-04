# AUDIT_PREVIEW_X — Sprint X LP + lead-magnet trilingual finalize

> **Date** : 2026-05-04
> **Branche** : `sprint-X-lp-lead-magnet-finalize`
> **PR** : #3 (https://github.com/wiggmap/wiggmap/pull/3)
> **Deploy preview** : https://deploy-preview-3--phenomenal-zabaione-d26a6d.netlify.app
> **Méthode** : audit cURL + Python parsing sur ~16 URLs distinctes du preview + monitor full run.

---

## TL;DR

| Check | État |
|---|---|
| 1. Lead-magnet × 3 : status 200 + canonical + 4 hreflang + noindex préservé | ✅ OK |
| 2. LP × 9 : status 200 (status-only spot-check, méta déjà validés pré-sprint) | ✅ OK |
| 3. Sitemap stabilité (924 URLs, inchangé) | ✅ OK |
| 4. Sprint 1+2+D1 non-régressé (skip-link + theme-color sur /en/, /fr/wiggmatch, /en/wiggmatch, /es/wiggmatch) | ✅ OK |
| 5. Monitor `monitor_post_merge.py` complet sur preview | ✅ OK (exit 0) |

**Bilan : 5/5 checks OK.** Aucun blocker. Le merge sur main est techniquement safe.

---

## CHECK 1 — Lead-magnet × 3 (X.1 livré)

| URL | Status | Canonical | Hreflang | x-default | noindex | OK |
|---|---|---|---|---|---|---|
| `/lead-magnet/visas-2026-en.html` | 200 | self ✓ | en, fr, es, x-default ✓ | → `/en/` ✓ | ✓ | ✅ |
| `/lead-magnet/visas-2026-fr.html` | 200 | self ✓ | en, fr, es, x-default ✓ | → `/en/` ✓ | ✓ | ✅ |
| `/lead-magnet/visas-2026-es.html` | 200 | self ✓ | en, fr, es, x-default ✓ | → `/en/` ✓ | ✓ | ✅ |

`<meta robots="noindex,nofollow">` préservé sur les 3 (gating opt-in inchangé). Le canonical + hreflang ajoutés respectent D4 (EN-source).

---

## CHECK 2 — LP × 9 (status-only, post-deploy)

| Slug | EN | FR | ES |
|---|---|---|---|
| `vivre-bali-budget` | 200 ✓ | 200 ✓ | 200 ✓ |
| `visa-mm2h-malaisie` | 200 ✓ | 200 ✓ | 200 ✓ |
| `erasmus-prague-budget` | 200 ✓ | 200 ✓ | 200 ✓ |

Les 9 LP étaient déjà conformes pré-sprint (canonical, hreflang, traductions natives — vérifié dans SPRINT_X_PLAN.md §1.1). Aucun changement, juste confirmation status 200.

---

## CHECK 3 — Sitemap stabilité

```
GET /sitemap.xml → 200 OK
URL count: 924 (attendu 924, inchangé) ✓
```

Sprint X ne touche pas la sitemap (les 12 URLs LP+lead-magnet étaient déjà incluses pré-sprint via `gen_sitemap.py`, et l'ajout de `<link rel=canonical>` dans le HTML n'affecte pas le sitemap qui utilise sa propre logique de hreflang).

---

## CHECK 4 — Sprint 1+2+D1 non-régressé

Spot-check sur 4 URLs représentatives :

| URL | skip-link `wm-skip` | theme-color `#1a5430` | OK |
|---|---|---|---|
| `/en/` | ✓ | ✓ | ✅ |
| `/fr/wiggmatch.html` | ✓ | ✓ | ✅ |
| `/en/wiggmatch.html` | ✓ | ✓ | ✅ |
| `/es/wiggmatch.html` | ✓ | ✓ | ✅ |

---

## CHECK 5 — Monitor `monitor_post_merge.py` complet sur preview

```
python3 scripts/monitor_post_merge.py --quiet --base https://deploy-preview-3--phenomenal-zabaione-d26a6d.netlify.app
→ Exit code: 0
→ All 85+ URLs return 200/301 as expected (12 new LP/lead-magnet URLs covered)
```

Le script a été étendu en X.3 pour couvrir les 9 LP + 3 lead-magnet, plus le check "redirect target → 200" déjà ajouté en Sprint D1.

---

## Recommandation

Sprint X (mini scope c) terminé techniquement. **Le merge sur main peut être autorisé** après ta validation manuelle minimale :
- Spot-check visuel d'une LP par langue (rendu, pas de régression)
- `curl -s https://deploy-preview-3--phenomenal-zabaione-d26a6d.netlify.app/lead-magnet/visas-2026-en.html | grep -E 'canonical|hreflang'` → 5 link tags propres

Post-merge sur main, lancer en local :
```bash
git pull origin main
python3 scripts/monitor_post_merge.py --quiet
```
Exit 0 attendu. Les nouvelles URLs LP/lead-magnet seront couvertes par le monitoring continu (T+1h, T+4h, T+24h).

---

*Audit produit le 2026-05-04. Aucun fichier source modifié dans cette phase.*
