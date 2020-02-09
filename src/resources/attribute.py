from flask_restful import Resource

data = [
    {
        "Openness": 85.7,
        "Conscientiousness": 80.3,
        "Extraversion": 42.2,
        "Agreeableness": 67.8,
        "Emotional Range": 24.9,
    },
    {
        "Openness": 70.9,
        "Conscientiousness": 20.2,
        "Extraversion": 40.3,
        "Agreeableness": 3.2,
        "Emotional Range": 82.4,
    },
    {
        "Openness": 10.5,
        "Conscientiousness": 50.3,
        "Extraversion": 80.3,
        "Agreeableness": 47.5,
        "Emotional Range": 0.5,
    },
]

class Attribute(Resource):
    def get(self, handle_id):
        if handle_id >= 1 and handle_id <= 3:
            return data[handle_id-1]
        else:
            return {}
