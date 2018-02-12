import os
import unittest
from StringIO import StringIO
from app import app
from app.results import create_flavors, compare
from app import query
import psycopg2
 
class TestDoveps(unittest.TestCase):

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

    def test_nullcases(self):
        engine_name = "postgresql://postgres:postgres@127.0.0.1:5432/travis_ci_test"
        conn = psycopg2.connect(engine_name)
        cur = conn.cursor()

        cur.execute("select store_debs(%s, %s ,%s, %s)", ('stat', None, 'test', 'test'))
        conn.commit()
        cur.execute("select store_debs(%s, %s ,%s, %s)", ('stat', None, 'test', 'test'))
        conn.commit()
        cur.execute("select count(*) from debs where stat=%s and name is null and version=%s and architecture=%s", ('stat', 'test', 'test'))
        count = cur.fetchone()
        self.assertEqual(count[0], 1)


if __name__ == '__main__':
    unittest.main()
