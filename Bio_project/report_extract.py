def getDictionary(fileName):
	try:
		reportFile = open(fileName, "r")
	except:
		print "=======Error opening file " + fileName

	i = 0

	dic = {}
	d = list(reportFile)

	for i in range(0, len(d)-1):
		line = d[i].split()
		nextline = d[i+1].split()

		if line[3] == 'G' and (nextline[3] != '-' and nextline[3] != 'S'):
			dic[line[4]] = int(line[1])
	

		elif line[3] == 'S' and nextline[3] != '-':
			dic[line[4]] = int(line[1])
	
		# else:
		# 	continue

		# print line
		# try:
		# 	if(lineInfo[3] == 'G'):
		# 		# print "found a G with not a dash following it or an S!\n"
		# 		# print line
		# 		dic[lineInfo[4]] = int(lineInfo[1])
		# 		# print prevLineInfo
		# except:
		# 	print "-----------\n", fileName, "\n-----------\n"
		# 	break
	return dic

# print getDictionary("reports/male/SRS011157_output_report.txt")
