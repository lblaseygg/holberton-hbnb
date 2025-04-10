from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self._name = None
        self.name = name
        self.places = []  # List to store places that have this amenity

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Amenity name must be a string")
        if len(value) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")
        if not value.strip():
            raise ValueError("Amenity name cannot be empty")
        self._name = value

    def add_place(self, place):
        """Add a place that has this amenity"""
        if place not in self.places:
            self.places.append(place) 