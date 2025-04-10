from app.services.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repository = InMemoryRepository()
        self.amenity_repository = InMemoryRepository()
        self.place_repository = InMemoryRepository()
        self.review_repository = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user"""
        try:
            user = User(**user_data)
            self.user_repository.add(user)
            return user
        except (ValueError, KeyError):
            return None

    def get_user(self, user_id):
        """Get a user by ID"""
        return self.user_repository.get(user_id)

    def get_all_users(self):
        """Get all users"""
        return self.user_repository.get_all()

    def get_user_by_email(self, email):
        """Get a user by email"""
        users = self.user_repository.get_all()
        for user in users:
            if user.email == email:
                return user
        return None

    def update_user(self, user_id, user_data):
        """Update a user"""
        user = self.user_repository.get(user_id)
        if not user:
            return None

        try:
            for key, value in user_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            return user
        except (ValueError, KeyError):
            return None

    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        try:
            amenity = Amenity(name=amenity_data['name'])
            return self.amenity_repository.add(amenity)
        except (ValueError, KeyError) as e:
            return None

    def get_amenity(self, amenity_id):
        """Get an amenity by ID"""
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity"""
        try:
            # Get the existing amenity
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                return None

            # Create a copy of the current amenity data
            update_data = {
                'name': amenity_data.get('name', amenity.name)
            }

            # Validate the new data by creating a temporary amenity
            temp_amenity = Amenity(name=update_data['name'])

            # If validation passes, update the amenity
            return self.amenity_repository.update(amenity_id, update_data)
        except ValueError as e:
            return None

    def create_place(self, place_data):
        """Create a new place"""
        try:
            # Validate owner exists
            owner = self.user_repository.get(place_data.get('owner_id'))
            print(f"Owner lookup result: {owner}")  # Debug log
            if not owner:
                return None

            # Create place with positional arguments
            try:
                place = Place(
                    title=place_data['title'],
                    description=place_data.get('description', ''),
                    price=place_data['price'],
                    latitude=place_data['latitude'],
                    longitude=place_data['longitude'],
                    owner=owner
                )
                print(f"Place created successfully: {place}")  # Debug log
            except Exception as e:
                print(f"Error creating place: {str(e)}")  # Debug log
                return None

            # Add amenities if provided
            if 'amenities' in place_data:
                for amenity_id in place_data['amenities']:
                    amenity = self.amenity_repository.get(amenity_id)
                    if amenity:
                        place.amenities.append(amenity)

            self.place_repository.add(place)
            return place
        except (ValueError, KeyError) as e:
            print(f"Error in create_place: {str(e)}")  # Debug log
            return None

    def get_place(self, place_id):
        """Get a place by ID"""
        return self.place_repository.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        """Update a place"""
        place = self.place_repository.get(place_id)
        if not place:
            return None

        try:
            # Update basic attributes
            for key, value in place_data.items():
                if key != 'amenities' and hasattr(place, key):
                    setattr(place, key, value)

            # Update amenities if provided
            if 'amenities' in place_data:
                place.amenities = []
                for amenity_id in place_data['amenities']:
                    amenity = self.get_amenity(amenity_id)
                    if amenity:
                        place.amenities.append(amenity)

            return place
        except (ValueError, KeyError):
            return None

    def create_review(self, review_data):
        """Create a new review"""
        try:
            # Validate user and place exist
            user = self.user_repository.get(review_data.get('user_id'))
            place = self.place_repository.get(review_data.get('place_id'))
            if not user or not place:
                return None

            # Create review with user and place objects
            review_data['user'] = user
            review_data['place'] = place
            del review_data['user_id']  # Remove user_id as it's not needed anymore
            del review_data['place_id']  # Remove place_id as it's not needed anymore
            review = Review(**review_data)

            self.review_repository.add(review)
            return review
        except (ValueError, KeyError):
            return None

    def get_review(self, review_id):
        """Get a review by ID"""
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        place = self.get_place(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        """Update a review"""
        review = self.review_repository.get(review_id)
        if not review:
            return None

        try:
            for key, value in review_data.items():
                if hasattr(review, key):
                    setattr(review, key, value)
            return review
        except (ValueError, KeyError):
            return None

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repository.get(review_id)
        if not review:
            return False
        self.review_repository.remove(review_id)
        return True 