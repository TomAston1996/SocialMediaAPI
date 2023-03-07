from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from . import models
from .routers import post, user, auth, vote
from .config import settings

#Run Live Server: uvicorn app.main:app --reload

##create the database (don't need when using alembic)
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# allowable domains that can talk to API - for a specific web app this would only allow a specific web domain.
#origins = ['https://www.google.com', 'https://youtube.com']
origins = ['*'] #allows all domains to talk to the API

# Allow cross origin resource sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #what domains are allowed to communicate with the API
    allow_credentials=True, 
    allow_methods=["*"], #allow only specific HTTP methods, all methods allowed for this API
    allow_headers=["*"], #allow on specific header, all headers allowed for this API
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "root"}


