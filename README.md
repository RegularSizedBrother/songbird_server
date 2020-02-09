# songbird-server

## Installation

```
pip install flask
pip install flask-restful
pip install flask-cors
```

## Creating the Database

```
$ python
>>> from src.app import app, db
>>> with app.app_context():
...     db.init_app(app)
```

## Running

```
python main.py
```
