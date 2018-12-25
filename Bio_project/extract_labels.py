import urllib2
import os
from bs4 import BeautifulSoup
import json

urls = []
names = []

def generate_urls():
	global urls
	global names

	with open("PRJEB11419.txt", "r") as f:
		for line in f:
			url = line.split()[2]
			if os.path.isfile("./labels/" + url + ".json"):
				print "File ", url, "exists!\n===================\n"
				continue

			names.append(url)
			url = "https://www.ebi.ac.uk/ena/data/view/"+url+"&display=xml&download=xml&filename="+url+".xml"
			urls.append(url)
	

	urls = urls[1:]
	names = names[1:]

def get_one_website(url, name):

	labels = {}

	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	
	soup = BeautifulSoup(response, "lxml")

	for pair in soup.find_all('sample_attribute'):
		labels[pair.tag.contents[0]] = pair.value.contents[0]

	with open("./labels/" + str(name) + ".json", 'w') as fp:
		json.dump(labels, fp, sort_keys=True, indent=4)

def get_all_websites():
	global urls
	global names

	for i in range(len(urls)):
		print "Working on ", names[i]
		print urls[i]
		print "--------------\n\n"
		get_one_website(urls[i], names[i])
	
generate_urls()
get_all_websites()	
