from src import app as base_app

from src.models.shared import db
from src.models.recommendation import Recommendation
from src.resources.tweet_dumper import TwitterDumper
from src.resources.reddit_dumper import RedditDumper
from src.resources.personality_analyzer import PersonalityAnalyzer
from src.resources.personality_translator import PersonalityTranslator

from src.jobs.config import huey
import src.jobs.spotify as spotify

from math import floor

#@huey.task()
def process_social_media(id, dumper_type=TwitterDumper):
    app = base_app.create_app()
    with app.app_context():
        print("### Starting social media job for id %i ###" % id)

        recommendation = Recommendation.query.get(id)

        dumper = dumper_type()
        analyzer = PersonalityAnalyzer()
        translator = PersonalityTranslator()

        if not dumper.valid_user(recommendation.handle):
            recommendation.error = True
            db.session.commit()
            return

        text = dumper.get_all_text(recommendation.handle)
        profile = analyzer.get_profile(text)
        traits = analyzer.traits_to_vector(profile)
        mbti = translator.calculator(traits)

        if profile is not None:
            recommendation.openness = floor(traits['Openness'] * 100)
            recommendation.conscientiousness = floor(traits['Conscientiousness'] * 100)
            recommendation.extraversion = floor(traits['Extraversion'] * 100)
            recommendation.agreeableness = floor(traits['Agreeableness'] * 100)
            recommendation.neuroticism = floor(traits['Emotional range'] * 100)
            recommendation.mbti = mbti
        else:
            recommendation.error = True

        recommendation.finished = True
        db.session.commit()

        if not recommendation.error:
            return spotify.process_spotify(id)

        print("### Finished social media job for id %i ###" % id)
