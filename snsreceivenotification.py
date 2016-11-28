import datetime
import json
import ast
import boto3
from elasticsearch import Elasticsearch
#from awses.connection import AWSConnection
def notification(request):
    #print(type(request))
    global client
    client = boto3.client('sns')
    request = request.decode("utf-8")
    request = ast.literal_eval(request)
    #print(request)
    if request["Type"] == 'SubscriptionConfirmation':
        sns_confirm = client.confirm_subscription(
        TopicArn=request["TopicArn"],
        Token=request["Token"],

        )
    else:
        if request["Type"] == 'Notification':
            tweet_data = ast.literal_eval(request['Message'])
            #print(tweet_data)
            #put_tweets_in_elasticsearch(tweet_data)
            put_tweets_in_elasticsearch_local(tweet_data)
def put_tweets_in_elasticsearch_local(tweet_data):
    es = Elasticsearch()

    doc = {
        'text': str(tweet_data['text']),
        'coordinates': str(tweet_data['coordinates']),
        'sentiment' : str(tweet_data['sentiment'])
        #'timestamp': datetime.now(),
    }
    res = es.index(index="test-index", doc_type='tweet', body=doc)
    print(res)

def put_tweets_in_elasticsearch(tweet_data):
    client = boto3.client('es')
    print(tweet_data)
    key = str(tweet_data['text'])
    value_cor = tweet_data['coordinates']
    value = str(tweet_data['coordinates'][0]) + ',' + str(tweet_data['coordinates'][1]) + ',' + str(tweet_data['sentiment'])
    print(
        value
    )
    #es = Elasticsearch('https://search-tweetsentiments-m2rfxbz2zfsmrre225ucbj4m64.us-west-2.es.amazonaws.com/')
    #res = es.index(index="tweet_sentiments", doc_type='tweet', id=1, body=tweet_data)
    #key = tweet_data['text']
    #value = tweet_data['coordinates'].'|'..
    #value = {}
    #value['coordinates'] =  tweet_data['coordinates']
    #value['sentiment'] = tweet_data['sentiment']
    #value = json.dumps(value)

    response = client.add_tags(
          ARN='arn:aws:es:us-west-2:704965676117:domain/tweetsentiments',
          TagList=[
               {
                   'Key': str(tweet_data['text']),
                   'Value': value,
                   #'Value': tweet_data['sentiment']
               },
               # {
               #     'Key': str(tweet_data['text']),
               #     #'Value': tweet_data['coordinates'],
               #      'Value': str(tweet_data['sentiment'])
               # },
          ]
    #     TagList = [tweet_data
    #                ]
    )
    # print(response)
    # doc = {
    #     'text': str(tweet_data['text']),
    #     'coordinates': str(tweet_data['coordinates']),
    #     'sentiment': str(tweet_data['sentiment']),
    # }
    # res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
    #print(res['created'])
    #print(res)

    #es = Elasticsearch()



    es = Elasticsearch(region='us-west-2',
                       host='https://search-tweetsentiments-m2rfxbz2zfsmrre225ucbj4m64.us-west-2.es.amazonaws.com/')
    print(es)
    # doc = {
    #     'text': str(tweet_data['text']),
    #     'coordinates': str(tweet_data['coordinates']),
    #     'sentiment': str(tweet_data['sentiment']),
    # }
    # res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
    # print(res['created'])
    # es = Elasticsearch()





