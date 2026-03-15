# WiggMap — Architecture des données & Flux techniques

## Système de données pays — 3 pistes JSON

### Piste 1 : `data/countries.json` (+ `countries.fr.json` + `countries.es.json`)
Source de la **table de données** sur les pages pays. Fichier chargé par `country.html` via fetch selon `localStorage("wigg_lang")`. Fallback toujours sur `countries.json`. Keyed par slug :

```json
"portugal": {
  "name": "Portugal",
  "aliases": ["Portugal", "Lisboa", "Lisbonne"],
  "subtitle": "Moyennes indicatives (Lisbonne plus élevé...)",
  "seo": { "title": "...", "description": "..." },
  "hero": { "src": "../assets/hero-portugal.jpg", "alt": "..." },
  "wigg": { "level": "green", "label": "WIGG: GREEN" },
  "fields": {
    "avg_salary":  { "value": "$1400", "hint": "salaire brut moyen..." },
    "rent_studio": { "value": "$570",  "hint": "loyer indicatif..." }
  }
}
```

**Tous les champs `fields` :**
`min_wage`, `avg_salary`, `doctor_salary`, `rent_studio`, `electricity`, `water`, `mobile`, `beer`, `coffee`, `dish`, `gas`, `vat`, `income_tax`, `smallbiz`, `iphone`, `samsung`, `immigration`, `happiness`, `sun`, `health`, `insurance`, `crime`, `pp`, `religion_christian`, `religion_muslim`, `religion_buddhist`, `religion_jewish`, `religion_other`

Chaque champ : `value` (string affichée) + `hint` (tooltip de contexte)

### Piste 2 : `data/details/[slug].json` (+ `details-fr/` + `details-es/`)
Source du **contenu éditorial** des pages pays. **Deux schémas coexistants** :

**Schema A** — pays secondaires (type Thailand) :
```
meta → country, slug, continent
presentation → capital, regions, population, currency, languages
climate → type, seasonal_variation, general_feeling
housing → rental_process, market_tension, notes
work → unemployment_rate, job_market_ease, top_sectors
visa → general_entry, examples, note
health_lifestyle → life_expectancy, healthcare_system, diet
transport → overall_quality, notes
society → relation_with_foreigners, safety_level...
things_to_know → [array de strings]
expat_score → score (/10)
```

**Schema B** — pays prioritaires (type Portugal, UK, France, Australie...) :
```json
{
  "country": "Portugal",
  "expat_score": { "value": 8.0, "max": 10, "label": "⭐ Score Expat : 8,0 / 10" },
  "snapshot": { "capital": "...", "population": "...", "languages": "...", "driving_side": "..." },
  "currency": { "name": "Euro (EUR)", "rate": "1 USD ≈ 0,92 €", "note": "..." },
  "crypto": { "friendly": "Oui/Non", "note": "..." },
  "article": "🧭 **Aperçu**\n...\n[[MAP]]\n🌦️ **Climat**\n...",
  "goDeeper": {
    "national_dish": { "name": "...", "note": "..." },
    "lgbt_acceptance": { "level": "...", "note": "..." },
    "top_sectors": ["...", "..."],
    "things_to_know": {
      "personality": { "name": "...", "era": "...", "story": "..." },
      "cards": [
        { "title": "🇪🇺 Titre card", "text": "..." }
      ]
    }
  }
}
```

Note : `[[MAP]]` dans `article` = placeholder, la carte Leaflet est injectée à cet endroit par le JS de country.html.

**Pays Schema B (prioritaires) :** Portugal, Espagne, France, Allemagne, Italie, Grèce, Royaume-Uni, Australie, Canada, Mexique, Colombie, Panama, Géorgie, Malte, Thaïlande, Singapour, UAE, Japon, États-Unis...

### Piste 3 : Données géo et temporelles
- `data/map/geo-by-slug2.json` → coordonnées géo (globe + cartes Leaflet)
- `data/timezones-by-slug.json` → fuseaux horaires (horloge locale sur les pages pays)

---

## Flux exact de country.html

```
1. URL parsée → slug extrait depuis ?country=slug
2. Selon wigg_lang (localStorage) :
   - fetch data/countries.fr.json (FR) / data/countries.es.json (ES) / data/countries.json (EN)
   - → popule la data table (tous les fields)
3. setSeo(seo, slug) → injecte title, meta description, canonical dynamique
4. renderRelatedChronicles(slug) → section #related-chronicles (masquée si vide)
5. renderComparePairs(slug) → section #compare-section (max 4 paires, masquée si vide)
6. loadDeepContent(slug) :
   - fetch data/details[-fr|-es]/[slug].json
   - renderSnapshotCard() → sidebar #snapshotCard
   - renderPersonaCard() → sidebar #personaCard (depuis goDeeper.things_to_know.personality)
   - renderThingsToKnow() → #deepContent (cards depuis goDeeper.things_to_know.cards)
   - renderArticle() → #deepContent (markdown → HTML, carte Leaflet injectée au milieu)
7. loadCountryMap() → carte Leaflet depuis geo-by-slug.json
8. data/share.js + data/correction-form.js chargés
```

---

## Système de scores WiggMap

### WIGG Level (badge trafic-lumière)
- `green` = conditions favorables (qualité de vie, expat-friendly, abordable ou bon salaire)
- `yellow` = conditions mixtes (positifs et négatifs notables)
- `red` = conditions difficiles (instabilité, coût extrême, visa restrictif)

