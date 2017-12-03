def model(arr):
	return [(i["technology_id"], len(i["keywords"])) for i in arr]