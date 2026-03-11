#!/usr/bin/env python3
"""Generator v3 — trilingual context paragraphs + details enrichment."""
import json, re, os

with open('data/countries.json') as f:
    RAW = json.load(f)

DETAILS = {}
for slug in ['thailand','vietnam','portugal','spain','france','germany','netherlands',
             'italy','greece','switzerland','georgia','malta','indonesia','malaysia',
             'philippines','australia','canada','new-zealand','singapore',
             'united-arab-emirates','colombia','panama','costa-rica','mexico',
             'brazil','peru']:
    path = f'data/details/{slug}.json'
    if os.path.exists(path):
        with open(path) as f:
            DETAILS[slug] = json.load(f)

def fv(slug, field):
    try: return RAW[slug]['fields'][field]['value']
    except: return ''

def dv(slug, *keys):
    """Get nested value from details."""
    try:
        d = DETAILS[slug]
        for k in keys: d = d[k]
        return d
    except: return None

def parse_float(s):
    s = str(s).replace(',','')
    m = re.search(r'[\d]+(?:\.\d+)?', s)
    return float(m.group()) if m else None

def nice(slug):
    return ' '.join(w.capitalize() for w in slug.replace('-',' ').split())

# ── Localized country names ──────────────────────────────────────────────────
NAME_FR = {
    'thailand':'la Thaïlande','vietnam':'le Vietnam','portugal':'le Portugal',
    'spain':'l\'Espagne','france':'la France','germany':'l\'Allemagne',
    'netherlands':'les Pays-Bas','italy':'l\'Italie','greece':'la Grèce',
    'switzerland':'la Suisse','georgia':'la Géorgie','malta':'Malte',
    'indonesia':'l\'Indonésie','malaysia':'la Malaisie','philippines':'les Philippines',
    'australia':'l\'Australie','canada':'le Canada','new-zealand':'la Nouvelle-Zélande',
    'singapore':'Singapour','united-arab-emirates':'les Émirats arabes unis',
    'colombia':'la Colombie','panama':'le Panama','costa-rica':'le Costa Rica',
    'mexico':'le Mexique','brazil':'le Brésil','peru':'le Pérou',
}
NAME_ES = {
    'thailand':'Tailandia','vietnam':'Vietnam','portugal':'Portugal',
    'spain':'España','france':'Francia','germany':'Alemania',
    'netherlands':'Países Bajos','italy':'Italia','greece':'Grecia',
    'switzerland':'Suiza','georgia':'Georgia','malta':'Malta',
    'indonesia':'Indonesia','malaysia':'Malasia','philippines':'Filipinas',
    'australia':'Australia','canada':'Canadá','new-zealand':'Nueva Zelanda',
    'singapore':'Singapur','united-arab-emirates':'Emiratos Árabes Unidos',
    'colombia':'Colombia','panama':'Panamá','costa-rica':'Costa Rica',
    'mexico':'México','brazil':'Brasil','peru':'Perú',
}
# Short form for "is for" sentences (no article)
NAME_FR_SHORT = {
    'thailand':'La Thaïlande','vietnam':'Le Vietnam','portugal':'Le Portugal',
    'spain':'L\'Espagne','france':'La France','germany':'L\'Allemagne',
    'netherlands':'Les Pays-Bas','italy':'L\'Italie','greece':'La Grèce',
    'switzerland':'La Suisse','georgia':'La Géorgie','malta':'Malte',
    'indonesia':'L\'Indonésie','malaysia':'La Malaisie','philippines':'Les Philippines',
    'australia':'L\'Australie','canada':'Le Canada','new-zealand':'La Nouvelle-Zélande',
    'singapore':'Singapour','united-arab-emirates':'Les Émirats arabes unis',
    'colombia':'La Colombie','panama':'Le Panama','costa-rica':'Le Costa Rica',
    'mexico':'Le Mexique','brazil':'Le Brésil','peru':'Le Pérou',
}

def nfr(slug): return NAME_FR.get(slug, nice(slug))
def nes(slug): return NAME_ES.get(slug, nice(slug))
def nfr_s(slug): return NAME_FR_SHORT.get(slug, nice(slug))

def de_nfr(slug):
    """Returns correct French genitive: 'du Portugal', 'de la France', 'de l\'Espagne', 'des Pays-Bas'."""
    n = NAME_FR.get(slug, nice(slug))
    if n.startswith('le '): return 'du ' + n[3:]
    if n.startswith('les '): return 'des ' + n[4:]
    return 'de ' + n  # "de la ...", "de l'...", bare names

def cap_fr(name):
    """Capitalize first character (for sentence-start country names like 'l\'Espagne' → 'L\'Espagne')."""
    if not name: return name
    return name[0].upper() + name[1:]

def convient_fr(profile_fr):
    """Returns 'convient aux ...' or 'convient à ...' depending on profile string."""
    p = profile_fr.strip()
    if p.startswith('aux ') or p.startswith('les '):
        # "les professionnels..." → "convient aux professionnels..."
        if p.startswith('les '): return 'convient aux ' + p[4:]
        return 'convient ' + p  # already "aux ..."
    return 'convient à ' + p

FLAGS = {
    'australia':'🇦🇺','brazil':'🇧🇷','canada':'🇨🇦','colombia':'🇨🇴',
    'costa-rica':'🇨🇷','france':'🇫🇷','georgia':'🇬🇪','germany':'🇩🇪',
    'greece':'🇬🇷','indonesia':'🇮🇩','italy':'🇮🇹','malaysia':'🇲🇾',
    'malta':'🇲🇹','mexico':'🇲🇽','netherlands':'🇳🇱','new-zealand':'🇳🇿',
    'panama':'🇵🇦','peru':'🇵🇪','philippines':'🇵🇭','portugal':'🇵🇹',
    'singapore':'🇸🇬','spain':'🇪🇸','switzerland':'🇨🇭','thailand':'🇹🇭',
    'united-arab-emirates':'🇦🇪','vietnam':'🇻🇳',
}
def flag(slug): return FLAGS.get(slug,'')

