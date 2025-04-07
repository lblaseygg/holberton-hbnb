"""Tests for user endpoints."""
from tests.test_base import TestBase

class TestUserEndpoints(TestBase):
    """Test cases for user endpoints."""

    def test_create_user_success(self):
        """Test successful user creation."""
        response = self.client.post('/api/v1/users/', json=self.test_user_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], self.test_user_data['first_name'])
        self.assertEqual(data['last_name'], self.test_user_data['last_name'])
        self.assertEqual(data['email'], self.test_user_data['email'])

    def test_create_user_invalid_email(self):
        """Test user creation with invalid email."""
        invalid_data = self.test_user_data.copy()
        invalid_data['email'] = 'invalid-email'
        response = self.client.post('/api/v1/users/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_name(self):
        """Test user creation with empty name."""
        invalid_data = self.test_user_data.copy()
        invalid_data['first_name'] = ''
        response = self.client.post('/api/v1/users/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_get_user_success(self):
        """Test successful user retrieval."""
        # First create a user
        create_response = self.client.post('/api/v1/users/', json=self.test_user_data)
        user_id = create_response.get_json()['id']

        # Then retrieve the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], self.test_user_data['first_name'])

    def test_get_user_not_found(self):
        """Test user retrieval with invalid ID."""
        response = self.client.get('/api/v1/users/invalid-id')
        self.assertEqual(response.status_code, 404)

    def test_update_user_success(self):
        """Test successful user update."""
        # First create a user
        create_response = self.client.post('/api/v1/users/', json=self.test_user_data)
        user_id = create_response.get_json()['id']

        # Then update the user
        update_data = {"first_name": "Updated"}
        response = self.client.put(f'/api/v1/users/{user_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], "Updated") 