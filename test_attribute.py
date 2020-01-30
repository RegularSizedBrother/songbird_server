from resources.attribute import Attribute

def test_handle():
    data = {
        "Openness": 85.7,
        "Conscientiousness": 80.3,
        "Extraversion": 42.2,
        "Agreeableness": 67.8,
        "Emotional Range": 24.9,
    }
    assert Attribute.get(1) == data