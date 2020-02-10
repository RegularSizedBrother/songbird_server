# songbird-server

## Installation

You will need to install redis to run a redis server. You can find information about that here: https://redis.io.

If on Windows, you will need a Linux subsystem to run the RQ workers. Find information about that here: https://docs.microsoft.com/en-us/windows/wsl/about.

Use the following command to install dependencies:

```
pip install
```

## Creating the Database

```
$ python
>>> from src.app import app, db
>>> with app.app_context():
...     db.init_app(app)
```

## Running

1) Start a redis server instance.
2) Start an RQ worker in a Linux shell with `rq worker songbird`.
3) Run `python main.py` to start the web server.

## Testing

```
pytest
```

## tweet_dumper.py execution

```
python tweet_dumper.py twitter_account_name
```

ex: `python tweet_dumper.py BarackObama`

## personality_insights_twitter.py guide

```
python personality_insights_twitter.py
```

The sample file is BarackObama_tweets.csv. The sample output:
['Openness', 0.8308440292711101, 'Conscientiousness', 0.9861259293312097, 'Extraversion', 0.7305364516013685, 'Agreeableness', 0.6430794048245583, 'Emotional range', 0.3100944253262048]
