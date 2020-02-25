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

    def test_generate_playlist_pos_seeds_live(self):
        test_url = spotify.generate_playlist(handle='@LiveMusic', seeds=(["cheese", "rock", "liveness"], []))
        expected_prefix = spotify_config.PLAYLIST_PREFIX
        assert test_url.find(expected_prefix) == 0
        assert len(test_url) > len(expected_prefix)
        sp = spotipy.Spotify(spotify.get_access_token())
        test_playlist_tracks = sp.playlist_tracks(playlist_id=test_url)
        assert len(test_playlist_tracks.get('items')) == spotify_config.PLAYLIST_SIZE
        sp.user_playlist_unfollow(user=spotify_config.SONGBIRD_USER_ID, playlist_id=test_url[len(
            spotify_config.PLAYLIST_PREFIX):])

    def test_generate_playlist_neg_seeds_neg_feature(self):
        test_url = spotify.generate_playlist(handle='@LowEnergy', seeds=(["cheese", "rock"], ["energy"]))
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

    def test_generate_playlist_pos_seeds_genres_some_invalid(self):
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

    def test_generate_playlist_lots_of_seeds(self):
        test_url = spotify.generate_playlist(handle='@ManySeeds', seeds=(
        ["cheese",  "valence", "loudness", "test", "Franklin", "rock", "hip-hop", "jazz", "danaceability"],
        ["classical", "loudness", "energy", "wow", "acousticness"]))
        expected_prefix = spotify_config.PLAYLIST_PREFIX
        assert test_url.find(expected_prefix) == 0
        assert len(test_url) > len(expected_prefix)
        sp = spotipy.Spotify(spotify.get_access_token())
        test_playlist_tracks = sp.playlist_tracks(playlist_id=test_url)
        assert len(test_playlist_tracks.get('items')) == spotify_config.PLAYLIST_SIZE
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

    def test_filter_seeds_duplicate_genres_no_feats(self):
        seeds = ['rock', 'rock', 'pop']
        genres = []
        features = []
        expected_genres = ['rock', 'pop']
        expected_features = []

        spotify.filter_seeds(seeds, genres, features)

        assert genres == expected_genres
        assert features == expected_features

    def test_filter_seeds_no_seeds(self):
        seeds = []
        genres = []
        features = []
        expected_genres = []
        expected_features = []

        spotify.filter_seeds(seeds, genres, features)

        assert genres == expected_genres
        assert features == expected_features

    def test_filter_seeds_only_genres_fake_terms(self):
        seeds = ['cheese', 'music bad', 0, 'seventy-two', 'rock', 'hip-hop', 'fake']
        genres = []
        features = []
        expected_genres = ['rock', 'hip-hop']
        expected_features = []

        spotify.filter_seeds(seeds, genres, features)

        assert genres == expected_genres
        assert features == expected_features

    def test_filter_rap(self):
        seeds = ['cheese', 'rap', 0, 'seventy-two', 'rock', 'jazz', 'fake']
        genres = []
        features = []
        expected_genres = ['hip-hop', 'rock', 'jazz']
        expected_features = []

        spotify.filter_seeds(seeds, genres, features)

        assert genres == expected_genres
        assert features == expected_features

    def test_filter_rap_duplicate(self):
        seeds = ['cheese', 'rap', 'hip-hop', 'seventy-two', 'rock', 'jazz', 'fake']
        genres = []
        features = []
        expected_genres = ['hip-hop', 'rock', 'jazz']
        expected_features = []

        spotify.filter_seeds(seeds, genres, features)

        assert genres == expected_genres
        assert features == expected_features

    def test_filter_rap_duplicate(self):
        seeds = ['cheese', 'rap', 'hip-hop', 'seventy-two', 'energy', 'rock', 'jazz', 'fake', 'valence']
        genres = []
        features = []
        expected_genres = ['hip-hop', 'rock', 'jazz']
        expected_features = ['energy', 'valence']

        spotify.filter_seeds(seeds, genres, features)

        assert genres == expected_genres
        assert features == expected_features

    def test_filter_duplicate_feats(self):
        seeds = ['cheese', 'rap', 'hip-hop', 'energy', 'seventy-two', 'energy', 'rock', 'jazz', 'fake', 'valence']
        genres = []
        features = []
        expected_genres = ['hip-hop', 'rock', 'jazz']
        expected_features = ['energy', 'valence']

        spotify.filter_seeds(seeds, genres, features)

        assert genres == expected_genres
        assert features == expected_features

    def test_filter_duplicate_in_prev_feats(self):
        seeds = ['cheese', 'rap', 'hip-hop', 'seventy-two', 'energy', 'rock', 'jazz', 'fake', 'valence']
        prev_features = ['valence', 'loudness']
        genres = []
        features = []
        expected_genres = ['hip-hop', 'rock', 'jazz']
        expected_features = ['energy']
        expected_prev_features = ['loudness']

        spotify.filter_seeds(seeds, genres, features, prev_features=prev_features)

        assert genres == expected_genres
        assert features == expected_features
        assert prev_features == expected_prev_features

    def test_recommendation_sorcery(self):
        genres = ['rock', 'pop']

        access_token = spotify.get_access_token()

        sp = spotipy.Spotify(access_token)

        # Can use the 'dict' object to pass in named arguments (keyword args)
        # KEY: name of parameter
        # VALUE: value of parameter
        # MUST USE ** to 'unpack' dict into parameter form
        magic = dict(seed_genres=genres, limit=spotify_config.PLAYLIST_SIZE)
        test = 'target_valence'
        magic[test] = 0.8
        test_recs = sp.recommendations(**magic)

        assert test_recs is not None
        assert len(test_recs.get('tracks')) == spotify_config.PLAYLIST_SIZE


if __name__ == '__main__':
    unittest.main()
