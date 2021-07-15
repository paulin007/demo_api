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

    def test_greeting(self):
        response = self.app.get('/greeting')
        self.assertEqual(200, response.status_code)

    def test_successful_signup(self):
        # Given
        payload={'email': 'pp1@gmail.com', 
                'first_name': 'pp', 
                'last_name': 'aa', 
                'password': 'password'}

        # When
        response = self.app.post('/register', headers={}, data=payload)
        print(response.json['message'])
        # Then
        self.assertEqual(str, type(response.json['message']))
        self.assertEqual(201, response.status_code)

