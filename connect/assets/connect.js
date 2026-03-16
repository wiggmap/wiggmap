/* ============================================================
   WiggMap Connect — Logique principale
   connect.js v1.0
   MVP : tout en localStorage, Supabase viendra en T2
   ============================================================ */

'use strict';

/* -------------------------------------------------------
   Constantes — Statuts de vie
   ------------------------------------------------------- */
const LIFE_STATUSES = [
  { id: 'curious',     icon: '💭', label: 'Curieux',        desc: 'J\'explore, pas encore décidé' },
  { id: 'planning',    icon: '📋', label: 'Planificateur',  desc: 'Départ prévu dans X mois' },
  { id: 'transition',  icon: '🚀', label: 'En transition',  desc: 'Vient de partir/arriver (< 3 mois)' },
  { id: 'settled',     icon: '🏠', label: 'Installé',       desc: 'Entre 3 mois et 3 ans' },
  { id: 'veteran',     icon: '🌐', label: 'Vétéran',        desc: '3+ ans dans le pays' },
  { id: 'returned',    icon: '↩️',  label: 'Rentré',         desc: 'A vécu là-bas, est rentré' },
  { id: 'local',       icon: '🗺️',  label: 'Local',          desc: 'Né ou vivant depuis toujours ici' },
  { id: 'pro',         icon: '💼', label: 'Pro vérifié',    desc: 'Professionnel vérifié (avocat, agent...)' },
];

/* -------------------------------------------------------
   Constantes — Secteurs professionnels
   ------------------------------------------------------- */
const SECTORS = [
  { id: 'tech',         label: 'Tech & Numérique' },
  { id: 'finance',      label: 'Finance & Banque' },
  { id: 'health',       label: 'Santé & Médecine' },
  { id: 'education',    label: 'Éducation & Formation' },
  { id: 'law',          label: 'Droit & Juridique' },
  { id: 'real-estate',  label: 'Immobilier' },
  { id: 'trade',        label: 'Commerce & Retail' },
  { id: 'hospitality',  label: 'Hôtellerie & Restauration' },
  { id: 'creative',     label: 'Création & Design' },
  { id: 'media',        label: 'Médias & Communication' },
  { id: 'logistics',    label: 'Logistique & Transport' },
  { id: 'engineering',  label: 'Ingénierie & BTP' },
  { id: 'agri',         label: 'Agriculture & Élevage' },
  { id: 'ngo',          label: 'ONG & Humanitaire' },
  { id: 'other',        label: 'Autre' },
];

/* -------------------------------------------------------
   Constantes — Langues disponibles
   ------------------------------------------------------- */
const LANGUAGES = [
  { id: 'fr', flag: '🇫🇷', label: 'Français' },
  { id: 'en', flag: '🇬🇧', label: 'Anglais' },
  { id: 'es', flag: '🇪🇸', label: 'Espagnol' },
  { id: 'pt', flag: '🇵🇹', label: 'Portugais' },
  { id: 'de', flag: '🇩🇪', label: 'Allemand' },
  { id: 'it', flag: '🇮🇹', label: 'Italien' },
  { id: 'ar', flag: '🇸🇦', label: 'Arabe' },
  { id: 'zh', flag: '🇨🇳', label: 'Mandarin' },
  { id: 'ja', flag: '🇯🇵', label: 'Japonais' },
  { id: 'ko', flag: '🇰🇷', label: 'Coréen' },
  { id: 'ru', flag: '🇷🇺', label: 'Russe' },
  { id: 'nl', flag: '🇳🇱', label: 'Néerlandais' },
  { id: 'pl', flag: '🇵🇱', label: 'Polonais' },
  { id: 'tr', flag: '🇹🇷', label: 'Turc' },
  { id: 'vi', flag: '🇻🇳', label: 'Vietnamien' },
  { id: 'th', flag: '🇹🇭', label: 'Thaï' },
  { id: 'hi', flag: '🇮🇳', label: 'Hindi' },
  { id: 'sw', flag: '🇰🇪', label: 'Swahili' },
];

/* -------------------------------------------------------
   Clés localStorage
   ------------------------------------------------------- */
const LS_PROFILE_KEY   = 'wigg_connect_profile';
const LS_LANG_KEY      = 'wigg_lang';  // Clé existante WiggMap

/* -------------------------------------------------------
   Lecture / écriture du profil
   ------------------------------------------------------- */

/**
 * Récupère le profil depuis localStorage.
 * Retourne null si aucun profil n'existe.
 * @returns {Object|null}
 */
