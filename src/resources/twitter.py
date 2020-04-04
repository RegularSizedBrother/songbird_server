from flask_restful import Resource, reqparse
from flask import request

from datetime import datetime, timedelta

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

        prev_recs = Recommendation.query.filter_by(handle=args["handle"]).all()
        record = None

        if self.should_use_cache(prev_recs):
            print("Using cached result for %s" % args["handle"])
            record = prev_recs[-1]
        else:
            record = Recommendation(handle=args["handle"])
            db.session.add(record)
            db.session.commit()

            if args["source"] == "twitter":
                social_media.process_social_media(record.id, dumper_type=TwitterDumper)
            elif args["source"] == "reddit":
                social_media.process_social_media(record.id, dumper_type=RedditDumper)
            else:
                print("Invalid source %s" % args["source"])

            id = record.id

        return {"handle_id": record.id}

    def should_use_cache(self, prev_recs):
        if(len(prev_recs) == 0):
            return False

        latest_rec = prev_recs[-1]
        return datetime.utcnow() - timedelta(days=7) < latest_rec.created_at
