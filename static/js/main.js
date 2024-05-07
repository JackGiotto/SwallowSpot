window.onload = function() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/js/service_worker.js')
            .then(function(registration) {
                console.log('Service worker registered successfully:', registration);
            })
            .catch(function(error) {
                console.error('Service worker registration failed:', error);
            });
    } else {
        console.log("non funziona il service worker");
    }
};
