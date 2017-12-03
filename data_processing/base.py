import nyt
import test

def merge(techs, arr):
	output1 = {}
	output2 = {}

	# append to temp
	for lst in arr:
		for el in lst:
			if str(el[0]) not in output1:
				output1[str(el[0])] = 0
			output1[str(el[0])] += el[1]

	# match output1
	for tech in techs:
		output2[tech["technology_name"]] = output1[str(tech["technology_id"])]

	return output2



out1 = nyt.model(technologies)
out2 = test.model(technologies)

print merge(technologies, [out1, out2])