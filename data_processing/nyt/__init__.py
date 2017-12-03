def model(arr):
	return [(i["technology_id"], len(i["keywords"]) * 2) for i in arr]