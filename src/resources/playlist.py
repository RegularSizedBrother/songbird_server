from flask_restful import Resource

from src.models.recommendation import Recommendation

class Playlist(Resource):
    def get(self, handle_id):
        recommendation = Recommendation.query.get(handle_id)

        if(recommendation.error):
            return {"error": True}
        elif(recommendation.playlist is not None):
            return {
                "error": False,
                "playlist": recommendation.playlist,
                "genres": recommendation.genres,
            }
        else:
            return {"wait": True}
