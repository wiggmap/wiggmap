# SPRINT_Z_PLAN — WiggMap Connect (audit T1 + T2 réaliste)

> **Date** : 2026-05-04
> **Mode** : audit + plan. Aucun fichier modifié dans cette phase.
> **Source de vérité** : `project-brain/wiggmap-connect-vision.md`

---

## ⚠️ Découverte critique qui réoriente le sprint

Le brief original disait : **"Sprint Z — WiggMap Connect T2 (feed + post-create + groups)"**. Mais l'audit montre que **T1 n'est PAS finalisé** :

| T1 deliverable | État réel | Observation |
|---|---|---|
| Landing `/connect/index.html` | ✅ 588 lignes | Mockup HTML/CSS complet |
| Onboarding `/connect/onboarding.html` | ⚠️ 1538 lignes | **0 référence Supabase** → mockup non-branché |
| Profile `/connect/profile.html` | ⚠️ 966 lignes | **0 référence Supabase** → mockup non-branché |
| Setup Supabase Auth | ❌ **non livré sur connect/** | Auth fonctionne sur `mon-compte.html` legacy + `connect/widget.js` (chronicles), pas sur les pages T1 connect |
| Tables Supabase profiles/posts/helped/etc | ❌ **non créées** (à confirmer Supabase dashboard) | La vision spec les requiert pour MVP T1 mais aucune migration SQL trouvée dans le repo |
| `connect/assets/connect.css` design system | ✅ 47 KB | Présent et complet |
| `connect/assets/connect.js` logique | ✅ 14 KB | Mais essentiellement i18n + UI helpers, pas de plumbing data |

**Conclusion** : T1 = **front-end UI complet**, T2 ne peut pas démarrer sans d'abord brancher T1 sur Supabase (auth + tables + reads/writes). Le brief "Sprint Z T2" est donc effectivement **T1-finalisation + T2** en un seul "sprint", ce qui n'est pas réalisable en 1 PR.

---

## 1. Inventaire détaillé du dossier `/connect/`

### 1.1 Pages HTML

```
connect/index.html         588 lignes   Landing — choix Connect / non
connect/onboarding.html   1538 lignes   Création profil (8 étapes UI, mockup statique)
connect/profile.html       966 lignes   Carte de vie utilisateur (mockup, pas d'auth)
connect/feed.html          471 lignes   Feed 4 types (témoignage/flash/journal/question), tabs Monde/Découvrir/Pays
connect/group.html         630 lignes   Groupe pays (vue par country_slug)
connect/swipe.html         399 lignes   WiggSwipe Tinder-like avec score miroir (T3 cible)
```

### 1.2 Assets

```
connect/assets/connect.css         47 KB  Design system Connect (palette night/card/green)
connect/assets/connect.js          14 KB  Logique UI (tabs, modals, helpers)
connect/assets/i18n.js             33 KB  Translations FR/EN/ES
connect/assets/wiggmap-connect-logo.png  154 KB  Logo
connect/widget.js                  26 KB  Widget chargé sur chronicles (Supabase wired ✓ — single page that works end-to-end)
connect/widget.css                  6 KB
```

### 1.3 Plumbing Supabase actuel

| Page | Ref Supabase |
|---|---|
| `connect/widget.js` | ✅ **complet** (clés + client + RLS-aware queries) |
| `connect/feed.html` | ⚠️ 5 références (bootstrap auth check seulement) |
| `connect/swipe.html` | ⚠️ 11 références (prototype WiggSwipe partiellement codé) |
| `connect/index.html` / `onboarding.html` / `profile.html` / `group.html` | ❌ 0 référence |

### 1.4 Auth Supabase déjà wired ailleurs

- `mon-compte.html` racine (3 réfs) — flow complet
- `connect/widget.js` — flow complet (chronicles comments)
- Clés publiques : `https://tkctreoftezvbfejhbto.supabase.co` + `sb_publishable_lAKWBnp2nbfgb2w5Uj55aQ_aD6fBWUb`

---

## 2. Vrais lots à exécuter (T1-finalisation + T2 réaliste)

Vu le volume et le risque (data prod), je propose **5 sous-sprints Z.0 → Z.4**, chacun mergeable indépendamment :

### **Z.0 — Setup Supabase + DB schema** (PRÉ-REQUIS)

| Action | Effort |
|---|---|
| Créer fichier `data/connect-config.js` (clés Supabase + constantes) | 30 min |
| Écrire migrations SQL : tables `profiles`, `posts`, `helped`, `conversations`, `messages` (per vision §171) | 2h |
| Définir RLS policies par table (qui peut lire/écrire quoi) | 2h |
| Setup Supabase Storage bucket pour avatars + media posts | 1h |
| **À FAIRE PAR FLO côté Supabase dashboard** : appliquer les migrations + activer RLS | (côté user) |
| Documenter dans `project-brain/connect-supabase-schema.md` | 30 min |

**Risque** : ⚠️ touche la prod Supabase. **Test obligatoire** sur projet Supabase staging avant prod.

**Effort total** : ~6h dev + intervention Flo dashboard.

### **Z.1 — Branchement auth + onboarding + profile** (T1-finalisation)

| Action | Effort |
|---|---|
| Brancher `connect/onboarding.html` sur Supabase Auth (Google OAuth + email/password) | 3h |
| Persister le profil dans table `profiles` à la fin de l'onboarding | 2h |
| Brancher `connect/profile.html` en lecture (own profile + autre profil par username) | 2h |
| Brancher `connect/index.html` landing : si déjà auth → redirige vers `/connect/feed.html`, sinon → `/connect/onboarding.html` | 1h |
| Tests : créer compte, créer profil, voir profil, déconnexion, reconnexion | 1h |

**Effort total** : ~9h dev + tests Flo.

### **Z.2 — Feed read** (T2 part 1 — coeur de Connect)

| Action | Effort |
|---|---|
| Brancher `connect/feed.html` tab "Mon Monde" : SELECT posts WHERE country_slug IN profile.country_targets | 3h |
| Tab "Découvrir" : SELECT posts ORDER BY helped_count DESC + recency | 2h |
| Tab "Pays" : SELECT posts WHERE country_slug = X (paramètre URL ou modal de sélection) | 2h |
| Affichage des 4 types de posts (Témoignage/Flash/Journal/Question/Commerce) avec badges | 1h |
| Bouton "✦ Aidé" : INSERT INTO helped (avec UPSERT idempotent + UI toggle) | 2h |
| Counter helped_count en realtime (Supabase subscription) | 1h |

**Effort total** : ~11h dev.

### **Z.3 — Post-create** (T2 part 2)

| Action | Effort |
|---|---|
| Créer modal `post-create` (probablement dans feed.html, déclenché par bouton flottant FAB) | 4h |
| 5 sélections : type, country_slug, city, title (optional), content, media (optional 1-3 images via Supabase Storage) | 3h |
| Spécial Journal : sélection `journal_series_id` existante ou créer nouvelle série | 2h |
| INSERT INTO posts + upload images vers Storage | 1h |
| Refresh feed après création réussie | 1h |
| Validation client (max 280 char content pour flash, etc.) + server (RLS + table constraints) | 1h |

**Effort total** : ~12h dev.

### **Z.4 — Groups** (T2 part 3)

| Action | Effort |
|---|---|
| Brancher `connect/group.html` sur Supabase : SELECT posts WHERE country_slug = X | 3h |
| Liste membres du groupe (profiles WHERE X IN country_targets OR country_origin=X OR country_current=X) | 2h |
| Header du groupe : nom du pays (slug WiggMap), drapeau, stats live (X membres, Y posts) | 2h |
| Lien depuis profile.html "voir tous les posts pays X" → group.html?country=X | 1h |
| Bouton "rejoindre groupe" — semantic : ajouter X à profile.country_targets | 2h |

**Effort total** : ~10h dev.

### **Récap effort estimé Sprint Z complet**

| Sous-sprint | Effort dev | PR cible |
|---|---|---|
| Z.0 setup DB | ~6h | sprint-Z0-supabase-setup |
| Z.1 auth + T1 | ~9h | sprint-Z1-auth-profiles |
| Z.2 feed read | ~11h | sprint-Z2-feed-read |
| Z.3 post-create | ~12h | sprint-Z3-post-create |
| Z.4 groups | ~10h | sprint-Z4-groups |
| **Total** | **~48h** = 1.5-2 semaines réelles | 5 PRs |

---

## 3. Risques majeurs

### R1 — Touche la prod Supabase

C'est le **premier sprint qui touche au backend live**. Si une migration SQL casse une table existante → leads / formulaires Netlify Forms / wiggmatch quiz unlock cassés.

**Mitigation** : tester en local sur projet Supabase de staging (créer projet jumeau), valider les migrations + RLS avant prod, faire un dump complet avant migration prod.

### R2 — Auth flow complexe

OAuth Google + magic link + email/password + session persistence + RLS = beaucoup de surface. La moindre erreur RLS = soit des données inaccessibles (tout le monde voit rien) soit des données over-exposées (n'importe qui voit tout).

**Mitigation** : test exhaustif des permissions sur 3 personas (anon, authed, owner-of-resource).

### R3 — Volume (~50h dev)

Trop gros pour 1 sprint. Découpage en 5 sous-sprints obligatoire.

**Mitigation** : valider Z.0 (DB schema) avant tout — c'est la fondation, tout le reste en dépend.

### R4 — Realtime Supabase = nouvelle dépendance

`subscribe()` aux changements live (helped_count, nouveaux posts) = WebSocket Supabase. Coût = 1 connexion par utilisateur online. Plan free : 200 connexions concurrent. À monitorer.

**Mitigation** : commencer sans realtime (Z.2 polling toutes les 30s) puis ajouter realtime en optimisation Z.5.

### R5 — Storage costs

Upload images posts = bucket Supabase Storage. Free tier : 1 GB. Si Connect prend du trafic → quota dépassé en 2 mois.

**Mitigation** : compresser côté client (max 1200px, JPG 80%, ~150 KB/image) + monitoring usage.

### R6 — Modération

Posts utilisateurs = risque contenu inapproprié. Pas de spam filter, pas de modération prévue dans la vision.

**Mitigation** : reporter à Sprint Z' (post-MVP), assumer le risque pour l'instant.

---

## 4. Décisions à arbitrer avant Z.0

### D1 — Tu valides l'analyse "T1 non finalisé" ?

- **(a)** Oui, T1 = mockup HTML, à brancher sur Supabase dans Z.0+Z.1
- **(b)** Non, je me suis trompé : Supabase auth/profil DÉJÀ branché ailleurs que je n'ai pas trouvé → me dire où

### D2 — Stratégie Supabase

- **(a)** Réutiliser le projet Supabase existant (`tkctreoftezvbfejhbto`) qui héberge déjà chronicles widget + mon-compte
- **(b)** Créer un projet Supabase staging séparé pour Connect, switch vers prod après validation
- **(c)** Créer un projet Supabase dédié `wiggmap-connect`

**Recommandation : (a)** mais avec migrations SQL **idempotentes + reversible** (DROP IF EXISTS + transactional). Garder un projet unique simplifie l'auth (un seul SSO Google, une seule URL).

### D3 — Ordre d'exécution Z.0 → Z.4

- **(a)** Strictement séquentiel (recommandé) : Z.0 → validation → Z.1 → ... → Z.4
- **(b)** Z.0 + Z.1 en parallèle (auth + DB peuvent avancer ensemble si Flo applique les migrations en parallèle)

**Recommandation : (a)**. Réduit la surface de risque.

### D4 — Scope T2 du brief original

Le brief disait "T2 = feed + post-create + groups". Confirmes-tu ?

- **(a)** Oui, scope = Z.2 + Z.3 + Z.4 (mais Z.0 + Z.1 obligatoires d'abord)
- **(b)** Réduire scope au minimum : juste Z.2 (feed read) pour démarrer le test utilisateur, le reste plus tard
- **(c)** Élargir : ajouter messagerie / WiggSwipe T3 pour avoir un MVP complet

**Recommandation : (a)** mais avec validation de Z.0 par Flo avant de continuer.

### D5 — Test utilisateur entre les lots

Vu le volume, tu peux vouloir un mini-test après chaque sous-sprint :
- **(a)** Tu testes après chaque PR mergée (5 cycles de feedback)
- **(b)** Tu testes seulement à la fin (Z.4 mergé)

**Recommandation : (a)**. Vu que Connect est nouveau et inconnu côté UX, le feedback rapide évite des surprises tardives.

### D6 — Données de test

Pour tester Connect, il faut des comptes + des profils + des posts.
- **(a)** Tu crées 3-5 comptes test toi-même via Google OAuth
- **(b)** Je crée un script `seed_test_data.py` qui génère 50 comptes + posts factices via Supabase API (intéressant pour test load + UX)
- **(c)** Pas de seed data, on attend des vrais utilisateurs

**Recommandation : (b)** pour Z.2/Z.3 (feed/post-create vide = aucun feedback UI possible).

### D7 — Création projet Supabase staging

Si D2 = (b), il faut créer un projet Supabase dédié.
- **(a)** Tu le crées toi-même (gratuit, 2 minutes)
- **(b)** Skipper staging, aller direct prod (D2 = (a))

**Recommandation : (b)** (cohérent avec D2 (a)).

---

## 5. Ce qui n'est PAS dans Sprint Z

- **WiggSwipe** (T3 — sprint dédié futur)
- **Messagerie** (T3 — sprint dédié futur)
- **Validation terrain / pros vérifiés** (T4)
- **Linkage depuis le site principal** (volontaire per vision : "Pas de lien depuis le site principal pour l'instant")

---

## 6. Décisions à valider

Réponds avec D1-D7 :

```
D1 (T1 non finalisé): a | b
D2 (Supabase strategy): a | b | c     — recommandé: a
D3 (ordre Z.0→Z.4): a | b             — recommandé: a
D4 (scope T2): a | b | c              — recommandé: a
D5 (tests entre lots): a | b          — recommandé: a
D6 (seed test data): a | b | c        — recommandé: b
D7 (projet Supabase staging): a | b   — recommandé: b
```

Avec tes 7 réponses, je démarre **Z.0** (création des migrations SQL + `data/connect-config.js`). Je m'arrêterai après Z.0 livré pour que tu valides côté Supabase dashboard avant Z.1.

---

*Plan rédigé le 2026-05-04. Aucun fichier source modifié. En attente arbitrage D1-D7.*
