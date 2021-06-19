##CIS 400 Final Project Part 2
##Greg Driscoll, Jared Kozak, Tyler Smelski 
##Sentiment analysis to predict the rise and fall of bitcoin prices.
##FinalProjectPt2.py - Accesses the MongoDB to get tweets and ratings to analyze to decide whether
##the price of bitcoin will rise or fall using a method similar to that of The Stock Sonar. 

import pymongo
from prettytable import PrettyTable
import matplotlib.pyplot as graph
import requests
from bs4 import BeautifulSoup


#grab the price from the string and cast it as a float
def grabPrice(ind, string):
    grab = ""
    for i in range(ind + 1, len(string)):
        if string[i] == ',':
            pass
        elif string[i].isnumeric() or string[i] == '.':
            grab += string[i]
        else:
            break
    return float(grab)

#get the price of bitcoin today by connecting to coinmarketcap.com using requests package
def getPriceToday():
    content = requests.get("https://coinmarketcap.com/currencies/bitcoin/").content

    soup = BeautifulSoup(content, 'html.parser')

    page = soup.find_all('span', class_= 'cmc-details-panel-price__price')

    #print(str(page)[46:55])
    page = str(page)
    price = -1
    for i in range(0, len(page)):
        if page[i] == '$':
            price = grabPrice(i, page)
            break

    return price

#getRatings() returns total number of ratings as scores[0], positive ratings as 
#scores[1] and negative ratings as scores[2] and neutral ratings as scores[3]
def getRatings():
    #connect to database using pymongo api
    password = "g0ldf1sh"
    client = pymongo.MongoClient("mongodb+srv://GregDriscoll:"+password+"@cis400finalproject-bqfrw.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = client.get_database('TweetsWithRatings')
    ratings = db.Ratings

    #count postive and negative tweets
    scores = []
    neutral = 0
    pos = 0
    neg = 0
    for i in ratings.find():
        if i['rating'] > 0:
            pos += 1
        elif i['rating'] < 0:
            neg +=1
        else:
            neutral += 1
            
    #add results to list: [total, pos, neg, neutral] and return
    scores.append(ratings.count_documents({}))
    scores.append(pos)
    scores.append(neg)
    scores.append(neutral)
    
    return scores
#Use prettytable package to display table and return percentages
def printTableDay(scores):
    table = PrettyTable()
    table.field_names = ["Tweet Sentiment", "Number of Tweets", "Percent of Tweets"]

    #calculate percents for pos, neg, and neutral sentiment
    rows = ["Positive", "Negative", "Neutral"]
    allPercents = []
    for i in range(1, 4):
        percent = int (((float(scores[i]) / float(scores[0])) * 10000.0)) / 100.0
        #add pos, neg and neutral rows to table 
        table.add_row([rows[i-1], str(scores[i]), str(percent) + "%"])
        allPercents.append(percent)

    totalPercent = "100%"
    table.add_row(["Total", str(scores[0]), totalPercent])
    
    print(table)
    print()

    #return percents in list [pos, neg, neutral]
    return allPercents

def main():
    #get today's bitcoin price
    price = getPriceToday()
    #get number of postive negative and neutral ratings for new day
    scores = getRatings()

    #display table and get percents
    print("Bitcoin sentiment for new day:")
    percents = printTableDay(scores)

    #The Stock Sonar scoring based on positive vs negative tweets
    tssScore = float(scores[1] - scores[2]) / float(scores[1] + scores[2] + 3)
    print("The Stock Sonar Score is: " + str(tssScore))

    #add the scores and percents to the database with the price 
    password = "g0ldf1sh"
    client = pymongo.MongoClient("mongodb+srv://GregDriscoll:"+password+"@cis400finalproject-bqfrw.gcp.mongodb.net/test?retryWrites=true&w=majority")
    db = client.get_database('TweetsWithRatings')
    totalScores = db.TotalScores

    totalScores.insert_one({'total' : scores[0],
                            'pos' : scores[1],
                            'neg' : scores[2],
                            'neut' : scores[3],
                            'posPercent' : percents[0],
                            'negPercent' : percents[1],
                            'neutPercent' : percents[2],
                            'tssScore' : tssScore,
                            'btcPriceToday' : price})

    #print line graph to show the change over n days
    allScores = db.TotalScores

    graph.title('TSS sentiment rating Vs. Price')

    graph.subplot(2,1,1)
    
    plotPointsY1 = []
    plotPointsX1 = []
    for i in allScores.find():
        plotPointsY1.append(i['tssScore'])

    for x in range(0, allScores.count_documents({})):
        plotPointsX1.append(x + 1)

    graph.ylabel("TSS Scores")
    #graph.xlabel("Day Number")

    graph.axis([-0.1, allScores.count_documents({})+1, -1.1, 1.1])

    graph.plot(plotPointsX1, plotPointsY1)

    #graph.show()

    #print line graph to show price of bitcoin for n days
    graph.subplot(2,1,2)
    
    plotPointsY2 = []
    plotPointsX2 = []

    highPrice = 0
    
    for i in allScores.find():
        if i['btcPriceToday'] > highPrice:
            highPrice = i['btcPriceToday']
        plotPointsY2.append(i['btcPriceToday'])

    for x in range(0, allScores.count_documents({})):
        plotPointsX2.append(x+1)

    graph.ylabel("Bitcoin Price ($)")
    graph.xlabel("Day Number")

    graph.axis([-0.1, allScores.count_documents({})+1, 0, highPrice + 2000])

    graph.plot(plotPointsX2, plotPointsY2)

    graph.show()
    
        
main()

