import src.jobs.social_media as social_media
import src.jobs.spotify as spotify
from src.resources.tweet_dumper import TwitterDumper
from src.resources.tweet_getter import TweetGetter
from src.resources.twit_reply import TwitterReply
from src.resources.twitter import Twitter
import src.app as base_app

from src.models.recommendation import Recommendation, db

class TwitterBotProcessor():
    def twitter_processor(self):
        app = base_app.create_app()
        with app.app_context():
            getter = TweetGetter()
            replier = TwitterReply()
            users = getter.get_trending_topic_users()
            user = users[0]
            record = Recommendation(handle=user)
            db.session.add(record)
            db.session.commit()
            playlist = social_media.process_social_media(record.id)
            replier.reply_with_spotify(user, playlist)

if __name__ == "__main__":
    processor = TwitterBotProcessor()
    processor.twitter_processor()

