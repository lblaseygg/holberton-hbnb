import unittest
from flask import Flask
from flask_restx import Api
from app.api.v1.amenities import api as amenities_api, facade
from app.services.facade import HBnBFacade

class TestAmenitiesAPI(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(amenities_api)
        self.client = self.app.test_client()
        self.facade = facade  # Use the same facade instance as the API

    def test_create_amenity(self):
        # Test creating a valid amenity
        amenity_data = {
            'name': 'Wi-Fi'
        }
        response = self.client.post('/amenities/', json=amenity_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], 'Wi-Fi')
        self.assertIsNotNone(data['id'])

        # Test creating an invalid amenity
        invalid_data = {
            'name': ''  # Empty name
        }
        response = self.client.post('/amenities/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        # Create test amenities
        self.facade.create_amenity({'name': 'Wi-Fi'})
        self.facade.create_amenity({'name': 'Air Conditioning'})

        # Test GET /amenities/
        response = self.client.get('/amenities/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) >= 2)
        names = [amenity['name'] for amenity in data]
        self.assertIn('Wi-Fi', names)
        self.assertIn('Air Conditioning', names)

    def test_get_amenity(self):
        # Create a test amenity
        amenity = self.facade.create_amenity({'name': 'Wi-Fi'})
        amenity_id = amenity.id

        # Test GET /amenities/<amenity_id>
        response = self.client.get(f'/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'Wi-Fi')
        self.assertEqual(data['id'], amenity_id)

        # Test getting non-existent amenity
        response = self.client.get('/amenities/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity(self):
        # Create a test amenity
        amenity = self.facade.create_amenity({'name': 'Wi-Fi'})
        amenity_id = amenity.id

        # Test PUT /amenities/<amenity_id>
        update_data = {
            'name': 'High-Speed Wi-Fi'
        }
        response = self.client.put(f'/amenities/{amenity_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'High-Speed Wi-Fi')
        self.assertEqual(data['id'], amenity_id)

        # Test updating non-existent amenity
        response = self.client.put('/amenities/nonexistent', json=update_data)
        self.assertEqual(response.status_code, 404)

        # Test invalid update data
        invalid_data = {
            'name': ''  # Empty name
        }
        response = self.client.put(f'/amenities/{amenity_id}', json=invalid_data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main() 