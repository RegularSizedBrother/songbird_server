import src.jobs.social_media as social_media
import src.jobs.spotify as spotify
from src.resources.tweet_dumper import TwitterDumper

from src.models.recommendation import Recommendation, db

class TwitterBotProcessor():
    def twitter_processor(self, tweet):
        record = Recommendation(handle=tweet.user.screen_name)
        db.session.add(record)
        db.session.commit()
        social_media.process_social_media(record.id, dumper_type=TwitterDumper)

