import unittest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.services.facade import HBnBFacade

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.facade = HBnBFacade()

        # Create test user
        self.test_user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com"
        )
        self.facade.user_repository.add(self.test_user)

        # Create test place
        self.test_place = Place(
            title="Test Place",
            description="A test place",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.test_user
        )
        self.facade.place_repository.add(self.test_place)

    def test_create_review_valid(self):
        """Test creating a review with valid data"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.test_user.id,
            "place_id": self.test_place.id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['text'], "Great place!")
        self.assertEqual(data['rating'], 5)
        self.assertEqual(data['user']['id'], self.test_user.id)
        self.assertEqual(data['place']['id'], self.test_place.id)

    def test_create_review_empty_text(self):
        """Test creating a review with empty text"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": self.test_user.id,
            "place_id": self.test_place.id
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_review_invalid_rating(self):
        """Test creating a review with invalid rating"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 6,  # Invalid rating (should be 1-5)
            "user_id": self.test_user.id,
            "place_id": self.test_place.id
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_review_invalid_user(self):
        """Test creating a review with invalid user"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": "nonexistent-id",
            "place_id": self.test_place.id
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_review_invalid_place(self):
        """Test creating a review with invalid place"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.test_user.id,
            "place_id": "nonexistent-id"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_review(self):
        """Test getting a review by ID"""
        # First create a review
        review = Review(
            text="Test review",
            rating=4,
            user=self.test_user,
            place=self.test_place
        )
        self.facade.review_repository.add(review)

        response = self.client.get(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['text'], "Test review")
        self.assertEqual(data['rating'], 4)
        self.assertEqual(data['user']['id'], self.test_user.id)
        self.assertEqual(data['place']['id'], self.test_place.id)

    def test_get_nonexistent_review(self):
        """Test getting a non-existent review"""
        response = self.client.get('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_reviews_by_place(self):
        """Test getting all reviews for a place"""
        # Create multiple reviews for the place
        review1 = Review(
            text="Review 1",
            rating=4,
            user=self.test_user,
            place=self.test_place
        )
        review2 = Review(
            text="Review 2",
            rating=5,
            user=self.test_user,
            place=self.test_place
        )
        self.facade.review_repository.add(review1)
        self.facade.review_repository.add(review2)

        response = self.client.get(f'/api/v1/places/{self.test_place.id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)

    def test_update_review(self):
        """Test updating a review"""
        # First create a review
        review = Review(
            text="Test review",
            rating=4,
            user=self.test_user,
            place=self.test_place
        )
        self.facade.review_repository.add(review)

        response = self.client.put(f'/api/v1/reviews/{review.id}', json={
            "text": "Updated review",
            "rating": 5
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['text'], "Updated review")
        self.assertEqual(data['rating'], 5)

    def test_update_review_invalid_rating(self):
        """Test updating a review with invalid rating"""
        review = Review(
            text="Test review",
            rating=4,
            user=self.test_user,
            place=self.test_place
        )
        self.facade.review_repository.add(review)

        response = self.client.put(f'/api/v1/reviews/{review.id}', json={
            "text": "Updated review",
            "rating": 6  # Invalid rating
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_delete_review(self):
        """Test deleting a review"""
        review = Review(
            text="Test review",
            rating=4,
            user=self.test_user,
            place=self.test_place
        )
        self.facade.review_repository.add(review)

        response = self.client.delete(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], "Review deleted successfully")

        # Verify the review is deleted
        response = self.client.get(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()