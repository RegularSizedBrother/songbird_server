from flask_restful import Resource

data = [
    "https://open.spotify.com/playlist/5EF18jWof9VRYaC7ss3Wte",
    "https://open.spotify.com/playlist/0RKi2UxVDVMrZqBA9uRSuT",
    "https://open.spotify.com/playlist/5KMBhQon3ArWQe2vPzC8KW",
]

class Playlist(Resource):
    def get(self, handle_id):
        playlist = ""
        if handle_id >= 1 and handle_id <= 3:
           playlist = data[handle_id-1]
        return {"playlist": playlist}