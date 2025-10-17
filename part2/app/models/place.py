from app.models.basemodel import BaseModel as BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude,
                 owner_id):
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
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError
        self.__title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if type(value) is not float:
            raise TypeError("Price enter is not of type float")
        elif value < 0:
            raise ValueError("Price should be positive")
        self._price = value

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        if type(value) is not float:
            raise TypeError("Latitude must be a number")
        elif value > 90 or value < -90:
            raise ValueError("Latitude must be between 90 and -90")
        self.__latitude = value

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        if type(value) is not float:
            raise TypeError("Longitude must be a number")
        elif value > 180 or value < -180:
            raise ValueError("Longitude must be between 180 and -180")
        self.__longitude = value
