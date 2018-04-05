import os, json
import unittest, logging
import testing.postgresql
from StringIO import StringIO
from app import app
from app.results import create_flavors, compare
from app import query
import psycopg2, json, sqlalchemy, mock
from pathlib2 import Path
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s')

class TestDoveps(unittest.TestCase):

    def test_acreate_flavor(self):
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)

        response = tester.post('/doveps/api/flavor/create/',
        data = {
            'files[]': [(StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.50/find_debs_stdout.log')),
                        (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.50/find_groups_stdout.log')),
                        (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.50/find_shadow_stdout.log')),
                        (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.50/find_users_stdout.log'))]
        })
        self.assertEqual(response.status_code, 200)

    def test_compare(self):
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)

        response = tester.post('/doveps/api/flavor/compare/',
        data = {
            'files[]': [(StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.51/find_debs_stdout.log')),
                        (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.51/find_groups_stdout.log')),
                        (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.51/find_shadow_stdout.log')),
                        (StringIO('My inputs'),(path + '/mono/savant/tests/Scanner_Files/33.33.33.51/find_users_stdout.log'))]
        })
        self.assertEqual(response.status_code, 200)

    def test_nullcases(self):        
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)

        resopnse = tester.get('/doveps/api/count/')
        data = json.loads(resopnse.data)

        self.assertEqual(data['Count'], [])

if __name__ == '__main__':
    unittest.main()
