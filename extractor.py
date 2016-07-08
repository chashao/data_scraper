#!/usr/bin/python
import csv
import os
import shutil
import mmap


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

package_installer('xlrd')
package_installer('pyodbc')

path_to_validation_file = r"C:\Users\melvin.huang\Desktop\06-19-14 NGS Validation Panel Allele Database.xlsx"
filename, file_ext = os.path.splitext(path_to_validation_file)
new_file_path = filename + '.csv'

def csv_from_excel(excel_file, csv_file):
    wb = xlrd.open_workbook(excel_file)
    sheet = wb.sheet_by_index(0)
    my_csv_file = open(csv_file, 'w+')
    wr = csv.writer(my_csv_file)

    for rownum in xrange(sheet.nrows):
        wr.writerow(sheet.row_values(rownum))

    my_csv_file.close()

csv_from_excel(path_to_validation_file, new_file_path)



# Connects to the database specified and pulls the datatable requested, writing it to a csv file
# MS SQL Server 2012 and 2014 uses Native Client 11.0. Change the other elements of the string to 
# connect to the desired server.

# DO NOT TOUCH THE FORMATTING OF THE LINE BELOW!!!!!!
connection = pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};' r'SERVER=(local)\FUSION_SQL14EXP;' \
	r'DATABASE=41_53116;' r'TRUSTED_CONNECTION=yes;')
cursor = connection.cursor()

cursor.execute("SELECT TOP 100000 [Value01] FROM [41_53116].[dbo].[WELL_RESULT] WHERE ResultType = '01'")

#Writes the data to a csv. I'm assuming that only one column (pair of alleles) will be selected...
with open("C:\Users\melvin.huang\Desktop\datatable.csv", "w+") as datatable:
	writer = csv.writer(datatable)
	for row in cursor.fetchall():
		writer.writerow(row)
	datatable.close()


# Writes the validation csv to a txt file for easy, non-structured parsing.
with open(new_file_path, 'rb') as temp:
	with open(r"C:\Users\melvin.huang\Desktop\validation.txt", "w+") as validation_txt:
		tmp_reader = csv.reader(temp)
		for row in tmp_reader:
			rowstring = ', '.join(row)
			validation_txt.write(rowstring)
os.remove(new_file_path)

# Comparison algorithm... Takes in a list of two elemets, converts it to string,
# and reads through the converted validation file to find matches. 

with open(r"C:\Users\melvin.huang\Desktop\validation.txt", "rb") as validation_file:
	with open("C:\Users\melvin.huang\Desktop\datatable.csv", "rb") as datatable_file:
		datatable_file_reader = csv.reader(datatable_file, delimiter = ' ')
		read_to_str = mmap.mmap(validation_file.fileno(), 0, access = mmap.ACCESS_READ)
		total_matches = 0
		counter = 1
		for row in datatable_file_reader:
			pair_str = ', '.join(row)
			if read_to_str.find(pair_str) != -1:
				total_matches += 1
				print(counter)
				counter += 1
			else:
				counter += 1
		print(str(total_matches) + " total matches")