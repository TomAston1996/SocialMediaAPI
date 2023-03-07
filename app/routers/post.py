from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix='/posts', #this will initiate all posts with /posts endpoint
    tags=['Posts'] #adds group to API's /docs
)


## POSTS ------------------------------------------------------------------------------------

# @router.get("/", 
#             response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, #this is a query parameter to limit the number of posts
              skip: int = 0, #this is a query parameter to skip 'x' amount of posts
              search: Optional[str] = '' #this is a search query parameter 
              ):
    '''
    GET all posts
    '''

    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results


@router.post("/", 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    '''
    Create post
    '''
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/{id}", 
            response_model=schemas.PostOut)
def get_post(id: int, 
             db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    '''
    GET single post
    '''

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')
    
    return post


@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    '''
    DELETE post
    '''
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    #check post exists
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id={id} was not found')
    
    #check the current user is deleteing their own post
    if post.owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='not authorized to perform requested action')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put('/{id}', 
            response_model=schemas.Post)
def update_post(id: int, response: Response, 
                updated_post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    '''
    UPDATE post
    '''
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id={id} was not found')
    
    #check the current user is updating their own post
    if post.owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='not authorized to perform requested action')
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()