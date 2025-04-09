from app.models.place import Place
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place model with place-specific queries."""
    
    def __init__(self):
        super().__init__(Place)

    def get_by_price_range(self, min_price, max_price):
        """Get places within a price range.
        
        Args:
            min_price: Minimum price
            max_price: Maximum price
            
        Returns:
            List of places within the price range
        """
        return self.model.query.filter(
            self.model.price >= min_price,
            self.model.price <= max_price
        ).all()

    def get_by_location(self, latitude, longitude, radius):
        """Get places within a radius of a location.
        
        Args:
            latitude: Center latitude
            longitude: Center longitude
            radius: Search radius in kilometers
            
        Returns:
            List of places within the radius
        """
        # This is a simplified version. In a real application,
        # you would use PostGIS or a similar spatial extension
        return self.model.query.filter(
            self.model.latitude.between(latitude - radius, latitude + radius),
            self.model.longitude.between(longitude - radius, longitude + radius)
        ).all() 