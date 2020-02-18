from flask_restful import Resource, reqparse
from flask import request

from src.jobs.twitter import process

from src.models.shared import db
from src.models.recommendation import Recommendation

parser = reqparse.RequestParser()
parser.add_argument('handle')

class Twitter(Resource):
    def post(self):
        args = parser.parse_args()

        record = Recommendation(handle=args["handle"])
        db.session.add(record)
        db.session.commit();

        process(record.id)

        return {"handle_id": record.id}
