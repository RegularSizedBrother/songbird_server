# Conglomeration for running huey. Import any
# job into this file to make it available.
from src.jobs.config import huey
from src.jobs.twitter import process_twitter
from src.jobs.spotify import process_spotify
