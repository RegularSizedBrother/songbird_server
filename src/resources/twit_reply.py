from src.models.recommendation import Recommendation, db
from src.resources.tweet_dumper import TwitterDumper

import tweepy

class TwitterReply():
    def reply_with_spotify(self, user, playlist):
        spotify_url = playlist
        api = TwitterDumper().api
        api.update_status("@" + user + " Hello! We made a playlist based on your Twitter activity. Listen now: " + spotify_url)

