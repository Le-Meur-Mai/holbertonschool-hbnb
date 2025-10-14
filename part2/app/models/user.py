from app.models.basemodel import BaseModel as BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = False
        self.reviews = []
        self.places = []

    def add_review(self, review):
        '''Add a review to the user'''
        self.reviews.append(review)

    def add_place(self, place):
        '''Add place to the user'''
        self.places.append(place)

