class InMemoryRepository:
    def __init__(self):
        self._objects = {}

    def add(self, obj):
        """Add an object to the repository"""
        self._objects[obj.id] = obj
        return obj

    def get(self, obj_id):
        """Get an object by ID"""
        return self._objects.get(obj_id)

    def get_all(self):
        """Get all objects"""
        return list(self._objects.values())

    def remove(self, obj_id):
        """Remove an object by ID"""
        if obj_id in self._objects:
            del self._objects[obj_id]
            return True
        return False 