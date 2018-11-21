import os
import report_extract as re
from sets import Set
import json

allKeys = []

for file in os.listdir("./AGData/"):
	if ".txt" not in file:
		continue
	path = "./AGData/" + str(file)
	# print path
	locDict = re.getDictionary(path)
	# print locDict

	# print str(locDict) + "\n\n"
	# Go through every key-value pair in locDict, 
	# and check if that key is present in the allKeys. 
	# If yes, then do nothing, else add that key to the allKeys

	for key, val in locDict.items():
		if key not in allKeys:
			allKeys.append(key)

allKeys = Set(allKeys)
print "Now printing the dicts after making all of them the same size"

for file in os.listdir("./AGData/"):
	if ".txt" not in file:
		continue
	path = "./AGData/" + str(file)
	locDict = re.getDictionary(path)

	# newFile = "./reports/male/" + "vec_" + str(file)

	locSet = Set(locDict.keys())

	newKeys = allKeys - locSet

	for i in newKeys:
		locDict[i] = 0

	filetemp = file.replace(".txt", ".json")
	path = "./AGjsons/" + filetemp
	with open(path, 'w') as fp:
		json.dump(locDict, fp, sort_keys=True, indent=4)

	print str(len(locDict)) + "====\n"