# ── Per-country expat profile (for Para 3) ───────────────────────────────────
PROFILE = {
    'thailand': {
        'en': 'retirees, beach-focused expats and digital nomads who value comfort and an established expat scene',
        'fr': 'aux retraités, aux expatriés axés plages et aux nomades numériques qui valorisent le confort et une communauté expat établie',
        'es': 'jubilados, expatriados centrados en las playas y nómadas digitales que valoran el confort y una escena expat consolidada',
    },
    'vietnam': {
        'en': 'budget-maximisers, English teachers and those drawn to a faster, younger energy — and for anyone excited by world-class street food and one of Asia\'s most dynamic economies',
        'fr': 'aux profils cherchant à optimiser leur budget, aux enseignants d\'anglais et à ceux attirés par une énergie plus jeune et plus dense — et à quiconque est sensible à une cuisine de rue d\'exception et à l\'une des économies les plus dynamiques d\'Asie',
        'es': 'quienes buscan maximizar el presupuesto, profesores de inglés y los atraídos por una energía más joven y densa — y para quienes se entusiasman con una gastronomía callejera excepcional y una de las economías más dinámicas de Asia',
    },
    'portugal': {
        'en': 'those who want European stability: retirees on the D7 visa, digital nomads seeking an EU legal framework, and families prioritising safety and long-term roots',
        'fr': 'ceux qui recherchent la stabilité européenne : retraités sous le visa D7, nomades numériques cherchant un cadre juridique européen, et familles qui privilégient la sécurité et l\'ancrage à long terme',
        'es': 'quienes buscan estabilidad europea: jubilados con visa D7, nómadas digitales que buscan un marco legal europeo, y familias que priorizan la seguridad y las raíces a largo plazo',
    },
    'spain': {
        'en': 'those seeking Southern European warmth with strong infrastructure: retirees, families and remote workers who want sun, culture and EU membership in one package',
        'fr': 'ceux qui recherchent la chaleur de l\'Europe du Sud avec une bonne infrastructure : retraités, familles et télétravailleurs souhaitant soleil, culture et appartenance à l\'UE',
        'es': 'quienes buscan el calor del sur de Europa con buena infraestructura: jubilados, familias y teletrabajadores que quieren sol, cultura y pertenencia a la UE',
    },
    'france': {
        'en': 'those who value cultural depth, healthcare quality and European prestige — accepting higher taxes in exchange for world-class public services',
        'fr': 'ceux qui valorisent la richesse culturelle, la qualité des soins de santé et le prestige européen — acceptant une fiscalité plus lourde en échange de services publics de premier rang',
        'es': 'quienes valoran la profundidad cultural, la calidad sanitaria y el prestigio europeo — aceptando impuestos más altos a cambio de servicios públicos de primer nivel',
    },
    'germany': {
        'en': 'those prioritising economic opportunity, strong institutions and a high standard of living — comfortable navigating a structured, rule-driven society',
        'fr': 'ceux qui privilégient les opportunités économiques, des institutions solides et un niveau de vie élevé — à l\'aise dans une société structurée et réglementée',
        'es': 'quienes priorizan las oportunidades económicas, instituciones sólidas y un alto nivel de vida — cómodos en una sociedad estructurada y orientada a las normas',
    },
    'netherlands': {
        'en': 'internationally mobile professionals, English speakers and those who value cycling culture, tolerance and a highly connected European base',
        'fr': 'les professionnels mobiles à l\'international, les anglophones et ceux qui apprécient la culture du vélo, la tolérance et une base européenne très connectée',
        'es': 'profesionales internacionalmente móviles, angloparlantes y quienes valoran la cultura ciclista, la tolerancia y una base europea muy conectada',
    },
    'italy': {
        'en': 'those who prioritise quality of life, food culture and history over economic dynamism — retirees, remote workers and lifestyle-first expats',
        'fr': 'ceux qui font passer la qualité de vie, la culture culinaire et l\'histoire avant le dynamisme économique — retraités, télétravailleurs et expatriés en quête de style de vie',
        'es': 'quienes priorizan la calidad de vida, la cultura gastronómica y la historia sobre el dinamismo económico — jubilados, teletrabajadores y expatriados que buscan estilo de vida',
    },
    'greece': {
        'en': 'retirees, remote workers and sun-seekers who want Mediterranean lifestyle at a lower price point than Western Europe',
        'fr': 'les retraités, télétravailleurs et amateurs de soleil qui veulent un mode de vie méditerranéen à un coût inférieur à l\'Europe occidentale',
        'es': 'jubilados, teletrabajadores y amantes del sol que quieren un estilo de vida mediterráneo a un coste inferior al de Europa occidental',
    },
    'switzerland': {
        'en': 'high-earning professionals who value political neutrality, safety, natural beauty and proximity to major European markets — and can absorb the high cost of living',
        'fr': 'les professionnels à hauts revenus qui valorisent la neutralité politique, la sécurité, la beauté naturelle et la proximité des grands marchés européens — et peuvent absorber le coût de vie élevé',
        'es': 'profesionales de altos ingresos que valoran la neutralidad política, la seguridad, la belleza natural y la proximidad a los grandes mercados europeos — y pueden absorber el alto coste de vida',
    },
    'georgia': {
        'en': 'digital nomads, crypto holders and budget-conscious expats drawn to low taxes, affordable living and a surprisingly vibrant Tbilisi scene',
        'fr': 'les nomades numériques, détenteurs de crypto et expatriés économes attirés par une fiscalité basse, un coût de vie accessible et une scène de Tbilissi étonnamment vivante',
        'es': 'nómadas digitales, holders de cripto y expatriados conscientes del presupuesto atraídos por los bajos impuestos, el coste de vida asequible y una escena de Tiflis sorprendentemente vibrante',
    },
    'malta': {
        'en': 'those seeking an English-speaking EU base with Mediterranean climate, low crime and straightforward residency pathways',
        'fr': 'ceux qui cherchent une base européenne anglophone avec un climat méditerranéen, une faible criminalité et des voies de résidence accessibles',
        'es': 'quienes buscan una base europea anglófona con clima mediterráneo, baja criminalidad y vías de residencia sencillas',
    },
    'indonesia': {
        'en': 'adventurous expats, surfers, Bali lifestyle-seekers and remote workers drawn to tropical beauty and some of Asia\'s lowest daily costs',
        'fr': 'les expatriés aventuriers, surfeurs, amateurs du style de vie balinais et télétravailleurs attirés par la beauté tropicale et l\'un des coûts quotidiens les plus bas d\'Asie',
        'es': 'expatriados aventureros, surfistas, buscadores del estilo de vida de Bali y teletrabajadores atraídos por la belleza tropical y algunos de los costes diarios más bajos de Asia',
    },
    'malaysia': {
        'en': 'expats seeking an English-speaking, multicultural Asian base with strong infrastructure, affordable living and the popular MM2H long-stay visa',
        'fr': 'les expatriés cherchant une base asiatique anglophone et multiculturelle avec une bonne infrastructure, un coût de vie accessible et le populaire visa MM2H',
        'es': 'expatriados que buscan una base asiática anglófona y multicultural con buena infraestructura, vida asequible y el popular visado MM2H',
    },
    'philippines': {
        'en': 'English-speaking expats, retirees on the SRRV visa and those drawn to island life, warm hospitality and low costs — comfortable with infrastructure gaps',
        'fr': 'les expatriés anglophones, retraités sous le visa SRRV et ceux attirés par la vie insulaire, l\'hospitalité chaleureuse et les faibles coûts — à l\'aise avec les lacunes d\'infrastructure',
        'es': 'expatriados angloparlantes, jubilados con visa SRRV y quienes se sienten atraídos por la vida isleña, la hospitalidad cálida y los bajos costes — cómodos con las carencias de infraestructura',
    },
    'australia': {
        'en': 'those seeking an English-speaking, high-quality-of-life destination with strong institutions, outdoor culture and significant career opportunities',
        'fr': 'ceux qui recherchent une destination anglophone de haute qualité de vie, avec des institutions solides, une culture outdoor et de réelles opportunités de carrière',
        'es': 'quienes buscan un destino anglófono de alta calidad de vida, con instituciones sólidas, cultura al aire libre y significativas oportunidades de carrera',
    },
    'canada': {
        'en': 'those seeking a stable, multicultural English-speaking environment with clear immigration pathways, strong social services and a high standard of living',
        'fr': 'ceux qui cherchent un environnement anglophone stable et multiculturel avec des voies d\'immigration claires, de solides services sociaux et un niveau de vie élevé',
        'es': 'quienes buscan un entorno anglófono estable y multicultural con vías de inmigración claras, sólidos servicios sociales y un alto nivel de vida',
    },
    'new-zealand': {
        'en': 'those who value quality of life, stunning natural environment and a relaxed pace — with English as a first language and clear immigration pathways',
        'fr': 'ceux qui valorisent la qualité de vie, un environnement naturel exceptionnel et un rythme détendu — avec l\'anglais comme langue maternelle et des voies d\'immigration claires',
        'es': 'quienes valoran la calidad de vida, un entorno natural impresionante y un ritmo tranquilo — con el inglés como lengua materna y vías de inmigración claras',
    },
    'singapore': {
        'en': 'high-income professionals seeking Asia\'s most efficient city-state: zero crime, world-class infrastructure and no capital gains tax — at the cost of high living expenses',
        'fr': 'les professionnels à hauts revenus cherchant la cité-État la plus efficace d\'Asie : criminalité quasi nulle, infrastructure de classe mondiale et pas de taxe sur les plus-values — au prix d\'un coût de vie élevé',
        'es': 'profesionales de altos ingresos que buscan la ciudad-estado más eficiente de Asia: criminalidad casi nula, infraestructura de clase mundial y sin impuesto sobre las ganancias de capital — al precio de un alto coste de vida',
    },
    'united-arab-emirates': {
        'en': 'high-earning professionals and entrepreneurs drawn by zero income tax, world-class amenities and a strategic location between East and West',
        'fr': 'les professionnels à hauts revenus et entrepreneurs attirés par l\'absence d\'impôt sur le revenu, des équipements de classe mondiale et un emplacement stratégique entre Est et Ouest',
        'es': 'profesionales de altos ingresos y emprendedores atraídos por el cero impuesto sobre la renta, instalaciones de clase mundial y una ubicación estratégica entre Oriente y Occidente',
    },
    'colombia': {
        'en': 'adventurous expats and digital nomads drawn to vibrant cities like Medellín, a growing startup ecosystem, warm climate and some of the Americas\' lowest costs',
        'fr': 'les expatriés aventuriers et nomades numériques attirés par des villes vibrantes comme Medellín, un écosystème startup en plein essor, un climat chaud et certains des coûts les plus bas des Amériques',
        'es': 'expatriados aventureros y nómadas digitales atraídos por ciudades vibrantes como Medellín, un ecosistema startup en crecimiento, clima cálido y algunos de los costes más bajos de las Américas',
    },
    'panama': {
        'en': 'retirees and remote workers seeking a dollarised economy, tropical climate, tax-friendly residency and easy access to both oceans',
        'fr': 'les retraités et télétravailleurs en quête d\'une économie dollarisée, d\'un climat tropical, d\'une résidence fiscalement avantageuse et d\'un accès facile aux deux océans',
        'es': 'jubilados y teletrabajadores que buscan una economía dolarizada, clima tropical, residencia fiscalmente favorable y acceso fácil a ambos océanos',
    },
    'costa-rica': {
        'en': 'nature lovers, retirees and remote workers who prioritise safety, biodiversity and a stable democracy in a region known for instability',
        'fr': 'les amateurs de nature, retraités et télétravailleurs qui privilégient la sécurité, la biodiversité et une démocratie stable dans une région connue pour son instabilité',
        'es': 'amantes de la naturaleza, jubilados y teletrabajadores que priorizan la seguridad, la biodiversidad y una democracia estable en una región conocida por su inestabilidad',
    },
    'mexico': {
        'en': 'digital nomads, retirees and sun-seekers drawn to rich culture, proximity to the US, accessible residency and highly affordable living in cities like Oaxaca and Mérida',
        'fr': 'les nomades numériques, retraités et amateurs de soleil attirés par la richesse culturelle, la proximité des États-Unis, une résidence accessible et un coût de vie très abordable dans des villes comme Oaxaca et Mérida',
        'es': 'nómadas digitales, jubilados y buscadores de sol atraídos por la rica cultura, la proximidad a EE.UU., la residencia accesible y un coste de vida muy asequible en ciudades como Oaxaca y Mérida',
    },
    'brazil': {
        'en': 'those drawn to extraordinary natural diversity, vibrant culture and Latin American scale — comfortable with urban complexity and a high cost in major cities',
        'fr': 'ceux qu\'attire une extraordinaire diversité naturelle, une culture vibrante et l\'échelle de l\'Amérique latine — à l\'aise avec la complexité urbaine et un coût élevé dans les grandes villes',
        'es': 'quienes se sienten atraídos por una extraordinaria diversidad natural, cultura vibrante y la escala de América Latina — cómodos con la complejidad urbana y un alto coste en las grandes ciudades',
    },
    'peru': {
        'en': 'adventurous expats, history enthusiasts and budget travellers drawn to Andean culture, world-class gastronomy and some of South America\'s lowest daily costs',
        'fr': 'les expatriés aventuriers, passionnés d\'histoire et voyageurs économes attirés par la culture andine, une gastronomie de classe mondiale et certains des coûts quotidiens les plus bas d\'Amérique du Sud',
        'es': 'expatriados aventureros, entusiastas de la historia y viajeros con presupuesto atraídos por la cultura andina, gastronomía de clase mundial y algunos de los costes diarios más bajos de América del Sur',
    },
}

