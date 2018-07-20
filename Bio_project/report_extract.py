def getDictionary(fileName):

	try:
		reportFile = open(fileName, "r")
	except:
		print "=======Error opening file " + fileName

	i = 0

	dic = {}

	prevLineInfo = ['0', '0', '0', '0', '0']
	for line in reportFile:

		lineInfo = line.split()
		# print prevLineInfo
		if((lineInfo[3] != '-' and lineInfo[3] != 'S') and prevLineInfo[3] == 'G'):
			# print "found a G with not a dash following it or an S!\n"
			# print line
			dic[prevLineInfo[4]] = int(prevLineInfo[1])
			# print prevLineInfo


		prevLineInfo = lineInfo

	return dic

# print getDictionary("reports/male/SRS011157_output_report.txt")
