    #Reference - http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html
import tweepy
import json
import boto.sqs
from boto.sqs.message import *
from flask import Flask
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from elasticsearch import Elasticsearch
application = Flask(__name__)
@application.route("/")


class twittListener(StreamListener):
    def on_data(self, raw_data):
        json_data = json.loads(raw_data)
        #print(json_data)
        tweet_store = {}
        if json_data.get("text", None) is not None:
            coordinates = json_data["coordinates"]
            location = json_data["user"]["location"]
            text = json_data['text']
            if coordinates is not None:
                #print(coordinates)
                tweet_store['text'] = json_data['text']
                tweet_store['coordinates'] = json_data["coordinates"]
                #print(tweet_store)
                #tweet_store = json.dumps(tweet_store)
                tweet_store = json.dumps(tweet_store)
                print(type(tweet_store))
                sqs_push(tweet_store)
                #print(location)


def sqs_push(tweet_store):
    print(tweet_store)
    my_queue = conn.get_queue('myqueue')
    #print(my_queue)
    m = Message()
    tweet_store_json = json.dumps(tweet_store)
    m.set_body(tweet_store_json)
    my_queue.write(m)



def create_sqs_connection():
    global conn
    conn = boto.sqs.connect_to_region(
        "us-west-2",
        aws_access_key_id='',
        aws_secret_access_key='')
    q = conn.create_queue('myqueue')

def main():
    create_sqs_connection()
    consumerkey = ""
    consumersecret = ""
    accesstoken = ""
    accesstokensecret = ""
    authhandler = OAuthHandler(consumerkey, consumersecret)
    authhandler.set_access_token(accesstoken, accesstokensecret)
    tweets = tweepy.Stream(authhandler, twittListener())
    #track = twitter & locations = -122.75, 36.8, -121.75, 37.8
    tweets.filter(track=["Instagram", "Facebook", "SundayMorning", "Trump", "Hillary","NYC","sports","football","cricket"],languages=["en"],async=True)
                  #locations = [-122.75, 36.8, -121.75, 37.8])
if __name__ == "__main__":
    main()
