# WiggMap — Roadmap & État du projet

## Vision et objectif

WiggMap est une plateforme éducative, récréative et attractive sur les pays du monde.
**Phase actuelle :** construire la qualité du contenu et acquérir du trafic organique.
**Objectif final :** monétisation propre une fois le trafic établi (affiliations, partenariats — SafetyWing, Wise, Booking, NordVPN, services de relocation). Pas de monétisation prématurée qui dégraderait l'expérience.

---

## Funnel acquisition / capture (mis en place 11 avril 2026)

```
Cold visitor (Search ou Meta)
   ↓
Landing page dédiée (3 LPs créées × 3 langues = 9 pages)
   ↓
Capture email (formulaire avec event Lead Meta)
   ↓
Stockage : Netlify Forms (primaire) + Buttondown (envoi)
   ↓
Welcome email avec lien lead magnet (3 versions FR/EN/ES)
   ↓
Drip 1 chronique/semaine via Buttondown
   ↓
Retour récurrent → Pixel Meta retargete → Conversion long terme
```

**Stack acquisition** :
- Pixel Meta : `867064843065581` (header.js, gated derrière le cookie consent)
- Buttondown : username `wiggmap`
- Netlify Forms : `newsletter` + `correction` (déclarés dans `forms.html`)
- Tracker : `window.wmTrackEvent('Lead', ...)` exposé globalement
- Lead magnet : `/lead-magnet/visas-2026-{en,fr,es}.html` — compile 25 visas (10 retraite + 10 nomade + 5 travail)
- Landing pages : `/lp/visa-mm2h-malaisie-{en,fr,es}.html`, `/lp/erasmus-prague-budget-{en,fr,es}.html`, `/lp/vivre-bali-budget-{en,fr,es}.html`

**Budget pub mensuel cible** : 300€/mois
- 30€ brand search Google ("wiggmap")
- 70€ retargeting Meta (visiteurs 30j)
- 50€ sponsoring newsletter expat (Beehiiv Boost ou direct)
- 100€ Search long-tail (Top 5 mots-clés audit)
- 50€ buffer outils + créa pubs

**Routine hebdo organique** : 2 chroniques + 2 vidéos TikTok/Insta + 2 posts X

---

## Priorités actuelles (Mars 2026)

### Court terme — contenu
1. **Ajouter ~10 nouvelles chronicles** — cible : 3 articles/semaine
2. **Vérifier et améliorer la qualité des données chiffrées** (countries2.json)

### Court terme — technique
3. **Ajouter la série Visa 2026 dans CHRONICLES.countries** (country.html) pour activer les liens "Related Chronicles" sur les pages pays concernées
4. **Mettre à jour sitemap.xml** avec les 9 URLs Visa 2026
5. **Résoudre les pages vides indexables** : compare.html + country.html sans paramètres

### Moyen terme
6. Améliorer le comparateur dynamique (compare.html) — UX + SEO
7. Rendre WiggGame plus attractif et addictif
8. Améliorer le globe interactif
9. Nouvelles idées de jeux ou outils engageants
10. Compléter les paires compare statiques manquantes à fort volume

### Long terme
11. Préparer les mécaniques communautaires
12. Monétisation progressive et propre

---

## État SEO (Avril 2026)

