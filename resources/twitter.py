from flask_restful import Resource, reqparse
from flask import request

from models.recommendation import Recommendation, db

parser = reqparse.RequestParser()
parser.add_argument('handle')

data = {
    "JeffBezos": 1,
    "Tim_Cook": 2,
    "OSUPrezDrake": 3,
}

class Twitter(Resource):
    def post(self):
        args = parser.parse_args()
        record = Recommendation(handle=args["handle"])
        return {"handle_id": data.get(args["handle"])
        # db.session.add(record)
        # db.session.commit();

        # return {"handle_id": record.id}
