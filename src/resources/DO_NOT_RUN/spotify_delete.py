import spotipy
from src.resources import spotify, spotify_config
import os

def delete_all_playlists():
    input('ARE YOU SURE YOU WANT TO DELETE 50 PLAYLISTS? HIT CTRL+C TO STOP, OR ENTER TO CONTINUE.')
    access_token = spotify.get_access_token()
    sp = spotipy.Spotify(access_token)
    playlists = sp.current_user_playlists()['items']
    for playlist in playlists:
        print("Deleting playlist '" + playlist['name'] + "'...")
        sp.user_playlist_unfollow(user=spotify_config.SONGBIRD_USER_ID, playlist_id=playlist['id'])
    os.remove('.spotipyoauthcache')
    print(str(len(playlists)) + " playlists deleted.")
delete_all_playlists()