### Complété ✅
- Canonicals : 100% chronicles corrects
- **sitemap.xml régénéré** : 866 URLs avec lastmod auto, priorités correctes
- robots.txt OK
- hreflang sur les chronicles (HTML + CHRONICLE_LANGS header.js)
- Titles + meta descriptions différenciés sur 161 pays
- H1 vide country.html + canonical dynamique via setSeo()
- Maillage pays ↔ chronicles : 67 pays couverts
- header.js CHRONICLE_LANGS : complet
- **JSON-LD WebSite + SearchAction + Organization** sur homepage (sitelinks Google débloqués)
- **404.html customisé** avec search bar countries fonctionnelle (FR/EN/ES auto)
- **Breadcrumbs visibles** sur toutes les chronicles (injection footer.js)
- **Bloc "Continue exploring"** en bas de chaque chronique (3 cards aléatoires)
- **Newsletter capture** dans footer + dual-post Netlify Forms + Buttondown
- **Runtime swap .jpg → .webp** (footer.js, MutationObserver)
- **Images optimisées** : 269 fichiers convertis en WebP (-593 MB → poids assets divisé par ~5)
- **Pixel Meta** installé (id 867064843065581) avec cookie consent gating
- **Hierarchie H1** : 1 seul H1 par page (homepage seoFallback corrigé)
- **Newsletter form Netlify** : `newsletter` + `correction` déclarés dans forms.html

### En attente 🔲
- Série Visa 2026 absente de `CHRONICLES.countries` dans country.html
- sitemap.xml : vérifier présence des 9 URLs Visa 2026
- header.js `CHRONICLE_LANGS` : ajouter les 2 groupes Asie Expatriation (Partie 1 + Partie 2)
- `CHRONICLES._index` dans country.html : ajouter les 2 groupes Asie Expatriation
- `CHRONICLES.countries` dans country.html : ajouter les pays Asie Expatriation (Partie 1 → thailand, vietnam, indonesia, philippines / Partie 2 → japan, laos, china, cambodia)
- sitemap.xml : ajouter les 6 URLs Asie Expatriation (3 par partie)
- `CHRONICLES._index` dans country.html : ajouter le groupe Pays oubliés
- `CHRONICLES.countries` dans country.html : ajouter les pays Pays oubliés
- sitemap.xml : ajouter les 3 URLs Pays oubliés
- compare.html + country.html sans paramètres = pages vides indexables
- Compare statiques : pas de hreflang (perte audience FR/ES)
- Liens compare pages pays : seulement ~20 pays couverts dans COMPARE_PAIRS

---

## Opportunités de contenu identifiées

### Chronicles à haute valeur — non encore couvertes
- Meilleurs pays pour investisseurs / HNWI 2026
- Meilleurs pays pour retraités européens (vs série visa déjà faite — angle plus lifestyle)
- Guide expatriation par région : Asie du Sud-Est, Europe du Sud, Amérique Latine
- Meilleurs pays pour les familles avec enfants scolarisés (vs 2026 déjà fait — mise à jour)
- Fiscalité crypto par pays 2026
- Les pays qui ont le plus changé en 5 ans

### Compare pages à fort volume non couvertes
- portugal-vs-france, portugal-vs-uk, spain-vs-portugal (doublon quasi) 
- japan-vs-south-korea, japan-vs-singapore
- mexico-vs-thailand, colombia-vs-thailand
- uae-vs-portugal, uae-vs-spain

---

## Checklist livraison nouvelle chronicle

- [ ] GTM tag EN PREMIER dans `<head>`
- [ ] Title unique 50-60 chars, keyword en tête
- [ ] Meta description unique 145-160 chars
- [ ] Canonical exact wiggmap.com/chronicles/{filename}.html
- [ ] hreflang × 4 (fr + en + es + x-default → EN)
- [ ] JSON-LD Article (+ FAQPage si section FAQ)
- [ ] Google Fonts : Fraunces + Source Serif 4 + Poppins
- [ ] `<div id="siteHeader"></div>` + header.js en début de body
- [ ] Styles inline complets (Style A narratif ou Style B visa)
- [ ] Voix Wigg — pas IA, ouverture humaine, pros + cons
- [ ] Pull quote + dbox ou tableau + section FAQ 4-6 questions
- [ ] Section liens internes (pages pays + chronicles liées)
- [ ] `<div id="siteFooter"></div>` + footer.js + sw.js
- [ ] ⚠️ Après livraison : header.js CHRONICLE_LANGS + sitemap.xml + CHRONICLES._index country.html
