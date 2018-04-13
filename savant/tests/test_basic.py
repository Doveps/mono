import os, json, psycopg2   
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

    def test_2_flavor(self):        
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)

        debs = tester.get('/doveps/api/count/debs/')
        debs_data = json.loads(debs.data)

        groups = tester.get('/doveps/api/count/groups/')
        groups_data = json.loads(groups.data)

        shadow = tester.get('/doveps/api/count/shadow/')
        shadow_data = json.loads(shadow.data)

        users = tester.get('/doveps/api/count/users/')
        users_data = json.loads(users.data)

        self.assertEqual(debs_data['Debs Count'][0][0], 362)
        self.assertEqual(groups_data['Groups Count'][0][0], 51)
        self.assertEqual(shadow_data['Shadow Count'][0][0], 25)
        self.assertEqual(users_data['Users Count'][0][0], 25)

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
        que_test = query.Query()        
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)

        flavor_resopnse = tester.get('/doveps/api/flavors/')
        data = json.loads(flavor_resopnse.data)

        debs = tester.get('/doveps/api/count/debs/')
        debs_data = json.loads(debs.data)

        groups = tester.get('/doveps/api/count/groups/')
        groups_data = json.loads(groups.data)

        shadow = tester.get('/doveps/api/count/shadow/')
        shadow_data = json.loads(shadow.data)

        users = tester.get('/doveps/api/count/users/')
        users_data = json.loads(users.data)

        max_debs = que_test.max_saved_debs()
        max_groups = que_test.max_saved_groups()
        max_shadow = que_test.max_saved_shadow()
        max_users = que_test.max_saved_users()

        self.assertNotEqual(debs_data['Debs Count'][0], max_debs)
        self.assertNotEqual(groups_data['Groups Count'][0], max_groups)
        self.assertNotEqual(shadow_data['Shadow Count'][0], max_shadow)
        self.assertNotEqual(users_data['Users Count'][0], max_users)
        self.assertEqual(data['Duplicates'], [])

    def test_5_recordknowledge(self):
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)

        list_of_files = glob.glob(path + '/mono/savant/app/Comparison-*')
        latest_file = max(list_of_files, key=os.path.getctime)
        latest_file = latest_file.split("app/", 1)[1]

        response = tester.get('/doveps/api/action/create/' + latest_file + '/debs/debs/save')
        data = json.loads(response.data)

        self.assertEqual(data['Message'], 'Linked')

if __name__ == '__main__':

    unittest.main()
