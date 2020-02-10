from flask_restful import Resource, reqparse
from flask import request

import rq
from redis import Redis

from src.models.recommendation import Recommendation, db

parser = reqparse.RequestParser()
parser.add_argument('handle')

class Twitter(Resource):
    def post(self):
        args = parser.parse_args()

        record = Recommendation(handle=args["handle"])
        db.session.add(record)
        db.session.commit();

        queue = rq.Queue('songbird', connection=Redis.from_url('redis://'))
        job = queue.enqueue('src.jobs.twitter.process', record.id)

        return {"handle_id": record.id}
