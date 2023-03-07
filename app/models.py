from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .database import Base

'''
This file stores all database models
Models represent tables in the database

This script will create a database with the following schemas IF it is not already present in the database.
'''

class Post(Base):
    __tablename__ = 'posts' #define table name

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    #set up foreign key to 'id' in users table, 
    #CASCADE means if the user is deleted all posts from the user will also be deleted
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    #set up sqlalchemy relationship - this nothing to do with the database 
    owner = relationship('User') 


class User(Base): 
    __tablename__ = 'users' #define table name

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String)


class Vote(Base): 
    __tablename__ = 'votes' #define table name

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    
    