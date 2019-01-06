import urllib2
import os
# from extract_labels import get_one_website

i = 0
try:
	for f in os.listdir("../zipfiles"):
		if os.path.isfile("./AmericanGutData/" + str(f).replace(".gz", ".txt")):
			print "File exists!\n"
			i += 1
			continue

		print "Zipfile is ", f

		print "-", i, "- \n__________\n"

		# Do the kraken process
		print "Kraken process started ...."
		os.system("kraken --only-classified-output --db minikraken_20171101_8GB_dustmasked --fastq-input --gzip-compressed ../zipfiles/"+f+" > example.kraken")
		os.system("kraken-report --db minikraken_20171101_8GB_dustmasked example.kraken > ./AmericanGutData/" + f.replace(".gz", ".txt").replace("./", ""))

		print "Kraken process done! Files stored"

		# # delete the example file and the zip file
		# os.remove(zipFileName)
		os.remove("example.kraken")
		# print "Deleted the files"


		print "===============\n\n"
		
		i += 1

except KeyboardInterrupt:
	print "\n====KeyboardInterrupt====\n\n"

except:
	print "Some problem with file=" + str(f)
	
# for line in f:
# 	if os.path.isfile("./AmericanGutData/" + str(line.split()[2]) + ".txt"):
# 		print "File ", line.split()[2], "exists!\n===================\n"
# 		i += 1
# 		continue
# 	url = line.split()[-4]
# 	url = "http://" + url
# 	if url == "http://sra_ftp":
# 		continue
# 	print i, ": ", url
# 	try:
# 		response = urllib2.urlopen(url)
# 		outp = response.read()
# 	except KeyboardInterrupt:
# 		print "\n====KeyboardInterrupt====\n\n"
# 		break
# 	except:
# 		print "ERROR 404!\n===================\n"
# 		i += 1
# 		continue

#  #    # Label extraction for that file
# 	# url = line.split()[2]
# 	# if os.path.isfile("./labels/" + url + ".json"):
# 	# 	print "File ", url, "exists!\n===================\n"
# 	# 	continue

# 	# url = "https://www.ebi.ac.uk/ena/data/view/"+url+"&display=xml&download=xml&filename="+url+".xml"
# 	# get_one_website(url, i)
# 	# # ==========================================


# 	# Store the zip file
# 	zipFileName = "./"+str(line.split()[2])+".gz"
# 	outputFile = open(zipFileName, "w")
# 	outputFile.write(outp)
# 	outputFile.close()
# 	print "Zipfile saved"	

# 	# Do the kraken process
# 	print "Kraken process started ...."
# 	os.system("kraken --only-classified-output --db minikraken_20171101_8GB_dustmasked --fastq-input --gzip-compressed "+zipFileName+" > example.kraken")
# 	os.system("kraken-report --db minikraken_20171101_8GB_dustmasked example.kraken > ./AmericanGutData/" + zipFileName.replace(".gz", ".txt").replace("./", ""))
# 	print "Kraken process done"

# 	# delete the example file and the zip file
# 	os.remove(zipFileName)
# 	os.remove("example.kraken")
# 	print "Deleted the files"

# 	print "===============\n\n"
	
# 	i += 1
	
