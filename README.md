# songbird-server

## Installation

```
pip install
```

To run the background consumers, you will need [SQLite](https://sqlite.org/) and [Huey](https://huey.readthedocs.io/en/latest/index.html).

## Creating the Database

```
python setup_db.py
```

## Running

Run the server

```
python main.py
```

Run the background jobs (be sure there is a SQLite instance runnning)

```
huey_consumer.py start_huey.huey
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
