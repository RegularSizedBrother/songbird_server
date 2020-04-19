from src.resources.config import create_api
from src.models.recommendation import Recommendation, db

import tweepy

class TwitterReply():
    def reply_with_spotify(api, tweet):
        username = tweet.user.screen_name
        records = Recommendation.query.filter_by(handle=username).all()
        record = records[-1]
        spotify_url = record.playlist

        api.update_status(
            status="Hello! We made a playlist based on your Twitter activity. Listen now: {spotify_url}",
            in_reply_to_status_id=tweet.id,
        )

