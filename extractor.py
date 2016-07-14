#!/usr/bin/python
import csv
import os
import shutil
import mmap
import io



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

val_file_path = r"C:\Users\melvin.huang\Desktop\validation.csv"

with open(new_file_path, "rb") as validation_file:
	with open(val_file_path, "w+") as formatted_file:
		validation_file_read = csv.reader(validation_file)
		formatted_file_write = csv.writer(formatted_file, delimiter = ",")
		validation_file_read.next()

		for row in validation_file_read:
			index = 2
			while index <= (len(row) - 6):
				formatted_file_write.writerow([row[0], row[index], row[index + 1]])
				index += 2

os.remove(new_file_path)
print "checkpoint 0"

#paths to each file
trays_path = r"C:\Users\melvin.huang\Desktop\trays.csv"
wells_path = r"C:\Users\melvin.huang\Desktop\wells.csv"
alleles_path = r"C:\Users\melvin.huang\Desktop\alleles.csv"


#Returns a csv of all the tray IDs
with open(trays_path, "w+") as trayfile:
	cursor.execute("SELECT TrayID FROM [41_53116].[dbo].[tray] ORDER BY adddt DESC")
	writer = csv.writer(trayfile)
	for row in cursor.fetchall():
	
		writer.writerow(row)
print "checkpoint 1"

#for each tray ID, output the wells and samples
with open(trays_path, "rb") as trayfile:
	with open(wells_path, "w+") as wellsfile:
		well_writer = csv.writer(wellsfile)
		tray_reader = csv.reader(trayfile)
		for entry in tray_reader:
			cursor.execute("SELECT WellID, SampleIDName FROM [41_53116].[dbo].[well],[41_53116].[dbo].[sample] WHERE TrayID = ? AND [well].SampleID = [sample].SampleID", entry)
			for line in cursor.fetchall():
				well_writer.writerow(line)

print "checkpoint 2"

with open(wells_path, "rb") as wells_file:
	with open(alleles_path, "w+") as allele_file:
		wells_reader = csv.reader(wells_file)
		writer = csv.writer(allele_file, delimiter = " ", quoting = csv.QUOTE_MINIMAL)
		for line in wells_reader:
			well_id = line[0]
			sample_id_name = line[1]
			cursor.execute("SELECT Value01 FROM [41_53116].[dbo].[WELL_RESULT] WHERE ResultType = '01' AND wellid =?", well_id)
			for line in cursor.fetchall():
				stringify = "".join(line)
				first_allele = stringify.split()[0]
				second_allele = stringify.split()[1]
				writer.writerow([sample_id_name, first_allele, second_allele])

print "checkpoint 3"


with open(val_file_path, "rb") as val_file:
	val_reader = csv.reader(val_file)
	with open(alleles_path, "rb") as allele_file:
		read_to_str = mmap.mmap(allele_file.fileno(), 0, access = mmap.ACCESS_READ)
		for row in val_reader:
			stringify = " ".join(row)
			if read_to_str.find(stringify) != -1:
				print row[0], "found match on pair", row[1], row[2]
			else:
				print row[0], "did not find match on pair", row[1], row[2]


			#analysis(formatted_file, sample_id_name)


		#insert function to read the file and do analysis to it.

<<<<<<< HEAD
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
=======
>>>>>>> new-algorithm
