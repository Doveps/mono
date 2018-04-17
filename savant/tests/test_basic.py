import os, json, psycopg2   
import unittest, logging, glob
from StringIO import StringIO
from app import app
from app.results import create_flavors, compare
from app import query

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s')

with open('db_config.json', 'r') as db_file:
        db_info = json.load(db_file)

db_name = db_info["database"]["database_name"]
username = db_info["database"]["username"]
password = db_info["database"]["password"]
host = db_info["database"]["host"]
engine_name = "postgresql://" + username + ":" + password + "@" + host + ":5432/" + db_name
conn = psycopg2.connect(engine_name)
cur = conn.cursor()


def max_saved_debs():
    cur.execute("select max(id) \
                        from ScanDebs")

    max_debs = cur.fetchall()

    return max_debs

def max_saved_groups():
    cur.execute("select max(id) \
                    from ScanGroups")

    max_groups = cur.fetchall()

    return max_groups

def max_saved_shadow():    
    cur.execute("select max(id) \
                    from ScanShadow")

    max_shadow = cur.fetchall()

    return max_shadow

def max_saved_users():
    cur.execute("select max(id) \
                    from ScanUsers")

    max_users = cur.fetchall()

    return max_users

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

        res_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res_data["Status"], "OK")
        self.assertEqual(res_data["Message"], "Saved")

    def test_2_flavor(self):        
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)

        debs = tester.get('/doveps/api/count/flavor/debs')
        debs_data = json.loads(debs.data)

        groups = tester.get('/doveps/api/count/flavor/groups')
        groups_data = json.loads(groups.data)

        shadow = tester.get('/doveps/api/count/flavor/shadow')
        shadow_data = json.loads(shadow.data)

        users = tester.get('/doveps/api/count/flavor/users')
        users_data = json.loads(users.data)

        self.assertEqual(debs_data['debs count'][0][0], 362)
        self.assertEqual(groups_data['groups count'][0][0], 51)
        self.assertEqual(shadow_data['shadow count'][0][0], 25)
        self.assertEqual(users_data['users count'][0][0], 25)

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

        list_of_files = glob.glob(path + '/mono/savant/app/Comparison-*')
        latest_file = max(list_of_files, key=os.path.getctime)
        latest_file = latest_file.split("app/", 1)[1]

        data_res = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data_res["File"], latest_file)

    def test_4_nullcases(self):        
        path = str(os.getcwd()).split("/mono", 1)[0]
        tester = app.test_client(self)

        flavor_resopnse = tester.get('/doveps/api/flavors-duplicates/')
        data = json.loads(flavor_resopnse.data)

        debs = tester.get('/doveps/api/count/flavor/debs')
        debs_data = json.loads(debs.data)

        groups = tester.get('/doveps/api/count/flavor/groups')
        groups_data = json.loads(groups.data)

        shadow = tester.get('/doveps/api/count/flavor/shadow')
        shadow_data = json.loads(shadow.data)

        users = tester.get('/doveps/api/count/flavor/users')
        users_data = json.loads(users.data)

        max_debs = max_saved_debs()
        max_groups = max_saved_groups()
        max_shadow = max_saved_shadow()
        max_users = max_saved_users()

        self.assertNotEqual(debs_data['debs count'][0], max_debs)
        self.assertNotEqual(groups_data['groups count'][0], max_groups)
        self.assertNotEqual(shadow_data['shadow count'][0], max_shadow)
        self.assertNotEqual(users_data['users count'][0], max_users)
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
