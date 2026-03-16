# WiggMap Connect — Vision & Specs pour Claude Code

## Ce que c'est

WiggMap Connect est un réseau social d'un nouveau genre intégré à WiggMap.
L'unité centrale n'est pas la personne — c'est le lieu.
Un réseau où les gens se parlent vraiment, s'entraident, échangent leur vécu.

**URL de production cible :** https://wiggmap.com/connect/
**Statut :** En développement — aucun lien depuis le site principal pour l'instant
**Stack :** HTML/CSS/JS vanilla + Supabase backend (même philosophie que WiggMap)

---

## Concept fondateur

**L'échange bilatéral — le miroir**
Un Français qui veut partir au Brésil + un Brésilien qui veut partir en France
= deux personnes en miroir parfait. Chacun a exactement ce que l'autre cherche.
Ce n'est pas un réseau social classique. C'est un réseau d'échange de vie.

**Ce que les gens font ici :**
- Trouver quelqu'un qui vit dans leur pays cible (expat ou local)
- Poser des vraies questions : logement, fiscalité, scolarité des enfants, démarches
- Partager leur vécu, leurs photos, leurs ressentis, leurs articles
- Présenter leur commerce ou association locale
- Trouver leur miroir et échanger directement (WiggSwipe)

---

## Design System — règles absolues

### Palette
```css
--wigg-night:     #0a0f1e;  /* Fond principal */
--wigg-card:      #0d1629;  /* Cartes */
--wigg-surface:   #141f33;  /* Surfaces secondaires */
--wigg-border:    #1e2a3a;  /* Bordures */
--wigg-green:     #22c55e;  /* Action principale, vie, "aidé" */
--wigg-green-dk:  #16a34a;  /* Hover vert */
--wigg-green-bg:  #0d2818;  /* Fond vert subtle */
--wigg-blue:      #378add;  /* Info, journaux */
--wigg-amber:     #ef9f27;  /* Flash, alerte */
--wigg-pink:      #d4537e;  /* Questions */
--wigg-text-1:    #e8edf5;  /* Texte principal */
--wigg-text-2:    #8a9ab5;  /* Texte secondaire */
--wigg-text-3:    #6b7fa3;  /* Texte tertiaire */
--wigg-text-4:    #3a4a5e;  /* Texte très discret */
```

### Typographie
- Font : system-ui / Poppins si dispo (déjà sur WiggMap)
- Display 18px / 500 : titres d'écran
- Heading 15px / 500 : noms, titres de post
- Body 12px / 400 : contenu
- Caption 10px / 400 : métadonnées, routes
- Micro 9px / 400 : badges, compteurs

### Composants de base
- Bordures : 0.5px solid var(--wigg-border)
- Border-radius cards : 14px
- Border-radius pills : 20px
- Border-radius boutons : 12px
- Pas de box-shadow — flat design
- Pas de gradients sur les fonds de cartes

### Règles design non-négociables
1. Le lieu AVANT la personne — toujours afficher la route 🇫🇷→🇧🇷 en premier
2. Une seule action positive : "✦ Aidé" — pas de like, pas de dislike
3. Pas de compteur de followers — uniquement "personnes aidées"
4. Chaque post affiche son type visuellement (Témoignage/Flash/Journal/Question)
5. Mobile first absolu

---

## Les 4 types de contenu (badges colorés)

```
Témoignage  → badge vert   #0d2818 / #22c55e
Flash       → badge ambre  #1a1500 / #ef9f27
Journal     → badge bleu   #0a1520 / #378add
Question    → badge rose   #1a0812 / #d4537e
Commerce    → badge gris   #141f33 / #8a9ab5
```

---

## Structure des profils

Chaque profil contient :
```
- Pays d'origine (flag + ville)
- Pays de résidence actuelle (flag + ville)
- Pays cibles (1 à 3)
- Statut de vie (voir liste ci-dessous)
- Secteur professionnel
- Langues parlées (avec niveau 1-5)
- Bio courte (max 200 chars)
- Type : individu / commerce / association
```

### Statuts de vie
```
💭 Curieux          — explore, pas encore décidé
📋 Planificateur    — départ prévu dans X mois
🚀 En transition    — vient de partir/arriver (< 3 mois)
🏠 Installé         — entre 3 mois et 3 ans
🌐 Vétéran          — 3+ ans dans le pays
↩️ Rentré           — a vécu là-bas, est rentré
🗺️ Local            — né ou vivant depuis toujours ici
💼 Pro vérifié      — professionnel vérifié (avocat, agent...)
```

---

## Le WiggSwipe

