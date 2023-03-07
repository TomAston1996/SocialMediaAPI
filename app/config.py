from pydantic import BaseSettings

'''
This file stores all environment variables
Pydantic model checks all variables in the correct format

These can all be set on your local machine/server.
'''

class Settings(BaseSettings): 
    database_hostname: str
    database_port: str 
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config: 
        env_file ='.env' #this tells Pydantic to import environment variables from .env file as opposed to local machine

settings = Settings()
