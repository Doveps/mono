import os
import unittest
from StringIO import StringIO
from app import app
from app.results import create_flavors, compare
from app import query
import psycopg2, json, sqlalchemy
 
class TestDoveps(unittest.TestCase):
    def setUp(self):
#	os.system("sh db.sh")
	url = os.getenv("DB_TEST_URL")
	print "url: ", url
	
	if not url:
		self.skipTest("No DB")
#	self.engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/doveps')
	self.engine = sqlalchemy.create_engine(url)
	self.connection = self.engine.connect()
	
	sql_file = open('./db/scripts/01_tables.sql', 'r')
	queries = sql_file.read()
	sql_file.close()

	self.connection.execute(queries)
	
    def test_acreate_flavor(self):
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)
        response = tester.post('/doveps/api/flavor/create/',
        data = {
            'file': (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.50/find_debs_stdout.log')),
            'file': (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.50/find_groups_stdout.log')),
            'file': (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.50/find_shadow_stdout.log')),
            'file': (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.50/find_users_stdout.log'))
        })
        self.assertEqual(response.status_code, 200)

    def test_compare(self):
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)

        response = tester.post('/doveps/api/flavor/compare/',
        data = {
            'file': (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.51/find_debs_stdout.log')),
            'file': (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.51/find_groups_stdout.log')),
            'file': (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.51/find_shadow_stdout.log')),
            'file': (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.51/find_users_stdout.log'))
        })
        self.assertEqual(response.status_code, 200)

    #def test_nullcases(self):
   #     path = str(os.getcwd()).split("/mono", 1)[0]
  #      tester = app.test_client(self)
 #       response = tester.get('/doveps/api/test-cases/null-values/')
#
if __name__ == '__main__':
    unittest.main()
