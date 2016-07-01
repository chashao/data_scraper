import csv
from import_script import package_installer

package_installer('pyodbc')
connection = pyodbc.connect('server to connect later')
cursor = connection.cursor()
cursor.execute("SQL query to extract the necessary tables from the database")


with open("datatable.csv", "w+") as datatable:
	writer = csv.writer(datatable)
	for row in cursor.fetchall():
		writer.writerow(row)