function getProfile() {
  try {
    const raw = localStorage.getItem(LS_PROFILE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    console.warn('[Connect] Erreur lecture profil:', e);
    return null;
  }
}

/**
 * Sauvegarde le profil dans localStorage.
 * @param {Object} data — données du profil
 * @returns {boolean} — succès de l'opération
 */
function saveProfile(data) {
  try {
    const profile = {
      ...data,
      updated_at: new Date().toISOString(),
      created_at: data.created_at || new Date().toISOString(),
    };
    localStorage.setItem(LS_PROFILE_KEY, JSON.stringify(profile));
    return true;
  } catch (e) {
    console.warn('[Connect] Erreur sauvegarde profil:', e);
    return false;
  }
}

/* -------------------------------------------------------
   Détection de langue
   ------------------------------------------------------- */

/**
 * Retourne la langue active de WiggMap (fr/en/es).
 * Se base sur wigg_lang en localStorage, défaut EN.
 * @returns {string}
 */
function getLang() {
  return localStorage.getItem(LS_LANG_KEY) || 'en';
}

/* -------------------------------------------------------
   Score miroir
   ------------------------------------------------------- */

/**
 * Calcule le score miroir entre deux profils (0-100).
 *
 * Règles de scoring :
 *   Pays croisés (origine A = cible B et vice versa) → 50 pts
 *   Secteur commun                                   → 20 pts
 *   Situation similaire                              → 15 pts
 *   Langues communes                                 → 15 pts
 *
 * @param {Object} profileA
 * @param {Object} profileB
 * @returns {number} — score entre 0 et 100
 */
function getMirrorScore(profileA, profileB) {
  let score = 0;

  // --- Pays croisés (50 pts) ---
  // A vient de X et veut aller en Y, B vient de Y et veut aller en X
  const targetsA = profileA.country_targets || [];
  const targetsB = profileB.country_targets || [];
  const originA  = profileA.country_origin;
  const originB  = profileB.country_origin;

  const mirrorAB = targetsA.includes(originB) && targetsB.includes(originA);
  if (mirrorAB) score += 50;
  else {
    // Miroir partiel : au moins un sens
    if (targetsA.includes(originB) || targetsB.includes(originA)) score += 20;
  }

  // --- Secteur commun (20 pts) ---
  if (profileA.sector && profileB.sector && profileA.sector === profileB.sector) {
    score += 20;
  }

  // --- Situation similaire (15 pts) ---
  if (profileA.life_status && profileB.life_status &&
      profileA.life_status === profileB.life_status) {
    score += 15;
  }

  // --- Langues communes (15 pts) ---
  const langsA = (profileA.languages || []).map(l => l.lang || l.id);
  const langsB = (profileB.languages || []).map(l => l.lang || l.id);
  const commonLangs = langsA.filter(l => langsB.includes(l));
  if (commonLangs.length > 0) {
    // Proportionnel : max 15 pts, minimum 5 pts si au moins 1 langue
    score += Math.min(15, 5 + (commonLangs.length - 1) * 5);
  }

  return Math.min(100, score);
}

/* -------------------------------------------------------
   Redirection intelligente
   ------------------------------------------------------- */

/**
 * Redirige vers feed.html si profil existe,
 * sinon vers onboarding.html.
 * À appeler depuis index.html.
 */
function redirectIfProfile() {
  const profile = getProfile();
  if (profile && profile.display_name) {
    window.location.href = 'feed.html';
  } else {
    window.location.href = 'onboarding.html';
  }
}

/* -------------------------------------------------------
   Utilitaires UI
   ------------------------------------------------------- */

/**
 * Affiche un toast de notification temporaire.
 * @param {string} message
 * @param {string} type — '' | 'success'
 * @param {number} duration — durée en ms (défaut 2500)
 */
function showToast(message, type = '', duration = 2500) {
  // Supprimer tout toast existant
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = 'toast' + (type ? ' toast--' + type : '');
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.3s';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

/**
 * Récupère le nom d'un pays depuis countries.json WiggMap.
 * @param {string} slug — slug pays (ex: 'france')
 * @returns {Promise<string>} — nom du pays
 */
async function getCountryName(slug) {
  try {
    const resp = await fetch('../data/countries.json');
    const data = await resp.json();
    return data[slug]?.name || slug;
  } catch {
    return slug;
  }
}

/**
 * Récupère tous les pays depuis countries.json WiggMap.
 * @returns {Promise<Array>} — [{slug, name, flag?}]
 */
async function getCountriesList() {
  try {
    const resp = await fetch('../data/countries.json');
    const data = await resp.json();
    return Object.entries(data).map(([slug, country]) => ({
      slug,
      name: country.name,
    })).sort((a, b) => a.name.localeCompare(b.name));
  } catch {
    return [];
  }
}

/* -------------------------------------------------------
   Drapeaux emoji (mapping slug → drapeau)
   ------------------------------------------------------- */
const FLAG_MAP = {
  'france': '🇫🇷', 'germany': '🇩🇪', 'spain': '🇪🇸', 'italy': '🇮🇹',
  'portugal': '🇵🇹', 'uk': '🇬🇧', 'united-states': '🇺🇸', 'canada': '🇨🇦',
  'brazil': '🇧🇷', 'argentina': '🇦🇷', 'mexico': '🇲🇽', 'colombia': '🇨🇴',
  'japan': '🇯🇵', 'china': '🇨🇳', 'south-korea': '🇰🇷', 'thailand': '🇹🇭',
  'vietnam': '🇻🇳', 'indonesia': '🇮🇩', 'malaysia': '🇲🇾', 'singapore': '🇸🇬',
  'india': '🇮🇳', 'australia': '🇦🇺', 'new-zealand': '🇳🇿', 'south-africa': '🇿🇦',
  'morocco': '🇲🇦', 'senegal': '🇸🇳', 'nigeria': '🇳🇬', 'kenya': '🇰🇪',
  'egypt': '🇪🇬', 'turkey': '🇹🇷', 'uae': '🇦🇪', 'saudi-arabia': '🇸🇦',
  'netherlands': '🇳🇱', 'belgium': '🇧🇪', 'switzerland': '🇨🇭', 'austria': '🇦🇹',
  'sweden': '🇸🇪', 'norway': '🇳🇴', 'denmark': '🇩🇰', 'finland': '🇫🇮',
  'poland': '🇵🇱', 'czech': '🇨🇿', 'hungary': '🇭🇺', 'romania': '🇷🇴',
  'greece': '🇬🇷', 'russia': '🇷🇺', 'ukraine': '🇺🇦', 'israel': '🇮🇱',
  'chile': '🇨🇱', 'peru': '🇵🇪', 'philippines': '🇵🇭', 'taiwan': '🇹🇼',
};

/**
 * Retourne le drapeau emoji pour un slug de pays.
 * Retourne 🌐 si non trouvé.
 * @param {string} slug
 * @returns {string}
 */
function getFlag(slug) {
  return FLAG_MAP[slug] || '🌐';
}

/* -------------------------------------------------------
   Switcher de langue — header partagé
   ------------------------------------------------------- */

/**
 * Initialise le switcher de langue dans l'élément #wcLangSwitcher.
 * Lit et écrit localStorage wigg_lang (valeurs : 'en' | 'fr' | 'es').
 * Appeler au DOMContentLoaded sur chaque page.
 */
function wcInitLangSwitcher() {
  var LANGS = ['en', 'fr', 'es'];
  var container = document.getElementById('wcLangSwitcher');
  if (!container) return;

  var isOpen = false;

  function getCurrentLang() {
    var stored = localStorage.getItem(LS_LANG_KEY);
    return LANGS.indexOf(stored) !== -1 ? stored : 'en';
  }

  function render() {
    var current = getCurrentLang();
    var others  = LANGS.filter(function(l) { return l !== current; });

    container.innerHTML =
      '<div class="wc-lang">' +
        '<button class="wc-lang__btn" id="wcLangBtn">' +
          current.toUpperCase() + ' ▾' +
        '</button>' +
        (isOpen
          ? '<div class="wc-lang__dropdown">' +
              others.map(function(l) {
                return '<div class="wc-lang__option" data-lang="' + l + '">' +
                         l.toUpperCase() +
                       '</div>';
              }).join('') +
            '</div>'
          : '') +
      '</div>';

    // Bouton — toggle dropdown
    document.getElementById('wcLangBtn').addEventListener('click', function(e) {
      e.stopPropagation();
      isOpen = !isOpen;
      render();
    });

    // Options — sélection
    if (isOpen) {
      container.querySelectorAll('.wc-lang__option').forEach(function(opt) {
        opt.addEventListener('click', function(e) {
          e.stopPropagation();
          localStorage.setItem(LS_LANG_KEY, opt.dataset.lang);
          isOpen = false;
          render();
        });
      });
    }
  }

  // Fermer au clic ailleurs
  document.addEventListener('click', function() {
    if (isOpen) { isOpen = false; render(); }
  });

  render();
}

/* -------------------------------------------------------
   Exports (pour les autres pages)
   ------------------------------------------------------- */
window.WiggConnect = {
  // Données
  LIFE_STATUSES,
  SECTORS,
  LANGUAGES,
  // Profil
  getProfile,
  saveProfile,
  getLang,
  // Logique
  getMirrorScore,
  redirectIfProfile,
  // UI
  showToast,
  // Pays
  getCountryName,
  getCountriesList,
  getFlag,
  // Header
  wcInitLangSwitcher,
};
