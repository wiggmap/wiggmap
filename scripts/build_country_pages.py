#!/usr/bin/env python3
"""
Generate static SEO-friendly country pages.

Reads:
  - data/countries.{json,fr.json,es.json}      (table fields per country, per lang)
  - data/details/{slug}.json                   (deep dive content, EN)
  - data/details-fr/{slug}.json                (FR)
  - data/details-es/{slug}.json                (ES)
  - data/geo-by-slug.json                      (ISO2 codes for flags)

Writes:
  - countries/{slug}-{lang}.html               (one file per country × lang)

Usage:
  python3 scripts/build_country_pages.py
"""

import json, os, re, sys, html, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'countries')

# ──────────────────────────────────────────────────────────────────────
# i18n labels
# ──────────────────────────────────────────────────────────────────────
LABELS = {
    'en': {
        'site': 'WiggMap',
        'home': 'Home', 'countries': 'Countries',
        'snapshot': 'Quick snapshot',
        'capital': 'Capital', 'population': 'Population',
        'languages': 'Languages', 'driving': 'Driving side',
        'currency': 'Currency', 'crypto': 'Crypto-friendly',
        'expat_score': 'Expat Score',
        'cost_table': 'Cost of living, salaries & quality of life',
        'overview': 'Country overview',
        'things_to_know': 'Things to know',
        'cities': 'City guides',
        'related': 'Related chronicles',
        'compare': 'Country comparisons',
        'compare_with': 'Compare with another country',
        'last_update': 'Last updated',
        'see_all_countries': 'See all 160+ countries',
        'sec_salaries': '💼 Salaries (net / month)',
        'sec_housing': '🏠 Housing & utilities (studio reference)',
        'sec_food': '🍽️ Food & drink (typical prices)',
        'sec_transport': '⛽ Transport',
        'sec_taxes': '🧾 Taxes (indicative)',
        'sec_tech': '📱 Tech (indicative prices)',
        'sec_immigration': '🛂 Moving & immigration',
        'sec_qol': '🌤️ Quality of life',
        'sec_indices': '📈 Indices',
        'sec_religion': '🕍 Religion snapshot',
        'fld': {
            'min_wage': 'Minimum wage', 'avg_salary': 'Average salary',
            'doctor_salary': 'Doctor (GP) salary',
            'rent_studio': 'Studio rent', 'electricity': 'Electricity',
            'water': 'Water', 'mobile': 'Mobile plan',
            'beer': 'Beer (pint)', 'coffee': 'Coffee', 'dish': 'Main dish',
            'gas': 'Gasoline / litre',
            'vat': 'VAT', 'income_tax': 'Income tax',
            'smallbiz': 'Small business tax',
            'iphone': 'iPhone (latest 256GB)', 'samsung': 'Galaxy S (latest 256GB)',
            'immigration': 'Immigration-friendly',
            'happiness': 'Happiness', 'sun': 'Sunny days / year',
            'health': 'Public healthcare', 'insurance': 'Private insurance / mo',
            'crime': 'Crime Index', 'pp': 'Purchasing Power',
            'religion_christian': 'Christian', 'religion_muslim': 'Muslim',
            'religion_buddhist': 'Buddhist', 'religion_jewish': 'Jewish',
            'religion_other': 'Other / None',
        },
        'view_chronicle': 'Read chronicle',
    },
    'fr': {
        'site': 'WiggMap',
        'home': 'Accueil', 'countries': 'Pays',
        'snapshot': 'Aperçu rapide',
        'capital': 'Capitale', 'population': 'Population',
        'languages': 'Langues', 'driving': 'Conduite',
        'currency': 'Monnaie', 'crypto': 'Crypto-friendly',
        'expat_score': 'Score Expat',
        'cost_table': 'Coût de la vie, salaires et qualité de vie',
        'overview': 'Aperçu du pays',
        'things_to_know': 'À savoir',
        'cities': 'Guides villes',
        'related': 'Chroniques liées',
        'compare': 'Comparaisons de pays',
        'compare_with': 'Comparer avec un autre pays',
        'last_update': 'Mise à jour',
        'see_all_countries': 'Voir les 160+ pays',
        'sec_salaries': '💼 Salaires (net / mois)',
        'sec_housing': '🏠 Logement et charges (studio référence)',
        'sec_food': '🍽️ Alimentation et boissons (prix indicatifs)',
        'sec_transport': '⛽ Transport',
        'sec_taxes': '🧾 Fiscalité (indicatif)',
        'sec_tech': '📱 Tech (prix indicatifs)',
        'sec_immigration': '🛂 Immigration et installation',
        'sec_qol': '🌤️ Qualité de vie',
        'sec_indices': '📈 Indices',
        'sec_religion': '🕍 Religion',
        'fld': {
            'min_wage': 'Salaire minimum', 'avg_salary': 'Salaire moyen',
            'doctor_salary': 'Salaire médecin (généraliste)',
            'rent_studio': 'Loyer studio', 'electricity': 'Électricité',
            'water': 'Eau', 'mobile': 'Forfait mobile',
            'beer': 'Bière (pinte)', 'coffee': 'Café', 'dish': 'Plat principal',
            'gas': 'Essence / litre',
            'vat': 'TVA', 'income_tax': 'Impôt sur le revenu',
            'smallbiz': 'Fiscalité petite entreprise',
            'iphone': 'iPhone (dernier 256 Go)', 'samsung': 'Galaxy S (dernier 256 Go)',
            'immigration': 'Facilité d\'immigration',
            'happiness': 'Bonheur', 'sun': 'Jours de soleil / an',
            'health': 'Santé publique', 'insurance': 'Assurance privée / mois',
            'crime': 'Indice criminalité', 'pp': 'Pouvoir d\'achat',
            'religion_christian': 'Chrétien', 'religion_muslim': 'Musulman',
            'religion_buddhist': 'Bouddhiste', 'religion_jewish': 'Juif',
            'religion_other': 'Autre / Aucune',
        },
        'view_chronicle': 'Lire la chronique',
    },
    'es': {
        'site': 'WiggMap',
        'home': 'Inicio', 'countries': 'Países',
        'snapshot': 'Vistazo rápido',
        'capital': 'Capital', 'population': 'Población',
        'languages': 'Idiomas', 'driving': 'Conducción',
        'currency': 'Moneda', 'crypto': 'Crypto-amigable',
        'expat_score': 'Puntuación expat',
        'cost_table': 'Coste de vida, salarios y calidad de vida',
        'overview': 'Visión general del país',
        'things_to_know': 'Lo que hay que saber',
        'cities': 'Guías de ciudades',
        'related': 'Crónicas relacionadas',
        'compare': 'Comparativas de países',
        'compare_with': 'Comparar con otro país',
        'last_update': 'Actualizado',
        'see_all_countries': 'Ver los 160+ países',
        'sec_salaries': '💼 Salarios (neto / mes)',
        'sec_housing': '🏠 Vivienda y servicios (estudio de referencia)',
        'sec_food': '🍽️ Comida y bebida (precios típicos)',
        'sec_transport': '⛽ Transporte',
        'sec_taxes': '🧾 Impuestos (indicativo)',
        'sec_tech': '📱 Tech (precios indicativos)',
        'sec_immigration': '🛂 Mudanza e inmigración',
        'sec_qol': '🌤️ Calidad de vida',
        'sec_indices': '📈 Índices',
        'sec_religion': '🕍 Religión',
        'fld': {
            'min_wage': 'Salario mínimo', 'avg_salary': 'Salario medio',
            'doctor_salary': 'Salario médico (general)',
            'rent_studio': 'Alquiler estudio', 'electricity': 'Electricidad',
            'water': 'Agua', 'mobile': 'Plan móvil',
            'beer': 'Cerveza (pinta)', 'coffee': 'Café', 'dish': 'Plato principal',
            'gas': 'Gasolina / litro',
            'vat': 'IVA', 'income_tax': 'Impuesto sobre la renta',
            'smallbiz': 'Impuesto pequeña empresa',
            'iphone': 'iPhone (último 256GB)', 'samsung': 'Galaxy S (último 256GB)',
            'immigration': 'Facilidad de inmigración',
            'happiness': 'Felicidad', 'sun': 'Días de sol / año',
            'health': 'Sanidad pública', 'insurance': 'Seguro privado / mes',
            'crime': 'Índice de criminalidad', 'pp': 'Poder adquisitivo',
            'religion_christian': 'Cristiano', 'religion_muslim': 'Musulmán',
            'religion_buddhist': 'Budista', 'religion_jewish': 'Judío',
            'religion_other': 'Otra / Ninguna',
        },
        'view_chronicle': 'Leer crónica',
    },
}

