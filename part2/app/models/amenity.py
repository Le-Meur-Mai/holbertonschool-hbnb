from app.models.basemodel import BaseModel as BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
