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

# Firebase Admin SDK initialization
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
    user_ref = db.reference('users/' + uid + '/favorites')
    favorites = user_ref.get()
    all_locations = fetch_data()
    
    if favorites:
        favorite_locations = [
            location for location in all_locations
            if location.get('id') in favorites
        ]
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
    {"type": "theme_tags", "name": "urban"},
    {"type": "theme_tags", "name": "park"},
    {"type": "theme_tags", "name": "café"},
    {"type": "theme_tags", "name": "restaurant"},
    {"type": "theme_tags", "name": "library"},
    {"type": "theme_tags", "name": "museum"},
    {"type": "theme_tags", "name": "historical"},
    {"type": "theme_tags", "name": "modern"},
    {"type": "theme_tags", "name": "bridge"},
    {"type": "theme_tags", "name": "street"},
    {"type": "theme_tags", "name": "train station"},
    {"type": "theme_tags", "name": "subway"},
    {"type": "theme_tags", "name": "harbor"},
    {"type": "theme_tags", "name": "rooftop"},
    {"type": "theme_tags", "name": "garden"},
    {"type": "theme_tags", "name": "castle"},
    {"type": "theme_tags", "name": "market"},
    {"type": "theme_tags", "name": "warehouse"},
    {"type": "theme_tags", "name": "studio"},
    {"type": "theme_tags", "name": "theater"},
    {"type": "theme_tags", "name": "concert hall"},
    {"type": "theme_tags", "name": "mall"},
    {"type": "theme_tags", "name": "temple"},
    {"type": "theme_tags", "name": "church"},
    {"type": "theme_tags", "name": "monument"},
    {"type": "theme_tags", "name": "ruins"},
    {"type": "theme_tags", "name": "hotel"},
    {"type": "theme_tags", "name": "university"},
    {"type": "theme_tags", "name": "office"},
    {"type": "theme_tags", "name": "zoo"},
    
    {"type": "type_tags", "name": "Historic"},
    {"type": "type_tags", "name": "Modern"},
    {"type": "type_tags", "name": "Industrial"},
    {"type": "type_tags", "name": "Natur"},
    {"type": "type_tags", "name": "Urban"},
    {"type": "type_tags", "name": "Vintage"},
    {"type": "type_tags", "name": "Künstlerisch"},
    {"type": "type_tags", "name": "Kulturell"},
    {"type": "type_tags", "name": "Bauhaus"},
    
    {"type": "usecase_tags", "name": "Fotografie"},
    {"type": "usecase_tags", "name": "Videodreh"},
    {"type": "usecase_tags", "name": "Mode-Shooting"},
    {"type": "usecase_tags", "name": "Filmdreh"},
    {"type": "usecase_tags", "name": "Musikvideo"},
    {"type": "usecase_tags", "name": "Werbung"},
    {"type": "usecase_tags", "name": "Social Media Content"},
    {"type": "usecase_tags", "name": "Live-Streaming"}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    global selected_tags, max_distance, user_lat, user_lon
    
    locations = fetch_data()
    filtered_locations = locations

    if user_lat is not None and user_lon is not None:
        for location in filtered_locations:
            if location['latitude'] != "" and location['longitude'] != "":
                distance = calculate_distance(user_lat, user_lon, float(location['latitude']), float(location['longitude']))
                location['distance'] = round(distance, 2)

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
    uid = request.args.get('uid')
    user_info = get_user_info(uid)
    favorite_locations = get_favorite_locations(uid)
    return render_template('favorites.html', uid=uid, user_info=user_info, locations=favorite_locations)

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
            'favorites': {
                '0': 'placeholder'  
            }
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
        return jsonify({'message': 'User logged in successfully', 'uid': user.uid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/set_favorite', methods=['POST'])
def set_favorite():
    data = request.json
    uid = session.get('user_info', {}).get('uid')
    location_id = data.get('favorite')
    
    if not uid:
        return jsonify({'status': 'error', 'message': 'User not authenticated'}), 401
    
    if not location_id:
        return jsonify({'status': 'error', 'message': 'Location ID not provided'}), 400
    
    try:
        user_ref = db.reference(f'users/{uid}/favorites')
        favorites = user_ref.get() or []
        
        if location_id not in favorites:
            favorites.append(location_id)
            user_ref.set(favorites)
            return jsonify({'status': 'added'})
        else:
            return jsonify({'status': 'already_favorite'})
    except Exception as e:
        print(f"Error adding favorite: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Database error'}), 500

@app.route('/delete_favorite', methods=['POST'])
def delete_favorite():
    data = request.json
    uid = session.get('user_info', {}).get('uid')
    location_id = data.get('favorite')
    
    if not uid:
        return jsonify({'status': 'error', 'message': 'User not authenticated'}), 401
    
    if not location_id:
        return jsonify({'status': 'error', 'message': 'Location ID not provided'}), 400
    
    try:
        user_ref = db.reference(f'users/{uid}/favorites')
        favorites = user_ref.get() or []
        
        if location_id in favorites:
            favorites.remove(location_id)
            user_ref.set(favorites)
            return jsonify({'status': 'removed'})
        else:
            return jsonify({'status': 'not_in_favorites'})
    except Exception as e:
        print(f"Error removing favorite: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Database error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
