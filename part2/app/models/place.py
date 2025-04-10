from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self._title = None
        self._price = None
        self._latitude = None
        self._longitude = None
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store reviews
        self.amenities = []  # List to store amenities

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise ValueError("Title must be a string")
        if len(value) > 100:
            raise ValueError("Title must not exceed 100 characters")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value <= 0:
            raise ValueError("Price must be positive")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number")
        if not -90 <= float(value) <= 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number")
        if not -180 <= float(value) <= 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
        self._longitude = float(value)

    def add_review(self, review):
        """Add a review to the place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            amenity.add_place(self) 