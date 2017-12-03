# Preliminary model to calculate the relevancy of a certain technology
import json

import sys
import numpy as np
from scipy import stats


technologies = [
	{
		"technology_id": 0,
		"technology_name": "Deep Learning",
		"keywords": ["deep learning", "computer vision", "autonomous vehicles"],
		"companies": ["MSFT", "GOOG", "UBER"]
	},
	{
		"technology_id": 1,
		"technology_name": "Smart Assistants",
		"keywords": ["siri", "google home", "alexa"],
		"companies": ["GOOG", "AAPL", "AMZN"]
	},
	{
		"technology_id": 2,
		"technology_name": "Blockchain",
		"keywords": ["blockchain", "cryptocurrency"],
		"companies": ["GOOG", "GS"]
	}
]


rankingCompaniesByAcquisitions = ["GOOG", "AAPL", "MSFT", 
									"INTC", "FB", "TWTR", 
									"CRM", "AMZN", "BIDU", "UBER"]

rankingCompaniesByInvestments = ["SBI", "GOOG", "OSTK", "CITI", "GS"]



def processFloatVector(array):
	temp = []
	for elem in array:
		elem = elem.strip()
		if elem == "None":
			temp.append(None)
		else:
			temp.append(float(elem))

	return temp

def processStartupFile(fileObject):
	mappingCompaniesToAcquisitions = {}
	for line in fileObject:
		if "#" in line:
			continue
		lineSplit = line.rstrip().split(",")
		companyTicker = lineSplit[0]
		startupCount = int(lineSplit[1])
		mappingCompaniesToAcquisitions[companyTicker] = startupCount
	return mappingCompaniesToAcquisitions

def processNASDAQFile(fileObject):
	myMap = {}
	for line in fileObject:
		if "#" in line:
			continue
		lineSplit = line.rstrip().split("\t")
		companyTicker = lineSplit[0]
		stockPrice = processFloatVector(lineSplit[1][1:-1].split(","))
		myMap[companyTicker] = stockPrice
	return myMap

def processNYTimes(fileObject):
	myMap = {}
	for line in fileObject:
		if "#" in line:
			continue
		lineSplit = line.rstrip().split("\t")


		keyword = lineSplit[0]
		sentimentArray = processFloatVector(lineSplit[1][1:-1].split(","))
		count = [int(x) for x in lineSplit[2][1:-1].split(",")]

		myMap[keyword] = {
			"sentiment": sentimentArray,
			"count": count 
		}
	return myMap

def processGuardian(fileObject):
	myMap = {}
	for line in fileObject:
		if "#" in line:
			continue
		lineSplit = line.rstrip().split("\t")
		keyword = lineSplit[0]
		frequencies = [int(x) for x in lineSplit[1][1:-1].split(",")]
		myMap[keyword] = frequencies
	return myMap


def modelCommercialRelevancyScore(startup, nyTimes, nasdaq, guardian, twitterData, blockchainInvestments):
	startupMap = processStartupFile(startup)
	nyTimesMap = processNYTimes(nyTimes)
	nasdaqMap = processNASDAQFile(nasdaq)
	guardianMap = processGuardian(guardian)
	blockchainMap = processStartupFile(blockchainInvestments)

	totalSentiment = 0

	technologyRelevancies = []
	

	for element in technologies:
		technologyKeywordRelevancies = []
		keywords = element["keywords"]
		for word in keywords:
			totalYears = len(nyTimesMap[word]["sentiment"])
			totalTwitterYears = len(twitterData[word]["sentiment"])
			sumCount = sum(nyTimesMap[word]["count"])
			sumTwitter = sum(twitterData[word]["count"])
			totalKeywordSentiment = 0
			for i in range(totalYears):
				if nyTimesMap[word]["sentiment"][i] == None:
					continue
				else:
					totalKeywordSentiment += nyTimesMap[word]["count"][i] * nyTimesMap[word]["sentiment"][i] 
			for i in range(totalTwitterYears):
				totalKeywordSentiment += twitterData[word]["count"][i] * twitterData[word]["sentiment"][i] 

			totalKeywordSentiment /= float(sumCount + sumTwitter)

			slope, intercept, r, p, e = stats.linregress(range(totalYears), nyTimesMap[word]["count"])
			slopeG, interceptG, rG, pG, eG = stats.linregress(range(len(guardianMap[word])), guardianMap[word])

			technologyKeywordRelevancies.append(slope * slopeG * totalKeywordSentiment)

			totalSentiment += slope * slopeG * totalKeywordSentiment



	
		acquisitionValue = 0
		averageDifferenceStock = []
		for company in element["companies"]:
			if element["technology_id"] == 0 or element["technology_id"] == 1:
				acquisitionValue += (len(rankingCompaniesByAcquisitions) - rankingCompaniesByAcquisitions.index(company)) * startupMap[company]
			else:
				acquisitionValue += (len(rankingCompaniesByInvestments) - rankingCompaniesByInvestments.index(company)) * blockchainMap[company]


			if company not in nasdaqMap:
				continue
			stockValues = nasdaqMap[company]
			differenceValue = sum([b - a for a, b in zip(stockValues[::2], stockValues[1::2])]) / len(stockValues)
			averageDifferenceStock.append(differenceValue)

		averageDifferenceStockValue = np.mean(averageDifferenceStock)
		acquisitionValue /= float(len(element["companies"]))



		topTierNeuralNetworkOutput = 0.1 * totalSentiment + 3.0 * acquisitionValue + 0.6 * averageDifferenceStockValue
		print totalSentiment, acquisitionValue, averageDifferenceStockValue

		# print technologyKeywordRelevancies


		technologyRelevancies.append((element["technology_name"], topTierNeuralNetworkOutput))

			
	

	print technologyRelevancies




def dumpJSON(startup, nyTimes, nasdaq, guardian):
	with open("results/aiStartupAcquisitions.json", "w") as fp:
		json.dump(processStartupFile(startup), fp)

	with open("results/nytimesResults.json", "w") as fp:
		json.dump(processNYTimes(nyTimes), fp)

	with open("results/companyNASDAQData.json", "w") as fp:
		json.dump(processNASDAQFile(nasdaq), fp)

	with open("results/theguardianResults.json", "w") as fp:
		json.dump(processGuardian(guardian), fp)


if __name__ == '__main__':
	startupAcquistions = open("results/aiStartupAcquisitions.txt", 'r')
	nytimesResults = open("results/nytimesResults.txt", 'r')
	companyNASDAQData = open("results/companyNASDAQData.txt", 'r')
	guardianResults = open("results/theguardianResults.txt", 'r')
	blockchainInvestments = open("results/blockchainStartupInvestment.txt", 'r')
	with open("results/twitter.json") as f:
		twitterData = json.load(f)

	modelCommercialRelevancyScore(startupAcquistions, nytimesResults, companyNASDAQData, guardianResults, twitterData, blockchainInvestments)
	# dumpJSON(startupAcquistions, nytimesResults, companyNASDAQData, guardianResults)