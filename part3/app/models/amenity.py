from app import db
from .base_model import BaseModel
from sqlalchemy.orm import validates

class Amenity(BaseModel):
    """Amenity model for storing place amenities."""
    __tablename__ = 'amenities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text)

    # Many-to-many relationship with places
    places = db.relationship('Place', secondary='place_amenities',
                           backref=db.backref('amenities', lazy='dynamic'))

    @validates('name')
    def validate_name(self, key, name):
        """Validate name field."""
        if not name or len(name.strip()) == 0:
            raise ValueError('Amenity name cannot be empty')
        return name.strip()

    def __init__(self, name, description=None):
        """Initialize a new amenity."""
        self.name = name
        self.description = description

    def to_dict(self):
        """Convert amenity instance to dictionary."""
        base_dict = super().to_dict()
        amenity_dict = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        base_dict.update(amenity_dict)
        return base_dict 