# WiggMap — Project Rules

## Stack
- HTML/CSS/JS vanilla, zero framework
- JSON data files in /data/
- Netlify deploy (no build step)
- Trilingual : EN / FR / ES

## Structure
- /countries/country.html?country=slug — country pages
- /compare/compare.html — dynamic compare tool
- /chronicles/ — long-form HTML articles
- /data/countries.json + countries.fr.json + countries.es.json
- /data/details/[slug].json — detailed country data
- header.js + footer.js loaded on every page

## Absolute rules
- Never rename or break existing URLs
- Never modify JSON source files without explicit approval
- Always test on 3 pages before any mass generation
- Every new page must load header.js and footer.js
- Always maintain EN/FR/ES compatibility
- Run no npm/build commands — files are served as-is

## Canonical URL base
https://wiggmap.com