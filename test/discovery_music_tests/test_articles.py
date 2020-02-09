from songbird_server.resources.articles import MusicGenreQuerier
import json

# Test plan(dummy version):
#   get_genres (dummy = True)
#       Cases:
#           Edge: empty array(return empty sets for positive and negative)
#                 all 5 traits
#           Routine: each of traits on its own
#                    combinations of 2, 3, and 4 traits
#                    same trait(s) but different order/capitalization (should return same results)
#   get_genre_entities_from_result
#       Edge: no results returned
#
def test_instantiation():
    querier_1 = MusicGenreQuerier()
    querier_2 = MusicGenreQuerier()

def test_get_genres_empty():
    music_querier = MusicGenreQuerier()
    assert music_querier.get_genres([], dummy=True) == ([], [])

def test_get_genres_all5():
    music_querier = MusicGenreQuerier()
    actual_genres = music_querier.get_genres(["openess to experience", "agreeableness", "extroversion", "conscientiousness", "neuroticism"], dummy=True)
    set_actual_genres = (set(actual_genres[0]),set(actual_genres[1]))
    set_expected_genres = (set(["rock", "energetic", "rebellious", "rhythmic", "conventional"]), set())
    assert set_expected_genres == set_actual_genres

def test_process_query_results():
    music_querier = MusicGenreQuerier()
    mock_file = open("songbird_server/test/discovery_music_tests/empty_dummy_query_result")
    actual_results = music_querier.get_genre_entities_from_result(json.load(mock_file))
    mock_file.close()
    expected_results = set()
    assert expected_results == actual_results



