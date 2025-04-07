"""Tests for place endpoints."""
from tests.test_base import TestBase

class TestPlaceEndpoints(TestBase):
    """Test cases for place endpoints."""

    def setUp(self):
        """Set up test client and create a test user."""
        super().setUp()
        response = self.client.post('/api/v1/users/', json=self.test_user_data)
        self.owner_id = response.get_json()['id']
        self.test_place_data['owner_id'] = self.owner_id

    def test_create_place_success(self):
        """Test successful place creation."""
        response = self.client.post('/api/v1/places/', json=self.test_place_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], self.test_place_data['title'])

    def test_create_place_invalid_price(self):
        """Test place creation with invalid price."""
        invalid_data = self.test_place_data.copy()
        invalid_data['price'] = -100
        response = self.client.post('/api/v1/places/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_coordinates(self):
        """Test place creation with invalid coordinates."""
        invalid_data = self.test_place_data.copy()
        invalid_data['latitude'] = 100
        response = self.client.post('/api/v1/places/', json=invalid_data)
        self.assertEqual(response.status_code, 400) 