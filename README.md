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

## Testing

```
pytest

```
## tweet/reddit_dumper.py execution

```
python tweet/reddit_dumper.py twitter/reddit_account_name

ex: python tweet/reddit_dumper.py BarackObama/thisisbillgates
```

## personality_insights_twitter/reddit.py guide
```
python personality_insights_twitter/reddit.py

The sample file is BarackObama_tweets.csv. The sample output:
['Openness', 0.8308440292711101, 'Conscientiousness', 0.9861259293312097, 'Extraversion', 0.7305364516013685, 'Agreeableness', 0.6430794048245583, 'Emotional range', 0.3100944253262048]
```
