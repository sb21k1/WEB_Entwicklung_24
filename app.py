from flask import Flask
from flask import render_template


app = Flask(__name__)

#später hier DB anbindung
locations = [
    {"name": "Location1", "description": "Beschreibung1"},
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

@app.route('/')
def index():
    return render_template('index.html', locations = locations)
