// service worker of the website

const NOTIFICATION_URL = '/notification';       // resource to fetch
const CACHE_NAME = 'swallow_spot_cache';        // cache's name               
const URLS_TO_CACHE = [                         // pages to put into the SW cache                         
    '/',
    '/static/manifest.json',
    '/info/',
    '/snake',
    '/reports/hydro/',
    '/reports/snow/',
    'static/risk.json'
];

// Install event: loading cache into the application
self.addEventListener('install', (event) => 
{
    event.waitUntil(                                        // wait until the promise is kept
        caches.open(CACHE_NAME)                             // opens cache
        .then((cache) =>                                    
        {
            console.log('Insert paths into cache', cache);
            return cache.addAll(URLS_TO_CACHE);               // adds into cache
        })
        .catch((error) =>                                   // in case of error
        {
            console.error('Failed to cache:', error);       
        })
    );
});

// Fetch event: try the network first, then cache
self.addEventListener('fetch', (event) => 
{ 
    event.respondWith(
        fetch(event.request)
        .then((response) => 
        {
            if (response && response.status === 200 && response.type === 'basic')       // if the server is online
            {
                const responseClone = response.clone();                                 // repli
                caches.open(CACHE_NAME).then((cache) => 
                {
                    cache.put(event.request, responseClone);
                });
            }
            return response;
        })
        .catch(() => 
        {
            // If the network is unavailable, try to get it from the cache
            return caches.match(event.request).then((cachedResponse) => 
            {
                return cachedResponse || caches.match('/');
            });
        })
    );
});
  
// Activate event: delete old caches
self.addEventListener('activate', (event) => 
{
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys()
        .then((cacheNames) => 
        {
            return Promise.all(
                cacheNames.map((cacheName) => 
                {
                    if (cacheWhitelist.indexOf(cacheName) === -1) 
                    {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});


self.addEventListener('message', (event) => {
    if (event.data.type === 'CHECK_NOTIFICATION') {
        checkNotification2();
    }
});

async function checkNotification2() {
    console.log('Checking for notifications...');
    try {
        const response = await fetch(NOTIFICATION_URL, { credentials: 'include' });
        console.log("ciao");
        if (response.ok) {
            console.log("ciao")
            const data = await response.json();
            console.log('Notifications:', data);
        } else {
            console.error('Failed to fetch notifications:', response.status);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
}



setInterval(await checkNotification2, 10 * 1000);      // call the function every 10 seconds

/*
// Install event: loading cache into the application
self.addEventListener('install', (event) => 
{
    event.waitUntil(                                        // wait until the promise is kept
        caches.open(CACHE_NAME)                             // opens cache
        .then((cache) =>                                    
        {
            console.log('Insert paths into cache');
            return cache.addAll(URLS_TO_CACHE);               // adds into cache
        })
        .catch((error) =>                                   // in case of error
        {
            console.error('Failed to cache:', error);       
        })
    );
});

// Activate event: updating the cache 
self.addEventListener('activate', (event) => 
{
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys()
        .then((cacheNames) => 
        {
            return Promise.all(
                cacheNames.map((cacheName) => 
                {
                    if (cacheWhitelist.indexOf(cacheName) === -1) 
                    {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Fetch event: respond with cache first, then network
self.addEventListener('fetch', (event) =>       
{
event.respondWith(
caches.match(event.request)
.then((response) => {
// Cache hit - return the cached response
if (response) {
return response;
}

// Cache miss - fetch from the network
return fetch(event.request)
.then((networkResponse) => {
// Check if the response is valid
if (!networkResponse || networkResponse.status !== 200 || networkResponse.status !== 304 || networkResponse.type !== 'basic')     // finds out if there are network response from the server
{
    return networkResponse;
}

// Clone the response
const responseToCache = networkResponse.clone();

// Cache the fetched response
caches.open(CACHE_NAME)
.then((cache) => {
cache.put(event.request, responseToCache);
});

return networkResponse;
});
})
.catch(() => {
// If both the cache and network fail, show a fallback message or page
return caches.match('/');
})
);
});
  

/*
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cache => {
                    if (cache !== CACHE_NAME) {
                        console.log('Deleting old cache');
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
});

self.addEventListener('fetch', event => {
    console.log(`fetching ${event.request.url}`);
    event.respondWith(
        fetch(event.request)
        .catch(() => caches.match(event.request))
    );
});

self.addEventListener('push', function(event)       // quando si effettua richiesta di notifica da una pagina 
{
    const options = 
    {
        body: event.data.text(),
    };

    event.waitUntil     // mantiene attivo il sw finché tutte le promesse vengono mantenute
    (
        self.registration.showNotification('Notifica push', options)        // mostra una notifica
    );
});

self.addEventListener('notificationclick', event => {
    const notification = event.notification;  
    notification.close();
  });
  
  
  self.addEventListener('push', event => { 
    const body = event.data.text();
  
    event.waitUntil(
      self.registration.showNotification("Notification", {
        body: body,
        vibrate: [100, 50, 100],
        requireInteraction: true,
      })
    );
  });
*/

