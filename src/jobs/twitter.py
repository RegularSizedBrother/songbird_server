from src import app as base_app

from src.models.shared import db
from src.models.recommendation import Recommendation
from src.resources.tweet_dumper import TwitterDumper
from src.resources.personality_insights_twitter import TwitterPersonality

from src.jobs.config import huey
import src.jobs.spotify as spotify

from math import floor

@huey.task()
def process_twitter(id, max_iterations=5):
    app = base_app.create_app()
    with app.app_context():
        print("### Starting twitter job for id %i ###" % id)

        recommendation = Recommendation.query.get(id)
        dumper = TwitterDumper()
        profile_getter = TwitterPersonality()

        if not dumper.valid_user(recommendation.handle):
            recommendation.error = True
            db.session.commit()
            return

        tweets = []
        iterations = 0
        while True:
            new_tweets = dumper.get_next_tweets(recommendation.handle)

            if new_tweets is None or iterations == max_iterations:
                break

            iterations += 1

            tweets.extend(new_tweets)
            print("       Downloaded %i tweets" % len(tweets))
            profile = profile_getter.get_profile_from_tweets(tweets)
            traits = profile_getter.traits_to_vector(profile)

            if profile is not None:
                recommendation.openness = floor(traits['Openness'] * 100)
                recommendation.conscientiousness = floor(traits['Conscientiousness'] * 100)
                recommendation.extraversion = floor(traits['Extraversion'] * 100)
                recommendation.agreeableness = floor(traits['Agreeableness'] * 100)
                recommendation.neuroticism = floor(traits['Emotional range'] * 100)
            else:
                recommendation.error = True

            db.session.commit()

        recommendation.finished = True
        db.session.commit()

        if not recommendation.error:
            spotify.process_spotify(id)

        print("### Finished twitter job for id %i ###" % id)
