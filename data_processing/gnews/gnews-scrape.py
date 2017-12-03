import requests
import json

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

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

    return sentiment.score


def getDailySentiment(year, topic, payload):
    r = requests.get('https://newsapi.org/v2/everything', params=payload)
    rJson = json.loads(r.text)
    res_list = rJson['articles']

    textList = []

    for art in res_list:
        textList.append(art['description'])

    score = 0;
    for desc in textList:
        score += getSentiment(desc)

    return score

def main():
    key = '7a2085b48b074e2c89f70738004a5a19'
    lang = 'en'
    keyword = 'deep learning'

    output = []
    x = []
    y = []

    for i in range(1, 30):

        fromDate = "2017-11-"+str(i)
        toDate = "2017-11-"+str(i)
        payload = {'q':keyword, 'from':fromDate,'to':toDate,'language':lang,'apiKey':key}

        dailyScore = getDailySentiment(i, keyword, payload)

        print(str(i) + ": " + str(dailyScore))

        x.append(int(i))
        y.append(dailyScore)

    output.append(x)
    output.append(y)

    filename = keyword + '.json'
    with open(filename, 'w') as outfile:
        json.dump(output, outfile)

if __name__ == "__main__":
    main()


