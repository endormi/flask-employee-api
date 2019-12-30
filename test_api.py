import unittest
import api
import json
import sys


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = api.app.test_client()

    # This only works without x-access-token
    def test_employees(self):
        response = self.app.get('http://127.0.0.1:5000/employee/1ab439cc-ec09-11e9-8090-4cedfb3cafc4')
        self.assertEqual(
            json.loads(response.get_data().decode(sys.getdefaultencoding())),
            {"Employee": {"admin": True, "job_title": "test", "name": "test"}}
        )


if __name__ == "__main__":
    unittest.main()
