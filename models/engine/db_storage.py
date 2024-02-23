#!/usr/bin/python3
"""Storage engine for mysql"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import os
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class DBStorage:
    """DB Storage class"""
    __engine = None
    __session = None
    """Initialize DBStorage"""
    def __init__(self):
        connection_string = 'mysql+mysqldb://{}:{}@{}/{}'.format(
            os.getenv('HBNB_MYSQL_USER'),
            os.getenv('HBNB_MYSQL_PWD'),
            os.getenv('HBNB_MYSQL_HOST', 'localhost'),
            os.getenv('HBNB_MYSQL_DB')
        )
        self.__engine = create_engine(connection_string, pool_pre_ping=True)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                        expire_on_commit=False))
        Base.metadata.create_all(self.__engine)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session all objects"""
        all_objects = {}
        classes = {
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }
        if cls is not None:
            class_instance = classes.get(cls)
        if class_instance is None:
            return
        classes = {cls: class_instance}

        for class_name, class_instance in classes.items():
            if class_instance:
                query_result = self.__session.query(class_instance).all()
                for obj in query_result:
                    key = "{}.{}".format(class_name, obj.id)
                    all_objects[key] = obj
        return all_objects

    def new(self, obj):
        """Add the object to the current database session)"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session if obj is not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                        expire_on_commit=False))
