import urllib2
import os
# from extract_labels import get_one_website

f = open("PRJEB11419.txt", "r")
i = 0
for line in f:

	url = line.split()[-4]
	url = "http://" + url
	if url == "http://sra_ftp":
		continue
	print i, ": ", url
	if os.path.isfile("./zipfiles/"+str(line.split()[2])+".gz"):
		print "File ", url, "exists!\n===================\n"
		i += 1
		continue
	try:
		response = urllib2.urlopen(url)
		outp = response.read()
	except KeyboardInterrupt:
		print "\n====KeyboardInterrupt====\n\n"
		break
	except:
		print "ERROR 404!\n===================\n"
		i += 1
		continue

 #    # Label extraction for that file
	# url = line.split()[2]
	# if os.path.isfile("./labels/" + url + ".json"):
	# 	print "File ", url, "exists!\n===================\n"
	# 	continue

	# url = "https://www.ebi.ac.uk/ena/data/view/"+url+"&display=xml&download=xml&filename="+url+".xml"
	# get_one_website(url, i)
	# # ==========================================


	# Store the zip file
	zipFileName = "./zipfiles/"+str(line.split()[2])+".gz"
	outputFile = open(zipFileName, "w")
	outputFile.write(outp)
	outputFile.close()
	print "Zipfile saved"	

	print "===============\n\n"
	
	i += 1
	
