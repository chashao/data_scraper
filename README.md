# data_scraper
This is a tool used to extract data from an SQL database into a .csv file, to be parsed and analyzed.

Things required for the tool to work:

1. Internet connection if the server is not local
2. Python 2.7
  a. if using Python 2.7.8 or earlier, follow these instructions: http://www.pip-installer.org/en/latest/installing.html
  b. if using Python 2.7.9+, pip is already installed.
3. SQL Server 2012 or later
  
Instructions for use:

1. Make sure the validation file named "06-19-14 NGS Validation Panel Allele Database.xlsx" is somewhere on your computer.
2. Have a database name ready
3. On a terminal, cd to the directory containing the script and run "python extractor.py <database-name>"
