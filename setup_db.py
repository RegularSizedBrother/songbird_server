from src.models.shared import db
from src.app import create_app

app = create_app()
with app.app_context():
    db.create_all()
