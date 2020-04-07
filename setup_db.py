from src.models.shared import db
from src.app import create_app, create_testing_app

app = create_app()
with app.app_context():
    db.create_all()

testing_app = create_testing_app()
with testing_app.app_context():
    db.create_all()
