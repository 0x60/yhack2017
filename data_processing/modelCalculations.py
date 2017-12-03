# Preliminary model to calculate the relevancy of a certain technology
import json
import sys

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
	}
]


rankingCompaniesByAcquisitions = ["GOOG", "AAPL", "MSFT", 
									"INTC", "FB", "TWTR", 
									"CRM", "AMZN", "BIDU", "UBER"]


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

		print lineSplit
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


def modelCommercialRelevancyScore(startup, nyTimes, nasdaq, guardian):
	return
	# print processStartupFile(startup)
	# print processNASDAQFile(nasdaq)
	# print processNYTimes(nyTimes)
	# print processGuardian(guardian)



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
	modelCommercialRelevancyScore(startupAcquistions, nytimesResults, companyNASDAQData, guardianResults)
	dumpJSON(startupAcquistions, nytimesResults, companyNASDAQData, guardianResults)