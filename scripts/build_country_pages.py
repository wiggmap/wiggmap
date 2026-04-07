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


def parse_article(text):
    """Convert the article markdown-ish text to clean HTML paragraphs."""
    if not text: return ''
    text = text.replace('[[MAP]]', '')
    # bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # split into paragraphs by blank lines
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    out = []
    for p in paragraphs:
        # detect heading-like lines starting with an emoji marker
        if re.match(r'^[^\w<]*<strong>([^<]+)</strong>\s*$', p):
            m = re.search(r'<strong>([^<]+)</strong>', p)
            heading = m.group(1) if m else p
            out.append(f'<h2>{heading}</h2>')
        elif p.startswith('🧭') or p.startswith('👥') or p.startswith('🌦️') or p.startswith('🏠') \
             or p.startswith('💼') or p.startswith('🛂') or p.startswith('🏥') or p.startswith('🚗') \
             or p.startswith('🍛') or p.startswith('🔎'):
            # Extract heading from "EMOJI **Title**\nrest..."
            lines = p.split('\n', 1)
            first = lines[0]
            rest = lines[1] if len(lines) > 1 else ''
            m = re.search(r'<strong>([^<]+)</strong>', first)
            if m:
                heading = first.split('<strong>')[0].strip() + ' ' + m.group(1)
                out.append(f'<h2>{heading}</h2>')
                if rest.strip():
                    out.append(f'<p>{rest.strip()}</p>')
            else:
                out.append(f'<p>{p}</p>')
        else:
            out.append(f'<p>{p}</p>')
    return '\n'.join(out)


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
    flag_emoji = iso2_to_flag(geo.get('iso2', ''))
    seo = base.get('seo', {})
    title = seo.get('title') or f"{name} — {L['cost_table']} | WiggMap"
    description = seo.get('description') or ''
    if not description:
        # Build a fallback from key fields
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

    # Snapshot
    snap = details.get('snapshot', {}) if details else {}
    capital = snap.get('capital', '—')
    population = snap.get('population', '—')
    languages = snap.get('languages', '—')
    driving = snap.get('driving_side', '—')
    currency = (details.get('currency', {}) or {}).get('name', '—') if details else '—'
    crypto_friendly = (details.get('crypto', {}) or {}).get('friendly', '—') if details else '—'
    expat_score = (details.get('expat_score', {}) or {}).get('value', '') if details else ''
    expat_max = (details.get('expat_score', {}) or {}).get('max', 10) if details else 10

    # WIGG badge
    wigg = base.get('wigg', {})
    wigg_label = wigg.get('label', '')
    wigg_level = wigg.get('level', 'green')

    # Cost-of-living table
    fields = base.get('fields', {})
    table_html = ''
    for sec_key, items in SECTIONS:
        rows = ''
        for fkey, icon in items:
            f = fields.get(fkey, {}) or {}
            v = esc(f.get('value', '—'))
            h = esc(f.get('hint', ''))
            label = esc(L['fld'].get(fkey, fkey))
            rows += f'''
      <tr>
        <td class="lbl"><span class="ico">{icon}</span>{label}</td>
        <td class="val">{v}</td>
        <td class="hint">{h}</td>
      </tr>'''
        if rows:
            table_html += f'''
    <tbody>
      <tr class="sec"><td colspan="3">{L[sec_key]}</td></tr>{rows}
    </tbody>'''

    # Article
    article_html = parse_article(details.get('article', '')) if details else ''

    # Things to know cards
    things_html = ''
    if details and details.get('goDeeper'):
        gd = details['goDeeper']
        cards = (gd.get('things_to_know', {}) or {}).get('cards', [])
        pers = (gd.get('things_to_know', {}) or {}).get('personality')
        if pers:
            things_html += f'''
      <div class="ttk-card">
        <div class="ttk-title">👤 {esc(pers.get("name",""))} <small>({esc(pers.get("era",""))})</small></div>
        <p>{esc(pers.get("story",""))}</p>
      </div>'''
        for c in cards:
            things_html += f'''
      <div class="ttk-card">
        <div class="ttk-title">{esc(c.get("title",""))}</div>
        <p>{esc(c.get("text",""))}</p>
      </div>'''

    # City guides
    cities_html = ''
    if slug in CITIES_BY_COUNTRY:
        items = []
        for city_slug in CITIES_BY_COUNTRY[slug]:
            url = find_city_chronicle_url(city_slug, slug, lang)
            if url:
                items.append(f'<li><a href="{url}">{city_slug.replace("-"," ").title()}</a></li>')
        if items:
            cities_html = f'<section class="related"><h2>{L["cities"]}</h2><ul class="link-list">{"".join(items)}</ul></section>'

    # Related chronicles
    chr_html = ''
    if slug in CHRONICLES_BY_COUNTRY:
        items = []
        for cid in CHRONICLES_BY_COUNTRY[slug]:
            entry = CHRONICLES_INDEX.get(cid, {}).get(lang) or CHRONICLES_INDEX.get(cid, {}).get('en')
            if entry:
                t, u = entry
                items.append(f'<li><a href="{u}">{esc(t)}</a></li>')
        if items:
            chr_html = f'<section class="related"><h2>{L["related"]}</h2><ul class="link-list">{"".join(items)}</ul></section>'

    # Comparisons
    cmp_html = ''
    cmps = find_comparisons(slug)
    if cmps:
        items = []
        for other, url in cmps:
            other_name = (all_country_data.get(other, {}).get('name')) or other.replace('-', ' ').title()
            items.append(f'<li><a href="{url}">{esc(name)} vs {esc(other_name)}</a></li>')
        cmp_html = f'<section class="related"><h2>{L["compare"]}</h2><ul class="link-list">{"".join(items)}</ul></section>'

    # Build HTML
    html_out = f'''<!DOCTYPE html>
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
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    :root{{--bg:#f6f1e8;--paper:#fffdf8;--ink:#171714;--ink-soft:#54554e;--line:rgba(23,23,20,.10);--green:#1d7f48;--green-dk:#155f36;--shadow:0 12px 34px rgba(25,20,12,.06);--radius:14px}}
    html{{scroll-behavior:smooth}}
    body{{font-family:"Inter",system-ui,sans-serif;color:var(--ink);background:linear-gradient(180deg,#f9f5ed 0%,#f3ede3 100%);font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased}}
    a{{color:var(--green);text-decoration:none}}
    a:hover{{text-decoration:underline}}
    main{{max-width:980px;margin:0 auto;padding:28px 20px 80px}}
    .crumb{{font-size:12px;color:var(--ink-soft);margin-bottom:18px;letter-spacing:.04em}}
    .crumb a{{color:var(--ink-soft)}}
    .hero{{background:var(--paper);border:1px solid var(--line);border-radius:24px;padding:36px 32px;box-shadow:var(--shadow);margin-bottom:24px;position:relative;overflow:hidden}}
    .hero::before{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 88% 18%,rgba(29,127,72,.05),transparent 30%);pointer-events:none}}
    .hero-flag{{font-size:48px;line-height:1;margin-bottom:14px}}
    .hero h1{{font-family:"Fraunces",Georgia,serif;font-size:clamp(36px,6vw,56px);font-weight:800;letter-spacing:-.02em;line-height:1;margin-bottom:10px;position:relative;z-index:1}}
    .hero .subtitle{{font-size:15px;color:var(--ink-soft);max-width:62ch;line-height:1.6;position:relative;z-index:1}}
    .hero-badges{{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px;position:relative;z-index:1}}
    .badge{{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:700;padding:6px 12px;border-radius:999px;background:#fff;border:1px solid var(--line)}}
    .badge.green{{background:#e6f4ec;color:var(--green-dk);border-color:rgba(29,127,72,.2)}}
    .badge.yellow{{background:#fef9e7;color:#a16207;border-color:rgba(202,138,4,.25)}}
    .badge.red{{background:#fdecec;color:#b91c1c;border-color:rgba(185,28,28,.25)}}
    .snapshot{{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:22px 26px;box-shadow:var(--shadow);margin-bottom:24px}}
    .snapshot h2{{font-family:"Fraunces",Georgia,serif;font-size:18px;font-weight:700;margin-bottom:14px}}
    .snap-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px}}
    .snap-item{{font-size:13px}}
    .snap-item strong{{display:block;color:var(--ink-soft);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;margin-bottom:3px}}
    .data-card{{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden;margin-bottom:24px}}
    .data-card h2{{font-family:"Fraunces",Georgia,serif;font-size:18px;font-weight:700;padding:20px 26px 8px}}
    .data-table{{width:100%;border-collapse:collapse;font-size:13px}}
    .data-table .sec td{{background:#f8f4eb;font-weight:800;text-transform:uppercase;letter-spacing:.06em;font-size:11px;padding:10px 26px;color:var(--ink-soft);border-top:1px solid var(--line)}}
    .data-table td{{padding:9px 26px;border-bottom:1px solid var(--line);vertical-align:top}}
    .data-table td.lbl{{width:42%;color:var(--ink)}}
    .data-table td.val{{width:22%;font-weight:700}}
    .data-table td.hint{{font-size:11.5px;color:var(--ink-soft)}}
    .data-table .ico{{margin-right:8px}}
    .article{{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:30px 36px;margin-bottom:24px}}
    .article h2{{font-family:"Fraunces",Georgia,serif;font-size:22px;font-weight:700;margin:24px 0 10px;color:var(--ink)}}
    .article h2:first-child{{margin-top:0}}
    .article p{{margin-bottom:14px;color:var(--ink-soft);font-size:15px;line-height:1.75}}
    .article p strong{{color:var(--ink);font-weight:600}}
    .ttk{{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:26px 30px;margin-bottom:24px}}
    .ttk h2{{font-family:"Fraunces",Georgia,serif;font-size:20px;font-weight:700;margin-bottom:16px}}
    .ttk-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}}
    .ttk-card{{background:#fbf7ee;border:1px solid var(--line);border-radius:10px;padding:16px 18px}}
    .ttk-card .ttk-title{{font-weight:700;font-size:13px;margin-bottom:6px;color:var(--ink)}}
    .ttk-card p{{font-size:12.5px;color:var(--ink-soft);line-height:1.55}}
    .ttk-card small{{font-weight:500;color:var(--ink-soft)}}
    .related{{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:22px 28px;margin-bottom:18px}}
    .related h2{{font-family:"Fraunces",Georgia,serif;font-size:17px;font-weight:700;margin-bottom:12px}}
    .link-list{{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:8px 18px}}
    .link-list li{{font-size:13.5px;line-height:1.5;padding-left:14px;position:relative}}
    .link-list li::before{{content:"›";position:absolute;left:0;color:var(--green)}}
    @media (max-width:640px){{
      main{{padding:20px 14px 60px}}
      .hero{{padding:26px 22px}}
      .data-table td{{padding:9px 16px}}
      .data-table .sec td{{padding:10px 16px}}
      .article{{padding:24px 22px}}
      .ttk{{padding:22px 22px}}
      .related{{padding:20px 22px}}
    }}
  </style>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-K4MMRD4R" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<div id="siteHeader"></div>
<script src="/data/header.js"></script>

<main>
  <nav class="crumb"><a href="/">{esc(L['home'])}</a> › <a href="/globe.html">{esc(L['countries'])}</a> › {esc(name)}</nav>

  <section class="hero">
    <div class="hero-flag">{flag_emoji}</div>
    <h1>{esc(name)}</h1>
    <p class="subtitle">{esc(base.get('subtitle',''))}</p>
    <div class="hero-badges">
      {f'<span class="badge {wigg_level}">{esc(wigg_label)}</span>' if wigg_label else ''}
      {f'<span class="badge">⭐ {L["expat_score"]}: {expat_score} / {expat_max}</span>' if expat_score else ''}
    </div>
  </section>

  <section class="snapshot">
    <h2>{esc(L['snapshot'])}</h2>
    <div class="snap-grid">
      <div class="snap-item"><strong>{esc(L['capital'])}</strong>{esc(capital)}</div>
      <div class="snap-item"><strong>{esc(L['population'])}</strong>{esc(population)}</div>
      <div class="snap-item"><strong>{esc(L['languages'])}</strong>{esc(languages)}</div>
      <div class="snap-item"><strong>{esc(L['driving'])}</strong>{esc(driving)}</div>
      <div class="snap-item"><strong>{esc(L['currency'])}</strong>{esc(currency)}</div>
      <div class="snap-item"><strong>{esc(L['crypto'])}</strong>{esc(crypto_friendly)}</div>
    </div>
  </section>

  <section class="data-card">
    <h2>{esc(L['cost_table'])}</h2>
    <table class="data-table">{table_html}
    </table>
  </section>

  {f'<section class="article"><h2>{esc(L["overview"])}</h2>{article_html}</section>' if article_html else ''}

  {f'<section class="ttk"><h2>{esc(L["things_to_know"])}</h2><div class="ttk-grid">{things_html}</div></section>' if things_html else ''}

  {cities_html}
  {chr_html}
  {cmp_html}

  <p style="text-align:center;margin-top:30px"><a href="/globe.html" style="font-weight:600">{esc(L['see_all_countries'])} →</a></p>
</main>

<div id="siteFooter"></div>
<script src="/data/footer.js"></script>
<script>if('serviceWorker' in navigator){{navigator.serviceWorker.register('/sw.js').catch(function(){{}})}}</script>
</body>
</html>
'''
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