### Expat Score (/10) — score propriétaire
- Score composite WiggMap — PAS dérivé d'un seul index externe
- 8+ = excellente destination | 6-7.5 = bon avec réserves | <5 = difficile
- Exemples : Portugal = 8.0 | Thaïlande = 8.5 | Estonie = 7.5 | Royaume-Uni = 7.5

### Immigration Score (/10)
- 8-10 = très facile (UE, programmes nomades actifs)
- 5-7 = modéré (permis requis, friction administrative)
- 1-4 = difficile (restrictif, fermé)

### Crime Index (/100)
⚠️ INVERSE — plus bas = plus sûr. C'est un index de criminalité, pas de sécurité.
- Portugal = ~30 (sûr) | Thaïlande = ~42 (modéré)

### Purchasing Power Index
- Relatif (UE ou mondial). Plus haut = plus de pouvoir d'achat.
- Estonie = 82 | Portugal = 70 | Thaïlande = 60

---

## Chronicles dans country.html

Deux objets hardcodés dans le JS de country.html :

**`CHRONICLES._index`** : 8 groupes historiques avec titres EN/FR/ES et URLs
**`CHRONICLES.countries`** : mapping slug pays → array d'IDs de groupes (67 pays couverts)

⚠️ La série Visa 2026 n'est PAS encore dans `CHRONICLES.countries` — à ajouter.

**`COMPARE_PAIRS`** : mapping slug pays → array de paires compare statiques (max 4 affichées)

---

## Chronicles existantes — 11 groupes × 3 langues = 33 fichiers

| Groupe | EN | FR | ES |
|--------|----|----|-----|
| Projections 2056 | chronicle-2056-best-countries-30-years-en.html | chronicle-2056-ou-vivra-t-on-le-mieux-fr.html | chronicle-2056-mejores-paises-30-anos-es.html |
| Digital Nomads (ancien) | digital-nomads-2026-en.html | digital-nomads-2026-fr.html | digital-nomads-2026-es.html |
| Expatriés & Crypto | expats-nomads-crypto-2026-en.html | expatries-nomades-crypto-2026-fr.html | expatriados-nomadas-crypto-2026-es.html |
| Amériques Partie 1 | chronicle-ameriques-partie1-en.html | chronicle-ameriques-partie1-fr.html | chronicle-ameriques-partie1-es.html |
| Amériques Partie 2 | chronicle-ameriques-partie2-en.html | chronicle-ameriques-partie2-fr.html | chronicle-ameriques-partie2-es.html |
| Amériques Partie 3 | chronicle-ameriques-partie3-en.html | chronicle-ameriques-partie3-fr.html | chronicle-ameriques-partie3-es.html |
| Élever des enfants | chronicle-raise-children-2026-en.html | chronicle-elever-enfants-2026-fr.html | chronicle-criar-hijos-2026-es.html |
| Australie Expat | chronicle-australia-expat-guide-2026-en.html | chronicle-australie-expatriation-2026-fr.html | chronicle-australia-guia-expatriados-2026-es.html |
| Visas Retraite | chronicle-retirement-visas-2026-en.html | chronicle-visas-retraite-2026-fr.html | chronicle-visas-jubilacion-2026-es.html |
| Visas Digital Nomad | chronicle-digital-nomad-visas-2026-en.html | chronicle-visas-digital-nomads-2026-fr.html | chronicle-visas-nomadas-digitales-2026-es.html |
| Visas Expatriation | chronicle-expat-work-visas-2026-en.html | chronicle-visas-expatriation-durable-2026-fr.html | chronicle-visas-expatriacion-2026-es.html |

**CHRONICLE_LANGS dans header.js : ✅ complet** — tous les 11 groupes mappés.

---

## 36 pages compare statiques existantes

Portugal cluster : portugal-vs-spain, portugal-vs-greece, portugal-vs-italy, portugal-vs-germany, portugal-vs-thailand, portugal-vs-vietnam, portugal-vs-panama, georgia-vs-portugal, malta-vs-portugal

Thaïlande cluster : germany-vs-thailand, france-vs-thailand, spain-vs-thailand, thailand-vs-vietnam, thailand-vs-indonesia, thailand-vs-malaysia, thailand-vs-philippines, thailand-vs-panama

Asie du Sud-Est : vietnam-vs-indonesia, vietnam-vs-philippines

Europe : france-vs-germany, spain-vs-france, spain-vs-italy, germany-vs-netherlands, switzerland-vs-germany, switzerland-vs-netherlands

Amérique Latine : mexico-vs-colombia, mexico-vs-costa-rica, panama-vs-colombia, panama-vs-mexico, brazil-vs-colombia, colombia-vs-peru

Hubs premium : united-arab-emirates-vs-singapore, singapore-vs-australia, australia-vs-canada, australia-vs-new-zealand

---

## Système multilingue — 3 stratégies coexistantes

1. **Fichiers séparés** (chronicles) : `-fr.html`, `-en.html`, `-es.html` — chacun autonome
2. **DOM swap inline** (compare statiques) : `data-i18n="key"` + blocs `<div id="ctx-fr">` / `<div id="ctx-es">` cachés, swappés par JS au chargement
3. **header.js global** : `localStorage.getItem("wigg_lang")` → `"en"` | `"fr"` | `"es"` (défaut `"en"`) + CHRONICLE_LANGS pour redirection au changement de langue sur un article
