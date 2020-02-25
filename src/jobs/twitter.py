import src.app as base_app

from src.models.shared import db
from src.models.recommendation import Recommendation
from src.resources.tweet_dumper import TwitterDumper
from src.resources.personality_insights_twitter import TwitterPersonality

from src.jobs.config import huey
import src.jobs.spotify as spotify

from math import floor

@huey.task()
def process_twitter(id):
    app = base_app.create_app()
    with app.app_context():
        print("starting twitter job for id %i" % id)

        recommendation = Recommendation.query.get(id)

        dumper = TwitterDumper()
        status = dumper.get_all_tweets(recommendation.handle)

        if(status != "error"):
            profile_getter = TwitterPersonality()
            profile = profile_getter.get_profile("tmp/%s_tweets.csv" % recommendation.handle)

            if profile is not None:
                traits = profile_getter.traits_to_vector(profile)

                recommendation.openness = floor(traits['Openness'] * 100)
                recommendation.conscientiousness = floor(traits['Conscientiousness'] * 100)
                recommendation.extraversion = floor(traits['Extraversion'] * 100)
                recommendation.agreeableness = floor(traits['Agreeableness'] * 100)
                recommendation.neuroticism = floor(traits['Emotional range'] * 100)

                spotify.process_spotify(id)
            else:
                recommendation.error = True
        else:
            recommendation.error = True

        db.session.commit()

        print("finished twitter job for id %i" % id)
