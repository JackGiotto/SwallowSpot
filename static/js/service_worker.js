// service-worker.js

const CACHE_NAME = 'my-site-cache-v1';
const urlsToCache = [
    '/',
    '../css/animations.css',
    '../favicon/swallowspot_favicon.png',
    '../images/login_background_2.png',
    '/auth/signup/',
    '/auth/login/',
    "/reports/hydro/",
    "/reports/snow/",
    "/profile/"
];

self.addEventListener('install', function(event) {
    // Perform install steps
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.filter(function(cacheName) {
                    return cacheName.startsWith('my-site-cache-') &&
                        cacheName !== CACHE_NAME;
                }).map(function(cacheName) {
                    return caches.delete(cacheName);
                })
            );
        })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        fetch(event.request)
            .then(function(response) {
                // Network request succeeded - cache the response
                const responseToCache = response.clone();
                caches.open(CACHE_NAME)
                    .then(function(cache) {
                        cache.put(event.request, responseToCache);
                    });

                return response;
            })
            .catch(function() {
                // Network request failed - try to retrieve the response from cache
                return caches.match(event.request)
                    .then(function(response) {
                        // Cache hit - return response
                        if (response) {
                            return response;
                        }

                        // Cache miss - return a fallback response
                        return caches.match('/offline.html');
                    });
            })
    );
});

