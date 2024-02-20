#!/usr/bin/python3
"""Storage engine for mysql"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
import os


class DBStorage:
    """DB Storage class"""
    __engine = None
    __session = None
    """Initialize DBStorage"""
    self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(os.getenv('HBNB_MYSQL_USER'),
                                             os.getenv('HBNB_MYSQL_PWD'),
                                             os.getenv('HBNB_MYSQL_HOST', 'localhost'),
                                             os.getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
    if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def __session(self):
        """Create a session"""
        if self.__session is None:
            self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                          expire_on_commit=False))
        return self.__session()

    def all(self, cls=None):
        """Query on the current database session all objects"""
        all_objects = {}
        classes = ["User", "State", "City", "Amenity", "Place", "Review"]

        if cls is not None:
            classes = [cls.__name__]

        for class_name in classes:
            query_result = self.__session().query(eval(class_name)).all()
            for obj in query_result:
                key = "{}.{}".format(class_name, obj.id)
                all_objects[key] = obj

        return all_objects

    def new(self, obj):
        """Add the object to the current database session (self.__session)"""
        self.__session().add(obj)

    def save(self):
        """Commit all changes of the current database session (self.__session)"""
        self.__session().commit()

    def delete(self, obj=None):
        """Delete from the current database session (self.__session) if obj is not None"""
        if obj:
            self.__session().delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
