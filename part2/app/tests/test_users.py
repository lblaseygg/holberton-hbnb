import unittest
from app import create_app
from app.models.user import User
from app.services.facade import HBnBFacade

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.facade = HBnBFacade()

    def test_create_user_valid(self):
        """Test creating a user with valid data"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['first_name'], "John")
        self.assertEqual(data['last_name'], "Doe")
        self.assertEqual(data['email'], "john.doe@example.com")
        self.assertIn('id', data)

    def test_create_user_empty_fields(self):
        """Test creating a user with empty fields"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": ""
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_user_invalid_email(self):
        """Test creating a user with invalid email format"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_user(self):
        """Test getting a user by ID"""
        # First create a user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com"
        )
        self.facade.user_repository.add(user)

        response = self.client.get(f'/api/v1/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], "Test")
        self.assertEqual(data['last_name'], "User")
        self.assertEqual(data['email'], "test@example.com")

    def test_get_nonexistent_user(self):
        """Test getting a non-existent user"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_all_users(self):
        """Test getting all users"""
        # Create multiple users
        user1 = User(
            first_name="User1",
            last_name="Test",
            email="user1@example.com"
        )
        user2 = User(
            first_name="User2",
            last_name="Test",
            email="user2@example.com"
        )
        self.facade.user_repository.add(user1)
        self.facade.user_repository.add(user2)

        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)

    def test_update_user(self):
        """Test updating a user"""
        # First create a user
        user = User(
            first_name="Original",
            last_name="User",
            email="original@example.com"
        )
        self.facade.user_repository.add(user)

        response = self.client.put(f'/api/v1/users/{user.id}', json={
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@example.com"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], "Updated")
        self.assertEqual(data['last_name'], "Name")
        self.assertEqual(data['email'], "updated@example.com")

    def test_update_user_invalid_data(self):
        """Test updating a user with invalid data"""
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com"
        )
        self.facade.user_repository.add(user)

        response = self.client.put(f'/api/v1/users/{user.id}', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main() 