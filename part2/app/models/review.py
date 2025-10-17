from app.models.basemodel import BaseModel as BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    @property
    def text(self):
        return self.text

    @text.setter
    def text(self, value):
        if not value:
            raise ValueError
        self.text = value

    @property
    def user_id(self):
        return self.user_id

    @user_id.setter
    def user_id(self, users, value):
        if self.user_id not in users:
            raise ValueError
        self.user_id = value

    @property
    def place_id(self):
        return self.place_id

    @place_id.setter
    def place_id(self, places, value):
        if self.place_id not in places:
            raise ValueError
        self.place_id = value
