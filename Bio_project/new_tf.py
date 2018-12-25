import json
import numpy as np
import pandas as pd
from collections import OrderedDict
import tensorflow as tf
import os

# Used for standardizing a random variable
from sklearn.preprocessing import scale


# filename = "/Users/samjain/Documents/Summer-Research/Bio_project/AGjsons/127.json"

# Generate a vector of features from the given file
def getVector(filename):
	dic = {}
	with open(filename) as file:
		dic = json.load(file, object_pairs_hook=OrderedDict)

	# The vectore of the values
	vec = dic.values()
	return vec

x = []
y = []
# Add to the matrix with vectors from the files
def addToMatrix(folder):
	for file in os.listdir(folder):
		vec = getVector(folder + file)
		print "mean=", np.array(vec).mean(), " std=", np.array(vec).std()
		x.append(vec)
		if "female" in folder:
			y.append(1)
		else:
			y.append(0)


maleFolder = "./jsons/male/"
femaleFolder = "./jsons/female/"
addToMatrix(maleFolder)
# print x[0]