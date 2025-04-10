import unittest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.services.facade import HBnBFacade
import pytest

class TestPlaceEndpoints(unittest.TestCase):
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

        # Create test amenities
        self.amenity1 = Amenity(name="WiFi")
        self.amenity2 = Amenity(name="Pool")
        self.facade.amenity_repository.add(self.amenity1)
        self.facade.amenity_repository.add(self.amenity2)

    def test_create_place_valid(self):
        """Test creating a place with valid data"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.test_user.id,
            "amenities": [self.amenity1.id, self.amenity2.id]
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], "Test Place")
        self.assertEqual(data['price'], 100.0)
        self.assertEqual(data['latitude'], 40.7128)
        self.assertEqual(data['longitude'], -74.0060)
        self.assertEqual(len(data['amenities']), 2)

    def test_create_place_empty_title(self):
        """Test creating a place with empty title"""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "A test place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.test_user.id
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_place_invalid_price(self):
        """Test creating a place with negative price"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place",
            "price": -100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.test_user.id
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_place_invalid_latitude(self):
        """Test creating a place with invalid latitude"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place",
            "price": 100.0,
            "latitude": 91.0,
            "longitude": -74.0060,
            "owner_id": self.test_user.id
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_place_invalid_longitude(self):
        """Test creating a place with invalid longitude"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": 181.0,
            "owner_id": self.test_user.id
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_place(self):
        """Test getting a place by ID"""
        # First create a place
        place = Place(
            title="Test Place",
            description="A test place",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.test_user
        )
        self.facade.place_repository.add(place)

        response = self.client.get(f'/api/v1/places/{place.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], "Test Place")
        self.assertEqual(data['price'], 100.0)

    def test_get_nonexistent_place(self):
        """Test getting a non-existent place"""
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_all_places(self):
        """Test getting all places"""
        # Create multiple places
        place1 = Place(
            title="Place 1",
            description="First place",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.test_user
        )
        place2 = Place(
            title="Place 2",
            description="Second place",
            price=200.0,
            latitude=41.7128,
            longitude=-75.0060,
            owner=self.test_user
        )
        self.facade.place_repository.add(place1)
        self.facade.place_repository.add(place2)

        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)

    def test_update_place(self):
        """Test updating a place"""
        # First create a place
        place = Place(
            title="Test Place",
            description="A test place",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.test_user
        )
        self.facade.place_repository.add(place)

        response = self.client.put(f'/api/v1/places/{place.id}', json={
            "title": "Updated Place",
            "price": 150.0,
            "amenities": [self.amenity1.id]
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], "Updated Place")
        self.assertEqual(data['price'], 150.0)
        self.assertEqual(len(data['amenities']), 1)

    def test_update_place_invalid_data(self):
        """Test updating a place with invalid data"""
        place = Place(
            title="Test Place",
            description="A test place",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.test_user
        )
        self.facade.place_repository.add(place)

        response = self.client.put(f'/api/v1/places/{place.id}', json={
            "title": "Updated Place",
            "price": -150.0,
            "latitude": 91.0
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

class TestPlaceEndpoints:
    def test_create_place(self, client, test_user):
        """Test creating a valid place"""
        response = client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": test_user.id,
            "amenities": []
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == "Test Place"
        assert data['price'] == 100.0
        assert data['owner']['id'] == test_user.id

    def test_create_place_empty_title(self, client, test_user):
        """Test creating a place with empty title"""
        response = client.post('/api/v1/places/', json={
            "title": "",
            "description": "A test place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": test_user.id
        })
        assert response.status_code == 400
        assert response.get_json()['error'] == "Invalid input data or owner not found"

    def test_create_place_negative_price(self, client, test_user):
        """Test creating a place with negative price"""
        response = client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place",
            "price": -100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": test_user.id
        })
        assert response.status_code == 400
        assert response.get_json()['error'] == "Invalid input data or owner not found"

    def test_create_place_invalid_latitude(self, client, test_user):
        """Test creating a place with invalid latitude"""
        response = client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place",
            "price": 100.0,
            "latitude": 91.0,  # Invalid latitude
            "longitude": -74.0060,
            "owner_id": test_user.id
        })
        assert response.status_code == 400
        assert response.get_json()['error'] == "Invalid input data or owner not found"

    def test_create_place_invalid_longitude(self, client, test_user):
        """Test creating a place with invalid longitude"""
        response = client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": 181.0,  # Invalid longitude
            "owner_id": test_user.id
        })
        assert response.status_code == 400
        assert response.get_json()['error'] == "Invalid input data or owner not found"

    def test_get_place(self, client, test_place):
        """Test getting a place by ID"""
        response = client.get(f'/api/v1/places/{test_place.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == test_place.title
        assert data['price'] == test_place.price
        assert data['owner']['id'] == test_place.owner.id

    def test_get_nonexistent_place(self, client):
        """Test getting a nonexistent place"""
        response = client.get('/api/v1/places/nonexistent-id')
        assert response.status_code == 404
        assert response.get_json()['error'] == "Place not found"

    def test_get_all_places(self, client, test_place):
        """Test getting all places"""
        response = client.get('/api/v1/places/')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_update_place(self, client, test_place):
        """Test updating a place"""
        response = client.put(f'/api/v1/places/{test_place.id}', json={
            "title": "Updated Place",
            "price": 150.0
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == "Updated Place"
        assert data['price'] == 150.0

    def test_update_place_invalid_data(self, client, test_place):
        """Test updating a place with invalid data"""
        response = client.put(f'/api/v1/places/{test_place.id}', json={
            "title": "",
            "price": -150.0
        })
        assert response.status_code == 400
        assert response.get_json()['error'] == "Invalid input data"

if __name__ == '__main__':
    unittest.main() 