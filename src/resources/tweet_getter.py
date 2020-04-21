import tweepy #https://github.com/tweepy/tweepy
import src.resources.tweet_dumper as tweet_dumper
import json


#WOEID- standardized where in the world id for location of trending topics, default 1(globe)
#num_topics, num_users- number of topics and number of users per topic to return
#return - a list of handles of users whose tweets were in trending topics
def get_trending_topic_users(WOEID=1, num_topics = 1, num_users=1):
    dumper = tweet_dumper.TwitterDumper()
    topics = dumper.api.trends_place(id=WOEID)[0]["trends"][0:num_topics]
    query_results = [dumper.api.search(topic["query"]) for topic in topics]
    users = []
    for query_result in query_results:
        users += [query_result[i]._json["user"]["screen_name"] for i in range(0, num_users)]
    return users

#WOEID- standardized where in the world id for location of trending topics, default 1(globe)
#num_topics, num_users- number of topics and number of users per topic to return
#return - a list of user profiles 
def get_trending_profiles(WOEID=1, num_topics = 1, num_users = 1):



if __name__ == "__main__":
    dumper = tweet_dumper.TwitterDumper()
    query = dumper.api.trends_place(id=1)[0]["trends"][0]["query"]
    print(json.dumps(dumper.api.search(query)[0]._json["user"]["screen_name"]))
    print(get_trending_topic_users())

