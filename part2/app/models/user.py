import re
from app.models import BaseModel

class User(BaseModel):
    """User class representing a user in the HBnB application."""
    
    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a new User instance.
        
        Args:
            first_name (str): The user's first name
            last_name (str): The user's last name
            email (str): The user's email address
            is_admin (bool): Whether the user has admin privileges
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # List to store places owned by the user
        self.reviews = []  # List to store reviews written by the user

    @property
    def first_name(self):
        """Get the first name."""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """Set the first name with validation."""
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        if len(value) > 50:
            raise ValueError("First name must be 50 characters or less")
        self._first_name = value

    @property
    def last_name(self):
        """Get the last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Set the last name with validation."""
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        if len(value) > 50:
            raise ValueError("Last name must be 50 characters or less")
        self._last_name = value

    @property
    def email(self):
        """Get the email."""
        return self._email

    @email.setter
    def email(self, value):
        """Set the email with validation."""
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        self._email = value

    def add_place(self, place):
        """Add a place owned by the user."""
        self.places.append(place)

    def add_review(self, review):
        """Add a review written by the user."""
        self.reviews.append(review)

    def to_dict(self):
        """Return a dictionary representation of the User."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
