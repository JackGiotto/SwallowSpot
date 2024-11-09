
const NOTIFICATION_URL = '/notification';       // resource to fetch
const CACHE_NAME = 'swallow_spot_cache';        // cache's name
const URLS_TO_CACHE = [                         // pages to put into the SW cache
    '/',
    '/static/manifest.json',
    '/info/',
    '/snake',
    '/reports/hydro/',
    '/reports/snow/'
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
            return caches.match(event.request).then((cachedResponse) =>                 // If the network is unavailable, try to get it from the cache
            {
                return cachedResponse || caches.match('/');
            });
        })
    );
});

// Activate event: delete old caches
self.addEventListener('activate', (event) =>                            // when the service worker is activated
{
    const cacheWhitelist = [CACHE_NAME];                                //
    event.waitUntil(                                                    //
        caches.keys()
        .then((cacheNames) =>
        {
            return Promise.all(                                         //
                cacheNames.map((cacheName) =>
                {
                    if (cacheWhitelist.indexOf(cacheName) === -1)       //
                    {
                        return caches.delete(cacheName);                // deletes the
                    }
                })
            );
        })
    );
});


// //
// self.addEventListener('message', (event) =>
// {
//     if (event.data.type === 'CHECK_NOTIFICATION')
//     {
//         checkNotification2();
//     }
// });

// self.addEventListener('notificationclick', event =>
// {
//     const notification = event.notification;
//     notification.close();
// });


// self.addEventListener('push', function(event)                           // quando si effettua richiesta di notifica da una pagina
// {
//     const options =
//     {
//         body: event.data.text(),
//     };

//     event.waitUntil                                                     // mantiene attivo il sw finché tutte le promesse vengono mantenute
//     (
//         self.registration.showNotification('Swallowspot', options)      // mostra una notifica
//     );
// });

// async function checkNotification2() {
//     console.log('Checking for notifications...');
//     try
//     {
//         const response = await fetch(NOTIFICATION_URL, { credentials: 'include' });
//         if (response.ok)
//         {
//             const data = await response.json();
//             if (data['hydro'] != 'verde' || data['hydro_geo'] != 'verde' || data['storms']['color_name'] != 'verde')
//             {
//                 registration.showNotification('Notifica push',          // mostra la notifica push e il suo contenuto
//                 {
//                     body: 'Allerta nella tua zona!'
//                 });
//             }
//         }
//         else
//         {
//             console.error('Failed to fetch notifications:', response.status);
//         }
//     }
//     catch (error)
//     {
//         console.error('Fetch error:', error);
//     }
// }


// self.addEventListener('sync', function(event) {
//     if (event.tag === 'syncNotification') { // Check if this is the sync you're interested in
//       event.waitUntil(checkNotification2()); // Call your function to check for notifications
//     }
//   });


// setInterval(checkNotification2, 72000 * 1000);      // call the function every 10 seconds
