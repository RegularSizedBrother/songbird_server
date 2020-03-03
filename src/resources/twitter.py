from flask_restful import Resource, reqparse
from flask import request

import src.jobs.twitter as twitter

from src.models.recommendation import Recommendation, db

parser = reqparse.RequestParser()
parser.add_argument('handle')

class Twitter(Resource):
    def post(self):
        args = parser.parse_args()

        record = Recommendation(handle=args["handle"])
        db.session.add(record)
        db.session.commit()

        twitter.process_twitter(record.id, max_iterations=7)

        return {"handle_id": record.id}
