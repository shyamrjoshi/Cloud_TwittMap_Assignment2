from awses.connection import AWSConnection
from elasticsearch import Elasticsearch

es = Elasticsearch(connection_class=AWSConnection,
                   region='us-west-2',
                   host='arn:aws:es:us-west-2:704965676117:domain/tweetsentiments')


