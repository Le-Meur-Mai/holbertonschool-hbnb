import uuid
from datetime import datetime


class BaseModel:
    """Base model providing common attributes and methods for all entities.

    Attributes:
        id (str): Unique identifier for the object (UUID4).
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of the last modification.
    """

    def __init__(self):
        """Initialize a new instance with a unique ID and timestamps."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the `updated_at` timestamp to the current time."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update object attributes based on a provided dictionary.

        Args:
            data (dict): A dictionary of attribute names and new values.

        Notes:
            - Only existing public attributes are updated.
            - Automatically updates the `updated_at` timestamp.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
