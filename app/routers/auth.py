from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)): 
     
    #OAuth2PasswordRequestForm will only return a 'username' and 'password' in a dict
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f'Invalid Credentials')
    
    plain_password = user_credentials.password #from login
    hashed_password = user.password #from database
    
    #verify the password
    if not utils.verify(plain_password, hashed_password): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f'Invalid Credentials')
    
    #create token
    access_token = oauth2.create_access_token(data = {'user_id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}




    

