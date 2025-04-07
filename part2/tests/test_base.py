"""Base test class."""
import unittest
from app import create_app
from app.services import facade

class TestBase(unittest.TestCase):
    """Base test class with setup and teardown."""

    def setUp(self):
        """Set up test client and other test variables."""
        self.app = create_app()
        self.client = self.app.test_client()
        
        # Create test data
        self.test_user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com"
        }
        
        self.test_place_data = {
            "title": "Test Place",
            "description": "A test place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194
        }
        
        self.test_review_data = {
            "text": "Great place!",
            "rating": 5
        }
        
        self.test_amenity_data = {
            "name": "Test Amenity"
        }

    def tearDown(self):
        """Clean up after each test."""
        # Clear the in-memory repositories
        facade.user_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()
        facade.amenity_repo._storage.clear() 