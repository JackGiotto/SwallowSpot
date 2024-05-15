// service worker

const CACHE_NAME = 'swallow_spot_cache';
const urlsToCache = [
    '/',
    '/static/manifest.json',
    '/info/',
    '/reports/hydro/',
    '/reports/snow/',
    '/static/js/search_bar.js',
    '/static/js/profile_actions.js',
    '/static/js/home.js',
    '/static/images/swallowspot_title_mini.png',
    '/static/images/swallowspot_title_mini_darkmode.png',
    '/static/images/swallowspot_title_main.png',
    '/static/images/swallowspot_title_main_darkmode.png',
    '/static/images/swallowspot_footer_icon.png',
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
    '/static/css/account/admin.css',
    'static/risk.json'
];

self.addEventListener('install', event => {
    console.log("Installed service worker");
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME)
        .then(cache => {
            return cache.addAll(urlsToCache);
        })
    );
});

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
  /*
async function checkNotification() // Function to check if notification should be sent
{
    try 
    {
        const cache = await caches.open(CACHE_NAME);            // Open the cache

        const response = await cache.match('/static/risk.json');        // Retrieve the JSON file from the cache
        if (response) 
        {
            // Parse JSON data
            const data = await response.json();         // Check if the value of the key 'value' is true
            if (data.value === true) 
            {
                self.registration.showNotification('Notification Title',     // Show notification
                {
                    body: 'Notification Body'
                });
            }
        }
    } 
    catch (error) 
    {
        console.error('Error checking notification:', error);
    }
}
  
// Check for notification every 30 seconds
setInterval(checkNotification, 30 * 1000);
*/

function checkNotification() // Function to check if notification should be sent
{
   console.log('ciao');
}

setInterval(checkNotification, 5);