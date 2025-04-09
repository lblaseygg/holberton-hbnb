from app.models.review import Review
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    """Repository for Review model with review-specific queries."""
    
    def __init__(self):
        super().__init__(Review)

    def get_by_rating_range(self, min_rating, max_rating):
        """Get reviews within a rating range.
        
        Args:
            min_rating: Minimum rating (1-5)
            max_rating: Maximum rating (1-5)
            
        Returns:
            List of reviews within the rating range
        """
        return self.model.query.filter(
            self.model.rating >= min_rating,
            self.model.rating <= max_rating
        ).all()

    def get_average_rating(self):
        """Get the average rating across all reviews.
        
        Returns:
            Average rating as a float
        """
        from sqlalchemy import func
        result = self.model.query.with_entities(
            func.avg(self.model.rating)
        ).scalar()
        return float(result) if result else 0.0 