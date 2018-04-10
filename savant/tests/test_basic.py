import os, json
import unittest, logging, glob
from StringIO import StringIO
from app import app
from app.results import create_flavors, compare
from app import query

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s')

class TestDoveps(unittest.TestCase):

    def test_1_create_flavor(self):
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

    def test_2_nullcases(self):        
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)

        resopnse = tester.get('/doveps/api/flavors/')
        data = json.loads(resopnse.data)

        print "Data: ", data

        self.assertEqual(data['Debs'][0][0], 362)
        self.assertEqual(data['Groups'][0][0], 51)
        self.assertEqual(data['Shadow'][0][0], 25)
        self.assertEqual(data['Users'][0][0], 25)

    def test_3_compare(self):
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

    def test_4_nullcases(self):        
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)

        resopnse = tester.get('/doveps/api/flavors/')
        data = json.loads(resopnse.data)

        print "Data: ", data

        self.assertNotEqual(data['Debs'][0], data['Total Debs'][0])
        self.assertNotEqual(data['Groups'][0], data['Total Groups'][0])
        self.assertNotEqual(data['Shadow'][0], data['Total Shadow'][0])
        self.assertNotEqual(data['Users'][0], data['Total Users'][0])
        self.assertEqual(data['Duplicates'], [])

    def test_5_recordknowledge(self):
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)

        list_of_files = glob.glob(path + '/mono/savant/app/Comparison-*')
        print 'List of files: ', list_of_files
        latest_file = max(list_of_files, key=os.path.getctime)
        latest_file = latest_file.split("app/", 1)[1]

        response = tester.get('/doveps/api/action/create/' + latest_file + '/debs/debs/save')
        data = json.loads(response.data)

        self.assertEqual(data['Message'], 'Linked')

if __name__ == '__main__':

    unittest.main()
