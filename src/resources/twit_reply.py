from src.models.recommendation import Recommendation, db

import tweepy

class TwitterReply():
    def reply_with_spotify(self, api, user):
        records = Recommendation.query.filter_by(handle=user).all()
        record = records[-1]
        spotify_url = record.playlist

        api.update_status(
            "@{user} Hello! We made a playlist based on your Twitter activity. Listen now: {spotify_url}"
        )

