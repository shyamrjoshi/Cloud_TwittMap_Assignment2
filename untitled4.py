from flask import Flask, render_template, request
import json
import elasticsearchgettweets
app = Flask(__name__)

import snsreceivenotification

@app.route('/')
def hello_world():
    if request.method == "POST":
        print("inside post")
        tag = request.form.get("tags")
        #tweets_sentiments = elasticsearchgettweets.search(tag)
        #print(tweets_sentiments)
        #return render_template("testmarker.html", data=tweets_sentiments)
        #return 'Hello World!'
    else:
        tag = 'all'
        print("inside Get")
        tweets_sentiments = elasticsearchgettweets.search(tag)
        print(tweets_sentiments)
        return render_template("testmarker.html",data=tweets_sentiments)
        #return 'Hello World!'

@app.route('/tweets',methods=['GET','POST'])
def search_keyword():
    if request.method == "POST":
        print("inside search keyword")
        tag = request.form.get("tags")
        tweets_sentiments = elasticsearchgettweets.search(tag)
        print(tweets_sentiments)
        return render_template("testmarker.html", data=tweets_sentiments)
        #return 'Hello World!'
    else:
        tag = 'all'
        print("inside get search keyword")
        tweets_sentiments = elasticsearchgettweets.search(tag)
        print(tweets_sentiments)
        return render_template("testmarker.html",data=tweets_sentiments)
        #return 'Hello World!'

@app.route('/notification',methods=['GET','POST'])
def notification():
    if request.method == 'POST':
        snsreceivenotification.notification(request.data)
        print('inside post')
        #print( request.data)
    return 'Hello GET!'

if __name__ == '__main__':
    app.run(debug=True)


