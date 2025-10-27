from abc import ABC, abstractmethod
from app import db  # Assuming you have set up SQLAlchemy in your Flask app
from app.models import User, Place, Review, Amenity  # Import your models


class Repository(ABC):
    """Abstract base class defining the interface for a repository.

    This repository pattern can be implemented for any storage type
    (e.g., in-memory, database) for managing entities.
    """

    @abstractmethod
    def add(self, obj):
        """Add a new object to the repository.

        Args:
            obj: The object to add.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its ID.

        Args:
            obj_id (str): Unique identifier of the object.

        Returns:
            The object if found, else None.
        """
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects from the repository.

        Returns:
            List of all objects.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object by its ID.

        Args:
            obj_id (str): Unique identifier of the object.
            data (dict): Dictionary of attributes to update.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by its ID.

        Args:
            obj_id (str): Unique identifier of the object to delete.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute value.

        Args:
            attr_name (str): Name of the attribute.
            attr_value: Value of the attribute to match.

        Returns:
            The first object matching the attribute, or None if not found.
        """
        pass


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()