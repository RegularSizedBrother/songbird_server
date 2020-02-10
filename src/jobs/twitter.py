from src.app import app, db
from src.models.recommendation import Recommendation

import rq
from redis import Redis

import time
import random

def process(id):
    with app.app_context():
        print("starting twitter job for id %i" % id)

        recommendation = Recommendation.query.get(id)

        time.sleep(5) # simulate processing

        recommendation.openness = random.randint(0, 100)
        recommendation.conscientiousness = random.randint(0, 100)
        recommendation.extraversion = random.randint(0, 100)
        recommendation.agreeableness = random.randint(0, 100)
        recommendation.neuroticism = random.randint(0, 100)

        db.session.commit()

        print("finished twitter job for id %i" % id)

        queue = rq.Queue('songbird', connection=Redis.from_url('redis://'))
        job = queue.enqueue('src.jobs.spotify.process', id)
