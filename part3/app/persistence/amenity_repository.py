from app.models.amenity import Amenity
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    """Repository for Amenity model with amenity-specific queries."""
    
    def __init__(self):
        super().__init__(Amenity)

    def get_by_name(self, name):
        """Get an amenity by name.
        
        Args:
            name: Name of the amenity
            
        Returns:
            Amenity object if found, None otherwise
        """
        return self.get_by_attribute('name', name)

    def search_by_name(self, search_term):
        """Search amenities by name (case-insensitive).
        
        Args:
            search_term: Term to search for in amenity names
            
        Returns:
            List of matching amenities
        """
        return self.model.query.filter(
            self.model.name.ilike(f'%{search_term}%')
        ).all() 