from resources.attribute import Attribute

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

def test_basic():
    assert 1 == 1

def test_attribute_1():
    index = 1
    curr = Attribute()
    assert data[index-1] == curr.get(index)

def test_attribute_2():
    index = 2
    curr = Attribute()
    assert data[index-1] == curr.get(index)

def test_attribute_3():
    index = 3
    curr = Attribute()
    assert data[index-1] == curr.get(index)

def test_attribute_0():
    empty_dict = {}
    index = 0
    curr = Attribute()
    assert curr.get(index) == empty_dict

def test_attribute_4():
    empty_dict = {}
    index = 4
    curr = Attribute()
    assert curr.get(index) == empty_dict
