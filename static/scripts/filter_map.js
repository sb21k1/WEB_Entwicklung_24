mapboxgl.accessToken = 'pk.eyJ1Ijoic2JrMjEiLCJhIjoiY2x3aHBkcGF2MGRvNzJpcGZmcW80c3djNCJ9.ut0vDzlCgM6Q10ZI52hpwQ';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v11',
    center: [13.4050, 52.5200], // Standardposition (Berlin)
    zoom: 10
});

map.on('load', function() {
    map.resize();
    loadSavedLocation();
});

map.on('idle', function() {
    map.resize();
});

var userLocation;
var output = document.getElementById('myDistanceInfo');

function initializeMap(position) {
    userLocation = [position.coords.longitude, position.coords.latitude];
    localStorage.setItem('userLocation', JSON.stringify(userLocation));
    console.log('User location saved:', userLocation);
    setupMap(userLocation);
}

function setupMap(center) {
    map.setCenter(center);

    new mapboxgl.Marker()
        .setLngLat(center)
        .addTo(map);

    var radius = document.getElementById('myRange').value;
    output.textContent = radius + " km";
    addCircle(center, radius);
    updateBounds(center, radius);
}

function loadSavedLocation() {
    var savedLocation = localStorage.getItem('userLocation');
    if (savedLocation) {
        userLocation = JSON.parse(savedLocation);
        console.log('Loaded saved location:', userLocation);

        setupMap(userLocation);

        var savedRadius = localStorage.getItem('circleRadius') || 10; // default to 10 if not set
        document.getElementById('myRange').value = savedRadius;
        addCircle(userLocation, savedRadius);
        updateBounds(userLocation, savedRadius);
    }
}

if (!userLocation && navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(initializeMap, () => {
        alert('Es ist nicht möglich, Ihre Position zu bestimmen.');
    });
} else if (!userLocation) {
    alert('Geolocation wird von Ihrem Browser nicht unterstützt.');
}

document.getElementById('myRange').addEventListener('input', function(e) {
    var radius = e.target.value;
    output.textContent = radius + " km";
    if (userLocation) {
        addCircle(userLocation, radius);
        updateBounds(userLocation, radius);
        localStorage.setItem('circleRadius', radius);
    }

});



document.querySelector('.close_dialog').addEventListener('click', function() {
    document.getElementById('geo_dialog').style.display = 'none';
});

function createGeoJSONCircle(center, radiusInKm, points = 64) {
    var coords = {
        latitude: center[1],
        longitude: center[0]
    };

    var km = radiusInKm;

    var ret = [];
    var distanceX = km / (111.32 * Math.cos(coords.latitude * Math.PI / 180));
    var distanceY = km / 110.574;

    for (var i = 0; i < points; i++) {
        var theta = (i / points) * (2 * Math.PI);
        var x = distanceX * Math.cos(theta);
        var y = distanceY * Math.sin(theta);

        ret.push([coords.longitude + x, coords.latitude + y]);
    }
    ret.push(ret[0]);

    return {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [ret]
        }
    };
}

function addCircle(center, radius) {
    if (map.getSource('circle')) {
        map.getSource('circle').setData(createGeoJSONCircle(center, radius));
    } else {
        map.addSource('circle', {
            "type": "geojson",
            "data": createGeoJSONCircle(center, radius)
        });

        map.addLayer({
            "id": "circle",
            "type": "fill",
            "source": "circle",
            "layout": {},
            "paint": {
                "fill-color": "#007cbf",
                "fill-opacity": 0.3
            }
        });
    }
}

function updateBounds(center, radiusInKm) {
    var coords = {
        latitude: center[1],
        longitude: center[0]
    };

    var km = radiusInKm;

    var distanceX = km / (111.32 * Math.cos(coords.latitude * Math.PI / 180));
    var distanceY = km / 110.574;

    var bounds = [
        [coords.longitude - distanceX, coords.latitude - distanceY],
        [coords.longitude + distanceX, coords.latitude + distanceY]
    ];

    map.fitBounds(bounds, { padding: 20 });
}