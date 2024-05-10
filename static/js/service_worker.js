// service-worker

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

self.addEventListener('install', function (event)       // quando viene installato il mio service worker
{
    event.waitUntil         // inserisce elementi nella cache della pagina web
    (                   
        caches.open(CACHE_NAME)
        .then(function(cache)        // promessa 
        {
            return cache.addAll([urlsToCache])
            .catch(function(error)
            {
                console.error("Error during the loading into the cookies: ", error)
            });
        })    
    );
});

self.addEventListener('fetch', (event) =>       // quando il browser prova a recuperare una risorsa (evento fetch)
{     
    if (event.request.mode === 'navigate')      // se il tipo di richiesta è di navigazione (apre nuova pagina o ricarica)
    {
        event.respondWith(caches.open(CACHE_NAME)
        .then((cache) =>       // risposta del SW all'evento fetch e apertura della cache
        {
            return fetch(event.request.url).then((fetchedResponse) =>       // richiesta di risposta da evento fetch
            {
                cache.put(event.request, fetchedResponse.clone());      // memorizza risposta nella cache
                return fetchedResponse;         // risposta al browser
            })
            .catch(() => 
            {
                return cache.match(event.request.url);      // se la rete non è raggiungibile recupera la risposta nella cache
            });
        }));
    }
});

self.addEventListener('push', function(event)       // quando si effettua richiesta di notifica da una pagina 
{
    const options = 
    {
        body: event.data.text(),
    };

    event.waitUntil     // mantiene attivo il sw finché tutte le promesse vengono mantenute
    (
        self.registration.showNotification('Push notification', options)        // shows a notification
    );
});



/*
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

self.addEventListener('install', function(event) 
{
    event.waitUntil(                // Perform install steps        
        caches.open(CACHE_NAME)
        .then(function(cache) 
        {
            console.log('Opened cache');
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener('activate', function(event) 
{
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

self.addEventListener('fetch', function(event) 
{
    event.respondWith
    (
        fetch(event.request) .then(function(response) 
        {
                // Network request succeeded - cache the response
                const responseToCache = response.clone();
                caches.open(CACHE_NAME)
                    .then(function(cache) {
                        cache.put(event.request, responseToCache);
                    });

                return response;
        })
        .catch(function() 
        {
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


self.addEventListener('push', function(event) 
{
    console.log('Push received', event);

    const title = 'New Notification';
    const options = {
        body: event.data.text(),
        icon: '/path/to/icon.png',
        badge: '/path/to/badge.png'
    };

    event.waitUntil
    (
        self.registration.showNotification(title, options)
    );
});
*/

