from flask_restful import Resource, reqparse
from flask import request

parser = reqparse.RequestParser()
parser.add_argument('handle')

data = {
    "JeffBezos": 1,
    "Tim_Cook": 2,
    "OSUPrezDrake": 3,
}

class BobTwitter(Resource):
    def post(self):
        args = parser.parse_args()
        print(args)
        return {"handle_id": data.get(args["handle"])}
        #return {"handle_id": data[args["handle"]]}
