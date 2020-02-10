from flask_restful import Resource

from src.models.recommendation import Recommendation

class Attribute(Resource):
    def get(self, handle_id):
        recommendation = Recommendation.query.get(handle_id)

        if(recommendation.error):
            return {"error": True}
        elif(recommendation.openness is not None):
            return {
                "error": False,
                "data": {
                    "Openness": recommendation.openness,
                    "Conscientiousness": recommendation.conscientiousness,
                    "Extraversion": recommendation.extraversion,
                    "Agreeableness": recommendation.agreeableness,
                    "Emotional Range": recommendation.neuroticism,
                }
            }
        else:
            return {"wait": True}
