// Sprint 2 — bumped v2 → v3 to invalidate caches that hold the legacy
// non-trilingual root structure. v3 caches a minimal core (root + the
// three language homes + manifest); the activate handler purges every
// older cache so users on v2 get a clean slate without stale /index.html.
const CACHE_NAME = "wiggmap-v3";

const CORE_ASSETS = [
  "/",
  "/en/",
  "/fr/",
  "/es/",
  "/manifest.webmanifest"
];

// Install: cache core
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS))
  );
  self.skipWaiting();
});

// Activate: cleanup old caches
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.map((k) => (k !== CACHE_NAME ? caches.delete(k) : null)))
    )
  );
  self.clients.claim();
});

// Fetch: network-first for JSON, cache-first for others
self.addEventListener("fetch", (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Only handle same-origin
  if (url.origin !== location.origin) return;

  const isJson = url.pathname.endsWith(".json");

  if (isJson) {
    // Network-first (always try fresh data)
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req))
    );
    return;
  }

  // HTML = network-first (toujours la version fraîche du serveur)
  const isHtml = req.headers.get("accept") && req.headers.get("accept").includes("text/html");
  if (isHtml) {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req))
    );
    return;
  }

  // Cache-first pour le reste (assets statiques)
  event.respondWith(
    caches.match(req).then((cached) => cached || fetch(req))
  );
});
