from flask_restful import Resource
import random

data = [
    "https://open.spotify.com/playlist/5EF18jWof9VRYaC7ss3Wte",
    "https://open.spotify.com/playlist/0RKi2UxVDVMrZqBA9uRSuT",
    "https://open.spotify.com/playlist/5KMBhQon3ArWQe2vPzC8KW",
]

class BobPlaylist(Resource):
    def get(self, handle_id):
        if random.randint(0, 1) == 0:
            return { "wait": True }

        if handle_id >= 1 and handle_id <= 3:
           playlist = data[handle_id-1]
           return { "error": False, "playlist": playlist }
        else:
           return { "error": True }