SECTIONS = [
    ('sec_salaries',     [('min_wage','🧾'),('avg_salary','📊'),('doctor_salary','🩺')]),
    ('sec_housing',      [('rent_studio','🏚️'),('electricity','⚡'),('water','💧'),('mobile','📱')]),
    ('sec_food',         [('beer','🍺'),('coffee','☕'),('dish','🍲')]),
    ('sec_transport',    [('gas','⛽')]),
    ('sec_taxes',        [('vat','🏷️'),('income_tax','👤'),('smallbiz','🏪')]),
    ('sec_tech',         [('iphone','🍎'),('samsung','📲')]),
    ('sec_immigration',  [('immigration','🛂')]),
    ('sec_qol',          [('happiness','🙂'),('sun','☀️'),('health','🏥'),('insurance','🧑‍⚕️')]),
    ('sec_indices',      [('crime','🚔'),('pp','💶')]),
    ('sec_religion',     [('religion_christian','✝️'),('religion_muslim','☪️'),
                          ('religion_buddhist','☸️'),('religion_jewish','✡️'),('religion_other','🕊️')]),
]

# ──────────────────────────────────────────────────────────────────────
# City chronicles per country (from country.html CITY_CHRONICLES.countries)
# Each entry maps the country to slugs that match chronicle filenames.
# We'll resolve each city to its actual chronicle URL by globbing.
# ──────────────────────────────────────────────────────────────────────
CITIES_BY_COUNTRY = {
    'france':        ['paris','lyon','marseille','nice'],
    'thailand':      ['bangkok','chiang-mai','phuket','hua-hin'],
    'australia':     ['sydney','melbourne','cairns','perth'],
    'canada':        ['vancouver','montreal','toronto','calgary'],
    'spain':         ['madrid','barcelone','valence','malaga'],
    'brazil':        ['sao-paulo','rio','florianopolis','salvador'],
    'japan':         ['tokyo','osaka','fukuoka','kyoto'],
    'mexico':        ['mexico-city','guadalajara','monterrey','cancun'],
    'united-states': ['new-york','los-angeles','miami','austin'],
    'portugal':      ['lisbonne','porto','faro','funchal'],
    'greece':        ['athenes','thessalonique','heraklion','la-canee'],
    'indonesia':     ['bali','jakarta','surabaya','yogyakarta'],
}

# ──────────────────────────────────────────────────────────────────────
# Related thematic chronicles per country (extracted from country.html)
# ──────────────────────────────────────────────────────────────────────
CHRONICLES_BY_COUNTRY = {
    'afghanistan': ['ameriques-2'], 'argentina': ['ameriques-3','study-americas-africa'],
    'armenia': ['chronicle-2056'],
    'australia': ['australia-guide','ameriques-3','raise-children','study-asia-pacific'],
    'austria': ['raise-children','chronicle-2056'],
    'bahamas': ['ameriques-1','ameriques-2','ameriques-3'],
    'belarus': ['ameriques-2'],
    'belgium': ['ameriques-1','ameriques-3','expats-crypto'],
    'bulgaria': ['expats-crypto','digital-nomads'],
    'cambodia': ['expats-crypto','asia-expat-2'],
    'canada': ['ameriques-1','ameriques-2','ameriques-3','study-americas-africa'],
    'chile': ['chronicle-2056'],
    'china': ['raise-children','chronicle-2056','asia-expat-2'],
    'colombia': ['ameriques-3','raise-children','chronicle-2056','property-abroad'],
    'costa-rica': ['ameriques-1','ameriques-2','ameriques-3'],
    'croatia': ['digital-nomads'], 'cuba': ['ameriques-2'],
    'cyprus': ['forgotten-countries','study-erasmus','property-abroad'],
    'czech-republic': ['chronicle-2056','study-erasmus'],
    'denmark': ['raise-children','chronicle-2056'],
    'estonia': ['expats-crypto','raise-children','chronicle-2056','study-erasmus'],
    'finland': ['raise-children','chronicle-2056'],
    'france': ['raise-children','expats-crypto','chronicle-2056','study-practical'],
    'georgia': ['expats-crypto','chronicle-2056'],
    'germany': ['ameriques-3','expats-crypto','raise-children','study-practical'],
    'greece': ['ameriques-1','digital-nomads','chronicle-2056','property-abroad'],
    'hungary': ['digital-nomads','chronicle-2056','study-erasmus'],
    'iceland': ['raise-children','chronicle-2056'],
    'indonesia': ['expats-crypto','asia-expat-1','property-abroad'],
    'iran': ['ameriques-2','chronicle-2056'], 'ireland': ['ameriques-3'],
    'israel': ['chronicle-2056'], 'italy': ['digital-nomads','chronicle-2056'],
    'japan': ['raise-children','chronicle-2056','asia-expat-2','study-asia-pacific','property-abroad'],
    'laos': ['expats-crypto','asia-expat-2'], 'latvia': ['study-erasmus'],
    'lebanon': ['chronicle-2056'], 'luxembourg': ['ameriques-2'],
    'malaysia': ['chronicle-2056','study-asia-pacific'],
    'malta': ['expats-crypto'], 'madagascar': ['africa-expat-1','africa-expat-2'],
    'mauritius': ['forgotten-countries','africa-expat-1','africa-expat-2'],
    'mexico': ['ameriques-2','ameriques-3','study-americas-africa','property-abroad'],
    'morocco': ['africa-expat-1','africa-expat-2','study-americas-africa','property-abroad'],
    'moldova': ['chronicle-2056'], 'monaco': ['ameriques-2'],
    'montenegro': ['forgotten-countries'],
    'netherlands': ['ameriques-2','ameriques-3','raise-children'],
    'new-zealand': ['raise-children','chronicle-2056'],
    'norway': ['raise-children','chronicle-2056'], 'oman': ['forgotten-countries'],
    'panama': ['ameriques-1','ameriques-2','ameriques-3','property-abroad'],
    'philippines': ['chronicle-2056','asia-expat-1','property-abroad'],
    'poland': ['chronicle-2056','study-erasmus'],
    'portugal': ['expats-crypto','digital-nomads','raise-children','property-abroad'],
    'russia': ['ameriques-2','chronicle-2056'], 'saudi-arabia': ['chronicle-2056'],
    'singapore': ['ameriques-2','expats-crypto','raise-children','study-asia-pacific'],
    'slovenia': ['digital-nomads','chronicle-2056','study-erasmus'],
    'south-korea': ['raise-children','chronicle-2056','study-asia-pacific'],
    'spain': ['ameriques-2','ameriques-3','expats-crypto','study-erasmus','property-abroad'],
    'sweden': ['raise-children','chronicle-2056'],
    'switzerland': ['ameriques-1','ameriques-2','expats-crypto'],
    'taiwan': ['chronicle-2056','forgotten-countries','study-asia-pacific'],
    'thailand': ['expats-crypto','digital-nomads','asia-expat-1','property-abroad'],
    'turkey': ['chronicle-2056','property-abroad'], 'ukraine': ['chronicle-2056'],
    'united-arab-emirates': ['expats-crypto','property-abroad'],
    'united-kingdom': ['ameriques-2','ameriques-3','raise-children','study-practical'],
    'united-states': ['ameriques-1','ameriques-2','expats-crypto','study-americas-africa'],
    'uruguay': ['chronicle-2056','forgotten-countries'], 'venezuela': ['chronicle-2056'],
    'vietnam': ['expats-crypto','chronicle-2056','asia-expat-1','property-abroad'],
    'yemen': ['chronicle-2056'], 'tunisia': ['africa-expat-1','africa-expat-2'],
    'egypt': ['africa-expat-1','africa-expat-2'],
    'seychelles': ['africa-expat-1','africa-expat-2'],
    'kenya': ['africa-expat-1','africa-expat-3'],
    'rwanda': ['africa-expat-1','africa-expat-3'],
    'tanzania': ['africa-expat-1','africa-expat-3'],
    'namibia': ['africa-expat-1','africa-expat-3'],
    'south-africa': ['africa-expat-1','africa-expat-3','study-americas-africa'],
    'botswana': ['africa-expat-1','africa-expat-3'],
    'senegal': ['africa-expat-1','africa-expat-4','study-americas-africa'],
    'ghana': ['africa-expat-1','africa-expat-4','study-americas-africa'],
    'ivory-coast': ['africa-expat-1','africa-expat-4'],
    'cape-verde': ['africa-expat-1','africa-expat-2'],
}

