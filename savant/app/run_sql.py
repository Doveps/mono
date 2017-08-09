import psycopg2
import sys
import os 

def execute_sql(sql_file):
	connection = psycopg2.connect("dbname='Doveps' user='postgres' host='localhost' password='postgres'")
	cursor = connection.cursor()
	print "connected?"

	cursor.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
	for table in cursor.fetchall():
		print "prev: ", table

	os.chdir("/home/josiah/Documents/Doveps/mono/savant/db_scripts")
	print "directory: ", os.getcwd()
	cursor.execute(open(str(sql_file), "r").read())
	cursor.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
	for table in cursor.fetchall():
		print "now: ", table
	connection.commit()
