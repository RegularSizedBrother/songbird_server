import unittest
from src.resources import spotify, spotify_config
import spotipy

class Spotify_Unit_Tests(unittest.TestCase):
    def test_get_access_token(self):
        test_access_token = spotify.get_access_token()
        print(len(test_access_token))
        print(test_access_token)
        assert test_access_token is not None
        #assert len(test_access_token) == spotify_config.ACCESS_TOKEN_LEN

    def test_generate_playlist_no_params(self):
        test_url = spotify.generate_playlist()
        expected_prefix = spotify_config.PLAYLIST_PREFIX
        assert test_url.find(expected_prefix) == 0
        assert len(test_url) > len(expected_prefix)
        sp = spotipy.Spotify(spotify.get_access_token())
        test_playlist_tracks = sp.playlist_tracks(playlist_id=test_url)
        correct_tracks = spotify_config.SOUNDS_OF_SILENCE
        assert len(test_playlist_tracks.get('items')) == 3
        for test_track in test_playlist_tracks.get('items'):
            assert test_track.get('track').get('id') in correct_tracks
        sp.user_playlist_unfollow(user=spotify_config.SONGBIRD_USER_ID, playlist_id=test_url[len(
            spotify_config.PLAYLIST_PREFIX):])

    def test_generate_playlist_only_handle(self):
        test_url = spotify.generate_playlist(handle='@SampleHandle')
        expected_prefix = spotify_config.PLAYLIST_PREFIX
        assert test_url.find(expected_prefix) == 0
        assert len(test_url) > len(expected_prefix)
        sp = spotipy.Spotify(spotify.get_access_token())
        test_playlist_tracks = sp.playlist_tracks(playlist_id=test_url)
        correct_tracks = spotify_config.SOUNDS_OF_SILENCE
        assert len(test_playlist_tracks.get('items')) == 3
        for test_track in test_playlist_tracks.get('items'):
            assert test_track.get('track').get('id') in correct_tracks
        sp.user_playlist_unfollow(user=spotify_config.SONGBIRD_USER_ID, playlist_id=test_url[len(
            spotify_config.PLAYLIST_PREFIX):])

    def test_generate_playlist_pos_seeds_under_5_valid_only_genres(self):
        test_url = spotify.generate_playlist(handle='@SomePositiveSeeds', seeds=(["rock", "hip-hop"], []))
        expected_prefix = spotify_config.PLAYLIST_PREFIX
        assert test_url.find(expected_prefix) == 0
        assert len(test_url) > len(expected_prefix)
        sp = spotipy.Spotify(spotify.get_access_token())
        test_playlist_tracks = sp.playlist_tracks(playlist_id=test_url)
        assert len(test_playlist_tracks.get('items')) == spotify_config.PLAYLIST_SIZE
        sp.user_playlist_unfollow(user=spotify_config.SONGBIRD_USER_ID, playlist_id=test_url[len(
            spotify_config.PLAYLIST_PREFIX):])


    def test_generate_playlist_pos_seeds_under_5_invalid(self):
        test_url = spotify.generate_playlist(handle='@SomePositiveInvalidSeeds', seeds=(["cheese", "rock", "hip-hop", "valence"], []))
        expected_prefix = spotify_config.PLAYLIST_PREFIX
        assert test_url.find(expected_prefix) == 0
        assert len(test_url) > len(expected_prefix)
        sp = spotipy.Spotify(spotify.get_access_token())
        test_playlist_tracks = sp.playlist_tracks(playlist_id=test_url)
        assert len(test_playlist_tracks.get('items')) == spotify_config.PLAYLIST_SIZE
        sp.user_playlist_unfollow(user=spotify_config.SONGBIRD_USER_ID, playlist_id=test_url[len(
            spotify_config.PLAYLIST_PREFIX):])

    def test_generate_playlist_pos_seeds_over_5_invalid(self):
        test_url = spotify.generate_playlist(handle='@ManyPositiveInvalidSeeds', seeds=(["valence", "rock", "hip-hop", "cheese", "classical", "disco", "electronic", "folk", "funk", "metal"], []))
        expected_prefix = spotify_config.PLAYLIST_PREFIX
        assert test_url.find(expected_prefix) == 0
        assert len(test_url) > len(expected_prefix)
        sp = spotipy.Spotify(spotify.get_access_token())
        test_playlist_tracks = sp.playlist_tracks(playlist_id=test_url)
        assert len(test_playlist_tracks.get('items')) == spotify_config.PLAYLIST_SIZE
        sp.user_playlist_unfollow(user=spotify_config.SONGBIRD_USER_ID, playlist_id=test_url[len(
            spotify_config.PLAYLIST_PREFIX):])

    def test_generate_playlist_pos_seeds_genres_all_invalid(self):
        test_url = spotify.generate_playlist(handle='@AllInvalidSeeds', seeds=(
        ["cheese",  "valence", "loudness", "test", "Franklin"], []))
        expected_prefix = spotify_config.PLAYLIST_PREFIX
        assert test_url.find(expected_prefix) == 0
        assert len(test_url) > len(expected_prefix)
        sp = spotipy.Spotify(spotify.get_access_token())
        test_playlist_tracks = sp.playlist_tracks(playlist_id=test_url)
        correct_tracks = spotify_config.SOUNDS_OF_SILENCE
        assert len(test_playlist_tracks.get('items')) == 3
        for test_track in test_playlist_tracks.get('items'):
            assert test_track.get('track').get('id') in correct_tracks
        sp.user_playlist_unfollow(user=spotify_config.SONGBIRD_USER_ID, playlist_id=test_url[len(
            spotify_config.PLAYLIST_PREFIX):])

    def test_get_recommendations_only_genres(self):
        genres = ['rock', 'pop']
        pos_features = []
        neg_features = []
        test_recs = spotify.get_recommendations(genres=genres, pos_features=pos_features, neg_features=neg_features)
        assert test_recs is not None
        assert len(test_recs.get('tracks')) == spotify_config.PLAYLIST_SIZE

    def test_get_recommendations_no_params(self):
        test_recs = spotify.get_recommendations()
        correct_track_ids = spotify_config.SOUNDS_OF_SILENCE
        assert test_recs is not None
        assert len(test_recs.get('tracks')) == 3
        for test_track in test_recs.get('tracks'):
            assert test_track.get('id') in correct_track_ids


if __name__ == '__main__':
    unittest.main()
