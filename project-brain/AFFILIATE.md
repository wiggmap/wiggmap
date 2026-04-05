# AFFILIATE.md — WiggMap Affiliate Brain
> Fichier de référence pour Claude Code. Toute intervention sur les affiliés doit partir d'ici.
> Ne jamais inventer de noms de fichiers. Toujours découvrir via ls/grep avant d'agir.

---

## 1. LIENS DE TRACKING — SOURCE OF TRUTH

| Partenaire | Lien de tracking | Statut |
|-----------|-----------------|--------|
| **Wise** | `https://wise.prf.hn/click/camref:1100l5IbJr` | ✅ Actif |
| **SafetyWing** | `https://safetywing.com/?referenceID=26499930&utm_source=26499930&utm_medium=Ambassador` | ✅ Actif |
| **NordVPN** | `https://go.nordvpn.net/aff_c?offer_id=15&aff_id=144301&url_id=902` | ✅ Actif |
| **Airalo** | `https://airalo.pxf.io/3kkEDk` | ✅ Actif |

Partenaires en attente (Foyer Global Health, iVisa, Genki, HousingAnywhere, Uniplaces) :
ne pas créer de liens placeholder. Mettre à jour cette section dès que les liens sont disponibles.

---

## 2. RÈGLES ÉDITORIALES — NON NÉGOCIABLES

1. **Famille de solution d'abord, marque ensuite.**
   - ✅ "un compte multi-devises... Wise est la référence pour..."
   - ❌ "Wise est la référence pour..." (marque en premier)

2. **Jamais de bouton CTA dans une chronicle éditoriale.** Les blocs `aff-inline` sont autorisés. Les gros boutons sont réservés aux landings conversion.

3. **Un lien par marque par page — sauf exception résumé/test final.** Si la page contient un résumé ou test final distinct du corps, un second lien est acceptable à condition que le texte d'ancre et la phrase soient différents des occurrences dans le corps.

4. **`rel="noopener sponsored"`** obligatoire sur tous les liens affiliés.

5. **Note de transparence obligatoire** dans chaque bloc : `<span class="aff-note">Lien affilié.</span>`

6. **Wise ≠ gratuit.** Wise a des frais, inférieurs aux banques classiques. Ne jamais écrire "sans frais".

7. **SafetyWing ≠ assurance expat complète.** Adapté aux nomades et voyageurs longue durée. Pour expats installés → Cigna Global / Foyer Global Health / Allianz Care.

8. **SafetyWing non disponible** pour résidents américains, canadiens, australiens. Ne pas placer sur les pages de ces pays.

---

## 3. MATRICE DE PLACEMENT PAR TYPE DE PAGE

### 3A. CHRONICLES ÉDITORIALES

L'affiliation arrive comme réponse à un problème soulevé dans le texte. Jamais en ouverture de section.

| Contexte dans le texte | Partenaire | Format |
|------------------------|------------|--------|
| Frais bancaires, change, virement international | Wise | `aff-inline` après le § problème |
| Assurance santé, couverture hors pays d'origine | SafetyWing (profils mobiles) | `aff-inline` après le § problème |
| Connexion à l'arrivée, roaming, eSIM | Airalo | `aff-inline` après le § problème |
| Accès services du pays d'origine depuis l'étranger | NordVPN | `aff-inline` après le § problème |
| Visa, démarches administratives | iVisa *(dès lien dispo)* | `aff-inline` |
| Logement à l'étranger, colocation expat | HousingAnywhere *(dès lien dispo)* | `aff-inline` |

**HTML du bloc `aff-inline` standard :**
```html
<div class="aff-inline">
  ✦ <strong>[Accroche contextuelle] :</strong> [Famille de solution avant marque].
  <a href="[LIEN]" target="_blank" rel="noopener sponsored">[Nom marque]</a> — [2-3 mots bénéfice clé].
  <span class="aff-note">Lien affilié.</span>
</div>
```

---

### 3B. PAGES PAYS (`country.html`)

Maximum 2 partenaires par page pays. Priorité :
1. **Wise** — dans le bloc banking/finances
2. **SafetyWing ou Airalo** — dans le bloc santé/connectivité selon pertinence pays

**Cas spéciaux :**
- USA, Canada, Australie → ne pas placer SafetyWing
- Zone Schengen UE → Wise + Airalo prioritaires (SafetyWing moins pertinent)
- Asie du Sud-Est, Amérique Latine, Afrique → SafetyWing + Airalo très pertinents
- Chine → NordVPN prioritaire (Great Firewall)
- Japon, Corée → NordVPN pertinent

Les pages pays sont générées dynamiquement depuis `country.html` + JSON. Les liens affiliés vont dans le template `country.html`, dans les sections banking et santé existantes — ou dans un bloc `<div class="practical-tips">` créé en bas de fiche si ces sections n'existent pas.

