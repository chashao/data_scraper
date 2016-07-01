# Connects to the database specified and pulls the datatable requested, writing it to a csv file
# MS SQL Server 2012 and 2014 uses Native Client 11.0. Change the other elements of the string to 
# connect to the desired server.

import csv
from import_script import package_installer

package_installer('pyodbc')
pyodbc.connect(r'DRIVER={SQL Server Native Client 11.0};SERVER = test;DATABASE = test;UID = user;PWD = password')
cursor = connection.cursor()

cursor.execute("SQL query to extract the necessary tables from the database")


with open("datatable.csv", "w+") as datatable:
	writer = csv.writer(datatable)
	for row in cursor.fetchall():
		writer.writerow(row)