# ── Vibe sentences (fallback for Para 2) ─────────────────────────────────────
REGION_MAP = {
    'portugal':'europe','spain':'europe','france':'europe','germany':'europe',
    'netherlands':'europe','italy':'europe','greece':'europe','switzerland':'europe',
    'georgia':'europe','malta':'europe',
    'thailand':'sea','vietnam':'sea','indonesia':'sea','malaysia':'sea','philippines':'sea',
    'mexico':'americas','colombia':'americas','costa-rica':'americas','panama':'americas',
    'brazil':'americas','peru':'americas',
    'australia':'anglophone','canada':'anglophone','new-zealand':'anglophone',
    'united-arab-emirates':'gulf','singapore':'gulf',
}

VIBE = {
    ('europe','europe'): {
        'en': 'Both countries sit within the EU framework, meaning similar regulatory environments — the gap comes down to cost base, fiscal pressure and lifestyle pace.',
        'fr': 'Les deux pays s\'inscrivent dans le cadre européen, avec des environnements réglementaires similaires — l\'écart tient au coût de base, à la pression fiscale et au rythme de vie.',
        'es': 'Ambos países comparten el marco europeo, con entornos regulatorios similares — la diferencia radica en el coste base, la presión fiscal y el ritmo de vida.',
    },
    ('europe','sea'): {
        'en': 'The Europe vs South-East Asia divide is one of the sharpest in expat circles: rule-of-law stability and social infrastructure in Europe, vs dramatically lower daily costs and warmer weather in Asia.',
        'fr': 'Le fossé Europe / Asie du Sud-Est est l\'un des plus marqués chez les expatriés : stabilité de l\'état de droit et infrastructure sociale en Europe, contre des coûts quotidiens nettement plus bas et un climat plus chaud en Asie.',
        'es': 'La brecha Europa / Sudeste Asiático es una de las más marcadas entre expatriados: estabilidad del estado de derecho e infraestructura social en Europa, frente a costes diarios mucho más bajos y clima más cálido en Asia.',
    },
    ('sea','europe'): {
        'en': 'The Europe vs South-East Asia divide is one of the sharpest in expat circles: rule-of-law stability and social infrastructure in Europe, vs dramatically lower daily costs and warmer weather in Asia.',
        'fr': 'Le fossé Europe / Asie du Sud-Est est l\'un des plus marqués chez les expatriés : stabilité de l\'état de droit et infrastructure sociale en Europe, contre des coûts quotidiens nettement plus bas et un climat plus chaud en Asie.',
        'es': 'La brecha Europa / Sudeste Asiático es una de las más marcadas entre expatriados: estabilidad del estado de derecho e infraestructura social en Europa, frente a costes diarios mucho más bajos y clima más cálido en Asia.',
    },
    ('sea','sea'): {
        'en': 'Both countries share the South-East Asian cost advantage — the differences here are in bureaucratic ease, expat community size and long-term visa options.',
        'fr': 'Les deux pays partagent l\'avantage de coût de l\'Asie du Sud-Est — les différences portent sur la facilité administrative, la taille de la communauté expatriée et les options de visa à long terme.',
        'es': 'Ambos países comparten la ventaja de coste del Sudeste Asiático — las diferencias radican en la facilidad burocrática, el tamaño de la comunidad expat y las opciones de visa a largo plazo.',
    },
    ('americas','americas'): {
        'en': 'Both countries share the Latin American context — similar cost bases and growing digital-nomad communities, with key differences in safety and ease of residency.',
        'fr': 'Les deux pays partagent le contexte latino-américain — bases de coût similaires et communautés de nomades numériques en plein essor, avec des différences clés sur la sécurité et la facilité de résidence.',
        'es': 'Ambos países comparten el contexto latinoamericano — bases de costes similares y comunidades de nómadas digitales en crecimiento, con diferencias clave en seguridad y facilidad de residencia.',
    },
    ('europe','americas'): {
        'en': 'European rule of law and established expat infrastructure vs Latin American affordability and climate — a trade-off familiar to many relocating professionals.',
        'fr': 'L\'état de droit européen et l\'infrastructure expat établie contre l\'accessibilité et le climat d\'Amérique latine — un compromis familier à de nombreux professionnels en mobilité.',
        'es': 'El estado de derecho europeo y la infraestructura expat consolidada frente a la asequibilidad y el clima latinoamericano — un compromiso conocido para muchos profesionales que se reubican.',
    },
    ('americas','europe'): {
        'en': 'European rule of law and established expat infrastructure vs Latin American affordability and climate — a trade-off familiar to many relocating professionals.',
        'fr': 'L\'état de droit européen et l\'infrastructure expat établie contre l\'accessibilité et le climat d\'Amérique latine — un compromis familier à de nombreux professionnels en mobilité.',
        'es': 'El estado de derecho europeo y la infraestructura expat consolidada frente a la asequibilidad y el clima latinoamericano — un compromiso conocido para muchos profesionales que se reubican.',
    },
    ('anglophone','anglophone'): {
        'en': 'Both countries share English as a first language and strong expat infrastructure — the differences here are cost, tax burden and geography.',
        'fr': 'Les deux pays ont l\'anglais comme langue maternelle et une infrastructure expat solide — les différences portent sur le coût, la pression fiscale et la géographie.',
        'es': 'Ambos países tienen el inglés como lengua materna y una sólida infraestructura expat — las diferencias son el coste, la carga fiscal y la geografía.',
    },
    ('anglophone','sea'): {
        'en': 'Anglophone stability and legal predictability vs South-East Asian cost efficiency and warmth — two very different value propositions for the long-term expat.',
        'fr': 'Stabilité anglophone et prévisibilité juridique contre efficacité de coût et chaleur d\'Asie du Sud-Est — deux propositions de valeur très différentes pour l\'expatrié long terme.',
        'es': 'Estabilidad anglófona y previsibilidad legal frente a eficiencia de costes y calidez del Sudeste Asiático — dos propuestas de valor muy distintas para el expatriado a largo plazo.',
    },
    ('sea','anglophone'): {
        'en': 'Anglophone stability and legal predictability vs South-East Asian cost efficiency and warmth — two very different value propositions for the long-term expat.',
        'fr': 'Stabilité anglophone et prévisibilité juridique contre efficacité de coût et chaleur d\'Asie du Sud-Est — deux propositions de valeur très différentes pour l\'expatrié long terme.',
        'es': 'Estabilidad anglófona y previsibilidad legal frente a eficiencia de costes y calidez del Sudeste Asiático — dos propuestas de valor muy distintas para el expatriado a largo plazo.',
    },
    ('gulf','gulf'): {
        'en': 'Both Gulf destinations attract expats with zero income tax and high salaries — the differences lie in lifestyle restrictions, residency pathways and cost of living.',
        'fr': 'Les deux destinations du Golfe attirent les expatriés avec l\'absence d\'impôt sur le revenu et des salaires élevés — les différences portent sur les restrictions de style de vie, les voies de résidence et le coût de la vie.',
        'es': 'Ambos destinos del Golfo atraen a expatriados con cero impuesto sobre la renta y salarios altos — las diferencias radican en las restricciones de estilo de vida, las vías de residencia y el coste de vida.',
    },
    ('gulf','europe'): {
        'en': 'Gulf zero-tax living vs European social infrastructure — a classic expat dilemma between financial optimisation and quality-of-life depth.',
        'fr': 'L\'absence de taxe du Golfe contre l\'infrastructure sociale européenne — un dilemme classique entre optimisation financière et profondeur de la qualité de vie.',
        'es': 'La vida sin impuestos del Golfo frente a la infraestructura social europea — un dilema expat clásico entre optimización financiera y profundidad de calidad de vida.',
    },
    ('europe','gulf'): {
        'en': 'Gulf zero-tax living vs European social infrastructure — a classic expat dilemma between financial optimisation and quality-of-life depth.',
        'fr': 'L\'absence de taxe du Golfe contre l\'infrastructure sociale européenne — un dilemme classique entre optimisation financière et profondeur de la qualité de vie.',
        'es': 'La vida sin impuestos del Golfo frente a la infraestructura social europea — un dilema expat clásico entre optimización financiera y profundidad de calidad de vida.',
    },
    ('americas','sea'): {
        'en': 'Latin American warmth and affordability vs South-East Asian cost efficiency — two budget-friendly worlds with very different cultural textures.',
        'fr': 'Chaleur et accessibilité latino-américaines contre efficacité de coût de l\'Asie du Sud-Est — deux mondes abordables aux textures culturelles très différentes.',
        'es': 'Calidez y asequibilidad latinoamericana frente a la eficiencia de costes del Sudeste Asiático — dos mundos económicos con texturas culturales muy distintas.',
    },
    ('sea','americas'): {
        'en': 'Latin American warmth and affordability vs South-East Asian cost efficiency — two budget-friendly worlds with very different cultural textures.',
        'fr': 'Chaleur et accessibilité latino-américaines contre efficacité de coût de l\'Asie du Sud-Est — deux mondes abordables aux textures culturelles très différentes.',
        'es': 'Calidez y asequibilidad latinoamericana frente a la eficiencia de costes del Sudeste Asiático — dos mundos económicos con texturas culturales muy distintas.',
    },
    ('anglophone','europe'): {
        'en': 'Anglophone ease and familiar culture vs European depth and continental access — the choice often comes down to language, tax structure and lifestyle pace.',
        'fr': 'Facilité anglophone et culture familière contre profondeur européenne et accès continental — le choix dépend souvent de la langue, de la fiscalité et du rythme de vie.',
        'es': 'Facilidad anglófona y cultura familiar frente a profundidad europea y acceso continental — la elección suele depender del idioma, la fiscalidad y el ritmo de vida.',
    },
    ('europe','anglophone'): {
        'en': 'Anglophone ease and familiar culture vs European depth and continental access — the choice often comes down to language, tax structure and lifestyle pace.',
        'fr': 'Facilité anglophone et culture familière contre profondeur européenne et accès continental — le choix dépend souvent de la langue, de la fiscalité et du rythme de vie.',
        'es': 'Facilidad anglófona y cultura familiar frente a profundidad europea y acceso continental — la elección suele depender del idioma, la fiscalidad y el ritmo de vida.',
    },
    ('gulf','sea'): {
        'en': 'Gulf tax efficiency and high salaries vs South-East Asian cost advantage and warmth — two very different routes to financial optimisation abroad.',
        'fr': 'Efficacité fiscale du Golfe et salaires élevés contre avantage de coût et chaleur d\'Asie du Sud-Est — deux voies très différentes vers l\'optimisation financière à l\'étranger.',
        'es': 'Eficiencia fiscal del Golfo y salarios altos frente a la ventaja de coste y calidez del Sudeste Asiático — dos rutas muy distintas hacia la optimización financiera en el extranjero.',
    },
    ('sea','gulf'): {
        'en': 'Gulf tax efficiency and high salaries vs South-East Asian cost advantage and warmth — two very different routes to financial optimisation abroad.',
        'fr': 'Efficacité fiscale du Golfe et salaires élevés contre avantage de coût et chaleur d\'Asie du Sud-Est — deux voies très différentes vers l\'optimisation financière à l\'étranger.',
        'es': 'Eficiencia fiscal del Golfo y salarios altos frente a la ventaja de coste y calidez del Sudeste Asiático — dos rutas muy distintas hacia la optimización financiera en el extranjero.',
    },
    ('gulf','americas'): {
        'en': 'Gulf zero-tax efficiency vs Latin American affordability and culture — two budget-conscious options with radically different lifestyles.',
        'fr': 'Efficacité sans taxe du Golfe contre accessibilité et culture latino-américaines — deux options économiques aux modes de vie radicalement différents.',
        'es': 'Eficiencia sin impuestos del Golfo frente a asequibilidad y cultura latinoamericana — dos opciones económicas con estilos de vida radicalmente distintos.',
    },
    ('americas','gulf'): {
        'en': 'Gulf zero-tax efficiency vs Latin American affordability and culture — two budget-conscious options with radically different lifestyles.',
        'fr': 'Efficacité sans taxe du Golfe contre accessibilité et culture latino-américaines — deux options économiques aux modes de vie radicalement différents.',
        'es': 'Eficiencia sin impuestos del Golfo frente a asequibilidad y cultura latinoamericana — dos opciones económicas con estilos de vida radicalmente distintos.',
    },
    ('anglophone','gulf'): {
        'en': 'Anglophone stability and social infrastructure vs Gulf tax efficiency — the trade-off between public services and take-home pay.',
        'fr': 'Stabilité anglophone et infrastructure sociale contre efficacité fiscale du Golfe — le compromis entre services publics et salaire net.',
        'es': 'Estabilidad anglófona e infraestructura social frente a eficiencia fiscal del Golfe — el compromiso entre servicios públicos y salario neto.',
    },
    ('gulf','anglophone'): {
        'en': 'Anglophone stability and social infrastructure vs Gulf tax efficiency — the trade-off between public services and take-home pay.',
        'fr': 'Stabilité anglophone et infrastructure sociale contre efficacité fiscale du Golfe — le compromis entre services publics et salaire net.',
        'es': 'Estabilidad anglófona e infraestructura social frente a eficiencia fiscal del Golfe — el compromiso entre servicios públicos y salario neto.',
    },
    ('anglophone','americas'): {
        'en': 'Anglophone stability and high wages vs Latin American affordability and warmth — a trade-off between comfort and cost that many expats face.',
        'fr': 'Stabilité anglophone et salaires élevés contre accessibilité et chaleur latino-américaines — un compromis entre confort et coût auquel de nombreux expatriés font face.',
        'es': 'Estabilidad anglófona y altos salarios frente a asequibilidad y calidez latinoamericana — un compromiso entre confort y coste al que se enfrentan muchos expatriados.',
    },
    ('americas','anglophone'): {
        'en': 'Anglophone stability and high wages vs Latin American affordability and warmth — a trade-off between comfort and cost that many expats face.',
        'fr': 'Stabilité anglophone et salaires élevés contre accessibilité et chaleur latino-américaines — un compromis entre confort et coût auquel de nombreux expatriés font face.',
        'es': 'Estabilidad anglófona y altos salarios frente a asequibilidad y calidez latinoamericana — un compromiso entre confort y coste al que se enfrentan muchos expatriados.',
    },
}
VIBE_DEFAULT = {
    'en': 'Both countries offer distinct expat experiences — the right choice depends on your priorities around cost, climate and bureaucratic ease.',
    'fr': 'Les deux pays offrent des expériences d\'expatriation distinctes — le bon choix dépend de vos priorités en matière de coût, de climat et de facilité administrative.',
    'es': 'Ambos países ofrecen experiencias expat distintas — la elección correcta depende de tus prioridades en cuanto a coste, clima y facilidad burocrática.',
}

