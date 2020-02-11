from src.app import app, db
from src.models.recommendation import Recommendation
from src.resources.tweet_dumper import TwitterDumper
from src.resources.personality_insights_twitter import TwitterPersonality

import rq
from redis import Redis
from math import floor

import time
import random

def process(id):
    with app.app_context():
        print("starting twitter job for id %i" % id)

        recommendation = Recommendation.query.get(id)

        tw = TwitterDumper()
        tw.get_all_tweets(recommendation.handle)

        tp = TwitterPersonality()
        p = tp.get_profile("%s_tweets.csv" % recommendation.handle)
        v = tp.traits_to_vector(p)

        recommendation.openness = floor(v['Openness'] * 100)
        recommendation.conscientiousness = floor(v['Conscientiousness'] * 100)
        recommendation.extraversion = floor(v['Extraversion'] * 100)
        recommendation.agreeableness = floor(v['Agreeableness'] * 100)
        recommendation.neuroticism = floor(v['Emotional range'] * 100)

        db.session.commit()

        print("finished twitter job for id %i" % id)

        queue = rq.Queue('songbird', connection=Redis.from_url('redis://'))
        job = queue.enqueue('src.jobs.spotify.process', id)
