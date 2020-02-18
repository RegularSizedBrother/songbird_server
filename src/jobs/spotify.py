# from src.app import app, db
from src.app import create_app
from src.models.shared import db
from src.models.recommendation import Recommendation

import src.resources.spotify as spotify
import src.resources.tweet_genres as tg
import time
import random
import string

app = create_app()

def process(id):
    with app.app_context():
        print("starting spotify job for id %i" % id)
        recommendation = Recommendation.query.get(id)

        t = {
            "Openness": recommendation.openness / 100,
            "Conscientiousness": recommendation.conscientiousness / 100,
            "Extraversion": recommendation.extraversion / 100,
            "Agreeableness": recommendation.agreeableness / 100,
            "Emotional Range": recommendation.neuroticism / 100
        }

        genres = tg.get_genres_from_profile(t)

        playlist = spotify.generate_playlist(recommendation.handle, genres)

        recommendation.playlist = playlist

        db.session.commit()

        print("finished spotify job for id %i" % id)