# Chronicle ID → titles + URLs per lang
CHRONICLES_INDEX = {
    'chronicle-2056': {
        'en': ('2056: Where Will Life Be Best in 30 Years?', '/chronicles/chronicle-2056-best-countries-30-years-en.html'),
        'fr': ('2056 : Où vivra-t-on le mieux dans 30 ans ?', '/chronicles/chronicle-2056-ou-vivra-t-on-le-mieux-fr.html'),
        'es': ('2056: ¿Dónde se vivirá mejor en 30 años?', '/chronicles/chronicle-2056-mejores-paises-30-anos-es.html'),
    },
    'ameriques-1': {
        'en': ('Panama, Costa Rica, Puerto Rico — The Americas Expat 2026 Part 1', '/chronicles/chronicle-ameriques-partie1-en.html'),
        'fr': ('Panama, Costa Rica, Puerto Rico — comparatif expat 2026 Partie 1', '/chronicles/chronicle-ameriques-partie1-fr.html'),
        'es': ('Panamá, Costa Rica, Puerto Rico — Expatriados 2026 Parte 1', '/chronicles/chronicle-ameriques-partie1-es.html'),
    },
    'ameriques-2': {
        'en': ('St. Kitts, Bahamas, Antigua — Zero Tax 2026 Part 2', '/chronicles/chronicle-ameriques-partie2-en.html'),
        'fr': ('Saint Kitts, Bahamas, Antigua — Zéro impôt 2026 Partie 2', '/chronicles/chronicle-ameriques-partie2-fr.html'),
        'es': ('St. Kitts, Bahamas, Antigua — Cero impuestos 2026 Parte 2', '/chronicles/chronicle-ameriques-partie2-es.html'),
    },
    'ameriques-3': {
        'en': ('Anguilla, BVI, Sint Maarten — Offshore 2026 Part 3', '/chronicles/chronicle-ameriques-partie3-en.html'),
        'fr': ('Anguilla, Îles Vierges, Sint Maarten — Offshore 2026 Partie 3', '/chronicles/chronicle-ameriques-partie3-fr.html'),
        'es': ('Anguila, Islas Vírgenes, Sint Maarten — Offshore 2026 Parte 3', '/chronicles/chronicle-ameriques-partie3-es.html'),
    },
    'australia-guide': {
        'en': ('Australia 2026 — Complete Expat Guide', '/chronicles/chronicle-australia-expat-guide-2026-en.html'),
        'fr': ('Australie 2026 — Guide complet expatriation', '/chronicles/chronicle-australie-expatriation-2026-fr.html'),
        'es': ('Australia 2026 — Guía completa', '/chronicles/chronicle-australia-guia-expatriados-2026-es.html'),
    },
    'raise-children': {
        'en': ('Best Countries to Raise Children 2026', '/chronicles/chronicle-raise-children-2026-en.html'),
        'fr': ('Où élever ses enfants en 2026 ?', '/chronicles/chronicle-elever-enfants-2026-fr.html'),
        'es': ('Mejores países para criar hijos 2026', '/chronicles/chronicle-criar-hijos-2026-es.html'),
    },
    'digital-nomads': {
        'en': ('Best Countries for Digital Nomads 2026', '/chronicles/digital-nomads-2026-en.html'),
        'fr': ('Meilleurs pays pour digital nomads 2026', '/chronicles/digital-nomads-2026-fr.html'),
        'es': ('Mejores países para nómadas digitales 2026', '/chronicles/digital-nomads-2026-es.html'),
    },
    'expats-crypto': {
        'en': ('Best Country for Expats, Nomads & Crypto 2026', '/chronicles/expats-nomads-crypto-2026-en.html'),
        'fr': ('Meilleur pays pour expatriés, nomades et crypto 2026', '/chronicles/expatries-nomades-crypto-2026-fr.html'),
        'es': ('Mejor país para expatriados, nómadas y crypto 2026', '/chronicles/expatriados-nomadas-crypto-2026-es.html'),
    },
    'asia-expat-1': {
        'en': ('Asia Expat Guide 2026 Part 1 — Thailand, Vietnam, Bali', '/chronicles/chronicle-asia-expat-guide-part1-2026-en.html'),
        'fr': ('Asie expatriation 2026 Partie 1 — Thaïlande, Vietnam, Bali', '/chronicles/chronicle-asie-expatriation-partie1-2026-fr.html'),
        'es': ('Asia Guía 2026 Parte 1 — Tailandia, Vietnam, Bali', '/chronicles/chronicle-asia-guia-expatriados-parte1-2026-es.html'),
    },
    'asia-expat-2': {
        'en': ('Asia Expat Guide 2026 Part 2 — Japan, Laos, China', '/chronicles/chronicle-asia-expat-guide-part2-2026-en.html'),
        'fr': ('Asie expatriation 2026 Partie 2 — Japon, Laos, Chine', '/chronicles/chronicle-asie-expatriation-partie2-2026-fr.html'),
        'es': ('Asia Guía 2026 Parte 2 — Japón, Laos, China', '/chronicles/chronicle-asia-guia-expatriados-parte2-2026-es.html'),
    },
    'forgotten-countries': {
        'en': ('The Forgotten Countries — 6 Underrated Expat Destinations', '/chronicles/chronicle-forgotten-expat-countries-2026-en.html'),
        'fr': ('Les pays oubliés — 6 destinations sous-cotées', '/chronicles/chronicle-pays-oublies-expatriation-2026-fr.html'),
        'es': ('Los países olvidados — 6 destinos infravalorados', '/chronicles/chronicle-paises-olvidados-expatriacion-2026-es.html'),
    },
    'africa-expat-1': {
        'en': ('Expat in Africa 2026 Part 1 — Overview & Key Data', '/chronicles/chronicle-africa-expat-p1-en.html'),
        'fr': ('S\'expatrier en Afrique 2026 Partie 1 — Vue d\'ensemble', '/chronicles/chronicle-afrique-expatrier-p1-fr.html'),
        'es': ('Expatriarse en África 2026 Parte 1 — Visión general', '/chronicles/chronicle-africa-expatriarse-p1-es.html'),
    },
    'africa-expat-2': {
        'en': ('Africa 2026 Part 2 — Morocco, Tunisia, Egypt, Mauritius', '/chronicles/chronicle-africa-expat-p2-en.html'),
        'fr': ('Afrique 2026 Partie 2 — Maroc, Tunisie, Égypte, Maurice', '/chronicles/chronicle-afrique-expatrier-p2-fr.html'),
        'es': ('África 2026 Parte 2 — Marruecos, Túnez, Egipto, Mauricio', '/chronicles/chronicle-africa-expatriarse-p2-es.html'),
    },
    'africa-expat-3': {
        'en': ('Africa 2026 Part 3 — Kenya, Rwanda, Tanzania, Namibia, South Africa', '/chronicles/chronicle-africa-expat-p3-en.html'),
        'fr': ('Afrique 2026 Partie 3 — Kenya, Rwanda, Tanzanie, Namibie, Afrique du Sud', '/chronicles/chronicle-afrique-expatrier-p3-fr.html'),
        'es': ('África 2026 Parte 3 — Kenia, Ruanda, Tanzania, Namibia, Sudáfrica', '/chronicles/chronicle-africa-expatriarse-p3-es.html'),
    },
    'africa-expat-4': {
        'en': ('Africa 2026 Part 4 — Senegal, Ghana, Ivory Coast', '/chronicles/chronicle-africa-expat-p4-en.html'),
        'fr': ('Afrique 2026 Partie 4 — Sénégal, Ghana, Côte d\'Ivoire', '/chronicles/chronicle-afrique-expatrier-p4-fr.html'),
        'es': ('África 2026 Parte 4 — Senegal, Ghana, Costa de Marfil', '/chronicles/chronicle-africa-expatriarse-p4-es.html'),
    },
    'study-erasmus': {
        'en': ('Studying Abroad in Europe 2026 — 8 Erasmus Destinations', '/chronicles/chronicle-study-abroad-europe-erasmus-2026-en.html'),
        'fr': ('Étudier en Europe 2026 — 8 destinations Erasmus', '/chronicles/chronicle-etudier-europe-erasmus-2026-fr.html'),
        'es': ('Estudiar en Europa 2026 — 8 destinos Erasmus', '/chronicles/chronicle-estudiar-europa-erasmus-2026-es.html'),
    },
    'study-americas-africa': {
        'en': ('Studying Abroad in the Americas & Africa 2026', '/chronicles/chronicle-study-abroad-americas-africa-2026-en.html'),
        'fr': ('Étudier aux Amériques et en Afrique 2026', '/chronicles/chronicle-etudier-ameriques-afrique-2026-fr.html'),
        'es': ('Estudiar en las Américas y África 2026', '/chronicles/chronicle-estudiar-americas-africa-2026-es.html'),
    },
    'study-asia-pacific': {
        'en': ('Studying Abroad in Asia-Pacific 2026', '/chronicles/chronicle-study-abroad-asia-pacific-2026-en.html'),
        'fr': ('Étudier en Asie-Pacifique 2026', '/chronicles/chronicle-etudier-asie-pacifique-2026-fr.html'),
        'es': ('Estudiar en Asia-Pacífico 2026', '/chronicles/chronicle-estudiar-asia-pacifico-2026-es.html'),
    },
    'study-practical': {
        'en': ('Study Abroad — The Complete Practical Guide 2026', '/chronicles/chronicle-study-abroad-practical-guide-2026-en.html'),
        'fr': ('Étudier à l\'étranger — Le guide pratique complet 2026', '/chronicles/chronicle-etudier-etranger-guide-pratique-2026-fr.html'),
        'es': ('Estudiar en el extranjero — Guía práctica completa 2026', '/chronicles/chronicle-estudiar-extranjero-guia-practica-2026-es.html'),
    },
    'property-abroad': {
        'en': ('Buying Property Abroad — What Foreigners Actually Own', '/chronicles/chronicle-property-abroad-2026-en.html'),
        'fr': ('Immobilier à l\'étranger — Ce que les étrangers possèdent vraiment', '/chronicles/chronicle-immo-etranger-2026-fr.html'),
        'es': ('Comprar propiedad en el extranjero — Lo que los extranjeros poseen', '/chronicles/chronicle-propiedad-extranjero-2026-es.html'),
    },
}


def iso2_to_flag(iso2):
    if not iso2 or len(iso2) != 2: return ''
    return ''.join(chr(ord(c) - ord('A') + 0x1F1E6) for c in iso2.upper())


