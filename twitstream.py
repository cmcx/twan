# -*- coding: utf-8 -*-

import tweepy
import json
import os
from tweepy import Stream
from tweepy.streaming import StreamListener

# authentication
################

# read credentials
twan_dir = os.path.expanduser('~') + '/.twan/'

with open(twan_dir + 'credentials', 'r') as f:
    credentials = [line.strip() for line in f if line.strip() != '']    # read the credentials line by line

creds = {}                                      # initialize a dictionary for storing the credentials
for cred in credentials:                        # iterate over the four entries
    cred = cred.split('=')                      # split the line into name and value
    creds[cred[0].strip()] = cred[1].strip()    # add it to the credentials store


def authenticate(consumer_key, consumer_secret, access_token, access_token_secret):
    '''
    authenticates with the necessary credentials, returns the shortened api
    '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth 


auth = authenticate(creds['consumer_key'], creds['consumer_secret'], creds['access_token'], creds['access_token_secret'])

 
class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('datastream.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True

def stream_filtered(search_phrase):
    '''
    establish a stream using a search phrase, 
    that is stream all tweets containing that search phrase, e.g. a hashtag,
    and save it in a file named datastream.json in the current directory
    '''
    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=[search_phrase])