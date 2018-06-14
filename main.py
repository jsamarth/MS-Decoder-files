import ExcelClasses as ec


fileName = "samples.xlsx"
spreadsheetName = "Isotope not necessarily lower"

col = raw_input("Column: ")
numberOfTags = raw_input("Number of tags: ")

d = ec.DataSheet(fileName, spreadsheetName)
ec.printHisto(d.getHistoColsEnergyNTags(int(col), True, int(numberOfTags)))