def get_vibe(s1, s2):
    r1 = REGION_MAP.get(s1,'other'); r2 = REGION_MAP.get(s2,'other')
    return VIBE.get((r1,r2), VIBE_DEFAULT)

# ── Details-enriched Para 2 overrides ────────────────────────────────────────
# For specific pairs, provide a richer Para 2 using details data.
# Key format: frozenset({s1, s2})
PARA2_RICH = {
    frozenset({'thailand','vietnam'}): {
        'en': 'Day-to-day life feels different in ways the numbers don\'t capture. Vietnam\'s 98 million people — nearly 40% more than Thailand\'s 70 million — give cities like Ho Chi Minh City a denser, faster energy. Thailand has a more established expat infrastructure: Chiang Mai is one of Asia\'s most recognised digital nomad hubs. One practical note that rarely makes comparisons: Thailand\'s lèse-majesté law means criticising the monarchy can result in up to 15 years in prison — foreigners are not exempt.',
        'fr': 'Le quotidien diffère d\'une façon que les chiffres ne capturent pas. Les 98 millions d\'habitants du Vietnam — près de 40 % de plus que les 70 millions de la Thaïlande — donnent à des villes comme Ho Chi Minh-Ville une énergie plus dense et plus rapide. La Thaïlande dispose d\'une infrastructure expatriée plus établie : Chiang Mai est l\'un des hubs pour nomades numériques les plus reconnus d\'Asie. Un point pratique rarement mentionné : la loi thaïlandaise de lèse-majesté expose à jusqu\'à 15 ans de prison pour avoir critiqué la monarchie — les étrangers ne sont pas exemptés.',
        'es': 'La vida cotidiana se siente diferente de maneras que los números no capturan. Los 98 millones de habitantes de Vietnam — casi un 40% más que los 70 millones de Tailandia — dan a ciudades como Ho Chi Minh una energía más densa y rápida. Tailandia cuenta con una infraestructura expat más consolidada: Chiang Mai es uno de los hubs de nómadas digitales más reconocidos de Asia. Un punto práctico que raramente aparece en las comparativas: la ley tailandesa de lesa majestad puede conllevar hasta 15 años de prisión por criticar a la monarquía — los extranjeros no están exentos.',
    },
    frozenset({'portugal','thailand'}): {
        'en': 'Safety is a real differentiator. Portugal\'s crime index sits at 30/100 vs 42/100 for Thailand — a gap that shapes daily life, insurance costs and the mental load of living abroad. The contrast runs deeper: Portugal is a stable EU democracy with universal healthcare and a citizenship pathway after 5 years of residence. Thailand, home to 70 million people, has experienced 13 military coups since 1932, and its lèse-majesté law — up to 15 years in prison for criticising the monarchy — applies to foreigners too.',
        'fr': 'La sécurité est un différenciateur réel. L\'indice de criminalité du Portugal s\'établit à 30/100 contre 42/100 pour la Thaïlande — un écart qui influence la vie quotidienne, les assurances et la charge mentale de l\'expatriation. Le contraste va plus loin : le Portugal est une démocratie européenne stable avec une couverture santé universelle et une voie vers la citoyenneté après 5 ans de résidence. La Thaïlande, avec ses 70 millions d\'habitants, a connu 13 coups d\'État militaires depuis 1932, et sa loi de lèse-majesté — jusqu\'à 15 ans de prison pour avoir critiqué la monarchie — s\'applique également aux étrangers.',
        'es': 'La seguridad es un diferenciador real. El índice de criminalidad de Portugal se sitúa en 30/100 frente a 42/100 para Tailandia — una brecha que moldea la vida cotidiana, los costes de seguro y la carga mental de vivir en el extranjero. El contraste va más lejos: Portugal es una democracia europea estable con sanidad universal y una vía hacia la ciudadanía tras 5 años de residencia. Tailandia, con sus 70 millones de habitantes, ha vivido 13 golpes militares desde 1932, y su ley de lesa majestad — hasta 15 años de prisión por criticar a la monarquía — se aplica también a los extranjeros.',
    },
    frozenset({'georgia','portugal'}): {
        'en': 'Beyond the numbers, the two countries offer fundamentally different propositions. Georgia\'s flat 1% tax for small businesses and zero tax on foreign income make it a magnet for digital nomads and crypto holders — Tbilisi has one of Europe\'s fastest-growing expat scenes. Portugal offers a more established path: EU membership, universal healthcare, and citizenship after 5 years of residence.',
        'fr': 'Au-delà des chiffres, les deux pays offrent des propositions fondamentalement différentes. Le taux d\'imposition fixe de 1 % pour les petites entreprises en Géorgie et l\'absence de taxe sur les revenus étrangers en font un aimant pour les nomades numériques et les détenteurs de crypto — Tbilissi est l\'une des scènes expat à la croissance la plus rapide d\'Europe. Le Portugal offre un chemin plus établi : appartenance à l\'UE, couverture santé universelle et citoyenneté après 5 ans de résidence.',
        'es': 'Más allá de los números, los dos países ofrecen propuestas fundamentalmente distintas. El impuesto fijo del 1% para pequeñas empresas en Georgia y la ausencia de impuesto sobre los ingresos extranjeros la convierten en un imán para nómadas digitales y holders de cripto — Tiflis tiene una de las escenas expat de más rápido crecimiento de Europa. Portugal ofrece un camino más consolidado: pertenencia a la UE, sanidad universal y ciudadanía tras 5 años de residencia.',
    },
    frozenset({'malta','portugal'}): {
        'en': 'Both are small, sunny EU states that attract expats for their quality of life and residency options. Malta is English-speaking and offers highly favourable tax programmes for high earners. Portugal has the edge on size, cultural depth and the D7 visa — one of Europe\'s most accessible routes to legal residency for remote workers.',
        'fr': 'Les deux sont de petits États européens ensoleillés qui attirent les expatriés pour leur qualité de vie et leurs options de résidence. Malte est anglophone et propose des régimes fiscaux très avantageux pour les hauts revenus. Le Portugal a l\'avantage par sa taille, sa profondeur culturelle et le visa D7 — l\'une des voies les plus accessibles d\'Europe vers la résidence légale pour les télétravailleurs.',
        'es': 'Ambos son pequeños estados europeos soleados que atraen a expatriados por su calidad de vida y opciones de residencia. Malta es anglófona y ofrece programas fiscales muy favorables para altos ingresos. Portugal tiene ventaja en tamaño, profundidad cultural y el visa D7 — una de las rutas más accesibles de Europa hacia la residencia legal para teletrabajadores.',
    },
    frozenset({'singapore','united-arab-emirates'}): {
        'en': 'Both are zero-income-tax city-states that compete for the world\'s highest-earning expats. Singapore offers Asia\'s most efficient urban environment and a clear path to permanent residence. The UAE — especially Dubai — has become a rival hub, with newer financial incentives, more residential space and a growing tech ecosystem, but with significantly stricter social laws.',
        'fr': 'Les deux sont des cités-États sans impôt sur le revenu qui se disputent les expatriés les mieux rémunérés du monde. Singapour offre l\'environnement urbain le plus efficace d\'Asie et une voie claire vers la résidence permanente. Les Émirats — notamment Dubaï — sont devenus un hub concurrent, avec de nouvelles incitations financières, plus d\'espace résidentiel et un écosystème tech en plein essor, mais avec des lois sociales nettement plus strictes.',
        'es': 'Ambas son ciudades-estado sin impuesto sobre la renta que compiten por los expatriados de mayores ingresos del mundo. Singapur ofrece el entorno urbano más eficiente de Asia y una vía clara hacia la residencia permanente. Los Emiratos — especialmente Dubái — se han convertido en un hub rival, con nuevos incentivos financieros, más espacio residencial y un ecosistema tecnológico en crecimiento, pero con leyes sociales significativamente más estrictas.',
    },
    frozenset({'australia','singapore'}): {
        'en': 'Singapore offers maximum financial efficiency in a compact, ultra-modern city — no capital gains tax, zero income tax on foreign earnings, and world-class connectivity. Australia offers scale, natural environment and a clearer quality-of-life balance — with solid social services and more space, at the cost of higher taxes.',
        'fr': 'Singapour offre une efficacité financière maximale dans une ville compacte et ultra-moderne — pas de taxe sur les plus-values, zéro impôt sur les revenus étrangers, et une connectivité de classe mondiale. L\'Australie offre l\'échelle, l\'environnement naturel et un meilleur équilibre qualité de vie — avec de solides services sociaux et plus d\'espace, au prix d\'une fiscalité plus lourde.',
        'es': 'Singapur ofrece máxima eficiencia financiera en una ciudad compacta y ultramoderna — sin impuesto sobre las ganancias de capital, cero impuesto sobre los ingresos extranjeros y conectividad de clase mundial. Australia ofrece escala, entorno natural y un equilibrio de calidad de vida más claro — con sólidos servicios sociales y más espacio, al precio de impuestos más altos.',
    },
}

