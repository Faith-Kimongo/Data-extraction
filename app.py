
import mysql.connector
import zipfile,  wget, csv
import sqlalchemy as db
import os

#DATASET = (os.environ["DATASET"])
#IMPORTFIELDS = (os.environ["DATASET"])

DATASET = input('Input the file you want to download: ')

url='https://data.cms.gov/provider-data/sites/default/files/archive/Doctors and clinicians/2022/'+DATASET

print('\nstarting to download...')
wget.download(url) # downloads the file



filename = url.split('/')[-1]  # Split URL to get the file name


#  extracting the zip file contents

with zipfile.ZipFile(filename, 'r') as my_file:
    csvfile_from_zip = my_file.namelist()[0] # geting the csv file from the zip and extracting it
    my_file.extract(csvfile_from_zip)
print('\nprocessing... ')


#connecting to database

mydb = mysql.connector.connect(
    host="db",
    user="root",
    password="etl@123"
        )
 
mycursor = mydb.cursor() 

#drops database if exists
mycursor.execute("DROP database IF EXISTS etl_database")

#create database 
sql_createdatabase = "CREATE database etl_database"
mycursor.execute( sql_createdatabase)

#select database to use
sql_selectdatabase = "USE etl_database"
mycursor.execute( sql_selectdatabase)


#create table

sql_createtable = '''CREATE TABLE etl(
   NPI VARCHAR(600),
   IndPACID VARCHAR(600),
   IndenrlID VARCHAR(600)
)'''
mycursor.execute( sql_createtable)


with open(csvfile_from_zip, encoding='unicode_escape') as csv_file:
    csvfile = csv.reader(csv_file, delimiter = ',')
    all_value = []
    for row in csvfile:
        value = (row[0], row[1], row[2])
        all_value.append(value)

#print(len(all_value))
Number_of_rows = len(all_value)
all_value_2 = all_value[1:2000]



sql = "INSERT INTO etl (NPI, IndPACID, IndenrlID ) VALUES (%s, %s, %s)"

mycursor = mydb.cursor()

print('importing.... ')

mycursor.executemany(sql, all_value_2)

mydb.commit()

row_count = str(mycursor.rowcount)

print('done. ' + row_count + " record imported.")

    


