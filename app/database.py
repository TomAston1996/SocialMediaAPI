from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

'''
This script is for connecting to the postgres database and defining the base model class
'''

#Format of database connection string for SQLAlchemy: 'postrgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Define base class
Base = declarative_base()

#Dependency - creates a session each time
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()