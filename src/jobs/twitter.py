import src.app as a

from src.models.shared import db
from src.models.recommendation import Recommendation
from src.resources.tweet_dumper import TwitterDumper
from src.resources.personality_insights_twitter import TwitterPersonality

from src.jobs.config import huey
import src.jobs.spotify as spotify

from math import floor

@huey.task()
def process_twitter(id):
    app = a.create_app()
    with app.app_context():
        print("starting twitter job for id %i" % id)

        recommendation = Recommendation.query.get(id)

        tw = TwitterDumper()
        status = tw.get_all_tweets(recommendation.handle)

        if(status != "error"):
            tp = TwitterPersonality()
            p = tp.get_profile("tmp/%s_tweets.csv" % recommendation.handle)

            if p is not None:
                v = tp.traits_to_vector(p)

                recommendation.openness = floor(v['Openness'] * 100)
                recommendation.conscientiousness = floor(v['Conscientiousness'] * 100)
                recommendation.extraversion = floor(v['Extraversion'] * 100)
                recommendation.agreeableness = floor(v['Agreeableness'] * 100)
                recommendation.neuroticism = floor(v['Emotional range'] * 100)

                db.session.commit()

                spotify.process_spotify(id)
            else:
                recommendation.error = True
        else:
            recommendation.error = True

        print("finished twitter job for id %i" % id)
