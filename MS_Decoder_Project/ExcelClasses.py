import pandas as pd
import numpy as np

class DataSheet:

	# Construct a datasheet with a given filename and spreadsheetname, and initializes the samples
	def __init__(self, fileName, spreadsheetName):
		self.fileName = fileName
		self.spreadsheetName = spreadsheetName
		self.samples = pd.read_excel(fileName, spreadsheetName)

	# Returns a histogram out of all the tables in a given column
	def getHistoCols(self, j):
		totalHisto = {}

		for i in range(0, 40):
			tble = Table(self.samples, i, j)
			histoTble = tble.histo

			for tag, ser in histoTble.items():
				if tag not in totalHisto:
					totalHisto[tag] = ser
					continue
				totalHisto[tag] = np.add(totalHisto[tag], ser)

		return totalHisto

	# Returns a histogram of a particular column and energy, with just n tags
	def getHistoColsEnergyNTags(self, j, isHighEnergy, n):
		totalHisto = {}
		count = 0
		for i in range(0, 40):
			tble = Table(self.samples, i, j)
			if(isHighEnergy != tble.isHighEnergy or n != tble.numberOfTags):
				continue
			count += 1
			histoTble = tble.histo

			for tag, ser in histoTble.items():
				if tag not in totalHisto:
					totalHisto[tag] = ser
					continue
				totalHisto[tag] = np.add(totalHisto[tag], ser)
		print("\n=== The table for column = "+str(j)+", High energy? = "+str(isHighEnergy)+", number of tags = " + str(n) + ", (total count = "+str(count)+") ===")
		return totalHisto

class Table:

	# Construct a table object with data members row, column, samples dataframe, numberOfTags, and isHighEnergy
	def __init__(self, samples, row, col):

		self.row = row
		self.col = col
		self.samples = samples

		r = row*16 + 5
		c = col*10 + 1

		string = samples.iloc[r:r+15 ,  c:c+9].iloc[0,0]
		self.isHighEnergy = False
		if str(type(string)) == "<type 'float'>":
			string = samples.iloc[r:r+15 ,  c:c+9].iloc[0,1]
		if "High" in string:
			self.isHighEnergy = True

		i = 0
		for i in range(1, 9):
			if str(type(samples.iloc[r:r+15 ,  c:c+9].iloc[3,i])) == "<type 'float'>":
				i = i-1
				break

		self.numberOfTags = i
		self.histo = self.getHisto()

	# Returns the histogram for that table (private method). Use self.histo property!
	def getHisto(self):
		r = self.row*16 + 5
		c = self.col*10 + 1
		table = self.samples.iloc[r:r+15 ,  c:c+9]
		
		histo = {}
		
		self.numCorrectCells = 0

		# Go column by column, starting from the column with tag "0"
		for i in range(1, 9):
			
			# This means that we do not have any more tags left  
			try:
				if str(type(table.iloc[3,i])) == "<type 'float'>":
					break
			except:
				print "i=" + str(i)
			
			if str(table.iloc[3,i]) == "Tag on byte":
				continue
				
			correctCode = str(table.iloc[4,i])
			tag = str(table.iloc[3,i])
			histo[tag] = [0, 0, 0, 0, 0, 0, 0, 0]
			
			for j in range(5, 13):
				if correctCode == str(table.iloc[j, i]):
					histo[tag][j-5] += 1
					self.numCorrectCells += 1
					
		return histo



# Print out a histogram
def printHisto(histo):
	print("\nSeries:\t\t\ta\tb\tc\td\tw\tx\ty\tz\n")

	def seriesString(arr):
		s = ""
		for i in arr:
			s = s + str(i) + "\t"
		return s

	for tag, series in histo.items():
		s = seriesString(series)
		print("Tag " + str(tag) + "\t\t\t" + s)


# fileName = "samples.xlsx"
# spreadsheetName = "Isotope not necessarily lower"

# d = DataSheet(fileName, spreadsheetName)
# printHisto(d.getHistoColsEnergyNTags(0, True, 4))

# t = Table(d.samples, 0,3)
# print t.isHighEnergy