# ── Context builder ───────────────────────────────────────────────────────────
def build_context_tri(s1, s2):
    """Returns list of {en, fr, es} paragraph dicts."""
    n1, n2 = nice(s1), nice(s2)
    f1fr, f2fr = nfr(s1), nfr(s2)
    f1es, f2es = nes(s1), nes(s2)
    de1fr, de2fr = de_nfr(s1), de_nfr(s2)
    sv1=fv(s1,'avg_salary'); sv2=fv(s2,'avg_salary')
    rv1=fv(s1,'rent_studio'); rv2=fv(s2,'rent_studio')
    sal1=parse_float(sv1); sal2=parse_float(sv2)
    rent1=parse_float(rv1); rent2=parse_float(rv2)
    paras = []

    # ── Para 1: Economic ──
    p1 = {}
    sal_t = {}; rent_t = {}

    if sal1 and sal2:
        ratio = max(sal1,sal2)/min(sal1,sal2)
        h1, h2 = (n1,n2) if sal1>sal2 else (n2,n1)
        h1fr = f1fr if sal1>sal2 else f2fr
        h2fr = f2fr if sal1>sal2 else f1fr
        deh2fr = de2fr if sal1>sal2 else de1fr
        h1es = f1es if sal1>sal2 else f2es
        h2es = f2es if sal1>sal2 else f1es
        sv_h = sv1 if sal1>sal2 else sv2
        sv_l = sv2 if sal1>sal2 else sv1
        if ratio >= 2.5:
            sal_t = {
                'en': f'Average salaries tell a stark story: {n1} workers earn {sv1}/month on average vs {sv2}/month in {n2} — a {ratio:.1f}× gap that reflects fundamentally different economic tiers.',
                'fr': f'Les salaires racontent une histoire sans équivoque : les travailleurs {de1fr} gagnent en moyenne {sv1}/mois contre {sv2}/mois pour {f2fr} — un écart de {ratio:.1f}× qui reflète des niveaux économiques fondamentalement différents.',
                'es': f'Los salarios cuentan una historia clara: los trabajadores en {f1es} ganan {sv1}/mes de media frente a {sv2}/mes en {f2es} — una brecha de {ratio:.1f}× que refleja niveles económicos fundamentalmente distintos.',
            }
        elif ratio >= 1.5:
            sal_t = {
                'en': f'{h1} pays significantly more: average monthly salary is {sv_h}/month vs {sv_l}/month in {h2} — a gap of {ratio:.1f}×.',
                'fr': f'{cap_fr(h1fr)} offre des salaires nettement plus élevés : le salaire moyen est de {sv_h}/mois contre {sv_l}/mois {deh2fr} — un écart de {ratio:.1f}×.',
                'es': f'{h1es} paga significativamente más: el salario mensual medio es {sv_h} frente a {sv_l} en {h2es} — una brecha de {ratio:.1f}×.',
            }
        else:
            sal_t = {
                'en': f'Average salaries are relatively close: {n1} at {sv1}/month, {n2} at {sv2}/month — so the real differentiator is the cost side of the equation.',
                'fr': f'Les salaires moyens sont relativement proches : {f1fr} à {sv1}/mois, {f2fr} à {sv2}/mois — le vrai différenciateur est donc le coût de la vie.',
                'es': f'Los salarios medios son relativamente similares: {f1es} en {sv1}/mes, {f2es} en {sv2}/mes — el verdadero diferenciador es el lado del coste.',
            }

    if rent1 and rent2:
        ch = n1 if rent1<rent2 else n2
        chfr = f1fr if rent1<rent2 else f2fr
        ches = f1es if rent1<rent2 else f2es
        rent_t = {
            'en': f'Housing costs follow the same direction: a studio in regional {n1} averages {rv1}/month vs {rv2}/month in {n2} — {ch} is the cheaper base for renters.',
            'fr': f'Les coûts de logement suivent la même tendance : un studio en région pour {f1fr} coûte en moyenne {rv1}/mois contre {rv2}/mois pour {f2fr} — {chfr} est la base moins chère pour les locataires.',
            'es': f'Los costes de vivienda siguen la misma dirección: un estudio en {f1es} cuesta {rv1}/mes de media frente a {rv2}/mes en {f2es} — {ches} es la base más económica para los inquilinos.',
        }

    for lang in ['en','fr','es']:
        parts = []
        if sal_t: parts.append(sal_t.get(lang,''))
        if rent_t: parts.append(rent_t.get(lang,''))
        p1[lang] = ' '.join(p for p in parts if p)
    if any(p1.values()):
        paras.append(p1)

    # ── Para 2: Hidden dimension (rich override first, then metric triggers, then vibe) ──
    pair_key = frozenset({s1,s2})
    if pair_key in PARA2_RICH:
        paras.append(PARA2_RICH[pair_key])
    else:
        crime1=parse_float(fv(s1,'crime')); crime2=parse_float(fv(s2,'crime'))
        immig1=parse_float(fv(s1,'immigration')); immig2=parse_float(fv(s2,'immigration'))
        sun1=parse_float(fv(s1,'sun')); sun2=parse_float(fv(s2,'sun'))
        tax1=parse_float(fv(s1,'income_tax')); tax2=parse_float(fv(s2,'income_tax'))
        p2 = None
        if crime1 is not None and crime2 is not None and abs(crime1-crime2)>=10:
            safer=n1 if crime1<crime2 else n2
            riskier=n2 if crime1<crime2 else n1
            safer_fr=f1fr if crime1<crime2 else f2fr
            riskier_fr=f2fr if crime1<crime2 else f1fr
            safer_es=f1es if crime1<crime2 else f2es
            riskier_es=f2es if crime1<crime2 else f1es
            sc=fv(s1,'crime') if crime1<crime2 else fv(s2,'crime')
            rc=fv(s2,'crime') if crime1<crime2 else fv(s1,'crime')
            p2 = {
                'en': f'Safety is a meaningful differentiator here. {safer} scores {sc} on the crime index vs {rc} for {riskier} — a gap that shapes daily life, insurance costs and the mental load of living abroad.',
                'fr': f'La sécurité est un facteur de différenciation important. {cap_fr(safer_fr)} obtient {sc} sur l\'indice de criminalité contre {rc} pour {riskier_fr} — un écart qui influence la vie quotidienne, les assurances et la charge mentale de l\'expatriation.',
                'es': f'La seguridad es un diferenciador significativo aquí. {safer_es} obtiene {sc} en el índice de criminalidad frente a {rc} en {riskier_es} — una brecha que moldea la vida cotidiana, los costes de seguro y la carga mental de vivir en el extranjero.',
            }
        elif immig1 is not None and immig2 is not None and abs(immig1-immig2)>=2:
            easier=n1 if immig1>immig2 else n2
            harder=n2 if immig1>immig2 else n1
            easier_fr=f1fr if immig1>immig2 else f2fr
            harder_fr=f2fr if immig1>immig2 else f1fr
            easier_es=f1es if immig1>immig2 else f2es
            harder_es=f2es if immig1>immig2 else f1es
            ei=fv(s1,'immigration') if immig1>immig2 else fv(s2,'immigration')
            hi=fv(s2,'immigration') if immig1>immig2 else fv(s1,'immigration')
            p2 = {
                'en': f'Bureaucratic ease is a key variable that rarely appears in cost comparisons. {easier} scores {ei} on expat & visa ease vs {hi} for {harder} — a practical difference that matters from day one of relocation.',
                'fr': f'La facilité administrative est une variable clé qui apparaît rarement dans les comparatifs de coûts. {cap_fr(easier_fr)} obtient {ei} sur la facilité d\'installation contre {hi} pour {harder_fr} — une différence concrète qui se fait sentir dès le premier jour.',
                'es': f'La facilidad burocrática es una variable clave que raramente aparece en las comparativas de costes. {easier_es} obtiene {ei} en facilidad de instalación frente a {hi} en {harder_es} — una diferencia práctica que importa desde el primer día.',
            }
        elif sun1 is not None and sun2 is not None and abs(sun1-sun2)>=50:
            sunnier=n1 if sun1>sun2 else n2
            darker=n2 if sun1>sun2 else n1
            sunnier_fr=f1fr if sun1>sun2 else f2fr
            darker_fr=f2fr if sun1>sun2 else f1fr
            sunnier_es=f1es if sun1>sun2 else f2es
            darker_es=f2es if sun1>sun2 else f1es
            sv_s=fv(s1,'sun') if sun1>sun2 else fv(s2,'sun')
            dv_s=fv(s2,'sun') if sun1>sun2 else fv(s1,'sun')
            p2 = {
                'en': f'Climate shapes quality of life in ways that don\'t show up on spreadsheets. {sunnier} averages {sv_s} vs {dv_s} in {darker} — a difference that affects mood, outdoor lifestyle and the texture of everyday living.',
                'fr': f'Le climat influence la qualité de vie d\'une façon que les tableurs ne capturent pas. {cap_fr(sunnier_fr)} enregistre en moyenne {sv_s} contre {dv_s} pour {darker_fr} — une différence qui affecte l\'humeur, le style de vie et la texture du quotidien.',
                'es': f'El clima moldea la calidad de vida de maneras que no aparecen en hojas de cálculo. {sunnier_es} registra {sv_s} de media frente a {dv_s} en {darker_es} — una diferencia que afecta el estado de ánimo, el estilo de vida y la textura del día a día.',
            }
        elif tax1 is not None and tax2 is not None and abs(tax1-tax2)>=7:
            lt_slug=s1 if tax1<tax2 else s2
            ht_slug=s2 if tax1<tax2 else s1
            lt_n=n1 if tax1<tax2 else n2
            ht_n=n2 if tax1<tax2 else n1
            lt_fr=f1fr if tax1<tax2 else f2fr
            ht_fr=f2fr if tax1<tax2 else f1fr
            lt_es=f1es if tax1<tax2 else f2es
            ht_es=f2es if tax1<tax2 else f1es
            lt=fv(lt_slug,'income_tax'); ht=fv(ht_slug,'income_tax')
            p2 = {
                'en': f'Tax burden is where many expats are surprised. {lt_n} sits at {lt} income tax at the mid-bracket vs {ht} in {ht_n} — a gap that compounds quickly for freelancers, remote workers and small business owners.',
                'fr': f'La fiscalité est là où beaucoup d\'expatriés ont de mauvaises surprises. {cap_fr(lt_fr)} affiche {lt} d\'impôt sur le revenu à la tranche médiane contre {ht} pour {ht_fr} — un écart qui s\'accumule vite pour les freelances, travailleurs à distance et petits entrepreneurs.',
                'es': f'La carga fiscal es donde muchos expatriados se sorprenden. {lt_es} tiene un {lt} de impuesto sobre la renta en el tramo medio frente a {ht} en {ht_es} — una brecha que se acumula rápido para freelancers, teletrabajadores y pequeños empresarios.',
            }
        else:
            p2 = get_vibe(s1,s2)
        if p2:
            paras.append(p2)

    # ── Para 3: Profile recommendation ──
    qol={}
    for s in [s1,s2]:
        h=parse_float(fv(s,'happiness')) or 0
        p=parse_float(fv(s,'pp')) or 0
        c=parse_float(fv(s,'crime')) or 50
        qol[s]=h*10+p*0.5-c*0.3
    aff={}
    for s in [s1,s2]:
        r=parse_float(fv(s,'rent_studio')) or 9999
        t=parse_float(fv(s,'income_tax')) or 30
        v=parse_float(fv(s,'vat')) or 20
        aff[s]=-(r+t*20+v*15)

    qw=s1 if qol[s1]>=qol[s2] else s2
    aw=s1 if aff[s1]>=aff[s2] else s2
    qw_n=nice(qw); aw_n=nice(aw)
    qw_fr=nfr_s(qw); aw_fr=nfr_s(aw)
    qw_es=nes(qw); aw_es=nes(aw)
    other_s=s2 if qw==s1 else s1

    prof_qw=PROFILE.get(qw,{}); prof_aw=PROFILE.get(aw,{})
    prof_other=PROFILE.get(other_s,{})

    other_fr=nfr_s(other_s); other_es=nes(other_s)
    qw_p_en=prof_qw.get('en','those who value quality of life and affordability')
    qw_p_fr=prof_qw.get('fr','ceux qui valorisent la qualité de vie')
    qw_p_es=prof_qw.get('es','quienes valoran la calidad de vida')
    ot_p_en=prof_other.get('en','a more specific expat profile')
    ot_p_fr=prof_other.get('fr','un profil expatrié plus spécifique')
    ot_p_es=prof_other.get('es','un perfil expat más específico')
    aw_p_en=prof_aw.get('en','those who put affordability first')
    aw_p_fr=prof_aw.get('fr','ceux qui font de l\'accessibilité leur priorité')
    aw_p_es=prof_aw.get('es','quienes colocan la asequibilidad en primer lugar')
    if qw==aw:
        p3={
            'en': f'{qw_n} is for {qw_p_en}. {nice(other_s)} is for {ot_p_en}.',
            'fr': f'{qw_fr} {convient_fr(qw_p_fr)}. {other_fr} {convient_fr(ot_p_fr)}.',
            'es': f'{qw_es} es para {qw_p_es}. {other_es} es para {ot_p_es}.',
        }
    else:
        p3={
            'en': f'{qw_n} is for {qw_p_en}. {aw_n} is for {aw_p_en}.',
            'fr': f'{qw_fr} {convient_fr(qw_p_fr)}. {aw_fr} {convient_fr(aw_p_fr)}.',
            'es': f'{qw_es} es para {qw_p_es}. {aw_es} es para {aw_p_es}.',
        }
    paras.append(p3)
    return paras

