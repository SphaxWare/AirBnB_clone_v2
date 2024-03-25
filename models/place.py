#!/usr/bin/python3
""" holds class Place"""
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


envstorage = getenv("HBNB_TYPE_STORAGE")
if envstorage == "db":
    place_amenity = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True, nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """Representation of Place """
    if envstorage == "db":
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=False)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        reviews = relationship("Review", cascade="all,delete", backref="place")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """returns Cities instances of current state_id"""
            reviews = []
            objs = models.storage.all(models.review.Review)
            for key in objs:
                if objs[key].place_id == self.id:
                    cities.append(objs[key])
            return reviews

        @property
        def amenities(self):
            """returns Cities instances of current state_id"""
            amenities = []
            objs = models.storage.all(models.amenity.Amenity)
            for key in objs:
                if objs[key].place_id == self.id:
                    amenities.append(objs[key])
            return amenities

            def __init__(self, *args, **kwargs):
                """initializes Place"""
                super().__init__(*args, **kwargs)
