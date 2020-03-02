# import src.app as base_app
from src import app as base_app

from src.models.shared import db
from src.models.recommendation import Recommendation
from src.resources.tweet_dumper import TwitterDumper

from src.jobs.config import huey

@huey.task()
def process_twitter(id):
    app = base_app.create_app()
    with app.app_context():
        print("### Starting twitter job for id %i ###" % id)

        recommendation = Recommendation.query.get(id)
        dumper = TwitterDumper()

        if not dumper.valid_user(recommendation.handle):
            recommendation.error = True
            db.session.commit()
            return

        dumper.get_all_tweets(id)

        print("### Finished twitter job for id %i ###" % id)
