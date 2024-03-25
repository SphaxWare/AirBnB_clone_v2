#!/usr/bin/python3
""" holds class City"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class City(BaseModel, Base):
    """Representation of city """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "cities"
        state_id = Column(String(60), ForeignKey("states.id"))
        name = Column(String(128), nullable=False)
        places = relationship('Place', cascade="all, delete", backref="cities")
    else:
        name = ""
        state_id = ""

        def __init__(self, *args, **kwargs):
            """initializes city"""
            super().__init__(*args, **kwargs)
