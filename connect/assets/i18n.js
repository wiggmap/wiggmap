/* ============================================================
   WiggMap Connect — Internationalisation (i18n)
   i18n.js — EN / FR / ES
   ============================================================ */

var WC_I18N = {

  /* =========================================================
     ENGLISH
     ========================================================= */
  en: {
    // ---- Shared navigation ----
    "nav.back_wiggmap":       "← wiggmap.com",
    "nav.back_connect":       "← WiggMap Connect",
    "footer.wiggmap":         "wiggmap.com",
    "footer.connect":         "WiggMap Connect",
    "footer.beta":            "Beta",

    // ---- Landing — Hero ----
    "landing.members_join":   "Join thousands of expats & locals",
    "landing.tagline":        "Every country has its reality. Connect with those who live it.",
    "landing.description":    "Useful stories. Expat, travel and local content. Communication, mutual aid. Welcome to WiggMap, the social network connecting expats, travelers and locals.",

    // ---- Landing — Mirror / WiggZ example ----
    "landing.mirror_name1":       "Lucas, Lyon",
    "landing.mirror_desc1":       "Wants to move to Brazil — looking for a flat in São Paulo",
    "landing.mirror_name2":       "Maria, São Paulo",
    "landing.mirror_desc2":       "Wants to come to France — looking for a neighborhood in Lyon",
    "landing.mirror_label":       "WiggZ*",
    "landing.mirror_conclusion":  "They have exactly what the other is looking for.",
    "landing.mirror_brand":       "That's WiggMap Connect.",

    // ---- Landing — CTA hero ----
    "btn.create_profile_free":    "Create my profile for free",
    "landing.wiggz_note":         "* WiggZ — the symmetric profile to yours: someone who comes from where you want to go, and who wants to go where you're from.",

    // ---- Landing — Country pills ----
    "landing.country_france":     "🇫🇷 France",
    "landing.country_brazil":     "🇧🇷 Brazil",
    "landing.country_portugal":   "🇵🇹 Portugal",
    "landing.country_canada":     "🇨🇦 Canada",
    "landing.country_morocco":    "🇲🇦 Morocco",
    "landing.country_thailand":   "🇹🇭 Thailand",
    "landing.country_australia":  "🇦🇺 Australia",
    "landing.country_germany":    "🇩🇪 Germany",
    "landing.country_japan":      "🇯🇵 Japan",
    "landing.country_spain":      "🇪🇸 Spain",

    // ---- Landing — Why Connect ----
    "landing.why_title":        "Why Connect?",
    "landing.value1_title":     "Real expats + Locals",
    "landing.value1_desc":      "Ask real questions to people who live in the country you're interested in. Housing, taxes, schooling, daily life — no commercial filter.",
    "landing.value2_title":     "WiggSwipe — Find your WiggZ*",
    "landing.value2_desc":      "Our algorithm spots perfect WiggZ* profiles: someone from where you want to go, who wants to go where you're from. Direct exchange, no middleman.",
    "landing.value3_title":     "Real mutual help",
    "landing.value3_desc":      "Here we measure \"people helped\", not followers. Every useful contribution is recognized by the community with a single gesture: \"✦ Helped\".",

    // ---- Landing — Testimonials ----
    "landing.testimonials_title": "They found their WiggZ*",
    "landing.test1_text":   "\"In 3 exchanges with Carlos, I had a flat and a school list for my kids. He was looking for exactly the same kind of neighborhood in Paris. We really helped each other.\"",
    "landing.test1_name":   "Sophie D.",
    "landing.test1_meta":   "Settled in Lisbon for 8 months · ✦ 12 people helped",
    "landing.test2_text":   "\"I had hundreds of questions about German visas. Here I found a Franco-Brazilian lawyer based in Berlin for 5 years. Her answers were worth 3 hours of research.\"",
    "landing.test2_name":   "Rafael M.",
    "landing.test2_meta":   "In transition · Web developer",
    "landing.test3_text":   "\"What convinced me was an 8-episode journal written by a Moroccan who arrived in Montreal last year. Everything was there: the struggles, the surprises, the real good spots.\"",
    "landing.test3_name":   "Amina K.",
    "landing.test3_meta":   "Planner · Departure planned June 2026",

    // ---- Landing — CTA final ----
    "landing.cta_title":      "Ready to find your WiggZ*?",
    "landing.cta_sub_1":      "Create your profile in 5 minutes.",
    "landing.cta_sub_2":      "Free, no ads, no opaque algorithm.",
    "btn.create_profile":     "Create my profile",
    "landing.login_link":     "Already a member? Log in",

    // ---- Onboarding — Navigation ----
    "onboarding.back":        "Back",
    "btn.next":               "Next →",
    "btn.skip":               "Skip",

    // ---- Onboarding — Step 1 ----
    "onboarding.step1.title":               "Where are you from?",
    "onboarding.step1.sub":                 "Your starting point — the place that defines you first.",
    "onboarding.step1.country_label":       "Country of origin *",
    "onboarding.step1.country_placeholder": "Search your country...",
    "onboarding.step1.city_label":          "City of origin *",
    "onboarding.step1.city_placeholder":    "e.g. Lyon, Brussels, Dakar...",

    // ---- Onboarding — Step 2 ----
    "onboarding.step2.title":           "Your situation",
    "onboarding.step2.sub":             "Where are you in your journey? Click your situation.",
    "onboarding.step2.curious_title":   "Curious",
    "onboarding.step2.curious_desc":    "I'm exploring the idea, no decision yet",
    "onboarding.step2.thinking_title":  "Thinking about it",
    "onboarding.step2.thinking_desc":   "I'm seriously considering leaving",
    "onboarding.step2.confirmed_title": "Confirmed project",
    "onboarding.step2.confirmed_desc":  "I've decided, I'm preparing my departure",
    "onboarding.step2.installed_title": "Already settled",
    "onboarding.step2.installed_desc":  "I already live abroad",

    // ---- Onboarding — Step 3 Multi ----
    "onboarding.step3.multi_title":       "Which countries interest you?",
    "onboarding.step3.multi_sub":         "Choose up to 5 countries that attract you. You can refine later.",
    "onboarding.step3.multi_placeholder": "Search a country...",
    "onboarding.step3.multi_skip":        "I'm still looking",

    // ---- Onboarding — Step 3 Single ----
    "onboarding.step3.single_title":              "Where will you settle?",
    "onboarding.step3.single_sub":                "The country and city of your destination.",
    "onboarding.step3.single_country_label":      "Destination country *",
    "onboarding.step3.single_country_placeholder":"Search your target country...",
    "onboarding.step3.single_city_label":         "Target city",
    "onboarding.step3.single_city_placeholder":   "e.g. Lisbon, Berlin, Bangkok...",
    "onboarding.step3.single_quarter_label":      "Planned departure",

    // ---- Onboarding — Step 3 Installed ----
    "onboarding.step3.inst_title":              "Where are you settled?",
    "onboarding.step3.inst_sub":                "The country where you currently live and for how long.",
    "onboarding.step3.inst_country_label":      "Current country *",
    "onboarding.step3.inst_country_placeholder":"Search your current country...",
    "onboarding.step3.inst_city_label":         "City",
    "onboarding.step3.inst_city_placeholder":   "e.g. Porto, Tokyo, Berlin...",
    "onboarding.step3.inst_duration_label":     "How long have you been there?",

    // ---- Onboarding — Step 4 ----
    "onboarding.step4.title":             "What you can contribute",
    "onboarding.step4.sub":               "Your knowledge and experiences help other members.",
    "onboarding.step4.sector_label":      "Your professional sector",
    "onboarding.step4.sector_placeholder":"e.g. Finance, Architecture, Marketing...",
    "onboarding.step4.hv_title":          "✦ High field-value profile",
    "onboarding.step4.hv_desc":           "Members in your sector are among the most sought-after. Your experience feedback can unblock complex situations for other expats.",
    "onboarding.step4.framing":           "Field feedback and lived experiences — not certified professional advice.",
    "onboarding.step4.topics_title":      "What topics can you help with?",
    "onboarding.step4.modes_title":       "How do you prefer to help?",
    "onboarding.step4.mode_messages":     "Private messages",
    "onboarding.step4.mode_messages_sub": "Answer questions directly",
    "onboarding.step4.mode_posts":        "Public posts",
    "onboarding.step4.mode_posts_sub":    "Share experience feedback",
    "onboarding.step4.mode_both":         "Both",
    "onboarding.step4.mode_both_sub":     "Messages + posts as you wish",
    "onboarding.step4.mode_none":         "Just observe",
    "onboarding.step4.mode_none_sub":     "For now, I prefer to learn",
    "onboarding.step4.chip_finance":      "Finance",
    "onboarding.step4.chip_law":          "Law",
    "onboarding.step4.chip_realestate":   "Real estate",
    "onboarding.step4.chip_health":       "Health",
    "onboarding.step4.chip_tech":         "Tech",
    "onboarding.step4.chip_education":    "Education",
    "onboarding.step4.chip_trade":        "Commerce",
    "onboarding.step4.chip_creative":     "Creative",

    // ---- Onboarding — Step 5 ----
    "onboarding.step5.title":            "Who are you?",
    "onboarding.step5.sub":              "Give yourself a presence. Photo and name are enough to start.",
    "onboarding.step5.photo_hint":       "Click to add a photo",
    "onboarding.step5.name_label":       "Display name",
    "onboarding.step5.name_placeholder": "First name or nickname...",
    "onboarding.step5.bio_label":        "Bio",
    "onboarding.step5.bio_chars":        "(160 chars)",
    "onboarding.step5.bio_placeholder":  "e.g. Lyon-based graphic designer heading to Lisbon...",
    "onboarding.step5.langs_label":      "Languages spoken",
    "onboarding.step5.account_label":    "Account type",
    "onboarding.step5.type_individu":    "Individual",
    "onboarding.step5.type_commerce":    "Business",
    "onboarding.step5.type_association": "Association",
    "btn.create_profile_final":          "Create my profile ✦",

    // ---- Onboarding — Exit ----
    "onboarding.exit.title":          "Here's what we found for you",
    "onboarding.exit.stat_suffix":    "members in your community",
    "onboarding.exit.discover":       "Discover my profile →",
    "onboarding.exit.complete_later": "You can complete your profile anytime",

    // ---- Profile — Navigation ----
    "nav.home":    "Home",
    "nav.feed":    "Feed",
    "nav.swipe":   "Swipe",
    "nav.profile": "Profile",
    "profile.edit": "Edit",

    // ---- Profile — Actions ----
    "btn.follow":   "+ Follow",
    "btn.message":  "Message",
    "btn.compat":   "~ Compat.",

    // ---- Profile — Stats ----
    "status.helped":      "helped",
    "status.recognized":  "recognized",
    "status.meetings":    "meetings",
    "status.mirrors":     "WiggZ",

    // ---- Profile — Tabs ----
    "profile.tab_journal": "Journal",
    "profile.tab_reels":   "Reels",
    "profile.tab_posts":   "Posts",
    "profile.tab_infos":   "Infos",
  },

  /* =========================================================
     FRANÇAIS
     ========================================================= */
  fr: {
    "nav.back_wiggmap":       "← wiggmap.com",
    "nav.back_connect":       "← WiggMap Connect",
    "footer.wiggmap":         "wiggmap.com",
    "footer.connect":         "WiggMap Connect",
    "footer.beta":            "Beta",

    "landing.members_join":   "Rejoins des milliers d'expats & locaux",
    "landing.tagline":        "Chaque pays a sa réalité. Connecte-toi avec ceux qui la vivent.",
    "landing.description":    "Des stories utiles. Du contenu expat, voyage, utile. De la communication, de l'entraide. Bienvenue sur WiggMap, le réseau social qui connecte expats, voyageurs et locaux.",

    "landing.mirror_name1":       "Lucas, Lyon",
    "landing.mirror_desc1":       "Veut partir au Brésil — cherche un appart à São Paulo",
    "landing.mirror_name2":       "Maria, São Paulo",
    "landing.mirror_desc2":       "Veut venir en France — cherche un quartier à Lyon",
    "landing.mirror_label":       "WiggZ*",
    "landing.mirror_conclusion":  "Ils ont exactement ce que l'autre cherche.",
    "landing.mirror_brand":       "C'est ça, WiggMap Connect.",

    "btn.create_profile_free":    "Créer mon profil gratuitement",
    "landing.wiggz_note":         "* WiggZ — le profil symétrique au tien : quelqu'un qui vient d'où tu veux aller, et qui veut aller d'où tu viens.",

    "landing.country_france":     "🇫🇷 France",
    "landing.country_brazil":     "🇧🇷 Brésil",
    "landing.country_portugal":   "🇵🇹 Portugal",
    "landing.country_canada":     "🇨🇦 Canada",
    "landing.country_morocco":    "🇲🇦 Maroc",
    "landing.country_thailand":   "🇹🇭 Thaïlande",
    "landing.country_australia":  "🇦🇺 Australie",
    "landing.country_germany":    "🇩🇪 Allemagne",
    "landing.country_japan":      "🇯🇵 Japon",
    "landing.country_spain":      "🇪🇸 Espagne",

    "landing.why_title":        "Pourquoi Connect ?",
    "landing.value1_title":     "Vrais expats + Locaux",
    "landing.value1_desc":      "Pose des vraies questions à des gens qui vivent dans le pays qui t'intéresse. Logement, fiscalité, scolarité, quotidien — sans filtre commercial.",
    "landing.value2_title":     "WiggSwipe — Trouve ton WiggZ*",
    "landing.value2_desc":      "Notre algorithme repère les profils WiggZ* parfaits : quelqu'un qui vient d'où tu veux aller, et qui veut aller d'où tu viens. Échange direct, sans intermédiaire.",
    "landing.value3_title":     "Entraide réelle",
    "landing.value3_desc":      "Ici on mesure les \"personnes aidées\", pas les followers. Chaque contribution utile est reconnue par la communauté avec un seul geste : \"✦ Aidé\".",

    "landing.testimonials_title": "Ils ont trouvé leur WiggZ*",
    "landing.test1_text":   "\"En 3 échanges avec Carlos, j'avais un appart et une liste d'écoles pour mes enfants. Il cherchait exactement le même type de quartier à Paris. On s'est vraiment aidés.\"",
    "landing.test1_name":   "Sophie D.",
    "landing.test1_meta":   "Installée à Lisbonne depuis 8 mois · ✦ 12 personnes aidées",
    "landing.test2_text":   "\"J'avais des centaines de questions sur les visas allemands. Ici j'ai trouvé une avocate franco-brésilienne installée à Berlin depuis 5 ans. Ses réponses valaient 3h de recherches.\"",
    "landing.test2_name":   "Rafael M.",
    "landing.test2_meta":   "En transition · Développeur web",
    "landing.test3_text":   "\"Ce qui m'a décidé, c'est un journal en 8 épisodes écrit par un Marocain arrivé à Montréal l'année dernière. Tout y était : les galères, les surprises, les vraies bonnes adresses.\"",
    "landing.test3_name":   "Amina K.",
    "landing.test3_meta":   "Planificatrice · Départ prévu juin 2026",

    "landing.cta_title":      "Prêt à trouver ton WiggZ* ?",
    "landing.cta_sub_1":      "Crée ton profil en 5 minutes.",
    "landing.cta_sub_2":      "Gratuit, sans publicité, sans algorithme opaque.",
    "btn.create_profile":     "Créer mon profil",
    "landing.login_link":     "Déjà membre ? Se connecter",

    "onboarding.back":        "Retour",
    "btn.next":               "Suivant →",
    "btn.skip":               "Passer",

    "onboarding.step1.title":               "D'où viens-tu ?",
    "onboarding.step1.sub":                 "Ton point de départ — le lieu qui te définit avant tout.",
    "onboarding.step1.country_label":       "Pays d'origine *",
    "onboarding.step1.country_placeholder": "Cherche ton pays...",
    "onboarding.step1.city_label":          "Ville d'origine *",
    "onboarding.step1.city_placeholder":    "ex. Lyon, Bruxelles, Dakar...",

    "onboarding.step2.title":           "Ta situation",
    "onboarding.step2.sub":             "Où en es-tu dans ton parcours ? Clique sur ta situation.",
    "onboarding.step2.curious_title":   "Curieux",
    "onboarding.step2.curious_desc":    "J'explore l'idée, sans décision prise",
    "onboarding.step2.thinking_title":  "En réflexion",
    "onboarding.step2.thinking_desc":   "Je réfléchis sérieusement à partir",
    "onboarding.step2.confirmed_title": "Projet confirmé",
    "onboarding.step2.confirmed_desc":  "J'ai décidé, je prépare mon départ",
    "onboarding.step2.installed_title": "Déjà installé",
    "onboarding.step2.installed_desc":  "Je vis déjà à l'étranger",

    "onboarding.step3.multi_title":       "Quels pays t'intéressent ?",
    "onboarding.step3.multi_sub":         "Choisis jusqu'à 5 pays qui t'attirent. Tu pourras affiner plus tard.",
    "onboarding.step3.multi_placeholder": "Cherche un pays...",
    "onboarding.step3.multi_skip":        "Je cherche encore",

    "onboarding.step3.single_title":              "Où vas-tu t'installer ?",
    "onboarding.step3.single_sub":                "Le pays et la ville de destination de ton projet.",
    "onboarding.step3.single_country_label":      "Pays de destination *",
    "onboarding.step3.single_country_placeholder":"Cherche ton pays cible...",
    "onboarding.step3.single_city_label":         "Ville cible",
    "onboarding.step3.single_city_placeholder":   "ex. Lisbonne, Berlin, Bangkok...",
    "onboarding.step3.single_quarter_label":      "Départ prévu",

    "onboarding.step3.inst_title":              "Où es-tu installé ?",
    "onboarding.step3.inst_sub":                "Le pays où tu vis actuellement et depuis combien de temps.",
    "onboarding.step3.inst_country_label":      "Pays actuel *",
    "onboarding.step3.inst_country_placeholder":"Cherche ton pays actuel...",
    "onboarding.step3.inst_city_label":         "Ville",
    "onboarding.step3.inst_city_placeholder":   "ex. Porto, Tokyo, Berlin...",
    "onboarding.step3.inst_duration_label":     "Depuis combien de temps ?",

    "onboarding.step4.title":             "Ce que tu peux apporter",
    "onboarding.step4.sub":               "Tes connaissances et expériences aident les autres membres.",
    "onboarding.step4.sector_label":      "Ton secteur professionnel",
    "onboarding.step4.sector_placeholder":"ex. Finance, Architecture, Marketing...",
    "onboarding.step4.hv_title":          "✦ Profil haute valeur terrain",
    "onboarding.step4.hv_desc":           "Les membres de ton secteur sont parmi les plus recherchés. Tes retours d'expérience peuvent débloquer des situations complexes pour d'autres expats.",
    "onboarding.step4.framing":           "Retours terrain et expériences vécues — pas des conseils professionnels certifiés.",
    "onboarding.step4.topics_title":      "Sur quels sujets tu peux aider ?",
    "onboarding.step4.modes_title":       "Comment préfères-tu aider ?",
    "onboarding.step4.mode_messages":     "Messages privés",
    "onboarding.step4.mode_messages_sub": "Réponds aux questions en direct",
    "onboarding.step4.mode_posts":        "Posts publics",
    "onboarding.step4.mode_posts_sub":    "Partage des retours d'expérience",
    "onboarding.step4.mode_both":         "Les deux",
    "onboarding.step4.mode_both_sub":     "Messages + posts selon l'envie",
    "onboarding.step4.mode_none":         "Juste observer",
    "onboarding.step4.mode_none_sub":     "Pour l'instant, je préfère apprendre",
    "onboarding.step4.chip_finance":      "Finance",
    "onboarding.step4.chip_law":          "Droit",
    "onboarding.step4.chip_realestate":   "Immobilier",
    "onboarding.step4.chip_health":       "Santé",
    "onboarding.step4.chip_tech":         "Tech",
    "onboarding.step4.chip_education":    "Éducation",
    "onboarding.step4.chip_trade":        "Commerce",
    "onboarding.step4.chip_creative":     "Création",

    "onboarding.step5.title":            "Qui es-tu ?",
    "onboarding.step5.sub":              "Donne-toi une présence. Photo et nom suffisent pour commencer.",
    "onboarding.step5.photo_hint":       "Clique pour ajouter une photo",
    "onboarding.step5.name_label":       "Nom affiché",
    "onboarding.step5.name_placeholder": "Prénom ou pseudo...",
    "onboarding.step5.bio_label":        "Bio",
    "onboarding.step5.bio_chars":        "(160 car.)",
    "onboarding.step5.bio_placeholder":  "ex. Graphiste lyonnais en route pour Lisbonne...",
    "onboarding.step5.langs_label":      "Langues parlées",
    "onboarding.step5.account_label":    "Type de compte",
    "onboarding.step5.type_individu":    "Individu",
    "onboarding.step5.type_commerce":    "Commerce",
    "onboarding.step5.type_association": "Association",
    "btn.create_profile_final":          "Créer mon profil ✦",

    "onboarding.exit.title":          "Voilà ce qu'on a trouvé pour toi",
    "onboarding.exit.stat_suffix":    "membres dans ta communauté",
    "onboarding.exit.discover":       "Découvrir mon profil →",
    "onboarding.exit.complete_later": "Tu pourras compléter ton profil à tout moment",

    "nav.home":    "Accueil",
    "nav.feed":    "Feed",
    "nav.swipe":   "Swipe",
    "nav.profile": "Profil",
    "profile.edit": "Modifier",

    "btn.follow":   "+ Suivre",
    "btn.message":  "Message",
    "btn.compat":   "~ Compat.",

    "status.helped":      "aidés",
    "status.recognized":  "reconnu",
    "status.meetings":    "rencontres",
    "status.mirrors":     "WiggZ",

    "profile.tab_journal": "Journal",
    "profile.tab_reels":   "Reels",
    "profile.tab_posts":   "Posts",
    "profile.tab_infos":   "Infos",
  },

  /* =========================================================
     ESPAÑOL
     ========================================================= */
  es: {
    "nav.back_wiggmap":       "← wiggmap.com",
    "nav.back_connect":       "← WiggMap Connect",
    "footer.wiggmap":         "wiggmap.com",
    "footer.connect":         "WiggMap Connect",
    "footer.beta":            "Beta",

    "landing.members_join":   "Únete a miles de expats y locales",
    "landing.tagline":        "Cada país tiene su realidad. Conéctate con quienes la viven.",
    "landing.description":    "Historias útiles. Contenido expat, viajes y local. Comunicación, ayuda mutua. Bienvenido a WiggMap, la red social que conecta expats, viajeros y locales.",

    "landing.mirror_name1":       "Lucas, Lyon",
    "landing.mirror_desc1":       "Quiere irse a Brasil — busca un piso en São Paulo",
    "landing.mirror_name2":       "Maria, São Paulo",
    "landing.mirror_desc2":       "Quiere ir a Francia — busca un barrio en Lyon",
    "landing.mirror_label":       "WiggZ*",
    "landing.mirror_conclusion":  "Tienen exactamente lo que el otro busca.",
    "landing.mirror_brand":       "Eso es WiggMap Connect.",

    "btn.create_profile_free":    "Crear mi perfil gratis",
    "landing.wiggz_note":         "* WiggZ — el perfil simétrico al tuyo: alguien que viene de donde quieres ir, y que quiere ir de donde vienes.",

    "landing.country_france":     "🇫🇷 Francia",
    "landing.country_brazil":     "🇧🇷 Brasil",
    "landing.country_portugal":   "🇵🇹 Portugal",
    "landing.country_canada":     "🇨🇦 Canadá",
    "landing.country_morocco":    "🇲🇦 Marruecos",
    "landing.country_thailand":   "🇹🇭 Tailandia",
    "landing.country_australia":  "🇦🇺 Australia",
    "landing.country_germany":    "🇩🇪 Alemania",
    "landing.country_japan":      "🇯🇵 Japón",
    "landing.country_spain":      "🇪🇸 España",

    "landing.why_title":        "¿Por qué Connect?",
    "landing.value1_title":     "Expats reales + Locales",
    "landing.value1_desc":      "Haz preguntas reales a personas que viven en el país que te interesa. Vivienda, impuestos, escolaridad, vida diaria — sin filtro comercial.",
    "landing.value2_title":     "WiggSwipe — Encuentra tu WiggZ*",
    "landing.value2_desc":      "Nuestro algoritmo detecta perfiles WiggZ* perfectos: alguien de donde quieres ir, que quiere ir de donde vienes. Intercambio directo, sin intermediarios.",
    "landing.value3_title":     "Ayuda mutua real",
    "landing.value3_desc":      "Aquí medimos \"personas ayudadas\", no seguidores. Cada contribución útil es reconocida por la comunidad con un solo gesto: \"✦ Ayudé\".",

    "landing.testimonials_title": "Encontraron su WiggZ*",
    "landing.test1_text":   "\"En 3 intercambios con Carlos, tenía un piso y una lista de escuelas para mis hijos. Él buscaba exactamente el mismo tipo de barrio en París. Nos ayudamos de verdad.\"",
    "landing.test1_name":   "Sophie D.",
    "landing.test1_meta":   "Instalada en Lisboa desde hace 8 meses · ✦ 12 personas ayudadas",
    "landing.test2_text":   "\"Tenía cientos de preguntas sobre visados alemanes. Aquí encontré una abogada franco-brasileña instalada en Berlín desde hace 5 años. Sus respuestas valían 3 horas de investigación.\"",
    "landing.test2_name":   "Rafael M.",
    "landing.test2_meta":   "En transición · Desarrollador web",
    "landing.test3_text":   "\"Lo que me decidió fue un diario de 8 episodios escrito por un marroquí que llegó a Montreal el año pasado. Todo estaba ahí: las dificultades, las sorpresas, las verdaderas buenas direcciones.\"",
    "landing.test3_name":   "Amina K.",
    "landing.test3_meta":   "Planificadora · Salida prevista junio 2026",

    "landing.cta_title":      "¿Listo para encontrar tu WiggZ*?",
    "landing.cta_sub_1":      "Crea tu perfil en 5 minutos.",
    "landing.cta_sub_2":      "Gratis, sin publicidad, sin algoritmo opaco.",
    "btn.create_profile":     "Crear mi perfil",
    "landing.login_link":     "¿Ya eres miembro? Inicia sesión",

    "onboarding.back":        "Atrás",
    "btn.next":               "Siguiente →",
    "btn.skip":               "Omitir",

    "onboarding.step1.title":               "¿De dónde eres?",
    "onboarding.step1.sub":                 "Tu punto de partida — el lugar que te define ante todo.",
    "onboarding.step1.country_label":       "País de origen *",
    "onboarding.step1.country_placeholder": "Busca tu país...",
    "onboarding.step1.city_label":          "Ciudad de origen *",
    "onboarding.step1.city_placeholder":    "ej. Lyon, Bruselas, Dakar...",

    "onboarding.step2.title":           "Tu situación",
    "onboarding.step2.sub":             "¿En qué punto estás de tu camino? Haz clic en tu situación.",
    "onboarding.step2.curious_title":   "Curioso",
    "onboarding.step2.curious_desc":    "Exploro la idea, sin decisión tomada",
    "onboarding.step2.thinking_title":  "En reflexión",
    "onboarding.step2.thinking_desc":   "Estoy pensando seriamente en irme",
    "onboarding.step2.confirmed_title": "Proyecto confirmado",
    "onboarding.step2.confirmed_desc":  "He decidido, preparo mi partida",
    "onboarding.step2.installed_title": "Ya instalado",
    "onboarding.step2.installed_desc":  "Ya vivo en el extranjero",

    "onboarding.step3.multi_title":       "¿Qué países te interesan?",
    "onboarding.step3.multi_sub":         "Elige hasta 5 países que te atraigan. Podrás afinar después.",
    "onboarding.step3.multi_placeholder": "Busca un país...",
    "onboarding.step3.multi_skip":        "Todavía busco",

    "onboarding.step3.single_title":              "¿Dónde vas a instalarte?",
    "onboarding.step3.single_sub":                "El país y la ciudad de destino de tu proyecto.",
    "onboarding.step3.single_country_label":      "País de destino *",
    "onboarding.step3.single_country_placeholder":"Busca tu país objetivo...",
    "onboarding.step3.single_city_label":         "Ciudad objetivo",
    "onboarding.step3.single_city_placeholder":   "ej. Lisboa, Berlín, Bangkok...",
    "onboarding.step3.single_quarter_label":      "Salida prevista",

    "onboarding.step3.inst_title":              "¿Dónde estás instalado?",
    "onboarding.step3.inst_sub":                "El país donde vives actualmente y desde hace cuánto tiempo.",
    "onboarding.step3.inst_country_label":      "País actual *",
    "onboarding.step3.inst_country_placeholder":"Busca tu país actual...",
    "onboarding.step3.inst_city_label":         "Ciudad",
    "onboarding.step3.inst_city_placeholder":   "ej. Porto, Tokio, Berlín...",
    "onboarding.step3.inst_duration_label":     "¿Desde hace cuánto tiempo?",

    "onboarding.step4.title":             "Lo que puedes aportar",
    "onboarding.step4.sub":               "Tus conocimientos y experiencias ayudan a otros miembros.",
    "onboarding.step4.sector_label":      "Tu sector profesional",
    "onboarding.step4.sector_placeholder":"ej. Finanzas, Arquitectura, Marketing...",
    "onboarding.step4.hv_title":          "✦ Perfil de alto valor de campo",
    "onboarding.step4.hv_desc":           "Los miembros de tu sector están entre los más buscados. Tus comentarios de experiencia pueden desbloquear situaciones complejas para otros expats.",
    "onboarding.step4.framing":           "Retroalimentación de campo y experiencias vividas — no consejos profesionales certificados.",
    "onboarding.step4.topics_title":      "¿En qué temas puedes ayudar?",
    "onboarding.step4.modes_title":       "¿Cómo prefieres ayudar?",
    "onboarding.step4.mode_messages":     "Mensajes privados",
    "onboarding.step4.mode_messages_sub": "Responde preguntas en directo",
    "onboarding.step4.mode_posts":        "Posts públicos",
    "onboarding.step4.mode_posts_sub":    "Comparte experiencias vividas",
    "onboarding.step4.mode_both":         "Ambos",
    "onboarding.step4.mode_both_sub":     "Mensajes + posts según quieras",
    "onboarding.step4.mode_none":         "Solo observar",
    "onboarding.step4.mode_none_sub":     "Por ahora, prefiero aprender",
    "onboarding.step4.chip_finance":      "Finanzas",
    "onboarding.step4.chip_law":          "Derecho",
    "onboarding.step4.chip_realestate":   "Inmobiliaria",
    "onboarding.step4.chip_health":       "Salud",
    "onboarding.step4.chip_tech":         "Tech",
    "onboarding.step4.chip_education":    "Educación",
    "onboarding.step4.chip_trade":        "Comercio",
    "onboarding.step4.chip_creative":     "Creación",

    "onboarding.step5.title":            "¿Quién eres?",
    "onboarding.step5.sub":              "Date presencia. Foto y nombre bastan para empezar.",
    "onboarding.step5.photo_hint":       "Haz clic para añadir una foto",
    "onboarding.step5.name_label":       "Nombre visible",
    "onboarding.step5.name_placeholder": "Nombre o apodo...",
    "onboarding.step5.bio_label":        "Bio",
    "onboarding.step5.bio_chars":        "(160 car.)",
    "onboarding.step5.bio_placeholder":  "ej. Diseñador gráfico de Lyon rumbo a Lisboa...",
    "onboarding.step5.langs_label":      "Idiomas hablados",
    "onboarding.step5.account_label":    "Tipo de cuenta",
    "onboarding.step5.type_individu":    "Individuo",
    "onboarding.step5.type_commerce":    "Comercio",
    "onboarding.step5.type_association": "Asociación",
    "btn.create_profile_final":          "Crear mi perfil ✦",

    "onboarding.exit.title":          "Esto es lo que encontramos para ti",
    "onboarding.exit.stat_suffix":    "miembros en tu comunidad",
    "onboarding.exit.discover":       "Descubrir mi perfil →",
    "onboarding.exit.complete_later": "Podrás completar tu perfil en cualquier momento",

    "nav.home":    "Inicio",
    "nav.feed":    "Feed",
    "nav.swipe":   "Swipe",
    "nav.profile": "Perfil",
    "profile.edit": "Editar",

    "btn.follow":   "+ Seguir",
    "btn.message":  "Mensaje",
    "btn.compat":   "~ Compat.",

    "status.helped":      "ayudados",
    "status.recognized":  "reconocido",
    "status.meetings":    "encuentros",
    "status.mirrors":     "WiggZ",

    "profile.tab_journal": "Diario",
    "profile.tab_reels":   "Reels",
    "profile.tab_posts":   "Posts",
    "profile.tab_infos":   "Info",
  },
};

/**
 * Applique les traductions i18n à tous les éléments taggés.
 * @param {string} lang — 'en' | 'fr' | 'es'
 */
function wcApplyLang(lang) {
  var t = WC_I18N[lang] || WC_I18N['en'];
  document.querySelectorAll('[data-wci18n]').forEach(function(el) {
    var key = el.getAttribute('data-wci18n');
    if (t[key]) el.textContent = t[key];
  });
  document.querySelectorAll('[data-wci18n-placeholder]').forEach(function(el) {
    var key = el.getAttribute('data-wci18n-placeholder');
    if (t[key]) el.placeholder = t[key];
  });
}
