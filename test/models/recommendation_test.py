from src.models.recommendation import Recommendation

def test_recommendation_model():
    recommendation = Recommendation(handle="my_handle")
    assert recommendation.handle == "my_handle"

def test_recommendation_representation():
    recommendation = Recommendation(handle="my_handle")
    assert str(recommendation) == '<Recommendation my_handle>'

