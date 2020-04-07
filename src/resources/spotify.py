'''
This file contains all the tools and functions needed for spotify integration.
'''

import spotipy
from spotipy import oauth2
from src.resources import spotify_config
import random
import os

#Default case will keep us logged into the Songbird account, but if it finds a token from a logged in user, it will
#read that first.
def get_access_token():
    #Check for user token
    sp_oauth = oauth2.SpotifyOAuth(spotify_config.SPOTIFY_CLIENT_ID,
                                   spotify_config.SPOTIFY_CLIENT_SECRET,
                                   spotify_config.SPOTIFY_REDIRECT_URL,
                                   scope=spotify_config.SCOPE,
                                   cache_path=spotify_config.USER_CACHE)
    token_info = sp_oauth.get_cached_token()

    if token_info:
        access_token = token_info['access_token']
    else:
        #Since the user token was not found, grab the default
        sp_oauth = oauth2.SpotifyOAuth(spotify_config.SPOTIFY_CLIENT_ID,
                                       spotify_config.SPOTIFY_CLIENT_SECRET,
                                       spotify_config.SPOTIFY_REDIRECT_URL,
                                       scope=spotify_config.SCOPE,
                                       cache_path=spotify_config.DEFAULT_CACHE)
        token_info = sp_oauth.get_cached_token()

        if token_info:
            access_token = token_info['access_token']
        else:
            #If not found, create the token - should never come up in actual use
            access_token = spotipy.util.prompt_for_user_token(spotify_config.SONGBIRD_USER_EMAIL,
                                                              scope=spotify_config.SCOPE,
                                                              client_id=spotify_config.SPOTIFY_CLIENT_ID,
                                                              client_secret=spotify_config.SPOTIFY_CLIENT_SECRET,
                                                              redirect_uri=spotify_config.SONGBIRD_CLIENT_REDIRECT_URL,
                                                              cache_path=spotify_config.CACHE)

    return access_token

#Determines if the file at the user token cache exists (if they are currently logged in)
def is_user_logged_in():
    return os.path.isfile(spotify_config.USER_CACHE)

#Saves token returned from url to the specified user cache location in spotify_config.py
#Parameters - URL - the full url from the CLIENT that was called back from the Spotify login button
def save_user_token(url):
    #create spotify oauth obejct for user cache
    sp_oauth = oauth2.SpotifyOAuth(spotify_config.SPOTIFY_CLIENT_ID,
                                   spotify_config.SPOTIFY_CLIENT_SECRET,
                                   spotify_config.SPOTIFY_REDIRECT_URL,
                                   scope=spotify_config.SCOPE,
                                   cache_path=spotify_config.USER_CACHE)

    print('Received url: ' + url)
    code = sp_oauth.parse_response_code(url)
    if code:
        print('Successfully parsed token! Code: ' + code)
    else:
        print('Failed to parse token.')

#Returns the User's name from the User's spotify token
#NOTE: RETURNS AN EMPTY STRING IF NO USER DETECTED
def get_user_name():
    if is_user_logged_in():
        access_token = get_access_token()
        sp = spotipy.Spotify(access_token)
        user_info = sp.current_user()
        #Can return more info if needed, for now only returning display name
        return user_info['Songbird']
    else:
        return ''

