'''
This file contains all the tools and functions needed for spotify integration.
'''

import spotipy
from spotipy import oauth2
from src.resources import spotify_config


# Request permissions?
# Not sure how this works yet, but not necessary for final product


# May? require editing if/when we want to allow other users, but this should keep us logged into the Songbird account
def get_access_token():
    sp_oauth = oauth2.SpotifyOAuth(spotify_config.SPOTIFY_CLIENT_ID, spotify_config.SPOTIFY_CLIENT_SECRET, spotify_config.SPOTIFY_REDIRECT_URI, scope=spotify_config.SCOPE, cache_path=spotify_config.CACHE)
    token_info = sp_oauth.get_cached_token()

    if token_info:
        access_token = token_info['access_token']
    else:
        access_token = spotipy.util.prompt_for_user_token(spotify_config.SONGBIRD_USER_EMAIL, scope=spotify_config.SCOPE, client_id=spotify_config.SPOTIFY_CLIENT_ID, client_secret=spotify_config.SPOTIFY_CLIENT_SECRET, redirect_uri='http://localhost:5000', cache_path=spotify_config.CACHE)

    return access_token


# Get recommendations - returns an array of tracks based on genres and traits - PRE SORTED
# REQUIRES 5 OR LESS GENRES - USE filter_seeds TO QUALITY CHECK
def get_recommendations(genres=[], pos_features=[], neg_features=[]):
    access_token = get_access_token()

    if access_token:
        sp = spotipy.Spotify(access_token)

        if len(genres) == 0:
            # If no genres and no traits, return 'The Sounds of Silence'
            return sp.tracks(spotify_config.SOUNDS_OF_SILENCE)
            #return sp.recommendations(seed_tracks=SOUNDS_OF_SILENCE)

        # Can use the 'dict' object to pass in named arguments (keyword args)
        # KEY: name of parameter
        # VALUE: value of parameter
        # MUST USE ** to 'unpack' dict into parameter form
        # example in 'test_spotify_unittest.py' - search 'sorcery'
        parameters = dict(seed_genres=genres, limit=spotify_config.PLAYLIST_SIZE)

        for pos in pos_features:
            if (pos in spotify_config.RATIO_FEATURES):
                parameters['target_' + pos] = 0.95

        for neg in neg_features:
            if (neg in spotify_config.RATIO_FEATURES):
                parameters['target_' + neg] = 0.05

        return sp.recommendations(**parameters)


# Create playlist for the specified user
# Name should be the name of the playlist (the twitter handle)
# User should be the user Id, defaulting to the Songbird user id - TBD
def create_playlist(name, user=None,):
    access_token = get_access_token()

    # Default to songbird user
    user_id = user
    if user_id is None:
        user_id = spotify_config.SONGBIRD_USER_ID

    pl_description = "Songbird created a playlist based on the Twitter handle " + name + "."

    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.user_playlist_create(user_id, name, description=pl_description)
        return results


# Add tracks to a specified playlist
# user parameter defaults to Songbird user, but might need changing for eventual login
def add_tracks(playlist, tracks, user=None):
    access_token = get_access_token()

    # The objects returned by other functions are dictionaries
    playlist_id = playlist.get('id')
    track_ids = [];
    tracks_list = tracks.get('tracks')
    for track in tracks_list:
        track_ids.append(track.get('id'))

    if access_token:
        sp = spotipy.Spotify(access_token)
        results = sp.user_playlist_add_tracks(spotify_config.SONGBIRD_USER_ID, playlist_id, track_ids)
        return results


# Separates Genres and features
# Limits genres length to only 5 genres (spotify recommendations only allows for 5 genre seeds)
def filter_seeds(seeds=None, genres=[], features=[], prev_features=[]):
    if seeds is not None:
        access_token = get_access_token()
        if access_token:
            sp = spotipy.Spotify(access_token)
            genres_dict = sp.recommendation_genre_seeds()
            available_genres = genres_dict.get('genres')
            for entry in seeds:
                if entry in available_genres and len(genres) < 5 and entry not in genres:
                    genres.append(entry)
                elif entry in spotify_config.FEATURES_LIST and entry not in features:
                    if entry not in prev_features:
                        features.append(entry)
                    else:
                        prev_features.remove(entry)
                    # features.append(entry)
                    # Commented out because features are not currently considered
                    # print('Feature: ' + str(entry))
                elif entry is 'rap' and 'hip-hop' not in genres and len(genres) < 5:
                    genres.append('hip-hop')


# Run overall workflow for spotify portion
# Input params: handle - twitter handle; seeds - output from Discovery (genre and feature seeds)
# Ideally, this will be updated to take two arrays, one for genre seeds and one for feature seeds
# Returns: URL link to generated spotify playlist
def generate_playlist(handle="No Twitter Handle", seeds=([], [])):
    playlist = create_playlist(handle)
    print('Playlist created for handle: ' + handle)

    positive = seeds[0]
    negative = seeds[1]
    genres = []
    pos_features = []
    neg_features = []
    filter_seeds(positive, genres, pos_features)
    # Spotify cannot do negatively correlated genres, so pass empty array
    filter_seeds(negative, [], neg_features, prev_features=pos_features)

    tracks = get_recommendations(genres=genres, pos_features=pos_features, neg_features=neg_features)
    add_tracks(playlist, tracks)

    # playlist object is a dictionary, so return only the URL string
    return playlist.get('external_urls').get('spotify')