**Format pour pages pays :**
```html
<div class="tip-inline">
  <strong>Compte international :</strong> pour recevoir et dépenser en devise locale
  sans frais cachés, <a href="https://wise.prf.hn/click/camref:1100l5IbJr"
  target="_blank" rel="noopener sponsored">Wise</a> est la référence parmi les expatriés.
  <span class="aff-note">Lien affilié.</span>
</div>
```

---

### 3C. CHRONICLES VILLES

| Section | Partenaire |
|---------|-----------|
| Budget / finances locales | Wise |
| Trouver un logement | HousingAnywhere *(dès lien dispo)* |
| SIM / connectivité à l'arrivée | Airalo |
| Santé / couverture médicale | SafetyWing |
| Section "avant de partir" ou checklist finale | Wise + SafetyWing |

Placement : dans la section éditoriale pertinente, jamais en tête de chronicle.

---

### 3D. LANDINGS CONVERSION (chronicles type checklist)

Format CTA autorisé sur ces pages uniquement :
```html
<div class="cta-card">
  <div class="cta-title">💳 Compte multi-devises</div>
  <div class="cta-body">Payez sans frais cachés dans 160+ pays.</div>
  <a href="https://wise.prf.hn/click/camref:1100l5IbJr" class="cta-btn"
     target="_blank" rel="noopener sponsored">Ouvrir un compte Wise →</a>
  <span class="aff-note">Lien affilié.</span>
</div>
```

---

### 3E. CHRONICLES IMMOBILIER — CAS SPÉCIAL

Contenu purement juridique/factuel. Placement uniquement là où c'est naturel :
- Section transferts / financement d'achat → **Wise** (virer les fonds sans marge de change)
- Section "avant de visiter / séjour de découverte" → **SafetyWing**

```html
<div class="aff-inline">
  ✦ <strong>Transferts internationaux :</strong> pour virer les fonds d'achat
  sans marge de change cachée, <a href="https://wise.prf.hn/click/camref:1100l5IbJr"
  target="_blank" rel="noopener sponsored">Wise</a> est l'option la plus utilisée
  par les acheteurs expats — IBAN locaux dans 10+ devises.
  <span class="aff-note">Lien affilié.</span>
</div>
```

---

## 4. ÉTAT ACTUEL DES PLACEMENTS — AVRIL 2026

### 4A. Chronicles thématiques (hors villes)

| Fichier (×3 langues EN/FR/ES) | Wise | SafetyWing | Airalo | NordVPN | Format |
|-------------------------------|:----:|:----------:|:------:|:-------:|--------|
| `digital-nomads-2026` | ✅ | ✅ | ✅ | ✅ | aff-inline |
| `expats-nomads-crypto-2026` | ✅ | ✅ | ✅ | ✅ | aff-inline |
| `chronicle-raise-children-2026` | ✅ | ✅ | — | — | aff-inline |
| `chronicle-healthcare-expats-2026` | ✅ | ✅ | — | — | aff-inline |
| `chronicle-retirement-visas-2026` | ✅ | ✅ | — | — | aff-inline |
| `chronicle-digital-nomad-visas-2026` | ✅ | ✅ | ✅ | — | aff-inline |
| `chronicle-expat-work-visas-2026` | ✅ | ✅ | — | — | aff-inline |
| `chronicle-forgotten-expat-countries-2026` | ✅ | ✅ | — | — | aff-inline |
| `chronicle-australia-expat-guide-2026` | ✅ | — | ✅ | — | aff-inline |
| `chronicle-ireland-expat-guide-2026` | ✅ | ✅ | — | — | aff-inline |
| `chronicle-ameriques-partie1/2/3` | ✅ | — | — | — | aff-inline |
| `chronicle-asia-expat-guide-part1/2-2026` | ✅ | ✅ | ✅ | — | aff-inline |
| `chronicle-africa-expat-p1/2/3/4` | ✅ | ✅ | ✅ | — | aff-inline |
| `chronicle-2056-best-countries-30-years` | — | — | — | — | aucun (prospectif) |
| `chronicle-study-abroad-europe-erasmus-2026` | — | ✅ | — | — | aff-inline |
| `chronicle-study-abroad-americas-africa-2026` | ✅ | — | — | — | aff-inline |
| `chronicle-study-abroad-asia-pacific-2026` | — | ✅ | — | — | aff-inline |
| `chronicle-study-abroad-practical-guide-2026` | ✅ | ✅ | ✅ | — | product-rec (checklist) |
| `chronicle-property-abroad-2026` | ✅ | — | — | — | aff-inline |
| `chronicle-ready-to-leave` | ✅ | ✅ | ✅ | ✅ | aff-inline |

