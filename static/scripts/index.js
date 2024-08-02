function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
}

function updateDistances(userLocation) {
    document.querySelectorAll('.location_preview_container').forEach(container => {
        const locationLat = parseFloat(container.getAttribute('data-latitude'));
        const locationLon = parseFloat(container.getAttribute('data-longitude'));
        console.log('Location coordinates:', locationLat, locationLon);
        console.log('User location:', userLocation);

        if (!isNaN(locationLat) && !isNaN(locationLon) && userLocation && userLocation.length === 2) {
            const distance = calculateDistance(userLocation[1], userLocation[0], locationLat, locationLon);
            const distanceElement = container.querySelector('#distance');
            if (distanceElement) {
                distanceElement.textContent = `${distance.toFixed(2)} km`;
            }
        } else {
            console.error('Invalid coordinates for location:', container);
        }
    });
}


function initializeUserLocation(position) {
    const userLocation = [position.coords.longitude, position.coords.latitude];
    localStorage.setItem('userLocation', JSON.stringify(userLocation));
    console.log('User location saved:', userLocation);
    updateDistances(userLocation);
}

function loadSavedLocation() {
    const savedLocation = localStorage.getItem('userLocation');
    if (savedLocation) {
        const userLocation = JSON.parse(savedLocation);
        console.log('Loaded saved location:', userLocation);
        updateDistances(userLocation);
    }
}

if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(initializeUserLocation, () => {
        alert('Es ist nicht möglich, Ihre Position zu bestimmen.');
        loadSavedLocation();
    });
} else {
    alert('Geolocation wird von Ihrem Browser nicht unterstützt.');
    loadSavedLocation();
}

document.getElementById('favourites_button').addEventListener('click', function() {
    window.location.href = '/favorites';
});


document.getElementById('logoutButton').addEventListener('click', function() {
    fetch('{{ url_for("logout") }}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        })
        .catch(error => console.error('Error:', error));
});
