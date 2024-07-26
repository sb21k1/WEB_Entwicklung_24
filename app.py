from flask import Flask, request, render_template
from firebase_admin import credentials, initialize_app, db
import firebase_admin

app = Flask(__name__)

#später hier DB anbindung
locations = [
    {"name": "Location1", "description": "Beschreibung"},
    {"name": "Location2", "description": "Beschreibung2"},
    {"name": "Location3", "description": "Beschreibung3"},
    {"name": "Location1", "description": "Beschreibung1"},
    {"name": "Location2", "description": "Beschreibung2"},
    {"name": "Location3", "description": "Beschreibung3"},
    {"name": "Location1", "description": "Beschreibung1"},
    {"name": "Location2", "description": "Beschreibung2"},
    {"name": "Location3", "description": "Beschreibung3"},
    {"name": "Location1", "description": "Beschreibung1"},
    {"name": "Location2", "description": "Beschreibung2"},
    {"name": "Location3", "description": "Beschreddibung3"}
    
]
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
    
    {"type": "type_tags", "name": "Historisch"},
    {"type": "type_tags", "name": "Modern"},
    {"type": "type_tags", "name": "Industriell"},
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
cred = credentials.Certificate("serviceKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://places-de11a-default-rtdb.firebaseio.com'
})


@app.route('/')
def index():
 uid = request.args.get('uid')
 user_info = get_user_info(uid)
 return render_template('index.html', uid=uid, user_info=user_info, locations=locations,tags=tags)


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    return render_template('login.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    return render_template('registration.html')

def get_user_info(uid):
    ref = db.reference(f'users/{uid}')
    return ref.get()

def get_locations(uid):
    # Ваша логика для получения локаций по UID
    pass

if __name__ == '__main__':
    app.run(debug=True)
