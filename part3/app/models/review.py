from app import db
from .base_model import BaseModel
from sqlalchemy.orm import validates

class Review(BaseModel):
    """Review model for storing user reviews."""
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    # Foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('reviews', lazy='dynamic'))

    @validates('text')
    def validate_text(self, key, text):
        """Validate text field."""
        if not text or len(text.strip()) == 0:
            raise ValueError('Review text cannot be empty')
        return text.strip()

    @validates('rating')
    def validate_rating(self, key, rating):
        """Validate rating field."""
        if rating is None or not 1 <= rating <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return rating

    def to_dict(self):
        """Convert review instance to dictionary."""
        base_dict = super().to_dict()
        review_dict = {
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id
        }
        base_dict.update(review_dict)
        return base_dict 