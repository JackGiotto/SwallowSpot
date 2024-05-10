
if('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/js/service_worker.js')
    .then(function(registration) { // Corrected the function parameter name from 'registration' to 'registration'
        console.log("Registration is ok ", registration);
    })
    .catch(function(error) {
        console.error("There was an error: ", error);
    });
}

window.onload = function() {
    document.getElementById('telegram').addEventListener('click', function() {
        Notification.requestPermission()
        .then(function(permission) {
            if(permission === 'granted') {
                navigator.serviceWorker.ready.then(function(registration) {
                    registration.showNotification('Notifica push', {
                        body: 'Ciao Pietro'
                    });
                });
            }
        });
    });
}


/* 
window.onload = function() 
{
    if ('serviceWorker' in navigator) 
    {
        navigator.serviceWorker.register('/service_worker.js')
        .then(function(registration) 
        {
            console.log('Service worker registered successfully:', registration);
        })
        .catch(function(error) 
        {
            console.error('Service worker registration failed:', error);
        });
    }
    else 
    {
        console.error("Service worker doesn't work");
    }
};
*/
