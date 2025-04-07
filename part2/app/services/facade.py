from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get a user by email."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Get all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information."""
        user = self.get_user(user_id)
        if user:
            user.update(user_data)
            self.user_repo.update(user_id, user)
        return user

    def create_place(self, place_data):
        """Create a new place."""
        # Validate owner exists
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        # Handle amenities if provided
        amenities = []
        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity {amenity_id} not found")
                amenities.append(amenity)

        # Create place
        place = Place(owner=owner, **place_data)
        
        # Add amenities to place
        for amenity in amenities:
            place.add_amenity(amenity)
            amenity.add_place(place)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place's information."""
        place = self.get_place(place_id)
        if not place:
            return None

        # Handle amenities update if provided
        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            place.amenities.clear()
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity {amenity_id} not found")
                place.add_amenity(amenity)
                amenity.add_place(place)

        # Update other fields
        place.update(place_data)
        self.place_repo.update(place_id, place)
        return place

    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity's information."""
        amenity = self.get_amenity(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            self.amenity_repo.update(amenity_id, amenity)
        return amenity

    def create_review(self, review_data):
        """Create a new review."""
        # Validate user exists
        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        # Validate place exists
        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        # Create review
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )

        # Add review to user and place
        user.add_review(review)
        place.add_review(review)

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place."""
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        return place.reviews

    def update_review(self, review_id, review_data):
        """Update a review's information."""
        review = self.get_review(review_id)
        if not review:
            return None

        review.update(review_data)
        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        """Delete a review."""
        review = self.get_review(review_id)
        if not review:
            return False

        # Remove review from user and place
        review.user.reviews.remove(review)
        review.place.reviews.remove(review)
        
        self.review_repo.delete(review_id)
        return True 