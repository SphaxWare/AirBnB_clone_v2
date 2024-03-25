 #!/usr/bin/python
""" holds class State"""
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """Representation of state """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""

        def __init__(self, *args, **kwargs):
            """initializes state"""
            super().__init__(*args, **kwargs)

    @property
    def cities(self):
        """returns Cities instances of current state_id"""
        cities = []
        objs = models.storage.all(models.city.City)
        for key in objs:
            if objs[key].state_id == self.id:
                cities.append(objs[key])
        return cities
