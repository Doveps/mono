import psycopg2
import sys
import os 

def execute_sql(sql_file):
	try:
		connection = psycopg2.connect("dbname='Doveps' user='postgres' host='localhost' password='postgres'")
	except:
		print "unable to connect"
	cursor = connection.cursor()

	os.chdir("./savant/db_scripts")
	cursor.execute(open(str(sql_file), "r").read())
	connection.commit()
