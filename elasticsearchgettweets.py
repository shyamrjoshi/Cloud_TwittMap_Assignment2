from elasticsearch import Elasticsearch,RequestsHttpConnection
import json
def search(term):
    if term == 'all':
        #term = "trump"
        elasticcollect = Elasticsearch()
        query = json.dumps({
            "query":{
                "match_all":{}

            }
        })
    else:
        #term = "trump"
        elasticcollect = Elasticsearch()
        query = json.dumps({
            "query": {
                "match": {
                    "text":term
                }

            }
        })
    queryresult = elasticcollect.search(index="test-index", doc_type="tweet", body=query)
    data_return = []
    for doc in queryresult['hits']['hits']:
        data_return.append(doc['_source'])

        #print(queryresult)
    #print(data_return)
    return data_return

if __name__ == "__main__":
    search("trump")
