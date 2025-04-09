from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    """Repository for User model with user-specific queries."""
    
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        """Get a user by email.
        
        Args:
            email: Email address to search for
            
        Returns:
            User object if found, None otherwise
        """
        return self.get_by_attribute('email', email)

    def authenticate(self, email, password):
        """Authenticate a user by email and password.
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        user = self.get_by_email(email)
        if user and user.verify_password(password):
            return user
        return None 