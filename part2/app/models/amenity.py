from app.models.basemodel import BaseModel as BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.__name = None
        self.name = name

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError
        self.__name = value
