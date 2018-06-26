import ExcelClasses as ec


fileName = "samples.xlsx"
spreadsheetName = "Isotope not necessarily lower"

col = raw_input("Column: ")
numberOfTags = raw_input("Number of tags: ")
isHighEnergy = False
inp = raw_input("Is it High Energy? (y/n): ")
if(inp == 'y'):
	isHighEnergy = True

d = ec.DataSheet(fileName, spreadsheetName)
ec.printHisto(d.getHistoColsEnergyNTags(int(col), isHighEnergy, int(numberOfTags)))