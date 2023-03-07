from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from app.database import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, utils

#Run Live Server: uvicorn app.main:app --reload

#create the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "root"}

## POSTS ------------------------------------------------------------------------------------

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    '''GET all posts'''
    posts = db.query(models.Post).all()

    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    '''Create post'''
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    '''GET single post'''
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')
    
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    '''DELETE post'''
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id={id} was not found')
    post.delete(synchronize_session=False)
    db.commit()

    return {'data': post.first()}


@app.put('/posts/{id}', response_model=schemas.Post)
def update_post(id: int, response: Response, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    '''UPDATE post'''
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id={id} was not found')
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()


## USERS ------------------------------------------------------------------------------------

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    '''Create user'''
    #check to see if user already exists
    user_check = db.query(models.User).filter(models.User.email == user.email).first()
    if user_check: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f'user with email: {user.email} already exists')
    
    #hash password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    #Add user
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    '''GET single user'''
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'user with id: {id} was not found')
    
    return user