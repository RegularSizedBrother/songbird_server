from songbird_server.resources.tweet_dumper import TwitterDumper
from songbird_server.resources.personality_insights_twitter import TwitterPersonality

def test_more_than_cap_twitter():
    user = "BarackObama"
    file_result = "%s_tweets.csv" % user
    twit_call = TwitterDumper()
    person_call = TwitterPersonality()
    twit_call.get_all_tweets("BarackObama")
    profile = person_call.traits_to_vector(person_call.get_profile(file_result))
    print(profile)
    assert profile is not None and len(profile) > 5

def test_less_than_cap_twitter():
    user = "Dennis42621058"
    file_result = "%s_tweets.csv" % user
    twit_call = TwitterDumper()
    person_call = TwitterPersonality()
    twit_call.get_all_tweets(user)
    profile = person_call.traits_to_vector(person_call.get_profile(file_result))
    print(profile)
    assert profile is not None and len(profile) > 5

def test_empty_twitter():
    file_result = "empty_tweets.csv"
    person_call = TwitterPersonality()
    profile = person_call.traits_to_vector(person_call.get_profile(file_result))
    print(profile)
    assert profile == []