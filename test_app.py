import unittest
from flask import Flask
from EmpApp import app

class TestEmpApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AddEmp.html', response.data)

    def test_about(self):
        response = self.app.post('/about')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

if __name__ == '__main__':
    unittest.main()
