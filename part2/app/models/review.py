from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self._text = None
        self._rating = None
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if not isinstance(value, str):
            raise ValueError("Review text must be a string")
        if not value.strip():
            raise ValueError("Review text cannot be empty")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        if not 1 <= value <= 5:
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value

    def to_dict(self):
        """Convert instance to dictionary with additional relationship data"""
        result = super().to_dict()
        result['place_id'] = self.place.id
        result['user_id'] = self.user.id
        return result 