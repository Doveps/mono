import psycopg2
import sys
import os 

def execute_sql(sql_file):
	connection = psycopg2.connect("dbname='Doveps' user='postgres' host='localhost' password='postgres'")
	cursor = connection.cursor()

	os.chdir("/home/josiah/Documents/Doveps/mono/savant/db_scripts")
	print "directory: ", os.getcwd()
	cursor.execute(open(str(sql_file), "r").read())
	connection.commit()
