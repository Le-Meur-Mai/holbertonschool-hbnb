from app.models.basemodel import BaseModel
from app import db


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
    __tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250))
    price = db.Column(db.Float, nullable=False, unique=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(128), nullable=False)

    def __init__(self, title, description, price, latitude, longitude,
                 owner_id):
        """Initialize a new Place instance with validation."""
        super().__init__()
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
