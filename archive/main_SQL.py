from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time


#Run Live Server: uvicorn app.main:app --reload

app = FastAPI()

class Post(BaseModel): 
    '''Post schema
    Required: title, content
    Optional: published, rating
    '''
    title: str
    content: str
    published: Optional[bool] = True #defaults to True


'''Connection to postgres SQL database
Connection Requirements: 
- Host: IP address of the database
- Database: Name of database to connect to
- User: Username
- Password: Password
- cursor_factory: Allows extraction of table column names
'''
while True:
    try: 
        conn = psycopg2.connect(
            host='localhost', 
            database='fastapi', 
            user='postgres', 
            password='password123', 
            cursor_factory=RealDictCursor
            )
        cursor = conn.cursor() #used to execute SQL statements
        print('Database connection was successful')
        break
    except Exception as error: 
        print(f'Database connection failed\nError: {error}')
        time.sleep(2)


my_posts = [
    {'title': 'post 1 title', 'content': 'post 1 content', 'id': 1},
    {'title': 'post 2 title', 'content': 'post 2 content', 'id': 2}
    ]


@app.get("/")
def root():
    return {"message": "root"}


@app.get("/posts")
def get_posts():
    '''GET all posts'''
    cursor.execute(''' SELECT * FROM posts ORDER BY id ASC ''') #note three commas
    posts = cursor.fetchall() #use fetchall() for multiple and fetchone() for singular
    
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    '''Create post'''
    cursor.execute(''' INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''', 
                   (post.title, post.content, post.published)) #use this format to avoid SQL injection attack
    new_post = cursor.fetchone()
    conn.commit()
    
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    '''GET single post'''
    cursor.execute(''' SELECT * FROM posts WHERE id = %s ''', (str(id),)) #keep comma after the str(id) due to issue with str conversion
    post = cursor.fetchone()

    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id: {id} was not found')
    
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, reponse: Response):
    '''DELETE post'''
    cursor.execute(''' DELETE FROM posts WHERE id = %s RETURNING * ''', (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id={id} was not found')
    
    return {'data': deleted_post}


@app.put('/posts/{id}')
def update_post(id: int, response: Response, post: Post):
    '''UPDATE post'''
    cursor.execute(''' UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * ''', 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f'post with id={id} was not found')

    return {'data': updated_post}
