from app.models.basemodel import BaseModel as BaseModel
# from email_validator import validate_email, EmailNotValidError

class User(BaseModel):
    def __init__(self, first_name, last_name, email):
        super().__init__()
        self.__first_name = None
        self.first_name = first_name
        self.__last_name = None
        self.last_name = last_name
        self.__email = None
        self.email = email
        self.is_admin = False
        self.reviews = []
        self.places = []

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not value:
            raise ValueError
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not value:
            raise ValueError
        self.__last_name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not value:
            raise ValueError
        
        try:
            valid = validate_email(value)
            self.__email = valid.email
        except EmailNotValidError:
            raise ValueError("Invalid email address format")

        self.__email = value

    def add_review(self, review):
        '''Add a review to the user'''
        self.reviews.append(review)

    def add_place(self, place):
        '''Add place to the user'''
        self.places.append(place)

