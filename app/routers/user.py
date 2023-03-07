from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import engine, get_db

router = APIRouter(
    prefix='/users', #this will initiate all posts with /user endpoint
    tags=['Users'] #adds group to API's /docs
)

## USERS ------------------------------------------------------------------------------------

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
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

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    '''GET single user'''
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'user with id: {id} was not found')
    
    return user