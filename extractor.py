#!/usr/bin/python
import csv
import os
import shutil
import mmap
import sys

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


driver_name = r'SQL Server Native Client 11.0'
server_name = r'(local)\FUSION_SQL14EXP'
database_name = sys.argv[1] # you need to enter that in the terminal yourself
trusted = 'yes'
tray_id = sys.argv[2]

def find_val_file(filename):
	for r, d, f in os.walk("C:\\"):
		for files in f:
			if files == filename:
				return os.path.join(r, files)


# the assumption is made here that the name of the file will not be changed for all eternity 
path_to_validation_file = find_val_file(r"06-19-14 NGS Validation Panel Allele Database.xlsx")
filename, file_ext = os.path.splitext(path_to_validation_file)
new_file_path = filename + '.csv'

#turns the xls file to a csv for ease of use
def csv_from_excel(excel_file, csv_file):
    wb = xlrd.open_workbook(excel_file)
    sheet = wb.sheet_by_index(0)
    my_csv_file = open(csv_file, 'w+')
    wr = csv.writer(my_csv_file)

    for rownum in xrange(sheet.nrows):
        wr.writerow(sheet.row_values(rownum))

    my_csv_file.close()

csv_from_excel(path_to_validation_file, new_file_path)


print "Lately, I've been, I've been losing sleep"


# Connects to the database specified and pulls the datatable requested, writing it to a csv file
# MS SQL Server 2012 and 2014 uses Native Client 11.0. Change the other elements of the string to 
# connect to the desired server.

# DO NOT TOUCH THE FORMATTING OF THE LINE BELOW!!!!!!
# will eventually variable-ize these... and completed :)


connection = pyodbc.connect(r'DRIVER={%s};' r'SERVER=%s;' r'DATABASE=%s;' r'TRUSTED_CONNECTION=%s;' % (driver_name, server_name, database_name, trusted))

cursor = connection.cursor()

#paths to each file
val_file_path = os.path.join(os.getcwd(), r"validation.csv")
trays_path = os.path.join(os.getcwd(), r"trays.csv") 
wells_path =  os.path.join(os.getcwd(), r"wells.csv")
alleles_path =  os.path.join(os.getcwd(), r"alleles.csv")
results_path =  os.path.join(os.getcwd(), r"results.csv")


#SQL queries - will eventually figure out how to turn the database name into a variable
tray_selector = "SELECT TrayID FROM tray WHERE trayID = ?"
well_and_sample_selector = "SELECT WellID, SampleIDName FROM well, sample WHERE TrayID =? AND [well].SampleID = [sample].SampleID"
allele_selector = "SELECT Value01 FROM WELL_RESULT WHERE ResultType = '01' AND wellid = ?"

#modifies the validation file into something that can be easily parsed
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


print "Dreaming about the things that we could be"


#Returns a csv of all the tray IDs
with open(trays_path, "w+") as trayfile:
	cursor.execute(tray_selector, tray_id)
	writer = csv.writer(trayfile)
	for row in cursor.fetchall():
		writer.writerow(row)


print "But baby, I've been, I've been praying hard"


#for each tray ID, output the wells and samples
with open(trays_path, "rb") as trayfile:
	with open(wells_path, "w+") as wellsfile:
		well_writer = csv.writer(wellsfile)
		tray_reader = csv.reader(trayfile)
		for entry in tray_reader:
			cursor.execute(well_and_sample_selector, entry)
			for line in cursor.fetchall():
				well_writer.writerow(line)


print "Said no more counting dollars"


#tags each allele pair with the corresponding sample ID name
with open(wells_path, "rb") as wells_file:
	with open(alleles_path, "w+") as allele_file:
		wells_reader = csv.reader(wells_file)
		writer = csv.writer(allele_file, delimiter = " ", quoting = csv.QUOTE_MINIMAL)
		for line in wells_reader:
			well_id = line[0]
			sample_id_name = line[1]
			cursor.execute(allele_selector, well_id)
			for line in cursor.fetchall():
				stringify = "".join(line)
				first_allele = stringify.split()[0]
				second_allele = stringify.split()[1]
				writer.writerow([sample_id_name, first_allele, second_allele])


print "We'll be counting stars"

#comparison algorithm
#should I be implementing a similarity algorithm here, like Levenshtein?

with open(val_file_path, "rb") as val_file:
	val_reader = csv.reader(val_file)
	with open(alleles_path, "rb") as allele_file:
		with open(results_path, "wb") as results_file:
			results_writer = csv.writer(results_file)
			results_writer.writerow(["Sample ID Name", "Expected 1", "Expected 2", "Actual 1", "Actual 2", "PASS"])
			read_to_str = mmap.mmap(allele_file.fileno(), 0, access = mmap.ACCESS_READ)
			for row in val_reader:
				stringify = " ".join(row)
				if read_to_str.find(stringify) != -1:
					results_writer.writerow([row[0], row[1], row[2], row[1], row[2], "YES"])
				else:
					results_writer.writerow([row[0], row[1], row[2], "", "", "NO"])



print "Yeah we'll be counting stars"


os.remove(trays_path)
os.remove(wells_path)
os.remove(val_file_path)