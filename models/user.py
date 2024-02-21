#!/usr/bin/python3
"""This module defines a class User"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.place import Place
from models.review import Review


class User(BaseModel):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    places = relationship(
        'Place',
        cascade="all, delete, delete-orphan",
        backref='user'
    )
    reviews = relationship(
        'Review',
        cascade="all, delete, delete-orphan",
        backref='user'
    )
