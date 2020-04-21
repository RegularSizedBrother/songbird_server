import src.app as base_app
from src.models.shared import db
from src.models.recommendation import Recommendation

from src.jobs.config import huey

import src.resources.spotify as spotify
import src.resources.tweet_genres as tweet_genres

#@huey.task()
def process_spotify(id):
    app = base_app.create_app()
    with app.app_context():
        print("### Starting spotify job for id %i ###" % id)

        recommendation = Recommendation.query.get(id)

        attributes = {
            "Openness": recommendation.openness / 100,
            "Conscientiousness": recommendation.conscientiousness / 100,
            "Extraversion": recommendation.extraversion / 100,
            "Agreeableness": recommendation.agreeableness / 100,
            "Emotional Range": recommendation.neuroticism / 100
        }

        genres = tweet_genres.get_genres_from_profile(attributes)
        playlist = spotify.generate_playlist(recommendation.handle, genres)
        recommendation.playlist = playlist
        recommendation.genres = ", ".join(genres[0])
        print(recommendation.genres)

        db.session.commit()

        print("### Finished spotify job for id %i ###" % id)
        return playlist
