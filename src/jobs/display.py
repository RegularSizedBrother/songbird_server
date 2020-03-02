from src import app as base_app

from src.jobs.config import huey
from src.models.recommendation import Recommendation, db

from src.resources.personality_insights_twitter import TwitterPersonality

from math import floor

@huey.task()
def process_display(id, tweets):
    app = base_app.create_app()
    with app.app_context():
        recommendation = Recommendation.query.get(id)

        profile_getter = TwitterPersonality()
        profile = profile_getter.get_profile_from_tweets(tweets)

        if profile is not None:
            traits = profile_getter.traits_to_vector(profile)

            recommendation.openness = floor(traits['Openness'] * 100)
            recommendation.conscientiousness = floor(traits['Conscientiousness'] * 100)
            recommendation.extraversion = floor(traits['Extraversion'] * 100)
            recommendation.agreeableness = floor(traits['Agreeableness'] * 100)
            recommendation.neuroticism = floor(traits['Emotional range'] * 100)

            db.session.commit()
        else:
            recommendation.error = True
