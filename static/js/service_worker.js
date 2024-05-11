// service-worker

const CACHE_NAME = 'my-site-cache-v1';
const urlsToCache = [
    '/',
    '/templates/layout.html',
    '/templates/info.html',
    '/templates/home.html',
    '/templates/user/settings.html',
    '/templates/user/profile.html',
    '/templates/user/admin_profile.html',
    '/templates/reports/snow.html',
    '/templates/reports/hydro.html',
    '/templates/reports/ava.html',
    '/templates/auth/signup.html',
    '/templates/auth/login.html',
    '/templates/auth/login_layout.html',
    '/temp/login.html',
    '/static/js/search_bar.js',
    '/static/js/profile_actions.js',
    '/static/js/main.js',
    '/static/js/home.js',
    '/static/images/swallowspot_title_mini.png',
    '/static/images/swallowspot_title_mini_darkmode.png',
    '/static/images/swallowspot_title_main.png',
    '/static/images/swallowspot_title_main_darkmode.png',
    '/static/images/swallowspot_footer_icon.png',
    '/static/images/login_background_darkmode.png',
    '/static/images/login_background_2.png',
    '/static/images/bell-solid.svg',
    '/static/favicon/swallowspot_favicon.png',
    '/static/css/search.css',
    '/static/css/login_layout.css',
    '/static/css/index.css',
    '/static/css/animations.css',
    '/static/css/slider/slider.css',
    '/static/css/slider/slider_visual_mode.css',
    '/static/css/slider/slider_notification.css',
    '/static/css/reports/risk.css',
    '/static/css/info/info.css',
    '/static/css/home/home.css',
    '/static/css/account/profile.css',
    '/static/css/account/admin.css'
];

self.addEventListener('install', function (event)       // when the service worker is installed
{
    event.waitUntil         // waits until the event is completed
    (                   
        caches.open(CACHE_NAME)         // opens the cache
        .then(function(cache)           // promise 
        {
            return cache.addAll
            ([
                urlsToCache
            ]).catch(function(error)
            {
                console.error("Errore durante il caricamento: ", error);
            });

            /*
            return cache.addAll([urlsToCache])
            .catch(function(error)
            {
                console.error("Error during the loading into the cookies: ", error)
            }); 
            */
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

