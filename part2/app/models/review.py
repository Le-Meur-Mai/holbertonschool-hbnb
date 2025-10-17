from app.models.basemodel import BaseModel as BaseModel


class Review(BaseModel):
    """Model representing a review made by a user for a place.

    Inherits from BaseModel and adds attributes for the review text,
    rating, associated user, and associated place.

    Attributes:
        text (str): The textual content of the review.
        rating (int): Rating given to the place (1–5).
        user_id (str): ID of the user who made the review.
        place_id (str): ID of the place being reviewed.
    """
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.__text = None
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    @property
    def text(self):
        """str: Get the text of the review."""
        return self.__text

    @text.setter
    def text(self, value):
        """Set the text of the review.

        Args:
            value (str): The textual content.

        Raises:
            ValueError: If the text is empty or None.
        """
        if not value:
            raise ValueError
        self.__text = value

    @property
    def rating(self):
        """Get the rating of the review."""
        return self.__rating

    @rating.setter
    def rating(self, value):
        """Set the rating of the review with validation.

        Args:
            value (int): The rating value to assign (must be an integer between 1 and 5).

        Raises:
            ValueError: If the value is not an integer or not in the range 1-5.
        """
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        self.__rating = value