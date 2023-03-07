from passlib.context import CryptContext

'''
Utility file i.e. for hashing passwords
'''

#defining hashing algorithm (bcrypt) for passwords
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password: str) -> str:
    '''
    Function for hashing user passwords
    '''
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str):
    '''
    Function to verify plain login password against stored hashed password in the database
    '''
    return pwd_context.verify(plain_password, hashed_password)
 


