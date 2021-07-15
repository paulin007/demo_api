import unittest
import json
import sys
import os
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir, '../src'))
from app import app


class SignupTest(unittest.TestCase): #extends unittest.TestCase

    def setUp(self):
        self.app = app.test_client()
        #self.db = db.get_db()

    def test_greeting(self):
        response = self.app.get('/greeting')
        self.assertEqual(200, response.status_code)

    def test_successful_signup(self):
        # Given
        payload={'email': 'paulin@test.com', 'password': 'P@ssw0rd'}

        # When
        response = self.app.post('/login', headers={}, data=payload)
        print(response.json['message'])
        # Then
        self.assertEqual(str, type(response.json['access_token']))
        self.assertEqual(200, response.status_code)