### 4B. Chronicles villes (120 fichiers, 40 villes × 3 langues)

Toutes les chronicles villes contiennent : Wise (budget) + SafetyWing (santé) + Airalo (SIM).
NordVPN présent uniquement sur les villes en zones à censure (Shanghai, Moscow).

### 4C. Pages pays (`country.html`)

Les chronicles sont liées aux pages pays via `CHRONICLES.countries` dans `country.html`.
Mapping actif pour les nouvelles chronicles :
- `study-erasmus` → CZ, PL, ES, HU, EE, SI, CY, LV
- `study-americas-africa` → CA, US, MX, AR, ZA, MA, SN, GH
- `study-asia-pacific` → JP, KR, AU, SG, TW, MY
- `study-practical` → FR, DE, UK
- `property-abroad` → TH, JP, MX, PT, ES, AE, ID, VN, MA, GR, TR, CY, CO, PA, PH
- `ready-to-leave` → (dans _index, pas encore mappé à des pays spécifiques)

---

## 5. PROCÉDURE D'AUDIT — ORDRE D'EXÉCUTION

### Étape 1 — Découverte des fichiers
```bash
# Lister toutes les chronicles
ls chronicles/*.html

# Lister tous les fichiers HTML du projet
find . -name "*.html" -not -path "*/node_modules/*"
```

### Étape 2 — Scan des mentions sans lien affilié
```bash
# Wise cité sans lien affilié
grep -rn "Wise" --include="*.html" | grep -v "wise.prf.hn"

# SafetyWing cité sans lien affilié
grep -rn "SafetyWing" --include="*.html" | grep -v "safetywing.com"

# NordVPN cité sans lien affilié
grep -rn "NordVPN" --include="*.html" | grep -v "nordvpn.net"

# Airalo cité sans lien affilié
grep -rn "Airalo" --include="*.html" | grep -v "airalo.pxf.io"
```

### Étape 3 — Scan des liens déjà présents
```bash
grep -rln "wise.prf.hn" --include="*.html"
grep -rln "safetywing.com" --include="*.html"
grep -rln "airalo.pxf.io" --include="*.html"
grep -rln "nordvpn.net" --include="*.html"
```

### Étape 4 — Générer le rapport avant toute modification
Produire un tableau à partir des résultats réels :

| Fichier | Wise | SafetyWing | Airalo | NordVPN | Action requise |
|---------|------|-----------|--------|---------|----------------|
| (remplir depuis les résultats grep) | | | | | |

### Étape 5 — Traiter les mentions non linkées
Pour chaque mention trouvée à l'étape 2 :
1. Lire le contexte ±5 lignes
2. Exclure : JSON-LD, `<title>`, `<meta>`, commentaires HTML, fichiers `.js`
3. Vérifier la règle "famille de solution d'abord" — réécrire si nécessaire
4. Insérer le lien avec `rel="noopener sponsored"`

### Étape 6 — Placer les affiliés manquants
Pour les fichiers sans aucun lien affilié : appliquer la matrice section 3 selon le type de page.

### Étape 7 — Rapport final
- Fichiers modifiés + détail des changements
- Mentions non linkées intentionnellement ignorées (avec raison)
- Fichiers qui n'avaient pas besoin de modification

---

## 6. ANTI-PATTERNS — CE QUE CLAUDE CODE NE DOIT PAS FAIRE

- ❌ Inventer des noms de fichiers — toujours découvrir via ls/find/grep
- ❌ Linker dans le JSON-LD, les `<title>`, les `<meta>`, les commentaires HTML
- ❌ Modifier `header.js`, `footer.js`, les fichiers `.js` de données
- ❌ Placer 2 liens identiques (même ancre, même contexte) vers la même marque
- ❌ Écrire "Wise est gratuit" — Wise a des frais, juste inférieurs aux banques classiques
- ❌ Recommander SafetyWing pour résidents US / CA / AU
- ❌ Placer une marque en premier sans avoir introduit la famille de solution
- ❌ Toucher aux hreflang ou canonicals lors de l'injection

---

## 7. PARTENAIRES EN ATTENTE

Mettre à jour la section 1 dès que ces liens sont disponibles, puis relancer l'audit :

| Partenaire | Placement prioritaire |
|-----------|----------------------|
| **iVisa** | Pages pays (section visa), chronicles sur l'immigration |
| **Foyer Global Health** | Chronicles santé, pages pays section assurance longue durée |
| **Genki** | Mêmes placements que SafetyWing — citer les deux comme alternatives |
| **HousingAnywhere** | Chronicles villes (section logement), pages pays populaires |
| **Uniplaces** | Chronicles villes (logement étudiant / jeune expat) |

---

*Dernière mise à jour : avril 2026*
