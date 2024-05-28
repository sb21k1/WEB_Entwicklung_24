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
theme_tags = [
    {"name": "urban"}, {"name": "park"},{"name": "café"},{"name": "restaurant"},{"name": "library"},{"name": "museum"},{"name": "historical"},{"name": "modern"},
    {"name": "bridge"},{"name": "street"},{"name": "train station"},{"name": "subway"},{"name": "harbor"},{"name": "rooftop"},{"name": "garden"},
    {"name": "castle"},{"name": "market"},{"name": "warehouse"},{"name": "studio"},{"name": "theater"},{"name": "concert hall"},{"name": "mall"},{"name": "temple"},
    {"name": "church"},{"name": "monument"},{"name": "ruins"},{"name": "hotel"},{"name": "university"},{"name": "office"},
    {"name": "zoo"}
]


@app.route('/')
def index():
    return render_template('index.html', locations = locations, theme_tags = theme_tags)
