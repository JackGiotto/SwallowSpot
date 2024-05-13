// service worker
/*
const CACHE_NAME = 'v2';

self.addEventListener('install', e => {         
    console.log("ServiceWorker: installed");

});

self.addEventListener('activate', e => {    // activates the SW
    console.log("ServiceWorker: activated");

    e.waitUntil(        // removes old cache files
        caches.keys()
        .then(cacheNames =>{
            return Promise.all(
                cacheNames.map(cache => {
                    if(cache != CACHE_NAME)
                    {
                        console.log('SW: clearing Old cache');
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
});

self.addEventListener('fetch', e => {   // for fetch event
    console.log('Service worker: Fetching');
    e.respondWith(
        fetch(e.request)
        .then(res => {
            const resClone = res.clone();
            caches
            .open(CACHE_NAME)
            .then(cache => {
                cache.put(e.request, resClone);
            });
            return res;
        })
        .catch(err => caches.match(e.request).then(res => res))
    );
});
*/
