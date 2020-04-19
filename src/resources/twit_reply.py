from src.resources.config import create_api
from src.models.recommendation import Recommendation, db

import tweepy

def reply_with_spotify(api, tweet):
    username = tweet.user.screen_name
    record = Recommendation(handle=username)
    spotify_url = record.playlist

    api.update_status(
        status="Hello! We made a playlist based on your Twitter activity. Listen now: {spotify_url}",
        in_reply_to_status_id=tweet.id,
    )

