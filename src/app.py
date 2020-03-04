from flask import Flask
from flask_cors import CORS

from src.models.shared import db
from src.resources.api import api

def create_app():
    app = Flask('songbird')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    CORS(app)

    db.init_app(app)
    api.init_app(app)

    return app

