import requests
import argparse
import json
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

nyTimesAPIEndpoint = "http://api.nytimes.com/svc/search/v2/articlesearch.json"

startingYear = 2000
endingYear = 2017

monthDay = "0101"

apiKey = "6da0b227c38d4f6091ae5b16261a62bd"


def getNYTimesJSON(query):

	client = language.LanguageServiceClient()

	sentimentScoreEvolution = []
	articleCount = []

	

	for index in range(startingYear, endingYear, 1):
		pageNumber = 0
		
		endPoint = nyTimesAPIEndpoint + "?fq=body:(\"" + query + "\")"

		print index
		starting = index
		ending = index + 1

		endPoint += "&page=" + str(pageNumber)

		startingFull = str(index) + monthDay
		endPoint += "&begin_date=" + startingFull

		endingFull = None
		if index + 1 == endingYear:
			endingFull = str(index + 1) + "1202"
		else:
			endingFull = str(index + 1) + monthDay

		endPoint += "&end_date=" + endingFull

		endPoint += "&api-key=" + apiKey

		response = requests.get(endPoint)



		while(response.status_code != 200):
			response = requests.get(endPoint)


		respdict = json.loads(response.text)

		countArticle = respdict["response"]["meta"]["hits"]
		sentimentTotalScore = 0

		while respdict["response"]["meta"]["hits"] > respdict["response"]["meta"]["offset"]:
			oldString = "&page=" + str(pageNumber)
			pageNumber += 1
			newString = "&page=" + str(pageNumber)

			endPoint = endPoint.replace(oldString, newString)

			print endPoint


			for article in respdict["response"]["docs"]:
				text = article["snippet"]

				document = types.Document(
			    	content=text,
			    	type=enums.Document.Type.PLAIN_TEXT)

				# Detects the sentiment of the text
				sentiment = client.analyze_sentiment(document=document).document_sentiment

				sentimentTotalScore += sentiment.score

			response = requests.get(endPoint)

			print response.status_code

			while(response.status_code != 200):
				response = requests.get(endPoint)

			respdict = json.loads(response.text)

		
		if countArticle != 0:
			averageSentimentScore = float(sentimentTotalScore) / countArticle
			sentimentScoreEvolution.append(averageSentimentScore)
		else:
			sentimentScoreEvolution.append(None)

		articleCount.append(countArticle)

	return sentimentScoreEvolution, articleCount



if __name__ == '__main__':
	# Instantiates a client
	

	sentiment, article = getNYTimesJSON("deep learning")
	print sentiment 
	print article 


