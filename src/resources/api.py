from flask_restful import Api

from src.resources.twitter import Twitter
from src.resources.attribute import Attribute
from src.resources.playlist import Playlist
from src.resources.bob.twitter import BobTwitter
from src.resources.bob.attribute import BobAttribute
from src.resources.bob.playlist import BobPlaylist

api = Api()

api.add_resource(Twitter, '/twitter')
api.add_resource(Attribute, '/attributes/<int:handle_id>')
api.add_resource(Playlist, '/playlist/<int:handle_id>')

api.add_resource(BobTwitter, '/bob/twitter')
api.add_resource(BobAttribute, '/bob/attributes/<int:handle_id>')
api.add_resource(BobPlaylist, '/bob/playlist/<int:handle_id>')
