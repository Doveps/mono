import os
import unittest
import testing.postgresql
from StringIO import StringIO
from app import app
from app.results import create_flavors, compare
from app import query
import psycopg2, json, sqlalchemy, mock
 
class TestDoveps(unittest.TestCase):

    # def setUp(self):
    #     self.path = str(os.getcwd()).split("/mono", 1)[0]
    #     self.db = testing.postgresql.Postgresql()
    #     self.db_conf = self.db.dsn()
    #     self.db_con = psycopg2.connect(**self.db_conf)
    #     self.db_con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    #     with self.db_con.cursor() as cur:
    #         cur.execute(open("tests/full.sql", "r").read())
    #         # cur.execute(slurp('db/scripts/full.sql'))
    @mock.patch('psycopg2.connect')
    def test_acreate_flavor(self, mock_connect):
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

    @mock.patch('psycopg2.connect')
    def test_compare(self, mock_connect):
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
