from app.models.basemodel import BaseModel as BaseModel


class Amenity(BaseModel):
    """Model representing an amenity (feature or service) available in a place.

    This class extends the BaseModel, inheriting common fields such as
    `id`, `created_at`, and `updated_at`.

    Attributes:
        name (str): The name of the amenity (e.g., "Wi-Fi", "Pool", "Parking").
    """

    def __init__(self, name):
        """Initialize a new Amenity instance.

        Args:
            name (str): The name of the amenity.

        Raises:
            ValueError: If the name is empty or None.
        """
        super().__init__()
        self.__name = None
        self.name = name

    @property
    def name(self):
        """str: Get the amenity's name."""
        return self.__name

    @name.setter
    def name(self, value):
        """Set the amenity's name.

        Args:
            value (str): The new name of the amenity.

        Raises:
            ValueError: If the name is empty or None.
        """
        if not value:
            raise ValueError
        self.__name = value
