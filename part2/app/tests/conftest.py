import pytest
from app import create_app
from app.services.facade import HBnBFacade

@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def facade():
    """Create a test facade instance."""
    return HBnBFacade()

@pytest.fixture
def test_user(facade):
    """Create a test user."""
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com"
    }
    return facade.create_user(user_data)

@pytest.fixture
def test_place(facade, test_user):
    """Create a test place."""
    place_data = {
        "title": "Test Place",
        "description": "A test place",
        "price": 100.0,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner": test_user
    }
    return facade.create_place(place_data)

@pytest.fixture
def test_amenity(facade):
    """Create a test amenity."""
    amenity_data = {
        "name": "Test Amenity"
    }
    return facade.create_amenity(amenity_data) 