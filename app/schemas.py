from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime


'''
Schemas define the request/response structure of our endpoints (this is not the database model)
'''

## USERS -----------------------------------------------------------------------------

class UserCreate(BaseModel): 
    '''UserCreate schema for creating users - REQUESTS'''
    email: EmailStr
    password: str


class UserOut(BaseModel): 
    '''UserOut schema for creating user - RESPONSE'''
    id: int
    email: EmailStr
    created_at: datetime

    class Config: 
        orm_mode=True

## POSTS -----------------------------------------------------------------------------

class PostBase(BaseModel):
    '''Post schema for REQUESTS'''
    title: str
    content: str
    published: Optional[bool] = True #defaults to True
    


class PostCreate(PostBase):
    '''Same as PostBase''' 
    pass


class Post(PostBase):
    ''' Post schema for RESPONSES'''
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut #return pydantic model UserOut - this is the sqlalchemy relationship set up


    class Config: 
        orm_mode = True

class PostOut(BaseModel): 
    Post: Post
    votes: int

    class Config: 
        orm_mode = True


## LOGIN -----------------------------------------------------------------------------

class UserLogin(BaseModel):
    '''UserLogin schema for loggin in - REQUEST''' 
    email: EmailStr
    password: str


## ACCESS TOKEN ---------------------------------------------------------------------

class Token(BaseModel):
    '''Schema for response with access token''' 
    access_token: str
    token_type: str

class TokenData(BaseModel): 
    id: Optional[str] = None


## Vote -----------------------------------------------------------------------------

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #Direction of the vote (either 0 or 1) - conint(less than or equal to 1)
