from src.app import app, db
from src.models.recommendation import Recommendation

import time
import random
import string

def process(id):
    with app.app_context():
        recommendation = Recommendation.query.get(id)

        time.sleep(5)

        letters = string.ascii_lowercase
        recommendation.playlist = ''.join(random.choice(letters) for i in range(30))

        db.session.commit()
