# WiggMap — Règles absolues & Architecture technique

## Stack
- HTML / CSS / JS vanilla — zéro framework, zéro npm, zéro build step
- Netlify — fichiers servis as-is
- Trilingue : EN / FR / ES
- GTM : GTM-K4MMRD4R | GA4 : G-36BWEJGCTB
- PWA : manifest.webmanifest + sw.js
- Canonical base : https://wiggmap.com

## Règles absolues — jamais les enfreindre
1. Ne jamais inventer des données ou des chiffres
2. Ne jamais casser une URL existante
3. Ne jamais modifier les fichiers JSON source sans validation explicite de Flo
4. Toujours tester sur 3 pages avant toute modification en masse
5. Toujours charger header.js et footer.js sur chaque nouvelle page
6. Toujours maintenir EN / FR / ES sur tout nouveau contenu
7. Zéro npm, zéro build — les fichiers sont servis tels quels
8. Avant toute action massive : montrer la liste et attendre validation
9. **À chaque création d'un nouvel article chronicle : ajouter ses 3 URLs dans `CHRONICLE_LANGS` dans `data/header.js`** — sans ça, le sélecteur de langue ne fonctionne pas dans l'article

## Changement de langue dans les articles chronicles — mécanisme obligatoire

Le changement de langue dans les articles est géré par `data/header.js` via l'objet `CHRONICLE_LANGS` (ligne ~252).

**Quand un nouvel article chronicle est créé (EN + FR + ES), il FAUT impérativement ajouter ses 3 URLs dans `CHRONICLE_LANGS` :**

```javascript
// Dans data/header.js, dans l'objet CHRONICLE_LANGS :
"/chronicles/[slug]-en.html": { en: "/chronicles/[slug]-en.html", fr: "/chronicles/[slug]-fr.html", es: "/chronicles/[slug]-es.html" },
"/chronicles/[slug]-fr.html": { en: "/chronicles/[slug]-en.html", fr: "/chronicles/[slug]-fr.html", es: "/chronicles/[slug]-es.html" },
"/chronicles/[slug]-es.html": { en: "/chronicles/[slug]-en.html", fr: "/chronicles/[slug]-fr.html", es: "/chronicles/[slug]-es.html" },
```

Sans ce mapping, le sélecteur de langue dans le header fait `location.reload()` au lieu de naviguer vers la bonne version — l'utilisateur reste bloqué dans la même langue.

## URLs exactes du site

```
/                                       → Homepage
/countries/country.html?country=[slug]  → Pages pays (template unique)
/compare.html                           → Comparateur dynamique (racine)
/compare/static/[a]-vs-[b]/             → ~36 pages compare statiques SEO
/chronicles/[slug]-[lang].html          → Articles longs formats
/indexchronicles.html                   → Index des chronicles
/globe.html                             → Globe 3D (racine)
/ggg/wigggame.html                      → WiggGame
/ggg/index.html                         → Landing WiggGame
/about.html / /terms.html / /privacy.html / /forms.html
```

## Fichiers de données — noms exacts

```
/data/countries.json            ← SOURCE TABLE PAYS EN (25+ champs par pays)
/data/countries.fr.json         ← SOURCE TABLE PAYS FR
/data/countries.es.json         ← SOURCE TABLE PAYS ES
/data/map/geo-by-slug2.json     ← Coordonnées géo (globe + cartes)
/data/details/[slug].json       ← Profils qualitatifs EN (~163 fichiers)
/data/details-fr/[slug].json    ← Profils qualitatifs FR
/data/details-es/[slug].json    ← Profils qualitatifs ES
/data/countries.json            ← Liste noms pays EN (search + random)
/data/countries.fr.json         ← Liste noms pays FR
/data/countries.es.json         ← Liste noms pays ES
/data/timezones-by-slug.json    ← Fuseaux horaires (horloge locale)
/data/header.js                 ← Header injecté dans <div id="siteHeader">
/data/footer.js                 ← Footer injecté dans <div id="siteFooter">
/data/share.js                  ← Bouton partage
/data/correction-form.js        ← Modal correction données (Netlify Forms)
/data/style.css                 ← CSS partagé (certaines chronicles)
/ggg/questions.json             ← Questions WiggGame EN
/ggg/Qfr/questionsfr.json       ← Questions WiggGame FR
/ggg/Qes/questionses.json       ← Questions WiggGame ES
/_gen_v3.py                     ← Script Python génération batch
/template_chronicles.html       ← Template HTML chronicle
```

## Header.js — logique de profondeur (critique)

Chaque nouvelle page doit respecter ce système de préfixes, sinon tous les liens cassent :

```javascript
isSubPage  = path.includes("/countries/") || path.includes("/chronicles/")
isDeepPage = path.includes("/compare/static/")
prefix = isDeepPage ? "../../../" : (isSubPage ? "../" : "")
```

- **Racine** (`/about.html`, `/globe.html`...) → prefix = `""`
- **Sous-pages** (`/countries/`, `/chronicles/`) → prefix = `"../"`
- **Pages profondes** (`/compare/static/a-vs-b/`) → prefix = `"../../../"`

Mount points obligatoires sur chaque page :
```html
<div id="siteHeader"></div>   ← header.js injecte ici
<div id="siteFooter"></div>   ← footer.js injecte ici
```

## Montage HTML selon type de page

### Chronicles
```html
<head>
  <!-- GTM EN PREMIER (pas de GA4 sur les chronicles) -->
  <script>(function(w,d,s,l,i){...GTM-K4MMRD4R...})</script>
  <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="icon" href="../assets/favicon.ico" />
  <link rel="manifest" href="../manifest.webmanifest" />
  <meta name="theme-color" content="#22c55e" />
  <title>{50-60 chars · WiggMap}</title>
  <meta name="description" content="{145-160 chars}" />
  <link rel="canonical" href="https://wiggmap.com/chronicles/{filename}.html" />
  <link rel="alternate" hreflang="fr" href="...{fr}.html" />
  <link rel="alternate" hreflang="en" href="...{en}.html" />
  <link rel="alternate" hreflang="es" href="...{es}.html" />
  <link rel="alternate" hreflang="x-default" href="...{en}.html" />
  <script type="application/ld+json">{"@type":"Article",...}</script>
  <!-- Google Fonts : Fraunces + Source Serif 4 + Poppins -->
  <style>/* styles inline complets */</style>
</head>
<body>
  <div id="siteHeader"></div>
  <script src="../data/header.js"></script>
  <!-- contenu -->
  <div id="siteFooter"></div>
  <script src="../data/footer.js"></script>
  <script>if('serviceWorker' in navigator){navigator.serviceWorker.register('../sw.js').catch(()=>{});}</script>
</body>
```

### country.html — différences importantes
- GA4 (gtag.js) D'ABORD dans `<head>`, puis GTM — ordre inverse des chronicles
- `<script src="../data/header.js">` chargé immédiatement après l'ouverture de `<body>`
- Footer : footer.js uniquement — PAS de sw.js sur country.html
- Scripts additionnels : `data/share.js` + `data/correction-form.js`

## Bugs de données connus (ne pas créer de doublons)
- `data/details/dominican-republic (1).json` = doublon de `dominican-republic.json`
- `data/details/irland.json` = typo, le bon fichier est `ireland.json`
- Ces doublons existent aussi dans `details-fr/` et `details-es/`
