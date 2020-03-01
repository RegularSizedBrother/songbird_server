#!/usr/bin/env python
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
      def get_all_comments(self, user_name):
          # write all comments to a txt file
          with open('%s_reddit.txt' % user_name, 'w', encoding = 'utf-8') as f:
               # get all submission and comments from a user's front page
               user = reddit.redditor(user_name)
               for submission in user.submissions.new():
                   f.write('%s\n' % submission.title)

               for comment in user.comments.new():
                   f.write('%s\n' % comment.body)
    

      if __name__ == '__main__':
          getter = RedditDumper()
          # get reddit username
          if len(sys.argv) == 2:
             getter.get_all_comments(sys.argv[1])
          else:
             print("Error: enter one username")   
