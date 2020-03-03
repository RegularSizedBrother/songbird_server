from src.resources.reddit_dumper import RedditDumper
from src.resources.personality_insights_reddit import RedditPersonality
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
empty_file = os.path.join(curr_dir, 'empty_reddit.txt')


def test_more_than_cap_reddit():
    user = "PresidentObama"
    file_result = "%s_reddit.txt" % user
    reddit_call = RedditDumper()
    person_call = RedditPersonality()
    reddit_call.get_all_comments(user)
    parsed_profile = person_call.traits_to_vector(person_call.get_profile(file_result))
    print(parsed_profile)
    assert parsed_profile is not None and len(parsed_profile) >= 5

def test_less_than_cap_reddit():
    user = "thisisbillgates"
    file_result = "%s_reddit.txt" % user
    reddit_call = RedditDumper()
    person_call = RedditPersonality()
    reddit_call.get_all_comments(user)
    parsed_profile = person_call.traits_to_vector(person_call.get_profile(file_result))
    print(parsed_profile)
    assert parsed_profile is not None and len(parsed_profile) >= 5

def test_empty_reddit():
    file_result = empty_file
    person_call = RedditPersonality()
    parsed_profile = person_call.traits_to_vector(person_call.get_profile(file_result))
    print(parsed_profile)
    assert parsed_profile == {}

def test_invalid_reddit():
    user = "j8ffbezos"
    file_result = "%s_reddit.csv" % user
    reddit_call = RedditDumper()
    person_call = RedditPersonality()
    reddit_call.get_all_tweets(user)
    parsed_profile = person_call.traits_to_vector(person_call.get_profile(file_result))
    print(parsed_profile)
    assert parsed_profile == {}