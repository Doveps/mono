import unittest
from app import app
from app.results import create_flavors, compare
 
class TestDoveps(unittest.TestCase):
 
    def test_create_flavor(self):
        tester = app.test_client(self)
        response = tester.post('/doveps/api/flavor/create/', content_type = 'json')
        self.assertEqual(response.status_code, 200)

    def test_compare(self):
        tester = app.test_client(self)
        response = tester.post('/doveps/api/flavor/compare/', content_type = 'json')
        self.assertEqual(response.status_code, 200)
 
if __name__ == '__main__':
    unittest.main()