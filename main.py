from src.app import create_app
from src.resources.api import api

if __name__ == '__main__':
    app = create_app()
    api.init_app(app)
    app.run(debug=True)
