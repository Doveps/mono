import psycopg2
import sys
import os 
from app.base_path import get_path

def execute_sql(sql_file):
	connection = psycopg2.connect("dbname='travis_ci_test' user='postgres' host='localhost' password='postgres'")
	cursor = connection.cursor()

	path = get_path()
	if not path.__contains__("/mono/savant/db_script"):
		db_directory = path + "/mono/savant/db_scripts"
	else:
		db_directory = path

	os.chdir(db_directory)
	cursor.execute(open(str(sql_file), "r").read())
	connection.commit()