Mécanique Tinder mais pour l'entraide — pas pour la rencontre romantique.

**Calcul du score miroir :**
```
Pays croisés (origine A = cible B et vice versa) → 50 pts
+ Secteur commun                                 → 20 pts
+ Situation similaire                            → 15 pts
+ Langues communes                               → 15 pts
= Score /100
```

**Interface :**
- Carte unique, une par une
- Deux actions seulement : Passer / Démarrer
- Brise-glace généré automatiquement si "Démarrer"
- Pas de "match" requis — contact direct asymétrique

---

## Structure des fichiers à créer

```
/connect/
├── index.html              ← Landing / onboarding
├── feed.html               ← Fil d'actu principal
├── swipe.html              ← WiggSwipe
├── profile.html            ← Profil (soi ou autre)
├── group.html              ← Groupe pays
├── message.html            ← Messagerie
├── post.html               ← Post individuel
├── onboarding.html         ← Création de profil
└── assets/
    ├── connect.css         ← Design system Connect
    └── connect.js          ← Logique principale

/data/
└── connect-config.js       ← Config Supabase + constantes
```

---

## Stack technique

```
Frontend    → HTML/CSS/JS vanilla (cohérent avec WiggMap)
Auth        → Supabase Auth (email + OAuth Google)
Database    → Supabase PostgreSQL
Realtime    → Supabase Realtime (messagerie)
Storage     → Supabase Storage (photos profil)
Search      → Supabase Full Text Search
Hosting     → Netlify (existant)
```

### Tables Supabase à créer (MVP T1)

```sql
-- Profils utilisateurs
profiles (
  id uuid references auth.users,
  username text unique,
  display_name text,
  country_origin text,        -- slug pays WiggMap
  country_current text,       -- slug pays WiggMap
  country_targets text[],     -- array de slugs
  life_status text,           -- curieux/planificateur/etc
  sector text,
  languages jsonb,            -- [{lang: 'fr', level: 5}]
  bio text,
  member_type text,           -- individu/commerce/association
  created_at timestamptz,
  updated_at timestamptz
)

-- Posts
posts (
  id uuid,
  author_id uuid references profiles,
  post_type text,             -- temoignage/flash/journal/question/commerce
  country_slug text,          -- pays concerné
  city text,
  title text,
  content text,
  media_urls text[],
  helped_count int default 0,
  journal_episode int,        -- null si pas un journal
  journal_series_id uuid,     -- null si pas un journal
  created_at timestamptz
)

-- "Aidé" (remplace les likes)
helped (
  post_id uuid references posts,
  user_id uuid references profiles,
  created_at timestamptz,
  primary key (post_id, user_id)
)

-- Conversations
conversations (
  id uuid,
  participant_a uuid references profiles,
  participant_b uuid references profiles,
  mirror_score int,
  themes jsonb,
  is_public boolean default false,
  created_at timestamptz
)

-- Messages
messages (
  id uuid,
  conversation_id uuid references conversations,
  sender_id uuid references profiles,
  content text,
  created_at timestamptz
)
```

---

## Intégration avec WiggMap existant

- Les slugs pays WiggMap sont réutilisés tels quels (portugal, thailand, etc.)
- header.js et footer.js sont chargés sur toutes les pages /connect/
- La palette verte #22c55e est partagée — cohérence visuelle
- Pas de lien depuis le site principal pour l'instant
- Le service worker sw.js existant couvre /connect/ automatiquement

---

## Règles absolues (héritées de WiggMap)

1. Jamais de framework — vanilla JS uniquement
2. Jamais de npm / build step
3. Toujours charger header.js + footer.js
4. Mobile first sur chaque écran
5. Pas de données inventées — tout vient de Supabase ou de WiggMap
6. Les slugs pays ne changent jamais
7. Toujours tester sur mobile avant de livrer

---

## Roadmap MVP

```
T1 (maintenant) :
  ✦ Design system CSS complet (connect.css)
  ✦ Page onboarding / création de profil
  ✦ Page profil (carte de vie)
  ✦ Setup Supabase Auth
  ✦ Landing page /connect/

T2 :
  ✦ Fil d'actu (feed.html) avec 4 types de posts
  ✦ Création de post
  ✦ Groupes pays

T3 :
  ✦ WiggSwipe (swipe.html)
  ✦ Messagerie (message.html)

T4 :
  ✦ Validation terrain
  ✦ Spécialités émergentes
  ✦ Profils pros vérifiés
```

---

*Ce fichier est la source de vérité pour tout développement sur WiggMap Connect.*
*Ne jamais dévier du design system ou de la stack sans validation de Flo.*
