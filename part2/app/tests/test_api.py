import unittest
from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_api, facade
from app.services.facade import HBnBFacade

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(users_api)
        self.client = self.app.test_client()
        self.facade = facade  # Use the same facade instance as the API

    def test_get_all_users(self):
        # Create a test user
        test_user = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }
        self.facade.create_user(test_user)

        # Test GET /users/
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['first_name'], 'John')
        self.assertEqual(data[0]['last_name'], 'Doe')
        self.assertEqual(data[0]['email'], 'john.doe@example.com')

    def test_update_user(self):
        # Create a test user
        test_user = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }
        user = self.facade.create_user(test_user)
        user_id = user.id

        # Test PUT /users/<user_id>
        update_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com'
        }
        response = self.client.put(f'/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'Jane')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'jane.doe@example.com')

        # Test updating non-existent user
        response = self.client.put('/users/nonexistent', json=update_data)
        self.assertEqual(response.status_code, 404)

        # Test invalid update data
        invalid_data = {
            'first_name': '',  # Empty first name
            'last_name': 'Doe',
            'email': 'invalid-email'
        }
        response = self.client.put(f'/users/{user_id}', json=invalid_data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main() 