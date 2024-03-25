#!/usr/bin/python3
"""DBStorage mode"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.amenity import Amenity
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None
    types = [User, State, City, Amenity, Place, Review]

    def __init__(self):
        """Initialize method"""
        self.__engine = create_engine('mysql://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')))
        if getenv('HBNB_MYSQL_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query all objs"""
        _dict = {}
        if cls is None:
            for typ in self.types:
                for obj in self.__session.query(typ).all():
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    _dict[key] = obj
        else:
            for obj in self.__session.query(cls):
                key = "{}.{}".format(cls.__class__.__name__, obj.id)
                _dict[key] = obj
        return _dict

    def new(self, obj):
        """adds an object"""
        self.__session.add(obj)

    def save(self):
        """commits changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes obj"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """creates all table in database and session"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
