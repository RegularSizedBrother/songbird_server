'''
This file contains all the tools and functions needed for spotify integration.
'''

import spotipy
from spotipy import oauth2

from src.resources.spotify_config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SCOPE, CACHE, \
    SONGBIRD_USER_ID

class SpotifyParser():
#Ideally would return the access token for the user, but im bad at APIs?
    def get_access_token(self):
        sp_oauth = oauth2.SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE)
        token_info = sp_oauth.get_cached_token()
        print("TEST")
        print(token_info)
        print("TEST")
        if token_info:
            print("Found cached token!")
            access_token = token_info['access_token']

        else:
            print("Did not find cached token?")
            access_token = spotipy.util.prompt_for_user_token('humes.35@osu.edu', scope=SCOPE, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri='http://localhost:5000', cache_path=CACHE)
            #access_token = "BQCl6WOvMSEc73xHDPFBMKKiuuSNR2T-BOFxBk0mSaIvdgm6c36LKuOZMrIMcjgpeJTAIULavhOjPWnScBApYJLjtFz06QmMPfMy5BhjBVyawGz6JE-aqOc7EbJeqoUakGaHLoqVcBDO2EtQ5--pRGKxrqLSZl-SIy1gIUdU6LMvqKRAdJRZOgoZwO_thURPcoaXG5ZGd9swu_B5yS976s7AKiuYtuTyEW0JujXYysTb975WRlHL"
        return access_token

    # Get recommendations - returns an array of tracks based on genres and traits - PRE SORTED
    # REQUIRES 5 OR LESS GENRES - USE filter_seeds TO QUALITY CHECK
    def get_recommendations(self, genres=[], features=[]):
        access_token = self.get_access_token()

        print('RECS')
        print(genres)
        print(features)

        if access_token:
            print("Access token available! Trying to get songs...")
            sp = spotipy.Spotify(access_token)

            if len(genres) == 0 and len(features) == 0:
                # If no genres and no traits, return 'The Sounds of Silence'
                # original: 3CepTOU9Y7FezTt0CF3lCw
                # Disturbed: 1Cj2vqUwlJVG27gJrun92y
                # PENTATONIX: 0ZFeVCKCMCXUQ1TKVd2azW
                sounds_of_silence = ['3CepTOU9Y7FezTt0CF3lCw', '1Cj2vqUwlJVG27gJrun92y', '0ZFeVCKCMCXUQ1TKVd2azW']
                print('silence...')
                return sp.tracks(sounds_of_silence)
                #return sp.recommendations(seed_tracks=sounds_of_silence)

            elif len(features) == 0:
                recs = sp.recommendations(seed_genres=genres)
                print('Recommending by genre!')
                print('______________')
                print(recs)
                print('______________')
                return recs

            else:
                print('Both feats and genres')

            print('W H A T')

    # Create playlist for the specified user
    # Name should be the name of the playlist (the twitter handle)
    # User should be the user Id, defaulting to the Songbird user id - TBD
    def create_playlist(self, name, user=None):
        access_token = self.get_access_token()

        # Default to songbird user
        user_id = user
        if user_id is None:
            user_id = SONGBIRD_USER_ID

        pl_description = "Songbird created a playlist based on the Twitter handle " + name + "."

        if access_token:
            print("Access token available! Trying to create playlist...")
            sp = spotipy.Spotify(access_token)
            results = sp.user_playlist_create(user_id, name, description=pl_description)
            return results

    #Add tracks to playlist
    def add_tracks(self, playlist, tracks, user=None):
        access_token = self.get_access_token()

        #The objects returned by other functions are dictionaries
        playlist_id = playlist.get('id')

        track_ids = []
        tracks_list = tracks.get('tracks')

        for track in tracks_list:
            track_ids.append(track.get('id'))
            print(track)

        if access_token:
            print("Access token available! Trying to add tracks...")
            sp = spotipy.Spotify(access_token)
            results = sp.user_playlist_add_tracks(SONGBIRD_USER_ID, playlist_id, track_ids)
            return results

    '''
    playlist = create_playlist('TEST')
    print(playlist)
    print('_____________________________________________')
    tracks = get_recommendations()
    print(tracks)
    print('_____________________________________________')
    print(add_tracks(playlist, tracks))
    '''

    #Delete playlist on Songbird user
    #   no user parameter to prevent app from deleting user playlists


    #Request permissions?
    #   Not sure how this works yet, but not necessary for final product

    # Separates Genres and features
    # Limits genres length to only 5 genres (spotify recommendations only allows for 5 genre seeds)
    def filter_seeds(self, seeds = None, genres = [], features = []):
        if seeds is not None:
            access_token = self.get_access_token()
            if access_token:
                sp = spotipy.Spotify(access_token)
                genres_dict = sp.recommendation_genre_seeds()
                available_genres = genres_dict.get('genres')
                for entry in seeds:
                    if entry in available_genres and len(genres) < 5:
                        genres.append(entry)
                    else:
                        #features.append(entry)
                        #Commented out because features are not currently considered
                        print('Feature: ' + entry)


    # Run overall workflow for spotify portion
    # Input params: handle - twitter handle; seeds - output from Discovery (genre and feature seeds)
    # Ideally, this will be updated to take two arrays, one for genre seeds and one for feature seeds
    # Returns: URL link to generated spotify playlist
    def generate_playlist(self, handle="No Twitter Handle", seeds=None):
        playlist = self.create_playlist(handle)
        print('Playlist created for handle: ' + handle)

        #Needed until Discovery can handle this
        genres = []
        features = []
        self.filter_seeds(seeds, genres, features)

        tracks = self.get_recommendations(genres=genres, features=features)
        print('Recommendations generated for handle: ' + handle)
        self.add_tracks(playlist, tracks)
        print('Recommended tracks have been added to the playlist for handle: ' + handle)

        #playlist object is a dictionary, so return only the URL string
        return playlist.get('external_urls').get('spotify')
'''
print('BIG TEST')
print(generate_playlist("@OMGWOWEE", ['test', 'rock', 'hip-hop', 'cheese']))
print('FINISH BIG TEST')
print('CHECK MORE THAN 5 GENRES')
print(generate_playlist("@LotsOfGenres", ['test', 'rock', 'hip-hop', 'cheese', 'classical', 'disco', 'electronic', 'folk', 'funk', 'metal']))
print('FINISH CHECK')
print('Empty')
print(generate_playlist())
print('Finish empty')


print('Hmmmmm')
sounds_of_silence = ['3CepTOU9Y7FezTt0CF3lCw', '1Cj2vqUwlJVG27gJrun92y', '0ZFeVCKCMCXUQ1TKVd2azW']
access_token = get_access_token()
sp = spotipy.Spotify(access_token)
print(sp.recommendations(seed_tracks=sounds_of_silence))
'''