# ── Chronicles ────────────────────────────────────────────────────────────────
CHRON_BY_COUNTRY={
    'portugal':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en','chronicle-2056-best-countries-30-years-en'],
    'spain':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en','chronicle-2056-best-countries-30-years-en'],
    'france':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en','chronicle-2056-best-countries-30-years-en'],
    'germany':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en'],
    'netherlands':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en'],
    'switzerland':['expats-nomads-crypto-2026-en'],
    'italy':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en','chronicle-2056-best-countries-30-years-en'],
    'greece':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en'],
    'georgia':['expats-nomads-crypto-2026-en'],
    'malta':['expats-nomads-crypto-2026-en'],
    'thailand':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en','chronicle-2056-best-countries-30-years-en'],
    'vietnam':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en'],
    'indonesia':['expats-nomads-crypto-2026-en'],
    'malaysia':['expats-nomads-crypto-2026-en'],
    'philippines':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en'],
    'australia':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en','chronicle-2056-best-countries-30-years-en'],
    'canada':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en','chronicle-2056-best-countries-30-years-en'],
    'new-zealand':['expats-nomads-crypto-2026-en','chronicle-raise-children-2026-en','chronicle-2056-best-countries-30-years-en'],
    'singapore':['expats-nomads-crypto-2026-en'],
    'united-arab-emirates':['expats-nomads-crypto-2026-en'],
    'colombia':['expats-nomads-crypto-2026-en','chronicle-ameriques-partie1-en'],
    'panama':['expats-nomads-crypto-2026-en','chronicle-ameriques-partie1-en'],
    'costa-rica':['expats-nomads-crypto-2026-en','chronicle-ameriques-partie1-en'],
    'mexico':['expats-nomads-crypto-2026-en','chronicle-ameriques-partie2-en'],
    'brazil':['expats-nomads-crypto-2026-en'],
    'peru':['expats-nomads-crypto-2026-en','chronicle-ameriques-partie2-en'],
}
CHRON_META={
    'expats-nomads-crypto-2026-en':{'icon':'🌍','title':'Expats, Nomads &amp; Crypto 2026','desc':'Where expats, crypto holders and remote earners keep the most of their money — full country breakdown.'},
    'chronicle-raise-children-2026-en':{'icon':'👨‍👩‍👧','title':'Best Countries to Raise Children 2026','desc':'Education, safety, healthcare and cost — which countries make the best home for the next generation.'},
    'chronicle-2056-best-countries-30-years-en':{'icon':'🔭','title':'Where Will Life Be Best in 2056?','desc':'Strategic analysis of long-term prospects — which countries offer the best quality of life over the next 30 years.'},
    'chronicle-ameriques-partie1-en':{'icon':'🌎','title':'Americas Series · Part 1 — Panama, Costa Rica, Puerto Rico','desc':'Tax havens, pura vida and US-dollar living — expat life in three of the Americas\' most accessible destinations.'},
    'chronicle-ameriques-partie2-en':{'icon':'🌎','title':'Americas Series · Part 2 — Mexico, Colombia, Peru','desc':'Warm climates, growing digital-nomad scenes and dramatically lower costs — expat life in three diverse Americas destinations.'},
}
def pick_chronicles(s1,s2):
    seen=[]
    for slug in [s1,s2]:
        for c in CHRON_BY_COUNTRY.get(slug,[]):
            if c not in seen: seen.append(c)
    return seen[:3]

