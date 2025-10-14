from app.models.basemodel import BaseModel as BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.owner = user
        self.place = place
