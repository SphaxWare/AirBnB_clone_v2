#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    id = Column(String(60), primary_key=True, nullable=False)
    name = Column(String(128), nullable=False)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
            "City",
            back_populates="state",
            cascade="all, delete, delete-orphan",
        )
    if os.getenv('HBNB_TYPE_STORAGE') == 'file':
        @property
        def cities(self):
            """Getter attribute for cities in FileStorage"""
            city_list = []
            from models import storage
            for city_id, city in models.storage.all(City).items():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
