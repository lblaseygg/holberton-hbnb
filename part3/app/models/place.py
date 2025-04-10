from app import db
from .base_model import BaseModel
from sqlalchemy.orm import validates
from .place_amenity import place_amenity

class Place(BaseModel):
    """Place model for storing accommodation information."""
    __tablename__ = 'places'

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('places', lazy='dynamic'))
    reviews = db.relationship('Review', backref='place', lazy='dynamic', cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                              backref=db.backref('places', lazy=True))

    @validates('title')
    def validate_title(self, key, title):
        """Validate title field."""
        if not title or len(title.strip()) == 0:
            raise ValueError('Title cannot be empty')
        return title.strip()

    @validates('description')
    def validate_description(self, key, description):
        """Validate description field."""
        if not description or len(description.strip()) == 0:
            raise ValueError('Description cannot be empty')
        return description.strip()

    @validates('price')
    def validate_price(self, key, price):
        """Validate price field."""
        if price is None or price < 0:
            raise ValueError('Price must be a non-negative number')
        return price

    @validates('latitude')
    def validate_latitude(self, key, latitude):
        """Validate latitude field."""
        if latitude is None or not -90 <= latitude <= 90:
            raise ValueError('Latitude must be between -90 and 90')
        return latitude

    @validates('longitude')
    def validate_longitude(self, key, longitude):
        """Validate longitude field."""
        if longitude is None or not -180 <= longitude <= 180:
            raise ValueError('Longitude must be between -180 and 180')
        return longitude

    def to_dict(self):
        """Convert place instance to dictionary."""
        base_dict = super().to_dict()
        place_dict = {
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'user_id': self.user_id
        }
        base_dict.update(place_dict)
        return base_dict 