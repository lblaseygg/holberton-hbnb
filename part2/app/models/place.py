from app.models import BaseModel

class Place(BaseModel):
    """Place class representing a rental property in the HBnB application."""
    
    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize a new Place instance.
        
        Args:
            title (str): The title of the place
            description (str): Description of the place
            price (float): Price per night
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            owner (User): The user who owns the place
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store reviews for this place
        self.amenities = []  # List to store amenities for this place

    @property
    def title(self):
        """Get the title."""
        return self._title

    @title.setter
    def title(self, value):
        """Set the title with validation."""
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if len(value) > 100:
            raise ValueError("Title must be 100 characters or less")
        self._title = value

    @property
    def description(self):
        """Get the description."""
        return self._description

    @description.setter
    def description(self, value):
        """Set the description with validation."""
        if value is not None and not isinstance(value, str):
            raise TypeError("Description must be a string")
        self._description = value

    @property
    def price(self):
        """Get the price."""
        return self._price

    @price.setter
    def price(self, value):
        """Set the price with validation."""
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value <= 0:
            raise ValueError("Price must be positive")
        self._price = float(value)

    @property
    def latitude(self):
        """Get the latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Set the latitude with validation."""
        if not isinstance(value, (int, float)):
            raise TypeError("Latitude must be a number")
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        """Get the longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Set the longitude with validation."""
        if not isinstance(value, (int, float)):
            raise TypeError("Longitude must be a number")
        if not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    @property
    def owner(self):
        """Get the owner."""
        return self._owner

    @owner.setter
    def owner(self, value):
        """Set the owner with validation."""
        from app.models.user import User
        if not isinstance(value, User):
            raise TypeError("Owner must be a User instance")
        self._owner = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self):
        """Return a dictionary representation of the Place."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
