from app.models import BaseModel

class Review(BaseModel):
    """Review class representing a user's review of a place in the HBnB application."""
    
    def __init__(self, text, rating, place, user):
        """
        Initialize a new Review instance.
        
        Args:
            text (str): The content of the review
            rating (int): Rating given to the place (1-5)
            place (Place): The place being reviewed
            user (User): The user who wrote the review
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        """Get the review text."""
        return self._text

    @text.setter
    def text(self, value):
        """Set the review text with validation."""
        if not isinstance(value, str):
            raise TypeError("Review text must be a string")
        self._text = value

    @property
    def rating(self):
        """Get the rating."""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Set the rating with validation."""
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        if not 1 <= value <= 5:
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value

    @property
    def place(self):
        """Get the place."""
        return self._place

    @place.setter
    def place(self, value):
        """Set the place with validation."""
        from app.models.place import Place
        if not isinstance(value, Place):
            raise TypeError("Place must be a Place instance")
        self._place = value

    @property
    def user(self):
        """Get the user."""
        return self._user

    @user.setter
    def user(self, value):
        """Set the user with validation."""
        from app.models.user import User
        if not isinstance(value, User):
            raise TypeError("User must be a User instance")
        self._user = value

    def to_dict(self):
        """Return a dictionary representation of the Review."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id,
            'user_id': self.user.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
