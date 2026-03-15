# WiggMap — Philosophie éditoriale & Voix "Wigg"

## Ce qu'est WiggMap

Un hybride entre plateforme de comparaison + média de découverte + outil d'aide à la décision + univers ludique + futur espace communautaire. Pas un simple blog. Pas un outil purement technique.

**Question centrale :** *"Where is the grass greener?"*

**Cible :** personnes curieuses du monde, envisageant un changement de vie, digital nomads, expatriés, familles, retraités à l'étranger, crypto holders — mais aussi n'importe qui qui aime comprendre comment le monde fonctionne ailleurs.

**Auteur de tous les articles :** "Wigg" / "By Wigg"

---

## La voix "Wigg" — règle non-négociable

Tout contenu WiggMap doit sonner comme écrit par un être humain intelligent, curieux, bien informé et bien voyagé. **Jamais par une IA.**

### Ton attendu
- Humain, fluide, vivant, attractif
- Informatif sans être froid
- Data-riche mais accessible
- Smart sans être académique
- Crédible sans être rébarbatif

### Ce qui fonctionne
- Ouvrir sur une histoire humaine concrète, un paradoxe ou une scène avant d'aller aux données
- Donner du contexte aux chiffres : *"$500/mois vs $1 400/mois — un écart de 2,8× qui reflète deux niveaux économiques fondamentalement différents"*
- Expliquer ce que les chiffres signifient dans la vie quotidienne, pas juste les lister
- Pull quotes qui capturent une tension ou un paradoxe — pas un fait répété
- Détails spécifiques et recherchés qui montrent que c'est vraiment travaillé
- Toujours pros ET cons — jamais de pure promotion

### Exemple bon opener
*"Work no longer has borders. But it now has a framework — thresholds, visas, and a tax code that can turn a 'great deal' into an administrative dead end."*

### Exemple mauvais opener
*"Dans cet article, nous allons comparer le coût de la vie dans plusieurs pays."*  
*"In this article we will cover..."*

### Ce qu'il ne faut jamais faire
- Commencer par "Dans cet article nous allons..." ou "In this article we will..."
- Phrases creuses ou génériques
- Répéter les mêmes formules d'un article à l'autre
- Ton robotique, scolaire, froid
- Listes à puces de faits génériques sans contexte
- Simplifier une nuance juridique pour fluidifier

---

## Règles sur les données

- **Jamais copier Numbeo** — chiffres propres WiggMap construits depuis plusieurs sources
- Les données indicatives sont assumées et honnêtes : un loyer en Russie varie énormément, on le dit
- Utiliser `~` pour les approximations + contexte dans le `hint`
- Quand une donnée vient d'une source qui doit être citée → source en fin d'article, discrète, petit format, uniquement les obligatoires
- **Pas de pages surchargées de références** — citer seulement ce qu'on est obligé de citer

---

## Structure d'une chronicle (pattern complet)

1. **Kicker** — ex : "Chronicle · Insight & Analysis"
2. **Titre H1** — keyword en tête, année spécifique ("2026") pour signal de fraîcheur SEO
3. **Deck** — hook en 1-2 phrases, tension ou promesse
4. **Séparateur** ornemental
5. **Lead paragraph long** — scène, atmosphère, ancrage humain. Pas de données encore.
6. **Paragraphe contexte** — pourquoi ce sujet maintenant, quelle question on résout
7. **Pull quote** — tension ou paradoxe clé de l'article
8. **Premier tableau ou dbox** — première salve de données
9. **Sections H2 par pays ou par thème** — chacune avec dbox + analyse nuancée (pros + cons)
10. **Séparateurs** `· · ✦ · ·` entre sections longues
11. **Section FAQ** — `<details>` accordéons, 4-6 questions à intent de recherche réel
12. **Liens internes** — pages pays + chronicles liées
13. **Sources** — uniquement les obligatoires, format discret en fin d'article

### Lead paragraphs : règle absolue
Jamais de données dans le lead. C'est de la scène, du contexte humain, de l'atmosphère. Les données arrivent dans le deuxième ou troisième paragraphe.

