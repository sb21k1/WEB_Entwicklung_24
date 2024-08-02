from flask import Flask, request, jsonify, redirect, url_for, render_template, session
from firebase_admin import credentials, initialize_app, db, storage, auth
import firebase_admin
import requests
from math import radians, sin, cos, sqrt, atan2
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

selected_tags = []
max_distance = None
user_lat = None
user_lon = None


cred = credentials.Certificate('serviceKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://places-de11a-default-rtdb.firebaseio.com',
    'storageBucket': 'places-de11a.appspot.com'
})

def fetch_data():
    ref = db.reference('locations')
    data = ref.get()

    locations = []
    if data and isinstance(data, list):
        for item in data:
            if item is not None:
                locations.append({
                    'description': item.get('Beschreibung', ''),
                    'latitude': item.get('geo', {}).get('latitude', ''),
                    'longitude': item.get('geo', {}).get('longitude', ''),
                    'name': item.get('name', ''),
                    'tags': item.get('tags', []),
                })
    print(locations)
    return locations

def get_favorite_locations(uid):
    user_ref = db.reference(f'users/{uid}/favorites')
    favorites = user_ref.get()
    all_locations = fetch_data()

    if favorites:
        favorite_locations = [
            location for location in all_locations
            if location['name'] in favorites
        ]

        images = fetch_images_for_locations(favorite_locations)
        image_mapping = {img['name']: img['image_urls'] for img in images}

        for location in favorite_locations:
            location['images'] = image_mapping.get(location['name'], [])
        
        return favorite_locations
    return []



