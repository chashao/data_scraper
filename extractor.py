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

val_file_path = r"C:\Users\melvin.huang\Desktop\validation.csv"

with open(new_file_path, "rb") as validation_file:
	with open(val_file_path, "w+") as formatted_file:
		validation_file_read = csv.reader(validation_file)
		formatted_file_write = csv.writer(formatted_file)
		validation_file_read.next()
		for row in validation_file_read:
			formatted_file_write.writerow([
				row[0],
				row[2], 
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


#paths to each file
trays_path = r"C:\Users\melvin.huang\Desktop\trays.csv"
wells_path = r"C:\Users\melvin.huang\Desktop\wells.csv"
alleles_path = r"C:\Users\melvin.huang\Desktop\alleles.csv"


def analysis(wellid, sampleIDName):
	cursor.execute("SELECT * FROM [41_53116].[dbo].[WELL_RESULT] WHERE ResultType = '01' AND wellid = ?", wellid)
	with open(alleles_path, "w+") as alleles_file:
		writer = csv.writer(alleles_file)
		for row in cursor.fetchall():
			writer.writerow(row)
	with open(alleles, "rb") as alleles_file_read:
		with open(val_file_path, "rb") as formatted_file:
			#compare the files
			validation_reader = csv.reader(formatted_file)
			for line in validation_reader:
				read_to_str = read_to_str = mmap.mmap(alleles_file_read.fileno(), 0, access = mmap.ACCESS_READ)
				if line[0] != sampleIDName:
					continue
				#else:



#Returns a csv of all the tray IDs
with open(trays_path, "w+") as trayfile:
	cursor.execute("SELECT TrayID FROM [41_53116].[dbo].[tray] ORDER BY adddt DESC")
	writer = csv.writer(trayfile)
	for row in cursor.fetchall():
		writer.writerow(row)

#for each tray ID, output the wells and samples
with open(trays_path, "rb") as trayfile:
	with open(wells_path, "w+") as wellsfile:
		well_writer = csv.writer(wellsfile)
		tray_reader = csv.reader(trayfile)
		for entry in tray_reader:
			print entry
			cursor.execute("SELECT WellID, SampleIDName FROM [41_53116].[dbo].[well],[41_53116].[dbo].[sample] WHERE TrayID = ? AND [well].SampleID = [sample].SampleID", entry)
			for line in cursor.fetchall():
				well_writer.writerow(line)

		#with open(wells_path, "rb") as wells_file:
		#	for line in wells_file:
		#		analysis(line[0], line[1])
		#insert function to read the file and do analysis to it.


"""

#Writes the data to a csv. I'm assuming that only one column (pair of alleles) will be selected...
with open("C:\Users\melvin.huang\Desktop\datatable.csv", "w+") as datatable:
	writer = csv.writer(datatable)
	for row in cursor.fetchall():
		writer.writerow(row)




with open(r"C:\Users\melvin.huang\Desktop\validation.csv", "rb") as formatted_file:
	with open("C:\Users\melvin.huang\Desktop\datatable.csv", "rb") as datatable:
#file-splitting operation:
		formatted_reader = csv.reader(formatted_file)
		read_to_str = mmap.mmap(datatable.fileno(), 0, access = mmap.ACCESS_READ)
		for row in formatted_reader:
			index = 0
			num_matches = 0
			while index <= (len(row) - 2):
				chunk = [row[index], row[index + 1]]
				chunk_string = " ".join(chunk)
				if read_to_str.find(chunk_string) != -1:
					print(chunk_string)
					index += 2
				else:
					index += 2
					print "Can't find this"

"""