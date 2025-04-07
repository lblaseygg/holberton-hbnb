from app.models import BaseModel

class Amenity(BaseModel):
    """Amenity class representing a feature or service available at a place."""
    
    def __init__(self, name):
        """
        Initialize a new Amenity instance.
        
        Args:
            name (str): The name of the amenity
        """
        super().__init__()
        self.name = name
        self.places = []  # List to store places that have this amenity

    @property
    def name(self):
        """Get the name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the name with validation."""
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value) > 50:
            raise ValueError("Name must be 50 characters or less")
        self._name = value

    def add_place(self, place):
        """Add a place that has this amenity."""
        self.places.append(place)

    def to_dict(self):
        """Return a dictionary representation of the Amenity."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