ALL_PAIRS=[
    'australia-vs-canada','australia-vs-new-zealand','brazil-vs-colombia',
    'colombia-vs-peru','france-vs-germany','france-vs-thailand','georgia-vs-portugal',
    'germany-vs-netherlands','germany-vs-thailand','malta-vs-portugal','mexico-vs-colombia',
    'mexico-vs-costa-rica','panama-vs-colombia','panama-vs-mexico','portugal-vs-germany',
    'portugal-vs-greece','portugal-vs-italy','portugal-vs-panama','portugal-vs-spain',
    'portugal-vs-thailand','portugal-vs-vietnam','singapore-vs-australia','spain-vs-france',
    'spain-vs-italy','spain-vs-thailand','switzerland-vs-germany','switzerland-vs-netherlands',
    'thailand-vs-indonesia','thailand-vs-malaysia','thailand-vs-panama','thailand-vs-philippines',
    'thailand-vs-vietnam','united-arab-emirates-vs-singapore','vietnam-vs-indonesia',
    'vietnam-vs-philippines',
]
def get_also(s1,s2,current):
    res=[]
    for p in ALL_PAIRS:
        if p==current: continue
        a,b=p.split('-vs-')
        if a==s1 or b==s1: res.append(p)
    for p in ALL_PAIRS:
        if p==current or p in res: continue
        a,b=p.split('-vs-')
        if a==s2 or b==s2: res.append(p)
    return res[:4]

# ── i18n script ───────────────────────────────────────────────────────────────
I18N=r"""<script>
(function(){
  var L=(localStorage.getItem('wigg_lang')||'en').toLowerCase();
  if(L!=='fr'&&L!=='es')return;
  var T={
    fr:{sub:'Coût de la vie, salaires &amp; qualité de vie — comparatif 2026',indicator:'Indicateur',avg_salary:'Salaire moyen mensuel',rent_studio:'Loyer studio (régional)',income_tax:'Impôt sur le revenu (tranche médiane)',vat:'TVA',happiness:'Indice de bonheur',pp:'Indice de pouvoir d\'achat',crime:'Indice de criminalité',sun:'Jours de soleil / an',immigration:'Facilité d\'installation',sec_context:'Ce que disent les chiffres',sec_explore:'Explorer chaque pays en détail',profile_sfx:'— profil complet',sec_chron:'Chroniques liées',sec_also:'Comparer aussi',breadcrumb_compare:'Comparer'},
    es:{sub:'Coste de vida, salarios &amp; calidad de vida — comparativa 2026',indicator:'Indicador',avg_salary:'Salario mensual medio',rent_studio:'Alquiler estudio (regional)',income_tax:'Impuesto sobre la renta (tramo medio)',vat:'IVA',happiness:'Índice de felicidad',pp:'Índice de poder adquisitivo',crime:'Índice de criminalidad',sun:'Días de sol / año',immigration:'Facilidad de instalación',sec_context:'Lo que dicen los números',sec_explore:'Explorar cada país en profundidad',profile_sfx:'— perfil completo',sec_chron:'Crónicas relacionadas',sec_also:'Comparar también',breadcrumb_compare:'Comparar'}
  };
  var t=T[L];if(!t)return;
  document.querySelectorAll('[data-i18n]').forEach(function(el){var k=el.getAttribute('data-i18n');if(t[k])el.innerHTML=t[k];});
  document.querySelectorAll('[data-i18n-badge-'+L+']').forEach(function(el){el.textContent=el.getAttribute('data-i18n-badge-'+L);});
  // Swap context paragraphs
  var ctx=document.getElementById('ctx-'+L);
  if(ctx){var box=document.getElementById('ctx-box');if(box){box.innerHTML=ctx.innerHTML;}}
})();
</script>"""

# ── Table ─────────────────────────────────────────────────────────────────────
def badge(en,fr,es):
    return f'<span class="vs-badge" data-i18n-badge-en="{en}" data-i18n-badge-fr="{fr}" data-i18n-badge-es="{es}">{en}</span>'

def build_table(s1,s2):
    rows=[]
    def add(key,len_en,len_fr,len_es,v1,v2,higher=True,ben='higher',bfr='plus élevé',bes='más alto',ben2=None,bfr2=None,bes2=None):
        f1=parse_float(v1); f2=parse_float(v2)
        if f1 is None or f2 is None:
            rows.append(f'<tr><td data-i18n="{key}">{len_en}</td><td>{v1}</td><td>{v2}</td></tr>'); return
        w1=(f1>f2) if higher else (f1<f2)
        eq=(f1==f2)
        b2en=ben2 or ben; b2fr=bfr2 or bfr; b2es=bes2 or bes
        if eq: c1=c2=''; bd1=bd2=''
        elif w1: c1='win';c2='';bd1=badge(ben,bfr,bes);bd2=''
        else: c1='';c2='win';bd1='';bd2=badge(b2en,b2fr,b2es)
        rows.append(f'<tr><td data-i18n="{key}">{len_en}</td><td class="{c1}">{v1}{bd1}</td><td class="{c2}">{v2}{bd2}</td></tr>')
    add('avg_salary','Avg monthly salary','Salaire moyen mensuel','Salario mensual medio',fv(s1,'avg_salary'),fv(s2,'avg_salary'),True,'higher','plus élevé','más alto')
    add('rent_studio','Studio rent (regional)','Loyer studio (régional)','Alquiler estudio (regional)',fv(s1,'rent_studio'),fv(s2,'rent_studio'),False,'cheaper','moins cher','más barato')
    add('income_tax','Income tax (mid-bracket)','Impôt sur le revenu (tranche médiane)','Impuesto sobre la renta (tramo medio)',fv(s1,'income_tax'),fv(s2,'income_tax'),False,'lower','plus bas','más bajo')
    add('vat','VAT','TVA','IVA',fv(s1,'vat'),fv(s2,'vat'),False,'lower','plus bas','más bajo')
    add('happiness','Happiness index','Indice de bonheur','Índice de felicidad',fv(s1,'happiness'),fv(s2,'happiness'),True,'higher','plus élevé','más alto')
    add('pp','Purchasing power index','Indice de pouvoir d\'achat','Índice de poder adquisitivo',fv(s1,'pp'),fv(s2,'pp'),True,'higher','plus élevé','más alto')
    add('crime','Crime index','Indice de criminalité','Índice de criminalidad',fv(s1,'crime'),fv(s2,'crime'),False,'safer','plus sûr','más seguro')
    add('sun','Sun days / year','Jours de soleil / an','Días de sol / año',fv(s1,'sun'),fv(s2,'sun'),True,'more sun','plus ensoleillé','más sol')
    add('immigration','Expat &amp; visa ease','Facilité d\'installation','Facilidad de instalación',fv(s1,'immigration'),fv(s2,'immigration'),True,'easier','plus facile','más fácil')
    return '\n        '.join(rows)

