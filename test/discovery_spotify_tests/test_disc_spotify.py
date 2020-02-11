from src.resources.articles import MusicGenreQuerier
from src.resources.spotify import SpotifyParser

def test_regular_genres():
    query = MusicGenreQuerier()
    spotify = SpotifyParser()
    user = "@BarackObama"
    traits = ["Openness to experience", "Agreeableness"]
    genres = query.get_genres(traits)
    link = spotify.generate_playlist(user,genres)
    assert link is not None 

def test_no_valid_genres():
    spotify = SpotifyParser()
    user = "@BarackObama"
    genres = ["cheese", "tamago", "yakuza"]
    link = spotify.generate_playlist(user,genres)
    assert link == ""

def test_many_valid_genres():
    spotify = SpotifyParser()
    user = "@BarackObama"
    genres = ["rock", "dance", "reggae", "anime", "jazz", "classical", "electronic", "funk", "R&B", "techno", "metal", "disco"]
    link = spotify.generate_playlist(user,genres)
    assert link is not None

def test_empty_genres():
    spotify = SpotifyParser()
    user = "@BarackObama"
    genres = []
    link = spotify.generate_playlist(user,genres)
    assert link == ""