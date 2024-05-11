// installation of the Service Worker on the browser

if('serviceWorker' in navigator) 
{
    navigator.serviceWorker.register('/static/js/service_worker.js')        // registration of the SW
    .then(function(registration)                                            // if the SW is register correctly
    { 
        console.log("SW registration successfully ", registration);         
    })
    .catch(function(error)                                                  // if something go wrong during the registration
    {
        console.error("There was an error during SW registration: ", error);
    });
}

function allowNotifications()           // ask the user if he would like to have notfication
{
    Notification.requestPermission()
}

window.onload = function() 
{
    document.getElementById('telegram').addEventListener('click', function() 
    {
        Notification.requestPermission()
        .then(function(permission) 
        {
            if(permission === 'granted') 
            {
                navigator.serviceWorker.ready.then(function(registration) 
                {
                    registration.showNotification('Notifica push', 
                    {
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