# Same color cycle as the SPA's formatPara() in country.html
TAG_COLORS = [
    ("rgba(34,197,94,.12)",  "rgba(34,197,94,.25)",  "#15803d"),
    ("rgba(59,130,246,.12)", "rgba(59,130,246,.25)", "#1d4ed8"),
    ("rgba(245,158,11,.12)", "rgba(245,158,11,.25)", "#92400e"),
    ("rgba(239,68,68,.12)",  "rgba(239,68,68,.25)",  "#b91c1c"),
    ("rgba(139,92,246,.12)", "rgba(139,92,246,.25)", "#6d28d9"),
    ("rgba(236,72,153,.12)", "rgba(236,72,153,.25)", "#be185d"),
    ("rgba(6,182,212,.12)",  "rgba(6,182,212,.25)",  "#0e7490"),
    ("rgba(249,115,22,.12)", "rgba(249,115,22,.25)", "#c2410c"),
]


def format_paragraph(text, tag_state):
    """Convert one paragraph: escape HTML, then **bold** → coloured art-tag with <br>."""
    safe = html.escape(text)
    def repl(m):
        title = m.group(1)
        bg, br, fg = TAG_COLORS[tag_state['i'] % len(TAG_COLORS)]
        tag_state['i'] += 1
        return f'<span class="art-tag" style="background:{bg};border:1px solid {br};color:{fg}">{title}</span><br>'
    safe = re.sub(r'\*\*(.+?)\*\*', repl, safe)
    return f'<p>{safe}</p>'


def render_article_body(article, map_block_html=''):
    """Match the SPA's renderArticleBodyWithMap: split paragraphs, insert map at midpoint."""
    if not article: return ''
    article = article.replace('[[MAP]]', '')
    paras = [p.strip() for p in re.split(r'\n{2,}', article) if p.strip()]
    if not paras: return ''
    state = {'i': 0}
    mid = len(paras) // 2
    before = ''.join(format_paragraph(p, state) for p in paras[:mid])
    after  = ''.join(format_paragraph(p, state) for p in paras[mid:])
    return before + map_block_html + after


# City slug → image filename inside /assetscity/ (matches CV_IMAGES from country.html)
CITY_IMAGE = {
    'paris': 'paris.png', 'lyon': 'lyon.png', 'marseille': 'marseille.png', 'nice': 'nice.png',
    'bangkok': 'bangkok.png', 'chiang-mai': 'chiangmai.png', 'phuket': 'phuket.png', 'hua-hin': 'huahin.png',
    'sydney': 'sydney.png', 'melbourne': 'melbourne.png', 'cairns': 'cairns.png', 'perth': 'perth.png',
    'vancouver': 'vancouver.png', 'montreal': 'montreal.png', 'toronto': 'toronto.png', 'calgary': 'calgary.png',
    'madrid': 'madrid.png', 'barcelone': 'barcelone.png', 'valence': 'valence.png', 'malaga': 'malaga.png',
    'sao-paulo': 'saopaulo.png', 'rio': 'rio.png', 'florianopolis': 'florianopolis.png', 'salvador': 'salvadorcity.png',
    'tokyo': 'tokyo.png', 'osaka': 'osaka.png', 'fukuoka': 'fukuoka.png', 'kyoto': 'kyoto.png',
    'mexico-city': 'mexicocity.png', 'guadalajara': 'guadalajara.png', 'monterrey': 'monterrey.png', 'cancun': 'cancun.png',
    'new-york': 'new york.png', 'los-angeles': 'LA.png', 'miami': 'miami.png', 'austin': 'austin.png',
    'lisbonne': 'lisbonne.png', 'porto': 'porto.png', 'faro': 'faro.png', 'funchal': 'funchal.png',
    'athenes': 'athenes.png', 'thessalonique': 'thessalonique.png', 'heraklion': 'heraklion.png', 'la-canee': 'la-canee.png',
    'bali': 'bali.png', 'jakarta': 'jakarta.png', 'surabaya': 'surabaya.png', 'yogyakarta': 'yogyakarta.png',
}

# Chronicle id → representative hero image (matches RC_IMAGES from country.html)
RC_IMAGES = {
    'chronicle-2056': '/assets/hero-norway.jpg',
    'ameriques-1':    '/assets/hero-panama.jpg',
    'ameriques-2':    '/assets/hero-bahamas.jpg',
    'ameriques-3':    '/assets/hero-bahamas.jpg',
    'australia-guide':'/assets/hero-australia.jpg',
    'raise-children': '/assets/hero-finland.jpg',
    'digital-nomads': '/assets/hero-indonesia.jpg',
    'expats-crypto':  '/assets/hero-uae.jpg',
    'asia-expat-1':   '/assets/hero-thailand.jpg',
    'asia-expat-2':   '/assets/hero-japan.jpg',
    'forgotten-countries': '/assets/hero-montenegro.jpg',
    'africa-expat-1': '/assets/hero-morocco.jpg',
    'africa-expat-2': '/assets/hero-tunisia.jpg',
    'africa-expat-3': '/assets/hero-kenya.jpg',
    'africa-expat-4': '/assets/hero-senegal.jpg',
    'study-erasmus':  '/assets/hero-czech-republic.jpg',
    'study-americas-africa': '/assets/hero-canada.jpg',
    'study-asia-pacific':    '/assets/hero-japan.jpg',
    'study-practical': '/assets/hero-france.jpg',
    'property-abroad': '/assets/hero-portugal.jpg',
    'ready-to-leave':  '/assets/hero-indonesia.jpg',
}

# City pretty name per language (used for thumbnails labels)
CITY_NAME = {
    'paris': {'en':'Paris','fr':'Paris','es':'París'},
    'lyon': {'en':'Lyon','fr':'Lyon','es':'Lyon'},
    'marseille': {'en':'Marseille','fr':'Marseille','es':'Marsella'},
    'nice': {'en':'Nice','fr':'Nice','es':'Niza'},
    'bangkok': {'en':'Bangkok','fr':'Bangkok','es':'Bangkok'},
    'chiang-mai': {'en':'Chiang Mai','fr':'Chiang Mai','es':'Chiang Mai'},
    'phuket': {'en':'Phuket','fr':'Phuket','es':'Phuket'},
    'hua-hin': {'en':'Hua Hin','fr':'Hua Hin','es':'Hua Hin'},
    'sydney': {'en':'Sydney','fr':'Sydney','es':'Sídney'},
    'melbourne': {'en':'Melbourne','fr':'Melbourne','es':'Melbourne'},
    'cairns': {'en':'Cairns','fr':'Cairns','es':'Cairns'},
    'perth': {'en':'Perth','fr':'Perth','es':'Perth'},
    'vancouver': {'en':'Vancouver','fr':'Vancouver','es':'Vancouver'},
    'montreal': {'en':'Montreal','fr':'Montréal','es':'Montreal'},
    'toronto': {'en':'Toronto','fr':'Toronto','es':'Toronto'},
    'calgary': {'en':'Calgary','fr':'Calgary','es':'Calgary'},
    'madrid': {'en':'Madrid','fr':'Madrid','es':'Madrid'},
    'barcelone': {'en':'Barcelona','fr':'Barcelone','es':'Barcelona'},
    'valence': {'en':'Valencia','fr':'Valence','es':'Valencia'},
    'malaga': {'en':'Malaga','fr':'Malaga','es':'Málaga'},
    'sao-paulo': {'en':'São Paulo','fr':'São Paulo','es':'São Paulo'},
    'rio': {'en':'Rio de Janeiro','fr':'Rio de Janeiro','es':'Río de Janeiro'},
    'florianopolis': {'en':'Florianópolis','fr':'Florianópolis','es':'Florianópolis'},
    'salvador': {'en':'Salvador de Bahia','fr':'Salvador de Bahia','es':'Salvador de Bahía'},
    'tokyo': {'en':'Tokyo','fr':'Tokyo','es':'Tokio'},
    'osaka': {'en':'Osaka','fr':'Osaka','es':'Osaka'},
    'fukuoka': {'en':'Fukuoka','fr':'Fukuoka','es':'Fukuoka'},
    'kyoto': {'en':'Kyoto','fr':'Kyoto','es':'Kioto'},
    'mexico-city': {'en':'Mexico City','fr':'Mexico','es':'Ciudad de México'},
    'guadalajara': {'en':'Guadalajara','fr':'Guadalajara','es':'Guadalajara'},
    'monterrey': {'en':'Monterrey','fr':'Monterrey','es':'Monterrey'},
    'cancun': {'en':'Cancún','fr':'Cancún','es':'Cancún'},
    'new-york': {'en':'New York','fr':'New York','es':'Nueva York'},
    'los-angeles': {'en':'Los Angeles','fr':'Los Angeles','es':'Los Ángeles'},
    'miami': {'en':'Miami','fr':'Miami','es':'Miami'},
    'austin': {'en':'Austin','fr':'Austin','es':'Austin'},
    'lisbonne': {'en':'Lisbon','fr':'Lisbonne','es':'Lisboa'},
    'porto': {'en':'Porto','fr':'Porto','es':'Oporto'},
    'faro': {'en':'Faro','fr':'Faro','es':'Faro'},
    'funchal': {'en':'Funchal','fr':'Funchal','es':'Funchal'},
    'athenes': {'en':'Athens','fr':'Athènes','es':'Atenas'},
    'thessalonique': {'en':'Thessaloniki','fr':'Thessalonique','es':'Tesalónica'},
    'heraklion': {'en':'Heraklion','fr':'Héraklion','es':'Heraclión'},
    'la-canee': {'en':'Chania','fr':'La Canée','es':'La Canea'},
    'bali': {'en':'Bali','fr':'Bali','es':'Bali'},
    'jakarta': {'en':'Jakarta','fr':'Jakarta','es':'Yakarta'},
    'surabaya': {'en':'Surabaya','fr':'Surabaya','es':'Surabaya'},
    'yogyakarta': {'en':'Yogyakarta','fr':'Yogyakarta','es':'Yogyakarta'},
}


