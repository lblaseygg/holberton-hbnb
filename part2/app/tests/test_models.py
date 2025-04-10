from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_user_creation():
    """Test user creation and validation"""
    user = User(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com"
    )
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    print("✓ User creation test passed!")

def test_place_creation():
    """Test place creation and validation"""
    owner = User(
        first_name="Alice",
        last_name="Smith",
        email="alice.smith@example.com"
    )
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    assert place.title == "Cozy Apartment"
    assert place.price == 100.0
    assert place.latitude == 37.7749
    assert place.longitude == -122.4194
    assert place.owner == owner
    print("✓ Place creation test passed!")

def test_review_creation():
    """Test review creation and validation"""
    user = User(
        first_name="Bob",
        last_name="Johnson",
        email="bob.johnson@example.com"
    )
    place = Place(
        title="Beach House",
        description="Beautiful beachfront property",
        price=200,
        latitude=25.7617,
        longitude=-80.1918,
        owner=user
    )
    review = Review(
        text="Great stay! Loved the location.",
        rating=5,
        place=place,
        user=user
    )
    assert review.text == "Great stay! Loved the location."
    assert review.rating == 5
    assert review.place == place
    assert review.user == user
    print("✓ Review creation test passed!")

def test_amenity_creation():
    """Test amenity creation and validation"""
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("✓ Amenity creation test passed!")

def test_relationships():
    """Test relationships between entities"""
    # Create user and place
    owner = User(
        first_name="Charlie",
        last_name="Brown",
        email="charlie.brown@example.com"
    )
    place = Place(
        title="Mountain Cabin",
        description="Cozy cabin in the woods",
        price=150,
        latitude=39.5501,
        longitude=-105.7821,
        owner=owner
    )
    owner.add_place(place)

    # Create amenities
    wifi = Amenity(name="Wi-Fi")
    parking = Amenity(name="Parking")
    place.add_amenity(wifi)
    place.add_amenity(parking)

    # Create review
    reviewer = User(
        first_name="Lucy",
        last_name="Smith",
        email="lucy.smith@example.com"
    )
    review = Review(
        text="Amazing cabin!",
        rating=5,
        place=place,
        user=reviewer
    )
    place.add_review(review)
    reviewer.add_review(review)

    # Test relationships
    assert place in owner.places
    assert wifi in place.amenities
    assert parking in place.amenities
    assert place in wifi.places
    assert place in parking.places
    assert review in place.reviews
    assert review in reviewer.reviews
    print("✓ Relationship tests passed!")

if __name__ == "__main__":
    test_user_creation()
    test_place_creation()
    test_review_creation()
    test_amenity_creation()
    test_relationships()
    print("\nAll tests passed successfully!") 