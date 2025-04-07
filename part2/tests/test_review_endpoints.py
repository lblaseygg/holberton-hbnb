"""Tests for review endpoints."""
from tests.test_base import TestBase

class TestReviewEndpoints(TestBase):
    """Test cases for review endpoints."""

    def setUp(self):
        """Set up test client and create test user and place."""
        super().setUp()
        # Create user
        user_response = self.client.post('/api/v1/users/', json=self.test_user_data)
        self.user_id = user_response.get_json()['id']
        
        # Create place
        place_data = self.test_place_data.copy()
        place_data['owner_id'] = self.user_id
        place_response = self.client.post('/api/v1/places/', json=place_data)
        self.place_id = place_response.get_json()['id']
        
        # Update review data
        self.test_review_data['user_id'] = self.user_id
        self.test_review_data['place_id'] = self.place_id

    def test_create_review_success(self):
        """Test successful review creation."""
        response = self.client.post('/api/v1/reviews/', json=self.test_review_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['text'], self.test_review_data['text'])

    def test_create_review_invalid_rating(self):
        """Test review creation with invalid rating."""
        invalid_data = self.test_review_data.copy()
        invalid_data['rating'] = 6
        response = self.client.post('/api/v1/reviews/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_delete_review_success(self):
        """Test successful review deletion."""
        # First create a review
        create_response = self.client.post('/api/v1/reviews/', json=self.test_review_data)
        review_id = create_response.get_json()['id']

        # Then delete it
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200) 