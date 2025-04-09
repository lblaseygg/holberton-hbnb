from app import db, bcrypt
from .base_model import BaseModel
from sqlalchemy.orm import validates

class User(BaseModel):
    """User model for storing user information."""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @validates('email')
    def validate_email(self, key, email):
        """Validate email format."""
        if not email or '@' not in email:
            raise ValueError('Invalid email format')
        return email

    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        """Validate name fields."""
        if not name or len(name.strip()) == 0:
            raise ValueError(f'{key} cannot be empty')
        return name.strip()

    def hash_password(self, password):
        """Hash the password before storing it."""
        if not password:
            raise ValueError('Password cannot be empty')
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convert user instance to dictionary."""
        base_dict = super().to_dict()
        user_dict = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
        base_dict.update(user_dict)
        return base_dict 