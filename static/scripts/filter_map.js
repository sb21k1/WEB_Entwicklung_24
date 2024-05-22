 // Google Maps JavaScript API einbinden
 (function(libraries) {
     var script, params = new URLSearchParams();
     params.set('key=AIzaSyDZgBTmkUtFXyDUf84rQvXTWMC4WUQ8c8c');
     params.set('libraries', libraries.join(','));
     params.set('callback', 'initMap');

     script = document.createElement('script');
     script.src = 'https://maps.googleapis.com/maps/api/js?' + params.toString();
     script.defer = true;
     script.async = true;

     script.onerror = function() {
         console.error('Die Google Maps JavaScript-API konnte nicht geladen werden.');
     };

     document.head.appendChild(script);
 })(['places-api-424100']); // Hier kannst du weitere Bibliotheken hinzufügen, z.B. 'geometry', 'drawing'

 function initMap() {
     // Hier kannst du deine Karteninitialisierung durchführen
     console.log('Google Maps JavaScript-API erfolgreich geladen.');
 }