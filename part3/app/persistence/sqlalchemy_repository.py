from app import db
from app.persistence.repository import Repository

class SQLAlchemyRepository(Repository):
    """SQLAlchemy-based implementation of the Repository interface."""
    
    def __init__(self, model):
        """Initialize the repository with a SQLAlchemy model.
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model

    def add(self, obj):
        """Add a new object to the database.
        
        Args:
            obj: Object to add
        """
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Get an object by ID.
        
        Args:
            obj_id: ID of the object to retrieve
            
        Returns:
            Object if found, None otherwise
        """
        return self.model.query.get(obj_id)

    def get_all(self):
        """Get all objects.
        
        Returns:
            List of all objects
        """
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object with new data.
        
        Args:
            obj_id: ID of the object to update
            data: Dictionary of attributes to update
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """Delete an object.
        
        Args:
            obj_id: ID of the object to delete
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by attribute value.
        
        Args:
            attr_name: Name of the attribute to filter by
            attr_value: Value to filter by
            
        Returns:
            Object if found, None otherwise
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first() 