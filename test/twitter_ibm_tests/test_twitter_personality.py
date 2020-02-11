from src.resources.tweet_dumper import TwitterDumper
from src.resources.personality_insights_twitter import TwitterPersonality
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
empty_file = os.path.join(curr_dir, 'empty_tweets.csv')


def test_more_than_cap_twitter():
    user = "BarackObama"
    file_result = "tmp/%s_tweets.csv" % user
    twit_call = TwitterDumper()
    person_call = TwitterPersonality()
    twit_call.get_all_tweets(user)
    parsed_profile = person_call.traits_to_vector(person_call.get_profile(file_result))
    print(parsed_profile)
    assert parsed_profile is not None and len(parsed_profile) >= 5

def test_less_than_cap_twitter():
    user = "Dennis42621058"
    file_result = "tmp/%s_tweets.csv" % user
    twit_call = TwitterDumper()
    person_call = TwitterPersonality()
    twit_call.get_all_tweets(user)
    parsed_profile = person_call.traits_to_vector(person_call.get_profile(file_result))
    print(parsed_profile)
    assert parsed_profile is not None and len(parsed_profile) >= 5

def test_empty_twitter():
    file_result = empty_file
    person_call = TwitterPersonality()
    parsed_profile = person_call.traits_to_vector(person_call.get_profile(file_result))
    print(parsed_profile)
    assert parsed_profile == {}

def test_invalid_twitter():
    user = "j8ffbezos"
    file_result = "tmp/%s_tweets.csv" % user
    twit_call = TwitterDumper()
    person_call = TwitterPersonality()
    twit_call.get_all_tweets(user)
    parsed_profile = person_call.traits_to_vector(person_call.get_profile(file_result))
    print(parsed_profile)
    assert parsed_profile == {}
