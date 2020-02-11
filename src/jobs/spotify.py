from src.app import app, db
from src.models.recommendation import Recommendation

import src.resources.spotify as spotify

import time
import random
import string

def process(id):
    with app.app_context():
        print("starting spotify job for id %i" % id)
        recommendation = Recommendation.query.get(id)

        time.sleep(5) # simulate processing

        playlist = spotify.generate_playlist(recommendation.handle, ())

        recommendation.playlist = plalist

        db.session.commit()

        print("finished spotify job for id %i" % id)
