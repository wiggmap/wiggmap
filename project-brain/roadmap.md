# WiggMap — Roadmap & État du projet

## Vision et objectif

WiggMap est une plateforme éducative, récréative et attractive sur les pays du monde.  
**Phase actuelle :** construire la qualité du contenu et acquérir du trafic organique.  
**Objectif final :** monétisation propre une fois le trafic établi (affiliations, partenariats — SafetyWing, Wise, Booking, NordVPN, services de relocation). Pas de monétisation prématurée qui dégraderait l'expérience.

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

## État SEO (Mars 2026)

### Complété ✅
- Canonicals : 42/42 chronicles corrects
- robots.txt + sitemap.xml (229 URLs)
- hreflang sur les 42 chronicles (HTML + CHRONICLE_LANGS header.js)
- Titles + meta descriptions différenciés sur 161 pays
- H1 vide country.html + canonical dynamique via setSeo()
- Maillage pays ↔ chronicles : 67 pays couverts
- header.js CHRONICLE_LANGS : complet incluant Visa 2026, Asie Expatriation et Pays oubliés

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
