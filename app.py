from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from resources.twitter import Twitter
from resources.attribute import Attribute
from resources.playlist import Playlist
from resources.bob.twitter import BobTwitter
from resources.bob.attribute import BobAttribute
from resources.bob.playlist import BobPlaylist

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Twitter, '/twitter')
api.add_resource(Attribute, '/attributes/<int:handle_id>')
api.add_resource(Playlist, '/playlist/<int:handle_id>')

api.add_resource(BobTwitter, '/bob/twitter')
api.add_resource(BobAttribute, '/bob/attributes/<int:handle_id>')
api.add_resource(BobPlaylist, '/bob/playlist/<int:handle_id>')

if __name__ == '__main__':
    app.run(debug=True)
