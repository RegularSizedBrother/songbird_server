#!/usr/bin/env python
# encoding: utf-8
#Code taken from: https://gist.github.com/yanofsky/5436496

from src.models.recommendation import Recommendation, db

import tweepy #https://github.com/tweepy/tweepy
import csv
import sys

#Twitter API credentials
consumer_key = "EMrzCUAxblUXdh5CSTI73tDbB"
consumer_secret = "Pc63SQxLggiQlLRAM8bHOgxK3o4ATePMBbkSzys88LeibUlcKW"
access_key = "1222999226679881729-I1j6gUKMqu8zTapQNbRRh5FN5v2BF5"
access_secret = "T6ziZON3bTbF1W9LAwuOXNJxqBesBA1bfwAtzmIflR7jD"


class TwitterDumper:
    def __init__(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)
        self.max_id = None

    def valid_user(self, handle):
        try:
            self.api.get_user(handle)
            return True
        except:
            return False

    def get_next_tweets(self, handle, count=200):
        try:
            if self.max_id is None:
                print("Getting tweets for %s" % handle)
                tweets = self.api.user_timeline(screen_name=handle, count=count)
            else:
                print("Getting tweets before %s" % (self.max_id))
                tweets = self.api.user_timeline(screen_name=handle, count=count, max_id=self.max_id)

            self.max_id = tweets[-1].id - 1
            return [tweet.text for tweet in tweets]

        except:
            print("Error: Invalid user")
            return

    def get_all_tweets(self, handle):
        alltweets = []
        while True:
            new_tweets = self.get_next_tweets(handle)

            if new_tweets is none:
                break

            tweets.extend(new_tweets)

        return [tweet.text for tweet in tweets]

    def write_tweets_to_file(self, filename, handle):
        tweets = self.get_all_tweets(handle)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(tweets)

if __name__ == '__main__':
    getter = TwitterDumper()

    if len(sys.argv) == 2:
        getter.write_tweets_to_file("tmp/%s.txt" % sys.argv[1], sys.argv[1])
    else:
        print("Error: enter one username")
