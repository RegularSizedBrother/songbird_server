from src.resources.bob.attribute import BobAttribute
from mock import mock

data = [
    {
        "error": False,
        "data": {
            "Openness": 85.7,
            "Conscientiousness": 80.3,
            "Extraversion": 42.2,
            "Agreeableness": 67.8,
            "Emotional Range": 24.9,
        }
    },
    {
        "error": False,
        "data": {
            "Openness": 70.9,
            "Conscientiousness": 20.2,
            "Extraversion": 40.3,
            "Agreeableness": 3.2,
            "Emotional Range": 82.4,
        }
    },
    {
        "error": False,
        "data": {
            "Openness": 10.5,
            "Conscientiousness": 50.3,
            "Extraversion": 80.3,
            "Agreeableness": 47.5,
            "Emotional Range": 0.5,
        }
    },
]

def test_attribute_1():
    with mock.patch('random.randint', return_value=1):
        index = 1
        curr = BobAttribute()
        assert data[index-1] == curr.get(index)

def test_attribute_2():
    with mock.patch('random.randint', return_value=1):
        index = 2
        curr = BobAttribute()
        assert data[index-1] == curr.get(index)

def test_attribute_3():
    with mock.patch('random.randint', return_value=1):
        index = 3
        curr = BobAttribute()
        assert data[index-1] == curr.get(index)

def test_wait():
    with mock.patch('random.randint', return_value=0):
        index = 1
        curr = BobAttribute()
        assert curr.get(index) == {"wait": True}

def test_error():
    with mock.patch('random.randint', return_value=1):
        index = 0
        curr = BobAttribute()
        assert curr.get(index) == {"error": True}
