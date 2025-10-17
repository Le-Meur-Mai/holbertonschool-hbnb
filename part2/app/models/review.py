from app.models.basemodel import BaseModel as BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.__text = None
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not value:
            raise ValueError
        self.__text = value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        self.__rating = value