def find_city_chronicle_url(city_slug, country_slug, lang):
    """Find the actual chronicle file for a city. Returns relative URL or None."""
    pattern = os.path.join(ROOT, 'chronicles/villes', f'chronicle-{city_slug}-*-{lang}.html')
    matches = glob.glob(pattern)
    if matches:
        return '/' + os.path.relpath(matches[0], ROOT).replace(os.sep, '/')
    return None


def find_comparisons(country_slug):
    """Find all static comparisons involving this country."""
    out = []
    base = os.path.join(ROOT, 'compare/static')
    if not os.path.isdir(base): return out
    for d in os.listdir(base):
        if f'-vs-' not in d: continue
        idx = os.path.join(base, d, 'index.html')
        if not os.path.isfile(idx): continue
        a, b = d.split('-vs-', 1)
        if country_slug == a:
            out.append((b, '/compare/static/' + d + '/'))
        elif country_slug == b:
            out.append((a, '/compare/static/' + d + '/'))
    return sorted(out)


def esc(s):
    if s is None: return ''
    return html.escape(str(s), quote=True)


def build_page(slug, lang, base, details, geo, all_country_data):
    L = LABELS[lang]
    name = base.get('name', slug.title())
    iso2 = (geo.get('iso2') or '').upper()
    tz = geo.get('tz', '')
    flag_emoji = iso2_to_flag(iso2)
    seo = base.get('seo', {})
    title = seo.get('title') or f"{name} — {L['cost_table']} | WiggMap"
    description = seo.get('description') or ''
    if not description:
        fields = base.get('fields', {})
        sal = fields.get('avg_salary', {}).get('value', '')
        rent = fields.get('rent_studio', {}).get('value', '')
        if sal or rent:
            description = f"{name}: {L['fld']['avg_salary']} {sal}, {L['fld']['rent_studio']} {rent}. {L['cost_table']} — WiggMap."

    canonical = f'https://wiggmap.com/countries/{slug}-{lang}.html'
    alternates = ''
    for L_code in ['en', 'fr', 'es']:
        alternates += f'<link rel="alternate" hreflang="{L_code}" href="https://wiggmap.com/countries/{slug}-{L_code}.html" />\n  '
    alternates += f'<link rel="alternate" hreflang="x-default" href="https://wiggmap.com/countries/{slug}-en.html" />'

    # ── Snapshot data ──────────────────────────────────────
    snap = (details.get('snapshot') if details else {}) or {}
    capital = snap.get('capital', '')
    population = snap.get('population', '')
    languages = snap.get('languages', '')
    driving = snap.get('driving_side', '')
    cur = (details.get('currency') if details else {}) or {}
    cur_name = cur.get('name', '')
    cur_rate = cur.get('rate', '')
    cur_note = cur.get('note', '')
    cry = (details.get('crypto') if details else {}) or {}
    cry_friendly = cry.get('friendly', '')
    cry_note = cry.get('note', '')
    expat_score = ((details.get('expat_score') if details else {}) or {}).get('value', '')
    expat_max = ((details.get('expat_score') if details else {}) or {}).get('max', 10) or 10
    top_sectors = (((details.get('goDeeper') if details else {}) or {}).get('top_sectors')) or []

    # ── Persona (Icon of the country) ──────────────────────
    persona = None
    if details and details.get('goDeeper'):
        ttk = (details['goDeeper'].get('things_to_know') or {})
        persona = ttk.get('personality') or details['goDeeper'].get('personality')

    # ── WIGG badge ─────────────────────────────────────────
    wigg = base.get('wigg', {})
    wigg_label = wigg.get('label', '')
    wigg_level = wigg.get('level', 'green')

    # ── Cost-of-living table ───────────────────────────────
    fields = base.get('fields', {})
    table_html = ''
    for sec_key, items in SECTIONS:
        rows = ''
        for fkey, icon in items:
            f = fields.get(fkey) or {}
            v = esc(f.get('value', '—'))
            h = esc(f.get('hint', ''))
            label = esc(L['fld'].get(fkey, fkey))
            rows += f'''
        <tr>
          <td class="lbl"><span class="ico">{icon}</span>{label}</td>
          <td class="val">{v}</td>
          <td class="hint">{h}</td>
          <td class="edit"><button class="edit-btn" onclick="openModal('{fkey}')" title="Suggest correction" aria-label="Suggest correction">✎</button></td>
        </tr>'''
        if rows:
            table_html += f'''
      <tbody>
        <tr class="sec"><td colspan="4">{L[sec_key]}</td></tr>{rows}
      </tbody>'''

    # ── Map block (embedded mid-article) ───────────────────
    # Localised map labels
    map_labels = {
        'en': ('Map', 'Light', 'Dark', 'Satellite', 'Loading map…', 'Map unavailable'),
        'fr': ('Carte', 'Clair', 'Sombre', 'Satellite', 'Chargement de la carte…', 'Carte indisponible'),
        'es': ('Mapa', 'Claro', 'Oscuro', 'Satélite', 'Cargando mapa…', 'Mapa no disponible'),
    }[lang]
    map_block_html = f'''
        <div class="map-card">
          <div class="map-header">
            <div class="map-title"><span class="map-flag">{flag_emoji or '🗺️'}</span><span>{esc(name)} — {map_labels[0]}</span></div>
            <div class="map-styles">
              <button type="button" class="map-style-btn active" data-style="light">{map_labels[1]}</button>
              <button type="button" class="map-style-btn" data-style="dark">{map_labels[2]}</button>
              <button type="button" class="map-style-btn" data-style="satellite">{map_labels[3]}</button>
            </div>
          </div>
          <div class="map-container">
            <div id="wigg-country-map"></div>
            <div class="map-loading" id="wiggMapLoading">{map_labels[4]}</div>
          </div>
        </div>'''

    # ── Article (with markdown bold parsed + map at midpoint) ──
    article_text = (details.get('article') if details else '') or ''
    article_body = render_article_body(article_text, map_block_html=map_block_html)
    article_html = ''
    if article_body:
        living_label = {'en': f'Living in {name}', 'fr': f'Vivre à {name}' if name.endswith('e') else f'Vivre au {name}', 'es': f'Vivir en {name}'}[lang]
        score_badge = f'<span class="score-badge"><span class="score-star">⭐</span> {L["expat_score"]}: {expat_score} / {expat_max}</span>' if expat_score else ''
        article_html = f'''
      <div class="article-card">
        <div class="section-head">
          <h2>{esc(living_label)}</h2>
          {score_badge}
        </div>
        <div class="article-body">{article_body}</div>
      </div>'''

    # ── Things to know cards ───────────────────────────────
    things_html = ''
    if details and details.get('goDeeper'):
        gd = details['goDeeper']
        ttk = gd.get('things_to_know') or {}
        cards = ttk.get('cards') or []
        extra = []
        nd = gd.get('national_dish') or {}
        if nd.get('name'):
            extra.append({'title': f"🍽️ {nd.get('name','')}", 'text': nd.get('note','')})
        lgbt = gd.get('lgbt_acceptance') or {}
        if lgbt.get('level'):
            extra.append({'title': f"🏳️‍🌈 LGBT+: {lgbt.get('level','')}", 'text': lgbt.get('note','')})
        all_cards = list(cards) + extra
        if all_cards:
            cards_html = ''
            for c in all_cards:
                t = esc(c.get('title') or c.get('heading') or '')
                txt = esc(c.get('text') or c.get('body') or '')
                cards_html += f'<div class="fact-card"><div class="fact-bar"></div><div class="fact-title">{t}</div><div class="fact-text">{txt}</div></div>'
            mustreads = {'en':'Must-reads','fr':'À lire','es':'Imprescindibles'}[lang]
            things_html = f'''
      <div class="things-section">
        <div class="section-head"><h2>{esc(L["things_to_know"])}</h2><span class="wg-badge">{mustreads}</span></div>
        <div class="facts-grid">{cards_html}</div>
      </div>'''

    # ── City guides carousel (with thumbnails) ────────────
    cities_carousel = ''
    if slug in CITIES_BY_COUNTRY:
        items = []
        for city_slug in CITIES_BY_COUNTRY[slug]:
            url = find_city_chronicle_url(city_slug, slug, lang)
            if not url: continue
            img = CITY_IMAGE.get(city_slug, f'{city_slug}.png')
            cname = CITY_NAME.get(city_slug, {}).get(lang) or city_slug.replace('-', ' ').title()
            items.append(
                f'<a class="rc-vcard" href="{url}">'
                f'<img class="rc-vimg" src="/assetscity/{img}" alt="{esc(cname)}" loading="lazy" '
                f'onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'">'
                f'<div class="rc-vemoji" style="display:none">🏙️</div>'
                f'<div class="rc-vgrad"></div>'
                f'<div class="rc-vbody"><div class="rc-vtitle">{esc(cname)}</div></div>'
                f'</a>'
            )
        if items:
            cities_carousel = f'''
        <div class="rc-box">
          <div class="rc-box-head">
            <h2>{esc(L["cities"])}</h2>
            <div class="rc-nav">
              <button class="rc-nav-btn" data-target="cv-list" data-dir="-1" aria-label="Previous">&#8249;</button>
              <button class="rc-nav-btn" data-target="cv-list" data-dir="1" aria-label="Next">&#8250;</button>
            </div>
          </div>
          <div class="rc-track"><div id="cv-list" class="rc-row">{''.join(items)}</div></div>
        </div>'''

    # ── Related chronicles carousel (with thumbnails) ─────
    chr_carousel = ''
    if slug in CHRONICLES_BY_COUNTRY:
        items = []
        for cid in CHRONICLES_BY_COUNTRY[slug]:
            entry = CHRONICLES_INDEX.get(cid, {}).get(lang) or CHRONICLES_INDEX.get(cid, {}).get('en')
            if not entry: continue
            t, u = entry
            img = RC_IMAGES.get(cid, '/assets/hero-fallback.jpg')
            items.append(
                f'<a class="rc-vcard" href="{u}">'
                f'<img class="rc-vimg" src="{img}" alt="{esc(t)}" loading="lazy" '
                f'onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'">'
                f'<div class="rc-vemoji" style="display:none">📄</div>'
                f'<div class="rc-vgrad"></div>'
                f'<div class="rc-vbody"><div class="rc-vtitle">{esc(t)}</div></div>'
                f'</a>'
            )
        if items:
            chr_carousel = f'''
        <div class="rc-box">
          <div class="rc-box-head">
            <h2>{esc(L["related"])}</h2>
            <div class="rc-nav">
              <button class="rc-nav-btn" data-target="rc-list" data-dir="-1" aria-label="Previous">&#8249;</button>
              <button class="rc-nav-btn" data-target="rc-list" data-dir="1" aria-label="Next">&#8250;</button>
            </div>
          </div>
          <div class="rc-track"><div id="rc-list" class="rc-row">{''.join(items)}</div></div>
        </div>'''

    # ── Comparisons (text list) ────────────────────────────
    cmp_html = ''
    cmps = find_comparisons(slug)
    if cmps:
        items = []
        for other, url in cmps:
            other_name = (all_country_data.get(other, {}).get('name')) or other.replace('-', ' ').title()
            items.append(f'<a class="cmp-pill" href="{url}">{esc(name)} vs {esc(other_name)}</a>')
        cmp_html = f'<section class="cmp-section"><h2>{esc(L["compare"])}</h2><div class="cmp-pills">{"".join(items)}</div></section>'

    # ── Sidebar HTML ───────────────────────────────────────
    snapshot_rows = ''
    if capital:    snapshot_rows += f'<div class="kv"><span>{esc(L["capital"])}</span><b>{esc(capital)}</b></div>'
    if population: snapshot_rows += f'<div class="kv"><span>{esc(L["population"])}</span><b>{esc(population)}</b></div>'
    if languages:  snapshot_rows += f'<div class="kv"><span>{esc(L["languages"])}</span><b>{esc(languages)}</b></div>'
    if cur_name:   snapshot_rows += f'<div class="kv"><span>{esc(L["currency"])}</span><b>{esc(cur_name)}</b></div>'
    if cur_rate:   snapshot_rows += f'<div class="kv kv-sub"><span>Exchange rate</span><b>{esc(cur_rate)}</b></div>'
    if cur_note:   snapshot_rows += f'<div class="kv-note">{esc(cur_note)}</div>'
    if cry_friendly: snapshot_rows += f'<div class="kv"><span>{esc(L["crypto"])}</span><b>{esc(cry_friendly)}</b></div>'
    if cry_note:   snapshot_rows += f'<div class="kv-note">{esc(cry_note)}</div>'
    if driving:    snapshot_rows += f'<div class="kv"><span>{esc(L["driving"])}</span><b>{esc(driving)}</b></div>'

    if top_sectors:
        top_label = {'en':'Top sectors','fr':'Secteurs phares','es':'Sectores principales'}[lang]
        sectors_html = ''.join(f'<div class="sector-pill">{esc(s)}</div>' for s in top_sectors)
        snapshot_rows += f'<div class="sector-block"><div class="sector-head">{top_label}</div><div class="sector-list">{sectors_html}</div></div>'

    persona_html = ''
    if persona and (persona.get('name') or persona.get('story')):
        pname = esc(persona.get('name') or '')
        pera  = esc(persona.get('era') or '')
        pstory = esc(persona.get('story') or persona.get('description') or '')
        icon_label = {'en':'Icon of the country','fr':'Figure du pays','es':'Figura del país'}[lang]
        persona_html = f'''
        <div class="card persona-card">
          <div class="snapshot-title">{icon_label}</div>
          <div class="persona-name">{pname}{f' <small>({pera})</small>' if pera else ''}</div>
          {f'<div class="persona-why">{pstory}</div>' if pstory else ''}
        </div>'''

    # Action buttons labels
    btn_labels = {
        'en': ('Correct data', 'Share', 'Compare'),
        'fr': ('Corriger les données', 'Partager', 'Comparer'),
        'es': ('Corregir datos', 'Compartir', 'Comparar'),
    }[lang]
    local_time_label = {'en':'Local time','fr':'Heure locale','es':'Hora local'}[lang]

    # ── HTML output (2-column rich layout, cream design preserved) ──
    html_out = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-K4MMRD4R');</script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <link rel="canonical" href="{canonical}" />
  {alternates}
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(description)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://wiggmap.com/assets/hero-{slug}.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" href="/assets/favicon.ico" />
  <link rel="manifest" href="/manifest.webmanifest" />
  <meta name="theme-color" content="#1d7f48" />
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"{esc(L["home"])}","item":"https://wiggmap.com/"}},{{"@type":"ListItem","position":2,"name":"{esc(L["countries"])}","item":"https://wiggmap.com/globe.html"}},{{"@type":"ListItem","position":3,"name":"{esc(name)}","item":"{canonical}"}}]}}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":{json.dumps(title, ensure_ascii=False)},"description":{json.dumps(description, ensure_ascii=False)},"author":{{"@type":"Organization","name":"WiggMap"}},"publisher":{{"@type":"Organization","name":"WiggMap","url":"https://wiggmap.com"}},"inLanguage":"{lang}","url":"{canonical}"}}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    :root{{--paper:#fffdf8;--paper-2:#fbf7ee;--ink:#171714;--ink-soft:#54554e;--line:rgba(23,23,20,.10);--line-soft:rgba(23,23,20,.06);--green:#1d7f48;--green-dk:#155f36;--green-light:#e6f4ec;--shadow:0 12px 34px rgba(25,20,12,.06);--radius:14px}}
    html{{scroll-behavior:smooth}}
    body{{font-family:"Inter",system-ui,sans-serif;color:var(--ink);background:linear-gradient(180deg,#f9f5ed 0%,#f3ede3 100%);font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased}}
    a{{color:var(--green);text-decoration:none}}
    a:hover{{text-decoration:underline}}
    .wrap{{max-width:1180px;margin:0 auto;padding:24px 20px 80px}}
    .crumb{{font-size:12px;color:var(--ink-soft);margin-bottom:14px;letter-spacing:.04em}}
    .crumb a{{color:var(--ink-soft)}}
    .country-head{{display:flex;justify-content:space-between;align-items:flex-start;gap:18px;margin-bottom:22px;flex-wrap:wrap}}
    .country-flag{{font-size:42px;line-height:1;margin-bottom:8px}}
    .country-head h1{{font-family:"Fraunces",Georgia,serif;font-size:clamp(34px,5.2vw,52px);font-weight:800;letter-spacing:-.02em;line-height:1.02}}
    .country-head .subtitle{{font-size:14px;color:var(--ink-soft);max-width:64ch;line-height:1.55;margin-top:8px}}
    .head-right{{display:flex;flex-direction:column;align-items:flex-end;gap:8px;flex-shrink:0}}
    .badge{{display:inline-flex;align-items:center;gap:7px;font-size:12px;font-weight:700;padding:7px 13px;border-radius:999px;background:#fff;border:1px solid var(--line)}}
    .badge.green{{background:var(--green-light);color:var(--green-dk);border-color:rgba(29,127,72,.22)}}
    .badge.yellow{{background:#fef9e7;color:#a16207;border-color:rgba(202,138,4,.25)}}
    .badge.red{{background:#fdecec;color:#b91c1c;border-color:rgba(185,28,28,.25)}}
    .badge .dot{{width:8px;height:8px;border-radius:999px;background:currentColor;display:inline-block}}
    .local-time{{font-size:12px;color:var(--ink-soft);font-weight:600}}
    .local-time b{{color:var(--ink);margin-left:5px;font-weight:800}}
    .main-grid{{display:grid;grid-template-columns:300px 1fr;gap:22px;align-items:start}}
    @media(max-width:900px){{.main-grid{{grid-template-columns:1fr}}}}
    .sidebar{{display:flex;flex-direction:column;gap:14px;align-self:start;position:sticky;top:18px}}
    @media(max-width:900px){{.sidebar{{position:static}}}}
    .card{{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden}}
    .hero-img{{width:100%;height:200px;object-fit:cover;display:block;background:#eaddc4}}
    .hero-actions{{padding:12px;display:flex;gap:8px;flex-wrap:wrap}}
    .btn{{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:8px 14px;border-radius:8px;font-family:inherit;font-weight:700;font-size:12.5px;border:1px solid var(--line);background:#fff;color:var(--ink);cursor:pointer;transition:background .14s,border-color .14s}}
    .btn:hover{{background:rgba(0,0,0,.04)}}
    .btn.primary{{background:var(--green);color:#fff;border-color:transparent}}
    .btn.primary:hover{{background:var(--green-dk)}}
    .snapshot-card{{padding:16px}}
    .snapshot-title{{font-family:"Fraunces",Georgia,serif;font-size:14px;font-weight:700;color:var(--ink);margin-bottom:10px;letter-spacing:-.01em}}
    .kv{{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;padding:7px 0;border-bottom:1px solid var(--line-soft);font-size:12.5px}}
    .kv span{{color:var(--ink-soft)}}
    .kv b{{color:var(--ink);font-weight:700;text-align:right;max-width:60%}}
    .kv-sub{{padding-left:10px;font-size:11.5px;opacity:.85}}
    .kv-note{{font-size:11px;color:var(--ink-soft);line-height:1.5;padding:6px 0 8px;font-style:italic;border-bottom:1px solid var(--line-soft)}}
    .sector-block{{padding-top:10px;margin-top:6px;border-top:1px solid var(--line-soft)}}
    .sector-head{{font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);margin-bottom:6px}}
    .sector-list{{display:flex;flex-direction:column;gap:5px}}
    .sector-pill{{background:rgba(29,127,72,.08);border:1px solid rgba(29,127,72,.2);border-radius:7px;padding:5px 10px;font-size:11.5px;font-weight:700;color:var(--green-dk);line-height:1.4}}
    .persona-card{{padding:16px}}
    .persona-name{{font-weight:800;font-size:13px;margin-bottom:6px}}
    .persona-name small{{font-weight:500;opacity:.6;font-size:11px}}
    .persona-why{{font-size:11.5px;color:var(--ink-soft);line-height:1.55;font-style:italic}}
    .right-col{{display:flex;flex-direction:column;gap:18px;min-width:0}}
    .rc-wrapper{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
    @media(max-width:760px){{.rc-wrapper{{grid-template-columns:1fr}}}}
    .rc-box{{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:14px 14px 12px;overflow:hidden}}
    .rc-box-head{{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;gap:6px}}
    .rc-box-head h2{{font-family:"Fraunces",Georgia,serif;font-size:13.5px;font-weight:700;color:var(--ink);letter-spacing:-.01em}}
    .rc-nav{{display:flex;gap:4px}}
    .rc-nav-btn{{width:24px;height:24px;border-radius:6px;border:1px solid var(--line);background:#fff;font-size:13px;cursor:pointer;color:var(--ink-soft);display:flex;align-items:center;justify-content:center;line-height:1;transition:all .14s}}
    .rc-nav-btn:hover{{background:var(--green);color:#fff;border-color:transparent}}
    .rc-nav-btn:disabled{{opacity:.35;cursor:not-allowed}}
    .rc-track{{overflow:hidden}}
    .rc-row{{display:flex;gap:9px;transition:transform .35s ease;will-change:transform}}
    .rc-vcard{{flex-shrink:0;width:130px;height:90px;border-radius:10px;overflow:hidden;position:relative;background:#e9dfca;border:1px solid var(--line);transition:transform .15s,box-shadow .15s}}
    .rc-vcard:hover{{transform:translateY(-2px);box-shadow:0 6px 18px rgba(0,0,0,.10);text-decoration:none}}
    .rc-vimg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
    .rc-vemoji{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:26px;background:linear-gradient(135deg,#ede5d8,#ddd3c4)}}
    .rc-vgrad{{position:absolute;inset:0;background:linear-gradient(to top,rgba(20,15,8,.85) 0%,rgba(20,15,8,.2) 55%,transparent 100%)}}
    .rc-vbody{{position:absolute;left:0;right:0;bottom:0;padding:7px 9px;z-index:2}}
    .rc-vtitle{{font-family:"Fraunces",Georgia,serif;font-size:10.5px;font-weight:700;color:#fff;line-height:1.25;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
    .data-card{{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden}}
    .data-table{{width:100%;border-collapse:collapse;font-size:13px}}
    .data-table .sec td{{background:#f4eedf;font-weight:800;text-transform:uppercase;letter-spacing:.06em;font-size:11px;padding:11px 22px;color:var(--ink-soft);border-top:1px solid var(--line)}}
    .data-table td{{padding:9px 22px;border-bottom:1px solid var(--line-soft);vertical-align:top}}
    .data-table tr:last-child td{{border-bottom:none}}
    .data-table td.lbl{{width:42%;color:var(--ink)}}
    .data-table td.val{{width:25%;font-weight:700}}
    .data-table td.hint{{font-size:11.5px;color:var(--ink-soft)}}
    .data-table td.edit{{width:30px;text-align:right;padding-right:14px}}
    .data-table .ico{{margin-right:8px}}
    .edit-btn{{background:none;border:none;color:var(--ink-soft);cursor:pointer;font-size:13px;opacity:.4;transition:opacity .14s;padding:2px 4px}}
    .edit-btn:hover{{opacity:1;color:var(--green)}}
    .article-card{{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:30px 36px}}
    .section-head{{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid var(--line)}}
    .section-head h2{{font-family:"Fraunces",Georgia,serif;font-size:22px;font-weight:800;letter-spacing:-.01em;color:var(--ink)}}
    .score-badge{{display:inline-flex;align-items:center;gap:5px;background:var(--green-light);border:1px solid rgba(29,127,72,.25);color:var(--green-dk);padding:5px 12px;border-radius:999px;font-size:12px;font-weight:700}}
    .article-body p{{margin-bottom:14px;color:var(--ink-soft);font-size:15px;line-height:1.78}}
    .article-body p:last-child{{margin-bottom:0}}
    .art-tag{{display:inline-block;padding:3px 10px;border-radius:6px;font-weight:700;font-size:13px;margin-bottom:6px;line-height:1.5}}
    .map-card{{margin:22px 0;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--paper-2)}}
    .map-header{{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;background:#fff;border-bottom:1px solid var(--line);gap:8px;flex-wrap:wrap}}
    .map-title{{display:flex;align-items:center;gap:8px;font-weight:700;font-size:13px}}
    .map-flag{{font-size:18px}}
    .map-styles{{display:flex;gap:4px}}
    .map-style-btn{{font-size:11px;font-weight:700;padding:5px 10px;border-radius:6px;border:1px solid var(--line);background:#fff;color:var(--ink-soft);cursor:pointer;transition:all .14s}}
    .map-style-btn:hover{{border-color:var(--green);color:var(--green)}}
    .map-style-btn.active{{background:var(--green);color:#fff;border-color:transparent}}
    .map-container{{position:relative;height:320px}}
    #wigg-country-map{{position:absolute;inset:0}}
    .map-loading{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:var(--paper-2);color:var(--ink-soft);font-size:13px;z-index:10}}
    .map-loading.hidden{{display:none}}
    .things-section{{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:26px 30px}}
    .wg-badge{{display:inline-flex;align-items:center;gap:5px;background:#fef3c7;border:1px solid rgba(202,138,4,.3);color:#92400e;padding:4px 12px;border-radius:999px;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase}}
    .facts-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}}
    .fact-card{{background:var(--paper-2);border:1px solid var(--line);border-radius:10px;padding:16px 18px;position:relative;overflow:hidden}}
    .fact-bar{{position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--green)}}
    .fact-title{{font-weight:800;font-size:13px;margin-bottom:6px;color:var(--ink);padding-left:6px}}
    .fact-text{{font-size:12.5px;color:var(--ink-soft);line-height:1.55;padding-left:6px}}
    .cmp-section{{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:22px 28px}}
    .cmp-section h2{{font-family:"Fraunces",Georgia,serif;font-size:17px;font-weight:700;margin-bottom:12px}}
    .cmp-pills{{display:flex;flex-wrap:wrap;gap:8px}}
    .cmp-pill{{display:inline-block;padding:7px 14px;border-radius:999px;border:1px solid var(--line);background:#fff;font-size:12.5px;font-weight:600;color:var(--ink);transition:all .14s}}
    .cmp-pill:hover{{border-color:var(--green);background:var(--green);color:#fff;text-decoration:none}}
    @media(max-width:640px){{
      .wrap{{padding:18px 14px 60px}}
      .country-head{{flex-direction:column}}
      .head-right{{align-items:flex-start}}
      .data-table td{{padding:9px 14px}}
      .data-table .sec td{{padding:11px 14px}}
      .article-card{{padding:24px 22px}}
      .things-section{{padding:22px 22px}}
      .cmp-section{{padding:20px 22px}}
      .map-container{{height:240px}}
    }}
  </style>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-K4MMRD4R" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<div id="siteHeader"></div>
<script src="/data/header.js"></script>

<main class="wrap">
  <nav class="crumb"><a href="/">{esc(L['home'])}</a> › <a href="/globe.html">{esc(L['countries'])}</a> › {esc(name)}</nav>

  <div class="country-head">
    <div>
      <div class="country-flag">{flag_emoji}</div>
      <h1>{esc(name)}</h1>
      <p class="subtitle">{esc(base.get('subtitle',''))}</p>
    </div>
    <div class="head-right">
      {f'<div class="badge {wigg_level}"><span class="dot"></span>{esc(wigg_label)}</div>' if wigg_label else ''}
      {f'<div class="local-time">{local_time_label} <b id="localTime" data-tz="{esc(tz)}">--:--</b></div>' if tz else ''}
    </div>
  </div>

  <div class="main-grid">
    <aside class="sidebar">
      <div class="card">
        <img class="hero-img" src="/assets/hero-{slug}.jpg" alt="{esc(name)}"
             onerror="this.onerror=null;this.src='/assets/hero-fallback.jpg'" />
        <div class="hero-actions">
          <button class="btn primary" type="button" onclick="openModal('general')">{btn_labels[0]}</button>
          <button class="btn" type="button" id="btnShare">{btn_labels[1]}</button>
          <a class="btn" href="/compare.html?country={slug}">{btn_labels[2]}</a>
        </div>
      </div>

      <div class="card snapshot-card">
        <div class="snapshot-title">{esc(L['snapshot'])}</div>
        {snapshot_rows}
      </div>

      {persona_html}
    </aside>

    <div class="right-col">
      <div class="rc-wrapper">
        {chr_carousel}
        {cities_carousel}
      </div>

      <div class="data-card">
        <table class="data-table">{table_html}
        </table>
      </div>

      {article_html}

      {things_html}

      {cmp_html}
    </div>
  </div>
</main>

<div id="siteFooter"></div>
<script src="/data/footer.js"></script>
<script src="/data/share.js"></script>
<script src="/data/correction-form.js"></script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
(function(){{
  var t = document.getElementById("localTime");
  if(t && t.dataset.tz){{
    function tick(){{
      try{{
        t.textContent = new Intl.DateTimeFormat("en-GB",{{
          timeZone: t.dataset.tz, hour:"2-digit", minute:"2-digit"
        }}).format(new Date());
      }}catch(e){{}}
    }}
    tick(); setInterval(tick, 30000);
  }}
  document.querySelectorAll(".rc-nav-btn").forEach(function(btn){{
    btn.addEventListener("click", function(){{
      var targetId = btn.dataset.target;
      var dir = parseInt(btn.dataset.dir||"1",10);
      var row = document.getElementById(targetId);
      if(!row) return;
      var box = row.parentElement;
      var first = row.querySelector(".rc-vcard");
      if(!first) return;
      var cardW = first.offsetWidth + 9;
      var visible = Math.max(1, Math.floor(box.offsetWidth / cardW));
      var maxOffset = Math.max(0, row.children.length - visible);
      var current = parseInt(row.dataset.offset||"0", 10);
      current = Math.min(maxOffset, Math.max(0, current + dir));
      row.dataset.offset = current;
      row.style.transform = "translateX(-" + (current * cardW) + "px)";
      var nav = btn.parentNode;
      var prev = nav.querySelector('[data-dir="-1"]');
      var next = nav.querySelector('[data-dir="1"]');
      if(prev) prev.disabled = (current === 0);
      if(next) next.disabled = (current >= maxOffset);
    }});
  }});
  var iso2 = {json.dumps(iso2)};
  if(!iso2 || typeof L === "undefined") return;
  var STYLES = {{
    light:     {{ url: "https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png", attr: "&copy; OSM &copy; CARTO" }},
    dark:      {{ url: "https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png",  attr: "&copy; OSM &copy; CARTO" }},
    satellite: {{ url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}", attr: "&copy; Esri" }}
  }};
  var wMap=null, wLayer=null, wMarker=null;
  function initMap(lat, lon){{
    var el = document.getElementById("wigg-country-map");
    if(!el) return;
    if(wMap){{ try{{wMap.remove();}}catch(e){{}} }}
    wMap = L.map("wigg-country-map",{{zoomControl:true}}).setView([lat,lon],5);
    wLayer = L.tileLayer(STYLES.light.url,{{attribution:STYLES.light.attr,maxZoom:18}}).addTo(wMap);
    wMarker = L.marker([lat,lon]).addTo(wMap);
    var loading = document.getElementById("wiggMapLoading");
    if(loading) loading.classList.add("hidden");
  }}
  document.querySelectorAll(".map-style-btn").forEach(function(b){{
    b.addEventListener("click", function(){{
      if(!wMap) return;
      var s = STYLES[b.dataset.style];
      if(!s) return;
      if(wLayer) wMap.removeLayer(wLayer);
      wLayer = L.tileLayer(s.url,{{attribution:s.attr,maxZoom:18}}).addTo(wMap);
      document.querySelectorAll(".map-style-btn").forEach(function(x){{x.classList.remove("active");}});
      b.classList.add("active");
    }});
  }});
  var cacheKey = "wigg_centroid_" + iso2;
  var cached = null;
  try {{ cached = JSON.parse(localStorage.getItem(cacheKey) || "null"); }} catch(e){{}}
  if(cached && cached.lat != null && cached.lon != null){{
    initMap(cached.lat, cached.lon); return;
  }}
  fetch("https://nominatim.openstreetmap.org/search?country=" + encodeURIComponent(iso2) + "&format=json&limit=1")
    .then(function(r){{ return r.json(); }})
    .then(function(d){{
      if(d && d[0]){{
        var coords = {{ lat: +d[0].lat, lon: +d[0].lon }};
        try {{ localStorage.setItem(cacheKey, JSON.stringify(coords)); }} catch(e){{}}
        initMap(coords.lat, coords.lon);
      }} else {{
        var l = document.getElementById("wiggMapLoading");
        if(l) l.textContent = {json.dumps(map_labels[5])};
      }}
    }})
    .catch(function(){{
      var l = document.getElementById("wiggMapLoading");
      if(l) l.textContent = {json.dumps(map_labels[5])};
    }});
}})();
</script>

<form name="wiggmap-corrections" method="POST" data-netlify="true" data-netlify-honeypot="bot-field" hidden>
  <input type="hidden" name="form-name" value="wiggmap-corrections" />
  <p><label>Don\'t fill this out: <input name="bot-field" /></label></p>
  <input name="country" /><input name="field" /><input name="value" /><input name="email" /><textarea name="notes"></textarea>
</form>

<script>if('serviceWorker' in navigator){{navigator.serviceWorker.register('/sw.js').catch(function(){{}})}}</script>
</body>
</html>
"""
    return html_out


def main():
    # Load data
    with open(os.path.join(ROOT, 'data/countries.json'), 'r', encoding='utf-8') as f:
        countries_en = json.load(f)
    with open(os.path.join(ROOT, 'data/countries.fr.json'), 'r', encoding='utf-8') as f:
        countries_fr = json.load(f)
    with open(os.path.join(ROOT, 'data/countries.es.json'), 'r', encoding='utf-8') as f:
        countries_es = json.load(f)
    with open(os.path.join(ROOT, 'data/geo-by-slug.json'), 'r', encoding='utf-8') as f:
        geo_data = json.load(f)

    by_lang = {'en': countries_en, 'fr': countries_fr, 'es': countries_es}
    details_dirs = {
        'en': os.path.join(ROOT, 'data/details'),
        'fr': os.path.join(ROOT, 'data/details-fr'),
        'es': os.path.join(ROOT, 'data/details-es'),
    }

    slugs = sorted(countries_en.keys())
    print(f"Generating pages for {len(slugs)} countries × 3 languages = {len(slugs)*3} files")
    written = 0
    skipped_no_details = 0

    for slug in slugs:
        for lang in ['en', 'fr', 'es']:
            base = by_lang[lang].get(slug)
            if not base:
                continue
            details_path = os.path.join(details_dirs[lang], f'{slug}.json')
            details = None
            if os.path.isfile(details_path):
                try:
                    with open(details_path, 'r', encoding='utf-8') as f:
                        details = json.load(f)
                except Exception as e:
                    print(f"  ! Could not parse {details_path}: {e}")
            else:
                skipped_no_details += 1
            geo = geo_data.get(slug, {}) if isinstance(geo_data, dict) else {}
            page = build_page(slug, lang, base, details, geo, countries_en)
            out_path = os.path.join(OUT_DIR, f'{slug}-{lang}.html')
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(page)
            written += 1

    print(f"\n✓ Written: {written} files")
    print(f"  (countries without deep-dive details: {skipped_no_details})")


if __name__ == '__main__':
    main()
