import re
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self._first_name = None
        self._last_name = None
        self._email = None
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # List to store places owned by the user
        self.reviews = []  # List to store reviews written by the user

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise ValueError("First name must be a string")
        if len(value) > 50:
            raise ValueError("First name must not exceed 50 characters")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise ValueError("Last name must be a string")
        if len(value) > 50:
            raise ValueError("Last name must not exceed 50 characters")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise ValueError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        self._email = value

    def add_place(self, place):
        """Add a place owned by the user"""
        self.places.append(place)

    def add_review(self, review):
        """Add a review written by the user"""
        self.reviews.append(review)

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value) 