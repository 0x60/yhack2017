import json
import tweepy
import sys
import random
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#Twitter credentials
consumer_key = 'Tjc28ECxL1ty5tFjdl4b5YhBX'
consumer_secret = 'KJWnUZDBcIiSKxHpwyOwgxPcjL9kzGBUummjdkWv7U7YzIzLY0'
access_token = '2922089034-LXhgqa8AHbfqep159glpZyJAHEGhfI4LO8HiPmg'
access_secret = 'XWGE4h9wxfgicQknDvU6BvKOYmpwZgcTveGH2Mn9tdtYo'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

#queryPos = "\"deep learning\" since:2016-11-21"
#resultsPos = api.search(q=queryPos, lang="en")
topic = sys.argv[1]
annualSentiment = []
annualFrequency = []

def getSentiment(text):
    # Instantiates a client
    client = language.LanguageServiceClient()

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    #print('Text: {}'.format(text))
    #print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

    return sentiment.score * sentiment.magnitude

def getYearlySentiment(year, topic):
    yearInc = year + 1
    queryString = "\"" + topic + "\" " + "since:" + str(year) + "-01-01" + "%20until:" + str(yearInc) + "-12-21"
    #print(queryString)

    results = api.search(q=queryString, lang="en")

    score = 0
    for tweet in results:
        score += getSentiment(tweet.text)

    annualSentiment.append(score/len(results))
    annualFrequency.append(len(results))
    
    return score/len(results)


output = []

for i in range(2001, 2016):

    yearScore = getYearlySentiment(i, topic) + random.uniform(0.001,0.000000001)

    print(str(i) + ": " + str(yearScore))

    output.append("%s\t%s\t%s" % (topic, str(annualSentiment), str(annualFrequency)))


filename = sys.argv[1] + '.json'
with open(filename, 'w') as outfile:
    json.dump(output, outfile)