---

## Deux styles visuels de chronicles

### Style A — Prospectif / Narratif
*(2056, Élever des enfants, Amériques)*

Palette : fond crème `#f7f5f0`, accent ambré `#92400e`, hero dark brown `#1c1710→#2d2218`

Composants spécifiques :
- `p.lead` avec drop cap (première lettre Fraunces 72px)
- `.toc` plan ancré 2 colonnes
- `.scenario` dark navy box — histoires projetées dans le futur
- `.quote` bordure gauche + fond crème, italique
- `.insight` / `.alert` encadrés colorés
- `.dbox` + `.dbox-grid` grilles de données
- `.tag.green` / `.tag.amber` / `.tag.red`
- `.orn` — `· · ✦ · ·` séparateur entre H2

### Style B — Visa / Guide pratique
*(Série Visa 2026)*

Palette : fond blanc `#ffffff`, vert `#22c55e`, hero navy `#0a1628→#243b55`

Composants spécifiques :
- `.visa-section` avec `.visa-num` (cercle vert numéroté)
- `.visa-pills` : `.pill.green` (revenus seuil) / `.pill.blue` (durée) / `.pill.amber` (fiscalité) / `.pill.red` (restriction)
- `.callout` / `.callout-warn` / `.callout-info`
- `.conclusion` profilée par niveau de revenus
- `.internal-links` + `.link-grid`

Structure par entrée pays (3 paragraphes) :
- §1 : conditions exactes (seuil, durée, éligibilité, procédure)
- §2 : nuances, pièges fréquents, ce que les gens comprennent mal
- §3 : cadre de vie réel, pour quel profil exact, verdict pratique

---

## Polices selon type de page

| Section | Police |
|---------|--------|
| Homepage | Poppins |
| Pages data / compare | Inter |
| Chronicles — titres display | Fraunces |
| Chronicles — corps de texte | Source Serif 4 |

---

## Règles de traduction FR → EN / ES

- Fidélité totale au master FR : même nombre de §, mêmes sections, mêmes callouts, mêmes chiffres
- Noms de programmes jamais traduits : D8, DE Rantau, LTR Visa, Welcome Stamp, Beckham, NHR/IFICI, DTV, VITEM...
- L'EN doit sonner comme un anglophone natif — pas du FR traduit mot à mot
- L'ES doit sonner comme un hispanophone natif — audience latino-américaine + ibérique
- FR : légèrement plus formel que EN, mais chaud — jamais bureaucratique

### Terminologie canonique

| FR | EN | ES |
|----|----|----|
| titre de séjour | residence permit | permiso de residencia |
| revenus de source étrangère | foreign-source income | ingresos de fuente extranjera |
| résidence fiscale | tax residency | residencia fiscal |
| seuil | threshold | umbral |
| régime Beckham | Beckham regime | régimen Beckham |
| plafond | ceiling / cap | límite / techo |
| ressortissant | national | nacional |
| voie directe | direct pathway | vía directa |
| permis de séjour | residence permit | permiso de residencia |

### Règles contenu visa (Style B)
- Callouts obligatoires pour pays politiquement sensibles (Géorgie, Équateur, Argentine, Turquie, Thaïlande...)
- Ne jamais affirmer "non renouvelable" sans préciser le cadre exact
- Sur toute affirmation fiscale : "mérite vérification selon la nationalité"
- Formulations temporelles : "en vigueur début 2026", "sous conditions"

---

## Terminologie WiggMap

- **WIGG** : système de notation maison (GREEN / YELLOW / RED)
- **Chronicle** : terme WiggMap pour les articles longs formats
- **Wigg** : persona/auteur éditorial de tous les articles
- **dbox** : composant visuel dark-header avec grille de stats clés
- **goDeeper** : section JSON Schema B avec cartes culturelles/pratiques enrichies
- **Snapshot card** : carte sidebar avec capital, population, langues, côté de conduite
- **Persona card** : carte sidebar "pour quel profil ce pays est-il fait ?"