# ── HTML ──────────────────────────────────────────────────────────────────────
def build_html(s1,s2):
    n1,n2=nice(s1),nice(s2)
    f1,f2=flag(s1),flag(s2)
    pair=f'{s1}-vs-{s2}'
    meta_s=(f'{n1}: avg salary {fv(s1,"avg_salary")}/mo, studio {fv(s1,"rent_studio")}/mo, income tax {fv(s1,"income_tax")}. '
            f'{n2}: avg salary {fv(s2,"avg_salary")}/mo, studio {fv(s2,"rent_studio")}/mo, income tax {fv(s2,"income_tax")}. '
            f'Full 2026 comparison of cost of living, salaries, taxes and expat conditions.')
    og_s=(f'{n1}: avg salary {fv(s1,"avg_salary")}/mo, studio {fv(s1,"rent_studio")}/mo. '
          f'{n2}: avg salary {fv(s2,"avg_salary")}/mo, studio {fv(s2,"rent_studio")}/mo. '
          f'Compare taxes, quality of life and expat scores.')
    canonical=f'https://wiggmap.com/compare/static/{pair}/'
    table=build_table(s1,s2)
    ctx_tri=build_context_tri(s1,s2)

    # EN paragraphs (server-rendered)
    ctx_en=''.join(f'<p>{p["en"]}</p>' for p in ctx_tri)
    # FR/ES hidden divs for JS swap
    ctx_fr=''.join(f'<p>{p["fr"]}</p>' for p in ctx_tri)
    ctx_es=''.join(f'<p>{p["es"]}</p>' for p in ctx_tri)

    chrns=pick_chronicles(s1,s2)
    chron_html=''
    for c in chrns:
        m=CHRON_META.get(c,{})
        if not m: continue
        chron_html+=f'      <a class="vs-chronicle-item" href="/chronicles/{c}.html">\n        <span class="chron-icon">{m["icon"]}</span>\n        <div>\n          <span class="chron-title">{m["title"]}</span>\n          <span class="chron-desc">{m["desc"]}</span>\n        </div>\n      </a>\n'

    also=get_also(s1,s2,pair)
    also_html=''
    for p in also:
        a,b=p.split('-vs-')
        also_html+=f'      <a class="vs-also-item" href="/compare/static/{p}/">\n        <span class="also-flags">{flag(a)} {flag(b)}</span>\n        {nice(a)} vs {nice(b)}\n      </a>\n'

    return f'''<!doctype html>
<html lang="en">
<head>
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-K4MMRD4R');</script>
  <link rel="manifest" href="/manifest.webmanifest">
  <meta name="theme-color" content="#22c55e">
  <link rel="apple-touch-icon" href="/assets/icons/icon-192.png">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="/assets/favicon.ico" type="image/x-icon" />
  <title>{n1} vs {n2} — Cost of Living, Salaries &amp; Quality of Life 2026 · WiggMap</title>
  <meta name="description" content="{meta_s}">
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{n1} vs {n2} — Cost of Living &amp; Salaries 2026 · WiggMap">
  <meta property="og:description" content="{og_s}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://wiggmap.com/assets/chronicles.png">
  <meta property="og:url" content="{canonical}">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebPage","name":"{n1} vs {n2} — Cost of Living, Salaries & Quality of Life 2026","description":"{meta_s[:200]}","url":"{canonical}","publisher":{{"@type":"Organization","name":"WiggMap","url":"https://wiggmap.com"}}}}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
    :root{{--green:#059669;--green-light:rgba(5,150,105,.09);--green-mid:rgba(5,150,105,.18);--ink:#14201a;--muted:rgba(20,32,26,.58);--bg:#f6f8f7;--paper:#ffffff;--border:rgba(0,0,0,.09);--radius:16px;--font:'Inter',system-ui,-apple-system,sans-serif;}}
    body{{background:var(--bg);color:var(--ink);font-family:var(--font);font-size:16px;line-height:1.6;}}
    a{{color:var(--green);text-decoration:none;}}
    a:hover{{text-decoration:underline;}}
    .vs-page{{max-width:780px;margin:0 auto;padding:36px 20px 72px;}}
    .vs-breadcrumb{{font-size:13px;color:var(--muted);margin-bottom:28px;}}
    .vs-breadcrumb a{{color:var(--muted);}}
    .vs-breadcrumb a:hover{{color:var(--green);text-decoration:none;}}
    .vs-breadcrumb span{{margin:0 6px;}}
    .vs-hero{{text-align:center;margin-bottom:40px;}}
    .vs-hero .vs-flags{{font-size:40px;display:block;margin-bottom:14px;letter-spacing:8px;}}
    .vs-hero h1{{font-size:clamp(28px,7vw,44px);font-weight:800;letter-spacing:-.6px;margin-bottom:8px;}}
    .vs-hero .vs-sub{{color:var(--muted);font-size:15px;}}
    .vs-card{{background:var(--paper);border-radius:var(--radius);border:1px solid var(--border);overflow:hidden;margin-bottom:32px;box-shadow:0 2px 14px rgba(0,0,0,.05);}}
    .vs-table{{width:100%;border-collapse:collapse;}}
    .vs-table th,.vs-table td{{padding:13px 18px;text-align:left;border-bottom:1px solid var(--border);font-size:15px;vertical-align:middle;}}
    .vs-table tr:last-child th,.vs-table tr:last-child td{{border-bottom:none;}}
    .vs-table thead th{{background:var(--green-light);font-weight:700;font-size:14px;}}
    .vs-table thead th:first-child{{width:36%;color:var(--muted);font-weight:600;}}
    .vs-flag{{font-size:18px;margin-right:6px;}}
    .vs-table td:first-child{{color:var(--muted);font-size:13.5px;font-weight:500;}}
    .vs-table td.win{{font-weight:700;}}
    .vs-table tbody tr:hover{{background:rgba(0,0,0,.014);}}
    .vs-badge{{display:inline-block;font-size:10.5px;font-weight:700;padding:2px 7px;border-radius:99px;background:var(--green-mid);color:var(--green);margin-left:6px;vertical-align:middle;white-space:nowrap;}}
    .vs-section{{margin-bottom:32px;}}
    .vs-section h2{{font-size:17px;font-weight:700;margin-bottom:14px;}}
    .vs-context p{{font-size:15px;line-height:1.78;margin-bottom:12px;}}
    .vs-context p:last-child{{margin-bottom:0;}}
    .vs-links{{display:flex;gap:12px;flex-wrap:wrap;}}
    .vs-link-btn{{display:inline-flex;align-items:center;gap:9px;padding:12px 22px;background:var(--paper);border:1.5px solid var(--border);border-radius:999px;font-weight:600;font-size:14px;color:var(--ink);transition:border-color .15s,background .15s;}}
    .vs-link-btn:hover{{border-color:var(--green);background:var(--green-light);text-decoration:none;}}
    .flag{{font-size:20px;}}
    .vs-chronicles{{display:flex;flex-direction:column;gap:10px;}}
    .vs-chronicle-item{{display:flex;align-items:flex-start;gap:13px;padding:14px 16px;background:var(--paper);border:1px solid var(--border);border-radius:12px;transition:border-color .15s,background .15s;color:var(--ink);}}
    .vs-chronicle-item:hover{{border-color:var(--green);background:var(--green-light);text-decoration:none;}}
    .chron-icon{{font-size:22px;flex-shrink:0;margin-top:1px;}}
    .chron-title{{display:block;font-weight:600;font-size:14px;margin-bottom:2px;color:var(--ink);}}
    .chron-desc{{font-size:13px;color:var(--muted);}}
    .vs-also{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;}}
    .vs-also-item{{display:block;padding:14px 16px;background:var(--paper);border:1px solid var(--border);border-radius:12px;font-weight:600;font-size:14px;color:var(--ink);transition:border-color .15s,background .15s;}}
    .vs-also-item:hover{{border-color:var(--green);background:var(--green-light);text-decoration:none;}}
    .also-flags{{display:block;font-size:20px;margin-bottom:4px;letter-spacing:3px;}}
    .ctx-lang{{display:none;}}
    @media(max-width:540px){{.vs-also{{grid-template-columns:1fr;}}.vs-table th,.vs-table td{{padding:10px 13px;font-size:14px;}}.vs-link-btn{{padding:10px 16px;}}}}
  </style>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-K4MMRD4R" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<div id="siteHeader"></div>
<main class="vs-page">
  <nav class="vs-breadcrumb" aria-label="breadcrumb">
    <a href="/">WiggMap</a><span>›</span>
    <a href="/compare.html" data-i18n="breadcrumb_compare">Compare</a><span>›</span>
    {n1} vs {n2}
  </nav>
  <div class="vs-hero">
    <span class="vs-flags">{f1} {f2}</span>
    <h1>{n1} vs {n2}</h1>
    <p class="vs-sub" data-i18n="sub">Cost of living, salaries &amp; quality of life — 2026 comparison</p>
  </div>
  <div class="vs-card">
    <table class="vs-table">
      <thead>
        <tr>
          <th data-i18n="indicator">Indicator</th>
          <th><span class="vs-flag">{f1}</span> {n1}</th>
          <th><span class="vs-flag">{f2}</span> {n2}</th>
        </tr>
      </thead>
      <tbody>
        {table}
      </tbody>
    </table>
  </div>
  <div class="vs-section vs-context">
    <h2 data-i18n="sec_context">What the numbers tell you</h2>
    <div id="ctx-box">{ctx_en}</div>
    <div id="ctx-fr" class="ctx-lang">{ctx_fr}</div>
    <div id="ctx-es" class="ctx-lang">{ctx_es}</div>
  </div>
  <div class="vs-section">
    <h2 data-i18n="sec_explore">Explore each country in depth</h2>
    <div class="vs-links">
      <a class="vs-link-btn" href="/countries/country.html?country={s1}"><span class="flag">{f1}</span> {n1} <span data-i18n="profile_sfx">— full profile</span></a>
      <a class="vs-link-btn" href="/countries/country.html?country={s2}"><span class="flag">{f2}</span> {n2} <span data-i18n="profile_sfx">— full profile</span></a>
    </div>
  </div>
  <div class="vs-section">
    <h2 data-i18n="sec_chron">Related chronicles</h2>
    <div class="vs-chronicles">
{chron_html}    </div>
  </div>
  <div class="vs-section">
    <h2 data-i18n="sec_also">Compare also</h2>
    <div class="vs-also">
{also_html}    </div>
  </div>
</main>
<div id="siteFooter"></div>
<script src="../../../data/header.js"></script>
<script src="../../../data/footer.js"></script>
{I18N}
</body>
</html>'''

# ── Run ───────────────────────────────────────────────────────────────────────
base='compare/static'
ok=0
for pair in ALL_PAIRS:
    s1,s2=pair.split('-vs-')
    out=os.path.join(base,pair)
    os.makedirs(out,exist_ok=True)
    with open(os.path.join(out,'index.html'),'w',encoding='utf-8') as f:
        f.write(build_html(s1,s2))
    ok+=1
print(f'Done: {ok}/{len(ALL_PAIRS)} pages generated.')
