import os
from sqlalchemy import create_engine
from models.base_model import Base

# Read environment variables
MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
MYSQL_DB = os.getenv('HBNB_MYSQL_DB')

# Construct the database URL
DB_URL = f'mysql://{MYSQL_USER}:{MYSQL_PWD}@{MYSQL_HOST}/{MYSQL_DB}'

# Create engine
engine = create_engine(DB_URL)

# Drop existing tables
Base.metadata.drop_all(engine)

# Create new tables
Base.metadata.create_all(engine)

# Close the engine connection
engine.dispose()
