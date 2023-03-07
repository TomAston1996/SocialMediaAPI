from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas, database, models
from .config import settings

'''
This script is for token handling for authentication
'''

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

##Requirements for the token
# to get a secret key run: openssl rand -hex 32
#Secret keys will be stored as an environment variable in production on the local computer
SECRET_KEY = settings.secret_key #arbitary long string
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    '''
    Function to create an access token
    '''
    to_encode = data.copy() #make a copy of the data dictonary which contains the payload

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire}) #add expire time to payload

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #encode using payload, signature and algorithm

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    '''
    Function for verifying access tokens
    '''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id is None: 
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError: 
        raise credentials_exception
    
    return token_data
    
    
def get_current_user(token: str = Depends(oauth2_scheme), 
                     db: Session = Depends(database.get_db)): 
    '''
    Will automatically verify users in the path operations
    '''
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail = f'Could not validate credentials', 
                                          headers={'WWW-Authenticate': 'Bearer'})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user



