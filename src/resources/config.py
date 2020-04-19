import tweepy
import os

#https://realpython.com/twitter-bot-python-tweepy/#how-to-make-a-twitter-bot-in-python-with-tweepy

#Twitter API credentials
consumer_key = "EMrzCUAxblUXdh5CSTI73tDbB"
consumer_secret = "Pc63SQxLggiQlLRAM8bHOgxK3o4ATePMBbkSzys88LeibUlcKW"
access_key = "1222999226679881729-I1j6gUKMqu8zTapQNbRRh5FN5v2BF5"
access_secret = "T6ziZON3bTbF1W9LAwuOXNJxqBesBA1bfwAtzmIflR7jD"

def create_api():
    CONSUMER_KEY = os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    return api