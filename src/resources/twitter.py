from flask_restful import Resource, reqparse
from flask import request

import src.jobs.social_media as social_media
from src.resources.tweet_dumper import TwitterDumper
from src.resources.reddit_dumper import RedditDumper

from src.models.recommendation import Recommendation, db

parser = reqparse.RequestParser()
parser.add_argument('handle')
parser.add_argument('source')

class Twitter(Resource):
    def post(self):
        args = parser.parse_args()

        record = Recommendation(handle=args["handle"])
        db.session.add(record)
        db.session.commit()

        if args["source"] == "twitter":
            social_media.process_social_media(record.id, dumper_type=TwitterDumper)
        elif args["source"] == "reddit":
            social_media.process_social_media(record.id, dumper_type=RedditDumper)
        else:
            print("Invalid source %s" % args["source"])

        return {"handle_id": record.id}
