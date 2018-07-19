def getDictionary(fileName):

	try:
		reportFile = open(fileName, "r")
	except:
		print "=======Error opening file " + fileName

	i = 0

	dic = {}

	for line in reportFile:
		i += 1
		if i < 6:
			continue

		lineInfo = line.split()
		# print lineInfo[3]
		if(lineInfo[3] == 'S' or lineInfo[3] == 'G'):
			# print lineInfo[1] + "\t" + lineInfo[4]
			dic[lineInfo[4]] = int(lineInfo[1])

	return dic

