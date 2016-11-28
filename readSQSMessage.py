import json
#import HTMLParser
import boto.sqs
import re
import certifi
import boto3
from boto.sqs.message import *
from alchemyapi import AlchemyAPI
#from html.parser import HTMLParser
#from datetime import datetime
from boto3 import *
import string

from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
alchemyapi = AlchemyAPI()
#sqs = boto3.resource('sqs')
def main():
        global conn
        conn = boto.sqs.connect_to_region(
                "us-west-2",
                aws_access_key_id='AKIAIVUTQRY6WTUNNKSQ',
                aws_secret_access_key='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')
        #q = conn.create_queue('myqueue')

        q = conn.get_queue('myqueue')
        connect_to_sns()
        #rs = q.get_messages()
        i=0
        count = 1
        while True:
            rs = q.get_messages()
            #print(rs[0].get_body())
            if len(rs) > 0:
                tweet_data = {}
                tweet_data = json.loads(rs[0].get_body())
                #print(tweet_data['text'])
                tweet_data = json.loads(tweet_data)
                print(type(tweet_data))
                tweet_text = tweet_data['text']
                coordinates = tweet_data['coordinates']['coordinates']
                # #print(tweet_text)
                # test_str = str(tweet_text)
                # if 'San Francisco CA' in test_str:
                #     print(tweet_text)
                tweet_text = clean_tweet_text(tweet_text)
                # #myText = "I'm excited to get started with AlchemyAPI!"
                # #print(tweet_text)
                try:
                    response = alchemyapi.sentiment("text", tweet_text,options={"language":'english'})

                    #print(tweet_text)
                    #print(response)
                    #print("Sentiment: ", response['docSentiment']['type'])
                    tweet_sentiments = {}
                    tweet_sentiments['text'] = tweet_text
                    tweet_sentiments['coordinates'] = coordinates
                    tweet_sentiments['sentiment'] = response['docSentiment']['type']
                    tweet_message = json.dumps(tweet_sentiments)
                    publsh_message = client.publish(
                        TopicArn=topicarn,
                        # TargetArn='string',
                        # PhoneNumber='string',
                        Message=json.dumps(tweet_sentiments, ensure_ascii=False),
                        #Subject='string',
                        MessageStructure='string',
                        # MessageAttributes={
                        # 'string': {
                        #     'DataType': 'string',
                        #     'StringValue': 'string',
                        #     'BinaryValue': 'string'
                        # }
                        # }
                    )
                    i=i+1
                    #rs = q.get_messages()
                    print('publish done')
                    # count = count + 1;
                except:
                    pass

        # all_messages = []
        # rs = q.get_messages(10)
        # while len(rs) > 0:
        #     all_messages.extend(rs)
        #     rs = q.get_messages(10)
        # Get the service resource
        # sqs = boto3.resource('sqs')
        #
        # # Get the queue
        # queue = sqs.get_queue_by_name(QueueName='myqueue')
        #
        # # Process messages by printing out body and optional author name
        # # for message in queue.receive_messages():
        # #     print(message.get('text'))

def clean_tweet_text(tweet_text):

    #print (tweet_text['text'])
    #html_parser = HTMLParser.HTMLParser()
    #tweet = html_parser.unescape(tweet_text)
    #tweet = tweet_text.decode("utf8").encode('ascii','ignore')
    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet_text).split())
    #tweet = re.sub(r"http\S+", "", tweet)
    #tweet = ' '.join(tweet.lower().strip().rstrip(string.punctuation))
    # Remove the stop words.
    #tweet = [t for t in tweet if t not in stopwords.words('english')]
    return tweet
    # Create the stemmer.
    #stemmer = LancasterStemmer()

    # Stem the words.
    #print ([stemmer.stem(t) for t in tweet])


def connect_to_sns():
    global client
    global topicarn
    client = boto3.client('sns')
    #return client
    response = client.create_topic(
        Name='tweet_sentiments'
    )

    #print(tweet_message)
    topicarn = response['TopicArn']
    #print(response)
    subscriber = client.subscribe(
        TopicArn=topicarn,
        Protocol='http' ,
        #Endpoint='http://127.0.0.1:5000/notification' 108.6.175.225
        Endpoint='http://cab6dbac.ngrok.io/notification'
        #Endpoint = 'http://35.162.251.85:5000/notification'
    )
    print(subscriber)
    # confirm = client.confirm_subscription(
    #     TopicArn=topicarn,
    #     Token=subscriber['ResponseMetadata'],
    #     AuthenticateOnUnsubscribe='string'
    # )

    # publsh_message = client.publish(
    #     TopicArn=topicarn,
    #     # TargetArn='string',
    #     #PhoneNumber='string',
    #     Message=tweet_message,
    #     Subject='string',
    #     MessageStructure='string',
    #     #MessageAttributes={
    #     #    'tweets': {
    #     #        'text': tweet_sentiments['text'],
    #      #       'coordinates': tweet_sentiments['coordinates'],
    #       #      'sentiment': tweet_sentiments['sentiment']
    #        # }
    #     #}
    # )


if __name__ == "__main__":
    main()
