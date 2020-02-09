#!/usr/bin/env python
# encoding: utf-8
#Code taken from: https://gist.github.com/yanofsky/5436496

import tweepy #https://github.com/tweepy/tweepy
import csv
import sys

#Twitter API credentials
consumer_key = "EMrzCUAxblUXdh5CSTI73tDbB"
consumer_secret = "Pc63SQxLggiQlLRAM8bHOgxK3o4ATePMBbkSzys88LeibUlcKW"
access_key = "1222999226679881729-I1j6gUKMqu8zTapQNbRRh5FN5v2BF5"
access_secret = "T6ziZON3bTbF1W9LAwuOXNJxqBesBA1bfwAtzmIflR7jD"


class TwitterDumper:
	def get_all_tweets(self, screen_name):
		#Twitter only allows access to a users most recent 3240 tweets with this method
		
		#authorize twitter, initialize tweepy
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_key, access_secret)
		api = tweepy.API(auth)
		
		#initialize a list to hold all the tweepy Tweets
		alltweets = []	
		
		new_tweets = []
		#make initial request for most recent tweets (200 is the maximum allowed count)
		try:
			new_tweets = api.user_timeline(screen_name = screen_name,count=200)
		except:
			print("Error: Invalid user")
			t = open('%s_tweets.csv' % screen_name, 'w')
			t.close()
			return
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		#keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:
			print("getting tweets before %s" % (oldest))
			
			#all subsiquent requests use the max_id param to prevent duplicates
			new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
			
			#save most recent tweets
			alltweets.extend(new_tweets)
			
			#update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1
			
			print("...%s tweets downloaded so far" % (len(alltweets)))
		
		#transform the tweepy tweets into a 2D array that will populate the csv	
		outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
		
		#write the csv	
		with open('%s_tweets.csv' % screen_name, 'w', encoding = "utf-8") as f:
			writer = csv.writer(f)
			writer.writerow(["id", "created_at", "text"])
			writer.writerows(outtweets)
		
		pass

	if __name__ == '__main__':
		getter = TwitterDumper()
		#get tweets for username passed at command line
		if len(sys.argv) == 2:
			getter.get_all_tweets(sys.argv[1])
		else:
			print("Error: enter one username")
