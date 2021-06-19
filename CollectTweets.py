##CIS 400 Final Project Part 1
##Greg Driscoll, Jared Kozak, Tyler Smelski
##Sentiment Analysis to predict rise and fall of bitcoin prices.
##FinalProjectPt1.py - Uses twitter stream API to collect tweets about a stock
##price and adds them to a MongoDB along with a sentiment rating from the 
##TextBlob api.

import pymongo
import twitter
import time
from textblob import TextBlob

#twitter api oauth_login from cookbook
def oauth_login():
    CONSUMER_KEY = "qBqaQB6eQRFMOouCGyniPFbHR"
    CONSUMER_SECRET = "mFwH64cQl0jEb7jGwiWlkK76miAvD5Mas2aFTkZQEqMMW03dxe"
    OAUTH_TOKEN = "1108161628493750274-SdSisRuFUqZX03PnbrCDV7EYs4TJ2u"
    OAUTH_TOKEN_SECRET = "ruqfKGOFDNCpDEEdauukm3UHayj6rE6fUEQbanyFSlEA6"

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    
    return twitter_api


#Use the twitter stream API to get tweets given a list of topics
def getTweets(topics = "", timeAmt = 7200, backoff = 1 ):
    twitter_api = oauth_login()

    if (backoff > 5):
        backoff = 5

    #open connection to twitter streaming api
    #if error connecting to api backoff and try agian
    try:
        twitter_stream = twitter.TwitterStream(auth = twitter_api.auth)
        stream = twitter_stream.statuses.filter(track=topics)
    except:
        print("Error connecting to the stream. Trying again in a minute")
        time.sleep(65 * backoff)
        getTweets(topics, timeAmt)
    
    #add tweets to database and exit after set amount of time using python
    #time package
    startTime = time.perf_counter()
    currentTime = time.perf_counter()
        
    try:
        for tweet in stream:
            currentTime = time.perf_counter()
            #addToDB(tweet['text'])
            
            if 'text' in tweet:
                addToDB(tweet['text'])
            elif 'disconnect' in tweet:
                print("Disconnect code is:", tweet['disconnect']['code'])
                break
            elif 'warning' in tweet:
                print("Falling behind. Hurry up.")
            else:
                pass

            if (int(currentTime) - int(startTime) > timeAmt):
                print("done")
                break

    #catch possible errors and employ back off time before calling api again
    except KeyError:
        print("KeyError. Skipping tweet.")
        time.sleep(65 * backoff)
    except ConnectionResetError:
        print("ConnectionResetError. Sleeping a minute then trying again.")
        time.sleep(65 * backoff)
    except:
        print("Unexpected Error. Will try agian in a minute.")
        time.sleep(65 * backoff)
          
           
#Add the tweet to MongoDB with a sentiment rating using TextBlob 
def addToDB(addTweet):
    print(addTweet)

    #connect to database using pymongo api
    password = "g0ldf1sh"
    client = pymongo.MongoClient("mongodb+srv://GregDriscoll:"+password+"@cis400finalproject-bqfrw.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = client.get_database('TweetsWithRatings')
    tweets = db.Ratings

    #Use TextBlob to get a sentiment rating for the tweet 
    tweetRating = TextBlob(addTweet)
    rating = tweetRating.sentiment.polarity
    print(rating)

    #Add tweet to MongoDB
    tweets.insert_one({"tweet": addTweet,
                       "rating": rating})
    print("---------------------------------")

def main():
    #connect to database using pymongo api to clear collection  
    password = "g0ldf1sh"
    client = pymongo.MongoClient("mongodb+srv://GregDriscoll:"+password+"@cis400finalproject-bqfrw.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = client.get_database('TweetsWithRatings')
    ratings = db.Ratings
    ratings.drop()

    #make sure tweets are collected for alotted amount of time 
    fullTime = 28800
    startTime = time.perf_counter()
    currentTime = time.perf_counter()
    count = 0
    while int(currentTime) - int(startTime) < fullTime:
        newTime = fullTime - (currentTime - startTime)
        getTweets(topics = 'bitcoin', timeAmt = newTime, backoff = count + 1)
        currentTime = time.perf_counter()
    
    print("xXx")

main()
