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
package_installer('numpy')

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

cursor.execute("SELECT [Value01] FROM [41_53116].[dbo].[WELL_RESULT] WHERE ResultType = '01'")

#Writes the data to a csv. I'm assuming that only one column (pair of alleles) will be selected...
with open("C:\Users\melvin.huang\Desktop\datatable.csv", "w+") as datatable:
	writer = csv.writer(datatable)
	for row in cursor.fetchall():
		writer.writerow(row)


with open(new_file_path, "rb") as validation_file:
	with open(r"C:\Users\melvin.huang\Desktop\validation.csv", "w+") as formatted_file:
		validation_file_read = csv.reader(validation_file)
		formatted_file_write = csv.writer(formatted_file)
		validation_file_read.next()
		for row in validation_file_read:
			formatted_file_write.writerow([row[2], 
				row[3], 
				row[4],
				row[5],
				row[6],
				row[7],
				row[8],
				row[9],
				row[10],
				row[11],
				row[12],
				row[13],
				row[14],
				row[15],
				row[16],
				row[17],
				row[18],
				row[19]])

os.remove(new_file_path)

with open(r"C:\Users\melvin.huang\Desktop\validation.csv", "rb") as formatted_file:
	with open("C:\Users\melvin.huang\Desktop\datatable.csv", "rb") as datatable:
#file-splitting operation:
		formatted_reader = csv.reader(formatted_file)
		read_to_str = mmap.mmap(datatable.fileno(), 0, access = mmap.ACCESS_READ)
		line_number = 0
		for row in formatted_reader:
			index = 0
			line_number += 1
			while index <= (len(row) - 2):
				chunk = [row[index], row[index + 1]]
				chunk_string = " ".join(chunk)
				if read_to_str.find(chunk_string) != -1:
					print "match found on line ", line_number
					index += 2
				else:
					index += 2