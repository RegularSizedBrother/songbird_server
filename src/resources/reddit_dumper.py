import praw
import pandas as pd
import datetime as dt
import sys
import csv

reddit = praw.Reddit(client_id='Ge1Tv8PTvT5uEg',
                     client_secret='GGwzIiuiqs-1Du3jxZFO0HSh8VM',
                     user_agent='Songbird', 
                     username='lesliesun016', 
                     password='123456789')

class RedditDumper:
    def valid_user(self, username):
        try:
            print(reddit.redditor(username).created_utc)
            return True
        except:
            print("       Invalid user")
            return False

    def get_all_text(self, username):
        text = []
        user = reddit.redditor(username)
        print(user)

        text.extend([sub.title for sub in user.submissions.new()])
        text.extend([comment.body for comment in user.comments.new()])

        return text

    def get_text_to_file(self, filename, username):
        with open(filename, 'w', encoding = 'utf-8') as f:
            text = self.get_all_text(username)

            for word in text:
                f.write(word)

if __name__ == '__main__':
  getter = RedditDumper()
  # get reddit username
  if len(sys.argv) == 2:
     getter.get_all_comments("%s_reddit.txt" % sys.argv[1], sys.argv[1])
  else:
     print("Error: enter one username")   