#Deletes the User's cached spotify token
#Should be used when logging out
def delete_user_token():
    print('Deleting cached user token...')
    os.remove(spotify_config.USER_CACHE)
    print('Cached user token deleted.')

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
        parameters = dict(seed_genres=genres, limit=spotify_config.PLAYLIST_SIZE, market=spotify_config.US_CODE)

        for pos in pos_features:
            if (pos in spotify_config.RATIO_FEATURES):
                parameters['target_' + pos] = spotify_config.HIGH_TARGET
                parameters['min_' + pos] = spotify_config.HIGH_TARGET-spotify_config.THRESHOLD

        for neg in neg_features:
            if (neg in spotify_config.RATIO_FEATURES):
                parameters['target_' + neg] = spotify_config.LOW_TARGET
                parameters['max_' + neg] = spotify_config.LOW_TARGET+spotify_config.THRESHOLD

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
                if entry in available_genres and len(genres) < 5 and entry not in genres and entry is not 'soundtracks':
                    genres.append(entry)
                elif entry in spotify_config.FEATURES_LIST and entry not in features:
                    if entry not in prev_features:
                        features.append(entry)
                    else:
                        prev_features.remove(entry)
                #Rap is not a spotify recommendation seed, but hip-hop is
                elif entry is 'rap' and 'hip-hop' not in genres and len(genres) < 5:
                    genres.append('hip-hop')
                #due to an error in discovery
                elif entry is '/funk' and 'funk' not in genres and len(genres) < 5:
                    genres.append('funk')
                #potential formatting
                elif entry is 'r&b' and 'r-n-b' not in genres and len(genres) < 5:
                    genres.append('funk')
                #potential formatting
                elif entry is 'R&B' and 'r-n-b' not in genres and len(genres) < 5:
                    genres.append('r-n-b')
                #How the "instrumentalness" feature will likely be described
                elif entry is 'instrumental' and 'instrumentalness' not in features:
                    if 'instrumentalness' not in prev_features:
                        features.append('instrumentalness')
                    else:
                        prev_features.remove('instrumentalness')
                #How the "valence" feature will likely be described
                elif entry is 'happy' and 'valence' not in features:
                    if 'valence' not in prev_features:
                        features.append('valence')
                    else:
                        prev_features.remove('valence')
                #Parsing the energetic feature
                elif entry is 'energetic' and 'energy' not in features:
                    if 'energy' not in prev_features:
                        features.append('energy')
                    else:
                        prev_features.remove('energy')
                #parsing the liveness feature
                elif entry is 'live' and 'liveness' not in features:
                    if 'liveness' not in prev_features:
                        features.append('liveness')
                    else:
                        prev_features.remove('liveness')
                #parsing the acousticness feature
                elif entry is 'acoustic' and 'acousticness' not in features:
                    if 'acousticness' not in prev_features:
                        features.append('accousticness')
                    else:
                        prev_features.remove('liveness')
                #There is no spoken word genre, and its not worth disrupting our entire process to get this niche genre.
                # my experience with the 'speechiness' trait leads to bad recommendations

def fill_genres(genres):
    if len(genres) < 5 and 'alternative' in genres and 'alt-rock' not in genres:
        genres.append('alt-rock')

    if len(genres) < 5 and 'r-n-b' in genres and 'soul' not in genres:
        genres.append('soul')

    if len(genres) < 5 and 'soul' in genres and 'r-n-b' not in genres:
        genres.append('r-n-b')

    if len(genres) < 5 and 'techno' in genres and 'detroit-techno' not in genres:
        genres.append('detroit-techno')

    if len(genres) < 5 and 'country' in genres and 'bluegrass' not in genres:
        genres.append('bluegrass')

    if len(genres) < 5 and 'dance' in genres and 'house' not in genres:
        genres.append('house')

    #Spotify has many genres that aren't able to be used as recommendation seed
    #   Unfortunately, almost all hip hop subgenres fall into that category, so they can't be filled out
    #   Trip-hop is listed as a hip-hop subgenre, but as a listener to both, I'd list them as pretty distinct
    #       - Portishead (a notable trip-hop band) does not sound like Kendrick Lamar, Drake, Kanye West, etc
    #if len(genres) < 5 and 'hip-hop' in genres:
    #    genres.append('trip-hop')

    avail_rock_genres = ['rock-n-roll', 'punk-rock', 'psych-rock', 'grunge', 'garage', 'alt-rock', 'hard-rock']
    avail_pop_genres = ['pop-film', 'synth-pop', 'party', 'indie-pop', 'club']

    if 'rock' in genres or 'pop' in genres:
        while len(genres) < 5:
            if 'rock' in genres:
                choice = random.choice(avail_rock_genres)
                if choice not in genres:
                    genres.append(choice)

            if 'pop' in genres:
                choice = random.choice(avail_pop_genres)
                if choice not in genres:
                    genres.append(choice)


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
    fill_genres(genres)
    # Spotify cannot do negatively correlated genres, so pass empty array
    filter_seeds(negative, [], neg_features, prev_features=pos_features)

    tracks = get_recommendations(genres=genres, pos_features=pos_features, neg_features=neg_features)
    add_tracks(playlist, tracks)

    # playlist object is a dictionary, so return only the URL string
    return playlist.get('external_urls').get('spotify')
