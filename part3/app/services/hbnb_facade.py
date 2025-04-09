from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository

class HBnBFacade:
    """Facade class for handling business logic operations."""
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    def create_user(self, user_data):
        """Create a new user.
        
        Args:
            user_data: Dictionary containing user information
            
        Returns:
            Created User object
        """
        user = User()
        for key, value in user_data.items():
            if key == 'password':
                user.hash_password(value)
            else:
                setattr(user, key, value)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get a user by ID.
        
        Args:
            user_id: ID of the user to retrieve
            
        Returns:
            User object if found, None otherwise
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get a user by email.
        
        Args:
            email: Email address to search for
            
        Returns:
            User object if found, None otherwise
        """
        return self.user_repo.get_by_email(email)

    def authenticate_user(self, email, password):
        """Authenticate a user.
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        return self.user_repo.authenticate(email, password)

    def update_user(self, user_id, user_data):
        """Update a user's information.
        
        Args:
            user_id: ID of the user to update
            user_data: Dictionary containing updated user information
            
        Returns:
            Updated User object
        """
        if 'password' in user_data:
            user = self.get_user(user_id)
            if user:
                user.hash_password(user_data['password'])
                del user_data['password']
        return self.user_repo.update(user_id, user_data)

    def delete_user(self, user_id):
        """Delete a user.
        
        Args:
            user_id: ID of the user to delete
        """
        self.user_repo.delete(user_id)

    def create_place(self, place_data):
        """Create a new place."""
        place = Place()
        for key, value in place_data.items():
            setattr(place, key, value)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get a place by ID."""
        return self.place_repo.get(place_id)

    def get_places_by_price_range(self, min_price, max_price):
        """Get places within a price range."""
        return self.place_repo.get_by_price_range(min_price, max_price)

    def get_places_by_location(self, latitude, longitude, radius):
        """Get places within a radius of a location."""
        return self.place_repo.get_by_location(latitude, longitude, radius)

    def update_place(self, place_id, place_data):
        """Update a place's information."""
        return self.place_repo.update(place_id, place_data)

    def delete_place(self, place_id):
        """Delete a place."""
        self.place_repo.delete(place_id)

    def create_review(self, review_data):
        """Create a new review."""
        review = Review()
        for key, value in review_data.items():
            setattr(review, key, value)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get a review by ID."""
        return self.review_repo.get(review_id)

    def get_reviews_by_rating_range(self, min_rating, max_rating):
        """Get reviews within a rating range."""
        return self.review_repo.get_by_rating_range(min_rating, max_rating)

    def get_average_rating(self):
        """Get the average rating across all reviews."""
        return self.review_repo.get_average_rating()

    def update_review(self, review_id, review_data):
        """Update a review's information."""
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review."""
        self.review_repo.delete(review_id)

    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity()
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_amenity_by_name(self, name):
        """Get an amenity by name."""
        return self.amenity_repo.get_by_name(name)

    def search_amenities(self, search_term):
        """Search amenities by name."""
        return self.amenity_repo.search_by_name(search_term)

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity's information."""
        return self.amenity_repo.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        """Delete an amenity."""
        self.amenity_repo.delete(amenity_id) 