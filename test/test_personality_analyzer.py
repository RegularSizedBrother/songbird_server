from src.resources.personality_analyzer import PersonalityAnalyzer

def test_traits_to_vector():
    analyzer = PersonalityAnalyzer()
    traits = {
        "personality": [
            { "name": "test", "percentile": 1 }
        ]
    }

    vector = analyzer.traits_to_vector(traits)
    assert vector["test"] == 1

def test_get_profile_not_enough_words():
    analyzer = PersonalityAnalyzer()
    words = ["test", "test"]
    assert analyzer.get_profile(words) is None

def test_get_profile():
    analyzer = PersonalityAnalyzer()
    words = ["test" for i in range(100)]
    assert analyzer.get_profile(words) is not None

