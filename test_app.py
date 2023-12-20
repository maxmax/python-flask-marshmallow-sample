import unittest
from unittest.mock import patch
from flask import json
from app import app  # Assuming your Flask app is defined in a file named 'app.py'

class UserApiTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('app.users', [
        {"id": 1, "name": "John Doe", "email": "johndoe@example.com"},
        {"id": 2, "name": "Jane Doe", "email": "janedoe@example.com"}
    ])
    def test_get_users(self):
        response = self.app.get('/users/')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

    @patch('app.users', [
        {"id": 1, "name": "John Doe", "email": "johndoe@example.com"},
        {"id": 2, "name": "Jane Doe", "email": "janedoe@example.com"}
    ])
    def test_get_user(self):
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], 'John Doe')
        self.assertEqual(data['email'], 'johndoe@example.com')

    @patch('app.users', [])
    def test_get_users_empty(self):
        response = self.app.get('/users/')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 0)

    @patch('app.users', [
        {"id": 1, "name": "John Doe", "email": "johndoe@example.com"}
    ])
    def test_update_user(self):
        user_data = {"name": "Tom Doe", "email": "tomdoe@example.com"}
        response = self.app.put('/users/1', json=user_data)
        self.assertEqual(response.status_code, 200)

    @patch('app.users', [])
    def test_delete_user_empty(self):
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 404)

    @patch('app.users', [
        {"id": 1, "name": "John Doe", "email": "johndoe@example.com"}
    ])
    def test_delete_user(self):
        response = self.app.delete('/users/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
