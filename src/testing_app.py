from flask import Flask
from src.models.shared import db

def create_testing_app():
    app = Flask('songbird_test')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songbird_test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app

