from app import db
from app.models.basemodel import BaseModel as BaseModel


class Amenity(BaseModel):
    """Model representing an amenity (feature or service) available in a place.

    This class extends the BaseModel, inheriting common fields such as
    `id`, `created_at`, and `updated_at`.

    Attributes:
        name (str): The name of the amenity (e.g., "Wi-Fi", "Pool", "Parking").
    """
    __tablename__ = "amenities"
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        """Initialize a new Amenity instance.

        Args:
            name (str): The name of the amenity.

        Raises:
            ValueError: If the name is empty or None.
        """


        super().__init__()
        self.name = name

    def to_dict(self):
        """Return a serializable dict version."""
        return {
            "id": self.id,
            "name": self.name,
        }