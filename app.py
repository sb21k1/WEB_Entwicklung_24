from flask import Flask, request, jsonify, redirect, url_for, render_template, session
from firebase_admin import credentials, initialize_app, db, storage
import firebase_admin
import requests

app = Flask(__name__)
selected_tags = []

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
                    'tags': item.get('tags', [])  
                })
    print(locations)
    return locations


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
    global selected_tags
    locations = fetch_data()

    if selected_tags:
        filtered_locations = [
            loc for loc in locations
            if any(tag.lower().strip() in (tag_name.lower().strip() for tag_name in loc['tags'])
            for tag in selected_tags)
        ]
    else:
        filtered_locations = locations

    images = fetch_images_for_locations(filtered_locations)
    image_mapping = {img['name']: img['image_urls'] for img in images}

    for location in filtered_locations:
        location['images'] = image_mapping.get(location['name'], [])

    uid = request.args.get('uid')
    user_info = get_user_info(uid)

    return render_template('index.html', uid=uid, user_info=user_info, locations=filtered_locations, tags=tags)

@app.route('/recieveTags', methods=['POST'])
def recieveTags():
    global selected_tags
    if request.method == 'POST':
        data = request.json
        selected_tags = data.get('tags', [])
        print('Ausgewählte Tags:', selected_tags)
        return jsonify({'status': 'success'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    return render_template('registration.html')

def get_user_info(uid):
    ref = db.reference(f'users/{uid}')
    return ref.get()

if __name__ == '__main__':
    app.run(debug=True)
