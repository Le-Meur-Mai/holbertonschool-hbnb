from app.models.basemodel import BaseModel as BaseModel


class Place(BaseModel):
    """Model representing a place or property.

    Inherits from BaseModel and adds location, pricing, ownership,
    reviews, and amenities attributes.

    Attributes:
        title (str): Title of the place.
        description (str): Description of the place.
        price (float): Price per night (must be positive).
        latitude (float): Latitude coordinate (-90 to 90).
        longitude (float): Longitude coordinate (-180 to 180).
        owner_id (str): ID of the user who owns the place.
        reviews (list): List of reviews associated with the place.
        amenities (list): List of amenities associated with the place.
    """

    def __init__(self, title, description, price, latitude, longitude,
                 owner_id):
        """Initialize a new Place instance with validation."""
        super().__init__()
        self.__title = None
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place.

        Args:
            review: A Review object to associate with this place.
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place.

        Args:
            amenity: An Amenity object to associate with this place.
        """
        self.amenities.append(amenity)

    @property
    def title(self):
        """str: Get the title of the place."""
        return self.__title

    @title.setter
    def title(self, value):
        """Set the title of the place.

        Args:
            value (str): The new title.

        Raises:
            ValueError: If the title is empty or None.
        """
        if not value:
            raise ValueError
        self.__title = value

    @property
    def price(self):
        """float: Get the price of the place."""
        return self._price

    @price.setter
    def price(self, value):
        """Set the price of the place.

        Args:
            value (float): The price per night.

        Raises:
            TypeError: If value is not a float.
            ValueError: If value is negative.
        """
        if type(value) is not float:
            raise TypeError("Price enter is not of type float")
        elif value < 0:
            raise ValueError("Price should be positive")
        self._price = value

    @property
    def latitude(self):
        """float: Get the latitude coordinate."""
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        """Set the latitude coordinate.

        Args:
            value (float): Latitude in degrees.

        Raises:
            TypeError: If value is not a float.
            ValueError: If value is not between -90 and 90.
        """
        if type(value) is not float:
            raise TypeError("Latitude must be a number")
        elif value > 90 or value < -90:
            raise ValueError("Latitude must be between 90 and -90")
        self.__latitude = value

    @property
    def longitude(self):
        """float: Get the longitude coordinate."""
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        """Set the longitude coordinate.

        Args:
            value (float): Longitude in degrees.

        Raises:
            TypeError: If value is not a float.
            ValueError: If value is not between -180 and 180.
        """
        if type(value) is not float:
            raise TypeError("Longitude must be a number")
        elif value > 180 or value < -180:
            raise ValueError("Longitude must be between 180 and -180")
        self.__longitude = value
