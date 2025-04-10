class InMemoryRepository:
    def __init__(self):
        self._data = {}

    def add(self, entity):
        """Add an entity to the repository"""
        self._data[entity.id] = entity
        return entity

    def get(self, entity_id):
        """Get an entity by ID"""
        return self._data.get(entity_id)

    def get_all(self):
        """Get all entities"""
        return list(self._data.values())

    def get_by_attribute(self, attribute, value):
        """Get an entity by attribute value"""
        for entity in self._data.values():
            if hasattr(entity, attribute) and getattr(entity, attribute) == value:
                return entity
        return None

    def update(self, entity_id, data):
        """Update an entity"""
        entity = self.get(entity_id)
        if entity:
            for key, value in data.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            return entity
        return None 