def is_valid_image(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.headers.get('Content-Type', '').startswith('image/')
    except requests.RequestException:
        return False

def fetch_images_for_locations(locations):
    bucket = storage.bucket()
    images = []

    for location in locations:
        folder_name = location['name']
        blobs = bucket.list_blobs(prefix=f"{folder_name}/")
        image_urls = []

        for blob in blobs:
            try:
                image_url = blob.generate_signed_url(version='v4', expiration=3600)
                if is_valid_image(image_url):
                    image_urls.append(image_url)
            except Exception as e:
                print(f"Error generating URL for {blob.name}: {e}")

        if image_urls:
            images.append({
                'name': location['name'],
                'image_urls': image_urls
            })
        else:
            print(f"No images found for location: {location['name']}")

    return images

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return distance

tags = [
    {"type": "theme_tags", "name": "Park"},
    {"type": "theme_tags", "name": "Café"},
    {"type": "theme_tags", "name": "Restaurant"},
    {"type": "theme_tags", "name": "Library"},
    {"type": "theme_tags", "name": "Museum"},
    {"type": "theme_tags", "name": "Bridge"},
    {"type": "theme_tags", "name": "Street"},
    {"type": "theme_tags", "name": "Train station"},
    {"type": "theme_tags", "name": "Subway"},
    {"type": "theme_tags", "name": "Harbor"},
    {"type": "theme_tags", "name": "Rooftop"},
    {"type": "theme_tags", "name": "Castle"},
    {"type": "theme_tags", "name": "Market"},
    {"type": "theme_tags", "name": "Warehouse"},
    {"type": "theme_tags", "name": "Studio"},
    {"type": "theme_tags", "name": "Theater"},
    {"type": "theme_tags", "name": "Concert Hall"},
    {"type": "theme_tags", "name": "Mall"},
    {"type": "theme_tags", "name": "Temple"},
    {"type": "theme_tags", "name": "Church"},
    {"type": "theme_tags", "name": "Monument"},
    {"type": "theme_tags", "name": "Ruins"},
    {"type": "theme_tags", "name": "Hotel"},
    {"type": "theme_tags", "name": "University"},
    {"type": "theme_tags", "name": "Office"},
    
    {"type": "type_tags", "name": "Historic"},
    {"type": "type_tags", "name": "Modern"},
    {"type": "type_tags", "name": "Industrial"},
    {"type": "type_tags", "name": "Nature"},
    {"type": "type_tags", "name": "Urban"},
    {"type": "type_tags", "name": "Vintage"},
    {"type": "type_tags", "name": "Artsy"},
    {"type": "type_tags", "name": "Cultural"},
    {"type": "type_tags", "name": "Bauhaus"},
    
    {"type": "usecase_tags", "name": "Fotografie"},
    {"type": "usecase_tags", "name": "Videodreh"},
    {"type": "usecase_tags", "name": "Mode-Shooting"},
    {"type": "usecase_tags", "name": "Filmdreh"},
    {"type": "usecase_tags", "name": "Musikvideo"},
    {"type": "usecase_tags", "name": "Werbung"},
    {"type": "usecase_tags", "name": "Social Media Content"}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    global selected_tags, max_distance, user_lat, user_lon
    locations = fetch_data()

    filtered_locations = locations

    if selected_tags or (user_lat is not None and user_lon is not None and max_distance is not None):
        if selected_tags:
            filtered_locations = [
                loc for loc in filtered_locations
                if any(tag.lower().strip() in (tag_name.lower().strip() for tag_name in loc['tags'])
                for tag in selected_tags)
            ]

    if user_lat != None and user_lon != None and max_distance != 0:
        new_filtered_locations = []
        for location in filtered_locations:
            if location['latitude'] != "" and location['longitude'] != "":
                distance = calculate_distance(user_lat, user_lon, float(location['latitude']), float(location['longitude']))
                location['distance'] = round(distance, 2)
                if distance <= max_distance:
                    new_filtered_locations.append(location)
        filtered_locations = new_filtered_locations

    images = fetch_images_for_locations(filtered_locations)
    image_mapping = {img['name']: img['image_urls'] for img in images}

    for location in filtered_locations:
        location['images'] = image_mapping.get(location['name'], [])

    user_info = session.get('user_info')

    return render_template('index.html', user_info=user_info, locations=filtered_locations, tags=tags)

@app.route('/recieveTags', methods=['POST'])
def recieveTags():
    global selected_tags, max_distance, user_lat, user_lon
    if request.method == 'POST':
        data = request.json
        selected_tags = data.get('tags', [])
        max_distance = float(data.get('max_distance', 100))
        user_lat = float(data.get('user_lat'))
        user_lon = float(data.get('user_lon'))
        print('Ausgewählte Tags:', selected_tags)
        print('Max Distance:', max_distance)
        print('User Location:', user_lat, user_lon)
        return jsonify({'status': 'success'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    return render_template('registration.html')

@app.route('/favorites')
def favorites():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    user_info = get_user_info(user_id)
    favorite_locations = get_favorite_locations(user_id)
    print(f"Rendering favorites for user {user_id}: {favorite_locations}")
    return render_template('favorites.html', uid=user_id, user_info=user_info, locations=favorite_locations)

def get_user_info(uid):
    ref = db.reference(f'users/{uid}')
    return ref.get()

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')

    try:
        user = auth.create_user(
            email=email,
            password=password
        )

        user_data = {
            'fullName': full_name,
            'email': email,
            }
        print(full_name, email)
        db.reference(f'users/{user.uid}').set(user_data)

        return jsonify({'message': 'User created successfully', 'uid': user.uid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/login_user', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        user = auth.get_user_by_email(email)
        user_info = get_user_info(user.uid)
        session['user_info'] = user_info
        session['user_id'] = user.uid 
        print(f"User logged in: {session['user_info']}")
        return jsonify({'message': 'User logged in successfully', 'uid': user.uid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400



@app.route('/set_favorite', methods=['POST'])
def set_favorite():
    data = request.json
    uid = session.get('user_id')
    location_name = data.get('favorite')

    if not uid:
        return jsonify({'status': 'error', 'message': 'User not authenticated'}), 401

    if not location_name:
        return jsonify({'status': 'error', 'message': 'Location name not provided'}), 400

    try:
        user_ref = db.reference(f'users/{uid}/favorites')
        user_ref.child(location_name).set(True)
        return jsonify({'status': 'added'})
    except Exception as e:
        print(f"Error adding favorite: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Database error'}), 500

@app.route('/delete_favorite', methods=['POST'])
def delete_favorite():
    data = request.json
    uid = session.get('user_id')
    location_name = data.get('favorite')

    if not uid:
        return jsonify({'status': 'error', 'message': 'User not authenticated'}), 401

    if not location_name:
        return jsonify({'status': 'error', 'message': 'Location name not provided'}), 400

    try:
        user_ref = db.reference(f'users/{uid}/favorites')
        user_ref.child(location_name).delete()
        return jsonify({'status': 'removed'})
    except Exception as e:
        print(f"Error removing favorite: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Database error'}), 500

    
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
