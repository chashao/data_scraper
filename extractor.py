#!/usr/bin/python
import csv
import os

# run for windows machines to install the necessary packages to run the rest of the code
# takes the name of the package to be installed as a string
def package_installer(package):
	import importlib
	try:
		importlib.import_module(package)
	except ImportError:
		import pip
		pip.main(['install', package])
	finally:
		globals()[package] = importlib.import_module(package)


path_to_validation_file = 'C:\Users\melvin.huang\AppData\Local\Microsoft\Windows\Temporary Internet Files\Content.Outlook\1J403MGV\06-19-14 NGS Validation Panel Allele Database.xlsx'
filename, file_ext = os.path.split(path_to_validation_file)
new_file_path = filename + 'csv'


# Connects to the database specified and pulls the datatable requested, writing it to a csv file
# MS SQL Server 2012 and 2014 uses Native Client 11.0. Change the other elements of the string to 
# connect to the desired server.

package_installer('pyodbc')

# DO NOT TOUCH THE FORMATTING OF THE LINE BELOW!!!!!!
connection = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};' r'SERVER=(local)\FUSION_SQL14EXP;' r'DATABASE=41_53116;' r'TRUSTED_CONNECTION=yes;')
cursor = connection.cursor()

cursor.execute("SELECT [SampleIDName], [WellPosition], [Value01], [ResultType] FROM ([41_53116].[dbo].[WELL] JOIN [41_53116].[dbo].[SAMPLE] ON [41_53116].[dbo].[SAMPLE].SampleID = [41_53116].[dbo].[WELL].SampleID) JOIN [41_53116].[dbo].[WELL_RESULT] ON [41_53116].[dbo].[WELL_RESULT].WellID = [41_53116].[dbo].[WELL].WellID WHERE [41_53116].[dbo].[WELL_RESULT].ResultType > '01' AND [41_53116].[dbo].[WELL_RESULT].ResultType < '04'")


with open("datatable.csv", "w+") as datatable:
	writer = csv.writer(datatable)
	for row in cursor.fetchall():
		writer.writerow(row)
	datatable.close()


with open("datatable.csv", "rb") as datatable_read:
	with open(new_file_path, "rb") as validation_file:
		reader = csv.reader(datatable_read)
		val_reader = csv.reader(validation_file)
		val_reader_indexed = list(val_reader)
		counter = 1
		output = open("output.txt", "w+")
		for i, row in enumerate(reader):
			if row != val_reader_indexed[i]:
				output.write(counter)
				counter += 1
			else:
				counter += 1
		output.close()
		validation_file.close()
	datatable_read.close()

		
			

